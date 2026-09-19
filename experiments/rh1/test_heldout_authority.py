import json
from pathlib import Path
import tempfile
import unittest

from heldout_authority import run_unit
from runner import Journal


class ControlledGateway:
    def __init__(self):
        self.calls = []
    def complete(self, arm, messages, session, info):
        self.calls.append((info, messages))
        if info['phase'] == 'endpoint':
            score = 3 if info['condition'] == 'N' else 2
            return json.dumps({'task_agreement': score, 'evidence_uncertainty': 3, 'readiness': 3})
        if info['phase'] == 'probe':
            share = 75 if info['condition'] == 'P-' and info['role'] == 'B' else 50
            return json.dumps({'authority_share': share})
        return 'We should state the claim carefully.'


class HeldoutTests(unittest.TestCase):
    def test_paired_receiver_delta_and_branch_isolation(self):
        cfg = json.loads((Path(__file__).parent / 'heldout_authority_config.json').read_text())
        model = cfg['models'][0]
        with tempfile.TemporaryDirectory() as tmp:
            gateway = ControlledGateway()
            result = run_unit(model, 0, cfg, gateway, Journal(Path(tmp)))
            self.assertEqual(len(gateway.calls), 30)
            self.assertTrue(result['matched'])
            self.assertEqual(result['receiver_delta'], .25)
            self.assertEqual(result['dyad_delta'], .125)
            n = json.loads((Path(tmp) / f'{model["arm"]}-unit0-N.json').read_text())
            p = json.loads((Path(tmp) / f'{model["arm"]}-unit0-P-.json').read_text())
            self.assertNotEqual(n['contexts']['B'], p['contexts']['B'])


if __name__ == '__main__':
    unittest.main()
