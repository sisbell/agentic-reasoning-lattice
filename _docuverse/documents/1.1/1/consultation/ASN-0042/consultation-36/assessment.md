# Channel Assignment — ASN-0042 review-36

**Date:** 2026-05-14 04:02

## Issue 1: Worked Example mislabels a₂ as a document address
Reason: Internal labeling inconsistency with T4c (LevelDetermination) already in the ASN. Fix is mechanical — either rename the address or correct the level label using the ASN's own zero-count semantics.

## Issue 2: Worked Example contradicts itself about a₁'s allocator
Reason: Internal inconsistency between two sections of the worked example. Fix requires picking one consistent narrative; no design intent or implementation evidence is at stake.

## Issue 3: AccountPrefix proof leaves an implicit zeros-count step in the O6 forward direction
Reason: Proof gap fillable from T4b (UniqueParse) and the Prefix (PrefixRelation) definition already cited in the ASN. Pure proof hygiene, no external evidence needed.

## Issue 4: O8 quantifier semantics underspecified
Reason: Formalization issue about how `delegated_Σ(π, π')` interacts with the outer quantifier over `Σ'`. Fix is to restate the trajectory binding using the ASN's existing notation; no design or implementation question.

## Issue 5: O10 Form B trailing-zero exclusion left implicit
Reason: Missing one-line invocation of T4a (SyntacticEquivalence), already cited elsewhere in the ASN. Pure proof gap, derivable internally.

## Issue 6: Sub-account namespace example skips intermediate baptisms
Reason: Requires aligning the example with ASN-0040's `next()` semantics already cited in the O10 trajectory. Internal to the formalization; no need to query Nelson's design intent or Gregory's implementation.
