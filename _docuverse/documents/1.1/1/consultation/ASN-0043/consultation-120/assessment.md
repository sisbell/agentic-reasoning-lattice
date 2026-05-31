# Channel Assignment — ASN-0043 review-120

**Date:** 2026-05-30 18:35

## Issue 1: L11a's shared-home embedding misstates the allocator structure, ignoring the second child-spawn that L1b forces
Reason: Internal. The correct allocator structure is fully determined by the ASN's own chain construction (L1c, L9 Case A, worked-example L1c) and T10a's at-most-once constraint — tracing both child-spawns or resting on tree membership requires only material already present in the ASN.

## Issue 2: L0b carries forward-reference meta-prose justifying non-repetition
Reason: Internal. Purely a prose trim to the bare attribution; the substantive content (derivation from L1c's chain via T10a.4) is already stated in the ASN.

## Issue 3: L9's "Selection of d'" introduces a vestigial rename
Reason: Internal. Mechanical removal of a no-op rename within the L9 proof; no design intent or implementation evidence bears on it.
