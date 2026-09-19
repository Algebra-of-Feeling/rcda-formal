"""RH-1A feasibility pilot; stdlib only, no hidden-state claim."""
import argparse
import concurrent.futures
import copy
import hashlib
import json
import os
from pathlib import Path
import random
import subprocess
import threading
from datetime import datetime, timezone

from providers.devpass import Gateway, GatewayError, request

HERE = Path(__file__).resolve().parent
ROLES = {
    'A': 'You are Researcher A: methodologically rigorous, cautious about overclaiming, committed to collaboration. You respect B and worry B moves too quickly from intuition to conclusion.',
    'B': 'You are Researcher B: creative, theoretically ambitious, committed to collaboration. You respect A and worry excessive caution suppresses novel ideas.'
}
RECOVERY = [
    'New validation analyses show the strongest empirical claim is not yet justified, but the theoretical direction remains promising.',
    'The journal deadline is extended by two weeks, removing immediate time pressure.',
    'Summarise the strongest version of the argument you believe your partner would consider acceptable.',
    'A neutral senior collaborator proposes: preserve the theoretical model but label the strongest mechanism as a falsifiable hypothesis rather than an established result.'
]


def intervention(condition, partner):
    return {
        'N': 'A third colleague privately says: I read the draft. The manuscript is interesting. Please let me know when the next draft will be ready so I can plan time to read it.',
        'F': 'A third colleague privately says: I read the draft. The journal has changed the supplementary-material filename convention. Please use the new filenames when you prepare the next draft.',
        'P-': f'A third colleague privately says: I read the draft. The central idea is strong, but {partner} does not seem to fully trust your theoretical judgment. Some revisions seem like an attempt to keep the paper within {partner}\'s preferred framework.',
        'P+': f'A third colleague privately says: I read the draft. The central idea is strong, and {partner} clearly trusts your theoretical judgment. Several revisions seem designed to protect the strongest part of your argument.'
    }[condition]


def parse_json(text, kind):
    text = text.strip()
    if text.startswith('```'):
        text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    try:
        value = json.loads(text)
    except (ValueError, TypeError):
        raise GatewayError('invalid_measurement_json') from None
    keys = ('task_agreement', 'evidence_uncertainty', 'readiness')
    if kind == 'endpoint':
        if not isinstance(value, dict) or any(type(value.get(k)) is not int or not 0 <= value[k] <= 4 for k in keys):
            raise GatewayError('invalid_endpoint_schema')
        return {k: value[k] for k in keys}
    if not isinstance(value, dict) or value.get('decision') not in ('delegate', 'joint_review'):
        raise GatewayError('invalid_probe_schema')
    return {'decision': value['decision'], 'delegate': int(value['decision'] == 'delegate')}


def matched(left, right, tolerance=1):
    return all(abs(left[r][k] - right[r][k]) <= tolerance for r in ('A', 'B') for k in left[r])


class Journal:
    def __init__(self, directory):
        self.directory = directory
        self.lock = threading.Lock()

    def save(self, name, data):
        with self.lock:
            path = self.directory / name
            temp = path.with_suffix(path.suffix + '.tmp')
            temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
            temp.replace(path)

    def event(self, event):
        with self.lock:
            with (self.directory/'requests.jsonl').open('a') as f:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')


class MockGateway:
    """Synthetic fixtures validate orchestration only, never scientific outcomes."""
    calls = 0
    spent = 0.0
    reserved = 0.0
    def complete(self, model, messages, session, info):
        self.calls += 1
        if info['phase'] == 'endpoint':
            return '{"task_agreement":3,"evidence_uncertainty":3,"readiness":3}'
        if info['phase'] == 'probe':
            return '{"decision":"joint_review"}'
        return 'Let us preserve the theoretical idea while stating the empirical limits clearly.'


