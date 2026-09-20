# DEV PASS RH-1A authority diagnostic, small resumed block

Freeze before inference. Four fresh, stateless chat completions in order
`kimi-k3`, `qwen3.8-flash`, `qwen3.8-flash`, `kimi-k3`. Use the exact
`system_by_role.A`, `scenario_inputs.soil_sensor_transfer.canonical_briefing`
and `probe` strings from `context_controls_v02_prompts.json`, as system, user,
user messages. `reasoning_effort: medium`; temperature and seed omitted. Request
2048 maximum completion tokens, no tools, streaming disabled.

Each completed response must contain a final JSON `authority_share` in
{0,25,50,75,100}, a supported finish reason, cost metadata, and no reported
model substitution. Preserve gateway-reported provider/version if available;
unknown values stay unknown. Stop on the first invalid output, transport failure,
missing cost, or budget guard. No retries or replacement calls. At most four
requests, hard incremental reported-cost guard USD 0.20. Combined conservative
historical exposure USD 7.6429305407 plus the separate v0.2 reserve USD 2.00
and this new cap = USD 9.8429305407, within the user's USD 10 authorization.
If a call fails before cost is returned, retain the unspent cap as uncertain
exposure rather than claiming zero billing.

The intended summary is scores and final-output success by requested model,
with descriptive comparisons only. This is not a paired-history RH-1 test,
latent-state measurement, preregistered H-M1 confirmation, or direct comparison
with the Grok CLI because channels and upstream routing differ.

The local Notes key stays in process memory and is never printed or saved. C++23
performs the execution, JSON parsing and numerical accounting under ADR009.
The current DevPass provider is smart-routed, so an upstream provider or exact
version not returned in metadata cannot be inferred from the requested ID.
