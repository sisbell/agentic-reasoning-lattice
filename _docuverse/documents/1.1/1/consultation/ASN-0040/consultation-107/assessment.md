# Channel Assignment — ASN-0040 review-107

**Date:** 2026-05-29 04:44

## Issue 1: Sequential-commitment rationale stated three times across the document
Reason: Pure editorial deduplication — consolidate the branching motivation at B-Seq and delete the restatements in the preamble and B8 proof. No design intent or implementation evidence is needed; the text to keep and cut is already present.

## Issue 2: B-Seq prose explains why the axiom is needed rather than what it says
Reason: The fix is to trim essay content down to the axiom statement plus the one-line implementation grounding already present, and relocate the reconciliation to the existing Open Questions entry. All source material is in the ASN; no new evidence required.

## Issue 3: B8 Case 1 — the step from comparability to `s₁' →* s₂` is asserted, not derived
Reason: A proof-rigor fix using only B-Seq's own definition (total order on states) — define "precedes" via →* and restate the WLOG to relabel the comparable states. Fully derivable from the ASN's existing axioms.
