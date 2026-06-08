# Review of ASN-0103

## REVISE

### Issue 1: Cross-chain distinctness asserts an exhaustive taxonomy of document-level addresses without deriving it

**ASN-0103, Effect One ("Freshness and distinctness," cross-chain case)**: "every document-level address (zeros = 2) not on S(A, 2) is emitted by some other SiblingStream — an account's document chain S(A'', 2) for A'' ≠ A, or a version chain S(d_src, 1) forked off any document-level d_src ... We discharge all of them with a single B7 instantiation."

**Problem**: The B7 discharge requires that *every* document-level address `b ∉ S(A,2)` actually lies in some `S(p', d')` with B6-valid `(p', d')`. The ASN asserts the partition (document chains `A_doc` ∪ version chains `A_v`) but never derives that these two families *exhaust* the zeros=2 addresses. The needed fact — every such `b` is an emission of an activated entity-level sub-allocator (ActivatedEmission, ASN-0047), and the only entity-level sub-allocators producing zeros=2 are `A_doc` and `A_v` (AllocatorHierarchy, ASN-0047) — is exactly the missing step. As written this is "the taxonomy follows from the structure," not a derivation. Since the present-and-future distinctness in CND.monotone is a *derived guarantee*, the standard requires the chain be made explicit (name the premises, show that `A_doc`/`A_v` are the only zeros=2 emitters).

**Required**: Insert the derivation: for any zeros=2 entity `b ∉ S(A,2)`, cite ActivatedEmission to place `b ∈ dom(A)` for some activated entity-level sub-allocator `A`, then cite AllocatorHierarchy to conclude `A` is either `A_doc(A'')` or `A_v(d_src)` (the only entity-level allocators emitting zeros=2), each a SiblingStream `S(p',d')` with B6-valid `(p',d') ≠ (A,2)`. Then B7 applies. (Note: the operation's *correctness* does not depend on this — freshness `d ∉ E` is fully and rigorously established via `S(A,2)\D_A = S(A,2)\E` — but the distinctness guarantee CND.monotone advertises must be derived, not asserted.)

## OUT_OF_SCOPE

### Topic 1: Concurrent CREATENEWDOCUMENT under one account
**Why out of scope**: The ASN proves distinctness under SequentialTransitionAxiom and explicitly defers concurrent same-account allocation to an Open Question. Same-namespace uniqueness under multiple authorities (B8 / B-Seq) is genuinely new territory, not a defect here.

### Topic 2: Effective-owner reading of ownership
**Why out of scope**: CND.own correctly establishes *structural* ownership (`pfx(π) ≼ d`) over the post-state and explicitly leaves effective ownership (`ω_Σ`) open, since that requires the entity-set/baptismal-registry coupling (ASN-0042 O17b) that account provisioning owes — correctly punted.

VERDICT: REVISE
