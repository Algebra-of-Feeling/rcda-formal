# RCDA / RCDB — canonical programme state

Snapshot date: 2026-09-19. Repository: https://github.com/Algebra-of-Feeling/rcda-formal

## Start here

The programme is **Álgebra do Sentir / Algebra of Feeling**.
RCDA means **Relational Cayley–Dickson Algebra**; RCDB means **Relational Cayley–Dickson Bundle**.
The conceptual genealogy recorded in the conversation is 168 → Octonionic Loop → Álgebra do Sentir → RCDA/RCDB; this is programme history, not a priority finding.

This repository is the canonical published snapshot. Chat proposes and explains;
a Work produces artifacts; verified, committed sources and receipts determine the
published formal state. New Work edits do not enter this snapshot automatically.

## Index

| Record | Role |
|---|---|
| [Proof Ledger](PROOF_LEDGER.md) | Stable P-*/C-*/H-* IDs and exact evidence boundaries |
| [Lean source](RCDA.lean), [catalogue](Audit.lean) | Machine-checked mathematics and tagged declarations |
| [Dependency map](DEPENDENCIES.md), [audit](AUDIT.md) | Premises, dependencies and limitations |
| [Receipt](verification/receipt.json), [axioms](verification/axioms.log) | Reproduced local Lean verification |
| [Import provenance](verification/import-provenance.json) | Exact archive digest and imported-file digests |
| [RH-1 protocol](RH1_PROTOCOL.md) | Preserved conceptual design plus unresolved operational choices |
| [RH-1 harness](experiments/rh1/README.md) | Implemented bounded RH-1A feasibility runner and broader RH-1A/RH-1B target contract |
| [Pilot freeze](experiments/rh1/PILOT_FREEZE.md) | Pre-execution design, matching, models, deviations and USD 10 ceiling |
| [RH-1A pilot findings](experiments/rh1/results/2026-09-19/FINDINGS.md) | Completed 48-trajectory feasibility run; no replicated relational-specific effect |
| [Reasoning follow-up](experiments/rh1/results/2026-09-19/REASONING_FOLLOWUP.md) | Exploratory GPT effort comparison and Inkling/Kimi/Qwen attempts; no consistent relational-specific effect |
| [Probe calibration](experiments/rh1/results/2026-09-19/PROBE_CALIBRATION.md) | Outcome-blind measurement calibration; graded authority share selected; Grok supplementary |
| [Held-out authority pilot](experiments/rh1/results/2026-09-19/HELDOUT_AUTHORITY.md) | Exploratory P−/N test of selected probe; three complete model arms, Qwen incomplete; no consistent replicated effect |
| [Controlled Grok comparison](experiments/rh1/results/2026-09-19/GROK_CONTROLLED.md) | Grok 4.6 versus pinned Grok 4.20 with N/F/P−/P+ controls; no cross-version replication; post-hoc 4.20 probe diagnostic |
| [Context audit](experiments/rh1/results/2026-09-19/CONTEXT_AUDIT.md) | Post-hoc audit of all 32 controlled trajectories; retained intervention in every receiver context; coarse matching does not certify equal state |
| [State-control design v0.2](experiments/rh1/RH1A_STATE_CONTROLS_V02.md) | Proposed full-history, message-removal and canonical-reset controls; not executed |
| [Formal Methods Note](FORMAL_METHODS_NOTE.md) | Manuscript skeleton; unpublished |
| [Sounio layer](sounio/README.md) | Imported finite runtime witnesses, distinct from universal Lean proofs |

## Verified scope of this import

