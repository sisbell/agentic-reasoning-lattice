# Channel Assignment — ASN-0047 review-44

**Date:** 2026-05-15 17:44

## Issue 1: K.δ descent case has incorrect zero-count formula
Reason: Purely structural error against TA5(d) of ASN-0034, which is cited in-ASN. The reviewer has already worked out the correct formula from the foundation; no design intent or implementation evidence is needed.

## Issue 2: K.μ~ definition is over-permissive relative to the realizable decomposition
Reason: The fix direction (tighten K.μ~ to forbid link-subspace permutation vs. broaden K.μ⁺ to admit link-subspace) depends on whether intra-document link reordering is intended. Nelson's "permanent order of arrival" suggests no, but explicit design confirmation matters; Gregory should confirm whether the implementation reorders link-subspace positions.
Nelson question: Does the design permit reordering of links within a document's link subspace, or is the "permanent order of arrival" for home-document links strict (i.e., link-subspace V-positions are fixed once allocated)?
Gregory question: Does udanax-green provide any operation that permutes link-subspace V-positions within a document's arrangement (analogous to rearrange for text), or does the implementation treat the link arrangement as append-only with fixed order?

## Issue 3: T7 invocation in L14 derivation is logically redundant
Reason: The redundancy is internal to the derivation — single-valuedness of `fields(a).E₁` plus SC-NEQ already closes the contradiction. Pure logic check against the ASN's own chain.

## Issue 4: K.δ for root nodes does not specify address allocation
Reason: Whether post-Σ₀ root-node creation is admitted is a design-intent question (Nelson on multi-node/federated docuverse architecture), and the allocation mechanism — if any — would be evidenced in udanax-green's node bootstrap path.
Nelson question: Does the design contemplate creation of additional root nodes (server nodes) after system initialization, or is the bootstrap node n₀ the unique root node fixed at system creation, with all subsequent entity creation occurring strictly beneath it?
Gregory question: Does udanax-green allocate node-level addresses dynamically at runtime (and if so, by what mechanism is uniqueness guaranteed across a federation), or is the node address fixed once at server startup with no in-system K.δ-equivalent for nodes?
