# Channel Assignment — ASN-0117 review-1

**Date:** 2026-06-08 17:19

## Issue 1: DELETE's operation definition omits the link-store frame condition
Reason: Internal — DELETE already establishes (throughout the note) that it touches only the arrangement enfilade and never the link orgl; adding the explicit `Σ'.L = Σ.L` frame clause and re-citing it (not L12) in P4 and the wp is a formalization fix derivable from the note's own non-destruction architecture.

## Issue 2: LP10 (ContractionMonotonicity) is misapplied to DELETE
Reason: Internal — the required `ran(M'(d)) ⊆ ran(M(d))` derivation already exists in the note's own wp section (DEL-LEFT/DEL-SHIFT preserve I-addresses, DEL-REMOVE drops the block, DEL-DOM fixes the domain); dropping the LP10 citation and replacing it with the in-note derivation needs no external channel.
