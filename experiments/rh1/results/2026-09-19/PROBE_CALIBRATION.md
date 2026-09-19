# RH-1A probe calibration: results

Source protocol and code were committed before the first call at `5f64574`;
the isolated continuation was frozen at `a6feead`, and the user-requested
Grok extension at `ff17a8f`. Raw request and response receipts remain in the
local evidence bundle, separate from the public repository. All five complete
model arms contain 54 unique prompt cases; the initial stopped Kimi/Qwen arms
are retained only as operational evidence.

This is calibration of a behavioural measurement, not an RH-1 path-dependence test.
The prompts contain no P− or P+ history. Three new manuscript topics and three task-evidence anchors were used.

**Primary four-model selection:** authority_share.
**Supplementary four-of-five sensitivity (including Grok):** authority_share.

Every complete arm requested medium reasoning. Provider receipts report
reasoning tokens: GPT-5.4 mini 9,995; Kimi K3 39,714; Qwen3.8 Flash 23,909;
Inkling 23,261; and Grok 4.6 39,165. These totals confirm that reasoning was
used, but token accounting and model behaviour are not directly comparable
across services. The underlying model revision was not uniformly exposed.

| Model | Probe | Valid / 18 | Neutral values | Neutral SD | Partner − self | Pass |
|---|---|---:|---:|---:|---:|---|
| gpt-5.4-mini__medium | binary_delegate | 18/18 | 1 | 0.000 | -1.000 | no |
| gpt-5.4-mini__medium | authority_share | 18/18 | 1 | 0.000 | +0.458 | no |
| gpt-5.4-mini__medium | verification_minutes | 18/18 | 1 | 0.000 | +0.125 | no |
| kimi-k3__medium | binary_delegate | 18/18 | 1 | 0.000 | +0.000 | no |
| kimi-k3__medium | authority_share | 18/18 | 3 | 0.186 | +0.333 | yes |
| kimi-k3__medium | verification_minutes | 18/18 | 3 | 0.144 | +0.125 | yes |
| qwen3.8-flash__medium | binary_delegate | 18/18 | 1 | 0.000 | +0.000 | no |
| qwen3.8-flash__medium | authority_share | 18/18 | 4 | 0.267 | +0.458 | yes |
| qwen3.8-flash__medium | verification_minutes | 18/18 | 3 | 0.250 | +0.083 | no |
| inkling__medium | binary_delegate | 18/18 | 1 | 0.000 | +0.333 | no |
| inkling__medium | authority_share | 18/18 | 4 | 0.267 | +0.250 | yes |
| inkling__medium | verification_minutes | 18/18 | 3 | 0.186 | +0.000 | no |
| grok-4.6__medium | binary_delegate | 18/18 | 1 | 0.000 | +0.000 | no |
| grok-4.6__medium | authority_share | 18/18 | 2 | 0.186 | +0.458 | yes |
| grok-4.6__medium | verification_minutes | 18/18 | 3 | 0.186 | +0.042 | no |

A pass requires at least 90% valid responses, at least two distinct scores among six neutral cases, and partner-verified mean at least 0.10 above self-verified mean. The original four-model rule requires three models to pass; the supplementary five-model check requires four.

Initial Kimi responses excluded: 7 valid before transport stop. Initial Qwen pseudo-rows were never sent to its model and are excluded.
Fresh Kimi and Qwen arms were run separately under the documented operational amendment.

Costs are per-request provider receipts; a prior-programme bound is included for perspective.
New reported calibration cost: $1.1992. Conservative programme upper bound including earlier runs: $3.5786.

The new cost includes the discarded operational Kimi attempts. Receipted
costs for the complete arms were GPT-5.4 mini $0.0545, Kimi K3 $0.6507,
Qwen3.8 Flash $0.0131, Inkling $0.0956, and Grok 4.6 $0.2888; the stopped
initial DEV PASS run added about $0.0965 for Kimi.

This calibration cannot establish relational holonomy, latent-state effects, or a causal P−/N difference. A selected probe, if any, must be evaluated on held-out RH-1A data.
