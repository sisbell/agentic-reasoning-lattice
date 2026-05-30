# Channel Assignment — ASN-0036 review-194

**Date:** 2026-05-29 23:37

## Issue 1: Duplicated "structural encoding, not a lookup" claim across S7a and the S7 proof
Reason: Pure deduplication — both paragraphs already exist in the ASN; choosing which restatement to drop requires no design intent or implementation evidence, only internal editing.

## Issue 2: S8a is a renamed alias of the domain-restriction axiom
Reason: The equivalence of S8a and the domain-restriction axiom is established within the ASN by T0; collapsing the two labels is a structural bookkeeping fix derivable from the note's own content.

## Issue 3: Implementation-internals grounding for S5 reaches into out-of-scope territory
Reason: The fix is to delete the global-index/code-path sentences; the S5 proof and Nelson quotation already carry the claim independently within the ASN, so the trim is internal and needs no channel.
