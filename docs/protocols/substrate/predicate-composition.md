# Predicate Composition

*Closing the chain — from atomic templates to the substrate's full predicate language.*

`shapes.md` shows that each `K ∈ T_cat` with `shape(K) = Σ_canon` generates a fixed family of atomic predicate templates `Tpl(Σ_canon)` (Sh5, TemplateGeneration). Instantiating those templates produces an *atomic vocabulary* of concrete predicates with stable signatures. This document closes the chain by defining what predicates can be expressed *from* the atomic vocabulary — the algebra of Boolean composition, quantification, and value composition under which the atoms compose into the substrate's full predicate language.

The pipeline in full:

> R0–R7 (typed relations + operations) → Sh0–Sh5 (shape restrictions, slot accessors, templates) → **PC0–PC6** (composed predicates) → application predicates

The substantive claim is PC6 (ExpressiveClosure): the substrate's predicate language is *exactly* the closure of the atomic vocabulary under finite Boolean composition, finite quantification, and value composition. No richer; no poorer. Composition extends within an expressive ceiling fixed by the shape catalog; it does not raise the ceiling.

We make this precise, prove the closure properties that justify it, and give the evaluation semantics under which composed predicates yield well-defined values at every substrate state.


## The Atomic Vocabulary

**Definition — AtomicPredicate.** An *atomic predicate of type K* is an instantiation `tpl[K]` of some template `tpl ∈ Tpl(shape(K))` at a specific type K, with formal arguments drawn from the slot-typed domains of `shape(K)`.

By Sh5 (TemplateGeneration, `shapes.md`), the template body of `tpl[K]` is mechanically determined by `shape(K)` and K's name. Each atomic predicate's evaluation reduces to one or more `Observe_K` calls against either `A_K^Σ` (operational view, R6) or `L_K^Σ` (audit view, definition in `typed-relations.md`), combined with finite Boolean and equality operators on the resulting tuple sets.

**Definition — AtomicVocabulary.** The *atomic vocabulary* is the static set

`V_atom = ⋃_{K ∈ T_cat} { tpl[K] : tpl ∈ Tpl(shape(K)) }`

`V_atom` depends on `T_cat` and the shape registry — both fixed by the substrate's specification. It does *not* depend on the dynamic state Σ. Each `P ∈ V_atom` is a function whose evaluation `P(args, Σ)` is state-dependent, but the *set* of available atoms is static. Adding a new K to `T_cat` extends `V_atom` by exactly the predicates `Tpl(shape(K))` instantiates; no state transition changes the vocabulary. By Sh5, each set in the union is fixed by `shape(K)`; by Sh-conf and Sh0–Sh3 (`shapes.md`), every atomic predicate has a stable signature.

**Definition — Signature.** Each atomic predicate has a *signature* of the form

`P : D₁ × ... × Dₙ → C`

with `Dᵢ ∈ {A_doc, A_rel, T_cat}` (or substrate-derivable subsets thereof) and codomain `C` drawn from

`Codom = {Bool, A_doc, A_rel, ℘_fin(A_doc), ℘_fin(A_rel), ℘_fin(A_rel × ℘_fin(A) × ℘_fin(A)), ℕ, ⊥}`

The codomain set is closed under the constructions used by the templates of `shapes.md` (point-valued, set-valued, count-valued, optional-valued).

**Definition — VocabularyPartition.** Partition `V_atom` by codomain:

`V_bool = {P ∈ V_atom : codom(P) = Bool}` — *Boolean atoms*

`V_val  = V_atom \ V_bool` — *value-returning atoms*

Examples: `is_K`, `has_K`, `cites_K`, `all_K_resolved` are Boolean atoms; `K_sidecar_of`, `K_incoming`, `latest_K_for_addr`, `outgoing_K`, `unresolved_K_comments` are value-returning atoms.

Boolean atoms compose under propositional connectives (PC0); value-returning atoms compose under function application (PC2) and feed into quantification domains (PC1).


## Boolean Composition (PC0)

**PC0 — BooleanClosure.** Let `P, Q` be predicates with shared signature `S → Bool` (atomic or already composed). Then the following are also predicates with signature `S → Bool`:

`P ∧ Q`, `P ∨ Q`, `¬P`, `P ⇒ Q`, `P ⇔ Q`

