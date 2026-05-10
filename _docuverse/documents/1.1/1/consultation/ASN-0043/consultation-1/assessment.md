# Revision Categorization — ASN-0043 review-1

**Date:** 2026-03-16 21:32

## Issue 1: Link value immutability is unaddressed
Category: BOTH
Reason: Whether link endsets are immutable after creation is a design intent question (Nelson) and requires checking whether any code path modifies a link's endsets post-creation (Gregory).
Nelson question: After a link is created via MAKELINK, can its endsets (from, to, type) be modified, or is the link value permanently fixed like content under S0?
Gregory question: Does the udanax-green implementation provide any operation that modifies a link's endsets after creation, or are link values write-once like content bytes?

## Issue 2: L4 asserts what the Open Questions leave unsettled
Category: INTERNAL
Reason: The contradiction is entirely between sections of the same ASN — properties assert definitive answers while Open Questions treat the same matters as unresolved. The fix is reconciliation, not new evidence.

## Issue 3: Coverage derivation from L5 is a non-sequitur
Category: INTERNAL
Reason: The error is a logical non-sequitur in the derivation chain — L5 (ordering irrelevance) does not entail coverage-level identity. The fix requires choosing an identity criterion and correcting the implication, all from definitions already present in the ASN.

## Issue 4: L10 has no formal statement
Category: INTERNAL
Reason: The formalization follows directly from T5 (ContiguousSubtrees) and T6 (ContainmentDecidable) already defined in ASN-0034. The worked example with MARGIN/FOOTNOTE addresses already contains the substance; it just needs quantified form.

## Issue 5: L14 exhaustiveness uses undefined "all stored addresses"
Category: INTERNAL
Reason: The distinction between entity stores (Σ.C, Σ.L) and arrangement mappings (Σ.M) is already conceptually present in the ASN. The fix is to define the term precisely using existing state components, not to gather new evidence.

## Issue 6: Non-transclusion claim is asserted without derivation
Category: INTERNAL
Reason: The review itself supplies the two-step derivation (S3 from ASN-0036 requires arrangement targets in dom(Σ.C); L0 establishes dom(Σ.L) ∩ dom(Σ.C) = ∅). Both premises are already stated; the fix is writing out the short proof.
