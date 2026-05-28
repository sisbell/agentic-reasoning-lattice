# Review of ASN-0095

## REVISE

### Issue 1: PC6 (⊇) direction hand-waves Observe_K pattern reduction

**ASN-0095, PC6 proof, height-0 leaves**: "A bare Observe_K call with a more exotic pattern would need to be expressible as a Boolean combination of these base atoms — and is, since slot-address patterns are exactly the union of from-side and to-side patterns over the catalog's shapes."

**Problem**: The proof claims arbitrary `Observe_K(F̂, Ĝ, view)` patterns — which range over `℘_fin(T) × ℘_fin(T)` per ASN-0086's signature — reduce to Boolean combinations of base atoms `pair_K`, `from_K`, `to_K`, etc., but does not exhibit the reduction. For a concrete pattern like `Observe_K({a, b}, {c, d}, oper)` returning matching tuples, the result is a *set of tuples*, not a Boolean. A "Boolean combination of base atoms" cannot produce a tuple-set value. The catalog atoms `from_K(b)` and `to_K(a)` are each single-address-keyed and set-valued; reconstructing the multi-address pattern would require set intersection (`from_K(b) ∩ from_K(a) ∩ to_K(c) ∩ to_K(d)`), which itself is not formally admitted by PC0–PC2. This is a "by similar reasoning" step in the load-bearing direction of the closure theorem.

**Required**: Either (a) exhibit the reduction as a concrete construction — show that an arbitrary Observe_K pattern decomposes into named PL operators applied to base atoms; or (b) admit a fourth composition primitive (set intersection / comprehension at PL level) and re-prove (⊇); or (c) acknowledge that "substrate-derived patterns" in `Observe_K` are restricted to the union of single-address from/to patterns and re-prove for that restricted class.

### Issue 2: PC2 admits substrate primitives (addr) in chains, but the closure says otherwise

**ASN-0095, Confirmation example**: "`latest_review_was_clean(d) ≡ is_clean(addr(latest_K_for_addr_review(d)))` — with `⊥`-dispatch per the *Partiality propagation rule* (ASN-0094)... The `addr` projection is admitted in the PC2 chain as a substrate primitive — it is itself substrate-evaluable as a trivial-height tree over the leaf forms of Definition — SubstrateEvaluable. (See Open Question on substrate-primitive admission in PC2 chains.)"

**Problem**: PC2's statement quantifies over "value-returning predicates (atomic or composed)". `addr : L^Σ → A_rel^Σ` is a substrate primitive from ASN-0086 (Definition — TupleAddress), not an entry in `V_atom` per the AtomicPredicate definition. The Open Questions section *explicitly flags this as unresolved*. A flagship example in the ASN therefore depends on an unresolved aspect of the algebra. PC6's (⊇) direction also leans on substrate primitives at leaf positions (`addr`, `home`, `slot_addrs`) but PC2 does not formally admit them mid-chain.

**Required**: Resolve the Open Question inside this ASN. Either (a) extend the AtomicPredicate definition to admit pure substrate primitives as degenerate atomic predicates with body equal to the projection (so `addr ∈ V_atom`); or (b) restate PC2 to admit "substrate-evaluable value functions" rather than just "predicates (atomic or composed)"; or (c) add a bridge lemma — PrimitiveAdmission — explicitly stating that the substrate primitives enumerated in Definition — SubstrateEvaluable compose via PC2 like atomic predicates. Whichever choice is made, the Confirmation example must be re-expressible without an unresolved appeal.

### Issue 3: PC1 does not handle empty quantification domains

**ASN-0095, PC1 proof**: "By QD-fin, `[D]_Σ` is finite at every reachable state Σ. The quantifiers reduce to finite Boolean conjunctions and disjunctions: `(∀ x ∈ D :: P(x, s))(Σ) ≡ ⋀_{x ∈ [D]_Σ} P(x, s, Σ)`..."

**Problem**: When `[D]_Σ = ∅`, the right-hand side has no terms. The conventions (empty ∀ = ⊤, empty ∃ = ⊥) need to be stated explicitly — particularly because QD admits filtered domains `{x ∈ D : P(x)}` whose interpretation can be empty even when `D`'s interpretation is non-empty. This boundary case is not gratuitous: predicates like `every_active_citation_resolves(d)` from the third example evaluate vacuously when `S_d = ∅`, and the answer should be well-defined.

**Required**: Add the empty-domain clauses to the PC1 reduction explicitly. State `⋀_∅ = ⊤` and `⋁_∅ = ⊥` as the meta-level conventions feeding the reduction.

### Issue 4: PC2's ⊥-dispatch introduces an if-then-else construct not in PC0–PC2

**ASN-0095, PC2 Remark — partial atoms**: "The standard guarding pattern is `if f(τ) ≠ ⊥ then g(f(τ)) else default-value`, which expresses the partiality at the predicate algebra level. PC2 admits this as a Boolean-conditioned composition — well-defined because the guard is itself a PC0-composed Boolean predicate."

