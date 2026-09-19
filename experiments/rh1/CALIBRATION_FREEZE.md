# RH-1A probe calibration — frozen before live responses

Date: 2026-09-19. Configuration: [calibration_config.json](calibration_config.json).
This is an instrument-calibration run, not a path-memory test. It uses three
new manuscript topics, neither of the outcome-evaluation topics. There are no
P− or P+ history interventions and no comparison of path effects. All prompts
are static vignettes, distinct from the generated dyads in the pilot.

For each topic, both roles A and B answer three candidate probes under three
task-evidence anchors: neutral (neither has independently rerun the analysis),
partner verified (partner independently reproduced the analysis), and self
verified (the respondent independently reproduced it while the partner has not
reviewed it). These anchors test whether the instrument responds to a clear
task-relevant change. They do not calibrate the RH-1 matching threshold.

The candidate probes are: the prior binary delegate/joint-review choice; a
0/25/50/75/100 percent share of final wording authority ceded to the partner;
and 0/15/30/45/60 minutes of independent verification within a fixed hour.
Scores are 0 or 1, authority_share/100, and 1 minus verification_minutes/60.
Higher scores mean greater reliance on the partner. Responses are parsed as
JSON. Exactly one fenced JSON block may be extracted from surrounding prose;
missing, ambiguous or out-of-range values are invalid. No automatic response
repair or scientific outcome-dependent retry is permitted.

There are 3 topics × 3 anchors × 2 roles × 3 probes = 54 calls per model, 216
planned. Models are GPT-5.4 mini, Kimi K3 and Qwen3.8 Flash via DEV PASS, plus
Inkling via the paid OpenRouter listing; all request medium reasoning effort.
Models and provider routes may still differ. No model seed is requested. Task
order is shuffled with the fixed local seed. Independent calls may execute
concurrently; the prompt and scoring rules are unchanged by completion order.

Selection uses only calibration responses. For a model/probe to pass: at least
90% of 18 calls must parse; among its six neutral scores at least two distinct
values must occur; and mean score for partner-verified cases must exceed mean
score for self-verified cases by at least 0.10. A probe is eligible if at least
three of four models pass. Select the eligible probe with the most passing
models; break ties by the mean neutral-score standard deviation across models,
then by fixed order authority_share, verification_minutes, binary_delegate.
If none is eligible, select nothing and redesign the measurement on separate
calibration data. Do not look at P−/N effects when choosing.

The already authorized USD 10 ceiling covers the whole programme pilot. The
previous runs account for under USD 2.38 including uncertainty. This run caps
new DEV PASS exposure at USD 2.00 and OpenRouter at USD 1.50, leaving ample
headroom. Keys are passed from local Apple Notes by unversioned bridges into
child-process environments; never save key values, headers or raw errors.

Gateway parameter semantics and usage receipts were checked against
[LLM Gateway reasoning](https://docs.llmgateway.io/features/reasoning) and
[OpenRouter chat completions](https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request).
