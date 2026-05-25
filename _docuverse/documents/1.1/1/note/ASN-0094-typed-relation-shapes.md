# ASN-0094: Typed Relation Shapes

*Restricting the relational primitive into a predicate language.*

ASN-0086 establishes typed relations `L_K` with the three operations Emit, Observe, Nullify, governed by the lemma family R0…R7a (concretely: R0, R0a, R0a-Cor1, R0a-Cor2, R1, R2, R3, R4, R5, R5-Cor, R6a, R6b, R6c, R6c-Corollary, R7a, together with the auxiliary lemma LinkStoreInvarianceUnderArrangement). The relational structure as defined there is too permissive to support a typed predicate vocabulary: F and G can be any finite endsets whose coverage lies anywhere in `T`, so a predicate over `L_K` has no fixed signature. Every predicate would have to take a pattern in `℘(T) × ℘(T)` and return Bool, "two relations of the same shape" would not be expressible, and slot accessors `from(τ)`, `to(τ)` would be partial in a way that defeats type-checking.

We are looking for the minimum additional layer that closes this gap. The answer is a single structural decision per type: each `K ∈ T_cat` is assigned a *shape* — a tuple of constraints on cardinality, target domain, and idempotency — and the substrate enforces shape-conformance at Emit time. From the shape, a predicate template family is mechanically organized (though not mechanically derived; see Sh5). The pipeline is:

> R0…R7a (typed relations + operations) → **shape restrictions** (this document) → predicate template families → composed predicates

Shapes are not derivable from R0…R7a. They are an additional design decision the substrate makes about which relations it admits and what `(F, G)` pairs each admits. We justify each constraint by what predicate forms it makes possible, and by what the substrate cannot express without it.

*Load-bearing semantic departure from ASN-0086.* The framework registers Retraction with `idem = ⊤`, which changes ASN-0086's apparent multiset semantics at R to *set semantics* at the bare `Nullify` alias: two consecutive bare `Nullify(Σ, d_retr, a)` calls at the same target `a` produce *one* tuple in `L_R^Σ`, not two. Layers requiring audit-grade multiset semantics use *attributed retraction* (`c_F ≥ 1` with a distinguishing from-slot value at each emission). The full rationale (Nelson's two-layer active/audit reading and the migration recipe) is detailed in the *Nullify Compatibility* section; this is flagged here because it affects every downstream consumer of `L_R^Σ` reading audit-slice multiplicity.


## Scope and Substrate Scaffolding

*Arity scope.* This framework restricts the standard-triple slice `L^Σ` of `dom(Σ.L)` — the arity-3 links collected by ASN-0086's `L^Σ` definition. Higher-arity links admitted by L3 (ASN-0043) are outside its scope: the cardinality and target-domain shape components are defined over two slots only (F and G), and the slot-accessor and template machinery presupposes the arity-3 structure. Extending the framework to higher arities would require additional shape components per extra slot, which we do not pursue here.

*Emit_K routing commitment.* The framework is a discipline imposed by a relational layer atop ASN-0086. Every class-(iii) emission of a type `K ∈ T_cat` is committed to route through `Emit_K`; non-`Emit_K` class-(iii) invocations of these types are outside the framework's scope. Sh-conf below binds `Emit_K` (the relational-layer operation), not K.λ (the substrate primitive — K.λ remains permissive at the substrate level: any `F, G ∈ Endset` with `K ∈ T_admissible` is admissible to K.λ). The inductive arguments for Sh0–Sh3 invoke the *Emit_K routing commitment* to conclude that every new tuple in `L_K^Σ` for `K ∈ T_cat` arrived via an `Emit_K` call subject to Sh-conf.

*Naming convention for framework commitments.* The framework's named commitments are:
- *Emit_K routing commitment*: every class-(iii) `K ∈ T_cat` emission routes through `Emit_K`.
- *Sh4 idempotency contract* (Sh4 section): Observe-then-Emit protocol clauses (i)–(iii) for `idem = ⊤` K.
- *FDD functional-dependency contract* (FDD subsection): at-most-one-tuple-per-from-slot protocol, strictly stronger than Sh4.
- *Single-home commitment* (SHCD subsection): per-K constraint that every K-emission uses one fixed home `d_K`.
- *Unit-depth retraction discipline* (ASN-0086): derived here as a consequence of the Retraction shape.

*Consolidated commitment reference table.* The four named layer-discipline commitments are tabulated below (with the *Unit-depth retraction discipline* of ASN-0086 in row 5 for completeness):

| Commitment | Defining section | Applicable K's | Gate position | Discharged theorem |
|---|---|---|---|---|
| *Emit_K routing commitment* | Scope and Substrate Scaffolding | All `K ∈ T_cat` | Pre-gate routing precondition | Sh0–Sh3 (and IH propagation in Sh4/FDD/SHCD) |
| *Sh4 idempotency contract* | Sh4 section | K with `shape(K).idem = ⊤` not under FDD (structural trigger; no opt-in) | Gate 3 | Sh4 (pairwise slot-pair distinctness on `A_K^Σ`) |
| *FDD functional-dependency contract* | FDD subsection | K with `shape(K) = (1, 1, A_doc, A_doc, ⊤)` + per-K FDD registration | Gate 3 (subsumes Sh4 at FDD-registered K) | FDD's from-slot uniqueness; secures `K_target_of` |
| *Single-home commitment* | SHCD subsection | K with `shape(K) = (1, 1, A_doc, A_doc, ⊥)` + per-K SHCD registration | Gate 1 | SHCD's homed-set commitment; secures `emission_order` |
| *Unit-depth retraction discipline* (ASN-0086) | ASN-0086 | K with `K ~ R` | Derived from Sh-conf gates on R | `NoCraftedSpanReachesD` discharge |

Gate positions index the *Gate Ordering (consolidated)* clause in the Sh-conf section below (five gates: 1 SHCD, 2 Sh-conf canonical-form, 3 Sh4/FDD, 4 Sh-conf cardinality/target-domain, 5 K.λ). Each commitment's preservation theorem holds under (a) the *Emit_K routing commitment* and (b) the commitment's own clauses at every applicable call site; a layer breaking either loses the corresponding theorem.

*Substrate-conforming-layer scaffolding.* The framework operates atop a substrate-conforming layer (ASN-0086, Definition). The following clauses surface the specific properties this ASN cites by name; we refer to them collectively as *the scaffolding clauses*.

- *Element-level content addresses.* Every `a ∈ dom(Σ.C)` is T4-valid with `zeros(a) = 3` and `#E(a) ≥ 2`. (Content-side analog of L1, L1b, L1c on the link side.)
- *Content subspace partition.* Fixed `s_C ∈ ℕ` with `s_C > 0` and `s_C ≠ s_L` such that `E(a).1 = s_C` for every `a ∈ dom(Σ.C)`. (Symmetric to L0 from ASN-0043.)
- *Link subspace partition.* Fixed `s_L ∈ ℕ` with `s_L > 0` such that `E(a).1 = s_L` for every `a ∈ dom(Σ.L)`. (Local commitment consistent with L0: the scaffolding fixes the layer-local identification `subspace_I(·) = E(·).1` on element-level addresses, making the partitions directly comparable at the first element-field component. Not derivable from L0 alone — L0 treats `subspace_I(·)` as uninterpreted. A substrate surfacing `subspace_I` via a different projection lies outside the framework's scope.)
- *Content-store antichain.* `dom(Σ.C)` is a tumbler-prefix antichain at every reachable state. (Content-side symmetric to R0a.)
- *Content-store monotonicity.* `dom(Σ.C) ⊆ dom(Σ'.C)` for every `Σ ↦ Σ'`. (Symmetric to L12a.)
- *Content-store finiteness.* `dom(Σ.C)` is finite at every reachable state. (Symmetric to L-fin.)
- *Document address structure.* Every `d ∈ dom(Σ.M)` is T4-valid with `zeros(d) = 2`.
- *Per-document link sub-allocator chains.* For each `d ∈ dom(Σ.M)` the layer supplies a link sub-allocator whose output chain enumerates `{ℓ : home(ℓ) = d}`; this is the chain referenced by ASN-0086's R0a-Cor1 and FreshEmissionAddress.
- *Uniform link sub-allocator chain length.* All outputs of a single document's link sub-allocator share the same tumbler length.
- *Link sub-allocator chain-index function.* For each `d ∈ dom(Σ.M)` and each chain element `ℓ`, the layer supplies a total `chain_index(ℓ, d) ∈ ℕ` with `ℓ = inc^{chain_index(ℓ, d)}(d.0.s_L.1, 0)` (well-defined and single-valued by T10a.7).

We refer to these collectively as *the scaffolding clauses*.

*Framework-wide commitment to the `subspace_I(·) = E(·).1` identification.* The identification surfaced by the subspace partition clauses above is adopted as a framework-wide invariant: every theorem, lemma, definition, template, and worked example below operates under it. Any layer instantiating the framework commits to `subspace_I(·) = E(·).1` on element-level addresses once, at the framework's interface; consumers reasoning at L0's abstract `subspace_I(·)` level must verify the layer-local identification before invoking any framework result. The framework makes no claims at substrates surfacing `subspace_I` via a different physical projection.

*The framework, defined.* "The framework" denotes the shape discipline atop ASN-0086 introduced here, comprising: (1) the conformance axiom **Sh-conf**, (2) preservation lemmas **Sh0–Sh3**, (3) the idempotency theorem **Sh4** with auxiliary lemma **LinkAddressNotPrefixOfEmit** and corollary **EffectiveWpSimplification**, (4) the META catalog **Sh5**, and (5) the four layer-discipline contracts plus the substrate-conforming-layer scaffolding. Sh4, FDD, and SHCD are conditional theorems under their respective contracts; Sh0–Sh3 hold under the *Emit_K routing commitment* alone.


## The Address-Set Projection

Shape constraints operate on a *syntactic* projection of `(F, G)` — the slot-address sets extracted from canonical-form endsets — together with an *allocated-address* projection that bridges the syntactic check to substrate semantics. Two projections matter.

**Definition — Coverage Projection.** For each tuple `(a, F, G) ∈ L_K`:

`cov : L_K → ℘(T) × ℘(T)`

`cov(a, F, G) = (coverage(F), coverage(G))`

where `coverage(·)` is the union of address sets denoted by the endset's spans (Definition, ASN-0043). By PrefixSpanCoverage (ASN-0043), the coverage of a single unit-depth span at `x` is `{t ∈ T : x ≼ t}`, which is *infinite* in `T` by T0(a)/T0(b) (ASN-0034). The set-theoretic cardinality `|coverage(F)|` is therefore infinite for every non-empty canonical-form `F`, so cardinality constraints cannot be stated against `|coverage(F)|` directly.

The address-set view is a lossy projection — by L5 (EndsetSetSemantics, ASN-0043), endsets with different span decompositions can have identical coverage. For shape purposes the loss is intentional: shapes are predicates over what addresses a slot references, not over how those addresses are denoted.

**Definition — AllocatedCoverage.** For an endset `F` and reachable state `Σ`:

`cov_allocated(F, Σ) := coverage(F) ∩ A^Σ`

where `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` is the address universe at Σ (ASN-0086). This set is finite at every Σ (since `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` is finite by the content-store finiteness scaffolding for `dom(Σ.C)` and L-fin (ASN-0043) for `dom(Σ.L)`) and monotone non-decreasing along `⊑̂`: `Σ ⊑̂ Σ'` entails `cov_allocated(F, Σ) ⊆ cov_allocated(F, Σ')` because `A^Σ ⊆ A^{Σ'}` and `coverage(F)` is a pure function of the endset value.

**Definition — CanonicalSlotForm.** An endset `F` is in *canonical-slot form* iff there exists a finite set `X_F ⊆ T` such that

`F = {(x, δ(1, #x)) : x ∈ X_F}`

The elements of `X_F` are the *slot addresses* of `F`. `X_F` is uniquely recoverable from any canonical-form `F` by reading the start address of each unit-depth span; equivalently, `X_F = {s ∈ T : (E (s, ℓ) ∈ F :: ℓ = δ(1, #s))}` is a well-defined set-valued function of `F`. The comprehension recovers exactly `X_F` because `F`'s span set is `{(x, δ(1, #x)) : x ∈ X_F}` by the canonical-slot equation, so a span has start `s` iff `s = x` for some `x ∈ X_F` iff `s ∈ X_F`; the comprehension's witness `(s, ℓ) ∈ F` forces `ℓ = δ(1, #s)` by canonical form, with no ambiguity in the displacement (every span in `F` has its displacement determined by its start). We write `slot_addrs(F) = X_F`.

`|slot_addrs(F)|` is a finite natural number (since `F` is a finite endset by ASN-0043's `Endset = ℘_fin(Span)`). For canonical-form `F`, `coverage(F) = (∪ x ∈ X_F : {t : x ≼ t})` — infinite in `T` when `X_F ≠ ∅`; what shape constraints check is the finite syntactic `slot_addrs(F)`.

The shape framework restricts every shape-conformant emission's `F` and `G` to canonical-slot form. The substrate as defined by ASN-0043 permits non-canonical endsets (L4); the shape framework rejects non-canonical emissions via Sh-conf below. This is a discipline imposed by the framework, not a substrate-level constraint.

**Lemma — AllocatedAddressAntichain.** For every reachable state `Σ` at a substrate-conforming layer (which, by the framework-wide commitment surfaced in *Scope and Substrate Scaffolding*, honors the `subspace_I(·) = E(·).1` identification), and every `x ∈ A^Σ`:

`cov_allocated({(x, δ(1, #x))}, Σ) = {x}`

*Element-level character of `A^Σ`.* Every address in `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` is element-level: link side by L1 + L1b (`zeros = 3`, `#E ≥ 2`); content side by the element-level content-address scaffolding clause. Under the framework-wide `subspace_I(·) = E(·).1` invariant, the bare hypothesis `x ∈ A^Σ` suffices for both the span well-formedness check (`#x ≥ 1` by T0) and the element-level case analysis below.

*Proof.* `coverage({(x, δ(1, #x))}) = {t : x ≼ t}` by PrefixSpanCoverage. The intersection with `A^Σ` is `S := {a ∈ A^Σ : x ≼ a}`. By Prefix reflexivity (ASN-0034), `x ∈ S`. For the reverse, fix `a ∈ S`; we show `a = x` by case on the domains.

*Case 1* (`x, a ∈ dom(Σ.L)`): By R0a (FlatLinkDomain, ASN-0086), `dom(Σ.L)` is a tumbler-prefix antichain, so `x ≼ a ⟹ x = a`.

*Case 2* (`x, a ∈ dom(Σ.C)`): By the content-store antichain assumption (Scope and Substrate Scaffolding above), `dom(Σ.C)` is a tumbler-prefix antichain, so `x ≼ a ⟹ x = a`.

*Case 3* (`x` and `a` lie in different domains). Sub-case 3a treats `x ∈ dom(Σ.L), a ∈ dom(Σ.C)`; Sub-case 3b treats `x ∈ dom(Σ.C), a ∈ dom(Σ.L)`. By L1 (LinkElementLevel, ASN-0043) and L1c (LinkAllocatorConformance, ASN-0043) on the link side — which via T10a.4 supplies T4-validity for every link-side address — together with the element-level content-address scaffolding clause on the content side — which supplies T4-validity directly for every content-side address — both `x` and `a` are element-level (`zeros(x) = zeros(a) = 3`) and T4-valid in either sub-case; Step 3.2 below establishes E-field non-emptiness (`#E(·) ≥ 1`) from T4's last-position non-zero clause `t_{#t} ≠ 0` alone (well-formed because both `x` and `a` are T4-valid), so both `E(x).1` and `E(a).1` are well-defined.

*Case-symmetry across Sub-cases 3a and 3b.* Both sub-cases share `x ≼ a` and discharge Steps 3.1 and 3.2 identically (those steps depend only on the prefix relation and the shared `zeros = 3` constraint, neither of which references domain membership). The sub-cases diverge only at Step 3.3, where the subspace partition scaffolding assigns `E(·).1` based on domain membership. The Step-3.3 disjointness predicate `s_L ≠ s_C` is symmetric, so the two sub-cases yield identical contradictions with side-labels swapped.

*Step 3.1 — Shared zero positions.* From `x ≼ a` (Prefix): `#x ≤ #a` and `aᵢ = xᵢ` for `1 ≤ i ≤ #x`. The zero-index set `Z_x := {i : 1 ≤ i ≤ #x ∧ xᵢ = 0}` has cardinality 3 (Case 3 hypothesis); enumerate its elements as `n_1 < n_2 < n_3` under T0's strict ℕ-order. Componentwise agreement gives `{n_1, n_2, n_3} ⊆ Z_a := {i : 1 ≤ i ≤ #a ∧ aᵢ = 0}`, both sides of cardinality 3, so `Z_a = {n_1, n_2, n_3}` (equal-cardinality subsets of finite ℕ-sets are equal).

*Step 3.2 — E-field first-position agreement.* The E-field of `x` is non-empty (we need only `#E(x) ≥ 1`, not the stronger `≥ 2` from L1b or its content-side analog, since Step 3.2's conclusion uses only the first position of `E(x)`): T4's last-position non-zero clause `t_{#t} ≠ 0` applied to `x` gives `x_{#x} ≠ 0`, while `x_{n_3} = 0`, so `n_3 ≠ #x`; combined with `n_3 ≤ #x` (since `n_3` is a position of `x`) this gives `n_3 < #x`, i.e., `#x − n_3 ≥ 1`. The E-field's positional range `n_3 + 1 .. #x` and the resulting length identity `#E(x) = #x − n_3` are read off T4a (SyntacticEquivalence, ASN-0034) — T4a identifies field segments as maximal contiguous non-zero sub-sequences delimited by the zeros, fixing the E-field as the segment after the third zero `n_3` — combined with T4b (UniqueParse, ASN-0034), which makes that segment a uniquely computable projection of `x`, and T4c (LevelDetermination, ASN-0034), which identifies the `zeros = 3` case with the four-field (N, U, D, E) hierarchy so the segment after `n_3` is labeled as the E-field. So `#E(x) ≥ 1`, and the first E-field position `E(x).1` is defined. The same E-field non-emptiness holds for `a` by the symmetric application of T4's last-position non-zero clause at `a`. By T4a + T4b + T4c (ASN-0034) applied independently to `x` and `a` — both element-level and sharing the same three zero positions `n_1 < n_2 < n_3` — the E-field of `x` occupies positions `n_3 + 1 .. #x` and the E-field of `a` occupies positions `n_3 + 1 .. #a` (T4a supplies the segment-between-zeros formula; T4b supplies uniqueness; T4c supplies the level-to-segment labeling); the index offset `E(·).j = ·_{n_3 + j}` for `1 ≤ j ≤ #E(·)` follows from the same triple. The componentwise agreement `xᵢ = aᵢ` on `1 ≤ i ≤ #x` from `x ≼ a`, instantiated at `i = n_3 + 1` (which satisfies `n_3 + 1 ≤ #x` since `#E(x) ≥ 1`), yields `x_{n_3 + 1} = a_{n_3 + 1}`; substituting the T4a + T4b + T4c index offset on both sides (taking `j = 1`) gives `E(x).1 = E(a).1`. This step holds in both sub-cases because the T4-validity citations and the T4a + T4b + T4c E-field structure apply uniformly to element-level addresses without reference to subspace identifier.

*Step 3.3a — Subspace contradiction (Sub-case 3a: `x ∈ dom(Σ.L), a ∈ dom(Σ.C)`).* The link subspace partition scaffolding gives `E(x).1 = s_L` directly (`x ∈ dom(Σ.L)`); the content subspace partition scaffolding gives `E(a).1 = s_C` directly (`a ∈ dom(Σ.C)`); the *Content subspace partition* scaffolding clause fixes `s_L ≠ s_C`. But Step 3.2 gives `E(x).1 = E(a).1`. Substituting, `s_L = s_C`, contradicting the scaffolding's disjointness. Sub-case 3a vacuous.

*Step 3.3b — Subspace contradiction (Sub-case 3b: `x ∈ dom(Σ.C), a ∈ dom(Σ.L)`).* The content subspace partition scaffolding gives `E(x).1 = s_C` directly (`x ∈ dom(Σ.C)`); the link subspace partition scaffolding gives `E(a).1 = s_L` directly (`a ∈ dom(Σ.L)`); the *Content subspace partition* scaffolding clause fixes `s_C ≠ s_L`. But Step 3.2 gives `E(x).1 = E(a).1`. Substituting, `s_C = s_L`, contradicting the scaffolding's disjointness. Sub-case 3b vacuous. The three substantive moves (subspace assignment on `x`, subspace assignment on `a`, disjointness invocation) parallel Sub-case 3a's Step 3.3a with the identifier names exchanged at sites (1) and (2); site (3)'s disjointness predicate `s_L ≠ s_C` is symmetric and licenses the same contradiction in both readings (per the *Dependence audit* in the Case-symmetry preamble above).

Both sub-cases of Case 3 are vacuous. ∎

*Worked example — Case 3 (cross-domain).* Fix subspace identifiers `s_C = 5`, `s_L = 7`. Take `x = [1, 0, 2, 0, 1, 0, 7, 1] ∈ T` (length 8, zeros at positions 2, 4, 6, satisfying T4) and suppose `x ∈ dom(Σ.L)` with `E(x).1 = s_L = 7`. Take `a = [1, 0, 2, 0, 1, 0, 7, 1, 5]` extending `x` and suppose toward contradiction `a ∈ dom(Σ.C)` with `x ≼ a`. Step 3.1 gives `Z_x = Z_a = {2, 4, 6}`; Step 3.2 gives `a_7 = x_7 = 7` so `E(a).1 = 7`. Step 3.3a forces `E(a).1 = s_C = 5`, contradicting `7 = 5` against `s_L ≠ s_C`. Sub-case 3b is symmetric under side-label exchange — the worked example replays identically with `x ∈ dom(Σ.C)` and `a ∈ dom(Σ.L)`, with the disjointness predicate reading `s_C ≠ s_L`. The configurations the example uses are themselves ruled out by the lemma being proved; the example exhibits the contradiction concretely under the supposition.

The lemma underwrites the syntactic-to-semantic bridge: a canonical-slot endset at an allocated address `x` denotes exactly `{x}` among allocated addresses, so `slot_addrs(F) = {x}` matches "what allocated address does this slot refer to" with no ambiguity. Without this lemma, "the slot at `x`" could resolve to multiple allocated addresses when `x` has allocated descendants — which is precisely what the antichain rules out at element level.


## Shape

**Definition — Shape.** A *shape* is a tuple

`Sh_K = (c_F, c_G, t_F, t_G, idem)`

with components:

- `c_F, c_G ∈ {0, 1, *, 0|1}` — *cardinality bounds* on the slot-address counts `|slot_addrs(F)|` and `|slot_addrs(G)|`. The values 0 and 1 are exact; `*` denotes "any natural number"; `0|1` denotes "0 or 1 exactly."
- `t_F, t_G` — *target-domain restrictions*. Each is one of the symbolic constants `A_doc`, `A_rel`, `A`, or the distinguished value `-` (used when the corresponding cardinality is `0`). At each state Σ the symbol expands to the corresponding allocated set: `A_doc ↦ A_doc^Σ = dom(Σ.C)`, `A_rel ↦ A_rel^Σ = dom(Σ.L)`, `A ↦ A^Σ = A_doc^Σ ∪ A_rel^Σ`, `- ↦ -^Σ = ∅` (the empty set, used only when the corresponding cardinality is `0`, in which case `X_F ⊆ ∅ ⟺ X_F = ∅`, which holds by `c_F = 0`).
- `idem ∈ {⊤, ⊥}` — the *idempotency flag*.

**Definition — ShapeWellFormedness.** A shape `Sh_K = (c_F, c_G, t_F, t_G, idem)` is *syntactically well-formed* iff all four of the following implications hold:

- `c_F = 0 ⟹ t_F = -`
- `t_F = - ⟹ c_F = 0`
- `c_G = 0 ⟹ t_G = -`
- `t_G = - ⟹ c_G = 0`

The shape registry admits only well-formed shapes.

**Definition — CardinalityMatch.** For `n ∈ ℕ` and `c ∈ {0, 1, *, 0|1}`:

`match(n, c) ≡ (c = 0 ∧ n = 0) ∨ (c = 1 ∧ n = 1) ∨ (c = * ∧ n ∈ ℕ) ∨ (c = 0|1 ∧ n ∈ {0, 1})`

**Definition — TypedRelationCatalog.** Fix a distinguished set `T_cat ⊆ T_admissible` *finite up to `~`* (equivalently, the quotient `T_cat / ~` is finite) that is *closed under coverage-equivalence* (ASN-0086, `~` definition): `K ∈ T_cat ∧ K ~ K' ⟹ K' ∈ T_cat`. Equivalently, `T_cat` is the union of finitely many `~`-equivalence classes; each class is itself infinite as an endset set (many endsets share the same coverage by L5, ASN-0043), but only finitely many classes appear in the catalog. Concretely, `T_cat` is specified by listing one representative per class, with closure under `~` implicit. "Finite distinguished set" in earlier drafts is misleading: a non-empty `~`-class has infinitely many endset members, so `T_cat` itself is not finite as a set of endsets — finiteness lives at the quotient level.

*Decidable membership.* Because `T_cat` is closed under `~` and finite at the quotient level, the predicate `K ∈ T_cat` is the coverage-class membership test `[K] ∈ T_cat / ~` — equivalently, "there exists `K'` in the registered representative list with `K ~ K'`". The test is decidable on arbitrary `K ∈ T_admissible` by checking `coverage(K) = coverage(K_rep)` against each of the finitely many registered representatives `K_rep`: coverage is a pure function of the endset value (Definition — Coverage, ASN-0043), and coverage-equality of two finite span sets is decidable per the derivation below. The membership predicate is therefore *not* a literal-equality test on the endset value `K` itself (which would reject every coverage-equivalent endset whose value differs from the listed representative); it is a coverage-equivalence test against the representative list. Subsequent prose referring to "the membership test `K ∈ T_cat`" or to "the literal membership test" abbreviates this coverage-equivalence check; the word "literal" applies to the registry's representative list (literally enumerated) and to the well-definedness of the check (no state-indexed quantification), not to the comparison operation on endsets (which is coverage-equivalence, not value-equality).

*Decidability of coverage-equality on finite span sets.* For any finite endset `E`, `coverage(E)` is a finite union of half-open intervals under T1. To test `coverage(E) = coverage(E')`: (1) compute both endpoint sets (T1, TumblerAdd); (2) sort their union under T1 (T2) into intervals delimited by consecutive endpoints; (3) test each delimited interval for membership in each coverage via a representative point (T1/T2); (4) equality holds iff every delimited interval has matching outcomes. The procedure is polynomial in `n + n'` and uses only T1/T2/T12/TumblerAdd, with no canonical-slot precondition.

*Lifetime constancy of `T_cat`.* The set `T_cat` is fixed at the substrate's initial state `Σ_init` and does not change as states evolve: at every reachable state Σ, the registered catalog is the same set `T_cat` declared at `Σ_init`. The lifetime constancy is required for the inductive baselines of Sh0–Sh4 to discharge uniformly. Each induction begins with "At `Σ_0`, every `L_K^{Σ_0} = ∅`; the universal quantifier is vacuous." A K admitted to `T_cat` only after some prior states have elapsed would face a non-vacuous baseline at its registration point — `L_K^{Σ_registered}` could be non-empty from class-(iii) emissions at coverage-equivalent type indices issued before K joined `T_cat` — and the induction's base case would not discharge. The framework forbids runtime extension of `T_cat`: layers that wish to introduce new typed relations must declare them at `Σ_init`, or face the burden of verifying `L_K^{Σ_registered} = ∅` at the registration point (equivalent to the framework's empty-baseline assumption).

For any `K ∈ T_admissible \ T_cat` (equivalently, every member of every class not represented), no shape is registered. The substrate's shape-conformance gate rejects `Emit_K` at unregistered types — the membership test `K ∈ T_cat`, decidable as the coverage-equivalence check against the representative list per the *Decidable membership* paragraph above (see Sh-conf below).

**Definition — ShapeRegistry.** A function

`shape : T_cat → Shape`

assigns each registered type its shape. Two properties:

- *Per-class constancy.* For `K, K' ∈ T_cat` with `K ~ K'`: `shape(K) = shape(K')`. The function `shape` factors through `T_cat / ~`.
- *Lifetime constancy.* `shape` is fixed across the substrate's lifetime; it does not change as states evolve.

*Registration interface.* The layer registers one representative endset `K_rep` per `~`-equivalence class in `T_cat / ~` (the same `K_rep` used in `T_cat`'s representative list) together with `shape(K_rep) ∈ Shape`. For any `K ∈ T_cat`, the registry resolves `shape(K)` by finding the unique `K_rep` with `K ~ K_rep` and returning `shape(K_rep)`. Per-class constancy follows by construction: `K ~ K'` resolves to the same representative, hence the same shape.

Lifetime constancy is a substrate-level commitment, not derivable from R0…R7a. It is what lets Sh-conf evaluate emissions against a stable shape that matches the shape under which prior tuples of the same type were emitted, so the inductive proofs of Sh0–Sh3 can rely on a fixed conformance predicate. Mutable shape re-registration (e.g., relaxing a cardinality bound after some tuples are already emitted) would invalidate the induction; the framework forbids it. The lifetime constancy at the registry level reads as: the representative list `T_cat / ~` and the function `shape ∘ (·/~)` are both fixed at `Σ_init` and do not change as states evolve.

**Definition — Conformance.** A tuple `(a, F, G) ∈ L_K^Σ` (with `K ∈ T_cat`) is *shape-conformant at state Σ* iff all of the following hold:

(a) `F` is in canonical-slot form; let `X_F = slot_addrs(F)`.
(b) `G` is in canonical-slot form; let `X_G = slot_addrs(G)`.
(c) `match(|X_F|, shape(K).c_F) ∧ match(|X_G|, shape(K).c_G)`.
(d) `X_F ⊆ shape(K).t_F^Σ ∧ X_G ⊆ shape(K).t_G^Σ`, with the symbolic `t` expanded per the Shape definition. When `t_F = -` (only legal under `c_F = 0`), the F-side of (d) is vacuously satisfied since `X_F = ∅`; symmetric for G.

Write `conf_K^Σ(F, G)` for this predicate.

*Structural gates.* Clauses (a) and (b) jointly form the **canonical-form gate** (one gate, two operands); clause (c) is the **cardinality gate**; clause (d) is the **target-domain gate**. Three independent gates, each rejecting independently. When the worked examples below refer to "Sh-conf's three independently-checked structural gates", they index the canonical-form, cardinality, and target-domain gates in that order; a non-canonical F (clause (a)) and a non-canonical G (clause (b)) are distinguishable as clause-level failures but both fall under the same gate.

*State-dependence and monotone discharge.* Conformance is state-indexed because clause (d) depends on the allocated sets `A_doc^Σ, A_rel^Σ, A^Σ`. These sets grow monotonically along `⊑̂`: `Σ ⊑̂ Σ'` entails `A^Σ ⊆ A^{Σ'}` and analogous for the partition sets (by L12a, ASN-0043, for `dom(Σ.L)` and by the content-store monotonicity scaffolding assumption (Scope and Substrate Scaffolding) for `dom(Σ.C)`). Therefore `conf_K^Σ(F, G) ⟹ conf_K^{Σ'}(F, G)` for every `Σ ⊑̂ Σ'`: once conformant, a tuple remains conformant under every reachable future state. This monotonicity is what permits the inductive arguments of Sh0–Sh3 to commute with arbitrary `↦*` transitions.


## The Conformance Axiom

**Sh-conf — ShapeConformanceAxiom.** The framework restricts `Emit_K` by adding two preconditions: `K ∈ T_cat` and `conf_K^Σ(F, G)`. Combined success condition: `Emit_K(Σ, d, F, G)` succeeds iff `d ∈ dom(Σ.M)` *and* `K ∈ T_cat` *and* `conf_K^Σ(F, G)`. On any failure, `Emit_K` returns `⊥` and leaves state unchanged; the return type extends from `Σ' × A_rel^{Σ'}` to `(Σ' × A_rel^{Σ'}) ∪ {⊥}`. Per-K discipline contracts (Sh4, FDD, SHCD) also return `⊥` on suppression. Callers can invoke the candidate-set queries `C_K`/`C_fd_K` or the *Caller-side rejection classification* protocol below to distinguish rejection causes.

**Definition — LayerCallableCandidateSets.** For each `K ∈ T_cat`, the framework exposes the following layer-callable candidate-set queries:

`C_K : Endset × Endset × Σ → ℘_fin(A_K^Σ)` defined when `shape(K).idem = ⊤` (i.e., K registered under the *Sh4 idempotency contract*):

`C_K(F, G, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)}`

`C_fd_K : Endset × Σ → ℘_fin(A_K^Σ)` defined when K is registered under the *FDD functional-dependency contract*:

`C_fd_K(F, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}`

Both queries are side-effect-free reads of the framework's relational state at Σ. `C_K(F, G, Σ)` is computed via `Observe_K(slot_addrs(F), slot_addrs(G), oper)` followed by an exact slot-pair-equality postfilter; `C_fd_K(F, Σ)` via `Observe_K(slot_addrs(F), ∅, oper)` followed by exact F-slot-equality postfilter. Well-formedness on canonical-slot F, G is inherited from Sh0/Sh1; the post-filter's exact-equality test is decidable in finite time. Callers use these queries to disambiguate Sh-conf rejection from per-K-discipline suppression before issuing `Emit_K`. The *single-home commitment* requires no candidate-set query — its check is the literal-equality test `d = d_K`.

**Definition — CallerSideClassification.** A caller wanting fine-grained classification of an `Emit_K` rejection cause invokes the following six side-effect-free checks in order, halting at the first failure to identify the rejecting gate (numbering mirrors the *Gate Ordering (consolidated)* below):

1. *Registry check* — Test `K ∈ T_cat` via the coverage-equivalence check against the registered representative list (per the *Decidable membership* paragraph in the TypedRelationCatalog Definition). Failure ⇒ registry rejection.
2. *Single-home check* (if K registered under SingleHomeCoverageDiscipline) — Test `d ?= d_K` against the per-K registration constant. Failure ⇒ single-home rejection.
3. *Canonical-form check* — Test whether F and G are each in canonical-slot form (per the CanonicalSlotForm Definition; the test is decidable on a finite endset by reading each span's start and verifying its displacement equals `δ(1, #start)`). Failure ⇒ canonical-form rejection.
4. *Discipline-suppression check* (if K registered under the *Sh4 idempotency contract* or the *FDD functional-dependency contract*) — Invoke `C_K(F, G, Σ)` (Sh4) or `C_fd_K(F, Σ)` (FDD) per the LayerCallableCandidateSets Definition above. Non-empty ⇒ discipline-suppression rejection.
5. *Cardinality check* — Test `match(|slot_addrs(F)|, shape(K).c_F)` and `match(|slot_addrs(G)|, shape(K).c_G)`. Failure ⇒ cardinality rejection.
6. *Target-domain check* — Test `slot_addrs(F) ⊆ shape(K).t_F^Σ` and `slot_addrs(G) ⊆ shape(K).t_G^Σ`. Failure ⇒ target-domain rejection.

A caller that passes all six checks may issue `Emit_K(Σ, d, F, G)` and expects the substrate K.λ-step to fire. The protocol uses only side-effect-free reads; running it ahead of `Emit_K` introduces no `↦`-step.

*Scope.* Sh-conf binds `Emit_K`, not K.λ. Chain-discipline and invariant-catalog facts (R0a-Cor1, R0a-Cor2, etc.) flow through the scaffolding clauses.

*Gate Ordering (consolidated).* The framework's per-K disciplines and Sh-conf's structural gates fire at every `Emit_K(Σ, d, F, G)` call site in a fixed sequence. Each per-K discipline contract specifies its local *Ordering with Sh-conf* clause (see the *Sh4 idempotency contract* section, the *FDD functional-dependency contract* sub-section, and the *single-home commitment* sub-section). The aggregate gate ordering at a call site for K with any registered discipline reads as follows:

1. **Single-home check** (if K registered under SingleHomeCoverageDiscipline): literal-equality test `d ?= d_K`. No `Observe_K` invocation, no state-dependent computation. On mismatch (`d ≠ d_K`), the *single-home commitment* clause (i) rejects the call outright with `⊥` and no subsequent gate fires. On match, the call proceeds to gate 2. (Skipped entirely at K not registered under SHCD.)

2. **Sh-conf canonical-form gate** (Sh-conf clauses (a) and (b)): test that `F` and `G` are each in canonical-slot form. On failure, `Emit_K` returns `⊥`; no subsequent per-K discipline contract fires (the per-K contracts' Observe steps would consume `slot_addrs(F)`/`slot_addrs(G)`, which are undefined for non-canonical endsets). On pass, the call proceeds to gate 3.

3. **Per-K Observe-then-Emit contract** (if K registered under Sh4 idempotency or FDD): either the *Sh4 idempotency contract* (when `shape(K).idem = ⊤` and K is not under FDD) or the *FDD functional-dependency contract* (when K is FDD-registered), executing clauses (i)–(iii) — Observe the candidate set, post-filter, then suppress or issue. On suppression (clause (ii) of either contract), `Emit_K` returns `⊥` and no subsequent gate fires. On issue (clause (iii)), the call proceeds to gate 4. (Skipped entirely at K not registered under any Observe-then-Emit discipline.)

4. **Sh-conf cardinality/target-domain gates** (Sh-conf clauses (c) and (d)): cardinality `match` on `|slot_addrs(F)|` and `|slot_addrs(G)|`; target-domain inclusion `slot_addrs(F) ⊆ t_F^Σ` and `slot_addrs(G) ⊆ t_G^Σ`. On failure of any conjunct, `Emit_K` returns `⊥`. On pass, the call proceeds to gate 5.

5. **Substrate primitive K.λ** (ASN-0086): the call invokes K.λ at home `d` with value `(F, G, K)`. K.λ's first/subsequent-emission protocol fires, depositing the new tuple at the fresh address `a_emit(Σ, d)`. The call returns `(Σ', addr) ∈ Σ' × A_rel^{Σ'}`.

FDD and SHCD cannot co-register at the same K (their required `idem` flags differ); at most one of gates 1 (SHCD) and 3 (FDD) fires per call site, and gate 3's Sh4 sub-branch fires only when K is not under FDD.


## Nullify Compatibility

*Baseline registration requirement.* The retraction type `R` (ASN-0086, Definition — RetractionType) is registered in `T_cat` with `shape(R) = (*, 1, A, A_rel, ⊤)`. R-registration is mandatory for any layer instantiating the framework; without it every `Emit_R` call fails Sh-conf's `K ∈ T_cat` conjunct.

*Sh-conf admits every well-formed Nullify call.* With R registered: `F = ∅` matches `c_F = *`, `∅ ⊆ A^Σ` vacuously; `G = {(a, δ(1, #a))}` is canonical-slot, matches `c_G = 1`, `{a} ⊆ A_rel^Σ` by Nullify's P1.

*Supersession of ASN-0086's Nullify-as-sole-R-producer route.* The Retraction shape `(*, 1, A, A_rel, ⊤)` admits any canonical-slot `F` (including `F ≠ ∅`). The unit-depth G-form (and hence ASN-0086's automatic `NoCraftedSpanReachesD` discharge) is preserved by Sh-conf's `c_G = 1` plus canonical-slot gates on G.

*Audit-slice set-semantics at the bare-Nullify alias.* Under `shape(R).idem = ⊤`, two consecutive bare-form `Nullify(Σ, d_retr, a)` calls at the same target produce *one* tuple in `L_R^Σ`, not two: the second is suppressed by the Sh4 contract. Layers needing per-event audit multiplicity use *attributed retraction* — `Emit_R(Σ, d_retr, {(c, δ(1, #c))}, {(a, δ(1, #a))})` with a distinguishing caller-context address `c ∈ A^Σ` — which Sh4 admits as a distinct slot-pair.

**Corollary — NullifyActiveSubsetCompatibility.** Under the Sh4 idempotency contract with R registered, every `Nullify(Σ, d_retr, a)` call satisfying ASN-0086's P0/P1/P2 delivers the active-subset content of ASN-0086's Nullify postcondition at `Σ_target`: (i) `{t : a ≼ t} ∩ A_rel^{Σ_target} = {a}`; (ii) `a ∈ nullified(Σ_target)` stable under R6a. This holds whether clause (iii) issues (`Σ_target := Σ'`) or clause (ii) suppresses (`Σ_target := Σ`). Audit-slice multiplicity is not preserved.

*Proof.* *Case A (issue, `C = ∅`).* Deposits `τ_new` with `G_{τ_new} = {(a, δ(1, #a))}`. (i) R0a at Σ' + `a ∈ A_rel^{Σ'}` (P1, L12a). (ii) `a ∈ coverage(G_{τ_new})` by PrefixSpanCoverage + reflexivity; `nullified` Definition gives the conclusion; R6a stabilizes. *Case B (suppress, `C ≠ ∅`).* `Σ_target := Σ`. (i) R0a at Σ + P1. (ii) Pick `τ_prior ∈ C`; `slot_addrs(G_{τ_prior}) = {a}` forces `a ∈ coverage(G_{τ_prior})`; `nullified` Definition gives `a ∈ nullified(Σ)`; R6a stabilizes. ∎


## Initial-State Baseline

*Initial-state baseline for preservation proofs.* Sh0–Sh4 presuppose `L_K^{Σ_init} = ∅` for every `K ∈ T_cat`. References to `Σ_0` in proofs denote this `Σ_init`. States reached before the *Emit_K routing commitment* was honored are outside the framework's scope.

*Global empty-link-store assumption (walkthrough convention).* The walkthroughs below assume the stronger `dom(Σ_init.L) = ∅` globally so K.λ's first-emission predicate fires uniformly at each walkthrough's first emission. This is a notational simplification, not a framework requirement — preservation theorems discharge from the per-K empty baseline `L_K^{Σ_init} = ∅` for `K ∈ T_cat` alone.

*Scope of the per-tuple-conformance relaxation.* "Every tuple in `L_K^{Σ_init}` satisfies `conf_K^{Σ_init}`" suffices for Sh0–Sh3 (whose universals quantify over single tuples), but *not* for Sh4 (pairwise slot-pair distinctness), FDD (pairwise from-slot uniqueness), or SHCD (the homed-set universal). For Sh4/FDD/SHCD the empty-baseline `L_K^{Σ_init} = ∅` is required.

*Per-walkthrough convention.* Every walkthrough below assumes: `T_cat` declared at `Σ_init`; R registered with `shape(R) = (*, 1, A, A_rel, ⊤)`; `L_K^{Σ_init} = ∅` for every `K ∈ T_cat`; `dom(Σ_init.L) = ∅` globally. Each walkthrough's "Registered catalog" paragraph declares only what is distinctive.


## Lemma — LinkAddressNotPrefixOfEmit

This lemma bridges Sh-conf's structural gates to `wp_086` simplification at Retraction-typed emissions. Independent of Sh0–Sh4.

**Lemma — LinkAddressNotPrefixOfEmit.** Let Σ be reachable from `Σ_init` under the framework's *Emit_K routing commitment*. For every `b ∈ dom(Σ.L)` and every `d ∈ dom(Σ.M)`:

`b ⋠ a_emit(Σ, d)`

*Generality.* The Lemma is stated about an *arbitrary* link-store address `b ∈ dom(Σ.L)`, not specifically about retraction-tuple slot addresses. This generalization is sound — the proof below uses only `b ∈ dom(Σ.L)` and `d ∈ dom(Σ.M)`, with no appeal to `b`'s membership in any particular slot of any particular relation — and it makes the Lemma directly applicable at both consumption sites in the EffectiveWpSimplification Corollary below: discharging `NoCraftedSpanReachesD(Σ, d)` (where `b` ranges over the slot addresses of *prior* R-tuples' G-endsets) and discharging the `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` disjunct under `K ~ R` (where `b` is the slot address of the *new* emission's G-endset under Sh-conf admittance). Both sites supply `b ∈ dom(Σ.L)` through Sh-conf clause (d) at `t_G = A_rel` of Retraction's catalog row.

*Proof.* Case-split on whether `b` and `a_emit(Σ, d)` share a home.

*Identification of `origin(·)` and `home(·)` for the proof's scope.* ASN-0086's FreshEmissionAddress states the first-emission gating predicate as `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}`, while R0a-Cor1 states the contiguous-prefix postcondition over `{a ∈ dom(Σ.L) : home(a) = d}`. The two projections refer to the same per-address projection — `origin(·)` is FreshEmissionAddress's name and `home(·)` is L1a's name (`home(a) = N(a).0.U(a).0.D(a)`) for the same function. The substrate-conforming layer's *Per-document link sub-allocator chains* scaffolding clause enumerates `{ℓ : home(ℓ) = d}` as the same chain whose enumeration FreshEmissionAddress and R0a-Cor1 jointly characterize, fixing the identification `origin(·) = home(·)` on element-level link addresses. We use `home(·)` throughout this proof and treat FreshEmissionAddress's `origin(·)` as the same function under this identification.

*Case I — `home(b) = d`.* Both `b` and `a_emit(Σ, d)` lie in `A_L(d)`'s chain enumeration — chain membership here is sourced through the *Per-document link sub-allocator chains* scaffolding clause (which is itself surfaced via ASN-0086's `SubstrateConformingLayer` Definition, not via any non-foundation ASN); the scaffolding clause enumerates `{ℓ : home(ℓ) = d}` as `A_L(d)`'s chain, so any `ℓ ∈ dom(Σ.L)` with `home(ℓ) = d` is a chain element of `A_L(d)` by direct unfolding of the scaffolding's enumeration. The case hypothesis `home(b) = d` together with `b ∈ dom(Σ.L)` places `b` in the homed set at `d`, so the homed set is non-empty; by R0a-Cor1 (ContiguousPrefix, ASN-0086) this forces `J_d^Σ ≥ 0` (the `J_d^Σ = -1` sentinel encodes an empty homed set, which the case hypothesis rules out), and `b` is enumerated at some chain index `0 ≤ i ≤ J_d^Σ` via `b = inc^i(d.0.s_L.1, 0)`. *FreshEmissionAddress branch forced under Case I.* Because the homed set at `d` is non-empty under the case hypothesis, FreshEmissionAddress (ASN-0086) selects the *subsequent-emission* branch (the first-emission branch's gating predicate `{ℓ' ∈ dom(Σ.L) : home(ℓ') = d} = ∅` — rewritten using the identification above — is *false* in Case I, since it contains at least `b` by the case hypothesis). The subsequent-emission branch sets `a_emit(Σ, d) = inc(ℓ_prev, 0)` where `ℓ_prev = max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` under T1; by R0a-Cor1 this maximum is the chain element at index `J_d^Σ`, so `a_emit(Σ, d) = inc^{J_d^Σ + 1}(d.0.s_L.1, 0)` lies at chain index `J_d^Σ + 1`. By the *Uniform link sub-allocator chain length* scaffolding clause (Scope and Substrate Scaffolding), `#b = #a_emit(Σ, d)`. By T10a.7 (EnumerationInjectivity, ASN-0034) applied to the chain at `A_L(d)`, distinct chain indices yield distinct tumblers; since `b`'s chain index `i ≤ J_d^Σ < J_d^Σ + 1 = a_emit(Σ, d)`'s chain index, `b ≠ a_emit(Σ, d)`. Two equal-length distinct tumblers are prefix-incomparable: if `b ≼ a_emit(Σ, d)`, then by Prefix (ASN-0034) the length clause `#b ≤ #a_emit(Σ, d)` combined with equal lengths forces componentwise agreement on all of `1..#b = 1..#a_emit(Σ, d)`, which by T3 (CanonicalRepresentation, ASN-0034) makes them identical — contradiction. So `b ⋠ a_emit(Σ, d)`.

*Case II — `home(b) ≠ d`.* Suppose toward contradiction `b ≼ a_emit(Σ, d)`. Set `a := a_emit(Σ, d)`. From Prefix (ASN-0034), `b ≼ a` unfolds to `#b ≤ #a` and componentwise agreement `aᵢ = bᵢ` for `1 ≤ i ≤ #b`. The case structure mirrors AllocatedAddressAntichain's Case 3 — explicit numbered Steps II.1 (zero-count additivity establishes a shared zero-position layout), II.2 (T4b drives positionwise N/U/D agreement), II.3 (L1a delivers the home contradiction) — preceded by a length dispatch on `#b = #a` versus `#b < #a` that handles the equal-length degenerate case at the front of the argument rather than at the end. Throughout, both `b` and `a` are T4-valid: `b` by L1c → T10a.4 (L1c places `b ∈ dom(Σ.L)` in a T10a-conforming chain, T10a.4 propagates T4-validity to every chain output); `a` by TA5a (IncrementPreservesT4, ASN-0034) applied to the K.λ construction — for first-emission `a = [d.0.s_L.1]`, the construction satisfies T4 directly from `zeros(d) = 2` and `s_L > 0`, and for subsequent-emission `a = inc(ℓ_prev, 0)`, TA5a's preservation under `inc(·, 0)` applies to T4-valid `ℓ_prev` (T4-valid by L1c → T10a.4 at `ℓ_prev`). Both `b` and `a` carry `zeros = 3`: for `b` by L1 (LinkElementLevel, ASN-0043) on `b ∈ dom(Σ.L)`; for `a` by K.λ's construction — first-emission `a = [d.0.s_L.1]` carries two zeros from `zeros(d) = 2` (by the *Document address structure* scaffolding clause, Scope and Substrate Scaffolding) plus one zero from the separator at position `#d + 1`, with `s_L > 0` (by the *Link subspace partition* scaffolding clause's positivity commitment) and the trailing `1` both non-zero, totaling 3; subsequent-emission `a = inc(ℓ_prev, 0)` preserves zeros (TA5(c), ASN-0034, modifies only position `sig(ℓ_prev)`, and on T4-valid `ℓ_prev` the sig position carries a non-zero value whose incremented value remains non-zero) from `zeros(ℓ_prev) = 3` (L1 at `ℓ_prev`).

