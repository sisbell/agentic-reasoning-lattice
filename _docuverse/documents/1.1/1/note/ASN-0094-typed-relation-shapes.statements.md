# ASN-0094 Claim Statements

*Source: ASN-0094-typed-relation-shapes.md (revised unknown) — Extracted: 2026-05-23*

## cov — CoverageProjection (DEF, definition)

For each tuple `(a, F, G) ∈ L_K`:

`cov : L_K → ℘(T) × ℘(T)`

`cov(a, F, G) = (coverage(F), coverage(G))`

where `coverage(·)` is the union of address sets denoted by the endset's spans (Definition, ASN-0043).

---

## cov_allocated — AllocatedCoverage (DEF, definition)

For an endset `F` and reachable state `Σ`:

`cov_allocated(F, Σ) := coverage(F) ∩ A^Σ`

where `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` is the address universe at Σ (ASN-0086).

This set is finite at every Σ and monotone non-decreasing along `⊑̂`: `Σ ⊑̂ Σ'` entails `cov_allocated(F, Σ) ⊆ cov_allocated(F, Σ')` because `A^Σ ⊆ A^{Σ'}` and `coverage(F)` is a pure function of the endset value.

---

## canonical-slot form — CanonicalSlotForm (DEF, definition)

An endset `F` is in *canonical-slot form* iff there exists a finite set `X_F ⊆ T` such that

`F = {(x, δ(1, #x)) : x ∈ X_F}`

The elements of `X_F` are the *slot addresses* of `F`. `X_F` is uniquely recoverable from any canonical-form `F` by reading the start address of each unit-depth span; equivalently, `X_F = {s ∈ T : (E (s, ℓ) ∈ F :: ℓ = δ(1, #s))}` is a well-defined set-valued function of `F`.

