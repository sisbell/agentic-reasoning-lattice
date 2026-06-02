# Channel Assignment — ASN-0047 review-317

**Date:** 2026-06-02 02:28

## Issue 1: The k=0-vs-k∈{1,2} freshness distinction is restated in five places
Reason: Purely editorial consolidation — the live-state `e∉E` discharge and the frontier-vs-at-most-once contrast are already fully defined in FrontierEquivalence and the K.δ box; the fix is to state once and cite by name, derivable from the ASN's own content.

## Issue 2: Multiple verification-matrix cells fan into the same downstream prose block
Reason: Purely editorial — each row's actual discharge (S8-fin via restrict+finite-extend, D-SEQ★ as derived, etc.) is already stated in the downstream block; the fix is to inline the correct one-line discharge per cell or rename the block, all internal.
