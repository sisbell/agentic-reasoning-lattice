# ASN-0095: Predicate Composition

*Closing the chain — from atomic templates to the substrate's full predicate language.*

ASN-0094 (`shapes.md`) establishes, for each `K ∈ T_cat` with `shape(K) = Σ_canon`, a fixed family of atomic predicate templates supplied by the canonical shape catalog (Sh5, TemplateCatalog). Instantiating those templates produces an *atomic vocabulary* of concrete predicates with stable signatures. This document closes the chain by defining what predicates can be expressed *from* the atomic vocabulary — the algebra of Boolean composition, quantification, and value composition under which the atoms compose into the substrate's full predicate language.

The pipeline in full:

> ASN-0086 (typed relations: Emit_K, Observe_K, Nullify; R0–R6c, R7a) → ASN-0094 (shape framework: Sh-conf, Sh0–Sh4 preservation, Sh5 catalog) → **PC0–PC6** (this ASN, composed predicates) → application predicates

The substantive claim is PC6 (ExpressiveClosure): the substrate's predicate language is *exactly* the closure of the atomic vocabulary under finite Boolean composition, finite quantification, and value composition. No richer; no poorer. Composition extends within an expressive ceiling fixed by the shape catalog; it does not raise the ceiling.

We make this precise, prove the closure properties that justify it, and give the evaluation semantics under which composed predicates yield well-defined values at every substrate state.


## Scope and Dependencies

The framework operates atop the substrate as defined by the following layers:

- *Tumbler algebra* (ASN-0034) — supplies `T2` (IntrinsicComparison) for tuple-address comparison in the Coverage-instantiation's `argmax` (consumed via the *Link sub-allocator chain-index function* scaffolding clause of ASN-0094), and `T10a` (AllocatorDiscipline) for the allocation-discipline lemmas ASN-0094's scaffolding consumes.
- *Strand model / arrangement* (ASN-0036) — referenced transitively through ASN-0094's *Content-store finiteness* scaffolding clause for `dom(Σ.C)` finiteness at every reachable state.
- *Tumbler fields and links* (ASN-0043) — supplies `L-fin` (LinkStoreFiniteness) for `dom(Σ.L)` finiteness, and `L5` (EndsetSetSemantics) for the address-set view this layer's atoms consume.
- *Typed relations* (ASN-0086) — supplies the substrate primitives `Emit_K`, `Observe_K`, `Nullify`; the typed relation `L_K^Σ`; the active subset `A_K^Σ` (Definition — ActiveSubset, computable from `Σ.L` alone by the Definition's own argument); the retraction relation `L_R^Σ` and `nullified(Σ)`; R0 (TupleAddressFreshness) for the concurrent-evaluation discussion; and R6a/R6b/R6c (retraction stability, single-depth retraction, restoration-by-reemission) governing how `A_K^Σ` evolves under retraction.
- *Typed relation shapes* (ASN-0094) — supplies `Sh5` (TemplateCatalog, the canonical catalog of per-shape template families); `Sh-conf` and `Sh0–Sh4` for atomic-predicate signature stability and idempotency; slot accessors (`from_K^Σ`, `to_K^Σ`, point and optional variants under SlotAccessorTotality); the canonical shape catalog by name (Classifier, Tuple-Classifier, DirectedPair, NonIdempotentDirectedPair, Resolution, Retraction, Provenance), together with role-specific instantiations (Coverage and Comment as instantiations of NonIdempotentDirectedPair); per-K opt-in disciplines (FunctionalDependencyDiscipline, SingleHomeCoverageDiscipline); and the substrate-conforming-layer scaffolding clauses by name (notably *Content-store finiteness*, used in QD-fin). The framework consumes ASN-0094's `T_cat` and shape registry, both lifetime-constant per ASN-0094.

*Static-vocabulary commitment.* The atomic vocabulary `V_atom`, the quantification-domain class `QD`, and the predicate language `PL` defined below are all *static* — fixed by `T_cat`, the shape registry, and the layer's per-K discipline registrations, all three lifetime-constant by ASN-0094. No state transition extends these classes; predicate evaluation against state Σ produces values, but the syntactic class of expressible predicates is invariant across Σ.

*Substrate read primitives.* The substrate's state-indexed read primitives entering predicate evaluation are exactly: `Observe_K` (ASN-0086, the only read operation on `Σ.L`); the active-subset derivation (Definition — ActiveSubset, ASN-0086, computing `A_K^Σ` from `L_K^Σ` and `L_R^Σ`); and membership tests against `dom(Σ.L)`, `dom(Σ.C)`, `dom(Σ.M)` (the universes of `A_rel`, `A_doc`, and the document set, respectively). Pure (state-independent) primitives include address projections (`home`, `addr`, `slot_addrs`, `from₁`, `to₁`), tumbler-algebra primitives (`≼`, T1 comparison, T2 intrinsic comparison), and named scaffolding accessors from ASN-0094 (`chain_index`, `emission_order` under SingleHomeCoverageDiscipline). All other substrate operations are *writes* (`Emit_K`, `Nullify`, and the underlying class (i)/(ii)/(iii) substrate primitives of ASN-0086) and lie outside predicate evaluation by construction.

*What substrate-evaluation excludes.* The framework does not admit reads of *content values* `Σ.C(a)` (e.g., the bytes at content address `a`) or *arrangement values* `Σ.M(d)(v)` (e.g., which content address sits at V-position `v` in document `d`). Predicates consume the *structural* substrate — the address universes and the typed-relation slice `Σ.L` — not the opaque value mappings inside `Σ.C` and `Σ.M`. A function that dereferences a content byte or queries which content address inhabits a particular arrangement position is outside the substrate predicate language; such queries are agent-time operations, not substrate predicates.

*Sh5's META status, consumed.* Sh5 (TemplateCatalog) in ASN-0094 is a META commitment about the catalog's construction discipline, not a mechanical-derivation theorem about template families. Concretely: Sh5(a) records that the per-shape template families are hand-curated against shapes.md's canonical catalog, with no procedure mapping arbitrary shapes to templates; Sh5(b) records the literal name-citation discipline restricting catalog rows' template bodies to depend only on shape components, K's name, named scaffolding accessors, and registered per-K disciplines or parametric type-indices. Predicate-composition consumes the *catalog* (the concrete table of base, opt-in, and parametric template families per row) as a fixed input from ASN-0094, not a generator function. The phrasing "for each K, the template family at K" denotes lookup into the catalog row for `shape(K)`, with opt-in templates restricted to K's that register the required discipline and parametric templates carrying their type-index as an additional formal argument.


## The Atomic Vocabulary

**Definition — AtomicPredicate.** An *atomic predicate of type K* is an instantiation `tpl[K]` of some template `tpl` from the canonical-catalog row at `shape(K)` (ASN-0094), at a specific type K, with formal arguments drawn from the slot-typed domains specified by `shape(K)` and the template's signature. The instantiation `tpl[K]` is well-formed iff `tpl` is a *base* template at `shape(K)`, or `tpl` is an *opt-in* template at `shape(K)` and K is registered with the corresponding per-K discipline, or `tpl` is a *parametric* template at `shape(K)` and its type-index argument is treated as a free formal argument of the resulting predicate.

By Sh5 (TemplateCatalog, ASN-0094), the catalog row for `shape(K)` enumerates the base, opt-in, and parametric template families at that shape; Sh5(b)'s discipline restricts each template body to depend only on shape components, K's name, named scaffolding accessors, and registered disciplines or parametric arguments. Each atomic predicate's evaluation reduces to one or more `Observe_K` calls against either `A_K^Σ` (operational view, Definition — ActiveSubset, ASN-0086) or `L_K^Σ` (audit view, Definition — TypedRelation, ASN-0086), combined with finite Boolean and equality operators on the resulting tuple sets and with named scaffolding accessors where the template body requires them (e.g., the Coverage instantiation's `latest_K_for_addr` consumes the *Link sub-allocator chain-index function* scaffolding clause via `emission_order`).

