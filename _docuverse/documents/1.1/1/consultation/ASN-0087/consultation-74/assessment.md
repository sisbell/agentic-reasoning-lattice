# Channel Assignment — ASN-0087 review-74

**Date:** 2026-06-04 03:49

## Issue 1: Per-subspace invariants D-CTG★, D-MIN★, D-SEQ★ discharged only for the link subspace at `d`
Reason: Internal. The required fix only adds explicit notes that the content-subspace conjunct at `d` and all conjuncts at `d' ≠ d` are preserved by the frame (`V_{s_C}(d)` unchanged, `M'(d') = M(d')`) — both frame facts are already established in the ASN's own *Effect* and *Invariant Preservation* sections.

## Issue 2: Redundant restatement of foundation definitions and a repeated mechanism/actual distinction
Reason: Internal. Citing the ASN-0098 `project`/`discoverable_from` definitions instead of re-typesetting them, and consolidating the mechanism-vs-actual distinction to the M-NoIndexState location, are editorial deduplication moves requiring no design intent or implementation evidence.
