# ASN-0094: Typed Relation Shapes

*Restricting the relational primitive into a predicate language.*

ASN-0086 establishes typed relations `L_K` with the three operations Emit, Observe, Nullify, governed by R0–R7. The relational structure as defined there is too permissive to support a typed predicate vocabulary: F and G can be any finite endsets whose coverage lies anywhere in `T`, so a predicate over `L_K` has no fixed signature. Every predicate would have to take a pattern in `℘(T) × ℘(T)` and return Bool, "two relations of the same shape" would not be expressible, and slot accessors `from(τ)`, `to(τ)` would be partial in a way that defeats type-checking.

We are looking for the minimum additional layer that closes this gap. The answer is a single structural decision per type: each `K ∈ T_cat` is assigned a *shape* — a tuple of constraints on cardinality, target domain, and idempotency — and the substrate enforces shape-conformance at Emit time. From the shape, a predicate template family is mechanically organized (though not mechanically derived; see Sh5). The pipeline is:

> R0–R7 (typed relations + operations) → **shape restrictions** (this document) → predicate template families → composed predicates

Shapes are not derivable from R0–R7. They are an additional design decision the substrate makes about which relations it admits and what `(F, G)` pairs each admits. We justify each constraint by what predicate forms it makes possible, and by what the substrate cannot express without it.


## The Address-Set Projection

Shape constraints operate on a *syntactic* projection of `(F, G)` — the slot-address sets extracted from canonical-form endsets — together with an *allocated-address* projection that bridges the syntactic check to substrate semantics. Two projections matter.

**Definition — Coverage Projection.** For each tuple `(a, F, G) ∈ L_K`:

`cov : L_K → ℘(T) × ℘(T)`

`cov(a, F, G) = (coverage(F), coverage(G))`

where `coverage(·)` is the union of address sets denoted by the endset's spans (Definition, ASN-0043). By PrefixSpanCoverage (ASN-0043), the coverage of a single unit-depth span at `x` is `{t ∈ T : x ≼ t}`, which is *infinite* in `T` by T0(a)/T0(b) (ASN-0034). The set-theoretic cardinality `|coverage(F)|` is therefore infinite for every non-empty canonical-form `F`, so cardinality constraints cannot be stated against `|coverage(F)|` directly.

The address-set view is a lossy projection — by L5 (EndsetSetSemantics, ASN-0043), endsets with different span decompositions can have identical coverage. For shape purposes the loss is intentional: shapes are predicates over what addresses a slot references, not over how those addresses are denoted.

**Definition — AllocatedCoverage.** For an endset `F` and reachable state `Σ`:

`cov_allocated(F, Σ) := coverage(F) ∩ A^Σ`

where `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` is the address universe at Σ (ASN-0086). This set is finite at every Σ (since `A^Σ` is finite by L-fin and C-fin) and monotone non-decreasing along `⊑̂`: `Σ ⊑̂ Σ'` entails `cov_allocated(F, Σ) ⊆ cov_allocated(F, Σ')` because `A^Σ ⊆ A^{Σ'}` and `coverage(F)` is a pure function of the endset value.

**Definition — CanonicalSlotForm.** An endset `F` is in *canonical-slot form* iff there exists a finite set `X_F ⊆ T` such that

`F = {(x, δ(1, #x)) : x ∈ X_F}`

The elements of `X_F` are the *slot addresses* of `F`. `X_F` is uniquely recoverable from any canonical-form `F` by reading the start address of each unit-depth span; equivalently, `X_F = {s ∈ T : (E (s, ℓ) ∈ F :: ℓ = δ(1, #s))}` is a well-defined set-valued function of `F`. We write `slot_addrs(F) = X_F`.

