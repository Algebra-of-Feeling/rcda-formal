import RCDA.Curvature

namespace RCDA
open AbelianGroup NonAssocRing
universe u v w

/-- An action with the usual module laws and central algebra compatibility.
R need not be ordered or complete. These are explicit algebraic structure laws. -/
class CentralAction (R : Type u) (E : Type v) [Ring R] [NonAssocRing E] where
  scale : R → E → E
  scale_add : ∀ r a b, scale r (a + b) = scale r a + scale r b
  add_scale : ∀ r s a, scale (r + s) a = scale r a + scale s a
  one_scale : ∀ a, scale 1 a = a
  mul_scale : ∀ r s a, scale (r * s) a = scale r (scale s a)
  scale_mul_left : ∀ r a b, scale r a * b = scale r (a * b)
  scale_mul_right : ∀ r a b, a * scale r b = scale r (a * b)

namespace CentralAction
variable {R : Type u} {E : Type v} [Ring R] [NonAssocRing E] [CentralAction R E]
@[simp] theorem scale_zero (r : R) : scale r (0 : E) = 0 := by
  have h := scale_add (E := E) r 0 0
  rw [zero_add] at h
  exact (add_left_cancel ((add_zero (scale r (0 : E))).trans h)).symm
@[simp] theorem scale_neg (r : R) (a : E) : scale r (-a) = -scale r a := by
  apply neg_unique
  rw [← scale_add, add_neg_cancel, scale_zero]
end CentralAction

variable {R : Type u} {E : Type v} {V : Type w}
  [Ring R] [NonAssocRing E] [CentralAction R E]
open CentralAction

/-- [P] Kappa is constant in the direction argument; no variable-scalar derivative is claimed. -/
theorem curvature_scaled_deformation (bracket : V → V → V)
    (D K : V → E) (κ : R) (x y : V) :
    curvature bracket (deform D (fun z => scale κ (K z))) x y =
      (curvature bracket D x y + scale κ (covariantExterior bracket D K x y)) +
        scale (κ * κ) (wedgeSquare K x y) := by
  rw [curvature_deformation]
  simp only [covariantExterior, wedgeSquare, sub, scale_add, scale_neg,
    scale_mul_left, scale_mul_right, mul_scale]
end RCDA
