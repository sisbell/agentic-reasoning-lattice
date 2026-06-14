# Channel Assignment — ASN-0123 review-44

**Date:** 2026-06-13 20:28

## Issue 1: Registry-purity asserted in full at three sites
Reason: Pure prose-consolidation fix internal to the ASN — the registry-purity property is already formally proved and stated in V5(b), and the task is to demote the two redundant restatements (the `nextv`-definition annotation and G1) to a bare line plus a pointer. No design-intent or implementation fact is in question; the store-list and congruence statement already exist in the document.

## Issue 2: VN-B1 closing remark is a forward-referencing ordering justification
Reason: Editorial relocation derivable from the ASN alone — the contiguity proof, its independence from VD, and V5(a)'s allocation-order-vs-fork-order distinction are all already present; the fix only drops a defensive forward-reference disclaimer and, if needed, moves the "whatever composite fires the step" robustness point into V5(a) as content. No external evidence about intent or code is required.