`|slot_addrs(F)|` is a finite natural number (since `F` is a finite endset by ASN-0043's `Endset = ℘_fin(Span)`). For canonical-form `F`, `coverage(F) = (∪ x ∈ X_F : {t : x ≼ t})` — infinite in `T` when `X_F ≠ ∅`; what shape constraints check is the finite syntactic `slot_addrs(F)`.

The shape framework restricts every shape-conformant emission's `F` and `G` to canonical-slot form. The substrate as defined by ASN-0043 permits non-canonical endsets (L4); the shape framework rejects non-canonical emissions via Sh-conf below. This is a discipline imposed by the framework, not a substrate-level constraint.

**Lemma — AllocatedAddressAntichain.** For every reachable state `Σ` and every `x ∈ A^Σ`:

`cov_allocated({(x, δ(1, #x))}, Σ) = {x}`

*Proof.* `coverage({(x, δ(1, #x))}) = {t : x ≼ t}` by PrefixSpanCoverage. The intersection with `A^Σ` is `S := {a ∈ A^Σ : x ≼ a}`. By Prefix reflexivity (ASN-0034), `x ∈ S`. For the reverse, fix `a ∈ S`; we show `a = x` by case on the domains.

*Case 1* (`x, a ∈ dom(Σ.L)`): By R0a (FlatLinkDomain, ASN-0086), `dom(Σ.L)` is a tumbler-prefix antichain, so `x ≼ a ⟹ x = a`.

*Case 2* (`x, a ∈ dom(Σ.C)`): By substrate-conforming chain discipline (ASN-0093 — ChainEnumerationInjectivity, ChainUniformLength, ChainPrefixExtension, CrossDocDisjointness), content sub-allocator outputs are pairwise prefix-incomparable within each `A_C(d)` chain (same length, distinct enumeration index) and across documents (anchors `b_C(d), b_C(d')` prefix-incomparable). Hence `dom(Σ.C)` is a tumbler-prefix antichain, and `x ≼ a ⟹ x = a`.

*Case 3* (`x ∈ dom(Σ.L), a ∈ dom(Σ.C)`, or vice versa): By L1 (LinkElementLevel, ASN-0043) and ASN-0093's content-side analog, both `x` and `a` are element-level (`zeros = 3`). The prefix `x ≼ a` with both element-level forces T4b's E-projection to satisfy `E(x) ≼ E(a)`, hence `E(x).1 = E(a).1`. But L0 (SubspacePartition, ASN-0043) gives `E(x).1 = s_L` for links and ASN-0093 gives `E(a).1 = s_C` for content, with `s_L ≠ s_C` (SC-NEQ). Contradiction; this case is vacuous. ∎

The lemma underwrites the syntactic-to-semantic bridge: a canonical-slot endset at an allocated address `x` denotes exactly `{x}` among allocated addresses, so `slot_addrs(F) = {x}` matches "what allocated address does this slot refer to" with no ambiguity. Without this lemma, "the slot at `x`" could resolve to multiple allocated addresses when `x` has allocated descendants — which is precisely what the antichain rules out at element level.


## Shape

**Definition — Shape.** A *shape* is a tuple

`Σ_K = (c_F, c_G, t_F, t_G, idem)`

with components:

- `c_F, c_G ∈ {0, 1, *, 0|1}` — *cardinality bounds* on the slot-address counts `|slot_addrs(F)|` and `|slot_addrs(G)|`. The values 0 and 1 are exact; `*` denotes "any natural number"; `0|1` denotes "0 or 1 exactly."
- `t_F, t_G` — *target-domain restrictions*. Each is one of the symbolic constants `A_doc`, `A_rel`, `A`, or the distinguished value `-` (used when the corresponding cardinality is `0`). At each state Σ the symbol expands to the corresponding allocated set: `A_doc ↦ A_doc^Σ = dom(Σ.C)`, `A_rel ↦ A_rel^Σ = dom(Σ.L)`, `A ↦ A^Σ = A_doc^Σ ∪ A_rel^Σ`.
- `idem ∈ {⊤, ⊥}` — the *idempotency flag*.

**Definition — CardinalityMatch.** For `n ∈ ℕ` and `c ∈ {0, 1, *, 0|1}`:

`match(n, c) ≡ (c = 0 ∧ n = 0) ∨ (c = 1 ∧ n = 1) ∨ (c = * ∧ n ∈ ℕ) ∨ (c = 0|1 ∧ n ∈ {0, 1})`

**Definition — TypedRelationCatalog.** Fix a finite distinguished set `T_cat ⊆ T_admissible`. The catalog enumerates the typed relations the substrate admits under shape registration. By coverage-equivalence (ASN-0086, `~` definition), `T_cat` is treated up to `~`: if `K ∈ T_cat` and `K ~ K'`, then `K'` inherits `K`'s shape (equivalently, the registry operates on the quotient `T_cat / ~`).

For any `K ∈ T_admissible` whose class `[K]` is not represented in `T_cat`, no shape is registered. The substrate's shape-conformance gate rejects `Emit_K` at unregistered types (see Sh-conf below).

**Definition — ShapeRegistry.** A function

`shape : T_cat → Shape`

assigns each registered type its shape. Two properties:

- *Per-class constancy.* For `K, K' ∈ T_cat` with `K ~ K'`: `shape(K) = shape(K')`. The function `shape` factors through `T_cat / ~`.
- *Lifetime constancy.* `shape` is fixed across the substrate's lifetime; it does not change as states evolve.

Lifetime constancy is a substrate-level commitment, not derivable from R0–R7. It is what lets Sh-conf evaluate emissions against a stable shape that matches the shape under which prior tuples of the same type were emitted, so the inductive proofs of Sh0–Sh3 can rely on a fixed conformance predicate. Mutable shape re-registration (e.g., relaxing a cardinality bound after some tuples are already emitted) would invalidate the induction; the framework forbids it.

**Definition — Conformance.** A tuple `(a, F, G) ∈ L_K^Σ` (with `K ∈ T_cat`) is *shape-conformant at state Σ* iff all of the following hold:

(a) `F` is in canonical-slot form; let `X_F = slot_addrs(F)`.
(b) `G` is in canonical-slot form; let `X_G = slot_addrs(G)`.
(c) `match(|X_F|, shape(K).c_F) ∧ match(|X_G|, shape(K).c_G)`.
(d) `X_F ⊆ shape(K).t_F^Σ ∧ X_G ⊆ shape(K).t_G^Σ`, with the symbolic `t` expanded per the Shape definition. When `t_F = -` (only legal under `c_F = 0`), the F-side of (d) is vacuously satisfied since `X_F = ∅`; symmetric for G.

Write `conf_K^Σ(F, G)` for this predicate.

*State-dependence and monotone discharge.* Conformance is state-indexed because clause (d) depends on the allocated sets `A_doc^Σ, A_rel^Σ, A^Σ`. These sets grow monotonically along `⊑̂`: `Σ ⊑̂ Σ'` entails `A^Σ ⊆ A^{Σ'}` and analogous for the partition sets (by L12a, ASN-0043, for `dom(Σ.L)` and the symmetric content-side claim from ASN-0093 for `dom(Σ.C)`). Therefore `conf_K^Σ(F, G) ⟹ conf_K^{Σ'}(F, G)` for every `Σ ⊑̂ Σ'`: once conformant, a tuple remains conformant under every reachable future state. This monotonicity is what permits the inductive arguments of Sh0–Sh3 to commute with arbitrary `↦*` transitions.


## The Conformance Axiom

**Sh-conf — ShapeConformanceAxiom.** The substrate restricts ASN-0086's `Emit_K` by adding two preconditions:

`Emit_K(Σ, d, F, G)` succeeds iff `K ∈ T_cat ∧ conf_K^Σ(F, G)`. Emissions failing either conjunct are rejected before any state transition occurs.

*Justification.* This is an axiom about the substrate's enforcement, not a theorem derivable from R0–R7. R0 (TupleAddressFreshness, ASN-0086) alone permits any `(F, G, K)` triple with `K ∈ T_admissible` to be emitted at a fresh address. Sh-conf narrows the admissible triples to those whose `F, G` are in canonical-slot form, whose slot-address cardinalities match the registered shape, and whose slot addresses land in the registered target domains.

Without Sh-conf, the cardinality and target-domain consequences (Sh0–Sh3 below) would not hold across state transitions — they would be vacuously true on an empty `L_K` and immediately false after the first non-conformant emission.

*Interaction with Nullify.* `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` (ASN-0086). For Sh-conf to admit Nullify under Retraction's shape `(*, 1, A, A_rel, ⊤)`:

- `F = ∅` is canonical-slot form with `X_F = ∅`; `match(0, *)` holds; `∅ ⊆ A^Σ` trivially.
- `G = {(a, δ(1, #a))}` is canonical-slot form with `X_G = {a}`; `match(1, 1)` holds; `{a} ⊆ A_rel^Σ` holds by Nullify's P1 precondition `a ∈ A_rel^Σ`.

Sh-conf admits every well-formed Nullify call; the substrate's retraction primitive is shape-conformant by construction, with no special-case exemption needed.


## Cardinality (Sh0, Sh1)

**Sh0 — FromSlotCanonicalAndCardinalityFixed.** For each `K ∈ T_cat`, every tuple in `L_K^Σ` at every reachable state Σ has `F` in canonical-slot form with `|slot_addrs(F)|` matching `c_F`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: F is canonical-slot form ∧ match(|slot_addrs(F)|, shape(K).c_F))`

*Proof.* By induction on the broad transition relation `↦*` from the initial state `Σ_0`. Reachable states are reached under `↦*` (the broader relation including arrangement-modifying steps), not just `→*`, so the induction must cover both transition classes.

*Base case.* At `Σ_0`, every `L_K^{Σ_0} = ∅`; the universal quantifier is vacuous.

*Inductive step.* Suppose the property holds at Σ; let `Σ ↦ Σ'` be a single broad transition. Two sub-cases.

