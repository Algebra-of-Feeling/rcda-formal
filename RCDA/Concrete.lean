import RCDA.CayleyDickson

/-! Concrete, kernel-reduced integer-coordinate Cayley-Dickson witnesses.
These witnesses do not constitute a real octonion division-algebra proof. -/
namespace RCDA
open AbelianGroup NonAssocRing
universe u

/-- Minimal extra laws for iterating the displayed doubling as a unital ring. -/
class AdditiveUnitalConjugation (A : Type u) [NonAssocRing A] extends Conjugation A where
  map_add : ∀ a b : A, conj (a + b) = conj a + conj b
  map_one : conj 1 = 1

/-- Connect the stronger octonion interface to the minimal doubling interface. -/
instance {A : Type u} [OctonionLike A] : AdditiveUnitalConjugation A where
  toConjugation := OctonionLike.toConjugation
  map_add := OctonionLike.conj_add
  map_one := OctonionLike.conj_one

instance : Ring Int where
  add_assoc := Int.add_assoc
  add_comm := Int.add_comm
  zero_add := Int.zero_add
  neg_add_cancel := Int.add_left_neg
  left_distrib := Int.mul_add
  right_distrib := Int.add_mul
  one_mul := Int.one_mul
  mul_one := Int.mul_one
  mul_assoc := Int.mul_assoc

instance : AdditiveUnitalConjugation Int where
  conj := id
  conj_zero := rfl
  map_add _ _ := rfl
  map_one := rfl

namespace Double
variable {A : Type u} [NonAssocRing A] [AdditiveUnitalConjugation A]

omit [NonAssocRing A] [AdditiveUnitalConjugation A] in
@[ext] theorem ext {x y : Double A} (hr : x.re = y.re) (hi : x.im = y.im) : x = y := by
  cases x
  cases y
  cases hr
  cases hi
  rfl

instance : Add (Double A) := ⟨fun x y => ⟨x.re + y.re, x.im + y.im⟩⟩
instance : Neg (Double A) := ⟨fun x => ⟨-x.re, -x.im⟩⟩
instance : One (Double A) := ⟨⟨1, 0⟩⟩

omit [AdditiveUnitalConjugation A] in
@[simp] theorem add_re (x y : Double A) : (x + y).re = x.re + y.re := rfl
omit [AdditiveUnitalConjugation A] in
@[simp] theorem add_im (x y : Double A) : (x + y).im = x.im + y.im := rfl
omit [AdditiveUnitalConjugation A] in
@[simp] theorem neg_re (x : Double A) : (-x).re = -x.re := rfl
omit [AdditiveUnitalConjugation A] in
@[simp] theorem neg_im (x : Double A) : (-x).im = -x.im := rfl
omit [AdditiveUnitalConjugation A] in
@[simp] theorem zero_re : (0 : Double A).re = 0 := rfl
omit [AdditiveUnitalConjugation A] in
@[simp] theorem zero_im : (0 : Double A).im = 0 := rfl
omit [AdditiveUnitalConjugation A] in
@[simp] theorem one_re : (1 : Double A).re = 1 := rfl
omit [AdditiveUnitalConjugation A] in
@[simp] theorem one_im : (1 : Double A).im = 0 := rfl
@[simp] theorem mul_re (x y : Double A) :
    (x * y).re = sub (x.re * y.re) (Conjugation.conj y.im * x.im) := rfl
@[simp] theorem mul_im (x y : Double A) :
    (x * y).im = y.im * x.re + x.im * Conjugation.conj y.re := rfl

instance : NonAssocRing (Double A) where
  add_assoc _ _ _ := ext (add_assoc _ _ _) (add_assoc _ _ _)
  add_comm _ _ := ext (add_comm _ _) (add_comm _ _)
  zero_add _ := ext (zero_add _) (zero_add _)
  neg_add_cancel _ := ext (neg_add_cancel _) (neg_add_cancel _)
  left_distrib x y z := by
    apply ext <;> simp only [mul_re, mul_im, add_re, add_im, sub,
      AdditiveUnitalConjugation.map_add, left_distrib, right_distrib, neg_add] <;>
      simp only [add_assoc, neg_add.add_left_comm]
  right_distrib x y z := by
    apply ext <;> simp only [mul_re, mul_im, add_re, add_im, sub,
      left_distrib, right_distrib, neg_add] <;>
      simp only [add_assoc, neg_add.add_left_comm]
  one_mul x := by
    apply ext <;> simp only [mul_re, mul_im, one_re, one_im, sub,
      one_mul, mul_one, mul_zero, zero_mul, neg_zero, add_zero]
  mul_one x := by
    apply ext <;> simp only [mul_re, mul_im, one_re, one_im, sub,
      Conjugation.conj_zero, AdditiveUnitalConjugation.map_one,
      mul_one, zero_mul, neg_zero, add_zero, zero_add]

