# RH-1A held-out authority-share pilot

**Run status:** incomplete. The protocol was frozen at commit `e9fba4e` before live responses.
The Qwen serial continuation was frozen at `c4cd14c` before its fresh arm.
Four new topics, four medium-reasoning models, paired N/P− trajectories.
Authority share was selected in a separate outcome-blind calibration.

| Model | Complete pairs | Matched | Receiver Δ all | Receiver Δ matched | Dyad Δ all | + / − / 0 |
|---|---:|---:|---:|---:|---:|---:|
| kimi-k3__medium | 4/4 | 4/4 | -0.062 | -0.062 | -0.125 | 0 / 1 / 3 |
| qwen3.8-flash__medium | 1/4 | 0/1 | -0.250 | NA | -0.125 | 0 / 1 / 0 |
| inkling__medium | 4/4 | 4/4 | +0.062 | +0.062 | +0.031 | 1 / 0 / 3 |
| grok-4.6__medium | 4/4 | 4/4 | -0.062 | -0.062 | +0.000 | 0 / 1 / 3 |

Receiver differences by topic index (0–3), with `M` for matched and `U` for unmatched:

- kimi-k3__medium: +0.00 (M), +0.00 (M), +0.00 (M), -0.25 (M)
- qwen3.8-flash__medium: -0.25 (U), —, —, —
- inkling__medium: +0.25 (M), +0.00 (M), +0.00 (M), +0.00 (M)
- grok-4.6__medium: +0.00 (M), -0.25 (M), +0.00 (M), +0.00 (M)

Among the 12 complete Kimi/Inkling/Grok pairs, nine receiver contrasts were
zero, two were −0.25 and one was +0.25. The nonzero contrasts occurred in
different topics. This small run does not show a consistent P− effect across
models. Qwen's sole completed contrast was unmatched and cannot fill the
missing three topic pairs.

Medium reasoning was requested for every model. Provider receipts recorded
16,373 reasoning tokens for complete Kimi, 41,272 for complete Inkling and
84,079 for complete Grok. The incomplete fresh Qwen arm recorded 8,849
reasoning tokens across 41 billed responses. These counts establish use of
reasoning tokens, but provider token accounting is not directly comparable.

Δ is P− minus N on a 0–1 scale; negative means less authority given to the partner after P−. The receiving role is the primary unit-level measure. Matching uses six self-rated endpoints with coordinate tolerance one. Reported all-unit and matched-subset means are descriptive.

New receipted cost including the excluded first Qwen attempt: $1.5860; uncertain reservation: $0.0150; conservative cumulative programme bound: $5.1797 versus the authorized $10 ceiling.

The first Qwen attempt had a transport failure before any complete pair. The fresh serial arm follows the frozen operational amendment; the initial responses are excluded from scientific analysis but retained in the cost and local evidence.

There are no F or P+ controls in this run. A P−/N difference cannot by itself demonstrate relational specificity. Four topic pairs per model are insufficient for a robust population-level or cross-model inference. No hidden activations were observed; this is RH-1A behaviour only, not RH-1B or geometric holonomy.

Incomplete model arms or invalid measurements must remain visible; do not treat missing units as zero effects.
