# ASN-0094: Typed Relation Shapes

*Restricting the relational primitive into a predicate language.*

ASN-0086 establishes typed relations `L_K` with the three operations Emit, Observe, Nullify, governed by the lemma family R0…R7a. The relational structure as defined there is too permissive to support a typed predicate vocabulary: F and G can be any finite endsets whose coverage lies anywhere in `T`, so a predicate over `L_K` has no fixed signature. Every predicate would have to take a pattern in `℘(T) × ℘(T)` and return Bool, "two relations of the same shape" would not be expressible, and slot accessors `from(τ)`, `to(τ)` would be partial in a way that defeats type-checking.

We are looking for the minimum additional layer that closes this gap. The answer is a single structural decision per type: each `K ∈ T_cat` is assigned a *shape* — a tuple of constraints on cardinality, target domain, and idempotency — and the substrate enforces shape-conformance at Emit time. From the shape, a predicate template family is mechanically organized (though not mechanically derived; see Sh5). The pipeline is:

> R0…R7a (typed relations + operations) → **shape restrictions** (this document) → predicate template families → composed predicates

Shapes are not derivable from R0…R7a. They are an additional design decision the substrate makes about which relations it admits and what `(F, G)` pairs each admits. We justify each constraint by what predicate forms it makes possible, and by what the substrate cannot express without it.

*Load-bearing semantic departure from ASN-0086.* The framework registers Retraction with `idem = ⊤`, which changes ASN-0086's apparent multiset semantics at R to *set semantics* at the bare `Nullify` alias: two consecutive bare `Nullify(Σ, d_retr, a)` calls at the same target `a` produce *one* tuple in `L_R^Σ`, not two. Layers requiring audit-grade multiset semantics use *attributed retraction* (`c_F ≥ 1` with a distinguishing from-slot value at each emission). The full rationale (Nelson's two-layer active/audit reading and the migration recipe) is detailed in the *Nullify Compatibility* section; this is flagged here because it affects every downstream consumer of `L_R^Σ` reading audit-slice multiplicity.


## Scope and Substrate Scaffolding

*Arity scope.* This framework restricts the standard-triple slice `L^Σ` of `dom(Σ.L)` — the arity-3 links collected by ASN-0086's `L^Σ` definition. Higher-arity links admitted by L3 (ASN-0043) are outside its scope: the cardinality and target-domain shape components are defined over two slots only (F and G), and the slot-accessor and template machinery presupposes the arity-3 structure. Extending the framework to higher arities would require additional shape components per extra slot, which we do not pursue here.

*Emit_K routing commitment.* The framework is a discipline imposed by a relational layer atop ASN-0086. Every class-(iii) emission of a type `K ∈ T_cat` is committed to route through `Emit_K`; non-`Emit_K` class-(iii) invocations of these types are outside the framework's scope. Sh-conf below binds `Emit_K` (the relational-layer operation), not K.λ (the substrate primitive — K.λ remains permissive at the substrate level: any `F, G ∈ Endset` with `K ∈ T_admissible` is admissible to K.λ). The inductive arguments for Sh0–Sh3 invoke the *Emit_K routing commitment* to conclude that every new tuple in `L_K^Σ` for `K ∈ T_cat` arrived via an `Emit_K` call subject to Sh-conf.

*Named layer-discipline commitments.* The framework introduces four commitments on top of the *Emit_K routing commitment* (every class-(iii) `K ∈ T_cat` emission routes through `Emit_K`); each is a theorem under its respective contract, not a substrate-enforced axiom — without the contract, the corresponding failure mode (duplicate slot-pairs for Sh4; duplicate from-slot values for FDD; emissions at distinct homes for SHCD) becomes admissible and the dependent accessors (`exists_K`, `K_target_of`, `latest_K_for_addr`, `emission_order`) become undefined:

| Commitment | Applicable K's | Gate | Discharged theorem |
|---|---|---|---|
| *Sh4 idempotency contract* | K with `shape(K).idem = ⊤` not under FDD | 3 | Sh4 (pairwise slot-pair distinctness on `A_K^Σ`) |
| *FDD functional-dependency contract* | K with `shape(K) = (1, 1, A_doc, A_doc, ⊤)` + per-K FDD registration | 3 (subsumes Sh4) | FDD's from-slot uniqueness; secures `K_target_of` |
| *Single-home commitment* | K with `shape(K) = (1, 1, A_doc, A_doc, ⊥)` + per-K SHCD registration | 1 | SHCD's homed-set commitment; secures `emission_order` |
| *Unit-depth retraction discipline* (ASN-0086) | K with `K ~ R` | derived | `NoCraftedSpanReachesD` discharge |

Gate positions index the five-gate ordering in the Sh-conf section below (1 SHCD, 2 Sh-conf canonical-form, 3 Sh4/FDD, 4 Sh-conf cardinality/target-domain, 5 K.λ).

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


## The Address-Set Projection

Shape constraints operate on a *syntactic* projection of `(F, G)` — the slot-address sets extracted from canonical-form endsets — together with an *allocated-address* projection that bridges the syntactic check to substrate semantics. Two projections matter.

**Definition — Coverage Projection.** For each tuple `(a, F, G) ∈ L_K`:

`cov : L_K → ℘(T) × ℘(T)`

`cov(a, F, G) = (coverage(F), coverage(G))`

where `coverage(·)` is the union of address sets denoted by the endset's spans (Definition, ASN-0043). By PrefixSpanCoverage (ASN-0043), the coverage of a single unit-depth span at `x` is `{t ∈ T : x ≼ t}`, which is *infinite* in `T` by T0(a)/T0(b) (ASN-0034). The set-theoretic cardinality `|coverage(F)|` is therefore infinite for every non-empty canonical-form `F`, so cardinality constraints cannot be stated against `|coverage(F)|` directly.

The address-set view is a lossy projection — by L5 (EndsetSetSemantics, ASN-0043), endsets with different span decompositions can have identical coverage. For shape purposes the loss is intentional: shapes are predicates over what addresses a slot references, not over how those addresses are denoted.

**Definition — AllocatedCoverage.** For an endset `F` and reachable state `Σ`:

`cov_allocated(F, Σ) := coverage(F) ∩ A^Σ`

where `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` is the address universe at Σ (ASN-0086).

*Postcondition — Finiteness.* `cov_allocated(F, Σ)` is finite at every reachable state Σ. (Proof: `cov_allocated(F, Σ) ⊆ A^Σ = dom(Σ.C) ∪ dom(Σ.L)`, which is finite by the content-store finiteness scaffolding for `dom(Σ.C)` and L-fin (ASN-0043) for `dom(Σ.L)`.)

*Postcondition — Monotonicity.* `cov_allocated(F, Σ) ⊆ cov_allocated(F, Σ')` for every `Σ ⊑̂ Σ'`. (Proof: `A^Σ ⊆ A^{Σ'}` by L12a (ASN-0043) and the content-store monotonicity scaffolding; `coverage(F)` is a pure function of the endset value.)

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

*Case 3* (`x` and `a` lie in different domains). Sub-case 3a treats `x ∈ dom(Σ.L), a ∈ dom(Σ.C)`; Sub-case 3b is symmetric (swap link/content side labels; the disjointness predicate `s_L ≠ s_C` is symmetric). By L1 (LinkElementLevel, ASN-0043) and L1c (LinkAllocatorConformance, ASN-0043) on the link side — which via T10a.4 supplies T4-validity for every link-side address — together with the element-level content-address scaffolding clause on the content side — which supplies T4-validity directly for every content-side address — both `x` and `a` are element-level (`zeros(x) = zeros(a) = 3`) and T4-valid in either sub-case.

*Step 3.1 — Shared zero positions.* From `x ≼ a` (Prefix): `#x ≤ #a` and `aᵢ = xᵢ` for `1 ≤ i ≤ #x`. The zero-index set `Z_x := {i : 1 ≤ i ≤ #x ∧ xᵢ = 0}` has cardinality 3 (Case 3 hypothesis); enumerate its elements as `n_1 < n_2 < n_3` under T0's strict ℕ-order. Componentwise agreement gives `{n_1, n_2, n_3} ⊆ Z_a := {i : 1 ≤ i ≤ #a ∧ aᵢ = 0}`, both sides of cardinality 3, so `Z_a = {n_1, n_2, n_3}` (equal-cardinality subsets of finite ℕ-sets are equal).

*Step 3.2 — E-field first-position agreement.* The E-field of `x` is non-empty (we need only `#E(x) ≥ 1`, not the stronger `≥ 2` from L1b or its content-side analog, since Step 3.2's conclusion uses only the first position of `E(x)`): T4's last-position non-zero clause `t_{#t} ≠ 0` applied to `x` gives `x_{#x} ≠ 0`, while `x_{n_3} = 0`, so `n_3 ≠ #x`; combined with `n_3 ≤ #x` (since `n_3` is a position of `x`) this gives `n_3 < #x`, i.e., `#x − n_3 ≥ 1`. The E-field's positional range `n_3 + 1 .. #x` and the resulting length identity `#E(x) = #x − n_3` are read off T4a (SyntacticEquivalence, ASN-0034) — T4a identifies field segments as maximal contiguous non-zero sub-sequences delimited by the zeros, fixing the E-field as the segment after the third zero `n_3` — combined with T4b (UniqueParse, ASN-0034), which makes that segment a uniquely computable projection of `x`, and T4c (LevelDetermination, ASN-0034), which identifies the `zeros = 3` case with the four-field (N, U, D, E) hierarchy so the segment after `n_3` is labeled as the E-field. So `#E(x) ≥ 1`, and the first E-field position `E(x).1` is defined. The same E-field non-emptiness holds for `a` by the symmetric application of T4's last-position non-zero clause at `a`. By T4a + T4b + T4c (ASN-0034) applied independently to `x` and `a` — both element-level and sharing the same three zero positions `n_1 < n_2 < n_3` — the E-field of `x` occupies positions `n_3 + 1 .. #x` and the E-field of `a` occupies positions `n_3 + 1 .. #a` (T4a supplies the segment-between-zeros formula; T4b supplies uniqueness; T4c supplies the level-to-segment labeling); the index offset `E(·).j = ·_{n_3 + j}` for `1 ≤ j ≤ #E(·)` follows from the same triple. The componentwise agreement `xᵢ = aᵢ` on `1 ≤ i ≤ #x` from `x ≼ a`, instantiated at `i = n_3 + 1` (which satisfies `n_3 + 1 ≤ #x` since `#E(x) ≥ 1`), yields `x_{n_3 + 1} = a_{n_3 + 1}`; substituting the T4a + T4b + T4c index offset on both sides (taking `j = 1`) gives `E(x).1 = E(a).1`. This step holds in both sub-cases because the T4-validity citations and the T4a + T4b + T4c E-field structure apply uniformly to element-level addresses without reference to subspace identifier.

*Step 3.3 — Subspace contradiction.* In Sub-case 3a: the link subspace partition scaffolding gives `E(x).1 = s_L`; the content subspace partition scaffolding gives `E(a).1 = s_C`; the *Content subspace partition* scaffolding clause fixes `s_L ≠ s_C`. But Step 3.2 gives `E(x).1 = E(a).1`, so `s_L = s_C` — contradiction. Sub-case 3b is symmetric. Both sub-cases of Case 3 are vacuous. ∎

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

*Decidability of coverage-equality on finite span sets.* For any finite endset `E = {(s_1, ℓ_1), …, (s_n, ℓ_n)}`, `coverage(E)` is a finite union of *bounded* half-open intervals under T1: each span `(s_i, ℓ_i)` denotes `{t ∈ T : s_i ≤ t < s_i ⊕ ℓ_i}` (T12 well-formedness, ASN-0034) — bounded above by the explicit upper endpoint `s_i ⊕ ℓ_i ∈ T` (well-defined by TA0, ASN-0034, since `Pos(ℓ_i)` and `actionPoint(ℓ_i) ≤ #s_i` hold by T12). Even the canonical unit-depth span `(x, δ(1, #x))`, whose prefix-closure reading `{t : x ≼ t}` (PrefixSpanCoverage, ASN-0043) might *appear* unbounded, is in fact bounded above by `x ⊕ δ(1, #x) = shift(x, 1)` (OrdinalShift, ASN-0034): the prefix-closure of `x` and the half-open interval `[x, shift(x, 1))` denote the same address set by T5 (ContiguousSubtrees, ASN-0034), so the procedure can treat every span uniformly as a bounded T1-interval. To test `coverage(E) = coverage(E')`:

(1) Compute both endpoint sets `EP := {s_i, s_i ⊕ ℓ_i : 1 ≤ i ≤ n} ∪ {s_j', s_j' ⊕ ℓ_j' : 1 ≤ j ≤ n'}` (T1, TA0, TumblerAdd) — at most `2(n + n')` tumblers, all in T.

(2) Sort `EP` under T1 into a strictly increasing sequence `e_1 < e_2 < … < e_m` with `m ≤ 2(n + n')` (T2 IntrinsicComparison, ASN-0034). This partitions the range `[e_1, e_m)` into `m − 1` consecutive half-open intervals `[e_k, e_{k+1})` for `1 ≤ k < m`.

(3) For each delimited interval `[e_k, e_{k+1})`, test membership in `coverage(E)` and in `coverage(E')` via the representative point `e_k`: `e_k ∈ coverage(E) ⟺ (∃ i : 1 ≤ i ≤ n : s_i ≤ e_k < s_i ⊕ ℓ_i)` — `n` T1 comparisons per interval (T2 IntrinsicComparison). Same for `coverage(E')`. Because each span is a T1-interval and the chosen partition is finer than every span's boundary, membership is uniform on each delimited interval: `e_k ∈ coverage(E)` iff every point of `[e_k, e_{k+1})` is in `coverage(E)` (the span's lower endpoint is `≤ e_k` and its upper endpoint is `≥ e_{k+1}`, so the interval lies inside the span).

(4) Equality holds iff every delimited interval has matching outcomes (`e_k ∈ coverage(E) ⟺ e_k ∈ coverage(E')` for every `1 ≤ k < m`). Outside `[e_1, e_m)`, both coverages are empty by construction (no span has an endpoint outside `EP`, so no span covers any point outside the range).

The procedure is polynomial in `n + n'`: step (1) is `O(n + n')` tumbler additions; step (2) is `O((n + n') \log(n + n'))` T1 comparisons; step (3) is `O((n + n')^2)` T1 comparisons (per-interval membership over both coverages). The procedure uses only T1/T2/T12/TumblerAdd/TA0/T5/PrefixSpanCoverage, with no canonical-slot precondition.

