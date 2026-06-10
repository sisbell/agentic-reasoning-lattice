# Channel Assignment — ASN-0126 review-77

**Date:** 2026-06-10 00:54

## Issue 1: The naming digression in "The registry" is non-load-bearing justification with a downstream forward reference
Reason: Purely editorial. The reviewer has already verified that no derivation (RegisteredAdmissible, (i)-decidability, P1/P2, P6) depends on the absence of a name field, and supplied the exact replacement sentence; cutting the Nelson motivation, ghost-survival argument, and observability aside changes no claim about what the system does, so neither design intent nor implementation evidence is in question.

## Issue 2: "The registry" restates ASN-0086's TypeEquivalence inline
Reason: Purely editorial. The fix is deleting a restatement of ASN-0086's `K ~ K' ≡ coverage(K) = coverage(K')` and `L_K = L_{K'}`; whether it duplicates ASN-0086 is settled by comparing sibling spec notes, not by Nelson's design intent or Gregory's udanax-green code, and the retained clause already cites TypeEquivalence.
