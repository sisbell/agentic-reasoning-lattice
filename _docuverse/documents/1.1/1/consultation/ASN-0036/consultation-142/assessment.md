# Channel Assignment — ASN-0036 review-142

**Date:** 2026-05-29 00:59

## Issue 1: The δ/TumblerAdd action-point fact is restated five times
Reason: Pure deduplication — the action-point consequence is a foundation fact from ASN-0034 (TumblerAdd/OrdinalShift), already cited in the ASN. Stating it once as a lemma and removing the four inline re-derivations is an internal restructuring requiring no external evidence or intent.

## Issue 2: Decorative weakest-precondition blocks restate their own axioms
Reason: The fix is to drop the wp framing in favor of the plain consequence sentence (or defer it to the operations ASN). Operations are out of scope here by the ASN's own framing, so the decision is internal and derivable from the ASN's stated scope.

## Issue 3: Implementation-mechanics prose in S1 does not bear on the abstract guarantee
Reason: The load-bearing claim (absence of a removal op in Σ) is already stated; cutting or compressing the `/*subtreefree(ptr);*/` detail is an editorial decision about redundancy. The evidence is already present in the ASN, so no new Gregory query is needed to make the cut.

## Issue 4: S0 "Read directionally" remark restates the frame
Reason: The frame clause in the Formal Contract already carries the directional reading; deleting the redundant sentence is internal and derivable from the ASN's own text.
