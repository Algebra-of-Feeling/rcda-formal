# DEV PASS authority diagnostic resumed — 2026-09-20

The four-call C++23 block frozen in [DEVPASS_AUTHORITY_RESUME_FREEZE.md](../../DEVPASS_AUTHORITY_RESUME_FREEZE.md) completed in the exact order Kimi, Qwen, Qwen, Kimi. Every call used the same stateless `soil_sensor_transfer` canonical briefing and role-A authority probe from `context_controls_v02_prompts.json`, medium effort requested, no temperature or seed requested, and no tools. Both model IDs were present in the live catalogue before inference. The local Apple Notes key remained in memory, was sent only to LLM Gateway, and was not logged or committed.

| Order | Requested model | Gateway reported provider | Gateway reported underlying model | Authority | Reported cost USD |
|---|---|---|---|---:|---:|
| 1 | `kimi-k3` | `runpod` | `kimi-k3` | 25% | 0.00472500 |
| 2 | `qwen3.8-flash` | `alibaba` | `qwen3.8-flash` | 25% | 0.00017648 |
| 3 | `qwen3.8-flash` | `alibaba` | `qwen3.8-flash` | 25% | 0.00018729 |
| 4 | `kimi-k3` | `runpod` | `kimi-k3` | 25% | 0.00364380 |

All four completed with `finish_reason: stop` and a valid final JSON `authority_share: 25`. The gateway metadata reported the requested model IDs without substitution; its underlying version string matched the same ID, not a pinned model revision. No temperature, seed, or applied effort value was independently returned, so those controls remain unverified beyond the sent request. Provider names are gateway metadata, not direct upstream attestations.

An [ADR009 C++23 verifier](../../verify_devpass_authority.cpp) checked the sequence, scores, model metadata and exact integer tick costs from the saved local receipt. It found Kimi cost 83,688,000 ticks (USD 0.00836880), Qwen 3,637,700 ticks (USD 0.00036377), and block total 87,325,700 ticks (USD 0.00873257). No uncertain reservation was added. Combined conservative historical exposure is 76,516,631,107 ticks (USD 7.6516631107); including the separate USD 2.00 prospective v0.2 reserve gives USD 9.6516631107. The unused USD 0.19126743 from this block cap is released. Subscription credit application was not independently verified.

This is a completed cross-model **static authority diagnostic**, not the path-dependence test: no counterfactual histories, intervention P-/N comparison, matched observable state, or latent activations were measured. Agreement at one coarse score across four calls does not establish model equivalence or H-M1. It does confirm that the gateway can deliver valid scored responses from both requested model IDs in this controlled prompt format. The principal prospective v0.2 remains unexecuted.
