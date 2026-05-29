# Channel Assignment — ASN-0042 review-67

**Date:** 2026-05-29 06:10

## Issue 1: O14 clause-numbering is internally contradictory
Reason: Pure internal renumbering — the canonical clause list (O1a→3, O1b→4, T4→5, non-nesting→6) is already stated in the same section; the fix aligns the multi-node references to it. No design intent or implementation evidence is at stake.

## Issue 2: Duplicated "historical vs structural reading" prose
Reason: Internal consolidation — both paragraphs are present in the ASN and say the same thing; the fix is to state the duality once at the definition and cite it in O8. No channel needed.

## Issue 3: Axiom prose explains *why the axiom is needed* rather than *what it says*
Reason: Internal editorial deletion of meta-classification taxonomy; the content of O1a/O1b (the `pfx` signature constraints) is fully present and unchanged. No channel needed.

## Issue 4: Use-site inventories on lemmas and table entries
Reason: Internal editorial removal of downstream-consumer lists; the lemma statements and proofs stand on their own. No channel needed.

## Issue 5: Verification-convention and notation essays in structural slots
Reason: Internal compression of reading-convention prose; the conventions themselves are retained inline at first use. No channel needed.

## Issue 6: Path-independence of `delegated_Σ*` asserted without derivation
Reason: Internal mathematical gap — the fix is either to prove introducing-event invariance across witnessing paths (using O15's at-most-one-new-principal and O12's no-re-introduction, both already in the ASN) or to redefine the closure sequence-independently over `Π_Σ`. All material is present in the ASN; no design or implementation input required.

## Issue 7: Self-referential table prose
Reason: Internal deletion of a sentence describing the property's own table row. No channel needed.
