# Revision Categorization — ASN-0001 review-10

**Date:** 2026-03-01 19:02

## Issue 1: TA7a verification for ⊖ rests on a false claim about the divergence point
Category: GREGORY
Reason: The fix requires knowing what operands are actually passed to `strongsub` during V-space editing shifts — whether they are full tumblers or element-relative positions — which determines where the divergence point falls and whether the current proof structure is salvageable.
Gregory question: When DELETE shifts V-space positions backward, what are the actual operands passed to `strongsub` — full tumblers with the document prefix, or element-relative positions within a subspace context?

## Issue 2: V-space position representation is ambiguous
Category: GREGORY
Reason: The ASN presents conflicting representations (full tumblers vs simple counters) and the implementation evidence would definitively show how V-positions are stored and manipulated in the enfilade's V-dimension.
Gregory question: In the 2D enfilade's V-dimension, are V-space displacements and positions represented as full tumblers (including document prefix and subspace identifier) or as element-local values relative to a document/subspace context?

## Issue 3: TA7a verification for ⊖ self-contradicts
Category: INTERNAL
Reason: The contradiction — "the subspace identifier is zeroed" followed by "the subspace identifier is preserved" — is a visible logical error in the ASN's own text; deleting the incorrect argument requires no external evidence. The replacement proof follows from resolving Issues 1 and 2.
