# ASN-0040 Claim Statements

*Source: ASN-0040-tumbler-baptism.md (revised 2026-03-15) — Extracted: 2026-04-09*

## Definition — Children

children(B, p, d) = B ∩ S(p, d)

*Used by:* next(B,p,d), hwm(B,p,d), B1, B2, B9, Bop.

## Definition — PrefixRelation

p ≼ cₙ ⟺ #cₙ ≥ #p ∧ (A i : 1 ≤ i ≤ #p : cₙᵢ = pᵢ)

*Used by:* S1, B7.

---

## Σ.B — BaptismalRegistry (DEF, state)

*Definition:* Σ.B ⊆ T — the set of tumblers that have been baptized or were present in the seed set B₀.

*Axiom:* Σ.B is a state component introduced by design. The type invariant Σ.B ⊆ T is preserved by B₀ conf. (seed validity), B0 (irrevocability), B0a (baptismal closure), TA5(c) (sibling increment well-definedness), TA5(d) (child increment well-definedness).

---

## S(p,d) — SiblingStream (DEF, function)

*Definition:* S(p, d) = c₁, c₂, c₃, ... where c₁ = inc(p, d) and cₙ₊₁ = inc(cₙ, 0) for n ≥ 1.

*Preconditions:* p ∈ T, d ≥ 1.

*Postconditions:* `(A n ≥ 1 : cₙ = [p₁, ..., p_{#p}, 0, ..., 0, n])` with d − 1 zeros and `#cₙ = #p + d`.

---

## hwm(B,p,d) — HighWaterMark (DEF, function)

*Definition:* hwm(B, p, d) = #children(B, p, d) where children(B, p, d) = {cₙ ∈ S(p, d) : cₙ ∈ B}.

*Preconditions:* B satisfies B1 for (p, d); p ∈ T, d ≥ 1; S(p, d) defined.

*Invariant:* hwm(B, p, d) = m implies children(B, p, d) = {c₁, ..., cₘ} and max(children) = cₘ (when m ≥ 1).

---

## next(B,p,d) — NextAddress (DEF, function)

*Definition:* next(B, p, d) = if children(B, p, d) = ∅ then inc(p, d) else inc(max(children(B, p, d)), 0), where children(B, p, d) = B ∩ S(p, d).

*Preconditions:* B ⊆ T finite; p ∈ T; d ≥ 1; S(p, d) defined.

*Postconditions:* next(B, p, d) ∈ T — the result is a valid tumbler.

---

## Bop — Baptism (OP, operation)

PRE: B6(p, d) — depth validity (defined below); B4 — serialized within namespace (p, d) (defined below); [parent prerequisite deferred to Open Questions]

POST: Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}

FRAME: only Σ.B is modified; all other state components are unchanged

*Preconditions:* p ∈ T, d ∈ ℕ with d ≥ 1; B6(p, d) holds; B4 holds for namespace (p, d); Σ.B satisfies B1 and B10.

*Postconditions:* Σ'.B = Σ.B ∪ {next(Σ.B, p, d)} with next(Σ.B, p, d) ∉ Σ.B; Σ'.B satisfies B0, B1, and B10.

*Frame:* Only Σ.B is modified; all other state components are unchanged.

---

## S0 — StreamOrdering (LEMMA, lemma)

`(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`

*Preconditions:* p ∈ T, d ≥ 1. S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).

