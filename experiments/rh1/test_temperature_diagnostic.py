import unittest
from unittest.mock import patch
from providers.xai import XaiGateway
from providers.devpass import GatewayError
from temperature_diagnostic import schedule
from context_controls import fingerprint

class TemperatureTests(unittest.TestCase):
    def test_schedule_holds_context_constant(self):
        jobs=schedule();self.assertEqual(len(jobs),12)
        groups={}
        for scenario,repeat,temp,messages in jobs:groups.setdefault(scenario,[]).append((repeat,temp,fingerprint(messages)))
        self.assertEqual(len(groups),2)
        for values in groups.values():
            self.assertEqual(len({v[2] for v in values}),1)
            self.assertEqual(len({v[:2] for v in values}),6)

    def test_payload_and_receipt_preserve_temperature(self):
        for temp in (None,.2,.7,1.2,2.0):
            events=[];g=XaiGateway('FAKE_SECRET',.25,1,events.append,temperature=temp)
            response={'model':'grok-4.6','status':'completed','temperature':temp,'usage':{'cost_in_usd_ticks':10000},'output':[{'type':'message','content':[{'type':'output_text','text':'{"authority_share":50}'}]}]}
            with patch('providers.xai.request',return_value=response) as call:
                g.complete('grok-4.6__medium',[{'role':'user','content':'test'}],'unused',{})
                payload=call.call_args.args[2]
                self.assertEqual('temperature' in payload,temp is not None)
                if temp is not None:self.assertEqual(payload['temperature'],temp)
            self.assertEqual(events[0]['temperature_returned'],temp)

    def test_maximum_schedule(self):
        jobs=schedule((2.0,))
        self.assertEqual(len(jobs),4)
        self.assertTrue(all(j[2]==2.0 for j in jobs))

    def test_invalid_temperature_rejected(self):
        for temp in (-1,3,float('nan'),True,'hot'):
            with self.assertRaises(GatewayError):XaiGateway('FAKE_SECRET',.25,1,lambda _:None,temperature=temp)

if __name__=='__main__':unittest.main()
