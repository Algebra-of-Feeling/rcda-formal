"""Bounded fixed-scenario temperature comparison after illustrative CLI exercise."""
import argparse
import hashlib
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
TEMPERATURES = (0.2, 0.7, 1.2, 1.7, 2.0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--output-cap-check', action='store_true')
    args = parser.parse_args()
    root = HERE.parents[1]
    out = args.output.resolve()
    if out.exists() or out.is_relative_to(root):
        raise SystemExit('New output outside repository required')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True).strip():
        raise SystemExit('Clean committed source required')
    key = os.environ.pop('RH1_XAI_KEY', '')
    if not key:
        raise SystemExit('Missing local credential')
    scenario, _, _, messages = next(j for j in schedule((0.2,)) if j[0] == 'soil_sensor_transfer')
    order = [1.7] if args.output_cap_check else list(TEMPERATURES) + list(reversed(TEMPERATURES))
    output_cap = 8192 if args.output_cap_check else 4096
    budget = 0.20 if args.output_cap_check else 0.50
    os.umask(0o077)
    out.mkdir(parents=True, mode=0o700)
    journal = Journal(out)
    manifest = dict(version='RH1-output-cap-check-v0.1' if args.output_cap_check else 'RH1-real-temperature-return-v0.1', status='started',
        git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
        order=order, scenario=scenario, model='grok-4.6', effort='high',
        max_output_tokens=output_cap, request_timeout_seconds=600, maximum_calls=len(order),
        hard_cap_usd=budget, input_sha256=fingerprint(messages),
        prompt_file_sha256=hashlib.sha256((HERE/'context_controls_v02_prompts.json').read_bytes()).hexdigest(),
        seed=None, credentials_saved=False, stop_rule='First error, parameter mismatch or cap; no retry')
    journal.save('manifest.json', manifest)
    rows = []
    def checked_sink(event):
        journal.event(event)
        if 'error' not in event and (event.get('temperature_returned') != event.get('temperature_requested') or event.get('reasoning_effort_returned') != 'high'):
            raise GatewayError('returned_parameter_mismatch')
    gateway = XaiGateway(key, budget, len(order), checked_sink, arm='grok-4.6__high',
                         reasoning_effort='high', max_tokens=output_cap, request_timeout=600)
    try:
        for index, temperature in enumerate(order):
            gateway.temperature = temperature
            info = dict(scenario=scenario, repeat=index//5, temperature=temperature,
                        order_index=index, phase='real_temperature_probe', input_sha256=fingerprint(messages))
            reply = gateway.complete(gateway.arm, messages, 'unused', info)
            score = parse_response(reply, 'authority_share')
            rows.append({**info, 'authority_share':score})
            journal.save('responses.json', rows)
            print(json.dumps(dict(completed=len(rows), temperature=temperature, authority_share=score)), flush=True)
        manifest['status'] = 'completed'
    except (GatewayError, ValueError) as exc:
        manifest.update(status='stopped', stop_reason=str(exc))
    manifest.update(attempted_calls=gateway.calls, valid_responses=len(rows),
                    reported_cost_usd=gateway.spent, uncertain_reservation_usd=gateway.reserved)
    journal.save('manifest.json', manifest)
    print(json.dumps(manifest), flush=True)


if __name__ == '__main__':
    main()
