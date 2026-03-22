# Revision Categorization — ASN-0063 review-19

**Date:** 2026-03-22 01:01



## Issue 1: J4 (Fork) compatibility with D-CTG/D-MIN amendment is not verified
Category: INTERNAL
Reason: The fix is fully derivable from existing definitions — J4's K.μ⁺ operates on a fresh document (M(d_new) = ∅ after K.δ), so constructing V-positions contiguously from the minimum satisfies D-CTG/D-MIN by definition. No external evidence needed.

## Issue 2: K.μ~ decomposition validity under D-CTG/D-MIN amendment is not established
Category: INTERNAL
Reason: The fix requires an explicit existence argument for the K.μ⁻/K.μ⁺ decomposition, but all ingredients are present in the ASN — link-subspace fixity (r = 0), D-SEQ at the input, and the observation that removing all content-subspace positions then re-adding is always valid. No design intent or implementation evidence is needed.
