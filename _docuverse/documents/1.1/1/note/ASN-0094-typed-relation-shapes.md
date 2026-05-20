# ASN-0094: Typed Relation Shapes

*Restricting the relational primitive into a predicate language.*

ASN-0086 establishes typed relations `L_K` with the three operations Emit, Observe, Nullify, governed by R0–R7. The relational structure as defined there is too permissive to support a typed predicate vocabulary: F and G can be any finite endsets whose coverage lies anywhere in `T`, so a predicate over `L_K` has no fixed signature. Every predicate would have to take a pattern in `℘(T) × ℘(T)` and return Bool, "two relations of the same shape" would not be expressible, and slot accessors `from(τ)`, `to(τ)` would be partial in a way that defeats type-checking.

We are looking for the minimum additional layer that closes this gap. The answer is a single structural decision per type: each `K ∈ T_cat` is assigned a *shape* — a tuple of constraints on cardinality, target domain, and idempotency — and the substrate enforces shape-conformance at Emit time. From the shape, a predicate template family is mechanically organized (though not mechanically derived; see Sh5). The pipeline is:

> R0–R7 (typed relations + operations) → **shape restrictions** (this document) → predicate template families → composed predicates

Shapes are not derivable from R0–R7. They are an additional design decision the substrate makes about which relations it admits and what `(F, G)` pairs each admits. We justify each constraint by what predicate forms it makes possible, and by what the substrate cannot express without it.


## Scope and Substrate Scaffolding

*Arity scope.* This framework restricts the standard-triple slice `L^Σ` of `dom(Σ.L)` — the arity-3 links collected by ASN-0086's `L^Σ` definition. Higher-arity links admitted by L3 (ASN-0043) are outside its scope: the cardinality and target-domain shape components are defined over two slots only (F and G), and the slot-accessor and template machinery presupposes the arity-3 structure. Extending the framework to higher arities would require additional shape components per extra slot, which we do not pursue here.

*Layer commitment.* The framework is a discipline imposed by a relational layer atop ASN-0086. Every class-(iii) emission of a type `K ∈ T_cat` is committed to route through `Emit_K`; non-`Emit_K` class-(iii) invocations of these types are outside the framework's scope. Sh-conf below binds `Emit_K` (the relational-layer operation), not K.λ (the substrate primitive — K.λ remains permissive at the substrate level: any `F, G ∈ Endset` with `K ∈ T_admissible` is admissible to K.λ). The inductive arguments for Sh0–Sh3 invoke this layer commitment to conclude that every new tuple in `L_K^Σ` for `K ∈ T_cat` arrived via an `Emit_K` call subject to Sh-conf.

*Content-side scaffolding.* The framework operates atop a *substrate-conforming layer* (ASN-0086, Definition). Where the framework's proofs and definitions require properties of `dom(Σ.C)` not derivable from ASN-0034/ASN-0043/ASN-0086 alone, they consume them through the substrate-conforming-layer interface. The properties consumed:

- *Element-level content addresses.* Every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3` and `#E(a) ≥ 2`. (Content-side analog of L1 and L1b from ASN-0043.)
- *Content subspace partition.* There is a fixed subspace identifier `s_C ∈ ℕ` with `s_C ≠ s_L` such that `E(a).1 = s_C` for every `a ∈ dom(Σ.C)`. (Symmetric to L0 from ASN-0043, with `s_C ≠ s_L` distinct.)
- *Content-store antichain.* `dom(Σ.C)` is a tumbler-prefix antichain at every reachable state: `(A a, a' ∈ dom(Σ.C) :: a ≼ a' ⟹ a = a')`. (Content-side symmetric to R0a from ASN-0086.)
- *Content-store monotonicity.* `dom(Σ.C) ⊆ dom(Σ'.C)` for every transition `Σ ↦ Σ'`. (Content-side symmetric to L12a from ASN-0043; content addresses are never deallocated.)
- *Per-document link sub-allocator chains.* For each `d ∈ dom(Σ.M)` the substrate-conforming layer supplies a link sub-allocator whose output chain enumerates `{ℓ : home(ℓ) = d}` under T9 (ForwardAllocation, ASN-0034); this is the same chain enumeration referenced by ASN-0086's R0a-Cor1 and FreshEmissionAddress.

We refer to these collectively as *the content-side scaffolding* and cite them by name in proofs below.


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

*Case 2* (`x, a ∈ dom(Σ.C)`): By the content-store antichain assumption (Scope and Substrate Scaffolding above), `dom(Σ.C)` is a tumbler-prefix antichain, so `x ≼ a ⟹ x = a`.

*Case 3* (`x` and `a` lie in different domains). WLOG `x ∈ dom(Σ.L), a ∈ dom(Σ.C)`; the symmetric sub-case `x ∈ dom(Σ.C), a ∈ dom(Σ.L)` follows by swapping the roles of `x` and `a` (the argument below uses only that one side carries `s_L` and the other `s_C`, with `s_L ≠ s_C` symmetric). By L1 (LinkElementLevel, ASN-0043) and the element-level content-address assumption, both `x` and `a` are element-level (`zeros = 3`); by L1b (ASN-0043) and the content-side analog `#E(·) ≥ 2`, both have a well-defined first element-field component. The prefix `x ≼ a` with both element-level forces T4b's E-projection to satisfy `E(x) ≼ E(a)`, hence `E(x).1 = E(a).1`. But L0 (SubspacePartition, ASN-0043) gives `E(x).1 = s_L` for links and the content subspace partition assumption gives `E(a).1 = s_C`, with `s_L ≠ s_C`. Contradiction. In the swapped sub-case, `E(x).1 = s_C` and `E(a).1 = s_L` instead, but `s_C ≠ s_L` is symmetric and yields the same contradiction. Both sub-cases vacuous. ∎

The lemma underwrites the syntactic-to-semantic bridge: a canonical-slot endset at an allocated address `x` denotes exactly `{x}` among allocated addresses, so `slot_addrs(F) = {x}` matches "what allocated address does this slot refer to" with no ambiguity. Without this lemma, "the slot at `x`" could resolve to multiple allocated addresses when `x` has allocated descendants — which is precisely what the antichain rules out at element level.


## Shape

**Definition — Shape.** A *shape* is a tuple

