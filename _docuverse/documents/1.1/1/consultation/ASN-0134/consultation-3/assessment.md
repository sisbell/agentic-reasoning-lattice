# Channel Assignment — ASN-0134 review-3

**Date:** 2026-06-13 18:43

## Issue 1: A multi-type quiescence verdict is not realizable as "one atomic snapshot Observe"
Reason: The fix is derivable internally — §4's step/operation seam is a direct template for the per-call-read/per-verdict-snapshot seam, §3's already-cited run-to-completion model grounds reader-side snapshot realizability (the global loop over-provides it exactly as it over-provides clause 2's per-home serialization), and §8 already carries Nelson's "one cross-section" intent. The note can add a reader-side snapshot clause by analogy to clause 2 (or restrict V0 per option c) using its own materials and the inherited `Observe_K` surface defined in its dependencies (ASN-0086/0128); no new external evidence is required.

## Issue 2: §1 equates batch *contiguity* with batch *atomicity*; this is false and contradicts the note's own Open Question
Reason: Internal self-consistency fix — the note already separates writer-side contiguity (W4) from reader-side observation (A0/A3), already defers run atomicity to Open Question 3, and already treats the distinction correctly in §6; correcting §1 and sharpening A5 only aligns one section with the note's own apparatus. No design intent or implementation evidence is in question.
