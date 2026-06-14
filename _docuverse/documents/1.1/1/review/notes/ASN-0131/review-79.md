# Review of ASN-0131

This is a careful, largely sound note. The core definition (RE-DEF), the union law (RE-UDIST), the intersection necessary-and-sufficient condition (RE-UDIST-∩), the contraction weakest precondition (RE-CWP), and the worked instance all check out under verification. The fresh-output addressability argument (RE-ADDR) is complete in its case analysis. The findings below are targeted gaps, not structural problems.

## REVISE

### Issue 1: Permanence of nullification cites R6a alone, which does not cover ASN-0047's full transition vocabulary

**ASN-0131, "Under retraction" and "Two senses of permanence"**: "Retracting ℓ removes ℓ from addressable(Σ) permanently (R6a)" and "The *specific retracted link's* membership in addressable is gone forever (R6a)."

**Problem**: "Permanently / gone forever" means `ℓ ∈ nullified(Σ')` for *every* ASN-0047-reachable `Σ'`. But ASN-0086's R6a is a one-step lemma over ASN-0086's transition relation `→ ≡ K.σ ∪ K.α ∪ K.λ` (Definition — StateTransition, ASN-0086). ASN-0047's vocabulary additionally contains K.δ, K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~, and K.ρ — none of which is an ASN-0086 `→` step. R6a, as cited, does not discharge persistence across these. The note's own `Σ.L`-evolution bridge is explicitly stated to transfer *state* lemmas ("any ∀-quantified ASN-0086 →*-reachable Σ.L-lemma carries to every ASN-0047-reachable state"), not transition lemmas over the larger vocabulary. R-Scope is fine here (it concerns the single Nullify = K.λ step, which is in `→`); it is the multi-step permanence that is under-cited.

The note has the ingredients — it establishes that "`nullified(Σ)` ... is a function of the link store `Σ.L` alone" and that the non-K.λ transitions frame `Σ.L` — but never assembles them into the permanence argument, while citing R6a as if it covered the whole path. Given this note's otherwise meticulous per-step discharge (the bridge, the frame inventories), the gap is conspicuous.

**Required**: At the permanence claims, add that the non-K.λ transitions (K.δ, K.μ-family, K.ρ) frame `Σ.L`, so `nullified` is preserved across them (it being a `Σ.L`-function), with R6a covering only the K.λ steps — or recast the import as `nullified`'s monotonicity in the `Σ.L`-configuration (which the bridge does transfer), so the chain closes over the full ASN-0047 vocabulary.

### Issue 2: The "survives every arrangement restriction" claim (RE-UDIST-∩) overreaches its proof

**ASN-0131, "Composing regions"** (and the claims table, RE-UDIST-∩): "The second obstruction lives in `touch_W` itself, and it survives *every* arrangement restriction, injectivity included" / "with no arrangement restriction recovering it."

**Problem**: What is rigorously demonstrated is narrower: counterexample 2 refutes *injectivity*, and the prose argues the split-witness obstruction is structural to `touch_W`. But the universal claim is false for degenerate arrangements: if `dom(Σ.M(d))` cannot furnish two disjoint regions with distinct nonempty images (e.g., a single active V-position), then `W₁ ∩ W₂` shares that position whenever both images are nonempty, `image(W₁ ∩ W₂)` is nonempty, and `⊇` holds vacuously. The split-witness obstruction is only *constructible* when two disjoint regions admit distinct nonempty images — exactly the case the two counterexamples assume. The injectivity-specific claim ("an arrangement restriction such as injectivity ... provably cannot recover") is sound; the unqualified universal is not. (The note's exact result — the necessary-and-sufficient touch-implication — is correct and unaffected.)

**Required**: Qualify the universal — e.g. "no *injectivity-style structural* restriction recovers `⊇`," or "the obstruction is constructible under any arrangement admitting two disjoint regions with distinct nonempty images" — rather than asserting it survives *every* arrangement restriction.

### Issue 3 (anti-bloat): Use-site preview in the addressable introduction

**ASN-0131, "The unit of the answer"**: "The retraction *discipline* — which constrains the way the withdrawn set grows — bears only on what a fresh emission, and what a retraction step, each leave addressable."

**Problem**: This sentence previews the two downstream sections (fresh emission → RE-ADDR; retraction step → RE-RET) rather than advancing the meaning of `addressable` at the point of its introduction — the "definition's introduction enumerates downstream consumers" pattern. A reader following the `addressable` definition does not yet need to know where the discipline will be exercised; the prior two sentences ("`addressable` depends on `Σ.L` alone, never on *how* a retraction was performed") already make the load-bearing point. This is the weakest of the three items, and the sentence can be read as a subtle state-function/transition-discipline separation point; flagging it for the reviser's judgment.

**Required**: Cut the sentence, or fold its separation point into the preceding two without naming the downstream use-sites.

## OUT_OF_SCOPE

None. The note correctly defers future territory (rendered answers, link-subspace regions, multi-store completeness, type-region matching, multiplicity, whole-vs-touching-spans, the structurally-restricted intersection condition) to its Open Questions rather than defining claims for them, and references only foundation ASNs (0034, 0036, 0043, 0047, 0058, 0082, 0086, 0093, 0098, 0127).

VERDICT: REVISE
