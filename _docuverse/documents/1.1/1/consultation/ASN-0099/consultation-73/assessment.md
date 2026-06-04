# Channel Assignment — ASN-0099 review-73

**Date:** 2026-06-04 14:20

## Issue 1: "Predicate domain" paragraph imagines a case the definitions already exclude
Reason: Internal fix. The deletion is justified by F14's own definition `{a ∈ dom(Σ.L) ∩ S : matches(a, I, Σ)}`, which structurally restricts the quantifier to `dom(Σ.L)`; no design intent or implementation evidence bears on removing bookkeeping the definitions already enforce.

## Issue 2: The F2-X ∧ F3-X paragraph restates the displayed conformance equations
Reason: Internal fix. The displayed equation block and the base-case argument one paragraph earlier already carry the claim; collapsing the restatement is a pure editorial judgment derivable from the ASN's own content.

## Issue 3: Implementation/index commentary in the Completeness obligation
Reason: Internal fix. The ASN itself lists "Caching" and "The procedure by which the operation is computed" under *What We Have Not Specified*, so the index/lockstep prose contradicts the ASN's own scope; the load-bearing sentence is pinned by F2 ∧ F3 already present.
