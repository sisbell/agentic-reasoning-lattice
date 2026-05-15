# Channel Assignment — ASN-0084 review-28

**Date:** 2026-05-15 12:18

## Issue 1: dom(M(d)) vs V_S(d) conflation in canonical decomposition
Reason: Pure formalization fix — the ASN already establishes the multi-subspace structure of dom(M(d)) and the text-subspace scope; restating the argument's domain is internally derivable.

## Issue 2: Existence-of-maximum hand-wave
Reason: Pure mathematical derivation using NAT-wellorder on the complement; entirely internal to the foundation already cited.

## Issue 3: Partition property not shown maintained through merges
Reason: Invariant-maintenance argument derivable from S8 (initial partition) and the Merge lemma already in the ASN; no external evidence needed.

## Issue 4: "Strict extension" used without formal definition
Reason: Definitional cleanup — the intended meaning (V-extent strict containment plus run-validity) is fully present in the ASN's existing run framework.

## Issue 5: Worked examples do not verify R-RI
Reason: One-line check using I-addresses already enumerated in the examples; entirely self-contained.

## Issue 6: Weakest-precondition analysis absent
Reason: Methodological tightening — wp(REARRANGE, Q) for an S8-style post-condition is computable from R-PRE and R-BLK already in the ASN.

## Issue 7: R-BLK's "valid but not necessarily maximal" lacks general characterization
Reason: Formal characterization expressible in terms of region assignment, π's region displacements (R-DISP), and the Merge mergeability conditions — all internal to the ASN.

## Issue 8: Empty-exterior boundary case not traced through R-BLK Phase 1
Reason: Trace through existing definitions (R-PRE(iv), D-SEQ, S8a) for the c_{n−1} ∉ V_S(d) configuration; fully derivable from current content.

## Issue 9: Region-partition exhaustiveness only stated, not derived
Reason: T1 trichotomy case analysis using cuts already given by CS2; pure internal derivation.

## Issue 10: NAT-sub domain verification implicit for ordinal subtraction
Reason: Single-line discharge from CS2 and T1's strict ordering, both already cited in the ASN.
