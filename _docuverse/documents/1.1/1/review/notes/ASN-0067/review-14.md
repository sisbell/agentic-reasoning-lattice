# Review of ASN-0067

## REVISE

### Issue 1: Missing source-subspace restriction on content references

**ASN-0067, COPY Preconditions (P.1–P.7)**: The preconditions restrict the *target* to the content subspace (P.7: `subspace(v) = s_C`) but impose no subspace restriction on the *source* content references.

**Problem**: The invariant preservation proof for S3 and the K.ρ precondition both depend on resolved I-addresses being in `dom(C)`. This is established by citing C1 (ResolutionIntegrity, ASN-0058), whose derivation invokes S3 (ASN-0036): `M(d_s)(v) ∈ dom(C)`. In the extended state, S3 is superseded by S3★, which distinguishes subspaces: content-subspace V-positions map to `dom(C)`, link-subspace V-positions map to `dom(L)`. If a content reference specifies a link-subspace V-span (`u₁ = s_L`), the resolved addresses are in `dom(L)`, not `dom(C)`. Placing them at content-subspace V-positions violates S3★. The K.ρ precondition (`a ∈ dom(C)`) also fails, since `dom(C) ∩ dom(L) = ∅` by L14.

The ContentReference definition (ASN-0058) does not formally restrict `u₁` to `s_C` — the name suggests content subspace, but the definition permits any subspace satisfying the structural conditions.

**Required**: Add a precondition (e.g., P.4a) requiring that each source reference `rⱼ = (d_sⱼ, σⱼ)` with `σⱼ = (uⱼ, ℓⱼ)` satisfies `subspace(uⱼ) = s_C`. Alternatively, note in the S3 verification that C1 applies because the source V-spans are content-subspace spans, under which S3★ reduces to S3 for the relevant positions.

### Issue 2: Incorrect T7 citation for V-position subspace disjointness

**ASN-0067, Well-Formedness of B', B2 (Disjointness)**: "B_other blocks have (v_β)₁ ≠ S, while B_pre, placed blocks, and shifted B_post all have first component S — disjoint by T7 (SubspaceDisjointness, ASN-0034)."

**Problem**: T7 is stated for element-level tumblers with `zeros(a) = 3`, using the notation `a.E₁` — the first component of the element field as parsed by T4 (HierarchicalParsing). V-positions have `zeros(v) = 0`; T4 assigns them no element field (they parse as node addresses). T7 does not apply to V-positions. The conclusion is correct: tumblers with different first components are distinct, which follows directly from T3 (CanonicalRepresentation) — if `a₁ ≠ b₁`, then `a ≠ b` since they differ at component 1.

**Required**: Replace the T7 citation with T3, or argue directly: V-positions with `(v_β)₁ ≠ S` differ from those with first component `S` in their first component, hence are distinct tumblers by T3.

## OUT_OF_SCOPE

None. The ASN's scope is well-bounded and the open questions correctly identify deferred topics.

VERDICT: REVISE
