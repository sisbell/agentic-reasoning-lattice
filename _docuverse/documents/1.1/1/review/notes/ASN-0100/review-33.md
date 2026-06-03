# Review of ASN-0100

This is a careful, thorough specification. The three-region decomposition, the I3 disclaimer analysis, the chain-shift lemma, the forced-ordering/commutativity treatment, and the wp analysis are all rigorous. I found two defects in the invariant-preservation arguments.

## REVISE

### Issue 1: M2 misapplied to the whole extended-state arrangement

**ASN-0100, §"Per-subspace span decomposition (S8★)"**: "The post-state content-subspace decomposition is finite and well-defined; its existence is also guaranteed independently by C1a applied to the restriction `M'(d)|_{V_{s_C}(d')}` (preconditions discharged below), with M2 applying directly to the whole post-state arrangement `M'(d)`."

**Problem**: M2 (DecompositionExistence, ASN-0058) carries the precondition S3 (ReferentialIntegrity, ASN-0036): `ran(M(d)) ⊆ dom(C)`. M2 was stated in ASN-0058's content-only model. In the ASN-0047 extended state the post-state arrangement `M'(d)` includes link-subspace positions mapping into `dom(L)`, so `ran(M'(d)) ⊄ dom(C)` — S3 fails for the whole arrangement. This is not hypothetical: case (i.b) of the substrate decomposition explicitly has `V_{s_L}(d) ≠ ∅`. M2 therefore cannot be applied "directly to the whole post-state arrangement `M'(d)`." The whole-arrangement satisfies S3★, not S3.

**Required**: Delete the "with M2 applying directly to the whole post-state arrangement" clause. The primary argument already routes through C1a (per-subspace restriction, where the content-subspace range is `⊆ dom(C)` and the link-subspace range is `⊆ dom(L)`), which is correct; the link subspace is handled by S8★'s trivial length-1 decomposition. The redundant M2-on-whole-arrangement remark is the only place the error appears.

### Issue 2: S8★ not verified at the composite's intermediate states

**ASN-0100, §"Atomicity and Canonical Order"**: "We verify that each intermediate state in INSERT's substrate decomposition satisfies the per-state invariants."

**Problem**: ASN-0047's ExtendedReachableStateInvariants lists S8★ (PerSubspaceSpanDecomposition) among the per-state invariants. The atomicity section groups the trivially-preserved invariants (entity-set family, S4, link-store family, C-fin, S3★-aux) and then does per-step analysis for "the invariants whose preservation requires non-trivial argument" — but S8★ appears in neither group. S8★ ranges over `M`, which changes at the K.μ⁻ and K.μ⁺ intermediates, so it is not trivially preserved. In particular, at the K.μ⁻ intermediate (content subspace truncated to the Left prefix) S8★ is left unaddressed, despite the dedicated S8★ section verifying it only at the post-state Σ'. The claim that "each intermediate state satisfies the per-state invariants" is therefore not discharged for S8★.

**Required**: Add per-intermediate verification of S8★. The K.μ⁻ intermediate's content subspace is a contiguous prefix `{[s_C,1,…,1,k] : 1 ≤ k < p_m}` (or empty), whose single-subspace restriction admits a decomposition by C1a/M11; the K.α and K.ρ intermediates leave `M` unchanged so S8★ inherits; the K.μ⁺ intermediate coincides with the post-state already verified.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion, COPY, DELETE, REARRANGE, version derivation, replication
**Why out of scope**: The ASN's "Bounding the Scope" section and Open Questions correctly defer these; no claim drift into them.

VERDICT: REVISE
