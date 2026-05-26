# Review of ASN-0098

## REVISE

### Issue 1: Forward reference — LP12a's boundary case uses LP-Fin Corollary established later
**ASN-0098, "Discoverability and Survival" section, LP12a "Boundary case — content-subspace empty, link-subspace retained"**: "We discharge this via the LP-Fin Corollary."

**Problem**: LP-Fin and its corollary are established in the "Boundary and Width Behaviour" section, which appears after LP12a in document order. A reader proceeding top-down cannot verify the boundary case argument without jumping forward to the later section. The corollary is the load-bearing premise for deriving `coverage(Σ.L(a).eᵢ) ∩ dom(Σ.L) = ∅` from canonical content-subspace construction — without that derivation, the conclusion that the wp evaluates to false on this class of links is unsupported at the point it appears.

**Required**: Either (a) move LP-Fin and LP-Fin Corollary to a position before LP12a in the document (perhaps in their own preliminary section), or (b) defer the boundary case discussion of LP12a to a position after LP-Fin Corollary is established. Option (a) is cleaner since LP-Fin Corollary is genuinely a structural result about F ∩ [s, s ⊕ ℓ) independent of the tightness predicate.

### Issue 2: Ambiguous directional reference in LP-Fin Corollary
**ASN-0098, "Boundary and Width Behaviour" section, LP-Fin Corollary**: "This corollary is invoked in LP12a's boundary case below to lift 'the span starts in the content subspace' to 'the entire coverage avoids `dom(L)`'."

**Problem**: "Below" naturally reads as forward in document order, but LP12a appears earlier than the corollary. The intended reading is probably "below [LP12a's main statement]", but the surrounding context makes this confusing — the corollary itself is "below LP12a" in document order, so "invoked below" suggests something even further forward.

**Required**: Replace with an unambiguous reference such as "invoked in LP12a's boundary case (Discoverability and Survival section, above)" or simply "invoked above in LP12a's boundary case".

## OUT_OF_SCOPE

None of the Open Questions identified at the end of the ASN are in-scope errors; they are correctly identified as questions for future ASNs. The scope exclusions (link type semantics, BEBE) are respected throughout.

VERDICT: REVISE
