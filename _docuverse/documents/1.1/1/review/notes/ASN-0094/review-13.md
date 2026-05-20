# Review of ASN-0094

## REVISE

### Issue 1: Provenance template family asymmetric in the catalog table
**ASN-0094, Canonical Shape Catalog table, Provenance row**: "`outgoing_K(s)`"
**Problem**: Every other catalog row with `c_F = 1` or `c_G = 1` lists a full base template family (`pair_K`, `from_K`, `to_K`, `from_addrs_K`, `to_addrs_K`). Provenance `(1, 0|1, A, A, ⊤)` has `c_F = 1` (so `from₁` is total) and would mechanically generate the same base templates (with `to_K⁻` partial under `to₁⁻`). Sh5(b)'s discipline says "every catalog row's templates depend only on (i) the shape components, (ii) K's name, and (iii) explicitly named layer-supplied accessors" — but the Provenance row offers only one template with no justification for the omission. Either the row violates Sh5(b) by under-deriving, or there is a missing rationale for why partial `to₁⁻` precludes the other base templates.
**Required**: Either list the full base family for Provenance (with explicit handling for `to₁⁻ = ⊥`), or document why `c_G = 0|1` shapes generate only `outgoing_K` while structurally similar shapes generate five templates.

### Issue 2: Catalog table column format is inconsistent
**ASN-0094, Canonical Shape Catalog table**: rows use different formats for the "Template family" column.
**Problem**: Some rows have explicit "*base:* ... ; *opt-in (per-K):* ... ; *parametric:* ..." labels (DirectedPair, NonIdempotentDirectedPair). Resolution and Retraction list only "*primary consumption:*" with parenthetical "(column lists only this consumer, not the base family)". Classifier, Tuple-Classifier, Provenance use bare template lists with no base/opt-in/parametric tagging. This violates Sh5(b)'s uniform organization: reading the table, one cannot tell at a glance which templates are base, which opt-in, which parametric.
**Required**: Use uniform "base/opt-in/parametric" tagging across every row, even when only base templates exist. Resolution and Retraction should list their inherited base templates explicitly rather than directing the reader to the walkthroughs.

### Issue 3: Template codomains are implicit
**ASN-0094, DirectedPair**: "`K_target_of(a) ≡ to₁(τ)` where τ is the unique element of `from_K(a)` (returns `⊥` when `from_K(a) = ∅`)"
**ASN-0094, NonIdempotentDirectedPair Coverage**: "`latest_K_for_addr : A_doc → A_K^Σ ∪ {⊥}`"
**Problem**: `K_target_of`'s signature is never declared. It should be `A_doc → A_doc^Σ ∪ {⊥}` (returning a sidecar address or undefined), parallel to `latest_K_for_addr`'s explicit `A_doc → A_K^Σ ∪ {⊥}`. Without the signature, downstream type-checking against the template is ambiguous: does `K_target_of(a)` return an address (`A_doc^Σ`), a tuple (`A_K^Σ`), or something else?
**Required**: Declare explicit codomains for all partial-valued templates: `K_target_of : A_doc → A_doc^Σ ∪ {⊥}`, `to₁⁻ : L_K^Σ → t_G^Σ ∪ {⊥}`, etc. The pattern should be uniform across the framework.

### Issue 4: AllocatedAddressAntichain Lemma's symmetric Case 3 sub-case is hand-waved
**ASN-0094, AllocatedAddressAntichain proof, Case 3**: "WLOG `x ∈ dom(Σ.L), a ∈ dom(Σ.C)`; the sub-case `x ∈ dom(Σ.C), a ∈ dom(Σ.L)` proceeds identically with the subspace identifiers `s_L` and `s_C` exchanged in Step 3.3"
**Problem**: Dijkstra discipline: "no proof by 'similarly'." The symmetric case is genuinely structurally identical, but the proof should at least exhibit the swap explicitly — Step 3.1 unchanged; Step 3.2 unchanged (because `x ≼ a` is the hypothesis, independent of which side is link vs. content); Step 3.3 swaps `s_L ↔ s_C` via the symmetric scaffolding clauses. The current text gives only a parenthetical hint. Even when cases are symmetric, the explicit symmetry argument should be written out at least once for the load-bearing lemma that underwrites the syntactic/semantic bridge.
**Required**: Write out the symmetric sub-case's Step 3.3 explicitly, or add a one-paragraph "Symmetry argument" justifying why the swap is structurally valid (i.e., that the lemma's hypothesis `x ≼ a` is asymmetric in x and a only via the subspace assignment, which is what's swapped).

### Issue 5: Sh4 Case D's atomicity scope is informally characterized
**ASN-0094, Sh4 contract**: "The layer commits to executing clauses (i)–(iii) atomically with respect to other Sh4-emitters at the same `~`-equivalence class of K — concurrent emission and retraction events at any K' with `K' ~ K` that could split (i)'s observation from (iii)'s emission must be serialized by the layer."
**Problem**: "Concurrent" is not defined. In a single-process substrate the term has no meaning (transitions are sequential by construction). In a multi-process substrate, what constitutes "the same ~-equivalence class of K" is observable but the layer's coordination protocol is not specified. The framework labels Sh4 a "theorem under the layer-discipline contract" but the contract's atomicity premise is informal. This is acknowledged at end of Open Questions ("cross-process consistency... not addressed") but the Case D proof relies on the atomicity assumption being well-defined.
**Required**: Either restrict the framework's scope explicitly to single-process substrates (in which case "concurrent" reduces to "interleaved between Observe and Emit within a single Emit_K call sequence", trivially handled by within-call sequentiality), or specify the multi-process model that makes atomicity statable.

