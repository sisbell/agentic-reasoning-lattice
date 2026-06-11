# Channel Assignment — ASN-0115 review-69

**Date:** 2026-06-10 22:16

## Issue 1: R11's "weakest precondition" postcondition is not pinned down, so the stated condition is not actually the weakest
Reason: The fix is internal — the review itself identifies the resolution (pin the postcondition to "an item resolved from `a`"), and the necessity/sufficiency argument is decidable from material already in the ASN: the `item` definition, S3★/S0 as cited, and the S4 coincidental-equality point R8 already states. No design-intent or implementation evidence bears on which postcondition phrasing the wp claim should use.

## Issue 2 (anti-bloat): proof-commentary asides that restate the claim's own scoping or comment on difficulty
Reason: Purely editorial deletion of meta-prose; the review specifies the exact clauses to drop and the substantive steps stand on the ASN's own cited invariants (S8-depth, Confinement). No external consultation needed.
