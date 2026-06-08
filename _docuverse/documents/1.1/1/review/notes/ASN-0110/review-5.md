# Review of ASN-0110

## REVISE

### Issue 1: RE-reveal overstates pairing non-recoverability as categorical

**ASN-0110, RE-reveal (observation)**: "From `retrieveendsets(I, Σ)` one recovers, for each role, the set of content regions... One *cannot* recover which from-endset pairs with which to-endset... never 'this from goes with that to.'"

**Problem**: The claim is stated universally but is false in degenerate cases. If exactly one link touches `I` (e.g. a store with a single touching link, or your own worked instance restricted to `a₁` alone), then `E₁`, `E₂`, `E₃` each contain at most one endset and the per-link from/to/type pairing is trivially recoverable. RE-reveal's categorical "one cannot recover" directly contradicts the ASN's own Open Question 3 ("Under what conditions is the per-link from/to/type pairing reconstructible... and when is that reconstruction provably impossible?"), which concedes the property is conditional. The grounding theorem RE-anon establishes only *existence* of indistinguishable states, not universal impossibility.

**Required**: Restate RE-reveal as conditional — pairing is dissolved *in general* / *not guaranteed recoverable*, with the precise conditions deferred to OQ3 — rather than asserting recovery is impossible for every state.

### Issue 2: RE-mono applies a single-step lemma to a multi-step transition

**ASN-0110, RE-mono (lemma)**: "For every reachable `Σ →* Σ'`, `Eᵢ(I, Σ) ⊆ Eᵢ(I, Σ')`. *Proof.* For `(a, i) ∈ W(I, Σ)`: link persistence gives `a ∈ dom(Σ'.L)` with `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` (RE-immut)..."

**Problem**: RE-mono quantifies over multi-step reachable transitions `Σ →* Σ'`, but the cited RE-immut is stated as a single-step lemma ("Across any transition `Σ → Σ'`..."). The proof invokes single-step persistence directly on a `→*` sequence without an induction or a multi-step closure step. The persistence needed is exactly the unconditional multi-step link persistence (LP13, ASN-0098) or the multi-step coverage invariance LP3★, neither of which RE-mono cites in its body.

**Required**: Cite the multi-step persistence result (LP13 / LP3★) for the `Σ →* Σ'` direction, or add the inductive closure of RE-immut, so the proof does not rest single-step persistence on a multi-step hypothesis.

## OUT_OF_SCOPE

### Topic 1: V-space presentation/clipping contract for returned endsets
The ASN repeatedly notes (RE-full, end of "Regions phrased in a document's V-space") that presenting a returned endset back in a querying document's V-coordinates is a separate, lossy projection, and defers its contract to Open Question 1. This is correctly future territory (the I→V presentation layer), not a gap in this operation.

### Topic 2: Sub-region/super-region invariants beyond additive union
RE-add covers union over the region; the richer lattice relation (OQ2) is appropriately deferred — it is new structure, not an error here.

VERDICT: REVISE
