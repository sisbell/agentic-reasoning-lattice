# Revision Categorization — ASN-0047 review-26

**Date:** 2026-03-17 14:12



## Issue 1: Reachable-state invariants table entry omits P7a
Category: INTERNAL
Reason: The theorem body already lists P7a and its derivation is provided in the ASN. The fix is adding the missing label to the summary table entry — purely a transcription error fixable from existing content.

## Issue 2: "M₀ is the empty function" contradicts established totality
Category: INTERNAL
Reason: The ASN already establishes M as a total function three paragraphs earlier and provides the correct characterization. The fix is rewording to match the already-stated totality convention — no external evidence needed.

## Issue 3: "Purely destructive" mischaracterizes K.μ~
Category: INTERNAL
Reason: The ASN itself distinguishes K.μ⁻ (removal) from K.μ~ (rearrangement preserving ran) and decomposes K.μ~ into K.μ⁻ + K.μ⁺. The correction follows directly from the ASN's own definitions — replacing "purely destructive" with phrasing like "non-constructive" or "admitting destructive change" requires only the distinctions already drawn in the text.
