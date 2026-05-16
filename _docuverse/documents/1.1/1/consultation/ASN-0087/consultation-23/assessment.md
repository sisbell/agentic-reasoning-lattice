# Revision Categorization — ASN-0063 review-23

**Date:** 2026-03-22 02:53

## Issue 1: S8 derivation chain cites wrong dependencies
Category: INTERNAL
Reason: The correct dependency list for S8 is stated in ASN-0036. The fix is mechanical substitution of the cited dependencies to match the source ASN's derivation chain.

## Issue 2: K.μ⁺_L permits foreign link placement without justification
Category: BOTH
Nelson question: Was link transclusion — placing a link owned by another document into your own document's arrangement, analogous to content transclusion — an intended feature of the design, or should a document's link subspace contain only links it originated?
Gregory question: Does the udanax-green implementation enforce that a document's link subspace contains only links whose origin matches the document, or does it permit placing foreign-origin links in a document's arrangement?

## Issue 3: Contains_C definition omits domain membership
Category: INTERNAL
Reason: The fix is adding `v ∈ dom(M(d))` to the existential quantifier, matching the explicit style of the foundation's Contains definition in ASN-0047. The correction is derivable from the referenced definition.