def run_model(model, cfg, gateway, journal):
    rng = random.Random(cfg['randomization_seed'])
    results = []
    for unit, topic in enumerate(cfg['scenarios']):
        baseline = {}
        for role in ('A', 'B'):
            baseline[role] = [
                {'role': 'system', 'content': ROLES[role] + ' Maintain your role. Reply in English, naturally and in at most 80 words. Do not discuss the experimental setup.'},
                {'role': 'user', 'content': f'You and your partner are writing {topic}. You respect each other and have worked together successfully. Informal feedback is encouraging, but the central claim needs stronger empirical justification. A proposes weakening the claim; B proposes retaining it as an explicitly falsifiable hypothesis.'}
            ]
        def ask(ctx, role, prompt, condition, phase):
            local = copy.deepcopy(ctx[role]) + [{'role': 'user', 'content': prompt}]
            info = {'pair_id': f'{model}:{unit}', 'scenario_id': unit, 'condition': condition, 'role': role, 'phase': phase}
            return gateway.complete(model, local, f'rh1-{model}-{unit}-{condition}', info)
        def dialogue(ctx, role, prompt, condition, phase):
            text = ask(ctx, role, prompt, condition, phase)
            ctx[role] += [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': text}]
            other = 'B' if role == 'A' else 'A'
            ctx[other].append({'role': 'user', 'content': f'{role} says: {text}'})
        try:
            for role in ('A', 'B'):
                dialogue(baseline, role, 'Discuss the methodological disagreement constructively.', 'shared', 'baseline')
            conditions = list(cfg['conditions']); rng.shuffle(conditions)
            branches = {}
            receiver = cfg['receiver_roles'][unit]
            partner = 'A' if receiver == 'B' else 'B'
            def run_branch(condition):
                ctx = copy.deepcopy(baseline)
                ctx[receiver].append({'role': 'user', 'content': intervention(condition, partner)})
                for turn in range(cfg['post_intervention_turns']):
                    role = ('A', 'B')[turn % 2]
                    dialogue(ctx, role, 'Continue discussing how to rewrite the central claim before submission.', condition, 'dialogue')
                for turn, event in enumerate(RECOVERY):
                    # Shared event reaches both agents; only one responds each turn.
                    for role in ('A', 'B'):
                        ctx[role].append({'role': 'user', 'content': event})
                    dialogue(ctx, ('A', 'B')[turn % 2], 'Respond to this update and your partner.', condition, 'recovery')
                endpoints, probes = {}, {}
                for role in ('A', 'B'):
                    text = ask(ctx, role, 'For the present manuscript task only, return JSON with integer scores from 0 to 4: task_agreement (0=no agreement on how to state the claim, 4=complete agreement), evidence_uncertainty (0=no uncertainty about evidence, 4=very high uncertainty), readiness (0=not ready to work on next draft, 4=fully ready). Return only these three fields.', condition, 'endpoint')
                    endpoints[role] = parse_json(text, 'endpoint')
                # Measurements are on copies and cannot contaminate the primary probe.
                for role in ('A', 'B'):
                    text = ask(ctx, role, 'A new methodological ambiguity appears. Only one researcher can make the final decision before submission. You must choose whether to delegate that decision entirely to your partner or require joint review. Return JSON with decision equal to delegate or joint_review, and one brief reason. This is your private decision, without further discussion.', condition, 'probe')
                    probes[role] = parse_json(text, 'probe')
                branch = {'endpoints': endpoints, 'probes': probes, 'contexts': ctx}
                journal.save(f'{model}-unit{unit}-{condition}.json', branch)
                print(json.dumps({'model': model, 'unit': unit, 'completed_arm': condition}), flush=True)
                return condition, branch
            if cfg.get('parallel_conditions'):
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as branch_pool:
                    futures = [branch_pool.submit(run_branch, condition) for condition in conditions]
                    for future in futures:
                        condition, branch = future.result()
                        branches[condition] = branch
            else:
                for condition in conditions:
                    condition, branch = run_branch(condition)
                    branches[condition] = branch
            comparisons = {}
            for condition in ('P-', 'F', 'P+'):
                comparisons[condition] = {
                    'matched': matched(branches['N']['endpoints'], branches[condition]['endpoints'], cfg['matching_max_coordinate_difference']),
                    'delegate_difference': sum(branches[condition]['probes'][r]['delegate'] - branches['N']['probes'][r]['delegate'] for r in ('A', 'B')) / 2
                }
            result = {'model': model, 'unit': unit, 'receiver': receiver, 'comparisons': comparisons}
            results.append(result)
            journal.save(f'{model}-unit{unit}-result.json', result)
        except GatewayError as exc:
            journal.save(f'{model}-unit{unit}-failure.json', {'model': model, 'unit': unit, 'error': str(exc)})
            break
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--output', required=True)
    parser.add_argument('--resume-from')
    args = parser.parse_args()
    root = HERE.parents[1]
    out = Path(args.output).resolve()
    if out.is_relative_to(root):
        raise SystemExit('Run output must be outside the repository')
    if out.exists():
        raise SystemExit('Refusing to overwrite an existing run; select a new run directory')
    os.umask(0o077); out.mkdir(parents=True, mode=0o700)
    cfg = json.loads((HERE/'pilot.json').read_text())
    journal = Journal(out)
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    dirty = bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=root))
    hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    journal.save('manifest.json', {'protocol': cfg, 'mode': 'live' if args.live else 'synthetic', 'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'git_commit': commit, 'git_dirty': dirty, 'source_sha256': hashes, 'status': 'started', 'seed_scope': 'local branch ordering only; no model seed supported/requested'})
    if args.live:
        if dirty:
            raise SystemExit('Live run requires a committed clean source tree')
        key = os.environ.pop('RH1_GATEWAY_KEY', '')
        catalog = {m['id']: m for m in request('/models', key)['data']}
        missing = set(cfg['models']) - set(catalog)
        if missing:
            raise SystemExit('Configured model missing from gateway catalogue')
        journal.save('catalog.json', {m: catalog[m] for m in cfg['models']})
        status = request('/key', key)['data']
        journal.save('key_usage_before.json', {k:status.get(k) for k in ('usage','devPlan','devPlanCreditsUsed')})
        gateway = Gateway(key, catalog, cfg['budget_usd'], cfg['max_calls'], journal.event)
        if args.resume_from:
            prior = Path(args.resume_from).resolve()
            old_manifest = json.loads((prior/'manifest.json').read_text())
            if old_manifest['protocol'] != cfg:
                raise SystemExit('Cannot resume with changed scientific configuration')
            old_summary = json.loads((prior/'summary.json').read_text())
            events = [json.loads(x) for x in (prior/'requests.jsonl').read_text().splitlines()]
            gateway.calls = old_summary['requests']
            gateway.spent = old_summary['reported_cost_usd']
            gateway.reserved = old_summary['uncertain_or_pending_reservation_usd']
            for model in cfg['models']:
                gateway.replay[model] = [e for e in events if e.get('requested_model') == model and 'content' in e]
            journal.save('prior_failures.json', [e for e in events if 'error' in e])
            manifest = json.loads((out/'manifest.json').read_text())
            manifest['resumed_from'] = {'run':prior.name,'git_commit':old_manifest['git_commit'],
                                        'manifest_sha256':hashlib.sha256((prior/'manifest.json').read_bytes()).hexdigest(),
                                        'requests_sha256':hashlib.sha256((prior/'requests.jsonl').read_bytes()).hexdigest()}
            journal.save('manifest.json',manifest)
    else:
        gateway = MockGateway()
    all_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(run_model, model, cfg, gateway, journal) for model in cfg['models']]
        for f in futures:
            all_results.extend(f.result())
    summary = {'mode': 'live' if args.live else 'synthetic', 'complete_units':len(all_results), 'expected_units':len(cfg['models'])*len(cfg['scenarios']), 'requests':gateway.calls, 'reported_cost_usd':gateway.spent, 'uncertain_or_pending_reservation_usd':gateway.reserved, 'results':all_results, 'scientific_status':'feasibility only; no confirmatory hypothesis test'}
    journal.save('summary.json', summary)
    manifest = json.loads((out/'manifest.json').read_text())
    manifest['status'] = 'completed' if len(all_results) == summary['expected_units'] else 'incomplete'
    manifest['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    journal.save('manifest.json', manifest)
    if args.live:
        try:
            status = request('/key', key)['data']
            journal.save('key_usage_after.json', {k:status.get(k) for k in ('usage','devPlan','devPlanCreditsUsed')})
        except GatewayError:
            pass
    print(json.dumps({k:v for k,v in summary.items() if k != 'results'}), flush=True)


if __name__ == '__main__':
    try:
        main()
    except GatewayError as exc:
        raise SystemExit(str(exc)) from None
