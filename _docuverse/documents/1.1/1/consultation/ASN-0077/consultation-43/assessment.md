# Channel Assignment — ASN-0077 review-43

**Date:** 2026-06-03 08:34

## Issue 1: S3★ used unconditionally where it only yields conditional membership
Reason: The fix is internal — O2 already demonstrates the correct pattern within this same ASN (citing S3★-aux for subspace exhaustiveness before S3★), so the required correction is just to propagate that established citation pattern to O7, O11, O11', and the postcondition. No design intent or implementation evidence is needed; both S3★ and S3★-aux are already named foundation facts (ASN-0047) used correctly elsewhere in the ASN.
