# Review of ASN-0094

## REVISE

### Issue 1: "Strictly increasing under →-steps by R3" wording in Sh0–Sh3 induction framings

**ASN-0094, Sh0/Sh1/Sh2/Sh3 inductive step paragraphs**: Each of the four preservation proofs opens its inductive step with the same imprecise phrasing:

> "`L_K` is monotone non-decreasing along `↦*` — strictly increasing under `→`-steps by R3 (TypedSliceMonotonicity, ASN-0086), equal under `↦ \ →`-steps by LinkStoreInvarianceUnderArrangement (ASN-0086)"

**Problem**: R3 (TypedSliceMonotonicity) gives non-strict monotonicity (`L_K^Σ ⊆ L_K^{Σ'}`), not strict increase. Under `→`-steps, `L_K` is unchanged for K.σ-steps, K.α-steps, and K.λ-steps emitting at any `K' ≁ K`. Strict increase happens only on K.λ-steps at K (or `K' ~ K`), and that strictness comes from R0 (TupleAddressFreshness) supplying a fresh address — not from R3 alone. The next sentence in each proof immediately says "The only effects on L_K are unchanged (Case A) or extended by one tuple (Case B)," directly contradicting the "strictly increasing" claim. The case analyses are correct; only the framing wording is wrong.

**Required**: Reword along the lines of "monotone non-decreasing along `↦*` by R3 on `→`-steps and LinkStoreInvarianceUnderArrangement on `↦ \ →`-steps, with strict increase only on K.λ-steps at K or `K' ~ K` (by R0's freshness)." Apply consistently across Sh0, Sh1, Sh2, Sh3.

### Issue 2: Sub-case II.B counterfactual example for `#w ≥ 2`

**ASN-0094, RetractionTargetNotOnChain *Sub-case II.B example with `#w ≥ 2`* worked example**: The example walks through a hypothetical `a = [1, 0, 2, 0, 5, 8, 0, 7, 1, 0, 3]` with `zeros(a) = 4`, then admits "This `a` is *not* K.λ-emittable for any `d`" and observes "concrete K.λ-emitted addresses *never* admit a `b ≼ a` with `b ∈ dom(Σ.L)` and `#w ≥ 2`."

**Problem**: The Lemma's `a := a_emit(Σ, d)` is by definition K.λ-emittable, so the `#w ≥ 2` regime is unreachable in the Lemma's scope. The "structural observation" paragraph derives the tight bound `#w ≤ 1` for concrete K.λ-emissions from L1 + T4(iv). This means the additivity argument at Step II.1 is proving something the structural constraint already rules out by construction. Either the proof should be simplified to exploit the `#w = 1` structural bound directly (collapsing Step II.1 to a trivial check), or the counterfactual exposition should be replaced with a direct argument showing why Step II.1's general form is needed despite the structural tightness (e.g., it's required for the proof to remain robust under future scaffolding extensions).

**Required**: Either (a) tighten the proof to use the structural `#w ≤ 1` bound and remove the additivity argument's generality, or (b) clarify why the general additivity argument is preserved despite being unreachable at the substrate level — citing the structural-robustness reading explicitly.

### Issue 3: Resolution row standalone admissibility lacks an exhibited example at a distinct K

**ASN-0094, Resolution catalog row + walkthrough**: The catalog row notes "*Standalone admissibility (settled, not exhibited)*" and the worked example "Resolution base templates exercised directly" threads `K_res` through Comment's parametric consumer (the existing K_res emissions ρ_1, ρ_2 from the Comment walkthrough).

**Problem**: The framework claims Sh5(b) admits standalone Resolution use at any registered K without a parametric consumer in scope. But the worked example reuses the same `K_res` that is being consumed parametrically — the standalone path is not actually exhibited at any K independent of the `_via` consumers. A reader cannot verify by inspection that the base templates would compute correctly at a fresh Resolution-shape K with no NonIdempotentDirectedPair consumer in scope; the author's "settled, not exhibited" annotation acknowledges the gap but does not close it.

**Required**: Add a brief standalone walkthrough at a Resolution-shape K (e.g., a hypothetical `K = approved_by` registered independently of any Comment-style relation), exhibiting the five base templates' evaluations and at least one rejection case. The exhibition need not be lengthy — a single emission plus template table would suffice.

### Issue 4: NullifyActiveSubsetCompatibility Case A proof says "in symmetry with Case B's explicit derivation" — but Case A is presented first

