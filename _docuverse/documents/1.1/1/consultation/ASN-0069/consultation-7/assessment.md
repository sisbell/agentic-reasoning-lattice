# Channel Assignment — ASN-0069 review-7

**Date:** 2026-05-25 13:56

## Issue 1: K.δ's uniform precondition `parent(e) ∈ E` not discharged
Reason: Fix is internal — the required discharge cites only KDeltaParentK01 and P8 from ASN-0047, both already in the ASN's reference base. No design intent or implementation evidence needed.

## Issue 2: K.δ's outer preconditions `ValidAddress(e)` and `¬IsElement(e)` not explicitly discharged
Reason: Fix is internal — required citations (T10a.4, SubAllocatorAxiom.T10aConformance, IsDocument→¬IsElement) all already in ASN-0034/ASN-0047 and used elsewhere in the ASN. Pure formal-completeness gap.

## Issue 3: Subsequent-fork freshness argument compresses two independent facts
Reason: Fix is internal — separation of T10a.7, SequentialTransitionAxiom+P1, and T10a.6 into three independent steps. All cited material already in ASN-0034/ASN-0047. Pure prose-structure fix.

## Issue 4: V12(d)'s intersection notation collapses to a trivial set
Reason: Fix is internal — simplification follows from V4 (already in ASN), P4★, and P2 from ASN-0047. The reviewer supplies the one-line derivation directly. No external input needed.

## Issue 5: V8b's "no monotonic-decay" claim requires more grounding
Reason: Fix is internal — the structural constraints (K.μ⁻'s per-subspace-suffix-retention precondition, K.μ⁺'s D-CTG★/D-MIN★/D-SEQ★) are all in ASN-0047. Restricting the re-installation claim to contiguity-admissible positions is a formal-precision fix derivable from existing references.
