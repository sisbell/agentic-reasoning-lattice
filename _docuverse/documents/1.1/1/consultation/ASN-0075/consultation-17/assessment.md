# Channel Assignment — ASN-0075 review-17

**Date:** 2026-05-25 17:53

## Issue 1: wp(SHOWDELETIONS, Q0) is not the weakest precondition
Reason: The fix is a structural correction to the wp formula using definitions and axioms already in the ASN (observational pass-through rule, P4★ from ASN-0047 which is already cited). No design intent or implementation evidence is needed — the asymmetry with Q1's wp inside the same section is sufficient guidance.

## Issue 2: Bijection in D-ACT — verify class-as-shift-chain explicitly
Reason: All three pieces (T1-contiguity of classes, no-intermediate-content lemma, min(C) as lower endpoint) are already proved earlier in the same D-ACT section. The fix is one chaining sentence assembling material the ASN already contains.

## Issue 3: D-ORD presentation order claim is weakly verified
Reason: The fix is a one-sentence consequence of S2 (ArrangementFunctionality, ASN-0036), which is already cited in the ASN for transclusion integrity. No external channel is needed to establish that a function's distinct outputs come from distinct inputs.
