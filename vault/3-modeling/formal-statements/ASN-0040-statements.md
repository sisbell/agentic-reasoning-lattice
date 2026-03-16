# ASN-0040 Formal Statements

*Source: ASN-0040-tumbler-baptism.md (revised 2026-03-15) — Index: 2026-03-16 — Extracted: 2026-03-16*

## Definition — BaptismalRegistry

  **Σ.B** ⊆ T — the set of baptized tumblers.

  A tumbler t is *baptized* iff t ∈ Σ.B. Initially Σ.B contains some non-empty seed set B₀ ⊆ T of root addresses established at system genesis.

## Definition — SiblingStream

  S(p, d) — the *sibling stream* of p at depth d:

  c₁ = inc(p, d)

  cₙ₊₁ = inc(cₙ, 0)    for n ≥ 1

  Every element of S(p, d) has the form [p₁, ..., p_{#p}, 0, ..., 0, n] — the parent's components, then d − 1 zeros, then the ordinal n.

## Definition — Children

  children(B, p, d) = B ∩ S(p, d)

  — the baptized addresses that belong to the sibling stream.

## Definition — Next

  next(B, p, d) = if children(B, p, d) = ∅ then inc(p, d) else inc(max(children(B, p, d)), 0)

  — find the greatest baptized sibling and produce its immediate successor; if none exists, produce the first child.

## Definition — HighWaterMark

  hwm(B, p, d) = #children(B, p, d)

---

## S0 — StreamStrictlyOrdered (LEMMA, lemma)

  `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`

  where c₁, c₂, c₃, ... = S(p, d) for fixed p, d.

## S1 — StreamExtendsParent (LEMMA, lemma)

  `(A n : n ≥ 1 : p ≼ cₙ)`

  — every stream element extends p as a prefix.

## B0 — Irrevocability (INV, predicate(State, State))

  `(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)`

## B0a — BaptismalClosure (INV, predicate(State, State))

  `(A Σ, Σ' : Σ → Σ' : (A t : t ∈ Σ'.B \ Σ.B : t was produced by baptism(p, d) for some (p, d) satisfying B6))`

  where "satisfying B6" means p satisfies T4, d ∈ {1, 2}, and zeros(p) + (d − 1) ≤ 3.

## B₀ conf. — SeedConformance (INV, predicate(set\<Tumbler\>))

  `(A p, d : children(B₀, p, d) is a contiguous prefix of S(p, d))` and `(A t ∈ B₀ : t satisfies T4)`

## B1 — ContiguousPrefix (INV, predicate(State))

  `(A p, d, n : n ≥ 1 ∧ cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B))`

  Equivalently: children(B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.

  where cₙ denotes the n-th element of S(p, d).

## B2 — HighWaterMarkSufficiency (LEMMA, lemma)

  `next(B, p, d) = c_{hwm(B,p,d) + 1}`

  Concretely: if hwm = 0, then next = inc(p, d) — the first child; if hwm = m > 0, then next = inc(cₘ, 0) — the next sibling.

## B3 — GhostValidity (INV, predicate(State))

  For any t ∈ T, exactly the following cases hold:

  - t ∈ Σ.B ∧ t occupied: a populated position (permitted)
  - t ∈ Σ.B ∧ t unoccupied: a ghost element (permitted)
  - t ∉ Σ.B ∧ t unoccupied: an unbaptized position (not addressable)
  - t ∉ Σ.B ∧ t occupied: **forbidden**

  Constraint: any operation that populates a position must have `t ∈ Σ.B` as a precondition.

## B4 — NamespaceSerialized (PRE, requires) — on baptize

  `(A β₁, β₂ : ns(β₁) = ns(β₂) : commit(β₁) ≺ read(β₂) ∨ commit(β₂) ≺ read(β₁))`

  where ns(β) = (p, d) is the namespace of baptism β, and ≺ denotes temporal precedence.

## B5 — FieldAdvancement (LEMMA, lemma)

  `zeros(inc(p, d)) = zeros(p) + (d − 1)`

  Combined with B5a, every element of S(p, d) satisfies:

  `(A n ≥ 1 : zeros(cₙ) = zeros(p) + (d − 1))`

## B5a — SiblingZerosPreserved (LEMMA, lemma)

  `(A t : t_{sig(t)} > 0 : zeros(inc(t, 0)) = zeros(t))`

  where sig(t) denotes the index of the last significant (non-trailing) component of t.

## B6 — ValidDepth (PRE, requires) — on baptize

  Baptism at depth d from parent p is valid iff all three hold:

  (i) p satisfies T4

  (ii) d ∈ {1, 2}

  (iii) zeros(p) + (d − 1) ≤ 3

## B7 — NamespaceDisjointness (LEMMA, lemma)

  For distinct valid pairs (p, d) ≠ (p', d') where both parents satisfy T4 and both depths satisfy B6:

  `S(p, d) ∩ S(p', d') = ∅`

  Three exhaustive cases:
  - *Case 1*: #p + d ≠ #p' + d' — streams have different element lengths, disjoint by T3.
  - *Case 2*: neither p nor p' is a prefix of the other — disjoint subtrees, no overlap by T10.
  - *Case 3*: p ≼ p' and #p + d = #p' + d' — forces d = 2, d' = 1, #p' = #p + 1. Position #p + 1 in S(p, 2) elements holds 0 (zero separator); in S(p', 1) elements holds p'_{#p+1} > 0 (by T4). Streams disagree at position #p + 1.

## B8 — GlobalUniqueness (LEMMA, lemma)

  `(A a, b : produced by distinct baptismal acts : a ≠ b)`

## B9 — UnboundedExtent (LEMMA, lemma)

  `(A p ∈ Σ.B, d satisfying B6, M ∈ ℕ : (E B' : B' reachable from B by a finite sequence of baptisms : hwm(B', p, d) ≥ M))`

## B10 — RegistryT4Validity (LEMMA, lemma)

  `(A t ∈ Σ.B : t satisfies T4)`

---

## Bop — RegistryGrowth (POST, ensures) — on baptize

  `Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}`

## Bop — OnlyRegistryModified (FRAME, ensures) — on baptize

  Only Σ.B is modified; all other state components are unchanged.
