**Definition (ValidInsertionPosition).** Given a depth parameter m ≥ 2, a V-position v is a *valid insertion position* for depth m in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅. By S8-fin, dom(M(d)) is finite, so V_S(d) is finite with |V_S(d)| = N for some natural number N. The common V-position depth in subspace S is determined by S8-depth; since V_S(d) is non-empty, its positions lie in dom(Σ.M(d)), so S8-vdepth gives this common depth is at least 2. The parameter m must equal this common depth — the existing positions determine the only admissible value. Then either v = min(V_S(d)) (the j = 0 case) or v = shift(min(V_S(d)), j) for some j with 1 ≤ j ≤ N. In both cases, #v = m.

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m. The lower bound m ≥ 2 is required for compatibility with S7c: once this position enters dom(Σ.M(d)), S8-vdepth demands #v ≥ 2, so the parameter must satisfy the same bound. For the given m, this is the unique valid position: the tuple [S, 1, ..., 1] of depth m is fully determined by S and m. This is the canonical minimum position required by D-MIN.

In both cases, S = v₁ is the subspace identifier.

In the non-empty case, there are exactly N + 1 valid insertion positions: the N positions coinciding with existing V-positions v₀ through v_{N−1}, plus the append position shift(min(V_S(d)), N). In the empty case, the parameter m determines a unique valid position [S, 1, ..., 1] of depth m.

We verify the structural claims. By D-MIN, min(V_S(d)) = [S, 1, ..., 1] of depth m. By OrdinalShift, since m ≥ 2, the prefix rule (`shift(v, j)ᵢ = vᵢ` for `i < m`) copies components 1 through m − 1 unchanged, and the last-component increment (`shift(v, j)_m = v_m + j`) sets position m to 1 + j. The explicit form is shift(min(V_S(d)), j) = [S, 1, ..., 1 + j].

*Distinctness.* The N + 1 positions have last components 1 (for j = 0, where v = min(V_S(d))), 2, 3, ..., N + 1 (for j = 1, ..., N). These are pairwise distinct natural numbers, so by T3 (CanonicalRepresentation, ASN-0034) the N + 1 tumblers are pairwise distinct.

*Depth preservation.* For j ≥ 1, #shift(v, j) = #v = m by the result-length identity of OrdinalShift (ASN-0034). For j = 0, #v = #min(V_S(d)) = m by D-MIN. In the empty case, #v = m by construction. Since m is an independent parameter of the predicate, the postcondition #v = m is a genuine constraint: it asserts that the position's depth equals the specified depth, not merely that the position has whatever depth it happens to have. All valid positions have the depth required by S8-depth.

*Subspace identity.* Since m ≥ 2, position 1 precedes position m, and OrdinalShift's prefix rule gives shift(min, j)₁ = min₁ = S for all j ≥ 1. For j = 0, v₁ = min₁ = S directly.

*S8a consistency.* The precondition requires S ≥ 1, which is the universal condition on subspace identifiers — it holds for every subspace, text or link alike. Every valid position [S, 1, ..., 1 + j] therefore has all components strictly positive: S ≥ 1 by precondition, intermediate components are 1, and the last component is 1 + j ≥ 1. Hence zeros(v) = 0 and v > 0, satisfying S8a for all subspaces. ∎

*Formal Contract:*
- *Definition:* Given depth m ≥ 2, a V-position v is a valid insertion position for depth m in subspace S of document d when either (1) V_S(d) ≠ ∅ with |V_S(d)| = N, m equals the common depth (S8-depth, S8-vdepth gives m ≥ 2), and v = min(V_S(d)) + j for 0 ≤ j ≤ N (where + is the ordinal displacement notation of S8-depth: v + 0 = v, v + k = shift(v, k) for k ≥ 1), or (2) V_S(d) = ∅ and v = [S, 1, ..., 1] of depth m.
- *Preconditions:* d satisfies D-CTG; S is a subspace identifier (S ≥ 1); m ≥ 2; S8-fin (dom(M(d)) is finite); in the non-empty case, m equals the common depth from S8-depth and S8-vdepth gives m ≥ 2; D-MIN holds for V_S(d).
- *Postconditions:* All valid insertion positions satisfy #v = m (depth preservation — m is an independent parameter, so this constrains the position's depth to equal the specified depth), v₁ = S (subspace identity), zeros(v) = 0 ∧ v > 0 (S8a consistency); in the non-empty case, the N + 1 positions are pairwise distinct (by T3).

### Valid insertion position examples

**Non-empty case.** Let subspace S = 1 and suppose V₁(d) = {[1, 1], [1, 2], [1, 3]}, so N = 3 and min(V₁(d)) = [1, 1]. The valid insertion positions are:

- j = 0: v = min(V₁(d)) = [1, 1]
- j = 1: v = shift([1, 1], 1) = [1, 2]
- j = 2: v = shift([1, 1], 2) = [1, 3]
- j = 3: v = shift([1, 1], 3) = [1, 4]

That gives N + 1 = 4 positions. After an operation places new content at, say, [1, 2] — with whatever displacement mechanism the operation defines — the resulting V₁(d) must satisfy D-CTG and D-MIN. Verifying this is the operation's obligation, not the predicate's.

**Empty case.** V₁(d) = ∅. For depth parameter m = 2, the unique valid insertion position is [1, 1]. D-MIN requires min(V₁(d)) = [1, 1] once the subspace becomes non-empty, so the position is exactly the one D-MIN demands. For m = 3, the unique valid position is [1, 1, 1]; by T3, this is a different tumbler — once placed, S8-depth locks the subspace to depth 3 for all future positions. The depth parameter distinguishes these as different predicates: for each m, exactly one position is valid.
