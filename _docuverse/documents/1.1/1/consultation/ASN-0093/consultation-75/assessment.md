# Channel Assignment — ASN-0093 review-75

**Date:** 2026-05-31 13:30

## Issue 1: Link invariants restate ASN-0043 using `origin` where the foundation defines `home`
Reason: This is a notation-reconciliation issue between cited foundation ASNs — ASN-0036's content-scoped `origin` vs ASN-0043's link-scoped `home`. The fix (adopt `home` for links, or add a one-line `origin ≡ home` equivalence) is derivable from the definitions already present in the cited foundations and this note; no design intent or implementation evidence is required.