**Problem**: `if-then-else` is not introduced as a composition primitive in PC0, PC1, or PC2. For Boolean codomain it is expressible as `(P ∧ a) ∨ (¬P ∧ b)`, but for arbitrary value codomain `C ∪ {⊥}` it requires dependent dispatch on the test result — not a function-composition step in PC2's sense. The phrase "PC2 admits this as a Boolean-conditioned composition" is asserted, not proved. Without explicit admission, the partial-composition pattern that the Confirmation example relies on sits outside the algebra defined by PC0–PC2.

**Required**: Either (a) add `if-then-else` (or a `case-on-⊥` constructor) as a fourth composition primitive with its own well-definedness and termination clauses; or (b) demonstrate that the guarding pattern reduces to existing PC0–PC2 forms; or (c) lift the partiality into the codomain (sum types) and let PC2 handle it via case-matching constructors.

### Issue 5: Set-theoretic operators at PL level are not formally admitted

**ASN-0095, PC2 Consequence (b)**: "`from_addrs_K(b) ≡ {from₁(τ) : τ ∈ A_K^Σ ∧ to₁(τ) = b}` (DirectedPair base template per ASN-0094) is a value composition that returns a set. PC2 admits this as a composed value, since the right-hand side is a finite set comprehension — a function of Σ and b alone."

**Problem**: PC2's statement is "function composition `g ∘ f`" — strictly unary function composition. Set comprehension `{f(x) : x ∈ D ∧ P(x)}` is a distinct constructor: it consumes a finite domain (a `QD`-expression) and produces a finite set via image-of-filter. Set intersection, union, and image-of-finite-set are similarly absent from PC0–PC2 but appear in atomic template bodies. The claim "PC2 admits this" is asserted but the operator does not appear in PC2's text.

**Required**: Either (a) admit set-theoretic operators (∩, ∪, image, comprehension) as a fourth composition primitive with closure properties; or (b) make clear that set comprehensions are *internal to atomic template bodies* (per Sh5(b)) and not first-class at PL level — in which case `from_addrs_K` is an atomic accessor, not a composed value, and the example wording needs correction.

### Issue 6: PC3 META status conflicts with its mathematical consequences

**ASN-0095, PC3 Justification**: "PC3 is META rather than LEMMA because it asserts a design property of the algebra (that view selection is global to a top-level predicate by convention) rather than a mathematical theorem about the closure."

**ASN-0095, PC3 Consequence (d)**: "the composed expression's purity (PC4) is preserved under either view selection because `L_K^Σ` and `A_K^Σ` are both slices of `Σ.L` (Definition — TypedRelation and Definition — ActiveSubset, ASN-0086)."

**Problem**: Consequence (d) is a substantive mathematical claim about purity preservation under mixed-view evaluation. It is also asserted by PC4 (whose proof explicitly enumerates that Observe-derived consumption goes through `Σ.L` and the active-subset derivation reads `L_R^Σ ⊆ Σ.L`). If PC3 is META, its consequences should be META; if Consequence (d) is a load-bearing mathematical fact, it belongs in PC4's statement or as a separate corollary. The current arrangement mixes design-convention assertions with mathematical content under a single META label.

**Required**: Either (a) demote Consequence (d) to "discussion" and remove its appeal to PC4's purity guarantee; or (b) promote Consequence (d) to a corollary of PC4 with explicit dependency on the view-independence of `Σ.L` slicing; or (c) split PC3 into a META design statement and a LEMMA on view-independence of purity.

### Issue 7: AtomicPredicate examples reference K's whose registration is not exhibited

**ASN-0095, is_claim_quiescent example**: "`all_revise_resolved_via` and `all_observe_resolved_via` are atomic predicates from the Comment instantiation of NonIdempotentDirectedPair... instantiated at types `K_revise` and `K_observe` respectively with corresponding resolver-type arguments `K_res_revise` and `K_res_observe`."

**ASN-0095, every_active_citation_resolves example**: "`S_d = {τ' ∈ A_{K_dep}^Σ : from₁(τ') = d}`... `is_claim(b)` (a Classifier-shape atomic predicate at `K_claim` per the Classifier catalog row)."

**Problem**: The examples invoke `K_revise`, `K_observe`, `K_res_revise`, `K_res_observe`, `K_dep`, `K_claim`, `K_review`, `K_clean` — each requiring registration in `T_cat` with a specific shape and (for some) a specific opt-in discipline. The examples do not list these registrations. Without them, the reader cannot verify that the example expressions actually lie in PL. Specifically, the Confirmation example requires `K_review` registered under SingleHomeCoverageDiscipline (so `latest_K_for_addr_review` is well-formed); the text mentions this but only after assuming the form is well-defined.

**Required**: Add a brief registration prologue to each example listing the K's, their shapes, and required disciplines. The examples are concrete instances of PL membership; their well-formedness should be derivable from the registrations exhibited.

### Issue 8: PC2 proof's appeal to Sh4 is imprecise

**ASN-0095, PC2 proof**: "Composition is total when the inner function is total over its domain (SlotAccessorTotality, ASN-0094, for the base point accessors `from₁`, `to₁` at `c = 1` shapes; Sh4 idempotency for templates whose well-definedness depends on uniqueness of an active match)."

