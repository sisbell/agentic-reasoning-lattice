# Channel Assignment — ASN-0040 review-53

**Date:** 2026-05-28 21:55

## Issue 1: hwm precondition not updated to the B6 scoping
Reason: Internal fix — the required change mirrors the B6 scoping already present on B1 and B2 within this ASN; no design intent or implementation evidence is needed.

## Issue 2: B1 statement carries a downstream-consumer inventory
Reason: Internal fix — deleting the consumer enumeration is a pure editing decision; the invariant's scope clause already carries the meaning.

## Issue 3: B1 proof closes with defensive scope justification
Reason: Internal fix — B0a already forces the case split to B6-valid pairs, so the paragraph can be removed using only the ASN's own structure.

## Issue 4: Bop body defers repeatedly to the Formal Contract
Reason: Internal fix — consolidating the frame and B4 statements is a presentation choice fully determined by content already in the ASN.

## Issue 5: B₀ conf. maps its conditions to downstream Base lines
Reason: Internal fix — dropping the mapping sentence is editorial; each downstream Base line already cites B₀ conf., as visible within the ASN.

## Issue 6: Foundation name cited inconsistently for T0(a)
Reason: Gregory holds the udanax-green/knowledge-base synthesis, but the foundation name `UnboundedComponentValues` is an ASN-0034 naming convention; the review already states the correct spelling, so the fix is internal.
