# Channel Assignment — ASN-0086 review-161

**Date:** 2026-06-01 05:46

## Issue 1: The unit-depth retraction discipline is claimed equivalent to "reached by relational-layer operations," but Nullify can target non-A_rel addresses
Reason: Internal reconciliation. Option (b) is mathematically blocked — a document-level ghost target `b` (zeros=2) can satisfy `b ≼ a` for a future link `a` homed under it, so `b ⋠ a` is unestablishable — forcing option (a), a layer-commitment restriction on Nullify targets, which the ASN can state from its own definitions of Nullify, R0a, and the discipline.

## Issue 2: Defensive meta-prose justifying the `↝` definition's existence
Reason: Internal prose deletion. The definitional content ("`↝` is the union of `→` with any higher-layer transition") is already present; removing the forward-referencing justification requires no external input.

## Issue 3: Use-site inventory plus defensive justification in the state-local-conforming definition
Reason: Internal prose reduction. Dropping the R0/R5/Emit_K enumeration and keeping the definitional statement plus a single no-reachability clause is fully specified by the review and derivable from the ASN's own text.
