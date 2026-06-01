# Channel Assignment — ASN-0086 review-152

**Date:** 2026-06-01 04:18

## Issue 1: Nullify concludes `a ∈ nullified(Σ')` without gating on P1
Reason: The fix is internal — the ASN already defines `nullified(Σ')` with its `a ∈ A_rel^{Σ'}` restriction, states P1's billed role, and exhibits the correct gating pattern in R6a (L12a applied to `a ∈ A_rel^Σ`). The revision just mirrors that existing argument; no design intent or implementation evidence is required.

## Issue 2: Redundant frame restatement in the `→` definition
Reason: Pure prose deduplication — collapsing two sentences that restate the same frame condition while retaining the distinct closure claim. Fully derivable from the ASN's own text; needs neither channel.
