# ASN-0086 Claim Statements

*Source: ASN-0086-typed-relations-on-address-sets.md (revised unknown) — Extracted: 2026-05-19*

---

## Definition — ZeroCountDepth

The *zero-count depth* of a tumbler `t` relative to its prefix `s ≼ t` is `zeros(t) − zeros(s)`. A child-spawn `(d, k')` with `k' ≥ 1` produces a child whose zero count exceeds `zeros(d)` by `k' − 1` (TA5 postcondition (d)), so the zero-count depth of the spawn relative to `d` is exactly `k' − 1`.

---

## Definition — AllocatorTreeDepth

The *allocator-tree depth* of an allocator A relative to a document `d ∈ dom(Σ.M)` is the number of T10a child-spawn pairs `(·, k')` with `k' ∈ {1, 2}` on ASN-0093's structural chain from `d` to A's base address (i.e., to A's first emission). A `(·, 1)` child-spawn opens a new allocator without introducing a new zero (TA5 with `k' = 1` gives `zeros` unchanged), so it advances the allocator hierarchy by one level without advancing zero-count depth.

---

## Definition — Extension

`Σ' extends Σ`, written `Σ ⊑ Σ'`, is the reflexive-transitive closure of `→`:

`Σ ⊑ Σ' ≡ Σ →* Σ'`

`Σ ⊑ Σ'` entails `dom(Σ.C) ⊆ dom(Σ'.C)`, `dom(Σ.M) ⊆ dom(Σ'.M)`, `dom(Σ.L) ⊆ dom(Σ'.L)`, with `Σ'.C|_{dom(Σ.C)} = Σ.C`, `Σ'.M|_{dom(Σ.M)} = Σ.M`, `Σ'.L|_{dom(Σ.L)} = Σ.L`.

---

## Definition — BroadExtension

`Σ ⊑̂ Σ'` is the reflexive-transitive closure of `↦` (the broader transition relation including arrangement modifications):

`Σ ⊑̂ Σ' ≡ Σ ↦* Σ'`

Every `Σ ⊑ Σ'` entails `Σ ⊑̂ Σ'` (since `→ ⊆ ↦`). Every arrangement-modifying step holds `Σ.C` and `Σ.L` identical and changes only `Σ.M`'s pointwise values.

---

## Definition — RetractionType

Fix a designated coverage class `[R]` reserved for retraction, represented by any `R ∈ T_admissible` whose coverage selects the conventional retraction address set. The corresponding typed relation `L_R^Σ` is the *retraction relation at state Σ*. Before the first retraction emission, `L_R^Σ = ∅`. By coverage-equivalence, any emission with a type endset `R'` satisfying `coverage(R') = coverage(R)` contributes to `L_R^Σ` and to `nullified(Σ)`.

---

## Definition — RetractionDirectionality

For the retraction coverage class `[R]`, the to-set carries the retraction's targets — addresses whose tuples are being withdrawn from the active subset — and the from-set is reserved for attribution-bearing endset content or is left empty for unattributed retractions.

---

## Definition — SubstrateConformingLayer

A layer is *substrate-conforming* iff every operation it publishes over `(Σ.C, Σ.M, Σ.L)` preserves both of the following catalogs at every step.

*(a) Invariant Catalog.* The full L/S/M/C invariant list of ASN-0036, ASN-0043, and ASN-0093:
- *ASN-0043 link-store invariants:* L0, L1, L1a, L1b, L1c, L2, L3, L5, L6, L8, L11a, L12, L12a, L12b, L13, L14, L14a, L-fin.
- *ASN-0036 content/arrangement invariants:* S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ.
- *ASN-0093 substrate invariants:* M0, M1, C0, C1, C1b, C1c, C-fin.

*(b) Chain Discipline Catalog.* SubAllocatorAxiom, ChainMembershipForOrigin, ChainEnumerationInjectivity, ChainUniformLength, ChainUniformZeroCount, ChainPrefixExtension, ChainElementT4Validity, DisjointSubAllocatorChains, StoreT4Validity, FirstEmissionFreshness, CrossDocDisjointness.

