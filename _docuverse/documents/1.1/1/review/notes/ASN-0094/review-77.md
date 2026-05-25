# Review of ASN-0094

## REVISE

### Issue 1: Direct references to non-foundation ASNs (ASN-0036, ASN-0093)
**ASN-0094, SubstrateConformingLayer Definition**: "*ASN-0036 content/arrangement invariants:* S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ. *ASN-0093 substrate invariants:* M0, M1, C0, C1, C1b, C1c, C-fin."
**Problem**: Per the review rules, only ASN-0034, ASN-0043, and ASN-0086 are foundation ASNs. References to ASN-0036 and ASN-0093 by number violate the no-cross-ASN-reference rule. Additional violations appear throughout the document: Lemma — LinkAddressNotPrefixOfEmit's scaffolding citations, Nullify Compatibility's "ASN-0036 invariants", multiple paragraphs invoking "ASN-0093 L0", "ASN-0093 R0a-Cor1" (where R0a-Cor1 is from ASN-0086, but the qualifier compounds the issue), and the Catalog (b) "ASN-0093 chain discipline catalog".
**Required**: Inline the substantive content (the scaffolding clauses section already does this for most usages — extend the same treatment to the SubstrateConformingLayer Definition). Reference cited invariants by their property names (S0, M0, etc.) without ASN qualifiers, OR define the necessary properties locally.

