# Short theorem dependency map

```text
Foundation: AbelianGroup → NonAssocRing → Ring
    │
    ├─ Associator: zero associator ↔ equality of bracketings
    │    └─ Sector: associative sector ↔ vanishing associator on the sector
    │
    ├─ Embedding: unique division → NoZeroDivisors
    │    + ProductEmbedding (injective, preserves zero/product)
    │    └─ embedded_sector_no_annihilation
    │         └─ nontrivial_annihilation_requires_sector_escape [P]
    │              + proved Double.canonicalEmbedding
    │              + supplied DivisionAlgebra / OctonionLike
    │              └─ Double.division_sector_escape [C]
    │                   + supplied RCDAModel annihilating pair
    │                   └─ RCDAModel.witness_escapes [C]
    │
    ├─ CayleyDickson + additive unital conjugation
    │    └─ Concrete: Int → CD1 → CD2 → CD3 → CD4
    │         ├─ concrete_octonion_associator [P]
    │         └─ concrete_annihilation [P]
    │              + annihilation_obstructs_left_inverse
    │              └─ concrete_no_universal_recovery [P]
    │
    ├─ Curvature: distributivity + abelian-group identities
    │    ├─ AddEnd M: associative ring of additive operators
    │    └─ curvature_deformation [P]
    │         + CentralAction module/centrality laws
    │         └─ curvature_scaled_deformation [P]
    │
    └─ Bundle
         ├─ PathGroupoid + Transport action laws
         │    └─ undo / redo
         │         └─ memory_iff_loop_displacement [P]
         └─ AssociatorCoupling model law + associative composition
              + curvature_zero_deformation
              └─ associative_preserves_reference [C]

Examples: F₂ and F₂ × F₂ → associativity_does_not_decide_annihilation [P]
Examples: CD3 witness + zero coupling → nonAssociative_with_zero_correction [P]

Audit: compiled declarations → transitive axiom audit + [P]/[C] catalogue
Scientific interpretations [H]: text only; no arrows into mathematical proofs
```

File imports are acyclic. `RCDA.lean` imports the complete proof library;
`Audit.lean` imports that library and Lean's bundled inspection tools.

**Open realization obligations:** construct a suitable scalar field, construct
and certify the intended octonion division algebra and its dimension, supply an
inhabitant of the complete `RCDAModel`, and connect algebraic transport to smooth
geometry and empirical measurements. The concrete integer-coordinate witnesses
do not discharge these distinct obligations.

## Sounio execution map

```text
Sounio CD basis-sign recurrence → bounded-integer CD product
    ├─ embedding: all 64 basis pairs + sector membership
    ├─ associator: 64 quaternion triples + octonion value 2e7
    └─ annihilating pair: zero product + nonzero factors + escape
Sounio 2x2 operators → scaled curvature witness + relative-loop memory
Sounio domain guards / native assertions → positive run + 5 rejection cases
Lean proofs ↔ shared convention and named witnesses (no refinement theorem)
```

The Sounio executable is the runtime claim authority; shell only orchestrates
compilation and captures exit codes and receipts.
