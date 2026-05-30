# Channel Assignment — ASN-0042 review-127

**Date:** 2026-05-30 05:51

## Issue 1: O1's "Ownership *is* the comparison" overclaims relative to the load-bearing ω
Reason: The fix hinges on whether udanax-green realizes any longest-match selection mechanism for `ω`, or only account-level containment via `tumbleraccounteq`. This is an implementation-evidence question, so Gregory is needed; Nelson's exclusivity intent is already settled in the ASN.
Gregory question: Does udanax-green contain any mechanism that selects the longest matching account prefix among multiple covering principals, or does ownership resolution stop at the binary `tumbleraccounteq` containment check with no longest-match arbitration anywhere?

## Issue 2: O7(c) statement and proof disagree on which delegation conditions are re-evaluated vs. discharged
Reason: The mismatch between O7(c)'s statement and its own proof is resolvable from the ASN's existing delegation predicate and proof structure — the correct partition (discharged: i, ii, iv; binding: iii, v) and the "at Σ' upon entry" scoping are both already present internally.

## Issue 3: Accumulated restatement of the refinement-only / no-revocation theme
Reason: This is a purely editorial deduplication of restated conclusions across O3/O8/O10, fully derivable from the ASN's own text with no design or implementation question at stake.
