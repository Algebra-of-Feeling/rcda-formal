"""Bounded direct xAI Responses transport for Grok RH-1A experiments."""
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
    def __init__(self, key, limit, max_calls, sink, *, model='grok-4.6',
                 arm='grok-4.6__medium', max_tokens=1536, input_rate=2,
                 output_rate=6, reasoning_effort='medium', temperature=None):
        if not key or not 0 < limit <= 2.3:
            raise GatewayError('missing_key_or_bad_budget')
        self.key, self.limit, self.max_calls, self.sink = key, limit, max_calls, sink
        self.model, self.arm, self.max_tokens = model, arm, max_tokens
        self.input_rate, self.output_rate = input_rate, output_rate
        if temperature is not None and (type(temperature) not in (int, float) or not math.isfinite(temperature) or not 0 <= temperature <= 2):
            raise GatewayError('invalid_temperature')
        self.temperature = temperature
        self.reasoning_effort = reasoning_effort
        self.lock = threading.Lock()
        self.pacing_lock = threading.Lock()
        self.last_request = 0
        self.calls = 0
        self.spent = self.reserved = 0.0
        self.halted = False

    def complete(self, arm, messages, session, info):
        if arm != self.arm:
            raise GatewayError('call_stop')
        with self.pacing_lock:
            delay = max(0, .85 - (time.monotonic() - self.last_request))
            if delay:
                time.sleep(delay)
            self.last_request = time.monotonic()
        nbytes = len(json.dumps(messages, ensure_ascii=False).encode()) + 2048
        max_tokens = self.max_tokens
        if nbytes > 40000:
            raise GatewayError('input_size_stop')
        estimate = 2 * (nbytes * self.input_rate / 1_000_000 +
                        max_tokens * self.output_rate / 1_000_000) + .001
        with self.lock:
            if self.halted or self.calls >= self.max_calls or self.spent + self.reserved + estimate > self.limit:
                self.halted = True
                raise GatewayError('budget_or_call_stop')
            self.calls += 1
            attempt = self.calls
            self.reserved += estimate
        payload = {'model': self.model, 'input': messages, 'max_output_tokens': max_tokens}
        if self.reasoning_effort is not None:
            payload['reasoning'] = {'effort': self.reasoning_effort}
        if self.temperature is not None:
            payload['temperature'] = self.temperature
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
            record = {**info, 'attempt_id': attempt, 'arm': arm, 'requested_model': self.model,
                      'model': data.get('model'), 'request_id': data.get('id'),
                      'timestamp_utc': started, 'reasoning_effort_requested': self.reasoning_effort,
                      'reasoning_effort_applied': None,
                      'reasoning_effort_returned': (data.get('reasoning') or {}).get('effort'),
                      'temperature_requested': self.temperature,
                      'temperature_returned': data.get('temperature'), 'reasoning_tokens':
                      (usage.get('output_tokens_details') or {}).get('reasoning_tokens'),
                      'input_tokens': usage.get('input_tokens'), 'output_tokens': usage.get('output_tokens'),
                      'cost_usd': cost, 'status': data.get('status'), 'content': content}
            if self.key in json.dumps(record):
                raise GatewayError('secret_in_response_stop')
            self.sink(record)
            if data.get('model') != self.model or data.get('status') != 'completed' or not content.strip():
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
