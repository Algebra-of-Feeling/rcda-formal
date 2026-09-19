"""Run the user-requested supplementary Grok arm without changing selection."""
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
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True).strip():
        raise SystemExit('Commit Grok extension before live calls')
    key = os.environ.pop('RH1_XAI_KEY', '')
    if not key:
        raise SystemExit('Missing local credential environment')
    listing = request('/models', key)['data']
    if not any(m.get('id') == 'grok-4.6' for m in listing):
        raise SystemExit('Grok 4.6 unavailable to local key')
    cfg = json.loads((HERE / 'calibration_config.json').read_text())
    model = {'arm': 'grok-4.6__medium', 'service': 'xai', 'model': 'grok-4.6',
             'effort': 'medium', 'max_tokens': 1536}
    os.umask(0o077)
    out.mkdir(parents=True, mode=0o700)
    (out / 'manifest.json').write_text(json.dumps({
        'calibration_version': cfg['version'], 'arm': model['arm'],
        'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
        'extension': 'GROK_EXTENSION_FREEZE.md', 'max_tokens': 1536,
        'budget_usd': 1.5, 'started_utc': datetime.now(timezone.utc).isoformat(),
        'credentials_saved': False}, indent=2) + '\n')
    journal = Journal(out)
    gateway = XaiGateway(key, 1.5, 54, journal.event)
    rows = run_arm(model, cfg, gateway, journal, 2)
    expanded = dict(cfg)
    expanded['models'] = cfg['models'] + [model]
    analysis = summarize(rows, expanded)
    analysis['cost'] = {'reported_usd': gateway.spent,
                        'uncertain_reservation_usd': gateway.reserved}
    (out / 'analysis.json').write_text(json.dumps(analysis, indent=2) + '\n')


if __name__ == '__main__':
    main()
