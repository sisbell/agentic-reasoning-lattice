# Channel Assignment — ASN-0122 review-6

**Date:** 2026-06-13 08:31

## Issue 1: X12 precondition re-derives the content-subspace-clip rationale already established at its definition site
Reason: Pure deduplication — both the X12 precondition and the *State, Instances, and Spec-Sets* paragraph already exist in the ASN, and the fix is to trim the precondition to a crisp statement plus a pointer to the existing derivation. No design-intent or implementation evidence is needed; the required replacement text is already supplied by the ASN's own content.

## Issue 2: the "value-matching over-reports / unreadable as the same part" gloss is delivered twice
Reason: Pure deduplication — both glosses are present in the ASN and the fix is editorial: anchor the over-report claim at one site (X2's discussion, its formal witness) and reference it from the other, preserving each passage's distinct surrounding material. Deciding the anchor and trimming the restatement is derivable from the ASN alone.
