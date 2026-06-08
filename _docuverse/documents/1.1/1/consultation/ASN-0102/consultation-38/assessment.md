# Channel Assignment — ASN-0102 review-38

**Date:** 2026-06-07 22:55

## Issue 1: Citation of a non-existent sub-clause `OrdShiftHom (c)`
Reason: Pure citation correction. The review already identifies the correct source (OrdinalShift, ASN-0034) for depth preservation; fixable from the foundation references the ASN already cites, with no design-intent or implementation evidence needed.

## Issue 2: OrdShiftHom over-cited for intermediate-component fixity
Reason: Same class of citation fix — the "increments only the last component" claim is the stated content of OrdinalShift (ASN-0034). Internal correction derivable from the foundation; no channel needed.

## Issue 3: Faulty justification in X8 — "maximally-merged ⟹ pairwise non-I-adjacent"
Reason: A proof-reasoning fix internal to the ASN. The merge condition M7 and MaximallyMerged (M12) from ASN-0058 are already in scope, and the review supplies the correct derivation (direct, or via D-SEQ V-contiguity); no external channel required.

## Issue 4: Coupling-invariant names diverge from the foundation
Reason: Naming alignment against ASN-0047's canonical labels (AllocationPlacementCoupling, ExtensionRecordsProvenance). Derivable from the foundation document itself; no design or implementation question.

## Issue 5: Provenance pair well-typedness only half-justified
Reason: Internal completeness fix — `Element(a_j+i)` follows from C1 (ASN-0058) plus S7b, both already cited in the ASN. The review states the exact derivation; no channel needed.

## Issue 6: Justificatory K.μ⁺ contrast in the Definition
Reason: Purely editorial trim of design-rationale prose; the operative effect is already stated in the effect clause. No external input required.
