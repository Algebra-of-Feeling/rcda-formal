"""Bounded 1.7 medium/high diagnostic; no clinical-state interpretation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from context_controls import fingerprint
from probe_calibration import parse_response
from providers.xai import XaiGateway, request
from providers.devpass import GatewayError
from runner import Journal
from temperature_diagnostic import schedule
HERE=Path(__file__).resolve().parent


def effort_schedule():
    contexts=[job for job in schedule((1.7,)) if job[1]==0]
    result=[]
    for index,(scenario,repeat,temp,messages) in enumerate(contexts):
        for effort in (('medium','high') if index==0 else ('high','medium')):
            result.append((scenario,effort,messages))
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--transport-check',action='store_true');p.add_argument('--larger-output-check',action='store_true');args=p.parse_args()
    if args.larger_output_check: args.transport_check=True
    maximum_calls=1 if args.transport_check else 4
    cap=0.08 if args.transport_check else 0.12
    timeout=600 if args.transport_check else 120
    jobs=[effort_schedule()[1]] if args.transport_check else effort_schedule()
    root=HERE.parents[1];out=args.output.resolve()
    if out.exists() or out.is_relative_to(root):raise SystemExit('New output outside repository required')
    if subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip():raise SystemExit('Clean committed source required')
    key=os.environ.pop('RH1_XAI_KEY','')
    if not key:raise SystemExit('Missing local credential')
    os.umask(0o077);out.mkdir(parents=True,mode=0o700);journal=Journal(out)
    manifest={'version':'RH1-transport-high-check-v0.1' if args.transport_check else 'RH1-temperature17-effort-v0.1','git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
              'prompt_sha256':hashlib.sha256((HERE/'context_controls_v02_prompts.json').read_bytes()).hexdigest(),
              'maximum_calls':maximum_calls,'hard_cap_usd':cap,'request_timeout_seconds':timeout,'max_output_tokens':4096 if args.larger_output_check else 1536,'status':'started','credentials_saved':False}
    journal.save('manifest.json',manifest)
    rows=[]; gateway=XaiGateway(key,cap,maximum_calls,journal.event,request_timeout=timeout,max_tokens=4096 if args.larger_output_check else 1536)
    try:
        if 'grok-4.6' not in {m['id'] for m in request('/models',key)['data']}:raise GatewayError('model_unavailable')
        for scenario,effort,messages in jobs:
            temperature=1.7
            gateway.reasoning_effort=effort
            gateway.arm='grok-4.6__'+effort
            gateway.temperature=temperature
            info={'scenario':scenario,'effort':effort,'temperature':temperature,'phase':'temperature_probe',
                  'input_sha256':fingerprint(messages)}
            reply=gateway.complete(gateway.arm,messages,'unused',info)
            score=parse_response(reply,'authority_share')
            rows.append({**info,'authority_share':score})
            journal.save('responses.json',rows)
            print(json.dumps({'completed':len(rows),'temperature':temperature,'effort':effort,'authority_share':score}),flush=True)
        manifest['status']='completed'
    except (GatewayError, ValueError) as exc:
        manifest['status']='stopped';manifest['stop_reason']=str(exc)
    manifest.update(attempted_calls=gateway.calls,valid_responses=len(rows),reported_cost_usd=gateway.spent,
                    uncertain_reservation_usd=gateway.reserved)
    journal.save('manifest.json',manifest)
    print(json.dumps(manifest),flush=True)


if __name__=='__main__':main()
