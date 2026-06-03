# Channel Assignment — ASN-0069 review-109

**Date:** 2026-06-03 03:06

## Issue 1: V9a asserts non-reconstructability of the acquisition path without proof
Reason: The fix is internal — both remedies are derivable from the ASN's own model. "Not stored" follows from `R ⊆ T × E_doc` (already stated); the two-history construction or the weakened containment-only claim both work entirely within the existing state model and V9/V9b, requiring no design intent or implementation evidence.

## Issue 2: V6a builds a self-contained link-query apparatus heavier than the fork guarantee requires
Reason: The fix is internal — anti-bloat reduction to the minimal statement (`L' = L` from the constituent frame conditions plus the shared-I-address consequence of V4) uses only material already present in the ASN. No design intent or implementation behavior is at issue; this is purely a scope-trimming edit.