### Issue 2: EffectiveWpSimplification corollary does not explicitly verify A_K^{Σ'} active-subset claim
**ASN-0094, EffectiveWpSimplification**: "the framework's *effective wp* for the postcondition 'a fresh `(a, F, G)` is deposited in `A_K^{Σ'}'`..."
**Problem**: The proof's Steps 1 and 2 discharge wp_086's preconditions (NoCraftedSpanReachesD and the self-coverage disjunct), but the postcondition is phrased over A_K^{Σ'} (active subset), not L_K^{Σ'} (audit slice). For K ≁ R the argument that addr(τ_new) ∉ nullified(Σ') follows because nullified(Σ') = nullified(Σ) and addr(τ_new) ∉ A_rel^Σ; for K ~ R the argument needs both Step 1 (no prior R-tuple nullifies τ_new) and Lemma RetractionSelfFreshness (τ_new does not self-nullify). Neither argument is explicit in the proof — RetractionSelfFreshness is not named at the active-subset step, and the fresh-address-not-in-nullified(Σ) reasoning is left implicit.
**Required**: Add an explicit Step 3.5 or appendix to the proof verifying that addr(τ_new) ∉ nullified(Σ') for both K ≁ R and K ~ R cases, naming RetractionSelfFreshness where invoked.

### Issue 3: Hand-curated template bodies acknowledged but framework's "predicate language" claim is weakened
**ASN-0094, Consequences (a)**: "*Adding a new relation inherits its shape-mate's templates by hand-curation.* ... Body-shape convergence with prior shape-mate rows is an aspiration of the present catalog (per the per-shape uniformity convention), not a framework-enforced derivation: registering a divergent template body at the same shape is not blocked by any mechanical gate."
**Problem**: The introduction claims the framework provides a "typed predicate vocabulary" with templates "mechanically organized (though not mechanically derived)". The mechanical organization is only the signature derivation; bodies are hand-curated and unverified. The framework's load-bearing content (Sh-conf + Sh0-Sh4 + contracts) does not constrain template body shape, only the shape registry and slot accessors. Consumers depending on "Citation usage" or "Attribute usage" aliases get those guarantees only through author diligence, not through framework derivation. The prompt's standard "Every invariant conjunct addressed" applies here: the body-shape uniformity convention is asserted but not provable, leaving a gap between the framework's pitch and its formal content.
**Required**: Reframe Consequences (a) to clearly distinguish what the framework formally provides (shape registry + Sh-conf + Sh0-Sh4 + slot-accessor totality from cardinality) from what is author-curated (template body shape consistency). Alternatively, provide a mechanical body-derivation rule from the shape components (which would tighten the framework but require additional work).

### Issue 4: Forward-reference accretion — repeated meta-prose around per-shape uniformity convention
**ASN-0094, Per-Shape Template Walkthroughs (multiple sections)**: The phrase "Signatures derived mechanically per the *Signature derivation rule*; bodies hand-curated against the DirectedPair shape-mate per the per-shape uniformity convention" appears verbatim or near-verbatim in DirectedPair, Resolution, Retraction, BundledDirectedPair, and Provenance sections. NonIdempotentDirectedPair has a near-identical phrasing without the explicit shape-mate reference.
**Problem**: Each per-shape section restates the curation convention rather than referencing it. The Catalog Curation Discipline note already establishes the conventions globally; repeating them in every per-shape section adds no information and increases the document's length without advancing the argument. This matches the forward-reference accretion pattern: "a paragraph looks like a prior finding's content relocated rather than removed".
**Required**: State the convention once in the Catalog Curation Discipline note. In per-shape walkthroughs, restate only shape-specific deviations from the convention (if any).

### Issue 5: SubAllocatorAxiom and chain-discipline catalog items are named but not defined
**ASN-0094, SubstrateConformingLayer Definition**: "*(b) Chain Discipline Catalog.* SubAllocatorAxiom, ChainMembershipForOrigin, ChainEnumerationInjectivity, ChainUniformLength, ChainUniformZeroCount, ChainPrefixExtension, ChainElementT4Validity, DisjointSubAllocatorChains, StoreT4Validity, FirstEmissionFreshness, CrossDocDisjointness."
**Problem**: These eleven properties are named but not defined or located in ASN-0094 itself. They presumably come from ASN-0093 (a non-foundation ASN), but the catalog gives no signatures or statements for any of them. Substrate-conforming layers must satisfy them, but the ASN under review provides no way to verify what "satisfy" means. The scaffolding clauses paragraph above introduces a few related items (per-document link sub-allocator chains, uniform chain length, chain-index function), but doesn't cover the eleven.
**Required**: Either define each chain-discipline catalog item locally (consistent with the framework being self-contained), OR fold them into the scaffolding clauses section with explicit signatures, OR remove the catalog (b) reference and rely solely on the scaffolding clauses.

### Issue 6: T_cat representative-list state model is informal
**ASN-0094, TypedRelationCatalog Definition**: "Concretely, T_cat is specified by listing one representative per class, with closure under ~ implicit."
**Problem**: The framework treats T_cat as lifetime-constant configuration, but does not formalize the "representative list" as a state component. The registration interface paragraph ("The layer registers one representative endset K_rep per ~-equivalence class in T_cat / ~") is described but not formalized — when does registration happen? What is the relationship between the list and Σ_init? The lifetime constancy claim depends on these unstated registration semantics.
**Required**: Formalize the representative list as a layer-supplied configuration parameter (analogous to the shape registry), with explicit lifetime-constancy semantics (e.g., "the layer fixes the representative list before Σ_init is constructed and never modifies it").

### Issue 7: NoCraftedSpanReachesD Step 1 implicitly assumes Sh1 and Sh3 apply at R
**ASN-0094, EffectiveWpSimplification Step 1**: "For every `(b̂, F', G') ∈ L_R^Σ`, Sh1 at `K := R` gives `G'` canonical-slot with `|slot_addrs(G')| = 1`; Sh3 at `K := R` gives `slot_addrs(G') ⊆ A_rel^Σ`."
**Problem**: Sh1 and Sh3 quantify over K ∈ T_cat. The proof assumes R ∈ T_cat. This is true under the framework's baseline registration requirement (NullifyCompatibility section), but the corollary's Preamble does not state R-registration as a hypothesis. The same omission affects Lemma RetractionSelfFreshness's invocation of Sh1/Sh3 in part (ii). Without explicit R-registration in the preconditions, the corollary applies only when R happens to be registered — which is asserted as mandatory elsewhere but not surfaced where it's load-bearing.
**Required**: Add "R ∈ T_cat" to the Preamble of EffectiveWpSimplification and RetractionSelfFreshness (or cite the mandatory registration from NullifyCompatibility explicitly in their preconditions).

### Issue 8: Sh-conf's Π_K formula's mutual-exclusivity claim is asserted but not proven
**ASN-0094, EffectiveWpSimplification**: "The three implications are mutually exclusive at any K (FDD and SHCD are structurally incompatible since they require distinct `idem` values; Sh4 fires automatically at idem = ⊤ K not under FDD)."
**Problem**: The parenthetical justification is informal. FDD requires `shape(K) = (1, 1, A_doc, A_doc, ⊤)` (idem = ⊤). SHCD requires `shape(K) = (1, 1, A_doc, A_doc, ⊥)` (idem = ⊥). At any K, shape(K).idem is fixed, so K cannot be under both FDD and SHCD simultaneously. The Sh4 clause "Sh4 fires automatically at idem = ⊤ K not under FDD" is true by the Sh4 contract's gating; but the disjointness claim that "Sh4 fires" excludes "Sh4 dormant under FDD" is implicit. State the mutual-exclusivity argument once explicitly so downstream consumers can verify which Π_K conjunct applies.
**Required**: Add a brief tabular or prose statement at the Π_K definition listing which combinations of K registrations select which implication, with the gate decisions explicit.

### Issue 9: Per-shape walkthroughs vary in completeness without explanation
**ASN-0094, Per-Shape Template Walkthroughs**: The Comment walkthrough (NonIdempotentDirectedPair) is detailed with 5 emissions, retraction, and template evaluations at multiple states. The Classifier walkthrough is much shorter, with one admit/reject pair. Resolution, Tuple-Classifier, Retraction, and Provenance have no standalone walkthroughs.
**Problem**: The asymmetric coverage doesn't establish that the framework's preservation theorems apply uniformly across shapes. The Comment walkthrough verifies Sh0-Sh3 at Σ_2 by direct check, but no analogous check appears for other shapes. The Sh4 idempotency contract's behavior under bare Retraction is described in the Nullify Compatibility section but not exercised in a worked example.
**Required**: Either justify the asymmetric coverage (e.g., "Comment is the most complex case; other shapes follow by symmetry"), OR add minimal walkthroughs for the missing shapes demonstrating one admit, one shape-distinctive rejection, and Sh0-Sh3 verification.

## OUT_OF_SCOPE

### Topic 1: Multi-process concurrency for Sh4/FDD/SHCD contracts
**Why out of scope**: Explicitly flagged as a scope boundary in Open Questions. The framework's single-process atomicity premise is a stated design commitment, not a gap.

### Topic 2: Non-empty initial L_K baselines
**Why out of scope**: Explicitly flagged in Open Questions as a retrofit limitation requiring layer-side baseline verification. Characterizing the minimum baseline check extends the framework rather than fixing it.

### Topic 3: Container-level link targeting (A_M symbol)
**Why out of scope**: Explicitly flagged in Open Questions. The framework's choice to omit document-container targeting follows the implementation; admitting it would require new catalog entries, not corrections to existing ones.

### Topic 4: Composite/parametric shape closure
**Why out of scope**: Open Question (b) on composite predicates and (f) on composite shapes both flag this as future work. The framework's atomic-shape catalog plus type-index parametrics is the current expressive vocabulary; extending it is a future ASN.

### Topic 5: Higher-arity (> 3) link support
**Why out of scope**: The Scope section explicitly restricts the framework to arity-3 (standard-triple) links. Extending to higher arities requires additional shape components and templates per slot, which is structural work for a different ASN.

VERDICT: REVISE
