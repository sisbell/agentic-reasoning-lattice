# Channel Assignment — ASN-0086 review-235

**Date:** 2026-06-01 20:28

## Issue 1: The Nullify *definition* slot contains a full two-branch correctness proof, duplicated in wp Case 1
Reason: Purely structural relocation — the self-emit correctness argument already lives in R-Scope and wp Case 1 within this ASN, so reducing the Definition slot to operation/P0/effect and citing those results is derivable from the note's own content. No design intent or implementation evidence is at stake.

## Issue 2: Forward-deferral accretion around emission/home machinery
Reason: Pure prose cleanup — deleting document-ordering narration and collapsing repeated re-explanations of the L3-conformance check requires only the ASN's existing text. No external channel bears on whether to drop narration sentences.
