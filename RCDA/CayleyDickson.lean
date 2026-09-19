import RCDA.Embedding

namespace RCDA
universe u

/-- Only zero preservation is required for the canonical embedding proof.
The stronger involution/anti-multiplicativity laws belong to a realization. -/
class Conjugation (A : Type u) [Zero A] where
  conj : A → A
  conj_zero : conj 0 = 0

/-- Octonion-like interface, NOT a construction or dimension-eight certificate. -/
class OctonionLike (A : Type u) extends DivisionAlgebra A, Conjugation A where
  left_alternative : ∀ a b : A, (a * a) * b = a * (a * b)
  right_alternative : ∀ a b : A, (a * b) * b = a * (b * b)
  non_associative : IsNonAssociative A
  conj_involutive : ∀ a : A, conj (conj a) = a
  conj_add : ∀ a b : A, conj (a + b) = conj a + conj b
  conj_mul : ∀ a b : A, conj (a * b) = conj b * conj a
  conj_one : conj 1 = 1

/-- One fixed Cayley-Dickson sign/order convention:
(a,b)(c,d) = (ac - conjugate(d)b, da + b conjugate(c)). -/
structure Double (A : Type u) where
  re : A
  im : A
  deriving DecidableEq

namespace Double
variable {A : Type u} [NonAssocRing A] [Conjugation A]
instance : Zero (Double A) := ⟨⟨0, 0⟩⟩
instance : Mul (Double A) := ⟨fun x y =>
  ⟨AbelianGroup.sub (x.re * y.re) (Conjugation.conj y.im * x.im),
    y.im * x.re + x.im * Conjugation.conj y.re⟩⟩

def embed (a : A) : Double A := ⟨a, 0⟩

omit [Conjugation A] in
@[simp] theorem embed_zero : embed (0 : A) = 0 := rfl

omit [Conjugation A] in
theorem embed_injective {a b : A} (h : embed a = embed b) : a = b :=
  congrArg Double.re h

/-- [P] Derived from the displayed multiplication, not assumed. -/
theorem embed_mul (a b : A) : embed (a * b) = embed a * embed b := by
  change (⟨a * b, 0⟩ : Double A) =
    ⟨AbelianGroup.sub (a * b) (Conjugation.conj 0 * 0),
      0 * a + 0 * Conjugation.conj b⟩
  simp only [AbelianGroup.sub, NonAssocRing.zero_mul,
    NonAssocRing.mul_zero, AbelianGroup.neg_zero,
    AbelianGroup.add_zero]

def canonicalEmbedding : ProductEmbedding A (Double A) where
  toFun := embed
  injective := embed_injective
  map_zero := embed_zero
  map_mul := embed_mul

/-- [C] Applying the generic theorem to a supplied division algebra. -/
theorem division_sector_escape {D : Type u} [DivisionAlgebra D] [Conjugation D] {x y : Double D}
    (h : NontrivialAnnihilation x y) :
    ¬ (InSector canonicalEmbedding x ∧ InSector canonicalEmbedding y) :=
  nontrivial_annihilation_requires_sector_escape canonicalEmbedding
    (division_noZeroDivisors D) h
end Double

/-- [C] A proposed sedenion-like RCDA model must SUPPLY an actual witness.
This record does not prove that a supplied OctonionLike instance exists,
or that its doubling has zero divisors. Neither obligation is hidden. -/
structure RCDAModel (O : Type u) [OctonionLike O] where
  annihilator₁ : Double O
  annihilator₂ : Double O
  annihilation : NontrivialAnnihilation annihilator₁ annihilator₂

namespace RCDAModel
variable {O : Type u} [OctonionLike O]

theorem witness_escapes (m : RCDAModel O) :
    ¬ (InSector Double.canonicalEmbedding m.annihilator₁ ∧
       InSector Double.canonicalEmbedding m.annihilator₂) :=
  Double.division_sector_escape m.annihilation
end RCDAModel
end RCDA
