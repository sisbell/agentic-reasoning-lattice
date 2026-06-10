# Channel Assignment — ASN-0127 review-7

**Date:** 2026-06-10 01:15

## Issue 1: D-NONMONO's K.μ~ subcase asserts "rise or fall" without the derivation its siblings receive
Reason: Internal — the fix is a mathematical construction fully derivable from the note's own machinery (F-IMG-SWING for the moved image, F-MATCH's per-slot existential, F-UDIST, and the worked-illustration apparatus). The review even hands over the exact reorder witness (`v_1↦a_1, v_2↦a_2`, region-local from-slots, swap on `R={v_1}`); lifting it through Phase 2 and noting the "sole in-region witness" condition needs no design intent or implementation evidence.

## Issue 2: Degenerate cases of `image` and `findlinks` are not stated
Reason: Internal — every required boundary value is a direct definitional consequence already in scope: `image(∅)=∅` and `image=∅` on `R∩dom(Σ.M(d))=∅` fall out of F-IMG's comprehension, `findlinks(∅)=∅` from F-MATCH's slot existential against `∅`, and the composite zero from F-V; the freshly-registered `dom(Σ.M(d))=∅` post-state is the K.δ Document case already grounded in cited ASN-0047.