*Proof.* Define each operator pointwise: for any `x ∈ S` and any state Σ,

`(P ∧ Q)(x, Σ) ≡ P(x, Σ) ∧_Bool Q(x, Σ)`

and similarly for the others, where `∧_Bool` is meta-level Boolean conjunction. The composed predicate's signature is `S → Bool` by construction. Both arguments are evaluated against the *same* Σ; no auxiliary state is consulted. By induction on the composition tree, well-definedness propagates from the atomic base case (Sh5) through every layer of composition. ∎

*Remark — algebraic structure.* The set of `S → Bool` functions over a fixed Σ forms a Boolean algebra under pointwise operations. PC0 is the statement that `V_bool(Σ)` and its closure under propositional operators form a sub-Boolean-algebra of the full function space. Identities like `P ∧ ¬P ⇔ ⊥` and `P ∨ ¬P ⇔ ⊤` follow from meta-level Boolean algebra and need no separate axiomatization.

*Consequences.*

(a) *Composite Boolean predicates have stable signatures.* The signature of `P ∧ Q` equals the signature of `P` (and of `Q`, which must match by typing). New signatures do not arise from PC0; only the vocabulary of expressible Bool functions over an existing signature grows.

(b) *Composition is shape-agnostic.* `P` may come from a Classifier-shape relation and `Q` from a Citation-shape relation, provided their signatures unify. PC0 does not inspect K's shape; it operates on each predicate's denotation alone.


## Quantification Domains

Quantification (PC1) requires a finite domain to range over. We separate the *syntactic class* of admissible domain expressions (static, fixed by `T_cat`) from the *interpretation* of each expression at a state (dynamic, finite at every reachable Σ).

**Definition — QuantificationDomain.** The class `QD` of *quantification-domain expressions* is the least class containing the *base domain expressions*

`A_K`, &nbsp; `L_K` &nbsp; for `K ∈ T_cat`
`C_dom` &nbsp; (the content-address space expression)
`L_dom` &nbsp; (the tuple-address space expression)
`T_cat` &nbsp; (the type catalog)

and closed under *filtering*: if `D ∈ QD` and `P : D → Bool` is a Boolean predicate from `PL` (the predicate language defined below), then `{x ∈ D : P(x)} ∈ QD`.

`QD` is mutually inductive with the predicate algebra (PC0–PC2). The mutual induction is well-founded because each expression has finite syntactic depth; the closure is the union over all finite-depth stages, equivalently the least fixed point of the constructor. `QD` depends on `T_cat` and the shape registry alone — it is static across substrate state transitions.

**Definition — DomainInterpretation.** Each `D ∈ QD` denotes, at state Σ, a finite set `[D]_Σ`. The interpretation function is fixed:

`[A_K]_Σ = A_K^Σ` &nbsp; (R6, typed-relations.md)
`[L_K]_Σ = L_K^Σ`
`[C_dom]_Σ = dom(Σ.C)`
`[L_dom]_Σ = dom(Σ.L)`
`[T_cat]_Σ = T_cat` &nbsp; (state-independent)
`[{x ∈ D : P(x)}]_Σ = {x ∈ [D]_Σ : P(x, Σ) = ⊤}`

We write `D ∈_Σ QD` for `[D]_Σ` when context makes the interpretation clear, and elide subscripts when no ambiguity arises.

**QD-fin — DomainFiniteness.** For every `D ∈ QD` and every state Σ, `[D]_Σ` is a finite set.

*Proof.* By induction on the construction of `D`.

*Base cases.* `dom(Σ.L)` is finite by L-fin (LinkStoreFiniteness, ASN-0043). `[A_K]_Σ ⊆ [L_K]_Σ ⊆ {(a, F, G) : a ∈ dom(Σ.L)}` is finite as a subset of a set bijective with `dom(Σ.L)`. `dom(Σ.C)` is finite by S8-fin (FiniteArrangement, ASN-0036) for each document's arrangement, combined with the substrate's allocation discipline — at any reachable state only finitely many content addresses are allocated, since allocation conforms to T10a (AllocatorDiscipline, ASN-0034) and the substrate produces only finitely many allocation events in any finite history. `T_cat` is finite by definition (the type catalog is closed and finite by ShapeRegistry, `shapes.md`).

