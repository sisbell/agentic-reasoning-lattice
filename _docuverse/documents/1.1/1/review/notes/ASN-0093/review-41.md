# Review of ASN-0093

## REVISE

### Issue 1: L0 mis-cited for the not-yet-committed key in SubsequentEmissionFreshness
**ASN-0093, Lemma (SubsequentEmissionFreshness), cross-subspace bullet**: "*Cross-subspace* (against `dom(L)`): `E(a)₁ = s_C` (read along `A_C(d)` via L0 / DisjointSubAllocatorChains) while `E(ℓ)₁ = s_L` for every `ℓ ∈ dom(L)` (L0)"
**Problem**: At the freshness-check point `a ∉ dom(C)` (it is the candidate about to be committed). L0's C-clause quantifies over `dom(C)`, so it cannot supply `E(a)₁ = s_C` for `a` — that would be circular. Only DisjointSubAllocatorChains (structural, `a ∈ A_C(d)`) licenses the reading. The inductive matrix gets this right (L14, K.α subsequent-emit: "reading `E(a)₁ = s_C` from DisjointSubAllocatorChains, each peer `ℓ ∈ dom(L)` carrying `E(ℓ)₁ = s_L` by IH-L0"), so the lemma text contradicts the matrix.
**Required**: Drop the "L0 /" alternative for the fresh key; cite DisjointSubAllocatorChains alone for `E(a)₁`, reserving L0 for the pre-existing peers `ℓ ∈ dom(L)`.

### Issue 2: Use-site inventory duplicates the per-discipline list that follows it
**ASN-0093, *Sub-allocator chains are ASN-0040 sibling streams***: "Consequently the ASN-0040 results this note consumes — `B6(a)`'s stream-T4-validity conclusion, the `SiblingStream` postconditions, `S0` (StreamOrdering), `S1` (StreamPrefix), `B5a` (SiblingZerosPreservation), and `B7` (NamespaceDisjointness) — apply to `A_C(d)` and `A_L(d)` directly."
**Problem**: This is a use-site inventory: it enumerates the downstream consumers (ChainElementT4Validity ← B6(a), ChainEnumerationInjectivity ← S0, ChainPrefixExtension ← S1, ChainUniformZeroCount ← B5a, DisjointSubAllocatorChains ← B7) immediately before the *Per-chain disciplines* block restates each citation individually. The sentence advances no reasoning the block does not. This is exactly the forward-reference accretion the note's anti-bloat classifier targets.
**Required**: Cut the inventory sentence; the per-discipline block already establishes applicability with its individual ASN-0040 sources. Retain only the single claim that each chain's parent `(b_·(d), 1)` is B6-valid (the actual precondition the block depends on).

### Issue 3: Multiple sections defer to the same "chain exhibition" location
**ASN-0093, C1c/L1c matrix cells and Properties table**: matrix discharges C1c "(see *C1c chain exhibition* below …)"; Properties table row C1c says "(see *C1c chain exhibition*)"; same doubling for L1c.
**Problem**: Two separate sites point at "C1c chain exhibition" (and two at "L1c chain exhibition") — the "multiple paragraphs defer to the same downstream location" pattern. The Properties-table deferral carries no proof obligation; it is a pointer to a pointer.
**Required**: Keep the deferral once, in the matrix cell that bears the discharge obligation. Remove the parenthetical pointer from the Properties table (the Status column already says LEMMA/INV).

### Issue 4: Frame preservation over-justified by "state-independence of E(·)"
**ASN-0093, inductive matrix, C1b (K.σ and K.λ cells), L1b (K.σ, K.α cells)**: "Preserved: `C` in frame — each prior key's `#E ≥ 2` transfers by the state-independence of `E(·)` (State model)."
**Problem**: Under frame `C' = C`, the key set and values are literally unchanged, so the IH `#E(a) ≥ 2` applies to `a ∈ dom(C') = dom(C)` directly. `E(·)` being state-independent is not load-bearing here — `#E(a)` depends only on the address `a`, which is fixed by frame regardless of any state-independence argument. The citation is decorative and the underlying "state-independent projections" paragraph in *State model* exists to support these citations that don't need it.
**Required**: Replace the "by the state-independence of `E(·)`" clauses with the plain frame appeal ("`dom(C)` unchanged, IH transfers"). If no remaining matrix cell genuinely requires the state-independence paragraph, trim that paragraph from *State model* as well.

## OUT_OF_SCOPE

(none — the Scope section cleanly fences arrangement mutation, entity stratification, provenance, coupling, and withdrawal.)

VERDICT: REVISE