`|slot_addrs(F)|` is a finite natural number (since `F` is a finite endset by ASN-0043's `Endset = ℘_fin(Span)`).

---

## slot_addrs — SlotAddrs (DEF, definition)

For a canonical-form endset `F` with `F = {(x, δ(1, #x)) : x ∈ X_F}`:

`slot_addrs(F) = X_F`

For canonical-form `F`, `coverage(F) = (∪ x ∈ X_F : {t : x ≼ t})` — infinite in `T` when `X_F ≠ ∅`; what shape constraints check is the finite syntactic `slot_addrs(F)`.

---

## AllocatedAddressAntichain — AllocatedAddressAntichain (LEMMA, lemma)

For every reachable state `Σ` and every `x ∈ A^Σ`:

`cov_allocated({(x, δ(1, #x))}, Σ) = {x}`

*Precondition note.* The hypothesis `x ∈ A^Σ` is sufficient: every address in `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` is element-level with non-empty element field. Span well-formedness `(x, δ(1, #x))` under T12 holds because `#x ≥ 1` for every `x ∈ T` (T0, ASN-0034).

---

## Sh_K — Shape (DEF, definition)

A *shape* is a tuple

`Sh_K = (c_F, c_G, t_F, t_G, idem)`

with components:

- `c_F, c_G ∈ {0, 1, *, 0|1}` — *cardinality bounds* on the slot-address counts `|slot_addrs(F)|` and `|slot_addrs(G)|`. The values 0 and 1 are exact; `*` denotes "any natural number"; `0|1` denotes "0 or 1 exactly."
- `t_F, t_G` — *target-domain restrictions*. Each is one of the symbolic constants `A_doc`, `A_rel`, `A`, or the distinguished value `-`. At each state Σ the symbol expands to the corresponding allocated set: `A_doc ↦ A_doc^Σ = dom(Σ.C)`, `A_rel ↦ A_rel^Σ = dom(Σ.L)`, `A ↦ A^Σ = A_doc^Σ ∪ A_rel^Σ`, `- ↦ -^Σ = ∅`.
- `idem ∈ {⊤, ⊥}` — the *idempotency flag*.

---

## ShapeWellFormedness — ShapeWellFormedness (DEF, definition)

A shape `Sh_K = (c_F, c_G, t_F, t_G, idem)` is *syntactically well-formed* iff all four of the following implications hold:

- `c_F = 0 ⟹ t_F = -`
- `t_F = - ⟹ c_F = 0`
- `c_G = 0 ⟹ t_G = -`
- `t_G = - ⟹ c_G = 0`

The cardinality side of each implication tests the *literal* registry value `0`, not the broader set `{0, 0|1}`: the values `0` and `0|1` are distinct entries in `{0, 1, *, 0|1}`, so the antecedent `c_F = 0` is false when `c_F = 0|1`. Similarly, `t_F = -` is the literal registry value `-`, distinct from `A_doc`, `A_rel`, and `A`.

---

## match — CardinalityMatch (DEF, definition)

For `n ∈ ℕ` and `c ∈ {0, 1, *, 0|1}`:

`match(n, c) ≡ (c = 0 ∧ n = 0) ∨ (c = 1 ∧ n = 1) ∨ (c = * ∧ n ∈ ℕ) ∨ (c = 0|1 ∧ n ∈ {0, 1})`

---

## T_cat — TypedRelationCatalog (DEF, definition)

Fix a distinguished set `T_cat ⊆ T_admissible` *finite up to `~`* (equivalently, the quotient `T_cat / ~` is finite) that is *closed under coverage-equivalence* (ASN-0086, `~` definition):

`K ∈ T_cat ∧ K ~ K' ⟹ K' ∈ T_cat`

Equivalently, `T_cat` is the union of finitely many `~`-equivalence classes.

*Decidable membership.* The predicate `K ∈ T_cat` is the coverage-class membership test `[K] ∈ T_cat / ~` — equivalently, "there exists `K'` in the registered representative list with `K ~ K'`". Decidable by checking `coverage(K) = coverage(K_rep)` against each of the finitely many registered representatives.

*Lifetime constancy.* `T_cat` is fixed at the substrate's initial state `Σ_init` and does not change as states evolve.

For any `K ∈ T_admissible \ T_cat`, no shape is registered; the substrate's shape-conformance gate rejects `Emit_K`.

---

## shape — ShapeRegistry (DEF, definition)

A function

`shape : T_cat → Shape`

with two properties:

- *Per-class constancy.* For `K, K' ∈ T_cat` with `K ~ K'`: `shape(K) = shape(K')`. The function `shape` factors through `T_cat / ~`.
- *Lifetime constancy.* `shape` is fixed across the substrate's lifetime; it does not change as states evolve.

*Registration interface.* For any `K ∈ T_cat`, the registry resolves `shape(K)` by finding the unique registered representative `K_rep` with `K ~ K_rep` and returning `shape(K_rep)`.

---

## conf_K^Σ — ShapeConformance (DEF, definition)

A tuple `(a, F, G) ∈ L_K^Σ` (with `K ∈ T_cat`) is *shape-conformant at state Σ* iff all of the following hold:

(a) `F` is in canonical-slot form; let `X_F = slot_addrs(F)`.
(b) `G` is in canonical-slot form; let `X_G = slot_addrs(G)`.
(c) `match(|X_F|, shape(K).c_F) ∧ match(|X_G|, shape(K).c_G)`.
(d) `X_F ⊆ shape(K).t_F^Σ ∧ X_G ⊆ shape(K).t_G^Σ`, with the symbolic `t` expanded per the Shape definition. When `t_F = -` (only legal under `c_F = 0`), the F-side of (d) is vacuously satisfied since `X_F = ∅`; symmetric for G.

Write `conf_K^Σ(F, G)` for this predicate.

*Monotone discharge.* `conf_K^Σ(F, G) ⟹ conf_K^{Σ'}(F, G)` for every `Σ ⊑̂ Σ'`.

---

## from_K^Σ, to_K^Σ — SetSlotAccessors (DEF, definition)

For each `K ∈ T_cat`, define at every state Σ:

`from_K^Σ : L_K^Σ → ℘_fin(shape(K).t_F^Σ)` &nbsp; with &nbsp; `from_K^Σ(a, F, G) = slot_addrs(F)`

`to_K^Σ   : L_K^Σ → ℘_fin(shape(K).t_G^Σ)` &nbsp; with &nbsp; `to_K^Σ(a, F, G) = slot_addrs(G)`

These are total on `L_K^Σ` for any shape: Sh0/Sh1 guarantee canonical-slot form (so `slot_addrs` is defined); Sh2/Sh3 restrict the codomain to the registered target domain at the current state.

---

## from₁, to₁ — PointSlotAccessors (DEF, definition)

For shapes with `c_F = 1`:

`from₁ : L_K^Σ → shape(K).t_F^Σ` &nbsp; with &nbsp; `from₁(τ) = the unique element of from_K^Σ(τ)`

For shapes with `c_G = 1`:

`to₁ : L_K^Σ → shape(K).t_G^Σ` &nbsp; with &nbsp; `to₁(τ) = the unique element of to_K^Σ(τ)`

---

## from₁⁻, to₁⁻ — PartialPointSlotAccessors (DEF, definition)

For shapes with `c_F ∈ {1, 0|1}`:

`from₁⁻ : L_K^Σ → shape(K).t_F^Σ ∪ {⊥}` — returns `⊥` iff `|slot_addrs(F)| = 0`, returns the unique element of `slot_addrs(F)` otherwise.

For shapes with `c_G ∈ {1, 0|1}`:

`to₁⁻ : L_K^Σ → shape(K).t_G^Σ ∪ {⊥}` — returns `⊥` iff `|slot_addrs(G)| = 0`, returns the unique element of `slot_addrs(G)` otherwise.

---

## Sh-conf — ShapeConformanceAxiom (AXIOM, axiom)

The framework restricts ASN-0086's `Emit_K` by adding two preconditions: `K ∈ T_cat` and `conf_K^Σ(F, G)`. The combined success condition is:

`Emit_K(Σ, d, F, G)` succeeds iff *ASN-0086's preconditions hold (specifically `d ∈ dom(Σ.M)`) and `K ∈ T_cat` and `conf_K^Σ(F, G)`*.

On any failure, `Emit_K` returns `⊥` and leaves the state unchanged (no `↦`-step occurs). The framework extends ASN-0086's `Emit_K` return type from `Σ' × A_rel^{Σ'}` to `(Σ' × A_rel^{Σ'}) ∪ {⊥}`.

*Scope.* Sh-conf binds `Emit_K`, not the substrate primitive K.λ. K.λ remains permissive at the substrate level: ASN-0086's R0 admits any `(F, G, K)` triple with `K ∈ T_admissible` at a fresh K.λ-emitted address.

---

## Definition — LayerCallableCandidateSets

For each `K ∈ T_cat`, the framework exposes:

`C_K : Endset × Endset × Σ → ℘_fin(A_K^Σ)` defined when `shape(K).idem = ⊤`:

`C_K(F, G, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)}`

`C_fd_K : Endset × Σ → ℘_fin(A_K^Σ)` defined when K is registered under the *FDD functional-dependency contract*:

`C_fd_K(F, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}`

Both queries are side-effect-free reads.

---

## RetractionTargetNotOnChain — RetractionTargetNotOnChain (LEMMA, lemma)

Let Σ be reachable from `Σ_init` under the framework's *Emit_K routing commitment*. For every `b ∈ dom(Σ.L)` and every `d ∈ dom(Σ.M)`:

`b ⋠ a_emit(Σ, d)`

*Generality.* The Lemma is stated about an *arbitrary* link-store address `b ∈ dom(Σ.L)`, not specifically about retraction-tuple slot addresses. The proof uses only `b ∈ dom(Σ.L)` and `d ∈ dom(Σ.M)`.

---

## EffectiveWpSimplification — EffectiveWpSimplification (COROLLARY, corollary)

Let Σ be reachable from `Σ_init` under the framework's *Emit_K routing commitment*.

*(Statement, conditional on substrate reach.)* For every `K ∈ T_admissible`, every `d ∈ dom(Σ.M)`, and every `F, G ∈ Endset`, at any call site for which the framework's Sh-conf gate would admit `Emit_K(Σ, d, F, G)` (i.e., the call reaches the substrate primitive K.λ), ASN-0086's `wp_086` simplifies to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`.

*(Effective wp at the framework's gate.)* The *effective wp* of `Emit_K` under the framework simplifies to:

`wp_eff(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) = d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)`

The effective-wp form holds at every call site.

---

## NullifyActiveSubsetCompatibility — NullifyActiveSubsetCompatibility (COROLLARY, corollary)

Under the framework's *Sh4 idempotency contract* with `R` registered in `T_cat` (baseline registration requirement), every `Nullify(Σ, d_retr, a)` call satisfying ASN-0086's P0/P1/P2 preconditions delivers ASN-0086's *active-subset content* of the Nullify postcondition — specifically:

(i) single-tuple scope: the property that any state `Σ_target` operationally reached at the conclusion of the call (where `Σ_target = Σ'` in the clause (iii) branch and `Σ_target = Σ` in the clause (ii) branch) satisfies `{t : a ≼ t} ∩ A_rel^{Σ_target} = {a}`;

(ii) nullification: `a ∈ nullified(Σ_target)` stable under R6a —

*whether the contract's clause (iii) admits a fresh `(Σ', _)` or clause (ii) suppresses to `⊥`*.

---

## Sh0 — FromSlotCanonicalAndCardinalityFixed (LEMMA, lemma)

For each `K ∈ T_cat`, every tuple in `L_K^Σ` at every reachable state Σ has `F` in canonical-slot form with `|slot_addrs(F)|` matching `c_F`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: F is canonical-slot form ∧ match(|slot_addrs(F)|, shape(K).c_F))`

*Proof structure.* By induction on `↦*` from `Σ_0 = Σ_init`:
- *Base:* `L_K^{Σ_0} = ∅`; universal vacuous.
- *Case A:* `L_K^{Σ'} = L_K^Σ` — property inherited by IH.
- *Case B:* `L_K^{Σ'} = L_K^Σ ∪ {τ_new}` — by *Emit_K routing commitment*, Sh-conf admitted the call because `conf_K^Σ(F, G)` held (clauses (a) and (c)); new tuple satisfies the property.

---

## Sh1 — ToSlotCanonicalAndCardinalityFixed (LEMMA, lemma)

The G-side analog of Sh0:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: G is canonical-slot form ∧ match(|slot_addrs(G)|, shape(K).c_G))`

*Proof structure.* By induction on `↦*` from `Σ_0 = Σ_init`:
- *Base:* `L_K^{Σ_0} = ∅`; universal vacuous.
- *Case A:* `L_K^{Σ'} = L_K^Σ` — inherited by IH.
- *Case B:* `L_K^{Σ'} = L_K^Σ ∪ {τ_new}` — by *Emit_K routing commitment*, Sh-conf clause (b) forces `G` canonical-slot; clause (c) forces `match(|slot_addrs(G)|, shape(K).c_G)`.

---

## Sh2 — FromSlotTargetRestricted (LEMMA, lemma)

For each `K ∈ T_cat`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(F) ⊆ shape(K).t_F^Σ)`

(vacuous on the F-side when `t_F = -`, i.e., when `c_F = 0`).

*Well-formedness precondition.* By Sh0 at the current state Σ, every `τ ∈ L_K^Σ` has F in canonical-slot form, so `slot_addrs(F)` is well-defined throughout.

*Proof structure.* By induction on `↦*` from `Σ_0 = Σ_init`:
- *Base:* `L_K^{Σ_0} = ∅` vacuously.
- *Case A:* `L_K^{Σ'} = L_K^Σ` — inherited with monotone preservation `X_F ⊆ t_F^Σ ⟹ X_F ⊆ t_F^{Σ'}` (since `t_F^Σ ⊆ t_F^{Σ'}`).
- *Case B:* `L_K^{Σ'} = L_K^Σ ∪ {τ_new}` — Sh-conf clause (d) at emission gives `X_F ⊆ t_F^Σ`; monotonicity extends to Σ'.

---

## Sh3 — ToSlotTargetRestricted (LEMMA, lemma)

Symmetric to Sh2 for `G`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(G) ⊆ shape(K).t_G^Σ)`

*Well-formedness precondition.* By Sh1 at the current state Σ, every `τ ∈ L_K^Σ` has G in canonical-slot form, so `slot_addrs(G)` is well-defined throughout.

*Retraction commutativity.* `A_K^Σ ⊆ L_K^Σ` always, so every tuple in `A_K^Σ` is also shape-conformant. Retraction removes tuples from `A_K^Σ` but never introduces non-conformant tuples.

---

## SlotAccessorTotality — SlotAccessorTotality (LEMMA, lemma)

When `shape(K).c_F = 1`, `from₁` is a total function on `L_K^Σ`. Similarly for `to₁` when `c_G = 1`.

*Proof.* By Sh0, every `τ ∈ L_K^Σ` has `F` in canonical-slot form with `|slot_addrs(F)| = 1` (since `match(n, 1) ⟺ n = 1`). A finite set of cardinality 1 has a unique element. Define `from₁(τ)` as that element. By Sh2, this element lies in `t_F^Σ`. ∎

---

## Sh4 — IdempotencyDiscipline (LEMMA, lemma)

When `shape(K).idem = ⊤`, a layer above the substrate enforces at most one *active* tuple in `L_K` with any given slot-address pair. For `τ = (a, F, G) ∈ L_K^Σ` write `F_τ := F` and `G_τ := G`. Then:

`(A τ, τ' ∈ A_K^Σ : (slot_addrs(F_τ), slot_addrs(G_τ)) = (slot_addrs(F_{τ'}), slot_addrs(G_{τ'})) :: addr(τ) = addr(τ'))`

*Universal scope.* The substantive content is off-diagonal: for any two *distinct* active tuples `τ, τ'` whose slot-address pairs match, Sh4 forces `addr(τ) = addr(τ')` — combined with R1 (AddressInjectivity, ASN-0086), this collapses `τ = τ'`, contradicting the off-diagonal assumption.

