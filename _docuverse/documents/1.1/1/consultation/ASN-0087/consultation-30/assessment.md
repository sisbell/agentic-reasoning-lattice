# Channel Assignment — ASN-0087 review-30

**Date:** 2026-06-03 22:40

## Issue 1: M-DepthConv content restated 6+ times across the note
Reason: Pure editorial consolidation. The convention (Σ leaves depth free when V_{s_L}(d)=∅, MAKELINK fixes m=2, else inherit m_L(d)) is fully stated within the ASN; collapsing the restatements to references requires no design intent or implementation evidence.

## Issue 2: J0/J1★/J1'★ discharge stated twice, then a third time in the claims table
Reason: Pure deletion of a redundant summary paragraph. The bullets and M-Inv-Bdry already carry the content; no external channel is needed to remove restated prose.

## Issue 3: L1c re-derives the full inc-chain that K.λ already guarantees
Reason: The fix turns on whether the link sub-allocator's emission inherently satisfies inc-chain conformance (L1c) for every A_L(d) output, the way freshness is packaged — an evidence question about what the allocator actually guarantees, which Gregory can confirm and the ASN cannot settle internally.
Gregory question: Does the udanax-green link allocator guarantee that every A_L(d) emission satisfies the inc-chain (L1c / LinkAllocatorConformance) structurally, so the property transfers from K.λ without per-step reconstruction?

## Issue 4: Home-document-not-privileged point restated across four sites
Reason: Editorial deduplication of an identical conclusion (privilege is structural placement, not semantic discoverability) already derived within the ASN; keeping one derivation plus the index entry needs no external input.
