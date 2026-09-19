# RH-1A feasibility pilot — frozen before live generation

Date: 2026-09-19. Configuration: [pilot.json](pilot.json).
This is a small operational pilot, not the full RH-1 v1.0 design and not a
confirmatory test. User-authorized total spend ceiling: USD 10. No auto top-up,
subscription change or purchased reset is permitted.

## Fixed design

- Three catalogued model families: GPT-4.1 mini, dated Claude Haiku 4.5, Gemini
  2.5 Flash Lite. These are model-family comparisons, not proof of independent
  training lineages. DevPass routes providers automatically.
- Four fixed manuscript-topic units per model, each sharing a two-turn generated
  baseline before branching into N, F, P-, P+. Forty-eight trajectories total.
- Separate role contexts. Only the intervention receiver sees the private message;
  receiver alternates B/A by unit. Six alternating post-intervention turns and
  four shared recovery events, with one response per event.
- Two endpoint measurements on context copies; two independent private delegation
  probes on copies of the unmeasured endpoint. Measurement outputs do not feed
  the probe. Responses are capped at 384 tokens; truncated outputs are invalid.
- Branch ordering is randomized with fixed local seed 20260919. No API model seed
  is requested: the inspected gateway schema exposes no seed field. Temperature
  requested is zero; applied temperature and determinism are not verified.
- 696 planned completion calls; cap 720; maximum three simultaneous calls. No
  automatic retries. Transport/cost/model-substitution failures stop the run;
  malformed measurement JSON invalidates the affected model's remaining units.

## Matching and primary descriptive contrast

Endpoints are self-reported task agreement, evidence uncertainty and readiness,
each an integer 0–4. A pair is matched if every coordinate differs by at most one
for both roles. This is a **fixed coarse feasibility threshold**, not a calibrated
equivalence margin or validation of complete individual-state matching. Trust is
not part of matching; unmeasured trust differences can explain delegation effects.

Outcome: each role independently chooses delegate=1 or joint_review=0; the dyad
score is their mean. Primary contrast is within-unit P- minus N. Report matched
and all-unit differences separately, plus admission rates. F and P+ contrasts are
descriptive controls. Shared controls are not independent data points. There is
no fitted incremental-prediction model, p-value, significance claim or causal
mediation estimate in this small pilot.

## Deviations from full RH-1

The pilot uses two generated baseline turns, four topic units per model, a fixed
ordinal matching tolerance instead of a repeatability-calibrated percentile, and
private structured choices instead of an unrestricted joint decision dialogue.
No secondary probes, hidden states, layer sweeps or context-reset arm are run.
The sample is for feasibility and score-range inspection; model/dyad/scenario
generalization and held-out predictive replication remain future work.

## Local evidence and cost boundaries

Manifests record the clean git commit and source hashes. Local run directories
hold prompts/contexts, measurement outputs, request identifiers, resolved models,
providers and allowlisted costs. Credentials are read from RH1_GATEWAY_KEY only;
the local Notes bridge is outside the repository and passes the key in memory.
No environment dump, credential hash, raw error body or auth header is persisted.

Before each request the shared budget reserves a conservative byte-based input
estimate and maximum output charge using the most expensive listed provider rates
with a factor-of-two margin. After success, reported cost settles the reservation.
Missing cost or uncertain billing stops further scheduling. The software ceiling
depends on the gateway honoring the documented rates and output cap; it is not
a server-side account spending limit. The run records uncertain reservations.

Docs checked before execution:
- [Gateway API](https://docs.llmgateway.io/developers)
- [Chat completions and metadata](https://docs.llmgateway.io/v1_chat_completions)
- [DevPass usage](https://docs.llmgateway.io/developers/devpass-usage)
- [DevPass routing](https://docs.llmgateway.io/learn/model-categories)

The initial catalogue is saved locally. Pilot results do not prove H-M1,
geometric holonomy, an independent C state or RCDA-specific mechanisms.
