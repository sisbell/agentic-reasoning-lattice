# Review of ASN-0094

## REVISE

### Issue 1: Sh0 proof's clause citations are non-parallel with Sh1's

**ASN-0094, Sh0 proof, Cardinality section**: "Sh-conf admitted that call only because `conf_K^Σ(F, G)` held — i.e., `F` is canonical-slot form and `match(|slot_addrs(F)|, c_F)`."

**Problem**: The Sh1 proof immediately following cites clauses by letter: "by Sh-conf clause (b), `G` is in canonical-slot form, and by clause (c), `match(...)`." Sh0's proof unpacks `conf_K^Σ` without naming the clauses. The framework introduces "canonical-form gate (clauses (a)/(b)), cardinality gate (clause (c)), target-domain gate (clause (d))" as a vocabulary, and Sh1/Sh2/Sh3 honor this naming. Sh0 should as well.

**Required**: Update Sh0's Case B to say "by Sh-conf clause (a), `F` is in canonical-slot form, and by clause (c), `match(|slot_addrs(F)|, c_F)`."

### Issue 2: BDP0 sealed-off narrative is structurally confusing

**ASN-0094, BundledDirectedPair walkthrough**: Emission BDP0 fires from `Σ_0` producing `Σ_0a`, then BDP1 fires from `Σ_0` (not `Σ_0a`), with bold text "**γ_0 does not participate in the rest of the walkthrough.**"

**Problem**: A reader following the temporal narrative sees BDP0 land a tuple, then sees BDP1 fire from the pre-BDP0 state, then sees the Σ_2 evaluation table report `pair_K(d_cite, ∅) = false` because γ_0 "doesn't exist" — but γ_0 was just shown to be emitted. The seal-off declaration is explicit, but the narrative timeline contradicts itself before resolving.

**Required**: Either (a) emit BDP0 in a labeled "Alternative continuation" sub-walkthrough at a parallel state line, with the main timeline branching from Σ_0 along BDP1→BDP2; or (b) reorder so BDP1→BDP2 fire first, then BDP0 fires as an explicit hypothetical exploration of the empty-G boundary from Σ_2 rather than Σ_0.

### Issue 3: Resolution standalone walkthrough's address origin is under-specified

**ASN-0094, "Resolution base templates at a standalone K"**: "the addresses `a_σ1, a_σ2 ∈ A_rel^{Σ_0}` (the latter two arrive in `dom(Σ_0.L)` via prior class-(iii) emissions at relations outside this `T_cat` scope; their specific K-of-origin is immaterial — only their membership in `A_rel^{Σ_0} = dom(Σ_0.L)` is consumed at Sh-conf clause (d))."

**Problem**: This is admissible (the *Emit_K routing commitment* binds only `K ∈ T_cat`, so class-(iii) emissions at unregistered K' are outside its scope), but the walkthrough doesn't say so explicitly. A reader who has internalized "every class-(iii) emission of `K ∈ T_cat` routes through `Emit_K`" may suspect a routing violation when the walkthrough creates link-store entries outside the declared T_cat = {approved_by, R}.

**Required**: Add a one-line note: "These prior class-(iii) emissions at K' ∉ T_cat lie outside the *Emit_K routing commitment*'s scope (which quantifies only over `K ∈ T_cat`), so they do not violate any framework theorem — the only property consumed here is `a_σ1, a_σ2 ∈ dom(Σ_0.L)`."

### Issue 4: Step 3.2 carries editorial commentary about prior drafts

**ASN-0094, AllocatedAddressAntichain proof, Step 3.2**: "(Earlier drafts derived the full Prefix relation `E(x) ≼ E(a)` and then took its `j = 1` conjunct; the Prefix step was unnecessary bookkeeping — only componentwise agreement at a single position is consumed — and has been dropped in favor of the direct derivation above.)"

**Problem**: This is change-log content, not specification content. A reader reviewing the current claim doesn't need the history; the parenthetical risks suggesting the current derivation is provisional rather than load-bearing.

**Required**: Remove the parenthetical. The current derivation stands on its own; if the contrast with the earlier form is pedagogically useful, move it to a footnote or commit message.

### Issue 5: Sh4 Case A's "expository orientation" enumeration is incomplete

**ASN-0094, Sh4 proof, Case A**: "The case is *defined* by the equation `A_K^{Σ'} = A_K^Σ`... The enumeration of principal transitions is retained as expository orientation only, not as a load-bearing case analysis."

**Problem**: The enumeration lists "K.σ, K.α, K.λ-steps emitting K' with K' ≁ K and K' ≁ R, and arrangement-modifying steps". But K.λ-steps emitting K' with K' ~ R (and K' ≁ K) can extend `nullified(Σ)` — and if some τ ∈ A_K^Σ is in coverage of the new R-tuple's G, that τ leaves A_K, falsifying `A_K^{Σ'} = A_K^Σ`. So K.λ-at-R-class-but-≁K is not unconditionally a Case A transition — it's Case A only when no τ ∈ A_K^Σ is nullified by it; otherwise it's Case C. The framework states Case A's case-equation alone suffices for closure (which is correct), but the "expository" enumeration mislabels these mixed transitions.

**Required**: Either tighten the enumeration to "K.λ-steps emitting K' with K' ≁ K and K' ≁ R, *and* K.λ-steps emitting K' with K' ≁ K and K' ~ R when no τ ∈ A_K^Σ is in the new tuple's G-coverage", or simplify the enumeration to "every transition satisfying the case-equation" and drop the partial classification.

## OUT_OF_SCOPE

### Topic 1: Closure theorem for composite predicates

**Why out of scope**: The framework explicitly disclaims a closure theorem ("The framework does not establish a closure theorem about these primitives"). Whether composition of catalog templates plus Boolean operators plus quantification reaches predicates outside the atomic vocabulary is a question for a downstream composition-language ASN, not for this shape framework.

### Topic 2: Mechanical body-shape uniformity gate at shape-mate rows

**Why out of scope**: The framework's Sh5(a) explicitly downgrades per-shape body-shape uniformity from a commitment to an aspiration. Sharpening this into a mechanical derivation procedure (e.g., a documented body-shape recipe from shape components) is recorded as an open work item. The present ASN's META status is honest; promotion belongs in a future Sh5'.

### Topic 3: Multi-process atomicity of the Sh4/FDD/SHCD contracts

**Why out of scope**: The framework explicitly scopes to single-process substrates, and the Open Questions section flags cross-process consistency as a scope boundary the framework commits to. A multi-process coordination protocol would extend the framework's reach, not patch a gap in the current claim.

### Topic 4: Cardinality vocabulary extension for `1..*` lower bounds

**Why out of scope**: BundledDirectedPair admits `n = 0` at `c_G = *` as a deliberate consequence of the framework's cardinality vocabulary `{0, 1, *, 0|1}`, which carries no `1..*` token. Adding `1..*` would require enriching the registry; flagged in Open Questions as a refinement candidate.

VERDICT: REVISE
