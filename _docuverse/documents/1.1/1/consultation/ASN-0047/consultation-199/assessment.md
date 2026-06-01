# Channel Assignment — ASN-0047 review-199

**Date:** 2026-06-01 02:15

## Issue 1: K.μ~-FIX jumps from per-subspace cardinality equality to set equality without establishing depth preservation
Reason: The mechanical repair (add `#π(v) = #v`, fix the necessity and link-fixity proofs) is internal, but deciding whether depth-changing reorders are legitimate is a semantic question about what "reordering" is meant to be — and what the implementation actually does — so design intent and implementation evidence both bear on whether depth-preservation is the correct constraint.
Nelson question: Is arrangement reordering intended to be a permutation of a document's existing V-positions (preserving their depth and structure), or may it relocate content into V-positions at a new depth?
Gregory question: Does the udanax-green reorder operation permute content among a document's existing V-positions at fixed depth, or can it emit V-positions whose depth differs from the pre-reorder arrangement?

## Issue 2: Reviser-drift — the "caller-checked guard / GlobalUniqueness preserves, does not supply" clarification is restated in four locations
Reason: Purely an editorial consolidation — state the guard-vs-preservation distinction once and cite it elsewhere; derivable from the ASN's own content with no design or implementation input needed.

## Issue 3: J1'★ derivation contains a defensive "what does not close the gap" essay before stating what does
Reason: Purely an editorial trim — keep the record-then-strip example and the single closing sentence, delete the repeated negative framing; no external channel needed.
