# Channel Assignment — ASN-0102 review-23

**Date:** 2026-06-05 07:54

## Issue 1: Definition-section rationale explains why decisions matter rather than stating the contract
Reason: Pure editorial removal of a notation parenthetical and a rationale sentence; X10/X15 already derive atomicity and pre-state resolution from SequentialTransitionAxiom within the ASN. No design intent or implementation evidence needed.

## Issue 2: Provenance-effect rationale prose
Reason: Deletion of a justification sentence whose obligation is discharged by X14's J1★ within the same note. Fully internal.

## Issue 3: Repeated deferral to X8
Reason: Replace a forward-deferral with the plain `k = Σ kᵢ` fact, which is already stated and proven (C1a, M12 per reference) in the ASN. Internal.

## Issue 4: X14 invariant inventory padded with relocated per-invariant callouts
Reason: Collapsing per-invariant callouts into grouped frame-discharge sentences using facts already present (`Σ'.L = Σ.L`, `Σ'.E = Σ.E`, X1, X6). No external channel required.
