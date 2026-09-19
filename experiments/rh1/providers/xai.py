"""Bounded direct xAI Responses transport for supplementary Grok calibration."""
from datetime import datetime, timezone
import json
import math
import threading
import time
import urllib.error
import urllib.request

from providers.devpass import GatewayError, NoRedirect

BASE = 'https://api.x.ai/v1'


def request(path, key, payload=None):
    if path not in ('/models', '/responses'):
        raise GatewayError('endpoint_not_allowed')
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=body,
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(req, timeout=120) as response:
            return json.load(response)
    except urllib.error.HTTPError as e:
        raise GatewayError('http_' + str(e.code)) from None
    except Exception:
        raise GatewayError('transport_or_json_failure') from None


class XaiGateway:
    def __init__(self, key, limit, max_calls, sink):
        if not key or not 0 < limit <= 1.5:
            raise GatewayError('missing_key_or_bad_budget')
        self.key, self.limit, self.max_calls, self.sink = key, limit, max_calls, sink
        self.lock = threading.Lock()
        self.pacing_lock = threading.Lock()
        self.last_request = 0
        self.calls = 0
        self.spent = self.reserved = 0.0
        self.halted = False

    def complete(self, arm, messages, session, info):
        if arm != 'grok-4.6__medium':
            raise GatewayError('call_stop')
        with self.pacing_lock:
            delay = max(0, .85 - (time.monotonic() - self.last_request))
            if delay:
                time.sleep(delay)
            self.last_request = time.monotonic()
        nbytes = len(json.dumps(messages, ensure_ascii=False).encode()) + 2048
        max_tokens = 1536
        if nbytes > 40000:
            raise GatewayError('input_size_stop')
        estimate = 2 * (nbytes * 2 / 1_000_000 + max_tokens * 6 / 1_000_000) + .001
        with self.lock:
            if self.halted or self.calls >= self.max_calls or self.spent + self.reserved + estimate > self.limit:
                self.halted = True
                raise GatewayError('budget_or_call_stop')
            self.calls += 1
            attempt = self.calls
            self.reserved += estimate
        payload = {'model': 'grok-4.6', 'input': messages, 'reasoning': {'effort': 'medium'},
                   'max_output_tokens': max_tokens}
        started = datetime.now(timezone.utc).isoformat()
        try:
            data = request('/responses', self.key, payload)
            usage = data.get('usage') or {}
            ticks = usage.get('cost_in_usd_ticks')
            if type(ticks) not in (int, float) or not math.isfinite(ticks) or ticks < 0:
                raise GatewayError('missing_valid_cost_stop')
            cost = ticks / 10_000_000_000
            with self.lock:
                self.reserved -= estimate
                self.spent += cost
                if cost > estimate or self.spent > self.limit:
                    self.halted = True
            output = data.get('output') or []
            texts = [c.get('text') for item in output if item.get('type') == 'message'
                     for c in item.get('content', []) if c.get('type') == 'output_text']
            content = '\n'.join(t for t in texts if isinstance(t, str))
            record = {**info, 'attempt_id': attempt, 'arm': arm, 'requested_model': 'grok-4.6',
                      'model': data.get('model'), 'request_id': data.get('id'),
                      'timestamp_utc': started, 'reasoning_effort_requested': 'medium',
                      'reasoning_effort_applied': None, 'reasoning_tokens':
                      usage.get('output_tokens_details', {}).get('reasoning_tokens'),
                      'input_tokens': usage.get('input_tokens'), 'output_tokens': usage.get('output_tokens'),
                      'cost_usd': cost, 'status': data.get('status'), 'content': content}
            if self.key in json.dumps(record):
                raise GatewayError('secret_in_response_stop')
            self.sink(record)
            if data.get('model') != 'grok-4.6' or data.get('status') != 'completed' or not content.strip():
                raise GatewayError('invalid_or_truncated_output')
            if self.halted:
                raise GatewayError('cost_exceeded_reservation_stop')
            return content
        except Exception as exc:
            with self.lock:
                self.halted = True
            code = str(exc) if isinstance(exc, GatewayError) else 'unexpected_failure'
            self.sink({**info, 'attempt_id': attempt, 'arm': arm,
                       'timestamp_utc': started, 'error': code})
            raise GatewayError(code) from None
