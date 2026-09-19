import RCDA.Concrete
import RCDA.Bundle

/-! Counterexamples and a finite model of the division interface. -/
namespace RCDA

/-- The two-element field, with all ring laws proved by finite enumeration. -/
instance : NonAssocRing Bool where
  zero := false
  one := true
  add := Bool.xor
  neg := id
  mul := Bool.and
  add_assoc := by decide
  add_comm := by decide
  zero_add := by decide
  neg_add_cancel := by decide
  left_distrib := by decide
  right_distrib := by decide
  one_mul := by decide
  mul_one := by decide

instance : Ring Bool where
  mul_assoc := by decide

instance : DivisionAlgebra Bool where
  one_ne_zero := by decide
  left_division := by decide
  right_division := by decide

theorem bool_noZeroDivisors : NoZeroDivisors Bool := division_noZeroDivisors Bool

theorem bool_associative : IsAssociative Bool := Ring.mul_assoc

theorem bool_has_no_annihilation : ¬ HasZeroDivisors Bool := by
  rintro ⟨x, y, hx, hy, hxy⟩
  rcases bool_noZeroDivisors x y hxy with h | h
  · exact hx h
  · exact hy h

/-- Coordinatewise product ring: associative, with nontrivial zero divisors. -/
instance {A B : Type} [NonAssocRing A] [NonAssocRing B] : NonAssocRing (A × B) where
  zero := (0, 0)
  one := (1, 1)
  add x y := (x.1 + y.1, x.2 + y.2)
  neg x := (-x.1, -x.2)
  mul x y := (x.1 * y.1, x.2 * y.2)
  add_assoc _ _ _ := Prod.ext (AbelianGroup.add_assoc _ _ _) (AbelianGroup.add_assoc _ _ _)
  add_comm _ _ := Prod.ext (AbelianGroup.add_comm _ _) (AbelianGroup.add_comm _ _)
  zero_add _ := Prod.ext (AbelianGroup.zero_add _) (AbelianGroup.zero_add _)
  neg_add_cancel _ := Prod.ext (AbelianGroup.neg_add_cancel _) (AbelianGroup.neg_add_cancel _)
  left_distrib _ _ _ := Prod.ext (NonAssocRing.left_distrib _ _ _) (NonAssocRing.left_distrib _ _ _)
  right_distrib _ _ _ := Prod.ext (NonAssocRing.right_distrib _ _ _) (NonAssocRing.right_distrib _ _ _)
  one_mul _ := Prod.ext (NonAssocRing.one_mul _) (NonAssocRing.one_mul _)
  mul_one _ := Prod.ext (NonAssocRing.mul_one _) (NonAssocRing.mul_one _)

instance {A B : Type} [Ring A] [Ring B] : Ring (A × B) where
  mul_assoc _ _ _ := Prod.ext (Ring.mul_assoc _ _ _) (Ring.mul_assoc _ _ _)

theorem associative_with_annihilation :
    IsAssociative (Bool × Bool) ∧ HasZeroDivisors (Bool × Bool) := by
  refine ⟨Ring.mul_assoc, (true, false), (false, true), ?_⟩
  unfold NontrivialAnnihilation
  decide

/-- [P] Both possible zero-divisor statuses occur in associative rings. -/
theorem associativity_does_not_decide_annihilation :
    (IsAssociative Bool ∧ ¬ HasZeroDivisors Bool) ∧
    (IsAssociative (Bool × Bool) ∧ HasZeroDivisors (Bool × Bool)) :=
  ⟨⟨bool_associative, bool_has_no_annihilation⟩, associative_with_annihilation⟩

/-- [P] Non-associativity with a permitted identically-zero coupling. -/
theorem nonAssociative_with_zero_correction :
    IsNonAssociative CD3 ∧
    ∀ x : Bool, (AssociatorCoupling.zero (A := CD3) (E := Int)).correction x = 0 :=
  ⟨concrete_octonion_nonAssociative, fun _ => rfl⟩

/-- [P] Exact information-loss consequence for the concrete CD witness. -/
theorem concrete_no_universal_recovery :
    ¬ ∃ recover : CD4 → CD4, ∀ z, recover (annihilatorLeft * z) = z :=
  annihilation_obstructs_left_inverse concrete_annihilation.2.1 concrete_annihilation.2.2
end RCDA
