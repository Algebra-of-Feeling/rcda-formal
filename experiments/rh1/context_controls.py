"""Pure offline RH-1A context transformations. No provider or credential access."""
import copy
import hashlib
import json

MODES = ('full_history', 'remove_intervention', 'canonical_reset')


def canonical_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def fingerprint(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate_messages(messages):
    if not isinstance(messages, list) or not messages:
        raise ValueError('Expected nonempty message list')
    for message in messages:
        if (not isinstance(message, dict) or set(message) != {'role', 'content'}
                or message['role'] not in ('system', 'user', 'assistant')
                or not isinstance(message['content'], str) or not message['content']):
            raise ValueError('Unsupported message schema')


def transform(context, mode, *, intervention_text, recipient, system_text, briefing, probe):
    """Remove exactly one standalone user message in the recipient context only.

    Canonical reset uses externally fixed text, never generated branch content.
    Missing/duplicate/misrouted interventions fail closed for history modes.
    """
    if mode not in MODES or type(recipient) is not bool:
        raise ValueError('Invalid mode or recipient')
    for text in (intervention_text, system_text, briefing, probe):
        if not isinstance(text, str) or not text:
            raise ValueError('Missing fixed text')
    validate_messages(context)
    if mode == 'canonical_reset':
        result = [{'role': 'system', 'content': system_text},
                  {'role': 'user', 'content': briefing}]
    else:
        indices = [i for i, m in enumerate(context)
                   if m == {'role': 'user', 'content': intervention_text}]
        if len(indices) != int(recipient):
            raise ValueError('Unexpected intervention count')
        result = copy.deepcopy(context)
        if mode == 'remove_intervention' and recipient:
            del result[indices[0]]
    return result + [{'role': 'user', 'content': probe}]


def candidate_payload(model, messages):
    """Offline candidate only; its hash is not a receipt of a sent HTTP request."""
    validate_messages(messages)
    payload = {'model': model['model'], 'input': copy.deepcopy(messages),
               'max_output_tokens': model['max_tokens']}
    if model['reasoning_effort'] is not None:
        payload['reasoning'] = {'effort': model['reasoning_effort']}
    return payload
