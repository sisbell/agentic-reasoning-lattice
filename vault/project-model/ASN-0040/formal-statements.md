# ASN-0040 Formal Statements

*Source: ASN-0040-tumbler-baptism.md (revised 2026-03-15) — Extracted: 2026-03-22*

## Definition — BaptismalRegistry

Σ.B ⊆ T — the set of baptized tumblers. A tumbler t is *baptized* iff t ∈ Σ.B. Initially Σ.B contains some non-empty seed set B₀ ⊆ T of root addresses established at system genesis.

## Definition — SiblingStream

S(p, d) — the sibling stream of p at depth d:

  c₁ = inc(p, d)

  cₙ₊₁ = inc(cₙ, 0)    for n ≥ 1

Every element of S(p, d) has the form [p₁, ..., p_{#p}, 0, ..., 0, n] — the parent's components, then d − 1 zeros, then the ordinal n.

## Definition — Children

  children(B, p, d) = B ∩ S(p, d)

— the baptized addresses that belong to the sibling stream.

## Definition — HighWaterMark

  hwm(B, p, d) = #children(B, p, d)

## Definition — NextAddress

  next(B, p, d) = if children(B, p, d) = ∅ then inc(p, d) else inc(max(children(B, p, d)), 0)

---

## S0 — StreamStrictlyOrdered (INV, predicate)

`(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`

## S1 — StreamExtendsParent (INV, predicate)

`(A n : n ≥ 1 : p ≼ cₙ)` — every stream element extends p as a prefix.

## B0 — Irrevocability (INV, predicate)

`(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)`

## B0a — BaptismalClosure (INV, predicate)

The registry grows only through baptism:

`(A Σ, Σ' : Σ → Σ' : (A t : t ∈ Σ'.B \ Σ.B : t was produced by baptism(p, d) for some (p, d) satisfying B6))`

where "satisfying B6" means p satisfies T4, d ∈ {1, 2}, and zeros(p) + (d − 1) ≤ 3.

## B₀ conf. — SeedConformance (PRE, requires)

`(A p, d : children(B₀, p, d) is a contiguous prefix of S(p, d))` and `(A t ∈ B₀ : t satisfies T4)`

## Bop — Baptize (OP, method)

PRE: B6(p, d) — depth validity; B4 — serialized within namespace (p, d)

POST: Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}

FRAME: only Σ.B is modified; all other state components are unchanged

## B1 — ContiguousPrefix (INV, predicate)

`(A p, d, n : n ≥ 1 ∧ cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B))`

Equivalently: children(B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.

Requires conforming B₀, B0a, and B7.

## B2 — HighWaterMarkSufficiency (LEMMA, lemma)

`next(B, p, d) = c_{hwm(B,p,d) + 1}`

Concretely: if hwm = 0, then next = inc(p, d); if hwm = m > 0, then next = inc(cₘ, 0). Follows from B1.

## B3 — GhostValidity (INV, predicate)

Baptism and content occupation are independent predicates. For any t ∈ T:

- t ∈ Σ.B ∧ t occupied: a populated position
- t ∈ Σ.B ∧ t unoccupied: a ghost element (permitted)
- t ∉ Σ.B: an unbaptized position (not addressable)
- t ∉ Σ.B ∧ t occupied: **forbidden**

## B4 — NamespaceSerializaton (INV, predicate)

For any two baptisms β₁, β₂ targeting the same namespace (p, d):

`(A β₁, β₂ : ns(β₁) = ns(β₂) : commit(β₁) ≺ read(β₂) ∨ commit(β₂) ≺ read(β₁))`

where ≺ denotes temporal precedence.

## B5 — FieldAdvancement (LEMMA, lemma)

`zeros(inc(p, d)) = zeros(p) + (d − 1)`

## B5a — SiblingZerosPreservation (LEMMA, lemma)

`(A t : t_{sig(t)} > 0 : zeros(inc(t, 0)) = zeros(t))`

Combined with B5:

`(A n ≥ 1 : zeros(cₙ) = zeros(p) + (d − 1))`

## B6 — ValidDepth (PRE, requires)

Baptism at depth d from parent p is valid iff:

  (i) p satisfies T4,

  (ii) d ∈ {1, 2}, and

  (iii) zeros(p) + (d − 1) ≤ 3

| Parent level | d = 1 (same level) | d = 2 (level crossing) |
|---|---|---|
| Node (zeros = 0) | node child | user child |
| User (zeros = 1) | user child | document child |
| Document (zeros = 2) | sub-document / version | element child |
| Element (zeros = 3) | sub-element | **invalid** |

## B7 — NamespaceDisjointness (LEMMA, lemma)

For distinct valid pairs (p, d) ≠ (p', d'), where both parents satisfy T4 and both depths satisfy B6:

`S(p, d) ∩ S(p', d') = ∅`

Three exhaustive cases:

- *Case 1*: `#p + d ≠ #p' + d'` — streams have different element lengths, disjoint by T3.
- *Case 2*: neither p nor p' is a prefix of the other — disjoint subtrees, disjoint by T10.
- *Case 3*: `p ≼ p'` and `#p + d = #p' + d'` — forces d = 2, d' = 1, #p' = #p + 1. At position #p + 1: S(p, 2) elements have 0 (zero separator from inc(p, 2)); S(p', 1) elements have p'_{#p+1} > 0 (T4 forbids trailing zero). Streams disagree at position #p + 1 and are disjoint.

## B8 — GlobalUniqueness (THEOREM, lemma)

`(A a, b : produced by distinct baptismal acts : a ≠ b)`

Within the same namespace: B4 ensures each baptism observes a distinct hwm value; B1 ensures sequential gap-free allocation, so distinct baptisms produce distinct stream indices, which S0 maps to distinct addresses. Across namespaces: B7 ensures non-overlapping ranges.

## B9 — UnboundedExtent (LEMMA, lemma)

`(A p ∈ Σ.B, d satisfying B6, M ∈ ℕ : (E B' : B' reachable from B by a finite sequence of baptisms : hwm(B', p, d) ≥ M))`

Follows from T0(a) (UnboundedComponents) and B1.

## B10 — RegistryT4Validity (INV, predicate)

`(A t ∈ Σ.B : t satisfies T4)`

Derived from B₀ conformance (T4 for seeds), B6(i) (T4 for parents), and IncrementPreservesValidity (ASN-0034), by induction on the baptism sequence:

- Base case: holds by B₀ conformance.
- Inductive step, hwm = 0: baptized element is c₁ = inc(p, d); p satisfies T4 by B6(i); IncrementPreservesValidity gives inc(p, d) satisfies T4 when d ∈ {1, 2} and zeros(p) + (d − 1) ≤ 3 (B6 conditions ii and iii).
- Inductive step, hwm = m > 0: baptized element is c_{m+1} = inc(cₘ, 0); cₘ satisfies T4 by inductive hypothesis; IncrementPreservesValidity with k = 0 preserves T4 unconditionally.
