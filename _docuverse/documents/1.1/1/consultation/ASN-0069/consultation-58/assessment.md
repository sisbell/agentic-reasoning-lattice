# Channel Assignment — ASN-0069 review-58

**Date:** 2026-06-02 15:36

## Issue 1: Foundation claims cited under incorrect names
Reason: Pure naming correction against ASN-0047's actual claim names, which the review already supplies (AllocationPlacementCoupling, ExtensionRecordsProvenance, ProvenanceRequiresExtension, ProvenanceBounds). No design intent or implementation evidence is in question — the fix is a mechanical substitution internal to the ASN.

## Issue 2: "Chain of custody is reconstructable" contradicts V9a
Reason: Internal consistency fix — the prose overstates what V9a already pins down. The corrected claim (fork-tree lineage via prefixes and content origin recoverable, but acquisition/transclusion path not) is derivable directly from V9a and §"Why I-Address Identity Suffices" in the ASN itself.
