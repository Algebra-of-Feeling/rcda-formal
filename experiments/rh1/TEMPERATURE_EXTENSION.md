# Temperature extension — 2026-09-19

Status before first call: frozen exploratory capability/measurement diagnostic.
This is separate from v0.2 Stage A/B; their original freeze and prompt hashes remain unchanged.

## Scope and interpretation

Hold context fixed; vary temperature only for the final authority decision.
Use the two fixed fictional scenario briefings from v0.2, role A, with no generated
histories or N/F/P−/P+ labels. Grok 4.6, medium reasoning, 1536 output-token maximum;
temperatures 0.2, 0.7 and 1.2, two repeats per context/value: 12 calls maximum.
The exact schedule and prompts are pinned by the pre-execution source commit.
Each context is identical across temperatures and repetitions. Cycle temperature
order by context index plus repetition index. No seed or top_p field is supplied.

Report raw authority scores, counts, within-context ranges and temperature means.
No significance tests, clinical interpretations, or inference of absence from a
zero difference with only two repetitions. This is not a study of associative
branching: a scalar authority probe cannot measure that construct. It is not
independent replication of H-M1 or a replacement for v0.2 Stage A calibration.
Using these fixed briefings now means future results must disclose that they
were also used in this preliminary diagnostic; do not claim wholly untouched
scenarios. No parameter or prompt will be selected from these outcomes.

The provider receipt records requested temperature and returned temperature
separately. HTTP acceptance, echoed value and measured output sensitivity are
three distinct observations. A null/absent returned value means application is
unverified. Even an echoed value is not an audit of internal sampling.
Stop at first API/schema/model/cost/transport failure or budget exhaustion;
no paid retries. Existing transport reserves conservative input/output cost.

## Budget

Previously reported conservative exposure: USD 7.230302540700002.
Diagnostic cap USD 0.25; v0.2's USD 2.50 remains separately reserved.
Combined maximum USD 9.980302540700002, within the authorized USD 10.
A failed call retains its uncertain reservation. Any later execution must use
actual diagnostic cost plus uncertainty in the shared programme ledger.
Keys are read locally at runtime, never recorded in this document or results.

## Documentation check

Official sources consulted on 2026-09-19:
- https://docs.x.ai/developers/rest-api-reference/inference/responses shows the temperature response field.
- https://docs.x.ai/build/settings includes a Grok 4.6 Responses configuration with temperature 0.7.
- https://docs.x.ai/developers/models/grok-4.6 lists medium reasoning and short-context input/output prices of USD 2/6 per million tokens.
These support a bounded compatibility check, not a guarantee that sampling
changes as intended. Live request and receipt evidence will be reported separately.

## Later behavioural extension, not executed here

To assess associative branching, independently specify tasks that elicit
multiple relevant alternatives, measure distinct alternatives, semantic distance,
coherence and factual adherence, and compare to independent human-coded criteria.
Temperature is a decoding manipulation; it is not a validated model of hypertimia,
mania or other clinical states. Any clinical analogue requires a separate
validation protocol. Prompted personas are a distinct experimental factor.

To investigate trajectory effects, later cross dialogue-generation temperature
with decision temperature. Do not vary both together in the initial diagnostic.
