# Channel Assignment — ASN-0130 review-31

**Date:** 2026-06-13 07:45

## Issue 1: Worked composition reuses occupied/reserved symbols
Reason: Pure notational hygiene — choosing fresh symbols (`chkW` for the capture-example definition, `Done`/`L_Done` for the marker class) so they don't collide with the lease class `H` and the `M_K` members operator. Both the collisions and the in-use symbols are entirely visible in the note's own text; no design intent or implementation evidence bears on which letters to pick.

## Issue 2: Forward-reference and editorializing meta-prose (anti-bloat)
Reason: Pure prose-trimming — the substance of each claim (what prefix-freeness is, that the domain is syntactic, how permanence divides across conjuncts) is already stated; the fix only deletes forward-gesture and self-praise fragments. Nothing about design intent or the implementation is needed to cut meta-commentary.
