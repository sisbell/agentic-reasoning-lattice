# Review of ASN-0127

I checked every lemma derivation, re-ran the worked illustration's arithmetic, verified the witness constructions in F-IMG-SWING and D-NONMONO against the K.μ~ admissibility constraints, and confirmed the foundation citations resolve to the correct claims. Detailed findings below.

## REVISE

None. The substantive points I stress-tested all hold:

- **F-IMG-SWING witnesses.** Both abstract witnesses reindex correctly. Injective: `M(d): v₁↦a, v₂↦b`, `W={v₁}`, `π=(v₁ v₂)` gives `image(W,d,Σ')={Σ.M(d)(v₂)}={b}` — equal cardinality, membership moved. Non-injective: `v₁↦a, v₂↦a, v₃↦b`, `π(v₁)=v₁, π(v₂)=v₃, π(v₃)=v₂` yields `Σ'.M(d): v₁↦a, v₂↦b, v₃↦a` and `image={a,b}` — a genuine cardinality gain with `ran` preserved. The companion image-shrinking witness checks out too. Crucially, the bijection-equation direction (`Σ'.M(d)=Σ.M(d)∘π⁻¹`) is applied consistently throughout.

- **D-NONMONO injective regime — the load-bearing existence claim.** The lemma correctly does *not* claim image-incomparability transfers to the discovery set (`findlinks` is monotone but not order-reflecting), and rests non-monotonicity on the *existence* of an incomparable discovery swing. That witness — the worked illustration's `{L_1}↦{L_2}` lateral swing under `π=(v_1 v_2)` — is in the injective regime, is genuinely incomparable, and is a valid K.μ~ (length/subspace-preserving, link-subspace-fixing vacuous, non-trivial net effect, post-state shape invariants preserved since the domain is fixed). The cardinality-changing variant `{L_1}↦{L_2,L_2'}` with image cardinality pinned at 1 is also correct and is a sharp illustration that discovery-set cardinality is not pinned even when image cardinality is.

- **Restriction decomposition (Phase 1).** The distinction between full-arrangement blocks (which would *overstate* the image when straddling W's boundary) and C1a's W-confined blocks (whose I-extents union *exactly* to the image) is correct and load-bearing. `f|W` maps each block's V-extent bijectively onto its I-extent, so `⋃ⱼ I(βⱼ)` is the image even under content sharing where I-extents overlap.

- **E-CONS exclusion direction.** The `a∈dom(Σ.L)` branch is correctly closed by E-INV: matching at Σ' forces matching at Σ, contradicting `a∉findlinks(I,Σ)`, leaving only path-created links. Both directions discharged.

- **D-CWP.** `A=A∪B ⟺ B⊆A` reduction is correct, with `A=findlinks(image(W,d_q,Σ'),Σ)` (F-INERT-bridged) and `B=findlinks(Δ,Σ)`; the total-clearance boundary is exercised in the existence-vs-discovery-zero illustration bullet.

- **F-PRES frame audit.** Every cited frame includes `L'=L` under the *amended* K.μ⁺ and K.μ⁻ (the unamended ASN-0047 K.μ⁺/K.μ⁻ frames omit it, but the ContentSubspaceRestriction and PerSubspaceContractionScope amendments add it); K.δ, K.α, K.ρ, K.μ⁺_L, and the derived K.μ~ frame all carry it. Vocabulary coverage is exhaustive: F-PRES+F-LAMBDA partition the entire K-vocabulary for fixed-I results, and D-NONMONO's four cases partition it for discovery results.

- **Foundation usage.** `image` is a genuine new primitive (forward V-region→I-address), not a reinvention of ASN-0098's backward `project`; `matches` legitimately generalizes LP12's per-slot existential from `ran(Σ.M(d))` to arbitrary `I`. The dual-keystone framing (F-CIL for the store-fixed lane, LP13 for the existence lane) is sound — F-CIL's `Σ.L=Σ'.L` hypothesis genuinely fails under K.λ on a `→*` path, which is why E-INV must route through LP13 instead. No non-foundation cross-references.

- **Worked illustration.** The `{x}`-as-canonical-unit-endset shorthand is explicitly defined; the pairwise prefix-incomparability premise (siblings on `A_C(d)` via T10a.2, plus `a_θ` in subspace `s_L`) correctly drives every `coverage({a_i})∩I = {a_i}∩I` reduction; all conforming-link side-conditions (arity ≥ 3, non-empty slot 3, admissible empty slot 2) are respected.

## OUT_OF_SCOPE

### Topic 1: Content-keyed query naming addresses through Σ.C
**Why out of scope**: The note explicitly treats only the arrangement-mediated case and raises the Σ.C-keyed variant as Open Question 1. This is a distinct primitive, correctly deferred.

### Topic 2: Uniform weakest precondition across the whole K-vocabulary
**Why out of scope**: D-CWP computes the wp for the K.μ⁻ contraction instance and Open Question 3 scopes the uniform characterization (extension, reorder, off-document) as future work. Providing one non-trivial wp and naming the general case as open is the right boundary.

### Topic 3: Composition with ASN-0098's link projection displacement
**Why out of scope**: `image()` (forward) and the LP** results (backward) both consult Σ.M; their composition ("project a link, then test the projection against a content region") is named in Open Question 4 and not addressed here. Legitimate future territory, not a gap in this note.

VERDICT: CONVERGED
