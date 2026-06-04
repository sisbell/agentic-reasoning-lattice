# Review of ASN-0091

## REVISE

### Issue 1: Circularity-reassurance prose in Per-Invariant Discharges
**ASN-0091, "Per-Invariant Discharges"**: "This layer is independent of K.μ~ and supplies exactly the shape invariants (S8a, S8-depth, D-CTG★, D-MIN★) that K.μ~'s admissibility clause (i) requires, so no circularity arises" — and the section header gloss "RA-adm is discharged in three layers, none circular against K.μ~'s admissibility."
**Problem**: This is the "non-circular by Y argument" accretion pattern. The discharge either consults K.μ~ or it does not; the reader establishes that from the cited premises (RA-dom, structural projections). The standing reassurance that no circularity arises does not advance the derivation and must be worked around.
**Required**: State the dependency facts (shape package depends only on RA-dom; clause (i) consumes the shape package) and delete the meta-claims about circularity.

### Issue 2: Worked Examples 1 and 2 duplicate the full RE-* verification list
**ASN-0091, "Worked Example — 4-cut Swap"**: the Verification list reproduces RE-C, RE-L, RE-dom, RE-ran, RE-μ, RE-cov, RE-disc, RE-proj, RE-other, RE-trans, RE-sub, RE-origin, RE-R already fully discharged in the first Worked Example, and the admissibility paragraph concedes "by the per-invariant discharge of the first Worked Example, with five V-positions in place of four. The only structurally distinctive clause under the 4-cut swap is S8★."
**Problem**: The interior-cut and bijection examples are already economical (they verify only the distinctive claims). The 3-cut/4-cut pair, by contrast, runs the same near-verbatim list twice. This is the "two paragraphs say the same thing in different words" pattern at trace scale.
**Required**: Reduce the 4-cut example to its genuine deltas (the μ-region displacement Δ(μ), R-SPERM, and the S8★ run-decomposition), citing the first example for every clause that "discharges exactly as in the first Worked Example."

### Issue 3: RE-sub and RE-ext restate the same abstract-vs-specific meta-distinction
**ASN-0091, "Subspace Frame" and "In-Subspace Exterior Frame"**: "The pointwise-fixity strengthening — both RE-sub's fixity on non-S V-positions and RE-ext's fixity on in-subspace exterior V-positions — is REARRANGE_K-specific, not abstract: a different concrete realisation ... could non-trivially permute ... and would still satisfy RA-adm" (RE-ext), echoing RE-sub's "admissibility allows non-identity permutations within each subspace under the abstract class" and "The subspace-preservation half is structurally necessary at the abstract level."
**Problem**: Two structurally parallel sections carry the identical "abstract admissibility permits within-subspace permutation; REARRANGE_K's cut sequence does not" point. The recent revise ("merge RE-sub/RE-ext specificity note") consolidated part of this; the closing paragraphs still duplicate the distinction.
**Required**: State the abstract-vs-REARRANGE_K-specific distinction once (it is identical for both frames) and have each section assert only its own pointwise clause.

### Issue 4: P4★ verified under the "Admissibility (RA-adm)" heading despite being excluded from RA-adm's scope
**ASN-0091, RA-adm definition**: "(composite-boundary properties P4★/P4a/P7a and state-independent theorems S5, T0(a/b) lie outside its scope, discharged by their own arguments)". **Worked Example 1, Admissibility (RA-adm)**: "*P4★:* `Contains_C(Σ') = ... = Contains_C(Σ)` ... so the pre-state inclusion `Contains_C(Σ) ⊆ Σ.R` carries over."
**Problem**: RA-adm definitionally excludes P4★, yet the worked example discharges P4★ inside a paragraph headed "Admissibility (RA-adm)," and P4a is likewise handled there. A precise reader who took RA-adm's scope clause at face value finds it contradicted by its own verification trace.
**Required**: Re-head the composite-boundary discharges (P4★, P4a, P7a) in the worked examples so they are not attributed to RA-adm, or relabel them as the separate composite-boundary layer the Per-Invariant Discharges section already names.

### Issue 5: The ★-form catalogue re-derives one case-split per claim
**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences"**: RE-dom★, RE-ran★, RE-μ★, RE-trans★ each independently spell out "at each step targeting `dᵢ`, either `dᵢ = d` (per-step claim applies) or `dᵢ ≠ d` (RE-other applies)."
**Problem**: The identical document-parameterised case split is restated four-plus times. This is repetitive boilerplate that the reader must re-read rather than reference.
**Required**: State the case-split lemma once ("a document-parameterised single-step equality at `d` chains across the sequence because every non-targeting step satisfies RE-other"), then cite it from each ★ claim.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The Open Questions correctly defer "what semantics rearrangement should carry on the link subspace" to a future ASN; this note fixes the cut subspace at S = s_C and is not obligated to specify link-subspace reordering.

### Topic 2: Upper bound on run-decomposition cardinality growth
**Why out of scope**: RE-frag establishes that cardinality can strictly increase; bounding the increase per invocation is a distinct quantitative result appropriately listed as an Open Question.

VERDICT: REVISE
