# Channel Assignment — ASN-0121 review-14

**Date:** 2026-06-09 02:02

## Issue 1: State model declared as a triple, then reasoned over as the ASN-0047 five-tuple
Reason: The fix is purely internal — the transition vocabulary the ASN already adopts is ASN-0047's, and the correction is to align the state declaration with the five-tuple already cited and reasoned over. No design intent or implementation evidence is needed; it is a consistency repair against an already-referenced foundation ASN.

## Issue 2: No weakest-precondition analysis for any operation that can change the result
Reason: The wp formula is fully determined by FL-DEF and the `lift`/`liftH`/`sat` definitions already present, and the review even supplies the target chain. The derivation follows mechanically from the ASN's own content (and the sibling-ASN wp templates it cites), needing neither Nelson nor Gregory.

## Issue 3: Decidability of the matching predicate is never established
Reason: Decidability of `touch` is an analogue of ASN-0086's CoverageEqualityDecidable, an already-cited foundation result; finiteness follows from L-fin. The lemma is discharged by the same cell-decomposition argument internal to the foundation, with no need for design intent or implementation evidence.

## Issue 4: The request grammar is described in prose but never formally typed
Reason: The ASN's own formalism (`athome(a,H) ≡ home(a) ∈ coverage(H)`) already shows the organizational-prefix restriction is unenforced and vacuous for element-rooted `H`, so the formalism-consistent resolution — type `q ∈ (Endset ∪ {∗})⁴` and demote prefix-rooting to convention — is derivable from the ASN alone.
