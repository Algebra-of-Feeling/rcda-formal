# Stored response structure audit

Four read-only GET requests retrieved the responses from the balanced cap comparison. No new inference request was submitted. Retrieved output structure was recorded with string types and lengths; reasoning strings and raw full payloads were not saved. The same final-message extraction rule as the existing adapter was applied independently.

| Call | Cap | Original POST output types | Retrieved GET output types | Retrieved final |
|---|---:|---|---|---|
| 1 | 4096 | reasoning, message | message | {"authority_share":25} |
| 2 | 8192 | reasoning, message | message | {"authority_share":25} |
| 3 | 8192 | reasoning | empty array | absent |
| 4 | 4096 | reasoning | empty array | absent |

All four stored responses returned completed status, null error and null incomplete_details. Model, temperature 1.7, effort high, output cap and usage agree with original receipts. The two empty responses contain no alternative final-answer field in the inspected structure. The successful controls recover the exact original JSON, so retrieval and the final-text path work for those cases.

This supports absence of a delivered final message for calls 3/4, rather than a simple message-extraction failure. It does not establish why the service produced that result or rule out every possible client/provider interaction. The original POST payloads were not retained in full; original output types come from contemporaneous receipts. GET omitted reasoning items in all four cases. Do not interpret that omission as evidence that reasoning never occurred.

The documented Responses contract supports retrieval by response ID and places generated items in output. [Official reference](https://docs.x.ai/developers/rest-api-reference/inference/responses). The known output-cap discrepancy remains: call 4 reports 10627 output tokens at requested/returned cap 4096. The empty call 3 used 6950 at cap 8192. No cap-exhaustion or temperature mechanism is proven.

Nine offline tests passed: three audit tests validate that reasoning text is neither mistaken for a final answer nor persisted, that messages after reasoning are extracted, and that completed empty output stays empty; six existing transport tests passed. No adapter behaviour was changed and no experimental score was imputed.

Conclusion: missing final messages confirmed in stored responses; parser-only explanation not supported for these records. Provider-side root cause and output-cap semantics remain unresolved. A concise vendor diagnostic packet can be assembled from these sanitized receipts if requested; no external support message was sent.

No new inference cost added; cumulative conservative exposure remains USD 7.6417725407, plus separate v0.2 reserve USD 2.00 gives USD 9.6417725407. These GET responses repeat historical cost metadata; those costs are not counted a second time. No local inference active.
