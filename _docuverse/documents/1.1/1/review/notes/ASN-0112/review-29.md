# Review of ASN-0112

I checked the core arithmetic (V2 coverage in both the `#origin_d ≤ #reach_d` and `#origin_d > #reach_d` cases, the reach biconditional via D0/D1, V3 tightness via TA5/sig, V5 exactness via D-SEQ★/D-CTG★, the worked example and its depth-divergent variant). The mathematics is sound — divergence is correctly bounded by `#origin_d` in all cases, the round-trip and round-trip-failure are applied with their preconditions discharged, and the cross-subspace `r⋆` computation matches the variant. All cross-ASN references are to foundation ASNs (rule 7 satisfied). The substantive issues are anti-bloat / prose, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: wp phrasing-convention preamble is defensive meta-prose
**ASN-0112, Preconditions and well-definedness**: "Both result properties below lead with a 'no span is returned, or …' clause: on the empty result ⟨⟩ there is no σ_d, so the span-dependent half would be ill-typed, and the clause makes each predicate hold vacuously there and be well-typed over the whole `Span + {⟨⟩}` codomain."
**Problem**: This is a full paragraph justifying *why a phrasing is used* rather than advancing the wp result — essay content in a structural slot. The reader must skip it to reach the actual derivations. The well-typedness point (vacuity over the tagged-union summand `⟨⟩`) is legitimate but needs at most a parenthetical inside each predicate definition, not a standalone preamble.
**Required**: Delete the paragraph; fold the vacuity note into each definition, e.g. `Exact ≡ "⟦σ_d⟧ contains no occupied-depth position outside O(d)" (vacuously true on the ⟨⟩ result)`.

### Issue 2: back-reference sentence in the wp derivation adds no step
**ASN-0112, Preconditions and well-definedness**: "The two directions exhaust the cases by S3★-aux. So the single-subspace condition is both necessary and sufficient, hence the *weakest* precondition; V6 records why the dichotomy is forced rather than incidental."
**Problem**: The trailing clause "V6 records why the dichotomy is forced rather than incidental" is a use-site pointer back to V6 that contributes nothing to the wp derivation — the dichotomy's forcedness is irrelevant to whether single-subspace is the weakest precondition. It is exactly the kind of cross-section deference the anti-bloat pass targets.
**Required**: Drop the clause; end the sentence at "hence the *weakest* precondition."

## OUT_OF_SCOPE

### Topic 1: relating multi-subspace extent to occupied-position count
**Why out of scope**: The first Open Question asks for an invariant tying the cross-subspace extent to `|O(d)|`. This is genuinely new territory (and the dense-run count coincidence is correctly confined to V5's single-subspace case); it belongs to a future note, not this one.

### Topic 2: per-subspace extent reporting
**Why out of scope**: The scope list excludes RETRIEVEDOCVSPANSET / ASN-0113. The ASN correctly does not specify per-subspace spans; V6's bounding-box framing is the honest single-span answer and stays in scope.

VERDICT: REVISE
