# Review of ASN-0094

## REVISE

### Issue 1: Pattern 6 misattribution in Common rejection patterns
**ASN-0094, Per-Shape Template Walkthroughs preamble**: "patterns 5–6 derived first at Classifier and at Comment's Edge case respectively."
**Problem**: Pattern 6 is "Per-K-discipline-suppression rejection." The Comment walkthrough's "Edge case" is a `Nullify` of τ_1 — a retraction event, not a per-K-discipline suppression. Per-K suppression is first derived later in the FDD walkthrough (Emission FDD2) and Provenance (Form 3). The forward reference is incorrect.
**Required**: Point pattern 6's first derivation to either the FDD walkthrough or the Provenance Form 3 example, whichever you intend as canonical.

### Issue 2: Missing section header for FDD walkthrough
**ASN-0094, Additional Worked Examples**: The walkthrough beginning "Register `K = attribute` with shape `(1, 1, A_doc, A_doc, ⊤)` (DirectedPair) and additionally register FunctionalDependencyDiscipline at K" has no section header, appearing immediately after the EffectiveWpSimplification walkthrough sub-paragraph inside the Attributed Retraction example.
**Problem**: Reader cannot locate the FDD example by scanning section headers; it appears to be a continuation of Attributed Retraction.
**Required**: Add a section header (e.g., "### Attribute under FunctionalDependencyDiscipline") at the right place.

### Issue 3: Cross-ASN references to ASN-0036 and ASN-0093
**ASN-0094, Definition — SubstrateConformingLayer**: "*(a) Invariant Catalog.* The full L/S/M/C invariant list of ASN-0036, ASN-0043, and ASN-0093: … *ASN-0036 content/arrangement invariants:* S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ. *ASN-0093 substrate invariants:* M0, M1, C0, C1, C1b, C1c, C-fin."
**Problem**: The foundation ASN list is ASN-0034, ASN-0043, ASN-0086. ASN-0036 and ASN-0093 are non-foundation references. The invariants named are not restated. Each scaffolding fact this ASN actually consumes is already captured by the explicit scaffolding clauses immediately below (element-level addresses, subspace partitions, content-store antichain/monotonicity/finiteness, document address structure, link sub-allocator chains, chain-index function).
**Required**: Drop the catalog (a) named-invariant listing entirely and rely solely on the scaffolding clauses. The ASN's preservation theorems do not actually invoke any S/M/C invariant by name beyond what the scaffolding already supplies.

### Issue 4: `wp_eff` does not cover the vacuous case
**ASN-0094, Corollary — EffectiveWpSimplification**: "`Π_K` is the per-K discipline non-suppression conjunct: K-under-SHCD ⟹ d = d_K (gate 1); K-with-idem = ⊤ ∧ not-under-FDD ⟹ C(F, G, Σ) = ∅ (gate 3 under Sh4); K-under-FDD ⟹ C_fd(F, Σ) = ∅ (gate 3 under FDD). The three implications are mutually exclusive…"
**Problem**: For K with `idem = ⊥` and neither SHCD nor FDD registered (e.g., bare NonIdempotentDirectedPair), all three implication antecedents are false, so `Π_K` is vacuously true. Stating mutual exclusivity without stating the vacuous case leaves the reader unsure whether the cases are exhaustive. The wp formula needs to be well-defined at every K registered in T_cat.
**Required**: Add: "When K is registered without any of the three disciplines (idem = ⊥ and not under SHCD/FDD), no implication's antecedent fires and `Π_K = true` vacuously."

### Issue 5: Sh-conf return-type composition under multi-gate rejection is implicit
**ASN-0094, Sh-conf section and Gate Ordering**: Sh-conf says "On any failure, `Emit_K` returns `⊥` and leaves state unchanged"; per-K contracts also return `⊥` on suppression. The Gate Ordering paragraph then describes a 5-gate sequence with "On failure of any conjunct, `Emit_K` returns `⊥`."
**Problem**: The formal specification of how the gates compose to yield a single `⊥` is not stated. Two gates failing at the same call produce one `⊥`, not two; this is operationally clear but not pinned down formally (e.g., as a sequential left-to-right short-circuit on the gate stack). The CallerSideClassification protocol depends on the order being deterministic.
**Required**: Add a one-sentence formal statement that the gates evaluate left-to-right in the Gate Ordering and short-circuit at the first failure, with the rejection cause being that gate's name. This matches the CallerSideClassification protocol's halt-at-first-failure semantics.

