# Revision Categorization — ASN-0047 review-4

**Date:** 2026-03-17 03:13

## Issue 1: P6 derivation invokes J0 for something J0 does not establish
Category: INTERNAL
Reason: The fix is a proof repair using definitions already present in the ASN and referenced ASNs. S7a (prefix allocation), the allocation mechanism (inc/TA5, ASN-0034), and P1 are all available — the derivation chain just needs to be corrected to route through "allocation requires origin(a) ∈ E_doc" rather than through J0.

## Issue 2: Worked example does not exercise destructive transitions
Category: INTERNAL
Reason: Adding a K.μ⁻ step to the worked example is mechanical — apply the already-defined contraction transition to the existing state Σ₃, verify J2's frame conditions, and show Contains shrinking while R is preserved. All needed definitions (K.μ⁻, J2, P4) are already in the ASN.
