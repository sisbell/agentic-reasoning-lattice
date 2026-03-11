# Revision Categorization — ASN-0029 review-3

**Date:** 2026-03-11 09:32

## Issue 1: D7 uniqueness claim is false
Category: INTERNAL
Reason: The fix (use longest prefix, or define via `fields()`) is already derivable from T4 (HierarchicalParsing) and the `fields()` function, both present in the ASN.

## Issue 2: D12 parameter `a_req` not related to `actor(op)`
Category: INTERNAL
Reason: The ASN establishes the `actor(op)` pattern in D0, D10a, and D15. Adding `a_req = actor(op)` restores internal consistency using conventions already present.

## Issue 3: Frame conditions do not bound Σ'.D from above
Category: INTERNAL
Reason: The ASN's prose makes clear that D0 creates exactly one document, D10a creates none, and D12 creates exactly one. Tightening the frame to `Σ'.D = Σ.D ∪ {d}` (or `= Σ.D`) follows directly from the stated semantics.

## Issue 4: D5(c) introduces undefined concept "designated associates"
Category: INTERNAL
Reason: The inconsistency between D5(c) (associates may access) and D12 (only owner may version private documents) is resolvable editorially: mark associates as deferred design intent and add a reconciling note in D12, both using information already in the ASN.

## Issue 5: D17 span well-formedness gap
Category: INTERNAL
Reason: T12 (SpanWellDefined) already requires `ℓ > 0` and is referenced in the ASN. The fix is adding an explicit precondition citing the existing property.

## Issue 6: D14 parent function undefined for root documents
Category: INTERNAL
Reason: The ASN's prose already notes "at most one immediate structural parent." Making `parent(d)` a partial function is a direct formalization of the stated intent.
