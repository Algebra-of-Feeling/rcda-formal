import RCDA.Associator
import RCDA.Curvature

namespace RCDA
universe u v w t

/-- An abstract groupoid, with composition read from left to right. -/
structure PathGroupoid (B : Type u) where
  Path : B → B → Type w
  identity : ∀ a, Path a a
  comp : {a b c : B} → Path a b → Path b c → Path a c
  inverse : {a b : B} → Path a b → Path b a
  assoc : ∀ {a b c d} (p : Path a b) (q : Path b c) (r : Path c d),
    comp (comp p q) r = comp p (comp q r)
  identity_left : ∀ {a b} (p : Path a b), comp (identity a) p = p
  identity_right : ∀ {a b} (p : Path a b), comp p (identity b) = p
  inverse_left : ∀ {a b} (p : Path a b), comp p (inverse p) = identity a
  inverse_right : ∀ {a b} (p : Path a b), comp (inverse p) p = identity b

/-- A groupoid action on a family of fibres; no smooth bundle is asserted. -/
structure Transport {B : Type u} (G : PathGroupoid.{u,w} B) (F : B → Type v) where
  along : {a b : B} → G.Path a b → F a → F b
  along_identity : ∀ a (s : F a), along (G.identity a) s = s
  along_comp : ∀ {a b c} (p : G.Path a b) (q : G.Path b c) (s : F a),
    along (G.comp p q) s = along q (along p s)

namespace Transport
variable {B : Type u} {G : PathGroupoid.{u,w} B} {F : B → Type v}
variable (T : Transport G F)

theorem undo {a b} (p : G.Path a b) (s : F a) :
    T.along (G.inverse p) (T.along p s) = s := by
  rw [← T.along_comp, G.inverse_left, T.along_identity]

theorem redo {a b} (p : G.Path a b) (s : F b) :
    T.along p (T.along (G.inverse p) s) = s := by
  rw [← T.along_comp, G.inverse_right, T.along_identity]

def Memory {a b} (p q : G.Path a b) (s : F a) : Prop := T.along p s ≠ T.along q s

/-- [P] Memory of a specified state is equivalent to displacement by the relative loop.
A nonidentity holonomy operator need not move EVERY state. -/
theorem memory_iff_loop_displacement {a b} (p q : G.Path a b) (s : F a) :
    T.Memory p q s ↔ T.along (G.comp p (G.inverse q)) s ≠ s := by
  constructor
  · intro h he
    apply h
    rw [T.along_comp] at he
    have he' := congrArg (fun z => T.along q z) he
    simpa only [T.redo] using he'
  · intro h he
    apply h
    rw [T.along_comp, he, T.undo]
end Transport

/-- [C] This is an additional model law, not a consequence of non-associativity. -/
structure AssociatorCoupling (A : Type u) (V : Type v) (E : Type w)
    [NonAssocRing A] [NonAssocRing E] where
  correction : V → E
  vanishes_when_associative : (∀ a b c : A, associator a b c = 0) →
    ∀ x, correction x = 0

namespace AssociatorCoupling
variable {A : Type u} {V : Type v} {E : Type w} [NonAssocRing A] [NonAssocRing E]

/-- The zero coupling is always permitted, even for non-associative A. -/
def zero : AssociatorCoupling A V E where
  correction _ := 0
  vanishes_when_associative _ _ := rfl

/-- [C] Coupling removes only the extra contribution, not reference curvature. -/
theorem associative_preserves_reference (C : AssociatorCoupling A V E)
    (hA : IsAssociative A) (bracket : V → V → V) (D : V → E) (x y : V) :
    curvature bracket (deform D C.correction) x y = curvature bracket D x y :=
  curvature_zero_deformation bracket D C.correction
    (C.vanishes_when_associative (associative_iff_associator_zero.mp hA)) x y
end AssociatorCoupling
end RCDA
