# Review of ASN-0127

## REVISE

### Issue 1: D-ZERO's gloss of a discovery zero drops the region qualifier
**ASN-0127, Anchoring: existence vs discovery, D-ZERO**: "A discovery zero `findlinks_disc(W, d_q, Σ) = ∅` asserts that no link in `dom(Σ.L)` is presently reachable from `d_q`'s arrangement at `Σ`."

**Problem**: As stated, this is false for proper sub-regions. `findlinks_disc(W, d_q, Σ) = ∅` asserts only that no link's coverage meets `image(W, d_q, Σ)` — reachability *through the queried region* — not that no link is reachable from `d_q`'s arrangement at all. The document-level reading is exactly the F-FULL specialization (`W ⊇ dom(Σ.M(d_q))`), and the ASN's own distinction between F-FULL and general `W` is what this sentence collapses. Counterexample from the ASN's own worked material: at the contracted state `Σ₁` of the "Rise under K.μ⁺" bullet (`dom(Σ₁.M(d)) = {v_1}`, `v_1 ↦ a_1`), take `W' = {v_2}`. Then `image(W', d, Σ₁) = ∅` so `findlinks_disc(W', d, Σ₁) = ∅` — a discovery zero — yet `L_1` is discoverable from `d` at `Σ₁` (slot-1 coverage `subtree(a_1)` meets `ran(Σ₁.M(d)) = {a_1}`, LP12). The lemma's third sentence already speaks of the "consulted arrangement" and "the region's image"; the first sentence must match.

**Required**: Region-qualify the assertion — e.g., "asserts that no link in `dom(Σ.L)` is presently reachable through the queried region's image `image(W, d_q, Σ)`" — or state it as the faithful unfolding "no link's coverage meets `image(W, d_q, Σ)`."

### Issue 2: the four-position incomparable witness needs pairwise distinctness of `a, b, c`
**ASN-0127, Phase 1, F-IMG-SWING (availability taxonomy)**: "with `Σ.M(d) : v₁ ↦ a, v₂ ↦ b, v₃ ↦ c, v₄ ↦ a` (so `a` is shared by `v₁` and `v₄`) and `W = {v₁, v₂}`, … the transposition `π = (v₂ v₃)` yields … `image(W, d, Σ') = {a, c}` — `⊆`-incomparable with `{a, b}`"

**Problem**: The incomparability conclusion requires `a`, `b`, `c` pairwise distinct, and the stated conditions do not secure this. The witness-admissibility paragraph guarantees only "at least two distinct values" (K.μ~'s precondition) and a non-trivial net effect (which forces `b ≠ c`, since `b = c` would make the transposition a value-level no-op). Neither excludes `a = c`. Take `a = c` with `a ≠ b`: the arrangement `v₁ ↦ a, v₂ ↦ b, v₃ ↦ a, v₄ ↦ a` satisfies every admissibility condition the paragraph claims for the witness (two distinct values, non-trivial effect `M'(v₂) = a ≠ b`, length/subspace preservation, K.μ~-FIX), yet `image(W, d, Σ') = {a}` ⊊ `{a, b}` — containment motion, not incomparable motion. The injective witness states its distinctness explicitly ("injective, `a ≠ b`"); this witness omits the analogous hypothesis that its conclusion depends on.

**Required**: State "`a, b, c` pairwise distinct" (or equivalently `c ∉ {a, b}` alongside `a ≠ b`) in the four-position witness.

### Issue 3: duplicated role/emphasis prose (anti-bloat)
**ASN-0127, three locations**:

1. **Phase 2, F-MATCH**: "A link matches the I-address set when *some* slot's coverage meets it. The existential over slots is essential: a multi-slot link that meets `I` in any one slot is matched." — The second sentence restates the first (∃-over-slots semantics) with no new content.
2. **The two-phase composite, after F-V**: "The factoring is what makes the stability analysis tractable: each phase consults only one of `Σ.M(d)` and `Σ.L`, so the composite's stability decomposes accordingly." — This repeats the intro paragraph's "The two phases are independent — Phase 1 consults `Σ.M`, Phase 2 consults `Σ.L` — and the stability properties of the composite are determined by which state component each operation moves."
3. **The stability keystone, F-CIL-perlink**: the sub-lemma is bracketed by two statements of the same role — the introduction "A weaker per-link form is the residual that F-LAMBDA applies at each prior key" and the derivation tail "The weaker hypothesis is load-bearing under K.λ, where `dom(Σ'.L) = dom(Σ.L) ∪ {ℓ_new} ≠ dom(Σ.L)` makes F-CIL's global hypothesis fail…". The tail sits inside the proof slot and explains why the sub-lemma is needed rather than what it establishes; the intro already names the consumer.

**Problem**: Each fact is stated twice in nearby prose; this is exactly the duplication and consumer-justification accretion the anti-bloat classifier targets, and a reader following the derivations must step around it.

**Required**: Keep one statement per fact. For F-CIL-perlink, retain the precise justification (the `dom`-change reason F-CIL's hypothesis fails) in at most one location — either the introduction or F-LAMBDA's application site — and drop the other; for F-MATCH and the F-V tail, delete the restating sentence.

## OUT_OF_SCOPE

### Topic 1: composite-boundary characterization of `findlinks_V` (fork and the uniform wp)
The per-elementary-step results lift across paths by induction (F-INERT) and the contraction wp is computed (D-CWP), but a boundary-to-boundary characterization for named composites — e.g., what `findlinks_V(W, d_new, ·)` is at the boundary of a fork that populates `d_new` from `d_op`, or the uniform weakest precondition across the whole K-vocabulary — is new territory the ASN itself defers (Q3, Q4).

**Why out of scope**: This is a follow-on ASN's subject matter; the elementary-step algebra here is complete on its own terms and the ASN explicitly registers the open questions.

VERDICT: REVISE
