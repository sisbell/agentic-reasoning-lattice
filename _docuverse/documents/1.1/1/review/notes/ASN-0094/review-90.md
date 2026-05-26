# Review of ASN-0094

## REVISE

### Issue 1: Multi-paragraph defensive prose for each commitment in Scope section
**ASN-0094, Scope and Substrate Scaffolding**: Every commitment paragraph (*Emit_K routing commitment*, *R-registration commitment*, *Empty-baseline commitment*, *Named layer-discipline commitments*, *Substrate-conforming-layer scaffolding*) follows the pattern: state the commitment in one sentence, then write multiple sentences explaining why it exists, what fails without it, and what falls "outside the framework's scope." The R-registration commitment alone consumes ~7 sentences justifying itself after a one-sentence statement.
**Problem**: New prose around an axiom explains why the axiom is needed rather than what it says — exactly the forward-reference accretion pattern. The justification is the same shape repeated for each commitment ("would otherwise reject..., produces ... the framework's preservation theorems cannot reason about").
**Required**: Each commitment should state the commitment in one or two sentences. Out-of-scope consequences belong in Open Questions or in a single shared sentence, not repeated per-commitment.

### Issue 2: ShapeRegistry's lifetime-constancy justification paragraph
**ASN-0094, ShapeRegistry definition**: "Lifetime constancy is a substrate-level commitment, not derivable from R0…R7a. It is what lets Sh-conf evaluate emissions against a stable shape that matches the shape under which prior tuples of the same type were emitted, so the inductive proofs of Sh0–Sh3 can rely on a fixed conformance predicate. Mutable shape re-registration (e.g., relaxing a cardinality bound after some tuples are already emitted) would invalidate the induction; the framework forbids it."
**Problem**: This explains why the property exists ("it is what lets...", "would invalidate the induction") rather than stating what it is. Definition prose enumerating downstream consumers.
**Required**: Replace with the property only. The "what would invalidate the induction" hypothetical and the appeal to Sh0–Sh3 are forward-references that the proofs themselves carry.

### Issue 3: FDD's "Strictly stronger than Sh4" paragraph
**ASN-0094, FunctionalDependencyDiscipline**: "Sh4 enforces pairwise distinctness of slot-address *pairs*, not of `slot_addrs(F_τ)` alone. Two emissions sharing from-slot `d` but distinct G-slots both pass Sh4 (distinct slot-pairs), yielding `|{τ : from₁(τ) = d}| = 2` — a singleton-returning accessor is ill-defined. FDD forbids the second emission outright."
**Problem**: Motivation prose imagining a case the framework already handles correctly (Sh4 admits it; FDD suppresses it). The corollary Sh4HoldsAtFDDRegisteredK is the load-bearing artifact; this paragraph is the motivation that led to the corollary.
**Required**: Either delete or reduce to one sentence. The structural fact ("FDD's candidate set is broader than Sh4's") suffices.

### Issue 4: SHCD's "Unlike the Sh4/FDD contracts" comparison paragraph
**ASN-0094, single-home commitment**: "Unlike the *Sh4 idempotency contract* and the *FDD functional-dependency contract*, the *single-home commitment* requires no Observe step: the home value `d_K` is a per-K registration constant, so the home check `d = d_K` is a literal-equality test against a fixed value, with no state-dependent computation. Atomicity is trivial (no race window exists between an Observe and the substrate K.λ-step)."
**Problem**: Comparison/justification prose. The single-home commitment's clause (i) — "If `d ≠ d_K`, the call is rejected outright" — is already self-contained.
**Required**: Drop the "Unlike..." paragraph. The contract clauses state what happens; the comparison is meta.

### Issue 5: "Standalone admissibility" defensive note for Resolution
**ASN-0094, Resolution walkthrough**: "*Standalone admissibility.* Resolution's base templates depend only on shape components and Sh0–Sh4; standalone registrations work identically to consumed registrations."
**Problem**: A paragraph imagines a case the framework's universal preservation theorems already exclude — Sh0–Sh4 quantify over every `K ∈ T_cat`, so consumption status is structurally irrelevant. The note defends against a non-issue.
**Required**: Delete.

