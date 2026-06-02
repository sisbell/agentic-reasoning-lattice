# Channel Assignment — ASN-0047 review-284

**Date:** 2026-06-01 20:16

## Issue 1: J4 introduction duplicates Definition (Fork) and defers to it
Reason: Pure editorial deduplication — removing restated allocation/operand-tracking content from the J4 intro and pointing to Definition (Fork). No design intent or implementation evidence is at stake; both texts already exist in the ASN.

## Issue 2: The full-clearance "links-retained-pointwise" fact is re-derived in at least three places
Reason: Internal refactor — extract one mechanical fact (`M'(d)|_{dom_L} = M(d)|_{dom_L}`) into a named one-line lemma and cite it at the three sites. The fact is already proved from the ASN's own transition definitions; nothing external is needed.

## Issue 3: Forward-pointer accretion to "Decomposition of K.μ~"
Reason: Internal restructuring — label the two downstream results (the K.μ⁻+K.μ⁺ realisation establishing S3★(Σ') and K.μ~ range-invariance) and cite the labels instead of the section. Both results are already derived within the ASN.

## Issue 4: D-SEQ★ reusability meta-justification and L14a redundant prose
Reason: Pure deletion/consolidation of prose already present in the ASN — drop the D-SEQ★ reusability sentence and collapse the duplicated L14a inapplicability statement. No channel input required.