*Status.* Sh4 is a theorem under the *Sh4 idempotency contract*, not a substrate-enforced axiom.

---

## Sh5 — TemplateCatalog (META, meta)

For each canonical shape `Sh_canon`, the shape framework specifies a hand-curated *template family* of predicate forms applicable to every `K ∈ T_cat` with `shape(K) = Sh_canon`.

*(a) META observation.* The template families are written by hand against the canonical shape catalog. There is no procedure mapping an arbitrary shape to its template family.

*(b) META discipline.* Every catalog row's templates depend only on:
(i) the shape components (cardinality, target-domain typing, idempotency flag);
(ii) K's name;
(iii) named scaffolding clauses from the *Scope and Substrate Scaffolding* list;
(iv) explicitly named per-K disciplines and per-call type-index parameters registered in the row's opt-in or parametric columns.

The criterion is *literal name-citation for data symbols*. Logical and set-theoretic primitives are not data symbols and are unrestricted.

*Signature derivation rule.* Template signatures derive mechanically from shape components: a template's input domain and codomain symbols are read from the shape's `t_F` and `t_G` values respectively.

---

## Definition — SingleHomeCoverageDiscipline

A registered Coverage relation `K` commits to *single-home emission* iff every emission `Emit_K(Σ, d, F, G)` for type K uses a single fixed home document `d = d_K ∈ dom(Σ.M)` across the relation's lifetime.