### Issue 6: Cross-`~`-class concurrency sentence in Sh4 contract
**ASN-0094, Sh4 idempotency contract**: "*Cross-`~`-class concurrency is benign.* Cross-`~`-class retraction does not race with Emit_K because it can only remove existing tuples, not introduce slot-pair collisions."
**Problem**: Single-sentence labeled paragraph commenting on what is *not* a concern. The framework is already restricted to single-process substrates by the prior "Scope" clause.
**Required**: Delete. Single-process scope already disposes of the concurrency question.

### Issue 7: Citation-guidance commentary after Sh4HoldsAtFDDRegisteredK
**ASN-0094, Sh4HoldsAtFDDRegisteredK**: "Downstream consumers citing Sh4 at FDD-registered K should cite this corollary rather than the *Sh4 idempotency contract*. The contract-side observation `C ⊆ C_fd` corroborates the same fact at the gate level (FDD's candidate set is at least as inclusive as Sh4's, so whenever FDD admits the emission Sh4 would too), but the corollary above is the load-bearing artifact."
**Problem**: Meta-commentary about how to cite, not load-bearing for the corollary itself.
**Required**: Delete. The corollary stands on its own.

### Issue 8: "This is the only correctness fact..." meta-sentence in Sh4 contract correctness
**ASN-0094, Sh4 idempotency contract, "Contract correctness" paragraph**: "...by Prefix reflexivity on each pattern address) and (i.b)'s filter. This is the only correctness fact the preservation theorem requires."
**Problem**: The final sentence is meta-commentary on what's needed downstream rather than reasoning about the correctness fact itself.
**Required**: End the paragraph at "and (i.b)'s filter."

### Issue 9: Empty-G semantics interpretive paragraph for BundledDirectedPair
**ASN-0094, BundledDirectedPair**: "*Empty-G semantics under `idem = ⊤`.* The combination `c_G = *` with `idem = ⊤` treats an empty-G emission as an affirmative declaration that the citing document has *zero* dependency targets... Layers that want "no declaration yet" semantics should omit the emission entirely rather than emit empty-G; layers that want "explicitly zero dependencies" use the empty-G form. The framework does not enforce either reading."
**Problem**: Layer-choice interpretation / style guidance about which reading to adopt. The framework's Sh4 set-equality test produces the same outcome regardless of which interpretation the layer holds.
**Required**: Delete. Layer semantics is not the framework's concern.

### Issue 10: Distinction-from-Resolution comparison paragraph
**ASN-0094, Tuple-Classifier walkthrough**: "*Distinction from Resolution.* Resolution `(1, 1, A_doc, A_rel, ⊤)` also targets `A_rel`, but its `c_F = 1` slot requires an actor... Use Resolution when the assertion needs an attributed asserter; use Tuple-Classifier when the assertion is a property of the targeted tuple itself, not an action upon it."
**Problem**: Style-guide content ("Use X when..., use Y when..."). The shape registry's tuple components already encode the distinction.
**Required**: Delete or reduce to a single sentence noting the shape-component difference.

### Issue 11: Duplicate "Note on `pair_K`'s set-equality argument"
**ASN-0094, Retraction and BundledDirectedPair walkthroughs**: The same defensive note — "The body matches by exact set equality on the [F/G]-side so the predicate is not redundant with `from_K(a) ∩ to_K(b) ≠ ∅` (the membership-reading), which is already expressible from the other base templates by intersection." — appears in both walkthroughs.
**Problem**: Two paragraphs in the same document say the same thing in different words; both defend a design choice against a hypothetical redundancy concern.
**Required**: Delete both. If the choice needs documentation, place it once at the catalog level.

