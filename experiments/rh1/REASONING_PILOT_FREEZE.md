# RH-1A reasoning follow-up — frozen before live generation

Date: 2026-09-19. Configuration: [reasoning_pilot.json](reasoning_pilot.json).
This is an exploratory follow-up to the first feasibility pilot. It is not a
confirmatory test of H-M1 or relational holonomy.

The two GPT-5.4 mini arms request `reasoning_effort=none` and `medium` on the
same model. Gemini 2.5 Flash requests `medium` as a second reasoning-capable
model family. The gateway catalogue must list each effort for at least one
provider mapping. Provider routing remains automatic; a catalogued capability
and accepted request do not by themselves prove that reasoning was applied.
Per-response reasoning token counts and resolved provider/model are recorded
when returned. No chain-of-thought text is logged.

Each arm uses the first two fixed topics from the original pilot and the same
four interventions, dialogue, recovery, matching and private delegation probe.
This gives six model-topic units, 24 trajectories and 348 planned calls. The
GPT `none`/`medium` contrast is a protocol comparison, not a guaranteed paired
random draw: model seeds are unavailable. Temperature is omitted because
reasoning models may reject it; determinism is not claimed. Output cap is 1536
tokens to allow reasoning. Raw outcomes may retain the earlier floor effect.

The earlier run reported USD 0.6451 plus USD 0.002754 uncertain reservation.
This follow-up caps additional reported plus reserved exposure at USD 9.00,
for less than the user's USD 10 total authorization. No top-up is allowed.
The reservation uses the highest live catalogue rate and a factor-of-two
input/output margin. One call every 0.85 seconds limits organization rate.
Missing cost, invalid output, substitution or uncertain transport stops further
use of the affected arm or entire run according to the transport.

Analysis is descriptive: endpoint matching, delegation rates and P− versus N
within each arm, plus the change in that contrast between GPT reasoning arms.
Two topic units cannot support significance or generalization. The experiment
does not access internal activations (RH-1B).

API semantics checked against the gateway's [reasoning documentation](https://docs.llmgateway.io/features/reasoning)
and [chat completions reference](https://docs.llmgateway.io/v1_chat_completions).
