# Channel Assignment — ASN-0036 review-86

**Date:** 2026-05-11 02:59

## Issue 1: OrdShiftHom omits subspace preservation as an explicit postcondition
Reason: The fix is internal — add postcondition (c) `subspace(shift(v, n)) = subspace(v)` derived from OrdAddHom (b) instantiated at `w = δ(n, m)`. OrdAddHom already supplies the subspace-preservation postcondition; the corollary just needs to transfer it.

## Issue 2: OrdAddHom and OrdAddS8a case analyses have unacknowledged empty branches at k = 2 and k = m
Reason: The fix is internal — acknowledge boundary regimes explicitly. TumblerAdd's three-region formula and the precondition `w₁ = 0` (forcing `k ≥ 2`) together with `actionPoint(w) ≤ m` already determine the boundary behavior; the proof needs only added prose, not new evidence.

## Issue 3: "Beyond position m" wording in the within-subspace incompatibility lemma misrepresents δ(1, m)'s structure
Reason: The fix is internal — a wording change. OrdinalDisplacement (ASN-0034) defines `δ(1, m)` to have length exactly `m`, and TumblerAdd is component-wise; reword to reference component-wise addition rather than nonexistent positions.
