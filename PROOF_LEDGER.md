# Proof Ledger — canonical certification map

Date: 2026-09-19. Stable IDs originate in the programme conversation.
The [historical ledger](docs/PROOF_LEDGER_CONVERSATION_V1.md) is preserved verbatim;
this document governs the current certification status.

**Evidence:** [Audit.lean](Audit.lean), [axiom log](verification/axioms.log),
[receipt](verification/receipt.json). All declarations below are in namespace RCDA.
A compiled conditional theorem proves an implication under supplied model laws;
a semantic interpretation is not itself Lean-certified.

## Stable mathematical IDs

| ID | Current status and statement | Lean evidence |
|---|---|---|
| P-A1 | Certified: associator zero iff the two bracketings agree | [Associator.lean](RCDA/Associator.lean): `associator_eq_zero_iff` |
| P-A2 | Certified: global and sector associativity characterized by vanishing associators | [Associator.lean](RCDA/Associator.lean): `associative_iff_associator_zero`, `Sector.associative_iff` |
| P-A3 | Certified: explicit nonzero associator in integer CD3 | [Concrete.lean](RCDA/Concrete.lean): `concrete_octonion_associator`, `concrete_octonion_associator_value` |
| P-Z1 | Certified under unique nonzero left division | [Embedding.lean](RCDA/Embedding.lean): `division_noZeroDivisors` |
| P-Z2 | Certified: canonical embedding preserves zero | [CayleyDickson.lean](RCDA/CayleyDickson.lean): `Double.embed_zero` |
| P-Z3 | Certified: embedding preserves multiplication | [CayleyDickson.lean](RCDA/CayleyDickson.lean): `Double.embed_mul` |
| P-Z4 | Certified structure construction with explicit conjugation laws | [Concrete.lean](RCDA/Concrete.lean): `Double.canonicalSector` (definition with proved closure fields) |
| P-Z5 | Certified: nonzero annihilating pair in integer CD4 | [Concrete.lean](RCDA/Concrete.lean): `concrete_annihilation`, `concrete_hasZeroDivisors` |
| P-SE1 | Certified: a nontrivial zero-product pair is not wholly inside the embedded zero-divisor-free domain | [Embedding.lean](RCDA/Embedding.lean): `nontrivial_annihilation_requires_sector_escape` |
| P-SE2 | Interpretation boundary of P-SE1, not a separately compiled counterexample theorem: do not strengthen “not both inside” to “both outside” | Exact conclusion of P-SE1 |
| P-R1 | Certified algebraic curvature deformation identity | [Curvature.lean](RCDA/Curvature.lean): `curvature_deformation` |
| P-R2 | Certified constant-central-scalar version | [ScalarCurvature.lean](RCDA/ScalarCurvature.lean): `curvature_scaled_deformation` |
| P-R3 | Certified construction of the additive-endomorphism ring | [Curvature.lean](RCDA/Curvature.lean): `AddEnd` and its `Ring` instance |
| P-M1 | Certified for a specified state: distinct transport iff relative-loop displacement | [Bundle.lean](RCDA/Bundle.lean): `Transport.memory_iff_loop_displacement` |
| P-M2 | Not separately formalized. A nonidentity **action/operator** has a moved-state witness classically; a nonidentity abstract loop may act trivially. Historical wording must not conflate them | No separate Lean declaration |
| P-M3 | Mathematical consequence of P-M1 when every relevant relative-loop action fixes every state; not separately formalized as a named theorem | P-M1, no separate declaration |
| P-I1 | Certified obstruction to a universal left inverse of annihilating multiplication | [Embedding.lean](RCDA/Embedding.lean): `annihilation_obstructs_left_inverse`; [Examples.lean](RCDA/Examples.lean): `concrete_no_universal_recovery` |

P-SE1 assumes an injective, zero- and product-preserving map and a
zero-divisor-free source. Unique division supplies the latter where available.
It does not establish that a supplied abstract OctonionLike model exists.

## Stable conditional / interpretation IDs

