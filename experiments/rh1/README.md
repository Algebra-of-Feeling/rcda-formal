# RH-1 local harness — implementation contract

**Status: a bounded feasibility runner and DevPass adapter are implemented.**
The broader contract below remains the target architecture. See
[PILOT_FREEZE.md](PILOT_FREEZE.md) for the smaller implemented design, deviations
and execution limits. Run locally with `python3 experiments/rh1/runner.py --output
/absolute/local/run-directory`; add `--live` only with the credential in the local
environment and a clean committed source tree. Protocol: [RH1-v1.1-design](../../RH1_PROTOCOL.md).
Parent scientific claim: H-M1.

The first live feasibility pilot is complete: [findings](results/2026-09-19/FINDINGS.md).
The separately authorized reasoning follow-up is recorded in
[REASONING_FOLLOWUP.md](results/2026-09-19/REASONING_FOLLOWUP.md). The versioned
transport supports DEV PASS and OpenRouter; the source contains no credentials.
The outcome-blind probe calibration selected the graded authority-share measure:
[protocol freeze](CALIBRATION_FREEZE.md), [operational amendment](CALIBRATION_AMENDMENT.md),
[Grok extension](GROK_EXTENSION_FREEZE.md), and
[aggregate results](results/2026-09-19/PROBE_CALIBRATION.md). The xAI adapter
supports the supplementary Grok arm; live response records stay local.
The selected probe was then used in an exploratory held-out P−/N pilot:
[frozen design](HELDOUT_AUTHORITY_FREEZE.md),
[Qwen operational amendment](HELDOUT_QWEN_AMENDMENT.md), and
[results](results/2026-09-19/HELDOUT_AUTHORITY.md). Three models completed four
paired topics each without a consistent P− effect; Qwen remained incomplete.
A controlled within-family follow-up compared Grok 4.6 with pinned Grok 4.20:
[frozen design](GROK_CONTROLLED_FREEZE.md),
[post-hoc instrument diagnostic](GROK420_POSTHOC_DIAGNOSTIC.md), and
[aggregate findings](results/2026-09-19/GROK_CONTROLLED.md). The isolated 4.6
contrast did not replicate in 4.20. Raw responses remain local.
Regenerate its descriptive tables with `python3 experiments/rh1/analysis.py
/absolute/local/run-directory /absolute/local/report-directory`.

## Proposed layout

```text
experiments/rh1/
  protocol.yaml
  scenarios/scientific_collaboration.yaml
  providers/base.py
  providers/devpass.py
  providers/local.py
  runner.py
  matching.py
  probes.py
  metrics.py
  analysis.py
```

The files above are planned modules, not a list of existing implementations;
the initial pilot combines orchestration, measurement and descriptive comparisons
in runner.py and uses pilot.json instead of YAML.
Only introduce provider-specific adapters when an actual interface requires them.
A routing service does not establish model independence or hidden-state access.

## Credential contract

The credential remains local on the Mac. Read it at runtime from an explicitly
configured environment variable or a local secret store. The environment variable
name and any Keychain service identifier must be supplied during implementation;
do not assume a DEV PASS convention.

Never put credential values in chat, GitHub, programme state, scripts, manifests,
request URLs, command-line arguments, logs, exception messages or test fixtures.
Never dump the environment, secret-store contents, request headers or raw SDK
exception objects. Logging must use an allowlist of safe fields and sanitized
errors, not serialization of the provider client. Run data stays outside the
checkout in an explicit local output directory.

For the authorized live runs, an unversioned local bridge read the exact Apple
Notes entries and passed the selected credentials to child processes in their
environment. The bridge and notes remain outside this repository; no secret
value was required in chat.
Authentication transmission must be restricted to the documented service origin;
do not forward credentials to redirects or arbitrary model-supplied URLs.

## Provider adapter contract

Before implementing devpass.py, verify the documented endpoint, request/response
schema, authentication mechanism, model identifiers, routing policy, error
semantics, rate limits and any cost information. Do not assume OpenAI-compatible
requests or invent model names.

Each adapter exposes a capability record:
- observable text output;
- internal activations and their extraction specification;
- whether a revision/fingerprint is returned;
- temperature/seed support and whether those settings were actually applied;
- token usage and cost reporting availability;
- context/cache/session behavior and whether routing fallback is possible.

RH-1A requires observable output and a recorded endpoint feature extractor.
RH-1B additionally requires real internal activations and a pinned extraction
specification. Refuse RH-1B when activations are unavailable; never substitute
text embeddings, self-reports or generated explanations as hidden states.

Record requested and resolved model separately. Disable provider fallback where
possible. A changed or unknown resolved model must be explicit and handled by a
prespecified exclusion/stratification rule. Unknown revision is null, not a
fabricated version string. Temperature zero and a requested seed are settings,
not a receipt of determinism.

## Run state and isolation

Default mode must be offline validation/dry-run with synthetic adapter fixtures.
A dry-run is orchestration validation and cannot count as experimental evidence.
Live mode requires explicit local activation, validated configuration, an allowed
model roster and hard request/token/cost budgets. No live call is authorized by
this specification.

The runner creates a baseline once, then branches contexts separately. It must
avoid state sharing between counterfactual branches or models. Pair and scenario
identifiers persist through matching, probing and analysis.

