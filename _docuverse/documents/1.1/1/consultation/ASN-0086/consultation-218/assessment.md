# Channel Assignment — ASN-0086 review-218

**Date:** 2026-06-01 17:37

## Issue 1: "Arrangement modification is out of scope" paragraph supports no downstream claim
Reason: Internal — the review already establishes that nothing downstream consumes M-immutability and that the fact is foundation-carried (ASN-0093 M2); deciding to delete or fold the paragraph is a self-contained editorial judgment over the note's own dependency structure.

## Issue 2: `home`/`origin` coincidence re-derived at three sites
Reason: Internal — the identity is a fixed consequence of two foundation definitions (ASN-0036 NUDE-prefix projection, ASN-0043 Home); naming it once and citing the label is a pure consolidation within the note's existing reasoning.

## Issue 3: Emit_K cites "R0's On-chain admissibility," but R0's formal statement does not expose it
Reason: Internal — the proof body already establishes on-chain admissibility and freshness for the caller-chosen `d`; restating R0 universally in `d` and promoting these to explicit postconditions is a reformulation of content already present, requiring no design intent or implementation evidence.
