# ASN-0045: Tumbler Fields

*2026-03-17*

The tumbler hierarchy (T4, ASN-0034) parses every T4-valid address into four field levels separated by zero components. T4c (LevelDetermination, ASN-0034) already pins those levels to zero-count: zeros(t) ∈ {0, 1, 2, 3} corresponds to node, user, document, element. ASN-0045 names those levels as predicates over T for downstream use, with one rename (user → account) recorded below.

## Naming Convention

T4c labels the level with zeros(t) = 1 as a *user address*. ASN-0045 adopts *account* as the canonical predicate name and treats T4c's *user* as an alias for the same address class. Nelson uses both terms in Literary Machines — "user" for the field-name slot, "account" for the addressable allocation (LM 4/29). The udanax-green implementation settles on "account" in its structural and addressing code (`tumbleraccounteq`, `ACCOUNT` constant). The other three labels (node, document, element) are taken verbatim from T4c.

The rename applies only to the address-class label. T4b's projection symbol `U : T ⇀ T` (the user-component projection on a parsed tumbler) is unchanged by ASN-0045; downstream uses of `U` and `t.Uᵢ` continue without rebinding.

## Hierarchy Level Definitions

For any tumbler t, T4-valid(t) (T4, ASN-0034) means t parses as a well-formed address. Given T4-valid(t), T4c assigns t to exactly one level by zeros(t). We name the four corresponding predicates by definitional equivalence:

**Node** — `Node(t) ≡ T4-valid(t) ∧ zeros(t) = 0`.

**Account** — `Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1`.

**Document** — `Document(t) ≡ T4-valid(t) ∧ zeros(t) = 2`.

**Element** — `Element(t) ≡ T4-valid(t) ∧ zeros(t) = 3`.

Each predicate is a one-place proposition on the tumbler carrier T (T0, ASN-0034). The definitions are total: for any t : T, T4-valid(t) is a well-formed proposition (T4, ASN-0034) and zeros(t) is a natural number (T4 + NAT-card, ASN-0034), so each conjunction is a well-formed proposition without precondition.

## Well-Definedness

T4c carries two postconditions on the T4-valid subdomain: *Exhaustion* (zeros(t) ∈ {0, 1, 2, 3}) and *Pairwise extensional disjointness* of the four level cases. We derive Partition as a corollary in three steps.

*Binding.* Fix t : T with T4-valid(t). By the definitions above, each of Node(t), Account(t), Document(t), Element(t) reduces to `zeros(t) = k` for k ∈ {0, 1, 2, 3} respectively.

*At-least-one.* By T4c's Exhaustion, zeros(t) ∈ {0, 1, 2, 3}, so at least one of the four equalities zeros(t) = k holds, hence at least one of the four predicates holds at t.

*At-most-one.* T4c's *Definition* slot supplies the biconditional `(zeros(t) = k ↔ Lₖ(t))` at T4-valid t for each k ∈ {0, 1, 2, 3}, where L₀, L₁, L₂, L₃ name the label predicates *node address*, *user address*, *document address*, *element address*. Combined with the *Binding* step, this gives `Pₖ(t) ⟺ Lₖ(t)` at T4-valid t, where P₀, P₁, P₂, P₃ are Node, Account, Document, Element. By T4c's *Pairwise extensional disjointness*, for distinct i, j ∈ {0, 1, 2, 3} the conjunction `Lᵢ(t) ∧ Lⱼ(t)` fails. Chaining biconditionals, `Pᵢ(t) ∧ Pⱼ(t) ⟹ Lᵢ(t) ∧ Lⱼ(t)` — contradiction. So no two of Node(t), Account(t), Document(t), Element(t) hold simultaneously.

Combining the two yields the Partition postcondition:

**Partition** — `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))`.

The quantifier ranges over the full carrier T; the antecedent T4-valid(t) restricts the assertion to parseable tumblers. Partition makes no claim about T4-invalid t.

## Examples

*Positive cases (T4-valid).* Each row classifies under exactly one predicate.

| Tumbler | zeros(t) | Level |
|---------|----------|-------|
| [7] | 0 | Node |
| [7, 0, 3] | 1 | Account |
| [7, 0, 3, 0, 5] | 2 | Document |
| [7, 0, 3, 0, 5, 0, 1] | 3 | Element |

*Counter-examples (T4-invalid).* For each, ¬T4-valid(t) holds, so all four predicates evaluate to false and Partition makes no claim.

