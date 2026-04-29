# Revision Categorization — ASN-0061 review-10

**Date:** 2026-03-22 23:33



## Issue 1: D-PRE(iii) makes an unverified assertion about link-subspace deletion
Category: INTERNAL
Reason: The fix is entirely derivable from the ASN's own content and its cited dependencies. The review already identifies the two options (restrict to text subspace or verify K.μ⁺_L decomposition), and all relevant transition definitions and invariants (K.μ⁺_L, CL-OWN) are in ASN-0047. No design-intent or implementation-evidence questions arise.

## Issue 2: State model and framework scope are not declared
Category: INTERNAL
Reason: This is a structural/notational issue resolvable from ASN-0047's exported definitions. The ASN already references both frameworks; the fix is choosing one and adding the missing verification paragraph or deferral statement. All invariants and frame conditions needed are already defined in ASN-0047.
