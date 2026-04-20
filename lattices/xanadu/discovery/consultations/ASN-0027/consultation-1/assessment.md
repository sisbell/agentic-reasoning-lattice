# Revision Categorization — ASN-0027 review-1

**Date:** 2026-03-10 09:17

## Issue 1: A4 (CopySharing) missing preconditions and target frame conditions
Category: INTERNAL
Reason: The fix follows the pattern already established by A2 (DELETE) in the same ASN — preconditions, length postcondition, left frame, and right shift. The identity clause already implies insertion semantics, so the missing clauses are derivable from existing conventions.

## Issue 2: A9 proof invokes cross-document frame for same-document references
Category: INTERNAL
Reason: The proof fix is purely logical — group references by document, delete lowest-position-first within each document. A2's compaction clause already specifies how positions shift, providing all information needed to correct the proof.

## Issue 3: No concrete example
Category: INTERNAL
Reason: Constructing a worked example requires only instantiating the existing formal definitions (A2, A6, A7) with specific values. The review even suggests a suitable example. No external evidence needed.

## Issue 4: A6 uses `correspond` in a cross-state sense not defined by ASN-0026
Category: INTERNAL
Reason: The fix is either defining cross-state correspondence (a straightforward extension of the existing single-state definition) or restating the claim directly using `Σ₂.V(d)(p+j) ≠ Σ₀.V(d)(p+j)`, which is already proven in A6. Both options are derivable from content already present.

## Issue 5: A3 (RearrangeIdentity) missing precondition
Category: INTERNAL
Reason: The minimum precondition `d ∈ Σ.D` follows the pattern of every other operation spec in the ASN. The review offers the option to note that the spec abstracts over permutation selection, which is an internal editorial decision.
