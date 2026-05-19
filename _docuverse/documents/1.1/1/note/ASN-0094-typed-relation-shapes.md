# ASN-0094: Typed Relation Shapes

*Restricting the relational primitive into a predicate language.*

ASN-0086 establishes typed relations `L_K` with the three operations Emit, Observe, Nullify, governed by R0–R7. The relational structure as defined there is too permissive to support a typed predicate vocabulary: F and G can be any finite endsets whose coverage lies anywhere in `A`, so a predicate over `L_K` has no fixed signature. Every predicate would have to take a pattern in `℘(A) × ℘(A)` and return Bool, "two relations of the same shape" would not be expressible, and slot accessors `from(τ)`, `to(τ)` would be partial in a way that defeats type-checking.

We are looking for the minimum additional layer that closes this gap. The answer is a single structural decision per type: each `K ∈ T_cat` is assigned a *shape* — a tuple of constraints on cardinality, target domain, and idempotency — and the substrate enforces shape-conformance at Emit time. From the shape, a predicate template family is mechanically derivable. The pipeline is:

> R0–R7 (typed relations + operations) → **shape restrictions** (this document) → predicate template families → composed predicates

Shapes are not derivable from R0–R7. They are an additional design decision the substrate makes about which relations it admits and what `(F, G)` pairs each admits. We justify each constraint by what predicate forms it makes possible, and by what the substrate cannot express without it.


## The Address-Set Projection

Shape constraints operate on the address-set view of a tuple, not on the underlying endset structure. We make the projection explicit.

**Definition — Coverage Projection.** For each tuple `(a, F, G) ∈ L_K`, define

`cov : L_K → ℘_fin(A) × ℘_fin(A)`

`cov(a, F, G) = (coverage(F), coverage(G))`

where `coverage(·)` is the union of address sets denoted by the endset's spans (Definition, ASN-0043).

The address-set view is a lossy projection — by L5 (EndsetSetSemantics, ASN-0043), endsets with different span decompositions can have identical coverage. For shape purposes the loss is intentional: shapes are predicates over what addresses a slot references, not over how those addresses are denoted.

**Convention — CanonicalSlotForm.** For c_F = 1 shapes with `t_F` an element-level address set, the canonical form of `F` is a single unit-depth span `{(x, δ(1, #x))}` at the slot's intended address `x`. By PrefixSpanCoverage (ASN-0043), `coverage({(x, δ(1, #x))}) = {t : x ≼ t}`; intersected with the set of allocated addresses, this denotes `{x}` plus any allocated extensions of `x`. For element-level addresses with no allocated descendants (the typical case), the intersection is the singleton `{x}`. Throughout this document, when we write `|coverage(F)| = 1`, we mean the cardinality at the canonical interpretation — the count of allocated addresses denoted, which for canonical-form F is one.


## Shape

**Definition — Shape.** A *shape* is a tuple

`Σ_K = (c_F, c_G, t_F, t_G, idem)`

with components:

- `c_F, c_G ∈ {0, 1, *, 0|1}` — *cardinality bounds* on `|coverage(F)|` and `|coverage(G)|`. The values 0 and 1 are exact; `*` denotes "any natural number"; `0|1` denotes "0 or 1 exactly."
- `t_F, t_G ⊆ A` — *target-domain restrictions*. Each is one of `A_doc`, `A_rel`, `A`, or the distinguished value `-` (used when the corresponding cardinality is `0`).
- `idem ∈ {⊤, ⊥}` — the *idempotency flag*.

**Definition — CardinalityMatch.** For `n ∈ ℕ` and `c ∈ {0, 1, *, 0|1}`:

`match(n, c) ≡ (c = 0 ∧ n = 0) ∨ (c = 1 ∧ n = 1) ∨ (c = * ∧ n ∈ ℕ) ∨ (c = 0|1 ∧ n ∈ {0, 1})`

**Definition — ShapeRegistry.** A function

`shape : T_cat → Shape`

assigns each typed relation in the catalog its shape. The shape registry is part of the substrate's specification — registering a new K in T_cat requires registering its shape.

**Definition — Conformance.** A tuple `(a, F, G) ∈ L_K` is *shape-conformant* iff

`match(|coverage(F)|, c_F) ∧ match(|coverage(G)|, c_G) ∧ coverage(F) ⊆ t_F ∧ coverage(G) ⊆ t_G`

