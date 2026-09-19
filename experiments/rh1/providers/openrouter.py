"""Bounded OpenRouter transport for the Inkling RH-1A candidate."""
import json
import math
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

from providers.devpass import GatewayError, NoRedirect

BASE = 'https://openrouter.ai/api/v1'


def request(path, key, payload=None):
    if path not in ('/key', '/chat/completions'):
        raise GatewayError('endpoint_not_allowed')
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data,
        headers={'Authorization':'Bearer '+key, 'Content-Type':'application/json'})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(req, timeout=90) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise GatewayError('http_' + str(exc.code)) from None
    except Exception:
        raise GatewayError('transport_or_json_failure') from None


class OpenRouterGateway:
    def __init__(self, key, model, pricing, limit, max_calls, sink, max_tokens=1536):
        if not key or not 0 < limit <= 10:
            raise GatewayError('missing_key_or_bad_budget')
        self.key, self.model, self.pricing = key, model, pricing
        self.limit, self.max_calls, self.sink = limit, max_calls, sink
        self.max_tokens = max_tokens
        self.calls = 0
        self.spent = self.reserved = 0.0
        self.halted = False
        self.last_request = 0.0
        self.lock = threading.Lock()
        self.pacing_lock = threading.Lock()

    def complete(self, arm, messages, session, info):
        if arm != 'inkling__medium':
            raise GatewayError('call_stop')
        with self.pacing_lock:
            delay = max(0, 0.85 - (time.monotonic() - self.last_request))
            if delay:
                time.sleep(delay)
            self.last_request = time.monotonic()
        max_tokens = self.max_tokens
        nbytes = len(json.dumps(messages,ensure_ascii=False).encode()) + 2048
        if nbytes > 40000:
            raise GatewayError('input_size_stop')
        estimate = 2 * (nbytes * float(self.pricing['prompt']) + max_tokens * float(self.pricing['completion'])) + .001
        with self.lock:
            if self.halted or self.calls >= self.max_calls or self.spent + self.reserved + estimate > self.limit:
                self.halted = True
                raise GatewayError('budget_or_call_stop')
            self.calls += 1
            attempt = self.calls
            self.reserved += estimate
        payload = {'model':self.model, 'messages':messages,
                   'reasoning':{'effort':'medium'}, 'max_tokens':max_tokens,
                   'usage':{'include':True}}
        started = datetime.now(timezone.utc).isoformat()
        try:
            data = request('/chat/completions', self.key, payload)
            usage = data.get('usage',{})
            cost = usage.get('cost')
            if cost is None or not math.isfinite(float(cost)) or float(cost) < 0:
                raise GatewayError('missing_valid_cost_stop')
            cost = float(cost)
            with self.lock:
                self.reserved -= estimate
                self.spent += cost
                if cost > estimate or self.spent > self.limit:
                    self.halted = True
                    raise GatewayError('cost_exceeded_reservation_stop')
            choice = data.get('choices',[{}])[0]
            content = choice.get('message',{}).get('content')
            record = {**info, 'attempt_id':attempt, 'arm':arm, 'requested_model':self.model,
                      'model':data.get('model'), 'request_id':data.get('id'),
                      'timestamp_utc':started, 'reasoning_effort_requested':'medium',
                      'reasoning_effort_applied':None,
                      'reasoning_tokens':usage.get('completion_tokens_details',{}).get('reasoning_tokens'),
                      'prompt_tokens':usage.get('prompt_tokens'),
                      'completion_tokens':usage.get('completion_tokens'),
                      'cost_usd':cost, 'finish_reason':choice.get('finish_reason'),
                      'content':content}
            if self.key in json.dumps(record):
                raise GatewayError('secret_in_response_stop')
            self.sink(record)
            if data.get('model') != self.model:
                raise GatewayError('resolved_model_mismatch')
            if choice.get('finish_reason') not in ('stop','end_turn') or not isinstance(content,str) or not content.strip():
                raise GatewayError('invalid_or_truncated_output')
            return content
        except Exception as exc:
            with self.lock:
                self.halted = True
            code = str(exc) if isinstance(exc,GatewayError) else 'unexpected_failure'
            self.sink({**info,'attempt_id':attempt,'arm':arm,'requested_model':self.model,
                       'timestamp_utc':started,'error':code})
            raise GatewayError(code) from None
