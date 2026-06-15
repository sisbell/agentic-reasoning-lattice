# Review of ASN-0131

## REVISE

### Issue 1: The K.λ stability case-split omits the self-emit Nullify

**ASN-0131, §"Stability...", paragraphs "Under link emission." and "Under retraction." (with RE-ADDR, RE-EDIT)**:

The stability analysis for `K.λ` transitions is presented as exhaustive but splits into only two shapes:

- "Under link emission" — explicitly restricted to *"a non-retraction emission (`K ≁ Θ`)"*, shown addressable by RE-ADDR and monotone-additive;
- "Under retraction" — RE-RET, withdrawing a *pre-existing* addressable link `ℓ`, with the load-bearing R-Scope step assuming the fresh emitter `b` is distinct from `ℓ` (*"Its to-set covers `ℓ`, not `b` (`ℓ ≠ b`, both in the flat antichain)"*).

ASN-0086's `Nullify` admits a third shape through P-tgt's self-emit branch: `Nullify(Σ, d_retr, a)` with `a = a_emit(Σ, d_retr)` — a fresh emission that retracts *its own emitter address*. This is `K ~ Θ` (so branch (a)'s `K ≁ Θ` excludes it) and has emitter = target (so RE-RET's "withdraw pre-existing `ℓ`, `ℓ ≠ b`" does not apply). RE-ADDR itself singles this case out — its guarantee is precisely for outputs *"that do not retract their own emitter address"* — so the ASN treats the self-retraction as live, yet the stability section never closes it. R-Scope (ASN-0086) and the wp Case 1 of ASN-0086 both cover the self-emit branch, so it is a genuine layer transition, not an excluded one.

**Problem**: A case-split offered as covering "every transition" leaves the self-emit Nullify unestablished. The outcome is in fact benign — by RE-ADDR's excluded branch the born-nullified emitter `b` is non-addressable (surfaces nothing); by R-Scope at target `= b`, `{t : b ≼ t} ∩ dom(Σ'.L) = {b}`, so it nullifies only its own address and removes no pre-existing addressable bearer; with `Σ.M(d)` framed, `RE(W, d, Σ') = RE(W, d, Σ)`. But the note does not show this. The reader cannot verify benignity from the analysis as written, and "Showing three operations preserve an invariant does not establish that all operations do."

**Required**: Add the self-emit Nullify to the `K.λ` case-split — one sentence stating it emits a born-nullified, non-addressable link (RE-ADDR's excluded branch) that nullifies only its own address (R-Scope at target = emitter), adding no addressable bearer and removing none, hence leaving `RE(W, d, ·)` unchanged.

### Issue 2 (anti-bloat): anticipatory use-site inventory in §"Fresh emissions"

**ASN-0131, §"Fresh emissions and the addressable population", opening**: *"`Σ.L` evolves only through `K.λ` — the arrangement movers (`K.μ` family), entity creation `K.δ`, provenance recording `K.ρ`, and content allocation `K.α` all frame the link store (`L' = L`, ASN-0047/ASN-0093)."*

**Problem**: This is a use-site inventory of which transitions frame `Σ.L`, but the section's deliverable (RE-ADDR) consumes none of it — its proof uses only the single-`K.λ`-step post-state, freshness (`ℓ_new ∉ dom(Σ.L)`), the prefix-antichain (the *following* sentence, R0a), the unit-depth discipline, and P-tgt. The "only `K.λ` changes `Σ.L`" fact is the premise actually used in §"Stability," which independently re-establishes the same per-transition frames ("*Content allocation `K.α` frames both stores... Provenance recording `K.ρ`... Entity creation `K.δ`...*"). The inventory thus sits a section early and duplicates §Stability. (Relatedly, the §Stability `K.ρ` treatment double-justifies the same conclusion — *"framing `M'(d) = M(d)` and `L' = L` ... — equivalently, its projection-invariance is LP14"* — two routes where one suffices.)

**Required**: Drop the anticipatory clause (retain the load-bearing antichain sentence), letting §Stability carry the frame inventory where it is consumed; keep a single justification for `K.ρ`'s invariance.

## OUT_OF_SCOPE

None to add. The seven Open Questions appropriately defer future territory (whole-endset vs. touching-spans return value, multiplicity preservation, V-rendered answers, a structurally-checkable intersection-equality condition, cross-store residence, type-slot matches against content, link-subspace regions), and the note correctly cites rather than rebuilds ASN-0127's image machinery and existence/discovery taxonomy.

Note for the record: the technical core is sound. RE-NCD's separator-zero argument is correct; RE-ADDR's fresh-output reasoning (antichain + freshness + unit-depth to-set) holds; RE-UDIST and the one-sided RE-UDIST-∩ (with both the non-injective and the injective split-witness counterexamples) are correct, including the necessary-and-sufficient touch-implication characterisation; RE-CWP's weakest precondition reduces correctly (`coverage(e) ∩ image ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅` ⟺ `coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅`) and its boundary `R = ∅` collapse is right; and RE-RET's iff is established in both directions under its stated hypothesis. The worked instance verifies RE-OVL/RE-CLIP/RE-WHOLE/RE-UNIT against a concrete state.

VERDICT: REVISE
