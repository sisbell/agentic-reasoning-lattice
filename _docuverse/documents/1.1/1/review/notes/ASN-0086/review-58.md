# Review of ASN-0086

## REVISE

### Issue 1: R0a's non-disciplined counterexample is computationally inconsistent

**ASN-0086, R0a proof, "Non-disciplined counterexample" paragraph**: "The substrate primitive admits an emission at `a' = a₁.0.1.1` — a fresh address satisfying all primitive preconditions: ... `zeros(a') = 3` (the spawn at depth introduces no new zero past `a₁`'s last component); (3) L1c — an admissible chain extension of `a₁`'s witness chain by `(a₁, 1)` then `(·, 0)` sibling steps reaches `a'`."

**Problem**: Two computational errors. (a) `a₁.0.1.1` is `a₁` followed by `[0, 1, 1]`. Since `zeros(a₁) = 3` (L1), the appended `0` brings `zeros(a') = 4`, violating L1 and contradicting the proof's own claim. (b) The cited chain `(a₁, 1)` then `(·, 0)` yields `inc(a₁, 1) = a₁.1` followed by `inc(a₁.1, 0) = a₁.2`. Neither equals `a₁.0.1.1`. The counterexample is therefore both internally inconsistent (zeros count) and unreachable by the stated chain.

**Required**: Replace with a valid prefix-extension respecting L1. Either `a' = a₁.1` (chain: single `inc(a₁, 1)` step; `zeros(a') = 3` since k=1 adds no zero; `a₁ ≼ a'`) or `a' = a₁.2` (chain: `inc(a₁, 1)` then `inc(a₁.1, 0)`; the sibling step at sig position keeps `a₁ ≼ a'` because the prefix positions 1..#a₁ are preserved). Either witnesses a class-(iii) emission that the substrate primitive admits but the discipline forbids. R0a's structural argument is unaffected; only the specific witness needs correction.

### Issue 2: R7a's substrate-wide extension of L12/L12a is asserted without justification

**ASN-0086, R7a proof, opening paragraph**: "L12 (LinkImmutability, ASN-0043) and L12a (LinkStoreMonotonicity, ASN-0043) are substrate-wide invariants that bind every state transition admissible at any layer of the substrate stack — every `Σ ↝ Σ'` satisfies `dom(Σ.L) ⊆ dom(Σ'.L)` (L12a) and `Σ'.L(a) = Σ.L(a)` for every `a ∈ dom(Σ.L)` (L12)."

**Problem**: L12 and L12a in ASN-0043 are stated with quantifiers over `→` (substrate one-step transitions), not over `↝` (categorical relation including higher-layer operations). The leap from "L12 holds for `→`-steps" to "L12 binds every `↝`-step admissible at any layer" is asserted, not derived. R7a's claim is categorical across all layers, so the justification must be load-bearing — it is not optional polish.

**Required**: Either (i) state explicitly as a precondition: "for any state-affecting `Σ ↝ Σ'` admissible at a layer that conforms to substrate invariants L12 and L12a..."; or (ii) supply a short conformance argument — e.g., that any layer publishing operations over the substrate's state vector must preserve substrate invariants, otherwise that layer is itself in violation of the substrate model. The current "L12 is substrate-wide" assertion sits between the two without committing to either.

### Issue 3: "Substrate guarantee" framing for Nullify's single-tuple scope is misleading

**ASN-0086, Definition of Nullify, "Single-tuple scope" paragraph**: "Single-tuple scope is *absolute* within the disciplined regime — a substrate guarantee from R0a, not a per-call caller obligation."

**Problem**: R0a is conditional on the sibling-frontier discipline, which the Implementation Notes describe as an implementation hypothesis held by udanax-green but not entailed by the substrate emission primitive in isolation. Issue 1's corrected counterexample exhibits a substrate-permitted emission that breaks R0a's antichain. Calling the resulting single-tuple scope a "substrate guarantee" conflates discipline-conditional properties with substrate-level commitments — exactly the conflation the rest of the note carefully avoids.

**Required**: Reframe as "discipline-level guarantee" or "guarantee under the sibling-frontier discipline". The single-tuple scope is substrate-derivable *given* the discipline, but the discipline itself is layered above the substrate primitive. The seventh Open Question explicitly asks whether the discipline should be elevated to a substrate guarantee; Nullify's definition should respect the layering as currently structured, not pre-elevate the discipline.

### Issue 4: WP Case 2 omits the regime-distinction's appearance in R6c Consequence (d)

**ASN-0086, R6c Consequences (d) and WP Case 2**: Consequence (d) observes that `A_K` is non-monotone, citing the Worked Sketch's `A_K^{Σ_0} → A_K^{Σ_1} → A_K^{Σ_2}` trajectory; WP Case 2 then distinguishes regime (i) "Nullify-only discipline" from regime (ii) "Crafted-span retractions admitted".

**Problem**: Consequence (d) ends with "The regime distinction governing exactly when a class-(iii) `Emit_K` step contributes to `A_K` versus to `L_K \ A_K` — turning on whether a pre-existing retraction's coverage already includes the fresh sibling-frontier address — is unpacked in WP Case 2." But WP Case 2 is itself silent on whether the *relational layer's* committed discipline rules out regime (ii). The unit-depth retraction discipline (Implementation Notes) implies regime (i); the layer's Emit_R is Nullify, which deposits unit-depth spans only. So under the relational layer's committed operations, regime (ii) cannot arise — yet Case 2's wp formula keeps `NoCraftedSpanReachesD` as a non-trivial conjunct, suggesting it can. The note never resolves which conjuncts actually need verification at relational-layer call sites.

**Required**: State explicitly that under the relational layer's committed operations (`Emit_K`, `Observe`, `Nullify`), regime (ii) is structurally impossible — every `L_R^Σ` tuple was emitted by Nullify, which by definition produces a unit-depth to-span. Then Case 2's wp simplifies definitionally to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ SFD(Σ)`, with `NoCraftedSpanReachesD` discharged by the layer's commitment. The current wording leaves callers wondering whether they need to verify `NoCraftedSpanReachesD` per emission.

VERDICT: REVISE
