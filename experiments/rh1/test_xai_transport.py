import io
import json
import unittest
import urllib.error
from unittest.mock import patch, MagicMock
from providers.xai import request, XaiGateway
from providers.devpass import GatewayError

class TransportTests(unittest.TestCase):
    def test_timeout_forwarding_and_json(self):
        opener=MagicMock();opener.open.return_value.__enter__.return_value=io.BytesIO(b'{"ok":true}')
        with patch('providers.xai.urllib.request.build_opener',return_value=opener):
            self.assertEqual(request('/responses','FAKE_SECRET',{},timeout=600),{'ok':True})
        self.assertEqual(opener.open.call_args.kwargs['timeout'],600)

    def test_sanitized_error_categories(self):
        cases=[(TimeoutError('FAKE_SECRET'),'transport_timeout'),
               (urllib.error.URLError(TimeoutError('FAKE_SECRET')),'transport_timeout'),
               (urllib.error.URLError('FAKE_SECRET'),'transport_url_failure'),
               (urllib.error.HTTPError('https://api.x.ai',429,'FAKE_SECRET',{},None),'http_429'),
               (OSError('FAKE_SECRET'),'transport_io_failure')]
        for error,code in cases:
            opener=MagicMock();opener.open.side_effect=error
            with patch('providers.xai.urllib.request.build_opener',return_value=opener):
                with self.assertRaises(GatewayError) as caught:request('/responses','FAKE_SECRET',{})
            self.assertEqual(str(caught.exception),code)

    def test_invalid_json_separate(self):
        opener=MagicMock();opener.open.return_value.__enter__.return_value=io.BytesIO(b'not json FAKE_SECRET')
        with patch('providers.xai.urllib.request.build_opener',return_value=opener):
            with self.assertRaisesRegex(GatewayError,'^response_json_failure$'):request('/responses','FAKE_SECRET',{})

    def test_uncertain_reservation_and_elapsed_receipt(self):
        events=[];g=XaiGateway('FAKE_SECRET',.08,1,events.append,request_timeout=600)
        with patch('providers.xai.request',side_effect=GatewayError('transport_timeout')) as call:
            with self.assertRaises(GatewayError):g.complete(g.arm,[{'role':'user','content':'test'}],'unused',{})
        self.assertGreater(g.reserved,0);self.assertTrue(g.halted)
        self.assertEqual(call.call_args.kwargs['timeout'],600)
        self.assertEqual(events[0]['request_timeout_seconds'],600)
        self.assertGreaterEqual(events[0]['elapsed_seconds'],0)
        self.assertNotIn('FAKE_SECRET',json.dumps(events))

    def test_invalid_timeout(self):
        for value in (0,-1,3601,float('nan'),True):
            with self.assertRaises(GatewayError):XaiGateway('FAKE_SECRET',.08,1,lambda _:None,request_timeout=value)

if __name__=='__main__':unittest.main()
