# Channel Assignment — ASN-0045 review-21

**Date:** 2026-05-28 20:21

## Issue 1: Pairwise distinctness of 0,1,2,3 mis-cited to T0
Reason: Internal. The at-least-one paragraph already routes consecutiveness/ordering correctly through NAT-addcompat and NAT-order, and T0's own stated convention (quoted in the review) confirms arithmetic facts live in the NAT-axioms; the corrected citation is a mechanical match to reasoning already present in the same ASN.

## Issue 2: Constant-existence citations inconsistent across the four predicates
Reason: Internal. The choice is purely a citation-convention matter within the spec's own axiom system — whether `0` is grounded by NAT-closure as additive identity or as a pure T0-carrier fact is fixed by the definitions of T0 and NAT-closure in ASN-0034, requiring no design intent or implementation evidence; the fix is to apply the per-step convention uniformly across the four structurally identical predicates.
