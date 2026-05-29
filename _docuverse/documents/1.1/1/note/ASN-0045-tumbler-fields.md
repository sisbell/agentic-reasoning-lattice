# ASN-0045: Tumbler Fields

*2026-03-17*

The tumbler hierarchy (T4, ASN-0034) parses every T4-valid address into four field levels separated by zero components. T4c (LevelDetermination, ASN-0034) already pins those levels to zero-count: zeros(t) ∈ {0, 1, 2, 3} corresponds to node, user, document, element. ASN-0045 names those levels as predicates over T for downstream use, with one rename (user → account) recorded below.

## Naming Convention

T4c labels the level with zeros(t) = 1 as a *user address*. ASN-0045 adopts *account* as the canonical predicate name and treats T4c's *user* as an alias for the same address class. Nelson uses both terms in Literary Machines — "user" for the field-name slot, "account" for the addressable allocation (LM 4/29). The udanax-green implementation settles on "account" in its structural and addressing code (`tumbleraccounteq`, `ACCOUNT` constant). The other three labels (node, document, element) are taken verbatim from T4c.

The rename applies only to the address-class label. T4b's projection symbol `U : T ⇀ T` (the user-component projection on a parsed tumbler) is unchanged by ASN-0045; downstream uses of `U` and `t.Uᵢ` continue without rebinding.

## Hierarchy Level Definitions

For any tumbler t, T4-valid(t) (T4, ASN-0034) means t parses as a well-formed address. T4 is a foundation axiom characterizing valid address tumblers but introduces no one-place predicate symbol; ASN-0045 coins `T4-valid` as the conjunction of T4's four clauses, pinned down explicitly:

**T4-valid** — `T4-valid(t) ≡ zeros(t) ≤ 3 ∧ (A i : 1 ≤ i < #t : ¬(tᵢ = 0 ∧ tᵢ₊₁ = 0)) ∧ t₁ ≠ 0 ∧ t_{#t} ≠ 0`.

Given T4-valid(t), T4c assigns t to exactly one level by zeros(t). We name the four corresponding predicates by definitional equivalence:

**Node** — `Node(t) ≡ T4-valid(t) ∧ zeros(t) = 0`.

**Account** — `Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1`.

**Document** — `Document(t) ≡ T4-valid(t) ∧ zeros(t) = 2`.

**Element** — `Element(t) ≡ T4-valid(t) ∧ zeros(t) = 3`.

Each predicate is a one-place proposition on the tumbler carrier T (T0, ASN-0034). The definitions are total: for any t : T, T4-valid(t) is a well-formed proposition (T4, ASN-0034) and zeros(t) is a natural number — the cardinality of a finite index set over T0's carrier ℕ, where T4 (ASN-0034) defines zeros(t) — so each conjunction is a well-formed proposition without precondition.

## Well-Definedness

Two facts about the T4-valid subdomain drive the corollary: T4's arithmetic bound `zeros(t) ≤ 3` (T4, ASN-0034) together with `zeros(t) ∈ ℕ` (T0, ASN-0034) confines the zero-count to `{0, 1, 2, 3}`, and T4c's map zeros(t) → level (T4c, ASN-0034) names each zeros-class as one of node/account/document/element. We derive Partition as a corollary in three steps.

*Binding.* Fix t : T with T4-valid(t). By the definitions above, each of Node(t), Account(t), Document(t), Element(t) reduces to `zeros(t) = k` for k ∈ {0, 1, 2, 3} respectively.

*At-least-one.* For T4-valid t, `zeros(t) ∈ {0, 1, 2, 3}`. This follows from the arithmetic bound, not from the bijection's domain. T4's axiom (ASN-0034) gives the upper bound `zeros(t) ≤ 3`, and T0's carrier ℕ (ASN-0034) gives the lower bound `zeros(t) ≥ 0`, since `zeros(t)` is a cardinality and hence a natural number. Together `0 ≤ zeros(t) ≤ 3` forces `zeros(t) ∈ {0, 1, 2, 3}`. Reading the conclusion off the bijection's domain would be circular: T4c's claim to be "a bijection on `{0, 1, 2, 3}`" presupposes that the zero-count being labeled already lies in `{0, 1, 2, 3}`, which is precisely what at-least-one must establish. With `zeros(t) ∈ {0, 1, 2, 3}` secured by the bound, T4c then attaches the level name to whichever value `zeros(t)` takes. Hence at least one of the four equalities zeros(t) = k holds, so at least one of the four predicates holds at t.

*At-most-one.* zeros(t) is a single natural number — the cardinality of a fixed finite index set (T4, ASN-0034) — so it is a function of t and equals at most one value. Each of Node, Account, Document, Element is defined directly as `zeros(t) = k` for a distinct k ∈ {0, 1, 2, 3}; the predicates never route through the level labels, so the comparison is between zero-counts, not levels. The four values 0, 1, 2, 3 are pairwise distinct as natural numbers (T0, ASN-0034). Since zeros(t) is single-valued and the four targets are distinct, no two of the equalities `zeros(t) = k` can hold at once, so no two predicates hold simultaneously at t. The disjointness rests solely on the functionality of zeros(t) (T4) and the pairwise distinctness of 0, 1, 2, 3 in ℕ (T0); T4c's injectivity — a statement about distinct *levels* in the codomain — does no work here.

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
| [1, 0, 1, 0, 1, 0, 1, 0, 1] | zeros(t) = 4 > 3 violates the bound `zeros(t) ≤ 3` | T4-valid fails; each predicate's left conjunct is false |