*Inductive step.* If `[D]_Σ` is finite and `P : D → Bool` is well-defined on D, then `[{x ∈ D : P(x)}]_Σ = {x ∈ [D]_Σ : P(x, Σ)}` is a subset of `[D]_Σ`, hence finite. ∎


## Quantification (PC1)

**PC1 — QuantificationClosure.** For any `D ∈ QD` and any predicate `P : D → Bool` (atomic or composed), the following are predicates with signature `() → Bool` (closed terms, no free variables):

`(∀ x ∈ D :: P(x))` &nbsp; — *universal*
`(∃ x ∈ D :: P(x))` &nbsp; — *existential*

If `P` has additional free arguments — `P : D × S → Bool` — then quantification yields predicates with signature `S → Bool`:

`(∀ x ∈ D :: P(x, ·)) : S → Bool` &nbsp; with &nbsp; `(∀ x ∈ D :: P(x, ·))(s, Σ) ≡ (∀ x ∈ [D]_Σ :: P(x, s, Σ))`

and dually for `∃`. The quantifier ranges syntactically over the domain expression D; the *interpretation* `[D]_Σ` is consulted at evaluation time to produce a finite enumeration.

*Proof.* By QD-fin, `[D]_Σ` is finite at every reachable state Σ. The quantifiers reduce to finite Boolean conjunctions and disjunctions:

`(∀ x ∈ D :: P(x, s))(Σ) ≡ ⋀_{x ∈ [D]_Σ} P(x, s, Σ)`
`(∃ x ∈ D :: P(x, s))(Σ) ≡ ⋁_{x ∈ [D]_Σ} P(x, s, Σ)`

The right-hand sides are finite Boolean expressions, well-defined by PC0 and the well-definedness of `P` on each `x ∈ [D]_Σ`. ∎

*Justification.* Without quantification, atomic predicates can only test specific tuples by their full content. Quantification lets predicates ask whether *anything* in a domain has property P or whether *everything* in a domain has property P — fundamental for predicates like "every comment of kind K is resolved" or "some review exists for d." The atomic templates of Sh5 already use quantification internally (e.g., `is_K(d) ≡ (E τ ∈ A_K^Σ :: to₁(τ) = d)`); PC1 lifts quantification to a composition operator over arbitrary predicates and arbitrary substrate-derived domains.

*Consequences.*

(a) *Predicates over relations become expressible at the algebra level.* Atomic predicates from Comment shape bind a single tuple. Quantifying over `A_{K_comment}^Σ` and asking "is each comment resolved?" composes the atomic with universal quantification — a predicate that template instantiation alone does not yield.

(b) *Quantifier domains are themselves substrate-derived.* A predicate of the form `(∀ τ ∈ {τ' ∈ A_K^Σ : Q(τ')} :: P(τ))` quantifies over a filtered active subset; the filter Q is itself a Bool predicate. Filtered domains compose freely.

(c) *Cross-type predicates are expressible.* Quantifying over `T_cat` lets a predicate ask "for every type K, does some relation in `L_K` target d?" — a question the atomic vocabulary at any single K cannot ask.


## Value Composition (PC2)

**PC2 — ValueComposition.** Let `f : S → C₁` be a value-returning predicate (atomic or composed) and `g : C₁ → C₂` be another predicate (atomic or composed) whose domain matches f's codomain. Then the *function composition*

`(g ∘ f) : S → C₂` &nbsp; with &nbsp; `(g ∘ f)(s, Σ) ≡ g(f(s, Σ), Σ)`

is a predicate. In particular: if `P : C₂ → Bool` and `f : S → C₁` is composable through some `g : C₁ → C₂`, then `P ∘ g ∘ f : S → Bool` is a Boolean composed predicate.

*Proof.* Function composition over typed function spaces is closed when the codomain of the inner function matches the domain of the outer. By Definition of Codom and Definition of Signature, the codomains used by the templates of Sh5 are exactly the domains permitted as predicate inputs (`A_doc`, `A_rel`, `℘_fin(A)`, etc.). Composition is total when the inner function is total over its domain (SlotAccessorTotality, `shapes.md`, plus Sh4 idempotency for templates whose well-definedness depends on uniqueness of an active match). For partial atoms (e.g., `to₁⁻` for `c_G = 0|1` shapes), see Remark below. ∎

