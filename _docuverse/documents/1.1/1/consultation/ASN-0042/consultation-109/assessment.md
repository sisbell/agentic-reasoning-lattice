# Channel Assignment — ASN-0042 review-109

**Date:** 2026-05-30 03:56

## Issue 1: `delegated` relation used with undefined two-place arity in O7
Reason: Purely a notational consistency fix — restate O7's quantifier and Formal Contract using the already-defined `delegated_Σ(π, π')` abbreviation or the four-place form; no design intent or implementation evidence is at stake.

## Issue 2: Prose around O17b explains downstream interaction rather than what the axiom says
Reason: Anti-bloat removal — drop the trailing reconciliation paragraph and rely on the existing O18/DelegatorAllocatesPrefix citation; entirely an editing decision internal to the ASN's own reasoning structure.

## Issue 3: Defensive justification against a non-claim in the Exclusivity Invariant
Reason: Reduce defensive meta-prose to the load-bearing sentence (exclusivity is a property of `ω`, established at O2); the content is already present in the ASN, so the fix is purely editorial.

## Issue 4: Forward-reference accretion to the Worked Example and to "below"
Reason: Either prove the unbounded-recursion claim where O7(c) is stated (the Worked Example chain already supplies the construction) or label it illustrated-not-proved, and strip ordering-justification asides — all derivable from existing ASN content.

## Issue 5: Derived result with no abstract consumer
Reason: A placement decision — show DelegatorAllocatesPrefix is load-bearing for an abstract claim and cite it, or demote it to an inline Worked Example remark; resolvable by inspecting the ASN's own derivation chains.
