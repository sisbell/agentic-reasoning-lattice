# Channel Assignment — ASN-0086 review-151

**Date:** 2026-06-01 04:10

## Issue 1: Definition — Nullified states the `A_rel` restriction's effect twice
Reason: Pure editorial deduplication — delete the redundant second sentence and fold the R5/L9 clause into the first. The fix is derivable entirely from the definition's own text; no design intent or implementation evidence is at stake.

## Issue 2: Definition — Nullified pre-states R6b's audit-slice semantics
Reason: The sentence to remove is restated verbatim in R6b's body and Remark, so deletion is a structural relocation derivable from the ASN's own content. No external channel needed.

## Issue 3: Corollary (reduction to Emit_K) asserts layer substrate-conformance without derivation
Reason: All premises for the missing inference already appear in the ASN — the K.λ contract satisfying clauses (a)–(c), the layer's operation set being Emit_K/Nullify (both K.λ steps) plus read-only Observe_K. The derivation is internal and requires no channel.