Catalog (b) is *strictly stronger* than catalog (a): L1c admits non-chain T10a-conforming chains (e.g., `a* = [d.0.s_L.1.1]`, which is L1c-admissible but off `A_L(d)`'s sibling-frontier chain); without catalog (b), a layer could publish an L-invariant-conforming non-chain emission that has no K.λ-replay.

---

## Definition — EmitKFunctionNess

`Emit_K` is a function: given `(Σ, d, F, G, K)`, the output `(Σ', a)` is uniquely determined.

K.λ's first/subsequent emission rule is deterministic in `(Σ, d)`:
- First-emission branch: `a = [d.0.s_L.1]` (deterministic projection of `d`).
- Subsequent-emission branch: `ℓ_prev = max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` — a unique extremum because, by R0a-Cor1, the homed set is a contiguous prefix of `A_L(d)`'s chain enumeration and so admits a unique maximum under T1 (LexicographicOrder, ASN-0034). Then `a = inc(ℓ_prev, 0)`.

---

## Definition — FreshEmissionAddress

For `d ∈ dom(Σ.M)`, the *fresh emission address* `a_emit(Σ, d)` is the address K.λ would deposit at home `d` in state Σ:

`a_emit(Σ, d) = [d.0.s_L.1]` when `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅` (first-emission branch);

`a_emit(Σ, d) = inc(ℓ_prev, 0)` otherwise, where `ℓ_prev := max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` (subsequent-emission branch).

The address that `Emit_K(Σ, d, F, G)` deposits is exactly `a_emit(Σ, d)`; the type-index `K` parameterizes the slot-3 value, not the address selection.

---

## Definition — NoCraftedSpanReachesD

`NoCraftedSpanReachesD(Σ, d) ≡ (A (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∉ coverage(G'))`

---

## Definition — WeakestPreconditionNullify

`wp(Nullify(Σ, d_retr, a), single-tuple scope at Σ') ≡ P0(Σ, d_retr) ∧ P1(Σ, a) ∧ P2(Σ, a)`

where:
- P0: `d_retr ∈ dom(Σ.M)`
- P1: `a ∈ A_rel^Σ`
- P2: `|Σ.L(a)| = 3`

Single-tuple scope postcondition: `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`.

---

## Definition — WeakestPreconditionEmitK

`wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ NoCraftedSpanReachesD(Σ, d) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`

Under the unit-depth retraction discipline (regime (i)), `NoCraftedSpanReachesD` is automatic, and the wp simplifies to:

`d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`

Under the relational layer's committed operations, both regime (ii) and (iii) are structurally impossible, and the wp simplifies definitionally to:

`d ∈ dom(Σ.M) ∧ K ∈ T_admissible`

---

## SharedDepthOneAllocator — SharedDepthOneAllocator (LEMMA, lemma)

Under each document address `d ∈ dom(Σ.M)`, T10a admits at most one allocator at allocator-tree depth 1 below `d` whose outputs sit at zero-count depth 1 relative to `d` — written `A_{d.0.1}` and opened by the `(d, 2)` child-spawn. When opened, this allocator is shared across all subspaces: its enumeration `d.0.1, d.0.2, d.0.3, …` indexes subspace identifiers, with position `s_C` landing in the content subspace and position `s_L` in the link subspace by ASN-0093 L0 (SubspacePartition). The subspace-specific sub-allocators ASN-0093 names — `A_C(d) = A_{d.0.s_C.1}` (anchored at `b_C(d)`) and `A_L(d) = A_{d.0.s_L.1}` (anchored at `b_L(d)`) — sit at allocator-tree depth 2, opened by `(d.0.s_C, 1)` and `(d.0.s_L, 1)` respectively.

Sub-claims:
*(a)* The only T10a-admissible child-spawns from `d` are `(d, 1)` and `(d, 2)`. Document addresses have `zeros(d) = 2` by S7d and M0. By TA5 postcondition (d), `zeros(inc(d, k')) = 2 + (k' - 1)` for `k' ≥ 1`; T4's cap `zeros ≤ 3` forces `k' ∈ {1, 2}`.

*(b)* Only `(d, 2)` opens an allocator at zero-count depth 1. By TA5(d), `(d, 1)` yields `zeros = 2` — zero-count depth 0 relative to `d`. `(d, 2)` yields `zeros = 3` — zero-count depth 1, the unique spawn introducing a new zero.

*(c)* Uniqueness via T10a at-most-once. T10a's at-most-once axiom on `(d, 2)` makes the allocator opened by `(d, 2)`, if opened at all, unique under `d`.

---

## A^Σ — AddressUniverse (DEF, definition)

The substrate's address universe at state Σ is

`A^Σ = dom(Σ.C) ∪ dom(Σ.L)`

---

## A_doc^Σ, A_rel^Σ — AddressPartition (DEF, definition)

`A_doc^Σ = dom(Σ.C)` — content addresses

`A_rel^Σ = dom(Σ.L)` — relation-tuple addresses

Claim: `A^Σ = A_doc^Σ ⊔ A_rel^Σ` (disjoint union). The disjointness is R4.

---

## T_ghost^Σ — GhostAddresses (DEF, definition)

The *ghost addresses* at state Σ are the tumblers outside the stored-entity universe:

`T_ghost^Σ = T \ (dom(Σ.C) ∪ dom(Σ.L))`

By L9 (TypeGhostPermission, ASN-0043), ghost addresses may appear in endset spans (including type-endset coverage) without contradiction.

---

## T_admissible — AdmissibleTypes (DEF, definition)

The set of *admissible types* is

`T_admissible = {K ∈ Endset : K ≠ ∅}`

— non-empty endsets, eligible to serve as a link's type endset by L3 (NEndsetStructure, ASN-0043).

---

## ~ — TypeEquivalence (DEF, definition)

Two admissible types are *type-equivalent* iff they cover the same address set:

`K ~ K' ≡ coverage(K) = coverage(K')`

The quotient `T_admissible / ~` is the set of *coverage classes*; the equivalence class of `K` is written `[K]`. Two `K, K' ∈ T_admissible` with `K ~ K'` induce the same slice: `L_K^Σ = L_{K'}^Σ` as sets.

---

## L_K^Σ — TypedRelation (DEF, definition)

For each `K ∈ T_admissible` and state Σ, the *typed relation of type K at Σ* is

`L_K^Σ = {(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a).e₁ = F ∧ Σ.L(a).e₂ = G ∧ coverage(Σ.L(a).e₃) = coverage(K)}`

Each member is a triple of (tuple-address, from-endset, to-endset). The pair `(F, G)` is the *relational content* of the tuple; `a` is the *tuple address*. The subscript `K` is a coverage-class index: `L_K^Σ = L_{K'}^Σ` whenever `K ~ K'`.

---

## L^Σ — StandardTripleLinkStore (DEF, definition)

The substrate's standard-triple link store at state Σ is the disjoint union over coverage classes:

`L^Σ = ⨆_{[K] ∈ T_admissible / ~} L_K^Σ`

`L^Σ` collects only the arity-3 links; higher-arity links in `dom(Σ.L)` are outside its scope.

---

## addr — TupleAddress (DEF, definition)

Define `addr : L^Σ → A_rel^Σ` by `addr(a, F, G) = a`.

---

## nullified(Σ) — NullifiedSet (DEF, definition)

The set of *nullified* tuple addresses at state `Σ` is

`nullified(Σ) = {a ∈ A_rel^Σ : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))}`

The existential checks `coverage(G')` only — the to-set's coverage — and does not inspect `coverage(F')`. The quantification ranges over `L_R^Σ` (audit slice), not `A_R^Σ` (active subset).

---

## A_K^Σ — ActiveSubset (DEF, definition)

For each `K ∈ T_admissible`, the *active subset of type K at state Σ* is

`A_K^Σ = {(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}`

`A_K^Σ` is computable from `Σ.L` alone.

---

## → — DomExtendingTransition (DEF, definition)

`→ ≡ K.σ ∪ K.α ∪ K.λ`

Each `→`-step is one of:
- *K.σ-step* (class (i)): document registration, extending `dom(Σ.M)` with a fresh document address `d` satisfying `T4-valid(d) ∧ zeros(d) = 2` and registering `M'(d) = ∅`.
- *K.α-step* (class (ii)): content allocation, extending `dom(Σ.C)` with a fresh content address `a` produced by `d`'s content sub-allocator `A_C(d)` for some `d ∈ dom(Σ.M)` (first-emission `a = [d.0.s_C.1]` or subsequent-emission `a = inc(a_prev, 0)`).
- *K.λ-step* (class (iii)): link allocation, extending `dom(Σ.L)` with a fresh link address `ℓ` produced by `d`'s link sub-allocator `A_L(d)` for some `d ∈ dom(Σ.M)` (first-emission `ℓ = [d.0.s_L.1]` or subsequent-emission `ℓ = inc(ℓ_prev, 0)`).

ASN-0093's frame conditions on each K-op ensure the two non-affected stores are preserved pointwise, and the affected store is extended by exactly one fresh key per step.

---

## Unit-depth retraction discipline — UnitDepthRetractionDiscipline (COMMITMENT, commitment)

A layer satisfies the *unit-depth retraction discipline* iff every `L_R^Σ` tuple, in every state Σ the layer reaches, has a to-endset of the form `{(b, δ(1, #b))}` for some target `b ∈ A_rel^Σ` — equivalently, every `L_R^Σ` tuple was produced by a `Nullify(Σ, d_retr, b)` call.

Under this discipline, `NoCraftedSpanReachesD(Σ, d)` holds automatically at every `Emit_K` call site, by R0a's antichain on `dom(Σ'.L)`.

---

## R0 — TupleAddressFreshness (LEMMA, lemma)

For any state Σ with `dom(Σ.M) ≠ ∅` and any `(F, G, K) ∈ Endset × Endset × T_admissible`, there exists a state Σ' with Σ → Σ' that emits a tuple with content (F, G) of type K at a fresh address:

`(A Σ : dom(Σ.M) ≠ ∅ :: (A F, G ∈ Endset, K ∈ T_admissible :: (E Σ' extending Σ, a : a ∉ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K))))`

Freshness against same-home chain elements, cross-home links, and content addresses decomposes into three sub-claims:
*(a)* Distinctness from same-home chain elements: by ChainEnumerationInjectivity at chain indices of `A_L(d)`, `a = inc(ℓ_prev, 0)` is strictly greater than every prior chain element.
*(b)* Distinctness from `dom(Σ.L)` elements homed at `d' ≠ d`: by CrossDocDisjointness, link sub-allocator anchors `b_L(d)` and `b_L(d')` are prefix-incomparable, so by T10 every address extending `b_L(d)` differs from every address extending `b_L(d')`.
*(c)* Distinctness from `dom(Σ.C)`: by DisjointSubAllocatorChains, `A_L(d)`'s outputs satisfy `E(·)₁ = s_L`; by ASN-0093 L0, every `a' ∈ dom(Σ.C)` has `E(a')₁ = s_C`; by SC-NEQ, `s_C ≠ s_L`.

---

## R0a — FlatLinkDomain (LEMMA, lemma)

At every reachable state Σ, `dom(Σ.L)` is a tumbler-prefix antichain:

`(A Σ : Σ reachable from Σ_init :: (A a, a' ∈ dom(Σ.L) :: a ≼ a' ⟹ a = a'))`

Under the K.λ contract of ASN-0093, R0a is unconditional: K.λ's first/subsequent emission rule, together with ASN-0093's sub-allocator chain axioms, enforce the sibling-frontier discipline as part of the substrate's class-(iii) primitive.

Proof decomposes by case:

*Case 1 — Cross-home (`home(a) ≠ home(a')`).* Suppose `a ≼ a'`; then `a' = a · w` for suffix `w`. By L1, `zeros(a) = zeros(a') = 3`, so `zeros(w) = 0`. By L1a's NUDE-prefix projection, the three zeros of `a'` sit at positions `≤ #a` coinciding with those of `a`, hence `home(a') = home(a)` — contradiction. Symmetric argument for `a' ≼ a`. Both directions excluded, so `a ≼ a' ⟹ a = a'` holds vacuously.

*Case 2 — Same-home (`home(a) = home(a') = d`).* By ChainMembershipForOrigin (ASN-0093), both `a` and `a'` are chain elements of `A_L(d)`. By ChainUniformLength, `#a = #a'`. If `a ≼ a'`, then `a` and `a'` coincide pointwise, so `a = a'` by T3.

---

## R0a-Cor1 — ContiguousPrefix (LEMMA, lemma)

At every reachable state Σ, for every `d ∈ dom(Σ.M)` there exists `J_d^Σ ∈ ℤ_{≥-1}` such that:

`(A Σ : Σ reachable from Σ_init :: (A d ∈ dom(Σ.M) :: (E J_d^Σ ∈ ℤ_{≥-1} :: {a ∈ dom(Σ.L) : home(a) = d} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ})))`

(with `J_d^Σ = -1` denoting the empty set when no link is homed at `d`).

Substantive postconditions:
*(a)* When `J_d^Σ ≥ 0` (non-empty homed-set), `max{a ∈ dom(Σ.L) : home(a) = d}` under T1 is well-defined and equals `inc^{J_d^Σ}(d.0.s_L.1, 0)`, the chain element at chain index `J_d^Σ`.
*(b)* `J_d^Σ = -1` absorbs the empty case; downstream consumers may reference `J_d^Σ + 1` as "next chain index" uniformly without case-splitting on emptiness.

---

## R0a-Cor2 — DepthTwoLinkAddresses (LEMMA, lemma)

At every reachable state Σ, every link address in `dom(Σ.L)` has an element field (T4b's `E` projection) of length exactly 2:

`(A Σ : Σ reachable from Σ_init :: (A a ∈ dom(Σ.L) :: #E(a) = 2))`

(This tightens L1b's substrate-level admission `#E ≥ 2` to `#E = 2` strictly.)

---

## R1 — AddressInjectivity (LEMMA, lemma)

The map `addr : L → A_rel` is an injection:

`(A (a, F, G), (a', F', G') ∈ L : a = a' :: F = F' ∧ G = G' ∧ both belong to the same coverage-class slice L_{[K]})`

---

## R2 — TupleAddressPermanence (LEMMA, lemma)

Once allocated, a tuple address resolves permanently to the same relational content:

`(A Σ → Σ', a ∈ dom(Σ.L), (F, G, K) = Σ.L(a) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K))`

---

## R3 — TypedSliceMonotonicity (LEMMA, lemma)

Each typed relation grows monotonically:

`(A Σ → Σ', K ∈ T_admissible :: L_K^Σ ⊆ L_K^{Σ'})`

---

## R4 — TupleAddressDisjointness (LEMMA, lemma)

Tuple addresses and document-content addresses are disjoint:

`A_doc^Σ ∩ A_rel^Σ = ∅`

---

## R5 — TupleSelfTargeting (LEMMA, lemma)

For any state Σ and any `a ∈ A_rel^Σ`, the unit-depth span `(a, δ(1, #a))` is well-formed and may appear in the from-set or to-set of an emitted tuple, with `a` in its coverage.

*(Step 1 — Span well-formedness.)* By L1, `zeros(a) = 3`; by L1b, `#E(a) ≥ 2`, so `#a ≥ 1`. By OrdinalDisplacement (ASN-0034), `δ(1, #a) = [0, …, 0, 1]` is a positive tumbler of length `#a` with action point `#a`. The span `(a, δ(1, #a))` satisfies T12 (SpanWellDefinedness). `actionPoint(δ(1, #a)) = #a ≤ #a`. By PrefixSpanCoverage, `coverage({(a, δ(1, #a))}) = {t : a ≼ t}`, which contains `a` by reflexivity of `≼`.

*(Step 2 — Endset admissibility.)* By L4(c), endset spans may reference link-subspace addresses. By L13 (ReflexiveAddressing) applied at `b = a`, the unit-depth span `(a, δ(1, #a))` is the canonical reference span for `a`. The singleton endset `G_self = {(a, δ(1, #a))}` is an admissible `Endset` member at any slot of an emitted link.

*(Step 3 — To-set case.)* The triple `(∅, G_self, K)` is L3-conforming: arity 3, `∅ ∈ Endset`, `G_self ∈ Endset` (from Step 2), `K ∈ T_admissible` non-empty. By R5-Cor at home `d ∈ dom(Σ.M)`, R0 emits at a fresh `a'` with `Σ'.L(a') = (∅, G_self, K)` and `a ∈ coverage(Σ'.L(a').e₂)`.

*(Step 4 — From-set case.)* The triple `(G_self, ∅, K)` is L3-conforming by the same checks. R5-Cor yields fresh `a''` with `a ∈ coverage(Σ''.L(a'').e₁)`.

---

## R5-Cor — EmitContentUniformity (LEMMA, lemma)

For any state Σ with `dom(Σ.M) ≠ ∅`, any `d ∈ dom(Σ.M)`, and any L3-conforming triple `(F, G, K)` — i.e., `F, G ∈ Endset` and `K ∈ T_admissible` (non-empty) — R0's emission and L-invariant verification proceed identically regardless of what addresses the endset spans target:

`(A Σ : dom(Σ.M) ≠ ∅ :: (A d ∈ dom(Σ.M), F, G ∈ Endset, K ∈ T_admissible :: (E Σ' extending Σ, a : a ∉ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K))))`

with no constraint on `coverage(F)`, `coverage(G)`, or `coverage(K)` beyond L3's well-formedness.

---

## R6a — RetractionStability (LEMMA, lemma)

Once a tuple's address is nullified, it stays nullified across all future state transitions:

`(A Σ → Σ', a ∈ A_rel^Σ : a ∈ nullified(Σ) :: a ∈ nullified(Σ'))`

Note: `coverage : Endset → ℘(T)` is a pure function on endset values, fixed by the substrate model; `coverage(E)` does not depend on the state Σ in which `E` is evaluated.

---

## R6b — SingleDepthRetraction (DEF-Consequence, def-consequence)

Retraction-of-retraction is not a fixpoint operation: an `Emit_R` call whose to-coverage targets a retractor `b` does not "undo" `b`'s nullifying effect on its prior targets. The decision procedure for `a ∈ nullified(Σ)` is *flat* — a single set-membership test independent of any retraction-chain depth in `L_R^Σ`, and unaffected by whether any witnessing retractor `b` is itself nullified:

`a ∈ nullified(Σ) ⟺ (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))`

The two possible readings:
*(i) Audit-slice reading (adopted):* the existential ranges over `L_R^Σ`. Witness `b`'s own status is never consulted. Decidable in time proportional to `|L_R^Σ|`.
*(ii) Active-subset reading (not adopted):* the existential would range over `A_R^Σ`, making deciding `a ∈ nullified(Σ)` depend recursively on `b ∉ nullified(Σ)` — a fixpoint computation with no fixed bound.

Consequence: attempting to "un-nullify" `a` by emitting `Nullify(b)` for retractor `b` has no effect on `a ∈ nullified(Σ')`: the original retraction tuple `(b, F', G') ∈ L_R^Σ ⊆ L_R^{Σ'}` (by R3), and `a ∈ coverage(G')` still witnesses `a ∈ nullified(Σ')` regardless of `b`'s status.

---

## R6c — RestorationByReemission (LEMMA, lemma)

Once retracted, a tuple stays out of every active subset at any state reachable from Σ:

`(A Σ, K, (a, F, G) ∈ L_K^Σ : a ∈ nullified(Σ) : (A Σ' : Σ ⊑ Σ' :: (a, F, G) ∉ A_K^{Σ'}))`

---

## LinkStoreInvarianceUnderArrangement — LinkStoreInvarianceUnderArrangement (LEMMA, lemma)

Under any arrangement-modifying transition `Σ ↦ Σ'` in `↦ \ →`, `Σ'.L = Σ.L` pointwise. Consequently, for every `K ∈ T_admissible`:

`L_K^{Σ'} = L_K^Σ`

`L_R^{Σ'} = L_R^Σ`

`nullified(Σ') = nullified(Σ)`

`A_K^{Σ'} = A_K^Σ`

Iterating along any `↦*`-chain composed entirely of arrangement-modifying steps yields the same pointwise equalities at the endpoint.

---

## R6c-Corollary — RestorationByReemissionBroad (LEMMA, lemma)

R6c's conclusion extends from `⊑` to `⊑̂`:

`(A Σ, K, (a, F, G) ∈ L_K^Σ : a ∈ nullified(Σ) : (A Σ' : Σ ⊑̂ Σ' :: (a, F, G) ∉ A_K^{Σ'}))`

---

## R7a — NoExtraClassAffectsL (LEMMA, lemma)

For any state-affecting transition `Σ ↝ Σ'` issued by a substrate-conforming layer with `Σ.L ≠ Σ'.L`, there exists a finite sequence `Σ = Σ_0 → Σ_1 → … → Σ_m` (`m ≥ 1`) of `→`-steps, each of class (i) or (iii), with:

`Σ_m.L = Σ'.L`

`dom(Σ_m.M) ⊆ dom(Σ'.M)`

`dom(Σ_m.C) = dom(Σ.C) ⊆ dom(Σ'.C)`

(no class-(ii) content-emission steps are introduced).

Precondition: the layer is substrate-conforming per the Definition of *substrate-conforming layer*, comprising catalogs (a) and (b).

Construction: Let `Δ := dom(Σ'.L) \ dom(Σ.L)` (finite, non-empty by L-fin + L12 + L12a). Enumerate `Δ = {a_1, …, a_n}` re-ordered so that fresh addresses homed at the same `d_k` appear in chain-order by R0a-Cor1. For each `k ∈ {1, …, n}`, set `d_k := home(a_k)` and `(F_k, G_k, K_k) := Σ'.L(a_k)`. If `d_k ∉ dom(Σ_{prev}.M)`, prefix a K.σ-step (Frame: `Σ_{prev}'.L = Σ_{prev}.L`, `Σ_{prev}'.C = Σ_{prev}.C`). Then issue a K.λ-step emitting `(F_k, G_k, K_k)` at `a_k`.

K.λ precondition discharge at each iteration:
*(1)* Freshness `a_k ∉ dom(Σ_{prev}'.L)`: K.σ-prefix held `Σ_{prev}'.L = Σ_{prev}.L = Σ.L ∪ {a_1, …, a_{k-1}}`; `a_k` is distinct from each by Δ-enumeration.
*(2)* L0/L1/L1b at `a_k`: state-independent structural predicates over `a_k`, inherited from Σ'.
*(2/3)* L1a at `a_k`: `home(a_k) = d_k ∈ dom(Σ_{prev}'.M)` by K.σ-prefix (if needed) or case hypothesis.
*(4)* First/subsequent emission rule selects `a_k`:
- *(i)* Chain-order existence: by catalog (b) preserved to Σ', R0a-Cor1 gives the homed set at `d_k` as a contiguous initial segment of `A_L(d_k)`'s chain enumeration.
- *(ii)* Cross-home iteration order is immaterial: K.λ's predicate is origin-scoped to `d_k`.
- *(iii)* Iteration in chain-order at each home selects `a_k`:
  - *Case A (fresh `d_k`):* first-emission branch fires; `a = [d_k.0.s_L.1]` equals `a_k` at chain index 0.
  - *Case B (existing `d_k`), sub-case B1 (`J_{d_k}^Σ = -1`):* first-emission branch fires identically to Case A.
  - *Case B, sub-case B2 (`J_{d_k}^Σ ≥ 0`):* subsequent-emission branch fires with `ℓ_prev = inc^{J_{d_k}^Σ}(d_k.0.s_L.1, 0)` (T1-max by ChainEnumerationInjectivity); `inc(ℓ_prev, 0)` lands at chain index `J_{d_k}^Σ + 1`, which R0a-Cor1 at Σ' assigns to `a_k`.

---

## Relational layer — RelationalLayer (COMMITMENT, commitment)

The relational layer's operations are `{Emit_K, Observe_K, Nullify}`, with `Nullify` a definitional alias for `Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` — `Emit_K` instantiated at `K := R`, `F := ∅`, `G := {(a, δ(1, #a))}`. The layer commits to `Emit_K` as its sole state-affecting class-(iii) emission, and admits no composites that touch `Σ.L` indirectly.

*Nullify-as-sole-`R`-producer discipline:* callers may invoke `Emit_K` only at type indices `K` satisfying `K ≁ R`; every `R`-typed emission is routed through the `Nullify` alias.

*Corollary (reduction to `Emit_K`):* The relational layer's state-affecting operations reduce to `{Emit_K}` (with `Nullify` as alias). Each relational-layer state-affecting operation is a single-step class-(iii) `→`-step by R7a with no K.σ-prefix (callers establish `d ∈ dom(Σ.M)` before calling).

---

## Emit_K — EmitK (OP, operation)

`Emit_K : Σ × dom(Σ.M) × Endset × Endset → Σ' × A_rel^{Σ'}`

Equivalently: `Emit : T_admissible × Σ × dom(Σ.M) × Endset × Endset → Σ' × A_rel^{Σ'}` with `Emit_K(·) := Emit(K, ·)`.

Precondition: `K ∈ T_admissible` (at type-index); `d ∈ dom(Σ.M)` (enforces `dom(Σ.M) ≠ ∅`); `F, G ∈ Endset`.

Effect: invokes K.λ at home `d` with value `(F, G, K)`. Fresh address `a` fixed by K.λ's first/subsequent emission rule:
- first emission (`{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅`): `a = [d.0.s_L.1]`
- subsequent emission (predicate negated): `a = inc(ℓ_prev, 0)` where `ℓ_prev := max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}`

Postcondition: `a ∉ dom(Σ.L)`, `a ∈ dom(Σ'.L)`, `home(a) = d`, `Σ'.L(a) = (F, G, K)`. By R2, this binding is permanent.

Frame: `Σ'.C = Σ.C` and `Σ'.M = Σ.M`.

---

## Observe_K — ObserveK (OP, operation)

For `K ∈ T_admissible`, pattern `(F̂, Ĝ) ∈ ℘_fin(T) × ℘_fin(T)`, and view selector `View ∈ {hist, oper}`:

`Observe_K : Σ × ℘_fin(T) × ℘_fin(T) × View → ℘_fin(L_K^Σ)`

Returns:

`{(a, F, G) ∈ view : F̂ ⊆ coverage(F) ∧ Ĝ ⊆ coverage(G)}`

where `view = L_K^Σ` if `View = hist` and `view = A_K^Σ` if `View = oper`. `Observe_K` leaves Σ unchanged.

Pattern domain: patterns range over the full tumbler space `T` (not `A^Σ`), to admit ghost-targeting queries per L9 + L4. The match relation `F̂ ⊆ coverage(F)` is decidable because `coverage(F)` is a finite subset of `T` for every finite endset `F` (T12 + finiteness of `F`).

---

## Nullify — Nullify (OP, operation)

Preconditions: (P0) `d_retr ∈ dom(Σ.M)`; (P1) `a ∈ A_rel^Σ`; (P2) `|Σ.L(a)| = 3`.

`Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`

By PrefixSpanCoverage, `coverage({(a, δ(1, #a))}) = {t : a ≼ t}`, which contains `a`. Let `(Σ', _) = Nullify(Σ, d_retr, a)`. By Definition of `nullified`, `a ∈ nullified(Σ')`. By R6a, `a` remains nullified thereafter.

*Single-tuple scope (absolute under R0a):* R0a's unconditional antichain gives `{a' ∈ dom(Σ.L) : a ≼ a'} = {a}`. The fresh emitter `b = a_emit(Σ, d_retr)` produced by K.λ satisfies `b ≠ a` (by K.λ freshness, `a ∈ dom(Σ.L)`) and `a ⊀ b` (by R0a on `dom(Σ'.L)`). Therefore `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`: Nullify contributes exactly `a` to `nullified(Σ')`, never a prefix-subtree.
