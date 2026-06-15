# Review of ASN-0131

I read this as a query-operation specification: it defines `RE(W, d, Σ)` over the abstract state, gives a declarative definition (RE-DEF), soundness/completeness, boundary cases, two algebraic laws, a full per-transition stability analysis, a non-trivial weakest precondition (RE-CWP), and a concrete worked instance. The correctness content is strong — I checked the proofs of RE-NCD, RE-ADDR, RE-UDIST, RE-UDIST-∩ (both failure constructions), RE-CWP, and RE-RET and found them sound. The depth requirements (concrete example, non-trivial wp, derived consequences) are met. No correctness defect, no missing critical edge case, no out-of-scope claims, no drift.

The note carries `review-mode.anti-bloat`, and the findings below are residual accretion plus one precision gap.

## REVISE

### Issue 1: Retraction section restates the emitter-harmlessness analysis twice
**ASN-0131, §Stability ("Under retraction")**: The paragraph beginning "We must ask what the emitter `b` can contribute" establishes that `b`'s three endsets are content-disjoint — from-set "`coverage(∅) = ∅` touches nothing," to-set "RE-NCD applies directly," type-set deferred to a hypothesis. The later paragraph beginning "We therefore record the emitter's harmlessness conditionally" then re-states the same three facts: "With the from-set and to-set already content-disjoint, `Θ` is the emitter's *only* possible content-region contribution ... all three of `b`'s endsets are content-disjoint, `b` is never surfaced."
**Problem**: This is two paragraphs saying the same thing — the second paragraph's first half recaps the from-set/to-set/type-set content-disjointness already established. The reader must re-read the prior analysis to confirm nothing new is added before reaching the load-bearing content.
**Required**: Keep only the genuinely new content of the second paragraph — the net-effect statement ("a retraction's net effect on `RE` is removal only") and the dependency of the forward direction on the hypothesis — and attach it directly after the type-set paragraph, dropping the disjointness recap.

### Issue 2: RE-NCD applied to the retraction to-set without establishing T4-validity
**ASN-0131, §Stability ("Under retraction")**: "The to-set is a unit-depth span ... whose start `ℓ` is genuinely element-level with `E(ℓ)₁ = s_L ≠ s_C` (L0, L1, ASN-0093; SC-NEQ) and is a link address `ℓ ∈ dom(Σ.L)` that `Nullify` targets, so RE-NCD applies directly."
**Problem**: RE-NCD's stated hypothesis is a *T4-valid* element-level address (`zeros(s) = 3`, `E(s)₁ ≠ s_C`). The cited L0/L1/SC-NEQ supply the subspace identifier and `zeros(ℓ) = 3`, but not the T4-validity that RE-NCD's own proof consumes (it agrees `c` with `s` on `1..#s` and counts separator zeros). The worked example discharges this for `θ` by stating it directly ("T4-valid and element-level"); the retraction application omits the corresponding citation.
**Required**: Cite the foundation fact that link-store addresses are T4-valid (StoreT4Validity, ASN-0093) when invoking RE-NCD on `ℓ`.

### Issue 3: RE-ADDR re-derives ASN-0086's UnitDepthRetractionDiscipline rather than citing it
**ASN-0131, §"Fresh emissions and the addressable population"**: "Since `Nullify` emits a tuple whose to-set is a single unit-depth span `{(t, δ(t, #t))}` at a prior link target `t` (ASN-0086's `Nullify`/`Emit_Θ`), and only `Nullify` grows `L_Θ`, every `L_Θ` to-set is unit-depth at a link target."
**Problem**: This re-walks the base/step induction that ASN-0086 already discharges as its UnitDepthRetractionDiscipline commitment ("Discharged for every layer-reachable state by induction"). The conclusion "every `L_Θ` to-set is unit-depth" is a foundation result, restated rather than cited.
**Required**: Adopt the standing discipline commitment and cite the unit-depth conclusion as UnitDepthRetractionDiscipline (ASN-0086); drop the inline re-derivation.

## OUT_OF_SCOPE

None to add. The note's seven Open Questions correctly defer future territory — the touching-spans return value (tied, well, to RE-UDIST), multiplicity preservation, rendered (V-order) answers, the structurally-restricted intersection condition, non-co-resident link stores, type-slot matches against content, and link-subspace regions. The content-subspace restriction is honestly carried as a caller obligation with its dependence acknowledged at the retraction argument ("what the standing `W ⊆ s_C` obligation buys"), and OQ7 owns the link-subspace case.

VERDICT: REVISE
