# Channel Assignment — ASN-0047 review-163

**Date:** 2026-05-31 19:46

## Issue 1: FrontierEquivalence content restated three times
Reason: Internal editorial deduplication — the lemma is already proved in the ASN; fix is to cite it by name at each use site and delete the prose re-derivations. No design intent or implementation evidence needed.

## Issue 2: K.δ freshness discharge is duplicated across three sections with circular deferral
Reason: Internal structural fix — the `e ∉ E` discharge is fully present in the ASN; the task is to keep exactly one locus and replace the others with a pointer. Derivable from the ASN alone.

## Issue 3: Sub-case A2 discharged twice in adjacent paragraphs
Reason: Internal deduplication — both paragraphs establish the same membership via the same T10a.6 appeal already in the ASN; collapse to one. No channels needed.

## Issue 4: LinkVPositionDepthAxiom is redundant given S8-depth + S8a + operational first-insertion
Reason: The redundancy claim is a formal comparison against S8a, S8-depth, and K.μ⁺'s own `ValidFirstInsertionPosition` treatment of content — all present in the ASN — so whether the axiom adds anything is decidable internally. The content/link asymmetry is resolved by mirroring the existing operational treatment.

## Issue 5: Properties-Introduced/Inherited entries carry use-site inventory and rationale instead of statement
Reason: Internal editorial fix — reduce the table entry to label + statement + foundation source, moving provenance/consumer prose out of the index. No channels needed.

## Issue 6: P7a cross-layer derivation cites superseded J1 rather than J1★
Reason: Internal consistency fix — the ASN already defines J1★ as superseding J1 and supplies the J0 + J1★ + S3★ + L14 + S3★-aux discharge in Class (b); align the standalone derivation to cite those. Derivable from the ASN alone.
