# Channel Assignment — ASN-0047 review-263

**Date:** 2026-06-01 15:51

## Issue 1: D-CTG★/D-MIN★ "Justification" does not justify the strengthening
Reason: Resolving this requires arguing whether contiguity is the correct contract for the link subspace against the foundation's documented tombstoning rationale — a design-intent question (Nelson) and an implementation-fact question (Gregory), neither of which is settled by the ASN's own content.
Nelson question: Did the design intend a document's links to form a dense, contiguous, arrival-ordered stream (so withdrawal can only truncate from the end), or did it intend tombstoning that leaves interior gaps when a link is withdrawn?
Gregory question: Does udanax-green store/index a document's links as a contiguous gap-free sequence, or does link deletion leave gaps (tombstones) at interior positions?

## Issue 2: J4 narrative duplicates Definition (Fork) step (ii)
Reason: Pure editorial deduplication — collapse the operand-tracking content-source statement to one load-bearing location and a pointer; no design intent or implementation evidence is in question.

## Issue 3: K.δ freshness mechanism stated in two places with a deferral
Reason: Pure editorial consolidation — keep the per-k freshness split in one location and have the other reference it; the mechanism itself is already fully specified in the ASN.
