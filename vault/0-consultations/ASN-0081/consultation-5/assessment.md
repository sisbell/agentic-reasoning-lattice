# Revision Categorization — ASN-0081 review-5

**Date:** 2026-04-09 19:43



## Issue 1: Registry Contraction entry lists D-SHIFT as a precondition
Category: INTERNAL
Reason: The correct preconditions are already fully stated in the Contraction formal contract section of this ASN. The fix is a mechanical replacement in the registry table.

## Issue 2: S8-fin preservation missing from invariant verification
Category: INTERNAL
Reason: S8-fin is a standard ASN-0036 invariant, and the proof follows directly from the already-established facts in this ASN (L and Q₃ are subsets of the finite pre-state domain; D-CS and D-CD preserve other subspaces/documents). No external design intent or implementation evidence is needed.