*Postconditions:* `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — the sibling stream is strictly increasing.

---

## S1 — StreamPrefix (LEMMA, lemma)

`(A n : n ≥ 1 : p ≼ cₙ)` — every stream element extends p as a prefix.

*Preconditions:* p ∈ T, d ≥ 1. S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).

*Postconditions:* `(A n : n ≥ 1 : p ≼ cₙ)` — every stream element extends p as a prefix.

---

## B0 — Irrevocability (AX, axiom)

`(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)`

---

## B0a — BaptismalClosure (AX, axiom)

`(A Σ, Σ' : Σ → Σ' : (A t : t ∈ Σ'.B \ Σ.B : t was produced by baptism(p, d) for some (p, d) satisfying B6))`

---

## B₀ conf. — SeedConformance (AX, axiom)

B₀ is non-empty and finite, `(A p, d : children(B₀, p, d) is a contiguous prefix of S(p, d))`, and `(A t ∈ B₀ : t satisfies T4)`.

---

## B1 — ContiguousPrefix (INV, invariant)

`(A p, d, n : n ≥ 1 ∧ cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B))`

Equivalently: children(B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.

*Invariant:* `(A p, d, n : n ≥ 1 ∧ cₙ ∈ Σ.B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ Σ.B))` — equivalently, children(Σ.B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.

*Base:* B₀ conf. — seed set satisfies contiguous prefix for all (p, d).

*Preservation:* Each baptism preserves B1 in the target namespace (by Bop, B0, B4, S0, TA5(c)) and in all other namespaces (by B7 for B6-valid pairs; by B10 for non-B6 pairs whose streams are entirely T4-invalid; by stream identity S(p, 1) = S(p', 2) — proved by first-element component comparison and deterministic recurrence — for non-B6 pairs where p ends in zero as its sole defect and d = 1).

---

## B2 — HighWaterMarkSufficiency (LEMMA, lemma)

`next(B, p, d) = c_{hwm(B,p,d) + 1}`

*Preconditions:* B satisfies B1 for all (p, d); p ∈ T, d ≥ 1; S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).

*Postconditions:* `next(B, p, d) = c_{hwm(B,p,d) + 1}`.

---

## B3 — GhostValidity (AX, axiom)

Baptism and content occupation are independent predicates. For any t ∈ T:

- t ∈ Σ.B ∧ t occupied: a populated position
- t ∈ Σ.B ∧ t unoccupied: a ghost element (permitted)
- t ∉ Σ.B: an unbaptized position (not addressable)
- t ∉ Σ.B ∧ t occupied: **forbidden**

---

## B4 — NamespaceSerialization (AX, axiom)

`(A β₁, β₂ : ns(β₁) = ns(β₂) : commit(β₁) ≺ read(β₂) ∨ commit(β₂) ≺ read(β₁))`

where ≺ denotes temporal precedence.

---

## B5 — FieldAdvancement (LEMMA, lemma)

`zeros(inc(p, d)) = zeros(p) + (d − 1)`

*Preconditions:* p ∈ T with d ≥ 1. (In the baptismal context, d ∈ {1, 2} by B6(ii).)

*Postconditions:* `zeros(inc(p, d)) = zeros(p) + (d − 1)`.

---

## B5a — SiblingZerosPreservation (LEMMA, lemma)

`(A t : t_{sig(t)} > 0 : zeros(inc(t, 0)) = zeros(t))`

*Preconditions:* t ∈ T with t_{sig(t)} > 0.

*Postconditions:* `zeros(inc(t, 0)) = zeros(t)`.

---

## B6 — ValidDepth (DEF, predicate)

Baptism at depth d from parent p is valid when:

(i) p satisfies T4,

(ii) d ∈ {1, 2}, and

(iii) zeros(p) + (d − 1) ≤ 3.

*Preconditions:* p ∈ T, d ∈ ℕ with d ≥ 1.

*Postconditions:*

(a) Sufficiency: `(p satisfies T4 ∧ d ∈ {1, 2} ∧ zeros(p) + (d − 1) ≤ 3) ⟹ (A n ≥ 1 : cₙ ∈ S(p, d) satisfies T4)`.

(b) Necessity: violating (ii) or (iii) produces T4 violations in S(p, d); violating (i) either propagates interior violations (adjacent zeros, leading zero) to every stream element via TA5(b), or — when the sole defect is a trailing zero — produces adjacent zeros for d = 2 (falling under interior violation) or creates a stream identical to some valid S(p', d') for d = 1, collapsing B7.

---

## B7 — NamespaceDisjointness (LEMMA, lemma)

For distinct valid pairs (p, d) ≠ (p', d'): S(p, d) ∩ S(p', d') = ∅

*Preconditions:* (p, d) ≠ (p', d') with p, p' satisfying T4 and d, d' satisfying B6.

*Postconditions:* `S(p, d) ∩ S(p', d') = ∅`.

---

## B8 — GlobalUniqueness (LEMMA, lemma)

`(A a, b : produced by distinct baptismal acts : a ≠ b)`

*Preconditions:* β₁, β₂ are distinct baptismal acts in a system conforming to B0, B0a, B1, B4, and B7; β₁ produces a in namespace (p, d) and β₂ produces b in namespace (p', d'), where both (p, d) and (p', d') satisfy B6.

*Postconditions:* `a ≠ b`.

---

## B9 — UnboundedExtent (LEMMA, lemma)

`(A p ∈ Σ.B, d satisfying B6, M ∈ ℕ : (E B' : B' reachable from B by a finite sequence of baptisms : hwm(B', p, d) ≥ M))`

*Preconditions:* p ∈ Σ.B, d satisfying B6(p, d), M ∈ ℕ.

*Postconditions:* There exists B' reachable from Σ.B by a finite sequence of baptisms such that hwm(B', p, d) ≥ M.

---

## B10 — T4ValidityInvariant (INV, invariant)

`(A t ∈ Σ.B : t satisfies T4)`

*Invariant:* `(A t ∈ Σ.B : t satisfies T4)` — every baptized address satisfies FieldSeparatorConstraint.

*Base:* B₀ conf. — every seed element satisfies T4.

*Preservation:* Each baptism preserves B10: when children are empty, by B6 and TA5a (IncrementPreservesT4, ASN-0034) with k = d; when children are non-empty, max(children) ∈ B satisfies T4 by the inductive hypothesis, and TA5a with k = 0 preserves T4 unconditionally. B0a ensures no non-baptismal mechanism introduces elements that might violate T4.
