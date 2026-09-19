# RH-1A held-out authority probe — frozen before live responses

Date: 2026-09-19. The preceding outcome-blind calibration selected the
authority-share probe. This exploratory test uses four manuscript topics absent
from all earlier pilot and calibration runs. The four models that passed the
probe calibration are Kimi K3, Qwen3.8 Flash, Inkling, and Grok 4.6. GPT-5.4
mini is excluded because its neutral calibration scores had no dynamic range.

Each model × topic is one paired unit. Generate one two-role baseline and branch
it into N and P−, with condition execution order shuffled by a fixed local
seed. Use the established role descriptions, intervention text, six discussion
turns, four shared recovery events, and the same six integer endpoint ratings
(three per role, 0–4) as the previous RH-1A feasibility runner. A pair is
"matched" if every corresponding endpoint rating differs by at most one.
This is a coarse self-report criterion; it does not establish equality of
observable or hidden model states.

At each branch endpoint, ask each role, on a copy of its conversation, what
percentage of final wording authority over the central claim it would give its
partner without its own sign-off. Allowed JSON integer values are 0, 25, 50,
75, 100. Parse with the calibration parser; invalid or truncated responses
invalidate the paired unit. No response repair or outcome-dependent retry.
The primary descriptive contrast is the receiving role's P− share minus N
share, divided by 100. The dyad-mean contrast is secondary. Report all paired
units and the matched subset separately for each model. Also report match and
failure rates. Do not pool models as independent replications, compute a
significance claim, or infer latent-state holonomy. With four topics per model,
these are small exploratory samples. There are no F or P+ controls in this run,
so an observed difference alone cannot demonstrate relational specificity.

The previous conservative cumulative exposure is USD 3.578630. This run caps
Kimi at USD 2.50, Qwen at USD 0.50, Inkling at USD 0.80 and Grok at USD 1.50:
new exposure at most USD 5.30 and cumulative exposure below the authorized
USD 10. All credentials remain in local Notes and process memory. Public
materials contain only aggregate results; raw model exchanges stay local.
