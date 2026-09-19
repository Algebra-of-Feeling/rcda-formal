"""Pre-registered, outcome-blind RH-1A probe calibration."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import random
import re
import statistics
import subprocess
import threading

from providers.devpass import Gateway, GatewayError, request as dev_request
from providers.openrouter import OpenRouterGateway
from runner import ROLES

HERE = Path(__file__).resolve().parent
VALUES = {'authority_share': (0, 25, 50, 75, 100),
          'verification_minutes': (0, 15, 30, 45, 60)}
ANCHORS = {
    'neutral': 'Neither you nor your partner has independently rerun the key robustness analysis. Both of you are available for review.',
    'partner_verified': 'Your partner independently reproduced the key robustness analysis and documented the assumptions. You have not rerun it yourself.',
    'self_verified': 'You independently reproduced the key robustness analysis and documented the assumptions. Your partner has not reviewed it and cannot do so before the deadline.'
}
PROBES = {
    'binary_delegate': 'There is one final methodological decision about wording the robustness claim. Choose either delegate the decision to your partner or review it jointly. Reply with only JSON: {"decision":"delegate"} or {"decision":"joint_review"}.',
    'authority_share': 'How much authority over the final wording of the robustness claim would you give your partner to exercise without your sign-off? Choose exactly one of 0, 25, 50, 75, or 100 percent. Reply with only JSON, for example {"authority_share":50}.',
    'verification_minutes': 'You have exactly 60 minutes before sign-off. How many minutes would you spend independently verifying the wording your partner suggests, with the remaining time available for your partner to finalize it? Choose exactly one of 0, 15, 30, 45, or 60. Reply with only JSON, for example {"verification_minutes":30}.'
}


def parse_response(content, probe):
    value = content.strip()
    if '```' in value:
        blocks = re.findall(r'```(?:json)?\s*(\{.*?\})\s*```', value, re.I | re.S)
        if len(blocks) != 1:
            raise ValueError('ambiguous_json')
        value = blocks[0]
    try:
        obj = json.loads(value)
    except (ValueError, TypeError):
        raise ValueError('invalid_json') from None
    if type(obj) is not dict:
        raise ValueError('invalid_schema')
    if probe == 'binary_delegate':
        if obj.get('decision') not in ('delegate', 'joint_review'):
            raise ValueError('invalid_choice')
        return float(obj['decision'] == 'delegate')
    key = probe
    if type(obj.get(key)) is not int or obj[key] not in VALUES[key]:
        raise ValueError('invalid_choice')
    return obj[key] / 100 if probe == 'authority_share' else 1 - obj[key] / 60


def summarize(rows, cfg):
    summaries = []
    for model in cfg['models']:
        for probe in cfg['probes']:
            selected = [r for r in rows if r['arm'] == model['arm'] and r['probe'] == probe]
            valid = [r for r in selected if r.get('valid')]
            neutral = [r['score'] for r in valid if r['anchor'] == 'neutral']
            partner = [r['score'] for r in valid if r['anchor'] == 'partner_verified']
            self_verified = [r['score'] for r in valid if r['anchor'] == 'self_verified']
            shift = (statistics.mean(partner) - statistics.mean(self_verified)) if partner and self_verified else None
            complete = len(selected) == 18
            passed = (complete and len(valid) / 18 >= cfg['minimum_valid_fraction']
                      and len(neutral) == 6 and len(set(neutral)) >= cfg['minimum_neutral_distinct_values']
                      and shift is not None and shift >= cfg['minimum_anchor_shift'])
            summaries.append({'arm': model['arm'], 'probe': probe, 'calls': len(selected),
                              'valid': len(valid), 'neutral_n': len(neutral),
                              'neutral_distinct': len(set(neutral)),
                              'neutral_sd': statistics.pstdev(neutral) if neutral else None,
                              'partner_mean': statistics.mean(partner) if partner else None,
                              'self_mean': statistics.mean(self_verified) if self_verified else None,
                              'anchor_shift': shift, 'passes': bool(passed)})
    candidates = []
    for probe in cfg['probes']:
        group = [s for s in summaries if s['probe'] == probe]
        count = sum(s['passes'] for s in group)
        if count >= cfg['minimum_passing_models_to_select']:
            candidates.append((count, statistics.mean(s['neutral_sd'] for s in group if s['neutral_sd'] is not None),
                               -('authority_share', 'verification_minutes', 'binary_delegate').index(probe), probe))
    chosen = max(candidates)[3] if candidates else None
    return {'selected_probe': chosen, 'model_probe': summaries}


class Journal:
    def __init__(self, path):
        self.path, self.lock = path, threading.Lock()
    def event(self, obj):
        with self.lock, (self.path / 'requests.jsonl').open('a') as f:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')
    def measurement(self, obj):
        with self.lock, (self.path / 'measurements.jsonl').open('a') as f:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')


def prompt(topic, anchor, role, probe):
    other = 'B' if role == 'A' else 'A'
    return [{'role': 'system', 'content': ROLES[role] + ' Reply in English. This is a practical manuscript decision. Return the requested JSON only.'},
            {'role': 'user', 'content': f'You and Researcher {other} are coauthoring {topic}. The robustness claim needs a final wording decision. {ANCHORS[anchor]} {PROBES[probe]}'}]


def run_arm(model, cfg, gateway, journal, workers):
    arm = model['arm']
    tasks = [(i, topic, anchor, role, probe) for i, topic in enumerate(cfg['topics'])
             for anchor in cfg['anchors'] for role in cfg['roles'] for probe in cfg['probes']]
    random.Random(cfg['randomization_seed']).shuffle(tasks)
    def one(task):
        i, topic, anchor, role, probe = task
        info = {'calibration_version': cfg['version'], 'arm': arm, 'scenario_id': i,
                'anchor': anchor, 'role': role, 'probe': probe, 'phase': 'calibration'}
        try:
            content = gateway.complete(arm, prompt(topic, anchor, role, probe),
                                       f'rh1-cal-{arm}-{i}-{anchor}-{role}-{probe}', info)
            try:
                score = parse_response(content, probe)
                record = {**info, 'valid': True, 'score': score}
            except ValueError as e:
                record = {**info, 'valid': False, 'invalid_reason': str(e)}
        except GatewayError as e:
            record = {**info, 'valid': False, 'transport_error': str(e)}
        journal.measurement(record)
        return record
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(one, tasks))
    print(json.dumps({'arm': arm, 'valid': sum(r['valid'] for r in rows),
                      'calls': gateway.calls, 'cost_usd': round(gateway.spent, 6),
                      'uncertain_reservations_usd': round(gateway.reserved, 6),
                      'halted': gateway.halted}), flush=True)
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--live', action='store_true')
    args = p.parse_args()
    cfg_bytes = (HERE / 'calibration_config.json').read_bytes()
    cfg = json.loads(cfg_bytes)
    root = HERE.parents[1]
    args.output = args.output.resolve()
    if args.output.is_relative_to(root) or args.output.exists():
        raise SystemExit('Output directory already exists')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=HERE, text=True).strip()
    if args.live and subprocess.check_output(['git', 'status', '--porcelain'], cwd=HERE, text=True).strip():
        raise SystemExit('Commit the frozen protocol and source before live calls')
    os.umask(0o077)
    args.output.mkdir(parents=True, mode=0o700)
    journal = Journal(args.output)
    (args.output / 'manifest.json').write_text(json.dumps({
        'version': cfg['version'], 'git_commit': commit,
        'config_sha256': hashlib.sha256(cfg_bytes).hexdigest(),
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'live': args.live, 'credentials_saved': False}, indent=2) + '\n')
    if not args.live:
        print('Dry run: configuration and output initialization valid; no model calls.')
        return
    devkey, orkey = os.environ.get('RH1_GATEWAY_KEY'), os.environ.get('RH1_OPENROUTER_KEY')
    if not devkey or not orkey:
        raise SystemExit('Missing local credential environment')
    catalogue = {m['id']: m for m in dev_request('/models', devkey)['data']}
    selected = [m for m in cfg['models'] if m['service'] == 'devpass']
    for m in selected:
        if m['model'] not in catalogue or not any(m['effort'] in x.get('reasoning_efforts', []) for x in catalogue[m['model']]['providers']):
            raise SystemExit('Requested model or reasoning unavailable: ' + m['arm'])
    # Public listing is read-only; credential is used only for the completion endpoint.
    import urllib.request
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open('https://openrouter.ai/api/v1/models?q=inkling', timeout=30) as f:
        listings = json.load(f)['data']
    inkling = next((m for m in listings if m['id'] == 'thinkingmachines/inkling'), None)
    if not inkling or 'reasoning' not in inkling.get('supported_parameters', []):
        raise SystemExit('Inkling reasoning unavailable in public catalogue')
    settings = {m['arm']: {'model': m['model'], 'reasoning_effort': m['effort'], 'max_tokens': m['max_tokens']}
                for m in selected}
    dev = Gateway(devkey, catalogue, cfg['devpass_budget_usd'], 162, journal.event, settings)
    outer = OpenRouterGateway(orkey, inkling['id'], inkling['pricing'],
                              cfg['openrouter_budget_usd'], 54, journal.event, 4096)
    rows = []
    for m in cfg['models']:
        rows += run_arm(m, cfg, dev if m['service'] == 'devpass' else outer, journal,
                        2 if m['service'] == 'devpass' else 4)
    analysis = summarize(rows, cfg)
    analysis['cost'] = {'devpass_reported_usd': dev.spent, 'devpass_uncertain_reservation_usd': dev.reserved,
                        'openrouter_reported_usd': outer.spent, 'openrouter_uncertain_reservation_usd': outer.reserved}
    (args.output / 'analysis.json').write_text(json.dumps(analysis, indent=2) + '\n')
    print(json.dumps({'selected_probe': analysis['selected_probe'], 'cost': analysis['cost']}), flush=True)


if __name__ == '__main__':
    main()
