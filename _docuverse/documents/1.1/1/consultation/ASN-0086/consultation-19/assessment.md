# Channel Assignment — ASN-0086 review-19

**Date:** 2026-05-17 00:23

## Issue 1: R7's proof is one sentence for a meta-claim
Reason: The closure argument is derivable from this ASN's own definitions plus L12 (LinkImmutability) and L12a (LinkStoreMonotonicity) from ASN-0043, which together force any Σ.L change to be a fresh-address extension via the substrate emission primitive — no design-intent or implementation evidence needed.

## Issue 2: Emit_K determinism in Case B is implicit
Reason: The independence-of-b argument follows directly from R0a's sibling-stream invariant (already proved in this ASN) plus the composition identity inc^i ∘ inc^k = inc^{i+k} on the depth-2 allocator's enumeration; the fix is a remark composing pieces already present.

## Issue 3: Shared-allocator interpretation buried in proof prose
Reason: Whether subspaces are enumerated by a single shared depth-1 allocator under each document (vs. independent per-subspace allocators) is a model commitment underlying R0's chain construction. Nelson clarifies whether the tumbler design intended a shared per-document allocator across subspaces; Gregory clarifies whether granfilade's implementation enumerates content and link positions via one allocator or separate ones.
Nelson question: Did the tumbler design intend each document's depth-1 element-field allocator to enumerate positions across all subspaces (content, link, etc.) in a single sibling stream — with subspace identity determined by first-element-field value of each output — rather than maintaining independent allocators per subspace?
Gregory question: Does udanax-green's granfilade orgl tree under each document use a single shared depth-1 element-field allocator producing positions that land in either content subspace (s_C) or link subspace (s_L) by their first-element-field value, or does it maintain separate per-subspace allocator trees?

## Issue 4: Arrangement-modification frame inheritance not specifically cited
Reason: The fix requires identifying specific ASN-0036 invariants (S9 for Σ.C invariance, the definitional scope of arrangement modifications for dom(Σ.M) preservation) and noting ASN-0036's silence on Σ.L combined with L12 + L12a from ASN-0043 — all derivable from existing foundation ASN content without external consultation.
