# Channel Assignment — ASN-0082 review-60

**Date:** 2026-05-30 11:02

## Issue 1: Justification embedded in a postcondition slot (D-SEP)
Reason: Pure structural edit — move the bracketing/contiguity argument out of the postcondition slot into the proof below it. Both the claim and its proof already exist in the ASN; this is text relocation, derivable internally.

## Issue 2: wp prose imagines preconditions the carrier already supplies
Reason: Editorial trimming of speculative prose; the discharge facts (S8a on v from `v ∈ dom(M(d))`, depth-1 restriction) are already stated in the ASN and the depth-generalization Open Question already exists. No external input needed.

## Issue 3: Duplicated cross-subspace closing prose
Reason: Deduplication of two paragraphs saying the same thing; the verification tables already carry the content. Purely internal.

## Issue 4: Scope paragraphs explain rationale rather than state the operation
Reason: Reducing Scope notes to object-level content (what each sub-operation transforms vs. leaves fixed), which is already recorded at I3-C and D-I. Removing the insertion-vs-contraction contrast is an internal editorial cut.

## Issue 5: D-SHIFT prose restates the postcondition
Reason: The postcondition `M'(d)(σ(v)) = M(d)(v)` and the Nelson quote both already exist in the ASN; the fix only drops the redundant prose restatement. Internal.
