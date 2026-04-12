**Definition (ValidInsertionPosition).** A V-position v is a *valid insertion position* in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅ with |V_S(d)| = N. Write m for the common V-position depth in subspace S (S8-depth); m ≥ 2, since the first position placed in any subspace is established by the empty case, which requires m ≥ 2, and S8-depth preserves depth thereafter. Then either v = min(V_S(d)) (the j = 0 case) or v = shift(min(V_S(d)), j) for some j with 1 ≤ j ≤ N. In both cases, #v = m.

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m ≥ 2, establishing the subspace's V-position depth at m. The lower bound m ≥ 2 is necessary: at m = 1, v = [S] and shift([S], 1) = [S] ⊕ δ(1, 1) = [S] ⊕ [1]; the action point of [1] is k = 1, so TumblerAdd gives r₁ = S + 1, producing [S + 1] — a position in subspace S + 1, not S. For m ≥ 2, δ(n, m) has action point m, and since m > 1, TumblerAdd copies component 1 unchanged — OrdinalShift preserves the subspace identifier. This is the canonical minimum position required by D-MIN. The choice of m is a one-time structural commitment: once any position is placed, S8-depth fixes the depth for all subsequent positions in the subspace.

In both cases, S = v₁ is the subspace identifier.

In the non-empty case, there are exactly N + 1 valid insertion positions: the N positions coinciding with existing V-positions v₀ through v_{N−1}, plus the append position shift(min(V_S(d)), N). In the empty case, there is one valid position per choice of depth m — but since m is chosen once and then held fixed by S8-depth, exactly one position is valid for any given depth.

We verify the structural claims. By D-MIN, min(V_S(d)) = [S, 1, ..., 1] of depth m. By OrdinalShift and TumblerAdd, shift([S, 1, ..., 1], j) = [S, 1, ..., 1] ⊕ δ(j, m); since δ(j, m) has action point m and m ≥ 2, TumblerAdd copies components 1 through m − 1 unchanged and sets the last component to 1 + j. The explicit form is shift(min(V_S(d)), j) = [S, 1, ..., 1 + j].

*Distinctness.* The N + 1 positions have last components 1 (for j = 0, where v = min(V_S(d))), 2, 3, ..., N + 1 (for j = 1, ..., N). These are pairwise distinct natural numbers, so by T3 (CanonicalRepresentation, ASN-0034) the N + 1 tumblers are pairwise distinct.

*Depth preservation.* For j ≥ 1, #shift(v, j) = #v = m by the result-length identity of OrdinalShift (ASN-0034). For j = 0, #v = #min(V_S(d)) = m by D-MIN. In the empty case, #v = m by construction. All valid positions have the common V-position depth required by S8-depth.

*Subspace identity.* Since δ(j, m) has action point m ≥ 2, TumblerAdd copies component 1 unchanged: shift(min, j)₁ = min₁ = S for all j ≥ 1. For j = 0, v₁ = min₁ = S directly.

*S8a consistency.* For text-subspace positions (S ≥ 1), every valid position [S, 1, ..., 1 + j] has all components strictly positive (S ≥ 1, intermediate components are 1, last component is 1 + j ≥ 1), so zeros(v) = 0 and v > 0 — satisfying S8a.

### Valid insertion position examples

**Non-empty case.** Let subspace S = 1 and suppose V₁(d) = {[1, 1], [1, 2], [1, 3]}, so N = 3 and min(V₁(d)) = [1, 1]. The valid insertion positions are:

- j = 0: v = min(V₁(d)) = [1, 1]
- j = 1: v = shift([1, 1], 1) = [1, 2]
- j = 2: v = shift([1, 1], 2) = [1, 3]
- j = 3: v = shift([1, 1], 3) = [1, 4]

That gives N + 1 = 4 positions. After an operation places new content at, say, [1, 2] — with whatever displacement mechanism the operation defines — the resulting V₁(d) must satisfy D-CTG and D-MIN. Verifying this is the operation's obligation, not the predicate's.

**Empty case.** V₁(d) = ∅. Choosing depth m = 2, the valid insertion position is [1, 1]. D-MIN requires min(V₁(d)) = [1, 1] once the subspace becomes non-empty, so the position is exactly the one D-MIN demands. Choosing m = 3 instead would give [1, 1, 1]; by T3, this is a different tumbler — once chosen, S8-depth locks the subspace to depth 3 for all future positions.

*Formal Contract:*
- *Definition:* A V-position v is a valid insertion position in subspace S of document d when: (a) V_S(d) ≠ ∅ with |V_S(d)| = N and v = shift(min(V_S(d)), j) for 0 ≤ j ≤ N (where shift(·, 0) is identity); or (b) V_S(d) = ∅ and v = [S, 1, ..., 1] of depth m ≥ 2.
- *Preconditions:* d satisfies D-CTG, D-MIN, S8-depth, S8a; S ≥ 1; in the non-empty case, m ≥ 2 (inherited from the empty-case establishment and S8-depth).
- *Postconditions:* (i) #v = m (depth preservation); (ii) v₁ = S (subspace identity); (iii) zeros(v) = 0 ∧ v > 0 (S8a compliance); (iv) the N + 1 valid positions in the non-empty case are pairwise distinct.