*Length dispatch (sub-case II.A: `#b = #a`).* By T3 (CanonicalRepresentation, ASN-0034) applied to the equal-length componentwise agreement, `b = a`. The function `home(·) := N(·).0.U(·).0.D(·)` is a deterministic projection (well-defined on T4-valid addresses with `zeros = 3` via T4b, regardless of `dom(Σ.L)` membership), so equal arguments produce equal outputs: `home(b) = home(a)`. K.λ's construction gives `home(a) = d` in both emission branches. *First-emission branch.* `a = [d.0.s_L.1]` carries the document prefix `d` at positions `1..#d`; `d` itself has `zeros(d) = 2` (by the *Document address structure* scaffolding clause), so `a`'s third zero is the separator at position `#d + 1`. The prefix of `a` ending at position `#d` is `d`, so T4b's `home(a) = N(d).0.U(d).0.D(d) = d`. *Subsequent-emission branch.* `a = inc(ℓ_prev, 0)` where `ℓ_prev` is a chain element at `d` with `home(ℓ_prev) = d` (per the *Per-document link sub-allocator chains* scaffolding clause). By TA5 postcondition (c), `inc(·, 0)` modifies only position `sig(ℓ_prev)` and leaves every other position unchanged. On T4-valid `ℓ_prev` (established via L1c → T10a.4), TA5-SigValid gives `sig(ℓ_prev) = #ℓ_prev`, which by the *Uniform link sub-allocator chain length* scaffolding clause equals the chain's base length `#[d.0.s_L.1] = #d + 3`; hence `sig(ℓ_prev) = #d + 3 > #d + 1`, strictly past the third zero. So `inc(·, 0)` leaves positions `1..#d` and the third zero at position `#d + 1` untouched, and the T4b projection `N(·).0.U(·).0.D(·)` (which reads only positions `1..n_3 − 1 ≤ #d`) yields `home(inc(ℓ_prev, 0)) = home(ℓ_prev) = d`. Either branch gives `home(a) = d`. Hence `home(b) = d`, contradicting `home(b) ≠ d`. ∎ (II.A)

*Length dispatch (sub-case II.B: `#b < #a`).* We derive the home contradiction through Steps II.1–II.3.

*Step II.1 — All zeros of `a` lie at positions ≤ `#b`.* Let `Z_a := {i : 1 ≤ i ≤ #a ∧ aᵢ = 0}` and `Z_b := {i : 1 ≤ i ≤ #b ∧ bᵢ = 0}`. By componentwise agreement on `1..#b`, every `i ∈ Z_b` satisfies `aᵢ = bᵢ = 0`, hence `Z_b ⊆ Z_a`. Both sides have cardinality 3 (preamble), so equal-cardinality subsets of finite ℕ-sets force `Z_b = Z_a`. Hence every zero of `a` sits at some position ≤ `#b`; positions `#b + 1..#a` carry no zero of `a`. Enumerate the three shared zero positions in strict order as `n_1 < n_2 < n_3`.

*Step II.2 — N/U/D agreement via T4b's positional index ranges.* All of `n_1, n_2, n_3` lie in `1..#b`, so T4b's field projections — `N(·)` at `1..n_1 − 1`, `U(·)` at `n_1 + 1..n_2 − 1`, `D(·)` at `n_2 + 1..n_3 − 1` — also lie within `1..n_3 − 1 ≤ #b`. Componentwise agreement on `1..#b` gives `aᵢ = bᵢ` at every N/U/D position; the three identifications jointly deliver `N(a) = N(b) ∧ U(a) = U(b) ∧ D(a) = D(b)`.


*Step II.3 — Home contradiction.* `home(·) := N(·).0.U(·).0.D(·)` is a deterministic projection of any T4-valid `zeros = 3` address (T4b). Step II.2's three field equalities give `home(b) = home(a)`. K.λ's construction gives `home(a) = d`. Hence `home(b) = d`, contradicting `home(b) ≠ d`. ∎ (II.B)

Either sub-case yields `b ⋠ a_emit(Σ, d)`, closing Case II.

Either case yields `b ⋠ a_emit(Σ, d)`. ∎

*Worked examples — Cases I and II at concrete tumblers.* To exhibit both branches of the proof's case-split concretely, fix `s_L = 7` and a document `d = [1, 0, 2, 0, 3] ∈ dom(Σ.M)` with `#d = 5` and `zeros(d) = 2` (consistent with the *Document address structure* scaffolding clause).

*Case I example (same-home, distinct chain indices).* Suppose `dom(Σ_0.L) = ∅` and three link emissions occur at `d`, producing chain elements `ℓ_0, ℓ_1, ℓ_2` of `A_L(d)`:
- ℓ_0 at chain index 0: `a_emit(Σ_0, d) = [d.0.s_L.1] = [1, 0, 2, 0, 3, 0, 7, 1]` (first-emission branch).
- ℓ_1 at chain index 1: `a_emit(Σ_1, d) = inc(ℓ_0, 0) = [1, 0, 2, 0, 3, 0, 7, 2]` (subsequent-emission branch).
- ℓ_2 at chain index 2: `a_emit(Σ_2, d) = inc(ℓ_1, 0) = [1, 0, 2, 0, 3, 0, 7, 3]`.

Now at Σ_3 (after all three emissions), `a_emit(Σ_3, d) = inc(ℓ_2, 0) = [1, 0, 2, 0, 3, 0, 7, 4]` lies at chain index 3. Take `b := ℓ_0` (so `b ∈ dom(Σ_3.L)` with `home(b) = d`). By the *Uniform link sub-allocator chain length* scaffolding, `#b = #a_emit(Σ_3, d) = 8`. By T10a.7, chain index 0 ≠ chain index 3 ⟹ `b ≠ a_emit(Σ_3, d)`; direct verification: `b_8 = 1 ≠ 4 = a_emit(Σ_3, d)_8`. Suppose toward contradiction `b ≼ a_emit(Σ_3, d)`. With equal lengths, Prefix's componentwise-agreement clause forces componentwise equality on all 8 positions, hence `b = a_emit(Σ_3, d)` by T3 — contradicting the chain-index distinctness. So `b ⋠ a_emit(Σ_3, d)`. ✓

*Sub-case II.A example.* For `b' ∈ dom(Σ.L)` with `#b' = #a_emit(Σ, d)`, `home(b') ≠ d`, and `b' ≼ a_emit(Σ, d)`: Prefix's componentwise agreement covers every position of both tumblers, T3 collapses to `b' = a_emit(Σ, d)`, L1a gives `home(b') = d`, contradicting `home(b') ≠ d`.



## Cardinality (Sh0, Sh1)

**Sh0 — FromSlotCanonicalAndCardinalityFixed.** For each `K ∈ T_cat`, every tuple in `L_K^Σ` at every reachable state Σ has `F` in canonical-slot form with `|slot_addrs(F)|` matching `c_F`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: F is canonical-slot form ∧ match(|slot_addrs(F)|, shape(K).c_F))`

*Proof.* By induction on the broad transition relation `↦*` from the initial state `Σ_0`. Reachable states are reached under `↦*` (the broader relation including arrangement-modifying steps), not just `→*`, so the induction must cover both transition classes.

*Base case.* At `Σ_0 = Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Initial-State Baseline section above), every `L_K^{Σ_0} = ∅`; the universal quantifier is vacuous.

*Inductive step.* Suppose the property holds at Σ; let `Σ ↦ Σ'` be a single broad transition. Fix `K ∈ T_cat`. `L_K` is monotone non-decreasing along `↦*` (R3 on `→`-steps; LinkStoreInvarianceUnderArrangement on `↦ \ →`-steps), with strict increase confined to K.λ-steps emitting at K or a `~`-equivalent type. Split on whether the step affects `L_K`.

*Case A (`L_K^{Σ'} = L_K^Σ`).* Set extensionality: inherited from IH; existing tuples retain values by R2. Covers K.σ/K.α (frame preserves `Σ.L`), K.λ at `K' ≁ K` (the new tuple enters a disjoint `~`-class slice), and arrangement-modifying steps (LinkStoreInvarianceUnderArrangement).

*Case B (`L_K^{Σ'} = L_K^Σ ∪ {τ_new}`).* By the *Emit_K routing commitment*, an `Emit_K` call at K (or a `~`-equivalent K' with `shape(K') = shape(K)` by per-class constancy). Sh-conf clauses (a) and (c) give τ_new canonical-slot with `match(|slot_addrs(F)|, c_F)`. Existing tuples preserved by R2 + IH.

Quantifying over K closes the induction. ∎

**Sh1 — ToSlotCanonicalAndCardinalityFixed.** The G-side analog of Sh0:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: G is canonical-slot form ∧ match(|slot_addrs(G)|, shape(K).c_G))`

*Proof.* By induction on `↦*`. Case A by case-equation. Case B: Sh-conf clauses (b) and (c) discharge canonical-slot form and cardinality match on the new tuple. ∎


## Target Domain (Sh2, Sh3)

**Sh2 — FromSlotTargetRestricted.** For each `K ∈ T_cat`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(F) ⊆ shape(K).t_F^Σ)`

(vacuous when `t_F = -`). `slot_addrs(F)` is well-defined throughout by Sh0.

*Proof.* By induction on `↦*`. Case A by case-equation, with monotone preservation `t_F^Σ ⊆ t_F^{Σ'}` lifting the IH. Case B: Sh-conf clause (d) gives `X_F ⊆ t_F^Σ ⊆ t_F^{Σ'}` for τ_new. ∎

**Sh3 — ToSlotTargetRestricted.** Symmetric for `G`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(G) ⊆ shape(K).t_G^Σ)`

Well-formedness from Sh1. *Proof.* Mirrors Sh2 with F → G, clauses (b) and (d). ∎

*Retraction commutativity.* `A_K^Σ ⊆ L_K^Σ` (filtering by `nullified(·)`). Sh0–Sh3 quantify over `L_K^Σ`, so every tuple in `A_K^Σ` is shape-conformant.


