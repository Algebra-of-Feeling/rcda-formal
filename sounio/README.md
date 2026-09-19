# RCDA / RCDB executable kernel in Sounio

**Sounio under Madaros is the executable authority. Lean supplies mathematical
proofs.** This implementation uses actual Cayley–Dickson multiplication, explicit
bracketings, and bounded integer coordinates. No foreign runtime determines the
pass/fail of the mathematical witnesses.

## Files and reproduction

- `rcda_core.sio`: carrier, arithmetic, embedding, associator, operator-curvature
  and relative-loop witnesses; each assertion executes in the native Sounio ELF.
- `verify.sh`: resolves the compiler through the repository's standard resolver,
  checks and compiles every case, runs each produced ELF, rejects native-refusal
  output, and records the compiler/source/executable identities.
- `verification/`: positive run, three mutation checks, two domain-refusal checks,
  compiler and source hashes, commands' diagnostic logs, and a result table.

On a Linux x86-64 Sounio workspace with the default Madaros compiler:

```sh
SOUNIO_REPO=/workspace/sounio bash verify.sh
```

The script uses standard shell utilities and `timeout`. It does not use Python as
an algebra evaluator, generate numerical goldens externally, or fall back to the
legacy compiler. `RCDA_OUT_DIR` can select another evidence directory.

To run the core alone through the canonical resolver:

```sh
source "$SOUNIO_REPO/scripts/lib/resolve_souc.sh"
"$SOUC_BIN" check rcda_core.sio
"$SOUC_BIN" compile rcda_core.sio -o rcda_core.elf
./rcda_core.elf
```

## Mathematical contract

`CD` stores coefficients of the Cayley–Dickson basis, with dimensions
1, 2, 4, 8 or 16 and zero unused coordinates. It is not ordinary componentwise
vector multiplication. Basis products have their sign derived recursively from

\[
(a,b)(c,d)=(ac-\overline d b,\; da+b\overline c),
\quad \overline{(a,b)}=(\overline a,-b).
\]

The basis-sign recurrence follows the repository's existing
`stdlib/algebra/cayley_dickson.sio`, specialized to `i64` coefficients and the
same convention as the Lean companion. Multiplication accumulates its bilinear
expansion; associators preserve the two distinct parenthesizations.

Inputs to CD arithmetic are checked for valid dimension, compatible dimensions,
zero unused coordinates, and coefficients in [-1,000,000, 1,000,000]. At most
16 terms contribute to each product coordinate, so a product accumulation has
absolute bound 16,000,000,000,000, within `i64`. Results can exceed the admitted
input bound; a subsequent operation then refuses rather than silently broadening
the domain. Thus this is a checked partial implementation of integer arithmetic,
not a claim that fixed-width words realize all Lean integers.

Matrix helpers operate only on the small fixed fixtures in this witness file;
they are not advertised as a general overflow-checked matrix library.

## Executed assertions

| Witness | Runtime scope | Lean counterpart |
|---|---|---|
| Canonical embedding | All 64 octonion basis pairs preserve product and remain in the sector; their products are nonzero | `Double.embed_mul`, `Double.canonicalSector`; abstract division-sector theorem separately conditional |
| Associative sector | All 64 quaternion basis triples have zero associator | `Sector.associative_iff`; the runtime enumeration itself is finite |
| Non-associative sector | `[e1,e2,e4] = 2e7` | `concrete_octonion_associator_value` |
| Nontrivial annihilation | `(e1+e10)(e4-e15)=0`, both factors nonzero | `concrete_annihilation` |
| Sector escape | The annihilating pair is not entirely in the embedded octonion sector | `nontrivial_annihilation_requires_sector_escape`; instance evidence here |
| Operator curvature | Noncommutative 2x2 integer matrices, kappa=3, including a nonzero quadratic term | `curvature_scaled_deformation` |
| Relative-loop memory | Two invertible transports differ on a specified state; the relative loop moves that state | `Transport.memory_iff_loop_displacement` |
| Fixed-state control | The same nonidentity relative transport fixes the zero state | Prevents overclaiming that every state moves |

The `[P:runtime]` prefix identifies execution of finite instances associated with
the mathematical layer. It does not promote a runtime test to a universal Lean
proof. `[C]` labels supplied model assumptions; `[H]` labels interpretation.

The scope remains explicit: no concrete octonion division-algebra instance over
a scalar field, no smooth bundle realization, and no empirical clinical claim
is established by these runs. The algebraic source and the Lean source share a
convention and independently checked named witnesses; there is no proved compiler
correctness theorem or general source-refinement theorem linking them.

## The gate must be able to fail

The gate compiles altered Sounio sources and requires controlled runtime rejection:

1. Replace every product contribution by zero — rejected by the embedded-basis
   nonzero assertion.
2. Replace `e15` by `e14` in the complementary factor — rejected by the annihilation
   assertion.
3. Remove the quadratic curvature term — rejected by the curvature equality.
4. Supply a coefficient of 1,000,001 — rejected by the exact-domain guard.
5. Multiply dimension-eight and dimension-sixteen inputs — rejected by the
   dimension guard.

Timeouts, kills and segmentation faults do not count as successful rejection.
The positive ELF must return zero and print its final pass marker. The compiler,
wrappers and input-source hashes must remain unchanged across the run.

## Execution provenance

This run uses the default remote `bin/souc` → Madaros path, not the old local
macOS binary and not the legacy `lean_single` engine. The recorded Madaros binary
was available in the shared workspace; it was **not rebuilt from compiler source
by this task**. Repository HEAD therefore identifies the observed checkout,
while the separate compiler hash identifies the executable actually measured.
No current-source compiler-equivalence or CI claim is inferred from HEAD.

All implementation and execution artifacts were isolated in
`/workspace/rcda-core-01a0badb`; no compiler, standard-library, or shared repository
source was edited. This delivery is a standalone artifact, not a commit, PR,
merge or published release. The repository's pre-commit external math-review
checkpoint was not invoked because no commit/PR/submission was performed.
