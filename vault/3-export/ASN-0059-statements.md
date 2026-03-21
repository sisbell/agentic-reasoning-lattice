# ASN-0059 Formal Statements

*Source: ASN-0059-insert-operation.md (revised 2026-03-20) — Extracted: 2026-03-21*

## Definition — OrdinalDisplacement

For n ≥ 1 and m ≥ 1, δ(n, m) = [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m, with action point m.

## Definition — OrdinalShift

For a V-position v of depth m and n ≥ 1, shift(v, n) = v ⊕ δ(n, m).

By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n.

## Definition — ShiftBlock

For β = (v, a, k) ∈ B_right and n ≥ 1:

`shift_block(β, n) = (shift(v, n), a, k)`

The V-start shifts but the I-start and width are unchanged.

## Definition — VContiguity

The text-subspace V-positions of document d in subspace S are *contiguous* when, letting V_S = {v ∈ dom(M(d)) : subspace(v) = S}, either V_S = ∅ or:

`(A u, w : u ∈ V_S ∧ w ∈ V_S ∧ u < w : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < w : v ∈ V_S))`

---

## I0 — FreshContiguousAllocation (POST, ensures)

Parameters: document d, V-position p, values (val₁, ..., valₙ) with n ≥ 1. Allocates addresses a₁, ..., aₙ:

(i) aᵢ ∉ dom(C) for 1 ≤ i ≤ n.

(ii) aᵢ₊₁ = aᵢ + 1 for 1 ≤ i < n, where + is ordinal increment via TA5(c).

(iii) origin(aᵢ) = d for 1 ≤ i ≤ n.

(iv) C' = C ∪ {aᵢ ↦ valᵢ : 1 ≤ i ≤ n}.

## I1 — PreInsertionStability (POST, ensures)

S = subspace(p) = p₁:

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## I2 — ContentPlacement (POST, ensures)

a₁ is the first allocated I-address from I0:

`(A k : 0 ≤ k < n : p + k ∈ dom(M'(d)) ∧ M'(d)(p + k) = a₁ + k)`

where p + k and a₁ + k are k ordinal increments via TA5(c).

## I3 — PostInsertionShift (POST, ensures)

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

## I4 — SubspaceStability (POST, ensures)

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## I5 — DocumentIsolation (POST, ensures)

`(A d' : d' ≠ d : M'(d') = M(d'))`

## I8 — InsertionPrecondition (PRE, requires)

INSERT(d, p, vals) requires:

(i) d ∈ E_doc.

(ii) p satisfies S8a: all components strictly positive, zeros(p) = 0.

(iii) subspace(p) = S where S ≥ 1.

(iv) When V_S = {v ∈ dom(M(d)) : subspace(v) = S} is non-empty, #p equals the common depth of V_S (S8-depth). When V_S = ∅, #p establishes the depth for the subspace.

(v) n ≥ 1.

(vi) #p ≥ 2.

## I9 — ContiguityPreservation (LEMMA, lemma)

If V_S is contiguous before INSERT, and p satisfies v_min ≤ p ≤ v_max + 1 (where v_min, v_max are the minimum and maximum of V_S; for V_S = ∅ any p is valid), then V_S is contiguous after INSERT.

## I10 — BlockDecompositionEffect (POST, ensures)

Let B be the block decomposition of M(d). Let B_S = {β = (v, a, k) ∈ B : subspace(v) = S} and B_other = B \ B_S.

Partition B_S relative to insertion point p:

(a) *Entirely before:* v + k ≤ p.

(b) *Entirely at or after:* v ≥ p.

(c) *Straddling:* v < p and v + k > p. Split β at offset c = pₘ − vₘ into β_L = (v, a, c) and β_R = (p, a + c, k − c).

Let B_left = {blocks from case (a)} ∪ {β_L if case (c) applies}.
Let B_right = {blocks from case (b)} ∪ {β_R if case (c) applies}.

`B' = B_other ∪ B_left ∪ {(p, a₁, n)} ∪ {shift_block(β, n) : β ∈ B_right}`

## TS1 — ShiftPreservesOrder (LEMMA, lemma) [cited ASN-0034]

For v₁, v₂ with #v₁ = #v₂ = m and v₁ < v₂:

`shift(v₁, n) < shift(v₂, n)`

## TS2 — ShiftInjective (LEMMA, lemma) [cited ASN-0034]

For v₁, v₂ with #v₁ = #v₂ = m:

`shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂`
