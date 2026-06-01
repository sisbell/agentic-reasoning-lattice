# Channel Assignment — ASN-0086 review-169

**Date:** 2026-06-01 07:06

## Issue 1: A_K computability leans on a mis-cited decidability of coverage-equality
Reason: Internal fix. The decidability of coverage-set-equality (finite unions of half-open T1-intervals) reduces to the same T2 (IntrinsicComparison, ASN-0034) primitives the note already uses for `nullified`; the derivation is available from the ASN's own cited machinery and only needs to be written out, not the asserted L8 basis.

## Issue 2: R7a's full ↝-decomposition generality is unused by its only cited consumer
Reason: Gregory. Deciding whether to keep R7a as a standalone closure theorem (with independent motivation) versus trimming it turns on whether real higher-layer operations actually emit multiple links across several K-steps — an evidence question about the implementation, not derivable from this ASN.
Gregory question: Do udanax-green operations (e.g. INSERT/DELETE/REARRANGE) ever emit more than one link into the spanf store within a single user-level operation, or does each operation touch the link store at most once?

## Issue 3: R0a proof states the same premise-inventory fact twice
Reason: Internal fix. Removing the duplicated premise-inventory sentence is a pure editorial deduplication derivable from the ASN text alone.
