# Channel Assignment — ASN-0094 review-22

**Date:** 2026-05-20 03:40

## Issue 1: Forward reference in EffectiveWpSimplification
Reason: Pure document reorganization — moving the corollary after Sh1/Sh3 proofs, or adding a dependency diagram. The acyclic dependency is already established in the ASN's own content; the fix is structural ordering.

## Issue 2: Sh-conf section is overloaded
Reason: Section splitting is a presentation-only refactor. All the content already exists in the ASN; no design intent or implementation evidence is needed to decide where section boundaries belong.

## Issue 3: Catalog row naming mixes structural and semantic conventions
Reason: Naming-policy decision the author can make from the ASN's own catalog. Either committing to structural names throughout or documenting the mixed-convention policy is an authorial choice not contingent on design intent or implementation evidence.

## Issue 4: SharedDepthOneAllocator lemma's role in ASN-0094 is unclear
Reason: Verifying whether the lemma is consumed requires searching ASN-0094's own proof sites; the reviewer already did this search and found no use. The fix (cite or mark as contextual) is internal to the ASN.

## Issue 5: Sh5(b) discipline relies on per-row hand-checking
Reason: META-status enforceability choice the author can make from the framework's own structure. Either acknowledging manual review as the cost of META status or introducing a derivation recipe is a design-presentation decision not requiring external input.