### Issue 12: Inline Observe_K semantics re-derivation in Sh4 contract clause (i.a)
**ASN-0094, Sh4 idempotency contract**: Clause (i.a) re-derives Observe_K's semantics inline: "Observe_K's semantics returns the (finite) set of active tuples whose slot coverages prefix-contain the pattern addresses — concretely, `{τ ∈ A_K^Σ : slot_addrs(F) ⊆ coverage(F_τ) ∧ slot_addrs(G) ⊆ coverage(G_τ)}`. Under Sh0/Sh1, every `τ ∈ A_K^Σ` has canonical-form slot endsets, so `coverage(F_τ) = ⋃ {{t : y ≼ t} : y ∈ slot_addrs(F_τ)}` and `slot_addrs(F) ⊆ coverage(F_τ) iff every `x ∈ slot_addrs(F)` has some `y ∈ slot_addrs(F_τ)` with `y ≼ x`."
**Problem**: Observe_K is a foundation Definition (ASN-0086). The inline expansion is essay-style re-derivation that duplicates the foundation. The remark about "iff every `x ∈ slot_addrs(F)` has some `y ∈ slot_addrs(F_τ)` with `y ≼ x`" is not used by the contract correctness argument.
**Required**: Replace with a one-sentence citation: "Observe_K's prefix-coverage semantics (ASN-0086) returns active tuples whose slot coverages contain the pattern addresses."

### Issue 13: Sh-conf Rejection Pattern 1's out-of-scope defensive prose
**ASN-0094, Sh-conf Rejection Patterns, Pattern 1**: "L4 (EndsetGenerality, ASN-0043) admits such endsets at the substrate level; the canonical-slot restriction is a framework-level discipline. The substrate primitive K.λ would still accept a non-canonical endset if invoked outside `Emit_K`, but per the *Emit_K routing commitment* the relational layer routes all class-(iii) emissions of `K ∈ T_cat` through `Emit_K`, so this bypass is not exercised within the framework's scope."
**Problem**: Imagines a case the *Emit_K routing commitment* already excludes ("invoked outside `Emit_K`"). The pattern is about clauses (a)/(b) rejecting; the "what would happen at the substrate" discussion is forward-reference accretion.
**Required**: Reduce the second sentence to: "Non-canonical endsets are admissible at the substrate by L4 (ASN-0043); the canonical-slot restriction is framework-level."

### Issue 14: Consequences section reads as essay content
**ASN-0094, Consequences (a)–(d)**: Four paragraphs of design commentary. (a) recapitulates what the registry provides (already in the catalog). (b) explicitly disclaims a closure theorem the framework doesn't make ("The framework does not establish a closure theorem about these primitives"). (d) ends with "Those are agent-time questions, not substrate questions" — a scope-boundary statement that belongs in Open Questions.
**Problem**: A definition's introduction (here, the framework's conclusion) enumerating downstream consumers and limitations rather than advancing meaning. Two of four entries (b, d) explicitly disclaim what they cover.
**Required**: Either delete the Consequences section or reduce to a single paragraph naming the predicate-language vocabulary. Items (b) and (d)'s scope-boundary content can move to Open Questions.

### Issue 15: Initial-State Baseline duplicates Empty-baseline commitment
**ASN-0094, Initial-State Baseline section**: "Sh0–Sh4 presuppose `L_K^{Σ_init} = ∅` for every `K ∈ T_cat`" — this is the *Empty-baseline commitment* from Scope and Substrate Scaffolding, restated.
**Problem**: Two paragraphs in different sections defer to the same fact. The Initial-State Baseline section's load-bearing content is the Σ_0 symbol convention and the *Per-walkthrough convention* — those are unique. The first sentence of the section duplicates the Scope commitment.
**Required**: Strip the duplicate restatement of the empty-baseline; lead with the Σ_0 / Σ_init symbol convention and the walkthrough-additional condition `dom(Σ_init.L) = ∅`.

### Issue 16: TypedRelationCatalog's "Representative list as layer-supplied configuration parameter" paragraph repeats lifetime-constancy commentary
**ASN-0094, TypedRelationCatalog definition**: The "Representative list" paragraph spends multiple sentences on lifetime constancy ("fixed *before* `Σ_init` is constructed and never modified across the substrate's lifetime"; "Membership tests `K ∈ T_cat` consult the same fixed list at every state, and per-class properties... inherit lifetime constancy from the representative list's"). The ShapeRegistry definition repeats lifetime constancy as a separate property.
**Problem**: Two paragraphs say the same thing in different words: that T_cat / shape are fixed across the substrate's lifetime.
**Required**: State lifetime constancy once. The TypedRelationCatalog paragraph can omit it (or state it once and have ShapeRegistry inherit by reference).

### Issue 17: Per-class registration discipline paragraph
**ASN-0094, Canonical Shape Catalog**: "*Per-class registration discipline.* Per-K discipline registrations (FDD, SHCD, and the *Sh4 idempotency contract*) apply at the `~`-equivalence-class level: registering at any `K ∈ T_cat` applies uniformly to every `K' ∈ T_cat` with `K' ~ K`. Since `L_K^Σ = L_{K'}^Σ` whenever `K ~ K'` (ASN-0086), a pinned-to-one-representative registration would leave coverage-equivalent emissions ungated and break preservation."
**Problem**: The final sentence is "what would break if X" — exactly the pattern of explaining why a design exists rather than what the design is.
**Required**: First sentence is sufficient; delete the "Since..." motivation and the "break preservation" hypothetical.

### Issue 18: Sh4 contract's atomicity scope paragraph
**ASN-0094, Sh4 idempotency contract**: "*Scope: single-process substrate.* The framework is restricted to single-process substrates: `↦`-transitions are sequential, and atomicity of (i)–(iii) reduces operationally to within-call sequencing between `Observe_K` and the substrate K.λ-step, with no intervening `↦`-step from another Sh4-emitter at a `~`-equivalent K."
**Problem**: Justifies why atomicity is achievable in this scope. The framework's Open Questions section already flags multi-process substrate as out of scope.
**Required**: Reduce to one sentence: "Scope: single-process substrate; multi-process semantics is out of scope (see Open Questions)."

### Issue 19: Multi-paragraph proof inside CaseAClosureForLK and CaseAClosureForAK
**ASN-0094, CaseAClosureForLK and CaseAClosureForAK lemmas**: Each lemma's "Proof" section consists of per-sub-class discharges that re-cite ASN-0086 lemmas already used in the per-Sh0–Sh4 preservation proofs. The lemmas are then themselves cited by Sh0–Sh4.
**Problem**: The extraction of CaseAClosureForLK / CaseAClosureForAK as named lemmas is sensible, but the proof prose re-states facts (R3 monotonicity, LinkStoreInvarianceUnderArrangement) that the Sh0–Sh4 preservation arguments would otherwise cite directly. Either the lemma proofs should be terse pointers, or the Sh0–Sh4 Case A bullets should not re-explain the dispatch.
**Required**: Either compress each lemma's proof to a one-paragraph dispatch with citations, or have the Sh0–Sh4 Case A arguments cite the lemma without restating the dispatch. The current arrangement does both.

### Issue 20: NonRSeparation proof attribution
**ASN-0094, NonRSeparation lemma**: The lemma's last sentence — "Each consuming site observes the local shape-tuple difference against R's `(*, 1, A, A_rel, ⊤)` — typically pointing out which components diverge — and cites the lemma rather than re-deriving the contrapositive." — is meta-commentary on how downstream sites use the lemma.
**Problem**: A lemma's body or proof should not describe its consumers.
**Required**: Delete the final sentence.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrates and cross-process registry consistency
**Why out of scope**: The framework is explicitly restricted to single-process substrates; cross-process coordination is acknowledged in Open Questions as a scope boundary.

### Topic 2: Composite shapes (relations whose F or G is constrained by another relation's content)
**Why out of scope**: Open Question, refinement candidate. The current canonical catalog covers atomic shape vocabulary.

### Topic 3: Closure theorem for composite predicates
**Why out of scope**: Consequences (b) explicitly disclaims this. The framework provides primitives; composite construction is layer-level.

META: The ASN is on-topic — it specifies a discipline atop ASN-0086's substrate, with state-relevant invariants (Sh0–Sh4, FDD, SHCD) and operations (Emit_K) that any conforming implementation must satisfy.

VERDICT: REVISE
