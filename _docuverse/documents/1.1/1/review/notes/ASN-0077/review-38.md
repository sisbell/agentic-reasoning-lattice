# Review of ASN-0077

## REVISE

### Issue 1: O0(b)/O0a take on an ungrounded vocabulary-completeness assumption that foundations already discharge

**ASN-0077, O0(b) and O0a**: "we fix the working frame's complete elementary transition vocabulary once and assert its exhaustiveness… `{K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ} ∪ {K.σ}`… **Frame-vocabulary exhaustiveness:** … no transition outside these nine modifies Σ."

**Problem**: The dom(L) half of the semantic correspondence ("`origin(ℓ)` names the document that allocated `ℓ`") is made to rest on (a) a *complete* transition vocabulary whose exhaustiveness is asserted, not derived, and (b) K.σ, a transition with no defining foundation ASN — only its M-effect is recoverable (via LP8 of ASN-0098). The completeness claim cannot be discharged from the foundation ASNs, so a load-bearing, central guarantee of the operation (origin = allocating document for links) is grounded on an unverifiable premise. This is gratuitous: the **Allocator hierarchy** definition of ASN-0047 already states that every output `ℓ` of `A_L(d)` satisfies `origin(ℓ) = d`, and L1c (LinkAllocatorConformance) already ties every `ℓ ∈ dom(L)` to a chain rooted at `origin(ℓ)` with `k₁ = 2` (descent into the document's link sub-allocator), with SubAllocatorAxiom (e) supplying disjointness. These foundation facts deliver "origin(ℓ) = its allocating document" directly, without any K.λ-event closure and without any vocabulary-completeness assumption.

**Required**: Ground O0(b)'s dom(L) correspondence (and O0(c)'s dom(L) totality) in L1c + SubAllocatorAxiom (Allocator hierarchy) alone, and delete the frame-vocabulary-exhaustiveness apparatus and K.σ dependency — or, if the K.λ-event closure is genuinely necessary for something L1c/SubAllocatorAxiom do not give, state precisely what that is. As written, the proof imports an assumption it does not need into the system's defining attribution guarantee.

### Issue 2: The frame-vocabulary exhaustiveness derivation is restated three times nearly verbatim

**ASN-0077, O0(b), O0(c), O0a**: the per-transition L-closure / C-closure inspection ("K.λ's effect clause `L' = L ∪ …` is the only effect that names `L`… every other transition either declares `L' = L` … K.σ … by the frame-exhaustiveness assumption …") appears in full in O0(b), is paraphrased again in O0(c), and is then re-extracted verbatim as O0a.

**Problem**: O0a is by its own admission "exactly the closure step established within O0(b)." The triplicated prose enlarges the load-bearing surface a reviewer must verify without adding content, and obscures which single fact O5/O6/O11★★ actually consume (none of them depend on the closure — O5 uses P3 + O3 purity). This is the sprawl-blinds-review failure mode: the same argument copied across three sites invites drift between copies on the next edit.

**Required**: State the closure once (as O0a, if retained per Issue 1), and have O0(b)/O0(c) cite it rather than re-derive it. If Issue 1 is taken, much of this collapses automatically.

## OUT_OF_SCOPE

### Topic 1: Link-origin reporting from an I-span
The I-span lift drops `dom(L)` addresses by definitional choice; the ASN flags this as Open Question 1. Correctly deferred — not an error here.

### Topic 2: Surfacing the intermediate transclusion chain, native-vs-transcluded distinction, and historical containment from Σ.R
The ASN explicitly excludes these (the "What SHOWORIGIN does not promise" section) and routes them to Open Questions. Each is genuinely a separate operation/ASN, not a gap in this one.

VERDICT: REVISE
