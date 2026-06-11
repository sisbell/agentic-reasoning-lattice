# Channel Assignment — ASN-0121 review-31

**Date:** 2026-06-11 14:10

## Issue 1: Membership inferred from `sat` alone, dropping the addressability conjunct
Reason: The fix is internal — FL-DEF, the `R_min`/`R_max` forcing argument, and Trace 7(a) already establish exactly why the addressability conjunct is required; the revision just adds the missing hypothesis to the witness and the word "addressable" to the FL-CUR gloss.

## Issue 2: FL-WP case (a)'s `L_R^{Σ'} = L_R^Σ` step omits the value-preservation premise
Reason: Internal citation-discipline fix — L12 is already invoked for the identical step in case (c) ("every prior tuple persists by L12"), so the revision copies an existing, correctly-used premise into case (a)'s two occurrences.

## Issue 3: FL-WP case labels out of presentation order, with a dangling forward reference
Reason: Purely editorial renumbering and cross-reference repair; no semantic content changes, so neither design intent nor implementation evidence bears on it.

## Issue 4: Duplicated clarifications restated across sections
Reason: Anti-bloat deduplication with canonical sites already designated by the review; every restatement is verbatim-redundant with content retained elsewhere in the ASN, so the fix is derivable from the ASN alone.

## Issue 5: Defensive meta-prose in structural slots
Reason: Internal anti-bloat edit — the one substantive fact to preserve (the wide element-rooted span covering a document-level tumbler, with its `p ⊕ ℓ` example) is already fully worked in the ASN and only needs relocating; everything else is deletion of meta-commentary.
