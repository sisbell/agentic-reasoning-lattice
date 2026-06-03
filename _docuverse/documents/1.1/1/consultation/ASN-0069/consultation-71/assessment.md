# Channel Assignment — ASN-0069 review-71

**Date:** 2026-06-02 23:30

## Issue 1: Use-site justification prose that does not advance the proof
Reason: Pure editorial deletion of meta-prose parentheticals; no design intent or implementation evidence is needed since the biconditionals above already discharge the obligation.

## Issue 2: Same statement repeated in two sections in different words
Reason: Editorial deduplication of an identical claim; resolvable entirely within the ASN by keeping the statement once and citing it.

## Issue 3: V10(b) assumes "d_new¹ is the first fork" but V10's premise does not establish it
Reason: Internal logical fix — either add the first-fork premise or restate (b) using each fork's own J4 operand `d_op^i`; both options follow from J4's operand-tracking and V1 already in the ASN.

## Issue 4: "Transitive correspondence" between d_src and d_new asserted without derivation
Reason: Internal derivation fix — either supply a V11-style unedited-source premise on `d_prev` and show the composition, or restrict the sentence to `d_op = d_src` and defer to V11; all required machinery (V8, V11) is present in the ASN.
