# Channel Assignment — ASN-0112 review-24

**Date:** 2026-06-08 09:44

## Issue 1: V8's m_C re-pinning digression defends against a case its own hypothesis excludes, and overlaps V18
Reason: Purely editorial reorganization — trim V8's defensive meta-prose and let the migration/depth-fixity accounting live once in V18. Both claims are already present in the ASN; no design intent or implementation evidence is needed to relocate the reasoning.

## Issue 2: V9 forward-references V16
Reason: Internal restructuring — V9's justification ("σ_d is a function of O(d) alone") is immediate from the definitions of origin_d and extent_d already stated in the note, so the forward-reference can be replaced with a self-contained derivation. No channel needed.

## Issue 3: the companion reach-wp is ill-typed on the empty result, unlike the Exact-wp
Reason: A typing-discipline fix derivable from the note's own V0/V11 codomain (`Span + {⟨⟩}`) and the existing vacuous-on-`⟨⟩` treatment already applied to `Exact`; the same handling extends to the reach predicate internally.