| ID | Status and exact boundary |
|---|---|
| C-A1 | Semantic identification of relational composition with multiplication; no empirical measurement map supplied |
| C-Z1 | Interpretation of the embedded domain as a relational regime; requires that identification and the division/no-zero-divisor laws |
| C-SE1 | Conditional formal specializations: `Double.division_sector_escape` and `RCDAModel.witness_escapes` in [CayleyDickson.lean](RCDA/CayleyDickson.lean). Relational meaning remains a model interpretation |
| C-R1 | Compiled: `AssociatorCoupling.associative_preserves_reference` in [Bundle.lean](RCDA/Bundle.lean), assuming zero associator implies zero correction |
| C-R2 | The same theorem preserves reference curvature; it does not force total curvature to vanish. Also `curvature_zero_deformation` |
| C-M1 | Semantic interpretation of groupoid transport as relational transport, not a certified smooth connection |
| C-M2 | Semantic interpretation of state displacement as relational memory; empirical identifiability is open |
| C-I1 | Interpretation of P-I1; no theorem of temporal or psychological irreversibility |

## Stable scientific hypothesis IDs

All entries below are scientific hypotheses, not Lean theorems. H-M1 has an
initial RH-1A feasibility pilot, with no replicated relational-specific effect;
the other listed experimental targets remain unexecuted in this repository.

| ID | Scientific question / experiment |
|---|---|
| H-A1 | Measurable relational grouping dependence; RA-1 |
| H-Z1 | Annihilation-capable regime versus ordinary decay; ZA-1 |
| H-SE1 | Latent sector escape/new directions before some ruptures; SE-1 |
| H-R1 | Nonzero empirical associator–transport/curvature coupling and possible mediation |
| H-M1 | RH-1A has a completed small feasibility pilot, not a held-out incremental-prediction test; no replicated relational-specific effect. RH-1B remains unexecuted. Neither modality alone certifies geometric holonomy. See [findings](experiments/rh1/results/2026-09-19/FINDINGS.md) and [RH-1](RH1_PROTOCOL.md) |
| H-I1 | Persistent post-rupture differences following apparent recovery |

These six programme IDs are not a one-to-one renaming of the six textual
hypotheses inside Audit.lean: that separate audit list also records ontology,
empirical identifiability and scientific novelty. Neither list constitutes
established experimental support. The recorded pilot does not promote H-M1 to a
proved or validated claim. Novelty/priority has not been verified here.

## Audit catalogue versus programme ledger

The source catalogue contains 26 [P]/[C] theorem entries. It includes supporting
results and counterexamples, so its count is not the count of stable programme IDs.
The appendixed declaration inventory is generated directly from the imported Audit.lean.
No new theorem is introduced by this mapping.

## Boundaries shared by all documents

No certified real octonion division algebra, full RCDAModel inhabitant, smooth
bundle/connection, clinical interpretation, empirical execution or novelty theorem
is supplied. Non-associativity alone forces neither zero divisors nor a nonzero
curvature correction. Logical axioms in the overall development are explicitly
disclosed in the receipt; structure fields are conditional premises.


## Exact imported catalogue

| Tag | Declaration |
|---|---|
| P | `RCDA.associator_eq_zero_iff` |
| P | `RCDA.associative_iff_associator_zero` |
| P | `RCDA.nonAssociative_iff_nonzero_associator` |
| P | `RCDA.Sector.associative_iff` |
| P | `RCDA.Sector.incompatible` |
| P | `RCDA.division_noZeroDivisors` |
| P | `RCDA.embedded_sector_no_annihilation` |
| P | `RCDA.nontrivial_annihilation_requires_sector_escape` |
| P | `RCDA.annihilation_obstructs_left_inverse` |
| P | `RCDA.Double.embed_mul` |
| C | `RCDA.Double.division_sector_escape` |
| C | `RCDA.RCDAModel.witness_escapes` |
| P | `RCDA.curvature_deformation` |
| P | `RCDA.curvature_scaled_deformation` |
| P | `RCDA.curvature_zero_deformation` |
| C | `RCDA.AssociatorCoupling.associative_preserves_reference` |
| P | `RCDA.Transport.memory_iff_loop_displacement` |
| P | `RCDA.concrete_annihilation` |
| P | `RCDA.concrete_hasZeroDivisors` |
| P | `RCDA.concrete_octonion_associator` |
| P | `RCDA.concrete_octonion_associator_value` |
| P | `RCDA.concrete_octonion_nonAssociative` |
| P | `RCDA.bool_noZeroDivisors` |
| P | `RCDA.associativity_does_not_decide_annihilation` |
| P | `RCDA.nonAssociative_with_zero_correction` |
| P | `RCDA.concrete_no_universal_recovery` |
