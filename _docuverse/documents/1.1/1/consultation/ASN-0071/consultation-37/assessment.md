# Channel Assignment — ASN-0071 review-37

**Date:** 2026-06-03 08:44

## Issue 1: Rationale prose justifying a precondition rather than stating it
Reason: Pure deletion of motivational prose; the preconditions (`subspace(u) = s_C`, `actionPoint(ℓ) = #u ≥ 2`) are already stated in the vspec definition and consumed by the PC derivation, so the fix is fully internal.

## Issue 2: Implementation-advice meta-prose in guarantee sections
Reason: Pure deletion of implementer-facing rationale; the formulae and their derivations already carry the guarantees, so the fix is internal.

## Issue 3: Forward-reference deferral of the subset claim's gating precondition
Reason: Restructuring only — the `wp-defined` precondition (`d_s ∈ Σ.E_doc`) is already defined in the ASN and merely needs relocation to the `iaddrs_one` definition; internal fix.

## Issue 4: Verification bullets restate the already-computed trace
Reason: Editorial reduction of duplicated bullets to one-line labels binding properties to trace lines; the trace already establishes each property, so the fix is internal.
