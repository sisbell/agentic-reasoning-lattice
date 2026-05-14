# Channel Assignment — ASN-0058 review-23

**Date:** 2026-05-13 20:58

## Issue 1: C0 proof implicitly assumes k ≤ m
Reason: Fix is internal — cite ActionPoint's postcondition from ASN-0034 (already an upstream dependency). No design intent or implementation evidence needed; the bound is structural.

## Issue 2: C1a "applies verbatim" overstates the extension
Reason: Pure proof-text revision. The substitution (S8-depth → C1a's common-depth assumption) is a bookkeeping fix internal to the ASN's own argument structure.

## Issue 3: Origin invariance within a block is implicit but never stated
Reason: Extract-and-name task — the fact is already derived inside M16's proof and reused at M6(d). Refactoring existing content into a named corollary, no external input required.

## Issue 4: Span Algebra Connection remark asserts imprecise correspondences
Reason: Reconciles two formal definitions (mapping block `V(β)` vs. ASN-0053 span denotation `⟦σ⟧`) and S3's adjacency scope. Both definitions live in already-cited ASNs; fix is derivable from text in hand.

## Issue 5: Element-level allocator T10a-conformance is implicit
Reason: Requires confirming whether element-level allocators are descendants in T10a's recursive allocator tree, which is a structural property of T10a itself.
Gregory question: In udanax-green, are element-level I-address allocators created by `inc(·, k')` operations applied to document-level allocators (i.e., descendants in the same allocator tree), such that any T10a-discipline placed on document-level allocators propagates to element-level allocators?
