# Channel Assignment — ASN-0070 review-50

**Date:** 2026-06-03 00:49

## Issue 1: F-subspace's main postcondition relies on S3★-aux but does not cite it
Reason: The fix is fully internal — S3★-aux (SubspaceExhaustiveness, ASN-0047) is already invoked in the same lemma's Consequence derivation, so adding it to Depends and making the case split explicit is derivable from the ASN's own content with no need for design intent or implementation evidence.