*Lifetime constancy of `T_cat`.* The set `T_cat` is fixed at the substrate's initial state `Σ_init` and does not change as states evolve: at every reachable state Σ, the registered catalog is the same set `T_cat` declared at `Σ_init`. The lifetime constancy is required for the inductive baselines of Sh0–Sh4 to discharge uniformly. Each induction begins with "At `Σ_init`, every `L_K^{Σ_init} = ∅`; the universal quantifier is vacuous." A K admitted to `T_cat` only after some prior states have elapsed would face a non-vacuous baseline at its registration point — `L_K^{Σ_registered}` could be non-empty from class-(iii) emissions at coverage-equivalent type indices issued before K joined `T_cat` — and the induction's base case would not discharge. The framework forbids runtime extension of `T_cat`: layers that wish to introduce new typed relations must declare them at `Σ_init`, or face the burden of verifying `L_K^{Σ_registered} = ∅` at the registration point (equivalent to the framework's empty-baseline assumption).

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

**Definition — CallerSideClassification.** A caller wanting fine-grained classification of an `Emit_K` rejection cause invokes the following six side-effect-free checks in order, halting at the first failure to identify the rejecting gate. The check numbering is *finer-grained* than the consolidated *Gate Ordering* below — the two enumerations are aligned but not identical:

- *Registry check* (#1) is implicit in the consolidated *Gate Ordering*: the substrate-level `K ∈ T_cat` test fires before any conformance gate, since `shape(K)` resolution presupposes registry membership. The consolidated ordering enumerates only the post-registry gates and folds registry rejection into the framework's admission gate; the Caller-side ordering surfaces it as a distinct check.
- *Single-home check* (#2) corresponds to consolidated gate 1.
- *Canonical-form check* (#3) corresponds to consolidated gate 2 (Sh-conf clauses (a)/(b)).
- *Discipline-suppression check* (#4) corresponds to consolidated gate 3 (the per-K Observe-then-Emit contract, encompassing both *Sh4 idempotency contract* and *FDD functional-dependency contract*).
- *Cardinality check* (#5) and *Target-domain check* (#6) together correspond to consolidated gate 4 (Sh-conf clauses (c) and (d), bundled into a single gate in the consolidated ordering). The Caller-side ordering splits them because they index distinct rejection causes (cardinality-rejection vs target-domain-rejection) the caller may wish to distinguish.

The six Caller-side checks therefore expand consolidated gates 1–4 into a finer six-check sequence; consolidated gate 5 (substrate primitive K.λ) is not a separate Caller-side check because it is the post-admission emission step, not a rejection cause. The Caller-side and consolidated orderings agree on relative gate ordering and on rejection outcomes.

1. *Registry check* — Test `K ∈ T_cat` via the coverage-equivalence check against the registered representative list (per the *Decidable membership* paragraph in the TypedRelationCatalog Definition). Failure ⇒ registry rejection.
2. *Single-home check* (if K registered under SingleHomeCoverageDiscipline) — Test `d ?= d_K` against the per-K registration constant. Failure ⇒ single-home rejection.
3. *Canonical-form check* — Test whether F and G are each in canonical-slot form (per the CanonicalSlotForm Definition; the test is decidable on a finite endset by reading each span's start and verifying its displacement equals `δ(1, #start)`). Failure ⇒ canonical-form rejection.
4. *Discipline-suppression check* (if K registered under the *Sh4 idempotency contract* or the *FDD functional-dependency contract*) — Invoke `C_K(F, G, Σ)` (Sh4) or `C_fd_K(F, Σ)` (FDD) per the LayerCallableCandidateSets Definition above. Non-empty ⇒ discipline-suppression rejection.
5. *Cardinality check* — Test `match(|slot_addrs(F)|, shape(K).c_F)` and `match(|slot_addrs(G)|, shape(K).c_G)`. Failure ⇒ cardinality rejection.
6. *Target-domain check* — Test `slot_addrs(F) ⊆ shape(K).t_F^Σ` and `slot_addrs(G) ⊆ shape(K).t_G^Σ`. Failure ⇒ target-domain rejection.

A caller that passes all six checks may issue `Emit_K(Σ, d, F, G)` and expects the substrate K.λ-step to fire. The protocol uses only side-effect-free reads; running it ahead of `Emit_K` introduces no `↦`-step.

*Scope.* Sh-conf binds `Emit_K`, not K.λ. Chain-discipline and invariant-catalog facts (R0a-Cor1, R0a-Cor2, etc.) flow through the scaffolding clauses.

*Gate Ordering (consolidated).* The framework's per-K disciplines and Sh-conf's structural gates fire at every `Emit_K(Σ, d, F, G)` call site in a fixed sequence. The gates evaluate left-to-right in the order enumerated below and short-circuit at the first failure: a single `⊥` is returned, identified by the rejecting gate's name; subsequent gates do not fire. This deterministic ordering is what the *CallerSideClassification* protocol depends on for halt-at-first-failure semantics. Each per-K discipline contract specifies its local *Ordering with Sh-conf* clause (see the *Sh4 idempotency contract* section, the *FDD functional-dependency contract* sub-section, and the *single-home commitment* sub-section). The aggregate gate ordering at a call site for K with any registered discipline reads as follows:

1. **Single-home check** (if K registered under SingleHomeCoverageDiscipline): literal-equality test `d ?= d_K`. No `Observe_K` invocation, no state-dependent computation. On mismatch (`d ≠ d_K`), the *single-home commitment* clause (i) rejects the call outright with `⊥` and no subsequent gate fires. On match, the call proceeds to gate 2. (Skipped entirely at K not registered under SHCD.)

2. **Sh-conf canonical-form gate** (Sh-conf clauses (a) and (b)): test that `F` and `G` are each in canonical-slot form. On failure, `Emit_K` returns `⊥`; no subsequent per-K discipline contract fires (the per-K contracts' Observe steps would consume `slot_addrs(F)`/`slot_addrs(G)`, which are undefined for non-canonical endsets). On pass, the call proceeds to gate 3.

3. **Per-K Observe-then-Emit contract** (if K registered under Sh4 idempotency or FDD): either the *Sh4 idempotency contract* (when `shape(K).idem = ⊤` and K is not under FDD) or the *FDD functional-dependency contract* (when K is FDD-registered), executing clauses (i)–(iii) — Observe the candidate set, post-filter, then suppress or issue. On suppression (clause (ii) of either contract), `Emit_K` returns `⊥` and no subsequent gate fires. On issue (clause (iii)), the call proceeds to gate 4. (Skipped entirely at K not registered under any Observe-then-Emit discipline.)

4. **Sh-conf cardinality/target-domain gates** (Sh-conf clauses (c) and (d)): cardinality `match` on `|slot_addrs(F)|` and `|slot_addrs(G)|`; target-domain inclusion `slot_addrs(F) ⊆ t_F^Σ` and `slot_addrs(G) ⊆ t_G^Σ`. On failure of any conjunct, `Emit_K` returns `⊥`. On pass, the call proceeds to gate 5.

5. **Substrate primitive K.λ** (ASN-0086): the call invokes K.λ at home `d` with value `(F, G, K)`. K.λ's first/subsequent-emission protocol fires, depositing the new tuple at the fresh address `a_emit(Σ, d)`. The call returns `(Σ', addr) ∈ Σ' × A_rel^{Σ'}`.

FDD and SHCD cannot co-register at the same K (their required `idem` flags differ); at most one of gates 1 (SHCD) and 3 (FDD) fires per call site, and gate 3's Sh4 sub-branch fires only when K is not under FDD.


## Nullify Compatibility

The retraction type `R` (ASN-0086, Definition — RetractionType) is registered in `T_cat` with `shape(R) = (*, 1, A, A_rel, ⊤)`; R-registration is mandatory. Under this shape, Sh-conf admits every well-formed Nullify call (`F = ∅` matches `c_F = *`; canonical-slot `G = {(a, δ(1, #a))}` matches `c_G = 1` with `{a} ⊆ A_rel^Σ` by Nullify's P1). The shape also admits attributed retractions (`F ≠ ∅`), and the unit-depth `G`-form preserves ASN-0086's automatic `NoCraftedSpanReachesD` discharge. Because `shape(R).idem = ⊤`, two consecutive bare-form `Nullify(Σ, d_retr, a)` calls at the same target produce *one* tuple in `L_R^Σ` (the second is suppressed by the Sh4 contract); layers needing per-event audit multiplicity use attributed retraction with a distinguishing caller-context address, which Sh4 admits as a distinct slot-pair.

**Corollary — NullifyActiveSubsetCompatibility.** Under the Sh4 idempotency contract with R registered, every `Nullify(Σ, d_retr, a)` call satisfying ASN-0086's P0/P1/P2 delivers the active-subset content of ASN-0086's Nullify postcondition at `Σ_target`: (i) `{t : a ≼ t} ∩ A_rel^{Σ_target} = {a}`; (ii) `a ∈ nullified(Σ_target)` stable under R6a. This holds whether clause (iii) issues (`Σ_target := Σ'`) or clause (ii) suppresses (`Σ_target := Σ`). Audit-slice multiplicity is not preserved.

*Proof.* *Case A (issue, `C = ∅`).* Deposits `τ_new` with `G_{τ_new} = {(a, δ(1, #a))}`. (i) R0a at Σ' + `a ∈ A_rel^{Σ'}` (P1, L12a). (ii) `a ∈ coverage(G_{τ_new})` by PrefixSpanCoverage + reflexivity; `nullified` Definition gives the conclusion; R6a stabilizes. *Case B (suppress, `C ≠ ∅`).* `Σ_target := Σ`. (i) R0a at Σ + P1. (ii) Pick `τ_prior ∈ C`; `slot_addrs(G_{τ_prior}) = {a}` forces `a ∈ coverage(G_{τ_prior})`; `nullified` Definition gives `a ∈ nullified(Σ)`; R6a stabilizes. ∎


## Initial-State Baseline

*Initial-state baseline for preservation proofs.* Sh0–Sh4 presuppose `L_K^{Σ_init} = ∅` for every `K ∈ T_cat`. Preservation-proof text below names this baseline `Σ_init` directly (avoiding the prior convention that aliased it as `Σ_0`); the symbol `Σ_0` is reserved for worked-example walkthrough setup, where it denotes a pre-emission state reached from `Σ_init` by a finite sequence of K.σ/K.α steps (no K.λ-steps) — so `dom(Σ_0.L) = ∅` holds in walkthroughs but `Σ_0` is not in general identified with `Σ_init`. States reached before the *Emit_K routing commitment* was honored are outside the framework's scope.

*Global empty-link-store assumption (walkthrough convention).* The walkthroughs below assume the stronger `dom(Σ_init.L) = ∅` globally so K.λ's first-emission predicate fires uniformly at each walkthrough's first emission. This is a notational simplification, not a framework requirement — preservation theorems discharge from the per-K empty baseline `L_K^{Σ_init} = ∅` for `K ∈ T_cat` alone.

*Scope of the per-tuple-conformance relaxation.* "Every tuple in `L_K^{Σ_init}` satisfies `conf_K^{Σ_init}`" suffices for Sh0–Sh3 (whose universals quantify over single tuples), but *not* for Sh4 (pairwise slot-pair distinctness), FDD (pairwise from-slot uniqueness), or SHCD (the homed-set universal). For Sh4/FDD/SHCD the empty-baseline `L_K^{Σ_init} = ∅` is required.

*Per-walkthrough convention.* Every walkthrough below assumes: `T_cat` declared at `Σ_init`; R registered with `shape(R) = (*, 1, A, A_rel, ⊤)`; `L_K^{Σ_init} = ∅` for every `K ∈ T_cat`; `dom(Σ_init.L) = ∅` globally. Each walkthrough's catalog is stated inline at first registration; walkthroughs introducing substantive distinctions (lifetime constancy across walkthroughs, discipline opt-ins, required empty-baseline conditions) carry a dedicated "Registered catalog" paragraph.


## Lemma — LinkAddressNotPrefixOfEmit

This lemma bridges Sh-conf's structural gates to `wp_086` simplification at Retraction-typed emissions. Independent of Sh0–Sh4.

**Lemma — LinkAddressNotPrefixOfEmit.** Let Σ be reachable from `Σ_init` under the framework's *Emit_K routing commitment*. For every `b ∈ dom(Σ.L)` and every `d ∈ dom(Σ.M)`:

`b ⋠ a_emit(Σ, d)`

*Proof.* Case-split on whether `b` and `a_emit(Σ, d)` share a home.

*Notation.* FreshEmissionAddress's `origin(·)` and L1a's `home(·)` (`= N(·).0.U(·).0.D(·)`) denote the same per-address projection, identified through the *Per-document link sub-allocator chains* scaffolding clause; we write `home(·)` throughout.

*Case I — `home(b) = d`.* Both `b` and `a_emit(Σ, d)` are chain elements of `A_L(d)` (per the scaffolding clause, which enumerates `{ℓ : home(ℓ) = d}` as that chain). The case hypothesis places `b` in the homed set at `d`, so the homed set is non-empty; by R0a-Cor1 (ContiguousPrefix, ASN-0086) `J_d^Σ ≥ 0` and `b` sits at some chain index `0 ≤ i ≤ J_d^Σ` via `b = inc^i(d.0.s_L.1, 0)`. The non-empty homed set forces FreshEmissionAddress's subsequent-emission branch: `a_emit(Σ, d) = inc(ℓ_prev, 0)` with `ℓ_prev = max{ℓ' ∈ dom(Σ.L) : home(ℓ') = d}` under T1; by R0a-Cor1 this maximum is the chain element at index `J_d^Σ`, so `a_emit(Σ, d) = inc^{J_d^Σ + 1}(d.0.s_L.1, 0)` lies at chain index `J_d^Σ + 1`. By the *Uniform link sub-allocator chain length* scaffolding clause, `#b = #a_emit(Σ, d)`. By T10a.7 (EnumerationInjectivity, ASN-0034), distinct chain indices yield distinct tumblers; since `i ≤ J_d^Σ < J_d^Σ + 1`, `b ≠ a_emit(Σ, d)`. Two equal-length distinct tumblers are prefix-incomparable: if `b ≼ a_emit(Σ, d)`, Prefix's componentwise-agreement clause plus equal length forces componentwise equality, contradicting T3 (CanonicalRepresentation, ASN-0034). So `b ⋠ a_emit(Σ, d)`.

*Case II — `home(b) ≠ d`.* Suppose toward contradiction `b ≼ a_emit(Σ, d)`. Set `a := a_emit(Σ, d)`. From Prefix (ASN-0034), `b ≼ a` unfolds to `#b ≤ #a` and componentwise agreement `aᵢ = bᵢ` for `1 ≤ i ≤ #b`. We dispatch on `#b = #a` versus `#b < #a`. Both `b` and `a` are T4-valid with `zeros = 3`: `b` by L1c → T10a.4 (L1c places `b ∈ dom(Σ.L)` in a T10a-conforming chain, T10a.4 propagates T4-validity) and L1 (LinkElementLevel, ASN-0043); `a` by TA5a (IncrementPreservesT4, ASN-0034) applied to K.λ's construction — first-emission `a = [d.0.s_L.1]` satisfies T4 from `zeros(d) = 2` and `s_L > 0` (totaling `zeros(a) = 3`); subsequent-emission `a = inc(ℓ_prev, 0)` preserves T4 and zero count (TA5(c) modifies only position `sig(ℓ_prev)`, which TA5-SigValid places past the third zero on T4-valid `ℓ_prev`).

*Length dispatch (sub-case II.A: `#b = #a`).* By T3 (CanonicalRepresentation, ASN-0034) applied to the equal-length componentwise agreement, `b = a`. But `b ∈ dom(Σ.L)` (Lemma preamble) and `a = a_emit(Σ, d) ∉ dom(Σ.L)` by K.λ's freshness postcondition (ASN-0086, R0): the first/subsequent-emission protocol deposits at an address fresh to `dom(Σ.L)`. Contradiction. ∎ (II.A)

*Length dispatch (sub-case II.B: `#b < #a`).* We derive the home contradiction through Steps II.1–II.3.

*Step II.1 — All zeros of `a` lie at positions ≤ `#b`.* Let `Z_a := {i : 1 ≤ i ≤ #a ∧ aᵢ = 0}` and `Z_b := {i : 1 ≤ i ≤ #b ∧ bᵢ = 0}`. By componentwise agreement on `1..#b`, every `i ∈ Z_b` satisfies `aᵢ = bᵢ = 0`, hence `Z_b ⊆ Z_a`. Both sides have cardinality 3 (preamble), so equal-cardinality subsets of finite ℕ-sets force `Z_b = Z_a`. Hence every zero of `a` sits at some position ≤ `#b`; positions `#b + 1..#a` carry no zero of `a`. Enumerate the three shared zero positions in strict order as `n_1 < n_2 < n_3`.

*Step II.2 — N/U/D agreement via T4b's positional index ranges.* All of `n_1, n_2, n_3` lie in `1..#b`, so T4b's field projections — `N(·)` at `1..n_1 − 1`, `U(·)` at `n_1 + 1..n_2 − 1`, `D(·)` at `n_2 + 1..n_3 − 1` — also lie within `1..n_3 − 1 ≤ #b`. Componentwise agreement on `1..#b` gives `aᵢ = bᵢ` at every N/U/D position; the three identifications jointly deliver `N(a) = N(b) ∧ U(a) = U(b) ∧ D(a) = D(b)`.


*Step II.3 — Home contradiction.* `home(·) := N(·).0.U(·).0.D(·)` is a deterministic projection of any T4-valid `zeros = 3` address (T4b). Step II.2's three field equalities give `home(b) = home(a)`. K.λ's construction gives `home(a) = d`. Hence `home(b) = d`, contradicting `home(b) ≠ d`. ∎ (II.B)

Either sub-case yields `b ⋠ a_emit(Σ, d)`, closing Case II.

Either case yields `b ⋠ a_emit(Σ, d)`. ∎


## Cardinality (Sh0, Sh1)

**Lemma — CaseAClosureForLK.** For every `K ∈ T_cat` and every broad transition `Σ ↦ Σ'` of the framework's `↦`-vocabulary, the case-equation `L_K^{Σ'} = L_K^Σ` holds whenever the step is one of the following three classes; equivalently, `L_K^{Σ'} ⊋ L_K^Σ` strictly only when the step is a K.λ-step at some type `K' ~ K`:

1. *K.σ-steps and K.α-steps:* the `→` Definition (ASN-0086) frames `Σ.L` pointwise; hence `Σ'.L = Σ.L` and `L_K^{Σ'} = L_K^Σ` for every `K`.
2. *K.λ-steps at type `K'` with `K' ≁ K`:* the new tuple enters the disjoint `~`-class slice `L_{K'}^{Σ'}`; since `L_K^Σ = L_{K''}^Σ` for every `K'' ~ K` (ASN-0086, `~`-class indexing), `L_K` is untouched.
3. *Arrangement-modifying steps in `↦ \ →`:* LinkStoreInvarianceUnderArrangement (ASN-0086) gives `Σ'.L = Σ.L` pointwise; hence `L_K^{Σ'} = L_K^Σ`.

The complement — Case B — is a single class: K.λ-steps at type `K' ~ K` extend `L_K` by exactly one tuple via the *Emit_K routing commitment*'s admit clauses on `Emit_K`. The exhaustiveness of the four-class classification (3 Case-A sub-classes + 1 Case-B class) covers the framework's complete `↦`-vocabulary. *Proof.* Each sub-class's case-equation discharge is the direct citation given inline above; the Case B claim follows from R3 (ASN-0086) under the *Emit_K routing commitment*. ∎

Sh0–Sh3 below all share this Case-A enumeration; each invokes the lemma at "Case A" and supplies its own Case B argument. The lemma's quantifier ranges over every `K ∈ T_cat`, so the inductive step's "Fix `K ∈ T_cat`" precondition is uniformly discharged across Sh0–Sh3.

**Sh0 — FromSlotCanonicalAndCardinalityFixed.** For each `K ∈ T_cat`, every tuple in `L_K^Σ` at every reachable state Σ has `F` in canonical-slot form with `|slot_addrs(F)|` matching `c_F`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: F is canonical-slot form ∧ match(|slot_addrs(F)|, shape(K).c_F))`

*Proof.* By induction on the broad transition relation `↦*` from the initial state `Σ_init`. Reachable states are reached under `↦*` (the broader relation including arrangement-modifying steps), not just `→*`, so the induction must cover both transition classes.

*Base case.* At `Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Initial-State Baseline section above), every `L_K^{Σ_init} = ∅`; the universal quantifier is vacuous.

*Inductive step.* Suppose the property holds at Σ; let `Σ ↦ Σ'` be a single broad transition. Fix `K ∈ T_cat`. By Lemma — CaseAClosureForLK, the step either falls into one of the three Case-A sub-classes (with `L_K^{Σ'} = L_K^Σ`) or is a K.λ-step at `K' ~ K` (Case B).

*Case A (`L_K^{Σ'} = L_K^Σ`).* Set extensionality from the lemma gives `L_K^{Σ'} = L_K^Σ` as the same set of triples; existing tuples retain values by R2 (ASN-0086). The IH applies pointwise to the unchanged set.

*Case B (`L_K^{Σ'} = L_K^Σ ∪ {τ_new}`, a K.λ-step at type `K' ~ K`).* By the *Emit_K routing commitment*, this K.λ-step originates as an `Emit_K` call (at K or a `~`-equivalent K' with `shape(K') = shape(K)` by per-class constancy). Sh-conf clause (a) gives `τ_new` canonical-slot on F; Sh-conf clause (c) gives `match(|slot_addrs(F_{τ_new})|, c_F)`. Existing tuples preserved by R2 + IH.

Quantifying over K closes the induction. ∎

**Sh1 — ToSlotCanonicalAndCardinalityFixed.** The G-side analog of Sh0:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: G is canonical-slot form ∧ match(|slot_addrs(G)|, shape(K).c_G))`

*Proof.* By induction on `↦*` with the same baseline (Σ_init, `L_K^{Σ_init} = ∅`) and the same Case-A/Case-B dispatch via Lemma — CaseAClosureForLK as Sh0. The two cases:

*Case A (`L_K^{Σ'} = L_K^Σ`).* The lemma classifies the step into one of: (i) K.σ/K.α (frame preserves `Σ.L`, so `L_K^{Σ'} = L_K^Σ`); (ii) K.λ at `K' ≁ K` (the new tuple enters the disjoint `L_{K'}^{Σ'}` slice); (iii) arrangement-modifying step in `↦ \ →` (LinkStoreInvarianceUnderArrangement gives `Σ'.L = Σ.L`). In every case the IH applies pointwise to the unchanged `L_K^{Σ'} = L_K^Σ`.

*Case B (`L_K^{Σ'} = L_K^Σ ∪ {τ_new}`, a K.λ-step at type `K' ~ K`).* By the *Emit_K routing commitment*, an `Emit_K` call at K' with `shape(K') = shape(K)` by per-class constancy. Sh-conf clauses (b) and (c) discharge canonical-slot form on G and `match(|slot_addrs(G_{τ_new})|, c_G)` on the new tuple. Existing tuples preserved by R2 + IH. ∎


## Target Domain (Sh2, Sh3)

**Sh2 — FromSlotTargetRestricted.** For each `K ∈ T_cat`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(F) ⊆ shape(K).t_F^Σ)`

(vacuous when `t_F = -`). `slot_addrs(F)` is well-defined throughout by Sh0.

*Proof.* By induction on `↦*` with the same baseline (Σ_init, `L_K^{Σ_init} = ∅`) and the same Case-A/Case-B dispatch via Lemma — CaseAClosureForLK as Sh0/Sh1.

*Case A (`L_K^{Σ'} = L_K^Σ`).* The lemma classifies the step into one of: (i) K.σ/K.α (frame preserves `Σ.L`); (ii) K.λ at `K' ≁ K` (disjoint slice); (iii) arrangement-modifying step in `↦ \ →` (LinkStoreInvarianceUnderArrangement). In every case `L_K^{Σ'} = L_K^Σ` as a set of triples, and monotone preservation `t_F^Σ ⊆ t_F^{Σ'}` (L12a, ASN-0043, for `A_rel`; content-store monotonicity scaffolding for `A_doc`; their union for `A`) lifts the IH from `slot_addrs(F) ⊆ t_F^Σ` to `slot_addrs(F) ⊆ t_F^{Σ'}` on every existing tuple.

*Case B (`L_K^{Σ'} = L_K^Σ ∪ {τ_new}`, a K.λ-step at type `K' ~ K`).* By the *Emit_K routing commitment*, an `Emit_K` call at K' with `shape(K') = shape(K)` by per-class constancy. Sh-conf clause (d) gives `slot_addrs(F_{τ_new}) ⊆ t_F^Σ ⊆ t_F^{Σ'}` (the second inclusion is the same monotone preservation invoked in Case A). Existing tuples preserved by R2 + IH + monotonicity. ∎

**Sh3 — ToSlotTargetRestricted.** Symmetric for `G`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(G) ⊆ shape(K).t_G^Σ)`

Well-formedness from Sh1.

*Proof.* By induction on `↦*` with the same baseline (Σ_init, `L_K^{Σ_init} = ∅`) and the same Case-A/Case-B dispatch via Lemma — CaseAClosureForLK as Sh0/Sh1/Sh2.

*Case A (`L_K^{Σ'} = L_K^Σ`).* The lemma classifies the step into one of: (i) K.σ/K.α (frame preserves `Σ.L`); (ii) K.λ at `K' ≁ K` (disjoint slice); (iii) arrangement-modifying step in `↦ \ →` (LinkStoreInvarianceUnderArrangement). In every case `L_K^{Σ'} = L_K^Σ`, and monotone preservation `t_G^Σ ⊆ t_G^{Σ'}` lifts the IH from `slot_addrs(G) ⊆ t_G^Σ` to `slot_addrs(G) ⊆ t_G^{Σ'}` on every existing tuple.

*Case B (`L_K^{Σ'} = L_K^Σ ∪ {τ_new}`, a K.λ-step at type `K' ~ K`).* By the *Emit_K routing commitment*, an `Emit_K` call at K' with `shape(K') = shape(K)` by per-class constancy. Sh-conf clauses (b) and (d) give `slot_addrs(G_{τ_new})` defined and `⊆ t_G^Σ ⊆ t_G^{Σ'}`. Existing tuples preserved by R2 + IH + monotonicity. ∎

*Retraction commutativity.* `A_K^Σ ⊆ L_K^Σ` (filtering by `nullified(·)`). Sh0–Sh3 quantify over `L_K^Σ`, so every tuple in `A_K^Σ` is shape-conformant.


## Corollary — EffectiveWpSimplification

**Corollary — EffectiveWpSimplification.** Let Σ be reachable from `Σ_init` under the *Emit_K routing commitment*, with `R ∈ T_cat`. *(Statement.)* At any call site where the framework's full gate stack (gates 1–4) admits `Emit_K(Σ, d, F, G)` — i.e., the call reaches substrate K.λ at gate 5 — ASN-0086's `wp_086` simplifies to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`. *(Effective wp at the framework's gate.)* Combining with each gate's admit conjunct, the framework's *effective wp* for the postcondition "a fresh `(a, F, G)` is deposited in `A_K^{Σ'}`" simplifies to

`wp_eff(Emit_K(Σ, d, F, G), fresh (a, F, G) ∈ A_K^{Σ'}) = d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G) ∧ Π_K(d, F, G, Σ)`

where `Π_K` is the per-K discipline non-suppression conjunct:
- `K-under-SHCD ⟹ d = d_K` (gate 1)
- `K-with-idem = ⊤ ∧ not-under-FDD ⟹ C(F, G, Σ) = ∅` (gate 3 under Sh4)
- `K-under-FDD ⟹ C_fd(F, Σ) = ∅` (gate 3 under FDD)

The three implications are mutually exclusive at any K (FDD and SHCD are structurally incompatible since they require distinct `idem` values; Sh4 fires automatically at idem = ⊤ K not under FDD). When K is registered without any of the three disciplines (`idem = ⊥` and not under SHCD/FDD — e.g., bare NonIdempotentDirectedPair), no implication's antecedent fires and `Π_K = true` vacuously. At a rejected call site, the failing gate's conjunct evaluates false, `wp_eff = false`, `Emit_K` returns `⊥`, and no tuple is deposited — the framework's `⊥`-return is exactly what `wp_eff = false` encodes. `Π_K` is necessary for the postcondition's *fresh-deposit* reading: at a discipline-suppressed call, the prior conjuncts `d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)` all hold, but no new tuple is deposited; only `Π_K` captures the suppression at the wp.

*Proof.* `wp_086` carries two non-trivial conjuncts beyond `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`: `NoCraftedSpanReachesD(Σ, d)` and `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`. Discharge each via Lemma — LinkAddressNotPrefixOfEmit.

*Step 1 — `NoCraftedSpanReachesD(Σ, d)`.* For every `(b̂, F', G') ∈ L_R^Σ`, Sh1 at `K := R` gives `G'` canonical-slot with `|slot_addrs(G')| = 1`; Sh3 at `K := R` gives `slot_addrs(G') ⊆ A_rel^Σ`. So `G' = {(b', δ(1, #b'))}` for `b' ∈ dom(Σ.L)`. The Lemma at `b := b'` gives `b' ⋠ a_emit(Σ, d)`, hence `a_emit(Σ, d) ∉ coverage(G')` by PrefixSpanCoverage. Quantifying over `L_R^Σ` discharges the conjunct.

*Step 2 — `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`.* Case A (`K ≁ R`): first arm holds. Case B (`K ~ R`): per-class constancy gives `shape(K) = shape(R) = (*, 1, A, A_rel, ⊤)`. The full gate stack's admit at gates 2/4 forces `G = {(b, δ(1, #b))}` with `b ∈ A_rel^Σ`; the Lemma at this new `b` gives `b ⋠ a_emit(Σ, d)`, so `a_emit(Σ, d) ∉ coverage(G)`.

*Step 3 — Assembly.* Steps 1 and 2 reduce `wp_086` to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`. Combined with gates 1–4's admit conjuncts (Sh-conf clauses (a)–(d) contribute `K ∈ T_cat ∧ conf_K^Σ(F, G)`; gates 1 and 3 contribute the `Π_K` implications), and absorbing `K ∈ T_admissible` into `K ∈ T_cat`, the named `wp_eff` form follows. ∎

*Coverage-class disjointness from R is enforced by the registry's per-class constancy applied at the Retraction shape tuple:* a new catalog row whose shape tuple is componentwise equal to R's is at the same shape position as R, and the registry's hand-curation requires its representative to register `K_rep ~ R`; otherwise the row is a divergent coverage class at R's shape and is rejected by the catalog author at registration. Per-class constancy then makes Case A's `K ≁ R` precondition supplied uniformly at every non-R catalog row.

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

*Proof.* By Sh0, every `τ ∈ L_K^Σ` has `F` in canonical-slot form with `|slot_addrs(F)| = 1` (since `match(n, 1) ⟺ n = 1`). A finite set of cardinality 1 has a unique element. Define `from₁(τ)` as that element. By Sh2, this element lies in `t_F^Σ`; AllocatedAddressAntichain at this `x = from₁(τ)` (well-formed precondition: `x ∈ t_F^Σ ⊆ A^Σ`) confirms `from₁(τ)` is the unique allocated address denoted by `F_τ`'s slot, ruling out any allocated descendant of `from₁(τ)` as an alternative "what address does this slot reference" answer — the syntactic-to-semantic bridge that makes the point accessor's image well-defined as a single allocated address rather than a prefix-closure of addresses. ∎

For the rest of this document, we drop subscripts and write `from`, `to` when the shape unambiguously fixes which accessor is meant. We additionally use `addr(τ) = a` for the tuple address (R1, AddressInjectivity, ASN-0086).


## Lemma — RetractionSelfFreshness

This lemma bridges Sh-conf's admit at a Retraction emission to the active-subset content of the resulting tuple. Independent of Sh4's preservation argument (cited downstream by Sh4 Case C and Case D), and structurally parallel to LinkAddressNotPrefixOfEmit's placement before Sh0.

**Lemma — RetractionSelfFreshness.** Let Σ be reachable from `Σ_init` under the framework's *Emit_K routing commitment*, with R registered in `T_cat` per the framework's baseline registration requirement (Nullify Compatibility). Suppose every framework gate at an `Emit_R(Σ, d, F, G)` call site admits the call — Sh-conf clauses (a)–(d) all pass and the *Sh4 idempotency contract* clause (iii) fires — so the call proceeds to K.λ at home `d` and deposits a fresh tuple τ_new with `addr(τ_new) = a_emit(Σ, d)`, producing result state Σ'. Then:

`addr(τ_new) ∉ nullified(Σ')`

— equivalently, `τ_new ∈ A_R^{Σ'}`.

*Proof.* By Definition (nullified, ASN-0086) at Σ', `addr(τ_new) ∈ nullified(Σ') ⟺ (E (b̂, F', G') ∈ L_R^{Σ'} :: addr(τ_new) ∈ coverage(G'))`; the existential ranges over `L_R^{Σ'} = L_R^Σ ∪ {τ_new}` (R3 monotonicity on `L_R`, since this is a class-(iii) `Emit_R` step that adds exactly τ_new to `L_R`). Two witnesses must be ruled out, both by Lemma — LinkAddressNotPrefixOfEmit:

(i) *Self-nullification check (witness `(b̂, F', G') = τ_new`).* Sh-conf at the new emission admitted the call only because clauses (a)–(d) held; under `shape(R) = (*, 1, A, A_rel, ⊤)`, clauses (b)/(c)/(d) force `G_{τ_new} = {(b, δ(1, #b))}` for a unique `b ∈ A_rel^Σ`, so by PrefixSpanCoverage (ASN-0043) `coverage(G_{τ_new}) = {t : b ≼ t}`. Lemma — LinkAddressNotPrefixOfEmit applied at `b ∈ dom(Σ.L)` and `d := home(τ_new) ∈ dom(Σ.M)` yields `b ⋠ a_emit(Σ, d) = addr(τ_new)`, so `addr(τ_new) ∉ {t : b ≼ t} = coverage(G_{τ_new})`.

(ii) *Cross-nullification check (witness ranges over `L_R^Σ`).* For every prior `(b̂, F', G') ∈ L_R^Σ`, Sh1 at `K := R` gives `G'` canonical-slot with `|slot_addrs(G')| = 1`, and Sh3 at `K := R` gives `slot_addrs(G') ⊆ A_rel^Σ ⊆ A_rel^{Σ'}`. So `G' = {(b', δ(1, #b'))}` for a unique `b' ∈ dom(Σ.L) ⊆ dom(Σ'.L)`. Lemma — LinkAddressNotPrefixOfEmit applied at `b'` and the same `d = home(τ_new)` yields `b' ⋠ a_emit(Σ, d) = addr(τ_new)`, so `addr(τ_new) ∉ coverage(G')`. Quantifying over all `(b̂, F', G') ∈ L_R^Σ` discharges the cross-nullification disjunct.

Combining (i) and (ii) over the full disjunction `L_R^{Σ'} = L_R^Σ ∪ {τ_new}`: for every witness in `L_R^{Σ'}`, `addr(τ_new) ∉ coverage(G')`. Hence `addr(τ_new) ∉ nullified(Σ')`, and τ_new ∈ A_R^{Σ'} by Definition (A_K^Σ, ASN-0086). ∎

*Use sites.* The lemma is cited by Sh4's preservation argument at:
- *Case C* — to rule out the `K ~ R` self-retraction sub-case (clause (i) of the lemma's proof gives `addr(τ_new) ∉ coverage(G_{τ_new})`, so τ_new is never self-nullified).
- *Case D* — to establish the structural pivot `τ_new ∈ A_R^{Σ'}` from which the simultaneous addition-and-contraction analysis proceeds.

The Nullify Compatibility section's *NullifyActiveSubsetCompatibility* Corollary uses R0a at Σ' directly for the same kind of antichain-driven reasoning, without going through this lemma — its postcondition (i) `{t : a ≼ t} ∩ A_rel^{Σ_target} = {a}` quantifies over the *target* address `a` (not over τ_new), so the lemma's `addr(τ_new) ∉ nullified(Σ')` conclusion is not the load-bearing fact there. The two results are dual: the Lemma names the *new tuple's freshness from nullification* at Σ'; the Corollary names the *target's single-tuple scope* in dom(Σ'.L) under R0a. Both rest on LinkAddressNotPrefixOfEmit.


## Idempotency (Sh4)

**Sh4 — IdempotencyDiscipline (conditional on the *Sh4 idempotency contract*).** When `shape(K).idem = ⊤` and the calling layer honors the *Sh4 idempotency contract* (defined below; the contract's clauses (i)–(iii) gate every `Emit_K` call site for such K), at most one *active* tuple in `L_K` shares any given slot-address pair. The contract is the load-bearing layer commitment: Sh4's conclusion fails at any state reachable by a contract-violating step, so callers depending on Sh4 must verify the contract's clauses are honored at every K with `shape(K).idem = ⊤`. For `τ = (a, F, G) ∈ L_K^Σ` we write `F_τ := F` and `G_τ := G` for the slot endsets of τ. Then:

`(A τ, τ' ∈ A_K^Σ : (slot_addrs(F_τ), slot_addrs(G_τ)) = (slot_addrs(F_{τ'}), slot_addrs(G_{τ'})) :: addr(τ) = addr(τ'))`

*Universal scope.* The two bound variables `τ` and `τ'` range independently over `A_K^Σ`, including the diagonal `τ = τ'`. On the diagonal the conclusion `addr(τ) = addr(τ')` reads `addr(τ) = addr(τ)`, satisfied by reflexivity of equality, so the diagonal contributes no constraint. The substantive content is off-diagonal: for any two *distinct* active tuples `τ, τ'` whose slot-address pairs match, Sh4 forces `addr(τ) = addr(τ')` — combined with R1 (AddressInjectivity, ASN-0086), the equality of addresses then collapses `τ = τ'`, contradicting the off-diagonal assumption. Read contrapositively: no two distinct active tuples in `A_K^Σ` share a slot-address pair. Subsequent appeals to "pairwise distinctness on `A_K^Σ`" mean exactly this off-diagonal content; the diagonal is dispatched once and for all by reflexivity.

*Sh4 idempotency contract.* For each `K ∈ T_cat` with `shape(K).idem = ⊤`, on every `Emit_K(Σ, d, F, G)` call site the layer enforces the following protocol (gate 3 per Gate Ordering):

(i) Before issuing the emission, the layer computes the candidate set
`C(F, G, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)}`
via the two-step procedure:

&nbsp;&nbsp;(i.a) Query `Observe_K(slot_addrs(F), slot_addrs(G), oper)` — a well-typed call by the ordering above: Sh-conf clauses (a)/(b) have already gated canonical-form, so `slot_addrs(F)` and `slot_addrs(G)` are finite subsets of `T` at this point in the protocol. Observe_K's semantics returns the (finite) set of active tuples whose slot coverages prefix-contain the pattern addresses — concretely, `{τ ∈ A_K^Σ : slot_addrs(F) ⊆ coverage(F_τ) ∧ slot_addrs(G) ⊆ coverage(G_τ)}`. Under Sh0/Sh1, every `τ ∈ A_K^Σ` has canonical-form slot endsets, so `coverage(F_τ) = ⋃ {{t : y ≼ t} : y ∈ slot_addrs(F_τ)}` and `slot_addrs(F) ⊆ coverage(F_τ)` iff every `x ∈ slot_addrs(F)` has some `y ∈ slot_addrs(F_τ)` with `y ≼ x`.

&nbsp;&nbsp;*Contract correctness.* `C(F, G, Σ)` equals the specified set regardless of Sh-conf clause (d): the post-filter (i.b) tests exact slot-address-set equality, and any τ in the specified set passes both (i.a)'s Observe (by Prefix reflexivity on each pattern address) and (i.b)'s filter. *AllocatedAddressAntichain citation.* When Sh-conf clause (d) *does* hold for the new emission's `F` and `G` (so `slot_addrs(F) ⊆ A^Σ` and `slot_addrs(G) ⊆ A^Σ`), the Lemma — AllocatedAddressAntichain tightens (i.a)'s prefix-containment over-approximation to exact slot-address-set equality on the allocated-address side: by the Lemma, for every `x ∈ slot_addrs(F)` and every `τ ∈ A_K^Σ` whose canonical-slot `slot_addrs(F_τ)` is contained in `A^Σ` (Sh2 + Sh0), the prefix relation `y ≼ x` for `y ∈ slot_addrs(F_τ)` forces `y = x` — making (i.a)'s over-approximation `{τ : slot_addrs(F) ⊆ coverage(F_τ)}` collapse to `{τ : slot_addrs(F) ⊆ slot_addrs(F_τ)}`. The post-filter (i.b) then refines this to set equality. This is the tightening argument the contract claims as "the same AllocatedAddressAntichain argument" when downstream consumers (notably FDD's contract correctness paragraph) cite back to Sh4. Under the conditional hypothesis (Sh-conf clause (d)), Observe-then-post-filter is *equivalent* to the post-filter alone.

&nbsp;&nbsp;*Without the conditional hypothesis (Sh-conf clause (d) fails on the new emission's pattern).* Suppose `slot_addrs(F) = {d_unallocated}` where `d_unallocated ∈ T \ A^Σ` — the caller patterned the F-slot at an unallocated address. We walk through the contract's behavior to show `C(F, G, Σ)` still equals the specified set:
- *Step 1 — (i.a)'s Observe returns over-approximation.* `Observe_K(slot_addrs(F), ·, oper)` returns `{τ ∈ A_K^Σ : slot_addrs(F) ⊆ coverage(F_τ)}`. The membership `d_unallocated ∈ coverage(F_τ)` reduces to `(E y ∈ slot_addrs(F_τ) :: y ≼ d_unallocated)` by canonical-slot unfolding (Sh0). Without the AllocatedAddressAntichain tightening (the Lemma's precondition `x ∈ A^Σ` fails on `d_unallocated`), this prefix-containment is genuinely *broader* than equality: some `y ∈ slot_addrs(F_τ) ⊆ A^Σ` (by Sh2) could be a proper prefix of the unallocated `d_unallocated`, satisfying the Observe semantics without satisfying the post-filter's set equality.
- *Step 2 — (i.b)'s post-filter forces exact equality.* The post-filter retains only `τ` with `slot_addrs(F_τ) = slot_addrs(F) = {d_unallocated}`. For any `τ ∈ A_K^Σ`, `slot_addrs(F_τ) ⊆ t_F^Σ ⊆ A^Σ` by Sh2; so `slot_addrs(F_τ) = {d_unallocated}` would force `d_unallocated ∈ A^Σ`, contradicting the unallocated-pattern hypothesis. No `τ` survives the post-filter.
- *Step 3 — Result.* `C(F, G, Σ) = ∅`, matching the specified set `{τ : slot_addrs(F_τ) = {d_unallocated} ∧ ⋯}` which is vacuously empty (no `τ` in `A_K^Σ` can have a slot-address set including an unallocated address). The contract's clause (iii) fires (the candidate set is empty); the call proceeds to gate 4, where Sh-conf clause (d) then rejects the emission.

&nbsp;&nbsp;The contract's correctness is therefore *unconditional* on Sh-conf clause (d): with the hypothesis, the AllocatedAddressAntichain tightening makes Observe-then-post-filter equivalent to the post-filter alone; without the hypothesis, the post-filter's exact-equality test alone still yields `C(F, G, Σ)` exactly. Sh-conf clause (d)'s subsequent gate-4 rejection is what actually halts the emission in the unallocated-pattern case; the Sh4 contract at gate 3 sees an empty candidate set, fires clause (iii), and defers the rejection downstream.

&nbsp;&nbsp;(i.b) Post-filter the result of (i.a): retain only τ with `slot_addrs(F_τ) = slot_addrs(F)` and `slot_addrs(G_τ) = slot_addrs(G)`. Each returned τ has canonical-slot form by Sh0/Sh1, so `slot_addrs(F_τ)` is a well-defined finite set; exact-equality checks against the finite pattern slot-address sets are decidable in finite time. The composition (i.a) ∘ (i.b) yields exactly `C(F, G, Σ)` as specified above.

(ii) If `C(F, G, Σ) ≠ ∅`, the emission is *suppressed*: no `→`-step occurs.

(iii) Only if `C(F, G, Σ) = ∅` does the layer issue `Emit_K(Σ, d, F, G)`.

The layer commits to executing clauses (i)–(iii) atomically with respect to other emitters and retractors at the same `~`-equivalence class of K — emission and retraction events at any K' with `K' ~ K` that could split (i)'s observation from (iii)'s emission must be serialized by the layer. `L_K` is `~`-class indexed (ASN-0086, `L_K^Σ = L_{K'}^Σ` whenever `K ~ K'`), so emitters at distinct-but-`~`-equivalent type indices write to the same active subset; atomicity scoped at the `~`-class is what closes the race.

*Scope: single-process substrate.* The framework is restricted to single-process substrates: `↦`-transitions are sequential, and atomicity of (i)–(iii) reduces operationally to within-call sequencing between `Observe_K` and the substrate K.λ-step, with no intervening `↦`-step from another Sh4-emitter at a `~`-equivalent K. Multi-process consistency is flagged in Open Questions.

*Cross-`~`-class concurrency is benign.* Cross-`~`-class retraction does not race with Emit_K because it can only remove existing tuples, not introduce slot-pair collisions.

*Preservation under the contract.* Sh4 holds at every reachable state under the contract, by induction on `↦*`. Fix `K ∈ T_cat` with `shape(K).idem = ⊤`.

*Base.* At `Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Initial-State Baseline section above), `L_K^{Σ_init} = A_K^{Σ_init} = ∅`; Sh4's universal is vacuous.

*Step (Case A: `A_K^{Σ'} = A_K^Σ`).* The active subset is unchanged at K. Once the case-equation holds, Sh4 is inherited directly: `A_K^{Σ'} = A_K^Σ` as sets of triples (by set extensionality), so Sh4's body — quantifying over triples — yields the same Boolean at both states. The case-equation's *closure* is therefore trivial; the substantive work in Case A is verifying that each `↦`-step in the framework's transition vocabulary which lands in Case A actually satisfies the case-equation. We enumerate those classes here exhaustively (the framework's `↦`-vocabulary is `↦ = (K.σ ∪ K.α ∪ K.λ) ∪ arrangement-modifying` per ASN-0086's `→` Definition and `↦` relation), with each class's case-equation discharge cited inline:

1. *K.σ-steps and K.α-steps:* preserve `Σ.L` pointwise (ASN-0086's `→` Definition's frame conditions), hence `L_K^{Σ'} = L_K^Σ`; `L_R^{Σ'} = L_R^Σ`, so `nullified(Σ') = nullified(Σ)`; therefore `A_K^{Σ'} = A_K^Σ`.
2. *K.λ-steps at type `K'` with `K' ≁ K` and `K' ≁ R`:* the new tuple enters the disjoint slice `L_{K'}^Σ`, leaving `L_K^Σ` and `L_R^Σ` untouched (ASN-0086's `~`-class indexing); same conclusion.
3. *K.λ-steps at type `K'` with `K' ≁ K` and `K' ~ R` when no τ ∈ A_K^Σ lies in the new R-tuple's G-coverage:* `L_K^Σ` untouched (still `K' ≁ K`); `nullified(Σ')` extends but the extension does not intersect `addr(·)` for any τ ∈ A_K^Σ, so `A_K^{Σ'} = A_K^Σ`. The complementary sub-regime (where some τ ∈ A_K^Σ *is* nullified) contracts `A_K` and is routed to Case C below.
4. *Arrangement-modifying steps in `↦ \ →`:* LinkStoreInvarianceUnderArrangement (ASN-0086) gives `Σ'.L = Σ.L` pointwise, hence `L_K^{Σ'} = L_K^Σ`, `L_R^{Σ'} = L_R^Σ`, and `nullified(Σ') = nullified(Σ)`; therefore `A_K^{Σ'} = A_K^Σ`.

The enumeration is exhaustive for *Case A coverage* within the framework's `↦`-vocabulary: every `↦`-step that produces the case-equation falls into exactly one of these four classes, and each class's discharge is cited explicitly so a reader can verify Case A's coverage end-to-end. Transition classes the full Xanadu substrate may admit at scopes outside this framework's commitment (e.g., publication-state transitions, BEBE topology migrations) lie outside `↦`'s vocabulary and so outside Sh4's preservation scope by construction.

*Step (Case B: `A_K^{Σ'} = A_K^Σ ∪ {τ_new}`, a K.λ-step at type K with `K ≁ R`).* The case is structurally restricted to `K ≁ R` rather than carrying a conditional "no concurrent nullification" qualifier: by the class-decomposition of `↦` (per ASN-0086's `→` Definition and `↦`'s broader transition relation), concurrent nullification at the same step happens only at `Emit_R` steps, since `nullified(Σ)`'s definition reads over `L_R^Σ`'s G-coverages and only `Emit_R` extends `L_R`. A non-Retraction-typed K.λ-step (i.e., the `K ≁ R` regime selected here) cannot extend `L_R^Σ` and therefore cannot expand `nullified(Σ)`, so no τ ∈ A_K^Σ leaves `A_K` at this step — concurrent nullification is structurally impossible in Case B, not a conditional precondition. The complementary `K ~ R` regime is routed to Case D below, where the step is by definition an `Emit_R`-step at the same `~`-class as K and the simultaneous addition-and-possible-contraction structure is handled via the candidate-set argument plus the structural bound `|leaving| ≤ 1`. The case-decomposition exhausts the simultaneous-effect possibilities at the K.λ class: Case B covers `K ≁ R` (no possible nullification), Case D covers `K ~ R` (possible nullification handled explicitly). By the *Emit_K routing commitment*, this K.λ-step originates as an `Emit_K` call (with K or `~`-equivalent registered type). By the *Sh4 idempotency contract* clause (iii), the emission proceeded only because `C(F, G, Σ) = ∅`. Let `τ_new` be the new tuple. Suppose, toward contradiction, that some prior `τ ∈ A_K^Σ` satisfies `(slot_addrs(F_τ), slot_addrs(G_τ)) = (slot_addrs(F_{τ_new}), slot_addrs(G_{τ_new}))`. Then by definition `τ ∈ C(F, G, Σ)`, contradicting `C(F, G, Σ) = ∅`. So no such `τ` exists, and `A_K^{Σ'}` extends with a slot-pair-unique element. The pairwise condition is preserved: existing pairs were Sh4-distinct by IH; `τ_new` shares no slot-pair with any prior active tuple.

*Step (Case C: `A_K^{Σ'} ⊆ A_K^Σ` strictly, an `Emit_R`-step nullifying one or more K-tuple addresses without adding to A_K).* Retraction filters `A_K^Σ` by `nullified(Σ)` membership but cannot introduce new K-tuples; the pairwise condition is preserved on any subset. This case fires when `K ≁ R` (so the Emit_R step's `τ_new` does not join `A_K`). The complementary `K ~ R` sub-case — where one might expect "self-retraction" of `τ_new` by the same step — is empty by the hoisted Lemma — RetractionSelfFreshness (top-level section above), part (i): under `K ~ R` the Lemma's self-nullification clause gives `addr(τ_new) ∉ coverage(G_{τ_new})`, so `τ_new` is never self-nullified. The `K ~ R` simultaneous-effect case where τ_new adds to A_R and one or more *prior* R-tuples leave is Case D below.

*Step (Case D: K ~ R, `Emit_R`-step adding τ_new to A_R while potentially nullifying prior R-tuple addresses).* By RetractionSelfFreshness, τ_new ∈ A_R^{Σ'}. Combined with `nullified(·)`-filtering, `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving` where `leaving := {τ ∈ A_R^Σ : addr(τ) ∈ coverage(G_{τ_new})}`. This case-description equation follows by unfolding ASN-0086's `A_K^Σ` and `nullified` Definitions at Σ': R3 gives `L_R^{Σ'} = L_R^Σ ∪ {τ_new}`; splitting `nullified(Σ')`'s existential by prior-tuple vs new-tuple witness yields `nullified(Σ') = nullified(Σ) ∪ {a : a ∈ coverage(G_{τ_new})}` restricted to `A_rel^{Σ'}`; substituting into `A_R^{Σ'}`'s Definition and applying RetractionSelfFreshness's `addr(τ_new) ∉ nullified(Σ')` yields the equation. When `leaving = ∅` the step is pure addition; when `|leaving| = 1` it is `+1, −1`.

*Structural bound on `|leaving|`.* By Sh-conf at R (`c_G = 1`, `t_G = A_rel`), `G_{τ_new} = {(b, δ(1, #b))}` for a unique `b ∈ A_rel^Σ = dom(Σ.L)`. By PrefixSpanCoverage, `coverage(G_{τ_new}) = {t : b ≼ t}`. By R0a (FlatLinkDomain, ASN-0086), `dom(Σ.L)` is a tumbler-prefix antichain, so `{a ∈ dom(Σ.L) : b ≼ a} = {b}` (Prefix reflexivity gives `b` in the set; R0a's antichain rules out any other element). Therefore `leaving = {τ ∈ A_R^Σ : addr(τ) = b}`, and R1 (AddressInjectivity) gives `|leaving| ≤ 1`. Case D is at most a `+1, −1` step.

By the *Sh4 idempotency contract* clause (iii) — which fires under `K ~ R` since per-class constancy gives `shape(K).idem = ⊤` — the candidate-set check `C(F_{τ_new}, G_{τ_new}, Σ) = ∅` was confirmed against the full `A_R^Σ`. So `τ_new` is slot-pair-distinct from every prior τ ∈ A_R^Σ. Sh4's predicate is symmetric in its two operands, so this single check covers both ordered-pair directions. Combined with the IH on `A_R^Σ`, pairwise distinctness holds on `A_R^Σ ∪ {τ_new}`. Since `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving` is a subset, and Sh4's body is preserved under subset restriction (the universal quantifier over a subset of a pairwise-distinct set inherits the distinctness), Sh4 holds on `A_R^{Σ'}`.

The induction closes. ∎

*Consequences.*

(a) *Existence-vs-count distinction.* Idempotent relations support `exists_K(F, G) : Bool` predicates with stable yes/no answers under the contract. Non-idempotent relations support `count_K(...)` predicates whose value reflects the number of distinct emission events.

(b) *Re-emit-vs-fail behavior is registry-driven.* Library helpers like `emit_attribute` consult `shape(K).idem` to decide whether to short-circuit on existing match or always allocate a fresh address. The decision is mechanical from the shape, not from inspection of K's name.

(c) *Idempotency is a property of A_K, not L_K.* By R3, `L_K` always retains every emission ever made — including any duplicates that may exist if the contract was ever violated. The contract restricts what reaches `A_K`. Under correct contract enforcement, once a duplicate would be emitted, the layer suppresses it. The audit slice `L_K` retains historical state regardless: retraction-then-reemit cycles can leave multiple coverage-identical tuples in `L_K` with at most one active.


## Template Catalog (Sh5)

**Sh5 — TemplateCatalog (META).** Sh5 is an organizational convenience for hand-curating the canonical shape catalog; it is not a mechanical-derivation theorem. Per-shape template families are written by hand against the canonical catalog, with two design conventions enforced by catalog-author diligence:

*(a) Per-shape uniformity is an aspiration.* The catalog's shape-mate convergences — DirectedPair/Resolution sharing five base templates modulo codomain shift; the two `(0, 1)` rows sharing `is_K`; NonIdempotentDirectedPair/BundledDirectedPair/Retraction/Provenance each adapting the same five-template skeleton from DirectedPair with one or both slot accessors lifted from point-accessor to set-accessor as forced by their cardinality components — are *hand-curated*, not framework-derived. Signature derivation from shape components is mechanical per Sh5(b)'s *Signature derivation rule*, but body-shape choice (which set comprehensions and which Boolean compositions appear under each signature) is the catalog author's design decision. The framework supplies no mechanical gate that would enforce body-shape convergence at any pair of shape-mate rows; a future catalog extension at an existing shape may register divergent template bodies without violating any framework gate. Subsequent catalog rows that note "bodies hand-curated against the DirectedPair shape-mate (Sh5(a))" or similar invoke this convention without restating its content.

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
| Resolution                | (1, 1)     | A_doc | A_rel | ⊤    | *base (hand-curated against the DirectedPair shape-mate per Sh5(a)):* `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`; *dominant downstream pattern:* parametric consumption by NonIdempotentDirectedPair's `_via` templates (with K serving as the `K_res` argument). Standalone registration consuming the base templates without any `_via` consumer is also admissible. |
| Retraction                | (\*, 1)    | A     | A_rel | ⊤    | *base (reformulated under `c_F = *`; bodies in the walkthrough):* `pair_K(F̂, b)` (F̂ matched by set equality), `from_K(a)` (membership-based: τ included iff `a ∈ slot_addrs(F_τ)`), `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`; *primary consumption:* by ASN-0086's `nullified(·)` definition, which reads each `L_R`-tuple's G-coverage directly over the audit slice `L_R^Σ` (not via the active-subset `to_K` accessor; the audit-slice reading is the one R6b commits to, blocking the recursive fixpoint the active-subset reading would introduce) |
| BundledDirectedPair       | (1, \*)    | A_doc | A_doc | ⊤    | *base (reformulated under `c_G = *`; bodies in the walkthrough):* `pair_K(a, Ĝ)` (Ĝ matched by set equality), `from_K(a)`, `to_K(b)` (membership-based: τ included iff `b ∈ slot_addrs(G_τ)`), `from_addrs_K(b)`, `to_addrs_K(a)`; *consumption:* admits both legacy single-target emissions (`\|slot_addrs(G)\| = 1`) and bundled multi-target emissions (`\|slot_addrs(G)\| ≥ 2`) under a single registration via `match(n, *)` for every `n ∈ ℕ`; coverage class disjoint from R by shape-tuple inequality (Retraction's `(*, 1, A, A_rel, ⊤)` differs on `c_F`, `c_G`, `t_F`, `t_G`), so per-class constancy forces `K ≁ R` for every K registered at this shape — EffectiveWpSimplification's Step 2 Case A applies directly without invoking the Lemma at the new emission's G |
| Provenance                | (1, 0\|1)  | A     | A     | ⊤    | *base (`c_G = 0|1` requires explicit `⊥`-handling on G-side templates; bodies in the walkthrough):* `outgoing_K(s)` (alias of `from_K(s)`), `pair_K(a, b)`, `from_K(a)`, `to_K(b)` (target-indexed; excludes tuples with empty G-slot since `⊥ ≠ b`), `from_addrs_K(b)`, `to_addrs_K(a)` (with `⊥`-filter). For full-domain queries over `A_K^Σ`, callers use `outgoing_K`/`from_K` rather than `to_K`. |

*Per-class registration discipline.* Per-K discipline registrations (FDD, SHCD, and the *Sh4 idempotency contract*) apply at the `~`-equivalence-class level: registering at any `K ∈ T_cat` applies uniformly to every `K' ∈ T_cat` with `K' ~ K`. Since `L_K^Σ = L_{K'}^Σ` whenever `K ~ K'` (ASN-0086), a pinned-to-one-representative registration would leave coverage-equivalent emissions ungated and break preservation. FDD attaches only to DirectedPair (`idem = ⊤`); SHCD attaches only to NonIdempotentDirectedPair (`idem = ⊥`); the two are structurally mutually exclusive at any single K since `shape(K).idem` is fixed.


## Per-Shape Template Walkthroughs

We walk the canonical shapes and exhibit the predicate templates each generates.

*Common rejection patterns.* Walkthroughs cite these patterns by number; the Comment walkthrough below derives patterns 1–4 in full as canonical references, pattern 5 is derived first at Classifier, and pattern 6 is derived first at BundledDirectedPair (the *Sh4 suppression on a duplicate empty-G attempt* sub-section of the BundledDirectedPair walkthrough).

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

*Walkthrough.* Register `K = is_claim` with the Classifier shape (`T_cat = {is_claim, R}`), pre-allocating a target document `d ∈ A_doc^{Σ_0}` and a home document `home_K ∈ dom(Σ_0.M)` (with `dom(Σ_0.L) = ∅` so K.λ's first-emission branch fires).

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

*Canonical template family (role-neutral, bodies hand-curated per Sh5(a)).* Every K registered at this shape inherits the following five templates by the catalog's hand-curation. Signatures derive mechanically per Sh5(b)'s *Signature derivation rule*; bodies are hand-curated per Sh5(a). Each listed template is unconditional under Sh0–Sh4 (Sh0/Sh1 supply canonical-slot form and unit cardinality; Sh2/Sh3 supply `A_doc^Σ` codomains for the slot accessors; Sh4 ensures the returned tuple-sets and address-sets are slot-pair-distinct, not multisets). Codomains are made explicit per the *Codomain convention* for templates:

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

The current draft attaches FDD only to the DirectedPair shape, which carries both constraints (`c_F = 1` and `t_F = A_doc`) by registration. Registering FDD at a shape with `c_F ≠ 1` or `t_F ≠ A_doc` is structurally rejected by the registration interface; the framework's preservation theorems and the `K_target_of` codomain typing both presuppose these preconditions.

*Strictly stronger than Sh4.* Sh4 enforces pairwise distinctness of slot-address *pairs*, not of `slot_addrs(F_τ)` alone. Two emissions sharing from-slot `d` but distinct G-slots both pass Sh4 (distinct slot-pairs), yielding `|{τ : from₁(τ) = d}| = 2` — a singleton-returning accessor is ill-defined. FDD forbids the second emission outright.

*FDD functional-dependency contract.* For each K with FunctionalDependencyDiscipline registered, on every `Emit_K(Σ, d, F, G)` call site (gate 3 per Gate Ordering):

*FDD subsumes Sh4 at FDD-registered K.* At FDD-registered K the layer runs only the FDD clauses (i)–(iii), with Sh4's clauses dormant. The Sh4 conclusion still holds because `C ⊆ C_fd`: FDD's stricter from-slot-uniqueness entails Sh4's weaker slot-pair-distinctness.

(i) Compute `C_fd(F, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}` via the two-step procedure: (i.a) query `Observe_K(slot_addrs(F), ∅, oper)` — well-typed by finiteness of `slot_addrs(F)`; the `∅` G-pattern matches every G-coverage trivially under Observe_K's `Ĝ ⊆ coverage(G)` semantics, so the result is `{τ ∈ A_K^Σ : slot_addrs(F) ⊆ coverage(F_τ)}`. By the same AllocatedAddressAntichain argument used in Sh4's contract, under the same conditional hypothesis (Sh-conf clause (d) holds for the new emission's F) this over-approximates *exactly* `slot_addrs(F_τ) ⊇ slot_addrs(F)`; the contract's correctness — that the computed `C_fd(F, Σ)` equals the specified `{τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}` — is independent of this tightness property, depending only on (i.a)'s finite over-approximation and (i.b)'s exact-equality post-filter, by the same expository-vs-substantive split made for Sh4's contract. (i.b) post-filter to exact from-slot-address equality on F — retain only τ with `|slot_addrs(F_τ)| = |slot_addrs(F)|` (which under canonical-slot form forces `slot_addrs(F_τ) = slot_addrs(F)` given the over-approximation under the conditional hypothesis; without the hypothesis, the post-filter still tests exact set equality on finite slot-address sets and still yields `C_fd(F, Σ)` exactly, but the contract returns `⊥` either via clause (ii) below or via the subsequent Sh-conf rejection).

(ii) If `C_fd(F, Σ) ≠ ∅`, the emission is *suppressed*: no `→`-step occurs.

(iii) Only if `C_fd(F, Σ) = ∅` does the layer issue `Emit_K(Σ, d, F, G)`.

The layer commits to executing (i)–(iii) atomically with respect to other emitters and retractors at the same `~`-equivalence class of K. The same single-process-substrate scope from Sh4's contract applies: atomicity reduces operationally to within-call sequentiality between `Observe_K` and the substrate K.λ-step within a single `Emit_K` call, with no intervening `↦`-step from another FDD-emitter at a `~`-equivalent K.

*Preservation under the discipline.* The inductive argument runs three cases: Case A (active subset unchanged), Case B (single new tuple at K), and Case C (retraction-only contraction). Case D (the K=R simultaneous addition-and-contraction case from Sh4) is excluded by shape-tuple structure: FDD requires `shape(K) = (1, 1, A_doc, A_doc, ⊤)`, while Retraction has `shape(R) = (*, 1, A, A_rel, ⊤)`; per-class constancy of `shape` (`K ~ K' ⟹ shape(K) = shape(K')`) and the shape-tuple inequality (differs on `c_F`, `t_F`, `t_G`) force `K ≁ R` for every FDD-registered K, so no `Emit_R` step can extend `A_K`.


Fix `K ∈ T_cat` with FDD registered. By the same off-diagonal/diagonal split as in Sh4 (see *Universal scope* above), the substantive content of FDD's property `(A τ, τ' ∈ A_K^Σ : from₁(τ) = from₁(τ') :: addr(τ) = addr(τ'))` is that no two *distinct* active K-tuples share a from-slot value; the diagonal `τ = τ'` is trivial by reflexivity of `addr(·) = addr(·)`. The candidate set `C_fd(F, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}` is broader in scope than Sh4's `C(F, G, Σ)` — it matches on from-slot alone rather than on the slot-pair — so `C ⊆ C_fd` at every state. The discipline is therefore *stricter as a gate* (more candidate sets are non-empty, so more emissions are suppressed) even though its candidate set is broader.

*Base.* At `Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Initial-State Baseline section above), `L_K^{Σ_init} = A_K^{Σ_init} = ∅`; FDD's universal is vacuous.

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

### Resolution — `(1, 1, A_doc, A_rel, ⊤)`

Tuples have form `slot_addrs(F) = {d}, slot_addrs(G) = {addr(σ)}` where `d ∈ A_doc^Σ` is the resolving document and `σ ∈ A_rel^Σ` is the comment-tuple being resolved. The shape `(1, 1, A_doc, A_rel, ⊤)` carries the same five-template base family as DirectedPair (with `t_G = A_rel` substituted for `A_doc`): `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`. Bodies hand-curated against the DirectedPair shape-mate (Sh5(a)).

*Standalone admissibility.* Resolution's base templates depend only on shape components and Sh0–Sh4; standalone registrations work identically to consumed registrations.

### Retraction — `(\*, 1, A, A_rel, ⊤)`

Tuples have form `slot_addrs(F) ⊆ A^Σ` (any finite set, possibly empty) and `slot_addrs(G) = {addr(σ)}` for `σ ∈ A_rel^Σ` the tuple being retracted. The retraction shape is consumed by ASN-0086's `A_K^Σ` Definition and Definition (nullified) directly: the active-subset definition uses `L_R`'s tuples to compute `nullified(Σ)`. Signatures derived mechanically per Sh5(b); bodies hand-curated against the DirectedPair shape-mate (Sh5(a)), re-formulated for the `c_F = *` setting since `from₁` is not defined when `c_F` is not `1`: DirectedPair's `from₁(τ)` point accessor is replaced by `slot_addrs(F_τ)` as a set accessor, with matching predicates lifted from address-equality to set-equality or set-membership as appropriate to each template's role:

`pair_K(F̂, b)        ≡ (E τ ∈ A_K^Σ :: slot_addrs(F_τ) = F̂ ∧ to₁(τ) = b)`

`from_K(a)           ≡ {τ ∈ A_K^Σ : a ∈ slot_addrs(F_τ)}`

`to_K(b)             ≡ {τ ∈ A_K^Σ : to₁(τ) = b}`

`from_addrs_K(b)     ≡ {x : (E τ ∈ A_K^Σ :: to₁(τ) = b ∧ x ∈ slot_addrs(F_τ))}`

`to_addrs_K(a)       ≡ {to₁(τ) : τ ∈ A_K^Σ ∧ a ∈ slot_addrs(F_τ)}`

The four set-valued templates take an *address* on the from-side (`from_K`, `from_addrs_K`'s witness `x`, and `to_addrs_K`'s argument `a`) using the membership relation `a ∈ slot_addrs(F_τ)` — every τ whose from-slot *contains* the queried address `a` is included. The Boolean `pair_K`'s F-side argument is an *address-set pattern* `F̂` matched by exact set equality `slot_addrs(F_τ) = F̂`; this preserves the role of `pair_K` as a Boolean existence test for a particular (from-pattern, to-address) combination. The to-side accessors and the `to_K` template use `to₁(·)` directly, since `c_G = 1` admits SlotAccessorTotality on the G-slot. Both `to_K` and `to_addrs_K` return well-typed sets — `to_K` a tuple-set in `℘_fin(A_K^Σ)`, `to_addrs_K` an address-set in `℘_fin(A_rel^Σ)` — by Sh3 on the G-slot. Even though Retraction's primary role is to flip `A_K` membership for arbitrary K via ASN-0086's `A_K^Σ` Definition (which filters `L_K^Σ` by `nullified(Σ)`-membership, with `nullified(Σ)` itself defined over `L_R^Σ`'s G-coverages), not to host its own predicates, the base template family is fully defined; the catalog row's "primary consumption" column flags this active-subset machinery as the principal consumer rather than enumerating the inherited base family a second time.

*Note on `pair_K`'s set-equality F-side argument.* The body matches by exact set equality on the F-side so the predicate is not redundant with `from_K(a) ∩ to_K(b) ≠ ∅` (the membership-reading), which is already expressible from the other base templates by intersection.

*Unit-depth retraction discipline secured by Retraction's shape.* Retraction's `c_G = 1` together with canonical-slot form (Sh-conf clauses (a)/(b)) forces every shape-conformant Retraction emission's G-endset to a single unit-depth span `{(b, δ(1, #b))}` for some `b ∈ A_rel^Σ`. This is exactly ASN-0086's unit-depth retraction discipline: every emission that lands in `L_R^Σ` via `Emit_R` satisfies the discipline by construction. Consequently, ASN-0086's wp simplification under regime (i) applies to every Sh-conf-admitted Retraction emission — `NoCraftedSpanReachesD(Σ, d)` holds automatically at every such call site by Lemma — LinkAddressNotPrefixOfEmit (whose generalized statement `b ⋠ a_emit(Σ, d)` for any `b ∈ dom(Σ.L)` is applied in the EffectiveWpSimplification Corollary's Step 1 to each prior R-tuple's unique G-slot address; the proof case-splits on `home(b) = d` vs `home(b) ≠ d` and rules out `b ≼ a_emit(Σ, d)` in each case) — so the wp_086 in the Sh-conf section's effective-wp derivation collapses to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible` without manual discharge.

The unrestricted from-slot (`c_F = *`) accommodates use cases where the retracting party is recorded in F (e.g., F's slot addresses include an agent address), as well as the bare retraction `Nullify(Σ, d_retr, a) = Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` of ASN-0086, where `F = ∅`. Both forms are canonical-slot (the bare form trivially, the attributed form when its from-slot endset is in canonical form). The shape framework rejects retractions whose from-slot uses non-canonical-form endsets, consistent with the discipline imposed across the catalog.

### BundledDirectedPair — `(1, \*, A_doc, A_doc, ⊤)`

Tuples have form `slot_addrs(F) = {a}` for `a ∈ A_doc^Σ` and `slot_addrs(G) ⊆ A_doc^Σ` (any finite set, possibly empty, possibly singleton, possibly multi-element). The shape's distinguishing feature is `c_G = *`: a single emission may bundle multiple to-side document targets into one tuple, rather than requiring a separate tuple per target. Role-specific readings (parent → multiple sidecars, citing → multiple cited works, source → multiple dependents) are layer conventions over a single structural shape.

*Motivating use case (`citation.depends`).* The shape was added to admit bundled dependency-style citation emissions where a single citing document depends on a finite set of cited documents — recorded atomically in one tuple rather than spread across several. The substrate primitive K.λ already admits multi-element G-endsets at any K (ASN-0086 R0 takes arbitrary `(F, G)` with `K ∈ T_admissible`); the framework's contribution is to register the shape so that Sh-conf admits these multi-element G-emissions under a stable cardinality bound `c_G = *`.

*Canonical base template family (signatures derived per Sh5(b); bodies hand-curated against the DirectedPair shape-mate per Sh5(a)).* The shape's signature derivation is mechanical; the body adapts DirectedPair's `to₁(τ)` point-accessor uses to `slot_addrs(G_τ)` set-accessor uses, with matching predicates lifted from address-equality to set-equality or set-membership as appropriate to each template's role. The F-side templates retain `from₁` as a point accessor by SlotAccessorTotality at `c_F = 1`:

`pair_K(a, Ĝ)        ≡ (E τ ∈ A_K^Σ :: from₁(τ) = a ∧ slot_addrs(G_τ) = Ĝ)`

`from_K(a)           ≡ {τ ∈ A_K^Σ : from₁(τ) = a}`

`to_K(b)             ≡ {τ ∈ A_K^Σ : b ∈ slot_addrs(G_τ)}`

`from_addrs_K(b)     ≡ {from₁(τ) : τ ∈ A_K^Σ ∧ b ∈ slot_addrs(G_τ)}`

`to_addrs_K(a)       ≡ {x : (E τ ∈ A_K^Σ :: from₁(τ) = a ∧ x ∈ slot_addrs(G_τ))}`

The Boolean `pair_K`'s G-side argument is an *address-set pattern* `Ĝ` matched by exact set equality `slot_addrs(G_τ) = Ĝ`; this preserves the role of `pair_K` as a Boolean existence test for a particular (from-address, to-pattern) combination. The four set-valued templates take an *address* on the to-side (`to_K`, `from_addrs_K`'s argument `b`, and `to_addrs_K`'s witness `x`) using the membership relation `b ∈ slot_addrs(G_τ)` — every τ whose to-slot *contains* the queried address `b` is included. The F-side templates use `from₁(·)` directly, since `c_F = 1` admits SlotAccessorTotality on the F-slot. Both `from_K` and `from_addrs_K` return well-typed sets — `from_K` a tuple-set in `℘_fin(A_K^Σ)`, `from_addrs_K` an address-set in `℘_fin(A_doc^Σ)` — by Sh2 on the F-slot.

*Note on `pair_K`'s set-equality G-side argument.* The body matches by exact set equality on the G-side so the predicate is not redundant with `from_K(a) ∩ to_K(b) ≠ ∅` (the membership-reading), which is already expressible from the other base templates by intersection.

*Backward compatibility with legacy single-target emissions.* Because `c_G = *` admits any `n ∈ ℕ` via `match(n, *)`, legacy emissions with `|slot_addrs(G)| = 1` — i.e., the shape of single-target `citation.depends` calls under a prior `c_G = 1` registration — remain shape-conformant under the new `c_G = *` registration. Concretely, an emission with `slot_addrs(G) = {b}` for a single `b ∈ A_doc^Σ` passes clause (c) at `match(1, *)` and clause (d) at `{b} ⊆ A_doc^Σ`; no separate migration discipline is required for pre-patch tuples. The transition from `c_G = 1` to `c_G = *` is one-way: a K registered at `c_G = *` admits both single- and multi-target tuples uniformly. Per-class constancy of `shape(·)` (lifetime-constant per the ShapeRegistry Definition) precludes re-registering K's shape after `Σ_init`; a layer migrating from a pre-patch `c_G = 1` registration must declare the relation at `c_G = *` from `Σ_init` to recover both regimes under one row, with `L_K^{Σ_init} = ∅` discharging the empty-baseline preservation theorems.

*Empty-G admissibility.* `c_G = *` admits `n = 0` per `match(0, *)`; the cardinality vocabulary `{0, 1, *, 0|1}` carries no `1..*` token, so a `1..*` lower bound cannot be expressed at the registry level. The asymmetry with Retraction: Retraction admits empty-F (the bare Nullify alias) with non-empty-G, while BundledDirectedPair admits non-empty-F with empty-G. Sh4 suppression and the audit-slice set-semantics commitment apply uniformly at `n = 0` (exact slot-pair-equality on the empty set is decidable).

*Coverage class disjointness from R (EffectiveWpSimplification implication).* The BundledDirectedPair shape tuple `(1, *, A_doc, A_doc, ⊤)` differs from Retraction's `(*, 1, A, A_rel, ⊤)` on four components (`c_F`, `c_G`, `t_F`, `t_G`). Per-class constancy of `shape(·)` (`K ~ K' ⟹ shape(K) = shape(K')`) gives the contrapositive: `shape(K) ≠ shape(K') ⟹ K ≁ K'`. Hence every K registered at the BundledDirectedPair shape satisfies `K ≁ R`. In EffectiveWpSimplification's Step 2 (proof in the EffectiveWpSimplification Corollary section), the case-split on K's `~`-class lands in Case A (`K ≁ R`): the first disjunct's arm holds directly and the Lemma — LinkAddressNotPrefixOfEmit is not invoked at the new emission's G-slot. Step 1's discharge of `NoCraftedSpanReachesD(Σ, d)` over prior R-tuples in `L_R^Σ` is unaffected (it quantifies over R-tuples regardless of the new emission's type). EffectiveWpSimplification's wp simplification therefore applies uniformly at every Sh-conf-admitted `Emit_K` call site for K at this shape.

*Worked example.* Register `K = citation.depends` with the BundledDirectedPair shape (`T_cat = {citation.depends, R}`), pre-allocating a citing document `d_cite ∈ A_doc^{Σ_0}`, three cited documents `d_src1, d_src2, d_src3 ∈ A_doc^{Σ_0}`, and a home `home_cite ∈ dom(Σ_0.M)` with `dom(Σ_0.L) = ∅`.

*Timeline structure.* The walkthrough's main timeline runs `Σ_0 → Σ_1 → Σ_2` via two emissions exercising the shape's two non-empty G-cardinality regimes — Emission BDP1 (bundled multi-target, `|slot_addrs(G)| = 3`) at `Σ_0 → Σ_1`, then Emission BDP2 (legacy single-target, `|slot_addrs(G)| = 1`) at `Σ_1 → Σ_2`. A separately-presented *narrative variant* — Emission BDP0 exercising the empty-G boundary `|slot_addrs(G)| = 0` — is presented at the end of this walkthrough; this variant returns to `Σ_0` (the same starting state) and applies a different first-step emission, producing a successor state we call `Σ_1'` (apostrophe-disambiguated from the main timeline's `Σ_1`). The "parallel" terminology in subsequent prose refers to the walkthrough author's choice of two separate first-step explorations from the same `Σ_0`, *not* to parallel reachability in the state graph (which is sequential under `↦`). Template evaluation at Σ_2 uses only the main timeline's active subset `A_K^{Σ_2} = {γ_1, γ_2}`; `Σ_1'` and any state reachable only from it are exhibited solely for the empty-G discussion and never compose into the main timeline.

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
| `pair_K(d_cite, ∅)` | `= false` | Empty-G cardinality boundary: BDP1 and BDP2 both emitted non-empty G, so no active τ at Σ_2 has empty G-slot. The narrative-variant emission BDP0 below would produce a γ_0 with empty G-slot at the alternative successor state `Σ_1'` of `Σ_0`; in that variant `pair_K(d_cite, ∅)` would evaluate to `true`. The present (main-timeline) value `false` reflects that γ_0 is not in `A_K^{Σ_2}` — `Σ_1'` is not a predecessor of `Σ_2` on the main timeline. |
| `from_K(d_cite)` | `{τ ∈ A_K^{Σ_2} : from₁(τ) = d_cite} = {γ_1, γ_2}` | Both tuples from the same citing document. |
| `to_K(d_src1)` | `{τ ∈ A_K^{Σ_2} : d_src1 ∈ slot_addrs(G_τ)} = {γ_1, γ_2}` | Both tuples reference d_src1 (γ_1 via the bundle, γ_2 directly). |
| `to_K(d_src2)` | `= {γ_1}` | Only γ_1's bundle references d_src2. |
| `to_K(d_src3)` | `= {γ_1}` | Only γ_1's bundle references d_src3. |
| `from_addrs_K(d_src1)` | `{d_cite}` | Collapsed: both tuples share the same from-side address. |
| `to_addrs_K(d_cite)` | `{d_src1, d_src2, d_src3}` | Flattens across γ_1's bundle and γ_2's singleton. |

The bundled (γ_1) and legacy (γ_2) tuples co-exist in the same active subset under one registration; `pair_K`'s set-equality test distinguishes the two regimes at the Boolean level, while membership-based `to_K(b)` admits queries that don't care about the bundle structure.

**Narrative variant from Σ_0 — Emission BDP0 (empty-G boundary, `|slot_addrs(G)| = 0`).** To exhibit the `n = 0` admissibility flagged in the *Empty-G admissibility* paragraph above, return to the same `Σ_0` the main timeline started from and apply a different first-step emission: fire `Emit_K(Σ_0, home_cite, F_BDP0, G_BDP0)` with `F_BDP0 = {(d_cite, δ(1, #d_cite))}` and `G_BDP0 = ∅` — citing document declares no dependency targets at all. **This first step produces a successor state `Σ_1'` of `Σ_0` (apostrophe-disambiguated from the main timeline's `Σ_1`) and is presented as a narrative variant, not as a parallel run of the state graph.** `Σ_1'` is exhibited only to walk the `n = 0` admissibility and the corresponding Sh4 suppression behavior; γ_0 never enters `A_K^{Σ_1}`, `A_K^{Σ_2}`, or any subsequent main-timeline state.

*Sh-conf check at Σ_0 (variant).* F_BDP0 canonical-slot with `slot_addrs(F_BDP0) = {d_cite}`, `|·| = 1`, `match(1, c_F = 1)` ✓. G_BDP0 is canonical-slot trivially with `slot_addrs(G_BDP0) = ∅`, `|·| = 0`, `match(0, c_G = *)` ✓ (since `0 ∈ ℕ`). Target-domain: `{d_cite} ⊆ A_doc^{Σ_0}` ✓; `∅ ⊆ A_doc^{Σ_0}` vacuously ✓. Sh4 contract clause (i) computes `C(F_BDP0, G_BDP0, Σ_0) = ∅` (no prior K-tuples at Σ_0). Clause (iii) issues. Admitted. Result `Σ_1'` with new tuple γ_0 having `slot_addrs(F_{γ_0}) = {d_cite}` and `slot_addrs(G_{γ_0}) = ∅`.

*Sh4 suppression on a duplicate empty-G attempt (within the variant).* From `Σ_1'`, attempt a *second* identical call `Emit_K(Σ_1', home_cite, F_BDP0, G_BDP0)`. Sh4 contract clause (i) computes `C(F_BDP0, G_BDP0, Σ_1') = {τ ∈ A_K^{Σ_1'} : slot_addrs(F_τ) = {d_cite} ∧ slot_addrs(G_τ) = ∅} = {γ_0}` (exact slot-pair-equality on the empty set matches γ_0 directly). Clause (ii) *suppresses*: `Emit_K` returns `⊥`, state remains `Σ_1'`, `A_K^{Σ_1'} = {γ_0}` unchanged — the empty-G slot-pair behaves identically to non-empty-G slot-pairs under Sh4.

*Template evaluation at `Σ_1'` (variant).* `A_K^{Σ_1'} = {γ_0}`. `pair_K(d_cite, ∅) = true` (witnessed by γ_0); `pair_K(d_cite, {d_src1})` and similar non-empty-G probes evaluate to `false` at `Σ_1'` (γ_0 has empty G-slot, so its slot-pair `({d_cite}, ∅)` does not match any non-empty G-pattern). This is the variant reading the main-timeline table's `pair_K(d_cite, ∅)` row contrasts against; under the main timeline at Σ_2, the same probe evaluates to `false` because the main-timeline emissions never produced an empty-G tuple, and `Σ_1'` is not a predecessor of `Σ_2`.

*Rejection case BDP3 (cardinality mismatch under a hypothetical `c_G = 1` re-registration).* If `K = citation.depends` had been registered at the prior `c_G = 1` shape, Emission BDP1 would have failed Sh-conf clause (c) with `match(3, c_G = 1) = false`. The new `c_G = *` registration is what admits BDP1; the new shape's strict superset relationship `{n ∈ ℕ : match(n, 1)} = {1} ⊂ ℕ = {n ∈ ℕ : match(n, *)}` formalizes the backward-compatible widening. ✗ at `c_G = 1`, ✓ at `c_G = *`.

### NonIdempotentDirectedPair — `(1, 1, A_doc, A_doc, ⊥)`

Non-idempotent directed-pair tuples allow multiple distinct emissions sharing the same slot-address pair — each emission is a distinct event, retained in `L_K` regardless of slot-address coincidence with prior tuples. Role-specific readings (witness → subject for coverage, commenter → target for comment, etc.) are layer conventions over a single structural shape.

*Canonical base templates (signatures derived per Sh5(b); bodies hand-curated against the DirectedPair shape-mate per Sh5(a)).* Every K registered at this shape inherits the following five templates by the catalog's hand-curation:

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

The well-definedness of `latest_K_for_addr` — that `argmax_{τ ∈ S_d} emission_order(τ)` selects a unique tuple — is conditional on the *single-home commitment* defined below. Under that commitment, `emission_order` is the substrate's chain-index function. Without it, the layer must supply a per-K `emission_order` accessor as part of its registration. Structural eligibility for SHCD is purely the shape `(1, 1, A_doc, A_doc, ⊥)`; no semantic taxonomy applies.

#### SingleHomeCoverageDiscipline (per-K, optional)

**Definition — SingleHomeCoverageDiscipline (conditional on the *single-home commitment*).** A K registered at NonIdempotentDirectedPair (shape `(1, 1, A_doc, A_doc, ⊥)`) commits to *single-home emission* iff every emission `Emit_K(Σ, d, F, G)` for type K uses a single fixed home document `d = d_K ∈ dom(Σ.M)` across the relation's lifetime. Eligibility is purely structural — any K at this shape may opt in, with no semantic-role precondition. The commitment is a per-K registration constraint, not a universal shape constraint. SHCD's conclusion — the homed-set property `(A τ ∈ L_K^Σ :: home(addr(τ)) = d_K)` — is load-bearing only under the *single-home commitment* (defined below; the contract's clauses (i)–(ii) gate every `Emit_K` call site for SHCD-registered K), so callers depending on the homed-set property (e.g., `latest_K_for_addr`'s well-definedness via `emission_order`) must verify the contract's clauses are honored at every SHCD-registered K. Structurally parallel to FunctionalDependencyDiscipline under DirectedPair: each is a per-K opt-in discipline atop its base shape, each is realized through a layer-discipline contract with its own preservation theorem.

*Single-home commitment (the layer-discipline contract for SingleHomeCoverageDiscipline).* The discipline is realized through the *single-home commitment* — the third per-K layer-discipline contract in the framework, distinct from the *Sh4 idempotency contract* and the *FDD functional-dependency contract*. The consolidated commitment reference table in *Scope and Substrate Scaffolding* records this commitment's signature (gate position 1, applicable K's with NonIdempotentDirectedPair shape + per-K SHCD opt-in, discharged theorem SHCD's homed-set commitment) alongside the framework's other named commitments. Under the *single-home commitment*, for each K with SingleHomeCoverageDiscipline registered, on every `Emit_K(Σ, d, F, G)` call site the layer enforces the following single-step protocol:


(i) If `d ≠ d_K`, the call is *rejected outright*: the layer does not issue `Emit_K(Σ, d, F, G)`; equivalently, `Emit_K` returns `⊥` at the layer's pre-substrate gate without invoking K.λ. (The framework's Sh-conf return-type extension to `(Σ' × A_rel^{Σ'}) ∪ {⊥}` accommodates this rejection at the same `⊥`-token; the caller distinguishes single-home rejection from Sh-conf rejection by inspecting the contract's pre-emission home check `d = d_K`.)

(ii) If `d = d_K`, the layer issues `Emit_K(Σ, d, F, G)` per the substrate's usual K.λ protocol (and any other applicable contracts at the same call site — Sh4, FDD, etc. — fire in their established order).

Unlike the *Sh4 idempotency contract* and the *FDD functional-dependency contract*, the *single-home commitment* requires no Observe step: the home value `d_K` is a per-K registration constant, so the home check `d = d_K` is a literal-equality test against a fixed value, with no state-dependent computation. Atomicity is trivial (no race window exists between an Observe and the substrate K.λ-step).

*Preservation under the single-home commitment.* The single-home property holds at every reachable state under the contract, by induction on `↦*`. Fix `K ∈ T_cat` with SingleHomeCoverageDiscipline registered at fixed home `d_K`.

The single-home property `(A τ ∈ L_K^Σ :: home(addr(τ)) = d_K)` is the homed-set commitment: every K-tuple ever emitted resides under `d_K`. The companion property `S_d ⊆ {chain elements at d_K}` for every `d ∈ A_doc^Σ` follows directly: `S_d = {τ ∈ A_K^Σ : to₁(τ) = d} ⊆ A_K^Σ ⊆ L_K^Σ`, and every τ ∈ L_K^Σ has `home(addr(τ)) = d_K` by the homed-set commitment, hence `addr(τ)` is a chain element at `d_K` by the *Per-document link sub-allocator chains* scaffolding clause.


*Base.* At `Σ_init`, `L_K^{Σ_init} = ∅`; the universal `(A τ ∈ L_K^{Σ_init} :: home(addr(τ)) = d_K)` is vacuous.

*Step (Case A: `L_K^{Σ'} = L_K^Σ`).* `L_K` is unchanged. The property is inherited tuple-by-tuple from the IH (no new τ to check; existing τ retain `home(addr(τ)) = d_K`).

*Step (Case B: `L_K^{Σ'} = L_K^Σ ∪ {τ_new}`).* By the *Emit_K routing commitment*, the K.λ-step originates as an `Emit_K(Σ, d, F, G)` call. The *single-home commitment* clause (i) admits the call only if `d = d_K`. Under clause (ii), K.λ's first/subsequent-emission protocol fires at home `d = d_K`, depositing τ_new at an address with `home(addr(τ_new)) = d_K` (ASN-0086, R0a-Cor1 places the deposit address in `d_K`'s link sub-allocator chain, so its home is `d_K` by L1a). So `home(addr(τ_new)) = d_K`. Combined with the IH on the older tuples, every τ ∈ L_K^{Σ'} has `home(addr(τ)) = d_K`.

*Step (Case C: `L_K^{Σ'} ⊆ L_K^Σ`)*. Impossible — L_K is monotone non-decreasing by R3. Skipped.

The induction closes. ∎

*Well-definedness of `latest_K_for_addr`.* Define `emission_order(τ) := chain_index(addr(τ), d_K)`, using the *Link sub-allocator chain-index function* scaffolding clause. Under SHCD, every `τ ∈ S_d` has `home(τ) = d_K` (homed-set commitment), so `addr(τ)` is a chain element at `d_K` and `chain_index(·, d_K)` is single-valued (T10a.7, ASN-0034). Three ingredients close `argmax_{τ ∈ S_d} emission_order(τ)`:

(i) `S_d` is finite: `S_d ⊆ dom(Σ.L)`, finite by L-fin (ASN-0043).

(ii) `τ ↦ emission_order(τ)` is injective on `S_d`: distinct addresses (R1, ASN-0086) get distinct chain indices.

(iii) Chain-index order coincides with T1 on the chain (T9 + TA5(a), ASN-0034), so the maximal-index element is uniquely selected.

`d_K` need not be exclusive to K — other relations may interleave their tuples into `d_K`'s chain; the argument restricts unchanged to any subset.

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

*Canonical base template family (signatures derived per Sh5(b); bodies hand-curated against the DirectedPair shape-mate per Sh5(a)).* The body adapts DirectedPair's templates with the asymmetry that `c_G = 0|1` requires explicit `⊥`-handling on G-side templates: F-side templates close over the totality of `from₁`; G-side templates must filter out tuples whose `to₁⁻` is undefined before applying the to-side accessor. Codomains follow the *Codomain convention for partial templates* established for partial accessors above:

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

**Emission 1' (non-idempotency demonstration).** `Emit_K(Σ_1, home_K, F_1, G_1)` with the *exact same* `F_1 = {(d_1, δ(1, #d_1))}` and `G_1 = {(d_2, δ(1, #d_2))}` as Emission 1 — a literal re-emission of the same slot-pair from the same commenter to the same target. Let the result be Σ_1' with new tuple `τ_1'`. K.λ's subsequent-emission branch fires at home_K: `{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = home_K} = {a_1}` (non-empty after Emission 1), so `ℓ_prev = max{a_1} = a_1` under T1 and `a_1' := addr(τ_1') = inc(a_1, 0)` (ASN-0086, K.λ subsequent-emission deposit address). Crucially, `addr(τ_1') = a_1' ≠ a_1 = addr(τ_1)` (T10a.7 EnumerationInjectivity, ASN-0034 — distinct chain indices yield distinct tumblers).

*Sh-conf check at Σ_1.* Identical to Emission 1's Sh-conf check; same canonical-slot, same cardinality match, same target-domain inclusion (the allocated-address sets are monotone, so `{d_1}, {d_2} ⊆ A_doc^{Σ_1}` still). Admitted. ✓

*Why no Sh4 suppression fires.* `comment` has `shape(K).idem = ⊥` (NonIdempotentDirectedPair), so K is not registered under the *Sh4 idempotency contract*. The Sh4 contract's gate-3 candidate-set check `C(F_1, G_1, Σ_1)` is *not executed* — gate 3 is skipped entirely at idem = ⊥ K not under FDD (per the *Gate Ordering* consolidated section). Compare against the hypothetical case where `comment` were registered with `idem = ⊤`: then `C(F_1, G_1, Σ_1) = {τ_1}` (slot-pair `({d_1}, {d_2})` matches τ_1 exactly), clause (ii) would suppress, and `Emit_K` would return `⊥`. The defining feature of NonIdempotentDirectedPair is exactly this admission of slot-pair-identical re-emissions as distinct active tuples. After Emission 1': `L_K^{Σ_1'} = A_K^{Σ_1'} = {τ_1, τ_1'}` — two active tuples with the *same* slot-address pair `({d_1}, {d_2})` but distinct tuple addresses `a_1 ≠ a_1'`.

**Emission 2.** `Emit_K(Σ_1', home_K, F_2, G_2)` with `F_2 = {(d_2, δ(1, #d_2))}` (commenter is d_2) and `G_2 = {(d_2, δ(1, #d_2))}` (target is d_2 again). Let the result be Σ_2 with new tuple `τ_2`. K.λ's subsequent-emission branch fires at home_K: `{ℓ' ∈ dom(Σ_1'.L) : origin(ℓ') = home_K} = {a_1, a_1'}` (non-empty after Emissions 1 and 1'), so `ℓ_prev = max{a_1, a_1'} = a_1'` under T1 (since `a_1' = inc(a_1, 0) > a_1` by TA5(a), ASN-0034) and `a_2 := addr(τ_2) = inc(a_1', 0)` (ASN-0086, K.λ subsequent-emission deposit address).

*Sh-conf check at Σ_1'.* Symmetric to Emission 1. Admitted. ✓

**Sh0–Sh3 hold at Σ_2 by direct check.** `L_K^{Σ_2} = {τ_1, τ_1', τ_2}`. Per-tuple verification:

- *τ_1:* `slot_addrs(F_1) = {d_1}`, `|{d_1}| = 1`, `match(1, c_F = 1)` ✓ (Sh0); `slot_addrs(G_1) = {d_2}`, `|{d_2}| = 1`, `match(1, c_G = 1)` ✓ (Sh1); `{d_1} ⊆ A_doc^{Σ_2}` ✓ (Sh2, `d_1` is allocated since `d_1 ∈ A_doc^{Σ_0} ⊆ A_doc^{Σ_2}` by allocated-set monotonicity); `{d_2} ⊆ A_doc^{Σ_2}` ✓ (Sh3, same).
- *τ_1':* `slot_addrs(F_{τ_1'}) = {d_1}`, `|{d_1}| = 1`, `match(1, c_F = 1)` ✓ (Sh0); `slot_addrs(G_{τ_1'}) = {d_2}`, `|{d_2}| = 1`, `match(1, c_G = 1)` ✓ (Sh1); `{d_1} ⊆ A_doc^{Σ_2}` ✓ (Sh2); `{d_2} ⊆ A_doc^{Σ_2}` ✓ (Sh3). The slot-address sets coincide with τ_1's, but Sh0–Sh3 quantify over each tuple independently — the per-tuple checks discharge identically without any pairwise-distinctness obligation. Sh4 would impose pairwise distinctness, but Sh4 is conditional on `shape(K).idem = ⊤`, and `comment`'s `idem = ⊥` excludes this K from Sh4's universal.
- *τ_2:* `slot_addrs(F_2) = {d_2}`, `|{d_2}| = 1`, `match(1, c_F = 1)` ✓ (Sh0); `slot_addrs(G_2) = {d_2}`, `|{d_2}| = 1`, `match(1, c_G = 1)` ✓ (Sh1); `{d_2} ⊆ A_doc^{Σ_2}` ✓ (Sh2 and Sh3, same slot address).

The per-tuple checks discharge each invariant pointwise; the universal quantifier in Sh0–Sh3 closes by inspection of the three-element relation. The slot-pair coincidence `(slot_addrs(F_{τ_1}), slot_addrs(G_{τ_1})) = (slot_addrs(F_{τ_1'}), slot_addrs(G_{τ_1'})) = ({d_1}, {d_2})` is admissible because `comment` is not under Sh4.

**Template evaluation at Σ_2.** Suppose no Resolution tuples have been emitted yet, so `A_{K_res}^{Σ_2} = ∅` for a chosen Resolution relation `K_res` of shape `(1, 1, A_doc, A_rel, ⊤)`. (The layer selects `K_res` as the resolver vocabulary; the framework imposes no co-registration.) Compute:

`A_K^{Σ_2} = L_K^{Σ_2} \ nullified(Σ_2) = {τ_1, τ_1', τ_2}` (no retractions issued).

The NonIdempotentDirectedPair base templates evaluate at Σ_2 as:

| Template | Evaluation at Σ_2 | Notes |
|---|---|---|
| `pair_K(d_1, d_2)` | `(E τ ∈ A_K^{Σ_2} :: from₁(τ) = d_1 ∧ to₁(τ) = d_2) = true` | Witnessed by *either* τ_1 *or* τ_1' (or both — pair_K is Boolean, so multiplicity is not visible at the witness level). |
| `from_K(d_1)` | `{τ ∈ A_K^{Σ_2} : from₁(τ) = d_1} = {τ_1, τ_1'}` | Both tuples have from₁(·) = d_1 (Emission 1 and Emission 1'). The slot-pair-identical tuples are kept distinct by tuple address (R1, ASN-0086) — the set carries both, exhibiting the non-idempotency that Sh4 would otherwise suppress. |
| `from_K(d_2)` | `{τ_2}` | Only τ_2 has from₁(·) = d_2. |
| `to_K(d_2)` | `{τ ∈ A_K^{Σ_2} : to₁(τ) = d_2} = {τ_1, τ_1', τ_2}` | All three active tuples target d_2; the multiplicity at τ_1 vs τ_1' is preserved in the tuple-valued accessor. |
| `to_addrs_K(d_1)` | `{to₁(τ) : τ ∈ A_K^{Σ_2} ∧ from₁(τ) = d_1} = {d_2}` | The set comprehension collapses τ_1 and τ_1' onto their shared to-address d_2; the address-valued projection is therefore a singleton even though `from_K(d_1)` has two tuples. |
| `from_addrs_K(d_2)` | `{from₁(τ) : τ ∈ A_K^{Σ_2} ∧ to₁(τ) = d_2} = {d_1, d_2}` | Address-side collapse across τ_1, τ_1', τ_2: τ_1 and τ_1' contribute d_1 (collapsed by set union); τ_2 contributes d_2. |

`unresolved_K_comments_via(K_res, d_2) = {τ ∈ A_K^{Σ_2} : to₁(τ) = d_2 ∧ ¬resolved_by(τ, K_res)}`

All three of τ_1, τ_1', τ_2 have `to₁(·) = d_2`; for each, `resolved_by(τ, K_res)` requires `(E ρ ∈ A_{K_res}^{Σ_2} :: to₁(ρ) = addr(τ))`, vacuously false since `A_{K_res}^{Σ_2} = ∅`. So:

`unresolved_K_comments_via(K_res, d_2) = {τ_1, τ_1', τ_2}`

`all_K_resolved_via(K_res, d_2) = false`.

**Emission 3 (resolution).** `ρ_1 := Emit_{K_res}(Σ_2, home_R, F_ρ, G_ρ)` with `F_ρ = {(d_2, δ(1, #d_2))}` (resolver) and `G_ρ = {(a_1, δ(1, #a_1))}` (resolves τ_1 via R5, TupleSelfTargeting, ASN-0086). Result Σ_3.

*Sh-conf check at Σ_2 (under K_res shape).* F_ρ canonical-slot, `slot_addrs = {d_2}`, matches `c_F = 1`, `{d_2} ⊆ A_doc^{Σ_2}`. G_ρ canonical-slot, `slot_addrs = {a_1}`, matches `c_G = 1`, `{a_1} ⊆ A_rel^{Σ_2}` (since a_1 ∈ dom(Σ.L)). Admitted. ✓

**Template evaluation at Σ_3.**

`A_{K_res}^{Σ_3} = {ρ_1}` (no nullification).

`resolved_by(τ_1, K_res) = true` (ρ_1 witnesses, since `to₁(ρ_1) = a_1 = addr(τ_1)`); `resolved_by(τ_1', K_res) = false` (ρ_1's to-slot is a_1, not a_1' = addr(τ_1') — the non-idempotency makes each slot-pair-identical tuple independently resolvable); `resolved_by(τ_2, K_res) = false`.

`unresolved_K_comments_via(K_res, d_2) = {τ_1', τ_2}`

`all_K_resolved_via(K_res, d_2) = false` (τ_1' and τ_2 still unresolved).

**Emission 4 (resolution of τ_1').** `ρ_1' := Emit_{K_res}(Σ_3, home_R, F_ρ, G_{ρ'})` with `F_ρ = {(d_2, δ(1, #d_2))}` and `G_{ρ'} = {(a_1', δ(1, #a_1'))}` (resolves τ_1'). Result Σ_4. *Sh-conf check at Σ_3 (under K_res shape).* F_ρ canonical-slot, `slot_addrs = {d_2}`, matches `c_F = 1`, `{d_2} ⊆ A_doc^{Σ_3}` (d_2 allocated). G_{ρ'} canonical-slot, `slot_addrs = {a_1'}`, matches `c_G = 1`, `{a_1'} ⊆ A_rel^{Σ_3}` (since `a_1' ∈ dom(Σ_1'.L) ⊆ dom(Σ_3.L)` by L12a monotonicity). Admitted. ✓ After this emission: `resolved_by(τ_1', K_res) = true` (ρ_1' witnesses).

**Emission 5 (resolution of τ_2).** Emit `ρ_2` resolving τ_2 (analogous to Emission 3 with `G = {(a_2, δ(1, #a_2))}`). Result Σ_5.

`A_K^{Σ_5} = {τ_1, τ_1', τ_2}` (no comment retractions issued; the resolution emissions extend `A_{K_res}`, not `A_K`).

`A_{K_res}^{Σ_5} = {ρ_1, ρ_1', ρ_2}`.

`unresolved_K_comments_via(K_res, d_2) = ∅` (all three comments now resolved).

`all_K_resolved_via(K_res, d_2) = true`. The flag flips as expected. The fact that *two* resolution emissions (ρ_1 for τ_1 and ρ_1' for τ_1') were required to resolve the slot-pair-identical comments — even though their slot-pairs coincide — is a direct consequence of NonIdempotentDirectedPair's `idem = ⊥`: resolution targets *tuple addresses* (via R5 TupleSelfTargeting, ASN-0086), and the two slot-pair-identical comments have distinct tuple addresses, hence require distinct resolutions.

**Rejection case 1: non-canonical from-set.** From Σ_5, attempt `Emit_K(Σ_5, home_K, F_3, G_3)` with `F_3 = {(d_1, δ(2, #d_1))}` — a width-2 displacement violating canonical-slot form, which requires unit-width displacements `δ(1, #x)` (the canonical form fixes the last-component value at 1; values ≥ 2 are rejected). Here `δ(2, #d_1)` and the canonical `δ(1, #d_1)` share the same length `#d_1` — the displacement *depth* is identical; they differ only at the last component, where the canonical form admits the value 1 and rejects 2. Sh-conf clause (a) fails: `F_3` is not in canonical-slot form, so `slot_addrs(F_3)` is undefined (there is no `X_F` such that `F_3 = {(x, δ(1, #x)) : x ∈ X_F}`). The emission is rejected before any state transition. State remains Σ_5 unchanged; in particular `L_K^{Σ_5}, A_K^{Σ_5}` are not modified. ✗

Note that L4 (EndsetGenerality, ASN-0043) permits `F_3` in the substrate's link store at the level of endset well-formedness; the framework rejects it as a layer-level discipline imposed by Sh-conf. The substrate primitive K.λ would still accept `F_3` if invoked outside Emit_K — but per the *Emit_K routing commitment* (Scope and Substrate Scaffolding), the relational layer routes all class-(iii) emissions of `K ∈ T_cat` through Emit_K, so this bypass is not exercised within the framework's scope.

**Rejection case 2: unallocated to-slot address.** From Σ_5, let `d_ghost ∈ T` be a tumbler outside `A^{Σ_5}` — an unallocated address (e.g., a future document not yet registered, or a deliberately-chosen ghost per L9 of ASN-0043). Attempt `Emit_K(Σ_5, home_K, F_4, G_4)` with `F_4 = {(d_1, δ(1, #d_1))}` (canonical-slot, `slot_addrs(F_4) = {d_1}`) and `G_4 = {(d_ghost, δ(1, #d_ghost))}` (canonical-slot, `slot_addrs(G_4) = {d_ghost}`). Sh-conf clause (d) fails on the G-side: `slot_addrs(G_4) = {d_ghost}` is not a subset of `t_G^{Σ_5} = A_doc^{Σ_5}` because `d_ghost ∉ A_doc^{Σ_5}`. The emission is rejected before any state transition. State remains Σ_5. ✗

This rejection is constitutive of the framework's discipline: shapes restrict slot addresses to *already-allocated* targets at emission time. L9 (TypeGhostPermission, ASN-0043) admits ghost spans in endsets generally — including in the type-endset slot — but the shape framework forbids ghost addresses in *slot positions* of registered relations. Whether a future shape family should admit ghost-targeting slot semantics is an open question (see Open Questions).

**Rejection case 3: cardinality mismatch.** From Σ_5, attempt `Emit_K(Σ_5, home_K, F_5, G_5)` with `F_5 = {(d_1, δ(1, #d_1)), (d_2, δ(1, #d_2))}` (canonical-slot, but `slot_addrs(F_5) = {d_1, d_2}` with `|·| = 2`) and `G_5 = {(d_2, δ(1, #d_2))}` (canonical-slot, single slot address). Sh-conf clause (c) fails on the F-side: `match(2, c_F = 1)` is false (cardinality 2 does not match the exact-1 requirement). The emission is rejected before any state transition. State remains Σ_5. ✗

Symmetric rejection: emitting with `F_5' = ∅` against `c_F = 1` fails on `match(0, 1)`; emitting with the same `G_5` swapped for an empty G fails on `match(0, c_G = 1)`. Cardinality is the second of Sh-conf's three independently-checked structural gates (canonical form, cardinality, target domain); a mismatch at any gate rejects.

**Rejection case 4: unregistered type (K ∉ T_cat).** Let `K_ghost ∈ T_admissible \ T_cat` be a non-empty type endset that has not been registered with the catalog — for example, a type endset whose coverage class corresponds to no canonical shape, perhaps because the calling layer has not yet declared the relation, or because the type was constructed ad-hoc and never added to `T_cat`. Attempt `Emit_{K_ghost}(Σ_5, home_K, F_6, G_6)` with arbitrary `F_6, G_6 ∈ Endset` — concretely, we reuse Emission 1's values: `F_6 = F_1 = {(d_1, δ(1, #d_1))}` and `G_6 = G_1 = {(d_2, δ(1, #d_2))}`, both canonical-slot and well-allocated. Sh-conf's first conjunct `K_ghost ∈ T_cat` is *false* at the coverage-equivalence membership test against the registered representative list (per the *Decidable membership* paragraph in the TypedRelationCatalog Definition above): `K_ghost`'s coverage class is not one of the registered classes, so no representative `K_rep` in the list satisfies `K_ghost ~ K_rep`. The emission is rejected at this gate; `Emit_K` returns `⊥` (per Sh-conf's extended return type) and no state transition occurs. The second conjunct `conf_{K_ghost}^{Σ_5}(F_6, G_6)` is unevaluable — `shape(K_ghost)` is undefined for unregistered K, so the conformance predicate has no shape tuple to test against — but the first conjunct's failure is sufficient to reject without proceeding to the conformance check. State remains Σ_5. ✗

The `K ∈ T_cat` gate is structurally separate from the three conformance gates (clauses (a)–(d) of Sh-conf). It protects the framework's invariants against accidental schema drift: only registered relations participate in shape-discipline reasoning, and emissions at unregistered types are rejected at the registry boundary regardless of how their `F, G` are structured. A layer that wants to admit `K_ghost` must first register it with the catalog — selecting a shape, committing to the per-class constancy of `shape(·)`, and accepting Sh-conf's structural gates for all subsequent emissions at that K.

**Edge case: retraction of τ_1.** From Σ_5, issue `Nullify(Σ_5, d_retr, a_1)` producing Σ_6. By R6c (RestorationByReemission, ASN-0086), τ_1 is permanently removed from `A_K^Σ` for all future states. So:

`A_K^{Σ_6} = {τ_1', τ_2}` (τ_1 nullified; τ_1' and τ_2 remain — τ_1' is unaffected by the retraction of τ_1, since the two have distinct tuple addresses despite sharing slot-pair).

`unresolved_K_comments_via(K_res, d_2) = {τ ∈ A_K^{Σ_6} : to₁(τ) = d_2 ∧ ¬resolved_by(τ, K_res)} = ∅` (τ_1' is still resolved by ρ_1' and τ_2 still resolved by ρ_2, both of which remain in `A_{K_res}^{Σ_6}`).

`all_K_resolved_via(K_res, d_2) = true`.

*Distinction from the idempotent case.* Under DirectedPair (idem = ⊤), Emission 1' would have been suppressed at gate 3 by Sh4, so τ_1' would never have entered A_K, and the retraction of τ_1 would have left `A_K^{Σ_6} = {τ_2}` — a single tuple at slot-pair ({d_1}, {d_2}) erased entirely. Under NonIdempotentDirectedPair (idem = ⊥), each emission produces a distinct active tuple, and retracting one leaves the others intact — this is the *event-distinct* semantics non-idempotent shapes are designed to preserve.

The framework gives stable, well-typed answers across emission and retraction events. Sh0–Sh3 are preserved inductively, template signatures match the shape registry, and the active-subset machinery composes cleanly with retraction.


## Consequences

(a) *Adding a new relation inherits its shape-mate's templates by hand-curation.* A new K registered at `shape(K) = DirectedPair` inherits the row's five base templates (`pair_K`, `from_K`, `to_K`, `from_addrs_K`, `to_addrs_K`) by the catalog's current hand-curation against the DirectedPair shape-mate, with signatures mechanically derived per Sh5(b)'s *Signature derivation rule*. Body-shape convergence with prior shape-mate rows is an aspiration of the present catalog (per Sh5(a)'s downgrade), not a framework-enforced derivation: registering a divergent template body at the same shape is not blocked by any mechanical gate. The cost of a new relation is one entry in the shape registry plus the author's diligence at Sh5(b)'s checklist. Layers consuming an Attribute-style or Citation-style reading further define aliases (`has_K`, `K_sidecars_of`, `cites_K`, `K_incoming`); the singleton-returning `K_target_of` becomes available when the layer additionally registers FunctionalDependencyDiscipline.

(b) *Composite predicates extend the catalog through the same compositional primitives.* A composite predicate combines atomic templates through Boolean operators and quantification over `T_cat`. The framework does not establish a closure theorem about these primitives. The design observation we record is weaker: the canonical-shape catalog is the registry's *atomic* vocabulary, and adding a structurally new pattern (e.g., a slot-cardinality combination not yet present) is handled by extending the catalog with a new canonical shape, not by composing existing relations.

(c) *Shape misregistration is a structural error.* Registering a relation with the wrong shape produces predicates with wrong signatures or wrong semantics — the substrate cannot self-correct this. By Sh-conf, attempts to emit non-conformant tuples are rejected, but the rejection assumes the registered shape is the *correct* shape; if the registry is wrong, the substrate enforces the wrong constraint. Shape registration is part of the relation's contract.

(d) *The predicate language is bounded by the shape catalog.* "What the substrate can ask" is determined by the templates the shapes generate. Questions about content quality ("is this proof complete?", "is this description good?") are not expressible because no canonical shape's template generates them. Those are agent-time questions, not substrate questions.


## Properties Introduced

*Load-bearing claims.* The axioms, lemmas, and corollaries on which the framework's preservation theorems and consumer accessors rest.

| Label | Type | Statement |
|-------|------|-----------|
| Sh-conf | AXIOM | Emit_K rejects unregistered types and non-conformant emissions; returns `⊥` on failure |
| CaseAClosureForLK | LEMMA | Classifies the four ↦-step classes preserving `L_K^{Σ'} = L_K^Σ` (Case A) versus extending it by one tuple (Case B); shared by Sh0–Sh3 |
| Sh0 | LEMMA | FromSlotCanonicalAndCardinalityFixed |
| Sh1 | LEMMA | ToSlotCanonicalAndCardinalityFixed |
| Sh2 | LEMMA | FromSlotTargetRestricted — `slot_addrs(F) ⊆ t_F^Σ` |
| Sh3 | LEMMA | ToSlotTargetRestricted — `slot_addrs(G) ⊆ t_G^Σ` |
| Sh4 | LEMMA | IdempotencyDiscipline — at-most-one active duplicate when `idem = ⊤`; conditional on the *Sh4 idempotency contract* |
| SlotAccessorTotality | LEMMA | When `c = 1`, the point accessor is total |
| AllocatedAddressAntichain | LEMMA | At a substrate-conforming layer, `cov_allocated({(x, δ(1, #x))}, Σ) = {x}` for every `x ∈ A^Σ` |
| LinkAddressNotPrefixOfEmit | LEMMA | `b ⋠ a_emit(Σ, d)` for every `b ∈ dom(Σ.L)` and `d ∈ dom(Σ.M)` |
| RetractionSelfFreshness | LEMMA | When R is registered and Sh-conf + Sh4 admit an `Emit_R` call to clause (iii), the freshly deposited tuple τ_new satisfies `addr(τ_new) ∉ nullified(Σ')` (equivalently, `τ_new ∈ A_R^{Σ'}`); hoisted as a top-level section before Sh4; cited by Sh4 Case C (self-retraction sub-case) and Case D (pivot for simultaneous addition-and-contraction); structurally dual to NullifyActiveSubsetCompatibility's R0a-driven postcondition on the target address |
| EffectiveWpSimplification | COROLLARY | Under the *Emit_K routing commitment*, `wp_eff = d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G) ∧ Π_K` with `Π_K` capturing per-K discipline non-suppression |
| NullifyActiveSubsetCompatibility | COROLLARY | Active-subset content of ASN-0086's Nullify postcondition holds at `Σ_target` whether the call issues or suppresses; audit-slice multiplicity not preserved |
| Sh4 idempotency contract | CONTRACT | Observe-then-Emit protocol for idempotent K, atomically scoped at `~`-class of K |
| FDD functional-dependency contract | CONTRACT | Observe-then-Emit protocol with from-slot-only candidate `C_fd` |
| single-home commitment | CONTRACT | Layer-discipline contract realizing SHCD; literal home-equality test, no Observe step |

*Supporting definitions.* Symbol introductions, projections, and accessor signatures used by the load-bearing claims.

| Label | Type | Statement |
|-------|------|-----------|
| cov | DEF | Coverage projection `L_K → ℘(T) × ℘(T)` |
| cov_allocated | DEF | `cov_allocated(F, Σ) = coverage(F) ∩ A^Σ`; finite, monotone along `⊑̂` |
| canonical-slot form | DEF | Endset form `{(x, δ(1, #x)) : x ∈ X_F}` |
| slot_addrs | DEF | Extraction `F ↦ X_F` for canonical-form F |
| Sh_K | DEF | Shape: `(c_F, c_G, t_F, t_G, idem)` |
| ShapeWellFormedness | DEF | Four implications relating `c = 0` to `t = -` (both sides); registry admits only well-formed shapes |
| match | DEF | Cardinality match predicate over `{0, 1, *, 0\|1}` |
| T_cat | DEF | Typed-relation catalog `⊆ T_admissible` (finite up to `~`); lifetime-constant |
| shape | DEF | Shape registry `T_cat → Shape`, per-class constant, lifetime-constant |
| conf_K^Σ | DEF | State-indexed conformance predicate; monotone along `⊑̂` |
| from_K^Σ, to_K^Σ | DEF | Total set-valued slot accessors |
| from₁, to₁ | DEF | Point-valued slot accessors (defined when c = 1) |
| from₁⁻, to₁⁻ | DEF | Optional point-valued slot accessors (defined when c = 0\|1) |
| SingleHomeCoverageDiscipline | DEF | Per-K opt-in at NonIdempotentDirectedPair; homed-set commitment via fixed `d_K` |
| FunctionalDependencyDiscipline | DEF | Per-K commitment for DirectedPair: at most one active tuple per from-slot |
| Sh5 | META | Template catalog organizational convenience; hand-curated per-shape template families |
| substrate-conforming-layer scaffolding | ASSUMPTION | Named scaffolding clauses: element-level addresses, subspace partitions, content-store antichain/monotonicity/finiteness, document address structure, link sub-allocator chains |
| Emit_K routing commitment | ASSUMPTION | Every class-(iii) emission of `K ∈ T_cat` routes through `Emit_K` |


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
- **[scope boundary]** The framework's preservation theorems for Sh4, FDD, and SHCD presuppose the empty-link-store baseline `L_K^{Σ_init} = ∅` at every `K ∈ T_cat`. ASN-0086 admits reachable states from arbitrary initial configurations, so a layer instantiating the framework atop a substrate-conforming layer that does *not* start with empty link stores gets weaker guarantees than the framework's preservation theorems state. The relaxed per-tuple-conformance baseline ("every tuple in `L_K^{Σ_init}` satisfies `conf_K^{Σ_init}`") suffices for Sh0–Sh3 but is not sufficient for Sh4/FDD/SHCD, whose pairwise-distinctness and homed-set conclusions require initial emptiness. Retrofitting the framework onto a non-empty initial link store requires the layer to verify Sh4/FDD/SHCD baselines per-K at the registration point — establishing that any pre-existing tuples in `L_K^{Σ_init}` already satisfy the discipline's pairwise condition. Characterizing the minimum per-K baseline check that secures each preservation theorem under non-empty initial states would *extend* the framework's scope; this item flags the boundary, not an unresolved internal question.