- Source: exported rcda-lean.zip from task `01a0badb-a3f0-7523-97af-ae65ba63dbf2`, “Formalize RCDA RCDB core in Lean”.
- The exported snapshot contains 11 Lean files, 26 tagged theorem catalogue entries and six textual scientific hypotheses. Counts refer to different inventories; generated Lean declarations are not original research-result counts.
- Fresh isolated verification passed under Lean 4.33.0: source gate, build and transitive axiom audit. No Mathlib or external packages; no project axiom declarations or admitted proofs.
- Foundational logical axioms used by the overall development: Classical.choice, Quot.sound and propext. “No project axioms” does not mean absence of all logical axioms.
- Sounio receipts are historical evidence imported from that Work, not rerun here. No universal source-to-binary refinement or compiler-correctness theorem is claimed in this snapshot. Compiled ELF artifacts are excluded.
- The source task was actively extending SounioBridge/IntegerBounds during import. Those working edits were not in this archive and are not certified by this snapshot.
- At initial kernel import, no experiment was recorded. The subsequent bounded RH-1A feasibility pilot, exploratory reasoning follow-up, outcome-blind probe calibration, held-out authority pilot and controlled Grok comparison are recorded (see findings). The full RH-1 protocol and RH-1B remain unexecuted; no confirmatory path-memory test, publication or novelty/priority verification is recorded.
- These are local verification receipts, not a GitHub Actions CI result.

## Stable claim policy

P-* identifies proved mathematical content under explicit premises; it requires a declaration/evidence mapping.
C-* identifies model consequences or interpretations; explicitly distinguish a compiled conditional theorem from a semantic interpretation without a Lean measurement map.
H-* identifies an empirical hypothesis, never a theorem or axiom.
Do not renumber established IDs to hide changes. Record status corrections and keep the historical ledger.

Editorial example: **Formal basis: P-SE1. Model interpretation: C-SE1. Empirical test: H-SE1.**

## Resume procedure

1. Read this file, PROOF_LEDGER.md and the latest git commit.
2. Run `python3 scripts/verify.py` for any change to the formal snapshot.
3. Compare source hashes before importing another Work; do not combine unverified working files with older receipts.
4. Update this index and affected claim mappings together with source changes.
5. Before experiments, close the operational decisions in RH1_PROTOCOL.md and explicitly authorize execution.

## Immediate next checkpoint

