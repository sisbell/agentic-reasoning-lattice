# Channel Assignment — ASN-0042 review-95

**Date:** 2026-05-30 02:19

## Issue 1: O9 applies T4 field-extraction to `a` without discharging `T4(a)`
Reason: Internal. O17 (AllocatedAddressValidity) is already present in the ASN and supplies `T4(a)` from `a ∈ Σ.B`; O6's proof already demonstrates the exact citation pattern. The fix is inserting the existing internal reference.

## Issue 2: `dom(π)` collides with the foundation's `dom(A)`
Reason: Internal. This is a notation-hygiene decision (rename or justify the overload); the colliding foundation symbol's meaning is already stated in the issue, and no design intent or implementation evidence bears on choosing a symbol.

## Issue 3: Summary overstates the model's axiomatic basis
Reason: Internal. The Properties table already enumerates which results are axioms (O5, O12–O18) versus derived, so the honest restatement is read directly off the ASN's own dependency structure.

## Issue 4: Repeated `docreatenewversion`/`makehint` citation in O10 (anti-bloat)
Reason: Internal. Pure editorial deduplication of an already-established implementation citation; no new evidence is required, only removal of redundant restatements.

## Issue 5: Duplicate-significance paragraphs in OwnershipDomainPermanence (anti-bloat)
Reason: Internal. Collapsing two paragraphs that assert the same content is an editorial merge derivable entirely from the existing text.
