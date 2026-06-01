# Channel Assignment — ASN-0047 review-235

**Date:** 2026-06-01 10:41

## Issue 1: Redundant freshness premise in the fork worked example
Reason: Purely editorial — the fix removes an over-supplied discharge premise. SubAllocatorBundle.FirstEmission already establishes full freshness internally; deciding to drop or demote premise (i) requires only the ASN's own proof structure, no design intent or implementation evidence.

## Issue 2: K.δ case (ii) dispatch stated three times
Reason: Internal consolidation of three overlapping restatements into one authoritative location with references. The per-k discharge content already exists in the ASN; choosing the canonical home and cross-referencing requires no external channel.

## Issue 3: K.μ⁻ contraction-shape deferral chain
Reason: Internal de-duplication — the constructive ⟺ post-state equivalence is fully derived in the dedicated section; removing the forward-pointer scaffolding from the definition and amendment is a structural edit derivable from the ASN alone.

## Issue 4: CL-UNIQ-under-K.μ~ derived twice
Reason: Internal — the same injectivity inference appears in sub-step (4) and the Class (a) verification prose. Keeping it in one site and referencing from the other needs only the ASN's existing proof, no external input.
