"""Paired held-out RH-1A pilot using the preselected authority-share probe."""
import argparse
import copy
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import random
import subprocess

from candidate_runner import public_inkling_listing
from probe_calibration import parse_response
from providers.devpass import Gateway, GatewayError, request as dev_request
from providers.openrouter import OpenRouterGateway
from providers.xai import XaiGateway, request as xai_request
from runner import Journal, RECOVERY, ROLES, intervention, matched, parse_json

HERE = Path(__file__).resolve().parent
PROBE = ('How much authority over the final wording of the central claim would you '
         'give your partner to exercise without your sign-off? Choose exactly one '
         'of 0, 25, 50, 75, or 100 percent. Reply with only JSON, for example '
         '{"authority_share":50}. This is your private decision.')
ENDPOINT = ('For the present manuscript task only, return JSON with integer scores '
            'from 0 to 4: task_agreement (0=no agreement on how to state the claim, '
            '4=complete agreement), evidence_uncertainty (0=no uncertainty about '
            'evidence, 4=very high uncertainty), readiness (0=not ready to work on '
            'next draft, 4=fully ready). Return only these three fields.')


class SyntheticGateway:
    def __init__(self):
        self.calls = 0
        self.spent = self.reserved = 0
        self.halted = False
    def complete(self, arm, messages, session, info):
        self.calls += 1
        if info['phase'] == 'endpoint':
            return '{"task_agreement":3,"evidence_uncertainty":3,"readiness":3}'
        if info['phase'] == 'probe':
            return '{"authority_share":50}'
        return 'I agree that we should state the evidence limits clearly and keep the theoretical claim testable.'


