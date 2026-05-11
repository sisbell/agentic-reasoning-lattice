# Channel Assignment — ASN-0036 review-87

**Date:** 2026-05-11 03:19

## Issue 1: S7c postcondition (c) layers two vacuous conditionals
Reason: The fix is purely internal restating — removing redundant guards based on S7c's own axiom and T4's positive-component constraint already established in ASN-0034. No design intent or implementation evidence needed.

## Issue 2: S5 cross-document construction asserts existence of N+1 distinct documents without citation
Reason: The fix is internal — either cite ASN-0034's T0(a)/T0(b) for an injection from ℕ into T or exhibit explicit document tumbler witnesses. Both options are derivable from the foundation ASN.

## Issue 3: S8 Postconditions assert subspace preservation as if load-bearing for the singleton decomposition
Reason: The fix is logical bookkeeping — split the contract or annotate the Depends list to reflect that S7c is consumed only by the auxiliary lemma's k ≥ 1 branch, vacuous for the singleton witness. Internal restructuring only.

## Issue 4: S5 within-document construction's S2 check cites distinctness "by hypothesis" when it's by construction
Reason: Pure wording fix — replace "by hypothesis" with "by construction (distinct last components, T3)". The justification is already present in the proof body and ASN-0034.
