# Channel Assignment — ASN-0099 review-30

**Date:** 2026-05-27 04:29

## Issue 1: F10's ordering property is not extended to filtered or scoped variants
Reason: The fix is internal. F10's structural argument (finite subset of dom(Σ.L) under T1's restriction is uniquely orderable) lifts directly to filtered/scoped via F2-filt/F3-filt and F2-sco/F3-sco bounding the result sets within dom(Σ.L), plus L-fin and T1's order properties — no design intent or implementation evidence needed.

## Issue 2: State name Σ'' is reused with different referents across queries in the worked example
Reason: The fix is internal. This is a naming/editorial conflict within the worked example itself — both Σ'' definitions are local to the ASN and the resolution is straightforward symbol renaming with no semantic question requiring Nelson or Gregory.
