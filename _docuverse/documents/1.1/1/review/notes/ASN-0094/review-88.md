# Review of ASN-0094

## REVISE

### Issue 1: Cross-ASN references to non-foundation ASNs in SubstrateConformingLayer Definition
**ASN-0094, Definition — SubstrateConformingLayer (catalog (a))**: "*ASN-0036 content/arrangement invariants:* S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ. *ASN-0093 substrate invariants:* M0, M1, C0, C1, C1b, C1c, C-fin."

Also in catalog (b): "SubAllocatorAxiom, ChainMembershipForOrigin, ChainEnumerationInjectivity, ChainUniformLength, ChainUniformZeroCount, ChainPrefixExtension, ChainElementT4Validity, DisjointSubAllocatorChains, StoreT4Validity, FirstEmissionFreshness, CrossDocDisjointness."

**Problem**: ASN-0036 and ASN-0093 are not in the foundation list (ASN-0034, ASN-0043, ASN-0086). The named claims (M0, M1, C0, C1, …, SubAllocatorAxiom, …) are defined elsewhere with no local statement in ASN-0094. The ASN itself claims self-containment in the same section: "every property the framework consumes is either a foundation claim (cited from ASN-0034, ASN-0043, ASN-0086 by name) or one of the named scaffolding clauses below; no external invariant catalog is imported by reference" — directly contradicted by these two catalog enumerations.

**Required**: Either (a) inline the specific invariants the framework actually consumes into the local scaffolding clauses (most are already covered there — the content-side antichain, monotonicity, finiteness, document address structure, chain function — so catalog (a) and (b) may be reducible to the existing scaffolding), or (b) drop the SubstrateConformingLayer definition's catalog enumeration and define "substrate-conforming" purely through the local scaffolding clauses, which is what the proofs actually use.

### Issue 2: Redundant restatement at end of Retraction walkthrough
**ASN-0094, Retraction subsection, "Coverage class self-identity at R"**: "every R-typed `Emit_K` call goes through Step 2's Case B (`K ~ R`) in EffectiveWpSimplification's proof, where the unit-depth G constraint (Sh-conf clauses (b)/(c)/(d) at `c_G = 1`) discharges `a_emit(Σ, d) ∉ coverage(G)` via Lemma — LinkAddressNotPrefixOfEmit."

**Problem**: This paragraph re-narrates content that EffectiveWpSimplification's Step 2 Case B already establishes. It defers to a downstream proof rather than advancing local content — a forward-reference accretion pattern. The Retraction subsection already states `shape(R) = (*, 1, A, A_rel, ⊤)` and the unit-depth discipline; the cross-reference adds no derivation.

**Required**: Remove the paragraph or replace it with a single sentence noting "Retraction is the K ~ R case in the framework's coverage classes."

### Issue 3: "Failure mode" paragraph is near-tautological
**ASN-0094, end of FDD subsection**: "*Failure mode.* Templates consuming FunctionalDependencyDiscipline (specifically `K_target_of` and its aliases) become undefined on the candidate set when the discipline is violated and the set contains multiple elements. Per-template specifications below state explicitly when a template's totality depends on this discipline."

**Problem**: The first sentence restates the definition of the discipline's contract obligation; the second is a forward-reference promise without content. This is reviser drift — a paragraph explaining why an axiom is needed rather than what it does.

**Required**: Remove the paragraph. The "Singleton-returning template under FunctionalDependencyDiscipline" paragraph already covers the precondition.

### Issue 4: Sh4 Case D "structurally restricted" justification is overdetermined
**ASN-0094, Sh4 preservation, Case B opening**: "The case is structurally restricted to `K ≁ R` rather than carrying a conditional 'no concurrent nullification' qualifier: by the class-decomposition of `↦` (per ASN-0086's `→` Definition and `↦`'s broader transition relation), concurrent nullification at the same step happens only at `Emit_R` steps, since `nullified(Σ)`'s definition reads over `L_R^Σ`'s G-coverages and only `Emit_R` extends `L_R`. A non-Retraction-typed K.λ-step (i.e., the `K ≁ R` regime selected here) cannot extend `L_R^Σ` and therefore cannot expand `nullified(Σ)`, so no τ ∈ A_K^Σ leaves `A_K` at this step — concurrent nullification is structurally impossible in Case B, not a conditional precondition."

**Problem**: This paragraph defends the case-split choice rather than discharging the proof step. A revised review apparently introduced this defense; the original case-split is correct without needing the meta-justification. The exhaustiveness routing belongs in the CaseAClosureForAK lemma's statement, not in Case B's body.

**Required**: Tighten to one sentence ("By Lemma — CaseAClosureForAK, Case B fires only at K.λ-steps with K' ~ K and K ≁ R; concurrent nullification at K ~ R is routed to Case D below.") or move the justification into CaseAClosureForAK's body.

### Issue 5: Empty-G + idem = ⊤ admits an unobserved boundary
**ASN-0094, BundledDirectedPair walkthrough, BDP0**: "G_BDP0 is canonical-slot trivially with `slot_addrs(G_BDP0) = ∅`, `|·| = 0`, `match(0, c_G = *)` ✓".