## Corollary — EffectiveWpSimplification

**Corollary — EffectiveWpSimplification.** Let Σ be reachable from `Σ_init` under the *Emit_K routing commitment*, with `R ∈ T_cat`. *(Statement.)* At any call site where the framework's full gate stack (gates 1–4) admits `Emit_K(Σ, d, F, G)` — i.e., the call reaches substrate K.λ at gate 5 — ASN-0086's `wp_086` simplifies to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`. *(Effective wp at the framework's gate.)* Combining with each gate's admit conjunct, the framework's *effective wp* for the postcondition "a fresh `(a, F, G)` is deposited in `A_K^{Σ'}`" simplifies to

`wp_eff(Emit_K(Σ, d, F, G), fresh (a, F, G) ∈ A_K^{Σ'}) = d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G) ∧ Π_K(d, F, G, Σ)`

where `Π_K` is the per-K discipline non-suppression conjunct:
- `K-under-SHCD ⟹ d = d_K` (gate 1)
- `K-with-idem = ⊤ ∧ not-under-FDD ⟹ C(F, G, Σ) = ∅` (gate 3 under Sh4)
- `K-under-FDD ⟹ C_fd(F, Σ) = ∅` (gate 3 under FDD)

The three implications are mutually exclusive at any K (FDD and SHCD are structurally incompatible since they require distinct `idem` values; Sh4 fires automatically at idem = ⊤ K not under FDD). At a rejected call site, the failing gate's conjunct evaluates false, `wp_eff = false`, `Emit_K` returns `⊥`, and no tuple is deposited — the framework's `⊥`-return is exactly what `wp_eff = false` encodes. `Π_K` is necessary for the postcondition's *fresh-deposit* reading: at a discipline-suppressed call, the prior conjuncts `d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)` all hold, but no new tuple is deposited; only `Π_K` captures the suppression at the wp.

*Proof.* `wp_086` carries two non-trivial conjuncts beyond `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`: `NoCraftedSpanReachesD(Σ, d)` and `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`. Discharge each via Lemma — LinkAddressNotPrefixOfEmit.

*Step 1 — `NoCraftedSpanReachesD(Σ, d)`.* For every `(b̂, F', G') ∈ L_R^Σ`, Sh1 at `K := R` gives `G'` canonical-slot with `|slot_addrs(G')| = 1`; Sh3 at `K := R` gives `slot_addrs(G') ⊆ A_rel^Σ`. So `G' = {(b', δ(1, #b'))}` for `b' ∈ dom(Σ.L)`. The Lemma at `b := b'` gives `b' ⋠ a_emit(Σ, d)`, hence `a_emit(Σ, d) ∉ coverage(G')` by PrefixSpanCoverage. Quantifying over `L_R^Σ` discharges the conjunct.

*Step 2 — `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`.* Case A (`K ≁ R`): first arm holds. Case B (`K ~ R`): per-class constancy gives `shape(K) = shape(R) = (*, 1, A, A_rel, ⊤)`. The full gate stack's admit at gates 2/4 forces `G = {(b, δ(1, #b))}` with `b ∈ A_rel^Σ`; the Lemma at this new `b` gives `b ⋠ a_emit(Σ, d)`, so `a_emit(Σ, d) ∉ coverage(G)`.

*Step 3 — Assembly.* Steps 1 and 2 reduce `wp_086` to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`. Combined with gates 1–4's admit conjuncts (Sh-conf clauses (a)–(d) contribute `K ∈ T_cat ∧ conf_K^Σ(F, G)`; gates 1 and 3 contribute the `Π_K` implications), and absorbing `K ∈ T_admissible` into `K ∈ T_cat`, the named `wp_eff` form follows. ∎

*Coverage-class disjointness from R is enforced by step 0 of Sh5(b)'s checklist:* a new catalog row with shape tuple componentwise equal to R's must register `K_rep ~ R`; otherwise rejected. Per-class constancy then makes Case A's `K ≁ R` precondition supplied uniformly at every non-R catalog row.

Downstream proofs that need to reason about `Emit_K`'s preconditions cite this Corollary directly rather than re-deriving the simplification.


## Slot Accessors

The cardinality and target-domain lemmas together permit total slot accessor functions.

**Definition — SetSlotAccessors.** For each `K ∈ T_cat`, define at every state Σ:

`from_K^Σ : L_K^Σ → ℘_fin(shape(K).t_F^Σ)` &nbsp; with &nbsp; `from_K^Σ(a, F, G) = slot_addrs(F)`

`to_K^Σ   : L_K^Σ → ℘_fin(shape(K).t_G^Σ)` &nbsp; with &nbsp; `to_K^Σ(a, F, G) = slot_addrs(G)`

These are total on `L_K^Σ` for any shape: Sh0/Sh1 guarantee canonical-slot form (so `slot_addrs` is defined); Sh2/Sh3 restrict the codomain to the registered target domain at the current state.

*Notational overload: `from_K^Σ` vs `from_K`.* `from_K^Σ(τ)` (this Definition) is the slot accessor on tuples: input τ ∈ L_K^Σ, output the finite set `slot_addrs(F)`. The catalog templates below introduce `from_K(a)` without Σ-superscript: input an address a, output `{τ ∈ A_K^Σ : from₁(τ) = a}`. The Σ-superscript and the argument type disambiguate; the two functions are never composable in either order.

**Definition — PointSlotAccessors.** For shapes with `c_F = 1`:

`from₁ : L_K^Σ → shape(K).t_F^Σ` &nbsp; with &nbsp; `from₁(τ) = the unique element of from_K^Σ(τ)`

For shapes with `c_G = 1`:

`to₁ : L_K^Σ → shape(K).t_G^Σ` &nbsp; with &nbsp; `to₁(τ) = the unique element of to_K^Σ(τ)`

For shapes with `c_F = 0|1` or `c_G = 0|1`, the partial accessor returns `⊥` (undefined) when the slot is empty:

`from₁⁻ : L_K^Σ → shape(K).t_F^Σ ∪ {⊥}` defined when `c_F ∈ {1, 0|1}`; returns `⊥` iff `|slot_addrs(F)| = 0`, and returns the unique element of `slot_addrs(F)` otherwise.

`to₁⁻ : L_K^Σ → shape(K).t_G^Σ ∪ {⊥}` defined analogously when `c_G ∈ {1, 0|1}`; returns `⊥` iff `|slot_addrs(G)| = 0`, and returns the unique element of `slot_addrs(G)` otherwise.

*Codomain convention for partial templates.* Every partial-valued template's codomain is `(typed set) ∪ {⊥}`. Concretely: `from₁⁻ : L_K^Σ → t_F^Σ ∪ {⊥}`; `to₁⁻ : L_K^Σ → t_G^Σ ∪ {⊥}`; `K_target_of : A_doc → A_doc^Σ ∪ {⊥}`; `latest_K_for_addr : A_doc → A_K^Σ ∪ {⊥}`.

*Notational convention.* Bare shape symbols (`A_doc`, `A_rel`, `A`) on the *domain* side of a signature carry implicit Σ-quantification at the state of evaluation; codomains use the explicit `^Σ` form. At a concrete invocation state, the domain symbol expands via the Shape Definition's symbol-expansion rule.

**Lemma — SlotAccessorTotality.** When `shape(K).c_F = 1`, `from₁` is a total function on `L_K^Σ`. Similarly for `to₁` when `c_G = 1`.

*Proof.* By Sh0, every `τ ∈ L_K^Σ` has `F` in canonical-slot form with `|slot_addrs(F)| = 1` (since `match(n, 1) ⟺ n = 1`). A finite set of cardinality 1 has a unique element. Define `from₁(τ)` as that element. By Sh2, this element lies in `t_F^Σ`. ∎

For the rest of this document, we drop subscripts and write `from`, `to` when the shape unambiguously fixes which accessor is meant. We additionally use `addr(τ) = a` for the tuple address (R1, AddressInjectivity, ASN-0086).


## Idempotency (Sh4)

**Sh4 — IdempotencyDiscipline (conditional on the *Sh4 idempotency contract*).** When `shape(K).idem = ⊤` and the calling layer honors the *Sh4 idempotency contract* (defined below; the contract's clauses (i)–(iii) gate every `Emit_K` call site for such K), at most one *active* tuple in `L_K` shares any given slot-address pair. The contract is the load-bearing layer commitment: Sh4's conclusion fails at any state reachable by a contract-violating step, so callers depending on Sh4 must verify the contract's clauses are honored at every K with `shape(K).idem = ⊤`. For `τ = (a, F, G) ∈ L_K^Σ` we write `F_τ := F` and `G_τ := G` for the slot endsets of τ. Then:

`(A τ, τ' ∈ A_K^Σ : (slot_addrs(F_τ), slot_addrs(G_τ)) = (slot_addrs(F_{τ'}), slot_addrs(G_{τ'})) :: addr(τ) = addr(τ'))`

*Universal scope.* The two bound variables `τ` and `τ'` range independently over `A_K^Σ`, including the diagonal `τ = τ'`. On the diagonal the conclusion `addr(τ) = addr(τ')` reads `addr(τ) = addr(τ)`, satisfied by reflexivity of equality, so the diagonal contributes no constraint. The substantive content is off-diagonal: for any two *distinct* active tuples `τ, τ'` whose slot-address pairs match, Sh4 forces `addr(τ) = addr(τ')` — combined with R1 (AddressInjectivity, ASN-0086), the equality of addresses then collapses `τ = τ'`, contradicting the off-diagonal assumption. Read contrapositively: no two distinct active tuples in `A_K^Σ` share a slot-address pair. Subsequent appeals to "pairwise distinctness on `A_K^Σ`" mean exactly this off-diagonal content; the diagonal is dispatched once and for all by reflexivity.

*Sh4 idempotency contract.* For each `K ∈ T_cat` with `shape(K).idem = ⊤`, on every `Emit_K(Σ, d, F, G)` call site the layer enforces the following protocol (gate 3 per Gate Ordering):

(i) Before issuing the emission, the layer computes the candidate set
`C(F, G, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)}`
via the two-step procedure:

&nbsp;&nbsp;(i.a) Query `Observe_K(slot_addrs(F), slot_addrs(G), oper)` — a well-typed call by the ordering above: Sh-conf clauses (a)/(b) have already gated canonical-form, so `slot_addrs(F)` and `slot_addrs(G)` are finite subsets of `T` at this point in the protocol. Observe_K's semantics returns the (finite) set of active tuples whose slot coverages prefix-contain the pattern addresses — concretely, `{τ ∈ A_K^Σ : slot_addrs(F) ⊆ coverage(F_τ) ∧ slot_addrs(G) ⊆ coverage(G_τ)}`. Under Sh0/Sh1, every `τ ∈ A_K^Σ` has canonical-form slot endsets, so `coverage(F_τ) = ⋃ {{t : y ≼ t} : y ∈ slot_addrs(F_τ)}` and `slot_addrs(F) ⊆ coverage(F_τ)` iff every `x ∈ slot_addrs(F)` has some `y ∈ slot_addrs(F_τ)` with `y ≼ x`.

&nbsp;&nbsp;*Contract correctness.* `C(F, G, Σ)` equals the specified set regardless of Sh-conf clause (d): the post-filter (i.b) tests exact slot-address-set equality, and any τ in the specified set passes both (i.a)'s Observe (by Prefix reflexivity on each pattern address) and (i.b)'s filter.

&nbsp;&nbsp;*Observe-step tightness (expository, under clause (d)).* When Sh-conf clause (d) admits the new emission (so `slot_addrs(F) ⊆ A^Σ`), Observe in (i.a) over-approximates exactly to `slot_addrs(F_τ) ⊇ slot_addrs(F)` (via AllocatedAddressAntichain applied per pattern element). Symmetric argument on G. This expository observation is not consumed by the contract's clauses (ii)/(iii) or by Sh4's preservation argument.

&nbsp;&nbsp;(i.b) Post-filter the result of (i.a): retain only τ with `slot_addrs(F_τ) = slot_addrs(F)` and `slot_addrs(G_τ) = slot_addrs(G)`. Each returned τ has canonical-slot form by Sh0/Sh1, so `slot_addrs(F_τ)` is a well-defined finite set; exact-equality checks against the finite pattern slot-address sets are decidable in finite time. The composition (i.a) ∘ (i.b) yields exactly `C(F, G, Σ)` as specified above.

(ii) If `C(F, G, Σ) ≠ ∅`, the emission is *suppressed*: no `→`-step occurs.

(iii) Only if `C(F, G, Σ) = ∅` does the layer issue `Emit_K(Σ, d, F, G)`.

The layer commits to executing clauses (i)–(iii) atomically with respect to other emitters and retractors at the same `~`-equivalence class of K — emission and retraction events at any K' with `K' ~ K` that could split (i)'s observation from (iii)'s emission must be serialized by the layer. `L_K` is `~`-class indexed (ASN-0086, `L_K^Σ = L_{K'}^Σ` whenever `K ~ K'`), so emitters at distinct-but-`~`-equivalent type indices write to the same active subset; atomicity scoped at the `~`-class is what closes the race.

*Scope: single-process substrate.* The framework is restricted to single-process substrates: `↦`-transitions are sequential, and atomicity of (i)–(iii) reduces operationally to within-call sequencing between `Observe_K` and the substrate K.λ-step, with no intervening `↦`-step from another Sh4-emitter at a `~`-equivalent K. Multi-process consistency is flagged in Open Questions.

*Cross-`~`-class concurrency is benign.* Concurrent `Emit_R` retracting K-tuples while `Emit_K` is in flight (with `R ≁ K`) does not require serialization. The only mutation an `Emit_R` step applies to `A_K` is removal (a K-tuple is filtered out by `nullified(Σ)` membership); removing a tuple from `A_K` cannot violate the pairwise-slot-pair-distinctness condition, only restore it (a removed tuple is no longer a candidate witness for any pair-violation). The Sh4 atomicity scope is therefore correctly tightened to the `~`-equivalence class of K and not widened to all retractors. When `R ~ K` (K is itself the retraction relation), retraction and emission write to the same `A_K = A_R`, and the layer's atomicity at the `~`-class scope already handles the race — this is the Case D analyzed below.

*Preservation under the contract.* Sh4 holds at every reachable state under the contract, by induction on `↦*`. Fix `K ∈ T_cat` with `shape(K).idem = ⊤`.


**Lemma — RetractionSelfFreshness.** Let Σ be reachable from `Σ_init` under the framework's *Emit_K routing commitment*, with R registered in `T_cat` per the framework's baseline registration requirement (Nullify Compatibility). Suppose every framework gate at an `Emit_R(Σ, d, F, G)` call site admits the call — Sh-conf clauses (a)–(d) all pass and the *Sh4 idempotency contract* clause (iii) fires — so the call proceeds to K.λ at home `d` and deposits a fresh tuple τ_new with `addr(τ_new) = a_emit(Σ, d)`, producing result state Σ'. Then:

`addr(τ_new) ∉ nullified(Σ')`

— equivalently, `τ_new ∈ A_R^{Σ'}`.

*Proof.* By Definition (nullified, ASN-0086) at Σ', `addr(τ_new) ∈ nullified(Σ') ⟺ (E (b̂, F', G') ∈ L_R^{Σ'} :: addr(τ_new) ∈ coverage(G'))`; the existential ranges over `L_R^{Σ'} = L_R^Σ ∪ {τ_new}` (R3 monotonicity on `L_R`, since this is a class-(iii) `Emit_R` step that adds exactly τ_new to `L_R`). Two witnesses must be ruled out, both by Lemma — LinkAddressNotPrefixOfEmit:

(i) *Self-nullification check (witness `(b̂, F', G') = τ_new`).* Sh-conf at the new emission admitted the call only because clauses (a)–(d) held; under `shape(R) = (*, 1, A, A_rel, ⊤)`, clauses (b)/(c)/(d) force `G_{τ_new} = {(b, δ(1, #b))}` for a unique `b ∈ A_rel^Σ`, so by PrefixSpanCoverage (ASN-0043) `coverage(G_{τ_new}) = {t : b ≼ t}`. Lemma — LinkAddressNotPrefixOfEmit applied at `b ∈ dom(Σ.L)` and `d := home(τ_new) ∈ dom(Σ.M)` yields `b ⋠ a_emit(Σ, d) = addr(τ_new)`, so `addr(τ_new) ∉ {t : b ≼ t} = coverage(G_{τ_new})`.

(ii) *Cross-nullification check (witness ranges over `L_R^Σ`).* For every prior `(b̂, F', G') ∈ L_R^Σ`, Sh1 at `K := R` gives `G'` canonical-slot with `|slot_addrs(G')| = 1`, and Sh3 at `K := R` gives `slot_addrs(G') ⊆ A_rel^Σ ⊆ A_rel^{Σ'}`. So `G' = {(b', δ(1, #b'))}` for a unique `b' ∈ dom(Σ.L) ⊆ dom(Σ'.L)`. Lemma — LinkAddressNotPrefixOfEmit applied at `b'` and the same `d = home(τ_new)` yields `b' ⋠ a_emit(Σ, d) = addr(τ_new)`, so `addr(τ_new) ∉ coverage(G')`. Quantifying over all `(b̂, F', G') ∈ L_R^Σ` discharges the cross-nullification disjunct.

Combining (i) and (ii) over the full disjunction `L_R^{Σ'} = L_R^Σ ∪ {τ_new}`: for every witness in `L_R^{Σ'}`, `addr(τ_new) ∉ coverage(G')`. Hence `addr(τ_new) ∉ nullified(Σ')`, and τ_new ∈ A_R^{Σ'} by Definition (A_K^Σ, ASN-0086). ∎

*Scope and consumption.* The Lemma's hypothesis — "every framework gate admits the call" — exhausts the conditions under which an `Emit_R` step actually deposits τ_new in `L_R^{Σ'}` (per the *Gate Ordering (consolidated)* clause in the Sh-conf section); at call sites where any gate rejects (`⊥`-return), no τ_new is produced and the Lemma's conclusion is vacuous. The Lemma is consumed at two sites in the Sh4 induction below: Case C's `K ~ R` sub-case uses part (i) alone (the τ_new produced at that step is not self-nullified, so the complementary sub-case is empty), and Case D cites the full conclusion to establish that the case-description equation `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving` *holds as a theorem*, not as a stipulation — Case D's structural set-up presupposes τ_new joins A_R^{Σ'}, and the Lemma discharges that presupposition. Stating RetractionSelfFreshness here, before the induction begins, separates the structural establishment of "what enters A_R^{Σ'}" from the pairwise-distinctness arguments of Cases C and D on the established active subset.

*Base.* At `Σ_0 = Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Initial-State Baseline section above), `L_K^{Σ_0} = A_K^{Σ_0} = ∅`; Sh4's universal is vacuous.

*Step (Case A: `A_K^{Σ'} = A_K^Σ`).* The active subset is unchanged at K. Once the case-equation holds, Sh4 is inherited directly: `A_K^{Σ'} = A_K^Σ` as sets of triples (by set extensionality), so Sh4's body — quantifying over triples — yields the same Boolean at both states. The case-equation's *closure* is therefore trivial; the substantive work in Case A is verifying that each `↦`-step in the framework's transition vocabulary which lands in Case A actually satisfies the case-equation. We enumerate those classes here exhaustively (the framework's `↦`-vocabulary is `↦ = (K.σ ∪ K.α ∪ K.λ) ∪ arrangement-modifying` per ASN-0086's `→` Definition and `↦` relation), with each class's case-equation discharge cited inline:

