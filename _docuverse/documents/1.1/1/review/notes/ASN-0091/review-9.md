# Review of ASN-0091

## REVISE

### Issue 1: Equality realizability claim is informally asserted but not formally witnessed

**ASN-0091, "Run Decomposition Is Not Invariant"**: "Together, RE-frag and RE-coal record that the maximal-run-decomposition cardinality is *neither monotonically non-decreasing nor monotonically non-increasing nor invariant* under REARRANGE — every relation between pre- and post-state cardinality (strict increase, strict decrease, equality) is realizable."

**Problem**: RE-frag witnesses strict increase; RE-coal witnesses strict decrease. The prose's "equality is realizable" claim has no formal backing — no RE-eq lemma, no equality-preserving witness. Under REARRANGE_K specifically, the cut-sequence structure forces non-identity π, so a cardinality-preserving REARRANGE_K instance must be exhibited, not assumed.

**Required**: Either temper the prose to match the formal claims (drop the equality clause), or add an explicit equality witness — e.g., a 3-cut pivot of two singletons from disjoint chains, where the post-state still has the same two singletons (now V-swapped) and total cardinality is preserved.

### Issue 2: RE-sub prose conflates π pointwise fixity with M(d) preservation

**ASN-0091, "Subspace Frame"**: "The pointwise form of RE-sub — that non-S V-positions are not permuted at all, not merely kept within their subspace — is what the cut-sequence structure supplies and what admissibility alone does not."

**Problem**: The formal RE-sub statement is `Σ'.M(d)(v) = Σ.M(d)(v)` for non-S V-positions — a claim about the arrangement, not about π. Under S5 (shared I-addresses), π could permute V-positions with identical M(d) values without violating M(d) preservation. The "not permuted at all" prose refers to π's behavior under R-PPERM/R-SPERM, which is genuinely pointwise (the constructions write `π(v) = v` for non-S v directly), but RE-sub as formally stated does not capture this. The prose claim about π is strictly stronger than the formal RE-sub statement.

**Required**: Either (a) separate the π-fixity property into a distinct claim (e.g., RE-sub-π) attributed directly to R-PPERM/R-SPERM, leaving RE-sub as the M(d) statement; or (b) strengthen RE-sub's formal statement to assert `π(v) = v` for non-S v, with derivation traced through R-PPERM/R-SPERM rather than R-FRAME-P/S(a).

### Issue 3: RE-proj's π-invariance under witness choice is implicit but not derived

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "Every RE-* claim derived from RA-π below is parameterised by the specific π witnessing the transition; RE-proj in particular states `project(e, d, Σ') = π(project(e, d, Σ))` for whichever π witnesses Σ → Σ', not for an arbitrary bijection."

**Problem**: When `Σ.M(d)` has shared I-addresses, π is not unique (the ASN notes this). The LHS `project(e, d, Σ')` is fixed (state-determined, independent of π choice), so for the RE-proj equation to hold across different π witnesses, the RHS `π(project(e, d, Σ))` must yield the same image-set for any valid π. This invariance — that π's freedom within arrangement pre-images preserves the projection image because the projection respects the pre-image partition — is load-bearing for RE-proj's interpretation as a property of Σ' (not of the triple (Σ, Σ', π)). The ASN never derives it.

**Required**: Add a short paragraph after RE-proj noting that for any v, v' in the same pre-image `Σ.M(d)⁻¹(a)`, both belong to `project(e, d, Σ)` or neither does (depending on whether `a ∈ coverage(e)`), so swapping them within π leaves `π(project(e, d, Σ))` unchanged as a set. This discharges the well-definedness of RE-proj across witnesses.

### Issue 4: Substrate-emittable closure used silently in LP-Fin Corollary applications

**ASN-0091, Worked Example**: "By LP-Fin Corollary (ASN-0098), `coverage(e₁) ∩ (dom(Σ.C) ∪ dom(Σ.L)) = {b₁}` — the single first emission of `A_C(d)` is the only F-candidate the canonical span admits in the interval."

**Problem**: LP-Fin Corollary gives `F ∩ [s, s ⊕ ℓ) = {chain elements}`. The ASN steps from this directly to the intersection with `dom(C) ∪ dom(L)`. The bridge — that `dom(C) ∪ dom(L) ⊆ F` (every emitted address is substrate-emittable) — is true but used silently. A reader without this fact in mind cannot follow the inference.

**Required**: One sentence in the example introduction noting that every emitted content/link address lies in F (by SubstrateEmittableAddresses / sub-allocator chain discipline), so `coverage ∩ (dom(C) ∪ dom(L)) = coverage ∩ F ∩ (dom(C) ∪ dom(L))`, after which LP-Fin Corollary identifies the F-side intersection.

## OUT_OF_SCOPE

The Open Questions section already identifies the natural extensions (cross-document transclusion fragmentation guarantees, link-subspace rearrangement semantics, observational equivalence at the discoverability level, run-cardinality upper bounds, completeness of cut-sequence rearrangements relative to all admissible bijections). Nothing additional to flag.

VERDICT: REVISE
