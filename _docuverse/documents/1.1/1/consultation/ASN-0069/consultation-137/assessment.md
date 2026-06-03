# Channel Assignment — ASN-0069 review-137

**Date:** 2026-06-03 05:01

## Issue 1: V12(d) invokes P4★ at the fork pre-state Σ without establishing Σ is a composite boundary
Reason: The fix is derivable from the ASN's own content. V0 already establishes the fork as a composite, so its invocation point Σ lies on the sequence of composite boundaries (P4a, ASN-0047, a declared dependency). The required one-sentence step — naming Σ as a composite boundary to discharge P4★'s precondition — uses only machinery already present; neither design intent nor implementation evidence is needed.
