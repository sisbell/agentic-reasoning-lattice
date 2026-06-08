# Channel Assignment — ASN-0102 review-38

**Date:** 2026-06-07 22:54

## Issue 1: Citation of a non-existent sub-clause `OrdShiftHom (c)`
Reason: Pure citation correction — the correct postcondition (`#shift(v,n) = #v`) lives in OrdinalShift (ASN-0034), already a dependency; no design intent or implementation evidence is involved.

## Issue 2: OrdShiftHom over-cited for intermediate-component fixity
Reason: Attribution fix derivable from the cited foundations themselves — OrdinalShift (ASN-0034) gives component-wise behavior, OrdShiftHom only subspace/S8a preservation. Internal.

## Issue 3: Faulty justification in X8 — "maximally-merged ⟹ pairwise non-I-adjacent"
Reason: The repair is a logical re-derivation from M7/M12 (ASN-0058) and D-SEQ already in scope; the conclusion stands, only the reasoning needs correcting. Internal.

## Issue 4: Coupling-invariant names diverge from the foundation
Reason: Naming alignment with ASN-0047's canonical labels (AllocationPlacementCoupling, ExtensionRecordsProvenance); mechanical substitution, no channel needed. Internal.

## Issue 5: Provenance pair well-typedness only half-justified
Reason: The missing `Element(a_j+i)` factor follows from C1 (ASN-0058) via S7b (ASN-0036), both already cited; only the explicit step needs stating. Internal.

## Issue 6 (anti-bloat): Justificatory K.μ⁺ contrast in the Definition
Reason: Editorial trim of design-rationale prose; the operative effect clause already carries the content. Internal.
