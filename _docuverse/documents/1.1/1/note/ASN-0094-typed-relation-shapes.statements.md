# ASN-0094 Claim Statements

*Source: ASN-0094-typed-relation-shapes.md (revised unknown) — Extracted: 2026-05-23*

## Definition — CoverageProjection

For each tuple `(a, F, G) ∈ L_K`:

`cov : L_K → ℘(T) × ℘(T)`

`cov(a, F, G) = (coverage(F), coverage(G))`

where `coverage(·)` is the union of address sets denoted by the endset's spans.

---

## Definition — AllocatedCoverage

For an endset `F` and reachable state `Σ`:

`cov_allocated(F, Σ) := coverage(F) ∩ A^Σ`

where `A^Σ = dom(Σ.C) ∪ dom(Σ.L)`.

Properties:
- Finite at every Σ (since `A^Σ` is finite by content-store finiteness and L-fin)
- Monotone non-decreasing along `⊑̂`: `Σ ⊑̂ Σ'` entails `cov_allocated(F, Σ) ⊆ cov_allocated(F, Σ')` because `A^Σ ⊆ A^{Σ'}` and `coverage(F)` is a pure function of the endset value

---

## Definition — CanonicalSlotForm

An endset `F` is in *canonical-slot form* iff there exists a finite set `X_F ⊆ T` such that

`F = {(x, δ(1, #x)) : x ∈ X_F}`

The elements of `X_F` are the *slot addresses* of `F`. `X_F` is uniquely recoverable from any canonical-form `F`:

`X_F = {s ∈ T : (E (s, ℓ) ∈ F :: ℓ = δ(1, #s))}`

---

## Definition — SlotAddrs

For a canonical-form endset `F`:

`slot_addrs(F) = X_F`

where `X_F = {s ∈ T : (E (s, ℓ) ∈ F :: ℓ = δ(1, #s))}`.

