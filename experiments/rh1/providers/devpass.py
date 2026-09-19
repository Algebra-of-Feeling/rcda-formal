"""Minimal audited transport. No SDK logs, redirects, tools or secret persistence."""
import json
import math
import os
import threading
import urllib.error
import urllib.request
from datetime import datetime, timezone

BASE = 'https://api.llmgateway.io/v1'


class GatewayError(RuntimeError):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(path, key, payload=None, session=None):
    if path not in ('/key', '/models', '/chat/completions'):
        raise GatewayError('endpoint_not_allowed')
    headers = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}
    if session:
        headers['X-Session-Id'] = session
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=body, headers=headers)
    try:
        # Disable environment proxies and redirects: credential only goes to BASE.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
        with opener.open(req, timeout=60) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise GatewayError('http_' + str(exc.code)) from None
    except Exception:
        raise GatewayError('transport_or_json_failure') from None


class Gateway:
    def __init__(self, key, catalog, limit, max_calls, sink):
        if not key:
            raise GatewayError('missing_local_credential')
        if not 0 < limit <= 10:
            raise GatewayError('budget_outside_authorization')
        self.key, self.catalog, self.limit = key, catalog, limit
        self.max_calls, self.sink = max_calls, sink
        self.lock = threading.Lock()
        self.spent = self.reserved = 0.0
        self.calls = 0
        self.halted = False

    def reserve(self, amount):
        with self.lock:
            if self.halted or self.calls >= self.max_calls or self.spent + self.reserved + amount > self.limit:
                raise GatewayError('budget_or_call_stop')
            self.calls += 1
            self.reserved += amount
            return self.calls

    def complete(self, model, messages, session, info):
        entry = self.catalog[model]
        pricing = [p['pricing'] for p in entry['providers']]
        # Conservative byte upper bound for input tokens, plus message overhead;
        # reserve twice the maximum catalog rate, including possible cache writes.
        nbytes = len(json.dumps(messages, ensure_ascii=False).encode()) + 2048
        if nbytes > 40000:
            raise GatewayError('input_size_stop')
        input_rate = max(max(float(p.get(k, 0)) for k in ('prompt', 'input_cache_write', 'input_cache_write_1h')) for p in pricing)
        output_rate = max(float(p['completion']) for p in pricing)
        estimate = 2 * (nbytes * input_rate + 384 * output_rate + max(float(p.get('request', 0)) for p in pricing)) + 0.001
        attempt = self.reserve(estimate)
        payload = {'model': model, 'messages': messages, 'temperature': 0, 'max_tokens': 384, 'stream': False}
        started = datetime.now(timezone.utc).isoformat()
        try:
            data = request('/chat/completions', self.key, payload, session)
            usage = data.get('usage', {})
            cost = usage.get('cost_details', {}).get('total_cost', usage.get('cost'))
            if cost is None or not math.isfinite(float(cost)) or float(cost) < 0:
                raise GatewayError('missing_valid_cost_stop')
            cost = float(cost)
            with self.lock:
                self.reserved -= estimate
                self.spent += cost
                if cost > estimate or self.spent > self.limit:
                    self.halted = True
            metadata = data.get('metadata', {})
            choice = data.get('choices', [{}])[0]
            content = choice.get('message', {}).get('content')
            result = {**info, 'attempt_id': attempt, 'timestamp_utc': started,
                      'requested_model': model, 'model': data.get('model'),
                      'used_model': metadata.get('used_model'),
                      'provider': metadata.get('used_provider'),
                      'model_version': metadata.get('underlying_used_model'),
                      'request_id': metadata.get('request_id', data.get('id')),
                      'temperature_requested': 0, 'temperature_applied': None,
                      'seed_requested': None, 'seed_applied': None,
                      'finish_reason': choice.get('finish_reason'),
                      'cached': metadata.get('cached'), 'cost_usd': cost,
                      'prompt_tokens': usage.get('prompt_tokens'),
                      'completion_tokens': usage.get('completion_tokens'),
                      'content': content}
            serialized = json.dumps(result)
            if self.key in serialized:
                raise GatewayError('secret_in_response_stop')
            self.sink(result)
            if choice.get('finish_reason') not in ('stop', 'end_turn') or not isinstance(content, str) or not content.strip():
                raise GatewayError('invalid_or_truncated_output')
            # Unknown provider is recorded, never invented. Model substitutions stop.
            resolved = metadata.get('used_model')
            if resolved and resolved != model:
                raise GatewayError('resolved_model_mismatch')
            if self.halted:
                raise GatewayError('cost_exceeded_reservation_stop')
            return content
        except Exception as exc:
            with self.lock:
                # A request may have been billed without a usable response. Stop
                # the whole run; retain the reservation as uncertain exposure.
                self.halted = True
            code = str(exc) if isinstance(exc, GatewayError) else 'unexpected_failure'
            self.sink({**info, 'attempt_id': attempt, 'timestamp_utc': started,
                       'requested_model': model, 'error': code})
            raise GatewayError(code) from None
