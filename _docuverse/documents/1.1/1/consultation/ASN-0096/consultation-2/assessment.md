# Revision Categorization — ASN-0051 review-2

**Date:** 2026-03-20 20:26

## Issue 1: SV6 proof omits T5 (ContiguousSubtrees)
Category: INTERNAL
Reason: The fix is to cite T5 (ContiguousSubtrees), which is an existing property in the spec. The missing proof step is fully derivable from T5's statement and the already-established endpoint sharing.

## Issue 2: SV10 prose contradicts its own formal statement
Category: INTERNAL
Reason: This is a prose/formula mismatch within the ASN. The formula demonstrates partial resolution while the prose claims empty resolution. Both the correct prose and the correct formula are derivable from the ASN's own definitions.

## Issue 3: SV11 proof — false convexity claim and unverified normalization precondition
Category: INTERNAL
Reason: (3a) The correct argument using span convexity (S0) plus ordinal monotonicity (TA-strict) is fully derivable from existing properties. (3b) S8's level-compatibility precondition is already stated in the spec; the fix is to add a precondition or weaken the claim accordingly.

## Issue 4: Endset Fragment definition is unsatisfiable
Category: INTERNAL
Reason: The informal gloss is correct and the formalization just needs to match it. The needed concepts — mapping blocks, ordinal sequences, π(e, d) — are all defined within the ASN. The fix replaces ⟦σ⟧ with contiguity within a mapping block's ordinal sequence.
