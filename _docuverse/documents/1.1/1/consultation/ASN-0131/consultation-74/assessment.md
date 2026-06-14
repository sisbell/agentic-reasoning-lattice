# Channel Assignment — ASN-0131 review-74

**Date:** 2026-06-14 12:16

## Issue 1: ASN-0082 insert/delete machinery is cited and then declared irrelevant
Reason: Neither channel. This is a pure compression cut — the note itself already certifies the depth-asymmetry, interior-span-delete caveat, and I3-V intermediate don't bear on RE's stability ("not a scope on RE's stability"), and the load-bearing M-only fact and conservative-lift assumption are already present in the text. Removing the self-certified digression requires no design intent or implementation evidence.

## Issue 2: The addressability section re-narrates ASN-0086's provenance and over-justifies the import
Reason: Neither channel. The imported facts (unit-depth to-set on `L_Θ`, flat antichain R0a, single-tuple scope R-Scope) and the reachability-bridge inclusion are already stated and cited to ASN-0086 in the note; the fix is to keep the bare citations and cut the re-narration of ASN-0086's induction and the use-site justifications — an internal editorial reduction needing no external evidence.

## Issue 3: The intersection characterization is stated twice in consecutive sentences
Reason: Neither channel. Two consecutive sentences assert the same necessary-and-sufficient characterisation already proved in the note; merging them into one is purely internal deduplication, derivable from the ASN's own content.
