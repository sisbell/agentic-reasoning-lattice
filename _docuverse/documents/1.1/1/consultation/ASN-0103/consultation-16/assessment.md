# Channel Assignment — ASN-0103 review-16

**Date:** 2026-06-05 01:55

## Issue 1: The version-dominance argument omits documents allocated under a properly-extending sub-account
Reason: The fix is internal. The reviewer's option (a) — narrow CND.monotone to `A_doc(A)` emissions and their version chains, and note that freshness against sub-account documents is already discharged by length/T1-divergence at position `#A+1` — is fully derivable from the ASN's own cited machinery (T1 lexicographic order, B8 uniqueness, the parse/length facts already proved). Option (b) would invoke the account-allocator uniform-length property, but the ASN already declares it out of scope and correctness needs only freshness, not total dominance, so the scoping decision requires neither design intent nor implementation evidence.
