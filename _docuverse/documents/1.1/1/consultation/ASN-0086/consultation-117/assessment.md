# Channel Assignment — ASN-0086 review-117

**Date:** 2026-05-31 22:41

## Issue 1: Forward-reference non-circularity justification in R0a-Cor1
Reason: Purely editorial — delete the citation-order disclaimer or reorder R0a-Cor1 before R0a. Both options are internal to the note's structure; no design-intent or implementation evidence is needed.

## Issue 2: Use-site inventory in "Definition — state-local-conforming state"
Reason: Editorial deletion of a consumer-enumeration sentence; the four-way containment and witness already define the set. Fully derivable from the ASN's own content.

## Issue 3: ASN-0040 seed contrast in EmptyInitialLinkStore
Reason: Removing the parenthetical contrast does not alter the assumption `dom(Σ_init.L) = ∅`; the `initmagicktricks` sentence already grounds it. Internal editorial fix.

## Issue 4: `P2`/`P2c` subscript collision across Nullify and wp Case 1
Reason: A label-renaming fix to disambiguate two distinct conditions; no semantic change. Fully internal.
