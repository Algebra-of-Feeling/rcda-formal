# Temperature 2.0 — user-authorized retry, 2026-09-19

The user requested continuation after the initial maximum-temperature attempt
failed with transport_or_json_failure. This authorizes one fresh bounded run,
not an automatic retry loop. Use the unchanged --maximum schedule: Grok 4.6,
medium reasoning, temperature 2.0, two canonical contexts, two repeats each,
1536 output-token maximum and four calls maximum. Keep timeout and prompts
unchanged. Stop on the first failure. No other provider or temperature fallback.

The first failed run remains part of the evidence with USD 0.035044 unresolved
reservation. Previous conservative programme bound: USD 7.3279145407.
Fresh run cap USD 0.15. Including the separate v0.2 reservation of USD 2.50,
maximum combined bound USD 9.9779145407, below the authorized USD 10.

Report this run separately and disclose the failed earlier attempt. Do not
pool failed/missing measurements as zero scores, erase the first reservation,
or infer a causal temperature effect from transport failure. This is still an
exploratory measurement diagnostic, not a clinical or confirmatory experiment.
