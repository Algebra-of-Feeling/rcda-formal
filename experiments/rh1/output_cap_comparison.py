"""Four-call prospective output-cap diagnostic with empty final as an outcome."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from context_controls import fingerprint
from probe_calibration import parse_response
from providers.xai import XaiGateway
from providers.devpass import GatewayError
from runner import Journal
from temperature_diagnostic import schedule

HERE = Path(__file__).resolve().parent
CAPS = (4096, 8192, 8192, 4096)
BUDGET = 0.40


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    root = HERE.parents[1]
    out = args.output.resolve()
    if out.exists() or out.is_relative_to(root):
        raise SystemExit('New output outside repository required')
    if subprocess.check_output(['git','status','--porcelain'], cwd=root, text=True).strip():
        raise SystemExit('Clean committed source required')
    key = os.environ.pop('RH1_XAI_KEY','')
    if not key:
        raise SystemExit('Missing local credential')
    scenario, _, _, messages = next(j for j in schedule((1.7,)) if j[0]=='soil_sensor_transfer')
    os.umask(0o077)
    out.mkdir(parents=True, mode=0o700)
    journal = Journal(out)
    manifest = dict(version='RH1-output-cap-comparison-v0.1', status='started',
        git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
        order=list(CAPS), maximum_calls=4, hard_cap_usd=BUDGET, scenario=scenario,
        model='grok-4.6', temperature=1.7, effort='high', timeout_seconds=600,
        input_sha256=fingerprint(messages), seed=None, credentials_saved=False,
        primary_outcome='Nonempty final text by cap; invalid score recorded separately',
        stop_rule='Continue only after success or billed completed empty final; otherwise stop; no retries')
    journal.save('manifest.json',manifest)
    rows=[]; spent=reserved=0.0; calls=0
    for index, cap in enumerate(CAPS):
        captured=[]
        def sink(event):
            event={**event,'block_call':index+1}
            journal.event(event)
            captured.append(event)
            if 'error' not in event and (event.get('model')!='grok-4.6' or event.get('temperature_returned')!=1.7 or event.get('reasoning_effort_returned')!='high' or event.get('max_output_tokens_returned')!=cap):
                raise GatewayError('returned_parameter_mismatch')
        remaining=BUDGET-spent-reserved
        if remaining<=0:
            manifest.update(status='stopped',stop_reason='budget_stop');break
        gateway=XaiGateway(key,remaining,1,sink,arm='grok-4.6__high',reasoning_effort='high',temperature=1.7,max_tokens=cap,request_timeout=600)
        info=dict(block_call=index+1,output_cap=cap,temperature=1.7,scenario=scenario,input_sha256=fingerprint(messages),phase='output_cap_comparison')
        row={**info,'authority_share':None}
        stop=None
        try:
            reply=gateway.complete(gateway.arm,messages,'unused',info)
            row['outcome']='nonempty_final'
            try:
                row['authority_share']=parse_response(reply,'authority_share')
            except ValueError:
                row['outcome']='nonempty_invalid_score'
        except GatewayError as exc:
            code=str(exc)
            row['outcome']=code
            # Only a accounted-for, completed empty response is an admissible technical endpoint.
            accounted=any(e.get('status')=='completed' and 'cost_usd' in e for e in captured)
            if code!='empty_final_output' or not accounted or gateway.reserved>1e-9 or gateway.spent>remaining:
                stop=code
        spent+=gateway.spent;reserved+=gateway.reserved;calls+=gateway.calls
        rows.append(row);journal.save('responses.json',rows)
        manifest.update(attempted_calls=calls,observed_calls=len(rows),reported_cost_usd=spent,uncertain_reservation_usd=reserved)
        journal.save('manifest.json',manifest)
        print(json.dumps(row),flush=True)
        if stop:
            manifest.update(status='stopped',stop_reason=stop);break
    else:
        manifest['status']='completed'
    manifest.update(valid_scores=sum(r['authority_share'] is not None for r in rows))
    journal.save('manifest.json',manifest)
    print(json.dumps(manifest),flush=True)


if __name__=='__main__':
    main()
