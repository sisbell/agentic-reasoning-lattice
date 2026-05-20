# ASN-0094: Typed Relation Shapes

*Restricting the relational primitive into a predicate language.*

ASN-0086 establishes typed relations `L_K` with the three operations Emit, Observe, Nullify, governed by the lemma family R0…R7a (concretely: R0, R0a, R0a-Cor1, R0a-Cor2, R1, R2, R3, R4, R5, R5-Cor, R6a, R6b, R6c, R6c-Corollary, R7a, together with the auxiliary lemma LinkStoreInvarianceUnderArrangement). The relational structure as defined there is too permissive to support a typed predicate vocabulary: F and G can be any finite endsets whose coverage lies anywhere in `T`, so a predicate over `L_K` has no fixed signature. Every predicate would have to take a pattern in `℘(T) × ℘(T)` and return Bool, "two relations of the same shape" would not be expressible, and slot accessors `from(τ)`, `to(τ)` would be partial in a way that defeats type-checking.

We are looking for the minimum additional layer that closes this gap. The answer is a single structural decision per type: each `K ∈ T_cat` is assigned a *shape* — a tuple of constraints on cardinality, target domain, and idempotency — and the substrate enforces shape-conformance at Emit time. From the shape, a predicate template family is mechanically organized (though not mechanically derived; see Sh5). The pipeline is:

> R0…R7a (typed relations + operations) → **shape restrictions** (this document) → predicate template families → composed predicates

Shapes are not derivable from R0…R7a. They are an additional design decision the substrate makes about which relations it admits and what `(F, G)` pairs each admits. We justify each constraint by what predicate forms it makes possible, and by what the substrate cannot express without it.


## Scope and Substrate Scaffolding

*Arity scope.* This framework restricts the standard-triple slice `L^Σ` of `dom(Σ.L)` — the arity-3 links collected by ASN-0086's `L^Σ` definition. Higher-arity links admitted by L3 (ASN-0043) are outside its scope: the cardinality and target-domain shape components are defined over two slots only (F and G), and the slot-accessor and template machinery presupposes the arity-3 structure. Extending the framework to higher arities would require additional shape components per extra slot, which we do not pursue here.

*Emit_K routing commitment.* The framework is a discipline imposed by a relational layer atop ASN-0086. Every class-(iii) emission of a type `K ∈ T_cat` is committed to route through `Emit_K`; non-`Emit_K` class-(iii) invocations of these types are outside the framework's scope. Sh-conf below binds `Emit_K` (the relational-layer operation), not K.λ (the substrate primitive — K.λ remains permissive at the substrate level: any `F, G ∈ Endset` with `K ∈ T_admissible` is admissible to K.λ). The inductive arguments for Sh0–Sh3 invoke the *Emit_K routing commitment* to conclude that every new tuple in `L_K^Σ` for `K ∈ T_cat` arrived via an `Emit_K` call subject to Sh-conf.

*Naming convention for distinct framework commitments.* The framework operates under several distinct, non-interchangeable commitments. Each carries an explicit name to prevent conflation:
- *Emit_K routing commitment* (this paragraph): every class-(iii) `K ∈ T_cat` emission routes through `Emit_K`. Distinct from any conformance content.
- *Sh4 idempotency contract* (defined in the Sh4 section as the *Layer-discipline contract*): the layer's Observe-then-Emit protocol clauses (i)–(iii) for `shape(K).idem = ⊤` types.
- *FDD functional-dependency contract* (defined in the FunctionalDependencyDiscipline section): the layer's at-most-one-tuple-per-from-slot Observe-then-Emit protocol, strictly stronger than Sh4.
- *Single-home commitment* (defined in the SingleHomeCoverageDiscipline section): a per-K registration constraint that every K-emission uses one fixed home `d_K`.
- *Unit-depth retraction discipline* (ASN-0086): every `L_R^Σ` tuple's G is a single unit-depth span; this framework derives the discipline as a consequence of the Retraction shape rather than re-imposing it.

Subsequent text uses these names consistently. Where ambiguity could arise (e.g., a step in a preservation proof invokes more than one commitment), each commitment is cited by its explicit name at the citation site.

*Substrate-conforming-layer scaffolding.* The framework operates atop a *substrate-conforming layer* (ASN-0086, Definition). Where the framework's proofs and definitions require properties of `dom(Σ.C)`, `dom(Σ.L)`, and `dom(Σ.M)` not derivable from ASN-0034/ASN-0043/ASN-0086 alone, they consume them through the substrate-conforming-layer interface. ASN-0086's `SubstrateConformingLayer` Definition enumerates the full substrate invariant and chain-discipline catalog that a conforming layer must preserve; the following scaffolding clauses surface the specific properties this ASN cites by name without re-attributing them to the layer's internal numbered invariants. The label *substrate-conforming-layer scaffolding* (or just *the scaffolding clauses*) is the framework's name for the union; earlier drafts called this *content-side scaffolding*, but the union spans both link-side, content-side, and document-side properties — five of the ten clauses below are not strictly content-side — so the name is retired in favor of the substrate-conforming-layer reading.

