# Channel Assignment — ASN-0107 review-18

**Date:** 2026-06-08 11:21

## Issue 1: R2 uses bare `Δnum` where the quantity is necessarily `Δnum_disc`
Reason: Purely a notation fix derivable from the ASN — E3 establishes contraction cannot move the existence count, and the claims table already labels this the discovery count, so `Δnum` must read `Δnum_disc`. No design intent or implementation evidence is at stake.

## Issue 2: A1a re-argues a case its own corollary-of-E3 status already excludes
Reason: A deletion of redundant prose whose redundancy is established by the ASN's own E3 corollary; cutting the ghost-reference/orphan walk requires only internal consistency, no external input.

## Issue 3: D2 extension bullet carries a use-site/exhaustiveness justification
Reason: Removing meta-prose ("Both must be named") and merging the two extension operations into one conclusion is an internal editorial change; the load-bearing claim that extension grows `Qᵢ` is already present and unchanged.

## Issue 4: R1's minimal-contraction split is re-derived wholesale in R6
Reason: A deduplication choice between two passages already in the ASN, resolvable by the document's own R6-subsumes-R1 logic; no design intent or code evidence bears on which copy to keep.