`|slot_addrs(F)|` is a finite natural number (since `F` is a finite endset by ASN-0043's `Endset = ℘_fin(Span)`).

---

## AllocatedAddressAntichain — AllocatedAddressAntichain (LEMMA, lemma)

For every reachable state `Σ` and every `x ∈ A^Σ`:

`cov_allocated({(x, δ(1, #x))}, Σ) = {x}`

---

## Definition — Shape

A *shape* is a tuple

`Sh_K = (c_F, c_G, t_F, t_G, idem)`

with components:

- `c_F, c_G ∈ {0, 1, *, 0|1}` — *cardinality bounds* on the slot-address counts `|slot_addrs(F)|` and `|slot_addrs(G)|`. The values 0 and 1 are exact; `*` denotes "any natural number"; `0|1` denotes "0 or 1 exactly."
- `t_F, t_G` — *target-domain restrictions*. Each is one of the symbolic constants `A_doc`, `A_rel`, `A`, or the distinguished value `-`. At each state Σ the symbol expands: `A_doc ↦ A_doc^Σ = dom(Σ.C)`, `A_rel ↦ A_rel^Σ = dom(Σ.L)`, `A ↦ A^Σ = A_doc^Σ ∪ A_rel^Σ`, `- ↦ -^Σ = ∅`.
- `idem ∈ {⊤, ⊥}` — the *idempotency flag*.

---

## Definition — ShapeWellFormedness

A shape `Sh_K = (c_F, c_G, t_F, t_G, idem)` is *syntactically well-formed* iff all four of the following implications hold:

- `c_F = 0 ⟹ t_F = -`
- `t_F = - ⟹ c_F = 0`
- `c_G = 0 ⟹ t_G = -`
- `t_G = - ⟹ c_G = 0`

The cardinality side of each implication tests the *literal* registry value `0`, not the broader set `{0, 0|1}`: the values `0` and `0|1` are distinct entries in `{0, 1, *, 0|1}`. Similarly, `t_F = -` is the literal registry value `-`, distinct from `A_doc`, `A_rel`, and `A`.

---

## Definition — CardinalityMatch

For `n ∈ ℕ` and `c ∈ {0, 1, *, 0|1}`:

`match(n, c) ≡ (c = 0 ∧ n = 0) ∨ (c = 1 ∧ n = 1) ∨ (c = * ∧ n ∈ ℕ) ∨ (c = 0|1 ∧ n ∈ {0, 1})`

---

## Definition — TypedRelationCatalog

Fix a distinguished set `T_cat ⊆ T_admissible` *finite up to `~`* (equivalently, the quotient `T_cat / ~` is finite) that is *closed under coverage-equivalence*: `K ∈ T_cat ∧ K ~ K' ⟹ K' ∈ T_cat`.

`T_cat` is fixed at the substrate's initial state `Σ_init` and does not change as states evolve: at every reachable state Σ, the registered catalog is the same set `T_cat` declared at `Σ_init`.

For any `K ∈ T_admissible \ T_cat`, no shape is registered.

---

## Definition — ShapeRegistry

A function

`shape : T_cat → Shape`

assigns each registered type its shape. Two properties:

- *Per-class constancy.* For `K, K' ∈ T_cat` with `K ~ K'`: `shape(K) = shape(K')`. The function `shape` factors through `T_cat / ~`.
- *Lifetime constancy.* `shape` is fixed across the substrate's lifetime; it does not change as states evolve.

---

## Definition — Conformance

A tuple `(a, F, G) ∈ L_K^Σ` (with `K ∈ T_cat`) is *shape-conformant at state Σ* iff all of the following hold:

(a) `F` is in canonical-slot form; let `X_F = slot_addrs(F)`.
(b) `G` is in canonical-slot form; let `X_G = slot_addrs(G)`.
(c) `match(|X_F|, shape(K).c_F) ∧ match(|X_G|, shape(K).c_G)`.
(d) `X_F ⊆ shape(K).t_F^Σ ∧ X_G ⊆ shape(K).t_G^Σ`, with the symbolic `t` expanded per the Shape definition. When `t_F = -` (only legal under `c_F = 0`), the F-side of (d) is vacuously satisfied since `X_F = ∅`; symmetric for G.

Write `conf_K^Σ(F, G)` for this predicate.

*State-dependence and monotone discharge:* `conf_K^Σ(F, G) ⟹ conf_K^{Σ'}(F, G)` for every `Σ ⊑̂ Σ'`.

---

## Definition — SetSlotAccessors

For each `K ∈ T_cat`, define at every state Σ:

`from_K^Σ : L_K^Σ → ℘_fin(shape(K).t_F^Σ)` &nbsp; with &nbsp; `from_K^Σ(a, F, G) = slot_addrs(F)`

`to_K^Σ   : L_K^Σ → ℘_fin(shape(K).t_G^Σ)` &nbsp; with &nbsp; `to_K^Σ(a, F, G) = slot_addrs(G)`

These are total on `L_K^Σ` for any shape: Sh0/Sh1 guarantee canonical-slot form (so `slot_addrs` is defined); Sh2/Sh3 restrict the codomain to the registered target domain at the current state.

---

## Definition — PointSlotAccessors

For shapes with `c_F = 1`:

`from₁ : L_K^Σ → shape(K).t_F^Σ` &nbsp; with &nbsp; `from₁(τ) = the unique element of from_K^Σ(τ)`

For shapes with `c_G = 1`:

`to₁ : L_K^Σ → shape(K).t_G^Σ` &nbsp; with &nbsp; `to₁(τ) = the unique element of to_K^Σ(τ)`

---

## Definition — PartialPointSlotAccessors

`from₁⁻ : L_K^Σ → shape(K).t_F^Σ ∪ {⊥}` defined when `c_F ∈ {1, 0|1}`; returns `⊥` iff `|slot_addrs(F)| = 0`, and returns the unique element of `slot_addrs(F)` otherwise.

`to₁⁻ : L_K^Σ → shape(K).t_G^Σ ∪ {⊥}` defined analogously when `c_G ∈ {1, 0|1}`; returns `⊥` iff `|slot_addrs(G)| = 0`, and returns the unique element of `slot_addrs(G)` otherwise.

---

## Definition — LayerCallableCandidateSets

`C_K : Endset × Endset × Σ → ℘_fin(A_K^Σ)` defined when `shape(K).idem = ⊤`:

`C_K(F, G, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)}`

`C_fd_K : Endset × Σ → ℘_fin(A_K^Σ)` defined when K is registered under the *FDD functional-dependency contract*:

`C_fd_K(F, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}`

---

## Sh-conf — ShapeConformanceAxiom (AXIOM, axiom)

`Emit_K(Σ, d, F, G)` succeeds iff *ASN-0086's preconditions hold (specifically `d ∈ dom(Σ.M)`, with the regime simplification of `wp_086` below) and `K ∈ T_cat` and `conf_K^Σ(F, G)`*.

The framework extends ASN-0086's `Emit_K` return type from `Σ' × A_rel^{Σ'}` to `(Σ' × A_rel^{Σ'}) ∪ {⊥}`: on any failure (substrate or framework), `Emit_K` returns `⊥` and leaves the state unchanged (no `↦`-step occurs).

---

## RetractionTargetNotOnChain — RetractionTargetNotOnChain (LEMMA, lemma)

Let Σ be reachable from `Σ_init` under the framework's *Emit_K routing commitment*. For every `b ∈ dom(Σ.L)` and every `d ∈ dom(Σ.M)`:

`b ⋠ a_emit(Σ, d)`

---

## EffectiveWpSimplification — EffectiveWpSimplification (COROLLARY, lemma)

*(Statement, conditional on substrate reach.)* For every `K ∈ T_admissible`, every `d ∈ dom(Σ.M)`, and every `F, G ∈ Endset`, *at any call site for which the framework's Sh-conf gate would admit `Emit_K(Σ, d, F, G)` (i.e., the call reaches the substrate primitive K.λ rather than being short-circuited to `⊥` by Sh-conf)*, ASN-0086's `wp_086` simplifies to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`.

*(Effective wp at the framework's gate.)*

`wp_eff(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) = d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)`

The effective-wp form holds at every call site, including the rejected ones: when any Sh-conf conjunct fails, `wp_eff` evaluates to false and `Emit_K` returns `⊥` without invoking the substrate primitive.

---

## NullifyActiveSubsetCompatibility — NullifyActiveSubsetCompatibility (COROLLARY, lemma)

Under the framework's *Sh4 idempotency contract* with `R` registered in `T_cat` (baseline registration requirement), every `Nullify(Σ, d_retr, a)` call satisfying ASN-0086's P0/P1/P2 preconditions delivers ASN-0086's *active-subset content* of the Nullify postcondition — specifically:

(i) single-tuple scope: the property that any state `Σ_target` operationally reached at the conclusion of the call (where `Σ_target = Σ'` in the clause (iii) branch and `Σ_target = Σ` in the clause (ii) branch) satisfies `{t : a ≼ t} ∩ A_rel^{Σ_target} = {a}`;

(ii) nullification: `a ∈ nullified(Σ_target)` stable under R6a;

*whether the contract's clause (iii) admits a fresh `(Σ', _)` or clause (ii) suppresses to `⊥`.*

---

## Sh0 — FromSlotCanonicalAndCardinalityFixed (LEMMA, lemma)

For each `K ∈ T_cat`, every tuple in `L_K^Σ` at every reachable state Σ has `F` in canonical-slot form with `|slot_addrs(F)|` matching `c_F`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: F is canonical-slot form ∧ match(|slot_addrs(F)|, shape(K).c_F))`

---

## Sh1 — ToSlotCanonicalAndCardinalityFixed (LEMMA, lemma)

The G-side analog of Sh0:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: G is canonical-slot form ∧ match(|slot_addrs(G)|, shape(K).c_G))`

---

## Sh2 — FromSlotTargetRestricted (LEMMA, lemma)

For each `K ∈ T_cat`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(F) ⊆ shape(K).t_F^Σ)`

