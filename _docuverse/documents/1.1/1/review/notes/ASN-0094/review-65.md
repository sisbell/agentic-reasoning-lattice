# Review of ASN-0094

## REVISE

### Issue 1: Global empty-link-store strengthening conflates framework requirement with walkthrough convenience
**ASN-0094, Initial-State Baseline**: "The framework additionally commits to the strictly stronger condition `dom(Σ_init.L) = ∅` globally — i.e., `L_K^{Σ_init} = ∅` for every `K ∈ T_admissible`, not just for every `K ∈ T_cat`. This is a substrate-level commitment of the framework's `Σ_init`."
**Problem**: The justification immediately after says the strengthening "is what underwrites the walkthroughs' `dom(Σ_0.L) = ∅` derivation through K.σ/K.α-only prefixes from `Σ_init`". But the framework's preservation theorems (Sh0–Sh4, FDD, SHCD) only consume per-K empty baselines `L_K^{Σ_init} = ∅` for `K ∈ T_cat`. The stronger global condition is justified as needed for K.λ first-emission predicate clarity in walkthroughs — i.e., for didactic purposes. The text labels this a "substrate-level commitment of the framework" but the preservation theorems don't require it.
**Required**: Either (a) downgrade the global strengthening to a walkthrough-only convention separable from the framework's substrate-level commitments, or (b) identify the specific framework-level claim that depends on it. The current presentation conflates two distinct levels.

### Issue 2: Sh4 contract clause (i.a) interleaves correctness and tightness derivations awkwardly
**ASN-0094, Sh4 idempotency contract clause (i.a)**: "Contract correctness is independent of clause (d) on the new emission's F. The contract's correctness... does not depend on whether the new emission's F satisfies Sh-conf clause (d)... *Over-approximation tightness — conditional on Sh-conf clause (d) holding for the new emission's F.*"
**Problem**: The contract specification's prose interleaves "what the contract guarantees regardless" with "what additional tightness holds conditionally". A reader must mentally separate the contract's load-bearing correctness (post-filter yields exact `C(F, G, Σ)` always) from the downstream tightness observation (Observe over-approximates only by superset relation when clause (d) holds). The factoring makes the contract harder to verify than necessary.
**Required**: Restructure clause (i.a) into two sequential paragraphs: first establish the contract's unconditional correctness (forward + reverse inclusion of `C(F, G, Σ)` via post-filter), then exhibit the tightness consequence under clause (d) as a downstream property used only in the *expository* analysis. The current commingling obscures which derivation discharges the contract.

### Issue 3: The four named layer-discipline commitments lack a consolidated reference
**ASN-0094, multiple sections**: The framework names *Emit_K routing commitment* (Scope and Substrate Scaffolding), *Sh4 idempotency contract* (Sh4 section), *FDD functional-dependency contract* (FunctionalDependencyDiscipline subsection), *single-home commitment* (SingleHomeCoverageDiscipline subsection).
**Problem**: Each commitment has distinct scope (per-K vs framework-wide), distinct trigger (shape-component vs opt-in registration), distinct gate position (1, 3, or pre-substrate), and distinct theorem discharged. The "Naming convention for distinct framework commitments" paragraph helps but readers tracking proof dependencies must consult multiple sections to recover each commitment's signature. The Gate Ordering (consolidated) clause partially addresses this but doesn't tabulate the commitments themselves.
**Required**: Add a consolidated reference table near Scope and Substrate Scaffolding listing the four commitments with columns: name, defining section, applicable K's, gate position, discharged theorem, and failure-mode summary. Forward-reference this table from each commitment's introduction.

### Issue 4: Walkthroughs are exhaustively detailed and impede framework readability
**ASN-0094, "Worked Example: K = comment" through "Sh4 emission suppression (Tuple-Classifier)"**: The walkthroughs collectively run thousands of lines, each enumerating multiple admission cases, rejection cases (often 3–4 per walkthrough), and per-template evaluation tables.
**Problem**: Each shape's walkthrough re-exercises Sh-conf's three gates and (where applicable) per-K discipline contracts with similar argumentative structure. Rejection cases like "G-side partition mismatch" appear in Classifier, Tuple-Classifier, and Attributed Retraction walkthroughs with structurally identical arguments. The volume buries the framework's substantive claims.
**Required**: Either (a) extract walkthroughs to an appendix, keeping a single canonical walkthrough per shape in the main body, or (b) cross-reference repeated rejection patterns rather than re-enumerating them. The Comment walkthrough's Rejection cases 1–4 establish patterns that subsequent walkthroughs invoke; flag this with cross-references.

