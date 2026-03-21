# ASN-0059 Formal Statements

*Source: ASN-0059-insert-operation.md (revised 2026-03-20) — Extracted: 2026-03-20*

## Definition — OrdinalDisplacement

For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

When the depth is determined by context (typically m = #p for insertion position p), we write δₙ.

## Definition — OrdinalShift

For a V-position v of depth m and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

By TumblerAdd (ASN-0034): shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n.

## Definition — VContiguity

The text-subspace V-positions of document d in subspace S are *contiguous* when, letting V_S = {v ∈ dom(M(d)) : subspace(v) = S}, either V_S = ∅ or:

`(A u, w : u ∈ V_S ∧ w ∈ V_S ∧ u < w : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < w : v ∈ V_S))`

## Definition — ShiftBlock

For block β = (v, a, k) and natural number n ≥ 1:

`shift_block(β, n) = (shift(v, n), a, k)`

The V-start shifts by n; the I-start and width are unchanged.

---

## I0 — FreshContiguousAllocation (INV, predicate)

Variables: d document, p V-position, vals = (val₁, ..., valₙ) with n ≥ 1, C content store, C' post-state content store, a₁..aₙ ∈ T allocated addresses.

(i) aᵢ ∉ dom(C) for 1 ≤ i ≤ n.

(ii) aᵢ₊₁ = aᵢ + 1 for 1 ≤ i < n, where + is ordinal increment via TA5(c).

(iii) origin(aᵢ) = d for 1 ≤ i ≤ n.

(iv) C' = C ∪ {aᵢ ↦ valᵢ : 1 ≤ i ≤ n}.

## I1 — PreInsertionStability (INV, predicate)

Variables: S = subspace(p), M(d) pre-state arrangement, M'(d) post-state arrangement.

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## I2 — ContentPlacement (INV, predicate)

Variables: a₁ first allocated I-address from I0, p + k and a₁ + k are k ordinal increments via TA5(c).

`(A k : 0 ≤ k < n : p + k ∈ dom(M'(d)) ∧ M'(d)(p + k) = a₁ + k)`

## I3 — PostInsertionShift (INV, predicate)

Variables: S = subspace(p), shift as defined in OrdinalShift.

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

## I4 — SubspaceStability (INV, predicate)

Variables: S = subspace(p).

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## I5 — DocumentIsolation (INV, predicate)

`(A d' : d' ≠ d : M'(d') = M(d'))`

## I6 — ShiftOrderPreservation (LEMMA, lemma)

Variables: m = #v₁ = #v₂, n ≥ 1.

`(A v₁, v₂ : #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

## I7 — ShiftInjectivity (LEMMA, lemma)

Variables: m = #v₁ = #v₂, n ≥ 1.

`(A v₁, v₂ : #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

## I8 — InsertionPrecondition (PRE, requires)

INSERT(d, p, vals) requires:

(i) d ∈ E_doc.

(ii) p satisfies S8a: all components strictly positive, zeros(p) = 0.

(iii) subspace(p) = S where S ≥ 1.

(iv) When V_S = {v ∈ dom(M(d)) : subspace(v) = S} is non-empty, #p equals the common depth of V_S (S8-depth). When V_S = ∅, #p establishes the depth for the subspace.

(v) n ≥ 1.

(vi) #p ≥ 2.

## I9 — ContiguityPreservation (LEMMA, lemma)

Variables: V_S = {v ∈ dom(M(d)) : subspace(v) = S}, v_min = min(V_S), v_max = max(V_S).

Requires: VContiguity holds for V_S before INSERT, and either V_S = ∅ or v_min ≤ p ≤ v_max + 1.

Ensures: VContiguity holds for V_S' = {v ∈ dom(M'(d)) : subspace(v) = S} after INSERT.

## I10 — BlockDecompositionEffect (LEMMA, lemma)

Variables:
- B current block decomposition of M(d).
- B_S = {β = (v, a, k) ∈ B : subspace(v) = S}, B_other = B \ B_S.
- B_left: blocks from B_S with V-extent entirely before p (case a: v + k ≤ p), plus β_L if a straddling block exists.
- B_right: blocks from B_S with V-extent starting at or beyond p (case b: v ≥ p), plus β_R if a straddling block exists.
- Straddling block split: for β = (v, a, k) with v < p and v + k > p, offset c = pₘ − vₘ, β_L = (v, a, c), β_R = (p, a + c, k − c).
- a₁ first allocated I-address from I0.

`B' = B_other ∪ B_left ∪ {(p, a₁, n)} ∪ {shift_block(β, n) : β ∈ B_right}`