### Issue 6: AllocatedAddressAntichain finiteness claim sits in Definition prose
**ASN-0094, Definition — AllocatedCoverage**: "This set is finite at every Σ (since `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` is finite by the content-store finiteness scaffolding for `dom(Σ.C)` and L-fin (ASN-0043) for `dom(Σ.L)`)..."
**Problem**: A derivation lives inside a Definition's prose with no postcondition label. Downstream proofs (Sh4 contract, FDD contract) consume this finiteness without citing it.
**Required**: Promote finiteness and monotonicity of `cov_allocated` into named postconditions of the Definition (or a brief Lemma), so consumers can cite by name.

### Issue 7: Bloat — forward-reference apologetics and scope-and-consumption paragraphs
**ASN-0094, Lemma LinkAddressNotPrefixOfEmit ("*Generality.*"), Lemma RetractionSelfFreshness ("*Scope and consumption.*"), and "*Stating RetractionSelfFreshness here, before the induction begins, separates the structural establishment...*"**
**Problem**: Multi-paragraph essays explaining where each lemma is consumed, why it's stated where it is, and what it is "deliberately recorded" to do. The `review-mode.anti-bloat` classifier flags this pattern: meta-prose about forward references and consumption sites does not advance the technical argument. A precise reader follows the proof at the use site; pre-justification is noise.
**Required**: Remove these meta-paragraphs. State each lemma once and use it. If a lemma is genuinely consumed at two sites, the consumption sites themselves discharge the relevance.

### Issue 8: Bloat — defensive design-choice essays
**ASN-0094, Retraction row ("*Note on `pair_K`'s set-equality F-side argument (deliberate, role-specific design choice).*")** and BundledDirectedPair row ("*Symmetric design choice with Retraction's `pair_K`.*"):
**Problem**: Multi-sentence essays explaining why a `pair_K` definition is "deliberate" and contrasting it against the rejected alternative. This is reviewer-response prose, not specification content. The Sh5(b) admissibility check covers form; the design intent is one sentence at most.
**Required**: Collapse each note to a single sentence stating the body and noting that the membership-reading is expressible from the other base templates by intersection.

### Issue 9: Bloat — Resolution standalone admissibility prose
**ASN-0094, Resolution catalog row and Resolution walkthrough**: Multiple paragraphs ("*Standalone admissibility (exhibited via hand-curation; verification depends on Sh5(b)'s citation convention)*" and "*The framework's preservation theorems (Sh0–Sh4) and the templates' definitional bodies are unchanged at a standalone registration*"…) defend that Resolution may be used without `_via` consumers in scope.
**Problem**: Sh5(b) is already declared as "a design convention enforced by catalog-author diligence rather than by a tooled gate," so a standalone-admissibility claim adds nothing beyond reading the listed bodies. The defensive framing is essay content.
**Required**: Collapse to one sentence: "Resolution's base templates depend only on shape components and Sh0–Sh4; standalone registrations work identically to consumed registrations."

### Issue 10: Bloat — "Nelson's design vocabulary" essay
**ASN-0094, NonIdempotentDirectedPair section**: "*Nelson's design vocabulary on links and semantics.* Nelson's design intent (Literary Machines) is explicit that all Xanadu links share one mechanism, with semantic interpretation (supersession, comment, citation, etc.) carried entirely by the type endset's address…"
**Problem**: Pure historical/philosophical defense of the framework's neutrality about supersession-vs-comment readings. Does not advance any claim, prove any theorem, or constrain any operation.
**Required**: Delete the paragraph. If a one-line note is needed to flag the neutrality, state it as "The discipline applies structurally to any `(1, 1, A_doc, A_doc, ⊥)` K; the framework imposes no semantic taxonomy on which readings are admissible."

