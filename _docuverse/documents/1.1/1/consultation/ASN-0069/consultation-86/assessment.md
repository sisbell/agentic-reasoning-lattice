# Channel Assignment — ASN-0069 review-86

**Date:** 2026-06-03 01:25

## Issue 1: §"Permanence Across Source and Fork" — three lead-in paragraphs duplicate V12's clauses verbatim
Reason: The fix is purely editorial — deleting redundant prose and folding citations into V12's existing clauses. All the facts (T8/P1/P0/S0/S1/P2/V9) are already present in the ASN; no design intent or implementation evidence is required.

## Issue 2: V8c instantiates the correspondence set over (d_src, d_new) while V8 establishes fullness only over (d_op, d_new)
Reason: The fix is internal — V8's own domain (`d_op`, equal to `d_src` only on first fork) and the first/subsequent-fork operand distinction are already fully specified in the ASN (V1, V8, V10b). Restating V8c over `(d_op, d_new)` or noting the first-fork specialization is derivable from existing content alone.