Use bounded retries with attempt identifiers. Keep failures and all attempts in
the local record, distinguishing infrastructure errors from outcomes and avoiding
duplicate trial counting. Retries can incur cost and must consume the same budget.
Write partial runs atomically and support resumption without silently repeating
completed trials.

## Safe manifest shape

This is a **non-executable example**, not a run receipt. Null means unresolved or
unavailable. A real manifest uses actual values and records capability limitations.

```json
{
  "schema_version": "rh1-manifest-v1",
  "record_kind": "design_example",
  "run_status": "not_started",
  "modality": null,
  "run_id": null,
  "pair_id": null,
  "scenario_id": "scientific_collaboration",
  "scenario_version": "RH1-v1.1-design",
  "scenario_sha256": null,
  "protocol_sha256": null,
  "router": "DEV PASS",
  "provider": null,
  "requested_model": null,
  "model": null,
  "model_version": null,
  "model_lineage": null,
  "temperature_requested": 0,
  "temperature_applied": null,
  "seed_requested": null,
  "seed_applied": null,
  "condition": null,
  "timestamp_utc": null,
  "git_commit": null,
  "git_dirty": null,
  "capabilities": null,
  "endpoint_measurement_spec": null,
  "scoring_spec_sha256": null,
  "split_id": null,
  "matching_calibration_sha256": null,
  "matching_status": null,
  "exclusion_reason": null,
  "attempt_id": null,
  "usage_tokens": null,
  "cost": null
}
```

Allowed condition codes: N, F, P-, P+. Allowed modalities: RH-1A, RH-1B.
Use actual UTC timestamps. Record unavailable token/cost information as null.
Manifests contain neither credential values nor authentication headers.
A dirty checkout needs an archived source diff/hash or a blocked run, not a
misleading clean commit pin.

## Analysis contract

- Freeze endpoint features and the delegation scoring rubric before outcomes.
- Preserve all generated trajectories, condition-specific matching/admission
  rates, exclusions, infrastructure failures and attempted costs locally.
- Use calibration data separate from outcome evaluation; no outcome-dependent
  matching thresholds, layer choices or prompt selection.
- Keep related branches, reused controls and scenario variants together in data
  partitions. Define independent units before choosing resampling procedures.
- Report effects and uncertainty per model first. Freeze the pooling/heterogeneity
  method and replication criterion before analysis; do not treat model labels or
  individual dialogue turns as independent experimental replications.
- Track P- versus N as the primary contrast. F and P+ qualify specificity and
  valence; secondary probes and layer sweeps remain labelled exploratory.
- For RH-1B, retain activation shape, dtype, layer/token selection, pooling and
  weights/runtime provenance. Cross-architecture geometric alignment is a
  separate prespecified analysis, never an implicit raw-coordinate comparison.
- A successful dry-run, HTTP response or completed job is not a positive H-M1
  result. A positive behavioural result is not a geometric holonomy certificate.

## Acceptance before the first paid call

The local implementation must demonstrate with synthetic data that branch
isolation, manifest validation, splits, retry accounting, budget stops and
credential-safe logging work. Deliberately inject a fake test secret into error
paths and verify it never reaches logs, manifests or persisted config.
Then freeze the unresolved methodological choices and explicitly authorize a
bounded live pilot. No model roster, budget or execution date is invented here.

## Context audit and proposed v0.2

See [the post-hoc audit](results/2026-09-19/CONTEXT_AUDIT.md) and
[proposed context controls](RH1A_STATE_CONTROLS_V02.md).
`audit_controlled_contexts.py --inputs DIR_46 DIR_420 --output FILE`
reproduces the structural audit offline from the saved controlled trajectories.
No new model execution is included.

The pure transformations in `context_controls.py` and historical replay in
`verify_context_controls.py` have [passed offline verification](results/2026-09-19/CONTEXT_CONTROLS.md).
They do not execute providers. Candidate request hashes are not API receipts.

[Prospective v0.2 execution freeze](CONTEXT_CONTROLS_V02_FREEZE.md): fixed fictional
scenarios, Stage A admission and budget; not executed. Integration runner pending.

[Temperature extension](TEMPERATURE_EXTENSION.md) and [completed diagnostic](results/2026-09-19/TEMPERATURE_DIAGNOSTIC.md): 12 valid calls, constant authority, returned temperatures match requests. Separate from the unexecuted v0.2 principal pilot.

[Temperature 2.0 attempt](results/2026-09-19/TEMPERATURE_MAXIMUM.md): stopped on first transport/JSON failure; no behavioural result or echoed value.

[User-authorized temperature 2.0 retry](results/2026-09-19/TEMPERATURE_MAXIMUM_RETRY.md): one valid 25% score with echoed 2.0, then a second transport/JSON failure; incomplete.

[Temperature 1.7 and medium/high attempt](results/2026-09-19/TEMPERATURE17_EFFORT.md): first medium call failed; high was not executed.

[xAI transport diagnosis](results/2026-09-19/XAI_TRANSPORT.md): configurable timeout and precise error categories; one completed empty reply, then a valid 1.7/high 50% score at cap 4096. No causal effort claim.

[Interactive Grok CLI authority probe](results/2026-09-19/GROK_TUI_AUTHORITY.md): one visible 25% response with Grok 4.6 high; temperature unverified and agent context uncontrolled. Exploratory, not an H-M1 replication.

[CLI repeatability check](results/2026-09-19/GROK_TUI_REPEAT.md): two new 25% responses; three of three including the earlier probe. One scenario, high displayed, temperature unknown.
