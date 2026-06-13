# Channel Assignment — ASN-0132 review-23

**Date:** 2026-06-13 12:39

## Issue 1: CN-UNIT case (d) is presented as an independent fourth multiplicity, then proven to reduce to (c)
Reason: Pure structural reorganization. The load-bearing fact — that the J4 fork composite (ASN-0047) ranges its V-to-I step over `V_{s_C}` and performs no `K.λ` or link-subspace extension, leaving `Σ.L` untouched — is already stated in the note's own case-(d) prose with its ASN-0047 citation. Folding (d) under (c), dropping the "one might fear" framing, and removing the fourth item from the CN-UNIT postcondition all rework content already present; no design intent or implementation evidence is in question.

## Issue 2: Final section ("Cost, and the meaning of asking for a number") restates two boundaries multiple times
Reason: De-duplication of prose already in the note. The delivery boundary, the "cost is out of scope" stance, and the implementation observation (Gregory's back end pays full enumeration cost) are all stated; the fix collapses repetition to one statement each. No new evidence is needed — the Gregory cost fact is already recorded as an implementation note and is being preserved, not re-sourced.

## Issue 3: CN-MONO claims-table cell carries the full wp derivation
Reason: Pure relocation. The wp formula and its FL-WP(a)/(b) and R0a refinements already appear in full in the body; trimming the table cell to the bare claim removes a duplicate, consulting nothing outside the note.
