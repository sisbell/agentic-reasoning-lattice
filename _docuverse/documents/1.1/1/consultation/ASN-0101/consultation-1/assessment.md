# Channel Assignment — ASN-0101 review-1

**Date:** 2026-05-27 14:01

## Issue 1: D1 justification cites wrong lemmas
Reason: Citation correction. The correct lemmas (TA3-strict, OrdinalOrderEquivalence, ASN-0082's D-BJ) exist in foundation ASNs and can be substituted mechanically.

## Issue 2: D7 statement omits link store membership
Reason: Internal precision fix. D2, D3, and L14 disjointness already establish the correct postcondition; the statement just needs to be widened to include `dom(L')`.

## Issue 3: D0 frame omits E and R
Reason: Internal fix following ASN-0047's established K.μ⁻ pattern (J2). The convention for framing E and R is documented in the foundation; DELETE inherits it.

## Issue 4: D8 missing invariants
Reason: Mechanical enumeration. The invariants are defined in ASN-0047/0036/0043/0093, and their preservation under DELETE follows structurally from D2/D3/D5/D6 plus the (corrected) framing of E and R.

## Issue 5: Relationship to foundation transition vocabulary unspecified
Reason: Requires design intent on whether middle-span deletion is a primitive operation kind and implementation evidence on whether it is performed atomically. Both channels inform the choice between extending ValidComposite★ vs decomposing into existing transitions.
Nelson question: Was middle-span DELETE intended as a single primitive operation distinct from the suffix-truncation K.μ⁻, or as a composite built from existing transition kinds?
Gregory question: Does udanax-green's two-phase (knife + classify-walk) protocol execute as one atomic transition, or does it sequence through observable intermediate states that correspond to existing K.μ⁻ / K.μ~ kinds?

## Issue 6: D8 cites OrdShiftHom incorrectly
Reason: Citation correction. TumblerSub's result-length identity and vpos's length-preserving construction are stated in ASN-0034 and can be substituted mechanically.

## Issue 7: No concrete worked example
Reason: Illustration is constructible directly from D0's specification; the reviewer even provides the numeric scenario. No external consultation needed.

## Issue 8: Boundary cases not systematically addressed
Reason: Mechanical case analysis against D0 and D8 as already stated. The configurations (empty subspace, start, end, singleton, interior) follow from the precondition envelope without external input.

## Issue 9: D1's contiguity claim has an undefined edge case
Reason: Pure rewording to handle the empty case. Internal fix.

## Issue 10: D9's third clause uses inconsistent quantification
Reason: Notation fix — either restrict LHS to subspace S explicitly or redefine L/X/R as subsets of `dom(M(d))`. Both options are derivable from the ASN's own definitions.
