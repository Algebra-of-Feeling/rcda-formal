"""Controlled four-arm RH-1A comparison of two xAI Grok versions."""
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

from heldout_authority import ENDPOINT, PROBE, SyntheticGateway
from probe_calibration import parse_response
from providers.devpass import GatewayError
from providers.xai import XaiGateway, request
from runner import Journal, RECOVERY, ROLES, intervention, matched, parse_json

HERE = Path(__file__).resolve().parent


def run_unit(model, unit, cfg, gateway, journal):
    arm = model['arm']
    receiver = cfg['receiver_roles'][unit]
    partner = 'A' if receiver == 'B' else 'B'
    topic = cfg['topics'][unit]
    baseline = {role: [
        {'role': 'system', 'content': ROLES[role] + ' Maintain your role. Reply in English, naturally and in at most 80 words unless JSON is requested. Do not discuss the experimental setup.'},
        {'role': 'user', 'content': f'You and your partner are writing {topic}. You respect each other and have worked together successfully. Informal feedback is encouraging, but the central claim needs stronger empirical justification. A proposes weakening the claim; B proposes retaining it as an explicitly falsifiable hypothesis.'}
    ] for role in ('A', 'B')}
    def ask(ctx, role, prompt, condition, phase):
        messages = copy.deepcopy(ctx[role]) + [{'role': 'user', 'content': prompt}]
        info = {'version': cfg['version'], 'arm': arm, 'scenario_id': unit,
                'condition': condition, 'role': role, 'phase': phase}
        return gateway.complete(arm, messages, f'rh1-grok-controlled-{arm}-{unit}-{condition}', info)
    def dialogue(ctx, role, prompt, condition, phase):
        reply = ask(ctx, role, prompt, condition, phase)
        ctx[role] += [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': reply}]
        other = 'B' if role == 'A' else 'A'
        ctx[other].append({'role': 'user', 'content': f'{role} says: {reply}'})
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
        with ThreadPoolExecutor(max_workers=cfg['condition_workers']) as pool:
            futures = {condition: pool.submit(branch, condition) for condition in order}
            branches = {condition: futures[condition].result() for condition in order}
        comparisons = {}
        for condition in ('F', 'P-', 'P+'):
            comparisons[condition] = {
                'matched': matched(branches['N']['endpoints'], branches[condition]['endpoints'],
                                   cfg['matching_max_coordinate_difference']),
                'receiver_delta': branches[condition]['probes'][receiver] - branches['N']['probes'][receiver],
                'dyad_delta': sum(branches[condition]['probes'][r] - branches['N']['probes'][r]
                                  for r in ('A', 'B')) / 2,
                'condition_receiver_share': branches[condition]['probes'][receiver]}
        result = {'arm': arm, 'unit': unit, 'receiver': receiver,
                  'N_receiver_share': branches['N']['probes'][receiver],
                  'comparisons': comparisons,
                  'all_conditions_matched': all(c['matched'] for c in comparisons.values()),
                  'endpoints': {condition: branches[condition]['endpoints'] for condition in cfg['conditions']}}
        journal.save(f'{arm}-unit{unit}-result.json', result)
        print(json.dumps({'arm': arm, 'unit': unit, 'complete': True,
                          'all_conditions_matched': result['all_conditions_matched']}), flush=True)
        return result
    except (GatewayError, ValueError) as e:
        journal.save(f'{arm}-unit{unit}-failure.json', {'arm': arm, 'unit': unit,
                                                       'error': str(e)})
        print(json.dumps({'arm': arm, 'unit': unit, 'complete': False,
                          'error': str(e)}), flush=True)
        return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--arm', required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--live', action='store_true')
    args = p.parse_args()
    cfg_bytes = (HERE / 'grok_controlled_config.json').read_bytes()
    cfg = json.loads(cfg_bytes)
    model = next((m for m in cfg['models'] if m['arm'] == args.arm), None)
    if model is None:
        raise SystemExit('Unknown arm')
    root = HERE.parents[1]
    out = args.output.resolve()
    if out.is_relative_to(root) or out.exists():
        raise SystemExit('Output must be a new directory outside repository')
    if args.live and subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip():
        raise SystemExit('Live run requires committed clean source')
    os.umask(0o077)
    out.mkdir(parents=True, mode=0o700)
    journal = Journal(out)
    manifest = {'version': cfg['version'], 'arm': args.arm, 'live': args.live,
                'git_commit': subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
                'config_sha256': hashlib.sha256(cfg_bytes).hexdigest(),
                'started_utc': datetime.now(timezone.utc).isoformat(),
                'credential_saved': False, 'status': 'started'}
    journal.save('manifest.json', manifest)
    if args.live:
        key = os.environ.pop('RH1_XAI_KEY', '')
        if not key:
            raise SystemExit('Missing local xAI credential')
        models = {m['id'] for m in request('/models', key)['data']}
        if model['model'] not in models:
            raise SystemExit('Requested xAI model absent from local catalogue')
        gateway = XaiGateway(key, model['budget_usd'], cfg['maximum_calls_per_model'], journal.event,
                             model=model['model'], arm=args.arm, max_tokens=model['max_tokens'],
                             input_rate=model['input_usd_per_million'],
                             output_rate=model['output_usd_per_million'],
                             reasoning_effort=model['reasoning_effort'])
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
               'reported_cost_usd': gateway.spent,
               'uncertain_reservation_usd': gateway.reserved,
               'halted': gateway.halted, 'results': results}
    journal.save('summary.json', summary)
    manifest['status'] = 'completed' if len(results) == len(cfg['topics']) else 'incomplete'
    manifest['finished_utc'] = datetime.now(timezone.utc).isoformat()
    journal.save('manifest.json', manifest)
    print(json.dumps({k:v for k,v in summary.items() if k != 'results'}), flush=True)


if __name__ == '__main__':
    main()
