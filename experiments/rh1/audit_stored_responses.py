"""Read-only audit of stored xAI replies; persist structure, never reasoning text."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import urllib.request
from providers.devpass import NoRedirect


def shape(value):
    if isinstance(value, dict):
        return {k:shape(v) for k,v in value.items()}
    if isinstance(value, list):
        return [shape(v) for v in value]
    if isinstance(value, str):
        return {'type':'string','characters':len(value)}
    return {'type':type(value).__name__}


def inspect(data):
    output=data.get('output') or []
    texts=[c.get('text','') for i in output if i.get('type')=='message'
           for c in i.get('content',[]) if c.get('type')=='output_text']
    usage=data.get('usage') or {}
    return dict(status=data.get('status'), model=data.get('model'),
        temperature=data.get('temperature'),effort=(data.get('reasoning') or {}).get('effort'),
        max_output_tokens=data.get('max_output_tokens'),
        incomplete_details_present=data.get('incomplete_details') is not None,
        error_present=data.get('error') is not None,
        output_item_types=[i.get('type') for i in output],
        output_content_types=[c.get('type') for i in output for c in i.get('content',[])],
        extracted_final_text='\n'.join(t for t in texts if isinstance(t,str)),
        input_tokens=usage.get('input_tokens'),output_tokens=usage.get('output_tokens'),
        reasoning_tokens=(usage.get('output_tokens_details') or {}).get('reasoning_tokens'),
        cost_in_usd_ticks=usage.get('cost_in_usd_ticks'),structure=shape(data))


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    key=os.environ.pop('RH1_XAI_KEY','')
    if not key:raise SystemExit('Missing credential')
    rows=[json.loads(x) for x in args.input.read_text().splitlines()]
    rows=[r for r in rows if 'request_id' in r]
    def get(row):
        result={'block_call':row['block_call'],'original':{k:row.get(k) for k in ('status','content','output_item_types','output_content_types','output_tokens','reasoning_tokens','max_output_tokens_returned')}}
        try:
            ident=row['request_id']
            if not all(c in '0123456789abcdef-' for c in ident):raise ValueError('bad_id')
            req=urllib.request.Request('https://api.x.ai/v1/responses/'+ident,headers={'Authorization':'Bearer '+key})
            opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
            with opener.open(req,timeout=30) as response:data=json.load(response)
            result['retrieved']=inspect(data)
            if key in json.dumps(result):raise ValueError('secret_in_result')
        except Exception as exc:
            result={'block_call':row['block_call'],'retrieval_error_type':type(exc).__name__}
        return result
    with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(get,rows))
    report=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),new_inference_calls=0,retrieval_get_calls=len(rows),results=results)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps([{'call':r['block_call'],'original':r.get('original'),'retrieved':{k:v for k,v in r.get('retrieved',{}).items() if k!='structure'},'error':r.get('retrieval_error_type')} for r in results],indent=2))


if __name__=='__main__':main()
