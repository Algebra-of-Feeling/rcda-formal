# Formal Methods Note — manuscript draft

Source: conversation `6aaeccad-c81c-83e9-8616-f713672713c1` (Garantir a novidade), retrieved 2026-09-19. Conversation text records programme decisions; it is not proof evidence.

**Status: manuscript skeleton, not a published or peer-reviewed result.** The current [Proof Ledger](PROOF_LEDGER.md) governs which statements are certified. In particular P-M2/P-M3 are not separate Lean theorems in this snapshot; nonidentity of an abstract path does not imply nonidentity of its action.

# Machine-Checked Foundations for Relational Cayley–Dickson Dynamics

## A Zero-Sorry Lean 4 Kernel for Non-Associativity, Sector Escape, Curvature Deformation, and Relational Transport

### Abstract

We present a machine-checked formal kernel for a class of relational dynamical models based on Cayley–Dickson-inspired algebraic structure. The development is implemented in Lean 4.33.0 without Mathlib, without `sorry`, and without user-declared axioms. The kernel deliberately separates established algebraic results from modelling assumptions and empirical hypotheses through a three-level epistemic classification: proved results [P], conditional model consequences [C], and scientific hypotheses [H].

The formal development covers associators and associative sectors, abstract division-like structures and exclusion of non-trivial zero divisors, a canonical lower-sector embedding, a sector-escape theorem for non-trivial annihilation, curvature-deformation identities for additive operator connections, groupoid-based fibre transport and relational memory, and a non-recovery result for multiplication by a zero divisor. Concrete kernel-verified witnesses demonstrate a non-zero associator in a three-fold Cayley–Dickson construction and a non-trivial zero-divisor pair in a four-fold construction over integer coordinates.

The central theorem proves that if \(x\neq0\), \(y\neq0\), and \(xy=0\), then the pair cannot lie entirely inside the embedded division sector. Importantly, the theorem establishes only that at least one factor lies outside the sector, avoiding the stronger and generally unjustified claim that both must do so.

The formal kernel does not encode phenomenological claims such as relational rupture, ghosting, psychological irreversibility, or empirical novelty. These remain explicitly external hypotheses. The resulting architecture provides a proof-carrying mathematical substrate for subsequent relational modelling and experimental work while preserving a strict boundary between theorem, model interpretation, and scientific conjecture.

---

# 1. Introduction

## 1.1 Motivation

Higher Cayley–Dickson algebras provide a natural hierarchy in which algebraic properties are progressively lost.

The intended relational programme uses these changes only as a candidate mathematical substrate.

The formal note asks a narrower question:

> Which structural claims can be machine-checked independently of any psychological interpretation?

---

## 1.2 Contribution

The paper provides:

1. a minimal Lean 4 algebraic foundation;
2. a formal associator layer;
3. a division-sector abstraction;
4. a canonical embedding layer;
5. a proved sector-escape theorem;
6. machine-checked Cayley–Dickson witnesses;
7. an algebraic curvature-deformation identity;
8. a groupoid model of fibre transport;
9. a formal non-recovery result;
10. an explicit [P]/[C]/[H] boundary.

---

## 1.3 Non-contributions

The paper does not claim to provide:

- a certified construction of the real octonion division algebra;
- full smooth differential geometry;
- empirical validation of relational Cayley–Dickson models;
- proof of psychological irreversibility;
- proof that any clinical phenomenon corresponds to a zero divisor.

---

# 2. Epistemic architecture

## 2.1 Three claim classes

### [P] Proven

Lean-certified statements.

### [C] Conditional

Results valid once explicit RCDA/RCDB modelling assumptions are adopted.

### [H] Hypothesis

Scientific interpretations requiring data.

---

## 2.2 Why this classification matters

The classification prevents mathematical structure from being silently converted into psychological fact.

---

# 3. Minimal formal foundation

## 3.1 Design constraints

The development uses:

- Lean 4.33.0;
- no Mathlib;
- zero `sorry`;
- no user-declared axioms.

The foundation is deliberately abstract.

No commitment to:

\[
\mathbb R,
\]

norms,

order,

completeness,

or topology

is required for the central algebraic results.

---

## 3.2 Algebraic hierarchy

Introduce:

- additive commutative groups;
- rings;
- associative multiplication only when required;
- division-like interfaces through solvability properties.

Explain why the development does not assume reassociation where it is not justified.

---

# 4. Associators

Define

\[
[x,y,z]
=
(xy)z-x(yz).
\]

Prove:

\[
[x,y,z]=0
\iff
(xy)z=x(yz).
\]

Characterise associative sectors.

