import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from grok_controlled import run_unit
from providers.xai import XaiGateway
from runner import Journal


class ControlledGateway:
    def __init__(self):
        self.calls = []
    def complete(self, arm, messages, session, info):
        self.calls.append(info)
        if info['phase'] == 'endpoint':
            return '{"task_agreement":3,"evidence_uncertainty":3,"readiness":3}'
        if info['phase'] == 'probe':
            share = {'N':50, 'F':50, 'P-':25, 'P+':75}[info['condition']]
            return json.dumps({'authority_share':share})
        return 'We should keep the claim testable and describe the uncertainty.'


class GrokControlledTests(unittest.TestCase):
    def test_controls_and_unit_count(self):
        cfg = json.loads((Path(__file__).parent / 'grok_controlled_config.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            gateway = ControlledGateway()
            result = run_unit(cfg['models'][0], 0, cfg, gateway, Journal(Path(tmp)))
        self.assertEqual(len(gateway.calls), 58)
        self.assertTrue(result['all_conditions_matched'])
        self.assertEqual(result['comparisons']['F']['receiver_delta'], 0)
        self.assertEqual(result['comparisons']['P-']['receiver_delta'], -.25)
        self.assertEqual(result['comparisons']['P+']['receiver_delta'], .25)

    def test_fixed_reasoning_model_omits_effort_parameter(self):
        seen = []
        reply = {'model':'grok-4.20-0309-reasoning', 'status':'completed', 'id':'test',
                 'usage':{'cost_in_usd_ticks':1000000, 'output_tokens_details':{'reasoning_tokens':4}},
                 'output':[{'type':'message','content':[{'type':'output_text','text':'{"authority_share":50}'}]}]}
        def fake_request(path, key, payload):
            seen.append(payload)
            return reply
        gateway = XaiGateway('FAKE_SECRET_DO_NOT_LOG', 1.5, 1, lambda _:None,
                             model='grok-4.20-0309-reasoning',
                             arm='grok-4.20-0309-reasoning', max_tokens=4096,
                             input_rate=1.25, output_rate=2.5, reasoning_effort=None)
        with patch('providers.xai.request', side_effect=fake_request):
            gateway.complete('grok-4.20-0309-reasoning', [{'role':'user','content':'test'}],
                             'session', {'phase':'probe'})
        self.assertNotIn('reasoning', seen[0])
        self.assertEqual(seen[0]['model'], 'grok-4.20-0309-reasoning')


if __name__ == '__main__':
    unittest.main()
