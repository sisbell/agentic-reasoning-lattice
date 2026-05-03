# ASN-0059 Claim Statements

*Source: ASN-0059-insert-operation.md (revised 2026-03-20) — Extracted: 2026-03-22*

## Definition — OrdinalDisplacement

For n ≥ 1 and m ≥ 1:

δ(n, m) = [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m, with action point m.

## Definition — OrdinalShift

For a V-position v of depth m and n ≥ 1:

shift(v, n) = v ⊕ δ(n, m)

By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n.

## Definition — ShiftBlock

For a block β = (v, a, k) ∈ B and n ≥ 1:

shift_block(β, n) = (shift(v, n), a, k)

The V-start shifts by n; the I-start and width are unchanged.

---

## I0 — FreshContiguousAllocation (POST, predicate)

Parameters: document d, insertion count n ≥ 1, values (val₁, ..., valₙ), pre-state content store C, post-state content store C'.

(i) There exist a₁, ..., aₙ ∈ T with aᵢ ∉ dom(C) for 1 ≤ i ≤ n.

(ii) aᵢ₊₁ = aᵢ + 1 for 1 ≤ i < n, where + is ordinal increment via TA5(c).

(iii) origin(aᵢ) = d for 1 ≤ i ≤ n.

(iv) C' = C ∪ {aᵢ ↦ valᵢ : 1 ≤ i ≤ n}.

## I1 — PreInsertionStability (POST, lemma)

Variables: d document, S = subspace(p), M pre-state arrangement, M' post-state arrangement, p insertion point.

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## I2 — ContentPlacement (POST, lemma)

Variables: p insertion point, a₁ first allocated I-address from I0, n insertion count, M' post-state arrangement; p + k and a₁ + k are k ordinal increments via TA5(c).

`(A k : 0 ≤ k < n : p + k ∈ dom(M'(d)) ∧ M'(d)(p + k) = a₁ + k)`

## I3 — PostInsertionShift (POST, lemma)

Variables: d document, S = subspace(p), M pre-state arrangement, M' post-state arrangement, p insertion point, n insertion count.

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

## I4 — SubspaceStability (POST, lemma)

Variables: d document, S = subspace(p), M pre-state arrangement, M' post-state arrangement.

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## I5 — DocumentIsolation (POST, lemma)

Variables: d target document, M pre-state arrangement function, M' post-state arrangement function.

`(A d' : d' ≠ d : M'(d') = M(d'))`

## TS1 — ShiftOrderPreservation (LEMMA, lemma)

Variables: v₁, v₂ tumblers with #v₁ = #v₂ = m, n ≥ 1.

For v₁, v₂ with #v₁ = #v₂ = m and v₁ < v₂: shift(v₁, n) < shift(v₂, n).

## TS2 — ShiftInjectivity (LEMMA, lemma)

Variables: v₁, v₂ tumblers with #v₁ = #v₂ = m, n ≥ 1.

For v₁, v₂ with #v₁ = #v₂ = m: shift(v₁, n) = shift(v₂, n) implies v₁ = v₂.

## I8 — InsertionPrecondition (PRE, requires)

Parameters: document d, insertion point p, value sequence vals with n = |vals| ≥ 1, entity set E_doc, arrangement M.

(i) d ∈ E_doc.

(ii) p satisfies S8a: all components strictly positive, zeros(p) = 0.

(iii) subspace(p) = S where S ≥ 1.

(iv) Let V_S = {v ∈ dom(M(d)) : subspace(v) = S}. When V_S ≠ ∅, #p equals the common depth of V_S. When V_S = ∅, #p is unconstrained beyond (ii) and (vi).

(v) n ≥ 1.

(vi) #p ≥ 2.

## I9 — ContiguityPreservation (LEMMA, lemma)

Variables: d document, S = subspace(p), V_S = {v ∈ dom(M(d)) : subspace(v) = S}, v_min = min(V_S), v_max = max(V_S), p insertion point, n ≥ 1.

Precondition: V_S is contiguous before INSERT, and either V_S = ∅ or v_min ≤ p ≤ v_max + 1.

Postcondition: V_S' = {v ∈ dom(M'(d)) : subspace(v) = S} is contiguous after INSERT.

Formally: V_S' = [v_min, v_max + n] with no gaps (where v_min is unchanged, v_max + n is the new maximum).

## I10 — BlockDecompositionEffect (LEMMA, lemma)

Variables: B current block decomposition of M(d), B_S = {β = (v, a, k) ∈ B : subspace(v) = S}, B_other = B \ B_S, p insertion point, n ≥ 1, a₁ first allocated I-address from I0.

Partition B_S relative to p. For each β = (v, a, k) ∈ B_S, exactly one of:

(a) Entirely before: v + k ≤ p.

(b) Entirely at or after: v ≥ p.

(c) Straddling: v < p and v + k > p. At most one block straddles p. For the straddling block, offset c = pₘ − vₘ where m = #v = #p; split β at c into β_L = (v, a, c) and β_R = (p, a + c, k − c).

Define:
- B_left = {β ∈ B_S : case (a)} ∪ ({β_L} if case (c) applies, else ∅)
- B_right = {β ∈ B_S : case (b)} ∪ ({β_R} if case (c) applies, else ∅)

Post-INSERT block decomposition:

`B' = B_other ∪ B_left ∪ {(p, a₁, n)} ∪ {shift_block(β, n) : β ∈ B_right}`

## D-CTG — VSpaceContiguity (INV, predicate)

Variables: d document, S subspace identifier, V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}.

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`
