# RH-1A controlled Grok comparison

**Status:** complete. Frozen protocol/code commit: `7edd196`.
The post-hoc diagnostic was frozen separately at `21dbd79` before its calls.
Four new topic units per model; N, F, P− and P+ branches from each shared baseline.
Authority share was selected in prior outcome-blind calibration.

| Model | Condition − N | Complete | Matched | Common match | Receiver Δ all | Receiver Δ matched | Receiver Δ common | + / − / 0 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| grok-4.6__medium | F | 4/4 | 4/4 | 4/4 | +0.000 | +0.000 | +0.000 | 0 / 0 / 4 |
| grok-4.6__medium | P- | 4/4 | 4/4 | 4/4 | -0.062 | -0.062 | -0.062 | 0 / 1 / 3 |
| grok-4.6__medium | P+ | 4/4 | 4/4 | 4/4 | +0.062 | +0.062 | +0.062 | 1 / 0 / 3 |
| grok-4.20-0309-reasoning | F | 4/4 | 4/4 | 2/4 | +0.000 | +0.000 | +0.000 | 0 / 0 / 4 |
| grok-4.20-0309-reasoning | P- | 4/4 | 3/4 | 2/4 | +0.000 | +0.000 | +0.000 | 0 / 0 / 4 |
| grok-4.20-0309-reasoning | P+ | 4/4 | 2/4 | 2/4 | +0.000 | +0.000 | +0.000 | 0 / 0 / 4 |

Per-topic receiver Δ and matching (M/U), in topic order 0–3:

- grok-4.6__medium:
  - F: +0.00 (M), +0.00 (M), +0.00 (M), +0.00 (M)
  - P-: +0.00 (M), -0.25 (M), +0.00 (M), +0.00 (M)
  - P+: +0.00 (M), +0.25 (M), +0.00 (M), +0.00 (M)
- grok-4.20-0309-reasoning:
  - F: +0.00 (M), +0.00 (M), +0.00 (M), +0.00 (M)
  - P-: +0.00 (M), +0.00 (U), +0.00 (M), +0.00 (M)
  - P+: +0.00 (M), +0.00 (U), +0.00 (M), +0.00 (U)

The controlled outcome does **not** replicate across Grok versions: 4.6 changed by −0.25 under P− and +0.25 under P+ in only topic 1, whereas 4.20 had zero authority-share differences in every topic and condition. The symmetric 4.6 response is compatible with sensitivity to valenced history text; it does not establish relational path memory or hidden-state holonomy.

After seeing the controlled result, a separate **post-hoc** static instrument check queried 4.20 in 18 calibration vignettes. It returned 18/18 valid answers, 2 distinct neutral scores, neutral SD 0.125, and a partner-verified minus self-verified shift of +0.250. This meets the earlier model/probe gate (yes), so the 4.20 measure can vary in static cases. Because this check was designed after observing all-zero outcomes, it cannot change the preregistered comparison.

Δ is the receiver’s authority share under the condition minus N, on a 0–1 scale. Negative P− means less authority given to the partner. The common-match column restricts all three contrasts to identical topic units. Matching is based on six coarse self-rated endpoints, not hidden states.

Controlled-run receipted cost: $2.0007; post-hoc diagnostic: $0.0499; new total: $2.0506; uncertain reservation: $0.0000; conservative cumulative programme bound: $7.2303 under the USD 10 authorization.

Reasoning-token receipts in the controlled runs: 4.6 = 155,418; 4.20 = 169,473. The 4.6 request fixed medium effort; the 4.20 request used a dedicated reasoning model without an effort parameter. Token accounting and reasoning depth are not directly comparable.

The two Grok versions share xAI and a model family. Even agreement would be within-family robustness, not independent architecture replication. Four topics per model do not support a significance or population-level claim. No internal activations were observed.
