# Review of ASN-0131

I checked the core definition, the worked instance, every derived claim, the weakest-precondition analysis, the two cross-model lifts (to ASN-0086 and ASN-0082), and the exhaustiveness of the stability case split. I report what I verified, then the verdict.

## Verification performed

**RE-DEF / RE-SND / RE-CMP.** Soundness and completeness are the two directions of the set-builder biconditional and are genuinely immediate, as claimed. The factoring `RE(W,d,Σ) = {(i,e) ∈ Avail(Σ) : touch_W(e)}` is valid because `touch_W(e)` is independent of the witness `a`, so it pulls out of the existential — this is load-bearing for RE-UDIST and it holds.

**Worked instance.** Checked each touch test. `e₁`'s first span `(a₂, δ(2, #a₂))` covers `{t : a₂ ≤ t < shift(a₂,2)} = [a₂, a₄)`, so `{a₂,a₃} ⊆ coverage(e₁)` (⊆, sufficient for the touch). The `e₃` disjointness argument is sound: agreement on `1..#θ` forces all three of `θ`'s zeros onto `c`, which (with `zeros(c)=3`) makes the third zeros coincide and forces `E(c)₁ = s_type ≠ s_C`. Result `{(1, e₁)}` is correct and exercises RE-OVL, RE-CLIP, RE-WHOLE, per-endset surfacing, and RE-UNIT.

**RE-UDIST.** Image-of-union distributivity (one-line, correct), touch-distributes-as-disjunction, and `Avail` region-independence compose correctly. The decision to leave intersection open is right — the forward image fails to distribute over intersection under non-injective `M` (M13/M14), and the inclusion-and-strictness reasoning is correct.

**RE-CWP.** Re-derived: `RE(Σ') = {(i,e) ∈ Avail : coverage(e) ∩ I_R ≠ ∅}` vs `RE(Σ) = {(i,e) ∈ Avail : coverage(e) ∩ (I_R ∪ Δ) ≠ ∅}`; equality reduces exactly to `coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅`. `Avail` fixity follows from K.μ⁻ framing `Σ.L` (extended-state `L'=L`) and `nullified` being a function of `Σ.L` alone. The `R = ∅` boundary collapses correctly to `RE(Σ) = ∅`. The contrast with D-CWP (endset-level vs link-level) is real and correctly drawn.

**RE-RET.** The hardest argument; checked in full. (i) `b` is addressable: wp Case 2 conjunct 2 holds via `b ∉ coverage(G)` (flat antichain, `ℓ ≠ b`), conjunct 3 via the unit-depth discipline + R0a. (ii) `b`'s from/to slots are content-disjoint unconditionally — the unit-depth field-agreement argument transfers because the to-set width is fixed at `δ(1,#ℓ)` and `ℓ` is a genuine link address (`E(ℓ)₁ = s_L`, L0/L1). (iii) The `coverage(Θ)` hypothesis is correctly identified as the *sole* non-theorem (the field argument does not reach wide-span interiors) and deferred to OQ6. (iv) The "drops iff sole bearer" iff: forward direction uses R6a + the hypothesis; backward uses R-Scope's single-tuple confinement (`{t:ℓ≼t} ∩ dom(Σ'.L) = {ℓ}`) to keep every other bearer addressable with value fixed (L12) and image fixed (`M'=M`). Both directions hold. The link-permanence-vs-pair-removal distinction is a genuine subtlety and correctly resolved.

**Cross-model bridges.** The ASN-0086 bridge ("`Σ.L` evolves only through K.λ in both models, so Σ.L-only lemmas hold verbatim") is sound — every ASN-0047 link-affecting op except K.λ frames `Σ.L`, and R6a/R-Scope/R0a/wp Case 2 are all Σ.L-only. The M-only lift for ASN-0082's shifts is a legitimate embedding stipulation (the displacement primitive writes only `Σ.M(d)`, reads `Σ.C`), correctly flagged as a lift and consistent with the framing every ASN-0047 mover already carries.

**Exhaustiveness of RE-EDIT.** The combined vocabulary {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ} ∪ {insert, delete} is fully covered; the link-subspace-confined class (K.μ⁺_L and content-retaining K.μ⁻) is correctly shown image-fixed under `W ⊆ s_C`, and the depth-independence note correctly observes RE-EDIT's M-only carrier is not bound by D-SHIFT's `#p = 2` realisation (a sound, hedged robustness statement, not an over-claim).

**Mechanics.** All citations resolve to the provided foundations (0034/0036/0043/0047/0058/0082/0086/0093/0098/0127); no non-foundation ASN numbers are cited; sibling operations named in prose (FINDLINKSFROMTOTHREE) are not ASN-number references. Boundary cases (empty image, no addressable links, empty endset slot) are all in RE-BND. No notation is reinvented (the `R`/`Σ.R`/`Θ`/`θ` deconfliction is genuine clash-avoidance with explicit identification).

## REVISE

(none)

## OUT_OF_SCOPE

The note's seven Open Questions correctly defer genuinely new territory (touching-spans-vs-whole rendering, multiplicity preservation, V-rendered answers, intersection-composability, non-co-resident link stores, type-slot/content matches, link-subspace regions). None of these is an error in this ASN, and the note does not define claims for any of the out-of-scope operations (it cites ASN-0127's image/taxonomy and ASN-0098's projection machinery rather than rebuilding them). Nothing to add.

## Anti-bloat assessment

I searched specifically for the flagged patterns. The cross-model bridge paragraphs (ASN-0086 import validity; M-only lift) read as load-bearing rather than gratuitous — the note draws on two foundations with different state models and must justify importing their Σ.L-only / Σ.M-only lemmas into the full state. The transition enumeration in RE-EDIT is required exhaustiveness, not padding. The few prose restatements I found (e.g., the pure-query gloss, the soundness paraphrase) are "statements of what the operation does," which the directive's own carve-out exempts. The M-only lift prose was the locus of recent tightening and now reads cleanly. I did not find accreted meta-prose that obstructs following any claim.

VERDICT: CONVERGED
