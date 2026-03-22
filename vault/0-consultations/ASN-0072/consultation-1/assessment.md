# Revision Categorization — ASN-0072 review-1

**Date:** 2026-03-22 10:42

## Issue 1: Pervasive cross-references to ASN-0043 (not a foundation ASN)
Category: INTERNAL
Reason: ASN-0043 already contains formal definitions for L0, L1, L1a, L3, L12, L14, and the Link type. The fix is restating or elevating existing content — no new design intent or implementation evidence is needed.

## Issue 2: s_C and s_L are undefined symbols; s_C ≠ s_L is never established
Category: INTERNAL
Reason: L0's partition (ASN-0043) already separates content and link addresses by subspace, and T7 (ASN-0034) establishes SubspaceDisjointness. The distinctness s_C ≠ s_L is derivable from L0's partition clause; the fix is making the implicit axiom explicit and clarifying the shared role of subspace identifiers across V-positions and I-addresses.

## Issue 3: P4★ and P7a are composite-level invariants, but the proof claims per-elementary preservation
Category: INTERNAL
Reason: The mathematical content (coupling constraints J0, J1★, J1'★) is already present in the ASN. The fix is restructuring the proof into elementary-level and composite-level layers — a purely organizational change requiring no external evidence.

## Issue 4: No concrete worked example
Category: INTERNAL
Reason: All operations (K.λ, K.μ⁺_L) and postconditions (S3★, CL-OWN, L14, D-CTG/D-MIN) are fully defined in the ASN and its dependencies. A worked example can be constructed by choosing concrete tumbler values satisfying the stated preconditions — no design intent or implementation evidence is needed.

## Issue 5: L3 missing from ExtendedReachableStateInvariants
Category: INTERNAL
Reason: The preservation argument is immediate from K.λ's precondition (establishes L3), L12 (preserves link values), and the frame conditions of all other transitions (L unchanged). Adding L3 to the theorem's invariant list requires only the formal statement from ASN-0043, which is an editorial dependency on Issue 1.
