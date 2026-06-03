# Channel Assignment — ASN-0075 review-61

**Date:** 2026-06-03 10:12

## Issue 1: Classification granularity over multiply-occurring I-addresses is left implicit
Reason: The note must justify set-granularity classification as intended semantics or scope per-occurrence detection out — both require knowing what "show deletions" was meant to compare (Nelson) and whether the implementation ever tracked per-occurrence removal (Gregory).
Nelson question: Was SHOWDELETIONS intended to compare content at I-address-set granularity (cross-document presence/absence), or to detect per-occurrence removal when an I-address occupies multiple V-positions within one document?
Gregory question: Does udanax-green's deletion/comparison machinery distinguish removing one of several V-occurrences of an I-address from removing the address entirely, or does it operate on set membership in a document's arrangement?