**Problem**: BundledDirectedPair has `idem = ⊤`. Two emissions with the same F-slot value and both empty G-slots would have identical slot-pairs `({d_cite}, ∅)`. The walkthrough's "Sh4 suppression on duplicate empty-G re-emission" probe handles this. But the *interpretation* — does empty-G mean "no dependencies declared yet" or "the emitter affirms there are zero dependencies"? — is not stated. The shape framework's idempotency over empty-G slot-pairs means a re-emission "declaring no dependencies" is suppressed; this may or may not match a layer's intended semantics.

**Required**: Either add a one-sentence note in the BundledDirectedPair section explaining the semantic implication of `c_G = *` + `idem = ⊤` on empty-G slot-pairs, or move the question to Open Questions.

### Issue 6: "Lifetime semantics for `T_cat^rep`" repeats the configuration-parameter claim three times
**ASN-0094, Definition — TypedRelationCatalog**: The body has three structurally similar paragraphs claiming `T_cat^rep` is layer-supplied, fixed pre-`Σ_init`, and constant across the substrate's lifetime: "*Representative list as layer-supplied configuration parameter*", "*Lifetime semantics for `T_cat^rep`*", and the later sentence "lifetime constancy is inherited from the configuration-parameter lifetime semantics for `T_cat^rep`" appearing in *ShapeRegistry*'s Registration interface paragraph.

**Problem**: Two paragraphs in the same definition say the same thing in different words. The first paragraph names `T_cat^rep`; the second paragraph re-asserts its lifetime constancy.

**Required**: Consolidate into one paragraph stating both the configuration-parameter status and the lifetime constancy.

### Issue 7: AllocatedAddressAntichain — Case 3 element-level case-split is undermotivated
**ASN-0094, AllocatedAddressAntichain proof, Step 3.2 opening**: "By T4a (SyntacticEquivalence, ASN-0034) + T4b (UniqueParse, ASN-0034) + T4c (LevelDetermination, ASN-0034), at any T4-valid `zeros = 3` address with zero positions `n_1 < n_2 < n_3`, the field projections occupy positions `1..n_1 − 1` (N-field), `n_1 + 1..n_2 − 1` (U-field), `n_2 + 1..n_3 − 1` (D-field), and `n_3 + 1..#·` (E-field)."

**Problem**: T4a, T4b, and T4c are cited collectively for a positional decomposition claim that is more naturally read off T4 directly. The proof would be cleaner if it cited T4's positional structure (zeros separate the fields) and invoked T4a/b/c only where their specific content (segment non-emptiness; unique parse; level-determination) is load-bearing. As written, the cumulative citation invites confusion about which theorem supplies which clause.

**Required**: Split the citations: cite T4 for the zero-separator structure, T4c for the level labeling (N, U, D, E), and reserve T4a/T4b citations for where they are specifically needed.

### Issue 8: Worked Example "verifies postconditions" but doesn't verify wp_eff explicitly
**ASN-0094, Worked Example: K = comment**: The walkthrough exercises emissions, retractions, template evaluations, and Sh-conf gating, but does not compute `wp_eff(Emit_K(Σ_0, home_K, F_1, G_1), fresh (a_1, F_1, G_1) ∈ A_K^{Σ_1})` explicitly.

**Problem**: The standards require non-trivial wp computation. EffectiveWpSimplification's formula expands to `d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G) ∧ Π_K`. At a K with `idem = ⊥` and no SHCD/FDD, Π_K is vacuously true, but conf_K^Σ is non-trivial. The walkthrough exhibits the gate-by-gate evaluation but doesn't relate it back to the wp formula. A reader trying to verify EffectiveWpSimplification against the example must reconstruct the connection.

**Required**: Add one explicit wp computation in the Worked Example — e.g., "For Emission 1, `wp_eff(...) = (home_K ∈ dom(Σ_0.M)) ∧ (K ∈ T_cat) ∧ (F_1, G_1 canonical-slot) ∧ ... ∧ true (no per-K discipline). All conjuncts hold, so Emit_K admits."

### Issue 9: Open Questions tag "[scope boundary]" for initial state baseline conflicts with framework reach
**ASN-0094, Open Questions**: "The framework's preservation theorems for Sh4, FDD, and SHCD presuppose the empty-link-store baseline `L_K^{Σ_init} = ∅` at every `K ∈ T_cat`."

**Problem**: This is tagged `[scope boundary]` but it is actually a precondition that load-bears on every preservation proof. A substrate-conforming layer that instantiates the framework atop a state with non-empty link stores gets no guarantees from Sh4/FDD/SHCD. The framework should either (a) state the empty-baseline assumption more prominently (it currently appears only in the Initial-State Baseline section), or (b) generalize the preservation proofs to handle non-empty baselines with a per-K conformance check at `Σ_init`.

**Required**: Either elevate the empty-baseline precondition to a top-level commitment in the Scope and Substrate Scaffolding section (alongside the *Emit_K routing commitment* and *R-registration commitment*), or generalize the proofs.

## OUT_OF_SCOPE

### Topic 1: Cross-process consistency of the shape registry
**Why out of scope**: The Open Questions list correctly tags this as `[scope boundary]`. Multi-process substrates would require coordination protocols outside this framework. The framework's single-process commitment is explicit.

### Topic 2: Composite shapes (relations constrained by other relations' content)
**Why out of scope**: Open Questions tags this `[refinement candidate]`. The current framework restricts shape components to cardinality and target domain; composite shapes would require an additional restriction axis.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: The framework's restriction of slot addresses to already-allocated addresses is explicit; admitting ghost slots requires new state-dependent conformance rules.

VERDICT: REVISE
