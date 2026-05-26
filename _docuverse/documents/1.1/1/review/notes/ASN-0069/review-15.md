# Review of ASN-0069

## REVISE

### Issue 1: V0 effects table cites V5/V5a for a universal frame condition that requires composite frame composition

**ASN-0069, V0 Effects (non-empty case)**: "`(A d' : d' ≠ d_new : M'(d') = M(d'))                (V5, V5a)`"

**Problem**: V5 establishes only `M'(d_src) = M(d_src)` — a specific instance for `d_src`. V5a is explicitly stated as governing *subsequent* transitions after the fork (`Σ' →* Σ''`), not the fork composite itself. The universal frame condition over all `d' ≠ d_new` during the fork composite must be derived from the elementary frame conditions composed: K.δ's frame `M¹(d') = M(d')` for `d' ≠ d_new` (when `IsDocument(e)`), K.μ⁺'s frame `M²(d') = M¹(d')` for `d' ≠ d_new`, and K.ρ's frame `(A d :: M'(d) = M(d))`. As cited, the table misleads a future reader into believing V5/V5a discharge the universal claim.

**Required**: Replace the citation with "(V5 for `d' = d_src`; K.δ + K.μ⁺ + K.ρ frame conditions for `d' ≠ d_src ∧ d' ≠ d_new`)" or equivalent.

### Issue 2: V10(a) cites T10a.6 to rule out a cross-allocator equality that cannot arise

**ASN-0069, V10(a)**: "T10a.7 (EnumerationInjectivity, ASN-0034) applied to `A_v(d_src)`'s enumeration gives distinct addresses at distinct indices; T10a.6 (DomainDisjointness) rules out cross-allocator equality. So `d_new¹ ≠ d_new²`."

**Problem**: V1 places *both* `d_new¹` and `d_new²` in `A_v(d_src)`'s domain — they are siblings in the same allocator's enumeration. T10a.6 (DomainDisjointness across *distinct* allocators) has no purchase here because there is no cross-allocator relationship to rule out. T10a.7 alone — injectivity of the indexing map within `A_v(d_src)` — is both necessary and sufficient. The extraneous citation reads as if the proof needed to discharge an obligation that does not exist, and a reader might infer that V10(a) covers a case (e.g., `d_new²` produced by a different allocator) that V1 has already foreclosed.

**Required**: Drop the T10a.6 sentence; the T10a.7 step alone closes the argument. If the intent is to flag that V1 fixes both emissions to `A_v(d_src)` (precluding cross-allocator confusion), say so explicitly and cite V1.

### Issue 3: V8b derivation conflates Corr_g and Π_g when arguing K.μ⁺_L invariance

**ASN-0069, V8b derivation**: "K.μ⁺_L extends only `V_{s_L}` of its target document, so the content-subspace projection feeding `Corr_g` — restricted to `dom(M_g(d_src)) ∩ dom(M_g(d_new))` — is unchanged on either side"

**Problem**: `Corr_g` as defined in V8b is *not* restricted to the content subspace — it ranges over all V-positions in the intersection of domains. The phrase "content-subspace projection feeding `Corr_g`" is opaque: the derivation should either argue (a) `Corr_g` itself is unchanged by K.μ⁺_L (which is true, because a single K.μ⁺_L on `d_src` adds `v_L` only to `dom(M_g(d_src))` and not to `dom(M_g(d_new))`, and even a pair of K.μ⁺_L on both would fail the equality conjunct by CL-OWN forcing distinct link origins), or (b) `Π_g = F ∩ Corr_g` is unchanged because `F` excludes link-subspace positions. The current phrasing collapses the two arguments and leaves the reader to reconstruct which mechanism is at work.

**Required**: Pick one mechanism and state it cleanly. Option (b) is the simpler line: "K.μ⁺_L extends only `V_{s_L}`; `F ⊆ V_{s_C}(d_src)` so `F ∩ V_{s_L} = ∅`; therefore `Π_g = F ∩ Corr_g` is unchanged regardless of any link-subspace effect on `Corr_g`."

## OUT_OF_SCOPE

None — the ASN's Open Questions section correctly defers concurrency, transcluded-source forks, snapshot-vs-living semantics, descendant discoverability, fork-size bounds, version-graph presentation, intra-session fork chains, V-stream depth renumbering, and post-fork source deletion to future ASNs.

VERDICT: REVISE
