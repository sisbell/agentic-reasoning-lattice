# Channel Assignment — ASN-0126 review-90

**Date:** 2026-06-10 04:39

## Issue 1: B2's transition-transfer clause is unjustified and its precondition is too weak
Reason: Internal. Every object involved — ProjectionBridge, B2, P6, and L12 (LinkImmutability) — is either defined in this note or cited from ASN-0043/0086 as already-established content; the reviewer's key fact, that L12 is quantified over →-steps not arbitrary reachable pairs, is the same step-to-step mapping P6 already uses correctly inline. Choosing option (a) or (b) and rewording the clause requires no design intent or implementation evidence.

## Issue 2: "The registry" section pre-narrates the operation set and transition relation
Reason: Internal. This is a relocation of existing prose — moving the operation-set and transition-relation refinement from "The registry" into "The shape-gated emit" — with no change to any claim, definition, or proof.

## Issue 3: "Empty-from Nullify has no →_sh image" stated three times
Reason: Internal. Deduplication of a fact the note already derives in "The shape-gated emit"; the fix replaces two restatements with citations, requiring no external input.

## Issue 4: Defensive justifications around the wp and P6 proofs
Reason: Internal. Pure compression of two parentheticals (the wp arity-guard remark and the P6 induction-hypothesis aside) into tighter positive statements; no claim changes, so no channel is needed.
