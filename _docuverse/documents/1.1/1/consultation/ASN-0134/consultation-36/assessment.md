# Channel Assignment — ASN-0134 review-36

**Date:** 2026-06-14 10:00

## Issue 1: G1(i) claims chain-contiguity is step-preserved, contradicting W3 and §5
Reason: Internal fix. Every fact the repair needs is already in the note — A6's package membership, the model-intrinsic vs. serialization-borne partition (§5), the frontier argument (H0/H1), and W3's classification of contiguity as serialization-borne. The task is to reorder the proof (validity first, then A6) and rescope sentence 1 to the model-intrinsic conjuncts so G1(i) stops contradicting the note's own §5; no design intent or implementation evidence is required.

## Issue 2: W0's motivation is mislabeled as its proof
Reason: Internal fix. The proof of W0 stands complete in the claim statement ("Needs A0, nothing more"), and the issue is a pure framing defect — relabeling the Nelson quote from "proof" to "motivation." The relabeling depends on nothing outside the ASN; the quote's content is unchanged and the proof already present.

## Issue 3: Two sections defer to the same downstream open problem (mild)
Reason: Internal fix. Purely a structural deduplication — state the reader-gap once at its natural home (A5) and replace W4's re-explanation with a bare pointer. No external input is needed to consolidate two cross-references the note already contains.
