# Review of ASN-0131

I read this as a query-operation note: it defines `RE(W, d, Σ)`, establishes a soundness/completeness contract, composition laws, a contraction weakest-precondition, and a full stability characterization. I checked the load-bearing arguments rather than the trivial reads.

**Proofs verified sound:**

- **RE-ADDR (fresh-output addressability).** The chain holds: `ℓ_new ∈ nullified(Σ')` requires a `L_Θ^{Σ'}` to-set covering it; unit-depth discipline gives `coverage(G') = {u : t ≼ u}` with `t ∈ dom(Σ'.L)`; FlatLinkDomain's antichain forces `t = ℓ_new`; P-tgt + freshness rules out every pre-existing tuple; the sole residual nullifier is `ℓ_new` self-retracting. The arity-independence claim is justified — the argument never consults `ℓ_new`'s endset content for `K ≁ Θ`.
- **The `Σ.L`-evolution bridge.** I confirmed `Σ.L` moves only through `K.λ` (every other operation frames `L`), and that `K.δ`-created documents meet `K.σ`'s precondition (M0), giving the inclusion *ASN-0047 `Σ.L`-configs ⊆ ASN-0086 `→*`-reachable*. The note correctly separates plain `→*`-reachable lemmas (R0a, R-Scope) from the layer-reachable unit-depth fact, discharging the latter via the standing commitment along the replayed sequence. This cross-model bridge is exactly the rigor required to apply ASN-0086 here, not a hand-wave.
- **RE-UDIST / RE-UDIST-∩.** Image-union distribution and the touch-disjunction give union-equality cleanly. The intersection result is the strongest novel content and it is correct: `⊆` unconditional; `⊇` refuted by *both* a non-injective and an *injective* two-span counterexample (the latter exploiting split witnesses `a`, `b` in the existential `touch_W`); the necessary-and-sufficient touch-implication on the region-independent pool `Avail(Σ)` is properly derived, and the "no arrangement restriction recovers `⊇`" claim is justified because the obstruction lives in endset structure, which no arrangement constraint can touch.
- **RE-CWP.** The WP derivation is correct: `image(W,d,Σ') = I_R` (D-CWP bridge), `K.μ⁻` frames `Σ.L` so `Avail` is fixed, dropped pairs are exactly those with `coverage(e) ∩ I_R = ∅ ∧ coverage(e) ∩ Δ ≠ ∅`, and the `R = ∅` boundary collapses correctly to `RE = ∅`. It is genuinely finer than D-CWP (same-endset vs. cross-slot rescue).
- **RE-RET.** The iff is sound under its two stated hypotheses. The emitter `b`'s from/to slots are content-disjoint unconditionally (the unit-depth field-agreement argument, reused with citation), R-Scope confines the nullification to `ℓ`, and L12 + the framed image preserve any other live bearer. The forward/backward halves both close.
- **Worked instance.** I recomputed it: `a₄ = shift(a₂,2)` (TS3) so `e₁`'s first span covers `[a₂,a₄)` ∋ `a₂,a₃`; the `e₃ ∩ dom(C) = ∅` separator-zero argument is rigorous; `RE = {(1,e₁)}` and every read-off (RE-OVL/CLIP/WHOLE/UNIT) checks out.

**Anti-bloat scrutiny.** Given the classifier, I examined the dense meta-sections specifically. The bridge, the standing-assumption scoping, and the per-transition no-effect inventory in the stability section are all load-bearing: cutting the bridge would make the ASN-0086 citations unjustified across the state-model boundary; cutting the inventory would force "by similar reasoning" over `K.α`/`K.δ`/`K.ρ`, which the standards prohibit. The forward-reference signposts I found (the `addressable` trailing sentence on where the discipline matters; the `touch_W` subscript note) carry real conceptual content (static addressability is discipline-independent) or legitimate notation-introduction. No relocated-finding prose, no axiom-rationale padding, no duplicated paragraphs (the field-agreement argument is reused by citation, not repeated). The length is driven by the review standards' own demands, not accretion.

## REVISE

(none)

## OUT_OF_SCOPE

The seven Open Questions correctly scope the deferred territory — whole-endset vs. touching-spans (OQ1), multiplicity (OQ2), V-rendered answers (OQ3), the structurally-restricted intersection-sufficiency condition (OQ4), cross-store completeness (OQ5), type-slot/content matching (OQ6), and link-subspace regions (OQ7). The reliance on ASN-0086's discipline commitment as a standing assumption (since ASN-0047's `K.λ` does not itself enforce Nullify-shaped retraction) is the one dependency a future ASN might discharge, but the note states it explicitly and conditions RE-ADDR/RE-RET on it, which is a legitimate within-scope move rather than a gap.

VERDICT: CONVERGED
