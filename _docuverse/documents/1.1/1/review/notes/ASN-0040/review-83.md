# Review of ASN-0040

## REVISE

### Issue 1: Disjointness and ordering re-derive foundation results instead of reducing to them

**ASN-0040, S0 and B7**:
- S0: "`(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`" proved "from TA5(a), T1."
- B7: "`S(p, d) ∩ S(p', d') = ∅`" proved via a multi-case length/prefix argument "from S(p,d), S1, T3, T4/TA5-SigValid, TA5(d)."

**Problem**: `S(p, d)` (base `c₁ = inc(p, d)`, then `cₙ₊₁ = inc(cₙ, 0)`) is structurally identical to a T10a allocator domain (`dom(A) = {tₙ}`, `tₙ₊₁ = inc(tₙ, 0)`, base a child-spawn output `inc(p, k')` with `k' ∈ {1,2}`). The foundation already proves the exact properties this ASN re-derives:
- **S0** restates T10a.7 (EnumerationInjectivity), whose contract explicitly concludes "the enumeration is strictly increasing under the tumbler order T1." S0 cites neither.
- **B7** restates T10a.6 (DomainDisjointness), which proves `dom(X) ∩ dom(Y) = ∅` for *all* distinct allocators (covering both the length-separation/ancestor-descendant case and the prefix-incomparability case that B7 re-walks by hand). B7's Depends omits T10a.6 entirely.

Standard #7 requires foundation results be used, not reinvented. The genuinely new content in B7 is only the *namespace-injectivity* fact — that distinct **B6-valid** `(p, d)` map to distinct streams, which is precisely what the aliasing remark (`([1,0],1)` vs `([1],2)`) shows fails without B6(i). That part is worth proving; the disjointness core is not.

**Required**: Reduce S0 to T10a.7 and B7 to T10a.6. Establish the `(p, d) → allocator` correspondence and the B6-injectivity that excludes aliasing, then cite T10a.6 for disjointness rather than re-proving via T3/T4/TA5-SigValid/TA5(d). If a deliberate decision keeps baptism independent of the T10a allocator framework, state and justify it — but the current text neither cites nor distinguishes the foundation theorems it duplicates. (B8 Case 1/Case 2 inherit this: their distinctness machinery is T10a.7 + B7; only the *co-reachability* framing is novel and should be all that remains as new argument.)

### Issue 2: Forward-reference announcement that carries no reasoning

**ASN-0040, State space and transitions**: "The partition of Σ that governs registry growth is fixed at B0a."

**Problem** (anti-bloat / forward-reference accretion): the sentence only announces where a later claim lives; it advances no argument. The reader learns the partition exists but nothing about it until B0a. This is exactly the meta-prose around forward references the `review-mode.anti-bloat` classifier flags. (Relatedly, B0a's baptismal-operation clause defines its effect via `next(s.B, p, d)` and "the operation specified by Bop below," both defined many sections later — a functional forward dependency that is tolerable for an axiom but is what the announcement sentence is compensating for.)

**Required**: Delete the announcement sentence; let B0a speak where it is stated.

### Issue 3: Implementation color in B2's structural slot

**ASN-0040, B2**: "No counter distinct from the data, no free list, no reservation table."

**Problem**: the load-bearing claim — that `#children` is a sufficient statistic for the next allocation — is already made by the surrounding sentence. The free-list / reservation-table enumeration is implementation commentary that does not advance the high-water-mark argument.

**Required**: Drop the enumeration; keep the "sufficient statistic" statement.

## OUT_OF_SCOPE

### Topic 1: B3 ghost-validity forward requirement

**Why out of scope**: B3 introduces `Occupied : T × 𝒮 → {⊤, ⊥}` and constrains future content-storage operations. Content storage is explicitly out of scope. B3 is correctly framed as a *forward requirement* on a future ASN rather than as a content-storage claim, and ghost elements are intrinsic to baptism's meaning (Nelson), so this is acceptable placement — but it is content-layer territory, not a baptism invariant, and should not accrete operational detail in future cycles.

VERDICT: REVISE
