# Channel Assignment — ASN-0070 review-23

**Date:** 2026-06-02 15:54

## Issue 1: No worked example exercises the cross-subspace straddling case (both result components non-empty)
Reason: The fix is internal — adding the worked configuration combines machinery already fully specified in the ASN (F0's partition, F-subspace's two-way decomposition, the joint-denotation disjointness, and the block-intersection computation from Configs 1 and 5). Constructing an endset with both a content span and a link span and verifying both branches simultaneously is mechanical given the existing definitions; no design intent or implementation behavior is at issue.
