# Revision Categorization — ASN-0025 review-6

**Date:** 2026-03-07 09:23

## Issue 1: Undefined expression p ⊕ [0] in INSERT and COPY postconditions
Category: INTERNAL
Reason: The fix is a notational adjustment (split the quantifier or define a convention) using ASN-0001's existing TumblerAdd definition. No external evidence needed.

## Issue 2: V-space postconditions lack domain closure
Category: INTERNAL
Reason: The ASN already demonstrates the correct pattern in CREATE VERSION and CREATE DOCUMENT (explicit `dom(Σ'.v(d'))` characterizations). Extending this to INSERT/DELETE/COPY is mechanical.

## Issue 3: V-space subspace ambiguity in the state model
Category: INTERNAL
Reason: The implementation evidence is already present (TA7a/TA7b, `strongsub` guard, Q13, Q16, Gregory's CREATE LINK evidence about 2.x positions). The fix is a modeling decision among well-understood options.

## Issue 4: COPY source ordering undefined
Category: INTERNAL
Reason: Nelson's transclusion description ("non-native byte-spans are called inclusions or virtual copies") and Gregory's `docopy` evidence both imply a source document. Adding the source document parameter and deriving S's ordering from it follows from existing content.

## Issue 5: CREATE LINK V-space postcondition not formalized
Category: INTERNAL
Reason: Gregory's evidence already specifies the mechanism precisely ("first link goes to 2.1; subsequent links append at the end of the 2.x extent"). Formalizing a `next_link(h, Σ)` function and quantified postconditions follows the INSERT pattern using this existing evidence.

## Issue 6: REARRANGE parameters and precondition underspecified
Category: GREGORY
Reason: The Gregory note mentions `slicecbcpm` and a "move step (phase 2)" but the operation's parameter structure (move? swap? arbitrary permutation?) is not established. The ASN needs to know what the implementation actually supports to decide the right specification level.
Gregory question: What are the parameters to the rearrange operation in udanax-green — does it take a source span and a target position (cut-paste move), two spans to swap, or something more general, and what is the entry-point function signature?

## Issue 7: UF-V target document ambiguous for creation operations
Category: INTERNAL
Reason: The fix is a clarification of existing frame conditions. The J0 proof already parenthetically states `Σ'.v(d) = Σ.v(d)` for CREATE VERSION — it just needs to be promoted to an explicit postcondition. No external evidence required.
