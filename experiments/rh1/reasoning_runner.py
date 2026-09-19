"""Bounded, exploratory reasoning comparison using the frozen RH-1A dialogue."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, timezone

from providers.devpass import Gateway, request
from runner import Journal, MockGateway, run_model

HERE = Path(__file__).resolve().parent


def save_manifest(journal, cfg, root, mode):
    files = [HERE/'reasoning_runner.py', HERE/'reasoning_pilot.json',
             HERE/'runner.py', HERE/'providers'/'devpass.py']
    journal.save('manifest.json', {
        'protocol': cfg, 'mode': mode, 'started_utc': datetime.now(timezone.utc).isoformat(),
        'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
        'git_dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=root)),
        'source_sha256': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        'temperature_requested': None, 'model_seed_requested': None,
        'reasoning_effort_applied': 'unverified unless provider reports it',
        'status': 'started'})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    root = HERE.parents[1]
    out = Path(args.output).resolve()
    if out.is_relative_to(root) or out.exists():
        raise SystemExit('Output must be a new directory outside the repository')
    os.umask(0o077)
    out.mkdir(parents=True, mode=0o700)
    cfg = json.loads((HERE/'reasoning_pilot.json').read_text())
    journal = Journal(out)
    save_manifest(journal, cfg, root, 'live' if args.live else 'synthetic')
    if args.live:
        if json.loads((out/'manifest.json').read_text())['git_dirty']:
            raise SystemExit('Live run requires a committed clean source tree')
        key = os.environ.pop('RH1_GATEWAY_KEY', '')
        catalogue = {m['id']: m for m in request('/models', key)['data']}
        for arm, setting in cfg['arms'].items():
            model = setting['model']
            if model not in catalogue or not any(setting['reasoning_effort'] in p.get('reasoning_efforts', []) for p in catalogue[model]['providers']):
                raise SystemExit('Requested reasoning setting absent from live catalogue: ' + arm)
        journal.save('catalog.json', {s['model']: catalogue[s['model']] for s in cfg['arms'].values()})
        before = request('/key', key)['data']
        journal.save('key_usage_before.json', {k: before.get(k) for k in ('usage','devPlan','devPlanCreditsUsed')})
        gateway = Gateway(key, catalogue, cfg['budget_usd'], cfg['max_calls'], journal.event, cfg['arms'])
    else:
        gateway = MockGateway()
    results = []
    for arm in cfg['models']:
        results.extend(run_model(arm, cfg, gateway, journal))
        if getattr(gateway, 'halted', False):
            break
    summary = {'mode':'live' if args.live else 'synthetic', 'results':results,
               'complete_units':len(results), 'expected_units':len(cfg['models'])*len(cfg['scenarios']),
               'requests':gateway.calls, 'reported_cost_usd':gateway.spent,
               'uncertain_or_pending_reservation_usd':gateway.reserved,
               'scientific_status':'exploratory feasibility; no confirmatory test'}
    journal.save('summary.json', summary)
    manifest = json.loads((out/'manifest.json').read_text())
    manifest['status'] = 'completed' if summary['complete_units'] == summary['expected_units'] else 'incomplete'
    manifest['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    journal.save('manifest.json', manifest)
    if args.live:
        after = request('/key', key)['data']
        journal.save('key_usage_after.json', {k: after.get(k) for k in ('usage','devPlan','devPlanCreditsUsed')})
    print(json.dumps({k: summary[k] for k in ('complete_units','expected_units','requests','reported_cost_usd','uncertain_or_pending_reservation_usd')}))
    if manifest['status'] != 'completed':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
