# Channel Assignment — ASN-0119 review-7

**Date:** 2026-06-09 00:52

## Issue 1: The "precisely when" characterization of footprint fragmentation is a false biconditional
Reason: The fix is pure permutation arithmetic — the note's own pivot machinery (P7a/P7c, R-P1/R-P2) supplies the counterexample and the corrected "image under π is again an interval" characterization. No design intent or implementation evidence is needed.

## Issue 2: Partiality and degenerate document sizes are never stated
Reason: The note already imports R-PRE and cites ASN-0084's statement that REARRANGE_K is "partial, defined exactly where R-PRE(K) holds"; the degenerate-size consequences follow directly from the strict-ascent + width-≥-1 conditions already present. Fully derivable from the ASN's own content.
