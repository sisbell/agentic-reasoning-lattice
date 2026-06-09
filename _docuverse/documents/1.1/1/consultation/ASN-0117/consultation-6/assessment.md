# Channel Assignment — ASN-0117 review-6

**Date:** 2026-06-08 22:34

## Issue 1: `ran(M'(d)) ⊆ ran(M(d))` is derived only over the text subspace
Reason: Internal — the missing step (link-subspace images carried verbatim by DEL-FSUB) is already stated in the ASN's own clauses and done correctly in the wp section; the fix just propagates that accounting to the P4 derivation. No design intent or implementation evidence is needed.

## Issue 2: the worked example never exercises a multi-position suffix shift
Reason: Internal — adding a scenario with `|R| ≥ 2` is a mechanical application of DEL-SHIFT (`σ(q_k) = q_{k−c}`) and D-BJ already established in the ASN; no external channel is required to compute the worked example.
