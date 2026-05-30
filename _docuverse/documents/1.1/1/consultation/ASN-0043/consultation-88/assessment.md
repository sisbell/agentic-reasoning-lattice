# Channel Assignment — ASN-0043 review-88

**Date:** 2026-05-30 10:57

## Issue 1: Exact duplicate sentence inside the FSP lemma statement
Reason: Purely an editing artifact — deleting one of two verbatim sentences requires no design intent or implementation evidence; the fix is internal text surgery.

## Issue 2: Pre-L3 meta-paragraph defers forward and duplicates L3's own verdict
Reason: The object-level evidence (`docreatelink`/`domakelink` behavior) and the out-of-scope verdict already exist in the ASN; consolidating them and dropping a forward-pointer sentence is a relocation, not new content requiring either channel.

## Issue 3: Redundant forward references to L9 for the ghost-address contrast
Reason: The home-must-be-allocated fact is already carried by L1a's own membership invariant `home(a) ∈ dom(Σ.M)`; removing redundant L9 forward pointers is derivable from the ASN's existing structure.
