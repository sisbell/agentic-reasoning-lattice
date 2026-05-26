# Review of ASN-0094

## REVISE

### Issue 1: Cross-ASN references to non-foundation ASNs

**ASN-0094, Definition — SubstrateConformingLayer**: "*ASN-0036 content/arrangement invariants:* S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ. *ASN-0093 substrate invariants:* M0, M1, C0, C1, C1b, C1c, C-fin."

**Problem**: ASN-0036 and ASN-0093 are not foundation ASNs (foundations are ASN-0034, ASN-0043, ASN-0086). The "Catalog (b) Chain Discipline Catalog" further enumerates ASN-0093-specific axioms by name (SubAllocatorAxiom, ChainMembershipForOrigin, etc.), and the paragraph explaining catalog (b)'s strictness ("L1c admits non-chain T10a-conforming chains... without catalog (b), a layer could publish an L-invariant-conforming non-chain emission that has no K.λ-replay") presupposes ASN-0093's specific chain discipline. The ASN restates needed properties as scaffolding clauses, but these enumerations create cross-ASN dependencies.

**Required**: Either drop the catalog enumerations (the locally stated scaffolding clauses already supply what the proofs need) or replace them with a self-contained characterization that does not name non-foundation invariants. The "Catalog (b) is strictly stronger" paragraph should be rephrased in terms of the ASN's own scaffolding clauses.

### Issue 2: Overly long introduction paragraph on semantic departure

**ASN-0094, introduction**: "*Load-bearing semantic departure from ASN-0086.* The framework registers Retraction with `idem = ⊤`, which changes ASN-0086's apparent multiset semantics at R to *set semantics* at the bare `Nullify` alias..."

**Problem**: This paragraph runs five sentences in the introduction, then defers to a downstream section ("The full rationale... is detailed in the *Nullify Compatibility* section"). The defer-to-downstream pattern combined with anticipatory motivation reads as front-matter accretion. The Nullify Compatibility section later covers the same material in proper context.

**Required**: Compress to a single sentence in the introduction naming the change and pointing to Nullify Compatibility. Move the rationale entirely into that section.

### Issue 3: Defensive meta-prose at parametric template signature

**ASN-0094, Resolution-shape parametric extension**: "The catalog's parametric column entries on the NonIdempotentDirectedPair row carry this shape precondition implicitly by naming 'Resolution' as the parametric-argument class — restated explicitly here, as the *Signature derivation rule* requires every template body to declare the registered shape of any parametric argument it consumes."

**Problem**: This sentence justifies why the explicit restatement exists (citing a hand-curation convention). It is "new prose around an axiom explains why [the explicit form] is needed rather than what it says." The preceding signature with shape precondition stands on its own; the meta-justification adds no information.

**Required**: Remove the trailing justification sentence. The shape precondition is part of the signature, as the paragraph already states.

### Issue 4: Two paragraphs covering coverage-class disjointness from R

**ASN-0094, after EffectiveWpSimplification**: "Coverage class disjointness from R is enforced by the registry's per-class constancy applied at the Retraction shape tuple..." followed immediately by "*General note for every non-R catalog row.* For every K registered at a catalog row whose shape tuple differs from R's..."

**Problem**: The two paragraphs handle adjacent cases (same-shape-as-R vs different-shape-from-R) but their joint purpose — establishing `K ≁ R` for every non-R catalog row — could be a single paragraph. The second paragraph's closing sentence ("Per-shape sections below cite this note rather than re-deriving...") is forward-reference accretion; the per-shape sections do not actually need to cite the note since `K ≁ R` follows directly from per-class constancy at each call site.

**Required**: Consolidate into one paragraph. Drop the "Per-shape sections below cite this note" sentence — the per-shape sections should derive `K ≁ R` inline if needed, not by named-reference.

### Issue 5: Sh4 Case A enumeration's "exhaustive coverage" defensiveness

**ASN-0094, Sh4 preservation proof, Case A**: "The enumeration is exhaustive for *Case A coverage* within the framework's `↦`-vocabulary: every `↦`-step that produces the case-equation falls into exactly one of these four classes, and each class's discharge is cited explicitly so a reader can verify Case A's coverage end-to-end."

**Problem**: This sentence asserts exhaustiveness after the four-class enumeration. Lemma CaseAClosureForLK already establishes the partition; restating exhaustiveness here is the "explains why X is needed rather than what it says" pattern. The Sh0 proof references CaseAClosureForLK directly without this prose; Sh4 should too.

**Required**: Remove the closing exhaustiveness sentence. The Case A discharge is identical in structure to Sh0/Sh1/Sh2/Sh3 (which cite CaseAClosureForLK); Sh4 can do the same instead of re-enumerating.

### Issue 6: AllocatedAddressAntichain Case 3 length handling

**ASN-0094, Lemma AllocatedAddressAntichain, Case 3**: "From `x ≼ a` (Prefix): `#x ≤ #a` and componentwise agreement `aᵢ = xᵢ` for `1 ≤ i ≤ #x`. We dispatch on `#x = #a` versus `#x < #a`."

**Problem**: The proof announces a dispatch on length but then proceeds through Steps 3.1–3.3 without using the dispatch. Step 3.2's E-field agreement at `i = n_3 + 1` works uniformly for both length cases. Either the dispatch is unnecessary (and the announcement misleads the reader) or there is a sub-case argument that has been collapsed.