*Notational shorthand.* Write `Tpl(Σ_canon)` for the set of templates at canonical shape `Σ_canon` admitted under the layer's discipline registrations — i.e., the union of (i) all base templates at `Σ_canon`, (ii) opt-in templates at `Σ_canon` for K's with the relevant discipline registered, and (iii) parametric templates at `Σ_canon` with their type-index argument treated as a free formal argument. `Tpl(Σ_canon)[K]` denotes the instantiation of these templates at type K. This notation is a shorthand into ASN-0094's catalog, not an independent function.

**Definition — AtomicVocabulary.** The *atomic vocabulary* is the static set

`V_atom = ⋃_{K ∈ T_cat} { tpl[K] : tpl ∈ Tpl(shape(K)) }`

`V_atom` depends on `T_cat`, the shape registry, and the layer's per-K discipline registrations — all three lifetime-constant by ASN-0094. It does *not* depend on the dynamic state Σ. Each `P ∈ V_atom` is a function whose evaluation `P(args, Σ)` is state-dependent, but the *set* of available atoms is static. Extending the layer's catalog (adding a new K to `T_cat`, or registering a new per-K discipline for an existing K) extends `V_atom` correspondingly; no state transition changes the vocabulary. By Sh5 (TemplateCatalog) together with Sh-conf and Sh0–Sh3 (ASN-0094), every atomic predicate has a stable signature.

**Definition — Codom.** The set of *codomains* used by atomic predicates is the static enumeration

```
Codom = { Bool, ℕ,                                                      -- state-independent
          A_doc, A_rel, A, A_K,                                          -- point address codomains
          ℘_fin(A_doc), ℘_fin(A_rel), ℘_fin(A), ℘_fin(A_K) }            -- finite-set codomains
        ∪ { C ∪ {⊥} : C ∈ {A_doc, A_rel, A, A_K} }                       -- partial variants
```

with state-expansion fixed per ASN-0094's symbol-expansion convention: `A_doc ↦ A_doc^Σ = dom(Σ.C)`, `A_rel ↦ A_rel^Σ = dom(Σ.L)`, `A ↦ A^Σ = A_doc^Σ ∪ A_rel^Σ`, `A_K ↦ A_K^Σ` (the active subset of K, Definition — ActiveSubset, ASN-0086, with K varying per-template), `℘_fin(X) ↦ ℘_fin(X^Σ)`, `Bool ↦ Bool`, `ℕ ↦ ℕ`, and `C ∪ {⊥} ↦ C^Σ ∪ {⊥}` for partial codomains. The partial variants follow the *Codomain convention for partial templates* (ASN-0094) at every catalog row whose template body can fail to produce a value: `from₁⁻`, `to₁⁻` (partial slot accessors for `c = 0|1` shapes), `K_target_of` (DirectedPair under FunctionalDependencyDiscipline), and `latest_K_for_addr` (NonIdempotentDirectedPair under SingleHomeCoverageDiscipline) each land in a `C ∪ {⊥}` codomain.

Concrete catalog correspondence (selected templates per the catalog in ASN-0094):

