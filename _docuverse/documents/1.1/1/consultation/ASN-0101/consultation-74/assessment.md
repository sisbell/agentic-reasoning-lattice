# Channel Assignment — ASN-0101 review-74

**Date:** 2026-06-04 15:54

## Issue 1: P4a discharge in the D11 boundary derivation relies on a single-step argument at a multi-step composite boundary
Reason: The fix is derivable from the ASN's own formal apparatus — it requires invoking composite validity's J1'★ clause (already cited elsewhere in D11) to show every new `(a, d) ∈ R' \ R` retains a content-subspace witness at the endpoint boundary. No design intent or implementation evidence is needed; the argument is purely about the existing invariant machinery.

## Issue 2: Wrong claim reference in the worked-example verification of D10
Reason: Pure textual correction — "D11 wp" must read "D10 wp" because D11 introduces no wp. Internal and mechanical.

## Issue 3 (anti-bloat): Defensive vocabulary-provenance prose in D11
Reason: Removal of an accreted scoping sentence; the vocabulary list already carries the information. Purely internal editorial fix.
