# Review of ASN-0103

## REVISE

### Issue 1: The document-frontier formula `d = inc(max(D_A), 0)` selects version addresses and collides with future version allocations

**ASN-0103, "Effect One" / CND.alloc / CND.def**: "`d = inc(d_prev, 0)` otherwise, where `d_prev = max(D_A)`" with `D_A = {e ∈ E : Document(e) ∧ parent(e) = A}`.

**Problem**: `D_A` is defined as *all* document-level entities whose parent is `A`, but by the foundation this set includes **versions**, not just direct documents. A version is created by `inc(d_src, 1)` (J4 ForkComposite, K.δ case (ii) k=1, ASN-0047); it is `Document(·)` (zeros preserved, K.δ-ID.zeros-0/1) and `parent(version) = parent(d_src) = A` (K.δ-ID.parent-0/1). So versions satisfy both conjuncts of `D_A`.

Concretely, let `A = [n,0,u]`. First document `d1 = inc(A,2) = [n,0,u,0,1]`. Fork it once: `v1 = inc(d1,1) = [n,0,u,0,1,1]`. Now `D_A = {d1, v1}` and `max(D_A) = v1` (since `d1 ≺ v1`). The ASN then sets `d = inc(v1, 0) = [n,0,u,0,1,2]`. But that address is **exactly the next emission of the version sub-allocator `A_v(d1)`** (`inc(v1,0)` is `v1`'s sibling step). A subsequent fork of `d1` will baptise the same `[n,0,u,0,1,2]` — a direct collision, violating B8 (Uniqueness, ASN-0040) and GlobalUniqueness (ASN-0034). The allocated `d` is not an emission of `A_doc(A)` at all, falsifying CND.alloc's claim that "`d` is the next emission of `A_doc(A)`."

The bug manifests whenever the highest-sorting member of `D_A` carries a version (any time the most-recent document has been forked).

**Required**: Restrict the document frontier to `A_doc(A)`'s own chain. The emissions of `A_doc(A)` all have length `#A + 2` (`inc(A,2)` gives `#A+2`; `inc(·,0)` preserves length), whereas versions have length `≥ #A + 3`. Redefine, e.g., `D_A = {e ∈ E : Document(e) ∧ parent(e) = A ∧ #e = #A + 2}` (or otherwise characterise membership in `A_doc(A)`'s `inc(·,0)` chain off `inc(A,2)`), and take `d_prev = max(D_A)` over that restricted set. Then verify non-collision against both the document chain and every version chain branching off it.

### Issue 2: Freshness/ordering of `A_doc(A)` emissions is justified by foundation lemmas scoped to content/link sub-allocators

**ASN-0103, "Effect One"**: "for a subsequent emission the enumeration of `A_doc(A)` is strictly increasing (ChainEnumerationInjectivity, ASN-0093)"; "For the first emission this is FirstEmission freshness."

**Problem**: `FirstEmission` and `ChainEnumerationInjectivity` (ASN-0093) are stated *only* for the content and link sub-allocators `A_C(d)`, `A_L(d)`. Neither covers the document sub-allocator `A_doc(A)`. The needed properties for `A_doc(A)` are derivable — from S0 (StreamOrdering) and B7/B8 (ASN-0040), since `A_doc(A)` is a SiblingStream — but the cited lemmas do not discharge them. The freshness of `A_doc(A)`'s first emission is likewise not "FirstEmission" (a content/link result).

**Required**: Cite the foundation results that actually cover the document sub-allocator (ASN-0040 S0 for strict increase, B7/B8 for disjointness/uniqueness), or state explicitly that `A_doc(A)`, as a SiblingStream, inherits these properties.

### Issue 3: CND.monotone's cross-allocator ordering is not established by T9

**ASN-0103, CND.monotone**: "d strictly exceeds every document address ever baptised under A, including never-populated ones; ... (T8, T9, GlobalUniqueness; ASN-0034)".

**Problem**: T9 (ForwardAllocation) yields `a < b` only when `same_allocator(a, b)`. Document addresses "baptised under A" span *distinct* allocators — `A_doc(A)` plus the version allocators `A_v(d_i)` for each forked document. T9 cannot order an `A_doc(A)` emission against an `A_v(d_i)` emission. GlobalUniqueness gives distinctness, not ordering. The "strictly exceeds every document address" claim therefore requires a direct T1 lexicographic argument (the frontier counter at position `#A+2` dominates every version's counter at that position), which is not shown.

**Required**: Replace the T9 appeal for cross-allocator pairs with an explicit T1 comparison, or narrow the claim to same-allocator (`A_doc(A)`) emissions.

### Issue 4: No concrete worked example verifying the post-state

**ASN-0103, throughout**: The ASN cites Gregory's implementation ("content granfilade unchanged, document granfilade modified") but never traces a specific scenario at the tumbler level.

**Problem**: Per the depth standard, an ASN should verify its key postconditions against at least one concrete scenario. The empty-account case (`D_A = ∅ ⟹ d = inc(A,2)`) and the subsequent-document case (`D_A ≠ ∅`) are exactly where the allocation logic must be checked — and a worked example with concrete tumblers would have surfaced Issue 1 immediately (the `inc(max(D_A),0)` collision).

**Required**: Add a worked example, e.g. "Account `A = [1,0,1]` with existing document `d1 = [1,0,1,0,1]` and version `v1 = [1,0,1,0,1,1]`; CREATENEWDOCUMENT(A) → check CND.alloc, CND.empty, CND.E, CND.monotone against the produced address," demonstrating the post-state and non-collision.

### Issue 5: The ownership transfer `ω_{Σ'}(d) = ω_Σ(A)` is asserted with a one-line derivation

**ASN-0103, CND.own**: "Since `d` is fresh and no finer principal sits between `A` and `d`, the new document's effective owner is the account's owner: `ω_{Σ'}(d) = ω_Σ(A)`."

**Problem**: `ω` (ASN-0042) is defined over the baptismal registry `Σ.B`, while CREATENEWDOCUMENT is specified entirely over the entity set `E` (ASN-0047). The equality presumes (i) `A ∈ Σ.B` and `d ∈ Σ'.B` (the E↔B coupling, O17b/O18, is not invoked), and (ii) that no principal prefix lies strictly between `A` and `d`. Claim (ii) is plausible via O1a (account-tier boundary `zeros(pfx(π')) ≤ 1`, so no principal prefix of zeros 2 can sit between account-level `A` and document-level `d`), but the derivation names no premise. A "derived" guarantee must show the chain.

**Required**: Make the derivation explicit — invoke the registry/entity coupling that places `d` (and `A`) in `Σ.B`, then apply O1a to exclude an intervening principal prefix, then conclude via the `ω` definition.

## OUT_OF_SCOPE

### Topic 1: Concurrent CREATENEWDOCUMENT under one account
The fourth Open Question (serialisation and address-ordering for independent concurrent creators) is genuinely new territory — a concurrency model the substrate's sequential-transition axiom does not yet address. Correctly deferred.

### Topic 2: Removal of created-but-never-populated documents
The Open Question on removing ghost documents touches deallocation, which the no-deallocation foundation excludes by design. A future ASN, not an error here.

VERDICT: REVISE