**ASN-0094, NullifyActiveSubsetCompatibility Corollary**: Case A's proof reads "We show (i) and (ii) hold at `Σ_target`, in symmetry with Case B's explicit derivation below."

**Problem**: Case A is presented before Case B in the proof body, so forward-referencing "Case B's explicit derivation below" inverts the natural derivation order. The actual argument for Case A (R0a applied at Σ' for single-tuple scope; PrefixSpanCoverage + reflexivity of ≼ + Definition (nullified) at Σ' for stable nullification) is given immediately after the forward reference, so the proof is self-contained — but the "in symmetry with" phrasing is misleading. Either swap the case order so Case B is derived first and Case A reads as "by the same argument with `τ_new` in place of `τ_prior`," or rewrite Case A's preamble to drop the forward reference and lead with the direct derivation.

**Required**: Restructure to either (a) present Case B first with full derivation and Case A as its symmetric counterpart, or (b) rewrite Case A's body to lead with its own direct argument without claiming symmetry with a not-yet-stated Case B.

### Issue 5: ShapeWellFormedness behavior at unregistered `(c_F = 0|1, t_F = -)` is unstated

**ASN-0094, ShapeWellFormedness Definition + *Behavior at `c_F = 0|1`* paragraph**: The behavior paragraph treats `(c_F = 0|1, t_F = A_doc/A_rel/A)` (admitted, since both implications are vacuously satisfied). It also rules out `(c_F = 0|1, t_F = -)` via the implication `t_F = - ⟹ c_F = 0` (consequent fails since `0|1 ≠ 0`).

**Problem**: The exclusion of `(c_F = 0|1, t_F = -)` is *load-bearing*: a row registered at this shape would have `slot_addrs(F) = ∅` on the empty-branch of `0|1` and the F-side of clause (d) would read `∅ ⊆ -^Σ = ∅`, vacuously true. But on the non-empty branch, clause (d) would read `slot_addrs(F) ⊆ -^Σ = ∅`, which forces `slot_addrs(F) = ∅` — contradicting the `c_F = 0|1`-branch claim that `|slot_addrs(F)| = 1`. So `(c_F = 0|1, t_F = -)` makes the non-empty branch uninstantiable. The exclusion is therefore semantically motivated, not merely syntactic. The Definition states the implication mechanically but doesn't explain *why* it's excluded — a reader could misread this as an arbitrary syntactic restriction rather than a substantive admissibility condition.

**Required**: Add one sentence to the *Behavior at `c_F = 0|1`* paragraph explaining the semantic reason for the exclusion: the non-empty branch of `0|1` at `t_F = -` would force `slot_addrs(F) ⊆ ∅`, making `|slot_addrs(F)| = 1` unsatisfiable.

## OUT_OF_SCOPE

### Topic 1: Bipartite completion of the canonical catalog
**Why out of scope**: Missing shape rows (e.g., `(1, 1, A_rel, A_rel, ⊤)`, `(1, 1, A_rel, A_doc, ⊤)`) are explicitly acknowledged as future work; the current catalog enumerates rows demanded by present-day templates.

### Topic 2: Multi-process atomicity for Sh4/FDD contracts
**Why out of scope**: The Sh4 and FDD contracts commit to single-process substrates by design. Multi-process coordination protocols are flagged as scope-extending work in Open Questions.

### Topic 3: Higher-arity (>3) link shapes
**Why out of scope**: The framework restricts to the standard-triple slice `L^Σ` per the *Arity scope* paragraph. Higher-arity links remain admissible at ASN-0043's substrate but outside the framework's shape vocabulary.

### Topic 4: Mechanical template derivation for new shapes
**Why out of scope**: Sh5(a) explicitly admits no mechanical-derivation procedure exists. The catalog is hand-curated; mechanical falsification (not derivation) is what Sh5(b) provides.

### Topic 5: Ghost-targeting slot semantics
**Why out of scope**: Sh-conf clause (d) restricts slot addresses to already-allocated targets at emission time. Admitting ghost addresses in slot positions is a future design choice, flagged in Open Questions.

### Topic 6: Document-container target-domain
**Why out of scope**: The framework provides no target-domain symbol for `dom(Σ.M)` addresses (document containers with `zeros = 2`). Layers must encode relations against designated content addresses within element fields. Acknowledged in the *Reach of the framework's target-domain symbols* note.

VERDICT: REVISE
