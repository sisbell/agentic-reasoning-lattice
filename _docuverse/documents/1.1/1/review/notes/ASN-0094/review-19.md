# Review of ASN-0094

## REVISE

### Issue 1: EffectiveWpSimplification forward-references Sh1 and Sh3

**ASN-0094, EffectiveWpSimplification Corollary, Step 1**: "By Sh1 at `K := R`, `G'` is canonical-slot with `match(|slot_addrs(G')|, 1)` (so `|slot_addrs(G')| = 1`); by Sh3 at `K := R`, `slot_addrs(G') ⊆ t_G^Σ = A_rel^Σ = dom(Σ.L)`. (Sh1 and Sh3 apply because R is registered in `T_cat` per the framework's baseline registration requirement; both are theorems-under-conformance proved by induction on `↦*` and so deliver current-state structure for every τ ∈ L_R^Σ, including tuples emitted in prior states.)"

**Problem**: The Corollary is presented in the document BEFORE Sh0-Sh3 are formally proved. The parenthetical justification cites "proved by induction on `↦*`" without explicit forward reference, leaving the reader to verify the dependency is acyclic. While the actual dependency IS acyclic (Sh1/Sh3 use only Sh-conf, not the Corollary), the presentation creates a navigation hazard.

**Required**: Either present the Corollary after Sh0-Sh3 are formally proved, or add explicit forward reference language: "Sh1 and Sh3 are established by induction below; we anticipate them here for downstream wp-simplification arguments. No circularity: Sh0-Sh3's proofs depend only on Sh-conf, not on this Corollary."

### Issue 2: Sh5(b) META discipline doesn't formalize meta-operator exemption

**ASN-0094, Sh5 status (b)**: "The criterion is *literal name-citation*: a template body that references a symbol must either be one of the shape-component slots, K itself, a scaffolding clause name (e.g., `chain_index`, `home(·)`, `s_L`), an accessor exported by a registered per-K discipline... or a parametric type-index argument; any symbol falling outside these four categories violates the discipline and the catalog rejects the addition."

**Problem**: The discipline lists four categories of per-K data symbols but doesn't explicitly carve out meta-operators (argmax, ∃, ∪, ℘_fin, etc.). The "Worked check at `latest_K_for_addr`" acknowledges this implicitly by parenthetically noting argmax as "a meta-operator over finite ℕ-indexed sets, not a per-K accessor" — but this is an inspection-time observation, not a formal rule. A reviewer who tried to apply the literal-name-citation criterion would reject `argmax`, `∃`, and set-comprehension constructs that the catalog uses freely.

**Required**: Tighten the discipline rule to explicitly carve out logical and set-theoretic primitives: "Data-symbol references must be in (i)-(iv); meta-operators (set comprehensions, quantifiers, argmax, set-theoretic operations) and logical connectives are unrestricted." This makes Sh5(b)'s discipline genuinely falsifiable without relying on case-by-case inspection.

### Issue 3: SingleHomeCoverageDiscipline rejection case missing from Coverage walkthrough

**ASN-0094, Coverage walkthrough Emissions C1-C3**: All three emissions use `d_K` as the home document; no emission with `d ≠ d_K` is attempted.

**Problem**: The walkthrough exercises the discipline's admission path but not its rejection path, breaking parallelism with the FDD walkthrough's "Emission FDD2 (rejected by FDD contract clause (ii))" case. A reader cannot verify from the walkthrough alone that the *single-home commitment*'s clause (i) actually rejects `d ≠ d_K` calls; they must trace the contract definition independently.

**Required**: Add a rejection case, e.g.: "Attempt `Emit_K(Σ_3, d_other, F_C4, G_C4)` with `d_other ∈ dom(Σ.M), d_other ≠ d_K`. The *single-home commitment* clause (i) rejects outright; `Emit_K` returns `⊥`. State remains Σ_3 unchanged."

