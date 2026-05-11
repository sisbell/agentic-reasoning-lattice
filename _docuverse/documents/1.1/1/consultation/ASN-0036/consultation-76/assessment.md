# Channel Assignment — ASN-0036 review-76

**Date:** 2026-05-11 00:26

## Issue 1: Citation imprecision in S8 cross-subspace uniqueness proof
Reason: The fix is purely internal — replace TA5(a)/(b) citations (which are about `inc(t, k)`) with the already-available TS4 (ShiftStrictIncrease) and OrdinalShift component preservation from ASN-0034. The within-subspace portion of the same proof already uses the correct citations.

## Issue 2: Subspace alignment between V-positions and I-addresses is not formalized
Reason: Deciding whether to add a SubspaceAlignment invariant or defer requires both design intent (was V/I subspace alignment architecturally load-bearing or coincidental?) and implementation evidence (does udanax-green enforce alignment, or could a text V-position map to a link I-address?).
Nelson question: Did the strand-level design intend a strict invariant that a V-position's subspace identifier must equal the I-address subspace identifier of the content it maps to, or was the V-side/I-side subspace correspondence treated as an operation-layer concern outside the two-stream foundation?
Gregory question: Does the udanax-green implementation ever permit (or actively prevent) an arrangement entry whose V-position lies in the text subspace from mapping to an I-address allocated in the link subspace (or vice versa), and is there code that enforces or assumes V/I subspace alignment?

## Issue 3: "v > 0" notation overloading and redundant conjuncts
Reason: The fix is purely internal — replace the overloaded `v > 0` with the canonical predicates `Pos(·)` and `Zero(·)` already defined in ASN-0034 (TA-Pos, TA6, TA-PosDom), and remove redundant conjuncts that follow from `zeros(v) = 0` together with T0's ℕ-valued carrier.
