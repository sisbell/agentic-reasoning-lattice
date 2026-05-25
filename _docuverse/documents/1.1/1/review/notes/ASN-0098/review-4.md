# Review of ASN-0098

## REVISE

### Issue 1: LP19 proof cites LP3★ unnecessarily

**ASN-0098, LP19 (proof of the consequence)**: "The coverage of `e` is unchanged across `Σ_post →* Σ_{n+1}` by LP3★ (applied through whichever link slot carries `e`), so `a_new ∉ coverage(e)` still holds at `Σ_{n+1}`."

**Problem**: Throughout the lemma, `e` is treated as a free-standing endset value, not as the slot of a specific link. `coverage(e)` is a deterministic function of `e`'s spans (per ASN-0043's coverage definition); it has no state-dependence at all. LP3★ is about preservation of `Σ.L(a).eᵢ` across transitions — applicable only when the endset is bound to a particular link slot. The parenthetical "applied through whichever link slot carries `e`" papers over this mismatch: if `e` is bound to a link, the lemma should say so; if not, LP3★ isn't needed and its invocation is misleading.

**Required**: Replace the LP3★ citation with "since `coverage(e)` is a function of `e`'s spans, which are fixed because `e` is itself a fixed value across the sequence" — or alternatively, restate the lemma so that `e` is explicitly the endset at a specific link slot of a specific link, in which case LP3★ can be applied directly to the slot.

### Issue 2: LP2 and LP3 proofs gloss over the `a ∈ dom(Σ'.L)` conclusion

**ASN-0098, LP2 (proof)**: "This follows from L12 (ASN-0043) by component projection on the sequence: equal sequences have equal entries at every position."

**Problem**: The equality `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` requires both sides to be well-defined. The LHS requires `a ∈ dom(Σ'.L)`. L12 of ASN-0043 supplies *both* conclusions — `a ∈ dom(Σ'.L)` AND `Σ'.L(a) = Σ.L(a)` — but the LP2 proof only invokes the second. The membership conclusion is needed for the slot accessor on the LHS to be defined; without it, the equation has no referent. LP3's proof, which derives from LP2, inherits the same gloss.

**Required**: In LP2's proof, note explicitly that L12 establishes both `a ∈ dom(Σ'.L)` (so the LHS is well-defined) and `Σ'.L(a) = Σ.L(a)` (so equality at slot `i` follows by component projection). LP3's proof then chains correctly.

### Issue 3: K.δ from ASN-0047 not explicitly addressed

**ASN-0098 (Frame Conditions section, LP5–LP8, LP14)**: The frame lemmas enumerate K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.α, K.λ, K.σ, K.ρ. K.δ from ASN-0047 — for creating nodes, accounts, and (under ASN-0047's vocabulary) documents — is never named.

**Problem**: ASN-0098 cites both ASN-0047 and ASN-0093 as foundations. ASN-0047's K.δ creates entities of three kinds: K.δ-IsNode and K.δ-IsAccount leave `M(d')` unchanged for every `d'`, so LP4 yields invariance trivially; K.δ-IsDocument creates a new document with `M(d_new) = ∅`, which is exactly LP8's K.σ scenario. The behaviour is derivable, but the ASN's claim to characterize every transition's effect on projection is incomplete in nomenclature. A reader auditing operation-by-operation will look for K.δ and not find it.

**Required**: Add a brief lemma or remark — one paragraph — noting that K.δ for IsNode and IsAccount leaves every `M(d)` unchanged (LP4 yields invariance), and K.δ for IsDocument is subsumed by LP8's argument. Or state explicitly that K.σ (ASN-0093) is the document-registration operation in this ASN's reference frame, superseding K.δ-IsDocument from ASN-0047, and that the remaining K.δ cases reduce to LP4.

### Issue 4: Quantifier scope in LP6, LP7, LP14

**ASN-0098, LP6**: "By LP4 applied to every `d`: `project(e, d, Σ') = project(e, d, Σ)` for every endset `e` and every `d`, whenever `Σ → Σ'` is a K.α transition."

**Problem**: `project(e, d, Σ)` is defined only when `d ∈ dom(Σ.M)`. The unrestricted "every `d`" is ill-formed for `d ∉ dom(Σ.M)`. The same problem appears verbatim in LP7 (K.λ) and LP14 (K.ρ). Since K.α, K.λ, and K.ρ all preserve `dom(M)`, the intended restriction is `d ∈ dom(Σ.M) = dom(Σ'.M)`, but this is not stated.

**Required**: Restrict each quantifier explicitly: "for every `d ∈ dom(Σ.M) = dom(Σ'.M)`". The amendment is one phrase per lemma.

### Issue 5: Worked example abstracts span-to-coverage relation

**ASN-0098, "A Worked Trace"**: "A link `a` with endset `e₁ = {(i₀, ℓ)}` covering I-addresses `{i₁, i₂, i₃, i₄}`, where `i₀ ≤ i₁ < i₂ < i₃ < i₄ < i₀ ⊕ ℓ`..."

**Problem**: A span `(i₀, ℓ)` covers `{t ∈ T : i₀ ≤ t < i₀ ⊕ ℓ}` per T12 — the entire half-open interval, not just the four named I-addresses. The trace silently treats `coverage(e₁) = {i₁, i₂, i₃, i₄}`, conflating geometric coverage with the I-addresses currently allocated. The projection at LP12 depends on `coverage ∩ ran(M(d))`, which is a subset of `coverage`. A reader following the lemmas literally will recognize the trace is implicitly conflating these, and the prose does not signal the abstraction.

**Required**: Either (a) state explicitly that `coverage(e₁) ⊇ {i₁, i₂, i₃, i₄}` and these four are precisely the addresses in `coverage(e₁) ∩ ran(Σ.M(d₁))` for the example's purposes, or (b) explicitly acknowledge the simplification ("for trace clarity we treat the four addresses as the entirety of `coverage(e₁)` that bears on the arrangements considered").

## OUT_OF_SCOPE

The seven open questions enumerated at the close of the ASN — reverse discovery, V-order preservation under K.μ~, contiguous-V-range expressibility of projections, link-to-link endset references, partially-unallocated coverage at creation, cross-document "same edit sequence" comparisons, and fork composites without link-subspace transclusion — are properly deferred. Each names a topic that would require its own invariants and lemmas; none of them is a gap in *this* ASN's stated subject of "displacement of an existing link's projection under arrangement-modifying operations".

VERDICT: REVISE
