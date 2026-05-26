# Channel Assignment — ASN-0075 review-24

**Date:** 2026-05-25 19:47

## Issue 1: D-ACT bijection proof omits explicit verification of Right-maximality and Left-maximality
Reason: The fix is a one-sentence proof addition for each maximality condition, and the review itself sketches the argument from equivalence-class closure under I-adjacency. All ingredients (I-adjacency definition, equivalence-class structure, shift function) are already in the ASN; no design-intent or implementation-evidence input is needed.

## Issue 2: C ⊆ dom(A_C(d)) inference relies on uncited reverse direction of SubAllocatorAxiom
Reason: The fix is a citation to SubAllocatorAxiom (e) (Disjointness) from ASN-0047, which the review identifies explicitly. The axiom is already established in the foundation chain this ASN imports; no further input is required.
