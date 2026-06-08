# Channel Assignment — ASN-0113 review-30

**Date:** 2026-06-08 09:34

## Issue 1: W12 / "What the pair reveals" is a state-space fact, not an operation guarantee
Reason: Purely structural — removing or demoting a claim that constrains no operation behavior, with the operation-relevant content already in W0. No design intent or implementation evidence is at stake; the fix is internal to the note.

## Issue 2: Forward-reference accretion to W0
Reason: Editorial reorganization of where the empty-vs-unallocated distinction is stated relative to W-pre/W0. Both claims already exist in the note; only their ordering and cross-reference need adjustment.

## Issue 3: W18 / "Permanence of the report" restates W8
Reason: Deduplication — folding the `M(d)`-locality increment into W8 and deleting restated purity prose. Both W8 and the increment are already present and derivable from the note's own content.
