# ASN-0045: Tumbler Fields

*2026-03-17*

The tumbler hierarchy (T4, ASN-0034) parses every T4-valid address into four field levels separated by zero components. T4c (LevelDetermination, ASN-0034) already pins those levels to zero-count: zeros(t) ∈ {0, 1, 2, 3} corresponds to node, user, document, element. ASN-0045 names those levels as predicates over E for downstream use, with one rename (user → account) recorded below.

## Naming Convention

T4c labels the level with zeros(t) = 1 as a *user*. ASN-0045 adopts *account* as the canonical name and treats T4c's *user* as an alias. Nelson uses both terms in Literary Machines — "user" for the field-name slot, "account" for the addressable allocation (LM 4/29). The udanax-green implementation settles on "account" in its structural and addressing code (`tumbleraccounteq`, `ACCOUNT` constant). The other three labels (node, document, element) are taken verbatim from T4c.

## Hierarchy Level Definitions

For any tumbler t, T4-valid(t) (T4, ASN-0034) means t parses as a well-formed address. Given T4-valid(t), T4c assigns t to exactly one level by zeros(t):

**E.node** — A *node* is a tumbler t with T4-valid(t) ∧ zeros(t) = 0.

**E.account** — An *account* is a tumbler t with T4-valid(t) ∧ zeros(t) = 1.

**E.document** — A *document* is a tumbler t with T4-valid(t) ∧ zeros(t) = 2.

**E.element** — An *element* is a tumbler t with T4-valid(t) ∧ zeros(t) = 3.

## Well-Definedness

T4c carries two postconditions on the T4-valid subdomain: *exhaustion* (zeros(t) ∈ {0, 1, 2, 3}) and *pairwise disjointness* of the four level predicates. Together they make the labeling a partition:

**E.partition** — For every t with T4-valid(t), exactly one of Node(t), Account(t), Document(t), Element(t) holds.

E.partition is a corollary of T4c; ASN-0045 records it as the postcondition the four naming predicates inherit.

## Examples

| Tumbler | zeros(t) | Level |
|---------|----------|-------|
| [7] | 0 | node |
| [7, 0, 3] | 1 | account |
| [7, 0, 3, 0, 5] | 2 | document |
| [7, 0, 3, 0, 5, 0, 1] | 3 | element |

Each row is a T4-valid tumbler; the level follows directly from T4c by counting zero components.

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| E.node | Node: T4-valid(t) ∧ zeros(t) = 0 | derived from T4c |
| E.account | Account: T4-valid(t) ∧ zeros(t) = 1 | derived from T4c (aliasing T4c's *user*) |
| E.document | Document: T4-valid(t) ∧ zeros(t) = 2 | derived from T4c |
| E.element | Element: T4-valid(t) ∧ zeros(t) = 3 | derived from T4c |
| E.partition | For all t with T4-valid(t), exactly one of Node(t), Account(t), Document(t), Element(t) holds | derived from T4c (exhaustion + pairwise disjointness) |