`Sh_K = (c_F, c_G, t_F, t_G, idem)`

with components:

- `c_F, c_G ∈ {0, 1, *, 0|1}` — *cardinality bounds* on the slot-address counts `|slot_addrs(F)|` and `|slot_addrs(G)|`. The values 0 and 1 are exact; `*` denotes "any natural number"; `0|1` denotes "0 or 1 exactly."
- `t_F, t_G` — *target-domain restrictions*. Each is one of the symbolic constants `A_doc`, `A_rel`, `A`, or the distinguished value `-` (used when the corresponding cardinality is `0`). At each state Σ the symbol expands to the corresponding allocated set: `A_doc ↦ A_doc^Σ = dom(Σ.C)`, `A_rel ↦ A_rel^Σ = dom(Σ.L)`, `A ↦ A^Σ = A_doc^Σ ∪ A_rel^Σ`, `- ↦ -^Σ = ∅` (the empty set, used only when the corresponding cardinality is `0`, in which case `X_F ⊆ ∅ ⟺ X_F = ∅`, which holds by `c_F = 0`).
- `idem ∈ {⊤, ⊥}` — the *idempotency flag*.

**Definition — CardinalityMatch.** For `n ∈ ℕ` and `c ∈ {0, 1, *, 0|1}`:

`match(n, c) ≡ (c = 0 ∧ n = 0) ∨ (c = 1 ∧ n = 1) ∨ (c = * ∧ n ∈ ℕ) ∨ (c = 0|1 ∧ n ∈ {0, 1})`

**Definition — TypedRelationCatalog.** Fix a finite distinguished set `T_cat ⊆ T_admissible` that is *closed under coverage-equivalence* (ASN-0086, `~` definition): `K ∈ T_cat ∧ K ~ K' ⟹ K' ∈ T_cat`. Equivalently, `T_cat` is a union of `~`-equivalence classes; concretely it is specified by listing one representative per class, with closure under `~` implicit.

For any `K ∈ T_admissible \ T_cat` (equivalently, every member of every class not represented), no shape is registered. The substrate's shape-conformance gate rejects `Emit_K` at unregistered types — the literal membership test `K ∈ T_cat` (see Sh-conf below).

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

*State-dependence and monotone discharge.* Conformance is state-indexed because clause (d) depends on the allocated sets `A_doc^Σ, A_rel^Σ, A^Σ`. These sets grow monotonically along `⊑̂`: `Σ ⊑̂ Σ'` entails `A^Σ ⊆ A^{Σ'}` and analogous for the partition sets (by L12a, ASN-0043, for `dom(Σ.L)` and by the content-store monotonicity scaffolding assumption (Scope and Substrate Scaffolding) for `dom(Σ.C)`). Therefore `conf_K^Σ(F, G) ⟹ conf_K^{Σ'}(F, G)` for every `Σ ⊑̂ Σ'`: once conformant, a tuple remains conformant under every reachable future state. This monotonicity is what permits the inductive arguments of Sh0–Sh3 to commute with arbitrary `↦*` transitions.


## The Conformance Axiom

**Sh-conf — ShapeConformanceAxiom.** The framework restricts ASN-0086's `Emit_K` (the relational-layer operation) by adding two preconditions:

`Emit_K(Σ, d, F, G)` succeeds iff `K ∈ T_cat ∧ conf_K^Σ(F, G)`. Emissions failing either conjunct are rejected before any state transition occurs.

*Scope.* Sh-conf binds `Emit_K`, not the substrate primitive K.λ. K.λ remains permissive at the substrate level: ASN-0086's R0 admits any `(F, G, K)` triple with `K ∈ T_admissible` at a fresh K.λ-emitted address. The framework's discipline is realized through the layer commitment of Scope and Substrate Scaffolding: every class-(iii) emission of a type `K ∈ T_cat` routes through `Emit_K`, and Sh-conf rejects non-conformant `Emit_K` calls before they reach K.λ. The inductive proofs of Sh0–Sh3 invoke the layer commitment to conclude that every new tuple in `L_K^{Σ'}` for `K ∈ T_cat` arrived via an `Emit_K` call subject to Sh-conf.

*Justification.* This is an axiom about the framework's layer-level enforcement, not a theorem derivable from R0–R7. R0 (TupleAddressFreshness, ASN-0086) alone permits any `(F, G, K)` triple with `K ∈ T_admissible` to be emitted at a fresh address. Sh-conf narrows the admissible triples — those traveling through `Emit_K` — to those whose `F, G` are in canonical-slot form, whose slot-address cardinalities match the registered shape, and whose slot addresses land in the registered target domains.

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

*Inductive step.* Suppose the property holds at Σ; let `Σ ↦ Σ'` be a single broad transition. We fix a particular `K ∈ T_cat` and split on whether the step affects `L_K`.

*Case A: `L_K^{Σ'} = L_K^Σ`.* The relation `L_K` is unchanged. The property is inherited tuple-by-tuple from the IH; existing tuples retain their values by R2 (TupleAddressPermanence, ASN-0086). This case covers all K.σ-steps and K.α-steps (which preserve `Σ.L` pointwise, hence `L_K` for every K, including this K); all K.λ-steps emitting a tuple of type `K'` not coverage-equivalent to K (since `L_K` slices only addresses whose stored type satisfies `coverage(e₃) = coverage(K)`); and all arrangement-modifying steps in `↦ \ →` (by LinkStoreInvarianceUnderArrangement, ASN-0086).

