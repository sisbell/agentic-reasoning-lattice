# Channel Assignment — ASN-0119 review-36

**Date:** 2026-06-10 05:58

## Issue 1: Four conjuncts of the discharged invariant package are not individually traceable
Reason: The fix is internal bookkeeping. The four missing conjuncts (S4, S7a, S7b, S7d) belong to ASN-0047's `ExtendedReachableStateInvariants` — a sibling spec the ASN already imports — and the review itself certifies that S4/S7a/S7b are `dom(C)` properties and S7d a document-tumbler property keyed on `E`, all frame-frozen by the ASN's own RA0 and inert-`E` frame. Closing the enumeration gap (naming the four, or stating the one-clause closure rule the review supplies) draws only on frame conditions already present; it needs neither design intent nor implementation evidence.
