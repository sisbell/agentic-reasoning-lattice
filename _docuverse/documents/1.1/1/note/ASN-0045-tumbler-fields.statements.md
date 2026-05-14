# ASN-0045 Claim Statements

*Source: ASN-0045-tumbler-fields.md (revised 2026-03-17) — Extracted: 2026-05-13*

## Definition — ExactlyOneOf

`exactly-one-of(P₁, P₂, P₃, P₄) ≡ (P₁ ∨ P₂ ∨ P₃ ∨ P₄) ∧ (A i, j : 1 ≤ i < j ≤ 4 :: ¬(Pᵢ ∧ Pⱼ))`

---

## Node — IsNode (predicate, DEF)

`Node(t) ≡ T4-valid(t) ∧ zeros(t) = 0`

- *Preconditions.* None (predicate is total on T).
- *Postcondition.* `(A t : T :: Node(t) ⟺ T4-valid(t) ∧ zeros(t) = 0)`.

---

## Account — IsAccount (predicate, DEF)

`Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1`

- *Preconditions.* None.
- *Postconditions.*
  - `(A t : T :: Account(t) ⟺ T4-valid(t) ∧ zeros(t) = 1)`.
  - *Rename equivalence:* `(A t : T : T4-valid(t) :: Account(t) ⟺ t is a user address per T4c)`.

---

## Document — IsDocument (predicate, DEF)

`Document(t) ≡ T4-valid(t) ∧ zeros(t) = 2`

- *Preconditions.* None.
- *Postcondition.* `(A t : T :: Document(t) ⟺ T4-valid(t) ∧ zeros(t) = 2)`.

---

## Element — IsElement (predicate, DEF)

`Element(t) ≡ T4-valid(t) ∧ zeros(t) = 3`

- *Preconditions.* None.
- *Postcondition.* `(A t : T :: Element(t) ⟺ T4-valid(t) ∧ zeros(t) = 3)`.

---

## Partition — Partition (LEMMA, derived)

`(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))`

- *Preconditions.* None.
- *Definition.* `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))`, where `exactly-one-of(P₁, P₂, P₃, P₄) ≡ (P₁ ∨ P₂ ∨ P₃ ∨ P₄) ∧ (A i, j : 1 ≤ i < j ≤ 4 :: ¬(Pᵢ ∧ Pⱼ))`.
- *Proof sketch.* At-least-one: by T4c's Exhaustion, `zeros(t) ∈ {0, 1, 2, 3}`, so at least one of the four equalities `zeros(t) = k` holds. At-most-one: by T4c's Pairwise extensional disjointness, for distinct i, j ∈ {0, 1, 2, 3} the conjunction `Lᵢ(t) ∧ Lⱼ(t)` fails; chaining biconditionals `Pₖ(t) ⟺ Lₖ(t)` gives `Pᵢ(t) ∧ Pⱼ(t) ⟹ Lᵢ(t) ∧ Lⱼ(t)` — contradiction.
