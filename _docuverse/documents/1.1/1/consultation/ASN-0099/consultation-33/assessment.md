# Channel Assignment — ASN-0099 review-33

**Date:** 2026-05-27 05:29

## Issue 1: Notation typo in Query 11 cross-step precondition list
Reason: Pure notational typo — "dom(M.L)" should be "dom(Σ.L)" or "dom(L)", matching ASN-0047's K.μ⁺_L precondition vocabulary already established and used correctly elsewhere in the same paragraph. Fix is internal.

## Issue 2: F10-filt/F10-sco derivations route through implementation conformance rather than direct comprehension structure
Reason: The fix substitutes a direct citation of the comprehension structure (`findlinks_filtered(C, Σ) ⊆ dom(Σ.L)` by the source set; `findlinks_scoped(I, S, Σ) ⊆ dom(Σ.L) ∩ S` by F14) for the unnecessary routing through `result_filtered`/`result_scoped`. All the components are already defined in the ASN. Fix is internal.

## Issue 3: F10's pairwise-to-n-document lift relies on T1 restriction being a strict total order without citing the source
Reason: The reviewer already supplies the discharge ("T1's postconditions (a) irreflexivity, (b) trichotomy, (c) transitivity quantify universally over T, so each specializes by instantiation to any S ⊆ T"), and T1's postconditions are published in ASN-0034 (already a load-bearing substrate citation in this ASN). Fix is internal.
