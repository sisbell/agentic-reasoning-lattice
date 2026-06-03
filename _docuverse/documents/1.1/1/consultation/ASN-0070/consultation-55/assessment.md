# Channel Assignment — ASN-0070 review-55

**Date:** 2026-06-03 01:26

## Issue 1: F-subspace proves its postcondition inside the Depends slot
Reason: Purely structural reorganization — move the existing proof text from the Depends slot into a Derivation slot, leaving Depends as a citation list. No design intent or implementation evidence needed; the proof content already exists in the note.

## Issue 2: "d need not be the home document" stated in three places
Reason: Editorial deduplication — delete the four "There is no requirement that..." sentences from F1, which are already formalized in F-multidoc/F-empty/F-persist and the WP analysis. Removal is derivable from the note's own structure.

## Issue 3: The "coverage, not decomposition" point is stated twice
Reason: Editorial deduplication — choose one location (F0, where it is a property of the definition) and remove the anticipatory restatement in The Setting. No external input required.

## Issue 4: Defensive exhaustiveness restatement in F-canonical Step 1
Reason: Delete the redundant clause; the cited bound `actionPoint(ℓ) ≤ #ℓ = m_S(d)` already entails it. Internal to the cited ASN-0034 postcondition.
