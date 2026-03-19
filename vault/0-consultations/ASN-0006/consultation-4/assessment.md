# Revision Categorization — ASN-0006 review-4

**Date:** 2026-03-06 23:52

## Issue 1: Position notation reinvents ASN-0001's subspace arithmetic
Category: INTERNAL
Reason: The fix requires restating ASN-0006's positions using ASN-0001's already-established definitions (T4, T7, TA7a, TA7b, T12). All necessary formalism is already present in ASN-0001.

## Issue 2: Transclusion independence theorem assumes B ≠ D without stating it
Category: INTERNAL
Reason: The proof already uses B ≠ D — the fix is adding the condition to the theorem statement and noting the self-transclusion exception. Entirely derivable from the ASN's own reasoning.

## Issue 3: `a↓doc` extraction assumes single-component fields
Category: INTERNAL
Reason: The fix is to define `a↓doc` using ASN-0001's `fields(t)` function (T4), which already handles multi-component fields. No external evidence needed.

## Issue 4: AX1 claims universality beyond its evidence
Category: GREGORY
Reason: Closing the operation set requires confirming that INSERT, DELETE, COPY, CREATENEWVERSION, and MAKELINK are the complete set of mutating FEBE operations — only implementation evidence can verify no other mutating operations exist.
Gregory question: Are there any mutating FEBE operations in udanax-green beyond INSERT, DELETE, COPY, CREATENEWVERSION, and MAKELINK that modify a document's POOM?

## Issue 5: Self-transclusion has no concrete trace
Category: INTERNAL
Reason: The trace is constructed mechanically from existing postconditions (TC2, TC4, TC7). The overlapping source/insertion scenario is fully determined by the ASN's own formal properties.

## Issue 6: Target POOM post-state domain not explicitly characterized
Category: INTERNAL
Reason: The domain characterization and disjointness proof are derivable from TC2 and TC7's existing postconditions — purely formal work requiring no external evidence.
