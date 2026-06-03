# Channel Assignment — ASN-0069 review-95

**Date:** 2026-06-03 02:06

## Issue 1: V9's consequence claims `{d_src, d_new}` but this is wrong for subsequent forks
Reason: The fix is internal — the ASN already contains everything needed. V12(d) correctly derives the operand-side record as `(a, d_op)`, J4's operand rule is restated in §"What Must Be Constructed", and the V1 first-fork/subsequent-fork dispatch (`d_op = d_src` vs `d_op = d_prev`) is already in this ASN. Restating V9's consequence as `{d_op, d_new}` is a mechanical correction against the ASN's own established machinery; no design intent or implementation evidence is required.