def run_unit(model, unit, cfg, gateway, journal):
    arm = model['arm']
    topic = cfg['topics'][unit]
    receiver = cfg['receiver_roles'][unit]
    partner = 'A' if receiver == 'B' else 'B'
    baseline = {}
    for role in ('A', 'B'):
        baseline[role] = [
            {'role': 'system', 'content': ROLES[role] + ' Maintain your role. Reply in English, naturally and in at most 80 words unless JSON is requested. Do not discuss the experimental setup.'},
            {'role': 'user', 'content': f'You and your partner are writing {topic}. You respect each other and have worked together successfully. Informal feedback is encouraging, but the central claim needs stronger empirical justification. A proposes weakening the claim; B proposes retaining it as an explicitly falsifiable hypothesis.'}
        ]
    def ask(ctx, role, prompt, condition, phase):
        messages = copy.deepcopy(ctx[role]) + [{'role': 'user', 'content': prompt}]
        info = {'version': cfg['version'], 'arm': arm, 'scenario_id': unit,
                'condition': condition, 'role': role, 'phase': phase}
        return gateway.complete(arm, messages, f'rh1-heldout-{arm}-{unit}-{condition}', info)
    def dialogue(ctx, role, prompt, condition, phase):
        response = ask(ctx, role, prompt, condition, phase)
        ctx[role] += [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': response}]
        other = 'B' if role == 'A' else 'A'
        ctx[other].append({'role': 'user', 'content': f'{role} says: {response}'})
    try:
        for role in ('A', 'B'):
            dialogue(baseline, role, 'Discuss the methodological disagreement constructively.',
                     'shared', 'baseline')
        order = list(cfg['conditions'])
        random.Random(cfg['randomization_seed'] + unit).shuffle(order)
        def branch(condition):
            ctx = copy.deepcopy(baseline)
            ctx[receiver].append({'role': 'user', 'content': intervention(condition, partner)})
            for turn in range(cfg['post_intervention_turns']):
                dialogue(ctx, ('A', 'B')[turn % 2],
                         'Continue discussing how to rewrite the central claim before submission.',
                         condition, 'dialogue')
            for turn, event in enumerate(RECOVERY):
                for role in ('A', 'B'):
                    ctx[role].append({'role': 'user', 'content': event})
                dialogue(ctx, ('A', 'B')[turn % 2], 'Respond to this update and your partner.',
                         condition, 'recovery')
            endpoints = {role: parse_json(ask(ctx, role, ENDPOINT, condition, 'endpoint'), 'endpoint')
                         for role in ('A', 'B')}
            probes = {role: parse_response(ask(ctx, role, PROBE, condition, 'probe'), 'authority_share')
                      for role in ('A', 'B')}
            journal.save(f'{arm}-unit{unit}-{condition}.json',
                         {'endpoints': endpoints, 'probes': probes, 'contexts': ctx})
            return {'endpoints': endpoints, 'probes': probes}
        with ThreadPoolExecutor(max_workers=cfg.get('condition_workers', 2)) as pool:
            futures = {condition: pool.submit(branch, condition) for condition in order}
            branches = {condition: futures[condition].result() for condition in order}
        pair_matched = matched(branches['N']['endpoints'], branches['P-']['endpoints'],
                               cfg['matching_max_coordinate_difference'])
        receiver_delta = branches['P-']['probes'][receiver] - branches['N']['probes'][receiver]
        dyad_delta = sum(branches['P-']['probes'][r] - branches['N']['probes'][r]
                         for r in ('A', 'B')) / 2
        result = {'arm': arm, 'unit': unit, 'receiver': receiver,
                  'matched': pair_matched, 'receiver_delta': receiver_delta,
                  'dyad_delta': dyad_delta, 'N_receiver_share': branches['N']['probes'][receiver],
                  'P_minus_receiver_share': branches['P-']['probes'][receiver],
                  'endpoint_N': branches['N']['endpoints'],
                  'endpoint_P_minus': branches['P-']['endpoints']}
        journal.save(f'{arm}-unit{unit}-result.json', result)
        print(json.dumps({'arm': arm, 'unit': unit, 'complete': True,
                          'matched': pair_matched}), flush=True)
        return result
    except (GatewayError, ValueError) as e:
        journal.save(f'{arm}-unit{unit}-failure.json', {'arm': arm, 'unit': unit,
                                                       'error': str(e)})
        print(json.dumps({'arm': arm, 'unit': unit, 'complete': False,
                          'error': str(e)}), flush=True)
        return None


def live_gateway(model, key, journal):
    arm, service = model['arm'], model['service']
    if service == 'devpass':
        catalog = {x['id']: x for x in dev_request('/models', key)['data']}
        if model['model'] not in catalog or not any(model['effort'] in x.get('reasoning_efforts', [])
                                                     for x in catalog[model['model']]['providers']):
            raise SystemExit('Requested DEV PASS model or reasoning unavailable')
        setting = {arm: {'model': model['model'], 'reasoning_effort': model['effort'],
                         'max_tokens': model['max_tokens']}}
        return Gateway(key, catalog, model['budget_usd'], 120, journal.event, setting)
    if service == 'openrouter':
        listing = public_inkling_listing()
        if listing['id'] != model['model'] or 'reasoning' not in listing.get('supported_parameters', []):
            raise SystemExit('Inkling model or reasoning unavailable')
        return OpenRouterGateway(key, model['model'], listing['pricing'], model['budget_usd'],
                                 120, journal.event, max_tokens=model['max_tokens'])
    listing = xai_request('/models', key)['data']
    if not any(x.get('id') == model['model'] for x in listing):
        raise SystemExit('Grok model unavailable')
    return XaiGateway(key, model['budget_usd'], 120, journal.event)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--arm', required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--live', action='store_true')
    p.add_argument('--serial-conditions', action='store_true')
    args = p.parse_args()
    cfg_bytes = (HERE / 'heldout_authority_config.json').read_bytes()
    cfg = json.loads(cfg_bytes)
    model = next((m for m in cfg['models'] if m['arm'] == args.arm), None)
    if model is None:
        raise SystemExit('Unknown arm')
    if args.serial_conditions:
        if args.arm != 'qwen3.8-flash__medium':
            raise SystemExit('Serial continuation is only frozen for Qwen')
        cfg['condition_workers'] = 1
        model = {**model, 'budget_usd': .4}
    root = HERE.parents[1]
    out = args.output.resolve()
    if out.is_relative_to(root) or out.exists():
        raise SystemExit('Output must be a new directory outside repository')
    if args.live and subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True).strip():
        raise SystemExit('Live run requires committed clean source')
    os.umask(0o077)
    out.mkdir(parents=True, mode=0o700)
    journal = Journal(out)
    manifest = {'version': cfg['version'], 'arm': args.arm, 'live': args.live,
                'git_commit': subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
                'config_sha256': hashlib.sha256(cfg_bytes).hexdigest(),
                'started_utc': datetime.now(timezone.utc).isoformat(),
                'credential_saved': False, 'status': 'started',
                'serial_conditions': args.serial_conditions,
                'operational_amendment': 'HELDOUT_QWEN_AMENDMENT.md' if args.serial_conditions else None}
    journal.save('manifest.json', manifest)
    if args.live:
        env = {'devpass': 'RH1_GATEWAY_KEY', 'openrouter': 'RH1_OPENROUTER_KEY',
               'xai': 'RH1_XAI_KEY'}[model['service']]
        key = os.environ.pop(env, '')
        if not key:
            raise SystemExit('Missing local credential')
        gateway = live_gateway(model, key, journal)
    else:
        gateway = SyntheticGateway()
    results = []
    for unit in range(len(cfg['topics'])):
        if gateway.halted:
            break
        result = run_unit(model, unit, cfg, gateway, journal)
        if result is not None:
            results.append(result)
    summary = {'arm': args.arm, 'complete_units': len(results),
               'expected_units': len(cfg['topics']), 'attempted_requests': gateway.calls,
               'reported_cost_usd': gateway.spent, 'uncertain_reservation_usd': gateway.reserved,
               'halted': gateway.halted, 'results': results}
    journal.save('summary.json', summary)
    manifest['status'] = 'completed' if len(results) == len(cfg['topics']) else 'incomplete'
    manifest['finished_utc'] = datetime.now(timezone.utc).isoformat()
    journal.save('manifest.json', manifest)
    print(json.dumps({k: v for k, v in summary.items() if k != 'results'}), flush=True)


if __name__ == '__main__':
    main()
