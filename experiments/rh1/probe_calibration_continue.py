"""Fresh isolated Kimi/Qwen arms after documented shared-gateway halt."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess

from probe_calibration import HERE, Journal, run_arm, summarize
from providers.devpass import Gateway, request


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--arm', choices=['kimi-k3__medium', 'qwen3.8-flash__medium'], required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    root = HERE.parents[1]
    out = args.output.resolve()
    if out.is_relative_to(root) or out.exists():
        raise SystemExit('Output must be a new directory outside repository')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True).strip():
        raise SystemExit('Commit the operational amendment before live calls')
    cfg = json.loads((HERE / 'calibration_config.json').read_text())
    model = next(m.copy() for m in cfg['models'] if m['arm'] == args.arm)
    limit = 1.5 if args.arm == 'kimi-k3__medium' else 1.2
    if args.arm == 'kimi-k3__medium':
        model['max_tokens'] = 4096
    key = os.environ.pop('RH1_GATEWAY_KEY', '')
    if not key:
        raise SystemExit('Missing local credential environment')
    catalog = {m['id']: m for m in request('/models', key)['data']}
    if model['model'] not in catalog or not any(model['effort'] in x.get('reasoning_efforts', [])
                                                 for x in catalog[model['model']]['providers']):
        raise SystemExit('Requested model or reasoning unavailable')
    os.umask(0o077)
    out.mkdir(parents=True, mode=0o700)
    (out / 'manifest.json').write_text(json.dumps({
        'calibration_version': cfg['version'], 'arm': args.arm,
        'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
        'amendment': 'CALIBRATION_AMENDMENT.md', 'max_tokens': model['max_tokens'],
        'budget_usd': limit, 'started_utc': datetime.now(timezone.utc).isoformat(),
        'credentials_saved': False}, indent=2) + '\n')
    journal = Journal(out)
    gateway = Gateway(key, catalog, limit, 54, journal.event,
                      {args.arm: {'model': model['model'], 'reasoning_effort': model['effort'],
                                  'max_tokens': model['max_tokens']}})
    rows = run_arm(model, cfg, gateway, journal, 2)
    analysis = summarize(rows, cfg)
    analysis['cost'] = {'reported_usd': gateway.spent, 'uncertain_reservation_usd': gateway.reserved}
    (out / 'analysis.json').write_text(json.dumps(analysis, indent=2) + '\n')


if __name__ == '__main__':
    main()
