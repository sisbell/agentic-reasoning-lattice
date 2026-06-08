# Channel Assignment — ASN-0102 review-40

**Date:** 2026-06-07 23:10

## Issue 1: X8 within-reference non-coalescence skips the load-bearing contiguity step
Reason: The missing step is the source content subspace's contiguity (D-SEQ, ASN-0036) — already a named foundation the ASN cites — which forces consecutive resolved runs to be source-V-adjacent so maximal-merge rules out their I-adjacency. Pure derivation from content already present; no design intent or implementation evidence needed.

## Issue 2: composite-boundary fact established twice (anti-bloat)
Reason: This is a prose-deduplication fix — state the composite-boundary consequence once in the Definition and have X14 invoke it by name. Entirely internal editorial work, derivable from the ASN's own structure.
