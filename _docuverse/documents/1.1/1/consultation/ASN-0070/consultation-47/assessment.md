# Channel Assignment — ASN-0070 review-47

**Date:** 2026-06-03 00:32

## Issue 1: No worked example exercises partial-block intersection (offset j > 0)
Reason: The fix only requires constructing a new worked configuration using machinery already fully defined in the ASN (F-contig, the `(j, c)` offset/width recording, V-run construction) and verifying F-sound/F-complete/F-contig against it. No design intent or implementation evidence is needed.
