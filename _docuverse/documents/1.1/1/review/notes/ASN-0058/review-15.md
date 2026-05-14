# Review of ASN-0058

## REVISE

### Issue 1: M5(b) disjointness skips an injectivity step
**ASN-0058, M5(b) Verification**: "V(β_L) = {v + k : 0 ≤ k < c} and V(β_R) = {v + k : c ≤ k < n}. The ranges [0, c) and [c, n) are disjoint, so V(β_L) ∩ V(β_R) = ∅."
**Problem**: Disjointness of the integer ranges [0, c) and [c, n) implies disjointness of the V-extents only if the map k ↦ v + k is injective on [0, n). That injectivity is established in M0's proof (via TS4/TS5) but M5 does not cite it. As stated, the argument is missing the inferential step from index-range disjointness to V-extent disjointness.
**Required**: Cite M0 (or M1, or the underlying TS4/TS5 monotonicity) when concluding that disjoint index ranges yield disjoint V-extents.

### Issue 2: M12 "immediate successor in the linear order" is false as stated
**ASN-0058, M12 proof (⟹, condition 3 fails)**: "So v' > v + n − 1, hence v' ≥ v + n (TS4/TS5: v + n is the immediate successor of v + n − 1 in the linear order, so there is no tumbler strictly between them)."
**Problem**: This claim is false in T's full linear order — tumblers such as (v + (n−1)).0, (v + (n−1)).0.0, …, (v + (n−1)).k for k ≥ 1 all lie strictly between v + (n − 1) and v + n by T1. TS4 (strict increase) and TS5 (strict monotonicity in the second argument) do not establish "immediate successor in the linear order"; they only establish strict monotonicity of shift. The conclusion v' ≥ v + n holds in this proof only because v' is constrained to depth m in v's subspace, and depth-m tumblers in one subspace are enumerated by their m-th component alone.
**Required**: Replace the false universal claim with the actual fact: among depth-m tumblers sharing the first m − 1 components with v₁, v + n is the smallest strictly greater than v + (n − 1). Justify via T1 reducing to component m once depth and prefix agreement are fixed.

### Issue 3: M12 condition 3 sub-case omits depth justification for v'
**ASN-0058, M12 proof (⟹, condition 3 fails)**: "the depth-m unit shift is injective (it increments only the m-th component), so v + (n − 1) = v' + (j − 1) ∈ V(β')."
**Problem**: For the depth-m unit-shift argument to apply uniformly to (v + (n−1)) + 1 and (v' + (j−1)) + 1, both v + (n − 1) and v' + (j − 1) must have depth m. The proof states "depth-m" but does not justify why v' (and hence v' + (j − 1)) has depth m. The required chain — v + n ∈ V(β'); OrdShiftHom gives subspace(v + n) = subspace(v); β' is in v + n's subspace, hence in v's subspace; S8-depth fixes that subspace's common depth at m; so #v' = m — should be made explicit.
**Required**: State the OrdShiftHom + S8-depth derivation that establishes #v' = m before invoking the depth-m unit-shift's injectivity.

### Issue 4: M12 condition 2 sub-case skips the "v' is the last position" derivation
**ASN-0058, M12 proof (⟹, condition 2 fails)**: "Since v' + 1 = v ∈ V(β), if v ∈ V(β'') then v ∈ V(β'') ∩ V(β), contradicting B2. So v' is the last position of β'': v' = v'' + (n'' − 1)."
**Problem**: The leap from "v ∉ V(β'')" to "v' is the last position of β''" is not stated. The required argument: v' ∈ V(β'') means v' = v'' + k for some 0 ≤ k < n''; if k < n'' − 1, then v'' + (k + 1) ∈ V(β''); by M-aux, v'' + (k + 1) = (v'' + k) + 1 = v' + 1 = v; so v ∈ V(β''), contradicting v ∉ V(β''); therefore k = n'' − 1.
**Required**: Insert the M-aux step ruling out k < n'' − 1 before concluding v' is the last position.

### Issue 5: M7 overlap case omits the prefix-agreement step for v₂
**ASN-0058, M7 necessity argument (overlap case)**: "M-aux gives v₁ + n₁ the same first m − 1 components as v₁, and T1 then reduces the comparison v₁ ≤ v₂ < v₁ + n₁ to component m"
**Problem**: T1 reduces the chained comparison to component m only after establishing (v₂)_j = (v₁)_j for all 1 ≤ j < m. The proof states the prefix-agreement fact for v₁ + n₁ vs. v₁ but not for v₂ vs. v₁. The required step: if v₁ and v₂ first diverged at some j₀ < m with (v₂)_{j₀} > (v₁)_{j₀}, then (v₂)_{j₀} > (v₁ + n₁)_{j₀} (since v₁ + n₁ agrees with v₁ at j₀ < m by TumblerAdd), giving v₂ > v₁ + n₁ by T1(i), contradicting v₂ < v₁ + n₁.
**Required**: Insert the case-elimination step forcing (v₂)_j = (v₁)_j for j < m before reducing the comparison to position m.

### Issue 6: M13 (SharedContent) lacks a derivation
**ASN-0058, M13**: "(E Σ : Σ satisfies S0–S3 : (E d, a :: |{v : M(d)(v) = a}| > 1))"
**Problem**: This is an existential claim, but the body provides no explicit witness and no explicit reduction. The text appeals informally to "transclusion" and notes "consistency with S5", without invoking S5 at a specific instantiation. An existential of this form should be discharged either by exhibiting a concrete Σ or by an explicit application of S5 at N = 1 with the within-a-single-document branch of S5's construction.
**Required**: Either give a one-paragraph concrete witness (e.g., a document with two mapping blocks ([1,1], a, 1) and ([1,5], a, 1) sharing I-start a at distinct V-positions, verifying S0–S3) or explicitly invoke S5 at N = 1 with the within-document branch.

### Issue 7: M7 overlap case — V_{v₁}(d) notation conflates membership and label
**ASN-0058, M7 necessity argument (overlap case)**: "By OrdShiftHom (ASN-0036), v₁ + n₁ shares subspace V_{v₁}(d) with v₁."
**Problem**: V_{s}(d), as used in S8-depth, denotes the *set* of V-positions in dom(M(d)) with subspace label s. The tumbler v₁ + n₁ may not be in dom(M(d)) at all (the overlap case is exactly the case where v₂ < v₁ + n₁, so v₁ + n₁ need not appear as a block's V-position). What OrdShiftHom delivers is the subspace label identity subspace(v₁ + n₁) = subspace(v₁), not membership in the set V_{v₁}(d).
**Required**: Rephrase to "subspace(v₁ + n₁) = subspace(v₁) by OrdShiftHom" (and separately invoke S8-depth on subspace(v₁) once v₂'s membership in dom(M(d)) is leveraged), keeping subspace identity distinct from set membership.

VERDICT: REVISE
