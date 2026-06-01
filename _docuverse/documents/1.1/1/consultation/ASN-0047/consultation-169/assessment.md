# Channel Assignment — ASN-0047 review-169

**Date:** 2026-05-31 20:45

## Issue 1: J1'★ derivation asserted "in the same manner," never shown
Reason: The fix is a weakest-precondition computation run backward from P4a (an invariant already stated in the ASN); naming the target invariant and showing the wp steps is internal formal work requiring neither design intent nor implementation evidence.

## Issue 2: Duplicated "T4b cannot identify the frontier" prose
Reason: Pure editorial deduplication between the K.δ rationale and the Properties table; no external input needed.

## Issue 3: SubAllocFresh "single carrier" sentence is use-site inventory
Reason: Pure editorial deletion of a meta-sentence; derivable from the ASN alone.
