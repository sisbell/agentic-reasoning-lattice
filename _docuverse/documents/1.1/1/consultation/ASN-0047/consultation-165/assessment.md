# Channel Assignment — ASN-0047 review-165

**Date:** 2026-05-31 20:06

## Issue 1: S8★ over-claims ASN-0036's S8 condition (b) for the link subspace
Reason: The fix is internal — the ASN already establishes that link labels reside in `dom(L)`, that L14 makes the stores disjoint, and that the link-subspace decomposition sidesteps S3/S7b/C1b; restating condition (b) with the explicit `dom(C) → dom(L)` substitution is a definitional adjustment derivable from content already present.

## Issue 2: Redundant double-derivation of `subspace(v) = s_C` in the P7a discharge
Reason: The fix is internal — it is purely editorial deletion of meta-commentary, retaining the existing S3★ + L14 contradiction route already written in the ASN.

## Issue 3: SubAllocatorAxiom sub-clauses carry deferral inventories rather than content
Reason: The fix is internal — reducing the parentheticals to a `per ASN-0093` citation is editorial trimming, with the inheritance note already carried once in the foundation table.

## Issue 4: K.μ⁻ admissible-shape equivalence reverse direction re-states its own hypothesis as a derivation
Reason: The fix is internal — compressing the constituent-source bookkeeping into one sentence is an editorial restructuring of prose already present in the proof.
