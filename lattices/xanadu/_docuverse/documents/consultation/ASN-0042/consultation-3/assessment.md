# Revision Categorization — ASN-0042 review-3

**Date:** 2026-03-15 20:46

## Issue 1: O8 (IrrevocableDelegation) is contradicted by sub-delegation
Category: INTERNAL
Reason: The contradiction is between O8, O3, and O7(c), all present in the ASN. The corrected formalization (parent never regains effective ownership) is derivable from the existing definitions and the reviewer's analysis.

## Issue 2: O6 (StructuralProvenance) has a counterexample
Category: BOTH
Reason: The counterexample is valid, but choosing the correct fix requires knowing whether account-level addresses extending the user field can exist without delegation — a design intent question and an implementation evidence question.
Nelson question: Does extending the user field (e.g., allocating `[1, 0, 2, 3]` within account `[1, 0, 2]`) always constitute delegation to a new principal, or can account-level addresses exist without a corresponding ownership principal?
Gregory question: Can the udanax-green allocator create account-level addresses (zeros = 1) that extend beyond the session's account prefix without creating a corresponding account entry — i.e., does any code path produce sub-account tumblers without delegation?

## Issue 3: `delegated(π, π')` is used but never defined
Category: INTERNAL
Reason: The ASN already contains all necessary primitives — principal introduction (O12), prefix ordering, effective ownership (O2), and subdivision authority (O5). The definition can be constructed as a state-transition predicate from these existing concepts.

## Issue 4: O7 formal statement omits authorization constraint
Category: INTERNAL
Reason: The missing constraint (most-specific covering principal) is already stated as O5 within the ASN and correctly invoked in the prose. The fix is incorporating the existing O5 predicate into O7's formal premises.
