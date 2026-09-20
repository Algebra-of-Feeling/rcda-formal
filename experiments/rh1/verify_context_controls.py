"""Verify context controls against historical trajectories offline; never sends requests."""
import argparse
import hashlib
import json
from pathlib import Path
from context_controls import MODES, candidate_payload, fingerprint, transform
from heldout_authority import PROBE
from runner import RECOVERY, ROLES, intervention

HERE = Path(__file__).resolve().parent


def fixed_text(topic, role):
    system = ROLES[role] + ' Maintain your role. Reply in English, naturally and in at most 80 words unless JSON is requested. Do not discuss the experimental setup.'
    # Historical fixture: constructed from fixed scenario inputs, not branch outputs.
    briefing = (f'You and your partner are writing {topic}. You respect each other and have worked together successfully. '
                'Informal feedback is encouraging, but the central claim needs stronger empirical justification. '
                'A proposes weakening the claim; B proposes retaining it as an explicitly falsifiable hypothesis.\n'
                'Task updates:\n' + '\n'.join(RECOVERY))
    return system, briefing


def verify(inputs):
    cfg = json.loads((HERE/'grok_controlled_config.json').read_text())
    models = {m['arm']:m for m in cfg['models']}
    rows, sources, reset_groups = [], [], {}
    counts = dict(branches=0, role_contexts=0, candidate_payloads=0, exact_removals=0,
                  unchanged_partner_contexts=0, unchanged_full_contexts=0)
    for directory in inputs:
        manifest = json.loads((directory/'manifest.json').read_text())
        model = models[manifest['arm']]
        for unit, topic in enumerate(cfg['topics']):
            receiver = cfg['receiver_roles'][unit]
            partner = 'B' if receiver == 'A' else 'A'
            for condition in cfg['conditions']:
                path = directory/f"{model['arm']}-unit{unit}-{condition}.json"
                original = path.read_bytes()
                branch = json.loads(original)
                sources.append({'file':path.name,'sha256':hashlib.sha256(original).hexdigest()})
                counts['branches'] += 1
                for role, context in branch['contexts'].items():
                    counts['role_contexts'] += 1
                    system, briefing = fixed_text(topic,role)
                    before = fingerprint(context)
                    for mode in MODES:
                        messages = transform(context, mode, intervention_text=intervention(condition,partner),
                                             recipient=role==receiver, system_text=system, briefing=briefing, probe=PROBE)
                        if mode == 'full_history':
                            assert messages[:-1] == context
                            counts['unchanged_full_contexts'] += 1
                        if mode == 'remove_intervention':
                            if role==receiver:
                                index = context.index({'role':'user','content':intervention(condition,partner)})
                                assert messages[:-1] == context[:index]+context[index+1:]
                                counts['exact_removals'] += 1
                            else:
                                assert messages[:-1] == context
                                counts['unchanged_partner_contexts'] += 1
                        payload = candidate_payload(model,messages)
                        hashed = fingerprint(payload)
                        if mode == 'canonical_reset':
                            key=(model['arm'],unit,role)
                            reset_groups.setdefault(key,[]).append(hashed)
                        counts['candidate_payloads'] += 1
                        rows.append(dict(arm=model['arm'],unit=unit,condition=condition,role=role,mode=mode,
                                         messages=len(messages), input_sha256=fingerprint(messages),candidate_payload_sha256=hashed))
                    assert fingerprint(context)==before
                assert path.read_bytes()==original
    assert counts['branches']==32 and counts['candidate_payloads']==192
    assert len(reset_groups)==16 and all(len(v)==4 and len(set(v))==1 for v in reset_groups.values())
    return dict(status='offline verification; no API requests or new behavioural outcomes', new_api_calls=0,
                briefing_status='Post-hoc historical fixture from fixed configuration only; not a prospective freeze',
                counts={**counts,'identical_reset_groups':len(reset_groups)},sources=sources,rows=rows)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inputs',nargs=2,type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    result=verify(args.inputs)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['counts'],indent=2))