instance : AdditiveUnitalConjugation (Double A) where
  conj x := ⟨Conjugation.conj x.re, -x.im⟩
  conj_zero := ext Conjugation.conj_zero neg_zero
  map_add _ _ := ext (AdditiveUnitalConjugation.map_add _ _) (neg_add _ _)
  map_one := ext AdditiveUnitalConjugation.map_one neg_zero

omit [AdditiveUnitalConjugation A] in
theorem embed_add (a b : A) : embed (a + b) = embed a + embed b :=
  ext rfl (zero_add 0).symm

omit [AdditiveUnitalConjugation A] in
theorem embed_neg (a : A) : embed (-a) = -embed a :=
  ext rfl neg_zero.symm

omit [AdditiveUnitalConjugation A] in
theorem embed_one : embed (1 : A) = 1 := rfl

/-- The canonical image really is a sector closed under the ring operations. -/
def canonicalSector : Sector (Double A) where
  mem := InSector canonicalEmbedding
  zero_mem := ⟨0, embed_zero⟩
  one_mem := ⟨1, embed_one⟩
  add_mem := by
    rintro _ _ ⟨a, rfl⟩ ⟨b, rfl⟩
    exact ⟨a + b, embed_add a b⟩
  neg_mem := by
    rintro _ ⟨a, rfl⟩
    exact ⟨-a, embed_neg a⟩
  mul_mem := by
    rintro _ _ ⟨a, rfl⟩ ⟨b, rfl⟩
    exact ⟨a * b, embed_mul a b⟩

end Double

abbrev CD0 := Int
abbrev CD1 := Double CD0
abbrev CD2 := Double CD1
abbrev CD3 := Double CD2
abbrev CD4 := Double CD3

/-- Basis vectors in the explicit 16-coordinate tower. -/
def basis (i : Nat) : CD4 :=
  ⟨⟨⟨⟨if i = 0 then 1 else 0, if i = 1 then 1 else 0⟩, ⟨if i = 2 then 1 else 0, if i = 3 then 1 else 0⟩⟩, ⟨⟨if i = 4 then 1 else 0, if i = 5 then 1 else 0⟩, ⟨if i = 6 then 1 else 0, if i = 7 then 1 else 0⟩⟩⟩, ⟨⟨⟨if i = 8 then 1 else 0, if i = 9 then 1 else 0⟩, ⟨if i = 10 then 1 else 0, if i = 11 then 1 else 0⟩⟩, ⟨⟨if i = 12 then 1 else 0, if i = 13 then 1 else 0⟩, ⟨if i = 14 then 1 else 0, if i = 15 then 1 else 0⟩⟩⟩⟩

/-- [P] Explicit annihilation in the integer-coordinate 16-dimensional carrier. -/
def annihilatorLeft : CD4 := basis 1 + basis 10
def annihilatorRight : CD4 := basis 4 + -(basis 15)

set_option maxRecDepth 4096 in
set_option maxHeartbeats 4000000 in
theorem concrete_annihilation : NontrivialAnnihilation annihilatorLeft annihilatorRight := by
  unfold NontrivialAnnihilation
  decide

theorem concrete_hasZeroDivisors : HasZeroDivisors CD4 :=
  ⟨annihilatorLeft, annihilatorRight, concrete_annihilation⟩

/- [P] A concrete associator witness in the eight-coordinate subcarrier. -/
set_option maxRecDepth 4096 in
set_option maxHeartbeats 4000000 in
theorem concrete_octonion_associator :
    associator (basis 1).re (basis 2).re (basis 4).re ≠ 0 := by
  decide

/- Exact coordinate receipt corresponding to the Sounio runtime witness. -/
set_option maxRecDepth 4096 in
set_option maxHeartbeats 4000000 in
theorem concrete_octonion_associator_value :
    associator (basis 1).re (basis 2).re (basis 4).re = (basis 7).re + (basis 7).re := by
  decide

theorem concrete_octonion_nonAssociative : IsNonAssociative CD3 :=
  nonAssociative_iff_nonzero_associator.mpr
    ⟨(basis 1).re, (basis 2).re, (basis 4).re, concrete_octonion_associator⟩

end RCDA