RH1-v1.1-design distinguishes behavioural replication (RH-1A) from internal-state
replication (RH-1B), both under H-M1. A smaller RH-1A feasibility pilot is now
implemented and frozen before execution, with an authorized USD 10 ceiling.
The LLM Gateway API contract, catalogue and DevPass key status were checked.
Credentials remain local and never enter programme documents, versioned scripts,
manifests or logs. The live pilot completed 48 trajectories with 696 successful
responses and one rate-limit rejection (697 attempts). Response-reported cost:
USD 0.645100, plus USD 0.002754 retained as a conservative uncertain reservation.
All 12 primary P-/N pairs passed the fixed coarse matching rule. GPT/Claude had
zero delegation throughout; Gemini showed a small negative P-/N difference also
present in controls. This is not replicated support for a relational-specific
effect, and does not refute H-M1. The separately authorized reasoning follow-up
compared GPT-5.4 mini at `none` and `medium`, and ran reasoning-enabled Inkling,
Kimi K3 and Qwen3.8 Flash. The GPT reasoning-token receipts differed (0 versus
8,629), but delegation was zero throughout both arms. Inkling was also at the
delegation floor. Kimi and Qwen varied, yet controls and matching outcomes did
not show a consistent P−-specific effect. Gemini 2.5 Flash stopped on an
invalid measurement and has no paired outcome. See the linked follow-up for
denominators, operational deviations and cost accounting. Calibrate probe
sensitivity on separate data before scaling. That calibration has now run on
three new static topics without P− or P+ histories. Its frozen criterion
selected graded authority share: Kimi, Qwen and Inkling passed the original
four-model rule; Grok 4.6 passed the supplementary fifth-model check. GPT-5.4
mini remained at a neutral-score floor. All five complete arms had 54 valid
responses; an initial shared-gateway Kimi truncation and its blocked Qwen
attempt were excluded and replaced by isolated, complete arms under a frozen
operational amendment. The new receipted cost was USD 1.199234, and the
conservative cumulative programme bound was USD 3.578630 under the authorized
USD 10 ceiling. This selected an instrument, not an H-M1 effect. The selected
probe was then tested on four new paired P−/N topics per model. Kimi, Inkling
and Grok completed all four pairs per model, all matched; nine of their 12
receiver contrasts were zero, two were −0.25 and one was +0.25, occurring in
different topics. Qwen completed only one unmatched pair before a second
transport failure, despite a frozen serial operational continuation. Its
remaining three topic pairs are missing, not zero effects. The held-out run's
reported cost, including the first Qwen attempt, was USD 1.586045 plus USD
0.015031 uncertain reservation; the conservative cumulative bound is USD
5.179706. No consistent P− effect was replicated. This is a small exploratory
RH-1A result without F/P+ specificity controls, not a refutation of H-M1 or
evidence of RH-1B holonomy. Diagnose the Qwen transport and predefine a larger,
controlled replication before making stronger claims. A two-version xAI follow-up
then used four new topics with N/F/P−/P+ controls. Grok 4.6 had one matched topic
with P− = −0.25 and P+ = +0.25, F = 0, and zero contrasts in the other three.
Pinned Grok 4.20 had zero authority-share contrasts in all four topics; its
P−/N match rate was 3/4 and only 2/4 topics matched all controls. Thus the
4.6 sign pattern did not replicate across versions. A separately labelled
post-hoc static probe check for 4.20 passed the earlier sensitivity gate, but
cannot alter the controlled comparison. The new receipted cost was USD 2.050597
including that diagnostic; the conservative cumulative bound is USD 7.230303.
This is still small exploratory RH-1A evidence, not a positive H-M1 or RH-1B
result. The two Grok versions share a provider and family. This record itself
does not authorize additional live spending.

Separately, review and import the completed Sounio–Lean bridge only after its own
source and verification receipts are available. The pilot introduces no new
Lean theorem or RH-1B result.

## Post-hoc context audit and next design

The offline audit of all 32 controlled Grok trajectories found the original
intervention retained in every receiver context. Of 24 contrasts, 21 pass
tolerance-one matching, but only one has identical endpoint ratings (F/N,
Grok 4.6 topic 3; zero receiver difference). No contrast has identical full
contexts. These are approximate task endpoints, not equal computational
states. A focal unblinded reading of topic 1 identifies plausible textual
paths, without establishing their causal contribution. H-M1 remains open.
The v0.2 design adds context-removal and canonical-reset controls; operational
choices must be frozen before a new run. No new API calls or spend occurred.
Prior experimental freezes and outcomes remain unchanged.

## Context-control implementation checkpoint

The [offline verification](experiments/rh1/results/2026-09-19/CONTEXT_CONTROLS.md)
processed 32 historical trajectories, 64 role contexts and 192 candidate inputs.
All 32 recipient removals were exact; all 32 partner contexts were preserved;
all 16 reset groups had identical candidate payloads across four conditions.
Seven unit tests passed. This is implementation evidence, not new behavioural
data. The historical reset briefing is explicitly post-hoc. No API requests
or additional expenditure occurred. Next: freeze a prospective pilot execution
design before any live calls.

## Prospective v0.2 plan frozen, not executed

See [the execution freeze](experiments/rh1/CONTEXT_CONTROLS_V02_FREEZE.md).
It specifies two new fictional topics crossed with receiver A/B, targeted Grok
4.6 follow-up, a 24-call repeated-input admission stage and up to 296 subsequent
calls. Hard new exposure cap USD 2.50; cumulative bound USD 9.730303. This is
a feasibility design, not a powered or externally preregistered replication.
Exact prompts/configuration are hashed. The prospective runner and integration
checks are the next checkpoint; no calls or credential reads occurred.