### Issue 4: Sh4 Case D's subset-closure argument is too compressed

**ASN-0094, Sh4 preservation Case D, closing sentence**: "Second, `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving` is a subset of the pairwise-distinct set `A_R^Σ ∪ {τ_new}`. Any subset of a pairwise-distinct set is pairwise-distinct (the universal quantifier ranges over fewer pairs but the predicate is unchanged). Sh4 holds on `A_R^{Σ'}`."

**Problem**: "Any subset of a pairwise-distinct set is pairwise-distinct" is a one-line argument for a structurally non-trivial step. The parenthetical asserts the result without explicitly showing the pair-quantification reduction. For a postcondition whose universal ranges over `A_K^Σ × A_K^Σ`, the subset-preservation should be derived rather than asserted.

**Required**: Expand the closure: "Let `P(τ, τ')` denote Sh4's body `(slot_addrs(F_τ), slot_addrs(G_τ)) = (slot_addrs(F_{τ'}), slot_addrs(G_{τ'})) ⟹ addr(τ) = addr(τ')`. Pairwise distinctness on S is `(A τ, τ' ∈ S :: P(τ, τ'))`. For any subset S' ⊆ S, `S'^2 ⊆ S^2`, so every pair (τ, τ') ∈ S'^2 is among the pairs constrained by the antecedent, with the same `P`. Hence `(A τ, τ' ∈ S' :: P(τ, τ'))` holds. Instantiate at S = A_R^Σ ∪ {τ_new}, S' = A_R^{Σ'}."

### Issue 5: Subspace identification scaffolding clause's relation to L0 understated

**ASN-0094, Link subspace partition scaffolding clause**: "(This scaffolding clause is a local commitment of the substrate-conforming layer that is consistent with L0 from ASN-0043 — L0 introduces an abstract identifier function `subspace_I(·)` and states `subspace_I(a) = s_L`; the scaffolding fixes the layer-local identification `subspace_I(·) = E(·).1` on element-level addresses... The identification is introduced here, not imported from upstream.)"

**Problem**: The clause acknowledges the identification is layer-local but does not state the *consequence*: any layer instantiating the framework commits to this identification, and any consumer reasoning at L0's abstract level (where `subspace_I` is uninterpreted) must verify the framework's claims against the layer-local identification. The AllocatedAddressAntichain proof's Case 3 critically depends on this identification (Steps 3.3a/3.3b read `E(x).1 = s_L` directly from membership), so the soundness of a major framework lemma rests on this scaffolding commitment.

**Required**: Strengthen the scaffolding clause to make the layer-commitment status explicit: "Consumers expecting L0's abstract reading (where `subspace_I(·)` is uninterpreted) must verify the layer-local identification `subspace_I(·) = E(·).1` at the layer's interface; the framework's preservation theorems and the AllocatedAddressAntichain lemma rest on this identification."

### Issue 6: Tuple-Classifier base template derivation under-specifies Sh5(b)'s signature rule

**ASN-0094, Tuple-Classifier walkthrough**: "(same body as Classifier's `is_K` with the signature shifted from `A_doc → Bool` to `A_rel → Bool` per Sh5(b))"

**Problem**: Sh5(b)'s discipline lists four categories of allowed symbols but doesn't explicitly state how template signatures derive from shape components. The reader must infer that the codomain `A_doc → Bool` vs `A_rel → Bool` derives from t_G's value via category (i) "shape components". Making this implicit signature-derivation rule explicit would close a presentation gap.

**Required**: Add to Sh5(b): "Template signatures derive from shape components — input domains and codomains take their target-domain symbols from t_F and t_G respectively. The body is otherwise identical for shape-mates."

### Issue 7: Resolution row's own base templates never exercised

**ASN-0094, Resolution catalog row and walkthroughs**: The catalog row labels Resolution's "*primary consumption:* parametrically by NonIdempotentDirectedPair's `_via` templates"; the walkthroughs show ρ_1, ρ_2 only as inputs to Comment's `unresolved_K_comments_via` and `all_K_resolved_via`.

