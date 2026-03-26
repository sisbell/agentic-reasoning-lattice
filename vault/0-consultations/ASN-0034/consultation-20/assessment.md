# Revision Categorization — ASN-0034 review-20

**Date:** 2026-03-26 02:33

## Issue 1: D0 — spurious dependency on D1, missing TumblerSub
Category: INTERNAL
Reason: The fix requires only reading the D0 paragraph to confirm the derivation direction (D0 → D1, not D1 → D0) and that TumblerSub's formula is invoked. All evidence is in the ASN text.

## Issue 2: TA4 — undeclared dependency on TumblerSub
Category: INTERNAL
Reason: The TA4 verification explicitly applies TumblerSub's constructive definition step-by-step. The missing dependency is visible directly in the proof text.

## Issue 3: ReverseInverse — undeclared dependencies on TumblerAdd and TumblerSub
Category: INTERNAL
Reason: The proof cites TumblerAdd's result-length identity and constructs y via TumblerSub's definition. Both usages are explicit in the ASN's own proof.

## Issue 4: TA1-strict — undeclared dependency on TumblerAdd
Category: INTERNAL
Reason: All three cases of the verification invoke TumblerAdd's component-level constructive definition. The dependency is visible in the proof text.

## Issue 5: TA-MTO — spurious dependency on TumblerSub
Category: INTERNAL
Reason: Neither the forward nor converse proof mentions or uses TumblerSub. The property characterizes addition equivalence classes only. Readable directly from the proof.

## Issue 6: D1 — undeclared dependency on Divergence
Category: INTERNAL
Reason: The proof's opening sentence classifies the divergence as "type (i)" using the Divergence definition. The usage is explicit in the first line of the proof.

## Issue 7: PositiveTumbler — spurious dependencies
Category: INTERNAL
Reason: PositiveTumbler is a predicate definition ("at least one component is nonzero"), not a derived result. Definitions have no follows_from. This is apparent from the ASN text.
