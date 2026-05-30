# Channel Assignment — ASN-0043 review-108

**Date:** 2026-05-30 14:59

## Issue 1: The worked example verifies L5 and L8 only in their degenerate singleton form, never exercising the multi-span semantics that is their actual content
Reason: The fix is internal — it requires only constructing multi-span endset instances and verifying L5 (extensional set equality) and L8 (coverage-based matching) using definitions already present in the ASN; the Coverage definition even supplies the canonical different-decomposition/identical-coverage example. No design intent or implementation evidence is needed.
