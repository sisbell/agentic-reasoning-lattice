# Channel Assignment — ASN-0118 review-8

**Date:** 2026-06-08 22:29

## Issue 1: The symbol `p` is overloaded — spec-set arity and insertion position
Reason: Pure notational renaming — pick a fresh symbol for spec-set length and reserve `p` for the insertion position. No design intent or implementation evidence bears on a symbol choice; the fix is internal to the ASN.

## Issue 2: CP3 prose attributes post-state function-ness to I3-S2, which covers only the shift
Reason: The decomposition section already states the correct scoping (I3 covers only the shift; gap-fill function-ness comes from the tiling/K.μ⁺ disjointness argument). The fix is to align the CP3 summary prose with reasoning already present in the ASN — derivable internally.
