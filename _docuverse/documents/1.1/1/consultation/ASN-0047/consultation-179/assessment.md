# Channel Assignment — ASN-0047 review-179

**Date:** 2026-05-31 22:37

## Issue 1: Circular citation of K.μ~-FIX in the sufficiency proof
Reason: The fix is internal — for the transposition witness `π_swap`, domain fixity follows by construction (a permutation fixing all but two elements has `dom(M'(d)) = π_swap(dom(M(d))) = dom(M(d))`), independent of any post-state invariant. Citing this construction instead of K.μ~-FIX is derivable from the ASN's own definition of `π_swap`.

## Issue 2: k=1 child-spawn zero-count condition denied rather than discharged
Reason: The fix is internal — the operand `t ∈ E_doc` has `zeros(t) = 2` (from the ASN's own E_doc definition), and T10a's `k' = 1` precondition (already cited from ASN-0034 and stated by the reviewer as `zeros(t) ≤ 3`) is satisfied a fortiori, discharged identically to the k=2 bullet's existing treatment.

## Issue 3: Why-needed justifications that imagine the excluded case
Reason: The fix is internal — both passages should simply state the precondition and the invariant it discharges, dropping the counterfactual "without it / were it otherwise" elaboration; no design intent or implementation evidence is required to remove text and keep the standing discharge.
