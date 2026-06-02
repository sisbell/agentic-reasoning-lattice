# Channel Assignment — ASN-0086 review-240

**Date:** 2026-06-01 21:15

## Issue 1: R-Scope self-emit branch mis-attributes the `=∅` claim to R0a "at Σ"
Reason: Pure proof-attribution fix — the correct state (Σ') and its antichain (R0a) are both already present in the ASN; reassigning the citation is internal bookkeeping needing no design intent or implementation evidence.

## Issue 2: R0's Value-shape consequence forward-references Emit_K for an L3 discharge that is self-contained
Reason: R0's own hypotheses `(F, G, K) ∈ Endset × Endset × T_admissible` already discharge L3; removing the forward pointer to Definition — Emit_K is a self-contained dependency-cleanup derivable from the ASN alone.

## Issue 3: Defensive rationale in the relational-layer definition
Reason: Dropping a justifying parenthetical while keeping the structural statement is a local prose edit; the content stands on its own ASN text with no external input required.
