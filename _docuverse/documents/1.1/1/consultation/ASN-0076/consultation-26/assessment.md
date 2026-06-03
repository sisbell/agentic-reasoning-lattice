# Channel Assignment — ASN-0076 review-26

**Date:** 2026-06-03 08:25

## Issue 1: Citation of a nonexistent foundation claim "S9"
Reason: This is a citation-accuracy fix against a sibling foundation ASN (ASN-0036), whose claim set is inspectable within the lattice; no design-intent or implementation evidence bears on whether S9 exists or what the intended label was.

## Issue 2: Sub-case (a) freshness is asserted at the wrong state
Reason: A pure proof-rigor gap — derive `ℓ_new ∉ dom(Σ.C) ∪ dom(Σ.L)` at `Σ` from the sub-case-(a) emptiness condition, mirroring sub-case (b)'s existing argument; all inputs are foundation invariants already cited in the ASN.

## Issue 3: Incorrect description of coverage as "having no extensions"
Reason: Coverage is defined combinatorially over `T` in ASN-0098 (already cited); correcting the parenthetical is internal to the ASN's own framework and needs no external authority.

## Issue 4: Foundation coupling claims cited under altered names
Reason: Mechanical alignment of descriptive names to ASN-0047's canonical names (AllocationPlacementCoupling, ExtensionRecordsProvenance, ProvenanceRequiresExtension); the foundation text is the sole source.
