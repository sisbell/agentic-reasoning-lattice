# Channel Assignment — ASN-0102 review-114

**Date:** 2026-06-08 06:17

## Issue 1: COPY's transition status is stated two contradictory ways and never cleanly resolved
Reason: Internal fix. The Amendment and Definition already fix COPY as a single elementary transition unconditionally, and X16's discharge depends only on that; the "also expressible as a composite" asides are non-load-bearing rationale that can be cut or quarantined using the note's own content. No design-intent or implementation evidence is needed to decide what COPY *is* — the ASN already states it.

## Issue 2: The singleton-composite framing is set up twice
Reason: Internal fix. This is pure structural deduplication — hoisting the "COPY-as-singleton-sequence is a valid composite, read `Σ` as `Σ_0`" setup into one sentence that both the boundary-property and P4a paragraphs reference. Entirely derivable from the ASN's existing text.
