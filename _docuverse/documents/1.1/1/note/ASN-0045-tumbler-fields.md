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

Each predicate is a one-place proposition on the tumbler carrier T (T0, ASN-0034). The definitions are total: for any t : T, T4-valid(t) is a well-formed proposition (T4, ASN-0034) and zeros(t) is a natural number — the cardinality of a finite index set over T0's carrier ℕ, where T4 (ASN-0034) defines zeros(t) — so each conjunction is a well-formed proposition without precondition.

## Well-Definedness

One fact about the T4-valid subdomain drives the corollary: the map zeros(t) → level is a bijection on `{0, 1, 2, 3}` (T4c, ASN-0034) that names each zeros-class as one of node/account/document/element. We derive Partition as a corollary in three steps.

*Binding.* Fix t : T with T4-valid(t). By the definitions above, each of Node(t), Account(t), Document(t), Element(t) reduces to `zeros(t) = k` for k ∈ {0, 1, 2, 3} respectively.

*At-least-one.* For T4-valid t, `zeros(t) ∈ {0, 1, 2, 3}`. This is immediate from T4c's bijection (ASN-0034): T4c asserts that `zeros(t) → hierarchical level` is a bijection *on* `{0, 1, 2, 3}`, and a bijection whose domain is `{0, 1, 2, 3}` is precisely the assertion that every T4-valid t has its zero-count in that set. Surjectivity of the bijection further guarantees each of the four values is realized. We need not reconstruct the range from the arithmetic bound `zeros(t) ≤ 3` and a lower anchor: the foundation already delivers the range as the bijection's domain. Hence at least one of the four equalities zeros(t) = k holds, so at least one of the four predicates holds at t.

*At-most-one.* zeros(t) is a single natural number — the cardinality of a fixed finite index set (T4, ASN-0034) — so it is a function of t and equals at most one value. T4c's bijection (ASN-0034) is injective: distinct zero counts map to distinct hierarchical levels, and conversely the four level-classes (node/account/document/element) are indexed by the four *distinct* values 0, 1, 2, 3 of the bijection's domain. Since each of Node, Account, Document, Element is defined as `zeros(t) = k` for a distinct k drawn from that domain, and zeros(t) is single-valued, no two predicates hold simultaneously at t. The disjointness thus rests on the functionality of zeros(t) together with T4c's injectivity, which already certifies the four indexing values as pairwise distinct.

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
- *Depends.* T0 (carrier ℕ; the constant 0 ∈ ℕ), T4 (T4-valid; axiom zeros(t) ≤ 3), T4c (level naming).
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
- *Depends.* T0, T4 (T4-valid), T4c, NAT-closure (successor and addition closure ground the numeral `2 := 1 + 1`).
- *Postcondition.* `(A t : T :: Document(t) ⟺ T4-valid(t) ∧ zeros(t) = 2)`.

**Element** (`Element(t) ≡ T4-valid(t) ∧ zeros(t) = 3`)

- *Preconditions.* None.
- *Definition.* The two-place conjunction above.
- *Depends.* T0, T4 (T4-valid), T4c, NAT-closure (successor and addition closure ground the numeral `3 := 2 + 1`).
- *Postcondition.* `(A t : T :: Element(t) ⟺ T4-valid(t) ∧ zeros(t) = 3)`.

**Partition**

- *Preconditions.* None.
- *Definition.* `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))`, where `exactly-one-of(P₁, P₂, P₃, P₄) ≡ (P₁ ∨ P₂ ∨ P₃ ∨ P₄) ∧ (A i, j : 1 ≤ i < j ≤ 4 :: ¬(Pᵢ ∧ Pⱼ))`.
- *Depends.* Node, Account, Document, Element (definitions above), T4c (bijection zeros(t) → level on `{0, 1, 2, 3}`: its domain supplies the range `zeros(t) ∈ {0, 1, 2, 3}` for at-least-one, and its injectivity — distinct zero counts to distinct levels — supplies the pairwise distinctness of the four indexing values for at-most-one), T4 (zeros(t) is the cardinality of a fixed finite index set, hence a single-valued function of t, for at-most-one).
- *Postcondition.* `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))` — derived by reading the range `zeros(t) ∈ {0, 1, 2, 3}` directly off the domain of T4c's bijection for the at-least-one direction, and combining the functionality of zeros(t) (T4) with T4c's injectivity (distinct zero counts → distinct levels, certifying the four indexing values as pairwise distinct) for the at-most-one direction, per the *Well-Definedness* derivation above. T4c's bijection zeros(t) → level supplies the level names.

## Summary

| Label | Statement | Status |
|-------|-----------|--------|
| Node | `Node(t) ≡ T4-valid(t) ∧ zeros(t) = 0` | derived from T4c |
| Account | `Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1` | derived from T4c; on T4-valid t, equivalent to T4c's *user address* |
| Document | `Document(t) ≡ T4-valid(t) ∧ zeros(t) = 2` | derived from T4c |
| Element | `Element(t) ≡ T4-valid(t) ∧ zeros(t) = 3` | derived from T4c |
| Partition | `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))` | derived from T4c bijection domain `{0,1,2,3}` (at-least-one) + functionality of zeros (T4) and T4c injectivity (at-most-one) |
