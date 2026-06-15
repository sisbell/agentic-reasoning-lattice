# Review of ASN-0131

I checked every introduced claim against its derivation, the worked instance against the postconditions it advertises, the boundary cases, and — given the `review-mode.anti-bloat` classifier — the prose around each forward reference. I report what I verified and then the verdict.

## What I verified

**RE-NCD (cross-subspace unit-span disjointness).** The proof is sound. If `s ≼ c` for content `c`, then `c` inherits all three of `s`'s separator zeros; since `zeros(c) = 3` these *are* `c`'s separators, so `s`'s third-zero position is `c`'s, forcing `E(c)₁ = E(s)₁ ≠ s_C`, contradicting `E(c)₁ = s_C` (L0). The implicit step that `E(s)₁` lies within the shared range (`p₃ + 1 ≤ #s`, from the non-empty element field with `s_{#s} ≠ 0`) holds.

**RE-ADDR (fresh-output addressability).** Sound under the standing discipline. Every `L_Θ^{Σ'}` to-set is unit-depth at a target `t ∈ dom(Σ'.L)`; with `dom(Σ'.L)` a prefix-antichain, `t ≼ ℓ_new ⟹ t = ℓ_new`, so only a to-set targeting `ℓ_new` covers it; pre-existing tuples target `dom(Σ.L) ∌ ℓ_new` (P-tgt + freshness); a non-self retraction of `ℓ_new` targets some `ℓ' ≠ ℓ_new` not covering `ℓ_new`. The three-way K.λ partition (non-retraction / retraction-of-other / self-retraction) is exhaustive and each case is placed correctly.

**RE-UDIST and RE-UDIST-∩.** The factorization `RE(W) = {(i,e) ∈ Avail(Σ) : touch_W(e)}` is valid because `touch_W` depends on `e` alone and `Avail(Σ)` is region-independent. The `⊆` half of intersection follows from forward-image `⊆`; the `⊇` failure is correctly exhibited *twice* — once via image non-distribution (non-injective `Σ.M(d)`) and once via the split-witness obstruction with `Σ.M(d)` **injective**, establishing that no injectivity restriction discharges it. The necessary-and-sufficient touch-implication condition is exactly `RE(W₁)∩RE(W₂) ⊆ RE(W₁∩W₂)` unfolded. The claim that the *touching-spans* reading breaks union-distributivity is correct: its return value `e|_{touching}` is region-dependent, so `RE(W₁∪W₂)` would carry one merged restricted endset while `RE(W₁)∪RE(W₂)` carries two distinct ones.

**RE-CWP.** The bridge `image(W,d,Σ') = I_R`, monotone shrinkage `RE(Σ') ⊆ RE(Σ)`, and the drop condition `coverage(e)∩Δ ≠ ∅ ∧ coverage(e)∩I_R = ∅` are correctly assembled into the wp; the per-endset refinement over D-CWP's per-link condition is real and well-argued; the `R = ∅` boundary collapses correctly to `RE(W,d,Σ) = ∅`.

**RE-RET and the newly-added self-retraction case.** The dual effect of a retraction (removes `ℓ`, adds addressable emitter `b`) is handled correctly; `b`'s from- and to-slots are content-disjoint unconditionally (∅ and RE-NCD), and the type-slot `Θ` is honestly carried as a hypothesis with its exception flagged to OQ6. The sole-bearer iff is proven both directions, the backward half via R-Scope confining the nullification to `{ℓ}`. The self-retraction case checks out: `b` is born-nullified hence non-addressable, R-Scope at target = emitter gives reach `{b}`, so `addressable(Σ') = addressable(Σ)` and `RE` is unchanged.

**Worked instance.** Recomputed: `coverage({(a₂, δ(2,#a₂))}) = [a₂, a₄)` contains `a₂, a₃` and excludes `a₄`; `coverage(e₂) = {t : a₁ ≼ t}` misses `a₂`; RE-NCD kills `e₃`. `RE = {(1, e₁)}` is correct, and each of RE-OVL/RE-CLIP/RE-WHOLE/RE-UNIT is genuinely exercised.

**Edge cases** (empty image, no addressable links, empty endset slot, single-position region, subspace-boundary handling via the `W ⊆ s_C` obligation) are all covered. Citations to foundation results spot-check accurate. No non-foundation cross-ASN references appear in the body; named operations (FINDLINKSFROMTOTHREE, etc.) are referenced by name, not number. No out-of-scope topics are given claims — the out-of-scope territory (rendered V-order answer, link-subspace regions, cross-store completeness, BEBE) is correctly held as Open Questions 3/5/7, not as errors.

**Anti-bloat pass.** I examined the prose around every forward reference (OQ1/3/4/6 and the Extent→RE-UDIST forward dependency). Each block does real work: the Extent paragraph's appeal to union-distributivity is the substantive reason RE-WHOLE is adopted; the OQ deferrals are single-purpose and none duplicate a downstream location. The recap of ASN-0127's existence/discovery taxonomy is one cited sentence plus application (RE-SEL), not a rebuild. The "coverage-permanent / selection-mediated" dichotomy recurs across the transclusion and stability framings, but each occurrence anchors a distinct local argument rather than restating idly. I did not find meta-prose a precise reader must skip to follow a claim.

## REVISE

(none)

## OUT_OF_SCOPE

### The provisional return-value clause (RE-WHOLE / OQ1)
The operation's return value is fully defined as written (RE-DEF returns the whole endset `Σ.L(a).eᵢ`); the "provisional" marking flags only a future reconsideration of whole-endset vs touching-spans. The union-distributivity argument already gives a decisive reason to keep whole-endset, and the selection is fully determined under both readings. This is honest deferral, not an incomplete specification.

META: (none — the ASN defines an operation on state with soundness/completeness, stability invariants, and a weakest-precondition analysis, all stated abstractly enough to bind any implementation; it has not drifted into implementation mechanics.)

VERDICT: CONVERGED
