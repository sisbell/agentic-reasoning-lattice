# Channel Assignment — ASN-0121 review-3

**Date:** 2026-06-09 01:17

## Issue 1: The transition relation for `→` / `→*` is never defined, and the permanence claims cite R6a beyond its established domain
Reason: Internal. The required fix is naming the transition relation (cite ASN-0047's atomic vocabulary) and stitching together already-established lemmas — R6a (ASN-0086), StoreMonotonicity★ (ASN-0098), and the immutability of `Σ.L` under K.μ edits. All needed facts are in cited foundation ASNs and the ASN's own reasoning; no design intent or implementation evidence is required.

## Issue 2: Matching of higher-arity links (arity > 3) is left implicit
Reason: The determinate semantics (slots 4+ unconstrained) is derivable from `sat`, but confirming this is the *intended* treatment of Nelson's n-set case (4/79) is a design-intent question for Nelson.
Nelson question: For a link with more than three endsets (the n-set case at 4/79), is FINDLINKSFROMTOTHREE meant to constrain only the from/to/type slots and leave any further endsets unmatched, or was a different treatment of the extra endsets intended?
