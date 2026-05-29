# Channel Assignment — ASN-0040 review-54

**Date:** 2026-05-28 22:02

## Issue 1: B4 asserts a serialization grain that the Open Questions still treats as unresolved
Reason: Internal. B4 already derives per-namespace grain from B7 (proven within the ASN), and the B6 table plus B7 already answer the dual-depth question; reconciling the two sections requires only recognizing what the ASN itself establishes.

## Issue 2: The hwm Justification duplicates B2 and forward-defers its own derivation
Reason: Internal. This is a structural deduplication between two passages already present in the ASN (hwm Justification and B2); no design intent or implementation evidence is needed to choose where the max = cₘ derivation lives.

## Issue 3: Meta-prose justifying the modeling choice in B0a
Reason: Internal. Deleting a sentence that justifies the formulation choice requires nothing beyond the ASN's own B0a statement.

## Issue 4: B4's atomicity prose carries non-advancing reasoning that overlaps B8
Reason: Internal. The ordering reasoning is already made in B8 Case 1 under the co-reachability hypothesis; trimming or relocating it is a structural edit derivable from the ASN's own content.
