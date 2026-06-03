# Review of ASN-0070

## REVISE

### Issue 1: Setting section forward-references `R(d, e)|_S` and `Σ_V^S` before they are defined

**ASN-0070, The Setting**: "A vacuous subspace S has `R(d, e)|_S = ∅`, and the only admissible V-span-set is the empty sequence `Σ_V^S = ⟨⟩` (V-Restricted Denotation, below)."

**Problem**: This sentence uses `R(d, e)|_S` — which F0 does not introduce until the next section — and `Σ_V^S` together with the vacuous-subspace convention, which the V-Restricted Denotation section defines later (it even parenthetically points "below"). The Setting is meant to fix the foundational backdrop; pre-stating a result about not-yet-defined notation is forward-reference accretion. The same convention is then stated a second time, in full, under V-Restricted Denotation, so the Setting copy carries no load.

**Required**: Remove the `R(d, e)|_S = ∅` / `Σ_V^S = ⟨⟩` sentence from the Setting. Keep only the depth-undefinedness fact ("`m_S(d)` is undefined and `S` is vacuous; next insertion re-pins at any `≥ 2`"); state the vacuous-subspace convention once, where the notation exists.

### Issue 2: F-det derivation re-derives F0's well-definedness

**ASN-0070, F-det derivation, steps 1–2**: "By S2 (ArrangementFunctionality), `M(d)` is a partial function, so its inverse image on any fixed subset of `T` is a single, uniquely determined set. … By the definition of `R` (F0), `R(d, L(ℓ).eᵢ) = M(d)⁻¹(coverage(L(ℓ).eᵢ))`, hence `R(d, L(ℓ).eᵢ)` is uniquely determined…"

**Problem**: This restates, almost verbatim, F0's own "Well-definedness" paragraph ("By S2 … the inverse image of `coverage(e)` is therefore a uniquely determined subset of `dom(M(d))`"). The determinism argument needs only to cite that F0 already establishes `R(d, e)` is uniquely determined; re-running the S2 argument is duplicated prose in different words.

**Required**: Collapse steps 1–2 to a citation of F0's well-definedness ("`R(d, L(ℓ).eᵢ)` is uniquely determined by Σ, d, i — F0"), then proceed to the subspace partition (step 3) and canonical-form steps.

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics under concurrent modification
**Why out of scope**: The note's third Open Question (concurrency guarantees when the queried document is mid-transition) is genuine new territory. `follow` is specified as a state-pure query against a fixed Σ; interleaving semantics belong to a transition/scheduling ASN, not here.

### Topic 2: Cross-document resolution relationships under shared transclusion lineage
**Why out of scope**: The first and third Open Questions (relating `follow(ℓ, d, i)` and `follow(ℓ, d', i)` across documents sharing transclusion lineage or drawing from different homes) require version/lineage structure this note deliberately does not model. F-multidoc correctly establishes only that no document is privileged; the relational guarantee is future work.

VERDICT: REVISE
