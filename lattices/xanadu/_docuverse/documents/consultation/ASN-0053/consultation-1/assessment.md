# Revision Categorization — ASN-0053 review-1

**Date:** 2026-03-18 17:08

## Issue 1: Displacement round-trip fails when #start > #width
Category: INTERNAL
Reason: The counterexample and fix are derivable from TumblerAdd, TumblerSubtract, and T3 definitions already in ASN-0034. Adding a same-length precondition requires no external evidence.

## Issue 2: S1 (IntersectionClosure) is false without level constraint
Category: INTERNAL
Reason: The counterexample is constructed entirely from existing tumbler arithmetic definitions. The fix — adding a level-compatibility precondition — follows from the same definitions that expose the failure.

## Issue 3: S4 partition proof uses invalid round-trip
Category: INTERNAL
Reason: The round-trip failure and the required precondition (#s ≤ #p) are derivable from the tumbler arithmetic in ASN-0034. The counterexample uses only definitions already present.

## Issue 4: S6 (LevelConstraint) must be a formal predicate
Category: INTERNAL
Reason: The counterexamples in Issues 1-3 already demonstrate that the length constraint (#t₁ = #t₂) is the correct formalization, not the divergence constraint. The disambiguation is derivable from the ASN's own definitions without external evidence.

## Issue 5: D0 is necessary but not sufficient
Category: INTERNAL
Reason: The insufficiency of D0 and the need for a length constraint are demonstrated by counterexamples constructed from existing ASN-0034 definitions. Strengthening D0 requires no design intent or implementation evidence.

## Issue 6: S9 Case 2 proof is tangled
Category: INTERNAL
Reason: The logic is acknowledged as correct — this is purely a presentation restructuring into explicit sub-cases, requiring no external input.

## Issue 7: No worked example for split or width composition
Category: INTERNAL
Reason: Constructing and verifying a worked example requires only the definitions already present in the ASN. The suggested example can be mechanically verified against S4 and S5.

## Issue 8: Five-case span classification is unlabeled
Category: INTERNAL
Reason: The classification is already present and complete — this is an editorial task of assigning a property label to existing content.