*Case A: `Σ → Σ'` is a dom-extending step (K.σ, K.α, K.λ).* K.σ and K.α leave `Σ.L` unchanged, so `L_K^{Σ'} = L_K^Σ` for every K; the property is inherited. The only sub-class affecting `dom(Σ.L)` is K.λ, which under Sh-conf succeeded only because `conf_K^Σ(F, G)` held — i.e., `F` is canonical-slot form and `match(|slot_addrs(F)|, c_F)`. The new tuple satisfies the property; existing tuples retain their values by R2 (TupleAddressPermanence, ASN-0086) and their conformance by the inductive hypothesis.

*Case B: `Σ ↦ Σ'` is an arrangement-modifying step in `↦ \ →`.* By LinkStoreInvarianceUnderArrangement (ASN-0086), `Σ'.L = Σ.L` pointwise, so `L_K^{Σ'} = L_K^Σ` for every K. The property is preserved trivially.

Both cases preserve the property; the induction closes. ∎

**Sh1 — ToSlotCanonicalAndCardinalityFixed.** Symmetric for `G`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: G is canonical-slot form ∧ match(|slot_addrs(G)|, shape(K).c_G))`

*Proof.* Symmetric to Sh0, with the same two-case induction over `↦*`. ∎

*Justification of the constraint.* Without uniform slot-cardinality per type, "the `d` in this tuple's `G`" is ambiguous when `|slot_addrs(G)|` varies — predicates that bind G's slot positions cannot be defined uniformly. Fixed cardinality lets templates parameterize on slot positions: a `(1, 1)`-shape relation has well-defined `from₁(τ)` and `to₁(τ)`; a `(0, 1)`-shape relation has only `to₁(τ)`; an `(*, 1)`-shape relation has `to₁(τ)` plus a from-set accessor returning a set.

*Consequences.*

(a) *Predicates have stable signatures.* For shape `(0, 1, -, A_doc, _)`, predicates take a single document argument: `is_K : A_doc → Bool`. For shape `(1, 1, A_doc, A_doc, _)`, predicates take an ordered pair. Signatures are determined by the shape, not by individual emissions.

(b) *Counting and aggregation are well-defined.* "How many comment-tuples target d?" is a number because `|slot_addrs(G)| = 1` (Sh1) and "targets d" has a uniform meaning across the relation.

(c) *Slot accessors are total on the relevant slots* (SlotAccessorTotality below).

(d) *Allocated-coverage matches syntactic intent.* By AllocatedAddressAntichain, for `c_F = 1` shapes with `slot_addrs(F) = {x}` and `x ∈ A^Σ`, `cov_allocated(F, Σ) = {x}` — the semantic "this slot refers to x" matches the syntactic `slot_addr(F) = x`. Sh-conf's target-domain check `X_F ⊆ t_F^Σ` requires `x ∈ A^Σ`, so the lemma's precondition is satisfied for every shape-conformant tuple.


## Target Domain (Sh2, Sh3)

**Sh2 — FromSlotTargetRestricted.** For each `K ∈ T_cat`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(F) ⊆ shape(K).t_F^Σ)`

(vacuous on the F-side when `t_F = -`, i.e., when `c_F = 0`).

*Proof.* By induction on `↦*` from `Σ_0`.

*Base case.* `L_K^{Σ_0} = ∅` vacuously.

*Inductive step.*

*Case A (`Σ → Σ'`).* K.σ and K.α do not affect `L_K`; the property is inherited on existing tuples, with monotone preservation `X_F ⊆ t_F^Σ ⟹ X_F ⊆ t_F^{Σ'}` because `t_F^Σ ⊆ t_F^{Σ'}` (allocated-set monotonicity along `→`). K.λ: the new tuple satisfies `X_F ⊆ t_F^Σ` by Sh-conf at emission, hence `X_F ⊆ t_F^{Σ'}` by monotonicity. Existing tuples retain their values by R2.

*Case B (`Σ ↦ Σ'` in `↦ \ →`).* `L_K^{Σ'} = L_K^Σ` by LinkStoreInvarianceUnderArrangement. Arrangement steps do not change `dom(Σ.C)` or `dom(Σ.L)` (they modify `Σ.M` pointwise; see ASN-0086), so `t_F^Σ = t_F^{Σ'}`. The property is preserved trivially. ∎

