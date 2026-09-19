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
| [Formal Methods Note](FORMAL_METHODS_NOTE.md) | Manuscript skeleton; unpublished |
| [Sounio layer](sounio/README.md) | Imported finite runtime witnesses, distinct from universal Lean proofs |

## Verified scope of this import

- Source: exported rcda-lean.zip from task `01a0badb-a3f0-7523-97af-ae65ba63dbf2`, “Formalize RCDA RCDB core in Lean”.
- The exported snapshot contains 11 Lean files, 26 tagged theorem catalogue entries and six textual scientific hypotheses. Counts refer to different inventories; generated Lean declarations are not original research-result counts.
- Fresh isolated verification passed under Lean 4.33.0: source gate, build and transitive axiom audit. No Mathlib or external packages; no project axiom declarations or admitted proofs.
- Foundational logical axioms used by the overall development: Classical.choice, Quot.sound and propext. “No project axioms” does not mean absence of all logical axioms.
- Sounio receipts are historical evidence imported from that Work, not rerun here. No universal source-to-binary refinement or compiler-correctness theorem is claimed in this snapshot. Compiled ELF artifacts are excluded.
- The source task was actively extending SounioBridge/IntegerBounds during import. Those working edits were not in this archive and are not certified by this snapshot.
- At initial kernel import, no experiment was recorded. The subsequent bounded RH-1A feasibility pilot is now completed (see findings). The full RH-1 protocol and RH-1B remain unexecuted; no confirmatory preregistration, publication or novelty/priority verification is recorded.
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
effect, and does not refute H-M1. Validate probe sensitivity on separate
calibration data before scaling or changing the design. No further live run is
authorized merely by this record.

Separately, review and import the completed Sounio–Lean bridge only after its own
source and verification receipts are available. The pilot introduces no new
Lean theorem or RH-1B result.
