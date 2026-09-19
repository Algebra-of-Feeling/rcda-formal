import RCDA.Foundation

namespace RCDA
open AbelianGroup
universe u
variable {A : Type u} [NonAssocRing A]

def associator (a b c : A) : A := sub ((a * b) * c) (a * (b * c))
def IsAssociative (A : Type u) [NonAssocRing A] : Prop :=
  ∀ a b c : A, (a * b) * c = a * (b * c)
def IsNonAssociative (A : Type u) [NonAssocRing A] : Prop :=
  ∃ a b c : A, (a * b) * c ≠ a * (b * c)

/-- [P] Vanishing is equivalent to equality of the two bracketings. -/
theorem associator_eq_zero_iff (a b c : A) :
    associator a b c = 0 ↔ (a * b) * c = a * (b * c) :=
  sub_eq_zero_iff _ _

theorem associative_iff_associator_zero :
    IsAssociative A ↔ ∀ a b c : A, associator a b c = 0 := by
  constructor
  · intro h a b c
    exact (associator_eq_zero_iff a b c).mpr (h a b c)
  · intro h a b c
    exact (associator_eq_zero_iff a b c).mp (h a b c)

theorem nonAssociative_iff_nonzero_associator :
    IsNonAssociative A ↔ ∃ a b c : A, associator a b c ≠ 0 := by
  constructor
  · rintro ⟨a, b, c, h⟩
    exact ⟨a, b, c, fun hz => h ((associator_eq_zero_iff a b c).mp hz)⟩
  · rintro ⟨a, b, c, h⟩
    exact ⟨a, b, c, fun he => h ((associator_eq_zero_iff a b c).mpr he)⟩

/-- A unital subring of a possibly non-associative ring. -/
structure Sector (A : Type u) [NonAssocRing A] where
  mem : A → Prop
  zero_mem : mem 0
  one_mem : mem 1
  add_mem : ∀ {a b}, mem a → mem b → mem (a + b)
  neg_mem : ∀ {a}, mem a → mem (-a)
  mul_mem : ∀ {a b}, mem a → mem b → mem (a * b)

def Sector.Associative (s : Sector A) : Prop :=
  ∀ a b c, s.mem a → s.mem b → s.mem c → (a * b) * c = a * (b * c)
def Sector.NonAssociative (s : Sector A) : Prop :=
  ∃ a b c, s.mem a ∧ s.mem b ∧ s.mem c ∧ (a * b) * c ≠ a * (b * c)

theorem Sector.associative_iff (s : Sector A) :
    s.Associative ↔ ∀ a b c, s.mem a → s.mem b → s.mem c → associator a b c = 0 := by
  constructor
  · intro h a b c ha hb hc
    exact (associator_eq_zero_iff a b c).mpr (h a b c ha hb hc)
  · intro h a b c ha hb hc
    exact (associator_eq_zero_iff a b c).mp (h a b c ha hb hc)

theorem Sector.incompatible (s : Sector A) (h : s.Associative) :
    ¬ s.NonAssociative := by
  rintro ⟨a, b, c, ha, hb, hc, hn⟩
  exact hn (h a b c ha hb hc)
end RCDA
