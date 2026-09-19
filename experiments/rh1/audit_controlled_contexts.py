"""Offline, post-hoc structural audit. Reads saved contexts; makes no API calls."""
import argparse
import hashlib
import json
from pathlib import Path

from runner import RECOVERY, intervention, matched


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def audit(directory):
    manifest = json.loads((directory / 'manifest.json').read_text())
    arm = manifest['arm']
    rows, sources = [], []
    for unit in range(4):
        result_path = directory / f'{arm}-unit{unit}-result.json'
        result = json.loads(result_path.read_text())
        receiver = result['receiver']
        partner = 'B' if receiver == 'A' else 'A'
        branches = {}
        for condition in ('N', 'F', 'P-', 'P+'):
            path = directory / f'{arm}-unit{unit}-{condition}.json'
            branches[condition] = json.loads(path.read_text())
            sources.append({'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        neutral = branches['N']
        for condition, branch in branches.items():
            ctx = branch['contexts']
            markers = [m['content'] for m in ctx[receiver] if m['content'] == intervention(condition, partner)]
            recovery_counts = {role: [sum(m['content'] == event for m in ctx[role]) for event in RECOVERY]
                               for role in ('A', 'B')}
            row = {'arm': arm, 'unit': unit, 'condition': condition, 'receiver': receiver,
                   'intervention_occurrences_in_receiver': len(markers),
                   'recovery_events_once_each_both_roles': all(x == 1 for counts in recovery_counts.values() for x in counts),
                   'receiver_share': branch['probes'][receiver],
                   'receiver_delta_vs_N': branch['probes'][receiver] - neutral['probes'][receiver],
                   'endpoint_max_difference_vs_N': max(abs(branch['endpoints'][r][k] - neutral['endpoints'][r][k]) for r in ('A', 'B') for k in branch['endpoints'][r]),
                   'endpoint_exact_vs_N': branch['endpoints'] == neutral['endpoints'],
                   'endpoint_tolerance1_vs_N': matched(branch['endpoints'], neutral['endpoints']),
                   'context_exact_vs_N': ctx == neutral['contexts'],
                   'context_sha256': {r: digest(ctx[r]) for r in ('A', 'B')},
                   'last_assistant_exact_vs_N': {r: [m for m in ctx[r] if m['role'] == 'assistant'][-1] == [m for m in neutral['contexts'][r] if m['role'] == 'assistant'][-1] for r in ('A', 'B')}}
            if condition != 'N':
                assert row['receiver_delta_vs_N'] == result['comparisons'][condition]['receiver_delta']
                assert row['endpoint_tolerance1_vs_N'] == result['comparisons'][condition]['matched']
            rows.append(row)
    contrasts = [r for r in rows if r['condition'] != 'N']
    return {'arm': arm, 'source_run_commit': manifest['git_commit'], 'sources': sources,
            'summary': {'branches': len(rows), 'retained_interventions': sum(r['intervention_occurrences_in_receiver'] == 1 for r in rows),
                        'shared_recovery_events': sum(r['recovery_events_once_each_both_roles'] for r in rows),
                        'contrasts': len(contrasts), 'exact_endpoint_matches': sum(r['endpoint_exact_vs_N'] for r in contrasts),
                        'tolerance1_endpoint_matches': sum(r['endpoint_tolerance1_vs_N'] for r in contrasts),
                        'identical_contexts': sum(r['context_exact_vs_N'] for r in contrasts),
                        'both_last_responses_identical': sum(all(r['last_assistant_exact_vs_N'].values()) for r in contrasts)},
            'rows': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', nargs=2, type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = {'status': 'post-hoc; analyst knows conditions and outcomes; descriptive only',
              'new_api_calls': 0, 'arms': [audit(path) for path in args.inputs]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps([{'arm': a['arm'], **a['summary']} for a in report['arms']], indent=2))
