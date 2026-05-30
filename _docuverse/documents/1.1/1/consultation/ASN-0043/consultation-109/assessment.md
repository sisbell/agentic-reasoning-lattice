# Channel Assignment — ASN-0043 review-109

**Date:** 2026-05-30 15:09

```
## Issue 1: CPP conflates its hypothesis with a conditional justification, hiding a caller obligation
Reason: Neither channel is needed. The fix is a proof-hygiene matter internal to the ASN — restating the sibling-advance length condition as an explicit precondition or deriving it from `p ≤ #t₀` plus the first-step ordering — all the relevant facts (TA5(b)/(c), TA5-SigValid, the L1c `k₁=2` and FSE `p = #home(a)` call sites) already appear in the ASN.

## Issue 2: L9 carries a navigational deferral sentence that advances no reasoning
Reason: Neither channel is needed. This is a pure deletion of meta-prose; the "Application to L9" paragraph already discharges FSP's payload hypothesis, so the fix is fully internal to the ASN.
```
