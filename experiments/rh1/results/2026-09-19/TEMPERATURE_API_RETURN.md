# Real API temperature return — incomplete diagnostic

Four calls were attempted from frozen source fb3a4e98488f56ed753846047155c362ca484333. All used the same stateless soil_sensor_transfer role-A messages, Grok 4.6, high effort, output cap 4096 and client timeout 600 seconds. The planned ten-call ascending/descending schedule stopped at its first unusable response. Ten existing transport/temperature unit tests passed.

| Requested and returned temperature | Valid authority result | Outcome |
|---|---:|---|
| 0.2 | 25% | Completed, 16.09 s |
| 0.7 | 25% | Completed, 17.04 s |
| 1.2 | 25% | Completed, 11.51 s |
| 1.7 | None | Completed status but no final text, 254.98 s |
| 2.0 | None | Not attempted |

The returned model, effort and temperature matched each request, including 1.7. Parameter echo is evidence of the API contract, not independent inspection of the internal sampler. The 1.7 response contained only a reasoning-type output item; no reasoning content was retained. Usage reported 6438 reasoning tokens and 6439 output tokens despite requested/returned max_output_tokens of 4096; incomplete_reason was null. This metadata inconsistency is not sufficient to assert truncation, a timeout, or a temperature-caused reasoning failure. No retries or additional calls followed.

Three valid responses agree at 25%, with only one observation per completed level. Two planned repetitions per level were not achieved. No temperature-effect, equivalence, psychiatric-state or H-M1 conclusion follows. The CLI illustrative table is excluded from this dataset, and the earlier API 50% at 1.7 remains a separate historical observation.

Reported total request cost: USD 0.058158 (including USD 0.039264 for the unusable 1.7 response). New unresolved reservation: zero. Earlier uncertain reservations remain in the cumulative conservative ledger: USD 7.4769225407. Current separate v0.2 reserve: USD 2.00; combined exposure plus reserve USD 9.4769225407. Unused portion of this diagnostic's USD 0.50 cap released: USD 0.441842. User reports subscription API credits; account credit coverage was not independently verified. Cost accounting follows the official [xAI per-request cost field](https://docs.x.ai/developers/cost-tracking). [Model documentation](https://docs.x.ai/developers/models/grok-4.6) lists high effort support and USD 2/6 per million input/output tokens, consistent with adapter rates.

No inference remains active locally. The next technical issue is the completed-but-empty response and output-cap semantics; enlarging the cap or changing effort would be a separate diagnostic, not an unlabelled continuation of this frozen comparison. The prospective v0.2 experiment remains unexecuted.