The single-home property preserved: `(A τ ∈ L_K^Σ :: home(addr(τ)) = d_K)` at every reachable state Σ.

The companion property: for every `d ∈ A_doc^Σ`, `S_d = {τ ∈ A_K^Σ : to₁(τ) = d} ⊆ {chain elements at d_K}`.

---

## single-home commitment — SingleHomeCommitment (DEF, definition)

The layer-discipline contract realizing SingleHomeCoverageDiscipline. For each K with SingleHomeCoverageDiscipline registered, on every `Emit_K(Σ, d, F, G)` call site:

*Ordering with Sh-conf.* The home check executes *before* Sh-conf's structural gates.

(i) If `d ≠ d_K`, the call is *rejected outright*: `Emit_K` returns `⊥` without invoking K.λ.

(ii) If `d = d_K`, the layer issues `Emit_K(Σ, d, F, G)` per the substrate's usual K.λ protocol.

No Observe step required; the home check is a literal-equality test against the per-K registration constant `d_K`.

---

## FunctionalDependencyDiscipline — FunctionalDependencyDiscipline (DEF, definition)

A K registered with the DirectedPair shape may additionally register a *FunctionalDependencyDiscipline* commitment: at most one active tuple per from-slot value, formally

`(A τ, τ' ∈ A_K^Σ : from₁(τ) = from₁(τ') :: addr(τ) = addr(τ'))`

