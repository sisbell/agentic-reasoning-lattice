# Channel Assignment — ASN-0043 review-46

**Date:** 2026-05-13 08:48

## Issue 1: T4-validity citation chain is unsound
Reason: Internal proof-citation fix using only ASN-0034 material (L1c, T10a, T10a.4) and the existing ASN-0036 framework — no external evidence needed.

## Issue 2: L0's T7 application omits the T4-validity precondition
Reason: Pure citation discharge using ASN-0034's T10a.4 for links and ASN-0036's existing framework for content addresses — internal to the formal stack.

## Issue 3: L9 proof does not establish T4-validity of ghost g
Reason: Constructive proof obligation using T0(a) plus T4 format constraints already in ASN-0034; the witness can be built from carrier axioms without design or implementation input.

## Issue 4: L6 SlotDistinction is stated only for the standard triple
Reason: Generalization is a formalization choice; the ASN already cites Nelson's N-endset intent and L3 already admits N ≥ 2 — the fix is a syntactic lift of the existing statement.

## Issue 5: L8 .type notation is undefined for arity-2 links
Reason: Resolving whether arity-2 links are admissible (untyped connections) requires both design intent (does Nelson admit truly untyped links?) and implementation evidence (does udanax-green actually instantiate 2-endset links, or is the conditional third always populated?).
Nelson question: Does the Xanadu design admit links of arity 2 with no type endset, or must every link carry a type endset (with arity-2 being merely an internal storage form)?
Gregory question: Does `docreatelink` (or any other code path) ever produce a link with only two endsets stored, or is the third endset always populated even when the "conditional" branch is taken?

## Issue 6: L9 proof assumes a document prefix d' exists without justification
Reason: Constructive existence proof from ASN-0034's carrier axioms (T0(b), T4 format) — internal to the formal framework.

## Issue 7: L1b justification conflates depth-1 and shift-action-point arguments
Reason: Cleanup rests on TA5 sibling-allocation semantics in ASN-0034; the shift-mechanics digression should be excised, requiring no external input.

## Issue 8: L11b verification cites L11a circularly
Reason: Pure phrasing fix — cite GlobalUniqueness directly rather than routing through L11a; no external evidence needed.
