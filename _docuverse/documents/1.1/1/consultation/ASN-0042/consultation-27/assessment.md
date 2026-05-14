# Channel Assignment — ASN-0042 review-27

**Date:** 2026-05-13 23:45

## Issue 1: O10's single-step framing is too tight for the construction
Reason: The fix is derivable from ASN-0042 itself plus its existing dependency on ASN-0040's baptism mechanism. Both the contract relaxation (`Σ → Σ'` → `Σ →⁺ Σ'`) and the invariant for intermediate baptisms follow from properties already in this ASN (O5, O1a, O7).

## Issue 2: T5/Prefix attribution errors
Reason: Pure citation correction. The `Prefix (PrefixRelation)` foundation property is already referenced in the ASN; T5's actual content (ContiguousSubtrees) is also already used correctly elsewhere. Internal fix.

## Issue 3: O1 mis-classified in the Properties Introduced table
Reason: Editorial relabeling to match the body's explicit statement that O1 is a definition. No external evidence required.

## Issue 4: O3 proof does not explicitly conclude that π' came from delegation
Reason: The chain (O15 + iterated O12 + O14) is already present in the ASN's axioms and is explicitly worked in AccountLevelPermanence's Step 1. The fix is to add the same closure sentence to O3.

## Issue 5: AccountLevelPermanence's multi-step rooting argument is muddled
Reason: The reviewer supplies the cleaner argument outline (first delegator into dom(π) must be π by O15 + already-proven prefix containment). All inputs are internal axioms.

## Issue 6: Worked example missing the self-ownership boundary case
Reason: The boundary case `ω(pfx(π))` resolves by direct application of O2 (longest match) and O1b (injectivity), both already established. No new evidence or intent needed.

## Issue 7: Redundancy between O2's proof and ω(a)'s proof
Reason: Pure structural/editorial merge. Both proofs already exist in the ASN; the fix is to consolidate them.

## Issue 8: `pfx(π)` formal contract lists postconditions that are not really postconditions of pfx
Reason: Editorial restructuring of the contract block. O1a and O1b are already stated as separate axioms; the fix is purely how they are presented in the `pfx` block.
