# Review of ASN-0131

I checked the definition, the load-bearing lemma (RE-ADDR), the worked instance, the composition laws, the weakest-precondition analysis, and the full stability case-split. Below I record where I pushed hardest and what held, then the correctly-deferred territory.

## Verification performed (no REVISE items found)

**RE-DEF and `I ⊆ dom(Σ.C)`.** For `v ∈ W ∩ dom(Σ.M(d))` with `subspace(v) = s_C`, S3★ (ASN-0047) gives `Σ.M(d)(v) ∈ dom(Σ.C)`, so the image lands in content. The `Avail(Σ)`-factoring (`RE = {(i,e) ∈ Avail : touch_W(e)}`) is valid precisely because `touch_W(e)` is independent of the witness `a`, so `∃a:(P(a,e) ∧ touch_W(e)) = (∃a:P(a,e)) ∧ touch_W(e)`. Sound.

**RE-ADDR.** Traced it: under unit-depth discipline every `L_R^{Σ'}` to-set covers `{u : t ≼ u}`; R0a's prefix-antichain forces `t ≼ ℓ_new ⟹ t = ℓ_new`; pre-existing targets lie in `dom(Σ.L)` so differ from fresh `ℓ_new`; hence only a self-targeting `ℓ_new` is nullified. Arity-independence holds because the argument never inspects `ℓ_new`'s slots. Sound.

**Worked instance.** Verified `a₂ ⊕ δ(2,#a₂) = shift(a₂,2) = a₄`, so the first span of `e₁` covers `{a₂,a₃}` and excludes `a₄`; `a₁ ⋠ a₂` (siblings, equal length, differing last component) so `e₂` misses; the `e₃`-vs-content separator-zero argument is correct (a shared third zero forces `E(c)₁ = E(θ)₁ ≠ s_C`). `RE = {(1,e₁)}` is right, and each tagged claim (RE-OVL/CLIP/WHOLE/UNIT) reads off it correctly.

**RE-UDIST-∩.** The `⊆` direction rests on the general forward-image fact `image(W₁∩W₂) ⊆ image(W₁) ∩ image(W₂)` (no injectivity), correct. The `⊇` counterexample is complete and valid: two distinct V-positions mapping to one `a` (M13/M14), `ℓ_e` addressable by RE-ADDR, `W₁∩W₂ = ∅` forcing `RE(W₁∩W₂) = ∅`.

**RE-CWP.** Re-derived independently: with `I_R ⊆ image(W,d,Σ)` and `Avail` frame-fixed, `RE(Σ')=RE(Σ)` iff `coverage(e)∩Δ≠∅ ⟹ coverage(e)∩I_R≠∅` for all available `(i,e)` (using `(A∨B)⟹A ≡ B⟹A`). Boundary `R=∅` collapses to `RE(W,d,Σ)=∅`. Matches.

**RE-RET.** Both halves discharged. Backward: R-Scope (`{t:ℓ≼t}∩dom(Σ'.L)={ℓ}`, arity-independent, carried by the `Σ.L`-evolution bridge) keeps every `ℓ'≠ℓ` addressable, L12 fixes its value, the `K.λ` frame fixes the image — so a co-borne pair survives. Forward: emitter `b`'s slots (`∅`, content-disjoint unit-depth to-set, and `Θ` under the stated hypothesis) cannot re-witness a content-touching pair, so a sole-borne pair drops. The hypothesis `coverage(Θ) ∩ dom(Σ.C) = ∅` is honestly carried as a condition and routed to OQ6.

**Stability case-split.** Checked every transition: K.μ⁺/K.μ⁻/K.μ~ move only the image (F-IMG-MONO/CONTR/SWING); K.α, K.δ (incl. document registration via LP8), K.ρ, and `d'≠d` edits leave both `Σ.M(d)` and `Σ.L` fixed; the link-subspace-confined edits (K.μ⁺_L and content-retaining K.μ⁻) leave `image(W,d,·)` fixed under `W ⊆ s_C`. The ASN-0082 insert/delete depth-scoping (`#p=2` delete, `#p≥2` insert) matches the foundation's I3/D-SHIFT preconditions exactly, and the bare-shift gap state is correctly excluded as a non-queryable non-atomic intermediate.

I found no hand-waves, no skipped boundary cases (empty image, no addressable links, empty endset slot all handled in RE-BND), no over-claims, and no cross-ASN references outside the foundation set. The note defines a query operation and its state-guarantees abstractly — not implementation mechanics — so it is in scope and not META.

On the anti-bloat dimension: the `Σ.L`-evolution bridge is established once and cited thereafter rather than re-derived; the transfer-justification ("no `dom(Σ.M)` hypothesis," "regardless of arity") is substantive scope-setting, not padding; the deferrals point to distinct Open Questions. I did not find an instance where meta-prose obscured a claim badly enough to flag.

## OUT_OF_SCOPE

### Topic 1: Unconditional retraction stability (retraction-type coverage)
**Why out of scope**: RE-RET's `coverage(Θ) ∩ dom(Σ.C) = ∅` is genuinely unprovable here — ASN-0086 leaves the retraction type's coverage unconstrained (type endsets may reference anywhere, L4/L9). The conditional statement is the most this ASN can establish; the unconditional version is correctly routed to Open Question 6.

### Topic 2: Link-subspace region queries (`W ⊆ s_L`)
**Why out of scope**: The content-subspace restriction is a caller obligation. A link-subspace region resolves (via S3★) to an image in `dom(Σ.L)`, surfacing anchoring aimed at links and adding a retraction-emitter term to RE-RET. This is new semantic territory, properly deferred to Open Question 7.

### Topic 3: Whole-endset vs touching-spans surfacing; multiplicity; rendered answers; intersection-equality refinement
**Why out of scope**: RE-WHOLE is honestly held provisional pending Open Question 1; the deduplication/multiplicity question (OQ2), the V-rendered mode (OQ3), and the injectivity refinement of RE-UDIST-∩ (OQ4) are all future-ASN refinements, not defects in the present formulation, which proves the unconditional facts (RE-CLIP universal, `⊆` unconditional) and exhibits the `⊇` failure.

VERDICT: CONVERGED
