# Revision Categorization — ASN-0047 review-36

**Date:** 2026-03-22 13:39

## Issue 1: K.μ~ decomposition undefined when content subspace is empty
Category: INTERNAL
Reason: The fix is purely formal — adding a case split for `dom_C(M(d)) = ∅` where π is forced to identity by link-subspace fixity, producing zero elementary steps. All definitions and reasoning needed are already present in the ASN (link-subspace fixity, K.μ⁺ amendment, ValidComposite★).
