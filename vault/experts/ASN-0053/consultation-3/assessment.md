# Revision Categorization — ASN-0053 review-3

**Date:** 2026-03-18 17:58

## Issue 1: Mutual determination claim is false for (width, reach) → start
Category: INTERNAL
Reason: The counterexample and correct statement are both derivable from TumblerAdd's definition already present in ASN-0034. The fix is narrowing the claim to the two directions that hold.

## Issue 2: D1 a = b remark is undefined
Category: INTERNAL
Reason: The TA0 precondition (w > 0) is already stated in ASN-0034. The fix is removing or correcting the remark based on the ASN's own preconditions.

## Issue 3: Constructed spans not verified against T12
Category: INTERNAL
Reason: T12 verification follows mechanically from the strict ordering of endpoints and the divergence properties already established in each proof. The missing steps are derivable from definitions already present.

## Issue 4: S11 statement lacks level preconditions
Category: INTERNAL
Reason: The proof already states the requirement; the fix is copying the same precondition pattern used in S1, S3, S4, and S5 into the formal statement. Purely an internal consistency fix.

## Issue 5: S8 does not prove denotation preservation
Category: INTERNAL
Reason: The construction is fully specified in the ASN. The missing loop invariant is a standard proof obligation derivable from the merge/emit steps already described.

## Issue 6: SC exhaustiveness asserted without case analysis
Category: INTERNAL
Reason: The case analysis is a combinatorial argument over orderings of four boundary points under a total order, using only the constraint start < reach. No external evidence needed.

## Issue 7: S7 proof is a single sentence
Category: INTERNAL
Reason: The unit span construction and its T12 verification follow directly from the tumbler definitions in ASN-0034. The fix is making the implicit construction explicit.