**Problem**: Sh4 (IdempotencyDiscipline) in ASN-0094 enforces uniqueness of slot-pair, not "uniqueness of an active match" generically. The phrase glosses Sh4's actual statement. Templates whose well-definedness depends on uniqueness typically depend on stronger disciplines (FunctionalDependencyDiscipline for point-valued from-keyed accessors; SingleHomeCoverageDiscipline + chain-index argmax for latest-by-chain-position accessors). The reference to Sh4 alone is too weak to license the totality claim for templates like `K_target_of` (which needs FDD, strictly stronger than Sh4 per ASN-0094's FunctionalDependencyDiscipline definition).

**Required**: Refine the reference: name the discipline (Sh4 for point uniqueness at slot-pair; FDD for from-keyed point recovery; SHCD for argmax-by-chain-index point recovery) corresponding to each totality claim, matching ASN-0094's per-K discipline registrations.

### Issue 9: Definition — Signature lists T_cat as an input domain but Codom omits it

**ASN-0095, Definition — Signature**: "Each atomic predicate has a *signature* of the form `P : D₁ × ... × Dₙ → C` with `Dᵢ ∈ {A_doc, A_rel, A, A_K, Endset, T_cat}`... and codomain `C ∈ Codom`."

**ASN-0095, Definition — Codom**: "Codom = { Bool, ℕ, A_doc, A_rel, A, A_K, ℘_fin(A_doc), ℘_fin(A_rel), ℘_fin(A), ℘_fin(A_K) } ∪ { C ∪ {⊥} : C ∈ {A_doc, A_rel, A, A_K} }"

**Problem**: `T_cat` appears as an admissible input domain but not as an admissible codomain. The asymmetry is intentional (atomic templates consume type-indices as parametric arguments; no template returns a type-index) but is not stated. Without acknowledgment, a reader checking Codom against the input-domain set might suspect omission. Additionally, the asymmetry has design consequences — for instance, a hypothetical atom "return the type of the unique active tuple at address `b`" would land in Codom-extension territory and is currently impossible.

**Required**: Acknowledge the input/output asymmetry. State explicitly that `T_cat` is consumed but never returned, and that admitting `T_cat` as a codomain would require new canonical shapes in ASN-0094's catalog.

### Issue 10: Definition — SubstrateEvaluable depends on PL for QD-derived sets

**ASN-0095, Definition — SubstrateEvaluable**: "*internal nodes* are finite Boolean combinators, finite-domain quantifiers (with the domain being a substrate-derivable set, i.e., a member of `QD`)..."

**Problem**: `QD` is defined mutually-inductively with `PL` (via filtered domains `{x ∈ D : P(x)}` with `P ∈ PL`). Definition — SubstrateEvaluable invokes "a member of `QD`" as a primitive notion, but `QD`'s definition in turn references PL-predicates as filters. The mutual induction is well-founded by depth (the ASN says so), but Definition — SubstrateEvaluable should make this circularity explicit: substrate-evaluability and PL membership are jointly defined; one cannot be checked without the other.

**Required**: State the mutual-induction structure explicitly in Definition — SubstrateEvaluable, with depth as the well-founding measure. Either (a) inline a recursive characterization or (b) reference PL's least-fixed-point construction and note that SubstrateEvaluable's "QD-membership" check resolves at the same fixed-point depth.

## OUT_OF_SCOPE

### Topic 1: Recursive / fixed-point predicate definitions (PC7)

**Why out of scope**: The Open Questions section explicitly defers this. Adding a fixed-point operator would extend the algebra, not correct it. Mutually-recursive predicates ("settled = depends-only-on-settled") require explicit well-founding which is a separate design question.

### Topic 2: Aggregation primitives beyond function composition

**Why out of scope**: Aggregation (counts, sums, argmax over non-chain orderings) appears inside atomic template bodies (e.g., `latest_K_for_addr`'s argmax) but is not lifted to PL-level. Whether to lift it is a separate ASN-level decision about the algebra's expressive ceiling — flagged as Open Question.

### Topic 3: Decision procedure for PL membership

**Why out of scope**: The Open Questions section asks whether PL admits an effective decision procedure or a normal form. This is a metatheoretic question about the algebra, not a correctness concern for the algebra's definition.

### Topic 4: Layer Composite substrate-evaluability obligation discharge

**Why out of scope**: The Remark on Layer Composites in PC2 acknowledges that layer-supplied accessors must expand to PL expressions, but the framework-level mechanism for enforcing this (per-accessor inspection, layer-published manifests, typing discipline) is a downstream interface design question.

### Topic 5: Per-K discipline registration manifest as first-class artifact

**Why out of scope**: Whether the layer publishes its discipline registrations as a manifest is an interface design question above the algebra layer.

### Topic 6: Substrate-primitive operator origins (arithmetic, argmax)

**Why out of scope**: Where `+`, `≤`, `argmax` originate — substrate, meta-level, or named scaffolding accessors — is flagged as Open Question. The answer affects PC5's termination accounting but does not falsify the closure structure.

VERDICT: REVISE
