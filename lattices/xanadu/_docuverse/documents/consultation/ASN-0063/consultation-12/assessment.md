# Revision Categorization — ASN-0063 review-12

**Date:** 2026-03-21 22:05



## Issue 1: P4★ K.μ~ preservation — compressed derivation
Category: INTERNAL
Reason: The fix requires making two elided inference steps explicit — both steps use only the bijection property of π and the link-subspace fixity already established in the ASN. No external design intent or implementation evidence is needed.

## Issue 2: J4 fork consequence — missing verification that fork remains a valid composite
Category: INTERNAL
Reason: The verification requires checking J1★ and J1'★ against J4's existing composite steps (K.μ⁺, K.ρ) under the amended preconditions — all definitions are present in ASN-0063 and ASN-0047. No Nelson design intent or Gregory implementation evidence is needed.
