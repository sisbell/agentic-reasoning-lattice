# Review of ASN-0093

## REVISE

### Issue 1: Restatement gloss appended to C1c and L1c invariant bodies
**ASN-0093, C1c / L1c**: C1c closes with "The chain witnesses `a`'s structural producibility from its home document via the content sub-allocator chain." L1c closes with the verbatim content↔link twin: "The chain witnesses `ℓ`'s structural producibility from its home document via the link sub-allocator."
**Problem**: The formal `(t₀, …, tₙ)` existential with `t₀ = origin(a)`, `tₙ = a`, and the per-step constraints already *is* the producibility statement. The trailing sentence re-describes it in prose and contributes no claim — and it is duplicated across the two invariants in different words. This is essay content occupying an invariant slot, the kind of meta-prose the precise reader must skip.
**Required**: Drop the trailing sentence from both C1c and L1c; the formal chain stands on its own.

### Issue 2: L0 body embeds the C-clause discharge that the inductive matrix already carries
**ASN-0093, L0 (SubspacePartition)**: "the C-clause is a derived substrate invariant, proved at the new content key by FirstEmission / DisjointSubAllocatorChains — the sub-allocator discipline (`b_C(d) = inc(d, 2)` landing at `s_C`) yields `E(a)₁ = s_C`."
**Problem**: This is the discharge argument sitting in the invariant *statement*. The inductive-step matrix already carries it, more precisely, in the L0 / K.α row ("E(a)₁ = s_C read from the pinned emission — FirstEmission (first-emit) / DisjointSubAllocatorChains (subsequent-emit, a = inc(a_prev, 0) ∈ A_C(d))"). The body version is the weaker copy: it collapses the first-emit/subsequent-emit split into a single gloss, so a reader who trusts it gets an incomplete picture and must cross-check the matrix anyway. Two paragraphs asserting the same discharge, one of them imprecise.
**Required**: In L0's body, state only that the C-clause is a derived substrate invariant (L-clause inherited); leave the FirstEmission / DisjointSubAllocatorChains discharge to the matrix row that already performs it.

## OUT_OF_SCOPE

### Topic 1: Referential integrity between content and arrangement
The substrate proves C2 (`origin(a) ∈ dom(M)`) and M2 (`M(d) = ∅`), so content is scoped to documents that hold the empty arrangement. The S3-style coupling that would relate content addresses to V-positions only becomes meaningful once arrangement-mutation primitives populate `M(d)`.
**Why out of scope**: Arrangement mutation (K.μ family) is explicitly deferred; there is no V-position state to bind content to yet.

META: ASN-0093 defines substrate state, three allocation operations, and the structural invariants they preserve — it remains a system-guarantee specification, not implementation mechanics.

VERDICT: REVISE
