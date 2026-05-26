# Channel Assignment — ASN-0098 review-7

**Date:** 2026-05-25 20:23

## Issue 1: The "tight" predicate is unachievable for any non-empty endset, making LP19a and LP19 vacuous
Reason: The mathematical defect is established by the review, but choosing between the two suggested reformulations (allocator-frontier discipline vs. T4-valid restriction) depends on what architectural property was actually intended and whether the implementation enforces a specific construction discipline.
Nelson question: What is the intended construction discipline for endsets that "refer to specific allocated content" — was the design intent that endset spans align with the allocator frontier so future K.α/K.λ emissions necessarily fall outside the span's reach, or something else that excludes future allocations from coverage?
Gregory question: How does udanax-green construct endset spans when a link is created against existing content, and what placement of span endpoints (start, width) does the implementation enforce relative to the allocator's emission sequence?

## Issue 2: Open Question 5 acknowledges the gap that LP19a/LP19 claim to close
Reason: This is a bookkeeping consistency issue resolved entirely by the outcome of Issue 1's repair — once `tight` is reformulated, the open question is either subsumed by the revised LP19 or rescoped to the non-tight case.
