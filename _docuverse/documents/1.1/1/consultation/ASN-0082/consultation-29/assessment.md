# Channel Assignment — ASN-0082 review-29

**Date:** 2026-05-15 10:38

## Issue 1: Post-I3 contiguity-violation discussion conflates text and link subspaces
Reason: Distinguishing the S=1 case ("violates D-CTG/D-MIN/D-SEQ") from S≠1 ("no foundation contiguity invariant applies") is derivable from ASN-0036's frame note already cited. But the "complete sub-operation requiring only content placement" framing for S≠1 asserts that INSERT-on-link exists in the design — that scope question needs Nelson.
Nelson question: Does Xanadu's design define INSERT for the link subspace (V_2), or is INSERT specified only for the text subspace by analogy with DELETEVSPAN's "vspan" prefix?

## Issue 2: wp analysis of I3-S2 leaves vacate/positive overlap unworked
Reason: I3-V's exclusion clause `v ∉ {shift(u, n) : ...}` is already stated and the discharge mechanism is local to the ASN's own assignment-region structure. The fix is to add a seventh wp case in the same pattern as the existing six — pure proof-bookkeeping derivable from the ASN.

## Issue 3: D-SEP(b) proof relies on containment without citing it
Reason: The containment precondition is already in the contract and the X-form derivation already uses it; the fix is to surface the dependency at the D-CTG application step where [1, p₂ + c − 1] ∈ V_1(d) is needed. Pure proof-presentation, internal to the ASN.

## Issue 4: Contraction lacks a sub-operation/full-operation framing
Reason: The Scope paragraph must state whether contraction is the *complete* DELETE or a sub-operation with future phases. S0/content immutability and D-I cover the no-content-removal half internally, but whether DELETE has additional phases (link backref updates, version-state changes, etc.) beyond the V-arrangement modification is a design-scope question for Nelson.
Nelson question: In Xanadu's design, does DELETE (DELETEVSPAN) consist solely of the V-arrangement contraction, or are there additional phases — link backref updates, version-state changes, allocation bookkeeping — that compose with the arrangement transformation?
