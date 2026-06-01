# Channel Assignment — ASN-0086 review-128

**Date:** 2026-06-01 00:24

## Issue 1: The R6a-vs-R6b distinction is stated three times
Reason: Pure editorial deduplication — keep the body parenthetical, delete the proof aside and table clause. The distinction is derivable from the two formulas already present in the ASN; no design intent or implementation evidence needed.

## Issue 2: The `a ∈ A_rel^Σ` restriction rationale is repeated across three properties
Reason: Editorial consolidation — state the `℘(T)` codomain rationale once at the `nullified` definition and have R6a/R6b cite it. The justification is already fully present in the ASN; relocating it requires no external channel.

## Issue 3: The `→` definition inlines ASN-0093 emission forms already fixed in foundation
Reason: The fix only deletes restated ASN-0093 emission arithmetic, replacing it with a by-reference summary; the note already cites ASN-0093 for these contracts and re-derives the forms where needed (R0, `a_emit`). Removing a foundation restatement is internal.

## Issue 4: WP Case 2 builds out a direct-K.λ-caller regime analysis the note's own operation set never reaches
Reason: The choice between scoping to the relational layer's two-conjunct form versus retaining a compressed direct-caller contrast is an authorial scoping decision; both options' content is already established within the ASN. No design intent or implementation evidence is required to trim or relabel existing prose.