**Sh3 — ToSlotTargetRestricted.** Symmetric for `G`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(G) ⊆ shape(K).t_G^Σ)`

*Proof.* Symmetric to Sh2. ∎

*Retraction commutativity.* `A_K^Σ ⊆ L_K^Σ` always (R6 derivation in ASN-0086, since `nullified(Σ)` filters but never adds). Sh0–Sh3 universally quantify over `L_K^Σ`, so every tuple in `A_K^Σ` is also shape-conformant. Retraction removes a tuple from `A_K^Σ` but never introduces a non-conformant tuple. The shape predicates over `A_K^Σ` are therefore well-typed at every state, including post-retraction states. This closes the question of whether shape commutes with retraction.

*Justification of the constraint itself.* R4 (TupleAddressDisjointness, ASN-0086) gives two address kinds — `A_doc` and `A_rel` — but does not by itself constrain *which* kind appears in any given slot. Sh2/Sh3 do: each slot of each relation targets one fixed kind. Without this, the same predicate template would have to handle both document targets and tuple targets, and predicate type-checking at the slot level would fail.

*Consequences.*

(a) *Predicates are typed at the slot level.* For relations targeting documents (`t_G = A_doc`), `to₁(τ) ∈ A_doc^Σ`; for relations targeting tuples (`t_G = A_rel`, e.g. retraction, resolution), `to₁(τ) ∈ A_rel^Σ`. The codomain of `to₁` is determined by `t_G`, not by individual emissions.

(b) *Self-referential and document-targeting relations are syntactically distinguished.* A relation with `t_G = A_rel` is *about other relations*; a relation with `t_G = A_doc` is *about documents*. The active-subset machinery (R6, ASN-0086) consumes only relations with `t_G = A_rel`; document-classifier predicates consume only relations with `t_G = A_doc`.

(c) *Operational composition is mechanically checkable.* Composing two relations through their slots requires joining slots have compatible target domains. Sh2/Sh3 make compatibility decidable from the shape registry alone.


## Slot Accessors

The cardinality and target-domain lemmas together permit total slot accessor functions.

**Definition — SetSlotAccessors.** For each `K ∈ T_cat`, define at every state Σ:

`from_K^Σ : L_K^Σ → ℘_fin(shape(K).t_F^Σ)` &nbsp; with &nbsp; `from_K^Σ(a, F, G) = slot_addrs(F)`

`to_K^Σ   : L_K^Σ → ℘_fin(shape(K).t_G^Σ)` &nbsp; with &nbsp; `to_K^Σ(a, F, G) = slot_addrs(G)`

These are total on `L_K^Σ` for any shape: Sh0/Sh1 guarantee canonical-slot form (so `slot_addrs` is defined); Sh2/Sh3 restrict the codomain to the registered target domain at the current state.

**Definition — PointSlotAccessors.** For shapes with `c_F = 1`:

`from₁ : L_K^Σ → shape(K).t_F^Σ` &nbsp; with &nbsp; `from₁(τ) = the unique element of from_K^Σ(τ)`

For shapes with `c_G = 1`:

`to₁ : L_K^Σ → shape(K).t_G^Σ` &nbsp; with &nbsp; `to₁(τ) = the unique element of to_K^Σ(τ)`

For shapes with `c_F = 0|1` or `c_G = 0|1`, the partial accessor returns `⊥` (undefined) when the slot is empty:

`from₁⁻ : L_K^Σ → shape(K).t_F^Σ ∪ {⊥}` defined when `c_F ∈ {1, 0|1}`; returns `⊥` iff `|slot_addrs(F)| = 0`.

`to₁⁻` defined analogously.

**Lemma — SlotAccessorTotality.** When `shape(K).c_F = 1`, `from₁` is a total function on `L_K^Σ`. Similarly for `to₁` when `c_G = 1`.

*Proof.* By Sh0, every `τ ∈ L_K^Σ` has `F` in canonical-slot form with `|slot_addrs(F)| = 1` (since `match(n, 1) ⟺ n = 1`). A finite set of cardinality 1 has a unique element. Define `from₁(τ)` as that element. By Sh2, this element lies in `t_F^Σ`. ∎

For the rest of this document, we drop subscripts and write `from`, `to` when the shape unambiguously fixes which accessor is meant. We additionally use `addr(τ) = a` for the tuple address (R1, AddressInjectivity, ASN-0086).


## Idempotency (Sh4)

**Sh4 — IdempotencyDiscipline.** When `shape(K).idem = ⊤`, a layer above the substrate enforces at most one *active* tuple in `L_K` with any given slot-address pair:

`(A τ, τ' ∈ A_K^Σ : (slot_addrs(F)(τ), slot_addrs(G)(τ)) = (slot_addrs(F)(τ'), slot_addrs(G)(τ')) :: addr(τ) = addr(τ'))`

*Status.* Sh4 is a *layer-level discipline*, not a substrate-enforced axiom. The substrate as defined by ASN-0086 does not enforce Sh4: R0 (TupleAddressFreshness) explicitly permits two emissions with identical `(F, G)` to produce two distinct tuples; R1 (AddressInjectivity) keeps them distinguishable. Sh4 is realized by the calling layer: before emitting `(F, G)` into an idempotent relation, the layer first executes `Observe_K(coverage(F), coverage(G), A_K^Σ)`; if a match exists, the emission is suppressed.

*Conditional consumption of Sh4 by templates.* Templates that consume Sh4 — specifically `K_sidecar_of` under the Attribute shape — are well-defined only when the calling layer's Sh4 enforcement is correct. Under Sh4 violation, the candidate set `{τ ∈ A_K^Σ : from₁(τ) = d}` may contain multiple elements, and the substrate offers no canonical choice among them. Per-template specifications below state explicitly when a template's totality depends on Sh4.

A defensive alternative (presented under the Attribute walkthrough) is to expose the set-valued accessor `K_sidecars_of(d) := {τ ∈ A_K^Σ : from₁(τ) = d}` and use it where Sh4 cannot be relied on. This is well-defined unconditionally.

*Justification of the policy.* Some predicates need yes/no semantics on tuple existence: "is `d` classified as a claim?" should not be answered by counting `(∅, {d})` tuples. For idempotent relations the predicate template uses *set semantics* — the active relation is treated as a set of `(F, G)` slot-address pairs, with multiplicities collapsed. For non-idempotent relations (e.g., Comment, where each comment is a distinct event), the predicate template uses *bag semantics* — multiplicities are preserved.

*Consequences.*

(a) *Existence-vs-count distinction.* Idempotent relations support `exists_K(F, G) : Bool` predicates with stable yes/no answers (modulo Sh4 enforcement). Non-idempotent relations support `count_K(...)` predicates whose value reflects the number of distinct emission events.

(b) *Re-emit-vs-fail behavior is registry-driven.* Library helpers like `emit_attribute` consult `shape(K).idem` to decide whether to short-circuit on existing match or always allocate a fresh address. The decision is mechanical from the shape, not from inspection of K's name.

(c) *Idempotency is a property of A_K, not L_K.* By R3, `L_K` always retains every emission ever made — duplicates included. Idempotency restricts what reaches `A_K`. Once a duplicate is emitted, it stays in `L_K` for audit but the emission policy ensures only one is active at a time. Retraction-then-reemit cycles can leave multiple coverage-identical tuples in `L_K` with at most one active.


## Template Catalog (Sh5)

**Sh5 — TemplateCatalog.** For each canonical shape `Σ_canon`, the shape framework specifies a hand-curated *template family* `Tpl(Σ_canon)` of predicate forms applicable to every `K ∈ T_cat` with `shape(K) = Σ_canon`. Each template is parameterized by K's name (and, where noted, by layer-supplied auxiliary accessors); instantiation substitutes the name into the template body and yields a per-K predicate or accessor.

*Status.* Sh5 is a META observation about the framework's organizing discipline, not a mechanical-derivation theorem. The template families exhibited in the walkthroughs below are written by hand against the canonical shape catalog. The framework *does* guarantee that templates depend only on (i) the shape components (cardinality, target-domain typing, idempotency flag), (ii) K's name, and (iii) explicitly named layer-supplied accessors — never on per-K design freedom beyond those. Adding a new K with a registered shape that matches a catalog entry yields the template family for free (subject to the auxiliary accessors).

*Auxiliary accessors.* Two templates depend on data outside the substrate's relational structure:

- `K_is_fresh` (filesystem freshness, presented under Layer Composites below) consumes a layer-supplied `mtime` accessor over `A_doc`. The substrate does not provide `mtime`; layers built atop the substrate furnish it.
- `latest_K_for_addr` (Coverage shape, see walkthrough) consumes an `emission_order` total order on per-document tuple subsets. The substrate provides this *only* when the Coverage relation commits to single-home emission (see SingleHomeCoverageDiscipline below); otherwise the layer must supply its own ordering.

*What Sh5 is not.* Sh5 does not claim a procedure that, given an arbitrary shape, derives a template family. New shapes added to the catalog acquire templates by analogy with existing entries and by hand-design; the framework discipline limits design choices to those compatible with Sh0–Sh4, but it does not eliminate the design step.


## The Canonical Shape Catalog

The substrate's relations fall into a small fixed set of canonical shapes. Each canonical shape pairs with a predicate template family that is forced by the shape — there is no design freedom in template selection once the shape is fixed.

| Shape            | (c_F, c_G) | t_F   | t_G   | idem | Template family                                              |
|------------------|------------|-------|-------|------|--------------------------------------------------------------|
| Classifier       | (0, 1)     | -     | A_doc | ⊤    | `is_K(d)`                                                    |
| Tuple-Classifier | (0, 1)     | -     | A_rel | ⊤    | `is_K(τ)`                                                    |
| Attribute        | (1, 1)     | A_doc | A_doc | ⊤    | `has_K(d)`, `K_sidecar_of(d)` (cond. on Sh4), `K_sidecars_of(d)` |
| Citation         | (1, 1)     | A_doc | A_doc | ⊤    | `cites_K(a, b)`, `K_incoming(b)`                             |
| Coverage         | (1, 1)     | A_doc | A_doc | ⊥    | `latest_K_for_addr(d)` (with SingleHomeCoverageDiscipline)    |
| Comment          | (1, 1)     | A_doc | A_doc | ⊥    | `unresolved_K_comments(d)`, `all_K_resolved(d)`              |
| Resolution       | (1, 1)     | A_doc | A_rel | ⊤    | (consumed by `all_K_resolved` template at Comment shape)     |
| Retraction       | (\*, 1)    | A     | A_rel | ⊤    | (consumed by R6's active-subset definition)                  |
| Provenance       | (1, 0\|1)  | A     | A     | ⊤    | `outgoing_K(s)`                                              |

The catalog has *bipartite coverage*: for each structural pattern (cardinality + idempotency), entries with `t_G = A_doc` and `t_G = A_rel` are listed separately. Classifier and Tuple-Classifier are the two `(0, 1, -, ·, ⊤)` rows; Attribute and (a hypothetical Tuple-Attribute) would be the two `(1, 1, ·, ·, ⊤)` rows on the document/tuple axis. The current catalog enumerates the rows demanded by present-day predicate templates; further bipartite entries can be added by extending the catalog.


## Per-Shape Template Walkthroughs

We walk the canonical shapes and exhibit the predicate templates each generates.

### Classifier — `(0, 1, -, A_doc, ⊤)`

Every tuple in `L_K` has `slot_addrs(F) = ∅` (Sh0) and `slot_addrs(G) = {d}` for some `d ∈ A_doc^Σ` (Sh1, Sh3). The to-accessor `to₁(τ) ∈ A_doc^Σ` is total (SlotAccessorTotality).

`is_K(d) ≡ (E τ ∈ A_K^Σ :: to₁(τ) = d)`

A document `d` is *classified as K* iff there exists an active tuple in `L_K` whose to-slot is `d`. By Sh4 idempotency (layer-enforced), the existential is yes/no — multiple slot-identical active tuples are precluded by policy.

### Tuple-Classifier — `(0, 1, -, A_rel, ⊤)`

Structurally identical to Classifier; the only difference is the target domain. Every tuple in `L_K` has `slot_addrs(F) = ∅` and `slot_addrs(G) = {τ}` for some `τ ∈ A_rel^Σ`. The to-accessor `to₁(σ) ∈ A_rel^Σ` is total.

`is_K(τ) ≡ (E σ ∈ A_K^Σ :: to₁(σ) = τ)`

A tuple `τ` is *classified as K* iff there exists an active classifier-tuple in `L_K` whose to-slot is `τ`. The single-letter substitution `d ↝ τ` from Classifier's template body is the only difference; signature changes from `A_doc → Bool` to `A_rel → Bool`.

Tuple-Classifier admits useful predicates over substrate-internal entities — marking a comment-tuple as endorsed, marking a citation-tuple as deprecated, marking a review-tuple as clean (so `is_clean(τ)` for `τ ∈ A_rel`). By Sh3 (`t_G = A_rel`), a Tuple-Classifier tuple's to-slot targets a tuple address, distinguishing it from a Classifier whose to-slot targets a document. The two are the bipartite halves of the same `(0, 1)` shape pattern.

*Distinction from Resolution.* Resolution `(1, 1, A_doc, A_rel, ⊤)` also targets `A_rel`, but its `c_F = 1` slot requires an actor — a resolving document. Tuple-Classifier has `c_F = 0`: no actor recorded in the tuple. Use Resolution when the assertion needs an attributed asserter; use Tuple-Classifier when the assertion is a property of the targeted tuple itself, not an action upon it.

### Attribute — `(1, 1, A_doc, A_doc, ⊤)`

Tuples have form `slot_addrs(F) = {d}, slot_addrs(G) = {s}` with `d, s ∈ A_doc^Σ` — `d` the parent document, `s` its attribute sidecar.

`has_K(d)              ≡ (E τ ∈ A_K^Σ :: from₁(τ) = d)`

`K_sidecars_of(d)      ≡ {to₁(τ) : τ ∈ A_K^Σ ∧ from₁(τ) = d)}`

`K_sidecar_of(d)       ≡ to₁(τ)` &nbsp; where τ is the unique element of `{τ ∈ A_K^Σ : from₁(τ) = d}`

The first two accessors are unconditional: `has_K(d) : A_doc → Bool` and `K_sidecars_of(d) : A_doc → ℘_fin(A_doc^Σ)` are well-defined for every state Σ regardless of Sh4 enforcement.

`K_sidecar_of(d)` requires Sh4 enforcement on the candidate set `{τ ∈ A_K^Σ : from₁(τ) = d}`: under Sh4, the set is empty or singleton, so the value-returning template is well-defined (returns `⊥` on empty set, the unique element on singleton). Under Sh4 violation, the set may have multiple elements; the substrate offers no canonical choice. Layers that cannot guarantee Sh4 should use `K_sidecars_of` and disambiguate at the consumer.

### Citation — `(1, 1, A_doc, A_doc, ⊤)`

Tuples have form `slot_addrs(F) = {a}, slot_addrs(G) = {b}` with `a, b ∈ A_doc^Σ`.

`cites_K(a, b)  ≡ (E τ ∈ A_K^Σ :: from₁(τ) = a ∧ to₁(τ) = b)`

`K_incoming(b)  ≡ {from₁(τ) : τ ∈ A_K^Σ ∧ to₁(τ) = b}`

The first is Boolean — does the citation exist? The second is value-returning — the set of documents citing b through K-typed citations. Sh4 ensures `K_incoming(b)` is a set of distinct addresses, not a multiset.

### Comment — `(1, 1, A_doc, A_doc, ⊥)`

Comments are non-idempotent: each comment is a distinct event, even with identical slot-addresses. The predicate template depends on a separate Resolution relation `K_res` of Resolution shape (see below).

`unresolved_K_comments(d) ≡ {τ ∈ A_K^Σ : to₁(τ) = d ∧ ¬resolved_by(τ, K_res)}`

where `resolved_by(τ, K_res) ≡ (E ρ ∈ A_{K_res}^Σ :: to₁(ρ) = addr(τ))`.

`all_K_resolved(d) ≡ unresolved_K_comments(d) = ∅`

A comment τ is *unresolved* iff no active resolution tuple targets τ's address (R5, TupleSelfTargeting, ASN-0086, makes this targeting expressible). This template is what consumes the Resolution shape — Resolution does not generate its own template family; it is consumed here.

### Resolution — `(1, 1, A_doc, A_rel, ⊤)`

Tuples have form `slot_addrs(F) = {d}, slot_addrs(G) = {addr(σ)}` where `d ∈ A_doc^Σ` is the resolving document and `σ ∈ A_rel^Σ` is the comment-tuple being resolved. The shape generates no standalone predicate template — its purpose is to feed the Comment template above. Sh3 (`t_G = A_rel`) is what makes that consumption possible: a Resolution tuple's to-slot targets a tuple address, not a document.

### Retraction — `(\*, 1, A, A_rel, ⊤)`

Tuples have form `slot_addrs(F) ⊆ A^Σ` (any finite set, possibly empty) and `slot_addrs(G) = {addr(σ)}` for `σ ∈ A_rel^Σ` the tuple being retracted. The retraction shape is consumed by R6 (ASN-0086) directly: the active-subset definition uses `L_R`'s tuples to compute `nullified(Σ)`. No predicate template family — Retraction's role is to flip A_K membership for arbitrary K, not to host its own predicates.

The unrestricted from-slot (`c_F = *`) accommodates use cases where the retracting party is recorded in F (e.g., F's slot addresses include an agent address), as well as the bare retraction `Nullify(Σ, d_retr, a) = Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` of ASN-0086, where `F = ∅`. Both forms are canonical-slot (the bare form trivially, the attributed form when its from-slot endset is in canonical form). The shape framework rejects retractions whose from-slot uses non-canonical-form endsets, consistent with the discipline imposed across the catalog.

### Coverage — `(1, 1, A_doc, A_doc, ⊥)`

For K with this shape, multiple emissions targeting the same document `d` are expected (e.g., evolving review status). The template projects to the most recent:

`latest_K_for_addr : A_doc → A_rel^Σ ∪ {⊥}`

`latest_K_for_addr(d) ≡ argmax_{τ ∈ S_d} emission_order(τ)` &nbsp; if &nbsp; `S_d ≠ ∅`

`latest_K_for_addr(d) ≡ ⊥` &nbsp; if &nbsp; `S_d = ∅`

where `S_d = {τ ∈ A_K^Σ : to₁(τ) = d}`. The accessor is *partial*: it returns `⊥` when no Coverage tuple has yet targeted `d`. Consumers of `latest_K_for_addr` must handle the `⊥` case explicitly.

**Definition — SingleHomeCoverageDiscipline.** A registered Coverage relation `K` commits to *single-home emission* iff every emission `Emit_K(Σ, d, F, G)` for type K uses a single fixed home document `d = d_K ∈ dom(Σ.M)` across the relation's lifetime. The commitment is a per-K registration constraint, not a universal shape constraint.

*Why single-home matters for `emission_order`.* T9 (ForwardAllocation, ASN-0034) supplies a total order on outputs of a single allocator's chain — specifically, for `same_allocator(a, b) ∧ allocated_before(a, b)`, T9 gives `a < b` under T1. Tuple addresses in a Coverage relation belong to `A_L(home(τ))` sub-allocators (ASN-0093). Under SingleHomeCoverageDiscipline, every `τ` with `to₁(τ) = d` has the same `home(τ) = d_K`, hence the same `A_L(d_K)` chain; T9 orders them, and that ordering is monotone in emission time. We define:

`emission_order(τ) := the chain-index of addr(τ) within A_L(d_K)`

equivalently, the unique `n ≥ 0` with `addr(τ) = inc^n(d_K.0.s_L.1, 0)` (by ASN-0093's chain enumeration discipline). The `argmax` in `latest_K_for_addr` is then well-defined under T1.

*Without SingleHomeCoverageDiscipline:* the Coverage relation must layer-supply an `emission_order` total order on `S_d`. Sh5's mechanical-derivability claim degrades at this point; the layer carries the ordering obligation. Coverage relations that decline to commit to single-home emission must register their layer-supplied `emission_order` accessor as part of their shape contract.

Coverage is the only canonical shape that uses `idem = ⊥` *intentionally* to retain all historical states. Comment's `idem = ⊥` is incidental — comments differ in F or G even when "looking the same" in content; Coverage's `idem = ⊥` is principled — coverage tuples by design supersede each other.

### Provenance — `(1, 0|1, A, A, ⊤)`

Provenance tuples attribute one substrate event (the F-slot) to another (the G-slot). The G-slot may be empty (`c_G = 0|1`) — used to record agent attribution where the attributed event is the emission itself. Slot accessor `to₁⁻` is partial (returns `⊥` when G is empty).

`outgoing_K(s) ≡ {τ ∈ A_K^Σ : from₁(τ) = s}`

The single template returns the set of provenance tuples sourced at s. Predicates over provenance are typically composed atomically into agent-attribution and audit queries. The unrestricted target domains (`t_F = t_G = A`) reflect that provenance can attribute either document events or relational events to either kind of source.


## Layer Composites

Some predicates frequently composed by layers above the substrate are not pure substrate templates: they depend on data outside the relational structure. We catalog them here, separated from the per-shape templates, to keep Sh5's discipline honest.

### `K_is_fresh` (Attribute + filesystem)

`K_is_fresh(d) ≡ has_K(d) ∧ mtime(K_sidecar_of(d)) ≥ mtime(d)`

A composite over an Attribute-shape relation `K` together with a layer-supplied `mtime : A_doc → ℕ` accessor (filesystem modification time). The substrate's contribution is `has_K` and `K_sidecar_of` (both substrate templates, with `K_sidecar_of` conditional on Sh4 as documented above); the layer's contribution is `mtime`. The composite is well-defined whenever `has_K(d)` and Sh4 hold; under Sh4 violation, replace `K_sidecar_of(d)` with iteration over `K_sidecars_of(d)`.

This composite was previously listed under the Attribute template family. It is moved here because Sh5's mechanical-organization claim applies only to templates that depend on K's name and shape — `mtime` is a separate registered accessor, not derivable from K.


## Worked Example: K = comment

To verify the framework on a concrete instance, register `K = comment` with the Comment shape `(1, 1, A_doc, A_doc, ⊥)`. Consider states reached by the following emissions, starting from an initial state Σ_0 with two pre-allocated documents `d_1, d_2 ∈ A_doc^{Σ_0}` and a home document `home_K ∈ dom(Σ_0.M)` (single-home not required for Comment; we use one home for simplicity).

**Emission 1.** `Emit_K(Σ_0, home_K, F_1, G_1)` with `F_1 = {(d_1, δ(1, #d_1))}` (commenter is d_1) and `G_1 = {(d_2, δ(1, #d_2))}` (target is d_2). Let the result be Σ_1 with new tuple `τ_1` at address `a_1 := addr(τ_1)`.

*Sh-conf check at Σ_0.* F_1 canonical-slot, `slot_addrs(F_1) = {d_1}`, `|{d_1}| = 1`, matches `c_F = 1`. G_1 canonical-slot, `slot_addrs(G_1) = {d_2}`, `|{d_2}| = 1`, matches `c_G = 1`. `{d_1} ⊆ A_doc^{Σ_0}` (d_1 allocated) and `{d_2} ⊆ A_doc^{Σ_0}` (d_2 allocated). Admitted. ✓

**Emission 2.** `Emit_K(Σ_1, home_K, F_2, G_2)` with `F_2 = {(d_2, δ(1, #d_2))}` (commenter is d_2) and `G_2 = {(d_2, δ(1, #d_2))}` (target is d_2 again). Let the result be Σ_2 with new tuple `τ_2` at address `a_2 := addr(τ_2)`.

*Sh-conf check at Σ_1.* Symmetric to Emission 1. Admitted. ✓

**Sh0–Sh3 hold at Σ_2 by direct check.** `L_K^{Σ_2} = {τ_1, τ_2}`. Both tuples have F and G canonical-slot, slot-cardinality 1, and slot-addresses in `A_doc^{Σ_2}` (the allocated-set has not shrunk). Sh0/Sh1 give the canonical-form-and-cardinality property; Sh2/Sh3 give the target-domain inclusion. ✓

**Template evaluation at Σ_2.** Suppose no Resolution tuples have been emitted yet, so `A_{K_res}^{Σ_2} = ∅` for a co-registered Resolution relation `K_res` of shape `(1, 1, A_doc, A_rel, ⊤)`. Compute:

`A_K^{Σ_2} = L_K^{Σ_2} \ nullified(Σ_2) = {τ_1, τ_2}` (no retractions issued).

`unresolved_K_comments(d_2) = {τ ∈ A_K^{Σ_2} : to₁(τ) = d_2 ∧ ¬resolved_by(τ, K_res)}`

Both τ_1 and τ_2 have `to₁(·) = d_2`; for each, `resolved_by(τ, K_res)` requires `(E ρ ∈ A_{K_res}^{Σ_2} :: to₁(ρ) = addr(τ))`, vacuously false since `A_{K_res}^{Σ_2} = ∅`. So:

`unresolved_K_comments(d_2) = {τ_1, τ_2}`

`all_K_resolved(d_2) = false`.

**Emission 3 (resolution).** `ρ_1 := Emit_{K_res}(Σ_2, home_R, F_ρ, G_ρ)` with `F_ρ = {(d_2, δ(1, #d_2))}` (resolver) and `G_ρ = {(a_1, δ(1, #a_1))}` (resolves τ_1 via R5, TupleSelfTargeting, ASN-0086). Result Σ_3.

*Sh-conf check at Σ_2 (under K_res shape).* F_ρ canonical-slot, `slot_addrs = {d_2}`, matches `c_F = 1`, `{d_2} ⊆ A_doc^{Σ_2}`. G_ρ canonical-slot, `slot_addrs = {a_1}`, matches `c_G = 1`, `{a_1} ⊆ A_rel^{Σ_2}` (since a_1 ∈ dom(Σ.L)). Admitted. ✓

**Template evaluation at Σ_3.**

`A_{K_res}^{Σ_3} = {ρ_1}` (no nullification).

`resolved_by(τ_1, K_res) = true` (ρ_1 witnesses); `resolved_by(τ_2, K_res) = false`.

`unresolved_K_comments(d_2) = {τ_2}`

`all_K_resolved(d_2) = false` (τ_2 still unresolved).

**Emission 4 (resolution of τ_2).** Emit `ρ_2` resolving τ_2 (analogous to Emission 3 with `G = {(a_2, δ(1, #a_2))}`). Result Σ_4.

`unresolved_K_comments(d_2) = ∅`

`all_K_resolved(d_2) = true`. The flag flips as expected.

**Edge case: retraction of τ_1.** From Σ_4, issue `Nullify(Σ_4, d_retr, a_1)` producing Σ_5. By R6c (RestorationByReemission, ASN-0086), τ_1 is permanently removed from `A_K^Σ` for all future states. So:

`A_K^{Σ_5} = {τ_2}` (τ_1 nullified; τ_2 remains).

`unresolved_K_comments(d_2) = {τ ∈ A_K^{Σ_5} : to₁(τ) = d_2 ∧ ¬resolved_by(τ, K_res)} = ∅` (τ_2 still resolved by ρ_2, which is in `A_{K_res}^{Σ_5}`).

`all_K_resolved(d_2) = true`.

The framework gives stable, well-typed answers across emission and retraction events. Sh0–Sh3 are preserved inductively, template signatures match the shape registry, and the active-subset machinery composes cleanly with retraction.


## Consequences

(a) *Adding a new relation generates predicates for free.* A new K with `shape(K) = Attribute` immediately yields `has_K`, `K_sidecars_of`, and `K_sidecar_of` (the last conditional on Sh4) — no per-relation predicate code is required. The cost of a new relation is one entry in the shape registry.

(b) *Composite predicates extend within the ceiling, not beyond it.* A composite predicate combines atomic predicates through Boolean operators and quantification over `T_cat`. The expressive ceiling is set by what the canonical shapes' templates yield; composition does not raise it. Capability beyond the ceiling requires a new canonical shape, not a new relation in an existing shape. Layer composites (e.g., `K_is_fresh`) extend beyond pure substrate templates by bringing in external accessors like `mtime`; these compose atop the framework but are not part of it.

(c) *Shape misregistration is a structural error.* Registering a relation with the wrong shape produces predicates with wrong signatures or wrong semantics — the substrate cannot self-correct this. By Sh-conf, attempts to emit non-conformant tuples are rejected, but the rejection assumes the registered shape is the *correct* shape; if the registry is wrong, the substrate enforces the wrong constraint. Shape registration is part of the relation's contract.

(d) *The predicate language is bounded by the shape catalog.* "What the substrate can ask" is determined by the templates the shapes generate. Questions about content quality ("is this proof complete?", "is this description good?") are not expressible because no canonical shape's template generates them. Those are agent-time questions, not substrate questions.


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| cov | DEF | Coverage projection `L_K → ℘(T) × ℘(T)` (codomain corrected from prior draft's `℘_fin`) | introduced |
| cov_allocated | DEF | Allocated-coverage projection `(F, Σ) → coverage(F) ∩ A^Σ`; finite per Σ, monotone along `⊑̂` | introduced |
| canonical-slot form | DEF | Endset form `{(x, δ(1, #x)) : x ∈ X_F}` with extractable slot-address set | introduced |
| slot_addrs | DEF | Extraction `F ↦ X_F` for canonical-form F | introduced |
| AllocatedAddressAntichain | LEMMA | For element-level `x ∈ A^Σ`, `cov_allocated({(x, δ(1, #x))}, Σ) = {x}` | introduced |
| Σ_K | DEF | Shape: `(c_F, c_G, t_F, t_G, idem)` | introduced |
| match | DEF | Cardinality match predicate over `{0, 1, *, 0\|1}` | introduced |
| T_cat | DEF | Typed-relation catalog: distinguished `T_cat ⊆ T_admissible` up to `~` | introduced |
| shape | DEF | Shape registry `T_cat → Shape`, per-class constant, lifetime-constant | introduced |
| conf_K^Σ | DEF | State-indexed conformance predicate; monotone along `⊑̂` | introduced |
| from_K^Σ, to_K^Σ | DEF | Total set-valued slot accessors | introduced |
| from₁, to₁ | DEF | Point-valued slot accessors (defined when c = 1) | introduced |
| from₁⁻, to₁⁻ | DEF | Optional point-valued slot accessors (defined when c = 0\|1) | introduced |
| Sh-conf | AXIOM | ShapeConformanceAxiom — Emit_K rejects unregistered types and non-conformant emissions | introduced |
| Sh0 | LEMMA | FromSlotCanonicalAndCardinalityFixed — proof covers both `→` and `↦ \ →` | introduced |
| Sh1 | LEMMA | ToSlotCanonicalAndCardinalityFixed — symmetric to Sh0 | introduced |
| Sh2 | LEMMA | FromSlotTargetRestricted — `slot_addrs(F) ⊆ t_F^Σ` on every tuple | introduced |
| Sh3 | LEMMA | ToSlotTargetRestricted — symmetric to Sh2; commutes with retraction (`A_K ⊆ L_K`) | introduced |
| SlotAccessorTotality | LEMMA | When `c = 1`, the point accessor is a total function | introduced |
| Sh4 | META | IdempotencyDiscipline — at-most-one active duplicate when `idem = ⊤`; layer policy, not substrate axiom | introduced |
| Sh5 | META | TemplateCatalog — hand-curated per-shape template families; mechanical-derivation downgraded from prior LEMMA claim | introduced |
| SingleHomeCoverageDiscipline | DEF | Per-K commitment securing `emission_order` for Coverage relations | introduced |
| Tpl | DEF | Map from canonical shape to its predicate template family | introduced |


## Open Questions

- Should `(0, 0)` shapes be admitted? A relation with `c_F = c_G = 0` would be a single-tuple existence flag whose only role is "this event happened" without any from/to attribution; whether the substrate has any such relations is unclear, and the slot accessors degenerate to constants on it.
- Provenance's `c_G = 0|1` mixes shapes — should it be split into two distinct canonical shapes (Provenance-with-target and Provenance-attribution-only), each generating separate templates? The current formulation requires the optional accessor `to₁⁻` to handle both cases in a single template.
- Is idempotency recoverable from cardinality plus target-domain alone, or is it an independent axis? Empirically the canonical catalog has both `idem = ⊤` and `idem = ⊥` for shapes with identical (cardinality, target-domain) — Comment vs. Citation, both `(1, 1, A_doc, A_doc, _)` — suggesting independence.
- The shape constraint `slot_addrs(F) ⊆ t_F^Σ` requires slot addresses to be already-allocated at emission time. This precludes shape-conformant emissions whose slot addresses are *ghost* (currently outside `A^Σ`, possibly to be allocated later). L9 (TypeGhostPermission, ASN-0043) permits ghost spans in endsets; the shape framework restricts this to *non-slot* uses only. Whether future shape families should admit ghost-targeting slot semantics — and under what state-dependent conformance rule — is an open design question.
- Do *composite shapes* (relations whose F or G is itself constrained by another relation's content) require a new restriction axis, or do they decompose into existing primitives plus auxiliary predicates expressible in the current template language?
- What guarantees the shape registry stays consistent across processes? Lifetime constancy is asserted as a substrate-level commitment within a single process; cross-process consistency (e.g., concurrent shape re-registration in a distributed substrate) is not addressed.
