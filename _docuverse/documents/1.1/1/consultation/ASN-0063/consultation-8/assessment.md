# Revision Categorization — ASN-0063 review-8

**Date:** 2026-03-21 20:25



## Issue 1: CL1 and CL2 are stated for arbitrary V-span-sets but proven only for text-subspace V-spans
Category: INTERNAL
Reason: The fix is derivable from the ASN's own content — the review already identifies the two options (add subspace precondition or scope VSpanImage), and the direct I-span-set form already handles the link-address case. No design intent or implementation evidence is needed.

## Issue 2: K.μ~ preservation of S3★ relies on a circular argument
Category: INTERNAL
Reason: The review itself provides the correct non-circular proof structure (decompose into K.μ⁻ then K.μ⁺, prove S3★ at each step independently). All definitions and properties needed are already present in the ASN. This is a proof restructuring issue, not a question about design intent or implementation behavior.
