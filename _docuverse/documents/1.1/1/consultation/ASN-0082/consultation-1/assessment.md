# Revision Categorization — ASN-0082 review-1

**Date:** 2026-04-09 14:07

## Issue 1: Cross-ASN reference to ASN-0047
Category: INTERNAL
Reason: The ASN already describes M(d) as "the arrangement function with M(d) : T ⇀ T for each document d." Defining it locally requires only promoting that prose description into a standalone definition and dropping the ASN-0047 citation.

## Issue 2: Implicit references to non-foundation ASN-0036
Category: INTERNAL
Reason: Both properties are already stated in the ASN's own prose ("all V-positions in the subspace share p's depth" and subspace identifier ≥ 1). The fix is restating them as named local axioms rather than dangling label references.

## Issue 3: I3 has no formal precondition block
Category: INTERNAL
Reason: All constraints (n ≥ 1, #p ≥ 2, S = subspace(p) ≥ 1, etc.) are present in the surrounding prose. The fix is collecting them into a structured precondition/postcondition block — no external evidence needed.

## Issue 4: No frame condition for positions below p
Category: INTERNAL
Reason: The ASN already asserts "the permanent identity of every existing byte is invariant under insertion" and the Nelson quote covers all bytes. The left-region frame, cross-subspace frame, and cross-document frame are the formal statements of that already-claimed invariance — standard specification completeness derivable from the ASN's own claims.

## Issue 5: Incorrect citation in subspace preservation argument
Category: INTERNAL
Reason: The ASN defines shift via TumblerAdd (⊕) and describes exactly how TumblerAdd copies positions below the action point. The fix is replacing the erroneous TA5(c) citation with the TumblerAdd definition already present in the ASN.

## Issue 6: Worked example does not verify the full postcondition
Category: INTERNAL
Reason: The example already establishes [1, 1] → b and [1, 2] → b + 1 in the before-state. Extending the table to show these unchanged in the after-state is mechanical once the frame condition from Issue 4 is stated.
