# Channel Assignment — ASN-0098 review-8

**Date:** 2026-05-25 20:58

## Issue 1: LP13 is a restatement of LP12
Reason: The fix is structural — either fold LP13 into LP12 and remove the label, or give it distinct content drawable from material already in the ASN (e.g., the unconditional `a ∈ dom(Σ'.L)` persistence follows from L12 of ASN-0043 plus LP3★, both already cited). No external input needed.

## Issue 2: Worked trace branches without demarcation
Reason: Pure editorial fix — relabel the branching state and add explicit transition language ("alternative continuation from Σ_1"). All technical content is already present; only the narrative thread needs clarification.

## Issue 3: Achievability discussion silent on nesting documents
Reason: The reviewer has already sketched the argument (descendants carry `1` or `2` at position `#d_0 + 1`, while `s ⊕ ℓ ≤ inc(t_m, 0)` keeps that position at `0`). Completing it requires only the chain-structure facts from ASN-0093 and divergence reasoning from ASN-0034's T-axioms, both already referenced. Internal completion.

## Issue 4: LP8's postcondition for newly registered d_new is informal
Reason: The content is already proved in the existing LP8 prose; the fix is to elevate it to a formal second postcondition and update the claims table. Restructuring only.

## Issue 5: F infiniteness not acknowledged
Reason: Requires a one-sentence acknowledgement plus pointer to the structural-form decidability argument. Both T0(a)/T0(b) of ASN-0034 and the chain-form characterisation are already cited; no new theory needed.

## Issue 6: No concrete numerical example for tightness or LP19
Reason: The example is to be built from the ASN's own definitions — specific chain indices, `inc` applications, and span endpoints already formalised. Construction is mechanical from existing material; verification of arithmetic against allocator behaviour is not required since the abstract chain structure already pins down what K.α emits.
