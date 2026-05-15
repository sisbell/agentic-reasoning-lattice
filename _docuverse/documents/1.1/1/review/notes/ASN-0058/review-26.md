# Review of ASN-0058

## REVISE

### Issue 1: M2's proof under-specifies the vocabulary translation
**ASN-0058, M2 (DecompositionExistence)**: "This is S8 (SpanDecomposition, ASN-0036) restated in our vocabulary — both range over every V-position in `dom(M(d))`, regardless of subspace, and M2 inherits S8's preconditions verbatim."
**Problem**: The translation from S8's correspondence runs to M2's mapping blocks is not 1-1 in conjuncts. S8 has two conjuncts ((a) coverage with E! and (b) consistency); M2 has three (B1, B2, B3). B1 and B2 are jointly equivalent to S8(a)'s E! quantifier (existence + uniqueness). Furthermore, S8(a)'s denotation range `vⱼ ≤ v < shift(vⱼ, nⱼ)` is a tumbler interval that includes positions at depths other than `#vⱼ`, whereas V(βⱼ) is the depth-`#vⱼ` discrete orbit; their coincidence on `dom(M(d))` requires invoking S8-depth and S8a.
**Required**: Spell out the explicit mapping: B1 ↔ existence in S8(a)'s E!; B2 ↔ uniqueness in S8(a)'s E!; B3 ↔ S8(b). Note that S8(a)'s range coincides with V(βⱼ) when restricted to `dom(M(d))` via S8-depth/S8a.

### Issue 2: M7's overlap case proof is overly dense
**ASN-0058, M7 (MergeCondition)**: "The case `v₂ < v₁ + n₁` (overlap) cannot occur when `β₁, β₂ ∈ B`. Since `β₁, β₂ ∈ B` and B is a decomposition of `M(d)`, B3 places `v₁, v₂ ∈ dom(M(d))`..."
**Problem**: A single paragraph compresses five layered arguments simultaneously: T1(i) divergence at component 1, subspace inheritance, S8-depth uniformity transfer, divergence-at-minimum-index iteration with `j₀ = min(J)`, and component-m reduction to ordinal shift culminating in `v₂ = v₁ + k` with `k ∈ [1, n₁)`. Verifying the proof requires tracking all five threads at once and recovering implicit T1 case (i) instantiations. The steps are correct, but the combined argument is hard to audit.
**Required**: Extract this argument as a named sub-lemma (e.g., "M7-cov: For β₁, β₂ in any decomposition with v₁ < v₂, then v₂ ≥ v₁ + n₁"). State its preconditions explicitly and separate the four steps — subspace agreement, depth equality, prefix agreement (components 1..m−1), component-m reduction — as numbered claims.

### Issue 3: M12 canonical uniqueness proof packs multiple intricate sub-arguments
**ASN-0058, M12 (CanonicalUniqueness)**: "We show that every maximally merged decomposition equals the set of *maximal runs* of `f = M(d)`, and that this set is uniquely determined by `f`."
**Problem**: The proof has three interleaved sub-arguments: (1) maximal runs partition `dom(f)` — itself requiring an intricate "exactly one maximal run contains v" argument with subspace/depth analysis mirroring M7's overlap case; (2) the (⟹) direction with right-extension and left-extension impossibility, each with its own dense divergence analysis; (3) the (⟸) direction. Subspace/depth machinery is reused inline multiple times without being lifted, and the same structural skeleton (subspace identification → S8-depth → prefix agreement → reduction to component m) recurs in M7, M12-partition, and M12-extension without being abstracted.
**Required**: Extract named sub-lemmas: (a) "M12a: Maximal runs of f pairwise have disjoint V-extents"; (b) "M12b: In a maximally merged decomposition, no block can be left-extended or right-extended as a maximal run". This would let the shared "two depth-m V-positions in M(d) cannot V-overlap" structural argument be cited once rather than re-derived twice.

## OUT_OF_SCOPE

None substantive. The Open Questions at the end correctly identify topics for future ASNs (lattice structure of decompositions, depth constraints between V and I starts, multi-source resolution ordering, etc.).

VERDICT: REVISE