1. *K.σ-steps and K.α-steps:* preserve `Σ.L` pointwise (ASN-0086's `→` Definition's frame conditions), hence `L_K^{Σ'} = L_K^Σ`; `L_R^{Σ'} = L_R^Σ`, so `nullified(Σ') = nullified(Σ)`; therefore `A_K^{Σ'} = A_K^Σ`.
2. *K.λ-steps at type `K'` with `K' ≁ K` and `K' ≁ R`:* the new tuple enters the disjoint slice `L_{K'}^Σ`, leaving `L_K^Σ` and `L_R^Σ` untouched (ASN-0086's `~`-class indexing); same conclusion.
3. *K.λ-steps at type `K'` with `K' ≁ K` and `K' ~ R` when no τ ∈ A_K^Σ lies in the new R-tuple's G-coverage:* `L_K^Σ` untouched (still `K' ≁ K`); `nullified(Σ')` extends but the extension does not intersect `addr(·)` for any τ ∈ A_K^Σ, so `A_K^{Σ'} = A_K^Σ`. The complementary sub-regime (where some τ ∈ A_K^Σ *is* nullified) contracts `A_K` and is routed to Case C below.
4. *Arrangement-modifying steps in `↦ \ →`:* LinkStoreInvarianceUnderArrangement (ASN-0086) gives `Σ'.L = Σ.L` pointwise, hence `L_K^{Σ'} = L_K^Σ`, `L_R^{Σ'} = L_R^Σ`, and `nullified(Σ') = nullified(Σ)`; therefore `A_K^{Σ'} = A_K^Σ`.

The enumeration is exhaustive for *Case A coverage* within the framework's `↦`-vocabulary: every `↦`-step that produces the case-equation falls into exactly one of these four classes, and each class's discharge is cited explicitly so a reader can verify Case A's coverage end-to-end. Transition classes the full Xanadu substrate may admit at scopes outside this framework's commitment (e.g., publication-state transitions, BEBE topology migrations) lie outside `↦`'s vocabulary and so outside Sh4's preservation scope by construction.

*Step (Case B: `A_K^{Σ'} = A_K^Σ ∪ {τ_new}`, a K.λ-step at type K with `K ≁ R`).* The case is structurally restricted to `K ≁ R` rather than carrying a conditional "no concurrent nullification" qualifier: by the class-decomposition of `↦` (per ASN-0086's `→` Definition and `↦`'s broader transition relation), concurrent nullification at the same step happens only at `Emit_R` steps, since `nullified(Σ)`'s definition reads over `L_R^Σ`'s G-coverages and only `Emit_R` extends `L_R`. A non-Retraction-typed K.λ-step (i.e., the `K ≁ R` regime selected here) cannot extend `L_R^Σ` and therefore cannot expand `nullified(Σ)`, so no τ ∈ A_K^Σ leaves `A_K` at this step — concurrent nullification is structurally impossible in Case B, not a conditional precondition. The complementary `K ~ R` regime is routed to Case D below, where the step is by definition an `Emit_R`-step at the same `~`-class as K and the simultaneous addition-and-possible-contraction structure is handled via the candidate-set argument plus the structural bound `|leaving| ≤ 1`. The case-decomposition exhausts the simultaneous-effect possibilities at the K.λ class: Case B covers `K ≁ R` (no possible nullification), Case D covers `K ~ R` (possible nullification handled explicitly). By the *Emit_K routing commitment*, this K.λ-step originates as an `Emit_K` call (with K or `~`-equivalent registered type). By the *Sh4 idempotency contract* clause (iii), the emission proceeded only because `C(F, G, Σ) = ∅`. Let `τ_new` be the new tuple. Suppose, toward contradiction, that some prior `τ ∈ A_K^Σ` satisfies `(slot_addrs(F_τ), slot_addrs(G_τ)) = (slot_addrs(F_{τ_new}), slot_addrs(G_{τ_new}))`. Then by definition `τ ∈ C(F, G, Σ)`, contradicting `C(F, G, Σ) = ∅`. So no such `τ` exists, and `A_K^{Σ'}` extends with a slot-pair-unique element. The pairwise condition is preserved: existing pairs were Sh4-distinct by IH; `τ_new` shares no slot-pair with any prior active tuple.

*Step (Case C: `A_K^{Σ'} ⊆ A_K^Σ` strictly, an `Emit_R`-step nullifying one or more K-tuple addresses without adding to A_K).* Retraction filters `A_K^Σ` by `nullified(Σ)` membership but cannot introduce new K-tuples; the pairwise condition is preserved on any subset. This case fires when `K ≁ R` (so the Emit_R step's `τ_new` does not join `A_K`). The complementary `K ~ R` sub-case — where one might expect "self-retraction" of `τ_new` by the same step — is empty by Lemma — RetractionSelfFreshness (stated above, before the Base), part (i): under `K ~ R` the Lemma's self-nullification clause gives `addr(τ_new) ∉ coverage(G_{τ_new})`, so `τ_new` is never self-nullified. The `K ~ R` simultaneous-effect case where τ_new adds to A_R and one or more *prior* R-tuples leave is Case D below.

*Step (Case D: K ~ R, `Emit_R`-step adding τ_new to A_R while potentially nullifying prior R-tuple addresses).* By RetractionSelfFreshness, τ_new ∈ A_R^{Σ'}. Combined with `nullified(·)`-filtering, `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving` where `leaving := {τ ∈ A_R^Σ : addr(τ) ∈ coverage(G_{τ_new})}`. This case-description equation follows by unfolding ASN-0086's `A_K^Σ` and `nullified` Definitions at Σ': R3 gives `L_R^{Σ'} = L_R^Σ ∪ {τ_new}`; splitting `nullified(Σ')`'s existential by prior-tuple vs new-tuple witness yields `nullified(Σ') = nullified(Σ) ∪ {a : a ∈ coverage(G_{τ_new})}` restricted to `A_rel^{Σ'}`; substituting into `A_R^{Σ'}`'s Definition and applying RetractionSelfFreshness's `addr(τ_new) ∉ nullified(Σ')` yields the equation. When `leaving = ∅` the step is pure addition; when `|leaving| = 1` it is `+1, −1`.

*Structural bound on `|leaving|`.* By Sh-conf at R (`c_G = 1`, `t_G = A_rel`), `G_{τ_new} = {(b, δ(1, #b))}` for a unique `b ∈ A_rel^Σ = dom(Σ.L)`. By PrefixSpanCoverage, `coverage(G_{τ_new}) = {t : b ≼ t}`. By R0a (FlatLinkDomain, ASN-0086), `dom(Σ.L)` is a tumbler-prefix antichain, so `{a ∈ dom(Σ.L) : b ≼ a} = {b}` (Prefix reflexivity gives `b` in the set; R0a's antichain rules out any other element). Therefore `leaving = {τ ∈ A_R^Σ : addr(τ) = b}`, and R1 (AddressInjectivity) gives `|leaving| ≤ 1`. Case D is at most a `+1, −1` step.

By the *Sh4 idempotency contract* clause (iii) — which fires under `K ~ R` since per-class constancy gives `shape(K).idem = ⊤` — the candidate-set check `C(F_{τ_new}, G_{τ_new}, Σ) = ∅` was confirmed against the full `A_R^Σ`. So `τ_new` is slot-pair-distinct from every prior τ ∈ A_R^Σ. Sh4's predicate is symmetric in its two operands, so this single check covers both ordered-pair directions. Combined with the IH on `A_R^Σ`, pairwise distinctness holds on `A_R^Σ ∪ {τ_new}`. Since `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving` is a subset, and Sh4's body is preserved under subset restriction (the universal quantifier over a subset of a pairwise-distinct set inherits the distinctness), Sh4 holds on `A_R^{Σ'}`.

The induction closes. ∎

*Status.* Sh4 is a *theorem under the Sh4 idempotency contract*, not a substrate-enforced axiom. The substrate as defined by ASN-0086 does not enforce Sh4 directly: R0 (TupleAddressFreshness) explicitly permits two emissions with identical `(F, G)` to produce two distinct tuples; R1 (AddressInjectivity) keeps them distinguishable. Without the *Sh4 idempotency contract*, the substrate would admit such emissions and Sh4 would fail. The framework's Sh4 conclusion depends on the layer's protocol fidelity at this specific contract.

*Failure modes under contract violation.* Breaking any of clauses (i)–(iii) may invalidate Sh4 at the resulting state. The set-valued accessors `from_K`, `to_K`, `from_addrs_K`, `to_addrs_K` degrade gracefully to multisets; the singleton-returning `K_target_of` (DirectedPair under FDD) requires the strictly stronger FunctionalDependencyDiscipline because Sh4 enforces slot-pair distinctness, not from-slot uniqueness.

*Consequences.*

(a) *Existence-vs-count distinction.* Idempotent relations support `exists_K(F, G) : Bool` predicates with stable yes/no answers under the contract. Non-idempotent relations support `count_K(...)` predicates whose value reflects the number of distinct emission events.

(b) *Re-emit-vs-fail behavior is registry-driven.* Library helpers like `emit_attribute` consult `shape(K).idem` to decide whether to short-circuit on existing match or always allocate a fresh address. The decision is mechanical from the shape, not from inspection of K's name.

(c) *Idempotency is a property of A_K, not L_K.* By R3, `L_K` always retains every emission ever made — including any duplicates that may exist if the contract was ever violated. The contract restricts what reaches `A_K`. Under correct contract enforcement, once a duplicate would be emitted, the layer suppresses it. The audit slice `L_K` retains historical state regardless: retraction-then-reemit cycles can leave multiple coverage-identical tuples in `L_K` with at most one active.


## Template Catalog (Sh5)

**Sh5 — TemplateCatalog (META).** Sh5 is an organizational convenience for hand-curating the canonical shape catalog; it is not a mechanical-derivation theorem. Per-shape template families are written by hand against the canonical catalog, with two design conventions enforced by catalog-author diligence:

*(a) Per-shape uniformity is an aspiration.* The catalog's shape-mate convergences (DirectedPair/Resolution sharing five base templates modulo codomain shift; the two `(0, 1)` rows sharing `is_K`) are hand-curated, not framework-derived. A future catalog extension at the same shape may register divergent template bodies without violating any framework gate.

*(b) Citation convention.* Catalog template bodies cite only: (i) shape-component-derived slot accessors (`from₁`, `to₁`, `from₁⁻`, `to₁⁻`, `from_K^Σ`, `to_K^Σ`); (ii) K's name; (iii) named scaffolding clauses (`chain_index`, `home(·)`, `s_L`); (iv) accessors exported by a registered per-K discipline (e.g., `emission_order` under SHCD); (v) meta-operators (logical, set-theoretic, arithmetic primitives); (vi) framework-internal base-machinery accessors (`A_K^Σ`, `addr(τ)`, `slot_addrs(·)`, `δ(1, #·)`). Categories (i)–(iv) are checked by reading the template body; (v) and (vi) are unrestricted.

*Signature derivation rule.* Template signatures derive mechanically from shape components (input/codomain symbols read from `t_F`/`t_G`); bodies do not.

The framework's actual content is therefore Sh-conf + Sh0–Sh4 + the layer-discipline contracts; the catalog and template families are an organizational layer on top.


## The Canonical Shape Catalog

The substrate's relations fall into a small fixed set of canonical shapes. Each canonical shape pairs with a *base* predicate template family that is forced by the shape — there is no design freedom in base template selection once the shape is fixed. Per-K opt-in and parametric extensions sit atop the base family and require additional registration (per-K disciplines) or additional arguments at evaluation time (type-index parameters).

*Target-domain symbol scope.* `A_doc = dom(Σ.C)` denotes content addresses (`zeros = 3`), not document-container addresses (`dom(Σ.M)`, `zeros = 2`); `A_rel = dom(Σ.L)`. The framework provides no symbol for `dom(Σ.M)` targeting (see Open Questions).

| Shape                     | (c_F, c_G) | t_F   | t_G   | idem | Template family                                              |
|---------------------------|------------|-------|-------|------|--------------------------------------------------------------|
| Classifier                | (0, 1)     | -     | A_doc | ⊤    | *base:* `is_K(d)` |
| Tuple-Classifier          | (0, 1)     | -     | A_rel | ⊤    | *base:* `is_K(τ)` (the body matches Classifier's `is_K` by the catalog's current hand-curation per Sh5(a); the signature shift from `A_doc → Bool` to `A_rel → Bool` is mechanical per Sh5(b)'s *Signature derivation rule*) |
| DirectedPair              | (1, 1)     | A_doc | A_doc | ⊤    | *base:* `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`; *opt-in (per-K):* `K_target_of(a)` under FunctionalDependencyDiscipline |
| NonIdempotentDirectedPair | (1, 1)     | A_doc | A_doc | ⊥    | *base:* `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)` (set-valued by R1 AddressInjectivity; may contain slot-pair-identical tuples without Sh4); *opt-in (per-K):* `latest_K_for_addr(d)` under SingleHomeCoverageDiscipline; *parametric:* `unresolved_K_comments_via(K_res, d)`, `all_K_resolved_via(K_res, d)` with `K_res ∈ T_cat` constrained to `shape(K_res) = (1, 1, A_doc, A_rel, ⊤)` (Resolution shape; the constraint is what makes `to₁(ρ)` total on `ρ ∈ A_{K_res}^Σ` and lands the equality `to₁(ρ) = addr(τ)` in `A_rel^Σ`) |
| Resolution                | (1, 1)     | A_doc | A_rel | ⊤    | *base (hand-curated against the DirectedPair shape-mate; per-shape body-shape uniformity is an aspiration of this catalog, not a framework gate — see *Status of per-shape uniformity* in Sh5(a)):* `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`; *dominant downstream pattern:* parametric consumption by NonIdempotentDirectedPair's `_via` templates (with K serving as the `K_res` argument). A standalone use (registering K at Resolution and consuming the base templates without any NonIdempotentDirectedPair consumer in scope) is admissible under the catalog's hand-curated row registration and is exhibited at the "Resolution base templates at a standalone K (no `_via` consumer in scope)" sub-walkthrough in *Additional Worked Examples* (`K = approved_by` registered with no parametric consumer in scope, exercising Emissions AB1, AB2, the AB3 rejection, and the full base-template evaluation table at Σ_2) |
| Retraction                | (\*, 1)    | A     | A_rel | ⊤    | *base (reformulated under `c_F = *`; bodies in the walkthrough):* `pair_K(F̂, b)` (F̂ matched by set equality), `from_K(a)` (membership-based: τ included iff `a ∈ slot_addrs(F_τ)`), `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`; *primary consumption:* by ASN-0086's `nullified(·)` definition, which reads each `L_R`-tuple's G-coverage directly over the audit slice `L_R^Σ` (not via the active-subset `to_K` accessor; the audit-slice reading is the one R6b commits to, blocking the recursive fixpoint the active-subset reading would introduce) |
| BundledDirectedPair       | (1, \*)    | A_doc | A_doc | ⊤    | *base (reformulated under `c_G = *`; bodies in the walkthrough):* `pair_K(a, Ĝ)` (Ĝ matched by set equality), `from_K(a)`, `to_K(b)` (membership-based: τ included iff `b ∈ slot_addrs(G_τ)`), `from_addrs_K(b)`, `to_addrs_K(a)`; *consumption:* admits both legacy single-target emissions (`\|slot_addrs(G)\| = 1`) and bundled multi-target emissions (`\|slot_addrs(G)\| ≥ 2`) under a single registration via `match(n, *)` for every `n ∈ ℕ`; coverage class disjoint from R by shape-tuple inequality (Retraction's `(*, 1, A, A_rel, ⊤)` differs on `c_F`, `c_G`, `t_F`, `t_G`), so per-class constancy forces `K ≁ R` for every K registered at this shape — EffectiveWpSimplification's Step 2 Case A applies directly without invoking the Lemma at the new emission's G |
| Provenance                | (1, 0\|1)  | A     | A     | ⊤    | *base (`c_G = 0|1` requires explicit `⊥`-handling on G-side templates; bodies in the walkthrough):* `outgoing_K(s)` (alias of `from_K(s)`), `pair_K(a, b)`, `from_K(a)`, `to_K(b)` (*target-indexed accessor: excludes tuples with empty G-slot by definition, since `⊥ ≠ b` for any `b ∈ A^Σ`; partial-domain consequence of `c_G = 0|1` — distinguishes Provenance's `to_K` from DirectedPair's `to_K` at `c_G = 1`, where all tuples in the relation appear*), `from_addrs_K(b)`, `to_addrs_K(a)` (with `⊥`-filter). *For full-domain queries over `A_K^Σ`, callers must use `outgoing_K` (or `from_K`) rather than `to_K`; see the *Asymmetry of `to_K` against DirectedPair's* note in the walkthrough body for the formal reading.* |

*Catalog row structure: base, opt-in, parametric.* Each row separates templates by what enables them. The three categories are defined by a precise criterion:

A template is *base* iff its definition is well-formed under exactly (a) the shape tuple's components, (b) K's name, and (c) the framework's Sh0–Sh4 guarantees (under the *Sh4 idempotency contract* when `shape(K).idem = ⊤`). At each K registered at the shape `Sh_canon`, the row's listed template bodies are the ones the framework's current catalog supplies *by hand-curation* — signature derivation from the shape components is mechanical per Sh5(b)'s *Signature derivation rule*, but body-shape convergence at shape-mate rows is an aspiration of the present catalog rather than a framework-enforced derivation (see *Status of per-shape uniformity (downgraded to aspiration in this draft)* in Sh5(a)). The word *inherit* used elsewhere in this document at base-template references at shape-mate rows reads as "supplied by the catalog's current hand-curation against the same template family" rather than "produced by a mechanical derivation"; a future catalog extension at the same shape may, in principle, register divergent template bodies without violating any framework gate.

A template is *opt-in (per-K)* iff its well-formedness additionally requires a per-K discipline registration listed in the catalog row (currently FunctionalDependencyDiscipline at DirectedPair and SingleHomeCoverageDiscipline at NonIdempotentDirectedPair Coverage). The discipline strengthens Sh-conf's gate at the registering K beyond what the bare shape demands.

A template is *parametric* iff it takes an additional type-index argument supplied at predicate-evaluation time (e.g., a Resolution relation `K_res` consumed by NonIdempotentDirectedPair's `_via` templates). Parametric templates require no registration commitment at K; the type-index is passed by the calling predicate.

The criterion is exhaustive: any template that depends on K-specific data outside (a)–(c), without a registered per-K discipline or a per-call type-index, would fail to be classifiable and so would be rejected by the META discipline of Sh5(b). The split is what makes Sh5's per-shape discipline falsifiable *at the citation-side*: rows whose templates cite a data symbol outside categories (i)–(iv) — and not within (v) or (vi) — violate Sh5(b) and are rejected per the *Catalog-wide citation audit*. Body-shape-level convergence between rows with identical `(c_F, c_G, t_F, t_G, idem)` tuples is a separate property — an *aspiration* of this catalog's hand-curation, not a framework commitment (see *Status of per-shape uniformity (downgraded to aspiration in this draft)* in Sh5(a)). The current catalog *exhibits* convergence at shape-mate rows (DirectedPair/Resolution sharing five base templates modulo codomain shift; the two `(0, 1)` rows sharing `is_K`), and the framework supplies no mechanical gate that would enforce convergence at a future catalog extension; a future draft proposing a divergent template body at an existing shape would not be rejected by any mechanical check the framework supplies. Per-shape uniformity at the body-shape level therefore reads as a design aspiration the present catalog meets by hand-curation, with body-shape design freedom retained at every new row.

The catalog has *bipartite coverage*: for each structural pattern (cardinality + idempotency), entries with `t_G = A_doc` and `t_G = A_rel` are listed separately. Classifier and Tuple-Classifier are the two `(0, 1, -, ·, ⊤)` rows; DirectedPair and (a hypothetical Tuple-DirectedPair) would be the two `(1, 1, ·, ·, ⊤)` rows on the document/tuple axis. The current catalog enumerates the rows demanded by present-day predicate templates; further bipartite entries can be added by extending the catalog.

*Per-K opt-in registry is partitioned by base shape.* FunctionalDependencyDiscipline attaches only to DirectedPair (`idem = ⊤`); SingleHomeCoverageDiscipline attaches only to NonIdempotentDirectedPair (`idem = ⊥`). The two are structurally mutually exclusive at any single K because their required `idem` values differ and `shape(K).idem` is fixed.


## Per-Shape Template Walkthroughs

We walk the canonical shapes and exhibit the predicate templates each generates.

*Common rejection patterns.* Walkthroughs cite these patterns by number; the Comment walkthrough below derives patterns 1–4 in full as canonical references, with patterns 5–6 derived first at Classifier and at Comment's Edge case respectively.

1. *Non-canonical from/to-set rejection* (Sh-conf clause (a)/(b) failure).
2. *Unallocated target rejection* (Sh-conf clause (d) failure, allocation aspect).
3. *Cardinality mismatch rejection* (Sh-conf clause (c) failure).
4. *Unregistered type rejection* (Sh-conf first conjunct `K ∈ T_cat` failure).
5. *G-side partition mismatch rejection* (Sh-conf clause (d) failure, partition aspect — e.g., a content address where the shape requires `t_G = A_rel`).
6. *Per-K-discipline-suppression rejection* (Sh4 clause (ii), FDD clause (ii), or SHCD clause (i) failure).

### Classifier — `(0, 1, -, A_doc, ⊤)`

Every tuple in `L_K` has `slot_addrs(F) = ∅` (Sh0) and `slot_addrs(G) = {d}` for some `d ∈ A_doc^Σ` (Sh1, Sh3). The to-accessor `to₁(τ) ∈ A_doc^Σ` is total (SlotAccessorTotality).

`is_K : A_doc → Bool`

`is_K(d) ≡ (E τ ∈ A_K^Σ :: to₁(τ) = d)`

A document `d` is *classified as K* iff there exists an active tuple in `L_K` whose to-slot is `d`. By Sh4 idempotency (layer-enforced), the existential is yes/no — multiple slot-identical active tuples are precluded by policy.

*Walkthrough.* Register `K = is_claim` with the Classifier shape, pre-allocating a target document `d ∈ A_doc^{Σ_0}` and a home document `home_K ∈ dom(Σ_0.M)` (with `dom(Σ_0.L) = ∅` so K.λ's first-emission branch fires).

*Registered catalog for this walkthrough.* `T_cat = {is_claim, R}` (closure under `~` implicit). `is_claim` is the Classifier-shape relation under exercise; no Retraction emissions are exercised here, but `R` carries the mandatory baseline registration.

*Admission.* `Emit_K(Σ_0, home_K, ∅, {(d, δ(1, #d))})`. Sh-conf check: F = ∅ canonical-slot, `slot_addrs(F) = ∅`, `match(0, c_F = 0)` ✓; F-side clause (d) reads `∅ ⊆ -^{Σ_0} = ∅`, vacuously true. G = `{(d, δ(1, #d))}` canonical-slot, `slot_addrs(G) = {d}`, `match(1, c_G = 1)` ✓; G-side clause (d) reads `{d} ⊆ A_doc^{Σ_0}` ✓ since `d` is pre-allocated. Admitted. Result Σ_1 with new tuple σ_1 at fresh address `addr(σ_1) ∈ A_rel^{Σ_1}` (a relation-tuple address, distinct from the document address `d`).

*Rejection (G-side partition mismatch — canonical reference for Pattern 5).* This rejection establishes the canonical Pattern 5 reference of the *Common rejection patterns*. From Σ_1, attempt `Emit_K(Σ_1, home_K, ∅, {(addr(σ_1), δ(1, #addr(σ_1)))})` — G targets the relation-tuple address `addr(σ_1) ∈ A_rel^{Σ_1}` instead of a document content address. Sh-conf clauses (a)/(b)/(c) all pass (G canonical-slot, cardinality 1). Clause (d) on G-side reads `{addr(σ_1)} ⊆ A_doc^{Σ_1}`, but `addr(σ_1) ∈ A_rel^{Σ_1} = dom(Σ_1.L)`, and by R4 (TupleAddressDisjointness, ASN-0086) `A_doc^{Σ_1} ∩ A_rel^{Σ_1} = ∅`, so `addr(σ_1) ∉ A_doc^{Σ_1}` and `{addr(σ_1)} ⊄ A_doc^{Σ_1}`. The emission is rejected; `Emit_K` returns `⊥` and state remains Σ_1 unchanged. The Classifier shape's `t_G = A_doc` is precisely what blocks classifier-emissions from targeting relation tuples — and inversely, Tuple-Classifier's `t_G = A_rel` blocks document targets. The two shapes are the bipartite halves of the same `(0, 1)` cardinality skeleton, partitioned by clause (d). ✗

*Template evaluation at Σ_1.* `A_K^{Σ_1} = {σ_1}` (no retractions). `is_K(d) ≡ (E τ ∈ A_K^{Σ_1} :: to₁(τ) = d)` — witnessed by σ_1 with `to₁(σ_1) = d`, so `is_K(d) = true`. For any other pre-allocated `d' ∈ A_doc^{Σ_1}` with `d' ≠ d`, no active tuple has `to₁(τ) = d'`, so `is_K(d') = false`.

### Tuple-Classifier — `(0, 1, -, A_rel, ⊤)`

Structurally identical to Classifier; the only difference is the target domain. Every tuple in `L_K` has `slot_addrs(F) = ∅` and `slot_addrs(G) = {τ}` for some `τ ∈ A_rel^Σ`. The to-accessor `to₁(σ) ∈ A_rel^Σ` is total.

`is_K : A_rel → Bool`

`is_K(τ) ≡ (E σ ∈ A_K^Σ :: to₁(σ) = τ)`

A tuple `τ` is *classified as K* iff there exists an active classifier-tuple in `L_K` whose to-slot is `τ`. The single-letter substitution `d ↝ τ` from Classifier's template body is the only difference; signature changes from `A_doc → Bool` to `A_rel → Bool`.

Tuple-Classifier admits useful predicates over substrate-internal entities — marking a comment-tuple as endorsed, marking a citation-tuple as deprecated, marking a review-tuple as clean (so `is_clean(τ)` for `τ ∈ A_rel`). By Sh3 (`t_G = A_rel`), a Tuple-Classifier tuple's to-slot targets a tuple address, distinguishing it from a Classifier whose to-slot targets a document. The two are the bipartite halves of the same `(0, 1)` shape pattern.

*Distinction from Resolution.* Resolution `(1, 1, A_doc, A_rel, ⊤)` also targets `A_rel`, but its `c_F = 1` slot requires an actor — a resolving document. Tuple-Classifier has `c_F = 0`: no actor recorded in the tuple. Use Resolution when the assertion needs an attributed asserter; use Tuple-Classifier when the assertion is a property of the targeted tuple itself, not an action upon it.

### DirectedPair — `(1, 1, A_doc, A_doc, ⊤)`

Tuples have form `slot_addrs(F) = {a}, slot_addrs(G) = {b}` with `a, b ∈ A_doc^Σ` — a single document address in each slot. Role-specific readings (parent → sidecar, citing → cited, asserter → asserted, etc.) are layer conventions over a single structural shape.

*Canonical template family (role-neutral, hand-curated body-shape).* Every K registered at this shape inherits the following five templates by the catalog's hand-curation; signatures derive mechanically from the shape components per Sh5(b)'s *Signature derivation rule*, but the body-shape (which set comprehensions and which Boolean compositions appear) is the catalog author's hand-curated choice — per *Status of per-shape uniformity* in Sh5(a), the framework supplies no mechanical gate that would force a future catalog extension at this shape to register the same template bodies. Each listed template is unconditional under Sh0–Sh4 (Sh0/Sh1 supply canonical-slot form and unit cardinality; Sh2/Sh3 supply `A_doc^Σ` codomains for the slot accessors; Sh4 ensures the returned tuple-sets and address-sets are slot-pair-distinct, not multisets). Codomains are made explicit per the *Codomain convention* for templates:

`pair_K : A_doc × A_doc → Bool`
`pair_K(a, b)         ≡ (E τ ∈ A_K^Σ :: from₁(τ) = a ∧ to₁(τ) = b)`

`from_K : A_doc → ℘_fin(A_K^Σ)`
`from_K(a)            ≡ {τ ∈ A_K^Σ : from₁(τ) = a}`

`to_K   : A_doc → ℘_fin(A_K^Σ)`
`to_K(b)              ≡ {τ ∈ A_K^Σ : to₁(τ) = b}`

`to_addrs_K   : A_doc → ℘_fin(A_doc^Σ)`
`to_addrs_K(a)        ≡ {to₁(τ) : τ ∈ A_K^Σ ∧ from₁(τ) = a}`

`from_addrs_K : A_doc → ℘_fin(A_doc^Σ)`
`from_addrs_K(b)      ≡ {from₁(τ) : τ ∈ A_K^Σ ∧ to₁(τ) = b}`

`pair_K` returns Boolean. `from_K` and `to_K` return tuple-sets in `℘_fin(A_K^Σ)`. `to_addrs_K` and `from_addrs_K` return address-sets in `℘_fin(A_doc^Σ)`, obtained by composing slot accessors over the corresponding tuple-set; the codomains are pinned to `A_doc^Σ` by Sh2/Sh3 at the DirectedPair shape.

*Layer aliasing conventions.* Specific K registrations may pair the canonical templates with role-specific names. Two common conventions:

- *Attribute usage* (K interpreted as parent → sidecar): `has_K(d) := from_K(d) ≠ ∅`, `K_sidecars_of(d) := to_addrs_K(d)`.
- *Citation usage* (K interpreted as citing → cited): `cites_K(a, b) := pair_K(a, b)`, `K_incoming(b) := from_addrs_K(b)`.

These aliases are layer constructs. The framework guarantees the canonical templates above; role-specific renaming is the layer's responsibility, with no mechanical derivation from K's name. Distinct layers may register distinct K's at this same shape and use different aliasing conventions per layer.

#### FunctionalDependencyDiscipline (per-K, optional)

**Definition — FunctionalDependencyDiscipline (conditional on the *FDD functional-dependency contract*).** A K registered with the DirectedPair shape `shape(K) = (1, 1, A_doc, A_doc, ⊤)` may additionally register a *FunctionalDependencyDiscipline* commitment: at most one active tuple per from-slot value, formally

`(A τ, τ' ∈ A_K^Σ : from₁(τ) = from₁(τ') :: addr(τ) = addr(τ'))`

at every reachable state Σ. The conclusion is load-bearing only under the *FDD functional-dependency contract* (defined below; the contract's clauses (i)–(iii) gate every `Emit_K` call site for FDD-registered K) — FDD's preservation theorem fails at any state reachable by a contract-violating step, so callers depending on FDD's from-slot-uniqueness conclusion must verify the contract's clauses are honored at every FDD-registered K.

*Structural preconditions (load-bearing for FDD's well-formedness).* FDD's body references `from₁(τ)` and the FDD-opt-in `K_target_of` template lands in `A_doc^Σ ∪ {⊥}` — both of which require explicit shape-component constraints on K:

- *`c_F = 1`* — SlotAccessorTotality at `c_F = 1` is what makes `from₁(τ)` total on `L_K^Σ`; without `c_F = 1`, `from₁` is undefined (`c_F = 0`) or partial (`c_F = 0|1`, returning `⊥`) and the body's `from₁(τ) = from₁(τ')` equality is either ill-formed or carries `⊥`-handling not captured by the formal statement. FDD's preservation argument's Case B step ("`from₁` of any tuple is the unique element of `slot_addrs(F)` (SlotAccessorTotality)") cites SlotAccessorTotality at `c_F = 1` directly, so the precondition is load-bearing for the preservation theorem, not just for the body's typing.
- *`t_F = A_doc`* — `K_target_of`'s codomain `A_doc^Σ ∪ {⊥}` reads `A_doc^Σ` off `t_F` via the Sh5(b) *Signature derivation rule*; without `t_F = A_doc`, the codomain symbol would shift (e.g., to `A_rel^Σ ∪ {⊥}` at `t_F = A_rel`) and the template's name and intended consumption pattern (filesystem-style "the K-target of this document") would no longer match.

The current draft attaches FDD only to the DirectedPair shape, which carries both constraints (`c_F = 1` and `t_F = A_doc`) by registration. A future generalization of FDD to admit any `c_F = 1` shape with a documented codomain shift (e.g., FDD at Resolution's `(1, 1, A_doc, A_rel, ⊤)` shape, which would land `K_target_of` in `A_rel^Σ ∪ {⊥}`) is admissible under the structural precondition `c_F = 1` alone, but is *not* exercised by this draft; the catalog's opt-in registry currently attaches FDD only at DirectedPair (per the *Per-K opt-in registry is partitioned by base shape* paragraph in the Canonical Shape Catalog section), with both `c_F = 1` and `t_F = A_doc` consequently fixed. Registering FDD at a shape with `c_F = 0`, `c_F = 0|1`, `c_F = *`, or `t_F ≠ A_doc` (without a documented FDD generalization) is *structurally rejected* by the registration interface; the framework's preservation theorems and the `K_target_of` codomain typing both presuppose these preconditions.

*Strictly stronger than Sh4.* Sh4 enforces pairwise distinctness of slot-address *pairs*, not of `slot_addrs(F_τ)` alone. Two emissions sharing from-slot `d` but distinct G-slots both pass Sh4 (distinct slot-pairs), yielding `|{τ : from₁(τ) = d}| = 2` — a singleton-returning accessor is ill-defined. FDD forbids the second emission outright.

*FDD functional-dependency contract.* For each K with FunctionalDependencyDiscipline registered, on every `Emit_K(Σ, d, F, G)` call site (gate 3 per Gate Ordering):

*FDD subsumes Sh4 at FDD-registered K.* At FDD-registered K the layer runs only the FDD clauses (i)–(iii), with Sh4's clauses dormant. The Sh4 conclusion still holds because `C ⊆ C_fd`: FDD's stricter from-slot-uniqueness entails Sh4's weaker slot-pair-distinctness.

(i) Compute `C_fd(F, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}` via the two-step procedure: (i.a) query `Observe_K(slot_addrs(F), ∅, oper)` — well-typed by finiteness of `slot_addrs(F)`; the `∅` G-pattern matches every G-coverage trivially under Observe_K's `Ĝ ⊆ coverage(G)` semantics, so the result is `{τ ∈ A_K^Σ : slot_addrs(F) ⊆ coverage(F_τ)}`. By the same AllocatedAddressAntichain argument used in Sh4's contract, under the same conditional hypothesis (Sh-conf clause (d) holds for the new emission's F) this over-approximates *exactly* `slot_addrs(F_τ) ⊇ slot_addrs(F)`; the contract's correctness — that the computed `C_fd(F, Σ)` equals the specified `{τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}` — is independent of this tightness property, depending only on (i.a)'s finite over-approximation and (i.b)'s exact-equality post-filter, by the same expository-vs-substantive split made for Sh4's contract. (i.b) post-filter to exact from-slot-address equality on F — retain only τ with `|slot_addrs(F_τ)| = |slot_addrs(F)|` (which under canonical-slot form forces `slot_addrs(F_τ) = slot_addrs(F)` given the over-approximation under the conditional hypothesis; without the hypothesis, the post-filter still tests exact set equality on finite slot-address sets and still yields `C_fd(F, Σ)` exactly, but the contract returns `⊥` either via clause (ii) below or via the subsequent Sh-conf rejection).

(ii) If `C_fd(F, Σ) ≠ ∅`, the emission is *suppressed*: no `→`-step occurs.

(iii) Only if `C_fd(F, Σ) = ∅` does the layer issue `Emit_K(Σ, d, F, G)`.

The layer commits to executing (i)–(iii) atomically with respect to other emitters and retractors at the same `~`-equivalence class of K. The same single-process-substrate scope from Sh4's contract applies: atomicity reduces operationally to within-call sequentiality between `Observe_K` and the substrate K.λ-step within a single `Emit_K` call, with no intervening `↦`-step from another FDD-emitter at a `~`-equivalent K.

*Preservation under the discipline.* The inductive argument runs three cases: Case A (active subset unchanged), Case B (single new tuple at K), and Case C (retraction-only contraction). Case D (the K=R simultaneous addition-and-contraction case from Sh4) is excluded by shape-tuple structure: FDD requires `shape(K) = (1, 1, A_doc, A_doc, ⊤)`, while Retraction has `shape(R) = (*, 1, A, A_rel, ⊤)`; per-class constancy of `shape` (`K ~ K' ⟹ shape(K) = shape(K')`) and the shape-tuple inequality (differs on `c_F`, `t_F`, `t_G`) force `K ≁ R` for every FDD-registered K, so no `Emit_R` step can extend `A_K`.


Fix `K ∈ T_cat` with FDD registered. By the same off-diagonal/diagonal split as in Sh4 (see *Universal scope* above), the substantive content of FDD's property `(A τ, τ' ∈ A_K^Σ : from₁(τ) = from₁(τ') :: addr(τ) = addr(τ'))` is that no two *distinct* active K-tuples share a from-slot value; the diagonal `τ = τ'` is trivial by reflexivity of `addr(·) = addr(·)`. The candidate set `C_fd(F, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}` is broader in scope than Sh4's `C(F, G, Σ)` — it matches on from-slot alone rather than on the slot-pair — so `C ⊆ C_fd` at every state. The discipline is therefore *stricter as a gate* (more candidate sets are non-empty, so more emissions are suppressed) even though its candidate set is broader.

*Base.* At `Σ_0 = Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Initial-State Baseline section above), `L_K^{Σ_0} = A_K^{Σ_0} = ∅`; FDD's universal is vacuous.

*Step (Case A: `A_K^{Σ'} = A_K^Σ`).* The active subset is unchanged at K. FDD is inherited directly from the IH: the same set of pairs `(τ, τ')` over `A_K` is being quantified over, with the same `from₁` values, so the implication's consequent is unchanged at every pair. This case covers all K.σ-steps, K.α-steps, K.λ-steps emitting a tuple of any type `K'` with `K' ≁ K` and `K' ≁ R` (so `L_K` and `nullified` are both untouched at K), and all arrangement-modifying steps in `↦ \ →` (by LinkStoreInvarianceUnderArrangement).

*Step (Case B: `A_K^{Σ'} = A_K^Σ ∪ {τ_new}`, a K.λ-step at type K with no concurrent nullification of any τ ∈ A_K^Σ).* By the *Emit_K routing commitment*, this K.λ-step originates as an `Emit_K` call (with K or `~`-equivalent registered type). By the *FDD functional-dependency contract* clause (iii), the emission proceeded only because `C_fd(F, Σ) = ∅`. Suppose, toward contradiction, that some prior `τ ∈ A_K^Σ` satisfies `from₁(τ) = from₁(τ_new)`. Under FDD's shape `(1, 1, A_doc, A_doc, ⊤)`, `from₁` of any tuple is the unique element of `slot_addrs(F)` (SlotAccessorTotality), so `from₁(τ) = from₁(τ_new)` iff `slot_addrs(F_τ) = slot_addrs(F_{τ_new})`. Hence `τ ∈ C_fd(F_{τ_new}, Σ)`, contradicting `C_fd(F, Σ) = ∅`. So no such `τ` exists, and `τ_new`'s from-slot value is fresh among `A_K^Σ`. Combined with the IH (which gives from-slot uniqueness off-diagonal on `A_K^Σ`) and reflexivity at the diagonal `(τ_new, τ_new)`, FDD holds on `A_K^{Σ'} = A_K^Σ ∪ {τ_new}`.

*Step (Case C: `A_K^{Σ'} ⊆ A_K^Σ` strictly, an `Emit_R`-step nullifying one or more K-tuple addresses without adding to A_K).* Retraction filters `A_K^Σ` by `nullified(Σ)` membership but cannot introduce new K-tuples (this case fires when `K ≁ R`, which holds for every FDD-registered K). The from-slot-uniqueness property is preserved on any subset: the universal quantifier ranges over fewer pairs but the predicate is unchanged, and any pair surviving in `A_K^{Σ'}` was already constrained by the IH on `A_K^Σ`.

The induction closes. ∎

*Singleton-returning template under FunctionalDependencyDiscipline.* When the discipline holds at every reachable state, the candidate set `from_K(a) = {τ ∈ A_K^Σ : from₁(τ) = a}` is empty or singleton for every `a`, so a value-returning accessor is well-defined:

`K_target_of : A_doc → A_doc^Σ ∪ {⊥}`

`K_target_of(a) ≡ to₁(τ)` &nbsp; where τ is the unique element of `from_K(a)` &nbsp; (returns `⊥` when `from_K(a) = ∅`)

*Precondition.* Under FunctionalDependencyDiscipline at K, `from_K(a)` is empty or singleton at every reachable state Σ (by the preservation theorem above, which discharges FDD inductively under the *FDD functional-dependency contract*); the "unique element" reading of the template's body is well-formed exactly because FDD guarantees cardinality `|from_K(a)| ∈ {0, 1}`. Without FDD, the bare DirectedPair shape does not constrain `|from_K(a)|`, the candidate set may carry multiple elements, and the template's body is ill-formed (no unique element exists to apply `to₁` to). The catalog entry's *opt-in (per-K) under FunctionalDependencyDiscipline* tagging encodes this precondition: registering K with DirectedPair but without FDD precludes instantiating `K_target_of`; consumers wanting a singleton-returning accessor at a non-FDD K must instead use `to_addrs_K(a)` (set-valued by Sh5's base templates) and disambiguate at the consumer's site.

The codomain `A_doc^Σ ∪ {⊥}` records that the template returns either a content address (in the to-slot's target domain `A_doc` per the DirectedPair shape's `t_G`) or the partiality token `⊥`; consumers must dispatch on the `⊥` case before composing further accessors.

*Aliases under FunctionalDependencyDiscipline.* An Attribute-style K committed to FunctionalDependencyDiscipline aliases the singleton accessor as `K_sidecar_of(d) := K_target_of(d)`. Without FunctionalDependencyDiscipline, layers must use `to_addrs_K(d)` (set-valued) and disambiguate at the consumer.

*Failure mode.* Templates consuming FunctionalDependencyDiscipline (specifically `K_target_of` and its aliases) become undefined on the candidate set when the discipline is violated and the set contains multiple elements. Per-template specifications below state explicitly when a template's totality depends on this discipline.

*Layer composite: `K_is_fresh`.* Layers may compose `K_target_of` with a layer-supplied accessor outside the substrate's relational structure — e.g., a filesystem `mtime` accessor — to form predicates such as `K_is_fresh(d) ≡ from_K(d) ≠ ∅ ∧ mtime(K_target_of(d)) ≥ mtime(d)`. This composite is illustrative of how `K_target_of` (substrate-supplied conditional on FDD) combines with layer-supplied data (`mtime : A_doc → ℕ`); it is *not* a Sh5(b)-admissible base template because `mtime` falls outside all six categories (i)–(vi) of the Sh5(b) discipline (the rejected-candidate row in the Sh5 audit table records this rejection). Under FDD violation the composite degrades: replace `K_target_of(d)` with iteration over `to_addrs_K(d)` and an explicit reduction (e.g., "max mtime over all targets"). The reduction is a layer-level choice, not a framework-derived projection. The composite is recorded here as documentation of the FDD-opt-in's downstream consumption pattern; it is not part of the framework's template catalog.

### Resolution — `(1, 1, A_doc, A_rel, ⊤)`

Tuples have form `slot_addrs(F) = {d}, slot_addrs(G) = {addr(σ)}` where `d ∈ A_doc^Σ` is the resolving document and `σ ∈ A_rel^Σ` is the comment-tuple being resolved. The shape `(1, 1, A_doc, A_rel, ⊤)` carries the same five-template base family as DirectedPair (with `t_G = A_rel` substituted for `A_doc`): `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`. The convergence with DirectedPair's base family at the body-shape level is a hand-curated aspiration of this catalog (per *Status of per-shape uniformity* in Sh5(a)), exhibited here against the DirectedPair shape-mate, not a framework-enforced mechanical derivation.

*Standalone admissibility (exhibited via hand-curation; verification depends on Sh5(b)'s convention).* The catalog's hand-curated row registration admits these five base templates at any K registered at the Resolution shape regardless of which downstream consumers (if any) are in scope. Concretely: a `K = approved_by` layer relation registered at Resolution — where reviewers `d ∈ A_doc^Σ` approve standalone document-targeting tuples `σ ∈ A_rel^Σ` and the layer consumes the base templates directly, with no NonIdempotentDirectedPair `_via` consumer in scope — passes the Sh5(b) per-row review checklist (steps 0–3) by hand-inspection. The framework's preservation theorems (Sh0–Sh4) and the templates' definitional bodies are unchanged at such a registration; no parametric consumer is required to validate the standalone path. Because Sh5(b) is a design convention enforced by author diligence rather than by a tooled gate (see *Sh5(b) is a hand-followed convention*), this "standalone admissibility" claim rests on the catalog author's audit walk rather than on a machine-checked verification — the standalone-path audit walk is exhibited in the "Resolution base templates at a standalone K" sub-walkthrough below. The catalog row's parametric-column entry documents the *dominant downstream pattern* observed in this framework (Comment's `_via` templates), not a constraint on Resolution's admissible use sites.

### Retraction — `(\*, 1, A, A_rel, ⊤)`

Tuples have form `slot_addrs(F) ⊆ A^Σ` (any finite set, possibly empty) and `slot_addrs(G) = {addr(σ)}` for `σ ∈ A_rel^Σ` the tuple being retracted. The retraction shape is consumed by ASN-0086's `A_K^Σ` Definition and Definition (nullified) directly: the active-subset definition uses `L_R`'s tuples to compute `nullified(Σ)`. By Sh5(b), the shape `(*, 1, A, A_rel, ⊤)` *mechanically derives* the signature of each base template per the *Signature derivation rule*, but the bodies are hand-curated against the DirectedPair shape-mate: bodies must be re-formulated for the `c_F = *` setting, since `from₁` is not defined when `c_F` is not `1`. The DirectedPair templates' use of `from₁(τ)` as a point accessor is replaced by `slot_addrs(F_τ)` as a set accessor; the matching predicates likewise lift from address-equality to set-equality or set-membership as appropriate to each template's role. Per *Status of per-shape uniformity* in Sh5(a), the framework supplies no mechanical gate that would force the present body-shape choices to be the *only* admissible ones at this shape; the bodies below are the catalog's hand-curated commitments:

`pair_K(F̂, b)        ≡ (E τ ∈ A_K^Σ :: slot_addrs(F_τ) = F̂ ∧ to₁(τ) = b)`

`from_K(a)           ≡ {τ ∈ A_K^Σ : a ∈ slot_addrs(F_τ)}`

`to_K(b)             ≡ {τ ∈ A_K^Σ : to₁(τ) = b}`

`from_addrs_K(b)     ≡ {x : (E τ ∈ A_K^Σ :: to₁(τ) = b ∧ x ∈ slot_addrs(F_τ))}`

`to_addrs_K(a)       ≡ {to₁(τ) : τ ∈ A_K^Σ ∧ a ∈ slot_addrs(F_τ)}`

The four set-valued templates take an *address* on the from-side (`from_K`, `from_addrs_K`'s witness `x`, and `to_addrs_K`'s argument `a`) using the membership relation `a ∈ slot_addrs(F_τ)` — every τ whose from-slot *contains* the queried address `a` is included. The Boolean `pair_K`'s F-side argument is an *address-set pattern* `F̂` matched by exact set equality `slot_addrs(F_τ) = F̂`; this preserves the role of `pair_K` as a Boolean existence test for a particular (from-pattern, to-address) combination. The to-side accessors and the `to_K` template use `to₁(·)` directly, since `c_G = 1` admits SlotAccessorTotality on the G-slot. Both `to_K` and `to_addrs_K` return well-typed sets — `to_K` a tuple-set in `℘_fin(A_K^Σ)`, `to_addrs_K` an address-set in `℘_fin(A_rel^Σ)` — by Sh3 on the G-slot. Even though Retraction's primary role is to flip `A_K` membership for arbitrary K via ASN-0086's `A_K^Σ` Definition (which filters `L_K^Σ` by `nullified(Σ)`-membership, with `nullified(Σ)` itself defined over `L_R^Σ`'s G-coverages), not to host its own predicates, the base template family is fully defined; the catalog row's "primary consumption" column flags this active-subset machinery as the principal consumer rather than enumerating the inherited base family a second time.

*Note on `pair_K`'s set-equality F-side argument (deliberate, role-specific design choice).* Retraction's `pair_K(F̂, b)` is the one catalog template that takes an *address-set pattern* on the from-side rather than an address, and matches by exact set equality rather than by membership. This is *not* the only Sh5(b)-admissible reading: an alternative would be `pair_K(a, b) ≡ (E τ ∈ A_K^Σ :: a ∈ slot_addrs(F_τ) ∧ to₁(τ) = b)`, mirroring the membership semantics of `from_K`. Either reading is well-formed under Sh5(b) — both depend only on (i) shape components (`c_F = *`, `c_G = 1`, `t_F = A`, `t_G = A_rel`, `idem = ⊤`), (ii) K's name, and (iii) no extra named accessors. The framework adopts the exact-set-equality reading as a deliberate role-specific design choice, recorded here in the catalog row rather than mechanically derived: because Retraction's `c_F = *` admits from-slots of any finite cardinality (including the bare-retraction case `c_F = 0` and multi-attributor retractions), "is there a tuple with this *exact* attribution-set targeting `b`" is the operationally meaningful Boolean test (matching the audit-grade question "did this specific attribution combination ever retract `b`"). The membership-reading `pair_K(a, b)` overlaps with `from_K(a) ∩ to_K(b) ≠ ∅`, which is already expressible from the base templates by intersection; retaining the set-equality reading for `pair_K` gives the catalog row a Boolean predicate that is not directly expressible from the other four templates, avoiding redundancy with the membership-based `from_K`. The choice is recorded as deliberate so that other shape rows with `c_F = 1` (DirectedPair, NonIdempotentDirectedPair, Resolution, Provenance) — where `slot_addrs(F_τ) = {from₁(τ)}` and set-equality with a single-element pattern collapses to address-equality — continue to read `pair_K(a, b)` as an address-pair predicate without disagreement with this row.

*Unit-depth retraction discipline secured by Retraction's shape.* Retraction's `c_G = 1` together with canonical-slot form (Sh-conf clauses (a)/(b)) forces every shape-conformant Retraction emission's G-endset to a single unit-depth span `{(b, δ(1, #b))}` for some `b ∈ A_rel^Σ`. This is exactly ASN-0086's unit-depth retraction discipline: every emission that lands in `L_R^Σ` via `Emit_R` satisfies the discipline by construction. Consequently, ASN-0086's wp simplification under regime (i) applies to every Sh-conf-admitted Retraction emission — `NoCraftedSpanReachesD(Σ, d)` holds automatically at every such call site by Lemma — LinkAddressNotPrefixOfEmit (whose generalized statement `b ⋠ a_emit(Σ, d)` for any `b ∈ dom(Σ.L)` is applied in the EffectiveWpSimplification Corollary's Step 1 to each prior R-tuple's unique G-slot address; the proof case-splits on `home(b) = d` vs `home(b) ≠ d` and rules out `b ≼ a_emit(Σ, d)` in each case) — so the wp_086 in the Sh-conf section's effective-wp derivation collapses to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible` without manual discharge.

The unrestricted from-slot (`c_F = *`) accommodates use cases where the retracting party is recorded in F (e.g., F's slot addresses include an agent address), as well as the bare retraction `Nullify(Σ, d_retr, a) = Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` of ASN-0086, where `F = ∅`. Both forms are canonical-slot (the bare form trivially, the attributed form when its from-slot endset is in canonical form). The shape framework rejects retractions whose from-slot uses non-canonical-form endsets, consistent with the discipline imposed across the catalog.

### BundledDirectedPair — `(1, \*, A_doc, A_doc, ⊤)`

Tuples have form `slot_addrs(F) = {a}` for `a ∈ A_doc^Σ` and `slot_addrs(G) ⊆ A_doc^Σ` (any finite set, possibly empty, possibly singleton, possibly multi-element). The shape's distinguishing feature is `c_G = *`: a single emission may bundle multiple to-side document targets into one tuple, rather than requiring a separate tuple per target. Role-specific readings (parent → multiple sidecars, citing → multiple cited works, source → multiple dependents) are layer conventions over a single structural shape.

*Motivating use case (`citation.depends`).* The shape was added to admit bundled dependency-style citation emissions where a single citing document depends on a finite set of cited documents — recorded atomically in one tuple rather than spread across several. The substrate primitive K.λ already admits multi-element G-endsets at any K (ASN-0086 R0 takes arbitrary `(F, G)` with `K ∈ T_admissible`); the framework's contribution is to register the shape so that Sh-conf admits these multi-element G-emissions under a stable cardinality bound `c_G = *`.

*Canonical base template family (signatures forced by shape; bodies hand-curated against the DirectedPair shape-mate).* By Sh5(b), the shape `(1, *, A_doc, A_doc, ⊤)` *mechanically derives* the signature of each base template per the *Signature derivation rule*, but the *body* is hand-curated against the DirectedPair shape-mate row — adapting DirectedPair's `to₁(τ)` point-accessor uses to `slot_addrs(G_τ)` set-accessor uses, with matching predicates lifted from address-equality to set-equality or set-membership as appropriate to each template's role. Per *Status of per-shape uniformity* in Sh5(a), the framework supplies no mechanical gate that would force the present body-shape choices to be the *only* admissible ones at this shape; the bodies below are the catalog's hand-curated commitments, not a derivation from the shape components. The F-side templates retain `from₁` as a point accessor by SlotAccessorTotality at `c_F = 1`:

`pair_K(a, Ĝ)        ≡ (E τ ∈ A_K^Σ :: from₁(τ) = a ∧ slot_addrs(G_τ) = Ĝ)`

`from_K(a)           ≡ {τ ∈ A_K^Σ : from₁(τ) = a}`

`to_K(b)             ≡ {τ ∈ A_K^Σ : b ∈ slot_addrs(G_τ)}`

`from_addrs_K(b)     ≡ {from₁(τ) : τ ∈ A_K^Σ ∧ b ∈ slot_addrs(G_τ)}`

`to_addrs_K(a)       ≡ {x : (E τ ∈ A_K^Σ :: from₁(τ) = a ∧ x ∈ slot_addrs(G_τ))}`

The Boolean `pair_K`'s G-side argument is an *address-set pattern* `Ĝ` matched by exact set equality `slot_addrs(G_τ) = Ĝ`; this preserves the role of `pair_K` as a Boolean existence test for a particular (from-address, to-pattern) combination. The four set-valued templates take an *address* on the to-side (`to_K`, `from_addrs_K`'s argument `b`, and `to_addrs_K`'s witness `x`) using the membership relation `b ∈ slot_addrs(G_τ)` — every τ whose to-slot *contains* the queried address `b` is included. The F-side templates use `from₁(·)` directly, since `c_F = 1` admits SlotAccessorTotality on the F-slot. Both `from_K` and `from_addrs_K` return well-typed sets — `from_K` a tuple-set in `℘_fin(A_K^Σ)`, `from_addrs_K` an address-set in `℘_fin(A_doc^Σ)` — by Sh2 on the F-slot.

*Symmetric design choice with Retraction's `pair_K`.* This row's `pair_K(a, Ĝ)` mirrors Retraction's role-specific design choice for `pair_K(F̂, b)` (deliberately recorded in the Retraction walkthrough): set-equality on the *unrestricted-cardinality* side is the operationally meaningful Boolean test ("is there a tuple with this *exact* to-set targeting `a`"), distinguishable from the membership-based `to_K(b)` (which would only test "is there any tuple targeting `b`"). The membership reading `pair_K(a, b) ≡ b ∈ slot_addrs(G_τ) ∧ from₁(τ) = a` would overlap with `from_K(a) ∩ to_K(b) ≠ ∅`, expressible from the four other templates by intersection; the set-equality reading gives the catalog row a Boolean predicate not directly expressible from the other four, avoiding redundancy.

*Backward compatibility with legacy single-target emissions.* Because `c_G = *` admits any `n ∈ ℕ` via `match(n, *)`, legacy emissions with `|slot_addrs(G)| = 1` — i.e., the shape of single-target `citation.depends` calls under a prior `c_G = 1` registration — remain shape-conformant under the new `c_G = *` registration. Concretely, an emission with `slot_addrs(G) = {b}` for a single `b ∈ A_doc^Σ` passes clause (c) at `match(1, *)` and clause (d) at `{b} ⊆ A_doc^Σ`; no separate migration discipline is required for pre-patch tuples. The transition from `c_G = 1` to `c_G = *` is one-way: a K registered at `c_G = *` admits both single- and multi-target tuples uniformly. Per-class constancy of `shape(·)` (lifetime-constant per the ShapeRegistry Definition) precludes re-registering K's shape after `Σ_init`; a layer migrating from a pre-patch `c_G = 1` registration must declare the relation at `c_G = *` from `Σ_init` to recover both regimes under one row, with `L_K^{Σ_init} = ∅` discharging the empty-baseline preservation theorems.

*Empty-G admissibility.* `c_G = *` admits `n = 0` per `match(0, *)`; the cardinality vocabulary `{0, 1, *, 0|1}` carries no `1..*` token, so a `1..*` lower bound cannot be expressed at the registry level. The asymmetry with Retraction: Retraction admits empty-F (the bare Nullify alias) with non-empty-G, while BundledDirectedPair admits non-empty-F with empty-G. Sh4 suppression and the audit-slice set-semantics commitment apply uniformly at `n = 0` (exact slot-pair-equality on the empty set is decidable).

*Coverage class disjointness from R (EffectiveWpSimplification implication).* The BundledDirectedPair shape tuple `(1, *, A_doc, A_doc, ⊤)` differs from Retraction's `(*, 1, A, A_rel, ⊤)` on four components (`c_F`, `c_G`, `t_F`, `t_G`). Per-class constancy of `shape(·)` (`K ~ K' ⟹ shape(K) = shape(K')`) gives the contrapositive: `shape(K) ≠ shape(K') ⟹ K ≁ K'`. Hence every K registered at the BundledDirectedPair shape satisfies `K ≁ R`. In EffectiveWpSimplification's Step 2 (proof in the EffectiveWpSimplification Corollary section), the case-split on K's `~`-class lands in Case A (`K ≁ R`): the first disjunct's arm holds directly and the Lemma — LinkAddressNotPrefixOfEmit is not invoked at the new emission's G-slot. Step 1's discharge of `NoCraftedSpanReachesD(Σ, d)` over prior R-tuples in `L_R^Σ` is unaffected (it quantifies over R-tuples regardless of the new emission's type). EffectiveWpSimplification's wp simplification therefore applies uniformly at every Sh-conf-admitted `Emit_K` call site for K at this shape.

*Worked example.* Register `K = citation.depends` with the BundledDirectedPair shape, pre-allocating a citing document `d_cite ∈ A_doc^{Σ_0}`, three cited documents `d_src1, d_src2, d_src3 ∈ A_doc^{Σ_0}`, and a home `home_cite ∈ dom(Σ_0.M)` with `dom(Σ_0.L) = ∅`.

*Registered catalog for this walkthrough.* `T_cat = {citation.depends, R}` (closure under `~` implicit). `citation.depends` is the BundledDirectedPair-shape relation under exercise.
*Timeline structure.* The walkthrough's main timeline runs `Σ_0 → Σ_1 → Σ_2` via two emissions exercising the shape's two non-empty G-cardinality regimes — Emission BDP1 (bundled multi-target, `|slot_addrs(G)| = 3`) at `Σ_0 → Σ_1`, then Emission BDP2 (legacy single-target, `|slot_addrs(G)| = 1`) at `Σ_1 → Σ_2`. A separately-labeled *alternative continuation from Σ_0* — Emission BDP0 exercising the empty-G boundary `|slot_addrs(G)| = 0` — is presented at the end of this walkthrough; that branch produces a parallel state Σ_0a and does *not* extend the main timeline. Template evaluation at Σ_2 uses only the main timeline's active subset `A_K^{Σ_2} = {γ_1, γ_2}`.

**Emission BDP1 (bundled multi-target, `|slot_addrs(G)| = 3`).** `Emit_K(Σ_0, home_cite, F_BDP1, G_BDP1)` with `F_BDP1 = {(d_cite, δ(1, #d_cite))}` and `G_BDP1 = {(d_src1, δ(1, #d_src1)), (d_src2, δ(1, #d_src2)), (d_src3, δ(1, #d_src3))}` (bundled dependency on three sources).

*Sh-conf check at Σ_0.* F_BDP1 canonical-slot with `slot_addrs(F_BDP1) = {d_cite}`, `|·| = 1`, `match(1, c_F = 1)` ✓. G_BDP1 canonical-slot with `slot_addrs(G_BDP1) = {d_src1, d_src2, d_src3}`, `|·| = 3`, `match(3, c_G = *)` ✓ (since `3 ∈ ℕ`). Target-domain: `{d_cite} ⊆ A_doc^{Σ_0}` ✓; `{d_src1, d_src2, d_src3} ⊆ A_doc^{Σ_0}` ✓. Sh4 contract clause (i) computes `C(F_BDP1, G_BDP1, Σ_0) = ∅` (no prior K-tuples; the per-element multi-slot argument from clause (i.a) applies *three times* on the G-side — once per `b ∈ {d_src1, d_src2, d_src3}` — yielding G-side over-approximation `slot_addrs(G_τ) ⊇ {d_src1, d_src2, d_src3}`, then the post-filter forces exact equality, yielding `C = ∅` vacuously since there are no τ to filter). Clause (iii) issues. Admitted. Result Σ_1 with new tuple γ_1.

**Emission BDP2 (legacy single-target, `|slot_addrs(G)| = 1`).** `Emit_K(Σ_1, home_cite, F_BDP2, G_BDP2)` with `F_BDP2 = {(d_cite, δ(1, #d_cite))}` (same citing document) and `G_BDP2 = {(d_src1, δ(1, #d_src1))}` (single dependency on d_src1).

*Sh-conf check at Σ_1.* F_BDP2 canonical-slot, `|·| = 1`, matches `c_F = 1`. G_BDP2 canonical-slot, `slot_addrs(G_BDP2) = {d_src1}`, `|·| = 1`, `match(1, c_G = *)` ✓ — the legacy single-target emission shape passes the cardinality gate at `c_G = *` exactly as it would have at `c_G = 1`. Target-domain ✓. Sh4 contract: `C(F_BDP2, G_BDP2, Σ_1) = {τ ∈ A_K^{Σ_1} : slot_addrs(F_τ) = {d_cite} ∧ slot_addrs(G_τ) = {d_src1}} = ∅` because γ_1 has `slot_addrs(G_{γ_1}) = {d_src1, d_src2, d_src3} ≠ {d_src1}` (the exact-set-equality post-filter rejects γ_1 even though `{d_src1} ⊂ {d_src1, d_src2, d_src3}`). Clause (iii) issues. Admitted. Result Σ_2 with new tuple γ_2.

*Sh4 idempotency at distinct slot-pairs.* The two emissions share `slot_addrs(F)` but differ on `slot_addrs(G)`: `{d_src1, d_src2, d_src3} ≠ {d_src1}` as sets. Sh4's pairwise-distinctness condition is preserved because the slot-pair `(slot_addrs(F_τ), slot_addrs(G_τ))` differs between γ_1 and γ_2. The shape admits both regimes under one registration.

**Template evaluation at Σ_2.** `A_K^{Σ_2} = {γ_1, γ_2}`. Per the canonical base templates:

| Template | Evaluation at Σ_2 | Notes |
|---|---|---|
| `pair_K(d_cite, {d_src1, d_src2, d_src3})` | `(E τ ∈ A_K^{Σ_2} :: from₁(τ) = d_cite ∧ slot_addrs(G_τ) = {d_src1, d_src2, d_src3}) = true` | Witnessed by γ_1; set-equality test on G. |
| `pair_K(d_cite, {d_src1})` | `= true` | Witnessed by γ_2; legacy single-target shape. |
| `pair_K(d_cite, {d_src1, d_src2})` | `= false` | No τ has G-slot exactly `{d_src1, d_src2}`. |
| `pair_K(d_cite, ∅)` | `= false` | Empty-G cardinality boundary: BDP1 and BDP2 both emitted non-empty G, so no active τ at Σ_2 has empty G-slot. The alternative continuation BDP0 below would produce a γ_0 with empty G-slot at the parallel state Σ_0a; in that branch `pair_K(d_cite, ∅)` would evaluate to `true`. The present (main-timeline) value `false` reflects that γ_0 is not in `A_K^{Σ_2}`. |
| `from_K(d_cite)` | `{τ ∈ A_K^{Σ_2} : from₁(τ) = d_cite} = {γ_1, γ_2}` | Both tuples from the same citing document. |
| `to_K(d_src1)` | `{τ ∈ A_K^{Σ_2} : d_src1 ∈ slot_addrs(G_τ)} = {γ_1, γ_2}` | Both tuples reference d_src1 (γ_1 via the bundle, γ_2 directly). |
| `to_K(d_src2)` | `= {γ_1}` | Only γ_1's bundle references d_src2. |
| `to_K(d_src3)` | `= {γ_1}` | Only γ_1's bundle references d_src3. |
| `from_addrs_K(d_src1)` | `{d_cite}` | Collapsed: both tuples share the same from-side address. |
| `to_addrs_K(d_cite)` | `{d_src1, d_src2, d_src3}` | Flattens across γ_1's bundle and γ_2's singleton. |

The bundled (γ_1) and legacy (γ_2) tuples co-exist in the same active subset under one registration; `pair_K`'s set-equality test distinguishes the two regimes at the Boolean level, while membership-based `to_K(b)` admits queries that don't care about the bundle structure.

**Alternative continuation from Σ_0 — Emission BDP0 (empty-G boundary, `|slot_addrs(G)| = 0`).** To exhibit the `n = 0` admissibility flagged in the *Empty-G admissibility* paragraph above, consider the parallel branch from the same `Σ_0` that the main timeline started from: fire `Emit_K(Σ_0, home_cite, F_BDP0, G_BDP0)` with `F_BDP0 = {(d_cite, δ(1, #d_cite))}` and `G_BDP0 = ∅` — citing document declares no dependency targets at all. **This branch produces a parallel state Σ_0a and does not extend the main timeline above.** Σ_0a is exhibited only to walk the `n = 0` admissibility and the corresponding Sh4 suppression behavior; γ_0 never enters `A_K^{Σ_1}`, `A_K^{Σ_2}`, or any subsequent main-timeline state.

*Sh-conf check at Σ_0 (alternative branch).* F_BDP0 canonical-slot with `slot_addrs(F_BDP0) = {d_cite}`, `|·| = 1`, `match(1, c_F = 1)` ✓. G_BDP0 is canonical-slot trivially with `slot_addrs(G_BDP0) = ∅`, `|·| = 0`, `match(0, c_G = *)` ✓ (since `0 ∈ ℕ`). Target-domain: `{d_cite} ⊆ A_doc^{Σ_0}` ✓; `∅ ⊆ A_doc^{Σ_0}` vacuously ✓. Sh4 contract clause (i) computes `C(F_BDP0, G_BDP0, Σ_0) = ∅` (no prior K-tuples at Σ_0). Clause (iii) issues. Admitted. Result Σ_0a with new tuple γ_0 having `slot_addrs(F_{γ_0}) = {d_cite}` and `slot_addrs(G_{γ_0}) = ∅`.

*Sh4 suppression on a duplicate empty-G attempt (within the alternative branch).* From Σ_0a, attempt a *second* identical call `Emit_K(Σ_0a, home_cite, F_BDP0, G_BDP0)`. Sh4 contract clause (i) computes `C(F_BDP0, G_BDP0, Σ_0a) = {τ ∈ A_K^{Σ_0a} : slot_addrs(F_τ) = {d_cite} ∧ slot_addrs(G_τ) = ∅} = {γ_0}` (exact slot-pair-equality on the empty set matches γ_0 directly). Clause (ii) *suppresses*: `Emit_K` returns `⊥`, state remains Σ_0a, `A_K^{Σ_0a} = {γ_0}` unchanged — the empty-G slot-pair behaves identically to non-empty-G slot-pairs under Sh4.

*Template evaluation at Σ_0a (alternative branch).* `A_K^{Σ_0a} = {γ_0}`. `pair_K(d_cite, ∅) = true` (witnessed by γ_0); `pair_K(d_cite, {d_src1})` and similar non-empty-G probes evaluate to `false` at Σ_0a (γ_0 has empty G-slot, so its slot-pair `({d_cite}, ∅)` does not match any non-empty G-pattern). This is the parallel reading the main-timeline table's `pair_K(d_cite, ∅)` row contrasts against; under the main timeline at Σ_2, the same probe evaluates to `false` because the main-timeline emissions never produced an empty-G tuple.

*Rejection case BDP3 (cardinality mismatch under a hypothetical `c_G = 1` re-registration).* If `K = citation.depends` had been registered at the prior `c_G = 1` shape, Emission BDP1 would have failed Sh-conf clause (c) with `match(3, c_G = 1) = false`. The new `c_G = *` registration is what admits BDP1; the new shape's strict superset relationship `{n ∈ ℕ : match(n, 1)} = {1} ⊂ ℕ = {n ∈ ℕ : match(n, *)}` formalizes the backward-compatible widening. ✗ at `c_G = 1`, ✓ at `c_G = *`.

### NonIdempotentDirectedPair — `(1, 1, A_doc, A_doc, ⊥)`

Non-idempotent directed-pair tuples allow multiple distinct emissions sharing the same slot-address pair — each emission is a distinct event, retained in `L_K` regardless of slot-address coincidence with prior tuples. Role-specific readings (witness → subject for coverage, commenter → target for comment, etc.) are layer conventions over a single structural shape.

*Canonical base templates (signatures forced by shape; bodies hand-curated against the DirectedPair shape-mate).* By Sh5(b), the shape `(1, 1, A_doc, A_doc, ⊥)` *mechanically derives* the signature of each base template per the *Signature derivation rule*, but the bodies below are the catalog's hand-curated commitments against the DirectedPair shape-mate row (Sh5(a)'s *Status of per-shape uniformity (downgraded to aspiration in this draft)* makes body-shape convergence at shape-mates an aspiration of this catalog, not a framework-enforced derivation; the framework supplies no mechanical gate that would force a future catalog extension at this shape to register the same template bodies). Every K registered at this shape inherits the following five templates by the catalog's hand-curation:

`pair_K(a, b)         ≡ (E τ ∈ A_K^Σ :: from₁(τ) = a ∧ to₁(τ) = b)`

`from_K(a)            ≡ {τ ∈ A_K^Σ : from₁(τ) = a}`

`to_K(b)              ≡ {τ ∈ A_K^Σ : to₁(τ) = b}`

`to_addrs_K(a)        ≡ {to₁(τ) : τ ∈ A_K^Σ ∧ from₁(τ) = a}`

`from_addrs_K(b)      ≡ {from₁(τ) : τ ∈ A_K^Σ ∧ to₁(τ) = b}`

The signatures match DirectedPair's. Without Sh4, the tuple-valued accessors `from_K` and `to_K` may contain multiple slot-pair-identical tuples (R1 keeps them distinct by tuple address; slot-pair duplicates are preserved). `pair_K` remains a Boolean: `(E τ ::)` is yes/no regardless of how many witnesses satisfy the body. The address-valued projections `to_addrs_K` and `from_addrs_K` are set-comprehensions over slot-addresses, so any multiplicity from `from_K`/`to_K` collapses on the address side.

Two catalog extensions sit atop NonIdempotentDirectedPair's base templates: a per-K *opt-in extension* registered through SingleHomeCoverageDiscipline (`latest_K_for_addr`), and a *parametric consumption pattern* taking a Resolution-shape type-index argument (`_via` templates). The two are jointly registrable at a single K — a K may opt into SHCD *and* be consumed by another K's `_via` parametric column without conflict, since the two extensions touch disjoint parts of the registry row. The subsections below describe each extension; their named roles ("Coverage", "Comment") are layer-level vocabulary for typical downstream uses, not catalog gates restricting which K's are eligible for which extension.

#### SHCD opt-in extension — `latest_K_for_addr` (per-K, via SingleHomeCoverageDiscipline)

The motivating downstream use is *coverage* — a witnessing document covers (reviews, revises, evaluates) a target document, with the from-slot identifying the *witness/asserter* (the document making the coverage claim, e.g., a review document) and the to-slot identifying the *subject* (the document being covered). The shape requires `c_F = 1` rather than `c_F = 0` because this typical use carries directional provenance: knowing *which* document witnessed an event is constitutive of the assertion, not auxiliary metadata. The `(0, 1)` Classifier shape already covers unattributed flags; `(1, 1)` encodes the witness-to-subject directionality. SHCD is *not* gated on this layer-level reading, however — its eligibility criterion is purely structural (the `(1, 1, A_doc, A_doc, ⊥)` shape plus the per-K registration), so any K at this shape may opt into SHCD regardless of the layer's intended semantic interpretation.

For K with SHCD opted in, multiple emissions targeting the same subject `d` are expected (e.g., evolving review status from the same or successive witnesses; or successive comments in a thread under comment-thread semantics). The opt-in `latest_K_for_addr` template projects to the most recent:

`latest_K_for_addr : A_doc → A_K^Σ ∪ {⊥}`

`latest_K_for_addr(d) ≡ argmax_{τ ∈ S_d} emission_order(τ)` &nbsp; if &nbsp; `S_d ≠ ∅`

`latest_K_for_addr(d) ≡ ⊥` &nbsp; if &nbsp; `S_d = ∅`

where `S_d = {τ ∈ A_K^Σ : to₁(τ) = d}`. The codomain is the tuple set `A_K^Σ ∪ {⊥}`; the consumer reads slot accessors off the returned tuple. The template is partial: returns `⊥` when no K-tuple targets `d`. Per the *Codomain convention*, consumers must dispatch on the `⊥` case before composing further accessors. The empty-`S_d` path fires at any state with `L_K^Σ = ∅`.

*Empty-`S_d` dispatch table* (initial-state empty regime; post-retraction emptiness on a non-idempotent K requires the consuming layer to track retraction-event coverage independently):

| Template | Evaluation at Σ | Consumer dispatch required |
|---|---|---|
| `S_d` | `{τ ∈ A_K^Σ : to₁(τ) = d} = ∅` | — (intermediate; defined as a set, not consumed directly by callers) |
| `latest_K_for_addr(d)` | `⊥` (case branch on `S_d = ∅`) | Consumer must test `≠ ⊥` *before* composing `from₁(·)`, `to₁(·)`, `addr(·)` |
| `from₁(latest_K_for_addr(d))` | *undefined* (would resolve as `from₁(⊥)`) | Caller must dispatch on the prior `⊥`; under failure, return consumer-level default (e.g., "no coverage assertion exists for `d` yet") |
| `to₁(latest_K_for_addr(d))` | *undefined* (analogous) | Same dispatch obligation |
| `addr(latest_K_for_addr(d))` | *undefined* (analogous) | Same dispatch obligation |

The undefined entries are not errors *in the framework's specification*; they are the operational meaning of the partiality token under the *Codomain convention*. A consumer that ignores the dispatch obligation is *operationally ill-formed*, not framework-non-conformant — the framework's templates remain well-defined, and the consumer is responsible for composing them under their declared codomain. The same dispatch obligation applies symmetrically to `K_target_of` (DirectedPair under FDD) and the partial slot accessors `from₁⁻`, `to₁⁻` (see Slot Accessors).

The well-definedness of `latest_K_for_addr` — that its `argmax_{τ ∈ S_d} emission_order(τ)` selects a unique tuple — is conditional on the *single-home commitment* (defined in the SingleHomeCoverageDiscipline sub-section below). Under that commitment, `emission_order` is mechanically supplied by the substrate-conforming layer's chain-index function; without it, the layer must supply a per-K `emission_order` accessor as part of its registration. See the SingleHomeCoverageDiscipline sub-section below for the discipline's definition, layer-discipline contract, preservation theorem, status, failure modes, and the well-definedness arguments for `latest_K_for_addr` under the discipline.

*Without SingleHomeCoverageDiscipline:* the `latest_K_for_addr` opt-in template is no longer determined by shape + substrate alone, since `emission_order` is no longer mechanically supplied by the substrate-conforming layer's per-document chain enumeration. The layer must supply a per-K `emission_order` accessor as part of its registration; the catalog row records this as a per-K registration obligation rather than a derived template. Sh5 itself is unchanged — its META observation (a) already acknowledges that templates are written by hand against the canonical catalog, and its META discipline (b) explicitly permits templates to depend on "explicitly named layer-supplied accessors registered in the row's opt-in or parametric columns"; an `emission_order` registration is exactly such a named accessor. SHCD-opt-in registrations that decline to commit to single-home emission must register their layer-supplied `emission_order` accessor as part of their per-K registration.

The structural eligibility for SHCD is exactly the shape `(1, 1, A_doc, A_doc, ⊥)` (matched in the registry's literal shape tuple) plus the per-K registration of SingleHomeCoverageDiscipline; SHCD does *not* depend on any semantic taxonomy distinguishing "supersession-style" from "comment-style" relations. Any K at this shape may opt into SHCD regardless of whether the layer treats the relation as a coverage assertion, a comment thread with ordering semantics, or any other reading consistent with the shape — and may simultaneously be consumed by another K's `_via` templates (the parametric extension below), since the two extensions are jointly registrable.

*Nelson's design vocabulary on links and semantics.* Nelson's design intent (Literary Machines) is explicit that all Xanadu links share one mechanism, with semantic interpretation (supersession, comment, citation, etc.) carried entirely by the type endset's address and interpreted at the front end, not by the storage substrate. The framework reflects this design: the relational layer is deliberately neutral about whether a given K is "principled" or "incidental" in its non-idempotency, and the registry admits SHCD at any `(1, 1, A_doc, A_doc, ⊥)` K that registers the opt-in. Layers that consume `latest_K_for_addr` at a K with comment-thread semantics — where the "latest by emission order" reading is one consumption pattern alongside others — are equally well-served by the framework as layers that consume it at a K with supersession semantics; the registry does not adjudicate. The "Coverage" name is layer-level vocabulary for the empirically-observed pattern in this framework's downstream consumers, not a catalog gate that privileges supersession-style readings.

#### SingleHomeCoverageDiscipline (per-K, optional)

**Definition — SingleHomeCoverageDiscipline (conditional on the *single-home commitment*).** A K registered at NonIdempotentDirectedPair (shape `(1, 1, A_doc, A_doc, ⊥)`) commits to *single-home emission* iff every emission `Emit_K(Σ, d, F, G)` for type K uses a single fixed home document `d = d_K ∈ dom(Σ.M)` across the relation's lifetime. Eligibility is purely structural — any K at this shape may opt in, with no semantic-role precondition. The commitment is a per-K registration constraint, not a universal shape constraint. SHCD's conclusion — the homed-set property `(A τ ∈ L_K^Σ :: home(addr(τ)) = d_K)` — is load-bearing only under the *single-home commitment* (defined below; the contract's clauses (i)–(ii) gate every `Emit_K` call site for SHCD-registered K), so callers depending on the homed-set property (e.g., `latest_K_for_addr`'s well-definedness via `emission_order`) must verify the contract's clauses are honored at every SHCD-registered K. Structurally parallel to FunctionalDependencyDiscipline under DirectedPair: each is a per-K opt-in discipline atop its base shape, each is realized through a layer-discipline contract with its own preservation theorem.

*Single-home commitment (the layer-discipline contract for SingleHomeCoverageDiscipline).* The discipline is realized through the *single-home commitment* — the third per-K layer-discipline contract in the framework, distinct from the *Sh4 idempotency contract* and the *FDD functional-dependency contract*. The consolidated commitment reference table in *Scope and Substrate Scaffolding* records this commitment's signature (gate position 1, applicable K's with NonIdempotentDirectedPair shape + per-K SHCD opt-in, discharged theorem SHCD's homed-set commitment) alongside the framework's other named commitments. Under the *single-home commitment*, for each K with SingleHomeCoverageDiscipline registered, on every `Emit_K(Σ, d, F, G)` call site the layer enforces the following single-step protocol:


(i) If `d ≠ d_K`, the call is *rejected outright*: the layer does not issue `Emit_K(Σ, d, F, G)`; equivalently, `Emit_K` returns `⊥` at the layer's pre-substrate gate without invoking K.λ. (The framework's Sh-conf return-type extension to `(Σ' × A_rel^{Σ'}) ∪ {⊥}` accommodates this rejection at the same `⊥`-token; the caller distinguishes single-home rejection from Sh-conf rejection by inspecting the contract's pre-emission home check `d = d_K`.)

(ii) If `d = d_K`, the layer issues `Emit_K(Σ, d, F, G)` per the substrate's usual K.λ protocol (and any other applicable contracts at the same call site — Sh4, FDD, etc. — fire in their established order).

Unlike the *Sh4 idempotency contract* and the *FDD functional-dependency contract*, the *single-home commitment* requires no Observe step: the home value `d_K` is a per-K registration constant, so the home check `d = d_K` is a literal-equality test against a fixed value, with no state-dependent computation. Atomicity is trivial (no race window exists between an Observe and the substrate K.λ-step).

*Preservation under the single-home commitment.* The single-home property holds at every reachable state under the contract, by induction on `↦*`. Fix `K ∈ T_cat` with SingleHomeCoverageDiscipline registered at fixed home `d_K`.

The single-home property `(A τ ∈ L_K^Σ :: home(addr(τ)) = d_K)` is the homed-set commitment: every K-tuple ever emitted resides under `d_K`. The companion property `S_d ⊆ {chain elements at d_K}` for every `d ∈ A_doc^Σ` follows directly: `S_d = {τ ∈ A_K^Σ : to₁(τ) = d} ⊆ A_K^Σ ⊆ L_K^Σ`, and every τ ∈ L_K^Σ has `home(addr(τ)) = d_K` by the homed-set commitment, hence `addr(τ)` is a chain element at `d_K` by the *Per-document link sub-allocator chains* scaffolding clause.


*Base.* At `Σ_0 = Σ_init`, `L_K^{Σ_0} = ∅`; the universal `(A τ ∈ L_K^{Σ_0} :: home(addr(τ)) = d_K)` is vacuous.

*Step (Case A: `L_K^{Σ'} = L_K^Σ`).* `L_K` is unchanged. The property is inherited tuple-by-tuple from the IH (no new τ to check; existing τ retain `home(addr(τ)) = d_K`).

*Step (Case B: `L_K^{Σ'} = L_K^Σ ∪ {τ_new}`).* By the *Emit_K routing commitment*, the K.λ-step originates as an `Emit_K(Σ, d, F, G)` call. The *single-home commitment* clause (i) admits the call only if `d = d_K`. Under clause (ii), K.λ's first/subsequent-emission protocol fires at home `d = d_K`, depositing τ_new at an address with `home(addr(τ_new)) = d_K` (ASN-0086, R0a-Cor1 places the deposit address in `d_K`'s link sub-allocator chain, so its home is `d_K` by L1a). So `home(addr(τ_new)) = d_K`. Combined with the IH on the older tuples, every τ ∈ L_K^{Σ'} has `home(addr(τ)) = d_K`.

*Step (Case C: `L_K^{Σ'} ⊆ L_K^Σ`)*. Impossible — L_K is monotone non-decreasing by R3. Skipped.

The induction closes. ∎

*Status.* Single-home is a *theorem under the single-home commitment*, not a substrate-enforced axiom. ASN-0086's K.λ accepts an emission at any `d ∈ dom(Σ.M)` regardless of any K-specific home; the single-home property holds for K-emissions because the *single-home commitment* rejects calls with `d ≠ d_K` at the layer's pre-substrate gate. Without the contract, the layer would admit K-emissions at distinct homes and the single-home property would fail at the resulting state.

*Failure modes under contract violation.* If the layer breaks clause (i) at any emission site — admitting an emission with `d ≠ d_K` — the homed-set commitment fails, the companion property `S_d ⊆ {chain elements at d_K}` fails, and `latest_K_for_addr`'s well-definedness argument (ii) collapses: τ ∈ S_d with `home(addr(τ)) ≠ d_K` have addresses in *other* allocators' chains, and `chain_index(addr(τ), d_K)` is undefined at those addresses. Templates consuming `emission_order` become undefined at the corrupted state. The framework's preservation theorem above is exactly what rules this out under correct contract enforcement.

*Why single-home matters for `emission_order`.* T9 (ForwardAllocation, ASN-0034) supplies a total order on outputs of a single allocator's chain — specifically, for `same_allocator(a, b) ∧ allocated_before(a, b)`, T9 gives `a < b` under T1. Tuple addresses at an SHCD-opt-in K belong to per-document link sub-allocators (the substrate-conforming layer's link-side chain enumeration referenced by Scope and Substrate Scaffolding; ASN-0086 R0a-Cor1 and FreshEmissionAddress consume this same enumeration). Under SingleHomeCoverageDiscipline, every `τ` with `to₁(τ) = d` has the same `home(τ) = d_K`, hence the same link sub-allocator chain. We define:

`emission_order(τ) := chain_index(addr(τ), d_K)`

— the *Link sub-allocator chain-index function* scaffolding clause supplies `chain_index(·, d_K) : {chain elements at d_K} → ℕ` directly as a named accessor, returning the unique `n ≥ 0` with `addr(τ) = inc^n(d_K.0.s_L.1, 0)` (well-defined and single-valued by T10a.7, EnumerationInjectivity, ASN-0034, as recorded in that scaffolding clause). `emission_order` is thus a direct composition of the scaffolding's chain-index function with `addr(·)` — no appeal to implicit chain enumeration is required, and the per-K template's well-formedness depends only on the named scaffolding accessor plus `addr(·)` (an R1 export from ASN-0086).

*Why the `argmax` in `latest_K_for_addr` is well-defined under T1.* Three ingredients:

(i) `S_d` is finite at every reachable Σ. `S_d ⊆ A_K^Σ ⊆ L_K^Σ ⊆ dom(Σ.L)`, and `dom(Σ.L)` is finite by L-fin (ASN-0043) — the link-side finiteness fact, whose content-side analog `dom(Σ.C)` finite is recorded as the content-store finiteness scaffolding clause and is the partner citation invoked at `cov_allocated`'s finiteness claim above.

(ii) The chain-index map `τ ↦ emission_order(τ)` is injective on `S_d`. Under SingleHomeCoverageDiscipline every `τ ∈ S_d` has `home(τ) = d_K`, so by the *Per-document link sub-allocator chains* scaffolding clause every such `addr(τ)` is a chain element at `d_K`. The *Link sub-allocator chain-index function* scaffolding clause then supplies a well-defined and single-valued `chain_index(addr(τ), d_K) ∈ ℕ` per τ (with single-valuedness inherited from T10a.7, EnumerationInjectivity, ASN-0034, as that scaffolding clause records). Distinct `τ, τ'` with distinct addresses (R1, AddressInjectivity, ASN-0086) therefore receive distinct chain indices, since the scaffolding's `chain_index(·, d_K)` is a function on chain-element inputs.

(iii) Chain-index order coincides with T1-order on the chain. By T9, within `A_L(d_K)`'s chain, `allocated_before(a, b) ⟹ a < b` under T1; combined with T10a.7's enumeration `tₙ₊₁ = inc(tₙ, 0)` and TA5(a)'s strict-increase under `inc(·, 0)`, the chain-index ordering on `A_L(d_K)` is strictly increasing under T1. Hence `argmax_{τ ∈ S_d} emission_order(τ)` selects the same unique element whether the ordering is read off chain-indices or off T1 — namely the τ of maximal chain-index in `S_d` (well-defined because `S_d` is finite and chain-indices are totally ordered on ℕ).

*Subset preservation when `d_K` hosts multiple relations.* SingleHomeCoverageDiscipline pins all K-tuples to one home document but does *not* require `d_K` to host only K. Other relations (any K' with `home(emission) = d_K`) interleave their tuples with K's into `d_K`'s link sub-allocator chain, so the chain-indices occupied by K-tuples need not be contiguous — chain indices 0, 2, 5 might be K while 1, 3, 4 are other relations. The argmax remains well-defined on this subset: (ii) injectivity is over `S_d ⊆ {chain elements at d_K}` and restricts to any subset; (iii) the T1-order strictly increasing along chain-indices restricts unchanged to any subset. So `argmax_{τ ∈ S_d} emission_order(τ)` picks the unique element of `S_d` with maximal chain-index regardless of whether the chain-index set is contiguous; SingleHomeCoverageDiscipline therefore does not constrain `d_K`'s exclusivity to K, only K's exclusivity to `d_K`.

#### Parametric consumption — `_via` templates (parametric in `K_res`)

The motivating downstream use is *comments* — events where each emission is distinct even with identical slot-addresses, threaded through a separate Resolution-shaped relation that records which comments have been resolved. The parametric extension adds a template family taking a *resolver-type argument* `K_res` of Resolution shape — the extension does not co-register a particular resolver at the type level. The framework treats any active `K_res`-typed tuple targeting τ's address as resolving τ, regardless of provenance: there is no notion of "the K_res paired with K"; the layer chooses which Resolution-shaped relation to consult when querying resolution status. The eligibility criterion for parametric `_via` consumption is purely structural (the `(1, 1, A_doc, A_doc, ⊥)` shape at the consumer K plus a Resolution-shape `K_res` argument at evaluation time), with no constraint on whether the consumer K also opts into SHCD.

*Template signature with shape precondition on `K_res`.* Both `unresolved_K_comments_via` and `all_K_resolved_via` take a type-index argument `K_res ∈ T_cat` whose shape must equal Resolution's canonical tuple `(1, 1, A_doc, A_rel, ⊤)`. The shape precondition is part of the signature, not an after-the-fact compatibility check:

`unresolved_K_comments_via : (K_res ∈ T_cat with shape(K_res) = (1, 1, A_doc, A_rel, ⊤)) × A_doc → ℘_fin(A_K^Σ)`

`all_K_resolved_via : (K_res ∈ T_cat with shape(K_res) = (1, 1, A_doc, A_rel, ⊤)) × A_doc → Bool`

The precondition `shape(K_res) = (1, 1, A_doc, A_rel, ⊤)` is what makes the template bodies well-typed: `resolved_by(τ, K_res)` invokes `to₁(ρ)` on `ρ ∈ A_{K_res}^Σ`, which under SlotAccessorTotality requires `K_res`'s `c_G = 1`; the comparison `to₁(ρ) = addr(τ)` lands `to₁(ρ) ∈ A_rel^Σ` opposite `addr(τ) ∈ A_rel^Σ`, which requires `K_res`'s `t_G = A_rel`. The other shape components (`c_F = 1`, `t_F = A_doc`, `idem = ⊤`) are inherited by the parametric column's commitment to *Resolution-shaped* `K_res` but are not invoked by the template bodies below. The catalog's parametric column entries on the NonIdempotentDirectedPair row carry this shape precondition implicitly by naming "Resolution" as the parametric-argument class — restated explicitly here, as Sh5(b) requires every template body to declare the registered shape of any parametric argument it consumes.

`unresolved_K_comments_via(K_res, d) ≡ {τ ∈ A_K^Σ : to₁(τ) = d ∧ ¬resolved_by(τ, K_res)}`

where `resolved_by(τ, K_res) ≡ (E ρ ∈ A_{K_res}^Σ :: to₁(ρ) = addr(τ))`.

`all_K_resolved_via(K_res, d) ≡ unresolved_K_comments_via(K_res, d) = ∅`

A comment τ is *unresolved with respect to K_res* iff no active `K_res`-tuple targets τ's address (R5, TupleSelfTargeting, ASN-0086, makes this targeting expressible). The template signature includes `K_res` explicitly because the framework imposes no co-registration between the consumer K and its resolvers: different layers may resolve the same consumer K under different `K_res`, and the predicate is well-defined parametrically across that choice, provided each choice of `K_res` satisfies the Resolution-shape precondition above.

The semantics are deliberately permissive — *any* active `K_res`-tuple targeting τ counts as a resolution, modulo whatever additional filtering the calling layer applies via its choice of `K_res`. This matches the substrate's open-ended type discipline: typed relations are claims surfaced for layer-level evaluation, not assertions adjudicated by the substrate.

*Layer-level aliasing convention.* When a calling layer commits to a single canonical resolver `K_res_canonical` for `K` (a layer convention, not a framework-level registration), it may define an alias `unresolved_K_comments(d) := unresolved_K_comments_via(K_res_canonical, d)`. This alias is a layer construct and is not part of the shape framework's template family.

These templates consume the Resolution shape parametrically — Resolution does not generate its own template family; it is consumed here.

### Provenance — `(1, 0|1, A, A, ⊤)`

Provenance tuples attribute one substrate event (the F-slot) to another (the G-slot). The G-slot may be empty (`c_G = 0|1`) — used to record agent attribution where the attributed event is the emission itself. Slot accessor `to₁⁻` is partial (returns `⊥` when G is empty); `from₁` remains total because `c_F = 1`.

*Canonical base template family (signatures forced by shape; bodies hand-curated against the DirectedPair shape-mate).* Per Sh5(b), the shape `(1, 0|1, A, A, ⊤)` *mechanically derives* the signature of each base template per the *Signature derivation rule*, but the *body* is hand-curated against the DirectedPair shape-mate row — adapting DirectedPair's templates with the asymmetry that `c_G = 0|1` requires explicit `⊥`-handling on G-side templates. The F-side templates close over the totality of `from₁`; the G-side templates must filter out tuples whose `to₁⁻` is undefined before applying the to-side accessor. Per *Status of per-shape uniformity* in Sh5(a), the framework supplies no mechanical gate that would force the present body-shape choices to be the *only* admissible ones at this shape; the bodies below are the catalog's hand-curated commitments. Codomains follow the *Codomain convention for partial templates* established for partial accessors above:

`outgoing_K       : A^Σ → ℘_fin(A_K^Σ)`
`outgoing_K(s)    ≡ {τ ∈ A_K^Σ : from₁(τ) = s}`

`pair_K           : A^Σ × A^Σ → Bool`
`pair_K(a, b)     ≡ (E τ ∈ A_K^Σ :: from₁(τ) = a ∧ to₁⁻(τ) = b)`

`from_K           : A^Σ → ℘_fin(A_K^Σ)`
`from_K(a)        ≡ {τ ∈ A_K^Σ : from₁(τ) = a}`

`to_K             : A^Σ → ℘_fin(A_K^Σ)`
`to_K(b)          ≡ {τ ∈ A_K^Σ : to₁⁻(τ) = b}`  (tuples with `to₁⁻(τ) = ⊥` are excluded because `⊥ ≠ b` for any `b ∈ A^Σ`)

`from_addrs_K     : A^Σ → ℘_fin(A^Σ)`
`from_addrs_K(b)  ≡ {from₁(τ) : τ ∈ A_K^Σ ∧ to₁⁻(τ) = b}`

`to_addrs_K       : A^Σ → ℘_fin(A^Σ)`
`to_addrs_K(a)    ≡ {to₁⁻(τ) : τ ∈ A_K^Σ ∧ from₁(τ) = a ∧ to₁⁻(τ) ≠ ⊥}`  (the `⊥`-filter is required because the set comprehension's codomain must remain `A^Σ`)

`outgoing_K(s)` is identical in body to `from_K(s)` and is retained as a named alias because the *outgoing* reading — "the set of provenance tuples sourced at the agent s" — is the dominant downstream consumption pattern; `from_K` is the role-neutral name. Predicates over provenance are typically composed atomically into agent-attribution and audit queries. The unrestricted target domains (`t_F = t_G = A`) reflect that provenance can attribute either document events or relational events to either kind of source. *Asymmetry of `to_K` against DirectedPair's `to_K`:* under DirectedPair (`c_G = 1`), `to_K` collects every tuple in the relation since `to₁` is total; under Provenance (`c_G = 0|1`), `to_K(b)` necessarily excludes the agent-attribution-only tuples (those with `to₁⁻(τ) = ⊥`). Consumers querying "all attribution sources" should use `outgoing_K` (or `from_K`) rather than `to_K`'s codomain.


## Worked Example: K = comment

To verify the framework on a concrete instance, register `K = comment` at NonIdempotentDirectedPair (shape `(1, 1, A_doc, A_doc, ⊥)`) and exercise the parametric `_via` templates with a Resolution-shape `K_res`. The walkthrough's `Σ_0` is reached from `Σ_init` by a finite sequence of K.σ/K.α steps (no K.λ-steps), so `dom(Σ_0.L) = ∅`. Pre-allocate two documents `d_1, d_2 ∈ A_doc^{Σ_0}` and two home documents `home_K, home_R ∈ dom(Σ_0.M)` (`home_K` for Comment emissions, `home_R` for Resolution emissions; single-home not required for either, we use one home per relation for simplicity).

*Registered catalog for this walkthrough.* `T_cat = {comment, K_res, R}` (closure under `~` implicit). Distinctive entries: `comment` (the NonIdempotentDirectedPair K under exercise via the `_via` parametric extension, shape `(1, 1, A_doc, A_doc, ⊥)`, with no SHCD opt-in registered) and `K_res` (a Resolution-shape relation, shape `(1, 1, A_doc, A_rel, ⊤)`; registered at `Σ_init` per lifetime constancy but first exercised at Emission 3 below). Every type used in the rejection cases below is checked against this explicit `T_cat`: `K_ghost` of Rejection case 4 is verifiable as `∉ T_cat` exactly because the catalog above does not name it.

**Emission 1.** `Emit_K(Σ_0, home_K, F_1, G_1)` with `F_1 = {(d_1, δ(1, #d_1))}` (commenter is d_1) and `G_1 = {(d_2, δ(1, #d_2))}` (target is d_2). Let the result be Σ_1 with new tuple `τ_1`. K.λ's first-emission branch fires at home_K: `{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = home_K} = ∅` (since `dom(Σ_0.L) = ∅` by the initial-state baseline above), so `a_1 := addr(τ_1) = [home_K.0.s_L.1]` (ASN-0086, K.λ first-emission deposit address).

*Sh-conf check at Σ_0.* F_1 canonical-slot, `slot_addrs(F_1) = {d_1}`, `|{d_1}| = 1`, matches `c_F = 1`. G_1 canonical-slot, `slot_addrs(G_1) = {d_2}`, `|{d_2}| = 1`, matches `c_G = 1`. `{d_1} ⊆ A_doc^{Σ_0}` (d_1 allocated) and `{d_2} ⊆ A_doc^{Σ_0}` (d_2 allocated). Admitted. ✓

**Emission 2.** `Emit_K(Σ_1, home_K, F_2, G_2)` with `F_2 = {(d_2, δ(1, #d_2))}` (commenter is d_2) and `G_2 = {(d_2, δ(1, #d_2))}` (target is d_2 again). Let the result be Σ_2 with new tuple `τ_2`. K.λ's subsequent-emission branch now fires at home_K: `{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = home_K} = {a_1}` (non-empty after Emission 1), so `ℓ_prev = max{a_1} = a_1` under T1 and `a_2 := addr(τ_2) = inc(a_1, 0)` (ASN-0086, K.λ subsequent-emission deposit address).

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

**Rejection case 1: non-canonical from-set.** From Σ_4, attempt `Emit_K(Σ_4, home_K, F_3, G_3)` with `F_3 = {(d_1, δ(2, #d_1))}` — a width-2 displacement violating canonical-slot form, which requires unit-width displacements `δ(1, #x)` (the canonical form fixes the last-component value at 1; values ≥ 2 are rejected). Here `δ(2, #d_1)` and the canonical `δ(1, #d_1)` share the same length `#d_1` — the displacement *depth* is identical; they differ only at the last component, where the canonical form admits the value 1 and rejects 2. Sh-conf clause (a) fails: `F_3` is not in canonical-slot form, so `slot_addrs(F_3)` is undefined (there is no `X_F` such that `F_3 = {(x, δ(1, #x)) : x ∈ X_F}`). The emission is rejected before any state transition. State remains Σ_4 unchanged; in particular `L_K^{Σ_4}, A_K^{Σ_4}` are not modified. ✗

Note that L4 (EndsetGenerality, ASN-0043) permits `F_3` in the substrate's link store at the level of endset well-formedness; the framework rejects it as a layer-level discipline imposed by Sh-conf. The substrate primitive K.λ would still accept `F_3` if invoked outside Emit_K — but per the *Emit_K routing commitment* (Scope and Substrate Scaffolding), the relational layer routes all class-(iii) emissions of `K ∈ T_cat` through Emit_K, so this bypass is not exercised within the framework's scope.

**Rejection case 2: unallocated to-slot address.** From Σ_4, let `d_ghost ∈ T` be a tumbler outside `A^{Σ_4}` — an unallocated address (e.g., a future document not yet registered, or a deliberately-chosen ghost per L9 of ASN-0043). Attempt `Emit_K(Σ_4, home_K, F_4, G_4)` with `F_4 = {(d_1, δ(1, #d_1))}` (canonical-slot, `slot_addrs(F_4) = {d_1}`) and `G_4 = {(d_ghost, δ(1, #d_ghost))}` (canonical-slot, `slot_addrs(G_4) = {d_ghost}`). Sh-conf clause (d) fails on the G-side: `slot_addrs(G_4) = {d_ghost}` is not a subset of `t_G^{Σ_4} = A_doc^{Σ_4}` because `d_ghost ∉ A_doc^{Σ_4}`. The emission is rejected before any state transition. State remains Σ_4. ✗

This rejection is constitutive of the framework's discipline: shapes restrict slot addresses to *already-allocated* targets at emission time. L9 (TypeGhostPermission, ASN-0043) admits ghost spans in endsets generally — including in the type-endset slot — but the shape framework forbids ghost addresses in *slot positions* of registered relations. Whether a future shape family should admit ghost-targeting slot semantics is an open question (see Open Questions).

**Rejection case 3: cardinality mismatch.** From Σ_4, attempt `Emit_K(Σ_4, home_K, F_5, G_5)` with `F_5 = {(d_1, δ(1, #d_1)), (d_2, δ(1, #d_2))}` (canonical-slot, but `slot_addrs(F_5) = {d_1, d_2}` with `|·| = 2`) and `G_5 = {(d_2, δ(1, #d_2))}` (canonical-slot, single slot address). Sh-conf clause (c) fails on the F-side: `match(2, c_F = 1)` is false (cardinality 2 does not match the exact-1 requirement). The emission is rejected before any state transition. State remains Σ_4. ✗

Symmetric rejection: emitting with `F_5' = ∅` against `c_F = 1` fails on `match(0, 1)`; emitting with the same `G_5` swapped for an empty G fails on `match(0, c_G = 1)`. Cardinality is the second of Sh-conf's three independently-checked structural gates (canonical form, cardinality, target domain); a mismatch at any gate rejects.

**Rejection case 4: unregistered type (K ∉ T_cat).** Let `K_ghost ∈ T_admissible \ T_cat` be a non-empty type endset that has not been registered with the catalog — for example, a type endset whose coverage class corresponds to no canonical shape, perhaps because the calling layer has not yet declared the relation, or because the type was constructed ad-hoc and never added to `T_cat`. Attempt `Emit_{K_ghost}(Σ_4, home_K, F_6, G_6)` with arbitrary `F_6, G_6 ∈ Endset` — concretely, we reuse Emission 1's values: `F_6 = F_1 = {(d_1, δ(1, #d_1))}` and `G_6 = G_1 = {(d_2, δ(1, #d_2))}`, both canonical-slot and well-allocated. Sh-conf's first conjunct `K_ghost ∈ T_cat` is *false* at the coverage-equivalence membership test against the registered representative list (per the *Decidable membership* paragraph in the TypedRelationCatalog Definition above): `K_ghost`'s coverage class is not one of the registered classes, so no representative `K_rep` in the list satisfies `K_ghost ~ K_rep`. The emission is rejected at this gate; `Emit_K` returns `⊥` (per Sh-conf's extended return type) and no state transition occurs. The second conjunct `conf_{K_ghost}^{Σ_4}(F_6, G_6)` is unevaluable — `shape(K_ghost)` is undefined for unregistered K, so the conformance predicate has no shape tuple to test against — but the first conjunct's failure is sufficient to reject without proceeding to the conformance check. State remains Σ_4. ✗

The `K ∈ T_cat` gate is structurally separate from the three conformance gates (clauses (a)–(d) of Sh-conf). It protects the framework's invariants against accidental schema drift: only registered relations participate in shape-discipline reasoning, and emissions at unregistered types are rejected at the registry boundary regardless of how their `F, G` are structured. A layer that wants to admit `K_ghost` must first register it with the catalog — selecting a shape, committing to the per-class constancy of `shape(·)`, and accepting Sh-conf's structural gates for all subsequent emissions at that K.

**Edge case: retraction of τ_1.** From Σ_4, issue `Nullify(Σ_4, d_retr, a_1)` producing Σ_5. By R6c (RestorationByReemission, ASN-0086), τ_1 is permanently removed from `A_K^Σ` for all future states. So:

`A_K^{Σ_5} = {τ_2}` (τ_1 nullified; τ_2 remains).

`unresolved_K_comments_via(K_res, d_2) = {τ ∈ A_K^{Σ_5} : to₁(τ) = d_2 ∧ ¬resolved_by(τ, K_res)} = ∅` (τ_2 still resolved by ρ_2, which is in `A_{K_res}^{Σ_5}`).

`all_K_resolved_via(K_res, d_2) = true`.

The framework gives stable, well-typed answers across emission and retraction events. Sh0–Sh3 are preserved inductively, template signatures match the shape registry, and the active-subset machinery composes cleanly with retraction.


## Additional Worked Examples

### Coverage under SingleHomeCoverageDiscipline

Register `K = review` at NonIdempotentDirectedPair (shape `(1, 1, A_doc, A_doc, ⊥)`) with SingleHomeCoverageDiscipline opted in, committed to single-home emission at `d_K ∈ dom(Σ_0.M)`. Pre-allocate `d_witness, d_subject ∈ A_doc^{Σ_0}` and `d_witness' ∈ A_doc^{Σ_0}`. Assume `dom(Σ_0.L) = ∅` (no links of any type yet emitted), so K.λ's first-emission predicate at `d_K` will fire at Emission C1.

*Registered catalog for this walkthrough.* `T_cat = {review, R}` (closure under `~` implicit). Distinctive: `review` is registered at NonIdempotentDirectedPair with the SHCD opt-in extension active at the per-K layer-discipline level. The walkthrough's reference to `Nullify(Σ_3, d_retr, a_3)` in the retraction segment invokes the bare-form retraction alias against `R`.
**Empty-`S_d` baseline at Σ_0.** Before C1, `A_K^{Σ_0} = ∅`, so `S_{d_subject} = ∅` and `latest_K_for_addr(d_subject) = ⊥`. Consumer dispatch obligations follow the *Empty-`S_d` dispatch table* of the SHCD opt-in extension.

**Emission C1.** `Emit_K(Σ_0, d_K, F_C1, G_C1)` with `F_C1 = {(d_witness, δ(1, #d_witness))}` (witness) and `G_C1 = {(d_subject, δ(1, #d_subject))}` (subject). Sh-conf admits (canonical-slot, cardinality 1/1, both `⊆ A_doc^{Σ_0}`). K.λ's first-emission branch fires at `d_K`: `{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = d_K} = ∅` (since `dom(Σ_0.L) = ∅`). Result Σ_1 with τ_1 at address `a_1 = [d_K.0.s_L.1]` (ASN-0086, K.λ first-emission deposit address). *Chain-index verification.* The substrate-conforming layer's *Per-document link sub-allocator chains* scaffolding enumerates `dom(A_L(d_K)) = {[d_K.0.s_L.1], inc([d_K.0.s_L.1], 0), inc^2([d_K.0.s_L.1], 0), …}`; `addr(τ_1) = [d_K.0.s_L.1]` is the chain element at index 0, so by the *Link sub-allocator chain-index function* scaffolding `chain_index(addr(τ_1), d_K) = 0`. Hence `emission_order(τ_1) = chain_index(addr(τ_1), d_K) = 0`.

**Emission C2.** `Emit_K(Σ_1, d_K, F_C2, G_C2)` with `F_C2 = {(d_witness', δ(1, #d_witness'))}` (different witness) and `G_C2 = G_C1` (same subject). Sh-conf admits. K.λ's subsequent-emission branch fires at `d_K`: `{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = d_K} = {a_1}` (non-empty after C1), so `ℓ_prev = max{a_1} = a_1` under T1 and `a_2 := addr(τ_2) = inc(a_1, 0)` (ASN-0086, K.λ subsequent-emission deposit address). Result Σ_2 with τ_2 at address `a_2`. *Chain-index verification.* By construction `a_2 = inc(a_1, 0) = inc(inc^0([d_K.0.s_L.1], 0), 0) = inc^1([d_K.0.s_L.1], 0)` (where `inc^0` denotes the identity), so `a_2` is the chain element at index 1. Hence `chain_index(addr(τ_2), d_K) = 1` and `emission_order(τ_2) = 1`.

**Emission C3.** `Emit_K(Σ_2, d_K, F_C3, G_C3)` with `F_C3 = F_C1` (original witness again) and `G_C3 = G_C1` (same subject). Coverage's `idem = ⊥` admits this even with identical slot-addresses to C1. K.λ's subsequent-emission branch fires: `{ℓ' ∈ dom(Σ_2.L) : origin(ℓ') = d_K} = {a_1, a_2}`, with `T1`-maximum `a_2` (by `a_1 < a_2` from TA5(a) at `inc(·, 0)`); so `ℓ_prev = a_2` and `a_3 := addr(τ_3) = inc(a_2, 0)`. Result Σ_3 with τ_3 at `a_3`. *Chain-index verification.* By construction `a_3 = inc(a_2, 0) = inc(inc^1([d_K.0.s_L.1], 0), 0) = inc^2([d_K.0.s_L.1], 0)`, so `a_3` is the chain element at index 2. Hence `chain_index(addr(τ_3), d_K) = 2` and `emission_order(τ_3) = 2`.

*Summary.* `A_K^{Σ_3} = {τ_1, τ_2, τ_3}` occupies chain indices 0, 1, 2; `argmax` selects τ_3 (chain-index 2).

**Rejection case C4 (single-home commitment clause (i)).** From Σ_3, with `d_other ≠ d_K`, attempt `Emit_K(Σ_3, d_other, F_C1, G_C1)`. The home check `d_other = d_K` fails; the call is rejected at gate 1, returning `⊥`. State unchanged. ✗

**Template evaluation at Σ_3.** All five NonIdempotentDirectedPair base templates plus the SHCD-opt-in `latest_K_for_addr` are evaluated below; recall `A_K^{Σ_3} = {τ_1, τ_2, τ_3}` with `from₁(τ_1) = d_witness, to₁(τ_1) = d_subject`, `from₁(τ_2) = d_witness', to₁(τ_2) = d_subject`, `from₁(τ_3) = d_witness, to₁(τ_3) = d_subject`.

| Template | Evaluation at Σ_3 | Notes |
|---|---|---|
| `pair_K(d_witness, d_subject)` | `(E τ ∈ A_K^{Σ_3} :: from₁(τ) = d_witness ∧ to₁(τ) = d_subject) = true` | Witnessed by τ_1 (and τ_3). |
| `pair_K(d_witness', d_subject)` | `= true` | Witnessed by τ_2. |
| `from_K(d_witness)` | `{τ ∈ A_K^{Σ_3} : from₁(τ) = d_witness} = {τ_1, τ_3}` | Cardinality 2 set — `idem = ⊥` admits slot-pair-identical tuples (τ_1 and τ_3 share `(from₁, to₁) = (d_witness, d_subject)`), but they are distinct in `A_K` by R1. |
| `from_K(d_witness')` | `= {τ_2}` | Singleton. |
| `to_K(d_subject)` | `{τ ∈ A_K^{Σ_3} : to₁(τ) = d_subject} = {τ_1, τ_2, τ_3}` | All three tuples target `d_subject`. |
| `from_addrs_K(d_subject)` | `{from₁(τ) : τ ∈ A_K^{Σ_3} ∧ to₁(τ) = d_subject} = {d_witness, d_witness'}` | Set-comprehension collapses τ_1 and τ_3's identical `from₁` to a single element. |
| `to_addrs_K(d_witness)` | `{to₁(τ) : τ ∈ A_K^{Σ_3} ∧ from₁(τ) = d_witness} = {d_subject}` | Singleton. |
| `to_addrs_K(d_witness')` | `= {d_subject}` | Singleton. |
| `latest_K_for_addr(d_subject)` | `argmax_{τ ∈ S_{d_subject}} emission_order(τ) = τ_3` (chain-index 2) | SHCD-opt-in; `S_{d_subject} = to_K(d_subject) = {τ_1, τ_2, τ_3}`. |

Reading the witness off the returned tuple at the SHCD-opt-in row: `from₁(τ_3) = d_witness`. The consumer recovers both the latest assertion *and* its attribution.

Sh4 suppression does *not* fire at NonIdempotentDirectedPair's `idem = ⊥`: emissions C1 and C3 share slot-pair `(d_witness, d_subject)` but both land in `A_K^{Σ_3}` because the *Sh4 idempotency contract* applies only at `idem = ⊤`. The base-template evaluation above exhibits the multiplicity in `from_K(d_witness) = {τ_1, τ_3}` and the corresponding collapse on the address side in `from_addrs_K`/`to_addrs_K`.

If a fourth emission C4 occurs with subject `d_subject` from any witness, `latest_K_for_addr(d_subject)` advances to that new τ_4 (chain-index 3); previous tuples remain in `L_K` and `A_K` but are no longer "latest." Retracting τ_3 (issuing `Nullify(Σ_3, d_retr, a_3)`) yields Σ_4 with `A_K^{Σ_4} = {τ_1, τ_2}` and `latest_K_for_addr(d_subject) = τ_2` (chain-index 1, the maximum surviving).

### Resolution base templates exercised directly

The catalog row for Resolution `(1, 1, A_doc, A_rel, ⊤)` flags its *dominant downstream pattern* as parametric use by NonIdempotentDirectedPair's `_via` templates, but Sh5(b) *mechanically derives* the signatures of the same five-template base family at the shape (per the *Signature derivation rule*) with bodies hand-curated against the DirectedPair shape-mate — and the standalone path (a Resolution registration with no `_via` consumer in scope) is admissible under Sh5(b), as the *Standalone admissibility (settled and exhibited)* clause of the Resolution catalog walkthrough records (with the standalone path exhibited at the next sub-walkthrough below). To verify the base templates are computed identically to DirectedPair's (modulo the `t_G = A_rel` codomain shift) within an evaluable example, reuse `K_res` and `ρ_1, ρ_2` from the Comment walkthrough's Emissions 3 and 4 — this example threads `K_res` through Comment's parametric consumer in scope solely for evaluability of the worked numerical instance; the standalone admissibility claim itself is settled in the Resolution catalog walkthrough's standalone-admissibility clause and is not in question here. At Σ_4: `A_{K_res}^{Σ_4} = {ρ_1, ρ_2}`, with `ρ_1` having `from₁(ρ_1) = d_2, to₁(ρ_1) = a_1` (the address of τ_1) and `ρ_2` having `from₁(ρ_2) = d_2, to₁(ρ_2) = a_2` (the address of τ_2).

The full base-template evaluation at Σ_4 reads as follows.

| Template | Evaluation at Σ_4 | Codomain (per shape) |
|---|---|---|
| `pair_{K_res}(d_2, a_1)` | `(E ρ ∈ A_{K_res}^{Σ_4} :: from₁(ρ) = d_2 ∧ to₁(ρ) = a_1) = true` (witnessed by ρ_1) | `Bool` |
| `pair_{K_res}(d_2, a_2)` | `= true` (witnessed by ρ_2) | `Bool` |
| `from_{K_res}(d_2)` | `{ρ ∈ A_{K_res}^{Σ_4} : from₁(ρ) = d_2} = {ρ_1, ρ_2}` | `℘_fin(A_{K_res}^{Σ_4})` |
| `to_{K_res}(a_1)` | `{ρ ∈ A_{K_res}^{Σ_4} : to₁(ρ) = a_1} = {ρ_1}` | `℘_fin(A_{K_res}^{Σ_4})` |
| `to_{K_res}(a_2)` | `{ρ ∈ A_{K_res}^{Σ_4} : to₁(ρ) = a_2} = {ρ_2}` | `℘_fin(A_{K_res}^{Σ_4})` |
| `from_addrs_{K_res}(a_1)` | `{from₁(ρ) : ρ ∈ A_{K_res}^{Σ_4} ∧ to₁(ρ) = a_1} = {d_2}` | `℘_fin(A_doc^{Σ_4})` |
| `from_addrs_{K_res}(a_2)` | `{from₁(ρ) : ρ ∈ A_{K_res}^{Σ_4} ∧ to₁(ρ) = a_2} = {d_2}` | `℘_fin(A_doc^{Σ_4})` |
| `to_addrs_{K_res}(d_2)` | `{to₁(ρ) : ρ ∈ A_{K_res}^{Σ_4} ∧ from₁(ρ) = d_2} = {a_1, a_2}` | `℘_fin(A_rel^{Σ_4})` |

Every base template's body is identical to DirectedPair's at the same row position; only the codomains shift per the *signature derivation rule* of Sh5(b) — `to_K` lands in `℘_fin(A_{K_res}^{Σ_4})` (tuple-set, identical to DirectedPair) but `to_addrs_K` lands in `℘_fin(A_rel^{Σ_4})` (versus DirectedPair's `℘_fin(A_doc^{Σ_4})`) because `t_G = A_rel` for Resolution rather than `t_G = A_doc` for DirectedPair. The eight evaluations confirm Resolution's base templates compute identically to DirectedPair's at the shape-mate level — same body, same set-comprehension structure, distinguished only by the codomain symbol read off `t_G`.

### Tuple-Classifier

*Registered catalog for this walkthrough.* `T_cat = {comment, K_res, R, endorsed}` (closure under `~` implicit), augmenting Comment's `T_cat` with `endorsed`. Distinctive: `endorsed` is declared at `Σ_init` alongside `comment`, `K_res`, and `R` (not introduced mid-stream at Σ_4) per lifetime constancy. Through every K.σ/K.α/K.λ step from `Σ_init` to `Σ_4` (Comment's emissions affect only `L_{comment}` and `L_{K_res}`, never `L_{endorsed}`), `L_{endorsed}` is preserved pointwise at ∅ by R3 plus the case-decomposition of `↦` — every prior emission falls under Case A of Sh0–Sh4 at `endorsed`.
Register `K = endorsed` with shape `(0, 1, -, A_rel, ⊤)`, intended to mark comment-tuples as endorsed. Working from Σ_4 of the Comment example, with τ_2 ∈ A_rel^{Σ_4}. We reuse the home document `home_K` from the Comment example as the home for `endorsed` emissions — this exercises the framework's permission for multiple distinct relations to share a single home document. (The substrate's per-document link sub-allocator chain at `home_K` interleaves tuples of different types, with R0a-Cor1 ensuring each type's homed-set remains well-defined within the chain.) To disambiguate the symbol within this walkthrough, write `home_endorsed := home_K` for `endorsed`-emissions:

The starting state for this walkthrough is `Σ_0 := Σ_4` from the Comment walkthrough (the symbol `Σ_0` is scoped to this walkthrough per implicit per-walkthrough scoping; the result of the single emission below is `Σ_1`).

`Emit_K(Σ_0, home_endorsed, ∅, {(a_2, δ(1, #a_2))})` — F empty (matches `c_F = 0`), G targets the tuple address `a_2`. Sh-conf admits (clause (d) for F is vacuous since `-^Σ = ∅` and `slot_addrs(F) = ∅ ⊆ ∅`; G-side checks `{a_2} ⊆ A_rel^{Σ_0}`). Result `Σ_1`.

Template evaluation: `is_K(a_2) ≡ (E σ ∈ A_K^{Σ_1} :: to₁(σ) = a_2) = true`; `is_K(a_1) = false`. The same single-letter substitution `d ↝ τ` from Classifier's template body, with the signature shifted from `A_doc → Bool` to `A_rel → Bool`.

**Rejection case TC1 (Pattern 5: G-side partition mismatch, symmetric to Classifier's rejection).** This case instantiates Pattern 5 of the *Common rejection patterns* at the Tuple-Classifier shape, with Classifier as its bipartite partner. From `Σ_1`, pre-allocate or reuse a document content address `d_doc ∈ A_doc^{Σ_1}` (any `d_doc ∈ dom(Σ_1.C)`; the Comment walkthrough leaves several such addresses in scope). Attempt `Emit_K(Σ_1, home_endorsed, ∅, {(d_doc, δ(1, #d_doc))})` — G targets the document content address `d_doc ∈ A_doc^{Σ_1}` instead of a tuple address. Sh-conf clauses (a)/(b) admit canonical-slot F and G; clause (c) admits at `match(0, 0)` and `match(1, 1)`. *Clause (d) on the G-side fails*: the Tuple-Classifier shape's `t_G = A_rel`, so the G-side target-domain check reads `slot_addrs(G) = {d_doc} ⊆ A_rel^{Σ_1}`. But `d_doc ∈ A_doc^{Σ_1} = dom(Σ_1.C)`, and by R4 (TupleAddressDisjointness, ASN-0086) `A_doc^{Σ_1} ∩ A_rel^{Σ_1} = ∅`, so `d_doc ∉ A_rel^{Σ_1}`, hence `{d_doc} ⊄ A_rel^{Σ_1}`. The emission is rejected; `Emit_K` returns `⊥` per the framework's extended return type, no K.λ invocation occurs, and no `↦`-step fires. State remains `Σ_1` unchanged. The Tuple-Classifier shape's `t_G = A_rel` is precisely what blocks tuple-classifier-emissions from targeting document content addresses — the exact mirror of Classifier's rejection of tuple targets at `t_G = A_doc` (Classifier walkthrough). The two shapes are the bipartite halves of the same `(0, 1)` cardinality skeleton, partitioned by clause (d), with each rejection case exhibiting the rejection symmetric to its partner. ✗

### Provenance (partial G-slot)

*Registered catalog for this walkthrough.* `T_cat = {attributed_by, R}` (closure under `~` implicit). Distinctive: `attributed_by` is the Provenance-shape relation under exercise. The walkthrough's `Σ_0` is reached from `Σ_init` by K.σ/K.α steps allocating `s`, `s'`, `t`, `t'`, and `home_prov`.

Register `K = attributed_by` with shape `(1, 0|1, A, A, ⊤)`. Let `home_prov ∈ dom(Σ.M)` be a fresh home document for `attributed_by` emissions (distinct from any prior walkthrough's home symbol; nothing in the framework forbids reusing a prior home, but we introduce a new symbol here to keep cross-walkthrough scopes disjoint). Pre-allocate `s, s', t, t' ∈ A^{Σ_0}` (any allocated addresses, pairwise distinct; `t_F = t_G = A` admits both content and relation addresses). Two emission forms exercise the `0|1` partiality; a third emission attempt exercises Sh4 suppression at `idem = ⊤`.

**Form 1 (with target):** `Emit_K(Σ_0, home_prov, {(s, δ(1, #s))}, {(t, δ(1, #t))})` with both `s, t ∈ A^{Σ_0}`. Sh-conf admits (canonical-slot, cardinality 1/1, `s ∈ A^{Σ_0}`, `t ∈ A^{Σ_0}`). Sh4 contract clause (i) computes `C(F, G, Σ_0) = ∅` (no prior K-tuples). Clause (iii) issues the emission. Result Σ_P1 with τ_P1 at fresh address; `from₁(τ_P1) = s`, `to₁⁻(τ_P1) = t` (defined).

**Form 2 (empty target):** `Emit_K(Σ_P1, home_prov, {(s', δ(1, #s'))}, ∅)` with `s' ∈ A^{Σ_P1}` (pre-allocated above, distinct from `s`; chosen distinct from `s` here so Forms 3 and 5 can exhibit slot-address-set inequality `{s'} ≠ {s}` in their Sh4 candidate-set filtering). Sh-conf admits (G is canonical-slot trivially with `slot_addrs(∅) = ∅`; `match(0, 0|1)` holds since `0 ∈ {0, 1}`; clause (d) for G is vacuous since `slot_addrs(∅) = ∅` is a subset of any target domain). Sh4 contract: `C({(s', δ(1, #s'))}, ∅, Σ_P1) = {τ ∈ A_K^{Σ_P1} : slot_addrs(F_τ) = {s'} ∧ slot_addrs(G_τ) = ∅} = ∅` (τ_P1 has `slot_addrs(G_{τ_P1}) = {t} ≠ ∅`, so τ_P1 is filtered out by the G-slot-address-set equality test). Clause (iii) issues the emission. Result Σ_P2 with τ_P2; `from₁(τ_P2) = s'`, `to₁⁻(τ_P2) = ⊥` (undefined).

**Form 3 (Sh4 suppression on duplicate of Form 1):** Attempt `Emit_K(Σ_P2, home_prov, {(s, δ(1, #s))}, {(t, δ(1, #t))})` — identical slot-addresses to Form 1. Sh-conf clauses (a)/(b) admit canonical-slot form. Sh4 contract clause (i) computes `C({(s, δ(1, #s))}, {(t, δ(1, #t))}, Σ_P2) = {τ ∈ A_K^{Σ_P2} : slot_addrs(F_τ) = {s} ∧ slot_addrs(G_τ) = {t}}`. The post-filter retains τ_P1 (its `slot_addrs(F_{τ_P1}) = {s}` and `slot_addrs(G_{τ_P1}) = {t}` both match) but rejects τ_P2 (whose `slot_addrs(F_{τ_P2}) = {s'} ≠ {s}` fails the F-slot post-filter, and whose `slot_addrs(G_{τ_P2}) = ∅ ≠ {t}` likewise fails the G-slot post-filter). So `C = {τ_P1} ≠ ∅`. Sh4 contract clause (ii) *suppresses* the emission; `Emit_K` returns `⊥` per the framework's extended return type, no `↦`-step fires, and state remains Σ_P2 unchanged. `A_K^{Σ_P2} = {τ_P1, τ_P2}` — no third tuple added — confirming Sh4 idempotency at Provenance's `idem = ⊤`.

**Form 4 (no Sh4 suppression at distinct G):** Attempt `Emit_K(Σ_P2, home_prov, {(s, δ(1, #s))}, {(t', δ(1, #t'))})` with `t' ≠ t`. The candidate set test now requires `slot_addrs(G_τ) = {t'}`; τ_P1's `{t} ≠ {t'}` fails, τ_P2's `∅ ≠ {t'}` fails, so `C = ∅`. Sh4 contract clause (iii) issues the emission. Result Σ_P3 with τ_P3; `from₁(τ_P3) = s`, `to₁⁻(τ_P3) = t'`. Sh4 enforces slot-pair distinctness, not from-slot distinctness — Forms 1 and 4 both have `from₁ = s` but distinct `to₁⁻` values, and the framework admits both as distinct slot-pairs.

**Form 5 (no Sh4 suppression: empty-G is distinct from non-empty-G at same F):** Attempt `Emit_K(Σ_P3, home_prov, {(s, δ(1, #s))}, ∅)` — same F as Form 1, empty G. Candidate test: τ_P1 has G-slot `{t}` ≠ ∅, τ_P2 has F-slot `{s'}` ≠ `{s}`, τ_P3 has G-slot `{t'}` ≠ ∅. So `C = ∅`, clause (iii) issues. Result Σ_P4 with τ_P4; `from₁(τ_P4) = s`, `to₁⁻(τ_P4) = ⊥`. The `0|1` partiality on G distinguishes empty-G and non-empty-G as distinct slot-pair tuples at Sh4's resolution; an attribution-only emission at F = {s} is not suppressed by a prior with-target emission at the same F.

**Base-template evaluation at Σ_P4.** With `A_K^{Σ_P4} = {τ_P1, τ_P2, τ_P3, τ_P4}` (no retractions), the Provenance base templates evaluate as follows:

| Template | Evaluation at Σ_P4 | Notes |
|---|---|---|
| `outgoing_K(s)` | `{τ ∈ A_K^{Σ_P4} : from₁(τ) = s} = {τ_P1, τ_P3, τ_P4}` | Three tuples sourced at `s`. |
| `outgoing_K(s')` | `= {τ_P2}` | Singleton. |
| `pair_K(s, t)` | `(E τ ∈ A_K^{Σ_P4} :: from₁(τ) = s ∧ to₁⁻(τ) = t) = true` | Witnessed by τ_P1. |
| `pair_K(s, t')` | `= true` | Witnessed by τ_P3. |
| `pair_K(s', t)` | `= false` | No τ has `from₁ = s' ∧ to₁⁻ = t`; τ_P2 has `to₁⁻ = ⊥ ≠ t`. |
| `from_K(s)` | `{τ ∈ A_K^{Σ_P4} : from₁(τ) = s} = {τ_P1, τ_P3, τ_P4}` | Alias of `outgoing_K(s)`. |
| `to_K(t)` | `{τ ∈ A_K^{Σ_P4} : to₁⁻(τ) = t} = {τ_P1}` | τ_P2 and τ_P4 excluded because `to₁⁻ = ⊥ ≠ t` per the *Asymmetry of `to_K`* note. |
| `to_K(t')` | `= {τ_P3}` | Singleton. |
| `from_addrs_K(t)` | `{from₁(τ) : τ ∈ A_K^{Σ_P4} ∧ to₁⁻(τ) = t} = {s}` | τ_P2/τ_P4 excluded by `⊥`-filter. |
| `to_addrs_K(s)` | `{to₁⁻(τ) : τ ∈ A_K^{Σ_P4} ∧ from₁(τ) = s ∧ to₁⁻(τ) ≠ ⊥} = {t, t'}` | τ_P4 excluded by `⊥`-filter despite `from₁(τ_P4) = s`. |

Both `to_K` and `to_addrs_K` exhibit the partial-G filtering: tuples with `to₁⁻(τ) = ⊥` are excluded from G-indexed accessors by definition (codomain `A^Σ` cannot accept `⊥`), while F-indexed accessors `outgoing_K`/`from_K` include all tuples regardless of G's partiality status. Forms 1, 3, 4 exercise the canonical-form, Sh4-suppression, slot-pair-distinct-by-G, and empty-G-vs-non-empty-G regimes respectively; the table demonstrates the partial-G filtering directly on each affected base template.

### Attributed Retraction (exercising `c_F = *`)

*Registered catalog for this walkthrough.* `T_cat = {R}` (closure under `~` implicit). Distinctive: only `R` is exercised. The walkthrough's `Σ_0` is reached from `Σ_init` by K.σ/K.α steps allocating `d_attr1`, `d_attr2`, `τ_c` (a prior class-(iii) emission at some other registered K outside this `T_cat`'s scope), and `d_retr`.

The Retraction shape `(*, 1, A, A_rel, ⊤)` admits an unrestricted from-slot cardinality. Standard `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` (ASN-0086) uses the `c_F = 0` boundary; we exercise the `c_F = 1` and `c_F = 2` cases here to verify Sh-conf and the multi-slot over-approximation argument from the Sh4 contract.

Pre-allocate `d_attr1, d_attr2 ∈ A^{Σ_0}` (any allocated addresses — `t_F = A` admits both `A_doc` and `A_rel`), a comment-tuple `τ_c ∈ A_rel^{Σ_0}` at address `a_c = addr(τ_c)`, and a retraction home `d_retr ∈ dom(Σ_0.M)`.

**Emission AR1 (attributed retraction, n = 1).** `Emit_R(Σ_0, d_retr, F_AR1, G_AR1)` with `F_AR1 = {(d_attr1, δ(1, #d_attr1))}` (attribution: one retracting party) and `G_AR1 = {(a_c, δ(1, #a_c))}` (target: the comment-tuple).

*Sh-conf check at Σ_0.* F_AR1 canonical-slot with `slot_addrs(F_AR1) = {d_attr1}`, `|{d_attr1}| = 1`, `match(1, c_F = *)` ✓ (since `1 ∈ ℕ`). G_AR1 canonical-slot with `slot_addrs(G_AR1) = {a_c}`, `|{a_c}| = 1`, `match(1, c_G = 1)` ✓. Target-domain: `{d_attr1} ⊆ A^{Σ_0}` (allocated) ✓; `{a_c} ⊆ A_rel^{Σ_0}` (τ_c is a tuple address) ✓. Admitted. Result Σ_1 with new tuple ρ_1 at address `b_1 := addr(ρ_1)`.

*Effect on nullification.* By Definition (nullified, ASN-0086), `nullified(Σ_1) = {a ∈ A_rel^{Σ_1} : (E (b, F', G') ∈ L_R^{Σ_1} :: a ∈ coverage(G'))}`. With ρ_1 ∈ L_R^{Σ_1} and `coverage(G_AR1) = {t : a_c ≼ t} ⊇ {a_c}`, we get `a_c ∈ nullified(Σ_1)`. The attribution `d_attr1` in F is informational metadata for downstream consumers; it does not change `nullified(·)`'s decision procedure (which inspects G's coverage only — see Definition (nullified)).

*Sh0 verification at ρ_1.* `slot_addrs(F_AR1) = {d_attr1}`, `|·| = 1`; `match(1, *)` ✓. F_AR1 is canonical-slot by construction. Both conjuncts of Sh0's body discharge at ρ_1.

**Emission AR2 (attributed retraction, n = 2).** `Emit_R(Σ_1, d_retr, F_AR2, G_AR2)` with `F_AR2 = {(d_attr1, δ(1, #d_attr1)), (d_attr2, δ(1, #d_attr2))}` (two retracting parties) and `G_AR2 = {(a_c', δ(1, #a_c'))}` targeting a different tuple `a_c' = addr(τ_c')` with `τ_c' ∈ A_rel^{Σ_1}, τ_c' ≠ τ_c`.

*Sh-conf check at Σ_1.* F_AR2 canonical-slot with `slot_addrs(F_AR2) = {d_attr1, d_attr2}`, `|{d_attr1, d_attr2}| = 2`, `match(2, c_F = *)` ✓. G_AR2 canonical-slot, cardinality 1 ✓. Target-domain: `{d_attr1, d_attr2} ⊆ A^{Σ_1}` ✓; `{a_c'} ⊆ A_rel^{Σ_1}` ✓. Sh4 contract: `C(F_AR2, G_AR2, Σ_1)` — the per-element multi-slot over-approximation argument from clause (i.a) applies *twice*, once at `d_attr1` and once at `d_attr2`, yielding `slot_addrs(F_τ) ⊇ {d_attr1, d_attr2}` over the Observe result. Post-filter retains only τ with exact equality `slot_addrs(F_τ) = {d_attr1, d_attr2}`; ρ_1 has `slot_addrs(F_{ρ_1}) = {d_attr1} ≠ {d_attr1, d_attr2}`, so ρ_1 is filtered out, and no other tuples exist at K=R in `A_R^{Σ_1}`. `C = ∅`, contract clause (iii) issues the emission. Admitted. Result Σ_2 with new tuple ρ_2 at address `b_2 = addr(ρ_2)`.

*Sh0 verification at ρ_2.* `slot_addrs(F_AR2) = {d_attr1, d_attr2}`, `|·| = 2`; `match(2, *)` ✓ (since `2 ∈ ℕ`). F_AR2 is canonical-slot by construction. Sh0 discharges.

*Resulting state.* `L_R^{Σ_2} = {ρ_1, ρ_2}`; `A_R^{Σ_2} = {ρ_1, ρ_2}` (no retractions of retractors). `nullified(Σ_2) = {a_c, a_c'}` (G-coverage of both retractors). Sh0–Sh3 hold pointwise on the two-element relation; the framework's per-element argument from Sh4's contract (i.a) generalized cleanly to `n = 2`, validating the multi-slot reading of `c_F = *`.

**Rejection case AR3 (Pattern 5: target-domain partition — G targets A_doc instead of A_rel).** This case instantiates Pattern 5 of the *Common rejection patterns* at the Retraction shape (cf. Classifier's *Rejection (G-side partition mismatch)* and Tuple-Classifier Rejection case TC1, both of which exhibit the same partition mismatch at distinct bipartite halves). From Σ_2, pre-allocate a content address `d_doc ∈ A_doc^{Σ_2}` (a regular document-content address, not a tuple address — i.e., `d_doc ∈ dom(Σ_2.C)`). Attempt `Emit_R(Σ_2, d_retr, F_AR3, G_AR3)` with `F_AR3 = ∅` (bare Nullify form, `c_F = 0` boundary of the Retraction shape) and `G_AR3 = {(d_doc, δ(1, #d_doc))}` (G targets a content address rather than a tuple address).

*Sh-conf check at Σ_2.* F_AR3 is canonical-slot trivially with `slot_addrs(F_AR3) = ∅`; `match(0, c_F = *)` ✓ (since `0 ∈ ℕ`); clause (d) on the F-side reads `∅ ⊆ A^{Σ_2}`, vacuously true. G_AR3 is canonical-slot with `slot_addrs(G_AR3) = {d_doc}`; `match(1, c_G = 1)` ✓. *Clause (d) on the G-side fails*: the Retraction shape's `t_G = A_rel`, so the G-side target-domain check reads `slot_addrs(G_AR3) = {d_doc} ⊆ A_rel^{Σ_2}`. But `d_doc ∈ dom(Σ_2.C) = A_doc^{Σ_2}`, and by R4 (TupleAddressDisjointness, ASN-0086) `A_doc^{Σ_2} ∩ A_rel^{Σ_2} = ∅`, so `d_doc ∉ A_rel^{Σ_2}`, hence `{d_doc} ⊄ A_rel^{Σ_2}`. The emission is rejected before any state transition. `Emit_R` returns `⊥` per Sh-conf's extended return type, no K.λ invocation occurs, and no `↦`-step fires. State remains Σ_2 unchanged; in particular `L_R^{Σ_2}` and `A_R^{Σ_2}` are not modified, and `nullified(Σ_2)` is preserved. ✗

This rejection exhibits the *partition* aspect of Sh-conf clause (d) at the Retraction shape's G-side — distinct from the *allocation* aspect exercised by the Comment walkthrough's Rejection case 2 (unallocated to-slot address). Rejection case 2 attempts to point an endset at an address outside `A^Σ` altogether (a ghost address); the present case attempts to point at an *allocated* address that nonetheless lies in the *wrong* partition (content rather than relation). Both fail Sh-conf clause (d), but at different sites: case 2 fails the membership test `d_ghost ∈ A^Σ`, whereas case AR3 fails the partition restriction `d_doc ∈ A_rel^Σ` despite passing `d_doc ∈ A^Σ`. The partition rejection is constitutive of the framework's discipline at the Retraction shape: the Retraction shape's `t_G = A_rel` is precisely what secures the unit-depth retraction discipline at the framework level — every shape-conformant `Emit_R` emission targets an *active retractable address* (a tuple, not a document content unit), so the substrate's nullification machinery operates against the correct partition.

Symmetric rejections at the G-side under the Retraction shape: attempts to point G at a `dom(Σ.M)` document-level container address fail at the F-side or G-side because document-level containers are not in `A_doc^Σ = dom(Σ.C)` either (the framework provides no target-domain symbol for `dom(Σ.M)` addresses; see the *Reach of the framework's target-domain symbols* note at the Canonical Shape Catalog). Attempts to point G at a link-subspace address that has not yet been allocated (i.e., outside `dom(Σ.L) = A_rel^Σ`) fail the allocation aspect of clause (d) by the same argument as Comment's Rejection case 2. The framework's three independent clause-(d) failure modes — partition mismatch (case AR3), unallocated target (case 2), and `dom(Σ.M)` un-targetability (the framework's structural limit) — exhaust the ways an otherwise-canonical, cardinality-conformant emission can fail at the target-domain gate.

**Walkthrough: EffectiveWpSimplification at Σ_2 (third successful retraction).** To exhibit how `wp_086`'s two non-trivial conjuncts discharge step-by-step in the presence of prior R-tuples, fire the third successful retraction `AR4` at Σ_2 (the state with `L_R^{Σ_2} = {ρ_1, ρ_2}` from Emissions AR1 and AR2; the prior `AR3` attempt was rejected and produced no state). Pre-allocate a third comment-tuple `τ_c'' ∈ A_rel^{Σ_2}` at address `a_c'' = addr(τ_c'')` (the target of the new retraction), and issue the bare-Nullify-form call `Emit_R(Σ_2, d_retr, ∅, {(a_c'', δ(1, #a_c''))})` — `F_{AR4} = ∅`, `G_{AR4} = {(a_c'', δ(1, #a_c''))}`.

*Step 1: discharge `NoCraftedSpanReachesD(Σ_2, d_retr)` over each prior R-tuple in `L_R^{Σ_2}`.* By the EffectiveWpSimplification Corollary's Step 1 argument, for every `(b̂, F', G') ∈ L_R^{Σ_2}`, Sh1 at `K := R` pins `G'` canonical-slot with `|slot_addrs(G')| = 1`, and Sh3 at `K := R` pins `slot_addrs(G') ⊆ A_rel^{Σ_2} = dom(Σ_2.L)`. Walk each tuple:
- *ρ_1 (`b̂ = b_1 = addr(ρ_1)`, `F' = F_{AR1}`, `G' = G_{AR1}`).* Sh1 at ρ_1 gives `slot_addrs(G_{AR1}) = {a_c}` (one element); Sh3 places `a_c ∈ A_rel^{Σ_2}`. Apply Lemma — LinkAddressNotPrefixOfEmit at `b := a_c`, `d := d_retr` (legal because `a_c ∈ dom(Σ_2.L)` and `d_retr ∈ dom(Σ_2.M)`): the Lemma yields `a_c ⋠ a_emit(Σ_2, d_retr)`. By PrefixSpanCoverage (ASN-0043), `coverage(G_{AR1}) = {t : a_c ≼ t}`, and `a_c ⋠ a_emit(Σ_2, d_retr)` gives `a_emit(Σ_2, d_retr) ∉ {t : a_c ≼ t} = coverage(G_{AR1})`. ✓
- *ρ_2 (`b̂ = b_2 = addr(ρ_2)`, `F' = F_{AR2}`, `G' = G_{AR2}`).* Symmetric argument: `slot_addrs(G_{AR2}) = {a_c'}` for `a_c' ∈ A_rel^{Σ_2}`; Lemma at `b := a_c'` yields `a_c' ⋠ a_emit(Σ_2, d_retr)`, hence `a_emit(Σ_2, d_retr) ∉ coverage(G_{AR2})`. ✓

Quantifying over both members of `L_R^{Σ_2}`, the universal `(A (b̂, F', G') ∈ L_R^{Σ_2} :: a_emit(Σ_2, d_retr) ∉ coverage(G'))` of ASN-0086's `NoCraftedSpanReachesD` definition holds. Step 1 discharges. ✓

*Step 2: discharge `(K ≁ R ∨ a_emit(Σ_2, d_retr) ∉ coverage(G_{AR4}))` for the new emission.* The new call's type is `K = R`, so `K ~ R` by reflexivity of `~` — Case B of Step 2's case-split fires (the first disjunct's arm is *false*; the second arm must be discharged). By Sh-conf admission of the new call with `shape(R) = (*, 1, A, A_rel, ⊤)`, Sh-conf clause (a) on `F_{AR4} = ∅` is trivially canonical-slot; clause (b) on `G_{AR4}` forces canonical-slot form; clause (c) at `c_G = 1` forces `|slot_addrs(G_{AR4})| = 1`; clause (d) at `t_G = A_rel` forces `slot_addrs(G_{AR4}) = {a_c''} ⊆ A_rel^{Σ_2}`. Apply Lemma — LinkAddressNotPrefixOfEmit at `b := a_c''`, `d := d_retr`: `a_c'' ⋠ a_emit(Σ_2, d_retr)`. By PrefixSpanCoverage, `coverage(G_{AR4}) = {t : a_c'' ≼ t}`, so `a_emit(Σ_2, d_retr) ∉ coverage(G_{AR4})`. The disjunct's second arm holds. ✓

With both `wp_086` non-trivial conjuncts discharged, `wp_086` reduces to `d_retr ∈ dom(Σ_2.M) ∧ R ∈ T_admissible`. Both hold trivially (`d_retr` is the registered retraction home; `R ∈ T_cat ⊆ T_admissible` by the framework's mandatory R-registration). The new emission is admitted, producing Σ_3 with `ρ_3 ∈ L_R^{Σ_3}` at a fresh address.

*Contrast — non-R call at the same Σ_2.* Were the new emission instead at `K = comment` (with `comment ≁ R` because `shape(comment) = (1, 1, A_doc, A_doc, ⊥)` and `shape(R) = (*, 1, A, A_rel, ⊤)` give distinct coverage classes), Step 2's Case A would fire: `K ≁ R` directly satisfies the first disjunct's arm, and the second arm is not consulted. The Lemma's role at the new emission's G-slot disappears for non-R calls — Step 1's prior-R-tuple discharge still applies (the universal over `L_R^{Σ_2}` is independent of the new call's type), but Step 2 simplifies to a Case A check that fires without the Lemma at the new G-slot. Both cases close out `wp_086`'s simplification at the framework's effective wp.

*Registered catalog for this walkthrough.* `T_cat = {attribute, R}` (closure under `~` implicit). Distinctive: `attribute` is the DirectedPair-shape relation registered together with FunctionalDependencyDiscipline. The empty-baseline is *required* (not merely sufficient) for FDD's preservation per the *Scope of the per-tuple-conformance relaxation* paragraph in Initial-State Baseline.

Register `K = attribute` with shape `(1, 1, A_doc, A_doc, ⊤)` (DirectedPair) and additionally register FunctionalDependencyDiscipline at K. Pre-allocate `d_parent, d_sidecar1, d_sidecar2 ∈ A_doc^{Σ_0}` and a fresh home `home_attr ∈ dom(Σ_0.M)` for `attribute` emissions (distinct from any home symbol introduced in prior walkthroughs; we use a relation-specific name to keep this walkthrough self-contained).

**Emission FDD1.** `Emit_K(Σ_0, home_attr, F_{FDD1}, G_{FDD1})` with `F_{FDD1} = {(d_parent, δ(1, #d_parent))}` (parent in from-slot) and `G_{FDD1} = {(d_sidecar1, δ(1, #d_sidecar1))}` (sidecar in to-slot).

*FDD contract clause (i):* Compute `C_fd(F_{FDD1}, Σ_0)` via the two-step procedure. (i.a) `Observe_K(slot_addrs(F_{FDD1}), ∅, oper) = Observe_K({d_parent}, ∅, oper)` returns ∅ (no prior K-tuples at the initial state). (i.b) Post-filter is vacuous on the empty result. `C_fd(F_{FDD1}, Σ_0) = ∅`.

*FDD contract clause (iii):* The candidate set is empty, so the layer issues `Emit_K(Σ_0, home_attr, F_{FDD1}, G_{FDD1})`. Sh-conf admits (canonical-slot, cardinality 1/1, `{d_parent} ⊆ A_doc^{Σ_0}`, `{d_sidecar1} ⊆ A_doc^{Σ_0}`). Result Σ_1 with τ_FDD1 at address `a_FDD1`.

*Singleton accessor evaluation at Σ_1.* `from_K(d_parent) = {τ_FDD1}` (unique element). `K_target_of(d_parent) = to₁(τ_FDD1) = d_sidecar1` (the well-defined singleton-returning accessor).

**Emission FDD2 (rejected by FDD contract clause (ii)).** Attempt `Emit_K(Σ_1, home_attr, F_{FDD2}, G_{FDD2})` with `F_{FDD2} = F_{FDD1}` (same parent) and `G_{FDD2} = {(d_sidecar2, δ(1, #d_sidecar2))}` (different sidecar — `d_sidecar2 ≠ d_sidecar1`). Note `G_{FDD2} ≠ G_{FDD1}`, so under Sh4 alone this emission would be *admitted* (slot-pair-distinct from τ_FDD1: Sh4's `C(F, G, Σ)` requires both slots to match).

*FDD contract clause (i):* Compute `C_fd(F_{FDD2}, Σ_1)`. (i.a) `Observe_K({d_parent}, ∅, oper)` returns `{τ_FDD1}` (τ_FDD1's F-coverage `{t : d_parent ≼ t}` contains d_parent). (i.b) Post-filter retains τ_FDD1 because `|slot_addrs(F_{τ_FDD1})| = |{d_parent}| = 1 = |slot_addrs(F_{FDD2})|`, forcing `slot_addrs(F_{τ_FDD1}) = {d_parent} = slot_addrs(F_{FDD2})` under the AllocatedAddressAntichain over-approximation. So `C_fd(F_{FDD2}, Σ_1) = {τ_FDD1} ≠ ∅`.

*FDD contract clause (ii):* The candidate set is non-empty, so the emission is *suppressed*. The layer returns `⊥` (per Sh-conf's extended return type). No `↦`-step occurs. State remains Σ_1; `A_K^{Σ_1} = {τ_FDD1}` unchanged.

*Singleton accessor evaluation post-suppression.* `from_K(d_parent) = {τ_FDD1}` (still unique). `K_target_of(d_parent) = d_sidecar1` (unchanged). FDD preserves single-valuedness of the singleton accessor across the duplicate-from-slot emission attempt.

**Contrast with Sh4 alone (FDD not registered).** Were the same K registered with bare DirectedPair shape (no FDD), Emission FDD2 would be admitted: Sh4's `C(F, G, Σ_1) = {τ ∈ A_K^{Σ_1} : slot_addrs(F_τ) = {d_parent} ∧ slot_addrs(G_τ) = {d_sidecar2}} = ∅` (τ_FDD1 fails the G-slot match), so suppression does not fire. The emission proceeds, producing `A_K^{Σ_2} = {τ_FDD1, τ_FDD2}` with `from_K(d_parent) = {τ_FDD1, τ_FDD2}` — a cardinality-2 set, on which a singleton-returning `K_target_of(d_parent)` would be ill-defined (it would have to choose between `d_sidecar1` and `d_sidecar2`). This is exactly the failure mode FDD prevents by restricting `C_fd` to the from-slot match.

## Consequences

(a) *Adding a new relation inherits its shape-mate's templates by hand-curation.* A new K registered at `shape(K) = DirectedPair` inherits the row's five base templates (`pair_K`, `from_K`, `to_K`, `from_addrs_K`, `to_addrs_K`) by the catalog's current hand-curation against the DirectedPair shape-mate, with signatures mechanically derived per Sh5(b)'s *Signature derivation rule*. Body-shape convergence with prior shape-mate rows is an aspiration of the present catalog (per Sh5(a)'s downgrade), not a framework-enforced derivation: registering a divergent template body at the same shape is not blocked by any mechanical gate. The cost of a new relation is one entry in the shape registry plus the author's diligence at Sh5(b)'s checklist. Layers consuming an Attribute-style or Citation-style reading further define aliases (`has_K`, `K_sidecars_of`, `cites_K`, `K_incoming`); the singleton-returning `K_target_of` becomes available when the layer additionally registers FunctionalDependencyDiscipline.

(b) *Composite predicates extend the catalog through the same compositional primitives.* A composite predicate combines atomic templates through Boolean operators and quantification over `T_cat`. The framework does not establish a closure theorem about these primitives — whether composition can express predicates strictly beyond what the catalog's atomic templates yield is a property of the composition language adopted, not a structural guarantee of Sh5. The design observation we record is weaker: the canonical-shape catalog is the registry's *atomic* vocabulary, and adding a structurally new pattern (e.g., a slot-cardinality combination not yet present) is handled by extending the catalog with a new canonical shape, not by composing existing relations. Layer composites (e.g., `K_is_fresh`) extend the predicate language further by bringing in external accessors like `mtime`; these compose atop the framework but are not part of it.

(c) *Shape misregistration is a structural error.* Registering a relation with the wrong shape produces predicates with wrong signatures or wrong semantics — the substrate cannot self-correct this. By Sh-conf, attempts to emit non-conformant tuples are rejected, but the rejection assumes the registered shape is the *correct* shape; if the registry is wrong, the substrate enforces the wrong constraint. Shape registration is part of the relation's contract.

(d) *The predicate language is bounded by the shape catalog.* "What the substrate can ask" is determined by the templates the shapes generate. Questions about content quality ("is this proof complete?", "is this description good?") are not expressible because no canonical shape's template generates them. Those are agent-time questions, not substrate questions.


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| cov | DEF | Coverage projection `L_K → ℘(T) × ℘(T)` | introduced |
| cov_allocated | DEF | `cov_allocated(F, Σ) = coverage(F) ∩ A^Σ`; finite, monotone along `⊑̂` | introduced |
| canonical-slot form | DEF | Endset form `{(x, δ(1, #x)) : x ∈ X_F}` | introduced |
| slot_addrs | DEF | Extraction `F ↦ X_F` for canonical-form F | introduced |
| AllocatedAddressAntichain | LEMMA | At a substrate-conforming layer, `cov_allocated({(x, δ(1, #x))}, Σ) = {x}` for every `x ∈ A^Σ` | introduced |
| Sh_K | DEF | Shape: `(c_F, c_G, t_F, t_G, idem)` | introduced |
| ShapeWellFormedness | DEF | Four implications relating `c = 0` to `t = -` (both sides); registry admits only well-formed shapes | introduced |
| match | DEF | Cardinality match predicate over `{0, 1, *, 0\|1}` | introduced |
| T_cat | DEF | Typed-relation catalog `⊆ T_admissible` (finite up to `~`); lifetime-constant | introduced |
| shape | DEF | Shape registry `T_cat → Shape`, per-class constant, lifetime-constant | introduced |
| conf_K^Σ | DEF | State-indexed conformance predicate; monotone along `⊑̂` | introduced |
| from_K^Σ, to_K^Σ | DEF | Total set-valued slot accessors | introduced |
| from₁, to₁ | DEF | Point-valued slot accessors (defined when c = 1) | introduced |
| from₁⁻, to₁⁻ | DEF | Optional point-valued slot accessors (defined when c = 0\|1) | introduced |
| Sh-conf | AXIOM | Emit_K rejects unregistered types and non-conformant emissions; returns `⊥` on failure | introduced |
| LinkAddressNotPrefixOfEmit | LEMMA | `b ⋠ a_emit(Σ, d)` for every `b ∈ dom(Σ.L)` and `d ∈ dom(Σ.M)` | introduced |
| EffectiveWpSimplification | COROLLARY | Under the *Emit_K routing commitment*, `wp_eff = d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G) ∧ Π_K` with `Π_K` capturing per-K discipline non-suppression | introduced |
| NullifyActiveSubsetCompatibility | COROLLARY | Active-subset content of ASN-0086's Nullify postcondition holds at `Σ_target` whether the call issues or suppresses; audit-slice multiplicity not preserved | introduced |
| Sh0 | LEMMA | FromSlotCanonicalAndCardinalityFixed | introduced |
| Sh1 | LEMMA | ToSlotCanonicalAndCardinalityFixed | introduced |
| Sh2 | LEMMA | FromSlotTargetRestricted — `slot_addrs(F) ⊆ t_F^Σ` | introduced |
| Sh3 | LEMMA | ToSlotTargetRestricted — `slot_addrs(G) ⊆ t_G^Σ` | introduced |
| SlotAccessorTotality | LEMMA | When `c = 1`, the point accessor is total | introduced |
| Sh4 | LEMMA | IdempotencyDiscipline — at-most-one active duplicate when `idem = ⊤`; conditional on the *Sh4 idempotency contract* | introduced |
| Sh5 | META | Template catalog organizational convenience; hand-curated per-shape template families | introduced |
| SingleHomeCoverageDiscipline | DEF | Per-K opt-in at NonIdempotentDirectedPair; homed-set commitment via fixed `d_K` | introduced |
| single-home commitment | DEF | Layer-discipline contract realizing SHCD; literal home-equality test, no Observe step | introduced |
| FunctionalDependencyDiscipline | DEF | Per-K commitment for DirectedPair: at most one active tuple per from-slot | introduced |
| Sh4 idempotency contract | DEF | Observe-then-Emit protocol for idempotent K, atomically scoped at `~`-class of K | introduced |
| FDD functional-dependency contract | DEF | Observe-then-Emit protocol with from-slot-only candidate `C_fd` | introduced |
| substrate-conforming-layer scaffolding | ASSUMPTION | Named scaffolding clauses: element-level addresses, subspace partitions, content-store antichain/monotonicity/finiteness, document address structure, link sub-allocator chains | introduced |
| Emit_K routing commitment | ASSUMPTION | Every class-(iii) emission of `K ∈ T_cat` routes through `Emit_K` | introduced |


## Open Questions

Tags: **[design choice]** — open design decision; **[refinement candidate]** — non-load-bearing elaboration; **[scope boundary]** — structural framework limitation.

- **[refinement candidate]** Should `(0, 0)` shapes be admitted? A relation with `c_F = c_G = 0` would be a single-tuple existence flag whose only role is "this event happened" without any from/to attribution; whether the substrate has any such relations is unclear, and the slot accessors degenerate to constants on it.
- **[design choice]** Provenance's `c_G = 0|1` mixes shapes — should it be split into two distinct canonical shapes (Provenance-with-target and Provenance-attribution-only), each generating separate templates? The current formulation requires the optional accessor `to₁⁻` to handle both cases in a single template.
- **[refinement candidate]** Is idempotency recoverable from cardinality plus target-domain alone, or is it an independent axis? Empirically the canonical catalog has both `idem = ⊤` (DirectedPair) and `idem = ⊥` (Coverage, Comment) at `(1, 1, A_doc, A_doc, _)`, suggesting independence.
- **[design choice]** Should the per-K opt-in registry — currently FunctionalDependencyDiscipline and SingleHomeCoverageDiscipline — be promoted to a sixth shape-tuple component, so that registrations with and without the discipline become structurally distinct rows rather than the same row with different opt-in flags? The current catalog encodes them as opt-in extensions atop a five-component shape; a sixth component would make the shape registry exhaustive but inflate the canonical-shape space considerably.
- **[design choice]** The shape constraint `slot_addrs(F) ⊆ t_F^Σ` requires slot addresses to be already-allocated at emission time. This precludes shape-conformant emissions whose slot addresses are *ghost* (currently outside `A^Σ`, possibly to be allocated later). L9 (TypeGhostPermission, ASN-0043) permits ghost spans in endsets; the shape framework restricts this to *non-slot* uses only. Whether future shape families should admit ghost-targeting slot semantics — and under what state-dependent conformance rule — is an open design question.
- **[refinement candidate]** Do *composite shapes* (relations whose F or G is itself constrained by another relation's content) require a new restriction axis, or do they decompose into existing primitives plus auxiliary predicates expressible in the current template language?
- **[scope boundary]** What guarantees the shape registry stays consistent across processes? Lifetime constancy is asserted as a substrate-level commitment within a single process; cross-process consistency (e.g., concurrent shape re-registration in a distributed substrate) is not addressed. Relatedly, the *Sh4 idempotency contract* and the *FDD functional-dependency contract* are both *committed* to single-process substrates by design — their atomicity premise reduces to within-call sequentiality between `Observe_K` and the substrate K.λ-step within a single `Emit_K` call (see the Sh4 contract's *Scope: single-process substrate* clause). This is a framework-scope commitment, not a topic awaiting future investigation: porting the framework to a multi-process substrate with racing Sh4-emitters at coverage-equivalent K's would require a coordination protocol (e.g., distributed lock at the `~`-equivalence class scope) outside the current framework. Characterizing the minimum protocol that preserves Sh4 in the multi-process setting would *extend* the framework's scope; this item is listed here to flag the boundary, not as an unresolved internal question.
- **[scope boundary]** Should the target-domain vocabulary admit a symbol `A_M` for document-container addresses (`dom(Σ.M)`)? Nelson's Literary Machines design admits container-level link targeting (metalinks: Title, Author, Document Supersession) under ghost-element semantics, but udanax-green's implementation restricts link endsets to permascroll content addresses only. The framework follows the implementation; layers needing container-level targeting use a designated content address per container as a workaround. Extending the catalog with `A_M` would re-enable metalink-style targeting at the registry level.


