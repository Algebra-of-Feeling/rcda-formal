# RH-1A v0.2 — frozen prospective pilot plan

Frozen 2026-09-19 before any calls under this plan. Status: design and fixed prompts only; execution has not begun. This is a local version-controlled freeze, not an external preregistration. Parent claim H-M1 remains open.

## Objective and selection

Investigate whether the previously observed Grok 4.6 authority pattern depends on the original intervention message or on the subsequent retained dialogue. Grok 4.6 is selected after examining v0.1; this is a targeted exploratory follow-up, not independent model replication. Grok 4.20 is outside this round. No claim about latent holonomy is an outcome of this protocol.

Two new fictional scenarios specify evidence and candidate wordings in advance: soil-moisture calibration transfer between farms and acoustic/manual pollinator count agreement. Numerical facts are synthetic. Each topic is crossed with receiver A and receiver B, producing four blocks. Roles retain their historical cautious/ambitious distinction. The intervention is about trust in the recipient's judgment and influence over wording; it is suitable for either role.

All exact system, scenario, intervention, recovery and measurement text is in `context_controls_v02_prompts.json`. N/F/P−/P+ messages share an opening. P− and P+ differ in trust and influence valence; N and F differ in decision relevance. These are controls, not a claim of perfect salience or semantic matching.

## Stage A: repeated-input calibration

Make six independent authority calls for each of the four scenario × role cells using its fixed canonical briefing: 24 calls maximum. Interleave cells by repetition; do not append earlier answers. All repetitions within a cell must have identical candidate payload hashes. Condition labels are absent from the model input.

Admission rule: all 24 outputs must be valid and at least three of four cells must have authority range no greater than 0.25. If the rule fails, stop after Stage A and report instability; do not loosen it or choose a preferred subset. A transport, schema, truncation or cost-receipt failure stops immediately. Range 0.25 is an operational tolerance chosen for this pilot, not a validated precision threshold. Passing does not establish deterministic behaviour.

Stage A estimates repeated-probe variation only. It does not estimate variation from regenerating a dialogue. Its cells will be reused as canonical inputs in Stage B and cannot be presented as an independent replication.

## Stage B: four exploratory blocks

If Stage A passes, run exactly four resource-bounded blocks. The size is fixed for feasibility, not selected as a powered sample; a confirmatory sample size remains undecided. This clarifies the earlier design suggestion to calibrate before sizing: only a future inferential study will use calibration to justify sample size.

For each block: generate two shared baseline turns, A then B. Fork identical baseline contexts into four conditions and deliver exactly one private intervention to the designated recipient. Produce six alternating A/B dialogue turns and four alternating recovery turns. Add each recovery event to both contexts before the scheduled speaker replies. This preserves the earlier conversational schedule; topic × receiver is now crossed.

Measure three task endpoint scores separately for each role from copies of the final full-history context. These are six approximate task ratings, not complete states. Do not append ratings to conversation history. For the recipient only, measure authority twice in each of three context modes, on independent copies, without feeding any probe answer back:

- Full history: entire context plus the authority probe.
- Remove intervention: delete exactly the standalone user intervention message; preserve every other message. Missing or duplicate matches halt execution.
- Canonical reset: fixed role, fixed scenario briefing and probe only. No generated conversation or condition label. Across conditions, payload hashes must match within each model × scenario × role cell.

Calls per block: 2 shared baseline + 4 × (6 dialogue + 4 recovery + 2 endpoints + 3 modes × 2 probes) = 74. Four blocks = 296 calls; Stage A + B = at most 320. There are 16 generated branches, 96 Stage B probe calls, and four block units; probe repetitions and conditions are not independent samples.

## Order and parameters

Configuration fixes block order and a four-row Latin order for conditions. Mode order cycles over the three modes using (block index + condition position + repetition index) modulo 3. Calls are serial. Probe repetition index is the outer loop and mode order the inner loop. Dialogue speaker alternation is not randomized; disclose this constraint.

Requested model: `grok-4.6`, medium reasoning, maximum output 1536 tokens. This is the identifier used in previous receipts, not an immutable weights revision. Record the actual returned model and halt if it differs. Omit unsupported or previously unused temperature/seed fields rather than inventing their behaviour. The configuration seed records scheduling reproducibility; the stated schedules are deterministic and it is not a model-generation seed. Record code commit, config/prompts hashes, candidate-input hashes, timestamps, exact supported parameters and returned usage. No hidden reasoning content or secrets are recorded.

## Analysis fixed before execution

Average the two authority responses within each block × condition × mode cell. The primary contrast is P− minus N for the recipient under full history, then an equal-weight mean across four blocks. Also report each block and the two topic means. Report F/N and P+/N regardless of sign. Secondary contrast: (P− minus N after removal) minus (P− minus N with full history), paired by block. Report canonical contrasts as negative-control diagnostics, not estimated relational memory.

An absolute mean difference of 0.125 is a descriptive reference chosen for planning (half one response category). It is not a scientific minimum established from evidence, an eligibility gate or a confirmation threshold. With only two topics, do not report a population confidence interval, significance test or general replication claim. Report both individual probe responses, their observed ranges, all block effects and between-topic variation. These ranges are not confidence intervals.

Use all valid paired blocks in primary summaries. Report matching with tolerance one and exact equality of six endpoint ratings descriptively; do not condition primary inclusion on this post-intervention measurement. No O versus O+H predictive model is fitted in this small pilot. There is no test of causal mediation or hidden-state equality.

For partial execution, show a planned-versus-observed cell inventory. Missing values are missing, never zero. Report complete contrasts with explicit denominators, but do not claim the four-block result if fewer than four complete. No replacement scenarios, reruns after a disappointing result, or adaptive model switch.

## Budget and stops

Previously recorded conservative exposure: USD 7.230302540700002. New hard ceiling: USD 2.50 including both stages and unresolved request reservations. Maximum cumulative bound: USD 9.730302540700002, below the existing USD 10 authorization. Cost estimates do not guarantee all planned calls will fit; an honest incomplete run is permitted.

Before any live call, verify model availability and current billing rules, implement a shared reservation ledger, and stop before a request whose conservative reservation would exceed the remaining ceiling. A timeout retains its unresolved reservation. Stop on invalid/truncated responses, model substitution, absent/invalid cost receipts, transport uncertainty or exhausted budget. No automatic paid retries. Credentials remain local and are read only at execution time; this planning step reads none.

## Execution readiness

The pure context transformations already passed offline historical checks. This plan still needs a prospective runner integrating the exact prompt schedule, Stage A admission, shared budget, failure stops and predetermined analysis. Verify that integration with synthetic transport and boundary tests before live execution; synthetic answers must never enter scientific results. The present freeze does not claim the runner is complete or that model calls occurred.

Next milestone: implement that runner and validate it offline against this frozen plan. A later live run must identify the final source commit and prompt/config hashes before the first call. Any necessary design change requires a dated amendment before affected calls.
