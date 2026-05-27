# Channel Assignment — ASN-0101 review-7

**Date:** 2026-05-27 15:55

## Issue 1: D10 conflates step-level vacuity with composite-level coupling
Reason: The reviewer has supplied the correct framing — distinguish "DEL creates no new coupling obligations" (true at the step level via D0's frame) from "DEL preserves all composite-level obligations" (false, as the counter-example shows). The fix is internal: re-read ASN-0047's ValidComposite★ scope and restate D10 accordingly.

## Issue 2: D7's justification misses the L0 citation for the I-subspace partition
Reason: This is a pure citation fix — L0 is already in ASN-0093's invariant catalogue, and the ASN already cites L14 alongside it. Adding the L0 link to bridge `subspace(v)` to `subspace_I(a)` is derivable from the ASN's own references.

## Issue 3: Boundary case enumeration omits the non-degenerate interior case
Reason: This is a structural/coverage fix to existing prose. The worked example already exercises the non-degenerate interior case; the choice is purely editorial — either trace it explicitly under boundary cases or point the closing remark to it. No external input needed.

## Issue 4: Atomicity argument's "observable intermediate state" is informal
Reason: The reviewer has supplied the correct formal framing (predicates over the transition sequence in SequentialAtomicTransitions). ASN-0093 supplies the formal apparatus the ASN already cites, so the reframe is derivable internally.

## Issue 5: Reduction argument's m_S = 2 boundary handling is implicit
Reason: Pure clarification — at `m_S = 2` the intermediate range `2 ≤ j ≤ m_S − 1` is empty and the claim holds vacuously. The reviewer has supplied the exact replacement sentence; this is internal.

## Issue 6: Worked content-subspace example doesn't address V_2(d) contribution to the projection
Reason: The symmetric reasoning (S3★ + L0 forces `M(d)(V_2(d)) ⊆ dom(L)` with `subspace_I = s_L`, disjoint from content-subspace coverage) is fully derivable from cited axioms. Pure writing fix.

## Issue 7: D8 Group (i) S2 functionality proof skips disjointness verification
Reason: The reviewer has supplied the one-line argument (`Λ` has last component `≤ p − 1`, `Q` has last component `≥ p`, ranges disjoint; cross-subspace via first-component difference). Fully internal.

## Issue 8: D9 second bullet uses asymmetric notation V_{S'}(M'(d)) vs V_{S'}(d)
Reason: Pure notational consistency fix — D6 (already established in the same ASN) makes the two sets equal. Internal.
