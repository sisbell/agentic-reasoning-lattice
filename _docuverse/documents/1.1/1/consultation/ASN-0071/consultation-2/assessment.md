# Channel Assignment — ASN-0071 review-2

**Date:** 2026-05-25 12:18

## Issue 1: Codomain proof for iaddrs has a gap; vspec preconditions admit subspace crossing
Reason: The fix is a technical adjustment internal to the ASN — either tighten the vspec precondition to require `actionPoint(ℓ) ≥ 2` or add explicit subspace filtering in `iaddrs_one`. The design intent ("level-uniform V-span over the content subspace") is already stated in the prose, and the relevant foundation invariants (S3★, TumblerAdd, ActionPoint, C0/C0a) are already cited; no design-intent or implementation evidence is needed.