Present the machine-checked non-zero witness in the 3-fold Cayley–Dickson construction.

---

# 5. Division sector and canonical inclusion

## 5.1 Abstract division-like interface

State the minimal properties required to exclude non-trivial zero divisors.

## 5.2 Canonical Cayley–Dickson inclusion

Define:

\[
\iota(a)=(a,0).
\]

Prove preservation of:

\[
0
\]

and multiplication.

Under declared laws, prove image closure.

---

# 6. Main theorem: non-trivial annihilation requires sector escape

### Theorem

If

\[
x\neq0,
\qquad
y\neq0,
\qquad
xy=0,
\]

then

\[
\neg
\left(
x\in\operatorname{im}\iota
\land
y\in\operatorname{im}\iota
\right).
\]

Give the Lean statement and proof outline.

---

## 6.1 Logical precision

Emphasise:

\[
\boxed{
\neg(A\land B)
}
\]

means

\[
\boxed{
\neg A\lor\neg B
}
\]

classically,

not

\[
\boxed{
\neg A\land\neg B.
}
\]

This is not a stylistic point.

It determines the scientifically permissible interpretation of “sector escape”.

---

# 7. Concrete zero-divisor witness

Using the documented Cayley–Dickson convention, present the kernel-verified identity

\[
\boxed{
(e_1+e_{10})(e_4-e_{15})=0.
}
\]

Prove each factor is non-zero.

Clarify that the integer-coordinate construction is a concrete algebraic witness, not yet a certified construction of the real sedenion algebra used in stronger semantic interpretations.

---

# 8. Curvature deformation

Define the operator framework.

Prove:

\[
R_{D+K}
=
R_D
+
d_DK
+
K\wedge K.
\]

Then prove the constant-central-scalar form:

\[
R_{D+\kappa K}
=
R_D
+
\kappa d_DK
+
\kappa^2K\wedge K.
\]

---

## 8.1 Conditional associator coupling

If the model supplies

\[
K_{\mathcal A}
\]

with

\[
\mathcal A=0
\Rightarrow
K_{\mathcal A}=0,
\]

then

\[
\mathcal A=0
\Rightarrow
R_{D+K_{\mathcal A}}=R_D.
\]

Explicitly state that:

\[
R_D
\]

may remain non-zero.

No identity

\[
\mathcal A=R
\]

is asserted.

---

# 9. Groupoid transport and memory

Model paths by a groupoid acting on fibres.

Show the equivalence between:

- different transported results along two paths;
- non-trivial action of the corresponding relative loop.

This gives a formally clean path-dependence object without prematurely assuming smooth geometry.

---

# 10. Non-recovery theorem

Formalise the impossibility of a universal recovery multiplier in the presence of a non-trivial zero divisor.

Interpret only conditionally:

\[
[P]:
\text{algebraic non-recovery}
\]

versus

\[
[H]:
\text{psychological non-restoration}.
\]

---

# 11. Audit of claims

Include the full Proof Ledger.

Every theorem receives:

- identifier;
- Lean file;
- dependencies;
- axiom report;
- classification;
- permitted interpretation.

---

# 12. Reproducibility

Provide:

```text
lake build
python3 scripts/verify.py
```

Archive:

- source files;
- Lean version;
- hashes;
- theorem inventory;
- `axioms.log`;
- `receipt.json`.

---

# 13. Limitations

The current formal kernel does not yet include:

1. certified \(\mathbb R\);
2. an eight-dimensional real octonion division algebra;
3. smooth manifolds;
4. smooth bundles;
5. differential forms in the conventional geometric sense;
6. probability;
7. entropy;
8. neural latent spaces;
9. empirical relational dynamics.

These are future extensions, not hidden assumptions.

---

# 14. Relationship to the broader RCDA/RCDB programme

The formal kernel supports a modelling programme in which:

\[
\mathcal A_R
\]

is interpreted as grouping sensitivity,

\[
R_R
\]

as relational curvature,

groupoid transport as relational history,

and zero-divisor structure as a candidate annihilation mechanism.

Those identifications belong to [C] or [H], not to the proved kernel.

---

# 15. Discussion

The central methodological claim of this work is not that formal verification validates a psychological theory.

Rather:

> formal verification constrains exactly what the mathematical substrate does and does not imply.

This allows empirical failure to target the scientific interpretation without contaminating the correctness of the underlying algebraic results.

---

# 16. Conclusion

The project establishes a minimal proof-carrying kernel for relational Cayley–Dickson-inspired dynamics while preserving a strict separation between formal mathematics, modelling assumptions, and empirical hypotheses.

That separation is intended as a feature, not a limitation.
