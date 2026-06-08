# Channel Assignment — ASN-0112 review-12

**Date:** 2026-06-08 08:19

## Issue 1: The reach biconditional is derived four times in four locations
Reason: Pure deduplication — consolidate one already-proven biconditional (D0/D1) into V2 and cite by label elsewhere. The reasoning is entirely internal to the ASN; no design intent or implementation evidence is in question.

## Issue 2: Repeated deferral to "the substrate distinction"
Reason: Editorial consolidation of the level-uniform vs endpoint-level-compatible distinction already developed in the substrate section. Removing deferral pointers requires no external input.

## Issue 3: Meta-commentary about what the implementation "never exercises"
Reason: The fix only removes scope rationale and folds a redundant worked variant whose arithmetic duplicates V2's case (ii); the `m_C = m_L` realization is already cited (Q2) and need not be re-confirmed. Internal.

## Issue 4: V8↔V18 mutual cross-referencing
Reason: Both claims' scopes are self-evident from their stated preconditions (content present vs content cleared); removing the bidirectional pointers is purely internal editing.

## Issue 5: The "empty ≠ zero-extent span" argument appears in both V0 and V11
Reason: The non-degeneracy point and its foundation citations (S2, TA6, Pos) are already present in the ASN; consolidating into V0 and leaving the operational consequence in V11 is internal.
