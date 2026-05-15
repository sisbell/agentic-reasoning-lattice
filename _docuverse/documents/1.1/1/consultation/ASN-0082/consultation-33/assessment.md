# Channel Assignment — ASN-0082 review-33

**Date:** 2026-05-15 12:09

## Issue 1: Commutativity of ℕ addition invoked without derivation
Reason: The fix is a formal-proof issue internal to the ASN and its foundation (ASN-0034). The three remediation options (derive from NAT-wellorder + induction, record as foundation extension, or restructure the postcondition) are all derivable from the existing formal apparatus; no design intent or implementation evidence is needed.

## Issue 2: Same commutativity dependency in D-S(a)
Reason: Same remediation as Issue 1 — a proof-structure problem internal to the formal apparatus. Whether we derive commutativity, extend the foundation, or restructure to avoid the swap, the choice is governed by the existing NAT-* axioms and proof obligations, not by design or implementation facts.

## Issue 3: I3-S(b) and D-S(b) route through commutativity unnecessarily
Reason: The reviewer has identified the direct route (NAT-sub left-telescoping `(n + m) − n = m`) using only foundation axioms already cited. Pure proof restructuring within the ASN's existing formal scope.

## Issue 4: TS4 citation name does not match foundation
Reason: A naming/citation correction. The reviewer has supplied the foundation's actual name (ShiftStrictIncrease); the fix is a mechanical replacement throughout the ASN.

## Issue 5: D-MIN-post step is implicit
Reason: The reviewer has supplied the missing inference verbatim ("L ≠ ∅ supplies some v ∈ V_1(d) with v < p, so min(V_1(d)) ≤ v < p; hence min(V_1(d)) ∈ L."). Insertion of an already-derived step.

## Issue 6: Worked examples for I3 cover only S = 1
Reason: The reviewer offers two derivable options: add a constructed example exercising S = 2 against a sparse pre-state, or add explicit prose noting that the lemmas establish generality. Both are internal — the ASN's existing cross-subspace section and historical notes (link-subspace mutation uses tombstoning, deferred) already supply the framing needed for either route.
