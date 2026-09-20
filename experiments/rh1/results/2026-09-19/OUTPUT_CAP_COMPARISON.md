# Balanced output-cap comparison — completed

Frozen source 0010dd64bd18fc465b66b5cf821296f16f65ef11 specified four fresh stateless calls in order 4096,8192,8192,4096. Grok 4.6, temperature 1.7, high effort, identical input fingerprint and 600-second client timeout were held fixed. Model, temperature, effort and cap echoed in every response. No retries or outcome-dependent expansion occurred.

| Order | Output cap | Final authority | Elapsed s | Output tokens | Reasoning tokens | Cost USD |
|---|---:|---|---:|---:|---:|---:|
| 1 | 4096 | 25% | 13.850 | 751 | 744 | 0.005136 |
| 2 | 8192 | 25% | 317.302 | 7849 | 7842 | 0.047724 |
| 3 | 8192 | No final text | 265.072 | 6950 | 6949 | 0.042330 |
| 4 | 4096 | No final text | 420.475 | 10627 | 10627 | 0.064392 |

Every response had completed status. Each cap produced one nonempty final and one empty final (1/2 each). The descriptive success difference is zero percentage points; n=2 per cap does not establish equivalence or estimate a reliable failure rate. Both valid scores were 25%; empty outcomes remain missing behavioural scores, never zero or imputed 25. Historical observations are not pooled into this block.

Raising the cap did not eliminate empty outputs in this block. The empty 8192 response reported 6950 output tokens, below its cap; the empty 4096 response reported 10627, above its cap. This is inconsistent with a simple explanation that all missing final text results from exhausting the requested cap. It does not identify an internal mechanism, prove a vendor bug, or establish a temperature effect. The prior successful 8192 call is not a demonstrated fix.

The small comparison is complete. Root cause of completed-but-empty responses and cap accounting remains unresolved. The appropriate next diagnostic is inspection of sanitized response structure and API contract consistency, rather than treating missing text as a behavioural or clinical result. No reasoning content or credentials were saved.

Total reported cost USD 0.159582; no new unresolved reservation. Conservative cumulative exposure USD 7.6417725407, including previous unresolved reservations. Separate v0.2 reserve USD 2.00; combined USD 9.6417725407. Unused part of this diagnostic cap USD 0.240418 released. Subscription credit coverage remains unverified. No local inference remains active. Original temperature sweep and prospective v0.2 remain incomplete/unexecuted respectively.
