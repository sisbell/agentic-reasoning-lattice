# Channel Assignment — ASN-0051 review-41

**Date:** 2026-05-16 03:26

## Issue 1: NoStaleResolutionState relies on un-enumerated transition inspection
Reason: The fix is purely mechanical enumeration of the 8 elementary transitions' write-targets, each of which is already documented in ASN-0047 (cited in the existing paragraph). The required per-transition lines can be composed from schema knowledge already in scope.

## Issue 2: SV6 sub-lemma — implicit T1 index bound at j ≤ #(s⊕ℓ)
Reason: The fix is a one-sentence citation chain combining ActionPoint codomain (ASN-0034) and TumblerAdd result-length identity (TA0), both already used elsewhere in the SV6 proof. Fully internal.

## Issue 3: SV11 worked example exhibits only mechanism (b) of the strictness biconditional
Reason: The fix is construction of a concrete tumbler scenario where a third span's denotation is disjoint from both block I-extents. This is internal construction work using the existing tumbler/span machinery; no design intent or implementation evidence is at stake.

## Issue 4: SV11 maximal-fragment count proof — the upper bound on fragment-per-term assumed without statement
Reason: The fix is a parenthetical citation of the S0-convexity argument already present in the same section. Purely internal cross-reference.
