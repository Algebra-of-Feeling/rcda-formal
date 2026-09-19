import RCDA.Foundation

/-! Algebraic operator curvature. Directions carry an arbitrary bracket;
no manifold, differentiation, Leibniz rule, or smoothness is asserted. -/
namespace RCDA
open AbelianGroup NonAssocRing
universe u v

/-- Additive operators, with ordinary associative composition. -/
structure AddEnd (M : Type u) [AbelianGroup M] where
  apply : M → M
  map_add : ∀ a b, apply (a + b) = apply a + apply b

namespace AddEnd
variable {M : Type u} [AbelianGroup M]
@[ext] theorem ext {f g : AddEnd M} (h : ∀ x, f.apply x = g.apply x) : f = g := by
  cases f with | mk f hf =>
    cases g with | mk g hg =>
      have he : f = g := funext h
      cases he
      rfl

instance : Zero (AddEnd M) := ⟨⟨fun _ => 0, fun _ _ => (zero_add 0).symm⟩⟩
instance : Add (AddEnd M) := ⟨fun f g => ⟨fun x => f.apply x + g.apply x, by
  intro a b
  rw [f.map_add, g.map_add]
  simp only [add_assoc, neg_add.add_left_comm]⟩⟩
instance : Neg (AddEnd M) := ⟨fun f => ⟨fun x => -f.apply x, by
  intro a b
  rw [f.map_add, neg_add]⟩⟩
instance : One (AddEnd M) := ⟨⟨fun x => x, fun _ _ => rfl⟩⟩
instance : Mul (AddEnd M) := ⟨fun f g => ⟨fun x => f.apply (g.apply x), by
  intro a b
  rw [g.map_add, f.map_add]⟩⟩

instance : Ring (AddEnd M) where
  add_assoc _f _g _h := ext (fun _ => add_assoc _ _ _)
  add_comm _f _g := ext (fun _ => add_comm _ _)
  zero_add _f := ext (fun _ => zero_add _)
  neg_add_cancel _f := ext (fun _ => neg_add_cancel _)
  left_distrib f _g _h := ext (fun _ => f.map_add _ _)
  right_distrib _f _g _h := ext (fun _ => rfl)
  one_mul _f := ext (fun _ => rfl)
  mul_one _f := ext (fun _ => rfl)
  mul_assoc _f _g _h := ext (fun _ => rfl)
end AddEnd

variable {V : Type v} {E : Type u} [NonAssocRing E]

def curvature (bracket : V → V → V) (D : V → E) (x y : V) : E :=
  sub (sub (D x * D y) (D y * D x)) (D (bracket x y))

def covariantExterior (bracket : V → V → V) (D K : V → E) (x y : V) : E :=
  sub (sub (D x * K y) (K y * D x) + sub (K x * D y) (D y * K x))
    (K (bracket x y))

def wedgeSquare (K : V → E) (x y : V) : E := sub (K x * K y) (K y * K x)
def deform (D K : V → E) : V → E := fun x => D x + K x

/-- [P] The full unscaled connection-difference polynomial identity.
It holds even without associativity of E; use AddEnd M for actual operators. -/
theorem curvature_deformation (bracket : V → V → V) (D K : V → E) (x y : V) :
    curvature bracket (deform D K) x y =
      (curvature bracket D x y + covariantExterior bracket D K x y) + wedgeSquare K x y := by
  simp only [curvature, deform, covariantExterior, wedgeSquare, sub,
    left_distrib, right_distrib, neg_add]
  simp only [add_assoc, add_comm, neg_add.add_left_comm]

/-- [P] Equality with reference curvature, not necessarily flatness. -/
theorem curvature_zero_deformation (bracket : V → V → V) (D K : V → E)
    (hK : ∀ x, K x = 0) (x y : V) :
    curvature bracket (deform D K) x y = curvature bracket D x y := by
  simp only [curvature, deform, hK, add_zero]
end RCDA
