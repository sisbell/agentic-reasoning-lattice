# Channel Assignment — ASN-0134 review-37

**Date:** 2026-06-14 10:24

## Issue 1: W3 mis-classifies population contiguity as serialization-borne
Reason: Internal — the reclassification follows from the ASN's own committed model: `inc(max,0)` deposits (ASN-0093, fixed in §1) plus monotone frontiers (`C0`/`L12`) couple uniqueness and contiguity, so the inductive argument is identical in structure to W0's, which the note already runs. The Gregory citation is removed by recognizing it describes the hypothetical counter-style allocator the committed model excludes — itself a recognition internal to §1's model commitment, needing no new evidence.

## Issue 2: §4 K.σ scoping paragraph describes a case it then assumes away, and duplicates it in H3
Reason: Internal — a redundancy/structure cut whose surviving content (K.σ is not a sub-allocator emission; d-freshness and prior registration are hypotheses from the excluded entity layer) is already stated in the ASN; no design intent or implementation evidence is at issue.

## Issue 3: Structural-narration and self-promotion in claim-adjacent prose
Reason: Internal — purely editorial removal of self-grading and document-structuring phrases; the underlying claims are unchanged and derivable from the ASN alone.
