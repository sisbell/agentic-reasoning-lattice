# Channel Assignment — ASN-0076 review-22

**Date:** 2026-05-27 13:15

## Issue 1: Notational collision around `Σ_0` in E5's proof
Reason: Pure notational disambiguation internal to the ASN's induction proof. No design intent or implementation evidence needed — choosing a non-colliding symbol is mechanical.

## Issue 2: Worked example does not verify E0's induction base for arity-2 element field
Reason: All cited facts (TA5(c), TA5(b), TA5-SigValid, T4 field-segment, T0 successor) are already named in the foundation recap and used in E0's general discharge. The fix is making the chain explicit at the concrete value `ℓ_sup = [4.0.2.0.3.0.2.2]`.

## Issue 3: E4's "no further atomic transitions intervene" argument under-discharges the cited axiom
Reason: The reviewer's diagnosis is that the SequentialTransitionAxiom citation is load-bearing for atomicity but not for adjacency — adjacency comes from the composite definition. Both repair paths (drop the citation or strengthen the composite definition) are internal editorial choices within ASN-0076's own framework.
