# Channel Assignment — ASN-0128 review-25

**Date:** 2026-06-11 06:24

## Issue 1: The born-nullified example grounds the exclusion in the covering retraction's *activity*, which the mechanism does not use
Reason: The correct semantics are already pinned in the ASN's own content — I3 and I2 state C3 over the audit slice, DR quantifies over `L_R^Θ`, and R6b's `L_R`-not-`A_R` reading is cited from ASN-0086. The fix is aligning the example's wording with commitments the note already makes; no design intent or implementation evidence is needed.

## Issue 2: SD's step classification is stated three times in different words
Reason: Pure redundancy consolidation — the classification's single authoritative statement (SD) and the genuinely new content to preserve (the two defeat modes) are both identified in the review; no external fact bears on which words to cut.

## Issue 3: The lens re-gloss duplicates the view definitions stated immediately above it
Reason: Internal prose deduplication — the three view definitions and the escape-hatch asymmetry (R6c) are both already present in the section; the fix only removes the restatement and preserves the asymmetry commitment.
