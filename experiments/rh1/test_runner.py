import copy
import unittest
from unittest.mock import patch
from providers.devpass import Gateway, GatewayError, NoRedirect
from providers.openrouter import OpenRouterGateway
from runner import matched, parse_json


class PilotTests(unittest.TestCase):
    def gateway(self):
        self.events = []
        return Gateway('FAKE_SECRET_DO_NOT_LOG', {'m': {'providers': [{'pricing': {'prompt': '0.000001', 'completion': '0.000001'}}]}}, 1, 2, self.events.append)

    def test_budget_concurrent_reservations(self):
        g = self.gateway(); g.reserve(.6)
        with self.assertRaises(GatewayError): g.reserve(.5)
        self.assertEqual(g.calls, 1)

    def test_transport_error_never_serialized(self):
        g = self.gateway()
        with patch('providers.devpass.request', side_effect=ValueError(g.key)):
            with self.assertRaises(GatewayError): g.complete('m', [], 's', {})
        self.assertNotIn(g.key, str(self.events))
        self.assertTrue(g.halted)
        self.assertGreater(g.reserved, 0)

    def test_secret_echo_never_logged(self):
        g = self.gateway()
        response = {'usage': {'cost': .0001}, 'choices': [{'finish_reason': 'stop', 'message': {'content':g.key}}]}
        with patch('providers.devpass.request', return_value=response):
            with self.assertRaises(GatewayError): g.complete('m', [], 's', {})
        self.assertNotIn(g.key, str(self.events))

    def test_missing_cost_stops(self):
        g = self.gateway()
        with patch('providers.devpass.request', return_value={'usage':{}}):
            with self.assertRaises(GatewayError): g.complete('m', [], 's', {})
        self.assertTrue(g.halted)

    def test_model_substitution_stops(self):
        g = self.gateway()
        response = {'usage': {'cost': .0001}, 'metadata': {'used_model':'other'}, 'choices':[{'finish_reason':'stop','message':{'content':'ok'}}]}
        with patch('providers.devpass.request', return_value=response):
            with self.assertRaises(GatewayError): g.complete('m', [], 's', {})

    def test_branch_isolation_and_matching(self):
        base = {'A':[{'role':'user','content':'baseline'}]}
        branch = copy.deepcopy(base); branch['A'].append({'role':'user','content':'perturbation'})
        self.assertEqual(len(base['A']),1)
        left = {r:{'readiness':2} for r in ('A','B')}
        right = copy.deepcopy(left); right['B']['readiness']=4
        self.assertFalse(matched(left,right))
        self.assertTrue(matched(left,left))

    def test_invalid_scales_and_outcomes_rejected(self):
        for content,kind in [('{"decision":"maybe"}','probe'), ('{"task_agreement":true,"evidence_uncertainty":1,"readiness":2}','endpoint')]:
            with self.assertRaises(GatewayError): parse_json(content,kind)

    def test_single_fenced_json_with_prose_is_parsed(self):
        content = 'Brief explanation.\n```json\n{"task_agreement":4,"evidence_uncertainty":3,"readiness":4}\n```'
        self.assertEqual(parse_json(content,'endpoint'),
                         {'task_agreement':4,'evidence_uncertainty':3,'readiness':4})
        with self.assertRaises(GatewayError):
            parse_json(content+'\n```json\n{"readiness":0}\n```','endpoint')

    def test_redirect_refused(self):
        self.assertIsNone(NoRedirect().redirect_request(None,None,302,'',{},'https://untrusted.example'))

    def test_reasoning_arm_sends_requested_effort_and_records_tokens(self):
        events = []
        g = Gateway('FAKE_SECRET_DO_NOT_LOG', {'m': {'providers': [{'pricing': {'prompt': '0.000001', 'completion': '0.000001'}}]}},
                    1, 2, events.append, {'m__medium': {'model':'m', 'reasoning_effort':'medium', 'max_tokens':1536}})
        response = {'usage': {'cost':.0001, 'reasoning_tokens':17},
                    'metadata': {'used_model':'m'},
                    'choices':[{'finish_reason':'stop','message':{'content':'ok'}}]}
        with patch('providers.devpass.request', return_value=response) as send:
            self.assertEqual(g.complete('m__medium', [], 's', {}), 'ok')
        payload = send.call_args.args[2]
        self.assertEqual(payload['model'], 'm')
        self.assertEqual(payload['reasoning_effort'], 'medium')
        self.assertEqual(payload['max_tokens'], 1536)
        self.assertNotIn('temperature', payload)
        self.assertEqual(events[0]['reasoning_tokens'], 17)
        self.assertIsNone(events[0]['reasoning_effort_applied'])

    def test_inkling_request_cost_and_reasoning_usage(self):
        events = []
        gateway = OpenRouterGateway('FAKE_SECRET_DO_NOT_LOG','thinkingmachines/inkling',
                                    {'prompt':'0.000001','completion':'0.00000405'},1,2,events.append)
        response = {'id':'gen-test','model':'thinkingmachines/inkling',
                    'usage':{'cost':.0002,'completion_tokens_details':{'reasoning_tokens':39}},
                    'choices':[{'finish_reason':'stop','message':{'content':'ok'}}]}
        with patch('providers.openrouter.request',return_value=response) as send:
            self.assertEqual(gateway.complete('inkling__medium',[],None,{}),'ok')
        payload = send.call_args.args[2]
        self.assertEqual(payload['reasoning'],{'effort':'medium'})
        self.assertTrue(payload['usage']['include'])
        self.assertEqual(events[0]['reasoning_tokens'],39)
        self.assertEqual(gateway.spent,.0002)

    def test_qwen_measurement_requests_native_schema(self):
        events=[]
        g=Gateway('FAKE_SECRET_DO_NOT_LOG',{'q':{'providers':[{'pricing':{'prompt':'0.000001','completion':'0.000001'}}]}},
                  1,2,events.append,{'q__medium':{'model':'q','reasoning_effort':'medium',
                                                  'max_tokens':1536,'structured_measurements':True}})
        response={'usage':{'cost':.0001,'completion_tokens_details':{'reasoning_tokens':10}},
                  'metadata':{'used_model':'q'},
                  'choices':[{'finish_reason':'stop','message':{'content':'{"decision":"joint_review","reason":"review"}'}}]}
        with patch('providers.devpass.request',return_value=response) as send:
            g.complete('q__medium',[],None,{'phase':'probe'})
        fmt=send.call_args.args[2]['response_format']
        self.assertEqual(fmt['type'],'json_schema')
        self.assertTrue(fmt['json_schema']['strict'])
        self.assertEqual(events[0]['response_format_requested'],'json_schema')


if __name__ == '__main__': unittest.main()