at every reachable state Σ.

This is strictly stronger than Sh4: Sh4 enforces pairwise distinctness of slot-address *pairs* `(slot_addrs(F_τ), slot_addrs(G_τ))`; FDD enforces pairwise distinctness of `slot_addrs(F_τ)` alone.

*Singleton-returning template enabled by FDD:*

`K_target_of : A_doc → A_doc^Σ ∪ {⊥}`

`K_target_of(a) ≡ to₁(τ)` where τ is the unique element of `from_K(a)` (returns `⊥` when `from_K(a) = ∅`).

---

## Sh4 idempotency contract — Sh4IdempotencyContract (DEF, definition)

The layer-discipline contract realizing Sh4. For each `K ∈ T_cat` with `shape(K).idem = ⊤`, on every `Emit_K(Σ, d, F, G)` call site (after Sh-conf's canonical-form gate has fired):

(i) Compute the candidate set:

`C(F, G, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)}`

via two steps:

(i.a) Query `Observe_K(slot_addrs(F), slot_addrs(G), oper)`.

(i.b) Post-filter: retain only τ with `slot_addrs(F_τ) = slot_addrs(F)` and `slot_addrs(G_τ) = slot_addrs(G)`.

(ii) If `C(F, G, Σ) ≠ ∅`, the emission is *suppressed*: no `→`-step occurs; `Emit_K` returns `⊥`.

(iii) Only if `C(F, G, Σ) = ∅` does the layer issue `Emit_K(Σ, d, F, G)`.

The layer commits to executing (i)–(iii) atomically with respect to other emitters and retractors at the same `~`-equivalence class of K (in the single-process substrate scope: within-call sequentiality between `Observe_K` and the substrate K.λ-step).

---

## FDD functional-dependency contract — FddFunctionalDependencyContract (DEF, definition)

The layer-discipline contract realizing FunctionalDependencyDiscipline. For each K with FunctionalDependencyDiscipline registered, on every `Emit_K(Σ, d, F, G)` call site (after Sh-conf's canonical-form gate has fired):

(i) Compute:

`C_fd(F, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}`

via two steps:

(i.a) Query `Observe_K(slot_addrs(F), ∅, oper)`.

(i.b) Post-filter: retain only τ with `slot_addrs(F_τ) = slot_addrs(F)`.

(ii) If `C_fd(F, Σ) ≠ ∅`, the emission is *suppressed*; `Emit_K` returns `⊥`.

(iii) Only if `C_fd(F, Σ) = ∅` does the layer issue `Emit_K(Σ, d, F, G)`.

*FDD subsumes the Sh4 idempotency contract* at FDD-registered K: `C ⊆ C_fd`, so `C_fd = ∅ ⟹ C = ∅`. At FDD-registered K, only the FDD contract clauses (i)–(iii) run; the Sh4 contract's clauses are dormant.

---

## substrate-conforming-layer scaffolding — SubstrateConformingLayerScaffolding (ASSUMPTION, assumption)

The following properties are assumed of the substrate-conforming layer and cited by name in proofs:

- *Element-level content addresses.* Every `a ∈ dom(Σ.C)` is T4-valid with `zeros(a) = 3` and `#E(a) ≥ 2`.
- *Content subspace partition.* There is a fixed `s_C ∈ ℕ` with `s_C > 0` and `s_C ≠ s_L` such that `E(a).1 = s_C` for every `a ∈ dom(Σ.C)`.
- *Link subspace partition.* There is a fixed `s_L ∈ ℕ` with `s_L > 0` such that `E(a).1 = s_L` for every `a ∈ dom(Σ.L)`. The identification `subspace_I(·) = E(·).1` on element-level addresses is introduced by the scaffolding (layer-local, not imported from L0).
- *Content-store antichain.* `(A a, a' ∈ dom(Σ.C) :: a ≼ a' ⟹ a = a')`.
- *Content-store monotonicity.* `dom(Σ.C) ⊆ dom(Σ'.C)` for every transition `Σ ↦ Σ'`.
- *Content-store finiteness.* `dom(Σ.C)` is finite at every reachable state.
- *Document address structure.* Every `d ∈ dom(Σ.M)` is T4-valid with `zeros(d) = 2`.
- *Per-document link sub-allocator chains.* For each `d ∈ dom(Σ.M)` the substrate-conforming layer supplies a link sub-allocator whose output chain enumerates `{ℓ : home(ℓ) = d}` under T9 (ForwardAllocation, ASN-0034).
- *Uniform link sub-allocator chain length.* For every `d ∈ dom(Σ.M)` and every pair `ℓ_1, ℓ_2` in the chain at `d`, `#ℓ_1 = #ℓ_2`.
- *Link sub-allocator chain-index function.* For each `d ∈ dom(Σ.M)` and each `ℓ` in the chain at `d`, a total function `chain_index(ℓ, d) ∈ ℕ` such that `ℓ = inc^{chain_index(ℓ, d)}(d.0.s_L.1, 0)` — well-defined and single-valued by T10a.7 (EnumerationInjectivity, ASN-0034).

---

## Emit_K routing commitment — EmitKRoutingCommitment (ASSUMPTION, assumption)

Every class-(iii) emission of a type `K ∈ T_cat` is committed to route through `Emit_K`; non-`Emit_K` class-(iii) invocations of these types are outside the framework's scope.

Sh-conf binds `Emit_K` (the relational-layer operation), not K.λ (the substrate primitive — K.λ remains permissive at the substrate level). The inductive arguments for Sh0–Sh4 invoke the *Emit_K routing commitment* to conclude that every new tuple in `L_K^Σ` for `K ∈ T_cat` arrived via an `Emit_K` call subject to Sh-conf.
