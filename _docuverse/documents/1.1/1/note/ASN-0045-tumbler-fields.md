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

Two facts about the T4-valid subdomain drive the corollary: T4's axiom bounds zeros(t) ≤ 3 (T4, ASN-0034), and the map zeros(t) → level is a bijection (T4c, ASN-0034) that names each zeros-class as one of node/account/document/element. We derive Partition as a corollary in three steps.

*Binding.* Fix t : T with T4-valid(t). By the definitions above, each of Node(t), Account(t), Document(t), Element(t) reduces to `zeros(t) = k` for k ∈ {0, 1, 2, 3} respectively.

*At-least-one.* T4's axiom gives zeros(t) ≤ 3 (T4, ASN-0034), and zeros(t) ∈ ℕ (a cardinality over T0's carrier). We must conclude zeros(t) ∈ {0, 1, 2, 3}, i.e. that `{n ∈ ℕ : n ≤ 3} = {0, 1, 2, 3}`. Order plus the bound `≤ 3` does not suffice: a merely totally-ordered carrier (order-isomorphic to ℚ≥0) admits infinitely many elements ≤ 3. What excludes intermediate values is NAT-discrete (ASN-0034): no natural lies strictly between `m` and `m + 1`. Applied successively — no natural strictly between 0 and 1, between 1 and 2, between 2 and 3 — discreteness leaves exactly the four numerals 0, 1, 2, 3 in the interval `{n ∈ ℕ : n ≤ 3}`. Hence zeros(t) ∈ {0, 1, 2, 3}: at least one of the four equalities zeros(t) = k holds, so at least one of the four predicates holds at t.

*At-most-one.* zeros(t) is a single natural number, so it equals at most one of the numerals 0, 1, 2, 3 — provided those four numerals are pairwise distinct. That distinctness is not delivered by trichotomy: trichotomy presupposes two values are given and resolves their order, but it does not establish `0 ≠ 1`. Indeed, were `zeros(t) = 0` and `zeros(t) = 1` both to hold, transitivity of equality would force `0 = 1`, so the at-most-one argument rests on the pairwise distinctness of the constructed numerals (`2 := 1 + 1`, `3 := 2 + 1`, via NAT-closure, ASN-0034). That distinctness comes from NAT-addcompat's strict successor inequality `n < n + 1` (ASN-0034): instantiating at n = 0, 1, 2 gives `0 < 1`, `1 < 2`, `2 < 3`, and NAT-order's transitivity (ASN-0034) composes these into `0 < 1 < 2 < 3`; NAT-order's irreflexivity then converts each strict inequality into an inequality of values (`0 ≠ 1`, `1 ≠ 2`, `2 ≠ 3`, and the composites `0 ≠ 2`, `0 ≠ 3`, `1 ≠ 3`). Each of Node, Account, Document, Element is defined as `zeros(t) = k` for a distinct k, so no two hold simultaneously at t. The disjointness rests only on the functionality of zeros(t) and this distinctness of the numerals; T4c's bijection zeros(t) → level (ASN-0034) is what licenses reading the four zeros-classes as the node/account/document/element levels.

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
- *Depends.* T0 (carrier ℕ; the constant 0 ∈ ℕ), T4 (T4-valid; axiom zeros(t) ≤ 3), T4c (level naming).
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
- *Depends.* T0, T4 (T4-valid), T4c, NAT-closure (successor and addition closure ground the numeral `2 := 1 + 1`), NAT-addcompat (strict successor inequality `n < n + 1`, distinguishing the numeral 2 from 0, 1, 3 — used in Partition's at-most-one direction).
- *Postcondition.* `(A t : T :: Document(t) ⟺ T4-valid(t) ∧ zeros(t) = 2)`.

**Element** (`Element(t) ≡ T4-valid(t) ∧ zeros(t) = 3`)

- *Preconditions.* None.
- *Definition.* The two-place conjunction above.
- *Depends.* T0, T4 (T4-valid), T4c, NAT-closure (successor and addition closure ground the numeral `3 := 2 + 1`), NAT-addcompat (strict successor inequality `n < n + 1`, distinguishing the numeral 3 from 0, 1, 2 — used in Partition's at-most-one direction).
- *Postcondition.* `(A t : T :: Element(t) ⟺ T4-valid(t) ∧ zeros(t) = 3)`.

**Partition**

- *Preconditions.* None.
- *Definition.* `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))`, where `exactly-one-of(P₁, P₂, P₃, P₄) ≡ (P₁ ∨ P₂ ∨ P₃ ∨ P₄) ∧ (A i, j : 1 ≤ i < j ≤ 4 :: ¬(Pᵢ ∧ Pⱼ))`.
- *Depends.* Node, Account, Document, Element (definitions above), T4 (axiom zeros(t) ≤ 3, for at-least-one), T4c (bijection zeros(t) → level, for the level naming), NAT-discrete (excludes naturals strictly between the numerals, collapsing `{n ∈ ℕ : n ≤ 3}` to `{0, 1, 2, 3}` for at-least-one), NAT-addcompat (strict successor inequality `n < n + 1`, supplying numeral distinctness for at-most-one), NAT-order (irreflexivity and transitivity, composing the successor inequalities into pairwise distinctness for at-most-one).
- *Postcondition.* `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))` — derived by combining T4's axiom zeros(t) ≤ 3 with zeros(t) ∈ ℕ and NAT-discrete (the latter collapsing `{n ∈ ℕ : n ≤ 3}` to `{0, 1, 2, 3}`) for the at-least-one direction, and the functionality of zeros(t) with the pairwise distinctness of the numerals 0, 1, 2, 3 — grounded in NAT-addcompat's `n < n + 1` composed via NAT-order's transitivity and converted to inequality by NAT-order's irreflexivity — for the at-most-one direction, per the *Well-Definedness* derivation above. T4c's bijection zeros(t) → level supplies the level names.

## Summary

| Label | Statement | Status |
|-------|-----------|--------|
| Node | `Node(t) ≡ T4-valid(t) ∧ zeros(t) = 0` | derived from T4c |
| Account | `Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1` | derived from T4c; on T4-valid t, equivalent to T4c's *user address* |
| Document | `Document(t) ≡ T4-valid(t) ∧ zeros(t) = 2` | derived from T4c |
| Element | `Element(t) ≡ T4-valid(t) ∧ zeros(t) = 3` | derived from T4c |
| Partition | `(A t : T : T4-valid(t) :: exactly-one-of(Node(t), Account(t), Document(t), Element(t)))` | derived from T4 (zeros ≤ 3) + NAT-discrete (at-least-one) + functionality of zeros + NAT-addcompat/NAT-order (numeral distinctness, at-most-one); levels named via T4c |
