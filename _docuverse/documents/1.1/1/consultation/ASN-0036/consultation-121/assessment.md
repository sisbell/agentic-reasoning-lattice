# Channel Assignment — ASN-0036 review-121

**Date:** 2026-05-28 21:46

## Issue 1: Dangling forward reference to "#runs(d) below"
Reason: Pure editorial fix — delete the forward pointer and `#runs(d)` notation, or replace it with the actual one-sentence statement already present below the proof. No design intent or implementation evidence is required.

## Issue 2: S8 corollary is conditioned on a run the theorem does not construct
Reason: The structural-preservation fact is already established by ShiftPreservation applied pointwise to each `aⱼ ∈ ran(M(d)) ⊆ dom(Σ.C)`, which the ASN proves. Restating it unconditionally is derivable from the ASN's own lemma; no channel needed.

## Issue 3: Repeated deferral to the same operations-layer location
Reason: Consolidating three deferrals into one statement and removing an intra-contract cross-reference is internal editorial work derivable from the ASN's existing structure.

## Issue 4: Verbatim-duplicated actionPoint-bound parenthetical
Reason: Removing a word-for-word duplicate and letting the second contract inherit the precondition silently is a purely mechanical edit internal to the ASN.

## Issue 5: S7c Consequence (a) "Derivation" is trivial filler
Reason: Dropping a vacuous derivation block that merely restates the axiom `#E(a) ≥ 2` is internal; the axiom already carries the content.

## Issue 6: ValidInsertionPosition structural postconditions asserted, not derived
Reason: The distinctness step is derivable from facts already cited in the ASN — T3 (CanonicalRepresentation) on distinct last components `1+j`, plus shift strict monotonicity (TS4). Adding the one-line derivation requires no external input.