*Case B: `L_K^{Σ'} = L_K^Σ ∪ {τ_new}` for a single new tuple.* By the layer commitment (Scope and Substrate Scaffolding), this is a K.λ-step originating as an `Emit_K` call at type K (or a K'-typed call with `K ~ K'`; by T_cat's `~`-closure, `K' ∈ T_cat`, and `Emit_{K'}` consults `shape(K') = shape(K)` by `~`-constancy). Sh-conf admitted that call only because `conf_K^Σ(F, G)` held — i.e., `F` is canonical-slot form and `match(|slot_addrs(F)|, c_F)`. The new tuple satisfies the property; existing tuples retain their values by R2 and their conformance by the IH.

Both cases preserve the property at the chosen K; quantifying over K closes the induction. ∎

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

*Proof.* By induction on `↦*` from `Σ_0`. Fix `K ∈ T_cat` and split on whether the step affects `L_K`.

*Base case.* `L_K^{Σ_0} = ∅` vacuously.

*Inductive step.*

*Case A: `L_K^{Σ'} = L_K^Σ`.* `L_K` is unchanged. The property is inherited on every existing tuple, with monotone preservation `X_F ⊆ t_F^Σ ⟹ X_F ⊆ t_F^{Σ'}` because `t_F^Σ ⊆ t_F^{Σ'}` (allocated-set monotonicity: link-side from L12a ASN-0043, content-side from the scaffolding assumption; arrangement steps preserve `dom(Σ.C)` and `dom(Σ.L)` so the inclusion is equality there). This case covers K.σ-steps, K.α-steps, K.λ-steps for non-K-coverage-equivalent types, and arrangement-modifying steps in `↦ \ →` (via LinkStoreInvarianceUnderArrangement).

*Case B: `L_K^{Σ'} = L_K^Σ ∪ {τ_new}`.* By the layer commitment, the K.λ-step originates as an `Emit_K`-class call (at K or a `~`-equivalent type by T_cat's `~`-closure) subject to Sh-conf; the new tuple satisfies `X_F ⊆ t_F^Σ` by Sh-conf at emission, hence `X_F ⊆ t_F^{Σ'}` by monotonicity. Existing tuples retain their values by R2 and their target-domain conformance by the IH plus monotonicity. ∎

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

**Sh4 — IdempotencyDiscipline.** When `shape(K).idem = ⊤`, a layer above the substrate enforces at most one *active* tuple in `L_K` with any given slot-address pair. For `τ = (a, F, G) ∈ L_K^Σ` we write `F_τ := F` and `G_τ := G` for the slot endsets of τ. Then:

`(A τ, τ' ∈ A_K^Σ : (slot_addrs(F_τ), slot_addrs(G_τ)) = (slot_addrs(F_{τ'}), slot_addrs(G_{τ'})) :: addr(τ) = addr(τ'))`

*Layer-discipline contract.* Sh4 is realized through a contract the calling layer commits to honor uniformly across every reachable state. For each `K ∈ T_cat` with `shape(K).idem = ⊤`, on every `Emit_K(Σ, d, F, G)` call site the layer enforces the following protocol:

(i) Before issuing the emission, the layer computes the candidate set
`C(F, G, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)}`
via `Observe_K(coverage(F), coverage(G), oper)` filtered to canonical-form matches.

(ii) If `C(F, G, Σ) ≠ ∅`, the emission is *suppressed*: no `→`-step occurs.

(iii) Only if `C(F, G, Σ) = ∅` does the layer issue `Emit_K(Σ, d, F, G)`.

The layer commits to executing clauses (i)–(iii) atomically with respect to other Sh4-emitters at the same K — concurrent emission and retraction events that could split (i)'s observation from (iii)'s emission must be serialized by the layer.

*Preservation under the contract.* Sh4 holds at every reachable state under the contract, by induction on `↦*`. Fix `K ∈ T_cat` with `shape(K).idem = ⊤`.

*Base.* At `Σ_0`, `L_K^{Σ_0} = A_K^{Σ_0} = ∅`; Sh4's universal is vacuous.

*Step (Case A: `A_K^{Σ'} = A_K^Σ`).* The active subset is unchanged at K. Sh4 is inherited directly. This case covers all K.σ-steps, K.α-steps, K.λ-steps emitting a tuple of any type `K'` with `K' ≁ K` and `K' ≁ R` (so `L_K` and `nullified` are both untouched at K), and all arrangement-modifying steps in `↦ \ →` (by LinkStoreInvarianceUnderArrangement, `Σ'.L = Σ.L` pointwise hence `L_K^{Σ'} = L_K^Σ`, `L_R^{Σ'} = L_R^Σ`, and `nullified(Σ') = nullified(Σ)`).

*Step (Case B: `A_K^{Σ'} = A_K^Σ ∪ {τ_new}`, a K.λ-step at type K).* By the layer commitment, this K.λ-step originates as an `Emit_K` call (with K or `~`-equivalent registered type). By contract clause (iii), the emission proceeded only because `C(F, G, Σ) = ∅`. Let `τ_new` be the new tuple. Suppose, toward contradiction, that some prior `τ ∈ A_K^Σ` satisfies `(slot_addrs(F_τ), slot_addrs(G_τ)) = (slot_addrs(F_{τ_new}), slot_addrs(G_{τ_new}))`. Then by definition `τ ∈ C(F, G, Σ)`, contradicting `C(F, G, Σ) = ∅`. So no such `τ` exists, and `A_K^{Σ'}` extends with a slot-pair-unique element. The pairwise condition is preserved: existing pairs were Sh4-distinct by IH; `τ_new` shares no slot-pair with any prior active tuple.

*Step (Case C: `A_K^{Σ'} ⊆ A_K^Σ` strictly, an `Emit_R`-step nullifying one or more K-tuple addresses).* Retraction filters `A_K^Σ` by `nullified(Σ)` membership but cannot introduce new K-tuples; the pairwise condition is preserved on any subset.

The induction closes. ∎

*Status.* Sh4 is a *theorem under the layer-discipline contract*, not a substrate-enforced axiom. The substrate as defined by ASN-0086 does not enforce Sh4 directly: R0 (TupleAddressFreshness) explicitly permits two emissions with identical `(F, G)` to produce two distinct tuples; R1 (AddressInjectivity) keeps them distinguishable. Without the layer contract, the substrate would admit such emissions and Sh4 would fail. The framework's Sh4 conclusion depends on the layer's protocol fidelity.

*Failure modes under contract violation.* If the layer breaks any of clauses (i)–(iii) at any emission site — forgetting to observe, racing with concurrent emitters, or admitting an emission whose `C(F, G, Σ) ≠ ∅` — Sh4 may fail at the resulting state. Templates that consume Sh4 (specifically `K_sidecar_of` under the Attribute shape) become undefined on the candidate set when it contains multiple elements. Per-template specifications below state explicitly when a template's totality depends on Sh4.

A defensive alternative (presented under the Attribute walkthrough) is to expose the set-valued accessor `K_sidecars_of(d) := {τ ∈ A_K^Σ : from₁(τ) = d}` and use it where Sh4 cannot be relied on. This is well-defined unconditionally.

*Why a layer-level contract rather than a substrate-level axiom.* Lifting Sh4 into Sh-conf as an `Emit_K`-precondition (e.g., "reject `Emit_K` when `shape(K).idem = ⊤ ∧ C(F, G, Σ) ≠ ∅`") is technically feasible but conflicts with the substrate's design intent. Type semantics in ASN-0086 are by address identity, not by content-equivalence policy; substrate-level idempotency enforcement would require the substrate to commit to a duplicate-detection semantics (set vs. multiset, exact vs. coverage-equivalent) and would couple the substrate to a particular Observe-time-of-emit transactional discipline. Keeping Sh4 at the layer separates the substrate's address-permanence guarantee from the layer's idempotency policy: layers may adopt set-semantics idempotency for some K and bag-semantics for others, with the substrate uniformly admitting all emissions and the framework's templates consuming whichever discipline the layer commits to.

*Justification of the policy.* Some predicates need yes/no semantics on tuple existence: "is `d` classified as a claim?" should not be answered by counting `(∅, {d})` tuples. `A_K` is always a set of distinct-address tuples (R1, AddressInjectivity, ASN-0086); what differs across `idem` is whether `(slot_addrs(F_τ), slot_addrs(G_τ))`-pair duplicates can persist in `A_K`. Under Sh4 (idem = ⊤), the layer contract collapses such duplicates at Emit time, so `A_K` carries at most one active tuple per slot-pair: existence-vs-count distinctions are well-defined as Boolean tests. Under idem = ⊥, multiple distinct-address tuples may share a slot-pair (e.g., two Comment tuples with identical commenter/target reflecting two distinct events); predicates that count or enumerate the slot-pair multiplicity are meaningful precisely because the active subset retains those distinctions.

*Consequences.*

(a) *Existence-vs-count distinction.* Idempotent relations support `exists_K(F, G) : Bool` predicates with stable yes/no answers under the contract. Non-idempotent relations support `count_K(...)` predicates whose value reflects the number of distinct emission events.

(b) *Re-emit-vs-fail behavior is registry-driven.* Library helpers like `emit_attribute` consult `shape(K).idem` to decide whether to short-circuit on existing match or always allocate a fresh address. The decision is mechanical from the shape, not from inspection of K's name.

(c) *Idempotency is a property of A_K, not L_K.* By R3, `L_K` always retains every emission ever made — including any duplicates that may exist if the contract was ever violated. The contract restricts what reaches `A_K`. Under correct contract enforcement, once a duplicate would be emitted, the layer suppresses it. The audit slice `L_K` retains historical state regardless: retraction-then-reemit cycles can leave multiple coverage-identical tuples in `L_K` with at most one active.


## Template Catalog (Sh5)

**Sh5 — TemplateCatalog.** For each canonical shape `Sh_canon`, the shape framework specifies a hand-curated *template family* of predicate forms applicable to every `K ∈ T_cat` with `shape(K) = Sh_canon`. Each template is parameterized by K's name (and, where noted, by layer-supplied auxiliary accessors); instantiation substitutes the name into the template body and yields a per-K predicate or accessor. The families are written by hand against the canonical shape catalog (Sh5 is META), not assembled into a single function over an explicit codomain.

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
| Comment          | (1, 1)     | A_doc | A_doc | ⊥    | `unresolved_K_comments_via(K_res, d)`, `all_K_resolved_via(K_res, d)` |
| Resolution       | (1, 1)     | A_doc | A_rel | ⊤    | (consumed parametrically by Comment's `_via` templates)      |
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

Comments are non-idempotent: each comment is a distinct event, even with identical slot-addresses. The Comment shape generates a template family parameterized by a *resolver-type argument* `K_res` of Resolution shape — Comment relations do not co-register a particular resolver in the shape registry. The framework treats any active `K_res`-typed tuple targeting τ's address as resolving τ, regardless of provenance: there is no notion of "the K_res paired with K"; the layer chooses which Resolution-shaped relation to consult when querying resolution status.

`unresolved_K_comments_via(K_res, d) ≡ {τ ∈ A_K^Σ : to₁(τ) = d ∧ ¬resolved_by(τ, K_res)}`

where `resolved_by(τ, K_res) ≡ (E ρ ∈ A_{K_res}^Σ :: to₁(ρ) = addr(τ))`.

`all_K_resolved_via(K_res, d) ≡ unresolved_K_comments_via(K_res, d) = ∅`

A comment τ is *unresolved with respect to K_res* iff no active `K_res`-tuple targets τ's address (R5, TupleSelfTargeting, ASN-0086, makes this targeting expressible). The template signature includes `K_res` explicitly because the framework imposes no co-registration between Comment relations and their resolvers: different layers may resolve the same comment relation under different `K_res`, and the predicate is well-defined parametrically across that choice.

The semantics are deliberately permissive — *any* active `K_res`-tuple targeting τ counts as a resolution, modulo whatever additional filtering the calling layer applies via its choice of `K_res`. This matches the substrate's open-ended type discipline: typed relations are claims surfaced for layer-level evaluation, not assertions adjudicated by the substrate.

*Layer-level aliasing convention.* When a calling layer commits to a single canonical resolver `K_res_canonical` for `K` (a layer convention, not a framework-level registration), it may define an alias `unresolved_K_comments(d) := unresolved_K_comments_via(K_res_canonical, d)`. This alias is a layer construct and is not part of the shape framework's template family.

This is the template that consumes the Resolution shape — Resolution does not generate its own template family; it is consumed parametrically here.

### Resolution — `(1, 1, A_doc, A_rel, ⊤)`

Tuples have form `slot_addrs(F) = {d}, slot_addrs(G) = {addr(σ)}` where `d ∈ A_doc^Σ` is the resolving document and `σ ∈ A_rel^Σ` is the comment-tuple being resolved. The shape generates no standalone predicate template — its purpose is to be consumed parametrically by Comment's `unresolved_K_comments_via` / `all_K_resolved_via` templates as the `K_res` argument. Sh3 (`t_G = A_rel`) is what makes that consumption possible: a Resolution tuple's to-slot targets a tuple address, not a document.

### Retraction — `(\*, 1, A, A_rel, ⊤)`

Tuples have form `slot_addrs(F) ⊆ A^Σ` (any finite set, possibly empty) and `slot_addrs(G) = {addr(σ)}` for `σ ∈ A_rel^Σ` the tuple being retracted. The retraction shape is consumed by R6 (ASN-0086) directly: the active-subset definition uses `L_R`'s tuples to compute `nullified(Σ)`. No predicate template family — Retraction's role is to flip A_K membership for arbitrary K, not to host its own predicates.

The unrestricted from-slot (`c_F = *`) accommodates use cases where the retracting party is recorded in F (e.g., F's slot addresses include an agent address), as well as the bare retraction `Nullify(Σ, d_retr, a) = Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` of ASN-0086, where `F = ∅`. Both forms are canonical-slot (the bare form trivially, the attributed form when its from-slot endset is in canonical form). The shape framework rejects retractions whose from-slot uses non-canonical-form endsets, consistent with the discipline imposed across the catalog.

### Coverage — `(1, 1, A_doc, A_doc, ⊥)`

Coverage tuples assert that a witnessing document covers (reviews, revises, evaluates) a target document. The from-slot identifies the *witness/asserter* — the document making the coverage claim (e.g., a review document, a revision document). The to-slot identifies the *subject* — the document being covered. The framework requires `c_F = 1` rather than `c_F = 0` because Coverage relations carry directional provenance: knowing *which* document witnessed a coverage event is constitutive of the assertion, not auxiliary metadata. A Coverage relation without an attributed witness would not be a coverage assertion at all; it would be an unattributed flag, which the Classifier shape `(0, 1)` already covers. The `(1, 1)` shape encodes the witness-to-subject directionality intrinsic to coverage semantics.

For K with this shape, multiple emissions targeting the same subject `d` are expected (e.g., evolving review status from the same or successive witnesses). The template projects to the most recent:

`latest_K_for_addr : A_doc → A_rel^Σ ∪ {⊥}`

`latest_K_for_addr(d) ≡ argmax_{τ ∈ S_d} emission_order(τ)` &nbsp; if &nbsp; `S_d ≠ ∅`

`latest_K_for_addr(d) ≡ ⊥` &nbsp; if &nbsp; `S_d = ∅`

where `S_d = {τ ∈ A_K^Σ : to₁(τ) = d}` ranges over all active Coverage tuples targeting `d`, regardless of which witness `from₁(τ)` they originate from. The template's signature is indexed by the subject alone because "the latest assertion about `d`" is a function of `d`'s coverage-event history; the from-slot is consulted by the *consumer* of `latest_K_for_addr(d)` (which can read `from₁` off the returned tuple to recover the witness), not by the template's projection itself. The accessor is *partial*: it returns `⊥` when no Coverage tuple has yet targeted `d`. Consumers of `latest_K_for_addr` must handle the `⊥` case explicitly.

**Definition — SingleHomeCoverageDiscipline.** A registered Coverage relation `K` commits to *single-home emission* iff every emission `Emit_K(Σ, d, F, G)` for type K uses a single fixed home document `d = d_K ∈ dom(Σ.M)` across the relation's lifetime. The commitment is a per-K registration constraint, not a universal shape constraint.

*Why single-home matters for `emission_order`.* T9 (ForwardAllocation, ASN-0034) supplies a total order on outputs of a single allocator's chain — specifically, for `same_allocator(a, b) ∧ allocated_before(a, b)`, T9 gives `a < b` under T1. Tuple addresses in a Coverage relation belong to per-document link sub-allocators (the substrate-conforming layer's link-side chain enumeration referenced by Scope and Substrate Scaffolding; ASN-0086 R0a-Cor1 and FreshEmissionAddress consume this same enumeration). Under SingleHomeCoverageDiscipline, every `τ` with `to₁(τ) = d` has the same `home(τ) = d_K`, hence the same link sub-allocator chain. We define:

`emission_order(τ) := the chain-index of addr(τ) within the link sub-allocator chain at d_K`

equivalently, the unique `n ≥ 0` with `addr(τ) = inc^n(d_K.0.s_L.1, 0)` (by the substrate-conforming layer's chain enumeration discipline; cf. ASN-0086's FreshEmissionAddress).

*Why the `argmax` in `latest_K_for_addr` is well-defined under T1.* Three ingredients:

(i) `S_d` is finite at every reachable Σ. `S_d ⊆ A_K^Σ ⊆ L_K^Σ ⊆ dom(Σ.L)`, and `dom(Σ.L)` is finite by L-fin (ASN-0043).

(ii) The chain-index map `τ ↦ emission_order(τ)` is injective on `S_d`. Under SingleHomeCoverageDiscipline every `τ ∈ S_d` has `home(τ) = d_K`, so by ChainMembershipForOrigin (ASN-0093) every such `addr(τ)` lies in `A_L(d_K)`'s enumeration; by T10a.7 (EnumerationInjectivity, ASN-0034) the chain index is the unique `n` with `addr(τ) = inc^n(d_K.0.s_L.1, 0)`, so distinct `τ, τ'` with distinct addresses (R1, AddressInjectivity, ASN-0086) have distinct chain indices.

(iii) Chain-index order coincides with T1-order on the chain. By T9, within `A_L(d_K)`'s chain, `allocated_before(a, b) ⟹ a < b` under T1; combined with T10a.7's enumeration `tₙ₊₁ = inc(tₙ, 0)` and TA5(a)'s strict-increase under `inc(·, 0)`, the chain-index ordering on `A_L(d_K)` is strictly increasing under T1. Hence `argmax_{τ ∈ S_d} emission_order(τ)` selects the same unique element whether the ordering is read off chain-indices or off T1 — namely the τ of maximal chain-index in `S_d` (well-defined because `S_d` is finite and chain-indices are totally ordered on ℕ).

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

**Sh0–Sh3 hold at Σ_2 by direct check.** `L_K^{Σ_2} = {τ_1, τ_2}`. Per-tuple verification:

- *τ_1:* `slot_addrs(F_1) = {d_1}`, `|{d_1}| = 1`, `match(1, c_F = 1)` ✓ (Sh0); `slot_addrs(G_1) = {d_2}`, `|{d_2}| = 1`, `match(1, c_G = 1)` ✓ (Sh1); `{d_1} ⊆ A_doc^{Σ_2}` ✓ (Sh2, `d_1` is allocated since `d_1 ∈ A_doc^{Σ_0} ⊆ A_doc^{Σ_2}` by allocated-set monotonicity); `{d_2} ⊆ A_doc^{Σ_2}` ✓ (Sh3, same).
- *τ_2:* `slot_addrs(F_2) = {d_2}`, `|{d_2}| = 1`, `match(1, c_F = 1)` ✓ (Sh0); `slot_addrs(G_2) = {d_2}`, `|{d_2}| = 1`, `match(1, c_G = 1)` ✓ (Sh1); `{d_2} ⊆ A_doc^{Σ_2}` ✓ (Sh2 and Sh3, same slot address).

The per-tuple checks discharge each invariant pointwise; the universal quantifier in Sh0–Sh3 closes by inspection of the two-element relation.

**Template evaluation at Σ_2.** Suppose no Resolution tuples have been emitted yet, so `A_{K_res}^{Σ_2} = ∅` for a chosen Resolution relation `K_res` of shape `(1, 1, A_doc, A_rel, ⊤)`. (The layer selects `K_res` as the resolver vocabulary; the framework imposes no co-registration.) Compute:

`A_K^{Σ_2} = L_K^{Σ_2} \ nullified(Σ_2) = {τ_1, τ_2}` (no retractions issued).

`unresolved_K_comments_via(K_res, d_2) = {τ ∈ A_K^{Σ_2} : to₁(τ) = d_2 ∧ ¬resolved_by(τ, K_res)}`

Both τ_1 and τ_2 have `to₁(·) = d_2`; for each, `resolved_by(τ, K_res)` requires `(E ρ ∈ A_{K_res}^{Σ_2} :: to₁(ρ) = addr(τ))`, vacuously false since `A_{K_res}^{Σ_2} = ∅`. So:

`unresolved_K_comments_via(K_res, d_2) = {τ_1, τ_2}`

`all_K_resolved_via(K_res, d_2) = false`.

**Emission 3 (resolution).** `ρ_1 := Emit_{K_res}(Σ_2, home_R, F_ρ, G_ρ)` with `F_ρ = {(d_2, δ(1, #d_2))}` (resolver) and `G_ρ = {(a_1, δ(1, #a_1))}` (resolves τ_1 via R5, TupleSelfTargeting, ASN-0086). Result Σ_3.

*Sh-conf check at Σ_2 (under K_res shape).* F_ρ canonical-slot, `slot_addrs = {d_2}`, matches `c_F = 1`, `{d_2} ⊆ A_doc^{Σ_2}`. G_ρ canonical-slot, `slot_addrs = {a_1}`, matches `c_G = 1`, `{a_1} ⊆ A_rel^{Σ_2}` (since a_1 ∈ dom(Σ.L)). Admitted. ✓

**Template evaluation at Σ_3.**

`A_{K_res}^{Σ_3} = {ρ_1}` (no nullification).

`resolved_by(τ_1, K_res) = true` (ρ_1 witnesses); `resolved_by(τ_2, K_res) = false`.

`unresolved_K_comments_via(K_res, d_2) = {τ_2}`

`all_K_resolved_via(K_res, d_2) = false` (τ_2 still unresolved).

**Emission 4 (resolution of τ_2).** Emit `ρ_2` resolving τ_2 (analogous to Emission 3 with `G = {(a_2, δ(1, #a_2))}`). Result Σ_4.

`unresolved_K_comments_via(K_res, d_2) = ∅`

`all_K_resolved_via(K_res, d_2) = true`. The flag flips as expected.

**Rejection case 1: non-canonical from-set.** From Σ_4, attempt `Emit_K(Σ_4, home_K, F_3, G_3)` with `F_3 = {(d_1, δ(2, #d_1))}` — a depth-2 span violating canonical-slot form, which requires unit-depth displacements `δ(1, #x)`. Sh-conf clause (a) fails: `F_3` is not in canonical-slot form, so `slot_addrs(F_3)` is undefined (there is no `X_F` such that `F_3 = {(x, δ(1, #x)) : x ∈ X_F}`). The emission is rejected before any state transition. State remains Σ_4 unchanged; in particular `L_K^{Σ_4}, A_K^{Σ_4}` are not modified. ✗

Note that L4 (EndsetGenerality, ASN-0043) permits `F_3` in the substrate's link store at the level of endset well-formedness; the framework rejects it as a layer-level discipline imposed by Sh-conf. The substrate primitive K.λ would still accept `F_3` if invoked outside Emit_K — but per the layer commitment (Scope and Substrate Scaffolding), the relational layer routes all class-(iii) emissions of `K ∈ T_cat` through Emit_K, so this bypass is not exercised within the framework's scope.

**Rejection case 2: unallocated to-slot address.** From Σ_4, let `d_ghost ∈ T` be a tumbler outside `A^{Σ_4}` — an unallocated address (e.g., a future document not yet registered, or a deliberately-chosen ghost per L9 of ASN-0043). Attempt `Emit_K(Σ_4, home_K, F_4, G_4)` with `F_4 = {(d_1, δ(1, #d_1))}` (canonical-slot, `slot_addrs(F_4) = {d_1}`) and `G_4 = {(d_ghost, δ(1, #d_ghost))}` (canonical-slot, `slot_addrs(G_4) = {d_ghost}`). Sh-conf clause (d) fails on the G-side: `slot_addrs(G_4) = {d_ghost}` is not a subset of `t_G^{Σ_4} = A_doc^{Σ_4}` because `d_ghost ∉ A_doc^{Σ_4}`. The emission is rejected before any state transition. State remains Σ_4. ✗

This rejection is constitutive of the framework's discipline: shapes restrict slot addresses to *already-allocated* targets at emission time. L9 (TypeGhostPermission, ASN-0043) admits ghost spans in endsets generally — including in the type-endset slot — but the shape framework forbids ghost addresses in *slot positions* of registered relations. Whether a future shape family should admit ghost-targeting slot semantics is an open question (see Open Questions).

**Rejection case 3: cardinality mismatch.** From Σ_4, attempt `Emit_K(Σ_4, home_K, F_5, G_5)` with `F_5 = {(d_1, δ(1, #d_1)), (d_2, δ(1, #d_2))}` (canonical-slot, but `slot_addrs(F_5) = {d_1, d_2}` with `|·| = 2`) and `G_5 = {(d_2, δ(1, #d_2))}` (canonical-slot, single slot address). Sh-conf clause (c) fails on the F-side: `match(2, c_F = 1)` is false (cardinality 2 does not match the exact-1 requirement). The emission is rejected before any state transition. State remains Σ_4. ✗

Symmetric rejection: emitting with `F_5' = ∅` against `c_F = 1` fails on `match(0, 1)`; emitting with the same `G_5` swapped for an empty G fails on `match(0, c_G = 1)`. Cardinality is the second of Sh-conf's three independently-checked structural gates (canonical form, cardinality, target domain); a mismatch at any gate rejects.

**Edge case: retraction of τ_1.** From Σ_4, issue `Nullify(Σ_4, d_retr, a_1)` producing Σ_5. By R6c (RestorationByReemission, ASN-0086), τ_1 is permanently removed from `A_K^Σ` for all future states. So:

`A_K^{Σ_5} = {τ_2}` (τ_1 nullified; τ_2 remains).

`unresolved_K_comments_via(K_res, d_2) = {τ ∈ A_K^{Σ_5} : to₁(τ) = d_2 ∧ ¬resolved_by(τ, K_res)} = ∅` (τ_2 still resolved by ρ_2, which is in `A_{K_res}^{Σ_5}`).

`all_K_resolved_via(K_res, d_2) = true`.

The framework gives stable, well-typed answers across emission and retraction events. Sh0–Sh3 are preserved inductively, template signatures match the shape registry, and the active-subset machinery composes cleanly with retraction.


## Additional Worked Examples

### Coverage under SingleHomeCoverageDiscipline

Register `K = review` with the Coverage shape `(1, 1, A_doc, A_doc, ⊥)`, committed to single-home emission at `d_K ∈ dom(Σ_0.M)`. Pre-allocate `d_witness, d_subject ∈ A_doc^{Σ_0}` and `d_witness' ∈ A_doc^{Σ_0}`.

**Emission C1.** `Emit_K(Σ_0, d_K, F_C1, G_C1)` with `F_C1 = {(d_witness, δ(1, #d_witness))}` (witness) and `G_C1 = {(d_subject, δ(1, #d_subject))}` (subject). Sh-conf admits (canonical-slot, cardinality 1/1, both `⊆ A_doc^{Σ_0}`). Result Σ_1 with τ_1 at address `a_1 = [d_K.0.s_L.1]` (first emission per K.λ's first-emission branch, ASN-0086). `emission_order(τ_1) = 0`.

**Emission C2.** `Emit_K(Σ_1, d_K, F_C2, G_C2)` with `F_C2 = {(d_witness', δ(1, #d_witness'))}` (different witness) and `G_C2 = G_C1` (same subject). Sh-conf admits. Result Σ_2 with τ_2 at address `a_2 = inc(a_1, 0)` (subsequent-emission branch). `emission_order(τ_2) = 1`.

**Emission C3.** `Emit_K(Σ_2, d_K, F_C3, G_C3)` with `F_C3 = F_C1` (original witness again) and `G_C3 = G_C1` (same subject). Coverage's `idem = ⊥` admits this even with identical slot-addresses to C1. Result Σ_3 with τ_3 at `a_3 = inc(a_2, 0)`. `emission_order(τ_3) = 2`.

**Template evaluation at Σ_3.**

`S_{d_subject} = {τ ∈ A_K^{Σ_3} : to₁(τ) = d_subject} = {τ_1, τ_2, τ_3}`.

`latest_K_for_addr(d_subject) = argmax_{τ ∈ S_{d_subject}} emission_order(τ) = τ_3` (chain-index 2).

Reading the witness off the returned tuple: `from₁(τ_3) = d_witness`. The consumer recovers both the latest assertion *and* its attribution.

If a fourth emission C4 occurs with subject `d_subject` from any witness, `latest_K_for_addr(d_subject)` advances to that new τ_4 (chain-index 3); previous tuples remain in `L_K` and `A_K` but are no longer "latest." Retracting τ_3 (issuing `Nullify(Σ_3, d_retr, a_3)`) yields Σ_4 with `A_K^{Σ_4} = {τ_1, τ_2}` and `latest_K_for_addr(d_subject) = τ_2` (chain-index 1, the maximum surviving).

### Tuple-Classifier

Register `K = endorsed` with shape `(0, 1, -, A_rel, ⊤)`, intended to mark comment-tuples as endorsed. Working from Σ_4 of the Comment example, with τ_2 ∈ A_rel^{Σ_4}:

`Emit_K(Σ_4, home_K, ∅, {(a_2, δ(1, #a_2))})` — F empty (matches `c_F = 0`), G targets the tuple address `a_2`. Sh-conf admits (clause (d) for F is vacuous since `-^Σ = ∅` and `slot_addrs(F) = ∅ ⊆ ∅`; G-side checks `{a_2} ⊆ A_rel^{Σ_4}`). Result Σ_4'.

Template evaluation: `is_K(a_2) ≡ (E σ ∈ A_K^{Σ_4'} :: to₁(σ) = a_2) = true`; `is_K(a_1) = false`. The same single-letter substitution `d ↝ τ` from Classifier's template body, with the signature shifted from `A_doc → Bool` to `A_rel → Bool`.

### Provenance (partial G-slot)

Register `K = attributed_by` with shape `(1, 0|1, A, A, ⊤)`. Two emission forms exercise the `0|1` partiality:

**Form 1 (with target):** `Emit_K(Σ, home_K, {(s, δ(1, #s))}, {(t, δ(1, #t))})` with both `s, t ∈ A^Σ`. Sh-conf admits (canonical-slot, cardinality 1/1, `s ∈ A^Σ`, `t ∈ A^Σ`). Resulting τ has `from₁(τ) = s`, `to₁⁻(τ) = t` (defined).

**Form 2 (empty target):** `Emit_K(Σ, home_K, {(s, δ(1, #s))}, ∅)` with `s ∈ A^Σ`. Sh-conf admits (G is canonical-slot trivially with `slot_addrs(∅) = ∅`; `match(0, 0|1)` holds since `0 ∈ {0, 1}`; clause (d) for G is vacuous since `slot_addrs(∅) = ∅` is a subset of any target domain). Resulting τ has `from₁(τ) = s`, `to₁⁻(τ) = ⊥` (undefined).

Template evaluation: `outgoing_K(s) = {τ ∈ A_K^Σ : from₁(τ) = s}` returns both forms; consumers that need to discriminate read `to₁⁻` on each result. `to₁⁻(τ) = ⊥` signals attribution-only events (e.g., agent recorded without a separate target); `to₁⁻(τ) ≠ ⊥` carries the attribution-target pair. Both shapes pass `from₁`'s total signature because `c_F = 1` always holds.


## Consequences

(a) *Adding a new relation generates predicates for free.* A new K with `shape(K) = Attribute` immediately yields `has_K`, `K_sidecars_of`, and `K_sidecar_of` (the last conditional on Sh4) — no per-relation predicate code is required. The cost of a new relation is one entry in the shape registry.

(b) *Composite predicates extend the catalog through the same compositional primitives.* A composite predicate combines atomic templates through Boolean operators and quantification over `T_cat`. The framework does not establish a closure theorem about these primitives — whether composition can express predicates strictly beyond what the catalog's atomic templates yield is a property of the composition language adopted, not a structural guarantee of Sh5. The design observation we record is weaker: the canonical-shape catalog is the registry's *atomic* vocabulary, and adding a structurally new pattern (e.g., a slot-cardinality combination not yet present) is handled by extending the catalog with a new canonical shape, not by composing existing relations. Layer composites (e.g., `K_is_fresh`) extend the predicate language further by bringing in external accessors like `mtime`; these compose atop the framework but are not part of it.

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
| Sh_K | DEF | Shape: `(c_F, c_G, t_F, t_G, idem)` | introduced |
| match | DEF | Cardinality match predicate over `{0, 1, *, 0\|1}` | introduced |
| T_cat | DEF | Typed-relation catalog: distinguished `T_cat ⊆ T_admissible` up to `~` | introduced |
| shape | DEF | Shape registry `T_cat → Shape`, per-class constant, lifetime-constant | introduced |
| conf_K^Σ | DEF | State-indexed conformance predicate; monotone along `⊑̂` | introduced |
| from_K^Σ, to_K^Σ | DEF | Total set-valued slot accessors | introduced |
| from₁, to₁ | DEF | Point-valued slot accessors (defined when c = 1) | introduced |
| from₁⁻, to₁⁻ | DEF | Optional point-valued slot accessors (defined when c = 0\|1) | introduced |
| Sh-conf | AXIOM | ShapeConformanceAxiom — Emit_K (relational-layer op) rejects unregistered types and non-conformant emissions; binds Emit_K, not K.λ | introduced |
| Sh0 | LEMMA | FromSlotCanonicalAndCardinalityFixed — proof covers both `→` and `↦ \ →`, via layer-commitment routing | introduced |
| Sh1 | LEMMA | ToSlotCanonicalAndCardinalityFixed — symmetric to Sh0 | introduced |
| Sh2 | LEMMA | FromSlotTargetRestricted — `slot_addrs(F) ⊆ t_F^Σ` on every tuple | introduced |
| Sh3 | LEMMA | ToSlotTargetRestricted — symmetric to Sh2; commutes with retraction (`A_K ⊆ L_K`) | introduced |
| SlotAccessorTotality | LEMMA | When `c = 1`, the point accessor is a total function | introduced |
| Sh4 | LEMMA | IdempotencyDiscipline — at-most-one active duplicate when `idem = ⊤`; theorem under the layer-discipline contract, with inductive preservation argument | introduced |
| Sh5 | META | TemplateCatalog — hand-curated per-shape template families; mechanical-derivation downgraded from prior LEMMA claim | introduced |
| SingleHomeCoverageDiscipline | DEF | Per-K commitment securing `emission_order` for Coverage relations | introduced |
| layer-discipline contract (Sh4) | DEF | Observe-then-Emit protocol clauses (i)–(iii) the layer commits to for idempotent K | introduced |
| content-side scaffolding | ASSUMPTION | Element-level content addresses, content subspace partition, content-store antichain, content-store monotonicity, per-document link sub-allocator chains — assumed of the substrate-conforming layer | introduced |
| layer commitment (Emit_K routing) | ASSUMPTION | Every class-(iii) emission of `K ∈ T_cat` routes through `Emit_K` | introduced |


## Open Questions

- Should `(0, 0)` shapes be admitted? A relation with `c_F = c_G = 0` would be a single-tuple existence flag whose only role is "this event happened" without any from/to attribution; whether the substrate has any such relations is unclear, and the slot accessors degenerate to constants on it.
- Provenance's `c_G = 0|1` mixes shapes — should it be split into two distinct canonical shapes (Provenance-with-target and Provenance-attribution-only), each generating separate templates? The current formulation requires the optional accessor `to₁⁻` to handle both cases in a single template.
- Is idempotency recoverable from cardinality plus target-domain alone, or is it an independent axis? Empirically the canonical catalog has both `idem = ⊤` and `idem = ⊥` for shapes with identical (cardinality, target-domain) — Comment vs. Citation, both `(1, 1, A_doc, A_doc, _)` — suggesting independence.
- The shape constraint `slot_addrs(F) ⊆ t_F^Σ` requires slot addresses to be already-allocated at emission time. This precludes shape-conformant emissions whose slot addresses are *ghost* (currently outside `A^Σ`, possibly to be allocated later). L9 (TypeGhostPermission, ASN-0043) permits ghost spans in endsets; the shape framework restricts this to *non-slot* uses only. Whether future shape families should admit ghost-targeting slot semantics — and under what state-dependent conformance rule — is an open design question.
- Do *composite shapes* (relations whose F or G is itself constrained by another relation's content) require a new restriction axis, or do they decompose into existing primitives plus auxiliary predicates expressible in the current template language?
- What guarantees the shape registry stays consistent across processes? Lifetime constancy is asserted as a substrate-level commitment within a single process; cross-process consistency (e.g., concurrent shape re-registration in a distributed substrate) is not addressed.
