import copy
import unittest
from context_controls import transform, candidate_payload, fingerprint


class ContextControlsTests(unittest.TestCase):
    def setUp(self):
        self.message = {'role': 'user', 'content': 'private intervention'}
        self.ctx = [{'role': 'system', 'content': 'role'}, self.message,
                    {'role': 'assistant', 'content': 'private intervention'},
                    {'role': 'user', 'content': 'A says: private intervention'}]
        self.kw = dict(intervention_text='private intervention', recipient=True,
                       system_text='fixed role', briefing='fixed task', probe='fixed probe')

    def test_exact_removal_preserves_quotes_and_input(self):
        before = copy.deepcopy(self.ctx)
        out = transform(self.ctx, 'remove_intervention', **self.kw)
        self.assertEqual(out[:-1], [self.ctx[0], *self.ctx[2:]])
        self.assertEqual(self.ctx, before)
        out[0]['content'] = 'mutated'
        self.assertEqual(self.ctx, before)

    def test_full_history_keeps_every_message(self):
        self.assertEqual(transform(self.ctx, 'full_history', **self.kw)[:-1], self.ctx)

    def test_missing_duplicate_and_misrouted_rejected(self):
        for ctx, recipient in [(self.ctx[:1], True), (self.ctx+[self.message], True), (self.ctx, False)]:
            with self.assertRaises(ValueError):
                transform(ctx, 'remove_intervention', **{**self.kw, 'recipient': recipient})

    def test_partner_context_preserved(self):
        ctx = [self.ctx[0], self.ctx[2], self.ctx[3]]
        self.assertEqual(transform(ctx, 'remove_intervention', **{**self.kw, 'recipient':False})[:-1], ctx)

    def test_reset_ignores_branch_content(self):
        left = transform(self.ctx, 'canonical_reset', **self.kw)
        right = transform([{'role':'user','content':'other condition outcome 100'}], 'canonical_reset', **self.kw)
        self.assertEqual(left, right)
        self.assertEqual(left, [{'role':'system','content':'fixed role'},
                               {'role':'user','content':'fixed task'}, {'role':'user','content':'fixed probe'}])

    def test_invalid_schema_and_mode_rejected(self):
        for ctx, mode in [([], 'full_history'), ([{'role':'user','content':'x','condition':'P-'}], 'full_history'), (self.ctx,'unknown')]:
            with self.assertRaises(ValueError):
                transform(ctx, mode, **self.kw)

    def test_payload_hash_includes_parameters_and_has_no_labels(self):
        model = dict(model='fixed',max_tokens=100,reasoning_effort=None)
        messages = transform(self.ctx, 'canonical_reset', **self.kw)
        a = candidate_payload(model,messages)
        self.assertEqual(set(a), {'model','input','max_output_tokens'})
        self.assertNotEqual(fingerprint(a),fingerprint(candidate_payload({**model,'max_tokens':101}, messages)))
        self.assertNotEqual(fingerprint(a),fingerprint(candidate_payload({**model,'reasoning_effort':'medium'}, messages)))


if __name__ == '__main__':
    unittest.main()
