# Channel Assignment — ASN-0108 review-39

**Date:** 2026-06-13 05:41

## Issue 1: The per-key computability mechanism is re-derived in W8, W9, W9b, and the claims table
Reason: Internal — this is a pure de-duplication fix. The per-key computability mechanism (held-value / endset-persistence / V-position-erasure) already exists in full at W8; the fix is to leave it there and replace the re-derivations in W9, W9b, and the table with bare citations to W8, keeping only each claim's own application. No design intent or implementation evidence is needed to relocate content already present in the note.

## Issue 2: Intra-W9 duplication and a defensive parenthetical
Reason: Internal — removing an intra-W9 repeated "either permanent key" statement and cutting/compressing the terminal-state parenthetical. The cut-point walk already in the note (`L_2` ending behind the final cursor) supplies the concrete witness the parenthetical restates abstractly, so the fix is derivable entirely from the ASN's own content.