(vacuous on the F-side when `t_F = -`, i.e., when `c_F = 0`).

---

## Sh3 — ToSlotTargetRestricted (LEMMA, lemma)

Symmetric for `G`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(G) ⊆ shape(K).t_G^Σ)`

---

## SlotAccessorTotality — SlotAccessorTotality (LEMMA, lemma)

When `shape(K).c_F = 1`, `from₁` is a total function on `L_K^Σ`. Similarly for `to₁` when `c_G = 1`.

---

## Sh4 — IdempotencyDiscipline (LEMMA, lemma)

When `shape(K).idem = ⊤`:

`(A τ, τ' ∈ A_K^Σ : (slot_addrs(F_τ), slot_addrs(G_τ)) = (slot_addrs(F_{τ'}), slot_addrs(G_{τ'})) :: addr(τ) = addr(τ'))`

*Universal scope:* The two bound variables range independently over `A_K^Σ`, including the diagonal `τ = τ'`. The substantive content is off-diagonal: for any two *distinct* active tuples whose slot-address pairs match, Sh4 forces `addr(τ) = addr(τ')`, which combined with R1 (AddressInjectivity) collapses `τ = τ'`.

*Theorem under the Sh4 idempotency contract (single-process substrate scope).*

---

## Sh5 — TemplateCatalog (META, meta)

