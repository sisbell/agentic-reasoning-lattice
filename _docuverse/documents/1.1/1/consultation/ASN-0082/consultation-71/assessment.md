# Channel Assignment — ASN-0082 review-71

**Date:** 2026-05-30 13:27

## Issue 1: σ(v) well-formedness is established three separate times
Reason: Pure deduplication — all three derivations already exist within the ASN; consolidating to the S8a-post lemma and replacing the others with citations needs no design intent or implementation evidence.

## Issue 2: D-SEP(a) re-proves OrdinalExceedsDisplacement(i) nearly verbatim
Reason: Both proofs are already present in the ASN; redirecting D-SEP(a) to cite OrdinalExceedsDisplacement(i) is internal editorial work derivable from the ASN's own content.

## Issue 3: NAT-comm introduced as a local axiom
Reason: The fix relocates an arithmetic fact into ASN-0034's NAT-* family and cites it — a sourcing/structural decision derivable from the existing spec conventions (the registry already routes ℕ associativity through TA-assoc), requiring neither Nelson's intent nor Gregory's code.

## Issue 4: meta-prose in structural slots
Reason: Collapsing the duplicate Scope paragraphs and dropping the clause-count framing is local prose trimming; the load-bearing content (I3-CS excludes the gap) is already stated, so the fix is internal.
