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
