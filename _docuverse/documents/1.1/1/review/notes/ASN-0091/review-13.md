# Review of ASN-0091

## REVISE

### Issue 1: Circular discharge of S3★ for REARRANGE_K
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "S3★ holds at Σ' because the subspace-preservation forced by RA-adm + L14 keeps each content-subspace V-position's image in dom(Σ'.C) = dom(Σ.C) (RE-C) and each link-subspace V-position's image in dom(Σ'.L) = dom(Σ.L) (RE-L)."
**Problem**: RA-adm is the definitional clause requiring Σ' to satisfy all foundation invariants, S3★ included. Using "RA-adm + L14" to derive subspace preservation (which is exactly a consequence of S3★ + L14) makes this a circular discharge of RA-adm. The actual mechanism is that R-PPERM/R-SPERM construct π by listing a non-S identity branch and an in-subspace branch (cut subspace = s_C, permuted within s_C only) — so π is subspace-preserving by construction, not by assumption.
**Required**: Reword to ground the discharge in constructive premises: R-PPERM/R-SPERM's per-branch construction gives subspace-preservation of π, R-FRAME-P/S(a) gives pointwise preservation on non-S, and pre-state S3★ at Σ combined with RE-C/RE-L extends the image-store correspondence to Σ'. Remove the "RA-adm + L14" appeal.

### Issue 2: Missing S3★-aux citation in RE-trans derivation
**ASN-0091, "Cross-Document Transclusion Preserved"**: "By CL-OWN (ASN-0047), every link-subspace V-position in d maps to a link with origin = d, so a foreign address a with origin(a) ≠ d cannot arise at a link-subspace V-position; the V-position witnessing a ∈ ran(Σ.M(d)) is therefore content-subspace..."
**Problem**: The inference "therefore content-subspace" requires V-positions in dom(M(d)) to be exhaustively content or link subspace. CL-OWN only excludes link-subspace; the exhaustiveness step needs S3★-aux (ASN-0047), which is uncited at this site.
**Required**: Insert citation of S3★-aux at the "therefore content-subspace" step: "...by S3★-aux (ASN-0047), V-positions in dom(M(d)) are either content-subspace or link-subspace, so v is content-subspace, after which S3★ gives a ∈ dom(Σ.C)."

### Issue 3: ★-form chaining for non-RE-trans equalities is too brief
**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences"**: "RE-C★, RE-L★, RE-dom★, RE-ran★, RE-other★, RE-sub★, RE-R★: equalities X(Σ₀) = X(Σ_n) follow by chaining X(Σᵢ) = X(Σᵢ₊₁) across the n steps."
**Problem**: For RE-dom★, RE-ran★, RE-sub★ the document parameter d is the *single-step* target, but across a sequence the target varies per step. RE-trans★ correctly handles this with an explicit per-step case-split (dᵢ = d vs. dᵢ ≠ d using RE-other for the second case). The other equality-chained claims need the same treatment to type-check — e.g., RE-other★ holds for d' only when no step in the sequence targets d'; RE-dom★/RE-ran★/RE-sub★ for a fixed d use RE-ran/RE-other depending on whether dᵢ = d. The current "chaining transitively" is too brief.
**Required**: Either (a) explicitly model the per-step case-split for each ★ form on the RE-trans★ pattern, or (b) state once that "for each fixed d, the per-step preservation chains by the same case-split as RE-trans★, with RE-other applying when the step's target dᵢ ≠ d."

## OUT_OF_SCOPE

The Open Questions enumerate appropriate future-ASN territory (link-subspace REARRANGE semantics, observational discoverability equivalence, run-cardinality upper bounds, cut-sequence completeness). No additional out-of-scope topics to flag.

VERDICT: REVISE
