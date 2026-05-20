# Review of ASN-0094

## REVISE

### Issue 1: Sh4 contract suppression of duplicate Nullify calls not addressed in Nullify Compatibility
**ASN-0094, Nullify Compatibility / Compatibility with ASN-0086's Nullify postcondition**: "every well-formed Nullify(Σ, d_retr, a) call (i.e., one satisfying ASN-0086's P0/P1/P2 preconditions) is admitted by Sh-conf via the conformance checks just enumerated, so the call returns (Σ', _) ∈ Σ' × A_rel^{Σ'} and ASN-0086's Nullify postcondition is met by the framework's call site."
**Problem**: The Sh4 idempotency contract applies to R since shape(R).idem = ⊤ ("For each K ∈ T_cat with shape(K).idem = ⊤, on every Emit_K(Σ, d, F, G) call site the layer enforces the following protocol..."). Under clause (ii), a duplicate-target Nullify (where a prior retraction tuple targeting the same address is still in A_R^Σ) is suppressed and returns ⊥. The "returns (Σ', _) ∈ Σ' × A_rel^{Σ'}" claim therefore fails for duplicate calls. The Compatibility section addresses Sh-conf admission but not Sh4-contract admission.
**Required**: Add explicit discussion of how the Sh4 contract interacts with Nullify. Distinguish first-Nullify-of-target (admitted) from duplicate-Nullify-of-target (suppressed under the contract). State explicitly that suppression is operationally equivalent to admission with respect to nullified(Σ) (since the audit slice uses L_R, not A_R, in nullified's definition, and the prior retraction's coverage contribution is already permanent under R6a), so the active-subset semantics of ASN-0086 are preserved; only the audit slice differs. Alternatively, argue why R should be exempt from the Sh4 contract despite shape(R).idem = ⊤, and justify the exemption.

### Issue 2: Stratification documentation inaccurate about Sh4's consumed lemmas
**ASN-0094, Sh-conf axiom / Stratified proof order**: "(5) Sh4 induction (Idempotency section, consumes Sh0–Sh3 and EffectiveWpSimplification as state-indexed lemmas)."
**Problem**: The Sh4 proof does not directly invoke EffectiveWpSimplification. Case C's K~R sub-case cites RetractionTargetNotOnChain (the Lemma at stratum 3): "is empty by Lemma — RetractionTargetNotOnChain: under K ~ R, Sh-conf forces G_{τ_new} = {(b, δ(1, #b))}... the Lemma applied at b...". Case D uses Sh-conf, PrefixSpanCoverage, R0a, R1, R3 without citing the Corollary. The Sh4 *Stratification* sub-clause itself says "Sh4's preservation argument consumes Sh0–Sh3" with no mention of EffectiveWpSimplification — inconsistent with the overall Stratified proof order's claim.
**Required**: Either correct the Stratified proof order to "Sh4 induction... consumes Sh0–Sh3 and RetractionTargetNotOnChain (at Case C's K~R sub-case)", or identify the site within Sh4's proof where EffectiveWpSimplification is actually consumed (if any, perhaps implicit via wp_086 discharge at the substrate K.λ-step) and cite it explicitly at that site.

### Issue 3: Retraction shape lacks a rejection-case walkthrough
**ASN-0094, Per-Shape Template Walkthroughs / Additional Worked Examples**: The "K = comment" walkthrough exhibits four distinct Sh-conf rejection cases (non-canonical F, unallocated to-slot, cardinality mismatch, unregistered K). The Attributed Retraction walkthrough exhibits only successful emissions at c_F = 1 and c_F = 2.
**Problem**: Retraction's t_G = A_rel is the constraint that secures the unit-depth retraction discipline at the framework level. No worked example exercises a rejection at this gate. A canonical-slot G targeting an A_doc address (rather than A_rel) would test Sh-conf clause (d) at the G-side at the Retraction shape — distinct from Comment's rejection case 2 (unallocated to-slot), which exercises the *allocation* aspect of clause (d) but not the *partition* aspect (A_rel vs A_doc).
**Required**: Add at least one rejection case in the Attributed Retraction walkthrough: e.g., attempt Emit_R with G = {(d_doc, δ(1, #d_doc))} for d_doc ∈ A_doc^Σ; show Sh-conf clause (d) rejects because {d_doc} ⊄ A_rel^Σ (using R4's disjointness).

### Issue 4: PointSlotAccessors codomain conventions vs domain symbol typing
**ASN-0094, Slot Accessors / Definition — PointSlotAccessors**: "K_target_of : A_doc → A_doc^Σ ∪ {⊥}"
**Problem**: The domain A_doc is the catalog's symbolic constant (which expands at each Σ); the codomain A_doc^Σ ∪ {⊥} is state-indexed. Asymmetric typing. The same asymmetry appears in `from_K : A_doc → ℘_fin(A_K^Σ)` and `to_K : A_doc → ℘_fin(A_K^Σ)` throughout the catalog templates. The Codomain convention for partial templates explicitly lists state-indexed codomains; consistency would either pin both domain and codomain to a specific Σ-instance or treat both as symbolic.
**Required**: Either (a) make domain typing state-indexed throughout: "K_target_of^Σ : A_doc^Σ → A_doc^Σ ∪ {⊥}" with explicit Σ-parameterization, or (b) add a notational convention stating that the domain symbol A_doc means "the address must lie in A_doc^Σ at the state of evaluation" (so the symbolic name carries an implicit Σ-quantification). The current mixed reading is workable but inconsistent.

### Issue 5: "Prior" terminology in Initial-State Baseline
**ASN-0094, Initial-State Baseline / Scope of the per-tuple-conformance relaxation**: "The weaker check 'every prior L_K-tuple satisfies conf_K^{Σ_init}' is equivalent to the empty-baseline only for the per-tuple lemmas Sh0–Sh3..."
**Problem**: Σ_init is the initial state by definition; "prior" suggests a temporal predecessor that does not exist. The intended reading is "every tuple in L_K^{Σ_init}." This minor ambiguity propagates through three further uses of "prior" in the same paragraph and may confuse readers.
**Required**: Replace "every prior L_K-tuple satisfies conf_K^{Σ_init}" with "every tuple in L_K^{Σ_init} satisfies conf_K^{Σ_init}" (and analogous edits to subsequent "prior" usages in the same paragraph).

### Issue 6: from_K notational overload between SetSlotAccessors and catalog templates
**ASN-0094, Slot Accessors vs Per-Shape Template Walkthroughs (DirectedPair)**: SetSlotAccessors defines "from_K^Σ : L_K^Σ → ℘_fin(shape(K).t_F^Σ) with from_K^Σ(a, F, G) = slot_addrs(F)" (tuple to slot-address set). The DirectedPair catalog defines "from_K : A_doc → ℘_fin(A_K^Σ); from_K(a) ≡ {τ ∈ A_K^Σ : from₁(τ) = a}" (address to tuple set).
**Problem**: Two distinct functions share the name from_K (modulo Σ superscript). The first is the slot accessor on tuples; the second is the inverse-image function on addresses. The Σ-superscript distinguishes them, but readers tracking which is meant in dense proof contexts (e.g., the Sh4 contract's clause (i.a) Observe-result analysis) must repeatedly disambiguate.
**Required**: Either rename the catalog's inverse-image function (e.g., from_K_inv or addrs_K_with_from) or add an explicit cross-reference at each catalog row's first use of from_K, noting that this is the inverse-image of from₁ at the argument address, distinct from the slot-accessor from_K^Σ on tuples.

## OUT_OF_SCOPE

### Topic 1: (0, 0) shapes and additional canonical-shape bipartite extensions
**Why out of scope**: Acknowledged in Open Questions. The framework's discipline accommodates new rows via the same Sh5 META process; missing rows (e.g., (1, 1, A_rel, A_doc, ⊤) or (1, 1, A_rel, A_rel, ⊤)) are catalog-extension questions, not errors in this ASN.

### Topic 2: Ghost-targeting slot semantics
**Why out of scope**: Acknowledged in Open Questions. The framework intentionally forbids ghost addresses in F/G slots while permitting them in type-endset coverage per L9; admitting ghost slot semantics would require state-dependent conformance rules outside the current scope.

### Topic 3: Cross-process shape-registry consistency and multi-process Sh4 atomicity
**Why out of scope**: Acknowledged in Open Questions. The framework's atomicity scope is explicitly single-process (within-call sequentiality); a coordination protocol for distributed substrates is a separate design.

### Topic 4: Composite shapes (relations whose F or G is constrained by another relation's content)
**Why out of scope**: Acknowledged in Open Questions. Cross-relational constraints are a new design axis beyond the cardinality/target-domain/idempotency triad.

### Topic 5: Procedural derivation of template families from shapes
**Why out of scope**: Sh5(a)'s META observation explicitly documents that template families are hand-curated rather than mechanically derived from arbitrary shapes. The cost of this design choice is documented and the falsifiability discipline (Sh5(b)) compensates.

VERDICT: REVISE
