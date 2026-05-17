# Channel Assignment — ASN-0047 review-72

**Date:** 2026-05-17 04:24

## Issue 1: Cross-document disjointness chain Case B sub-case enumeration is incomplete
Reason: The fix is internal — the dispatch via T10a.{2,5,6} is already in scope from ASN-0034, and the cross-account version-vs-version configuration follows from T10a.5 applied to non-lineage version sub-allocators. The repair is editorial (expanding sub-case enumeration or weakening the closure assertion to match what T10a's machinery actually delivers).

## Issue 2: ExtendedReachableStateInvariants S5 omission unexplained
Reason: The fix is internal — S5 (UnrestrictedSharing) from ASN-0036 can be checked against the extended state's invariant set directly. Either it is preserved as a derived consequence of S2 + S3★ + the absence of an injectivity constraint on M(d), or the omission needs explicit justification; both determinations are derivable from the ASN's own content plus ASN-0036's S5 statement.
