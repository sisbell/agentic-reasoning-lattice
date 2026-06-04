# Channel Assignment — ASN-0091 review-87

**Date:** 2026-06-04 05:03

## Issue 1: Defensive meta-prose contrasting an unused derivation route
Reason: This is a pure editorial deletion of defensive prose; the ExtendedReachableStateInvariants citation under RA-bndy is already the complete argument and is fully present in the ASN. No design intent or implementation evidence is needed.

## Issue 2: Clause (v) discharge forward-references a frame stated ~10 sections downstream
Reason: RE-sub/RE-ext derive directly from ASN-0084's R-PPERM/R-SPERM and R-FRAME-P/S(a), both already cited in the ASN; relocating them ahead of the clause table is a structural rearrangement derivable from the note's own dependency order. No external channel is needed.