| Tumbler | T4 clause violated | Why all four predicates are false |
|---------|--------------------|-----------------------------------|
| [7, 0, 0, 3] | adjacent zeros | T4-valid fails; each predicate's left conjunct is false |
| [0, 7] | leading zero | T4-valid fails; each predicate's left conjunct is false |
| [7, 0] | trailing zero | T4-valid fails; each predicate's left conjunct is false |
| [1, 0, 1, 0, 1, 0, 1, 0, 1] | zeros(t) = 4 > 3 violates T4(i) | T4-valid fails; each predicate's left conjunct is false |

The counter-examples show why Partition's antecedent T4-valid(t) is load-bearing: dropping it would force at-least-one to fail on every T4-invalid tumbler.

## Properties Introduced

**Node** (`Node(t) ≡ T4-valid(t) ∧ zeros(t) = 0`)

- *Preconditions.* None (predicate is total on T).
- *Definition.* The two-place conjunction above.
- *Depends.* T0 (carrier), T4 (T4-valid), T4c (zeros range), NAT-zero (the constant 0).
- *Postcondition.* `(A t : T :: Node(t) ⟺ T4-valid(t) ∧ zeros(t) = 0)`.

**Account** (`Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1`)

- *Preconditions.* None.
- *Definition.* The two-place conjunction above.
- *Depends.* T0, T4, T4c, NAT-closure (the constant 1).
- *Postconditions.*
  - `(A t : T :: Account(t) ⟺ T4-valid(t) ∧ zeros(t) = 1)`.
  - *Rename equivalence:* `(A t : T : T4-valid(t) :: Account(t) ⟺ t is a user address per T4c)` — derived: fix t : T with T4-valid(t); the definition `Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1` collapses under the T4-valid antecedent to the biconditional `Account(t) ⟺ zeros(t) = 1`; T4c's *Definition* slot instantiated at t supplies `zeros(t) = 1 ⟺ t is a user address`; chaining the two biconditionals yields `Account(t) ⟺ t is a user address`. ASN-0045's *account* and T4c's *user address* denote the same predicate on the T4-valid subdomain.

**Document** (`Document(t) ≡ T4-valid(t) ∧ zeros(t) = 2`)

- *Preconditions.* None.
- *Definition.* The two-place conjunction above.
- *Depends.* T0, T4 (T4-valid; *Numerals* clause defining `2 := 1 + 1`), T4c, NAT-closure (`1 ∈ ℕ` and addition closure grounding T4's numeral definition in ℕ).
- *Postcondition.* `(A t : T :: Document(t) ⟺ T4-valid(t) ∧ zeros(t) = 2)`.

**Element** (`Element(t) ≡ T4-valid(t) ∧ zeros(t) = 3`)

- *Preconditions.* None.
- *Definition.* The two-place conjunction above.
- *Depends.* T0, T4 (T4-valid; *Numerals* clause defining `3 := 2 + 1`), T4c, NAT-closure (`1 ∈ ℕ` and addition closure grounding T4's numeral definitions in ℕ).
- *Postcondition.* `(A t : T :: Element(t) ⟺ T4-valid(t) ∧ zeros(t) = 3)`.

**Partition**

- *Preconditions.* None.
- *Definition.* `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))`, where `exactly-one-of(P₁, P₂, P₃, P₄) ≡ (P₁ ∨ P₂ ∨ P₃ ∨ P₄) ∧ (A i, j : 1 ≤ i < j ≤ 4 :: ¬(Pᵢ ∧ Pⱼ))`.
- *Depends.* Node, Account, Document, Element (definitions above), T4c (Exhaustion + Pairwise extensional disjointness).
- *Postcondition.* `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))` — derived by combining T4c's *Exhaustion* (zeros(t) ∈ {0, 1, 2, 3}) for the at-least-one direction with T4c's *Pairwise extensional disjointness* for the at-most-one direction, per the *Well-Definedness* derivation above.

## Summary

| Label | Statement | Status |
|-------|-----------|--------|
| Node | `Node(t) ≡ T4-valid(t) ∧ zeros(t) = 0` | derived from T4c |
| Account | `Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1` | derived from T4c; on T4-valid t, equivalent to T4c's *user address* |
| Document | `Document(t) ≡ T4-valid(t) ∧ zeros(t) = 2` | derived from T4c |
| Element | `Element(t) ≡ T4-valid(t) ∧ zeros(t) = 3` | derived from T4c |
| Partition | `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))` | derived from T4c (Exhaustion + Pairwise extensional disjointness) |
