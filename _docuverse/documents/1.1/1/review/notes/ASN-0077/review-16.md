# Review of ASN-0077

## REVISE

### Issue 1: O11 and O11' establish equality, not just inclusion — framing as "monotonic growth" understates

**ASN-0077, O11 and O11'**: claims `origins_V(Σ, d, σ) ⊆ origins_V(Σ', d, σ)` for K.μ⁺ and K.μ⁺_L transitions, framed as "V-span monotonic growth".

**Problem**: Under the V-span operation's well-formedness precondition (vi), both transitions exactly preserve `origins_V(·, d, σ)` for fixed σ — equality, not strict inclusion. The framing "monotonic growth" misleads readers to expect that K.μ⁺ or K.μ⁺_L might introduce new origins; in fact no new origin ever enters origins_V on a fixed well-formed σ under these transitions.

The missing ⊇ direction (not derived in the ASN): Fix `o ∈ origins_V(Σ', d, σ)` with `v ∈ ⟦σ⟧ ∩ dom(M'(d))` and `origin(M'(d)(v)) = o`. Either (i) `v ∈ dom(M(d))`, so `M'(d)(v) = M(d)(v)` by K.μ⁺'s mapping preservation, giving `o ∈ origins_V(Σ, d, σ)`; or (ii) `v ∈ dom(M'(d)) ∖ dom(M(d))`, which is impossible — by D-SEQ★, new K.μ⁺ positions occupy `V_{s_C}(d)` indices `> n_C`, while precondition (vi) at Σ on σ covering indices `[k_1, k_1 + n - 1]` forces `k_1 + n - 1 ≤ n_C`. Hence the smallest new position has last-component value `≥ n_C + 1 ≥ k_1 + n = reach(σ)`'s last component, placing it at or beyond `reach(σ)` and outside `⟦σ⟧`. Symmetric for K.μ⁺_L (one fresh `v_ℓ` past `max(V_{s_L}(d))` ≥ σ's max index by (vi)).

The worked example corroborates equality rather than strict growth: K.μ⁺ across Σ₀ → Σ₁ for d₃'s native [d₃.0.1.1], [d₃.0.1.2] adds positions [1,1,6], [1,1,7] beyond any well-formed σ over [1,1,1]..[1,1,5]; `origins_V` on that σ is `{d₁}` at both states. To exhibit strict inclusion under K.μ⁺ one would need a V-span well-formed at both states yet picking up new positions — which (vi) forbids.

**Required**: Either (a) strengthen O11 and O11' to equality with full derivation including the ⊇ direction, or (b) note that the inclusion holds with equality under the operation's preconditions and revise the claim labels from "monotonic growth" to "preservation" (or "invariance"). Option (a) is preferable since downstream proofs about attribution permanence under arrangement-extending operations likely need the stronger result.

### Issue 2: O4's transclusion-by-reference prose lacks foundation grounding

**ASN-0077, "Direct resolution through transclusion" section preceding O4**: "Because each transclusion is by reference rather than copy, the I-address recorded in every intermediate document's arrangement is the *same* — it points to the bytes baptised by d₁."

**Problem**: This motivational claim establishes O4's hypothesis (each `d_i` has `M(d_i)(v_i) = a`) but is presented without grounding in the foundation operations that produce this state:
- **J4 (ForkComposite, ASN-0047)** for fork-based transclusion: `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})` propagates I-addresses through fork chains by range inclusion;
- **K.μ⁺ (ArrangementExtension, ASN-0047)** for general transclusion extensions: the precondition `a ∈ dom(C)` admits any allocated I-address as a target, including foreign ones.

The formal O4 derivation is correct from its stated hypothesis, but readers verifying that real transclusion scenarios satisfy O4's hypothesis must trace through J4 and K.μ⁺ themselves; the connection between "transclusion by reference" and `M(d_i)(v_i) = a` is left implicit.

**Required**: Cite J4 (and K.μ⁺'s permissive precondition) in the prose immediately before O4 to ground the by-reference principle. A sentence such as "K.μ⁺'s precondition `a ∈ dom(C)` admits any allocated I-address as a transclusion target, while J4 (ForkComposite) propagates ranges through forks; together they realize O4's hypothesis along any chain of transclusion operations" would close the gap.

## OUT_OF_SCOPE

None — the six listed Open Questions appropriately defer cross-subspace I-span handling, transitive provenance, native-vs-transcluded distinction, unreachability behavior, historical containment, and intra-document sharing to future ASNs.

VERDICT: REVISE
