# Channel Assignment — ASN-0047 review-157

**Date:** 2026-05-31 18:37

## Issue 1: J1 cited in extended-state Fork discharge where J1★ governs
Reason: Internal citation drift — the ASN already declares J1 superseded by J1★ in the extended state and the fork's own discharge paragraph uses J1★. The fix is a uniform relabeling derivable from the ASN's own supersession statements.

## Issue 2: Link V-position depth is pinned per-document but content V-position depth is not, with no stated rationale
Reason: Resolving whether content depth may vary across re-populations (while link depth is fixed) requires the designer's intent on whether text V-position depth is a fixed per-document property, and implementation evidence on whether udanax-green fixes or re-derives text depth after clearance — neither is settled by the ASN's own content.
Nelson question: Is a document's text (content-subspace) V-position depth a fixed per-document property determined at first insertion, or may it legitimately differ each time the text is fully cleared and re-populated — and if links are fixed but text is not, what design distinction justifies the asymmetry?
Gregory question: After a document's text is fully deleted and new text is inserted, does udanax-green re-establish the same V-position depth for the text subspace, or can the re-populated text occupy a different depth than before?

## Issue 3: Duplicated frame-conjunct justification prose (anti-bloat)
Reason: Pure editorial deduplication — the convention about extending ASN-0093's frame with `E' = E ∧ R' = R` can be stated once and the per-transition repetition dropped, all derivable from the ASN.

## Issue 4: Definition-slot justification of the SD/L14 restatement (anti-bloat)
Reason: Editorial — collapsing the L14 restatement to a single citation of ASN-0093 SD and removing the premise re-enumeration is internal to the ASN's existing structure.

## Issue 5: Repeated forward-pointer accretion for K.λ and K.μ⁺_L (anti-bloat)
Reason: Editorial — reducing repeated forward references to a single pointer each is a mechanical cleanup derivable from the ASN alone.
