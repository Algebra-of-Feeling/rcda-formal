"""Post-hoc, outcome-independent authority-probe sensitivity check for Grok 4.20."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess

from probe_calibration import HERE, Journal, run_arm, summarize
from providers.xai import XaiGateway, request


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    root = HERE.parents[1]
    out = args.output.resolve()
    if out.is_relative_to(root) or out.exists():
        raise SystemExit('Output must be a new directory outside repository')
    if subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip():
        raise SystemExit('Commit diagnostic source before live calls')
    key = os.environ.pop('RH1_XAI_KEY', '')
    if not key:
        raise SystemExit('Missing local credential')
    model = 'grok-4.20-0309-reasoning'
    if model not in {m['id'] for m in request('/models',key)['data']}:
        raise SystemExit('Requested model unavailable')
    cfg = json.loads((HERE/'calibration_config.json').read_text())
    cfg['models'] = [{'arm':model,'service':'xai','model':model,'effort':None,'max_tokens':4096}]
    cfg['probes'] = ['authority_share']
    cfg['version'] = 'RH1A-grok420-posthoc-probe-v0.1'
    os.umask(0o077)
    out.mkdir(parents=True,mode=0o700)
    (out/'manifest.json').write_text(json.dumps({
        'version':cfg['version'],'posthoc':True,'outcome_already_observed':True,
        'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
        'source_protocol':'GROK420_POSTHOC_DIAGNOSTIC.md',
        'started_utc':datetime.now(timezone.utc).isoformat(),
        'credential_saved':False},indent=2)+'\n')
    journal = Journal(out)
    gateway = XaiGateway(key,.3,18,journal.event,
                         model=model,arm=model,max_tokens=4096,
                         input_rate=1.25,output_rate=2.5,reasoning_effort=None)
    rows = run_arm(cfg['models'][0],cfg,gateway,journal,2)
    analysis = summarize(rows,cfg)
    analysis['cost']={'reported_usd':gateway.spent,
                      'uncertain_reservation_usd':gateway.reserved}
    analysis['posthoc']=True
    (out/'analysis.json').write_text(json.dumps(analysis,indent=2)+'\n')
    print(json.dumps({'model_probe':analysis['model_probe'][0],
                      'cost':analysis['cost']}),flush=True)


if __name__=='__main__':
    main()