**Required**: Drop the "We dispatch on `#x = #a` versus `#x < #a`" sentence. The argument is uniform; no length dispatch is needed.

### Issue 7: Two scope-related sentences in different sections covering single-process substrate

**ASN-0094, Sh4 contract section**: "*Scope: single-process substrate.* The framework is restricted to single-process substrates..."

**ASN-0094, Open Questions [scope boundary]**: "Should the shape registry stay consistent across processes? Lifetime constancy is asserted as a substrate-level commitment within a single process..."

**ASN-0094, FDD contract section**: "The same single-process-substrate scope from Sh4's contract applies..."

**Problem**: Three locations re-establish the single-process scope. The Open Questions entry is the appropriate location for the scope boundary; the Sh4 and FDD contract sections cite the scope but don't need to re-explain it. The third mention is "multiple paragraphs in different sections defer to the same downstream location."

**Required**: Establish the scope once (in either the Scope and Substrate Scaffolding section or in a single Open Questions entry). Other locations should refer to it by name without restating the rationale.

### Issue 8: Template signatures use overloaded `from_K^Σ`/`from_K(a)` without explicit disambiguation

**ASN-0094, Definition — SetSlotAccessors**: `from_K^Σ : L_K^Σ → ℘_fin(shape(K).t_F^Σ)`; **DirectedPair template**: `from_K(a) ≡ {τ ∈ A_K^Σ : from₁(τ) = a}`.

**Problem**: The same symbol `from_K` is used for two functions with different signatures and semantics (one takes a tuple, returns slot-address set; the other takes an address, returns tuple-set). The "Notational overload" comment notes them but the disambiguation rests on argument type alone. With Σ-superscript on one and not the other, readers must infer which is meant from context.

**Required**: Rename one of the two functions to remove the overload. For example, use `slots_F(τ)` for the tuple-to-slot-address-set accessor and reserve `from_K(a)` for the address-to-tuple-set accessor. The current convention is workable but invites confusion in proofs.

### Issue 9: Catalog Curation Discipline NOTE entry in Properties Introduced

**ASN-0094, Properties Introduced (Supporting definitions table)**: "Catalog Curation Discipline | NOTE | Hand-curation conventions for per-shape template families..."

**Problem**: This entry is meta-organizational rather than load-bearing. The three "hand-curation conventions" are author conventions, not specification content. Listing them in the Properties Introduced table elevates author conventions to the same status as definitions and lemmas, blurring what the framework actually guarantees.

**Required**: Remove from Properties Introduced. If author conventions need a named anchor, place them in a separate "Authoring Conventions" section that is clearly distinct from spec content.

### Issue 10: Worked example for K = comment has inconsistent reference to Sh-conf gate ordering

**ASN-0094, K = comment walkthrough**: Emission 1' description: "Why no Sh4 suppression fires. `comment` has `shape(K).idem = ⊥` (NonIdempotentDirectedPair), so K is not registered under the *Sh4 idempotency contract*. The Sh4 contract's gate-3 candidate-set check `C(F_1, G_1, Σ_1)` is *not executed* — gate 3 is skipped entirely at idem = ⊥ K not under FDD..."

**Problem**: The walkthrough invokes gate 3 by reference without re-establishing context. The Gate Ordering section is in a different part of the document (early in the Conformance Axiom section). Long walkthrough text should be self-contained or cite the precise location.

**Required**: Either (a) repeat the gate position label at first use in each walkthrough, or (b) drop the "gate-3" terminology and use the natural language "the Sh4 contract's candidate-set check does not fire because `comment` is not under that contract."

## OUT_OF_SCOPE

### Topic 1: Cross-process consistency of the shape registry

**Why out of scope**: The framework explicitly restricts itself to single-process substrates. Multi-process registry consistency (concurrent shape re-registration, distributed Sh4 atomicity at the `~`-class scope) is correctly flagged in Open Questions as a future direction. A future ASN can address distributed substrate semantics.

### Topic 2: Non-empty initial link store baseline

**Why out of scope**: Sh4/FDD/SHCD preservation requires `L_K^{Σ_init} = ∅`. The framework documents this in Open Questions as a scope boundary; retrofitting onto persistent or loaded link stores belongs in a separate ASN that establishes the registration-time verification protocol.

### Topic 3: A_M symbol for document-container targeting

**Why out of scope**: The framework provides target-domain symbols `A_doc` (content), `A_rel` (relation), `A` (union). It correctly notes in Open Questions that adding `A_M` for `dom(Σ.M)` would re-enable metalink-style targeting at the registry level. This is a real extension that belongs in a follow-on ASN.

### Topic 4: Composite shapes (relations constrained by another relation's content)

**Why out of scope**: Whether to admit composite shapes — relations whose slot constraints depend on the content of other relations — is a structural extension question. Currently the catalog's atomic vocabulary plus parametric `_via` templates suffices; composite shapes are correctly listed as a refinement candidate in Open Questions.

### Topic 5: Closure theorem for composite predicates

**Why out of scope**: The framework does not establish a closure result for predicates built by Boolean composition and quantification over `T_cat`. The Consequences section appropriately notes this is a weaker claim than a closure theorem. A formal closure result would be a future ASN topic.

VERDICT: REVISE