*Remark — partial atoms.* For shapes with `c = 0|1` (e.g., Provenance), the point accessor `to₁⁻ : L_K → t_G ∪ {⊥}` is partial; the value `⊥` denotes "slot is empty." Value composition through partial atoms requires explicit handling: `g(to₁⁻(τ))` is undefined when `to₁⁻(τ) = ⊥`. The standard guarding pattern is

`if to₁⁻(τ) ≠ ⊥ then g(to₁⁻(τ)) else default-value`

which expresses the partiality at the predicate algebra level. PC2 admits this as a Boolean-conditioned composition — well-defined because the guard is itself a PC0-composed Boolean predicate.

*Justification.* Some predicates depend on values pulled from the substrate, not just on tuple existence. `K_is_fresh(d)` consumes `K_sidecar_of(d)` and joins it with metadata. `latest_K_for_addr(d)` consumes `argmax` over a domain. Without value composition, predicates could only test pre-canonicalized tuple membership; with PC2, the substrate's structured data flows into the predicate algebra.

*Consequences.*

(a) *Pipelines are expressible.* `is_K_fresh(d) ≡ has_K(d) ∧ mtime(K_sidecar_of(d)) ≥ mtime(d)` is a value-composing Boolean predicate. Substrate state and ambient metadata flow through `K_sidecar_of` and `mtime` into the Boolean test.

(b) *Aggregation via finite domains.* `K_incoming(b) ≡ {from₁(τ) : τ ∈ A_K^Σ ∧ to₁(τ) = b}` is a value composition that returns a set. PC2 admits this as a composed value, since the right-hand side is a finite set comprehension — a function of Σ and b alone.

(c) *Closure under finite codomains only.* PC2 does not introduce new codomains beyond Codom; composition is closed within the codomain set fixed by Sh5's templates. New codomains require new templates (i.e., new canonical shapes), not new composition primitives.


## View Parametricity (PC3)

**PC3 — ViewParametricity (META).** Every composed predicate `P` takes an *implicit view parameter* `view ∈ {active, audit}` that fixes the relation values its atomic queries consult. The same composed predicate body P denotes two distinct predicates `P_active` and `P_audit` according to the view selection:

`P_active(args, Σ) ≡ P(args, Σ) evaluated with all atomic queries against A_K^Σ`

`P_audit(args, Σ)  ≡ P(args, Σ) evaluated with all atomic queries against L_K^Σ`

*Justification.* Atomic predicates in the templates of Sh5 query `A_K^Σ` by default — this is the operational view, "what is currently in effect." But every atomic template can equally be evaluated against `L_K^Σ` to ask audit questions: "did this fact ever exist?" rather than "does this fact exist now?" The view is a parameter of evaluation, not of predicate definition. PC3 is META rather than LEMMA because it asserts a design property of the algebra (that view selection is global to a top-level predicate by convention) rather than a mathematical theorem about the closure.

*Consequences.*

(a) *Operational and historical queries share the predicate algebra.* The same body `is_K(d)` can ask "is d a claim now?" (active view) or "was d ever classified as a claim?" (audit view). The substrate exposes both through one composition framework.

(b) *Mixed-view predicates are admitted but rare.* A predicate could combine an active query with an audit query — "is τ active *and* did some retraction ever target τ?" The composition is permitted by PC0–PC2, but its meaning is application-specific. The standard convention is to fix the view once per top-level predicate and let atomic queries inherit it.

(c) *Default view is the active subset.* When the view is unspecified, A_K is meant. Audit predicates are explicitly marked.


## Evaluation Semantics (PC4, PC5)

**PC4 — Purity.** Composed predicates are pure functions of `(Σ.C, Σ.M, Σ.L)` and their explicit arguments. Predicate evaluation has no side effects on the substrate, no memoized state across cycles, and no dependency on the order or history of past emissions.

`(A composed predicate P, args ∈ dom(P), Σ :: P(args, Σ) is determined by (Σ.C, Σ.M, Σ.L) and args alone)`

*Proof.* By induction on the syntactic structure of the composition.

