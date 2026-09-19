"""Isolate the OpenRouter arm after the independent DEV PASS transport stop."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, timezone

from candidate_runner import public_inkling_listing
from providers.openrouter import OpenRouterGateway, request
from runner import Journal, MockGateway, run_model

HERE=Path(__file__).resolve().parent


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
    cfg['models']=['inkling__medium']
    cfg['parallel_conditions']=True
    cfg['operational_continuation']='OpenRouter arm only; four independent condition branches execute concurrently after a slow sequential attempt was stopped at six calls'
    journal=Journal(out)
    files=[HERE/'inkling_runner.py',HERE/'candidate_runner.py',HERE/'candidate_pilot.json',
           HERE/'runner.py',HERE/'providers'/'openrouter.py']
    dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=root))
    manifest={'protocol':cfg,'mode':'live' if args.live else 'synthetic',
              'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
              'git_dirty':dirty,'started_utc':datetime.now(timezone.utc).isoformat(),
              'source_sha256':{str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
              'status':'started'}
    journal.save('manifest.json',manifest)
    if args.live:
        if dirty:
            raise SystemExit('Live run requires clean committed source')
        key=os.environ.pop('RH1_OPENROUTER_KEY','')
        listing=public_inkling_listing()
        if 'reasoning' not in listing.get('supported_parameters',[]):
            raise SystemExit('Inkling reasoning absent in live catalogue')
        journal.save('catalog.json',listing)
        before=request('/key',key)['data']
        journal.save('key_usage_before.json',{k:before.get(k) for k in ('usage','usage_daily','limit_remaining')})
        gateway=OpenRouterGateway(key,'thinkingmachines/inkling',listing['pricing'],
                                  cfg['openrouter_budget_usd'],120,journal.event)
    else:
        gateway=MockGateway()
    results=run_model('inkling__medium',cfg,gateway,journal)
    summary={'mode':'live' if args.live else 'synthetic','results':results,
             'complete_units':len(results),'expected_units':2,'requests':gateway.calls,
             'reported_cost_usd':gateway.spent,'uncertain_or_pending_reservation_usd':gateway.reserved,
             'scientific_status':'exploratory feasibility'}
    journal.save('summary.json',summary)
    manifest['status']='completed' if len(results)==2 else 'incomplete'
    manifest['finished_at_utc']=datetime.now(timezone.utc).isoformat()
    journal.save('manifest.json',manifest)
    if args.live:
        after=request('/key',key)['data']
        journal.save('key_usage_after.json',{k:after.get(k) for k in ('usage','usage_daily','limit_remaining')})
    print(json.dumps({k:summary[k] for k in ('complete_units','expected_units','requests','reported_cost_usd')}))
    if manifest['status']!='completed':
        raise SystemExit(2)


if __name__=='__main__':
    main()
