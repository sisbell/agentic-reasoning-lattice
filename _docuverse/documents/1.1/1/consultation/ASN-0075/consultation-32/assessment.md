# Channel Assignment — ASN-0075 review-32

**Date:** 2026-06-03 00:47

## Issue 1: D-ACT derives a new I-set run-decomposition algebra from scratch inside an operation ASN
Reason: Internal. The ASN already concedes the witness-run presentation is "a form, not a fundamental commitment" and that the abstract spec fixes only the I-address set; reducing D-ACT to that set-level claim (with D-IDENT/D-ORIG) and removing or out-factoring the bijection proof is a scope decision derivable from the ASN's own text and the review standard. No design intent or implementation evidence is needed to delete reusable algebra that the operation does not require.

## Issue 2: D-ORD specifies presentation ordering, not a state guarantee
Reason: Internal. The Definition returns a pair of sets; restating D-ORD as the derivable fact that the deletion set inherits T1's total order (or dropping it) is settled by the ASN's own definitions and the cited T1 properties, with no presentation commitment to resolve via Nelson or Gregory.

## Issue 3: Peripheral negative/prose claims inflate the operation contract
Reason: Internal. Compressing D-STORE under D-OBS, dropping the speculative restoration prose, and reducing the empty-shared-content edge case to the definition-matching condition are purely editorial reductions derivable from the ASN's existing claims.
