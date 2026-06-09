# Channel Assignment — ASN-0117 review-27

**Date:** 2026-06-09 10:57

## Issue 1: Duplicated summary across Effect section and conclusion
Reason: Pure deletion of a redundant sentence whose content is carried by the conclusion and the claim table; no design intent or implementation evidence bears on it.

## Issue 2: Meta-prose around what is/isn't a "distinct claim"
Reason: Editorial collapse of defensive prose into one sentence; address-permanence-is-P0 and the invariant-package wording are already fully grounded in the ASN's own claims, so the fix is internal.

## Issue 3: Invariant-package appeal assumes reachability without stating it
Reason: This is a proof-discipline fix about how ASN-0047's ExtendedReachableStateInvariants is invoked — either tighten DELETE's precondition with reachability or recast as an inductive step. Both options are derivable from the ASN's own structure and the cited foundation; no design intent or implementation evidence is needed.
