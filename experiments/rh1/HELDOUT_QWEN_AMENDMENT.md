# Held-out Qwen operational restart — frozen before continuation

Date: 2026-09-19. In the first Qwen3.8 Flash held-out arm, two concurrent
dialogue requests failed with `transport_or_json_failure` during unit 0. No
paired unit, endpoint or authority-share outcome was produced. The transport
halted after six attempts. Its four successful replies are baseline/early
dialogue only and will not be used in scientific analysis. The reported cost
was USD 0.000511, with USD 0.008547 reserved as uncertain exposure.

Start a **fresh four-topic Qwen arm** with the unchanged protocol and seeded
condition order, but execute N and P− branches sequentially rather than
concurrently. This is an operational stability change, not an outcome-driven
probe change. No prompts, intervention, model, reasoning effort, matching rule,
receiver contrast or scoring rule change. Do not mix responses from the first
attempt with the fresh arm. If the fresh arm fails, report it as incomplete;
do not retry individual responses.

The fresh Qwen arm has a USD 0.40 cap. Even if the entire original USD 0.50
Qwen reservation and the fresh USD 0.40 were spent, the prior programme bound
plus all held-out model caps would remain below the authorized USD 10.