## Temperature diagnostic completed

The [separate temperature diagnostic](experiments/rh1/results/2026-09-19/TEMPERATURE_DIAGNOSTIC.md)
completed 12/12 calls at 0.2, 0.7 and 1.2 with two fixed canonical role-A
contexts and two repetitions. All authority scores were 0.25. All 12 provider
receipts echoed the requested temperature; this does not audit internal
sampling. No clinical/associative-state claim follows from this scalar probe.
Actual cost USD 0.062568, no uncertain reservation; conservative programme
exposure USD 7.2928705407. Including the separately reserved v0.2 USD 2.50
gives USD 9.7928705407. Original v0.2 freeze hashes are unchanged; Stage A/B
remain unexecuted. The briefings have now been used in this diagnostic, so
later studies must disclose reuse and cannot call them wholly unseen.

## Maximum-temperature attempt

At user request, temperature 2.0 (documented SDK upper bound) was attempted
with the same canonical probe. [The run](experiments/rh1/results/2026-09-19/TEMPERATURE_MAXIMUM.md)
stopped on its first request with transport_or_json_failure: 0/4 valid
measurements and no returned-temperature receipt. No retry occurred. Recorded
cost USD 0; unresolved reservation USD 0.035044, not proof of zero billing.
Conservative programme exposure USD 7.3279145407; with the USD 2.50 v0.2
reservation, USD 9.8279145407. Failure does not establish a temperature effect
or acceptance of 2.0 by this live request.

## User-authorized temperature 2.0 retry

The [fresh bounded retry](experiments/rh1/results/2026-09-19/TEMPERATURE_MAXIMUM_RETRY.md)
returned one valid soil-sensor score of 0.25 with temperature 2.0 echoed,
then stopped on transport_or_json_failure in the second request. One of four
planned measurements completed. New reported cost USD 0.003168 plus unresolved
reservation USD 0.035100. The previous failed request reservation USD 0.035044
is preserved. Updated cumulative conservative bound USD 7.3661825407; including
the separate v0.2 USD 2.50 reservation, USD 9.8661825407. Across both attempts
there are three calls, one valid score and two failures; no temperature-caused
failure or behavioural change is established. Principal v0.2 remains unexecuted.

## Temperature 1.7 versus effort diagnostic stopped

[The medium/high plan](experiments/rh1/TEMPERATURE17_EFFORT_FREEZE.md) interpreted
the user's heavy as documented high, explicitly not xhigh. The first 1.7 medium
call failed with transport_or_json_failure; 0/4 valid measurements and high
was not attempted. [Result](experiments/rh1/results/2026-09-19/TEMPERATURE17_EFFORT.md).
New unresolved reservation USD 0.035044; reported cost zero is not proof of zero
billing. Cumulative conservative exposure USD 7.4012265407; with reserved v0.2
USD 2.50, USD 9.9012265407. No behavioural/effort comparison is available.
Repeated transport failures should be diagnosed before interpreting temperature
effects or extending the paid sweep. No requests remain active.

## xAI documentation and transport diagnosis

[Documentation and live validation](experiments/rh1/results/2026-09-19/XAI_TRANSPORT.md)
found three historical failures within ~0.09 s of the old 120-second client
limit. Timeout is strongly suggested but not retrospectively proven. The
adapter now records sanitized categories, elapsed time and response structure;
request timeout is configurable, default remains 120 for frozen protocols.
A 1.7/high request with 1536 cap returned completed with no final text after
77.735 s, 2267 reasoning tokens; this is not demonstrated truncation. A separate
4096-cap request with the identical input completed in 10.987 s, echoed 1.7/high,
and returned 50% authority with 342 reasoning tokens. No matched 1.7/medium
observation exists, so effort causation is untested; output cap also changed.
Remote agent was located at /home/devsounio/.local/bin/agent on t560, version
1.0.34, but reported unauthenticated; no CLI inference or credential transfer.
Twelve local tests passed. New cost USD 0.017538, no new uncertainty;
conservative cumulative exposure USD 7.4187645407, plus reserved v0.2 USD 2.50
= USD 9.9187645407. Previous uncertain reservations remain intact.

