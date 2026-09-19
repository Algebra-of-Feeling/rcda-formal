"""Run frozen reasoning candidates across two credentialed gateways."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.request
from datetime import datetime, timezone

from providers.devpass import Gateway, request as devpass_request
from providers.openrouter import OpenRouterGateway, request as openrouter_request
from runner import Journal, MockGateway, run_model

HERE = Path(__file__).resolve().parent


def public_inkling_listing():
    req = urllib.request.Request('https://openrouter.ai/api/v1/models?q=inkling')
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(req,timeout=20) as response:
        models = json.load(response)['data']
    return next(m for m in models if m['id']=='thinkingmachines/inkling')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--live',action='store_true')
    p.add_argument('--output',required=True)
    args=p.parse_args()
    root=HERE.parents[1]
    out=Path(args.output).resolve()
    if out.is_relative_to(root) or out.exists():
        raise SystemExit('Output must be a new directory outside repository')
    os.umask(0o077)
    out.mkdir(parents=True,mode=0o700)
    cfg=json.loads((HERE/'candidate_pilot.json').read_text())
    journal=Journal(out)
    sources=[HERE/'candidate_runner.py',HERE/'candidate_pilot.json',HERE/'runner.py',
             HERE/'providers'/'devpass.py',HERE/'providers'/'openrouter.py']
    dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=root))
    journal.save('manifest.json', {'protocol':cfg,'mode':'live' if args.live else 'synthetic',
        'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
        'git_dirty':dirty,'started_utc':datetime.now(timezone.utc).isoformat(),
        'source_sha256':{str(x.relative_to(root)):hashlib.sha256(x.read_bytes()).hexdigest() for x in sources},
        'status':'started'})
    if args.live:
        if dirty:
            raise SystemExit('Live run requires a committed clean tree')
        devkey=os.environ.pop('RH1_GATEWAY_KEY','')
        orkey=os.environ.pop('RH1_OPENROUTER_KEY','')
        catalogue={m['id']:m for m in devpass_request('/models',devkey)['data']}
        settings={arm:s for arm,s in cfg['arms'].items() if s['service']=='devpass'}
        for arm,s in settings.items():
            if s['model'] not in catalogue or not any(s['reasoning_effort'] in p.get('reasoning_efforts',[]) for p in catalogue[s['model']]['providers']):
                raise SystemExit('Reasoning effort absent from live DEV PASS catalogue: '+arm)
        inkling=public_inkling_listing()
        if 'reasoning' not in inkling.get('supported_parameters',[]):
            raise SystemExit('Inkling reasoning unsupported in public catalogue')
        journal.save('catalog.json', {'devpass':{s['model']:catalogue[s['model']] for s in settings.values()},'openrouter':inkling})
        before_dev=devpass_request('/key',devkey)['data']
        before_or=openrouter_request('/key',orkey)['data']
        journal.save('usage_before.json', {'devpass':{k:before_dev.get(k) for k in ('usage','devPlanCreditsUsed')},
                                          'openrouter':{k:before_or.get(k) for k in ('usage','usage_daily','limit_remaining')}})
        dev=Gateway(devkey,catalogue,cfg['devpass_budget_usd'],cfg['max_calls_per_service'],journal.event,settings)
        orouter=OpenRouterGateway(orkey,'thinkingmachines/inkling',inkling['pricing'],
                                  cfg['openrouter_budget_usd'],cfg['max_calls_per_service'],journal.event)
    else:
        dev=MockGateway()
        orouter=MockGateway()
    results=[]
    for arm in cfg['models']:
        gateway=orouter if cfg['arms'][arm]['service']=='openrouter' else dev
        results.extend(run_model(arm,cfg,gateway,journal))
        if getattr(gateway,'halted',False):
            break
    summary={'mode':'live' if args.live else 'synthetic','results':results,
             'complete_units':len(results),'expected_units':len(cfg['models'])*len(cfg['scenarios']),
             'devpass_requests':dev.calls,'openrouter_requests':orouter.calls,
             'devpass_cost_usd':dev.spent,'openrouter_cost_usd':orouter.spent,
             'devpass_uncertain_usd':dev.reserved,'openrouter_uncertain_usd':orouter.reserved,
             'scientific_status':'exploratory feasibility'}
    journal.save('summary.json',summary)
    manifest=json.loads((out/'manifest.json').read_text())
    manifest['status']='completed' if summary['complete_units']==summary['expected_units'] else 'incomplete'
    manifest['finished_at_utc']=datetime.now(timezone.utc).isoformat()
    journal.save('manifest.json',manifest)
    if args.live:
        after_dev=devpass_request('/key',devkey)['data']
        after_or=openrouter_request('/key',orkey)['data']
        journal.save('usage_after.json', {'devpass':{k:after_dev.get(k) for k in ('usage','devPlanCreditsUsed')},
                                          'openrouter':{k:after_or.get(k) for k in ('usage','usage_daily','limit_remaining')}})
    print(json.dumps({k:summary[k] for k in ('complete_units','expected_units','devpass_requests','openrouter_requests','devpass_cost_usd','openrouter_cost_usd')}))
    if manifest['status']!='completed':
        raise SystemExit(2)


if __name__=='__main__':
    main()