### Issue 6: `K_target_of`'s singleton-returning behavior depends on FDD but the dependency is not stated in the template's location
**ASN-0094, DirectedPair section, "Singleton-returning template under FunctionalDependencyDiscipline"**: The template definition appears after FDD's contract, but the catalog table row for DirectedPair lists `K_target_of(a)` as "*opt-in (per-K):* ... under FunctionalDependencyDiscipline".
**Problem**: A reader scanning the catalog table sees `K_target_of(a)` as an opt-in template. Following the table to the walkthrough section, the template is defined inside the FDD subsection. But the template's body ("the unique element of `from_K(a)`") presupposes singletonhood — a property guaranteed only by FDD, not derivable from the bare DirectedPair shape. If a reader registers `K` with DirectedPair *without* FDD and instantiates `K_target_of` from the catalog row, the template's definition is ill-formed (`from_K(a)` may be multi-valued). The opt-in tag in the table is necessary but the framework should also explicitly cite FDD's preservation theorem within the template's body.
**Required**: In the template's definition, add a precondition clause: "*Under FunctionalDependencyDiscipline, `from_K(a)` is empty or singleton at every reachable state* (by Lemma — FDD preservation, this section); `K_target_of(a)` returns `to₁` of the singleton when present and `⊥` otherwise." Without FDD, the template is undefined; the framework's catalog entry should make this unambiguous at the template's site of definition, not just in the table column.

### Issue 7: The catalog's NonIdempotentDirectedPair Coverage row depends on a derived `emission_order` not formally registered as a scaffolding clause
**ASN-0094, SingleHomeCoverageDiscipline definition**: "`emission_order(τ) := the chain-index of addr(τ) within the link sub-allocator chain at d_K` (by the substrate-conforming layer's chain enumeration discipline; cf. ASN-0086's FreshEmissionAddress)."
**Problem**: `emission_order` is presented as derived from chain enumeration plus T10a.7 plus T9, but the chain-index function itself is not a named scaffolding clause. The scaffolding section names "Per-document link sub-allocator chains" (existence) and "Uniform link sub-allocator chain length" (cardinality), but does not name "chain-index of an output" as an accessor. Sh5(b)'s discipline requires templates to depend only on shape + name + explicitly named accessors. `emission_order` is a derived function over implicit substrate machinery; its well-definedness requires the scaffolding to surface chain-indexing as a named accessor.
**Required**: Add a scaffolding clause: "*Link sub-allocator chain-index function.* For each `d ∈ dom(Σ.M)` and each `ℓ` in the chain at `d`, the substrate-conforming layer supplies `chain_index(ℓ, d) ∈ ℕ` such that `addr(ℓ) = inc^{chain_index(ℓ, d)}(d.0.s_L.1, 0)`. Well-defined by T10a.7." Then derive `emission_order(τ) := chain_index(addr(τ), home(τ))` from this scaffolding directly, without invoking implicit chain enumeration.

### Issue 8: The framework's effective-wp derivation forward-references Lemma RetractionTargetNotOnChain
**ASN-0094, Sh-conf section, "Effective weakest-precondition under Sh-conf"**: "Within the shape framework, this regime (i) collapse is secured *by Retraction's shape itself*... `NoCraftedSpanReachesD(Σ, d)` holds automatically at every Sh-conf-admitted Retraction call site (by Lemma — RetractionTargetNotOnChain below..."
**Problem**: Forward reference to a lemma proved later in the same section is OK in principle, but the wp derivation cites the lemma as part of its derivation chain — the reader must accept the lemma's conclusion before reading the lemma. The natural reading order is: state Sh-conf as axiom; state the lemma; derive the wp using the lemma. Alternatively, label the wp derivation as preliminary and note it depends on the upcoming lemma.
**Required**: Either reorder so that the lemma appears before the wp derivation, or add an explicit "(see Lemma below for proof)" marker at the point of citation.

## OUT_OF_SCOPE

### Topic 1: `(0, 0)` shape admission
**Why out of scope**: Raised in Open Questions. Whether a "single-tuple existence flag" shape is useful is a future design question, not an error in this ASN's current scope.

### Topic 2: Composite shapes (F or G constrained by another relation's content)
**Why out of scope**: Raised in Open Questions. Composite shapes require a new restriction axis beyond cardinality/target-domain/idempotency; this is forward work, not a defect in the current framework.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: Raised in Open Questions. The current framework forbids ghost slot addresses by Sh-conf clause (d); whether a future shape family should relax this is a design extension.

### Topic 4: Promoting FDD/SingleHomeCoverageDiscipline to shape-tuple components
**Why out of scope**: Raised in Open Questions. The current treatment as opt-in extensions atop the five-component shape is internally consistent; restructuring to a sixth component is a future refactor.

### Topic 5: Cross-process registry consistency
**Why out of scope**: Raised in Open Questions. Distributed substrate consistency is a deployment concern beyond the framework's current single-substrate scope.

VERDICT: REVISE
