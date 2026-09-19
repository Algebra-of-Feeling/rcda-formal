import copy
import unittest
from unittest.mock import patch
from providers.devpass import Gateway, GatewayError, NoRedirect
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

    def test_redirect_refused(self):
        self.assertIsNone(NoRedirect().redirect_request(None,None,302,'',{},'https://untrusted.example'))


if __name__ == '__main__': unittest.main()