*(META discipline.)* This framework's catalog adheres to the rule that every catalog row's templates depend only on the following four input categories of *data symbols*:

(i) the shape components (cardinality, target-domain typing, idempotency flag);
(ii) K's name;
(iii) named scaffolding clauses surfaced in the *Scope and Substrate Scaffolding* list;
(iv) explicitly named per-K disciplines and per-call type-index parameters registered in the row's opt-in or parametric columns.

The criterion is *literal name-citation for data symbols*: a data-symbol reference in a template body must either be one of the shape-component slots, K itself, a scaffolding clause name, an accessor exported by a registered per-K discipline, or a parametric type-index argument; any data symbol falling outside these four categories violates the discipline and the catalog rejects the addition.

---

## Definition — SingleHomeCoverageDiscipline

A registered Coverage relation `K` commits to *single-home emission* iff every emission `Emit_K(Σ, d, F, G)` for type K uses a single fixed home document `d = d_K ∈ dom(Σ.M)` across the relation's lifetime.

Preservation property (theorem under the *single-home commitment*):

`(A τ ∈ L_K^Σ :: home(addr(τ)) = d_K)` at every reachable state Σ.

Companion property: `S_d ⊆ {chain elements at d_K}` for every `d ∈ A_doc^Σ`, where `S_d = {τ ∈ A_K^Σ : to₁(τ) = d}`.

`emission_order(τ) := chain_index(addr(τ), d_K)` — the unique `n ≥ 0` with `addr(τ) = inc^n(d_K.0.s_L.1, 0)`.

---

## Definition — SingleHomeCommitment