- `Bool`: `is_K`, `pair_K`, `has_review` and other PC1-existentials, `all_K_resolved_via`.
- `A_doc^Σ ∪ {⊥}`: `K_target_of` (DirectedPair + FDD).
- `A_K^Σ ∪ {⊥}`: `latest_K_for_addr` (NonIdempotentDirectedPair + SHCD, returning a tuple from K's active subset).
- `A_F^Σ ∪ {⊥}`, `A_G^Σ ∪ {⊥}`: `from₁⁻`, `to₁⁻` at `c = 0|1` shapes (Provenance's `to₁⁻`).
- `℘_fin(A_K^Σ)`: tuple-set accessors `from_K`, `to_K`, `outgoing_K`, `unresolved_K_comments_via`.
- `℘_fin(A_doc^Σ)`, `℘_fin(A_rel^Σ)`, `℘_fin(A^Σ)`: address-set accessors `from_addrs_K`, `to_addrs_K` (codomain reads off `t_F`/`t_G` per the Sh5(b) signature-derivation rule).
- `ℕ`: chain-index returns and emission-order projections (`emission_order` under SingleHomeCoverageDiscipline).

**Definition — Signature.** Each atomic predicate has a *signature* of the form

`P : D₁ × ... × Dₙ → C`

with `Dᵢ ∈ {A_doc, A_rel, A, A_K, Endset, T_cat}` (each expanding at state Σ per ASN-0094's symbol-expansion convention) and codomain `C ∈ Codom`. The input domain set includes:

- `A_doc`, `A_rel`, `A` — point-address arguments at the canonical-catalog shapes' `t_F` and `t_G` positions.
- `A_K` — tuple arguments for Tuple-Classifier and the Comment instantiation's `resolved_by` helper.
- `Endset` — for Retraction's `pair_K(F̂, b)` whose F-side argument is an address-set pattern matched by exact set equality (ASN-0094, Retraction catalog row).
- `T_cat` — for parametric templates whose type-index is a free formal argument (e.g., the Comment instantiation's `K_res` argument), and for PC1 quantifications ranging over the type catalog.

The codomain set Codom is closed under the constructions used by ASN-0094's templates (point-valued, set-valued, count-valued, optional-valued). Composition primitives PC0–PC2 (below) do not introduce codomains outside Codom; new codomains require new canonical shapes in ASN-0094's catalog.

**Definition — VocabularyPartition.** Partition `V_atom` by codomain:

`V_bool = {P ∈ V_atom : codom(P) = Bool}` — *Boolean atoms*

`V_val  = V_atom \ V_bool` — *value-returning atoms*

Examples drawn from the canonical catalog (ASN-0094):

- Boolean atoms: `is_K` (Classifier and Tuple-Classifier), `pair_K` (DirectedPair, NonIdempotentDirectedPair, Resolution, Retraction, Provenance — body varies by shape), `all_K_resolved_via` (Comment parametric in `K_res`).
- Value-returning atoms: `from_K`, `to_K`, `from_addrs_K`, `to_addrs_K`, `outgoing_K` (base set-valued and address-set-valued); `K_target_of` (DirectedPair + FunctionalDependencyDiscipline, point-valued with partiality); `latest_K_for_addr` (NonIdempotentDirectedPair + SingleHomeCoverageDiscipline, tuple-valued with partiality); `unresolved_K_comments_via` (Comment parametric, set-valued).

Boolean atoms compose under propositional connectives (PC0); value-returning atoms compose under function application (PC2) and feed into quantification domains (PC1).


## Boolean Composition

**PC0 (BooleanClosure).** Let `P, Q` be predicates with shared signature `S → Bool` (atomic or already composed). Then the following are also predicates with signature `S → Bool`:

`P ∧ Q`, `P ∨ Q`, `¬P`, `P ⇒ Q`, `P ⇔ Q`

*Proof.* Define each operator pointwise: for any `x ∈ S` and any state Σ,

`(P ∧ Q)(x, Σ) ≡ P(x, Σ) ∧_Bool Q(x, Σ)`

and similarly for the others, where `∧_Bool` is meta-level Boolean conjunction. The composed predicate's signature is `S → Bool` by construction. Both arguments are evaluated against the *same* Σ; no auxiliary state is consulted. By induction on the composition tree, well-definedness propagates from the atomic base case (Sh5, TemplateCatalog, ASN-0094) through every layer of composition; signature stability is preserved at each composition step because PC0's pointwise definition does not alter the input domain, and atomic signatures are stable by Sh-conf and Sh0–Sh3 (ASN-0094). ∎

*Remark — algebraic structure.* The set of `S → Bool` functions over a fixed Σ forms a Boolean algebra under pointwise operations. PC0 is the statement that `V_bool(Σ)` and its closure under propositional operators form a sub-Boolean-algebra of the full function space. Identities like `P ∧ ¬P ⇔ ⊥` and `P ∨ ¬P ⇔ ⊤` follow from meta-level Boolean algebra and need no separate axiomatization.

*Consequences.*

(a) *Composite Boolean predicates have stable signatures.* The signature of `P ∧ Q` equals the signature of `P` (and of `Q`, which must match by typing). New signatures do not arise from PC0; only the vocabulary of expressible Bool functions over an existing signature grows.

(b) *Composition is shape-agnostic.* `P` may come from a Classifier-shape relation and `Q` from a DirectedPair-shape relation, provided their signatures unify. PC0 does not inspect K's shape; it operates on each predicate's denotation alone.


## Quantification Domains

Quantification (PC1) requires a finite domain to range over. We separate the *syntactic class* of admissible domain expressions (static, fixed by `T_cat`) from the *interpretation* of each expression at a state (dynamic, finite at every reachable Σ).

**Definition — QuantificationDomain.** The class `QD` of *quantification-domain expressions* is the least class containing the *base domain expressions*

- `A_K`, `L_K` for `K ∈ T_cat`;
- `C_dom` (the content-address space expression);
- `L_dom` (the tuple-address space expression);
- `T_cat` (the type catalog);

and closed under *filtering*: if `D ∈ QD` and `P : D → Bool` is a Boolean predicate from `PL` (defined below), then `{x ∈ D : P(x)} ∈ QD`.

`QD` is mutually inductive with the predicate algebra (PC0–PC2). The mutual induction is well-founded because each expression has finite syntactic depth; the closure is the union over all finite-depth stages, equivalently the least fixed point of the constructor. `QD` depends on `T_cat` and the shape registry alone — it is static across substrate state transitions.

**Definition — DomainInterpretation.** Each `D ∈ QD` denotes, at state Σ, a finite set `[D]_Σ`. The interpretation function is fixed:

- `[A_K]_Σ = A_K^Σ` (Definition — ActiveSubset, ASN-0086)
- `[L_K]_Σ = L_K^Σ` (Definition — TypedRelation, ASN-0086)
- `[C_dom]_Σ = dom(Σ.C)`
- `[L_dom]_Σ = dom(Σ.L)`
- `[T_cat]_Σ = T_cat` (state-independent, lifetime-constant by ASN-0094)
- `[{x ∈ D : P(x)}]_Σ = {x ∈ [D]_Σ : P(x, Σ) = ⊤}`

**QD-fin (DomainFiniteness).** For every `D ∈ QD` and every state Σ, `[D]_Σ` is a finite set.

*Proof.* By induction on the construction of `D`.

*Base cases.*

- `[L_dom]_Σ = dom(Σ.L)` is finite by L-fin (LinkStoreFiniteness, ASN-0043).
- `[L_K]_Σ` is finite as a subset of `dom(Σ.L)`: by Definition — TypedRelation (ASN-0086), `L_K^Σ = {(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a).e₁ = F ∧ Σ.L(a).e₂ = G ∧ coverage(Σ.L(a).e₃) = coverage(K)}`, so the map `(a, F, G) ↦ a` injects `L_K^Σ` into `dom(Σ.L)`.
- `[A_K]_Σ = A_K^Σ ⊆ L_K^Σ` is finite as a subset of `L_K^Σ` (Definition — ActiveSubset, ASN-0086: `A_K^Σ = {(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}`).
- `[C_dom]_Σ = dom(Σ.C)` is finite by the *Content-store finiteness* scaffolding clause (ASN-0094, Scope and Substrate Scaffolding). ASN-0094 surfaces this as a named substrate-conforming-layer commitment; predicate-composition consumes it directly without unpacking the upstream chain through ASN-0036 or ASN-0034.
- `[T_cat]_Σ = T_cat` is finite (up to `~`) by Definition — TypedRelationCatalog (ASN-0094): the catalog is closed and finite at the quotient level `T_cat / ~`, with decidable coverage-equivalence membership. The finite-quotient structure is what the universal quantifier in PC1 ranges over (with each `~`-equivalence class representable by its registered representative).

*Inductive step.* If `[D]_Σ` is finite and `P : D → Bool` is well-defined on D, then `[{x ∈ D : P(x)}]_Σ = {x ∈ [D]_Σ : P(x, Σ)}` is a subset of `[D]_Σ`, hence finite. ∎


## Quantification

**PC1 (QuantificationClosure).** For any `D ∈ QD` and any predicate `P : D → Bool` (atomic or composed), the following are predicates with signature `() → Bool` (closed terms, no free variables):

`(∀ x ∈ D :: P(x))` — *universal*

`(∃ x ∈ D :: P(x))` — *existential*

If `P` has additional free arguments — `P : D × S → Bool` — then quantification yields predicates with signature `S → Bool`:

`(∀ x ∈ D :: P(x, ·)) : S → Bool` with `(∀ x ∈ D :: P(x, ·))(s, Σ) ≡ (∀ x ∈ [D]_Σ :: P(x, s, Σ))`

and dually for `∃`. The quantifier ranges syntactically over the domain expression D; the *interpretation* `[D]_Σ` is consulted at evaluation time to produce a finite enumeration.

*Proof.* By QD-fin, `[D]_Σ` is finite at every reachable state Σ. The quantifiers reduce to finite Boolean conjunctions and disjunctions:

`(∀ x ∈ D :: P(x, s))(Σ) ≡ ⋀_{x ∈ [D]_Σ} P(x, s, Σ)`

`(∃ x ∈ D :: P(x, s))(Σ) ≡ ⋁_{x ∈ [D]_Σ} P(x, s, Σ)`

The right-hand sides are finite Boolean expressions, well-defined by PC0 and the well-definedness of `P` on each `x ∈ [D]_Σ`. ∎

*Justification.* Without quantification, atomic predicates can only test specific tuples by their full content. Quantification lets predicates ask whether *anything* in a domain has property P or whether *everything* in a domain has property P — fundamental for predicates like "every comment of kind K is resolved" or "some review exists for d." The atomic templates of Sh5 already use quantification internally (e.g., `is_K(d) ≡ (E τ ∈ A_K^Σ :: to₁(τ) = d)` at the Classifier catalog row of ASN-0094); PC1 lifts quantification to a composition operator over arbitrary predicates and arbitrary substrate-derived domains.

*Consequences.*

(a) *Predicates over relations become expressible at the algebra level.* Atomic predicates from the Comment instantiation (NonIdempotentDirectedPair parametric, ASN-0094) bind a single tuple. Quantifying over `A_{K_comment}^Σ` and asking "is each comment resolved?" composes the atomic with universal quantification — a predicate that template instantiation alone does not yield.

(b) *Quantifier domains are themselves substrate-derived.* A predicate of the form `(∀ τ ∈ {τ' ∈ A_K^Σ : Q(τ')} :: P(τ))` quantifies over a filtered active subset; the filter Q is itself a Bool predicate. Filtered domains compose freely.

(c) *Cross-type predicates are expressible.* Quantifying over `T_cat` lets a predicate ask "for every type K, does some relation in `L_K` target d?" — a question the atomic vocabulary at any single K cannot ask.

(d) *Parametric templates universalize.* For parametric templates from ASN-0094 (the Comment instantiation's `K_res` argument; analogous parametric type-indices at other shapes), PC1 quantification over `T_cat` produces predicates that universalize the parametric: `(∀ K_res ∈ T_cat :: all_K_resolved_via(K_res, d))` asks "is d resolved by every resolver type?", and `(∃ K_res ∈ T_cat :: unresolved_K_comments_via(K_res, d) ≠ ∅)` asks "does d have any unresolved comments under any resolver type?" These cross-resolver questions are not expressible at any single template instantiation; they require PC1 to bind the parametric argument, with the parametric becoming a quantified variable rather than a layer-fixed type-index.


## Value Composition

**PC2 (ValueComposition).** Let `f : S → C₁` be a value-returning predicate (atomic or composed) and `g : C₁ → C₂` be another predicate (atomic or composed) whose domain matches f's codomain. Then the *function composition*

`(g ∘ f) : S → C₂` with `(g ∘ f)(s, Σ) ≡ g(f(s, Σ), Σ)`

is a predicate. In particular: if `P : C₂ → Bool` and `f : S → C₁` is composable through some `g : C₁ → C₂`, then `P ∘ g ∘ f : S → Bool` is a Boolean composed predicate.

*Proof.* Function composition over typed function spaces is closed when the codomain of the inner function matches the domain of the outer. By Definition of Codom and Definition of Signature, the codomains used by ASN-0094's templates are exactly the domains permitted as predicate inputs (`A_doc`, `A_rel`, `A`, `A_K`, `℘_fin(·)`, etc.). Composition is total when the inner function is total over its domain (SlotAccessorTotality, ASN-0094, for the base point accessors `from₁`, `to₁` at `c = 1` shapes; Sh4 idempotency for templates whose well-definedness depends on uniqueness of an active match). For partial atoms (e.g., `to₁⁻` for `c_G = 0|1` shapes; `K_target_of` under FunctionalDependencyDiscipline; `latest_K_for_addr` under SingleHomeCoverageDiscipline), see Remark below. ∎

*Remark — partial atoms.* For partial-valued templates declared with codomain `C ∪ {⊥}` per the *Codomain convention for partial templates* (ASN-0094), value composition through the partial atom requires explicit `⊥`-handling: `g(f(τ))` is undefined when `f(τ) = ⊥`. The standard guarding pattern is

`if f(τ) ≠ ⊥ then g(f(τ)) else default-value`

which expresses the partiality at the predicate algebra level. PC2 admits this as a Boolean-conditioned composition — well-defined because the guard is itself a PC0-composed Boolean predicate. The *Partiality propagation rule* (ASN-0094, in the NonIdempotentDirectedPair Coverage walkthrough) makes this dispatch obligation uniform across all `... ∪ {⊥}` codomains.

*Remark — Layer Composites.* Layers may introduce their own named accessors (e.g., a layer-supplied `mtime` mapping each `A_doc^Σ` address to a logical timestamp) that look like atomic predicates but are not entries in ASN-0094's canonical catalog. PC2's composition is closed under whatever signature-matching functions a layer provides, but for a composition involving layer accessors to land in PL — i.e., to remain substrate-evaluable per PC6 — each layer accessor must itself expand to a PL expression: a PC0–PC2 composition over `V_atom` and the substrate read primitives enumerated in the Definition — SubstrateEvaluable. Layer Composites (ASN-0094) are *named abbreviations* for PL expressions; their substrate-evaluability is a layer obligation, not a PC2 admission criterion. A layer accessor whose body consults `Σ.C(a)` value mappings or `Σ.M(d)(v)` arrangement values is outside PL by PC6's exclusion clause and cannot participate in substrate predicates — it can be invoked at agent time but not in a quiescence-checkable composition.

*Justification.* Some predicates depend on values pulled from the substrate, not just on tuple existence. `is_K_fresh(d)` consumes `K_target_of(d)` (DirectedPair + FDD per ASN-0094's catalog) and composes with a layer-supplied `mtime` accessor. `latest_K_for_addr(d)` consumes `argmax` over a domain (via the *Link sub-allocator chain-index function* scaffolding clause). Without value composition, predicates could only test pre-canonicalized tuple membership; with PC2, the substrate's structured data flows into the predicate algebra.

*Consequences.*

(a) *Pipelines are expressible.* `is_K_fresh(d) ≡ from_K(d) ≠ ∅ ∧ mtime(K_target_of(d)) ≥ mtime(d)` is a value-composing Boolean predicate, assuming `mtime : A_doc → ℕ` is a layer-supplied accessor whose body expands to a PL expression (typically a derivation via the *Link sub-allocator chain-index function* scaffolding clause, projecting a structural ordering on home-document allocators). DirectedPair + FunctionalDependencyDiscipline supplies `K_target_of` (point-valued with partiality); composition with the layer's `mtime` requires `⊥`-dispatch at K_target_of's partial codomain per the *Partiality propagation rule*. With both ingredients substrate-evaluable, the composition lies in PL.

(b) *Aggregation via finite domains.* `from_addrs_K(b) ≡ {from₁(τ) : τ ∈ A_K^Σ ∧ to₁(τ) = b}` (DirectedPair base template per ASN-0094) is a value composition that returns a set. PC2 admits this as a composed value, since the right-hand side is a finite set comprehension — a function of Σ and b alone.

(c) *Closure under finite codomains only.* PC2 does not introduce new codomains beyond Codom; composition is closed within the codomain set fixed by ASN-0094's templates. New codomains require new templates (i.e., new canonical shapes), not new composition primitives.


## View Parametricity

**PC3 (ViewParametricity — META).** Every composed predicate `P` takes an *implicit view parameter* `view ∈ {active, audit}` that fixes the relation values its atomic queries consult. The same composed predicate body P denotes two distinct predicates `P_active` and `P_audit` according to the view selection:

`P_active(args, Σ) ≡ P(args, Σ)` evaluated with all atomic queries against `A_K^Σ`

`P_audit(args, Σ) ≡ P(args, Σ)` evaluated with all atomic queries against `L_K^Σ`

*Justification.* Atomic predicates in ASN-0094's templates query `A_K^Σ` by default — this is the operational view, "what is currently in effect." But every atomic template can equally be evaluated against `L_K^Σ` to ask audit questions: "did this fact ever exist?" rather than "does this fact exist now?" The view is a parameter of evaluation, not of predicate definition. PC3 is META rather than LEMMA because it asserts a design property of the algebra (that view selection is global to a top-level predicate by convention) rather than a mathematical theorem about the closure.

*Consequences.*

(a) *Operational and historical queries share the predicate algebra.* The same body `is_K(d)` can ask "is d a claim now?" (active view) or "was d ever classified as a claim?" (audit view). The substrate exposes both through one composition framework.

(b) *Mixed-view predicates are admitted but rare.* A predicate could combine an active query with an audit query — "is τ active *and* did some retraction ever target τ?" The composition is permitted by PC0–PC2, but its meaning is application-specific. The standard convention is to fix the view once per top-level predicate and let atomic queries inherit it.

(c) *Default view is the active subset.* When the view is unspecified, A_K is meant. Audit predicates are explicitly marked.

(d) *View affects only Observe_K reads.* The view parameter distinguishes between consulting `A_K^Σ` (operational) and `L_K^Σ` (audit). Scaffolding accessors (`chain_index`, `emission_order`, `home`, `addr`), pure address-level projections (`slot_addrs`, `from₁`, `to₁`, partial variants), and tumbler-algebra primitives (`≼`, T1, T2) are view-independent — they project structural properties of addresses, not state-indexed relation contents. In a mixed-view predicate, only the Observe-derived leaves carry the view distinction; the composed expression's purity (PC4) is preserved under either view selection because `L_K^Σ` and `A_K^Σ` are both slices of `Σ.L` (Definition — TypedRelation and Definition — ActiveSubset, ASN-0086).


## Evaluation Semantics

**PC4 (Purity).** Composed predicates are pure functions of the substrate state and their explicit arguments:

`(A composed predicate P, args ∈ dom(P), Σ, Σ' :: P depends on Σ only through (dom(Σ.C), dom(Σ.M), Σ.L); when those agree on Σ and Σ', P(args, Σ) = P(args, Σ'))`

Equivalently, predicate evaluation has no side effects on the substrate, no memoized state across cycles, and no dependency on the order or history of past emissions or on the value mappings inside `Σ.C` or `Σ.M`.

*Proof.* By induction on the syntactic structure of the composition.

*Base case — atomic predicates.* Each atom in `V_atom` consumes some combination of (i) `Observe_K` queries against `Σ.L` (returning `L_K^Σ` or `A_K^Σ`, depending on view), (ii) named scaffolding accessors from ASN-0094 (`chain_index`, `emission_order` under SingleHomeCoverageDiscipline, `home`, `addr`), (iii) pure address-level projections (`slot_addrs`, `from₁`, `to₁`, partial variants), and (iv) tumbler-algebra primitives from ASN-0034 (`≼`, T1 comparison, T2 intrinsic comparison). We verify each consumes only the structural substrate `(dom(Σ.C), dom(Σ.M), Σ.L)`:

- *(i) Observe_K* reads `Σ.L` directly. For the operational view, the active-subset derivation also reads `L_R^Σ ⊆ Σ.L` to compute `nullified(Σ)`. The Definition — ActiveSubset (ASN-0086) makes `A_K^Σ` computable from `Σ.L` alone: `L_K^Σ` is a slice of `Σ.L`, `nullified(Σ)` is fixed by `L_R^Σ`, itself a slice of `Σ.L`. So Observe_K consumes only `Σ.L`.
- *(ii) Scaffolding accessors* are pure functions of their address inputs and their reference document (for `chain_index`, `emission_order`). They do not consult `Σ.C(a)` or `Σ.M(d)(v)` value mappings; they read only structural projections of the input addresses.
- *(iii) Pure address-level projections* are state-independent functions of the address argument.
- *(iv) Tumbler-algebra primitives* are state-independent functions of their arguments.

Atomic evaluation therefore depends on Σ only through `(dom(Σ.C), dom(Σ.M), Σ.L)` — specifically, through `Σ.L` for the Observe-derived parts and through `dom(Σ.C)`, `dom(Σ.M)` only as universes from which input arguments are drawn. Two states Σ, Σ' that agree on these components produce identical atomic predicate values for any well-typed args.

*Inductive step.* PC0 yields composed predicates whose denotation is a meta-level Boolean operator on its constituents — closed under pointwise application, preserving purity. PC1 yields finite quantifications which reduce to finite Boolean expressions over a quantification domain (itself a function of Σ through `(dom(Σ.C), dom(Σ.M), Σ.L)` by the DomainInterpretation function and QD-fin); each iteration is a pure constituent evaluation. PC2 yields function compositions over typed function spaces; each function in the chain is pure by inductive hypothesis, and finite composition of pure functions is pure. ∎

*Consequence — predicate evaluation is reproducible.* Recording `(dom(Σ.C), dom(Σ.M), Σ.L)` at any state Σ together with a predicate P fixes P(args, Σ) for every well-typed args. Σ.C's content-value mapping and Σ.M's arrangement-value mapping do not need to be recorded — they are not consulted by any predicate in PL.

**PC5 (TerminationOnFiniteSubstrate).** For any composed predicate P, any state Σ with finite `dom(Σ.L)` (which holds at every reachable state by L-fin, ASN-0043), and any well-typed args, evaluation of `P(args, Σ)` terminates in finite time.

*Proof.* By induction on composition structure.

*Base case — atomic predicates.* Each atomic evaluation decomposes into (i) at most one `Observe_K` call, returning a subset of `L_K^Σ` of cardinality `≤ |dom(Σ.L)|`, finite by L-fin; (ii) a finite number of pure scaffolding-accessor invocations (each constant-time on its argument); (iii) a finite number of pure address-level projections (each constant-time); and (iv) a finite number of tumbler-algebra primitive invocations (each constant-time, since tumbler lengths are finite by T0, ASN-0034). The atomic predicate's body composes these via finite Boolean operators and equality tests over the returned tuple set, all of which terminate in finitely many steps.

For atoms involving `argmax` (the Coverage instantiation's `latest_K_for_addr` under SingleHomeCoverageDiscipline), the maximization ranges over a finite set `S_d = {τ ∈ A_K^Σ : to₁(τ) = d}`, finite by L-fin, with the comparison delegated to `emission_order` (a `chain_index` invocation per τ, constant-time per invocation per the scaffolding clause). Finite domain, constant-time comparisons, total order on the comparison values (T1 on chain indices, ASN-0034) — `argmax` terminates.

*Inductive step.* PC0 reduces to constant-time meta-Boolean operators on already-evaluated constituents. PC1 reduces to finite ⋀ and ⋁ over finite domains (QD-fin); each iteration is a constituent evaluation, which terminates by inductive hypothesis. PC2 is finite function composition: each function in the chain terminates by inductive hypothesis, and the chain itself has bounded depth fixed by the predicate's syntax. The full composition tree is finite by the syntactic finiteness of the predicate term. ∎

*Consequences of PC4 + PC5.*

(a) *No memoization across cycles.* Every predicate evaluation reads the current substrate from scratch. The runner's quiescence check fires-then-evaluates; it does not consult prior evaluation results. Stale predicate values cannot poison the system because none are retained.

(b) *Concurrent evaluation is safe by construction.* Two agents evaluating the same predicate against the same Σ produce the same answer; no synchronization is required for correctness of evaluation. Coordination during emit is a separate concern, addressed by R0 (TupleAddressFreshness, ASN-0086).

(c) *Predicates are decidable on any reachable substrate.* PC5 makes every composed predicate's truth value a computable function. The substrate's reachable-state finiteness ensures decidability is automatic.


## Expressive Closure

**Definition — SubstrateEvaluable.** A function `F : args × State → C` is *substrate-evaluable* iff its evaluation can be specified as a finite tree whose:

- *leaves* are state-indexed read primitives — `Observe_K` queries against `Σ.L` (in either view), membership tests against `dom(Σ.C)`, `dom(Σ.M)`, `dom(Σ.L)`, named scaffolding accessors of ASN-0094 (`chain_index`, `emission_order`), pure address-level projections (`home`, `addr`, `slot_addrs`, `from₁`, `to₁`, partial variants), and tumbler-algebra primitives (`≼`, T1, T2) — together with state-independent constants and the predicate's argument bindings;
- *internal nodes* are finite Boolean combinators, finite-domain quantifiers (with the domain being a substrate-derivable set, i.e., a member of `QD`), or function compositions over typed codomains.

By construction, substrate-evaluable functions do *not* consult `Σ.C(a)` (the byte mapping at content address `a`) or `Σ.M(d)(v)` (the arrangement value at V-position `v` of document `d`). They consume the *structural* substrate alone.

**PC6 (ExpressiveClosure).** The substrate-evaluable functions, under the layer's current discipline registrations, are exactly the predicate language `PL` — the least closure of `V_atom` under PC0 (Boolean composition), PC1 (quantification), and PC2 (value composition).

Formally:

`(A function F : args × State → C : F is substrate-evaluable :: F ∈ PL)`

`PL` is static — fixed by `T_cat`, the shape registry, and the layer's per-K discipline registrations, like `V_atom` and `QD`. Each `P ∈ PL` denotes, at state Σ and arguments args, a value `P(args, Σ)` in its codomain.

*Proof.* Two directions.

*(⊆) Every PL expression is substrate-evaluable.* By induction on the syntactic structure of the expression.

- *Base.* Every `tpl[K] ∈ V_atom` is substrate-evaluable: its body consumes only the read primitives enumerated in the Definition above (concretely, one or more Observe_K queries plus the scaffolding accessors, pure projections, and tumbler-algebra primitives the catalog row's template body invokes — by Sh5(b) restricted to (i)–(iv) per the catalog discipline). Its evaluation tree is finite by the catalog body's finite syntactic depth.
- *Inductive step.* PC0, PC1, PC2 each produce a finite tree whose root is a Boolean combinator, finite-domain quantifier, or function composition — exactly the internal-node forms admitted in the Definition above. By inductive hypothesis the constituent subtrees are substrate-evaluable; the composed tree is therefore substrate-evaluable.

*(⊇) Every substrate-evaluable function lies in PL.* Let F be substrate-evaluable. Its evaluation tree has finite depth; we induct on tree height.

- *Height 0 — leaves.* A leaf is one of the read primitives or a state-independent constant. We show each leaf form is expressible in `V_atom` or as a trivial composition over `V_atom`.

  - An `Observe_K(Σ, F̂, Ĝ, view)` call with a substrate-derived pattern `(F̂, Ĝ)` returns a finite subset of `L_K^Σ` (audit) or `A_K^Σ` (operational). For each canonical-catalog shape in ASN-0094, the base template family at that shape exposes the substrate-derivable Observe queries against that shape's `(t_F, t_G)` slot structure: `pair_K`, `from_K`, `to_K`, `from_addrs_K`, `to_addrs_K` (DirectedPair, NonIdempotentDirectedPair, Resolution, Retraction, Provenance) cover the slot-pair, from-slot, to-slot, and address-projection Observe forms; `is_K` (Classifier, Tuple-Classifier) covers the to-slot existential at `c_F = 0` shapes; `outgoing_K` (Provenance) covers the from-slot accessor at `c_G = 0|1` shapes. Together these enumerate every Observe pattern derivable from slot-address arguments at every catalog shape. A bare `Observe_K` call with a more exotic pattern would need to be expressible as a Boolean combination of these base atoms — and is, since slot-address patterns are exactly the union of from-side and to-side patterns over the catalog's shapes.

  - A membership test `a ∈ dom(Σ.C)` (equivalently, `a ∈ A_doc^Σ`) is realized as a precondition on input arguments and as the implicit domain for inputs typed `A_doc`. Similarly for `a ∈ dom(Σ.L) = A_rel^Σ` and document-set membership. These appear in PL through Signature: every predicate's input domain is one of `{A_doc, A_rel, A, A_K, Endset, T_cat}`, each of which interprets at Σ as a finite subset of `T`. Membership tests against these domains do not require dedicated atoms; they are subsumed by the Signature's domain typing.

  - Named scaffolding accessors (`chain_index(ℓ, d)`, `emission_order(τ)`, `home(a)`, `addr(τ)`) appear in catalog template bodies under the Sh5(b) discipline. `emission_order` specifically appears inside `latest_K_for_addr` (NonIdempotentDirectedPair + SHCD); `home` and `addr` appear in multiple catalog rows as base-machinery accessors. Their use is bundled into the atoms that invoke them; they do not stand alone as predicates.

  - Pure address-level projections (`slot_addrs`, `from₁`, `to₁`, `from₁⁻`, `to₁⁻`) appear inside catalog template bodies and as slot-accessor exports per ASN-0094's SlotAccessorTotality lemma. They are bundled into the atoms that invoke them.

  - Tumbler-algebra primitives (`≼`, T1, T2) appear inside catalog template bodies (notably T2 in the Coverage instantiation's `argmax`) and as comparison operators between addresses. They are bundled into the atoms that invoke them.

  Every leaf form therefore corresponds to (or is bundled into) an atom in `V_atom` admissible at the layer's discipline registrations.

- *Height n+1 — internal nodes.* An internal node is a Boolean combinator, finite-domain quantifier, or function composition. By inductive hypothesis the subtrees are in PL. PC0, PC1, PC2 admit Boolean combination, finite-domain quantification (over substrate-derivable `D ∈ QD`), and function composition respectively. The composed tree is therefore in PL.

By induction on tree height, F ∈ PL. ∎

*Consequences.*

(a) *Capability is bounded by the shape catalog plus the layer's discipline registrations.* Adding a new canonical shape to ASN-0094's catalog (with its own template family) is the only way to raise the catalog's expressive ceiling. Adding a new K with an existing shape generates atoms within the existing ceiling; adding a new shape adds new atomic forms, hence new closures. Registering a new per-K discipline at an existing shape (e.g., FDD at a previously-FDD-unregistered DirectedPair K) extends the opt-in template families admissible at the registering K's; this likewise extends `V_atom` and PL without raising the catalog's expressive ceiling.

(b) *Quality questions are non-substrate.* "Is this proof correct?", "is this description coherent?", "are these two claims really equivalent?" — none of these has a finite Observe-tree decomposition. They are agent-time questions; the substrate cannot ask or answer them.

(c) *Quiescence is itself a substrate predicate.* The convergence condition — "every public predicate of every agent evaluates true against `A_K^Σ`" — is a finite ∀ over a finite agent set composed with each agent's public predicate. By PC0 + PC1, this is in `PL`. By PC4 it is pure; by PC5 it is decidable. The system's terminal condition is recognizable by the substrate itself — a property crucial for the runner's quiescence check.

(d) *Content-value and arrangement-value queries are out of scope.* A function like `Σ.C(a) = "claim"` (testing the byte content at address `a`) or `Σ.M(d)(v) = a'` (testing which content sits at V-position `v` in document `d`) is *not* in PL, and PC6 makes no claim about such functions. They are agent-time operations — the agent can read Σ.C and Σ.M values during its own decision process — but the substrate predicate language closes only over the structural substrate, not the value mappings.


## Examples

We illustrate composition with three concrete predicates, decomposed into their atomic and compositional structure.

### Quiescence of a claim

`is_claim_quiescent(d) ≡ all_revise_resolved_via(K_res_revise, d) ∧ all_observe_resolved_via(K_res_observe, d)`

- `all_revise_resolved_via` and `all_observe_resolved_via` are atomic predicates from the Comment instantiation of NonIdempotentDirectedPair (Sh5 walkthrough, ASN-0094), instantiated at types `K_revise` and `K_observe` respectively with corresponding resolver-type arguments `K_res_revise` and `K_res_observe`. Each takes a single `A_doc` argument plus its parametric `K_res ∈ T_cat`.
- The composition is a Boolean conjunction (PC0) with shared signature `A_doc → Bool` (with the `K_res` arguments fixed to the layer's canonical resolver registrations).
- View parameterization (PC3): both atomic queries default to `A_K^Σ` and consult the corresponding active resolution relation; the audit-view variant `is_claim_quiescent_audit(d)` would ask "was d ever quiescent?" — meaningful but rare.

### Confirmation of a claim

`is_claim_confirmed(d) ≡ is_claim_quiescent(d) ∧ has_review(d) ∧ latest_review_was_clean(d)`

- `is_claim_quiescent(d)` — defined above; a PC0-composed Boolean.
- `has_review(d)` — composed via PC1 from a Boolean atom on the Coverage instantiation:

  `has_review(d) ≡ (∃ τ ∈ A_{K_review}^Σ :: to₁(τ) = d)`

  An existential quantification (PC1) over the active subset of the review-coverage relation (Coverage instantiation of NonIdempotentDirectedPair, ASN-0094), whose body is an equality test on the slot accessor `to₁`.

- `latest_review_was_clean(d)` — uses the Coverage instantiation's `latest_K_for_addr` (an opt-in template under SingleHomeCoverageDiscipline per ASN-0094) to retrieve the latest review tuple, extracts the tuple's tumbler address via the `addr` substrate primitive (the R1 export from ASN-0086, a pure projection from `A_K^Σ` to `A_rel^Σ` listed in Definition — SubstrateEvaluable as a pure address-level projection), passes the resulting address through a Tuple-Classifier atom `is_clean : A_rel → Bool` (Tuple-Classifier shape `(0, 1, -, A_rel, ⊤)` per ASN-0094), and composes via PC2:

  `latest_review_was_clean(d) ≡ is_clean(addr(latest_K_for_addr_review(d)))` — with `⊥`-dispatch per the *Partiality propagation rule* (ASN-0094) when no review tuple exists for `d`.

  The decomposition is `(is_clean ∘ addr ∘ latest_K_for_addr_review)(d)` with explicit `⊥`-handling at the partial codomain. The atomic `is_clean(τ)` is the Tuple-Classifier base template `is_K(τ) ≡ (E σ ∈ A_K^Σ :: to₁(σ) = τ)` at `K = is_clean`. The composition requires (i) `K_review` registered under SingleHomeCoverageDiscipline (so `latest_K_for_addr_review` is well-formed with codomain `A_K_review^Σ ∪ {⊥}`) and (ii) `K_clean` registered as a Tuple-Classifier (so `is_clean : A_rel^Σ → Bool` is in `V_atom`). The `addr` projection is admitted in the PC2 chain as a substrate primitive — it is itself substrate-evaluable as a trivial-height tree over the leaf forms of Definition — SubstrateEvaluable. (See Open Question on substrate-primitive admission in PC2 chains.)

The full composition has signature `A_doc → Bool`; it combines Comment-instantiation parametric atoms, a Coverage-instantiation existential (via PC1), a Tuple-Classifier atom composed through an opt-in Coverage atom (PC2 with `⊥`-dispatch), and Boolean conjunction (PC0). Every step lies in PC0–PC2; no construction outside the closure is needed.

### Frame-condition style universality

`every_active_citation_resolves(d) ≡ (∀ τ ∈ S_d :: (∃ b ∈ dom(Σ.C) :: to₁(τ) = b ∧ is_claim(b)))`

where `S_d = {τ' ∈ A_{K_dep}^Σ : from₁(τ') = d}` is a filtered quantification domain.

- `S_d` is built by filtering `A_{K_dep}` (a base domain expression, interpreted at Σ as `A_{K_dep}^Σ`) by a Boolean predicate on `from₁` (DirectedPair base accessor at `K_dep` registered as DirectedPair per the catalog row). By the inductive QD construction, `S_d ∈ QD`.
- The outer ∀ (PC1) ranges over `S_d`; the body is an existential over `dom(Σ.C)` testing the conjunction (PC0) of `to₁(τ) = b` (a Boolean atom on slot equality) and `is_claim(b)` (a Classifier-shape atomic predicate at `K_claim` per the Classifier catalog row).
- The quantification `(∃ b ∈ dom(Σ.C) :: ...)` enumerates the content-address universe — `dom(Σ.C) = A_doc^Σ`, a base domain expression in QD by inclusion. Per PC6's Definition — SubstrateEvaluable, this is a *structural enumeration* of allocated content addresses, not a value read into Σ.C: no byte mapping at `b` is dereferenced, only `b`'s membership in `dom(Σ.C)` and its participation in `to₁(τ) = b` and `is_claim(b)`. The predicate stays in PL because no `Σ.C(a)` or `Σ.M(d)(v)` value mapping is consulted.
- The composition is fully within PC0–PC2; the predicate states "every outgoing dependency of d resolves to an active claim."


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| AtomicPredicate | DEF | `tpl[K]` — instantiation of a template from ASN-0094's canonical catalog at a specific type K, with base/opt-in/parametric admissibility per K's discipline registrations | introduced |
| V_atom | DEF | Atomic vocabulary `⋃_K Tpl(shape(K))[K]` — *static*, fixed by `T_cat`, shape registry, and per-K discipline registrations (all three lifetime-constant by ASN-0094) | introduced |
| V_bool, V_val | DEF | Partition of `V_atom` by codomain (Bool vs value-returning) | introduced |
| Codom | DEF | Set of admissible codomains: `{Bool, ℕ, A_doc, A_rel, A, A_K, ℘_fin(A_doc), ℘_fin(A_rel), ℘_fin(A), ℘_fin(A_K)} ∪ {C ∪ {⊥} : C point or tuple}` — matched to ASN-0094's catalog template codomains per the *Codomain convention for partial templates* | introduced |
| Signature | DEF | Predicate signature `D₁ × ... × Dₙ → C` with `Dᵢ ∈ {A_doc, A_rel, A, A_K, Endset, T_cat}` and `C ∈ Codom` | introduced |
| QD | DEF | Static class of quantification-domain expressions; least class containing base domains `A_K, L_K, C_dom, L_dom, T_cat` and closed under filtering by `PL`-predicates | introduced |
| `[D]_Σ` | DEF | Interpretation of domain expression D at state Σ — finite by QD-fin | introduced |
| QD-fin | LEMMA | DomainFiniteness — every domain interpretation is finite (= L-fin from ASN-0043 + *Content-store finiteness* scaffolding from ASN-0094 + `T_cat / ~` finite at registry per ASN-0094) | introduced |
| PL | DEF | Predicate language — least closure of `V_atom` under PC0–PC2; *static* (same parameters as V_atom) | introduced |
| SubstrateEvaluable | DEF | Functions whose evaluation decomposes into a finite tree of substrate read primitives + finite combinators; explicitly excludes `Σ.C(a)` and `Σ.M(d)(v)` value reads | introduced |
| PC0 | LEMMA | BooleanClosure — `V_bool` closed under ∧, ∨, ¬, ⇒, ⇔ | introduced |
| PC1 | LEMMA | QuantificationClosure — finite ∀ and ∃ over `D ∈ QD` interpreted at Σ | introduced |
| PC2 | LEMMA | ValueComposition — function composition over typed codomains; partial-codomain compositions require `⊥`-dispatch per ASN-0094's *Partiality propagation rule* | introduced |
| PC3 | META | ViewParametricity — `A_K` vs `L_K` is an evaluation parameter, global to a top-level predicate by convention | introduced |
| PC4 | LEMMA | Purity — composed predicates are pure functions of `(dom(Σ.C), dom(Σ.M), Σ.L)` and explicit arguments; do not consume `Σ.C` value mappings or `Σ.M(d)(v)` arrangement values; base case discharges by enumerating atomic-template consumption against ASN-0086/ASN-0094 read primitives | introduced |
| PC5 | LEMMA | TerminationOnFiniteSubstrate — evaluation halts in finite time; base case includes scaffolding accessors and tumbler-algebra primitives as constant-time, and `argmax` over finite domains for Coverage's `latest_K_for_addr` | introduced |
| PC6 | THM | ExpressiveClosure — substrate-evaluable predicates = `PL`, parametrized by the layer's discipline registrations; proof enumerates ASN-0094 catalog rows for each substrate read-primitive form | introduced |


## Open Questions

- Is *recursion* over predicates expressible? `is_claim_confirmed` references `is_claim_quiescent`, which is a definitional macro-expansion (substitution at parse time). Mutually-recursive predicate definitions ("a tuple is settled iff every tuple it depends on is settled") would not terminate under PC5 without an explicit fixed-point operator. Should the substrate admit a least-fixed-point operator (PC7?), or rule recursion out by construction and require recursion to be unrolled at agent time?

- *Aggregation* (counts, sums, max/min over numeric value codomains) appears in templates like `latest_K_for_addr` (via `argmax` over `emission_order`). Is aggregation a fourth composition primitive distinct from PC2, or is it sufficiently captured by value composition over substrate-derived numeric atoms? In particular: where do the arithmetic operators (`+`, `≤`, `argmax`) come from — are they substrate primitives, meta-level, or named scaffolding accessors per ASN-0094?

- The mutual induction defining `QD` and `PL` produces a least fixed point. Are there derivable domains the language *cannot* express — domains expressible at a meta level but not constructible by base + filter? In particular, can the language express domains defined by ∃-introduced existential witnesses (e.g., "the set of x such that some y witnesses P(x, y)"), or must such domains be flattened into PC1's quantifier prefix?

- PC3 makes the view a global parameter per top-level predicate by convention. Mixed-view predicates are admitted by the algebra; PC3 Consequence (d) clarifies that view affects only Observe leaves, with scaffolding accessors, pure projections, and tumbler primitives being view-independent. Should a composition primitive promote the view to a first-class parameter (e.g., `P[view]`), allowing fine-grained mixing at the Observe-leaf level? The purity invariant is automatic — both `L_K^Σ` and `A_K^Σ` are slices of `Σ.L` — but the *semantics* of mixed-view predicates ("is τ active *and* did some retraction ever target τ?") remains application-specific and lacks a uniform interpretation.

- The closure theorem (PC6) asserts the predicate language equals a specific algebraic closure. Is there an effective decision procedure that, given an arbitrary syntactic expression, decides whether it lies in `PL`? Well-typing is decidable (it reduces to signature unification and ASN-0094 catalog-row lookup); whether `PL` *restricted to extensionally non-equivalent predicates* admits a normal form is open.

- *Side-effecting evaluation* — predicates that emit substrate facts as a byproduct of evaluation — would violate PC4 (Purity). The architecture rules this out at the predicate algebra level, but agents that observe-then-emit during their own decision process produce a similar effect at a different layer. Where is the boundary between predicate evaluation (pure) and agent computation (which may emit), and what invariants does that boundary preserve?

- Per-K discipline registrations are lifetime-constant by ASN-0094, but the layer chooses *which* disciplines to register at startup. Phase 1's AtomicPredicate definition makes the precondition self-evident from template references (opt-in templates name their required discipline at the catalog row). The remaining question: should the layer publish a *registration manifest* — a tabular enumeration of which K's carry which disciplines and which parametric type-indices are bound — surfaced as a first-class artifact so V_atom's content is determinable at a glance? Currently V_atom is implicitly fixed by the manifest; making it explicit could simplify auditing, cross-layer composition, and the framework-level identification of which atoms are admissible at a layer.

- PC6's proof argues every substrate-evaluable function decomposes into atoms-plus-composition by enumerating ASN-0094's catalog rows. The enumeration is implicit in the catalog table; making it *explicit* (a tabular correspondence between substrate read-primitive forms and catalog rows) would make PC6's proof mechanically falsifiable in the same sense Sh5(b) is. Should this correspondence be a separate property — PC6-Cor (CatalogCorrespondence) — surfaced as a check the catalog must satisfy at every extension?

- *Substrate-primitive admission in PC2 chains.* PC2's statement quantifies over "predicates (atomic or composed)", but compositions involving pure scaffolding primitives — `addr`, `home`, `slot_addrs`, partial slot accessors, tumbler-algebra comparisons — admit those primitives as value functions even though they are not entries in V_atom (the Confirmation example's `addr` extraction illustrates the case). PC6's Definition — SubstrateEvaluable lists these primitives as legitimate leaf forms, but PC2's text does not formally admit them. Three resolutions: (a) extend V_atom to include the pure primitives as degenerate atomic predicates (signature-typed, body equal to the projection); (b) restate PC2 to admit "substrate-evaluable value functions" rather than just predicates; (c) add a small bridge lemma — PrimitiveAdmission — stating that any substrate primitive in Definition — SubstrateEvaluable composes via PC2 just like an atomic predicate. The choice affects how clean PC2 chains read when they need to type-adapt between A_K^Σ and A_rel^Σ (or between Endset and ℘_fin(A) via `slot_addrs`, etc.).

- Layer Composites (Remark to PC2) are layer-supplied named accessors that expand to PL expressions; their substrate-evaluability is a layer obligation. How should this obligation be discharged at framework level — per-accessor inspection by the layer's author, a layer-published manifest of accessor expansions, or a typing discipline that distinguishes PL-expanding accessors from agent-time accessors at their declarations? The choice matters when layers compose: a downstream layer cannot tell whether an imported accessor is substrate-evaluable without inspecting its body, unless the obligation is published.