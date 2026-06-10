# Channel Assignment — ASN-0126 review-103

**Date:** 2026-06-10 11:46

## Issue 1: Registry frame conditions stated three times, transition relation redefined
Reason: Pure anti-bloat consolidation — the fix deletes redundant restatements of content already present in the note (the `→_sh` definition in The shape-gated emit, the frame bullets). No design intent or implementation evidence bears on which telling to keep.

## Issue 2: P5's proof states the address-pinning twice, the first time ahead of its B1 step
Reason: Intra-paragraph duplication fix — the correct derivation (contract pins `a_emit(π(Σ), d)`, then B1 identifies it with `a_emit(Σ, d)`) already appears in the same paragraph; the revision just removes the premature duplicate. Entirely derivable from the proof's own text.

## Issue 3: C3-liveness rationale owned by two sections
Reason: Single-owner deduplication — the wp section already contains the full self-contained rationale; the fix deletes the forward-announcing sentence from the bridge section. No external grounding needed to choose the owner.
