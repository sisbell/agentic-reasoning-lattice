# ASN-0059 Formal Statements

*Source: ASN-0059-insert-operation.md (revised 2026-03-20) — Extracted: 2026-03-21*

## Definition — OrdinalDisplacement

For n ≥ 1 and m ≥ 1: δ(n, m) = [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m, with action point m.

## Definition — OrdinalShift

For a V-position v of depth m and n ≥ 1:

shift(v, n) = v ⊕ δ(n, m)

By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n.

## Definition — ShiftBlock

For a block β = (v, a, k) and n ≥ 1:

shift_block(β, n) = (shift(v, n), a, k)

---

## I0 — FreshContiguousAllocation (POST, ensures)

Variables: d document, p V-position, (val₁, ..., valₙ) content values with n ≥ 1, C content store, C' post-state content store, a₁, ..., aₙ allocated I-addresses.

(i) aᵢ ∉ dom(C) for 1 ≤ i ≤ n.

(ii) aᵢ₊₁ = aᵢ + 1 for 1 ≤ i < n, where + is ordinal increment via TA5(c).

(iii) origin(aᵢ) = d for 1 ≤ i ≤ n.

(iv) C' = C ∪ {aᵢ ↦ valᵢ : 1 ≤ i ≤ n}.

## I1 — PreInsertionStability (POST, ensures)

Variables: M(d) pre-state arrangement, M'(d) post-state arrangement, S = subspace(p), p insertion V-position.

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## I2 — ContentPlacement (POST, ensures)

Variables: p insertion V-position, n number of values, a₁ first allocated I-address from I0. p + k and a₁ + k are k ordinal increments via TA5(c).

`(A k : 0 ≤ k < n : p + k ∈ dom(M'(d)) ∧ M'(d)(p + k) = a₁ + k)`

## I3 — PostInsertionShift (POST, ensures)

Variables: M(d), M'(d), S = subspace(p), p insertion point, n length.

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

## I4 — SubspaceStability (POST, ensures)

Variables: M(d), M'(d), S = subspace(p).

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## I5 — DocumentIsolation (POST, ensures)

Variables: d the target document, M arrangement function.

`(A d' : d' ≠ d : M'(d') = M(d'))`

## TS1 — ShiftOrderPreservation (LEMMA, lemma)

For v₁, v₂ with #v₁ = #v₂ = m and v₁ < v₂:

`shift(v₁, n) < shift(v₂, n)`

## TS2 — ShiftInjectivity (LEMMA, lemma)

For v₁, v₂ with #v₁ = #v₂ = m:

`shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂`

## I8 — InsertionPrecondition (PRE, requires)

INSERT(d, p, vals) requires:

(i) d ∈ E_doc.

(ii) p satisfies S8a: all components strictly positive, zeros(p) = 0.

(iii) subspace(p) = S where S ≥ 1.

(iv) When V_S = {v ∈ dom(M(d)) : subspace(v) = S} is non-empty, #p equals the common depth of V_S. When V_S = ∅, #p establishes the depth for the subspace.

(v) n ≥ 1.

(vi) #p ≥ 2.

## I9 — ContiguityPreservation (LEMMA, lemma)

Variables: V_S = {v ∈ dom(M(d)) : subspace(v) = S}, v_min = min(V_S), v_max = max(V_S) when V_S ≠ ∅.

Precondition: V_S satisfies D-CTG before INSERT, and v_min ≤ p ≤ v_max + 1 (for V_S = ∅, any p is valid).

Conclusion: V_S' satisfies D-CTG after INSERT.

## I10 — BlockDecompositionEffect (POST, ensures)

Variables: B current block decomposition of M(d). S = subspace(p). B_S = {β = (v, a, k) ∈ B : subspace(v) = S}. B_other = B \ B_S.

Partition B_S relative to p:

(a) *Entirely before:* v + k ≤ p.
(b) *Entirely at or after:* v ≥ p.
(c) *Straddling:* v < p and v + k > p. At most one block satisfies (c) by B2.

For case (c): offset c = pₘ − vₘ where m = #p, with 0 < c < k. Split β = (v, a, k) into β_L = (v, a, c) and β_R = (p, a + c, k − c).

B_left = {blocks from case (a)} ∪ {β_L if case (c) applies}.
B_right = {blocks from case (b)} ∪ {β_R if case (c) applies}.

`B' = B_other ∪ B_left ∪ {(p, a₁, n)} ∪ {shift_block(β, n) : β ∈ B_right}`

## D-CTG — VSpaceContiguity (INV, predicate)

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`
