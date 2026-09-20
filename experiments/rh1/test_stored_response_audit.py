import json
import unittest
from audit_stored_responses import inspect


class StoredResponseAuditTests(unittest.TestCase):
    def test_reasoning_is_not_final_or_persisted(self):
        result=inspect({'output':[{'type':'reasoning','summary':[{'text':'PRIVATE_REASONING_SENTINEL'}]}], 'status':'completed'})
        self.assertEqual(result['extracted_final_text'],'')
        self.assertNotIn('PRIVATE_REASONING_SENTINEL',json.dumps(result))

    def test_message_after_reasoning_extracted(self):
        result=inspect({'output':[{'type':'reasoning','content':[{'type':'reasoning_text','text':'PRIVATE_REASONING_SENTINEL'}]}, {'type':'message','content':[{'type':'output_text','text':'{"authority_share":25}'}]}]})
        self.assertEqual(result['extracted_final_text'],'{"authority_share":25}')
        self.assertNotIn('PRIVATE_REASONING_SENTINEL',json.dumps(result))

    def test_empty_completed_not_fabricated(self):
        result=inspect({'status':'completed','output':[],'error':None,'incomplete_details':None})
        self.assertEqual(result['extracted_final_text'],'')
        self.assertFalse(result['error_present'])
        self.assertFalse(result['incomplete_details_present'])


if __name__=='__main__':unittest.main()
