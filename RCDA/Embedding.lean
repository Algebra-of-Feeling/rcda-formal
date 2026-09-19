import RCDA.Associator

namespace RCDA
universe u v

/-- A product embedding, with exactly the laws needed for annihilation. -/
structure ProductEmbedding (D : Type u) (S : Type v) [Zero D] [Mul D] [Zero S] [Mul S] where
  toFun : D → S
  injective : ∀ {a b}, toFun a = toFun b → a = b
  map_zero : toFun 0 = 0
  map_mul : ∀ a b, toFun (a * b) = toFun a * toFun b

def InSector {D : Type u} {S : Type v} [Zero D] [Mul D] [Zero S] [Mul S]
    (i : ProductEmbedding D S) (x : S) : Prop := ∃ a, i.toFun a = x

def NoZeroDivisors (A : Type u) [Zero A] [Mul A] : Prop :=
  ∀ a b : A, a * b = 0 → a = 0 ∨ b = 0

def NontrivialAnnihilation {A : Type u} [Zero A] [Mul A] (x y : A) : Prop :=
  x ≠ 0 ∧ y ≠ 0 ∧ x * y = 0

def HasZeroDivisors (A : Type u) [Zero A] [Mul A] : Prop :=
  ∃ x y : A, NontrivialAnnihilation x y

/-- Division is unique solvability on both sides, not inverse reassociation. -/
class DivisionAlgebra (D : Type u) extends NonAssocRing D where
  one_ne_zero : (1 : D) ≠ 0
  left_division : ∀ a : D, a ≠ 0 → ∀ b, ∃ x, a * x = b ∧ ∀ y, a * y = b → y = x
  right_division : ∀ a : D, a ≠ 0 → ∀ b, ∃ x, x * a = b ∧ ∀ y, y * a = b → y = x

/-- [P] Requires no associativity or alternativity. -/
theorem division_noZeroDivisors (D : Type u) [DivisionAlgebra D] : NoZeroDivisors D := by
  intro a b hab
  by_cases ha : a = 0
  · exact Or.inl ha
  · obtain ⟨x, _, unique⟩ := DivisionAlgebra.left_division a ha 0
    exact Or.inr ((unique b hab).trans (unique 0 (NonAssocRing.mul_zero a)).symm)

variable {D : Type u} {S : Type v} [Zero D] [Mul D] [Zero S] [Mul S]

/-- [P] A general embedding theorem; no RCDA-specific premise is used. -/
theorem embedded_sector_no_annihilation (i : ProductEmbedding D S)
    (hD : NoZeroDivisors D) {x y : S} (hx : InSector i x) (hy : InSector i y)
    (hxy : x * y = 0) : x = 0 ∨ y = 0 := by
  obtain ⟨a, rfl⟩ := hx
  obtain ⟨b, rfl⟩ := hy
  have hab : a * b = 0 := i.injective (by rw [i.map_mul, hxy, i.map_zero])
  rcases hD a b hab with ha | hb
  · exact Or.inl (by rw [ha, i.map_zero])
  · exact Or.inr (by rw [hb, i.map_zero])

/-- [P] At least one factor escapes; NOT necessarily both. -/
theorem nontrivial_annihilation_requires_sector_escape (i : ProductEmbedding D S)
    (hD : NoZeroDivisors D) {x y : S} (h : NontrivialAnnihilation x y) :
    ¬ (InSector i x ∧ InSector i y) := by
  intro hs
  rcases embedded_sector_no_annihilation i hD hs.1 hs.2 h.2.2 with hx | hy
  · exact h.1 hx
  · exact h.2.1 hy

/-- [P] A zero-divisor gives information loss for this multiplication map only. -/
theorem annihilation_obstructs_left_inverse {T : Type u} [NonAssocRing T] {x y : T}
    (hy : y ≠ 0) (hxy : x * y = 0) :
    ¬ ∃ recover : T → T, ∀ z, recover (x * z) = z := by
  rintro ⟨recover, h⟩
  have hz := h (0 : T)
  have hy' := h y
  rw [NonAssocRing.mul_zero] at hz
  rw [hxy, hz] at hy'
  exact hy hy'.symm
end RCDA
