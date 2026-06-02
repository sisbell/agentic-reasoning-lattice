# Channel Assignment — ASN-0070 review-20

**Date:** 2026-06-02 15:42

## Issue 1: The fragmentation sub-case and partial-block intersection are claimed but never demonstrated
Reason: Constructing a worked configuration where one endset I-span hits two non-adjacent same-subspace blocks at a non-zero offset is pure instantiation of F0 and F-contig, both fully specified within the note; the inverse-image computation, offset/width derivation, and F-sound/F-complete verification follow the same mechanics as C1–C5 already present, so no design intent or implementation evidence is required.
