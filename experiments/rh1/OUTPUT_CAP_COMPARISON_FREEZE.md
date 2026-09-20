# Four-call output-cap comparison

Before new inference: order 4096,8192,8192,4096; identical soil_sensor_transfer
role-A messages, Grok 4.6, temperature 1.7, high effort, timeout 600 seconds,
no seed. Four fresh stateless responses, no historical observations pooled.
Primary endpoint: nonempty final output by cap. Secondary: valid authority
score, reported token count, latency, completed/incomplete status. Report counts
and all missing/invalid outputs, no significance or equivalence claims with n=2.

A billed completed empty final is an endpoint and does not stop this diagnostic.
Transport error, parameter mismatch, invalid cost, budget excess or other error
stops the block; no automatic retries. Separate per-call gateways share remaining
budget and accumulated unresolved reservations. Maximum USD 0.40. Baseline
conservative exposure USD 7.4821905407 plus unchanged v0.2 reserve USD 2.00 plus
this cap is USD 9.8821905407. User-authorized next diagnostic; no new credentials.

Rationale: previous 4096-cap empty call and fresh 8192-cap success do not establish
causation, particularly since the successful call used only 773 output tokens.
This small balanced-order comparison describes repeatability, not internal
reasoning mechanism or RH-1 path memory. Temperature is fixed throughout.
