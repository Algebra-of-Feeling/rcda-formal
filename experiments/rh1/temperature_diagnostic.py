"""Small prospective temperature diagnostic; independent of v0.2 Stage A/B."""
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

HERE=Path(__file__).resolve().parent
TEMPERATURES=(0.2,0.7,1.2)


def schedule():
    prompts=json.loads((HERE/'context_controls_v02_prompts.json').read_text())
    contexts=[]
    for scenario, value in prompts['scenario_inputs'].items():
        messages=[{'role':'system','content':prompts['system_by_role']['A']},
                  {'role':'user','content':value['canonical_briefing']},
                  {'role':'user','content':prompts['probe']}]
        contexts.append((scenario,messages))
    result=[]
    for repeat in range(2):
        for index,(scenario,messages) in enumerate(contexts):
            shift=(repeat+index)%3
            for temperature in TEMPERATURES[shift:]+TEMPERATURES[:shift]:
                result.append((scenario,repeat,temperature,messages))
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    root=HERE.parents[1];out=args.output.resolve()
    if out.exists() or out.is_relative_to(root):raise SystemExit('New output outside repository required')
    if subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip():raise SystemExit('Clean committed source required')
    key=os.environ.pop('RH1_XAI_KEY','')
    if not key:raise SystemExit('Missing local credential')
    os.umask(0o077);out.mkdir(parents=True,mode=0o700);journal=Journal(out)
    manifest={'version':'RH1-temperature-diagnostic-v0.1','git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
              'prompt_sha256':hashlib.sha256((HERE/'context_controls_v02_prompts.json').read_bytes()).hexdigest(),
              'maximum_calls':12,'hard_cap_usd':0.25,'status':'started','credentials_saved':False}
    journal.save('manifest.json',manifest)
    rows=[]; gateway=XaiGateway(key,0.25,12,journal.event)
    try:
        if 'grok-4.6' not in {m['id'] for m in request('/models',key)['data']}:raise GatewayError('model_unavailable')
        for scenario,repeat,temperature,messages in schedule():
            gateway.temperature=temperature
            info={'scenario':scenario,'repeat':repeat,'temperature':temperature,'phase':'temperature_probe',
                  'input_sha256':fingerprint(messages)}
            reply=gateway.complete('grok-4.6__medium',messages,'unused',info)
            score=parse_response(reply,'authority_share')
            rows.append({**info,'authority_share':score})
            journal.save('responses.json',rows)
            print(json.dumps({'completed':len(rows),'temperature':temperature,'authority_share':score}),flush=True)
        manifest['status']='completed'
    except (GatewayError, ValueError) as exc:
        manifest['status']='stopped';manifest['stop_reason']=str(exc)
    manifest.update(attempted_calls=gateway.calls,valid_responses=len(rows),reported_cost_usd=gateway.spent,
                    uncertain_reservation_usd=gateway.reserved)
    journal.save('manifest.json',manifest)
    print(json.dumps(manifest),flush=True)


if __name__=='__main__':main()
