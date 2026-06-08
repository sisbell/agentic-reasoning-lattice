# Channel Assignment — ASN-0102 review-90

**Date:** 2026-06-08 04:14

## Issue 1: P4★ invoked at COPY's pre-state, but P4★ is a composite-boundary property
Reason: The fix is internal — it re-routes the justification through invariants already in scope (P4★ at the composite's initial boundary plus P2 provenance permanence, both from ASN-0047, already cited in the note). No design intent or implementation evidence is needed; the correction is a matter of citing the right invariant at the right state.

## Issue 2: X2's allocation-handle derivation omits the first-emission case
Reason: The fix is internal — K.α's two-case structure is a cited foundation (ASN-0093) and the review itself supplies the first-emission form `[d.0.s_C.1]`. Discharging the "frontier identical" claim for the empty-`{a':origin(a')=d}` case follows from X1 and the already-referenced K.α definition, needing no implementation evidence or design intent.

## Issue 3: Internal redundancy and repeated downstream deferral (anti-bloat)
Reason: Purely editorial deduplication — consolidate the SL-feeds-couplings statement and composite-level deferral into X14 and let the example exhibit the instance. No external channel bears on prose consolidation.
