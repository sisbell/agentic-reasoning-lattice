# Channel Assignment — ASN-0094 review-28

**Date:** 2026-05-20 06:22

## Issue 1: Sh4 and FDD contract interaction at FDD-registered K is underspecified
Reason: The fix is internal. Both contracts are framework-introduced layer disciplines; their interaction is a design choice within this ASN's own contract semantics, with the `C ⊆ C_fd` containment already established as the natural input to the resolution.

## Issue 2: RetractionTargetNotOnChain Case II's home-equality step compresses T4b structure
Reason: The fix is internal. T4b (ASN-0034) is already cited elsewhere in the ASN, and the missing expansion is just an explicit positional-index derivation using axioms already in scope — comparable to the detail level the AllocatedAddressAntichain proof's Steps 3.1/3.2 already exhibit.

## Issue 3: Provenance `to_K`'s exclusion of attribution-only tuples could be explained at the catalog row
Reason: The fix is internal. The semantics of `to₁⁻` returning `⊥` and the `to_K(b)` body excluding `⊥` results are already defined in the Provenance walkthrough; the fix is purely an annotation/documentation improvement at the catalog row.

## Issue 4: Sh4 Case B's qualifier framing is informational but invites confusion
Reason: The fix is internal. The case-decomposition argument (K ≁ R automatic; K ~ R routed to Case D) is already in the ASN; the fix is just rewriting the case heading to reflect the structural restriction the decomposition already enforces.

## Issue 5: AllocatedAddressAntichain Step 3's symmetry claim could be tightened
Reason: The fix is internal. This is a presentation choice between two structurally equivalent formulations of the same proof, with no new mathematical content needed.