The counter-examples show why Partition's antecedent T4-valid(t) is load-bearing: dropping it would force at-least-one to fail on every T4-invalid tumbler.

## Properties Introduced

**Node** (`Node(t) ≡ T4-valid(t) ∧ zeros(t) = 0`)

- *Preconditions.* None (predicate is total on T).
- *Definition.* The two-place conjunction above.
- *Depends.* T0 (carrier ℕ; the constant 0 ∈ ℕ), T4 (T4-valid). T4c justifies the *node* level label only; it does no work in this biconditional and is not a proof dependency.
- *Postcondition.* `(A t : T :: Node(t) ⟺ T4-valid(t) ∧ zeros(t) = 0)`.

**Account** (`Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1`)

- *Preconditions.* None.
- *Definition.* The two-place conjunction above.
- *Depends.* T0, T4, T4c, NAT-closure (the constant 1).
- *Postconditions.*
  - `(A t : T :: Account(t) ⟺ T4-valid(t) ∧ zeros(t) = 1)`.
  - *Rename equivalence:* `(A t : T : T4-valid(t) :: Account(t) ⟺ t is a user address per T4c)` — derived: fix t : T with T4-valid(t); the definition `Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1` collapses under the T4-valid antecedent to the biconditional `Account(t) ⟺ zeros(t) = 1`; T4c's *Postcondition* (the bijection clause) instantiated at t supplies `zeros(t) = 1 ⟺ t is a user address`; chaining the two biconditionals yields `Account(t) ⟺ t is a user address`. ASN-0045's *account* and T4c's *user address* denote the same predicate on the T4-valid subdomain.

**Document** (`Document(t) ≡ T4-valid(t) ∧ zeros(t) = 2`)

- *Preconditions.* None.
- *Definition.* The two-place conjunction above.
- *Depends.* T0, T4 (T4-valid), NAT-closure (successor and addition closure ground the numeral `2 := 1 + 1`). T4c justifies the *document* level label only; it does no work in this biconditional and is not a proof dependency.
- *Postcondition.* `(A t : T :: Document(t) ⟺ T4-valid(t) ∧ zeros(t) = 2)`.

**Element** (`Element(t) ≡ T4-valid(t) ∧ zeros(t) = 3`)

- *Preconditions.* None.
- *Definition.* The two-place conjunction above.
- *Depends.* T0, T4 (T4-valid), NAT-closure (successor and addition closure ground the numeral `3 := 2 + 1`). T4c justifies the *element* level label only; it does no work in this biconditional and is not a proof dependency.
- *Postcondition.* `(A t : T :: Element(t) ⟺ T4-valid(t) ∧ zeros(t) = 3)`.

**Partition**

- *Preconditions.* None.
- *Definition.* `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))`, where `exactly-one-of(P₁, P₂, P₃, P₄) ≡ (P₁ ∨ P₂ ∨ P₃ ∨ P₄) ∧ (A i, j : 1 ≤ i < j ≤ 4 :: ¬(Pᵢ ∧ Pⱼ))`.
- *Depends.* Node, Account, Document, Element (definitions above), T4 (axiom `zeros(t) ≤ 3` supplies the upper bound for at-least-one; zeros(t) is the cardinality of a fixed finite index set, hence a single-valued function of t, for at-most-one), T0 (carrier ℕ supplies `zeros(t) ≥ 0` for at-least-one, and the pairwise distinctness of 0, 1, 2, 3 in ℕ for at-most-one), T4c (level naming zeros(t) → level, attaching the four level names once `zeros(t) ∈ {0, 1, 2, 3}` is established).
- *Postcondition.* `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))` — derived by confining the range to `zeros(t) ∈ {0, 1, 2, 3}` via T4's bound `zeros(t) ≤ 3` and T0's `zeros(t) ≥ 0` for the at-least-one direction, and combining the functionality of zeros(t) (T4) with the pairwise distinctness of 0, 1, 2, 3 in ℕ (T0) for the at-most-one direction, per the *Well-Definedness* derivation above. T4c supplies the level names.

## Summary

| Label | Statement | Status |
|-------|-----------|--------|
| Node | `Node(t) ≡ T4-valid(t) ∧ zeros(t) = 0` | derived from T4c |
| Account | `Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1` | derived from T4c; on T4-valid t, equivalent to T4c's *user address* |
| Document | `Document(t) ≡ T4-valid(t) ∧ zeros(t) = 2` | derived from T4c |
| Element | `Element(t) ≡ T4-valid(t) ∧ zeros(t) = 3` | derived from T4c |
| Partition | `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))` | derived from T4 bound `zeros(t) ≤ 3` + T0 `zeros(t) ≥ 0` (at-least-one) and functionality of zeros (T4) + distinctness of 0,1,2,3 in ℕ (T0) (at-most-one); T4c supplies level names |
