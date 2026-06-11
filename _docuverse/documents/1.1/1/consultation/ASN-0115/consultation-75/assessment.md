# Channel Assignment — ASN-0115 review-75

**Date:** 2026-06-10 23:26

## Issue 1: UnitSpec (a) leaves the V-spec definition's `zeros(d) = 2` conjunct undischarged
Reason: The fix is internal — the review itself identifies the closing fact (M0, ASN-0093, gives `zeros(d) = 2` for every `d ∈ dom(Σ.M)` at reachable states, and the ASN's standing reachability precondition applies), so the revision is a one-line citation discharge requiring no design intent or implementation evidence.