*Base case.* Atomic predicates evaluate via `Observe_K` (typed-relations.md). Observe takes a pattern and a view and returns the matching tuple set; by definition it reads `Σ.L` (and, for the active view, `L_R^Σ` to compute `nullified(Σ)`). No additional state is consulted. R6 (ActiveSubsetWellDefinedness) confirms that `A_K^Σ` is determined by `Σ.L` alone. So atomic evaluation depends only on Σ and the template's substituted arguments.

*Inductive step.* PC0 yields composed predicates whose denotation is a meta-level Boolean operator on its constituents; PC1 yields finite quantifications which reduce to finite Boolean expressions over a quantification domain (itself a function of Σ by QD-fin); PC2 yields function compositions over typed function spaces. Each operation preserves purity: a finite combination of pure functions is pure; a finite quantification over a Σ-dependent domain composed of pure body-evaluations is pure. ∎

**PC5 — TerminationOnFiniteSubstrate.** For any composed predicate P, any state Σ with finite L (which holds at every reachable state by L-fin), and any well-typed args, evaluation of `P(args, Σ)` terminates in finite time.

*Proof.* By induction on composition structure.

*Base case.* Atomic predicates terminate by finite enumeration of `A_K^Σ` (finite by QD-fin, established above) and finite Boolean / equality tests on each enumerated tuple.

*Inductive step.* PC0 reduces to constant-time meta-Boolean operators on already-evaluated constituents. PC1 reduces to finite ⋀ and ⋁ over finite domains (QD-fin); each iteration is a constituent evaluation, which terminates by inductive hypothesis. PC2 is finite function composition: each function in the chain terminates by inductive hypothesis, and the chain itself has bounded depth fixed by the predicate's syntax. The full composition tree is finite by the syntactic finiteness of the predicate term. ∎

*Consequences of PC4 + PC5.*

(a) *No memoization across cycles.* Every predicate evaluation reads the current substrate from scratch. The runner's quiescence check fires-then-evaluates; it does not consult prior evaluation results. Stale predicate values cannot poison the system because none are retained.

(b) *Concurrent evaluation is safe by construction.* Two agents evaluating the same predicate against the same Σ produce the same answer; no synchronization is required for correctness of evaluation. Coordination during emit is a separate concern, addressed by R0 (TupleAddressFreshness).

(c) *Predicates are decidable on any reachable substrate.* PC5 makes every composed predicate's truth value a computable function. The substrate's reachable-state finiteness ensures decidability is automatic.


## Expressive Closure (PC6)

**PC6 — ExpressiveClosure.** The substrate's predicate language is *exactly* the closure of the atomic vocabulary `V_atom` under PC0 (Boolean composition), PC1 (quantification), and PC2 (value composition). No predicate outside this closure is expressible at the substrate level.

Formally, define the *predicate language* `PL` as the least class of (typed, finite-arity) predicate expressions over substrate-derived domains containing `V_atom` and closed under PC0, PC1, and PC2. `PL` is static — fixed by `T_cat` and the shape registry, like `V_atom` and `QD`. Each `P ∈ PL` denotes, at state Σ and arguments args, a value `P(args, Σ)` in its codomain. Then:

`(A function F : args × State → C : F is substrate-evaluable :: F ∈ PL)`

*Proof.* The "⊆" direction is immediate: every member of `PL` is substrate-evaluable by PC4 (Purity) and PC5 (Termination), where evaluation against state Σ is well-defined for every expression in `PL`.