where `(c_F, c_G, t_F, t_G, _) = shape(K)`. We write `conf_K(F, G)` for the predicate that an `(F, G)` pair would produce a conformant tuple under type K.


## The Conformance Axiom

**Sh-conf — ShapeConformanceAxiom.** The substrate restricts Emit_K from ASN-0086 by adding a precondition:

`Emit_K(F, G)` succeeds iff `conf_K(F, G)`; emissions failing the precondition are rejected before any state transition occurs.

*Justification.* This is an axiom about the substrate's enforcement, not a theorem derivable from R0–R7. R0 (TupleAddressFreshness) alone permits any `(F, G, K)` triple to be emitted. Sh-conf narrows the admissible triples; that narrowing is what makes the predicate language well-typed. Without Sh-conf, the cardinality and target-domain consequences (Sh0–Sh3 below) would not hold across state transitions — they would be vacuously true on an empty `L_K` and immediately false after the first non-conformant emission.


## Cardinality (Sh0, Sh1)

**Sh0 — FromCardinalityFixed.** For each `K ∈ T_cat`, every tuple in `L_K` has from-set address-cardinality matching `c_F`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: match(|coverage(F)|, shape(K).c_F))`

*Proof.* By induction on the state Σ.

*Base case.* At the initial state, `L_K^{Σ_0} = ∅` for every K, so the universal quantifier is vacuous.

*Inductive step.* Suppose the property holds at Σ, and let `Σ → Σ'` be a state transition. By R3 (TypedSliceMonotonicity, ASN-0086), `L_K^Σ ⊆ L_K^{Σ'}`. Tuples in `L_K^Σ` retain their value (by R2, TupleAddressPermanence) and therefore retain their from-set coverage; conformance is preserved for them by the inductive hypothesis. New tuples `(a, F, G) ∈ L_K^{Σ'} \ L_K^Σ` arise only via Emit_K. By Sh-conf, the emission succeeded only if `conf_K(F, G)`, which requires `match(|coverage(F)|, c_F)`. So all new tuples are conformant in the from-slot. ∎

**Sh1 — ToCardinalityFixed.** Same for the to-set:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: match(|coverage(G)|, shape(K).c_G))`

*Proof.* Symmetric to Sh0. ∎

*Justification of the constraint itself.* Without uniform cardinality per type, "the d in this tuple's G" is ambiguous when `|coverage(G)|` varies — predicates that bind G's slot positions cannot be defined uniformly. Fixed cardinality lets templates parameterize on slot positions: a (1, 1)-shape relation has well-defined `from(τ)` and `to(τ)` accessors; a (0, 1)-shape relation has only `to(τ)`; an (\*, 1)-shape relation has `to(τ)` plus a from-set accessor that returns a set rather than a single address.

*Consequences.*

(a) *Predicates have stable signatures.* For a relation of shape `(0, 1, -, A_doc, _)`, predicates take a single document argument: `is_K : A_doc → Bool`. For shape `(1, 1, A_doc, A_doc, _)`, predicates take an ordered pair: `cites_K : A_doc × A_doc → Bool`. The signature is determined by the shape, not by individual emissions.

(b) *Counting and aggregation are well-defined.* "How many comment-tuples target d?" is a number because `|coverage(G)| = 1` (Sh1) and "targets d" has a uniform meaning across the relation.

(c) *Slot accessors are total on the relevant slots.* See SlotAccessorTotality below.


## Target Domain (Sh2, Sh3)

**Sh2 — FromTargetRestricted.** For each `K ∈ T_cat` with `shape(K).t_F` defined (i.e., `c_F ≠ 0`):

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: coverage(F) ⊆ shape(K).t_F)`

*Proof.* By induction on Σ, identical in structure to Sh0. The base case is vacuous (`L_K^{Σ_0} = ∅`); the inductive step uses R2, R3, and Sh-conf to inherit and preserve the constraint. ∎

