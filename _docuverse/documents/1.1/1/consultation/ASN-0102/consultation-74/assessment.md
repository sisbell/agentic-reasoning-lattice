# Channel Assignment — ASN-0102 review-74

**Date:** 2026-06-08 03:01

## Issue 1: P4a discharged at the wrong state — "Σ' is a trace state" is unsound in the general case
Reason: The fix is internal — the review itself specifies the corrected derivation (discharge P4a at `Σ_clo` mirroring the P4★ argument, using composite-wide J1'★ to force range-residence at the closing boundary). All needed machinery (P4a's witnessing semantics, J1'★, P4★ pattern, ASN-0047) is already present in the ASN; no design intent or implementation evidence is required.

## Issue 2: Trailing restatement at the end of X14 (anti-bloat)
Reason: Pure deletion/fold of redundant prose that restates X14's own effect and X6's attribution point; derivable from the ASN alone with no external input.

## Issue 3: Repeated citation gloss for ASN-0058 C1 (anti-bloat)
Reason: Editorial consolidation of a thrice-repeated parenthetical whose fact is already established at PC1/the wp step; entirely internal to the ASN's existing content.
