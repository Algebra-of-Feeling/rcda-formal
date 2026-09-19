# Grok calibration extension — frozen before xAI calls

Date: 2026-09-19. The user requested Grok from xAI as an additional model.
Run the same 54 static calibration tasks, in the same seeded order, with the
unchanged prompts, JSON parser, anchors and scoring. Use `grok-4.6` directly
through the xAI Responses API with medium reasoning and a 1536-token output
cap. It is a fifth, supplementary model; the original four-model probe
selection rule in `CALIBRATION_FREEZE.md` remains primary. Report its validity,
neutral range and anchor shift using the same pass criterion. A supplementary
four-of-five sensitivity check may be reported, but it cannot reverse the
pre-registered four-model selection or justify an RH-1 path-memory claim.

Only the local Apple Note titled `GROK X AI API KEY` supplies the credential.
The credential passes in process memory and is never logged or versioned. The
new xAI spending ceiling is USD 1.50. Together with the prior programme bound
of USD 2.38, the DEV PASS ceiling of USD 3.50 and OpenRouter ceiling of USD
1.50, maximum exposure is below the user's USD 10 pilot authorization.

Model, reasoning and billing fields were checked in the official
[xAI model documentation](https://docs.x.ai/developers/grok-4-6),
[reasoning documentation](https://docs.x.ai/developers/model-capabilities/text/reasoning)
and [cost tracking documentation](https://docs.x.ai/developers/cost-tracking).
