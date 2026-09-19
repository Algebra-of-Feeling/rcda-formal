import Init

/-! Minimal algebraic interfaces. All laws are explicit structure fields.
No order, completeness, norm, characteristic, or real-number axioms are used. -/
namespace RCDA
universe u

class AbelianGroup (A : Type u) extends Zero A, Add A, Neg A where
  add_assoc : ∀ a b c : A, (a + b) + c = a + (b + c)
  add_comm : ∀ a b : A, a + b = b + a
  zero_add : ∀ a : A, 0 + a = a
  neg_add_cancel : ∀ a : A, -a + a = 0

namespace AbelianGroup
variable {A : Type u} [AbelianGroup A]
@[simp] theorem add_zero (a : A) : a + 0 = a := by rw [add_comm, zero_add]
@[simp] theorem add_neg_cancel (a : A) : a + -a = 0 := by
  rw [add_comm, neg_add_cancel]
theorem add_left_cancel {a b c : A} (h : a + b = a + c) : b = c := by
  have h' := congrArg (fun x => -a + x) h
  simpa only [← add_assoc, neg_add_cancel, zero_add] using h'
theorem neg_unique {a b : A} (h : a + b = 0) : b = -a :=
  add_left_cancel (h.trans (add_neg_cancel a).symm)
@[simp] theorem neg_zero : -(0 : A) = 0 := by
  have h := neg_add_cancel (0 : A)
  simpa only [add_zero] using h
@[simp] theorem neg_neg (a : A) : -(-a) = a :=
  (neg_unique (neg_add_cancel a)).symm
@[simp] theorem neg_add (a b : A) : -(a + b) = -a + -b := by
  apply Eq.symm
  apply neg_unique
  calc
    (a + b) + (-a + -b) = (a + -a) + (b + -b) := by
      simp only [add_assoc, add_left_comm]
    _ = 0 := by rw [add_neg_cancel, add_neg_cancel, zero_add]
where
  add_left_comm (a b c : A) : a + (b + c) = b + (a + c) := by
    rw [← add_assoc, add_comm a b, add_assoc]

def sub (a b : A) : A := a + -b

theorem sub_eq_zero_iff (a b : A) : sub a b = 0 ↔ a = b := by
  constructor
  · intro h
    have h' := congrArg (fun x => x + b) h
    simpa only [sub, add_assoc, neg_add_cancel, add_zero, zero_add] using h'
  · intro h
    subst b
    exact add_neg_cancel a
end AbelianGroup

/-- Multiplication is deliberately NOT assumed associative. -/
class NonAssocRing (A : Type u) extends AbelianGroup A, Mul A, One A where
  left_distrib : ∀ a b c : A, a * (b + c) = a * b + a * c
  right_distrib : ∀ a b c : A, (a + b) * c = a * c + b * c
  one_mul : ∀ a : A, 1 * a = a
  mul_one : ∀ a : A, a * 1 = a

class Ring (A : Type u) extends NonAssocRing A where
  mul_assoc : ∀ a b c : A, (a * b) * c = a * (b * c)

namespace NonAssocRing
open AbelianGroup
variable {A : Type u} [NonAssocRing A]
@[simp] theorem mul_zero (a : A) : a * 0 = 0 := by
  have h := left_distrib a 0 0
  rw [zero_add] at h
  exact add_left_cancel ((add_zero (a * 0)).trans h) |>.symm
@[simp] theorem zero_mul (a : A) : 0 * a = 0 := by
  have h := right_distrib 0 0 a
  rw [zero_add] at h
  exact add_left_cancel ((add_zero (0 * a)).trans h) |>.symm
@[simp] theorem mul_neg (a b : A) : a * -b = -(a * b) := by
  apply neg_unique
  rw [← left_distrib, add_neg_cancel, mul_zero]
@[simp] theorem neg_mul (a b : A) : -a * b = -(a * b) := by
  apply neg_unique
  rw [← right_distrib, add_neg_cancel, zero_mul]
end NonAssocRing
end RCDA