- *Element-level content addresses.* Every `a ∈ dom(Σ.C)` is T4-valid (in the sense of T4, ASN-0034) with `zeros(a) = 3` and `#E(a) ≥ 2`. (Content-side analog of L1, L1b, and L1c from ASN-0043; T4-validity is the content-side counterpart to L1c's derivation via T10a.4 on the link side, and is required to apply T4(iv) at content addresses — e.g., in AllocatedAddressAntichain's Step 3.2.)
- *Content subspace partition.* There is a fixed subspace identifier `s_C ∈ ℕ` with `s_C > 0` and `s_C ≠ s_L` such that `E(a).1 = s_C` for every `a ∈ dom(Σ.C)`. (Symmetric to L0 from ASN-0043, with `s_C ≠ s_L` distinct. The positivity `s_C > 0` is forced by the element-level content-address clause's `zeros(a) = 3`: a constant `s_C = 0` would make every content address carry a fourth zero at the first E-field position, contradicting `zeros(a) = 3`.)
- *Link subspace partition.* There is a fixed subspace identifier `s_L ∈ ℕ` with `s_L > 0` such that `E(a).1 = s_L` for every `a ∈ dom(Σ.L)`. (Concrete realization of L0 from ASN-0043 — L0 states `subspace_I(a) = s_L` over an abstract identifier function `subspace_I(·)`; the scaffolding commits the substrate-conforming layer to the identification `subspace_I(·) = E(·).1` on element-level addresses, making the link-side and content-side subspace partitions symmetric and directly comparable at the first element-field component. The positivity `s_L > 0` is forced by L1's `zeros(a) = 3` for every `a ∈ dom(Σ.L)`, by the same argument as for `s_C > 0`.)
- *Content-store antichain.* `dom(Σ.C)` is a tumbler-prefix antichain at every reachable state: `(A a, a' ∈ dom(Σ.C) :: a ≼ a' ⟹ a = a')`. (Content-side symmetric to R0a from ASN-0086.)
- *Content-store monotonicity.* `dom(Σ.C) ⊆ dom(Σ'.C)` for every transition `Σ ↦ Σ'`. (Content-side symmetric to L12a from ASN-0043; content addresses are never deallocated.)
- *Content-store finiteness.* `dom(Σ.C)` is finite at every reachable state. (Content-side symmetric to L-fin from ASN-0043 — the link-side finiteness fact — supplied by the substrate-conforming layer.)
- *Document address structure.* Every `d ∈ dom(Σ.M)` is T4-valid with `zeros(d) = 2` — i.e., a document-level tumbler with two field-separator zeros (after node and user fields), no element-field zero. This is the property of document addresses surfaced by the substrate-conforming layer; the framework cites it directly without unpacking the chain through any specific numbered substrate invariant.
- *Per-document link sub-allocator chains.* For each `d ∈ dom(Σ.M)` the substrate-conforming layer supplies a link sub-allocator whose output chain enumerates `{ℓ : home(ℓ) = d}` under T9 (ForwardAllocation, ASN-0034); this is the same chain enumeration referenced by ASN-0086's R0a-Cor1 and FreshEmissionAddress.
- *Uniform link sub-allocator chain length.* All outputs of a single document's link sub-allocator share the same tumbler length: for every `d ∈ dom(Σ.M)` and every pair `ℓ_1, ℓ_2` in the chain at `d`, `#ℓ_1 = #ℓ_2`. (Property of the chain discipline supplied by the substrate-conforming layer; the framework cites this scaffolding name in proofs that need to compare two chain elements' lengths.)
- *Link sub-allocator chain-index function.* For each `d ∈ dom(Σ.M)` and each `ℓ` in the chain at `d`, the substrate-conforming layer supplies a total function `chain_index(ℓ, d) ∈ ℕ` such that `ℓ = inc^{chain_index(ℓ, d)}(d.0.s_L.1, 0)` — the unique non-negative integer indexing `ℓ`'s position in the link sub-allocator's enumeration. Well-defined and single-valued by T10a.7 (EnumerationInjectivity, ASN-0034) applied to the chain at `d`; total because the lemma's hypothesis "`ℓ` in the chain at `d`" supplies a chain index by construction. The framework cites this scaffolding name when downstream templates and disciplines (e.g., `emission_order` in the Coverage walkthrough) need a named accessor onto the chain-index machinery rather than appealing to implicit chain enumeration.

We refer to these collectively as *the scaffolding clauses* (equivalently, *the substrate-conforming-layer scaffolding*) and cite them by name in proofs below.


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

**Lemma — AllocatedAddressAntichain.** For every reachable state `Σ` and every `x ∈ A^Σ`:

`cov_allocated({(x, δ(1, #x))}, Σ) = {x}`

*Element-level character of `A^Σ`.* The hypothesis `x ∈ A^Σ` is sufficient to invoke the lemma without a separate side-condition: every address in `A^Σ = dom(Σ.C) ∪ dom(Σ.L)` is element-level with non-empty element field. The link side `dom(Σ.L)` is element-level by L1 (LinkElementLevel, ASN-0043) with `zeros(·) = 3` and `#E(·) ≥ 2` by L1b. The content side `dom(Σ.C)` is element-level by the element-level content-address clause of the substrate-conforming-layer scaffolding (Scope and Substrate Scaffolding). Span well-formedness `(x, δ(1, #x))` under T12 (SpanWellDefinedness, ASN-0034) holds because `#x ≥ 1` for every `x ∈ T` (T0, ASN-0034), so the bare hypothesis `x ∈ A^Σ` suffices for both the span well-formedness check and the element-level case analysis below.

*Proof.* `coverage({(x, δ(1, #x))}) = {t : x ≼ t}` by PrefixSpanCoverage. The intersection with `A^Σ` is `S := {a ∈ A^Σ : x ≼ a}`. By Prefix reflexivity (ASN-0034), `x ∈ S`. For the reverse, fix `a ∈ S`; we show `a = x` by case on the domains.

*Case 1* (`x, a ∈ dom(Σ.L)`): By R0a (FlatLinkDomain, ASN-0086), `dom(Σ.L)` is a tumbler-prefix antichain, so `x ≼ a ⟹ x = a`.

*Case 2* (`x, a ∈ dom(Σ.C)`): By the content-store antichain assumption (Scope and Substrate Scaffolding above), `dom(Σ.C)` is a tumbler-prefix antichain, so `x ≼ a ⟹ x = a`.

*Case 3* (`x` and `a` lie in different domains). Sub-case 3a treats `x ∈ dom(Σ.L), a ∈ dom(Σ.C)`; Sub-case 3b treats `x ∈ dom(Σ.C), a ∈ dom(Σ.L)`. By L1 (LinkElementLevel, ASN-0043) and L1c (LinkAllocatorConformance, ASN-0043) on the link side — which via T10a.4 supplies T4-validity for every link-side address — together with the element-level content-address scaffolding clause on the content side — which supplies T4-validity directly for every content-side address — both `x` and `a` are element-level (`zeros(x) = zeros(a) = 3`) and T4-valid in either sub-case; Step 3.2 below establishes E-field non-emptiness (`#E(·) ≥ 1`) from T4(iv) alone (well-formed because both `x` and `a` are T4-valid), so both `E(x).1` and `E(a).1` are well-defined.

*Case-symmetry across Sub-cases 3a and 3b.* Sub-cases 3a and 3b share the hypothesis `x ≼ a` and discharge Steps 3.1 and 3.2 identically: those two steps quantify over the positional structure of `x` and `a` (their zero positions, their E-field offsets, their componentwise agreement under the prefix relation) without reference to which side is link versus content, so both steps deliver identical conclusions in both sub-cases. The two sub-cases diverge only at Step 3.3, where the subspace partition scaffolding clauses assign `E(·).1` based on domain membership — `E(·).1 = s_L` for link-side, `E(·).1 = s_C` for content-side. The two sub-cases therefore differ only in which side carries which subspace identifier; the `s_L ≠ s_C` disjointness is itself symmetric, so both sub-cases reach the same contradiction by the same final step. Steps 3.1 and 3.2 are written once and apply to both sub-cases; Step 3.3 is written out explicitly for each.

*Step 3.1 — Shared zero positions.* The prefix `x ≼ a` gives `#x ≤ #a` and componentwise agreement `aᵢ = xᵢ` for `1 ≤ i ≤ #x`. Let `x`'s three zero positions be `n_1 < n_2 < n_3` with `1 ≤ n_1` and `n_3 ≤ #x` (the three witnesses to `zeros(x) = 3`). By componentwise agreement at positions `n_1, n_2, n_3 ≤ #x`, `a` also has `aₙ₁ = aₙ₂ = aₙ₃ = 0`. Suppose, toward contradiction, that `a` has a fourth zero at some position `m ∈ {1, ..., #a} ∖ {n_1, n_2, n_3}`: if `m ≤ #x`, then `aₘ = 0` together with componentwise agreement forces `xₘ = 0`, adding a fourth zero to `x` and contradicting `zeros(x) = 3`; if `m > #x`, then `m` is a zero position in `a` outside `{n_1, n_2, n_3}` (which all lie at positions `≤ #x`), so `zeros(a) ≥ 4`, contradicting `zeros(a) = 3`. So `a`'s three zero positions are exactly `n_1 < n_2 < n_3`, the same as `x`'s. This step holds in both sub-cases because it consumes only the prefix relation `x ≼ a` and the shared-`zeros = 3` constraint, neither of which references domain membership.

*Step 3.2 — E-field first-position agreement.* The E-field of `x` is non-empty (we need only `#E(x) ≥ 1`, not the stronger `≥ 2` from L1b or its content-side analog, since Step 3.2's conclusion uses only the first position of `E(x)`): T4(iv) applied to `x` gives `x_{#x} ≠ 0`, while `x_{n_3} = 0`, so `n_3 ≠ #x`; combined with `n_3 ≤ #x` (since `n_3` is a position of `x`) this gives `n_3 < #x`, i.e., `#x − n_3 ≥ 1`. By T4b's E-field index range `n_3 + 1 .. #x` with length `#E(x) = #x − n_3`, `#E(x) ≥ 1`, so the first E-field position `E(x).1` is defined. The same E-field non-emptiness holds for `a` by the symmetric T4(iv) application at `a`. By T4b (UniqueParse, ASN-0034), with both `x` and `a` element-level and sharing the same three zero positions `n_1 < n_2 < n_3`, the E-field of `x` occupies positions `n_3 + 1 .. #x` and the E-field of `a` occupies positions `n_3 + 1 .. #a`; T4b's index offset gives `E(x).j = x_{n_3 + j}` for `1 ≤ j ≤ #E(x)` (and symmetric for `a`). The componentwise agreement `xᵢ = aᵢ` on `1 ≤ i ≤ #x` from `x ≼ a`, instantiated at `i = n_3 + 1` (which satisfies `n_3 + 1 ≤ #x` since `#E(x) ≥ 1`), yields `x_{n_3 + 1} = a_{n_3 + 1}`; substituting T4b's index offset on both sides (taking `j = 1`) gives `E(x).1 = E(a).1`. This step holds in both sub-cases because the T4-validity citations and T4b's E-field structure apply uniformly to element-level addresses without reference to subspace identifier. (Earlier drafts derived the full Prefix relation `E(x) ≼ E(a)` and then took its `j = 1` conjunct; the Prefix step was unnecessary bookkeeping — only componentwise agreement at a single position is consumed — and has been dropped in favor of the direct derivation above.)

*Step 3.3a — Subspace contradiction (Sub-case 3a: `x ∈ dom(Σ.L), a ∈ dom(Σ.C)`).* The link subspace partition scaffolding gives `E(x).1 = s_L` directly (`x ∈ dom(Σ.L)`); the content subspace partition scaffolding gives `E(a).1 = s_C` directly (`a ∈ dom(Σ.C)`); the *Content subspace partition* scaffolding clause fixes `s_L ≠ s_C`. But Step 3.2 gives `E(x).1 = E(a).1`. Substituting, `s_L = s_C`, contradicting the scaffolding's disjointness. Sub-case 3a vacuous.

*Step 3.3b — Subspace contradiction (Sub-case 3b: `x ∈ dom(Σ.C), a ∈ dom(Σ.L)`).* By the symmetric application of the scaffolding clauses: the content subspace partition scaffolding gives `E(x).1 = s_C` directly (`x ∈ dom(Σ.C)`); the link subspace partition scaffolding gives `E(a).1 = s_L` directly (`a ∈ dom(Σ.L)`); the *Content subspace partition* scaffolding clause again fixes `s_C ≠ s_L`. Step 3.2 gives `E(x).1 = E(a).1`, so substituting yields `s_C = s_L`, contradicting the scaffolding's disjointness (the disjointness predicate `s_C ≠ s_L` is symmetric, so the contradiction reads the same regardless of which side of the equality the link or content identifier appears on). Sub-case 3b vacuous.

Both sub-cases of Case 3 are vacuous. ∎

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

The shape registry admits only well-formed shapes. The cardinality side of each implication tests the *literal* registry value `0`, not the broader set `{0, 0|1}`: the values `0` and `0|1` are distinct entries in `{0, 1, *, 0|1}`, so the antecedent `c_F = 0` is false when `c_F = 0|1`. Similarly, `t_F = -` is the literal registry value `-`, distinct from `A_doc`, `A_rel`, and `A`.

*Behavior at `c_F = 0|1`.* Neither `c_F = 0` fires (since `0|1 ≠ 0`) nor `t_F = -` fires at a `c_F = 0|1` row: `t_F = -` is excluded at `c_F = 0|1` rows by the well-formedness implication `t_F = - ⟹ c_F = 0`, whose consequent fails (`0|1 ≠ 0`). Both implications on the F-side are vacuously satisfied; `t_F` may take any of `A_doc, A_rel, A`. Thus the Provenance shape `(1, 0|1, A, A, ⊤)` is well-formed: the G-side antecedents `c_G = 0` and `t_G = -` are both false (`0|1 ≠ 0` and `A ≠ -`), so both G-side implications are vacuously satisfied. When the slot is empty at emission time (the `0` branch of `0|1`), clause (d) of Sh-conf reads `∅ ⊆ A^Σ`, vacuously true; when the slot is non-empty (the `1` branch), clause (d) enforces `slot_addrs ⊆ A^Σ` normally. The same reading applies to any future shape carrying `c_X = 0|1` paired with a non-`-` target domain.

*Why the constraint matters.* Without these implications, two registry entries with operationally equivalent meaning — e.g., `(c_F = 0, t_F = A_doc)` and `(c_F = 0, t_F = -)`, both rendering clause (d) of Sh-conf vacuous on F since `slot_addrs(F) = ∅ ⊆ X` for any X — could disagree on the registered shape value. That disagreement would break the per-class constancy of `shape(·)` and the downstream catalog reasoning that case-splits on the registered shape tuple (e.g., the canonical shape catalog below indexes template families by shape; two operationally equivalent but syntactically distinct entries would index different rows).

**Definition — CardinalityMatch.** For `n ∈ ℕ` and `c ∈ {0, 1, *, 0|1}`:

`match(n, c) ≡ (c = 0 ∧ n = 0) ∨ (c = 1 ∧ n = 1) ∨ (c = * ∧ n ∈ ℕ) ∨ (c = 0|1 ∧ n ∈ {0, 1})`

**Definition — TypedRelationCatalog.** Fix a distinguished set `T_cat ⊆ T_admissible` *finite up to `~`* (equivalently, the quotient `T_cat / ~` is finite) that is *closed under coverage-equivalence* (ASN-0086, `~` definition): `K ∈ T_cat ∧ K ~ K' ⟹ K' ∈ T_cat`. Equivalently, `T_cat` is the union of finitely many `~`-equivalence classes; each class is itself infinite as an endset set (many endsets share the same coverage by L5, ASN-0043), but only finitely many classes appear in the catalog. Concretely, `T_cat` is specified by listing one representative per class, with closure under `~` implicit. "Finite distinguished set" in earlier drafts is misleading: a non-empty `~`-class has infinitely many endset members, so `T_cat` itself is not finite as a set of endsets — finiteness lives at the quotient level.

*Lifetime constancy of `T_cat`.* The set `T_cat` is fixed at the substrate's initial state `Σ_init` and does not change as states evolve: at every reachable state Σ, the registered catalog is the same set `T_cat` declared at `Σ_init`. The lifetime constancy is required for the inductive baselines of Sh0–Sh4 to discharge uniformly. Each induction begins with "At `Σ_0`, every `L_K^{Σ_0} = ∅`; the universal quantifier is vacuous." A K admitted to `T_cat` only after some prior states have elapsed would face a non-vacuous baseline at its registration point — `L_K^{Σ_registered}` could be non-empty from class-(iii) emissions at coverage-equivalent type indices issued before K joined `T_cat` — and the induction's base case would not discharge. The framework forbids runtime extension of `T_cat`: layers that wish to introduce new typed relations must declare them at `Σ_init`, or face the burden of verifying `L_K^{Σ_registered} = ∅` at the registration point (equivalent to the framework's empty-baseline assumption).

For any `K ∈ T_admissible \ T_cat` (equivalently, every member of every class not represented), no shape is registered. The substrate's shape-conformance gate rejects `Emit_K` at unregistered types — the literal membership test `K ∈ T_cat` (see Sh-conf below).

**Definition — ShapeRegistry.** A function

`shape : T_cat → Shape`

assigns each registered type its shape. Two properties:

- *Per-class constancy.* For `K, K' ∈ T_cat` with `K ~ K'`: `shape(K) = shape(K')`. The function `shape` factors through `T_cat / ~`.
- *Lifetime constancy.* `shape` is fixed across the substrate's lifetime; it does not change as states evolve.

Lifetime constancy is a substrate-level commitment, not derivable from R0…R7a. It is what lets Sh-conf evaluate emissions against a stable shape that matches the shape under which prior tuples of the same type were emitted, so the inductive proofs of Sh0–Sh3 can rely on a fixed conformance predicate. Mutable shape re-registration (e.g., relaxing a cardinality bound after some tuples are already emitted) would invalidate the induction; the framework forbids it.

**Definition — Conformance.** A tuple `(a, F, G) ∈ L_K^Σ` (with `K ∈ T_cat`) is *shape-conformant at state Σ* iff all of the following hold:

(a) `F` is in canonical-slot form; let `X_F = slot_addrs(F)`.
(b) `G` is in canonical-slot form; let `X_G = slot_addrs(G)`.
(c) `match(|X_F|, shape(K).c_F) ∧ match(|X_G|, shape(K).c_G)`.
(d) `X_F ⊆ shape(K).t_F^Σ ∧ X_G ⊆ shape(K).t_G^Σ`, with the symbolic `t` expanded per the Shape definition. When `t_F = -` (only legal under `c_F = 0`), the F-side of (d) is vacuously satisfied since `X_F = ∅`; symmetric for G.

Write `conf_K^Σ(F, G)` for this predicate.

*Structural gates.* Clauses (a) and (b) jointly form the **canonical-form gate** (one gate, two operands); clause (c) is the **cardinality gate**; clause (d) is the **target-domain gate**. Three independent gates, each rejecting independently. When the worked examples below refer to "Sh-conf's three independently-checked structural gates", they index the canonical-form, cardinality, and target-domain gates in that order; a non-canonical F (clause (a)) and a non-canonical G (clause (b)) are distinguishable as clause-level failures but both fall under the same gate.

*State-dependence and monotone discharge.* Conformance is state-indexed because clause (d) depends on the allocated sets `A_doc^Σ, A_rel^Σ, A^Σ`. These sets grow monotonically along `⊑̂`: `Σ ⊑̂ Σ'` entails `A^Σ ⊆ A^{Σ'}` and analogous for the partition sets (by L12a, ASN-0043, for `dom(Σ.L)` and by the content-store monotonicity scaffolding assumption (Scope and Substrate Scaffolding) for `dom(Σ.C)`). Therefore `conf_K^Σ(F, G) ⟹ conf_K^{Σ'}(F, G)` for every `Σ ⊑̂ Σ'`: once conformant, a tuple remains conformant under every reachable future state. This monotonicity is what permits the inductive arguments of Sh0–Sh3 to commute with arbitrary `↦*` transitions.


## The Conformance Axiom

**Sh-conf — ShapeConformanceAxiom.** The framework restricts ASN-0086's `Emit_K` (the relational-layer operation) by adding two preconditions: `K ∈ T_cat` and `conf_K^Σ(F, G)`. These are *added* to ASN-0086's existing preconditions; they do not displace them. The combined success condition is:

`Emit_K(Σ, d, F, G)` succeeds iff *ASN-0086's preconditions hold (specifically `d ∈ dom(Σ.M)`, with the regime simplification of `wp_086` below) and `K ∈ T_cat` and `conf_K^Σ(F, G)`*. Equivalently, the framework imposes two new conjuncts atop ASN-0086's `wp_086`: failure of either added conjunct, or failure of any ASN-0086 conjunct, produces `⊥`. The framework extends ASN-0086's `Emit_K` return type from `Σ' × A_rel^{Σ'}` to `(Σ' × A_rel^{Σ'}) ∪ {⊥}` where `⊥` is a distinguished rejection token: on any failure (substrate or framework), `Emit_K` returns `⊥` and leaves the state unchanged (no `↦`-step occurs). The layer-discipline contracts of Sh4 and FunctionalDependencyDiscipline below additionally return `⊥` on suppression (clause (ii) of their respective contracts); a caller that needs to distinguish rejection-by-Sh-conf from rejection-by-discipline-suppression may consult the discipline's pre-emission candidate-set computation before issuing the `Emit_K` call. The framework does not impose a finer-grained sum type at the substrate boundary; callers wanting that granularity wrap `Emit_K` with their own classification.

*Effective weakest-precondition under Sh-conf (preview).* ASN-0086 (`Emit_K`, WeakestPreconditionEmitK) defines

`wp_086(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ NoCraftedSpanReachesD(Σ, d) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`

with the last two conjuncts collapsing to `⊤` under the relational layer's committed operations (regime (i) of ASN-0086's wp simplification under the unit-depth retraction discipline). Within the shape framework, this regime (i) collapse is secured *by Retraction's shape itself*: Retraction's catalog entry `(*, 1, A, A_rel, ⊤)` together with Sh-conf clauses (a)/(b) (canonical-slot form) and clause (c) at `c_G = 1` (`|slot_addrs(G)| = 1`) forces every shape-conformant `Emit_R` emission's G-endset to a single unit-depth span `{(b, δ(1, #b))}` for some `b ∈ A_rel^Σ` — exactly ASN-0086's unit-depth retraction discipline. (The same point is elaborated under *Unit-depth retraction discipline secured by Retraction's shape* in the Retraction catalog row's walkthrough.) This paragraph is a *preview*: the formal collapse is established by Lemma — RetractionTargetNotOnChain (next subsection, which spells out the per-home and cross-home chain-element argument) and lifted to the named result by Corollary — EffectiveWpSimplification (immediately after that lemma's proof). Downstream proofs cite the Corollary, not this preview; readers may treat this paragraph as motivational on first pass and consult the Corollary for the canonical statement. The Corollary's named conclusion is

`wp_eff(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) = d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)`

The `⊥` rejection corresponds to wp failure on either source: a `K ∉ T_cat` failure (Sh-conf's first conjunct) blocks the wp at the registry boundary; a `¬conf_K^Σ(F, G)` failure (Sh-conf's second conjunct, decomposing into clauses (a)–(d)) blocks the wp at the shape gates; an ASN-0086 wp failure (e.g., `d ∉ dom(Σ.M)`) blocks the wp at the substrate boundary. Each source contributes its own rejection site; the layer's call site reaches the substrate primitive K.λ only when all conjuncts hold simultaneously.

*Scope.* Sh-conf binds `Emit_K`, not the substrate primitive K.λ. K.λ remains permissive at the substrate level: ASN-0086's R0 admits any `(F, G, K)` triple with `K ∈ T_admissible` at a fresh K.λ-emitted address. The framework's discipline is realized through the *Emit_K routing commitment* of Scope and Substrate Scaffolding: every class-(iii) emission of a type `K ∈ T_cat` routes through `Emit_K`, and Sh-conf rejects non-conformant `Emit_K` calls before they reach K.λ. The inductive proofs of Sh0–Sh3 invoke the *Emit_K routing commitment* to conclude that every new tuple in `L_K^{Σ'}` for `K ∈ T_cat` arrived via an `Emit_K` call subject to Sh-conf.

*Justification.* This is an axiom about the framework's layer-level enforcement, not a theorem derivable from R0…R7a. R0 (TupleAddressFreshness, ASN-0086) alone permits any `(F, G, K)` triple with `K ∈ T_admissible` to be emitted at a fresh address. Sh-conf narrows the admissible triples — those traveling through `Emit_K` — to those whose `F, G` are in canonical-slot form, whose slot-address cardinalities match the registered shape, and whose slot addresses land in the registered target domains.

Without Sh-conf, the cardinality and target-domain consequences (Sh0–Sh3 below) would not hold across state transitions — they would be vacuously true on an empty `L_K` and immediately false after the first non-conformant emission.

*Interaction with Nullify.* `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` (ASN-0086). The framework imposes a *baseline registration requirement*: the retraction type `R` (named by ASN-0086's Definition — RetractionType) is registered in `T_cat` with `shape(R) = (*, 1, A, A_rel, ⊤)` (the Retraction row of the canonical catalog below). This registration is a precondition of the framework's preservation theorems — without it, every `Nullify` call (and every other `Emit_R`) fails Sh-conf's first conjunct `K ∈ T_cat` and is rejected with `⊥`, leaving the substrate's retraction primitive uncallable through the relational layer. Since ASN-0086 commits the relational layer to routing every class-(iii) `R`-emission through `Emit_R` (via Nullify), R-registration is mandatory for any layer instantiating the framework. With R registered, Sh-conf admits every well-formed Nullify call:

- `F = ∅` is canonical-slot form with `X_F = ∅`; `match(0, *)` holds; `∅ ⊆ A^Σ` trivially.
- `G = {(a, δ(1, #a))}` is canonical-slot form with `X_G = {a}`; `match(1, 1)` holds; `{a} ⊆ A_rel^Σ` holds by Nullify's P1 precondition `a ∈ A_rel^Σ`.

The substrate's retraction primitive is shape-conformant by construction, with no special-case exemption needed at the framework's gates — but the baseline R-registration in `T_cat` is what makes the conformant call admissible at the registry boundary.

*Compatibility with ASN-0086's Nullify postcondition.* ASN-0086's `Emit_K` is typed `Σ × dom(Σ.M) × Endset × Endset → Σ' × A_rel^{Σ'}` with no `⊥`-case, and `Nullify`'s postcondition (single-tuple-scope nullification, R6a stability) assumes a `Σ'` is produced. The framework's return-type extension to `(Σ' × A_rel^{Σ'}) ∪ {⊥}` would, if Sh-conf rejected `R`-typed calls, leave ASN-0086's `Nullify` postcondition unmet at every Nullify call site. The baseline registration requirement closes this gap: under the mandatory R-registration, every well-formed `Nullify(Σ, d_retr, a)` call (i.e., one satisfying ASN-0086's P0/P1/P2 preconditions) is admitted by Sh-conf via the conformance checks just enumerated, so the call returns `(Σ', _) ∈ Σ' × A_rel^{Σ'}` and ASN-0086's `Nullify` postcondition is met by the framework's call site. The `⊥`-branch of the extended return type is unreachable on R-typed calls under baseline registration. Equivalently: *the framework's preservation theorems and ASN-0086's `Nullify` postcondition are jointly compatible exactly when R is registered in `T_cat`*. A substrate layer that declines to register R falls outside the framework's scope; its `Nullify` calls are uncallable through the relational layer, and the framework makes no claims about its reachable states. The framework's preservation theorems thus apply only to substrates where R is registered — equivalently, where every `Nullify` call is admitted by Sh-conf and returns a non-`⊥` value.

*Initial-state baseline for preservation proofs.* The inductive proofs of Sh0–Sh4 below presuppose an initial state `Σ_init` with `L_K^{Σ_init} = ∅` for every `K ∈ T_cat`. The base cases discharge against this baseline. References to `Σ_0` in the proofs below denote this `Σ_init`. States reached before the framework's *Emit_K routing commitment* was honored — e.g., substrate states from a prior process generation in which `Emit_K` did not exist, or any reachable state in which a class-(iii) emission of a type `K ∈ T_cat` bypassed `Emit_K` — are outside the framework's scope; the framework's preservation theorems make no claims about such states. A substrate that wants the framework's guarantees from a given starting point must verify `L_K^{Σ_init} = ∅` (or, equivalently, that every prior `L_K`-tuple satisfies `conf_K^{Σ_init}`) at that point.

**Lemma — RetractionTargetNotOnChain.** Let Σ be reachable from `Σ_init` under the framework's *Emit_K routing commitment*. For every `b ∈ dom(Σ.L)` and every `d ∈ dom(Σ.M)`:

`b ⋠ a_emit(Σ, d)`

*Generality.* The Lemma is stated about an *arbitrary* link-store address `b ∈ dom(Σ.L)`, not specifically about retraction-tuple slot addresses. This generalization is sound — the proof below uses only `b ∈ dom(Σ.L)` and `d ∈ dom(Σ.M)`, with no appeal to `b`'s membership in any particular slot of any particular relation — and it makes the Lemma directly applicable at both consumption sites in the EffectiveWpSimplification Corollary below: discharging `NoCraftedSpanReachesD(Σ, d)` (where `b` ranges over the slot addresses of *prior* R-tuples' G-endsets) and discharging the `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` disjunct under `K ~ R` (where `b` is the slot address of the *new* emission's G-endset under Sh-conf admittance). Both sites supply `b ∈ dom(Σ.L)` through Sh-conf clause (d) at `t_G = A_rel` of Retraction's catalog row.

*Proof.* Case-split on whether `b` and `a_emit(Σ, d)` share a home.

*Case I — `home(b) = d`.* Both `b` and `a_emit(Σ, d)` lie in `A_L(d)`'s chain enumeration: `b` by R0a-Cor1 (ContiguousPrefix, ASN-0086) applied to the homed set at `d` (so `b = inc^i(d.0.s_L.1, 0)` for some chain index `0 ≤ i ≤ J_d^Σ`); `a_emit(Σ, d)` by FreshEmissionAddress (ASN-0086) at chain index `J_d^Σ + 1` (whether first-emission or subsequent-emission branch fires, both branches deposit the next chain element). By the *Uniform link sub-allocator chain length* scaffolding clause (Scope and Substrate Scaffolding), `#b = #a_emit(Σ, d)`. By T10a.7 (EnumerationInjectivity, ASN-0034) applied to the chain at `A_L(d)`, distinct chain indices yield distinct tumblers; since `b`'s chain index `i ≤ J_d^Σ < J_d^Σ + 1 = a_emit(Σ, d)`'s chain index, `b ≠ a_emit(Σ, d)`. Two equal-length distinct tumblers are prefix-incomparable: if `b ≼ a_emit(Σ, d)`, then by Prefix (ASN-0034) the length clause `#b ≤ #a_emit(Σ, d)` combined with equal lengths forces componentwise agreement on all of `1..#b = 1..#a_emit(Σ, d)`, which by T3 (CanonicalRepresentation, ASN-0034) makes them identical — contradiction. So `b ⋠ a_emit(Σ, d)`.

*Case II — `home(b) ≠ d`.* Suppose toward contradiction `b ≼ a_emit(Σ, d)`. Then `a_emit(Σ, d) = b · w` for some suffix `w` (Prefix definition, ASN-0034). By L1 (LinkElementLevel, ASN-0043) applied to `b ∈ dom(Σ.L)`, `zeros(b) = 3`. The fresh emission address `a_emit(Σ, d)` has `zeros = 3` by construction: in the first-emission branch `a_emit(Σ, d) = [d.0.s_L.1]` has two zeros from `zeros(d) = 2` (by the *Document address structure* scaffolding clause, Scope and Substrate Scaffolding), one zero from the separator at position `#d + 1`, zero zeros from `s_L` at position `#d + 2` (since `s_L > 0` by the *Link subspace partition* scaffolding clause's positivity commitment), and zero zeros from the trailing `1` — total 3; in the subsequent-emission branch `a_emit(Σ, d) = inc(ℓ_prev, 0)` preserves `zeros` (TA5(c) with `k = 0`, ASN-0034: the step modifies only position `sig(ℓ_prev)`, and on T4-valid `ℓ_prev` — T4-validity supplied by L1c via T10a.4 on the link side — that position carries a non-zero value whose incremented value remains non-zero, so neither the modified position nor any other contributes a new zero) from `zeros(ℓ_prev) = 3` (by L1 applied to `ℓ_prev ∈ dom(Σ.L)`). *Zero-count additivity over prefix decomposition.* From `a_emit(Σ, d) = b · w` and Prefix (ASN-0034), `(a_emit(Σ, d))ᵢ = bᵢ` for `1 ≤ i ≤ #b` and `(a_emit(Σ, d))ᵢ = w_{i − #b}` for `#b < i ≤ #b + #w = #a_emit(Σ, d)` (by definition of the prefix-suffix decomposition `·`). Hence the zero-index set partitions: `{i : 1 ≤ i ≤ #a_emit(Σ, d) ∧ (a_emit(Σ, d))ᵢ = 0} = {i : 1 ≤ i ≤ #b ∧ bᵢ = 0} ⊔ {i : #b < i ≤ #a_emit(Σ, d) ∧ w_{i − #b} = 0}`. The disjoint-union cardinality (NAT-card, NatFiniteSetCardinality, ASN-0034) gives `zeros(a_emit(Σ, d)) = zeros(b) + zeros(w)`; rearranging, `zeros(w) = zeros(a_emit(Σ, d)) − zeros(b) = 3 − 3 = 0`. By L1a (LinkScopedAllocation, ASN-0043), `home(b)` is determined by `b`'s three-zero prefix structure — specifically, `home(b) = N(b).0.U(b).0.D(b)` reads off the field projections of `b`'s zero positions. Since `a_emit(Σ, d)` shares its first `#b` components with `b` (Prefix definition gives this directly) and `w` contributes no additional zeros, `a_emit(Σ, d)`'s three zero positions lie within positions `1..#b`, agreeing pointwise with `b`'s three zero positions. Hence `N(a_emit(Σ, d)) = N(b)`, `U(a_emit(Σ, d)) = U(b)`, `D(a_emit(Σ, d)) = D(b)`, so `home(a_emit(Σ, d)) = home(b)`. But `a_emit(Σ, d)`'s home is `d` by construction (first-emission deposits at `[d.0.s_L.1]` whose home is `d`; subsequent-emission inherits home from the parent chain at `d`). So `d = home(b)`, contradicting `home(b) ≠ d`. So `b ⋠ a_emit(Σ, d)`.

Either case yields `b ⋠ a_emit(Σ, d)`. ∎

The Lemma's one-directional reading — it asks `b ⋠ a_emit(Σ, d)`, not the converse `a_emit(Σ, d) ⋠ b` — matches what both consumers in the EffectiveWpSimplification Corollary need: each consumer's coverage set has the form `{t : b ≼ t}` (PrefixSpanCoverage, ASN-0043), and the question is whether `a_emit(Σ, d)` lies in it. The converse direction `a_emit(Σ, d) ≼ b` is not asked about by any wp_086 conjunct.

**Corollary — EffectiveWpSimplification.** Let Σ be reachable from `Σ_init` under the framework's *Emit_K routing commitment*. For every `K ∈ T_admissible`, every `d ∈ dom(Σ.M)`, and every `F, G ∈ Endset`, ASN-0086's `wp_086` for `Emit_K(Σ, d, F, G)` simplifies to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`, and the *effective wp* under Sh-conf simplifies to

`wp_eff(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) = d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)`

*Proof.* `wp_086` carries two non-trivial conjuncts beyond `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`: `NoCraftedSpanReachesD(Σ, d)` and `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`. We discharge each via Lemma — RetractionTargetNotOnChain (just proved) applied at the appropriate `b ∈ dom(Σ.L)`.

*Step 1 — Discharge of `NoCraftedSpanReachesD(Σ, d)`.* For every prior R-tuple `(b̂, F', G') ∈ L_R^Σ`, Sh-conf admission at past emission forces (clauses (a)/(b)) `G'` canonical-slot, (clause (c) at `c_G = 1` of Retraction's catalog row) `|slot_addrs(G')| = 1`, and (clause (d) at `t_G = A_rel`) `slot_addrs(G') ⊆ A_rel^Σ = dom(Σ.L)`. So `G' = {(b', δ(1, #b'))}` for a unique `b' ∈ dom(Σ.L)`. By PrefixSpanCoverage (ASN-0043), `coverage(G') = {t : b' ≼ t}`. Applying the Lemma at `b := b'` (legal because `b' ∈ dom(Σ.L)`) gives `b' ⋠ a_emit(Σ, d)`, so `a_emit(Σ, d) ∉ coverage(G')`. Quantifying over `(b̂, F', G') ∈ L_R^Σ` discharges `NoCraftedSpanReachesD(Σ, d)` per ASN-0086's Definition.

*Step 2 — Discharge of `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`.* Case-split on K's `~`-class.

- *Case A: `K ≁ R`.* The disjunct's first arm holds directly. The second arm need not be considered.
- *Case B: `K ~ R`.* The first arm of the disjunct is false; the second arm must be discharged. For the call to reach K.λ at all, Sh-conf must admit it. With K's shape inherited from R's catalog row via per-class constancy of `shape(·)` (`K ~ R ⟹ shape(K) = shape(R) = (*, 1, A, A_rel, ⊤)`), Sh-conf clauses (a)/(b) force the call's G canonical-slot, clause (c) at `c_G = 1` forces `|slot_addrs(G)| = 1`, and clause (d) at `t_G = A_rel` forces `slot_addrs(G) ⊆ A_rel^Σ = dom(Σ.L)`. So `G = {(b, δ(1, #b))}` for a unique `b ∈ dom(Σ.L)`. Applying the Lemma at this *new-emission* `b` (legal because `b ∈ dom(Σ.L)`, supplied independently of any prior R-tuple — this is the case the Lemma's generalization makes directly applicable) gives `b ⋠ a_emit(Σ, d)`, hence by PrefixSpanCoverage `a_emit(Σ, d) ∉ {t : b ≼ t} = coverage(G)`. The disjunct's second arm holds.

Both Cases A and B discharge the disjunct, completing Step 2. (If Sh-conf would reject the call — e.g., because G is non-canonical or its slot addresses are not in `A_rel^Σ` — then the call returns `⊥` and never reaches K.λ, so wp_086 is moot at that call site; Step 2's discharge is consumed only at call sites that reach K.λ, which by the *Emit_K routing commitment* are exactly the Sh-conf-admitted ones.)

With both `wp_086`-conjuncts discharged, `wp_086` reduces to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`. Sh-conf adds the conjuncts `K ∈ T_cat ∧ conf_K^Σ(F, G)`; since `T_cat ⊆ T_admissible`, `K ∈ T_cat` absorbs `K ∈ T_admissible`, yielding the named `wp_eff`. ∎

Downstream proofs that need to reason about `Emit_K`'s preconditions cite this Corollary directly rather than re-deriving the simplification.


## Cardinality (Sh0, Sh1)

**Sh0 — FromSlotCanonicalAndCardinalityFixed.** For each `K ∈ T_cat`, every tuple in `L_K^Σ` at every reachable state Σ has `F` in canonical-slot form with `|slot_addrs(F)|` matching `c_F`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: F is canonical-slot form ∧ match(|slot_addrs(F)|, shape(K).c_F))`

*Proof.* By induction on the broad transition relation `↦*` from the initial state `Σ_0`. Reachable states are reached under `↦*` (the broader relation including arrangement-modifying steps), not just `→*`, so the induction must cover both transition classes.

*Base case.* At `Σ_0 = Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Sh-conf section above), every `L_K^{Σ_0} = ∅`; the universal quantifier is vacuous.

*Inductive step.* Suppose the property holds at Σ; let `Σ ↦ Σ'` be a single broad transition. We fix a particular `K ∈ T_cat`. `L_K` is monotone non-decreasing along `↦*` — strictly increasing under `→`-steps by R3 (TypedSliceMonotonicity, ASN-0086), equal under `↦ \ →`-steps by LinkStoreInvarianceUnderArrangement (ASN-0086); `L_K` never contracts. The only effects on `L_K` are unchanged (Case A) or extended by one tuple (Case B). The contraction cases that appear in Sh4 over `A_K` (which filters `L_K` by `nullified(·)` membership) do not arise here because Sh0's universal ranges over `L_K`, not `A_K`. We split on whether the step affects `L_K`.

*Case A: `L_K^{Σ'} = L_K^Σ`.* The relation `L_K` is unchanged. The property is inherited tuple-by-tuple from the IH; existing tuples retain their values by R2 (TupleAddressPermanence, ASN-0086). This case covers all K.σ-steps and K.α-steps (which preserve `Σ.L` pointwise, hence `L_K` for every K, including this K); all K.λ-steps emitting a tuple of type `K'` not coverage-equivalent to K (since `L_K` slices only addresses whose stored type satisfies `coverage(e₃) = coverage(K)`); and all arrangement-modifying steps in `↦ \ →` (by LinkStoreInvarianceUnderArrangement, ASN-0086).

*Case B: `L_K^{Σ'} = L_K^Σ ∪ {τ_new}` for a single new tuple.* By the *Emit_K routing commitment* (Scope and Substrate Scaffolding), this is a K.λ-step originating as an `Emit_K` call at type K (or a K'-typed call with `K ~ K'`; by T_cat's `~`-closure, `K' ∈ T_cat`, and `Emit_{K'}` consults `shape(K') = shape(K)` by `~`-constancy). Sh-conf admitted that call only because `conf_K^Σ(F, G)` held — i.e., `F` is canonical-slot form and `match(|slot_addrs(F)|, c_F)`. The new tuple satisfies the property; existing tuples retain their values by R2 and their conformance by the IH.

Both cases preserve the property at the chosen K; quantifying over K closes the induction. ∎

**Sh1 — ToSlotCanonicalAndCardinalityFixed.** The G-side analog of Sh0:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: G is canonical-slot form ∧ match(|slot_addrs(G)|, shape(K).c_G))`

*Proof.* By induction on `↦*` from `Σ_0`. Reachable states are reached under `↦*`, so the induction must cover both `→`-steps and arrangement-modifying steps in `↦ \ →`. Fix `K ∈ T_cat`.

*Base case.* At `Σ_0 = Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Sh-conf section above), `L_K^{Σ_0} = ∅`; the universal quantifier is vacuous.

*Inductive step.* Suppose the property holds at Σ; let `Σ ↦ Σ'` be a single broad transition. `L_K` is monotone non-decreasing along `↦*` — strictly increasing under `→`-steps by R3 (TypedSliceMonotonicity, ASN-0086), equal under `↦ \ →`-steps by LinkStoreInvarianceUnderArrangement (ASN-0086) — so the only effects on `L_K` are Case A (unchanged) or Case B (one new tuple). Split on whether the step affects `L_K`.

*Case A* (`L_K^{Σ'} = L_K^Σ`). The relation is unchanged; existing tuples retain their values by R2 (TupleAddressPermanence, ASN-0086), and the property is inherited tuple-by-tuple from the IH. This case covers the same step classes enumerated under Sh0's Case A: K.σ-steps and K.α-steps (which preserve `Σ.L` pointwise); K.λ-steps emitting a tuple of type `K'` not coverage-equivalent to K (since `L_K` slices only addresses whose stored type satisfies `coverage(e₃) = coverage(K)`); and arrangement-modifying steps in `↦ \ →` (by LinkStoreInvarianceUnderArrangement, ASN-0086).

*Case B* (`L_K^{Σ'} = L_K^Σ ∪ {τ_new}` for a single new tuple). By the *Emit_K routing commitment* (Scope and Substrate Scaffolding), this is a K.λ-step originating as an `Emit_K` call at type K (or a `~`-equivalent type `K'`; by T_cat's `~`-closure, `K' ∈ T_cat`, and `shape(K') = shape(K)` by per-class constancy). Sh-conf admitted that call only because `conf_K^Σ(F, G)` held — in particular, by Sh-conf's *clause (b)*, `G` is in canonical-slot form, and by *clause (c)*, `match(|slot_addrs(G)|, shape(K).c_G)`. So τ_new satisfies the G-side property: the first conjunct of Sh1's body is discharged by clause (b); the second conjunct by clause (c). Existing tuples retain their values by R2 and their G-side conformance by the IH.

Both cases preserve the property at the chosen K; quantifying over K closes the induction. ∎

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

*Proof.* By induction on `↦*` from `Σ_0`. Fix `K ∈ T_cat`. `L_K` is monotone non-decreasing along `↦*` — strictly increasing under `→`-steps by R3 (TypedSliceMonotonicity, ASN-0086), equal under `↦ \ →`-steps by LinkStoreInvarianceUnderArrangement (ASN-0086) — so the inductive step splits on whether the transition leaves `L_K` unchanged (Case A) or extends it by one tuple (Case B); no contraction case for `L_K` arises.

*Base case.* At `Σ_0 = Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Sh-conf section above), `L_K^{Σ_0} = ∅` vacuously.

*Inductive step.*

*Case A: `L_K^{Σ'} = L_K^Σ`.* `L_K` is unchanged. The property is inherited on every existing tuple, with monotone preservation `X_F ⊆ t_F^Σ ⟹ X_F ⊆ t_F^{Σ'}` because `t_F^Σ ⊆ t_F^{Σ'}` (allocated-set monotonicity: link-side from L12a ASN-0043, content-side from the scaffolding assumption; arrangement steps preserve `dom(Σ.C)` and `dom(Σ.L)` so the inclusion is equality there). This case covers K.σ-steps, K.α-steps, K.λ-steps for non-K-coverage-equivalent types, and arrangement-modifying steps in `↦ \ →` (via LinkStoreInvarianceUnderArrangement).

*Case B: `L_K^{Σ'} = L_K^Σ ∪ {τ_new}`.* By the *Emit_K routing commitment*, the K.λ-step originates as an `Emit_K`-class call (at K or a `~`-equivalent type by T_cat's `~`-closure) subject to Sh-conf; the new tuple satisfies `X_F ⊆ t_F^Σ` by Sh-conf at emission, hence `X_F ⊆ t_F^{Σ'}` by monotonicity. Existing tuples retain their values by R2 and their target-domain conformance by the IH plus monotonicity. ∎

**Sh3 — ToSlotTargetRestricted.** Symmetric for `G`:

`(A K ∈ T_cat, (a, F, G) ∈ L_K^Σ :: slot_addrs(G) ⊆ shape(K).t_G^Σ)`

*Proof.* By induction on `↦*` from `Σ_0`. Fix `K ∈ T_cat`. `L_K` is monotone non-decreasing along `↦*` — strictly increasing under `→`-steps by R3 (TypedSliceMonotonicity, ASN-0086), equal under `↦ \ →`-steps by LinkStoreInvarianceUnderArrangement (ASN-0086) — so the inductive step splits on whether the transition leaves `L_K` unchanged (Case A) or extends it by one tuple (Case B); no contraction case for `L_K` arises. The structure mirrors Sh2 with the substitution F → G throughout — clauses (b) and (c) of Sh-conf cited where Sh2 cites (a) and (c), and `t_G` substituted for `t_F`.

*Base case.* At `Σ_0 = Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Sh-conf section above), `L_K^{Σ_0} = ∅` vacuously.

*Inductive step.*

*Case A: `L_K^{Σ'} = L_K^Σ`.* `L_K` is unchanged. The property is inherited on every existing tuple, with monotone preservation `X_G ⊆ t_G^Σ ⟹ X_G ⊆ t_G^{Σ'}` because `t_G^Σ ⊆ t_G^{Σ'}` (allocated-set monotonicity: link-side from L12a ASN-0043, content-side from the scaffolding assumption; arrangement steps preserve `dom(Σ.C)` and `dom(Σ.L)` so the inclusion is equality there). This case covers K.σ-steps, K.α-steps, K.λ-steps for non-K-coverage-equivalent types, and arrangement-modifying steps in `↦ \ →` (via LinkStoreInvarianceUnderArrangement).

*Case B: `L_K^{Σ'} = L_K^Σ ∪ {τ_new}`.* By the *Emit_K routing commitment*, the K.λ-step originates as an `Emit_K`-class call (at K or a `~`-equivalent type by T_cat's `~`-closure) subject to Sh-conf. Sh-conf admitted that call only because `conf_K^Σ(F, G)` held — in particular, by Sh-conf clause (b), `G` is in canonical-slot form (so `slot_addrs(G) = X_G` is well-defined), and by Sh-conf clause (d) on the G-side, `X_G ⊆ t_G^Σ` at emission, hence `X_G ⊆ t_G^{Σ'}` by monotonicity. Existing tuples retain their values by R2 and their target-domain conformance by the IH plus monotonicity. ∎

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

`from₁⁻ : L_K^Σ → shape(K).t_F^Σ ∪ {⊥}` defined when `c_F ∈ {1, 0|1}`; returns `⊥` iff `|slot_addrs(F)| = 0`, and returns the unique element of `slot_addrs(F)` otherwise.

`to₁⁻ : L_K^Σ → shape(K).t_G^Σ ∪ {⊥}` defined analogously when `c_G ∈ {1, 0|1}`; returns `⊥` iff `|slot_addrs(G)| = 0`, and returns the unique element of `slot_addrs(G)` otherwise.

*Codomain convention for partial templates.* Every partial-valued template introduced in this framework declares its codomain as `(typed allocated set) ∪ {⊥}` where `⊥` is the distinguished partiality token. Concretely: `from₁⁻` lands in `t_F^Σ ∪ {⊥}`; `to₁⁻` lands in `t_G^Σ ∪ {⊥}`; `K_target_of` (DirectedPair under FDD) lands in `A_doc^Σ ∪ {⊥}`; `latest_K_for_addr` (NonIdempotentDirectedPair under SHCD) lands in `A_K^Σ ∪ {⊥}` (returning a tuple rather than an address, the tuple-valued analog). The pattern is uniform: every template whose body's "unique element" or "argmax" step can fail to produce a value declares the failure value as `⊥` and the success value's domain explicitly.

**Lemma — SlotAccessorTotality.** When `shape(K).c_F = 1`, `from₁` is a total function on `L_K^Σ`. Similarly for `to₁` when `c_G = 1`.

*Proof.* By Sh0, every `τ ∈ L_K^Σ` has `F` in canonical-slot form with `|slot_addrs(F)| = 1` (since `match(n, 1) ⟺ n = 1`). A finite set of cardinality 1 has a unique element. Define `from₁(τ)` as that element. By Sh2, this element lies in `t_F^Σ`. ∎

For the rest of this document, we drop subscripts and write `from`, `to` when the shape unambiguously fixes which accessor is meant. We additionally use `addr(τ) = a` for the tuple address (R1, AddressInjectivity, ASN-0086).


## Idempotency (Sh4)

**Sh4 — IdempotencyDiscipline.** When `shape(K).idem = ⊤`, a layer above the substrate enforces at most one *active* tuple in `L_K` with any given slot-address pair. For `τ = (a, F, G) ∈ L_K^Σ` we write `F_τ := F` and `G_τ := G` for the slot endsets of τ. Then:

`(A τ, τ' ∈ A_K^Σ : (slot_addrs(F_τ), slot_addrs(G_τ)) = (slot_addrs(F_{τ'}), slot_addrs(G_{τ'})) :: addr(τ) = addr(τ'))`

*Universal scope.* The two bound variables `τ` and `τ'` range independently over `A_K^Σ`, including the diagonal `τ = τ'`. On the diagonal the conclusion `addr(τ) = addr(τ')` reads `addr(τ) = addr(τ)`, satisfied by reflexivity of equality, so the diagonal contributes no constraint. The substantive content is off-diagonal: for any two *distinct* active tuples `τ, τ'` whose slot-address pairs match, Sh4 forces `addr(τ) = addr(τ')` — combined with R1 (AddressInjectivity, ASN-0086), the equality of addresses then collapses `τ = τ'`, contradicting the off-diagonal assumption. Read contrapositively: no two distinct active tuples in `A_K^Σ` share a slot-address pair. Subsequent appeals to "pairwise distinctness on `A_K^Σ`" mean exactly this off-diagonal content; the diagonal is dispatched once and for all by reflexivity.

*Sh4 idempotency contract (the layer-discipline contract for Sh4).* Sh4 is realized through a contract the calling layer commits to honor uniformly across every reachable state — the *Sh4 idempotency contract*, distinct from the *Emit_K routing commitment* of Scope and Substrate Scaffolding (which routes calls through `Emit_K`) and from the *FDD functional-dependency contract* (defined under FunctionalDependencyDiscipline below). Subsequent text uses *Sh4 idempotency contract* to disambiguate when more than one commitment is in scope. For each `K ∈ T_cat` with `shape(K).idem = ⊤`, on every `Emit_K(Σ, d, F, G)` call site the layer enforces the following protocol:

*Ordering with Sh-conf.* Sh-conf's canonical-form gate (clauses (a) and (b)) executes *before* the Sh4 contract clauses (i)–(iii) at every call site. If `F` or `G` is non-canonical, Sh-conf clauses (a)/(b) reject the emission and `Emit_K` returns `⊥` without the Sh4 contract evaluating; in that case `slot_addrs(F)` and `slot_addrs(G)` are never read by the contract. Equivalently, the contract presupposes canonical-form `F, G` as a precondition discharged by Sh-conf's prior gate. The remaining Sh-conf gates (cardinality clause (c) and target-domain clause (d)) execute after the Sh4 contract: if the contract suppresses (clause (ii)), `Emit_K` returns `⊥` and the Sh-conf cardinality/target-domain gates are never reached; if the contract issues (clause (iii)), Sh-conf's cardinality/target-domain gates fire as the next rejection sites. This ordering — canonical-form gate first, Sh4 contract second, cardinality/target-domain gates third — is what makes every step of the contract well-defined.

(i) Before issuing the emission, the layer computes the candidate set
`C(F, G, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)}`
via the two-step procedure:

&nbsp;&nbsp;(i.a) Query `Observe_K(slot_addrs(F), slot_addrs(G), oper)` — a well-typed call by the ordering above: Sh-conf clauses (a)/(b) have already gated canonical-form, so `slot_addrs(F)` and `slot_addrs(G)` are finite subsets of `T` at this point in the protocol. Observe_K's semantics returns the (finite) set of active tuples whose slot coverages prefix-contain the pattern addresses — concretely, `{τ ∈ A_K^Σ : slot_addrs(F) ⊆ coverage(F_τ) ∧ slot_addrs(G) ⊆ coverage(G_τ)}`. Under Sh0/Sh1, every `τ ∈ A_K^Σ` has canonical-form slot endsets, so `coverage(F_τ) = ⋃ {{t : y ≼ t} : y ∈ slot_addrs(F_τ)}` and `slot_addrs(F) ⊆ coverage(F_τ)` iff every `x ∈ slot_addrs(F)` has some `y ∈ slot_addrs(F_τ)` with `y ≼ x`. *Per-element argument.* Fix any `x ∈ slot_addrs(F)`. By Sh-conf clause (d), `x ∈ t_F^Σ ⊆ A^Σ`, so `x` is allocated. The pattern-containment hypothesis supplies some `y ∈ slot_addrs(F_τ)` with `y ≼ x`. By Sh2 applied to `τ`, `y ∈ t_F^Σ ⊆ A^Σ`, so `y` is allocated. By AllocatedAddressAntichain at the witness `y` (using `x ∈ A^Σ` and `y ≼ x`), `y = x`. So every `x ∈ slot_addrs(F)` is itself an element of `slot_addrs(F_τ)`; quantifying over `x` gives `slot_addrs(F) ⊆ slot_addrs(F_τ)`. *Multi-slot generalization.* The same per-element argument applies independently to each `x ∈ slot_addrs(F)` regardless of `|slot_addrs(F)|` — including `c_F = *` shapes with `n ≥ 2`, where the argument fires `n` times to yield set-containment from per-element containment. Symmetric argument with G in place of F yields `slot_addrs(G) ⊆ slot_addrs(G_τ)`. So the Observe over-approximates exact slot-set equality by `slot_addrs(F_τ) ⊇ slot_addrs(F)` and `slot_addrs(G_τ) ⊇ slot_addrs(G)`, and may include τ with strictly larger slot-address sets.

&nbsp;&nbsp;(i.b) Post-filter the result of (i.a): retain only τ with `slot_addrs(F_τ) = slot_addrs(F)` and `slot_addrs(G_τ) = slot_addrs(G)`. Each returned τ has canonical-slot form by Sh0/Sh1, so `slot_addrs(F_τ)` is a well-defined finite set; exact-equality checks against the finite pattern slot-address sets are decidable in finite time. The composition (i.a) ∘ (i.b) yields exactly `C(F, G, Σ)` as specified above.

(ii) If `C(F, G, Σ) ≠ ∅`, the emission is *suppressed*: no `→`-step occurs.

(iii) Only if `C(F, G, Σ) = ∅` does the layer issue `Emit_K(Σ, d, F, G)`.

The layer commits to executing clauses (i)–(iii) atomically with respect to other emitters and retractors at the same `~`-equivalence class of K — emission and retraction events at any K' with `K' ~ K` that could split (i)'s observation from (iii)'s emission must be serialized by the layer. `L_K` is `~`-class indexed (ASN-0086, `L_K^Σ = L_{K'}^Σ` whenever `K ~ K'`), so emitters at distinct-but-`~`-equivalent type indices write to the same active subset; atomicity scoped at the `~`-class is what closes the race.

*Scope: single-process substrate.* The framework's scope is restricted to single-process substrates, in which `↦`-transitions are sequential by construction — between any two transitions there is a well-defined "before" and "after" state and no third transition interleaves. Under this scope, "atomicity of clauses (i)–(iii)" reduces operationally to "within a single `Emit_K` call site, clauses (i.a), (i.b), and (iii) execute in sequence without intervening `↦`-steps from any other source." A layer satisfies this by issuing the `Observe_K` call of (i.a), the post-filter of (i.b), and (if `C = ∅`) the substrate K.λ-step of (iii) as a single uninterrupted procedure call. The "concurrent emitter or retractor" wording above refers to this within-call sequencing requirement: no other Sh4-emitter at a `~`-equivalent K may interleave a `↦`-step between (i) and (iii) of an in-progress call. Multi-process substrates — where two emitter processes might race to compute `C(F, G, Σ)` against the same state — would require a coordination protocol beyond the within-call sequentiality this framework assumes; the Open Questions section flags cross-process consistency as not addressed.

*Cross-`~`-class concurrency is benign.* Concurrent `Emit_R` retracting K-tuples while `Emit_K` is in flight (with `R ≁ K`) does not require serialization. The only mutation an `Emit_R` step applies to `A_K` is removal (a K-tuple is filtered out by `nullified(Σ)` membership); removing a tuple from `A_K` cannot violate the pairwise-slot-pair-distinctness condition, only restore it (a removed tuple is no longer a candidate witness for any pair-violation). The Sh4 atomicity scope is therefore correctly tightened to the `~`-equivalence class of K and not widened to all retractors. When `R ~ K` (K is itself the retraction relation), retraction and emission write to the same `A_K = A_R`, and the layer's atomicity at the `~`-class scope already handles the race — this is the Case D analyzed below.

*Preservation under the contract.* Sh4 holds at every reachable state under the contract, by induction on `↦*`. Fix `K ∈ T_cat` with `shape(K).idem = ⊤`.

*Stratification.* Sh4's preservation argument consumes Sh0–Sh3 (and their consumed accessor totalities, e.g., SlotAccessorTotality) as previously-established lemmas evaluated at the current state Σ — for instance, the contract specification's per-element argument in clause (i.a) cites Sh2 to land witnesses `y` in `A^Σ`. Sh0–Sh3 are each proved by their own independent inductions over `↦*` above, against the same empty-baseline `Σ_init`; they are not part of Sh4's inductive hypothesis. The stratification is: Sh0–Sh3 first (each independently induct), then Sh4 (induct using Sh0–Sh3 as state-indexed lemmas). No cycle: Sh4 never appears as a premise of Sh0–Sh3's proofs.

*Base.* At `Σ_0 = Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Sh-conf section above), `L_K^{Σ_0} = A_K^{Σ_0} = ∅`; Sh4's universal is vacuous.

*Step (Case A: `A_K^{Σ'} = A_K^Σ`).* The active subset is unchanged at K. Sh4 is inherited directly. The case is *defined* by the equation `A_K^{Σ'} = A_K^Σ`, which the IH discharges without enumerating which transition classes achieve it; Case A's preservation is closed at the case-equation. The enumeration of principal transitions is retained as expository orientation only, not as a load-bearing case analysis: all K.σ-steps, K.α-steps, K.λ-steps emitting a tuple of any type `K'` with `K' ≁ K` and `K' ≁ R` (so `L_K` and `nullified` are both untouched at K), and all arrangement-modifying steps in `↦ \ →` (by LinkStoreInvarianceUnderArrangement, `Σ'.L = Σ.L` pointwise hence `L_K^{Σ'} = L_K^Σ`, `L_R^{Σ'} = L_R^Σ`, and `nullified(Σ') = nullified(Σ)`) all satisfy the case-equation by direct inspection of the substrate transition vocabulary. Residual scenarios — transitions falling under the case-equation but outside the principal enumeration above — are *not separately analyzed*: the IH plus the case-equation `A_K^{Σ'} = A_K^Σ` suffice to discharge Sh4 at Case A regardless of how the transition arose. The case-equation is the formal closure; the principal-transitions enumeration is an aid to the reader, not a proof obligation.

*Step (Case B: `A_K^{Σ'} = A_K^Σ ∪ {τ_new}`, a K.λ-step at type K with no concurrent nullification of any τ ∈ A_K^Σ).* By the *Emit_K routing commitment*, this K.λ-step originates as an `Emit_K` call (with K or `~`-equivalent registered type). By the *Sh4 idempotency contract* clause (iii), the emission proceeded only because `C(F, G, Σ) = ∅`. Let `τ_new` be the new tuple. Suppose, toward contradiction, that some prior `τ ∈ A_K^Σ` satisfies `(slot_addrs(F_τ), slot_addrs(G_τ)) = (slot_addrs(F_{τ_new}), slot_addrs(G_{τ_new}))`. Then by definition `τ ∈ C(F, G, Σ)`, contradicting `C(F, G, Σ) = ∅`. So no such `τ` exists, and `A_K^{Σ'}` extends with a slot-pair-unique element. The pairwise condition is preserved: existing pairs were Sh4-distinct by IH; `τ_new` shares no slot-pair with any prior active tuple.

*Step (Case C: `A_K^{Σ'} ⊆ A_K^Σ` strictly, an `Emit_R`-step nullifying one or more K-tuple addresses without adding to A_K).* Retraction filters `A_K^Σ` by `nullified(Σ)` membership but cannot introduce new K-tuples; the pairwise condition is preserved on any subset. This case fires when `K ≁ R` (so the Emit_R step's `τ_new` does not join `A_K`) or when `K ~ R` but `τ_new` is itself nullified by the same step (self-retraction).

*Step (Case D: K is `~`-equivalent to R, an `Emit_R`-step that both adds τ_new to A_R and nullifies one or more prior R-tuple addresses).* This is the simultaneous-effect case for the retraction relation: τ_new joins `A_R^{Σ'}` and a non-empty subset `leaving := {τ ∈ A_R^Σ : addr(τ) ∈ coverage(G_{τ_new})}` exits. The resulting active subset is `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving`, which is neither pure addition (Case B) nor pure contraction (Case C) nor unchanged (Case A).

First, by Case B's argument: the *Sh4 idempotency contract* clause (iii) confirmed `C(F_{τ_new}, G_{τ_new}, Σ) = ∅` against the full `A_R^Σ` (the two-step procedure (i.a) + (i.b) runs over `A_R^Σ` before the step fires, not over any post-step subset). So τ_new is slot-pair-distinct from every prior τ ∈ A_R^Σ, including the τ ∈ leaving that will subsequently exit via nullification. Pairwise distinctness on `A_R^Σ ∪ {τ_new}` is established by the IH (which gives pairwise distinctness on A_R^Σ) together with τ_new's slot-pair distinctness from every member of A_R^Σ (the IH is the *off-diagonal* content of Sh4's universal — see the *Universal scope* clarification above — and τ_new's diagonal `(τ_new, τ_new)` case is trivially satisfied by reflexivity of `addr(τ_new) = addr(τ_new)`). Second, `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving` is a subset of the pairwise-distinct set `A_R^Σ ∪ {τ_new}`. Any subset of a pairwise-distinct set is pairwise-distinct (the universal quantifier ranges over fewer pairs but the predicate is unchanged). Sh4 holds on `A_R^{Σ'}`.

The induction closes. ∎

*Status.* Sh4 is a *theorem under the Sh4 idempotency contract*, not a substrate-enforced axiom. The substrate as defined by ASN-0086 does not enforce Sh4 directly: R0 (TupleAddressFreshness) explicitly permits two emissions with identical `(F, G)` to produce two distinct tuples; R1 (AddressInjectivity) keeps them distinguishable. Without the *Sh4 idempotency contract*, the substrate would admit such emissions and Sh4 would fail. The framework's Sh4 conclusion depends on the layer's protocol fidelity at this specific contract.

*Failure modes under contract violation.* If the layer breaks any of clauses (i)–(iii) at any emission site — forgetting to observe, racing with concurrent emitters or with retractors, or admitting an emission whose `C(F, G, Σ) ≠ ∅` — Sh4 may fail at the resulting state. Templates that consume Sh4 directly become undefined or multi-valued where Sh4 would have collapsed slot-pair duplicates to a single representative; per-template specifications state explicitly when a template's totality depends on Sh4. Note that the set-valued accessors `from_K`, `to_K`, `from_addrs_K`, `to_addrs_K` (DirectedPair walkthrough) consume Sh4 only weakly — they degrade from sets of slot-pair-distinct tuples to multisets when Sh4 fails — and remain well-defined as multisets.

The singleton-returning `K_target_of` accessor (DirectedPair walkthrough) requires a strictly stronger commitment, FunctionalDependencyDiscipline, presented separately: Sh4 alone is insufficient because Sh4 enforces slot-pair distinctness, not from-slot uniqueness.

*Why a layer-level contract rather than a substrate-level axiom.* Lifting Sh4 into Sh-conf as an `Emit_K`-precondition (e.g., "reject `Emit_K` when `shape(K).idem = ⊤ ∧ C(F, G, Σ) ≠ ∅`") is technically feasible but conflicts with the substrate's design intent. Type semantics in ASN-0086 are by address identity, not by content-equivalence policy; substrate-level idempotency enforcement would require the substrate to commit to a duplicate-detection semantics (set vs. multiset, exact vs. coverage-equivalent) and would couple the substrate to a particular Observe-time-of-emit transactional discipline. Keeping Sh4 at the layer separates the substrate's address-permanence guarantee from the layer's idempotency policy: layers may adopt set-semantics idempotency for some K and bag-semantics for others, with the substrate uniformly admitting all emissions and the framework's templates consuming whichever discipline the layer commits to.

*Justification of the policy.* Some predicates need yes/no semantics on tuple existence: "is `d` classified as a claim?" should not be answered by counting `(∅, {d})` tuples. `A_K` is always a set of distinct-address tuples (R1, AddressInjectivity, ASN-0086); what differs across `idem` is whether `(slot_addrs(F_τ), slot_addrs(G_τ))`-pair duplicates can persist in `A_K`. Under Sh4 (idem = ⊤), the layer contract collapses such duplicates at Emit time, so `A_K` carries at most one active tuple per slot-pair: existence-vs-count distinctions are well-defined as Boolean tests. Under idem = ⊥, multiple distinct-address tuples may share a slot-pair (e.g., two Comment tuples with identical commenter/target reflecting two distinct events); predicates that count or enumerate the slot-pair multiplicity are meaningful precisely because the active subset retains those distinctions.

*Consequences.*

(a) *Existence-vs-count distinction.* Idempotent relations support `exists_K(F, G) : Bool` predicates with stable yes/no answers under the contract. Non-idempotent relations support `count_K(...)` predicates whose value reflects the number of distinct emission events.

(b) *Re-emit-vs-fail behavior is registry-driven.* Library helpers like `emit_attribute` consult `shape(K).idem` to decide whether to short-circuit on existing match or always allocate a fresh address. The decision is mechanical from the shape, not from inspection of K's name.

(c) *Idempotency is a property of A_K, not L_K.* By R3, `L_K` always retains every emission ever made — including any duplicates that may exist if the contract was ever violated. The contract restricts what reaches `A_K`. Under correct contract enforcement, once a duplicate would be emitted, the layer suppresses it. The audit slice `L_K` retains historical state regardless: retraction-then-reemit cycles can leave multiple coverage-identical tuples in `L_K` with at most one active.


## Template Catalog (Sh5)

**Sh5 — TemplateCatalog.** For each canonical shape `Sh_canon`, the shape framework specifies a hand-curated *template family* of predicate forms applicable to every `K ∈ T_cat` with `shape(K) = Sh_canon`. Each template is parameterized by K's name (and, where noted, by layer-supplied auxiliary accessors); instantiation substitutes the name into the template body and yields a per-K predicate or accessor. The families are written by hand against the canonical shape catalog (Sh5 is META), not assembled into a single function over an explicit codomain.

*Status.* Sh5 is a META commitment about how this framework constructs and maintains its canonical shape catalog, not a mechanical-derivation theorem about all possible catalogs. The status splits into two distinct components:

(a) *META observation.* The template families exhibited in the walkthroughs below are written by hand against the canonical shape catalog. There is no procedure mapping an arbitrary shape to its template family; new shapes acquire templates by analogy with existing entries and by hand-design.

(b) *META discipline.* This framework's catalog adheres to the rule that every catalog row's templates depend only on the following four input categories: (i) the shape components (cardinality, target-domain typing, idempotency flag); (ii) K's name; (iii) named scaffolding clauses surfaced in the *Scope and Substrate Scaffolding* list; and (iv) explicitly named per-K disciplines and per-call type-index parameters registered in the row's opt-in or parametric columns. The criterion is *literal name-citation*: a template body that references a symbol must either be one of the shape-component slots, K itself, a scaffolding clause name (e.g., `chain_index`, `home(·)`, `s_L`), an accessor exported by a registered per-K discipline (e.g., `emission_order` under SingleHomeCoverageDiscipline), or a parametric type-index argument; any symbol falling outside these four categories violates the discipline and the catalog rejects the addition. The opt-in column registers per-K disciplines (their names, their preservation contracts, and the accessor symbols they export); the parametric column registers per-call type-index arguments. Scaffolding clauses are catalog-row-independent (every row may cite them by name without per-row registration) because they are uniform substrate-layer commitments listed once in *Scope and Substrate Scaffolding*. This is a META commitment about this catalog's construction, not a theorem provable from R0…R7a plus Sh0–Sh4: a future draft proposing to add a template whose well-formedness depends on K-specific data outside (i)–(iv) would violate the discipline, and the framework would reject the addition. The discipline is what makes Sh5's per-shape organization falsifiable: a catalog row with diverging base templates from a shape-mate row, or a template body referencing a symbol outside (i)–(iv), would visibly violate the discipline.

*Worked check at `latest_K_for_addr`.* The Coverage walkthrough's `latest_K_for_addr` template body `argmax_{τ ∈ S_d} emission_order(τ)` references three external symbols beyond shape and K: `S_d` (defined inline as `{τ ∈ A_K^Σ : to₁(τ) = d}`, using shape-component-derived accessors `to₁` and base-machinery `A_K^Σ`); `argmax` (a meta-operator over finite ℕ-indexed sets, not a per-K accessor); and `emission_order(τ)`, which under SingleHomeCoverageDiscipline is `chain_index(addr(τ), d_K)`. The symbol `chain_index` is named in the *Link sub-allocator chain-index function* scaffolding clause (category (iii)); the symbol `d_K` is registered by SingleHomeCoverageDiscipline as a per-K commitment (category (iv)); the symbol `addr` is an R1 export from ASN-0086 (a base-machinery accessor on every `L_K`-tuple, available at every row regardless of opt-in). All three of `emission_order`'s constituents are within the four input categories. The template clears the discipline.

Adding a new K with a registered shape that matches a catalog entry yields the row's template family for free (subject to the auxiliary accessors named in opt-in/parametric extensions).

*Auxiliary accessors.* Two templates depend on data outside the substrate's relational structure:

- `K_is_fresh` (filesystem freshness, presented under Layer Composites below) consumes a layer-supplied `mtime` accessor over `A_doc`. The substrate does not provide `mtime`; layers built atop the substrate furnish it.
- `latest_K_for_addr` (Coverage instantiation of NonIdempotentDirectedPair, see walkthrough) consumes an `emission_order` total order on per-document tuple subsets. The substrate provides this *only* when the Coverage instantiation commits to single-home emission (see SingleHomeCoverageDiscipline below); otherwise the layer must supply its own ordering.

*What Sh5 is not.* Sh5 does not claim a procedure that, given an arbitrary shape, derives a template family. New shapes added to the catalog acquire templates by analogy with existing entries and by hand-design; the framework discipline limits design choices to those compatible with Sh0–Sh4, but it does not eliminate the design step.


## The Canonical Shape Catalog

The substrate's relations fall into a small fixed set of canonical shapes. Each canonical shape pairs with a *base* predicate template family that is forced by the shape — there is no design freedom in base template selection once the shape is fixed. Per-K opt-in and parametric extensions sit atop the base family and require additional registration (per-K disciplines) or additional arguments at evaluation time (type-index parameters).

*Reach of the framework's target-domain symbols.* Throughout this catalog, `A_doc` denotes content addresses (per ASN-0086, `A_doc^Σ = dom(Σ.C)` — content-store entries with `zeros(·) = 3`), *not* document-level container addresses (which live in `dom(Σ.M)` with `zeros(·) = 2` and are not directly targetable by shape constraints). Similarly `A_rel = dom(Σ.L)` denotes tuple addresses (also `zeros(·) = 3`). When prose below speaks of "documents" or "a document `d`" as the target of a relation (e.g., "is this document classified as K"), the formal reading is that `d ∈ A_doc^Σ` — a content-level address in the document's element-field interior, not the document's bare container address in `dom(Σ.M)`. The framework provides no target-domain symbol for `dom(Σ.M)` addresses; shape constraints cannot target document-level containers. Layers that need to relate document containers must record the relation against a designated content address within each container's element field (e.g., a conventional "document head" content address) and target that address via `A_doc`.

| Shape                     | (c_F, c_G) | t_F   | t_G   | idem | Template family                                              |
|---------------------------|------------|-------|-------|------|--------------------------------------------------------------|
| Classifier                | (0, 1)     | -     | A_doc | ⊤    | *base:* `is_K(d)` |
| Tuple-Classifier          | (0, 1)     | -     | A_rel | ⊤    | *base:* `is_K(τ)` (same body as Classifier's `is_K` with the signature shifted from `A_doc → Bool` to `A_rel → Bool` per Sh5(b)) |
| DirectedPair              | (1, 1)     | A_doc | A_doc | ⊤    | *base:* `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`; *opt-in (per-K):* `K_target_of(a)` under FunctionalDependencyDiscipline |
| NonIdempotentDirectedPair | (1, 1)     | A_doc | A_doc | ⊥    | *base:* `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)` (set-valued by R1 AddressInjectivity; may contain slot-pair-identical tuples without Sh4); *opt-in (per-K):* `latest_K_for_addr(d)` under SingleHomeCoverageDiscipline; *parametric:* `unresolved_K_comments_via(K_res, d)`, `all_K_resolved_via(K_res, d)` in any Resolution-shaped `K_res` |
| Resolution                | (1, 1)     | A_doc | A_rel | ⊤    | *base (inherited from `(1, 1, A_doc, A_rel, ⊤)` per Sh5(b)):* `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`; *primary consumption:* parametrically by NonIdempotentDirectedPair's `_via` templates |
| Retraction                | (\*, 1)    | A     | A_rel | ⊤    | *base (reformulated under `c_F = *`; bodies in the walkthrough):* `pair_K(F̂, b)` (F̂ matched by set equality), `from_K(a)` (membership-based: τ included iff `a ∈ slot_addrs(F_τ)`), `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`; *primary consumption:* by ASN-0086's `nullified(·)` definition, which reads each `L_R`-tuple's G-coverage directly over the audit slice `L_R^Σ` (not via the active-subset `to_K` accessor; the audit-slice reading is the one R6b commits to, blocking the recursive fixpoint the active-subset reading would introduce) |
| Provenance                | (1, 0\|1)  | A     | A     | ⊤    | *base (`c_G = 0|1` requires explicit `⊥`-handling on G-side templates; bodies in the walkthrough):* `outgoing_K(s)` (alias of `from_K(s)`), `pair_K(a, b)`, `from_K(a)`, `to_K(b)` (excludes attribution-only tuples), `from_addrs_K(b)`, `to_addrs_K(a)` (with `⊥`-filter) |

*Catalog row structure: base, opt-in, parametric.* Each row separates templates by what enables them. The three categories are defined by a precise criterion:

A template is *base* iff its definition is well-formed under exactly (a) the shape tuple's components, (b) K's name, and (c) the framework's Sh0–Sh4 guarantees (under the *Sh4 idempotency contract* when `shape(K).idem = ⊤`). Every K registered at the shape generates the row's base templates mechanically.

A template is *opt-in (per-K)* iff its well-formedness additionally requires a per-K discipline registration listed in the catalog row (currently FunctionalDependencyDiscipline at DirectedPair and SingleHomeCoverageDiscipline at NonIdempotentDirectedPair Coverage). The discipline strengthens Sh-conf's gate at the registering K beyond what the bare shape demands.

A template is *parametric* iff it takes an additional type-index argument supplied at predicate-evaluation time (e.g., a Resolution relation `K_res` consumed by NonIdempotentDirectedPair's `_via` templates). Parametric templates require no registration commitment at K; the type-index is passed by the calling predicate.

The criterion is exhaustive: any template that depends on K-specific data outside (a)–(c), without a registered per-K discipline or a per-call type-index, would fail to be classifiable and so would be rejected by the META discipline of Sh5(b). The split is what makes Sh5's per-shape discipline falsifiable: rows with identical `(c_F, c_G, t_F, t_G, idem)` tuples agree on base templates by Sh5; divergent base-template families across two equal-shape rows would falsify the discipline.

The catalog has *bipartite coverage*: for each structural pattern (cardinality + idempotency), entries with `t_G = A_doc` and `t_G = A_rel` are listed separately. Classifier and Tuple-Classifier are the two `(0, 1, -, ·, ⊤)` rows; DirectedPair and (a hypothetical Tuple-DirectedPair) would be the two `(1, 1, ·, ·, ⊤)` rows on the document/tuple axis. The current catalog enumerates the rows demanded by present-day predicate templates; further bipartite entries can be added by extending the catalog.

*Per-K opt-in registry is partitioned by base shape.* The per-K disciplines available at a K are determined by K's base shape: FunctionalDependencyDiscipline attaches only to DirectedPair (`(1, 1, A_doc, A_doc, ⊤)`); SingleHomeCoverageDiscipline attaches only to the Coverage instantiation of NonIdempotentDirectedPair (`(1, 1, A_doc, A_doc, ⊥)`). The two are structurally exclusive: no K can carry both, because the underlying shape's `idem` flag is fixed at the catalog level — FDD requires `idem = ⊤`, SHCD requires `idem = ⊥`, and a single registered K has exactly one `shape(K).idem` value. The framework therefore forbids registering both disciplines on the same K, and the opt-in registry is partitioned by base shape: the set of disciplines available at K is determined by `shape(K)` alone. Future disciplines added to the catalog will likewise attach to specific base shapes (or to specific shape-component subsets, e.g., disciplines that apply uniformly to all `(1, 1, A_doc, A_doc, _)` shapes regardless of idem) and inherit this partitioning.

*Naming conventions are layer constructs, not catalog rows.* Two structurally identical shapes — i.e., shapes whose tuples `(c_F, c_G, t_F, t_G, idem)` are equal — necessarily share the same canonical *base* template family by Sh5: there is no design freedom in base template selection once the shape is fixed. Per-K opt-in and parametric extensions are layer registrations atop the bare shape — they refine the templates that K supports without changing what shape-mates of K must share. Therefore relations that prior drafts of this catalog separated by role-specific naming — e.g., "Attribute" for parent → sidecar and "Citation" for citing → cited (both `(1, 1, A_doc, A_doc, ⊤)`); "Coverage" for witness → subject and "Comment" for commenter → target (both `(1, 1, A_doc, A_doc, ⊥)`) — collapse into a single shape row each (DirectedPair and NonIdempotentDirectedPair respectively). Distinguishing them at the catalog level would split a single base template family into two non-derivable lists, violating Sh5's per-shape-derives-base-templates discipline. The role-specific naming belongs to the layer that registers a particular K with the canonical shape, not to the framework; per-K disciplines (FDD, SingleHomeCoverageDiscipline) and parametric arguments (`K_res`) belong to the catalog row as opt-in/parametric extensions but do not modify the shape tuple.


## Per-Shape Template Walkthroughs

We walk the canonical shapes and exhibit the predicate templates each generates.

### Classifier — `(0, 1, -, A_doc, ⊤)`

Every tuple in `L_K` has `slot_addrs(F) = ∅` (Sh0) and `slot_addrs(G) = {d}` for some `d ∈ A_doc^Σ` (Sh1, Sh3). The to-accessor `to₁(τ) ∈ A_doc^Σ` is total (SlotAccessorTotality).

`is_K : A_doc → Bool`

`is_K(d) ≡ (E τ ∈ A_K^Σ :: to₁(τ) = d)`

A document `d` is *classified as K* iff there exists an active tuple in `L_K` whose to-slot is `d`. By Sh4 idempotency (layer-enforced), the existential is yes/no — multiple slot-identical active tuples are precluded by policy.

### Tuple-Classifier — `(0, 1, -, A_rel, ⊤)`

Structurally identical to Classifier; the only difference is the target domain. Every tuple in `L_K` has `slot_addrs(F) = ∅` and `slot_addrs(G) = {τ}` for some `τ ∈ A_rel^Σ`. The to-accessor `to₁(σ) ∈ A_rel^Σ` is total.

`is_K : A_rel → Bool`

`is_K(τ) ≡ (E σ ∈ A_K^Σ :: to₁(σ) = τ)`

A tuple `τ` is *classified as K* iff there exists an active classifier-tuple in `L_K` whose to-slot is `τ`. The single-letter substitution `d ↝ τ` from Classifier's template body is the only difference; signature changes from `A_doc → Bool` to `A_rel → Bool`.

Tuple-Classifier admits useful predicates over substrate-internal entities — marking a comment-tuple as endorsed, marking a citation-tuple as deprecated, marking a review-tuple as clean (so `is_clean(τ)` for `τ ∈ A_rel`). By Sh3 (`t_G = A_rel`), a Tuple-Classifier tuple's to-slot targets a tuple address, distinguishing it from a Classifier whose to-slot targets a document. The two are the bipartite halves of the same `(0, 1)` shape pattern.

*Distinction from Resolution.* Resolution `(1, 1, A_doc, A_rel, ⊤)` also targets `A_rel`, but its `c_F = 1` slot requires an actor — a resolving document. Tuple-Classifier has `c_F = 0`: no actor recorded in the tuple. Use Resolution when the assertion needs an attributed asserter; use Tuple-Classifier when the assertion is a property of the targeted tuple itself, not an action upon it.

### DirectedPair — `(1, 1, A_doc, A_doc, ⊤)`

Tuples have form `slot_addrs(F) = {a}, slot_addrs(G) = {b}` with `a, b ∈ A_doc^Σ` — a single document address in each slot. Role-specific readings (parent → sidecar, citing → cited, asserter → asserted, etc.) are layer conventions over a single structural shape.

*Canonical template family (role-neutral).* Every K registered at this shape generates the following five templates mechanically from the shape components. Each is unconditional under Sh0–Sh4 (Sh0/Sh1 supply canonical-slot form and unit cardinality; Sh2/Sh3 supply `A_doc^Σ` codomains for the slot accessors; Sh4 ensures the returned tuple-sets and address-sets are slot-pair-distinct, not multisets). Codomains are made explicit per the *Codomain convention* for templates:

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

**Definition — FunctionalDependencyDiscipline.** A K registered with the DirectedPair shape may additionally register a *FunctionalDependencyDiscipline* commitment: at most one active tuple per from-slot value, formally

`(A τ, τ' ∈ A_K^Σ : from₁(τ) = from₁(τ') :: addr(τ) = addr(τ'))`

at every reachable state Σ.

*Why this is strictly stronger than Sh4.* Sh4 enforces pairwise distinctness of slot-address *pairs* `(slot_addrs(F_τ), slot_addrs(G_τ))`, not pairwise distinctness of `slot_addrs(F_τ)` alone. Concrete counterexample under Sh4 alone: emissions `Emit_K(Σ, h, {(d, δ_d)}, {(s_1, δ_{s_1})})` and `Emit_K(Σ', h, {(d, δ_d)}, {(s_2, δ_{s_2})})` with `s_1 ≠ s_2` both pass Sh4's contract (different G-slots → distinct slot-pairs → `C(F, G, Σ') = ∅` at the second call). The result is `A_K^{Σ''} ⊇ {τ_1, τ_2}` with `from₁(τ_1) = from₁(τ_2) = d` and `to₁(τ_1) ≠ to₁(τ_2)`. So `{τ ∈ A_K^{Σ''} : from₁(τ) = d}` has cardinality 2; a singleton-returning accessor is ill-defined. FunctionalDependencyDiscipline forbids the second emission outright.

*FDD functional-dependency contract (the layer-discipline contract for FunctionalDependencyDiscipline).* The discipline is enforced by the layer at Emit time via the same Observe-then-Emit protocol used for the *Sh4 idempotency contract*, with the candidate-set restricted to from-slot match alone. The *FDD functional-dependency contract* is named to distinguish it from the *Sh4 idempotency contract* and the *Emit_K routing commitment* of Scope and Substrate Scaffolding; subsequent text cites it by this name. For each K with FunctionalDependencyDiscipline registered, on every `Emit_K(Σ, d, F, G)` call site:

(i) Compute `C_fd(F, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}` via the two-step procedure: (i.a) query `Observe_K(slot_addrs(F), ∅, oper)` — well-typed by finiteness of `slot_addrs(F)`; the `∅` G-pattern matches every G-coverage trivially under Observe_K's `Ĝ ⊆ coverage(G)` semantics, so the result is `{τ ∈ A_K^Σ : slot_addrs(F) ⊆ coverage(F_τ)}`. By the same AllocatedAddressAntichain argument used in Sh4's contract, this over-approximates `slot_addrs(F_τ) ⊇ slot_addrs(F)`. (i.b) post-filter to exact from-slot-address equality on F — retain only τ with `|slot_addrs(F_τ)| = |slot_addrs(F)|` (which under canonical-slot form forces `slot_addrs(F_τ) = slot_addrs(F)` given the over-approximation).

(ii) If `C_fd(F, Σ) ≠ ∅`, the emission is *suppressed*: no `→`-step occurs.

(iii) Only if `C_fd(F, Σ) = ∅` does the layer issue `Emit_K(Σ, d, F, G)`.

The layer commits to executing (i)–(iii) atomically with respect to other emitters and retractors at the same `~`-equivalence class of K. The same single-process-substrate scope from Sh4's contract applies: atomicity reduces operationally to within-call sequentiality between `Observe_K` and the substrate K.λ-step within a single `Emit_K` call, with no intervening `↦`-step from another FDD-emitter at a `~`-equivalent K.

*Preservation under the discipline.* The inductive argument runs three cases: Case A (active subset unchanged), Case B (single new tuple at K), and Case C (retraction-only contraction). Case D (the K=R simultaneous addition-and-contraction case from Sh4) is excluded by shape-tuple structure: FDD requires `shape(K) = (1, 1, A_doc, A_doc, ⊤)`, while Retraction has `shape(R) = (*, 1, A, A_rel, ⊤)`; per-class constancy of `shape` (`K ~ K' ⟹ shape(K) = shape(K')`) and the shape-tuple inequality (differs on `c_F`, `t_F`, `t_G`) force `K ≁ R` for every FDD-registered K, so no `Emit_R` step can extend `A_K`.

*Stratification.* As with Sh4's preservation proof, FDD's induction consumes Sh0–Sh3 (and SlotAccessorTotality at `c_F = c_G = 1`) as previously-established state-indexed lemmas — used, for instance, to land `from₁(τ)` in `A_doc^Σ` and to identify `slot_addrs(F_τ)` with `{from₁(τ)}` in the Case B argument. Sh0–Sh3 are proved by their own independent inductions over `↦*` against the same empty-baseline `Σ_init`; they are not part of FDD's inductive hypothesis. The stratification (Sh0–Sh3 first, then Sh4/FDD using them as state-indexed lemmas) is the same as for Sh4. No cycle: FDD never appears as a premise of Sh0–Sh3's proofs.

Fix `K ∈ T_cat` with FDD registered. The FDD property `(A τ, τ' ∈ A_K^Σ : from₁(τ) = from₁(τ') :: addr(τ) = addr(τ'))` has the same off-diagonal/diagonal structure as Sh4: the diagonal is trivial by reflexivity, the substantive content is that no two *distinct* active K-tuples share a from-slot value. The candidate set `C_fd(F, Σ) := {τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F)}` is broader in scope than Sh4's `C(F, G, Σ)` — it matches on from-slot alone rather than on the slot-pair — so `C ⊆ C_fd` at every state. The discipline is therefore *stricter as a gate* (more candidate sets are non-empty, so more emissions are suppressed) even though its candidate set is broader.

*Base.* At `Σ_0 = Σ_init` (per the framework's empty-baseline assumption, *Initial-state baseline for preservation proofs* in the Sh-conf section above), `L_K^{Σ_0} = A_K^{Σ_0} = ∅`; FDD's universal is vacuous.

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

Tuples have form `slot_addrs(F) = {d}, slot_addrs(G) = {addr(σ)}` where `d ∈ A_doc^Σ` is the resolving document and `σ ∈ A_rel^Σ` is the comment-tuple being resolved. By Sh5(b), the shape `(1, 1, A_doc, A_rel, ⊤)` mechanically generates the same base template family as DirectedPair (with `t_G = A_rel` substituted for `A_doc`): `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`. The walkthroughs below focus on Resolution's *primary consumption* — parametric use by Comment's `unresolved_K_comments_via` / `all_K_resolved_via` templates as the `K_res` argument, with Sh3 (`t_G = A_rel`) being what makes that consumption possible — but the base templates are available for any K registered at this shape. The catalog row's "primary consumption" column flags the parametric use case rather than enumerating the inherited base family a second time; per Sh5(b), the base templates are mechanically determined by the shape and need no per-row restatement.

### Retraction — `(\*, 1, A, A_rel, ⊤)`

Tuples have form `slot_addrs(F) ⊆ A^Σ` (any finite set, possibly empty) and `slot_addrs(G) = {addr(σ)}` for `σ ∈ A_rel^Σ` the tuple being retracted. The retraction shape is consumed by R6 (ASN-0086) directly: the active-subset definition uses `L_R`'s tuples to compute `nullified(Σ)`. By Sh5(b), the shape `(*, 1, A, A_rel, ⊤)` mechanically generates the base template family — though the bodies must be re-formulated for the `c_F = *` setting, since `from₁` is not defined when `c_F` is not `1`. The DirectedPair templates' use of `from₁(τ)` as a point accessor is replaced by `slot_addrs(F_τ)` as a set accessor; the matching predicates likewise lift from address-equality to set-equality or set-membership as appropriate to each template's role:

`pair_K(F̂, b)        ≡ (E τ ∈ A_K^Σ :: slot_addrs(F_τ) = F̂ ∧ to₁(τ) = b)`

`from_K(a)           ≡ {τ ∈ A_K^Σ : a ∈ slot_addrs(F_τ)}`

`to_K(b)             ≡ {τ ∈ A_K^Σ : to₁(τ) = b}`

`from_addrs_K(b)     ≡ {x : (E τ ∈ A_K^Σ :: to₁(τ) = b ∧ x ∈ slot_addrs(F_τ))}`

`to_addrs_K(a)       ≡ {to₁(τ) : τ ∈ A_K^Σ ∧ a ∈ slot_addrs(F_τ)}`

The four set-valued templates take an *address* on the from-side (`from_K`, `from_addrs_K`'s witness `x`, and `to_addrs_K`'s argument `a`) using the membership relation `a ∈ slot_addrs(F_τ)` — every τ whose from-slot *contains* the queried address `a` is included. The Boolean `pair_K`'s F-side argument is an *address-set pattern* `F̂` matched by exact set equality `slot_addrs(F_τ) = F̂`; this preserves the role of `pair_K` as a Boolean existence test for a particular (from-pattern, to-address) combination. The to-side accessors and the `to_K` template use `to₁(·)` directly, since `c_G = 1` admits SlotAccessorTotality on the G-slot. Both `to_K` and `to_addrs_K` return well-typed sets — `to_K` a tuple-set in `℘_fin(A_K^Σ)`, `to_addrs_K` an address-set in `℘_fin(A_rel^Σ)` — by Sh3 on the G-slot. Even though Retraction's primary role is to flip `A_K` membership for arbitrary K via R6, not to host its own predicates, the base template family is fully defined; the catalog row's "primary consumption" column flags R6 as the principal consumer rather than enumerating the inherited base family a second time.

*Note on `pair_K`'s set-equality F-side argument (deliberate, role-specific design choice).* Retraction's `pair_K(F̂, b)` is the one catalog template that takes an *address-set pattern* on the from-side rather than an address, and matches by exact set equality rather than by membership. This is *not* the only Sh5(b)-admissible reading: an alternative would be `pair_K(a, b) ≡ (E τ ∈ A_K^Σ :: a ∈ slot_addrs(F_τ) ∧ to₁(τ) = b)`, mirroring the membership semantics of `from_K`. Either reading is well-formed under Sh5(b) — both depend only on (i) shape components (`c_F = *`, `c_G = 1`, `t_F = A`, `t_G = A_rel`, `idem = ⊤`), (ii) K's name, and (iii) no extra named accessors. The framework adopts the exact-set-equality reading as a deliberate role-specific design choice, recorded here in the catalog row rather than mechanically derived: because Retraction's `c_F = *` admits from-slots of any finite cardinality (including the bare-retraction case `c_F = 0` and multi-attributor retractions), "is there a tuple with this *exact* attribution-set targeting `b`" is the operationally meaningful Boolean test (matching the audit-grade question "did this specific attribution combination ever retract `b`"). The membership-reading `pair_K(a, b)` overlaps with `from_K(a) ∩ to_K(b) ≠ ∅`, which is already expressible from the base templates by intersection; retaining the set-equality reading for `pair_K` gives the catalog row a Boolean predicate that is not directly expressible from the other four templates, avoiding redundancy with the membership-based `from_K`. The choice is recorded as deliberate so that other shape rows with `c_F = 1` (DirectedPair, NonIdempotentDirectedPair, Resolution, Provenance) — where `slot_addrs(F_τ) = {from₁(τ)}` and set-equality with a single-element pattern collapses to address-equality — continue to read `pair_K(a, b)` as an address-pair predicate without disagreement with this row.

*Unit-depth retraction discipline secured by Retraction's shape.* Retraction's `c_G = 1` together with canonical-slot form (Sh-conf clauses (a)/(b)) forces every shape-conformant Retraction emission's G-endset to a single unit-depth span `{(b, δ(1, #b))}` for some `b ∈ A_rel^Σ`. This is exactly ASN-0086's unit-depth retraction discipline: every emission that lands in `L_R^Σ` via `Emit_R` satisfies the discipline by construction. Consequently, ASN-0086's wp simplification under regime (i) applies to every Sh-conf-admitted Retraction emission — `NoCraftedSpanReachesD(Σ, d)` holds automatically at every such call site by Lemma — RetractionTargetNotOnChain (whose generalized statement `b ⋠ a_emit(Σ, d)` for any `b ∈ dom(Σ.L)` is applied in the EffectiveWpSimplification Corollary's Step 1 to each prior R-tuple's unique G-slot address; the proof case-splits on `home(b) = d` vs `home(b) ≠ d` and rules out `b ≼ a_emit(Σ, d)` in each case) — so the wp_086 in the Sh-conf section's effective-wp derivation collapses to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible` without manual discharge.

The unrestricted from-slot (`c_F = *`) accommodates use cases where the retracting party is recorded in F (e.g., F's slot addresses include an agent address), as well as the bare retraction `Nullify(Σ, d_retr, a) = Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` of ASN-0086, where `F = ∅`. Both forms are canonical-slot (the bare form trivially, the attributed form when its from-slot endset is in canonical form). The shape framework rejects retractions whose from-slot uses non-canonical-form endsets, consistent with the discipline imposed across the catalog.

### NonIdempotentDirectedPair — `(1, 1, A_doc, A_doc, ⊥)`

Non-idempotent directed-pair tuples allow multiple distinct emissions sharing the same slot-address pair — each emission is a distinct event, retained in `L_K` regardless of slot-address coincidence with prior tuples. Role-specific readings (witness → subject for coverage, commenter → target for comment, etc.) are layer conventions over a single structural shape.

*Canonical base templates (forced by shape).* By analogy with DirectedPair, every K registered at this shape generates:

`pair_K(a, b)         ≡ (E τ ∈ A_K^Σ :: from₁(τ) = a ∧ to₁(τ) = b)`

`from_K(a)            ≡ {τ ∈ A_K^Σ : from₁(τ) = a}`

`to_K(b)              ≡ {τ ∈ A_K^Σ : to₁(τ) = b}`

`to_addrs_K(a)        ≡ {to₁(τ) : τ ∈ A_K^Σ ∧ from₁(τ) = a}`

`from_addrs_K(b)      ≡ {from₁(τ) : τ ∈ A_K^Σ ∧ to₁(τ) = b}`

The signatures match DirectedPair's. Without Sh4, the tuple-valued accessors `from_K` and `to_K` may contain multiple slot-pair-identical tuples (R1 keeps them distinct by tuple address; slot-pair duplicates are preserved). `pair_K` remains a Boolean: `(E τ ::)` is yes/no regardless of how many witnesses satisfy the body. The address-valued projections `to_addrs_K` and `from_addrs_K` are set-comprehensions over slot-addresses, so any multiplicity from `from_K`/`to_K` collapses on the address side.

Two role-specific instantiations of NonIdempotentDirectedPair are catalogued, each adding extensions atop the base templates.

#### Coverage instantiation (opt-in via SingleHomeCoverageDiscipline)

Coverage tuples assert that a witnessing document covers (reviews, revises, evaluates) a target document. The from-slot identifies the *witness/asserter* — the document making the coverage claim (e.g., a review document, a revision document). The to-slot identifies the *subject* — the document being covered. The framework requires `c_F = 1` rather than `c_F = 0` because Coverage relations carry directional provenance: knowing *which* document witnessed a coverage event is constitutive of the assertion, not auxiliary metadata. A Coverage relation without an attributed witness would not be a coverage assertion at all; it would be an unattributed flag, which the Classifier shape `(0, 1)` already covers. The `(1, 1)` shape encodes the witness-to-subject directionality intrinsic to coverage semantics.

For K with this instantiation, multiple emissions targeting the same subject `d` are expected (e.g., evolving review status from the same or successive witnesses). The opt-in `latest_K_for_addr` template projects to the most recent:

`latest_K_for_addr : A_doc → A_K^Σ ∪ {⊥}`

`latest_K_for_addr(d) ≡ argmax_{τ ∈ S_d} emission_order(τ)` &nbsp; if &nbsp; `S_d ≠ ∅`

`latest_K_for_addr(d) ≡ ⊥` &nbsp; if &nbsp; `S_d = ∅`

where `S_d = {τ ∈ A_K^Σ : to₁(τ) = d}` ranges over all active Coverage tuples targeting `d`, regardless of which witness `from₁(τ)` they originate from. The codomain is the tuple set `A_K^Σ ∪ {⊥}` (not the address set): `argmax` selects a tuple from `S_d ⊆ A_K^Σ`, and the consumer reads slot accessors `from₁(·)`, `to₁(·)`, `addr(·)` off the returned tuple by re-querying the substrate's relational structure. The template's signature is indexed by the subject alone because "the latest assertion about `d`" is a function of `d`'s coverage-event history; the from-slot is consulted by the *consumer* of `latest_K_for_addr(d)` (which can read `from₁` off the returned tuple to recover the witness), not by the template's projection itself. The accessor is *partial*: it returns `⊥` when no Coverage tuple has yet targeted `d`. Consumers of `latest_K_for_addr` must handle the `⊥` case explicitly.

**Definition — SingleHomeCoverageDiscipline.** A registered Coverage relation `K` commits to *single-home emission* iff every emission `Emit_K(Σ, d, F, G)` for type K uses a single fixed home document `d = d_K ∈ dom(Σ.M)` across the relation's lifetime. The commitment is a per-K registration constraint, not a universal shape constraint.

*Single-home commitment (the layer-discipline contract for SingleHomeCoverageDiscipline).* The discipline is realized through the *single-home commitment* — the third per-K layer-discipline contract in the framework, distinct from the *Sh4 idempotency contract* and the *FDD functional-dependency contract*. Under the *single-home commitment*, for each K with SingleHomeCoverageDiscipline registered, on every `Emit_K(Σ, d, F, G)` call site the layer enforces the following single-step protocol:

(i) If `d ≠ d_K`, the call is *rejected outright*: the layer does not issue `Emit_K(Σ, d, F, G)`; equivalently, `Emit_K` returns `⊥` at the layer's pre-substrate gate without invoking K.λ. (The framework's Sh-conf return-type extension to `(Σ' × A_rel^{Σ'}) ∪ {⊥}` accommodates this rejection at the same `⊥`-token; the caller distinguishes single-home rejection from Sh-conf rejection by inspecting the contract's pre-emission home check `d = d_K`.)

(ii) If `d = d_K`, the layer issues `Emit_K(Σ, d, F, G)` per the substrate's usual K.λ protocol (and any other applicable contracts at the same call site — Sh4, FDD, etc. — fire in their established order).

Unlike the *Sh4 idempotency contract* and the *FDD functional-dependency contract*, the *single-home commitment* requires no Observe step: the home value `d_K` is a per-K registration constant, so the home check `d = d_K` is a literal-equality test against a fixed value, with no state-dependent computation. Atomicity is trivial (no race window exists between an Observe and the substrate K.λ-step).

*Preservation under the single-home commitment.* The single-home property holds at every reachable state under the contract, by induction on `↦*`. Fix `K ∈ T_cat` with SingleHomeCoverageDiscipline registered at fixed home `d_K`.

The single-home property `(A τ ∈ L_K^Σ :: home(addr(τ)) = d_K)` is the homed-set commitment: every K-tuple ever emitted resides under `d_K`. The companion property `S_d ⊆ {chain elements at d_K}` for every `d ∈ A_doc^Σ` follows directly: `S_d = {τ ∈ A_K^Σ : to₁(τ) = d} ⊆ A_K^Σ ⊆ L_K^Σ`, and every τ ∈ L_K^Σ has `home(addr(τ)) = d_K` by the homed-set commitment, hence `addr(τ)` is a chain element at `d_K` by the *Per-document link sub-allocator chains* scaffolding clause.

*Stratification.* As with Sh4 and FDD, the single-home commitment's induction consumes Sh0–Sh3 (and `home(·)` from ASN-0086) as previously-established state-indexed lemmas. Sh0–Sh3 are proved by their own inductions; they are not part of this contract's inductive hypothesis. No cycle.

*Base.* At `Σ_0 = Σ_init`, `L_K^{Σ_0} = ∅`; the universal `(A τ ∈ L_K^{Σ_0} :: home(addr(τ)) = d_K)` is vacuous.

*Step (Case A: `L_K^{Σ'} = L_K^Σ`).* `L_K` is unchanged. The property is inherited tuple-by-tuple from the IH (no new τ to check; existing τ retain `home(addr(τ)) = d_K`).

*Step (Case B: `L_K^{Σ'} = L_K^Σ ∪ {τ_new}`).* By the *Emit_K routing commitment*, the K.λ-step originates as an `Emit_K(Σ, d, F, G)` call. The *single-home commitment* clause (i) admits the call only if `d = d_K`. Under clause (ii), K.λ's first/subsequent-emission protocol fires at home `d = d_K`, depositing τ_new at an address with `home(addr(τ_new)) = d_K` (ASN-0086, R0a-Cor1 places the deposit address in `d_K`'s link sub-allocator chain, so its home is `d_K` by L1a). So `home(addr(τ_new)) = d_K`. Combined with the IH on the older tuples, every τ ∈ L_K^{Σ'} has `home(addr(τ)) = d_K`.

*Step (Case C: `L_K^{Σ'} ⊆ L_K^Σ`)*. Impossible — L_K is monotone non-decreasing by R3. Skipped.

The induction closes. ∎

*Status.* Single-home is a *theorem under the single-home commitment*, not a substrate-enforced axiom. ASN-0086's K.λ accepts an emission at any `d ∈ dom(Σ.M)` regardless of any K-specific home; the single-home property holds for K-emissions because the *single-home commitment* rejects calls with `d ≠ d_K` at the layer's pre-substrate gate. Without the contract, the layer would admit K-emissions at distinct homes and the single-home property would fail at the resulting state.

*Failure modes under contract violation.* If the layer breaks clause (i) at any emission site — admitting an emission with `d ≠ d_K` — the homed-set commitment fails, the companion property `S_d ⊆ {chain elements at d_K}` fails, and `latest_K_for_addr`'s well-definedness argument (ii) collapses: τ ∈ S_d with `home(addr(τ)) ≠ d_K` have addresses in *other* allocators' chains, and `chain_index(addr(τ), d_K)` is undefined at those addresses. Templates consuming `emission_order` become undefined at the corrupted state. The framework's preservation theorem above is exactly what rules this out under correct contract enforcement.

*Why single-home matters for `emission_order`.* T9 (ForwardAllocation, ASN-0034) supplies a total order on outputs of a single allocator's chain — specifically, for `same_allocator(a, b) ∧ allocated_before(a, b)`, T9 gives `a < b` under T1. Tuple addresses in a Coverage relation belong to per-document link sub-allocators (the substrate-conforming layer's link-side chain enumeration referenced by Scope and Substrate Scaffolding; ASN-0086 R0a-Cor1 and FreshEmissionAddress consume this same enumeration). Under SingleHomeCoverageDiscipline, every `τ` with `to₁(τ) = d` has the same `home(τ) = d_K`, hence the same link sub-allocator chain. We define:

`emission_order(τ) := chain_index(addr(τ), d_K)`

— the *Link sub-allocator chain-index function* scaffolding clause supplies `chain_index(·, d_K) : {chain elements at d_K} → ℕ` directly as a named accessor, returning the unique `n ≥ 0` with `addr(τ) = inc^n(d_K.0.s_L.1, 0)` (well-defined and single-valued by T10a.7, EnumerationInjectivity, ASN-0034, as recorded in that scaffolding clause). `emission_order` is thus a direct composition of the scaffolding's chain-index function with `addr(·)` — no appeal to implicit chain enumeration is required, and the per-K template's well-formedness depends only on the named scaffolding accessor plus `addr(·)` (an R1 export from ASN-0086).

*Why the `argmax` in `latest_K_for_addr` is well-defined under T1.* Three ingredients:

(i) `S_d` is finite at every reachable Σ. `S_d ⊆ A_K^Σ ⊆ L_K^Σ ⊆ dom(Σ.L)`, and `dom(Σ.L)` is finite by L-fin (ASN-0043) — the link-side finiteness fact, whose content-side analog `dom(Σ.C)` finite is recorded as the content-store finiteness scaffolding clause and is the partner citation invoked at `cov_allocated`'s finiteness claim above.

(ii) The chain-index map `τ ↦ emission_order(τ)` is injective on `S_d`. Under SingleHomeCoverageDiscipline every `τ ∈ S_d` has `home(τ) = d_K`, so by the *Per-document link sub-allocator chains* scaffolding clause every such `addr(τ)` is a chain element at `d_K`. The *Link sub-allocator chain-index function* scaffolding clause then supplies a well-defined and single-valued `chain_index(addr(τ), d_K) ∈ ℕ` per τ (with single-valuedness inherited from T10a.7, EnumerationInjectivity, ASN-0034, as that scaffolding clause records). Distinct `τ, τ'` with distinct addresses (R1, AddressInjectivity, ASN-0086) therefore receive distinct chain indices, since the scaffolding's `chain_index(·, d_K)` is a function on chain-element inputs.

(iii) Chain-index order coincides with T1-order on the chain. By T9, within `A_L(d_K)`'s chain, `allocated_before(a, b) ⟹ a < b` under T1; combined with T10a.7's enumeration `tₙ₊₁ = inc(tₙ, 0)` and TA5(a)'s strict-increase under `inc(·, 0)`, the chain-index ordering on `A_L(d_K)` is strictly increasing under T1. Hence `argmax_{τ ∈ S_d} emission_order(τ)` selects the same unique element whether the ordering is read off chain-indices or off T1 — namely the τ of maximal chain-index in `S_d` (well-defined because `S_d` is finite and chain-indices are totally ordered on ℕ).

*Subset preservation when `d_K` hosts multiple relations.* SingleHomeCoverageDiscipline pins all K-tuples to one home document but does *not* require `d_K` to host only K. Other relations (any K' with `home(emission) = d_K`) interleave their tuples with K's into `d_K`'s link sub-allocator chain, so the chain-indices occupied by K-tuples need not be contiguous — chain indices 0, 2, 5 might be K while 1, 3, 4 are other relations. The argmax remains well-defined on this subset: (ii) injectivity is over `S_d ⊆ {chain elements at d_K}` and restricts to any subset; (iii) the T1-order strictly increasing along chain-indices restricts unchanged to any subset. So `argmax_{τ ∈ S_d} emission_order(τ)` picks the unique element of `S_d` with maximal chain-index regardless of whether the chain-index set is contiguous; SingleHomeCoverageDiscipline therefore does not constrain `d_K`'s exclusivity to K, only K's exclusivity to `d_K`.

*Without SingleHomeCoverageDiscipline:* the Coverage instantiation's `latest_K_for_addr` is no longer determined by shape + substrate alone, since `emission_order` is no longer mechanically supplied by the substrate-conforming layer's per-document chain enumeration. The layer must supply a per-K `emission_order` accessor as part of its registration; the catalog row records this as a per-K registration obligation rather than a derived template. Sh5 itself is unchanged — its META observation (a) already acknowledges that templates are written by hand against the canonical catalog, and its META discipline (b) explicitly permits templates to depend on "explicitly named layer-supplied accessors registered in the row's opt-in or parametric columns"; an `emission_order` registration is exactly such a named accessor. Coverage instantiations that decline to commit to single-home emission must register their layer-supplied `emission_order` accessor as part of their per-K registration.

Coverage and Comment both use `idem = ⊥` but for different reasons. Coverage's `idem = ⊥` is principled — coverage tuples by design supersede each other (the `latest_K_for_addr` opt-in template surfaces this directly). Comment's `idem = ⊥` is incidental — comments differ in F or G even when "looking the same" in content; the parametric `_via` templates do not consume an ordering, they consume a resolver type.

#### Comment instantiation (parametric in K_res)

Comments are events: each comment is a distinct emission, even with identical slot-addresses. The Comment instantiation adds a parametric template family taking a *resolver-type argument* `K_res` of Resolution shape — Comment instantiations do not co-register a particular resolver at the type level. The framework treats any active `K_res`-typed tuple targeting τ's address as resolving τ, regardless of provenance: there is no notion of "the K_res paired with K"; the layer chooses which Resolution-shaped relation to consult when querying resolution status.

`unresolved_K_comments_via(K_res, d) ≡ {τ ∈ A_K^Σ : to₁(τ) = d ∧ ¬resolved_by(τ, K_res)}`

where `resolved_by(τ, K_res) ≡ (E ρ ∈ A_{K_res}^Σ :: to₁(ρ) = addr(τ))`.

`all_K_resolved_via(K_res, d) ≡ unresolved_K_comments_via(K_res, d) = ∅`

A comment τ is *unresolved with respect to K_res* iff no active `K_res`-tuple targets τ's address (R5, TupleSelfTargeting, ASN-0086, makes this targeting expressible). The template signature includes `K_res` explicitly because the framework imposes no co-registration between Comment instantiations and their resolvers: different layers may resolve the same Comment relation under different `K_res`, and the predicate is well-defined parametrically across that choice.

The semantics are deliberately permissive — *any* active `K_res`-tuple targeting τ counts as a resolution, modulo whatever additional filtering the calling layer applies via its choice of `K_res`. This matches the substrate's open-ended type discipline: typed relations are claims surfaced for layer-level evaluation, not assertions adjudicated by the substrate.

*Layer-level aliasing convention.* When a calling layer commits to a single canonical resolver `K_res_canonical` for `K` (a layer convention, not a framework-level registration), it may define an alias `unresolved_K_comments(d) := unresolved_K_comments_via(K_res_canonical, d)`. This alias is a layer construct and is not part of the shape framework's template family.

These templates consume the Resolution shape parametrically — Resolution does not generate its own template family; it is consumed here.

### Provenance — `(1, 0|1, A, A, ⊤)`

Provenance tuples attribute one substrate event (the F-slot) to another (the G-slot). The G-slot may be empty (`c_G = 0|1`) — used to record agent attribution where the attributed event is the emission itself. Slot accessor `to₁⁻` is partial (returns `⊥` when G is empty); `from₁` remains total because `c_F = 1`.

*Canonical base template family.* Per Sh5(b), the shape `(1, 0|1, A, A, ⊤)` mechanically generates a base template family analogous to DirectedPair's, with the asymmetry that `c_G = 0|1` requires explicit `⊥`-handling on G-side templates. The F-side templates close over the totality of `from₁`; the G-side templates must filter out tuples whose `to₁⁻` is undefined before applying the to-side accessor. Codomains follow the *Codomain convention for partial templates* established for partial accessors above:

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


## Layer Composites

Some predicates frequently composed by layers above the substrate are not pure substrate templates: they depend on data outside the relational structure. We catalog them here, separated from the per-shape templates, to keep Sh5's discipline honest.

### `K_is_fresh` (DirectedPair + FunctionalDependencyDiscipline + filesystem)

`K_is_fresh(d) ≡ from_K(d) ≠ ∅ ∧ mtime(K_target_of(d)) ≥ mtime(d)`

A composite over a DirectedPair-shape relation `K` registered with FunctionalDependencyDiscipline (so the singleton-returning `K_target_of` is well-defined), together with a layer-supplied `mtime : A_doc → ℕ` accessor (filesystem modification time). The substrate's contribution is `from_K` (canonical) and `K_target_of` (conditional on FunctionalDependencyDiscipline); the layer's contribution is `mtime`.

Under FunctionalDependencyDiscipline violation, the composite degrades: replace `K_target_of(d)` with iteration over `to_addrs_K(d)` and an explicit reduction (e.g., "max mtime over all targets"). The reduction is a layer-level choice, not a framework-derived projection.

This composite was previously listed under the (now-merged) Attribute template family. It is moved here because Sh5's mechanical-organization claim applies only to templates that depend on K's name and shape — `mtime` is a separate registered accessor, not derivable from K — and because `K_target_of`'s well-definedness depends on the per-K FunctionalDependencyDiscipline commitment, which is a layer registration beyond the bare DirectedPair shape.


## Worked Example: K = comment

To verify the framework on a concrete instance, register `K = comment` with the Comment instantiation of NonIdempotentDirectedPair (shape `(1, 1, A_doc, A_doc, ⊥)`). Consider states reached by the following emissions, starting from an initial state Σ_0 with two pre-allocated documents `d_1, d_2 ∈ A_doc^{Σ_0}` and two home documents `home_K, home_R ∈ dom(Σ_0.M)` — `home_K` for Comment emissions and `home_R` for Resolution emissions (single-home not required for either; we use one home per relation for simplicity). We also assume `dom(Σ_0.L) = ∅` (no links of any type have yet been emitted at Σ_0); this is what makes K.λ's first-emission branch fire at the first emission below — the predicate `{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = home_K}` ranges over *all* of `dom(Σ_0.L)`, not just K-typed links, so the empty-`L_K` reading is insufficient.

*Registered catalog for this walkthrough.* `T_cat = {comment, K_res, R}` (closure under `~` implicit). The walkthrough exercises three registered types: `comment` (the Comment instantiation under exercise), `K_res` (a Resolution-shape relation, introduced by name when Emission 3 fires below — the layer registers it under shape `(1, 1, A_doc, A_rel, ⊤)` at `Σ_0`), and `R` (the framework's mandatory baseline retraction type per the *Interaction with Nullify* paragraph above, with `shape(R) = (*, 1, A, A_rel, ⊤)`). Every type used in the rejection cases below is checked against this explicit `T_cat`: `K_ghost` of Rejection case 4 is verifiable as `∉ T_cat` exactly because the catalog above does not name it. The lifetime-constancy of `T_cat` (fixed at `Σ_init`, unchanged through every reachable state in this walkthrough) is what underwrites the inductive baseline for Sh0–Sh4 at the three registered types throughout the walkthrough.

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

**Rejection case 4: unregistered type (K ∉ T_cat).** Let `K_ghost ∈ T_admissible \ T_cat` be a non-empty type endset that has not been registered with the catalog — for example, a type endset whose coverage class corresponds to no canonical shape, perhaps because the calling layer has not yet declared the relation, or because the type was constructed ad-hoc and never added to `T_cat`. Attempt `Emit_{K_ghost}(Σ_4, home_K, F_6, G_6)` with arbitrary `F_6, G_6 ∈ Endset` — concretely, we reuse Emission 1's values: `F_6 = F_1 = {(d_1, δ(1, #d_1))}` and `G_6 = G_1 = {(d_2, δ(1, #d_2))}`, both canonical-slot and well-allocated. Sh-conf's first conjunct `K_ghost ∈ T_cat` is *false* at the literal-membership test against the registered catalog. The emission is rejected at this gate; `Emit_K` returns `⊥` (per Sh-conf's extended return type) and no state transition occurs. The second conjunct `conf_{K_ghost}^{Σ_4}(F_6, G_6)` is unevaluable — `shape(K_ghost)` is undefined for unregistered K, so the conformance predicate has no shape tuple to test against — but the first conjunct's failure is sufficient to reject without proceeding to the conformance check. State remains Σ_4. ✗

The `K ∈ T_cat` gate is structurally separate from the three conformance gates (clauses (a)–(d) of Sh-conf). It protects the framework's invariants against accidental schema drift: only registered relations participate in shape-discipline reasoning, and emissions at unregistered types are rejected at the registry boundary regardless of how their `F, G` are structured. A layer that wants to admit `K_ghost` must first register it with the catalog — selecting a shape, committing to the per-class constancy of `shape(·)`, and accepting Sh-conf's structural gates for all subsequent emissions at that K.

**Edge case: retraction of τ_1.** From Σ_4, issue `Nullify(Σ_4, d_retr, a_1)` producing Σ_5. By R6c (RestorationByReemission, ASN-0086), τ_1 is permanently removed from `A_K^Σ` for all future states. So:

`A_K^{Σ_5} = {τ_2}` (τ_1 nullified; τ_2 remains).

`unresolved_K_comments_via(K_res, d_2) = {τ ∈ A_K^{Σ_5} : to₁(τ) = d_2 ∧ ¬resolved_by(τ, K_res)} = ∅` (τ_2 still resolved by ρ_2, which is in `A_{K_res}^{Σ_5}`).

`all_K_resolved_via(K_res, d_2) = true`.

The framework gives stable, well-typed answers across emission and retraction events. Sh0–Sh3 are preserved inductively, template signatures match the shape registry, and the active-subset machinery composes cleanly with retraction.


## Additional Worked Examples

### Coverage under SingleHomeCoverageDiscipline

Register `K = review` with the Coverage instantiation of NonIdempotentDirectedPair (shape `(1, 1, A_doc, A_doc, ⊥)`), committed to single-home emission at `d_K ∈ dom(Σ_0.M)`. Pre-allocate `d_witness, d_subject ∈ A_doc^{Σ_0}` and `d_witness' ∈ A_doc^{Σ_0}`. Assume `dom(Σ_0.L) = ∅` (no links of any type yet emitted), so K.λ's first-emission predicate at `d_K` will fire at Emission C1.

**Emission C1.** `Emit_K(Σ_0, d_K, F_C1, G_C1)` with `F_C1 = {(d_witness, δ(1, #d_witness))}` (witness) and `G_C1 = {(d_subject, δ(1, #d_subject))}` (subject). Sh-conf admits (canonical-slot, cardinality 1/1, both `⊆ A_doc^{Σ_0}`). K.λ's first-emission branch fires at `d_K`: `{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = d_K} = ∅` (since `dom(Σ_0.L) = ∅`). Result Σ_1 with τ_1 at address `a_1 = [d_K.0.s_L.1]` (ASN-0086). `emission_order(τ_1) = 0`.

**Emission C2.** `Emit_K(Σ_1, d_K, F_C2, G_C2)` with `F_C2 = {(d_witness', δ(1, #d_witness'))}` (different witness) and `G_C2 = G_C1` (same subject). Sh-conf admits. Result Σ_2 with τ_2 at address `a_2 = inc(a_1, 0)` (subsequent-emission branch). `emission_order(τ_2) = 1`.

**Emission C3.** `Emit_K(Σ_2, d_K, F_C3, G_C3)` with `F_C3 = F_C1` (original witness again) and `G_C3 = G_C1` (same subject). Coverage's `idem = ⊥` admits this even with identical slot-addresses to C1. Result Σ_3 with τ_3 at `a_3 = inc(a_2, 0)`. `emission_order(τ_3) = 2`.

**Template evaluation at Σ_3.**

`S_{d_subject} = {τ ∈ A_K^{Σ_3} : to₁(τ) = d_subject} = {τ_1, τ_2, τ_3}`.

`latest_K_for_addr(d_subject) = argmax_{τ ∈ S_{d_subject}} emission_order(τ) = τ_3` (chain-index 2).

Reading the witness off the returned tuple: `from₁(τ_3) = d_witness`. The consumer recovers both the latest assertion *and* its attribution.

If a fourth emission C4 occurs with subject `d_subject` from any witness, `latest_K_for_addr(d_subject)` advances to that new τ_4 (chain-index 3); previous tuples remain in `L_K` and `A_K` but are no longer "latest." Retracting τ_3 (issuing `Nullify(Σ_3, d_retr, a_3)`) yields Σ_4 with `A_K^{Σ_4} = {τ_1, τ_2}` and `latest_K_for_addr(d_subject) = τ_2` (chain-index 1, the maximum surviving).

### Tuple-Classifier

Register `K = endorsed` with shape `(0, 1, -, A_rel, ⊤)`, intended to mark comment-tuples as endorsed. Working from Σ_4 of the Comment example, with τ_2 ∈ A_rel^{Σ_4}. We reuse the home document `home_K` from the Comment example as the home for `endorsed` emissions — this exercises the framework's permission for multiple distinct relations to share a single home document. (The substrate's per-document link sub-allocator chain at `home_K` interleaves tuples of different types, with R0a-Cor1 ensuring each type's homed-set remains well-defined within the chain.) To disambiguate the symbol within this walkthrough, write `home_endorsed := home_K` for `endorsed`-emissions:

`Emit_K(Σ_4, home_endorsed, ∅, {(a_2, δ(1, #a_2))})` — F empty (matches `c_F = 0`), G targets the tuple address `a_2`. Sh-conf admits (clause (d) for F is vacuous since `-^Σ = ∅` and `slot_addrs(F) = ∅ ⊆ ∅`; G-side checks `{a_2} ⊆ A_rel^{Σ_4}`). Result Σ_4'.

Template evaluation: `is_K(a_2) ≡ (E σ ∈ A_K^{Σ_4'} :: to₁(σ) = a_2) = true`; `is_K(a_1) = false`. The same single-letter substitution `d ↝ τ` from Classifier's template body, with the signature shifted from `A_doc → Bool` to `A_rel → Bool`.

### Provenance (partial G-slot)

Register `K = attributed_by` with shape `(1, 0|1, A, A, ⊤)`. Let `home_prov ∈ dom(Σ.M)` be a fresh home document for `attributed_by` emissions (distinct from any prior walkthrough's home symbol; nothing in the framework forbids reusing a prior home, but we introduce a new symbol here to keep cross-walkthrough scopes disjoint). Two emission forms exercise the `0|1` partiality:

**Form 1 (with target):** `Emit_K(Σ, home_prov, {(s, δ(1, #s))}, {(t, δ(1, #t))})` with both `s, t ∈ A^Σ`. Sh-conf admits (canonical-slot, cardinality 1/1, `s ∈ A^Σ`, `t ∈ A^Σ`). Resulting τ has `from₁(τ) = s`, `to₁⁻(τ) = t` (defined).

**Form 2 (empty target):** `Emit_K(Σ, home_prov, {(s, δ(1, #s))}, ∅)` with `s ∈ A^Σ`. Sh-conf admits (G is canonical-slot trivially with `slot_addrs(∅) = ∅`; `match(0, 0|1)` holds since `0 ∈ {0, 1}`; clause (d) for G is vacuous since `slot_addrs(∅) = ∅` is a subset of any target domain). Resulting τ has `from₁(τ) = s`, `to₁⁻(τ) = ⊥` (undefined).

Template evaluation: `outgoing_K(s) = {τ ∈ A_K^Σ : from₁(τ) = s}` returns both forms; consumers that need to discriminate read `to₁⁻` on each result. `to₁⁻(τ) = ⊥` signals attribution-only events (e.g., agent recorded without a separate target); `to₁⁻(τ) ≠ ⊥` carries the attribution-target pair. Both shapes pass `from₁`'s total signature because `c_F = 1` always holds.

### Attributed Retraction (exercising `c_F = *`)

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

### Sh4 emission suppression (Tuple-Classifier, idem = ⊤)

To exhibit Sh4 suppression in action (independent of FDD), register `K = endorsed_v2` with shape `(0, 1, -, A_rel, ⊤)` (Tuple-Classifier, `idem = ⊤`). Working from a state Σ where `τ_target ∈ A_rel^Σ` is a target tuple-address and `home_endorsed_v2 ∈ dom(Σ.M)` is a fresh home document for `endorsed_v2` emissions (named per-relation to keep this walkthrough's scope disjoint from prior walkthroughs that bound `home_K`).

**Emission ENDX1.** `Emit_K(Σ, home_endorsed_v2, ∅, {(τ_target, δ(1, #τ_target))})`.

*Sh4 contract clause (i):* Compute `C(F, G, Σ)` via the two-step procedure. (i.a) `Observe_K(∅, {τ_target}, oper)` — the `slot_addrs(F) = ∅` pattern is vacuously contained in any F-coverage; the `{τ_target}` G-pattern selects tuples whose G-coverage contains τ_target. Result: ∅ (no prior K-tuples). (i.b) Post-filter vacuous. `C = ∅`.

*Sh4 contract clause (iii):* `C = ∅`, so emission proceeds. Sh-conf admits. Result Σ' with new tuple σ_1 at fresh address a_σ1.

*Active subset after ENDX1.* `A_K^{Σ'} = {σ_1}`. Template: `is_K(τ_target) = true`.

**Emission ENDX2 (suppressed by Sh4 contract clause (ii)).** From Σ', attempt the *same* emission again: `Emit_K(Σ', home_endorsed_v2, ∅, {(τ_target, δ(1, #τ_target))})` — identical slot-addresses to ENDX1.

*Sh4 contract clause (i):* Compute `C(F, G, Σ')`. (i.a) `Observe_K(∅, {τ_target}, oper)` returns `{σ_1}` (σ_1's G-coverage `{t : τ_target ≼ t}` contains τ_target). (i.b) Post-filter: σ_1 has `slot_addrs(F_{σ_1}) = ∅` and `slot_addrs(G_{σ_1}) = {τ_target}`, exactly matching the patterns. So `C = {σ_1} ≠ ∅`.

*Sh4 contract clause (ii):* `C ≠ ∅`, so the emission is *suppressed*. The layer returns `⊥`. No `↦`-step. State remains Σ'. `A_K^{Σ'} = {σ_1}` unchanged — exactly *one* active tuple, not two.

*Verification of Sh4.* `|A_K^{Σ'}| = 1`. The pairwise-distinctness condition over `A_K^{Σ'}` is vacuous off-diagonal (no two distinct active tuples to consider), and the diagonal `(σ_1, σ_1)` is trivially satisfied by reflexivity. Sh4 holds. Crucially, the framework preserved Sh4 by suppressing the duplicate emission attempt; under R0 (TupleAddressFreshness, ASN-0086) alone, the substrate would have admitted ENDX2 and produced `A_K = {σ_1, σ_2}` with both targeting τ_target — violating Sh4 because the slot-address pair `(∅, {τ_target})` would witness two distinct active tuples. The *Sh4 idempotency contract* is what makes Sh4 hold.

*Contrast with `idem = ⊥`.* Were `idem = ⊥` registered for the same shape (a hypothetical NonIdempotentTupleClassifier), ENDX2 would not be suppressed: the contract clauses (i)–(iii) are conditioned on `shape(K).idem = ⊤`. The second emission would land at a fresh address, and `A_K` would carry two distinct active tuples sharing the same slot-address pair — admissible under the non-idempotent reading where each emission records a distinct event.


## Consequences

(a) *Adding a new relation generates predicates for free.* A new K with `shape(K) = DirectedPair` immediately yields `pair_K`, `from_K`, `to_K`, `from_addrs_K`, and `to_addrs_K` — no per-relation predicate code is required. The cost of a new relation is one entry in the shape registry. Layers consuming an Attribute-style or Citation-style reading further define aliases (`has_K`, `K_sidecars_of`, `cites_K`, `K_incoming`) over the canonical names; the singleton-returning `K_target_of` (and its `K_sidecar_of` alias) becomes available when the layer additionally registers FunctionalDependencyDiscipline for that K.

(b) *Composite predicates extend the catalog through the same compositional primitives.* A composite predicate combines atomic templates through Boolean operators and quantification over `T_cat`. The framework does not establish a closure theorem about these primitives — whether composition can express predicates strictly beyond what the catalog's atomic templates yield is a property of the composition language adopted, not a structural guarantee of Sh5. The design observation we record is weaker: the canonical-shape catalog is the registry's *atomic* vocabulary, and adding a structurally new pattern (e.g., a slot-cardinality combination not yet present) is handled by extending the catalog with a new canonical shape, not by composing existing relations. Layer composites (e.g., `K_is_fresh`) extend the predicate language further by bringing in external accessors like `mtime`; these compose atop the framework but are not part of it.

(c) *Shape misregistration is a structural error.* Registering a relation with the wrong shape produces predicates with wrong signatures or wrong semantics — the substrate cannot self-correct this. By Sh-conf, attempts to emit non-conformant tuples are rejected, but the rejection assumes the registered shape is the *correct* shape; if the registry is wrong, the substrate enforces the wrong constraint. Shape registration is part of the relation's contract.

(d) *The predicate language is bounded by the shape catalog.* "What the substrate can ask" is determined by the templates the shapes generate. Questions about content quality ("is this proof complete?", "is this description good?") are not expressible because no canonical shape's template generates them. Those are agent-time questions, not substrate questions.


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| cov | DEF | Coverage projection `L_K → ℘(T) × ℘(T)` | introduced |
| cov_allocated | DEF | Allocated-coverage projection `(F, Σ) → coverage(F) ∩ A^Σ`; finite per Σ, monotone along `⊑̂` | introduced |
| canonical-slot form | DEF | Endset form `{(x, δ(1, #x)) : x ∈ X_F}` with extractable slot-address set | introduced |
| slot_addrs | DEF | Extraction `F ↦ X_F` for canonical-form F | introduced |
| AllocatedAddressAntichain | LEMMA | For every reachable Σ and every `x ∈ A^Σ`, `cov_allocated({(x, δ(1, #x))}, Σ) = {x}`; the element-level character of `A^Σ` is derived (L1 + L1b for the link side, scaffolding for the content side), so the bare `x ∈ A^Σ` hypothesis suffices | introduced |
| Sh_K | DEF | Shape: `(c_F, c_G, t_F, t_G, idem)` | introduced |
| ShapeWellFormedness | DEF | Syntactic well-formedness: four explicit implications `c_F = 0 ⟹ t_F = -`, `t_F = - ⟹ c_F = 0`, and symmetric pair for G; antecedents test the literal registry values `0` and `-` (distinct from `0|1`, `A_doc`, `A_rel`, `A`); registry admits only well-formed shapes; admits Provenance's `(1, 0|1, A, A, ⊤)` | introduced |
| match | DEF | Cardinality match predicate over `{0, 1, *, 0\|1}` | introduced |
| T_cat | DEF | Typed-relation catalog: distinguished `T_cat ⊆ T_admissible` up to `~`; lifetime-constant (fixed at `Σ_init` and unchanged across reachable states), enforcing the empty-baseline assumption of Sh0–Sh4 inductions | introduced |
| shape | DEF | Shape registry `T_cat → Shape`, per-class constant, lifetime-constant | introduced |
| conf_K^Σ | DEF | State-indexed conformance predicate; monotone along `⊑̂` | introduced |
| from_K^Σ, to_K^Σ | DEF | Total set-valued slot accessors | introduced |
| from₁, to₁ | DEF | Point-valued slot accessors (defined when c = 1) | introduced |
| from₁⁻, to₁⁻ | DEF | Optional point-valued slot accessors (defined when c = 0\|1) | introduced |
| Sh-conf | AXIOM | ShapeConformanceAxiom — Emit_K (relational-layer op) rejects unregistered types and non-conformant emissions; binds Emit_K, not K.λ; returns `⊥` on failure (extended return type `(Σ' × A_rel^{Σ'}) ∪ {⊥}`) | introduced |
| RetractionTargetNotOnChain | LEMMA | At any state Σ reachable from `Σ_init` under the *Emit_K routing commitment*, every `b ∈ dom(Σ.L)` paired with every `d ∈ dom(Σ.M)` satisfies `b ⋠ a_emit(Σ, d)`. Generalized to arbitrary link-store addresses (not just retraction-tuple G-slot witnesses) so that both consumption sites in the EffectiveWpSimplification Corollary — discharging `NoCraftedSpanReachesD(Σ, d)` for prior R-tuples and discharging the `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` disjunct's `K ~ R` arm for the new emission's G — fall under one statement. Case split: per-home distinctness via the *Uniform link sub-allocator chain length* scaffolding clause + T10a.7 + T3; cross-home distinctness via L1 + L1a's home-from-zero-positions reading, with the *Document address structure* scaffolding clause supplying `zeros(d) = 2`, the *Link subspace partition* scaffolding clause's `s_L > 0` securing the first-emission `zeros = 3` count, and inline zero-count additivity over prefix decomposition (NAT-card + componentwise agreement under Prefix). | introduced |
| EffectiveWpSimplification | COROLLARY | Under the framework's *Emit_K routing commitment*, `wp_086` simplifies to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible` and the effective wp under Sh-conf simplifies to `d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)`. Established immediately after Lemma — RetractionTargetNotOnChain so downstream proofs cite a named result rather than the preliminary derivation in the Sh-conf section's preview. Proof body now splits into two explicit steps: Step 1 discharges `NoCraftedSpanReachesD` by applying the Lemma at each prior R-tuple's G-slot address; Step 2 case-splits on `K ≁ R` vs `K ~ R` and, in the `K ~ R` case, applies the Lemma at the *new* emission's G-slot address (legal under the Lemma's generalization). | introduced |
| Sh0 | LEMMA | FromSlotCanonicalAndCardinalityFixed — proof covers both `→` and `↦ \ →`, via the *Emit_K routing commitment* | introduced |
| Sh1 | LEMMA | ToSlotCanonicalAndCardinalityFixed — G-side analog of Sh0; proof exhibits Sh-conf clauses (b) and (c) at the substituted sites | introduced |
| Sh2 | LEMMA | FromSlotTargetRestricted — `slot_addrs(F) ⊆ t_F^Σ` on every tuple | introduced |
| Sh3 | LEMMA | ToSlotTargetRestricted — symmetric to Sh2; commutes with retraction (`A_K ⊆ L_K`) | introduced |
| SlotAccessorTotality | LEMMA | When `c = 1`, the point accessor is a total function | introduced |
| Sh4 | LEMMA | IdempotencyDiscipline — at-most-one active duplicate when `idem = ⊤`; theorem under the *Sh4 idempotency contract* (single-process substrate scope: atomicity of clauses (i)–(iii) reduces to within-call sequentiality between `Observe_K` and the substrate K.λ-step); universal scope clarified (off-diagonal substance, diagonal trivial); proof covers A/B/C plus Case D (K=R simultaneous addition and contraction); Case A simplified to rely on the case-equation `A_K^{Σ'} = A_K^Σ` alone, with the principal-transitions enumeration retained as expository orientation rather than a load-bearing case analysis | introduced |
| Sh5 | META | TemplateCatalog — hand-curated per-shape template families; status split into META observation (no procedure derives templates from arbitrary shapes) and META discipline (templates depend only on shape + K's name + named accessors); base/opt-in/parametric criterion formalized | introduced |
| SingleHomeCoverageDiscipline | DEF | Per-K commitment securing `emission_order` for Coverage instantiations of NonIdempotentDirectedPair; allows non-K relations at the same home as long as K is single-home; realized through the *single-home commitment* layer-discipline contract | introduced |
| single-home commitment | DEF | The layer-discipline contract realizing SingleHomeCoverageDiscipline. Single-step protocol: rejects `Emit_K(Σ, d, F, G)` outright when `d ≠ d_K`; admits when `d = d_K`. No Observe step required (home check is literal-equality against a per-K registration constant); atomicity trivial. Preservation theorem establishes the homed-set commitment `(A τ ∈ L_K^Σ :: home(addr(τ)) = d_K)` inductively, with Case A/B/C structure analogous to Sh4 and FDD; companion property `S_d ⊆ {chain elements at d_K}` follows for every `d ∈ A_doc^Σ` | introduced |
| FunctionalDependencyDiscipline | DEF | Per-K commitment (strictly stronger than Sh4) for DirectedPair: at most one active tuple per from-slot value; secures the singleton-returning `K_target_of` accessor | introduced |
| Sh4 idempotency contract | DEF | The layer-discipline contract realizing Sh4. Observe-then-Emit protocol clauses (i)–(iii) the layer commits to for idempotent K; clause (i) uses the two-step procedure (i.a) finite-argument `Observe_K(slot_addrs(F), slot_addrs(G), oper)` over-approximation + (i.b) exact-slot-equality post-filter; atomically scoped at the `~`-equivalence class of K | introduced |
| FDD functional-dependency contract | DEF | The layer-discipline contract realizing FunctionalDependencyDiscipline. Observe-then-Emit protocol with from-slot-only candidate set `C_fd`; same two-step procedure as the *Sh4 idempotency contract*; same atomicity scope as Sh4; structurally exclusive with SingleHomeCoverageDiscipline by `idem` flag | introduced |
| substrate-conforming-layer scaffolding | ASSUMPTION | Element-level content addresses, content subspace partition (`s_C > 0`, `s_C ≠ s_L`), link subspace partition (`E(a).1 = s_L` with `s_L > 0` for every `a ∈ dom(Σ.L)`; concrete realization of L0's abstract `subspace_I(·)` as `E(·).1`; positivities forced by the element-level `zeros = 3` clauses on each side), content-store antichain, content-store monotonicity, content-store finiteness, document address structure (`zeros(d) = 2`), per-document link sub-allocator chains, uniform link sub-allocator chain length, link sub-allocator chain-index function (`chain_index(ℓ, d) ∈ ℕ` with `ℓ = inc^{chain_index(ℓ, d)}(d.0.s_L.1, 0)`, single-valued by T10a.7) — assumed of the substrate-conforming layer; surfaced as named scaffolding clauses for direct citation, with attribution to specific upstream numbered invariants kept inside the layer's interface. (Earlier drafts called this *content-side scaffolding*; the union spans both link-side, content-side, and document-side properties, so the name has been retired in favor of the substrate-conforming-layer reading.) | introduced |
| Emit_K routing commitment | ASSUMPTION | Every class-(iii) emission of `K ∈ T_cat` routes through `Emit_K`; the framework's foundational commitment from which the other named commitments (*Sh4 idempotency contract*, *FDD functional-dependency contract*, *single-home commitment*) are distinguished. Subsequent prose cites this commitment by name to disambiguate from the four other framework commitments | introduced |


## Open Questions

- Should `(0, 0)` shapes be admitted? A relation with `c_F = c_G = 0` would be a single-tuple existence flag whose only role is "this event happened" without any from/to attribution; whether the substrate has any such relations is unclear, and the slot accessors degenerate to constants on it.
- Provenance's `c_G = 0|1` mixes shapes — should it be split into two distinct canonical shapes (Provenance-with-target and Provenance-attribution-only), each generating separate templates? The current formulation requires the optional accessor `to₁⁻` to handle both cases in a single template.
- Is idempotency recoverable from cardinality plus target-domain alone, or is it an independent axis? Empirically the canonical catalog has both `idem = ⊤` (DirectedPair) and `idem = ⊥` (Coverage, Comment) at `(1, 1, A_doc, A_doc, _)`, suggesting independence.
- Should the per-K opt-in registry — currently FunctionalDependencyDiscipline and SingleHomeCoverageDiscipline — be promoted to a sixth shape-tuple component, so that registrations with and without the discipline become structurally distinct rows rather than the same row with different opt-in flags? The current catalog encodes them as opt-in extensions atop a five-component shape; a sixth component would make the shape registry exhaustive but inflate the canonical-shape space considerably.
- The shape constraint `slot_addrs(F) ⊆ t_F^Σ` requires slot addresses to be already-allocated at emission time. This precludes shape-conformant emissions whose slot addresses are *ghost* (currently outside `A^Σ`, possibly to be allocated later). L9 (TypeGhostPermission, ASN-0043) permits ghost spans in endsets; the shape framework restricts this to *non-slot* uses only. Whether future shape families should admit ghost-targeting slot semantics — and under what state-dependent conformance rule — is an open design question.
- Do *composite shapes* (relations whose F or G is itself constrained by another relation's content) require a new restriction axis, or do they decompose into existing primitives plus auxiliary predicates expressible in the current template language?
- What guarantees the shape registry stays consistent across processes? Lifetime constancy is asserted as a substrate-level commitment within a single process; cross-process consistency (e.g., concurrent shape re-registration in a distributed substrate) is not addressed. Relatedly, the *Sh4 idempotency contract* is scoped to single-process substrates — its atomicity premise reduces to within-call sequentiality between `Observe_K` and the substrate K.λ-step within a single `Emit_K` call. Multi-process substrates with racing Sh4-emitters at coverage-equivalent K's would require a coordination protocol (e.g., distributed lock at the `~`-equivalence class scope) not specified by this framework; characterizing the minimum protocol that preserves Sh4 in the multi-process setting is open.