For "⊇" — that nothing else is substrate-evaluable — observe: the substrate's read primitives are exactly Observe (typed-relations.md, the only read operation on `Σ.L`), the active-subset machinery (R6, derived from Observe via `L_R^Σ`), and the substrate's address arithmetic (T2 IntrinsicComparison, ASN-0034, used for tuple-address comparison in the Coverage shape's `argmax`). Every other operation in the substrate is Emit, which is a write — not part of predicate evaluation.

A substrate-evaluable function therefore has its evaluation tree decomposable as a finite tree whose leaves are Observe queries (yielding finite tuple sets by QD-fin) and whose internal nodes are meta-level Boolean operators, finite-domain quantifiers, or function compositions over typed codomains. The atomic templates of Sh5 enumerate the leaf-level forms (each atom is one or more Observe queries plus a fixed combinator); PC0–PC2 enumerate the internal-node forms. By induction on the evaluation tree, every substrate-evaluable function decomposes into atoms-plus-composition, hence lies in `PL`. ∎

*Consequences.*

(a) *Capability is bounded by the shape catalog.* Adding a new canonical shape to the catalog (with its own template family) is the only way to raise the expressive ceiling of the predicate language. Adding a new K with an existing shape generates atoms within the existing ceiling; adding a new shape adds new atomic forms, hence new closures.

(b) *Quality questions are non-substrate.* "Is this proof correct?", "is this description coherent?", "are these two claims really equivalent?" — none of these has a finite Observe-tree decomposition. They are agent-time questions; the substrate cannot ask or answer them.

(c) *Quiescence is itself a substrate predicate.* The convergence condition — "every public predicate of every agent evaluates true against `A_K^Σ`" — is a finite ∀ over a finite agent set composed with each agent's public predicate. By PC0 + PC1, this is in `PL`. By PC4 it is pure; by PC5 it is decidable. The system's terminal condition is recognizable by the substrate itself — a property crucial for the runner's quiescence check.


## Examples

We illustrate composition with three concrete predicates, decomposed into their atomic and compositional structure.

### Quiescence of a claim

`is_claim_quiescent(d) ≡ all_revise_resolved(d) ∧ all_observe_resolved(d)`

- `all_revise_resolved` and `all_observe_resolved` are atomic predicates from Comment shape (Sh5 walkthrough), instantiated at types `K_revise` and `K_observe` respectively. Each takes a single `A_doc` argument.
- The composition is a Boolean conjunction (PC0) with shared signature `A_doc → Bool`.
- View parameterization (PC3): both atomic queries default to `A_K^Σ` and consult the corresponding active resolution relation; the audit-view variant `is_claim_quiescent_audit(d)` would ask "was d ever quiescent?" — meaningful but rare.

### Confirmation of a claim

`is_claim_confirmed(d) ≡ is_claim_quiescent(d) ∧ has_review(d) ∧ latest_review_was_clean(d)`

- `is_claim_quiescent(d)` — defined above; a PC0-composed Boolean.
- `has_review(d)` — composed via PC1 from a Boolean atom on Coverage shape:

  `has_review(d) ≡ (∃ τ ∈ A_{K_review}^Σ :: to₁(τ) = d)`

  An existential quantification (PC1) over the active subset of the review-coverage relation, whose body is an equality test on the Boolean-yielding atom from the slot accessor.

- `latest_review_was_clean(d)` — uses Coverage shape's `latest_K_for_addr` (a value-returning atom from Sh5) to retrieve the latest review tuple, passes the result through a Tuple-Classifier atom `is_clean : A_rel → Bool` (Sh5 walkthrough, `shapes.md`), and composes via PC2:

  `latest_review_was_clean(d) ≡ is_clean(latest_K_for_addr_review(d))`

  The decomposition is `(is_clean ∘ latest_K_for_addr_review)(d)`. The atomic `is_clean(τ)` is generated by Tuple-Classifier shape `(0, 1, -, A_rel, ⊤)` — the A_rel-targeted bipartite analogue of Classifier; the outer structure is PC2 composition through a value-returning Coverage atom.

The full composition has signature `A_doc → Bool`; it combines Comment-shape atoms, a Coverage-shape existential (via PC1), a Tuple-Classifier atom composed through a value-returning Coverage atom (PC2), and Boolean conjunction (PC0). Every step lies in PC0–PC2; no construction outside the closure is needed.

### Frame-condition style universality

`every_active_citation_resolves(d) ≡ (∀ τ ∈ S_d :: (∃ b ∈ dom(Σ.C) :: to₁(τ) = b ∧ is_claim(b)))`

where `S_d = {τ' ∈ A_{K_dep}^Σ : from₁(τ') = d}` is a filtered quantification domain.

- `S_d` is built by filtering `A_{K_dep}` (a base domain expression, interpreted at Σ as `A_{K_dep}^Σ`) by a Boolean predicate on `from₁`. By the inductive QD construction, `S_d ∈ QD`.
- The outer ∀ (PC1) ranges over `S_d`; the body is an existential over `dom(Σ.C)` testing the conjunction (PC0) of `to₁(τ) = b` (a Boolean atom on slot equality) and `is_claim(b)` (a Classifier-shape atomic predicate).
- The composition is fully within PC0–PC2; the predicate states "every outgoing dependency of d resolves to an active claim."


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| V_atom | DEF | Atomic vocabulary `⋃_K Tpl(shape(K))[K]` — *static*, fixed by `T_cat` and shape registry | introduced |
| V_bool, V_val | DEF | Partition of `V_atom` by codomain (Bool vs value-returning) | introduced |
| Codom | DEF | Set of admissible codomains for atomic and composed predicates | introduced |
| Signature | DEF | Predicate signature `D₁ × ... × Dₙ → C` | introduced |
| QD | DEF | Static class of quantification-domain expressions, closed under filtering | introduced |
| `[D]_Σ` | DEF | Interpretation of domain expression D at state Σ — finite by QD-fin | introduced |
| QD-fin | LEMMA | DomainFiniteness — every domain interpretation is finite (= L-fin + S8-fin + \|T_cat\| < ∞) | introduced |
| PL | DEF | Predicate language — least closure of `V_atom` under PC0–PC2; *static* | introduced |
| PC0 | LEMMA | BooleanClosure — `V_bool` closed under ∧, ∨, ¬, ⇒, ⇔ | introduced |
| PC1 | LEMMA | QuantificationClosure — finite ∀ and ∃ over `D ∈ QD` interpreted at Σ | introduced |
| PC2 | LEMMA | ValueComposition — function composition over typed codomains | introduced |
| PC3 | META | ViewParametricity — `A_K` vs `L_K` is an evaluation parameter | introduced |
| PC4 | LEMMA | Purity — composed predicates are pure functions of `(Σ, args)` | introduced |
| PC5 | LEMMA | TerminationOnFiniteSubstrate — evaluation halts in finite time | introduced |
| PC6 | THM | ExpressiveClosure — substrate-evaluable predicates = `PL` | introduced |


## Open Questions

- Is *recursion* over predicates expressible? `is_claim_confirmed` references `is_claim_quiescent`, which is a definitional macro-expansion (substitution at parse time). Mutually-recursive predicate definitions ("a tuple is settled iff every tuple it depends on is settled") would not terminate under PC5 without an explicit fixed-point operator. Should the substrate admit a least-fixed-point operator (PC7?), or rule recursion out by construction and require recursion to be unrolled at agent time?

- *Aggregation* (counts, sums, max/min over numeric value codomains) appears in templates like `latest_K_for_addr` (via `argmax`). Is aggregation a fourth composition primitive distinct from PC2, or is it sufficiently captured by value composition over substrate-derived numeric atoms? In particular: where do the arithmetic operators (`+`, `≤`, `argmax`) come from — are they substrate primitives or meta-level?

- The mutual induction defining `QD` and `PL` produces a least fixed point. Are there derivable domains the language *cannot* express — domains expressible at a meta level but not constructible by base + filter? In particular, can the language express domains defined by ∃-introduced existential witnesses (e.g., "the set of x such that some y witnesses P(x, y)"), or must such domains be flattened into PC1's quantifier prefix?

- PC3 makes the view a global parameter per top-level predicate by convention. Mixed-view predicates are admitted by the algebra. Should a composition primitive promote the view to a first-class parameter (e.g., `P[view]`), allowing fine-grained mixing — and if so, what invariants must hold across view boundaries?

- The closure theorem (PC6) asserts the predicate language equals a specific algebraic closure. Is there an effective decision procedure that, given an arbitrary syntactic expression, decides whether it lies in `PL`? Well-typing is decidable (it reduces to signature unification and shape-registry lookup); whether `PL` *restricted to extensionally non-equivalent predicates* admits a normal form is open.

- *Side-effecting evaluation* — predicates that emit substrate facts as a byproduct of evaluation — would violate PC4 (Purity). The architecture rules this out at the predicate algebra level, but agents that observe-then-emit during their own decision process produce a similar effect at a different layer. Where is the boundary between predicate evaluation (pure) and agent computation (which may emit), and what invariants does that boundary preserve?