## Remote CLI authentication rechecked

The user confirmed an existing Heavy subscription. A fresh PTY/interactive
SSH check on t560 reported logged in with grok.com, updating the earlier
unauthenticated observation; the subscription tier was not independently
returned. A minimal agent inference request was denied with HTTP 403
permission-denied, no valid answer. [Receipt](experiments/rh1/results/2026-09-19/GROK_CLI_ACCESS.md).
Authentication and inference entitlement are distinct. No local API key
transfer, permission changes or retry occurred. Subscription usage receipt
was unavailable; API exposure ledger remains USD 7.4187645407.

## Interactive Grok CLI succeeded

Following the user's instruction to type through the terminal UI, a fresh
Termius connection to t560 launched agent without flags. A benign prompt typed
into the TUI received a visible completed answer in Grok 4.6 high. The earlier
headless 403 is mode-specific evidence and does not establish general account
denial. The exact routing difference is unknown. TUI shows ~27k context tokens
and Sounio-Language configuration, so this is a connectivity check, not a
controlled RH-1 trial. Temperature unverified; no new local-API spend.

## Interactive Grok authority probe completed

[One exploratory CLI probe](experiments/rh1/results/2026-09-19/GROK_TUI_AUTHORITY.md)
returned authority 25% in Grok 4.6 high, with 24 seconds displayed. A fresh
session was started, but agent context persists (approximately 2.2k before
and 28k after). Temperature is unverified. Single-user-message representation
and injected CLI context differ from the API diagnostic that returned 50%;
no causal effort/temperature contrast or H-M1 replication follows. No API
harness calls; subscription usage unmeasured. The API exposure ledger and
the unexecuted prospective v0.2 status remain unchanged.

## Interactive Grok repeatability check completed

[Two new fresh-session CLI repetitions](experiments/rh1/results/2026-09-19/GROK_TUI_REPEAT.md)
returned 25% each in Grok 4.6 high (29 and 40 seconds displayed). Combined
with the earlier 24-second observation, scores are 25%, 25%, 25%. This is
exploratory same-scenario consistency, not determinism or H-M1 replication.
Temperature remains unknown; no causal effort comparison was performed.
No new API harness calls; subscription usage unmeasured. v0.2 remains unexecuted.

## CLI medium/high comparison awaiting observable result

[Four-call plan](experiments/rh1/results/2026-09-19/GROK_TUI_EFFORT.md) fixed
medium/high/high/medium before inference. Medium control was verified and one
request submitted; no final result could be verified because the captured
terminal image stopped updating. Remaining three calls not started. Remote
completion/cancellation unknown: recover existing session before retrying.
No behavioural effort comparison or new API harness spend.

## User-reported medium and extra-high results

The user resolved the first pending CLI medium response as 25% and separately
reported extra high at 25%. [Updated evidence](experiments/rh1/results/2026-09-19/GROK_TUI_EFFORT.md)
distinguishes those user observations from three earlier assistant-observed
high results of 25%. Extra-high prompt/session/model matching is unverified;
it is outside the planned medium/high block, whose remaining three calls are
pending. Agreement of scores does not establish effort equivalence or H-M1.
No assistant model calls were made for this update.

## Requested temperature illustration completed

[Grok CLI illustration](experiments/rh1/results/2026-09-19/GROK_TEMPERATURE_ILLUSTRATION.md)
produced nominal labels 0.2/0.7/1.2/1.7/2.0 with illustrative authority
25/0/25/50/25 in one response, xhigh displayed. Actual temperature unknown.
This is prompt-conditioned illustrative content, excluded from experimental
results and H-M1 evidence. No new API harness calls.
