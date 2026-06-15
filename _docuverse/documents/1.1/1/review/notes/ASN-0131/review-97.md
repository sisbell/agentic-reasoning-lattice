# Review of ASN-0131

I reviewed this note for correctness (every claim, boundary, and proof), for the anti-bloat patterns the classifier flags, and for the cite-don't-rebuild discipline its scope demands. I worked the proofs rather than the summaries.

**Correctness — verified, not waved through:**

- **RE-NCD** is sound. Tracing `s ≼ c` for `c ∈ dom(Σ.C)`: the three separator zeros of `s` carry onto `c`; since `zeros(c) = 3` those *are* `c`'s separators; `s`'s last component is nonzero (T4) so the third zero sits strictly before `#s`, placing the subspace-identifier position `z₃+1 ≤ #s` inside the agreement range — forcing `E(c)₁ = E(s)₁ ≠ s_C`, contradicting L0. Holds.
- **RE-ADDR** is sound. The flat antichain `dom(Σ'.L)` (R0a) plus unit-depth retraction discipline confine any nullifying cover of `ℓ_new` to a tuple *targeting* `ℓ_new`; freshness rules out pre-existing such tuples; only a self-emitter qualifies. The standing assumption is correctly scoped to the addressability results.
- **RE-CWP** is a genuine weakest precondition. Verified `post ⊆ pre` always (D-CWP bridge `image(Σ') = I_R`), so equality reduces to "no surfaced pair drops," and the implication `coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅` over `Avail(Σ)` is equivalent whether quantified over `Avail` or `RE(Σ)` (vacuous on non-touching pairs). The `R = ∅` collapse to `RE(Σ) = ∅` checks out. The per-endset-vs-per-link contrast with ASN-0127's D-CWP is correct and load-bearing.
- **RE-UDIST-∩** is genuinely necessary-and-sufficient (verified both directions), and the two `⊇`-failure constructions correctly separate the obstructions: the first exploits non-injective image non-distribution, the second the split-witness phenomenon *under an injective arrangement* — the note is right that no injectivity restriction discharges it.
- **RE-RET** biconditional holds under its stated hypothesis. `nullified(Σ') = nullified(Σ) ∪ {ℓ}` (R-Scope confines the fresh nullification to `ℓ`; the fresh emitter `b` is not nullified and, under `coverage(Θ) ∩ dom(Σ.C) = ∅`, contributes nothing to a content image), so `addressable(Σ') = (addressable(Σ) ∖ {ℓ}) ∪ {b}` — both halves of "sole bearer iff drops" follow.
- **Boundaries** are covered: empty image, no addressable links, empty endset slot (RE-BND); `d ∉ dom(Σ.M)` excluded by precondition; link-subspace `W` deferred (OQ7). The **worked instance** is arithmetically correct (`a₂ = inc(a₁,0) = shift(a₁,1)` since content addresses are T4-valid; first span covers `[a₂, a₄)` ∋ `a₂, a₃`) and exercises RE-OVL, RE-CLIP, RE-WHOLE, per-endset surfacing, and RE-UNIT simultaneously.
- The **stability sweep covers the complete ASN-0047 vocabulary** plus the ASN-0082 displacement lift — no operation is skipped, and the `Σ.L`-only / `Σ.M(d)`-only factoring (via `nullified` depending on `Σ.L` alone) is correctly used to dispatch the framing transitions.

**Anti-bloat / forward-reference accretion:** I looked specifically for the flagged patterns. The forward references (OQ1–7) are crisp one-shot deferrals to distinct locations, not repeated pointers to one spot. The motivational containment-vs-overlap passage and the clipping illustration are concrete examples/analogies, which the guidance explicitly excludes from meta-prose. The `Θ` rename of ASN-0086's retraction type `R` is collision-forced (this note carries `Σ.R` for provenance and `R` for K.μ⁻ retention sets) and explicitly bridged — disambiguation, not parallel vocabulary. The exhaustive stability enumeration produces real per-transition results (RE-EDIT, RE-CWP, RE-RET), and the five "framing" transitions correctly split into two distinct mechanisms (entire-`Σ.M(d)` frame vs. content-subspace-image preservation), so they do not collapse to one line. I found no relocated-finding residue, no axiom-rationale prose (there is no new axiom), and no use-site/consumer inventories on the definitions.

**Cite-don't-rebuild:** §Existence-and-discoverability and §transclusion *apply* ASN-0127's taxonomy and ASN-0098's LP16 (deriving `sel = findlinks_V ∩ addressable`, RE-TRANS, RE-IDENT) without reproving E-MONO/D-NONMONO/D-ZERO. The image machinery is cited (F-IMG), not rebuilt.

## REVISE

None.

## OUT_OF_SCOPE

None. The note stays in its lane — it withholds link identities (RE-UNIT) rather than enumerating them, disclaims counting, and references FINDLINKSFROMTOTHREE only to contrast scope.

VERDICT: CONVERGED
