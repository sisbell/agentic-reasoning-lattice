# Channel Assignment — ASN-0093 review-5

**Date:** 2026-05-18 15:07

## Issue 1: Prefix-extension property of A_C(d) and A_L(d) is load-bearing but never derived
Reason: Internal derivation — base case follows from SubAllocatorAxiom.FirstEmission's concrete form, inductive step from TA5(c) + TA5-SigValid (both ASN-0034 foundation). No design intent or implementation evidence required.

## Issue 2: T4-validity of dom(C) ∪ dom(L) is needed for T7 but never stated as a derived invariant
Reason: Internal derivation — chain admissibility in C1c/L1c plus M0's T4-valid origin and TA5a's T4-preservation conditional give the result by induction. All inputs already present in the ASN.

## Issue 3: Remark "derivable clauses" omits two premises in the FirstEmission-freshness derivation
Reason: Internal — the fix is to either retract the "derivable" framing or write out the complete premise set explicitly using items already present in the ASN. No external input needed.

## Issue 4: ChainMembershipForOrigin proof and the discharge matrix are mutually dependent; simultaneous induction is not flagged
Reason: Internal — purely a proof-structure clarification stating that the matrix and lemma form one joint induction. Verification that no step uses a same-step conclusion is internal bookkeeping.

## Issue 5: K.α / K.λ subsequent-emit cross-document freshness has no derivation depth
Reason: Internal — after Issue 1 is fixed, the three-step expansion (chain-element extends anchor, cross-document a' extends its own anchor, Cross-doc disjointness + T10) is a mechanical assembly of existing lemmas.

## Issue 6: Worked example does not exercise K.λ subsequent-emit
Reason: Internal — adding a second K.λ emission under d uses already-defined operations and freshness machinery; the example just needs to instantiate the existing subsequent-emit branch with concrete tumblers.

## Issue 7: Worked example does not exercise Case B (prefix-incomparable documents) of Cross-document disjointness
Reason: Internal — Case B's witness-extraction strategy is fully specified in the lemma proof; the worked example just needs to pick a prefix-incomparable pair and walk through B.i or B.ii.

## Issue 8: Contiguity of dom(C)_d as a prefix of A_C(d) is implicit
Reason: Internal — the contiguous-prefix property is a direct consequence of the K.α/K.λ emission rule (FirstEmission for index 1, inc(max{...}, 0) for subsequent steps). The strengthening uses only already-stated emission discipline.
