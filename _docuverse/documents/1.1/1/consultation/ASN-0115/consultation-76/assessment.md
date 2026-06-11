# Channel Assignment — ASN-0115 review-76

**Date:** 2026-06-10 23:36

## Issue 1: Cross-substrate invariant discharge — M0 (and SD) cited over the wrong state space
Reason: The fix is internal — the review already identifies the correct in-model route (`dom(M) = E_doc` from ASN-0047 M1 plus Document from ASN-0045 for the tumbler shape, and L14 for store disjointness), and the facts being discharged are unchanged. This is a citation re-routing within the ASN's existing dependency cone, requiring neither design intent nor implementation evidence.

## Issue 2: Nominal-extent attainment biconditional is asserted before, and not fully covered by, its supporting analysis
Reason: The fix is internal — assembling the three-branch argument (depth-incompatible via ActionPoint's `w_{actionPoint(w)} ≥ 1` postcondition from ASN-0034, the `V_S(d) = ∅` branch, and the S8-depth slice-containment step) or relocating the corollary after the R6 frontier analysis uses only definitions and lemmas already present in the ASN and its cited dependencies.

## Issue 3: Anti-bloat — defensive justifications in claim slots and intra-section duplication
Reason: The fix is internal — it is purely editorial (deleting duplicated phrasings, stripping WLOG/use-site defenses, moving the M1 discharge from the R7 claim box into the body proof), with no change to any technical claim that would require design-intent or implementation evidence.
