# RH-1A reasoning candidate extension — frozen before live generation

Date: 2026-09-19. Configuration: [candidate_pilot.json](candidate_pilot.json).
This extension tests Qwen3.8 Flash and Kimi K3 via DEV PASS and Inkling via
OpenRouter, all requesting medium reasoning effort. Their model identifiers
were verified in live catalogues. One short preflight request per candidate
returned nonzero reasoning tokens, including 39 for Inkling. Preflights are
separate from experimental trajectories and do not enter analysis.

Each model gets the same two fixed topics, N/F/P−/P+ interventions, dialogue,
recovery, endpoint matching and private delegation probe as the earlier
reasoning pilot. There are 116 planned calls per model, 348 total. Provider
and vendor effects are confounded; this is a cross-model feasibility survey.
Reasoning effort is requested; nonzero reported reasoning tokens verify that
at least some requests used it, while any missing token count stays unknown.

Incremental software spending ceilings are USD 2 on DEV PASS and USD 2 on
OpenRouter. The earlier pilot accounted for about USD 0.648 and the first
reasoning comparison has its own observed cost receipt. Together these caps
remain below the user's USD 10 total ceiling. No balance purchase or top-up
is authorized. OpenRouter uses the paid Inkling listing rather than the free
research endpoint. Local Apple Notes keys remain outside the repository and
are passed to the child process only through its environment.

This remains exploratory and has only two topic units per model. No p-values,
generalization, state-holonomy or RH-1B claim follows from it.

Sources: [OpenRouter model catalogue](https://openrouter.ai/docs/api/api-reference/models/get-models),
[OpenRouter reasoning request](https://openrouter.ai/docs/api/api-reference/presets/create-presets-chat-completions),
[Thinking Machines Inkling model card](https://thinkingmachines.ai/model-card/inkling/).