**Problem**: Per Sh5(b), Resolution at shape `(1, 1, A_doc, A_rel, ⊤)` mechanically generates its own base templates `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`. These are never instantiated or exercised in any walkthrough, so the catalog's claim that Resolution shares the DirectedPair base family is unverified concretely. A reader cannot tell whether `pair_K(d_2, addr(τ_c))` for the Resolution row is computed identically to DirectedPair's `pair_K`.

**Required**: Add a brief Resolution-only walkthrough exercising at least `pair_K` and `to_addrs_K` on a Resolution emission, demonstrating that the base templates behave identically to DirectedPair's modulo the `t_G = A_rel` codomain shift.

### Issue 8: RetractionTargetNotOnChain Case I doesn't address J_d^Σ = -1 sub-case

**ASN-0094, Lemma RetractionTargetNotOnChain Case I**: "Both `b` and `a_emit(Σ, d)` lie in `A_L(d)`'s chain enumeration: `b` by R0a-Cor1 (ContiguousPrefix, ASN-0086) applied to the homed set at `d` (so `b = inc^i(d.0.s_L.1, 0)` for some chain index `0 ≤ i ≤ J_d^Σ`)..."

**Problem**: The proof assumes `b` has a chain index `0 ≤ i ≤ J_d^Σ`, which presupposes `J_d^Σ ≥ 0` (non-empty homed set at d). R0a-Cor1 explicitly admits `J_d^Σ = -1` for the empty homed-set case. If `home(b) = d` is the case hypothesis, the existence of `b` in the homed set forces `J_d^Σ ≥ 0`, but this is never noted. The proof should make this implicit step explicit.

**Required**: After "By R0a-Cor1... applied to the homed set at d", add: "The case hypothesis `home(b) = d` places `b` in the homed set at d, forcing `J_d^Σ ≥ 0` per R0a-Cor1's `ℤ_{≥-1}` codomain. Hence `b = inc^i(d.0.s_L.1, 0)` for some chain index `0 ≤ i ≤ J_d^Σ` is well-formed."

## OUT_OF_SCOPE

### Topic 1: Closure of the composite predicate language

The Consequences section mentions composite predicates extending the catalog through Boolean operators and quantification over `T_cat`. The framework explicitly declines to claim closure: "The framework does not establish a closure theorem about these primitives." Whether composite predicates can express predicates strictly beyond what atomic templates yield is a property of the composition language, not the shape framework.

**Why out of scope**: A closure theorem would be a new structural result about predicate expressivity, not a constraint the shape framework itself imposes.

### Topic 2: Multi-process substrate coordination

The Sh4 idempotency contract is explicitly scoped to single-process substrates. The Open Questions section flags cross-process consistency: "Multi-process substrates with racing Sh4-emitters at coverage-equivalent K's would require a coordination protocol... not specified by this framework."

**Why out of scope**: Cross-process coordination is a distributed-systems extension beyond the framework's single-process atomicity model.

### Topic 3: Ghost-targeting slot semantics

The framework rejects ghost addresses in slot positions of registered relations (Sh-conf clause (d)). L9 (TypeGhostPermission, ASN-0043) permits ghost spans in endsets generally; admitting ghosts in slot positions would require a state-dependent conformance rule.

**Why out of scope**: This is a future design question explicitly noted in Open Questions.

### Topic 4: Bipartite catalog completion

The catalog has Classifier/Tuple-Classifier as bipartite pairs at `(0, 1)` but no bipartite Tuple-DirectedPair, Tuple-NonIdempotentDirectedPair, etc. The framework notes "Further bipartite entries can be added by extending the catalog."

**Why out of scope**: Completing the bipartite structure is catalog extension work, not a correctness issue with the current ASN.

VERDICT: REVISE