### Issue 11: Bloat — Status and Failure-modes repeated across three contracts
**ASN-0094, Sh4 / FDD / SHCD subsections**: Each contract has near-identically structured *Status.* and *Failure modes under contract violation.* paragraphs explaining "this is a theorem under the contract, not a substrate-enforced axiom."
**Problem**: Three repetitions of the same structural observation. The Consolidated Commitment Reference Table already establishes that each contract has a layer obligation and a corresponding theorem.
**Required**: Factor a single "Contract status and failure modes" paragraph at the framework level, with per-contract specifics referenced from there.

### Issue 12: Bloat — opening R-lemma inventory
**ASN-0094, opening paragraph**: "ASN-0086 establishes typed relations `L_K` with the three operations Emit, Observe, Nullify, governed by the lemma family R0…R7a (concretely: R0, R0a, R0a-Cor1, R0a-Cor2, R1, R2, R3, R4, R5, R5-Cor, R6a, R6b, R6c, R6c-Corollary, R7a, together with the auxiliary lemma LinkStoreInvarianceUnderArrangement)."
**Problem**: The enumerated inventory is a use-site inventory. Reader does not gain anything from seeing every R-lemma named in the first sentence.
**Required**: Cut the parenthetical inventory. "R0…R7a" suffices; consumers cite individual R-lemmas at use sites.

### Issue 13: Bloat — "Cross-`~`-class concurrency is benign" paragraph
**ASN-0094, Sh4 idempotency contract**: A paragraph defending why the contract's atomicity scope is restricted to the `~`-equivalence class of K and not widened to all retractors.
**Problem**: Defensive justification of a scope choice. The contract's atomicity statement plus the active-subset construction at retraction already give the reader what they need.
**Required**: Delete the paragraph or reduce to one sentence: "Cross-`~`-class retraction does not race with Emit_K because it can only remove existing tuples, not introduce slot-pair collisions."

### Issue 14: Bloat — per-walkthrough "Registered catalog" paragraphs after framework-level convention
**ASN-0094, Initial-State Baseline ("*Per-walkthrough convention.*") and every walkthrough's "Registered catalog for this walkthrough"**: The framework establishes the per-walkthrough convention once, then each walkthrough still prefixes a "Registered catalog" paragraph re-declaring T_cat.
**Problem**: Duplication. Most walkthroughs add only one entry beyond `R`; that information can ride at the head of the walkthrough's first emission instead of a stand-alone paragraph.
**Required**: Keep the framework-level convention; drop the per-walkthrough paragraph except when the walkthrough's T_cat genuinely needs explanation beyond a one-liner (FDD example, possibly Comment).

### Issue 15: Bloat — "the framework, defined" use-site listing
**ASN-0094, end of Scope and Substrate Scaffolding**: "*The framework, defined.* 'The framework' denotes the shape discipline atop ASN-0086 introduced here, comprising: (1) the conformance axiom **Sh-conf**, (2) preservation lemmas **Sh0–Sh4**, (3) the idempotency theorem **Sh4** with auxiliary lemma **LinkAddressNotPrefixOfEmit** and corollary **EffectiveWpSimplification**, (4) the META catalog **Sh5**, and (5) the four layer-discipline contracts plus the substrate-conforming-layer scaffolding."
**Problem**: Reads like an essay's table of contents inside the prose. The Properties Introduced table at the end already serves this role.
**Required**: Drop this paragraph; the Properties Introduced table is the structural index.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate / distributed Sh4 atomicity
The Sh4 and FDD contracts commit to single-process serialization. A multi-process substrate would need a `~`-class lock or equivalent. Open Questions flags this correctly.

### Topic 2: `dom(Σ.M)` (container-level) targeting
The catalog provides no `A_M` symbol; container-level targeting (Nelson's metalinks) is not expressible. Open Questions flags this as scope boundary.

### Topic 3: Ghost-targeting slot semantics
L9 admits ghost spans generally but Sh-conf forbids them in slot positions. A future shape family could admit ghost targeting under a state-conformance rule. Open Questions flags this.

### Topic 4: Non-empty initial link store
Sh4/FDD/SHCD preservation theorems require `L_K^{Σ_init} = ∅`. Retrofitting onto a non-empty initial store would need per-K baseline verification. Open Questions flags this.

VERDICT: REVISE