The layer-discipline contract realizing SingleHomeCoverageDiscipline. For each K with SingleHomeCoverageDiscipline registered, on every `Emit_K(Σ, d, F, G)` call site (executes before Sh-conf's structural gates):

(i) If `d ≠ d_K`, the call is *rejected outright*: `Emit_K` returns `⊥` at the layer's pre-substrate gate without invoking K.λ.
(ii) If `d = d_K`, the layer issues `Emit_K(Σ, d, F, G)` per the substrate's usual K.λ protocol (and any other applicable contracts at the same call site fire in their established order).

No Observe step required; the home check is a literal-equality test against a per-K registration constant.

---

## Definition — FunctionalDependencyDiscipline

A K registered with the DirectedPair shape may additionally register a *FunctionalDependencyDiscipline* commitment: at most one active tuple per from-slot value, formally

`(A τ, τ' ∈ A_K^Σ : from₁(τ) = from₁(τ') :: addr(τ) = addr(τ'))`

at every reachable state Σ.

*Strictly stronger than Sh4:* Sh4 enforces pairwise distinctness of slot-address *pairs* `(slot_addrs(F_τ), slot_addrs(G_τ))`; FDD enforces pairwise distinctness of `slot_addrs(F_τ)` alone.

Singleton-returning template (when FDD holds):

`K_target_of : A_doc → A_doc^Σ ∪ {⊥}`

`K_target_of(a) ≡ to₁(τ)` where τ is the unique element of `from_K(a)` (returns `⊥` when `from_K(a) = ∅`).

---

## Definition — Sh4IdempotencyContract

The layer-discipline contract realizing Sh4. For each `K ∈ T_cat` with `shape(K).idem = ⊤`, on every `Emit_K(Σ, d, F, G)` call site (after Sh-conf canonical-form gate, before cardinality/target-domain gates):

(i) Compute the candidate set

`C(F, G, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)}`

via:
- (i.a) Query `Observe_K(slot_addrs(F), slot_addrs(G), oper)` — returns `{τ ∈ A_K^Σ : slot_addrs(F) ⊆ coverage(F_τ) ∧ slot_addrs(G) ⊆ coverage(G_τ)}`
- (i.b) Post-filter: retain only τ with `slot_addrs(F_τ) = slot_addrs(F)` and `slot_addrs(G_τ) = slot_addrs(G)`

(ii) If `C(F, G, Σ) ≠ ∅`, the emission is *suppressed*: no `→`-step occurs.

(iii) Only if `C(F, G, Σ) = ∅` does the layer issue `Emit_K(Σ, d, F, G)`.

The layer commits to executing (i)–(iii) atomically with respect to other emitters and retractors at the same `~`-equivalence class of K.

---

## Definition — FddFunctionalDependencyContract

The layer-discipline contract realizing FunctionalDependencyDiscipline. For each K with FunctionalDependencyDiscipline registered, on every `Emit_K(Σ, d, F, G)` call site (after Sh-conf canonical-form gate, before cardinality/target-domain gates):

(i) Compute `C_fd(F, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}` via:
- (i.a) query `Observe_K(slot_addrs(F), ∅, oper)`
- (i.b) post-filter: retain only τ with `slot_addrs(F_τ) = slot_addrs(F)`

(ii) If `C_fd(F, Σ) ≠ ∅`, the emission is *suppressed*: no `→`-step occurs.

(iii) Only if `C_fd(F, Σ) = ∅` does the layer issue `Emit_K(Σ, d, F, G)`.

`C ⊆ C_fd` at every state (FDD's candidate set is broader; the discipline is stricter as a gate).

---

## substrate-conforming-layer scaffolding — SubstrateConformingLayerScaffolding (ASSUMPTION, axiom)

The following scaffolding clauses are assumed of the substrate-conforming layer:

- *Element-level content addresses:* Every `a ∈ dom(Σ.C)` is T4-valid with `zeros(a) = 3` and `#E(a) ≥ 2`.
- *Content subspace partition:* There is a fixed `s_C ∈ ℕ` with `s_C > 0` and `s_C ≠ s_L` such that `E(a).1 = s_C` for every `a ∈ dom(Σ.C)`.
- *Link subspace partition:* There is a fixed `s_L ∈ ℕ` with `s_L > 0` such that `E(a).1 = s_L` for every `a ∈ dom(Σ.L)`. The identification `subspace_I(·) = E(·).1` on element-level addresses is introduced by this layer commitment (consistent with L0's abstract `subspace_I(·) = s_L`).
- *Content-store antichain:* `(A a, a' ∈ dom(Σ.C) :: a ≼ a' ⟹ a = a')`.
- *Content-store monotonicity:* `dom(Σ.C) ⊆ dom(Σ'.C)` for every transition `Σ ↦ Σ'`.
- *Content-store finiteness:* `dom(Σ.C)` is finite at every reachable state.
- *Document address structure:* Every `d ∈ dom(Σ.M)` is T4-valid with `zeros(d) = 2`.
- *Per-document link sub-allocator chains:* For each `d ∈ dom(Σ.M)`, the substrate supplies a link sub-allocator whose output chain enumerates `{ℓ : home(ℓ) = d}` under T9.
- *Uniform link sub-allocator chain length:* For every `d ∈ dom(Σ.M)` and every pair `ℓ_1, ℓ_2` in the chain at `d`, `#ℓ_1 = #ℓ_2`.
- *Link sub-allocator chain-index function:* For each `d ∈ dom(Σ.M)` and each `ℓ` in the chain at `d`, `chain_index(ℓ, d) ∈ ℕ` such that `ℓ = inc^{chain_index(ℓ, d)}(d.0.s_L.1, 0)`, single-valued by T10a.7.

---

## Emit_K routing commitment — EmitKRoutingCommitment (ASSUMPTION, axiom)

Every class-(iii) emission of a type `K ∈ T_cat` routes through `Emit_K`; non-`Emit_K` class-(iii) invocations of these types are outside the framework's scope.
