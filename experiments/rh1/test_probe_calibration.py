import json
import unittest
from pathlib import Path

from probe_calibration import parse_response, summarize


class CalibrationTests(unittest.TestCase):
    def test_parse_and_orientation(self):
        self.assertEqual(parse_response('{"decision":"delegate"}', 'binary_delegate'), 1)
        self.assertEqual(parse_response('```json\n{"authority_share":25}\n```', 'authority_share'), .25)
        self.assertEqual(parse_response('{"verification_minutes":45}', 'verification_minutes'), .25)
        for raw in ('{"authority_share":true}', '{"authority_share":30}', '{}',
                    '```json\n{"authority_share":25}\n```\n```json\n{"authority_share":50}\n```'):
            with self.assertRaises(ValueError):
                parse_response(raw, 'authority_share')

    def test_selection_requires_calibration_passes(self):
        cfg = json.loads((Path(__file__).parent / 'calibration_config.json').read_text())
        rows = []
        for m in cfg['models']:
            for probe in cfg['probes']:
                for i in range(3):
                    for role in ('A', 'B'):
                        for anchor in cfg['anchors']:
                            score = {'neutral': i / 4, 'partner_verified': .75,
                                     'self_verified': .25}[anchor]
                            rows.append({'arm': m['arm'], 'probe': probe, 'anchor': anchor,
                                         'valid': True, 'score': score})
        self.assertEqual(summarize(rows, cfg)['selected_probe'], 'authority_share')
        rows = [r for r in rows if r['probe'] == 'binary_delegate' and r['arm'] in
                (cfg['models'][0]['arm'], cfg['models'][1]['arm'])]
        self.assertIsNone(summarize(rows, cfg)['selected_probe'])


if __name__ == '__main__':
    unittest.main()
