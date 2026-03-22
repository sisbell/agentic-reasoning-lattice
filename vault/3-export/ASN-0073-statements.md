# ASN-0073 Formal Statements

*Source: ASN-0073-streams-0.md (revised 2026-03-22) — Extracted: 2026-03-22*

## ValidInsertionPosition — ValidInsertionPosition (DEF, predicate)

A V-position v is a *valid insertion position* in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅ with |V_S(d)| = N. Write m for the common V-position depth in subspace S (S8-depth); m ≥ 2. Then either v = min(V_S(d)) (the j = 0 case) or v = shift(min(V_S(d)), j) for some j with 1 ≤ j ≤ N. In both cases, #v = m.

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m ≥ 2. In both cases, S = v₁ is the subspace identifier.

**Structural claims:**

(a) *Explicit form.* shift(min(V_S(d)), j) = [S, 1, ..., 1 + j]. By D-MIN, min(V_S(d)) = [S, 1, ..., 1] of depth m. By OrdinalShift and TumblerAdd, shift([S, 1, ..., 1], j) = [S, 1, ..., 1] ⊕ δ(j, m); since δ(j, m) has action point m and m ≥ 2, TumblerAdd copies components 1 through m − 1 unchanged and sets the last component to 1 + j.

(b) *Distinctness.* The N + 1 positions have last components 1 (for j = 0), 2, 3, ..., N + 1 (for j = 1, ..., N). These are pairwise distinct natural numbers, so by T3 (CanonicalRepresentation) the N + 1 tumblers are pairwise distinct.

(c) *Depth preservation.* For j ≥ 1, #shift(v, j) = #v = m by the result-length identity of OrdinalShift. For j = 0, #v = #min(V_S(d)) = m by D-MIN. In the empty case, #v = m by construction.

(d) *Subspace identity.* Since δ(j, m) has action point m ≥ 2, TumblerAdd copies component 1 unchanged: shift(min, j)₁ = min₁ = S for all j ≥ 1. For j = 0, v₁ = min₁ = S directly.

(e) *S8a consistency.* For text-subspace positions (S ≥ 1), every valid position [S, 1, ..., 1 + j] has all components strictly positive (S ≥ 1, intermediate components are 1, last component is 1 + j ≥ 1), so zeros(v) = 0 and v > 0.

**Count.** In the non-empty case, there are exactly N + 1 valid insertion positions: the N positions coinciding with existing V-positions v₀ through v_{N−1}, plus the append position shift(min(V_S(d)), N). In the empty case, exactly one position is valid for any given depth m.