### Issue 5: Sh5(b) checklist's "decidable per row" claim conflates per-symbol decidability with end-to-end procedural assurance
**ASN-0094, Sh5 META discipline, *Status of the audit table* paragraph**: "The checklist is procedural, not algorithmic: step 0 requires the author to compare the proposed shape tuple componentwise against R's... There is no automated tooling, no machine-checked enforcement, and no auditor role distinct from the catalog author — but every step is *decidable per row*..."
**Problem**: The phrase "decidable per row" suggests mechanical falsifiability, but the gap between per-symbol decidability and end-to-end checklist execution is significant. A catalog author may misclassify a symbol (e.g., omitting it from step 1's enumeration, or assigning it to the wrong category at step 2). The framework's META status acknowledges no auditor distinct from the catalog author; this leaves catalog correctness dependent on the catalog author's diligence, with no verification mechanism.
**Required**: Either (a) commit to a documented verification mechanism (e.g., a separate auditor role with explicit acceptance criteria), or (b) explicitly acknowledge that catalog correctness is contingent on the catalog author's diligence at each row, with the audit table serving as the post-hoc record rather than a verification gate. The current framing oscillates between these two readings.

### Issue 6: SubstrateConsumerActiveSubsetCompatibility's "exhaustiveness proof" Path (a) cites a hypothetical layer transition vocabulary the framework doesn't model
**ASN-0094, SubstrateConsumerActiveSubsetCompatibility Lemma, Path (a)**: "any layer that hosts an external component `X` whose value can vary independently of `(Σ.C, Σ.M, Σ.L)` admits transitions outside `↦`'s scope (e.g., wall-clock updates, layer-side metadata mutations, filesystem mtimes), and the construction proceeds in that layer's transition vocabulary."
**Problem**: The exhaustiveness argument's distinguishability construction operates at "the consuming layer's side, not the framework's" — but the framework provides no formal model of what the consuming layer's transition vocabulary may include. The Lemma's exhaustiveness then rests on an informal appeal to the existence of layer-side transitions outside `↦`'s scope, without formalizing such transitions. Path (b)'s "vacuous-satisfaction collapses" argument is rigorous; Path (a)'s argument is informal.
**Required**: Either (a) formalize the consuming layer's transition vocabulary extension as a parametric model the Lemma quantifies over, or (b) acknowledge Path (a) as an informal sketch rather than a load-bearing exhaustiveness proof, and rely on Path (b) alone for the formal exhaustiveness claim.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate support
**Why out of scope**: The framework explicitly commits to single-process substrates per the Sh4 idempotency contract's *Scope: single-process substrate* clause. Extending to multi-process settings would require a coordination protocol outside the framework. The Open Questions section flags this as a scope boundary.

### Topic 2: Mechanical template-body derivation from shape components
**Why out of scope**: Sh5(a) acknowledges no procedure derives template bodies from arbitrary shapes. Body-shape derivation requires meta-mathematical work beyond the framework's current commitment.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: Sh-conf clause (d) requires already-allocated slot addresses. Admitting ghost-targeting requires state-dependent conformance rules. Open Questions flags this.

### Topic 4: Runtime extension of T_cat
**Why out of scope**: Framework requires T_cat fixed at Σ_init. Runtime catalog growth would require modifying the empty-baseline assumption of Sh0–Sh4. Open Questions implicitly excludes this.

### Topic 5: Cross-process catalog consistency
**Why out of scope**: Lifetime constancy is asserted as a substrate-level commitment within a single process. Distributed catalog coordination is not addressed; Open Questions flags this as a scope boundary.

VERDICT: REVISE
