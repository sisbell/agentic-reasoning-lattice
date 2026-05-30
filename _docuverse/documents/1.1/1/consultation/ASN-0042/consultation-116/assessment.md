# Channel Assignment — ASN-0042 review-116

**Date:** 2026-05-30 04:42

## Issue 1: O7(c) enumerates the wrong set of conditions to re-check at the delegation site
Reason: The proof body already establishes the correct classification — (iii) and (v) bind, (i) is fixed by the choice of `p''`, and (ii)/(iv) auto-discharge. The fix is reconciling the statement and contract with reasoning already present in the ASN.

## Issue 2: Standalone cross-reference paragraph that advances no reasoning
Reason: Pure deletion of a back-pointer; the induction it references is self-locating in *The Account-Level Boundary*. Fully internal editorial fix.

## Issue 3: Forward-reference document-ordering justification embedded in the induction setup
Reason: Removal of a parenthetical meta-note about where O15 conditions are defined; the inline citation suffices. Internal editorial fix.

## Issue 4: Provenance pointers embedded inside property statements
Reason: Relocating "shared induction" provenance from the O1a/O1b claim lines into the proof prose or Status column. The provenance content already exists elsewhere in the ASN; only placement changes.

## Issue 5: Unilateral O10★ quantifies over all π but its prose only justifies the account-level case
Reason: The Form-A exclusion line needed for the node-level branch already appears in O10's non-coverage analysis (`a'` carries 0 at position `#pfx(π)+1`, Form-A sub-delegates carry positive there). The fix imports that existing reasoning into the Unilateral★ justification.
