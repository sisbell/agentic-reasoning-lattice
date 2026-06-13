# Channel Assignment — ASN-0125 review-10

**Date:** 2026-06-13 11:03

## Issue 1: Edit-discipline is never assembled into an invariant — the base case and Nullify/frame-op preservation are unstated
Reason: The fix is internal — the base case follows from L₀ = ∅ (ASN-0047, already cited in the substrate references), the two halves of edit-discipline are Df-DISC's own definition, Nullify's effect (one unit-depth [R] tuple, no [K_sup] claim) and the frame-ops' inertness (Vocabulary fact V: `L' = L`, slices and `dom(L)` unchanged) are already established, and the admissible operation set is forced by the ASN's own framework (EL1's Remark already concedes a bare non-conforming emission would break discipline). Assembling the induction reorganizes present material; it needs no new design intent or implementation evidence.

## Issue 2: "Layer transfer" paragraph is a use-site inventory wrapped in a defensive disclaimer
Reason: Pure prose compression — the reviewer supplies the exact replacement kernel, and that kernel (ASN-0086's results depend only on Σ.L and dom(M); both evolve identically under the full vocabulary via Vocabulary fact V and M1) is already present in the paragraph. Dropping the use-site fact inventory and the defensive disclaimer is internal editing that requires no channel.
