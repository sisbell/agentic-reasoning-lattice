# Channel Assignment — ASN-0119 review-3

**Date:** 2026-06-09 00:23

## Issue 1: P7c (ContiguityWP) is not the weakest precondition — it is wrong in both directions
Reason: The fix is internal — both counterexamples are built from facts already in the note (π is a uniform ordinal shift per region, the destinations tile abuttingly so β-end becomes adjacent to α-start, and coverage is an arbitrary address set via L4 EndsetGenerality). Correcting the wp to require a pre-contiguous run and account for the relocated seams is pure derivation from the ASN's own permutation geometry; neither design intent nor implementation evidence bears on the logical error.
