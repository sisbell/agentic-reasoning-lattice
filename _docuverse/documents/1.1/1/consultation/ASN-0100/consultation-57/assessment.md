# Channel Assignment — ASN-0100 review-57

**Date:** 2026-06-05 01:50

## Issue 1: Shifted-right provenance grounded in the wrong invariant
Reason: The fix is internal — the correct grounding (pre-state P4★ establishes `(a, d) ∈ R`, then P2 preserves to R') is already present two paragraphs later in the same section; this is a self-consistency repair using the ASN's own content.

## Issue 2: §INSERT vs. COPY specifies an out-of-scope operation in prose
Reason: The fix is internal — collapsing COPY exposition to the single identity-fixing contrast is a scope/editorial decision; the load-bearing point is already carried by INS.identity and its corollaries within the ASN, requiring no design intent or implementation evidence.

## Issue 3: Narrative/editorial meta-prose in structural slots
Reason: The fix is internal — deleting rhetorical framing or replacing it with the already-stated object-level fact ("INSERT never reassigns an existing I-address") needs no external input.