**Sh3 — ToTargetRestricted.** Symmetric for the to-slot:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: coverage(G) ⊆ shape(K).t_G)`

*Proof.* Symmetric to Sh2. ∎

*Justification of the constraint itself.* R4 (TupleAddressDisjointness, ASN-0086) gives us two address kinds — `A_doc` and `A_rel` — but does not by itself constrain *which* kind appears in any given slot. Sh2/Sh3 do: each slot of each relation targets one fixed kind. Without this, the same predicate template would have to handle both document targets and tuple targets, and predicate type-checking at the slot level would fail.

*Consequences.*

(a) *Predicates are typed at the slot level.* For relations targeting documents (`t_G = A_doc`), `to(τ) : L_K → A_doc`; for relations targeting tuples (`t_G = A_rel`, e.g. retraction, resolution), `to(τ) : L_K → A_rel`. The codomain of `to` is determined by `t_G`, not by individual emissions.

(b) *Self-referential and document-targeting relations are syntactically distinguished.* A relation with `t_G = A_rel` is *about other relations*; a relation with `t_G = A_doc` is *about documents*. The active-subset machinery (R6, ASN-0086) consumes only relations with `t_G = A_rel`; document-classifier predicates consume only relations with `t_G = A_doc`. The shape registry tells you which is which, statically.

(c) *Operational composition is mechanically checkable.* Composing two relations through their slots requires that the joining slots have compatible target domains. Sh2/Sh3 make compatibility decidable from the shape registry alone.


## Slot Accessors

The cardinality and target-domain constraints together permit the definition of slot accessor functions whose totality is guaranteed by Sh0–Sh3.

**Definition — SetSlotAccessors.** For each `K ∈ T_cat`:

`from_K : L_K → ℘_fin(shape(K).t_F)` &nbsp; with &nbsp; `from_K(a, F, G) = coverage(F)`

`to_K   : L_K → ℘_fin(shape(K).t_G)` &nbsp; with &nbsp; `to_K(a, F, G) = coverage(G)`

These are total on `L_K` for any shape; the codomain is restricted by Sh2/Sh3.

**Definition — PointSlotAccessors.** For shapes with `c_F = 1`:

`from₁ : L_K → shape(K).t_F` &nbsp; with &nbsp; `from₁(τ) = the unique element of from_K(τ)`

For shapes with `c_G = 1`:

`to₁ : L_K → shape(K).t_G` &nbsp; with &nbsp; `to₁(τ) = the unique element of to_K(τ)`

For shapes with `c_F = 0|1` or `c_G = 0|1`, the point accessor returns `⊥` (undefined) when the coverage is empty:

`from₁⁻ : L_K → shape(K).t_F ∪ {⊥}` &nbsp; defined when `c_F ∈ {1, 0|1}`.

**Lemma — SlotAccessorTotality.** When `shape(K).c_F = 1`, `from₁` is a total function on `L_K`. Similarly for `to₁` when `c_G = 1`.

*Proof.* By Sh0, every `τ ∈ L_K` has `|from_K(τ)| = |coverage(F)| = 1` (since `match(n, 1) ⟺ n = 1`). A finite set of cardinality 1 has a unique element. Define `from₁(τ)` as that element. By Sh2, this element lies in `t_F`. ∎

For the rest of this document, we drop subscripts and write `from`, `to` when the shape unambiguously fixes which accessor is meant. We additionally use `addr(τ) = a` for the tuple address (R1, AddressInjectivity, ASN-0086).


## Idempotency (Sh4)

**Sh4 — IdempotencyDiscipline.** When `shape(K).idem = ⊤`, higher layers above the substrate enforce at most one *active* tuple in `L_K` with any given coverage pair:

`(A τ, τ' ∈ A_K^Σ : cov(τ) = cov(τ') :: addr(τ) = addr(τ'))`

*Status.* Sh4 is a policy, not a substrate-enforced axiom. The substrate itself does not enforce it. R0 (TupleAddressFreshness) explicitly permits two emissions with identical `(F, G)` to produce two distinct tuples; R1 (AddressInjectivity) keeps them distinguishable. Idempotency is realized as: before emitting `(F, G)` into an idempotent relation, the calling layer first executes `Observe_K(coverage(F), coverage(G), A_K^Σ)`; if a match exists, the emission is suppressed.

*Justification of the policy.* Some predicates need yes/no semantics on tuple existence: "is `d` classified as a claim?" should not be answered by counting the number of `(∅, {d})` tuples in `L_claim`. For idempotent relations the predicate template uses *set semantics* — the active relation is treated as a set of `(F, G)` coverage pairs at the active level, with multiplicities collapsed. For non-idempotent relations (e.g., Comment, where each comment is a distinct event even if it has identical coverage), the predicate template uses *bag semantics* — multiplicities are preserved.

*Consequences.*

(a) *Existence-vs-count distinction.* Idempotent relations support `exists_K(F, G) : Bool` predicates with stable yes/no answers. Non-idempotent relations support `count_K(...)` predicates whose value reflects the number of distinct emission events.

(b) *Re-emit-vs-fail behavior is registry-driven.* Library helpers like `emit_attribute` consult `shape(K).idem` to decide whether to short-circuit on existing match or always allocate a fresh address. The decision is mechanical from the shape, not from inspection of K's name.

(c) *Idempotency is a property of A_K, not L_K.* By R3, `L_K` always retains every emission ever made — duplicates included. Idempotency restricts what reaches `A_K`. Once a duplicate is emitted, it stays in `L_K` for audit but the emission policy ensures only one is active at a time. Retraction-then-reemit cycles can leave multiple coverage-identical tuples in `L_K` with at most one active.


## Template Generation (Sh5)

**Sh5 — TemplateGeneration.** For each canonical shape `Σ_canon`, there exists a fixed family of predicate templates `Tpl(Σ_canon)` such that for any `K ∈ T_cat` with `shape(K) = Σ_canon`, the predicates `{tpl[K] : tpl ∈ Tpl(Σ_canon)}` are mechanically derivable from K's shape and name alone.

*Proof sketch.* Each template body is expressed in terms of (i) slot accessors (`from`, `to`, `addr`) whose existence and totality are guaranteed by Sh0–Sh3 and SlotAccessorTotality; (ii) target-domain typing (Sh2/Sh3) that determines whether a slot returns an `A_doc` address or an `A_rel` address; (iii) the active-subset view `A_K^Σ` (R6, ASN-0086), refined per Sh4 into set semantics (`idem = ⊤`) or bag semantics (`idem = ⊥`); and (iv) the existential and universal quantifiers of the substrate's logic. None of these depends on K beyond K's name; instantiating a template at a particular K substitutes K's name into the template body, with no additional design decisions. ∎

The substantive content of Sh5 is what the templates *are* — not just that they exist, but what predicate forms each canonical shape generates. We exhibit them in the catalog and walkthrough below.


## The Canonical Shape Catalog

The substrate's relations fall into a small fixed set of canonical shapes. Each canonical shape pairs with a predicate template family that is forced by the shape — there is no design freedom in template selection once the shape is fixed.

| Shape            | (c_F, c_G) | t_F   | t_G   | idem | Template family                                              |
|------------------|------------|-------|-------|------|--------------------------------------------------------------|
| Classifier       | (0, 1)     | -     | A_doc | ⊤    | `is_K(d)`                                                    |
| Tuple-Classifier | (0, 1)     | -     | A_rel | ⊤    | `is_K(τ)`                                                    |
| Attribute        | (1, 1)     | A_doc | A_doc | ⊤    | `has_K(d)`, `K_sidecar_of(d)`, `K_is_fresh(d)`               |
| Citation         | (1, 1)     | A_doc | A_doc | ⊤    | `cites_K(a, b)`, `K_incoming(b)`                             |
| Coverage         | (1, 1)     | A_doc | A_doc | ⊥    | `latest_K_for_addr(d)`                                       |
| Comment          | (1, 1)     | A_doc | A_doc | ⊥    | `unresolved_K_comments(d)`, `all_K_resolved(d)`              |
| Resolution       | (1, 1)     | A_doc | A_rel | ⊤    | (consumed by `all_K_resolved` template at Comment shape)     |
| Retraction       | (\*, 1)    | A     | A_rel | ⊤    | (consumed by R6's active-subset definition)                  |
| Provenance       | (1, 0\|1)  | A     | A     | ⊤    | `outgoing_K(s)`                                              |

The catalog has *bipartite coverage*: for each structural pattern (cardinality + idempotency), entries with `t_G = A_doc` and `t_G = A_rel` are listed separately. Classifier and Tuple-Classifier are the two `(0, 1, -, ·, ⊤)` rows; Attribute and (a hypothetical Tuple-Attribute) would be the two `(1, 1, ·, ·, ⊤)` rows on the document/tuple axis. The current catalog enumerates the rows demanded by present-day predicate templates; further bipartite entries can be added without changing the framework.


## Per-Shape Template Walkthroughs

We walk the canonical shapes and exhibit the predicate templates each generates.

### Classifier — `(0, 1, -, A_doc, ⊤)`

Every tuple in `L_K` has `coverage(F) = ∅` (Sh0) and `coverage(G) = {d}` for some `d ∈ A_doc` (Sh1, Sh3). The to-accessor `to₁(τ) ∈ A_doc` is total (SlotAccessorTotality).

`is_K(d) ≡ (E τ ∈ A_K^Σ :: to₁(τ) = d)`

A document `d` is *classified as K* iff there exists an active tuple in `L_K` whose to-slot is `d`. By Sh4 idempotency, the existential is yes/no — multiple coverage-identical active tuples are precluded by policy.

### Tuple-Classifier — `(0, 1, -, A_rel, ⊤)`

Structurally identical to Classifier; the only difference is the target domain. Every tuple in `L_K` has `coverage(F) = ∅` and `coverage(G) = {τ}` for some `τ ∈ A_rel`. The to-accessor `to₁(σ) ∈ A_rel` is total.

`is_K(τ) ≡ (E σ ∈ A_K^Σ :: to₁(σ) = τ)`

A tuple `τ` is *classified as K* iff there exists an active classifier-tuple in `L_K` whose to-slot is `τ`. The single-letter substitution `d ↝ τ` from Classifier's template body is the only difference; signature changes from `A_doc → Bool` to `A_rel → Bool`.

Tuple-Classifier admits useful predicates over substrate-internal entities — marking a comment-tuple as endorsed, marking a citation-tuple as deprecated, marking a review-tuple as clean (so `is_clean(τ)` for `τ ∈ A_rel`). By Sh3 (`t_G = A_rel`), a Tuple-Classifier tuple's to-slot targets a tuple address, distinguishing it from a Classifier whose to-slot targets a document. The two are the bipartite halves of the same `(0, 1)` shape pattern.

*Distinction from Resolution.* Resolution `(1, 1, A_doc, A_rel, ⊤)` also targets `A_rel`, but its `c_F = 1` slot requires an actor — a resolving document. Tuple-Classifier has `c_F = 0`: no actor recorded in the tuple. Use Resolution when the assertion needs an attributed asserter; use Tuple-Classifier when the assertion is a property of the targeted tuple itself, not an action upon it.

### Attribute — `(1, 1, A_doc, A_doc, ⊤)`

Tuples have form `cov(τ) = ({d}, {s})` with `d, s ∈ A_doc` — `d` the parent document, `s` its attribute sidecar.

`has_K(d)        ≡ (E τ ∈ A_K^Σ :: from₁(τ) = d)`

`K_sidecar_of(d) ≡ to₁(τ)` &nbsp; where τ is the unique element of `{τ ∈ A_K^Σ : from₁(τ) = d}` (uniqueness by Sh4)

`K_is_fresh(d)   ≡ has_K(d) ∧ mtime(K_sidecar_of(d)) ≥ mtime(d)`

`has_K` is Boolean over A_K membership. `K_sidecar_of` is value-returning — well-defined by Sh4 idempotency, which collapses the candidate set to a singleton on success. `K_is_fresh` joins substrate state with filesystem-level metadata; it is the only template here that depends on data outside the relational structure, and its instantiation requires the user-specified `mtime` accessor in addition to K's name.

### Citation — `(1, 1, A_doc, A_doc, ⊤)`

Tuples have form `cov(τ) = ({a}, {b})` with `a, b ∈ A_doc`.

`cites_K(a, b)  ≡ (E τ ∈ A_K^Σ :: from₁(τ) = a ∧ to₁(τ) = b)`

`K_incoming(b)  ≡ {from₁(τ) : τ ∈ A_K^Σ ∧ to₁(τ) = b}`

The first is Boolean — does the citation exist? The second is value-returning — the set of documents citing b through K-typed citations. Sh4 ensures `K_incoming(b)` is a set of distinct addresses, not a multiset.

### Comment — `(1, 1, A_doc, A_doc, ⊥)`

Comments are non-idempotent: each comment is a distinct event, even with identical coverage. The predicate template depends on a separate Resolution relation `K_res` of Resolution shape (see below).

`unresolved_K_comments(d) ≡ {τ ∈ A_K^Σ : to₁(τ) = d ∧ ¬resolved_by(τ, K_res)}`

where `resolved_by(τ, K_res) ≡ (E ρ ∈ A_{K_res}^Σ :: to₁(ρ) = addr(τ))`.

`all_K_resolved(d) ≡ unresolved_K_comments(d) = ∅`

A comment τ is *unresolved* iff no active resolution tuple targets τ's address (R5, TupleSelfTargeting, ASN-0086, makes this targeting expressible). This template is what consumes the Resolution shape — Resolution does not generate its own template family; it is consumed here.

### Resolution — `(1, 1, A_doc, A_rel, ⊤)`

Tuples have form `cov(τ) = ({d}, {addr(σ)})` where `d ∈ A_doc` is the resolving document and `σ ∈ A_rel` is the comment-tuple being resolved. The shape generates no standalone predicate template — its purpose is to feed the Comment template above. Sh3 (`t_G = A_rel`) is what makes that consumption possible: a Resolution tuple's to-slot targets a tuple address, not a document.

### Retraction — `(\*, 1, A, A_rel, ⊤)`

Tuples have form `cov(τ) = (S, {addr(σ)})` for some `S ⊆ A` (possibly empty, possibly large) and `σ ∈ A_rel` the tuple being retracted. The retraction shape is consumed by R6 (ASN-0086) directly: the active-subset definition uses `L_R`'s tuples to compute `nullified(Σ)`. No predicate template family — Retraction's role is to flip A_K membership for arbitrary K, not to host its own predicates.

The unrestricted from-slot (`c_F = *`) accommodates use cases where the retracting party is recorded in F (e.g., F = {agent_address}), as well as the bare retraction `Nullify(a) ≡ Emit_R(∅, {(a, δ(1, #a))})` of R7, where F = ∅.

### Coverage — `(1, 1, A_doc, A_doc, ⊥)`

For K with this shape, multiple emissions targeting the same document d are expected (e.g., evolving review status). The template projects to the most recent:

`latest_K_for_addr(d) ≡ argmax_{τ ∈ S_d} emission_order(τ)` &nbsp; where &nbsp; `S_d = {τ ∈ A_K^Σ : to₁(τ) = d}`

This template depends on a total ordering on tuples — typically by tuple-address allocation order, which is monotone in emission time under T9 (ForwardAllocation, ASN-0034). Coverage is the only canonical shape that uses `idem = ⊥` *intentionally* to retain all historical states. Comment's `idem = ⊥` is incidental — comments differ in F or G even when "looking the same" in content; Coverage's `idem = ⊥` is principled — coverage tuples by design supersede each other.

### Provenance — `(1, 0|1, A, A, ⊤)`

Provenance tuples attribute one substrate event (the F-slot) to another (the G-slot). The G-slot may be empty (`c_G = 0|1`) — used to record agent attribution where the attributed event is the emission itself. Slot accessor `to₁⁻` is partial (returns `⊥` when G is empty).

`outgoing_K(s) ≡ {τ ∈ A_K^Σ : from₁(τ) = s}`

The single template returns the set of provenance tuples sourced at s. Predicates over provenance are typically composed atomically into agent-attribution and audit queries. The unrestricted target domains (`t_F = t_G = A`) reflect that provenance can attribute either document events or relational events to either kind of source.


## Consequences

(a) *Adding a new relation generates predicates for free.* A new K with `shape(K) = Attribute` immediately yields `has_K`, `K_sidecar_of`, `K_is_fresh` — no per-relation predicate code is required. The cost of a new relation is one entry in the shape registry.

(b) *Composite predicates extend within the ceiling, not beyond it.* A composite predicate combines atomic predicates through Boolean operators and quantification over `T_cat`. The expressive ceiling is set by what the canonical shapes' templates yield; composition does not raise it. Capability beyond the ceiling requires a new canonical shape, not a new relation in an existing shape.

(c) *Shape misregistration is a structural error.* Registering a relation with the wrong shape produces predicates with wrong signatures or wrong semantics — the substrate cannot self-correct this. By Sh-conf, attempts to emit non-conformant tuples are rejected, but the rejection assumes the registered shape is the *correct* shape; if the registry is wrong, the substrate enforces the wrong constraint. Shape registration is part of the relation's contract.

(d) *The predicate language is bounded by the shape catalog.* "What the substrate can ask" is determined by the templates the shapes generate. Questions about content quality ("is this proof complete?", "is this description good?") are not expressible because no canonical shape's template generates them. Those are agent-time questions, not substrate questions.


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| cov | DEF | Coverage projection `L_K → ℘_fin(A) × ℘_fin(A)` | introduced |
| Σ_K | DEF | Shape: `(c_F, c_G, t_F, t_G, idem)` | introduced |
| match | DEF | Cardinality match predicate over `{0, 1, *, 0\|1}` | introduced |
| shape | DEF | Shape registry `T_cat → Shape` | introduced |
| conf_K | DEF | Conformance predicate for type K | introduced |
| from_K, to_K | DEF | Total set-valued slot accessors | introduced |
| from₁, to₁ | DEF | Point-valued slot accessors (defined when c = 1) | introduced |
| from₁⁻, to₁⁻ | DEF | Optional point-valued slot accessors (defined when c = 0\|1) | introduced |
| Sh-conf | AXIOM | ShapeConformanceAxiom — Emit_K rejects non-conformant emissions | introduced |
| Sh0 | LEMMA | FromCardinalityFixed — uniform from-coverage cardinality per type | introduced |
| Sh1 | LEMMA | ToCardinalityFixed — uniform to-coverage cardinality per type | introduced |
| Sh2 | LEMMA | FromTargetRestricted — `coverage(F) ⊆ t_F` on every tuple | introduced |
| Sh3 | LEMMA | ToTargetRestricted — `coverage(G) ⊆ t_G` on every tuple | introduced |
| SlotAccessorTotality | LEMMA | When `c = 1`, the point accessor is a total function | introduced |
| Sh4 | META | IdempotencyDiscipline — at-most-one active duplicate when `idem = ⊤`; policy, not substrate axiom | introduced |
| Sh5 | LEMMA | TemplateGeneration — each canonical shape forces a fixed template family | introduced |
| Tpl | DEF | Map from canonical shape to its predicate template family | introduced |


## Open Questions

- Should `(0, 0)` shapes be admitted? A relation with `c_F = c_G = 0` would be a single-tuple existence flag whose only role is "this event happened" without any from/to attribution; whether the substrate has any such relations is unclear, and the slot accessors degenerate to constants on it.
- Provenance's `c_G = 0|1` mixes shapes — should it be split into two distinct canonical shapes (Provenance-with-target and Provenance-attribution-only), each generating separate templates? The current formulation requires the optional accessor `to₁⁻` to handle both cases in a single template.
- Is idempotency recoverable from cardinality plus target-domain alone, or is it an independent axis? Empirically the canonical catalog has both `idem = ⊤` and `idem = ⊥` for shapes with identical (cardinality, target-domain) — Comment vs. Citation, both `(1, 1, A_doc, A_doc, _)` — suggesting independence.
- What guarantees the shape registry stays consistent across processes? The registry is part of the substrate's specification, but its persistence and concurrent-update semantics are not addressed by Sh-conf alone.
- Do *composite shapes* (relations whose F or G is itself constrained by another relation's content) require a new restriction axis, or do they decompose into existing primitives plus auxiliary predicates expressible in the current template language?
- For Coverage relations, must `emission_order` be a substrate-level guarantee, or is ASN-0034's T9 (ForwardAllocation) sufficient as an implicit ordering on tuple addresses inherited via R0 (TupleAddressFreshness)?
- The shape constraint `coverage(F) ⊆ t_F` assumes coverage is computed against the canonical interpretation. For spans whose reach exceeds the start address — e.g., type-endset spans referencing future addresses (L9, TypeGhostPermission, ASN-0043) — coverage may grow as the address space fills. Must the shape registry enforce conformance only at emission time, or must conformance be invariant under coverage growth?
- Do shape constraints commute with retraction? Specifically: if a tuple `τ` is conformant when emitted but `nullified(Σ)` later removes it from `A_K`, do predicates over `A_K` remain well-typed under Sh5's template family, or does the substrate need an additional invariant relating retraction to shape-conformance preservation?