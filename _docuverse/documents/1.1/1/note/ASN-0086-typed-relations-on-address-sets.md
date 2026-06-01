# ASN-0086: Typed Relations on Address Sets

*Drawing the link model forward into a relational vocabulary*

ASN-0043 establishes the link as a primitive: an addressed, owned, typed connection between spans of content. ASN-0093 wraps that primitive (along with content and document allocation) in three K-operations — K.σ, K.α, K.λ — that fix the sibling-frontier emission discipline and the sub-allocator chain structure. This note layers on top of ASN-0093's K-operations, adopting a different vocabulary for the link store: where ASN-0043 speaks of *links* and *endsets*, we speak of *tuples* and *typed relations*. The two vocabularies describe one object — a standard-triple link `(F, G, Θ)` at address `a ∈ dom(Σ.L)` is a tuple in a typed relation indexed by `Θ` — but predicates compose more cleanly over relations than over endsets, and several substrate-level guarantees become easier to state in this form.

We are looking for what a relation algebra over the link store affords. The answer is structural properties on the typed-relation substrate, partitioned by status: R0–R5 are derived lemmas from ASN-0043 + ASN-0093; R6a/R6b/R6c are the substantive lemmas carrying the *active/audit distinction* between `L_K` (audit trail) and `A_K` (operational currently-in-effect set). On top of these we define three operations (Emit_K, Observe, Nullify) and prove R7a (no `Σ.L`-affecting transition lies outside class (iii) = K.λ); the relational layer is then *defined* to commit `Emit_K` as its sole state-affecting K.λ-emission, from which the reduction of relational-layer state change to `Emit_K` follows (Corollary, below). (Document allocation (K.σ) and content emission (K.α), the other two primitive transitions in `→`, are inherited from ASN-0093 and are not reductions of `Emit_K`; the scope of the reduction is the link store `Σ.L` and the typed relations indexed over it.)


## The Two Foundational Sets

**Foundation.** We work in systems satisfying ASN-0093 (and therefore ASN-0043, ASN-0036, ASN-0034). ASN-0093 owns the K-operation contract — the three primitive emissions K.σ (DocumentRegistration), K.α (ContentAllocation), K.λ (LinkAllocation) — together with the sub-allocator chain lemmas (ChainDiscipline, FirstEmission, ChainMembershipForOrigin, and supporting chain-structure lemmas) making T10a's runtime activation chain explicit, and the SubspaceConventionAxiom fixing `s_C = 1 ∧ s_L = 2` with named consequence `SC-NEQ: s_C ≠ s_L`. We consume these directly rather than reinventing them. Citations of S3 refer to S3 (ReferentialIntegrity, ASN-0036).

**State transition relation.** We write `Σ → Σ'` for the substrate's *dom-extending* one-step transition relation, which we identify exactly with the union of ASN-0093's three K-operations: `→ ≡ K.σ ∪ K.α ∪ K.λ`. Concretely, each `→`-step is one of:

- a *K.σ-step* — document registration, extending `dom(Σ.M)` with a fresh document address `d` satisfying `T4-valid(d) ∧ zeros(d) = 2` and registering `M'(d) = ∅`;
- a *K.α-step* — content allocation, extending `dom(Σ.C)` with a fresh content address `a` produced by `d`'s content sub-allocator `A_C(d)` for some `d ∈ dom(Σ.M)` (first-emission `a = [d.0.s_C.1]` or subsequent-emission `a = inc(a_prev, 0)`);
- a *K.λ-step* — link allocation, extending `dom(Σ.L)` with a fresh link address `ℓ` produced by `d`'s link sub-allocator `A_L(d)` for some `d ∈ dom(Σ.M)` (first-emission `ℓ = [d.0.s_L.1]` or subsequent-emission `ℓ = inc(ℓ_prev, 0)`).

In what follows we sometimes refer to the three classes as *class (i)*, *class (ii)*, *class (iii)* respectively (mnemonic for K.σ, K.α, K.λ); the K-operation labels are authoritative. ASN-0093's frame conditions on each K-op ensure that the two non-affected stores are preserved pointwise, and that the affected store is extended by exactly one fresh key per step. Every dom-extending transition in `→` is one of the three K-ops; the substrate exposes no removal, replacement, or in-place mutation transition that touches `(dom(Σ.C), dom(Σ.M), dom(Σ.L))` (consistent with S0, L12, T8, and ASN-0093 M1/C0/L12 across the underlying ASNs). The operations defined later in this note (Observe, Nullify) either compose `Emit_K` (Nullify is `Emit_R` with a designated argument shape) or leave Σ unchanged (Observe).

*Arrangement modification is out of scope.* ASN-0093's M2 (EmptyArrangement) is an invariant of the foundation we adopt: `(A d ∈ dom(M) :: M(d) = ∅)`. Under M2 every document's arrangement is empty at every reachable state, so the substrate admits no arrangement-modifying transition — `→` is the complete dom-extending vocabulary, and persistence claims (R6c) are stated and proved against `→` alone. No claim in this note relies on any transition M2 forbids.

*Categorical transition relation `↝`.* We write `↝` for the *categorical* state-transition relation: the union of `→` with every state-transition relation any higher-layer operation may admit over `(Σ.C, Σ.M, Σ.L)`. Every `→`-step is an `↝`-step; `Σ ↝ Σ'` holds iff some admissible operation in some layer carries Σ to Σ'.

**Definition — Reachability.** `Σ' is →-reachable from Σ`, written `Σ →* Σ'`, is the reflexive-transitive closure of `→`. This is a *reachability* relation, distinct from ASN-0043's store-extension relation `⊒` (StateExtension), which asserts store-inclusion-with-agreement on a single pair of states without requiring a `→`-path between them. We use `→*` and never `⊑`/`⊒` for it, to avoid colliding with ASN-0043's notation.

By the frame conditions of (i)–(iii) — each primitive transition extends exactly one of `Σ.C`, `Σ.M`, `Σ.L` at a fresh key and leaves the other two components unchanged — `Σ →* Σ'` entails `dom(Σ.C) ⊆ dom(Σ'.C)`, `dom(Σ.M) ⊆ dom(Σ'.M)`, `dom(Σ.L) ⊆ dom(Σ'.L)`, with `Σ'.C|_{dom(Σ.C)} = Σ.C`, `Σ'.M|_{dom(Σ.M)} = Σ.M`, `Σ'.L|_{dom(Σ.L)} = Σ.L`. Equivalently, `Σ →* Σ'` implies `Σ' ⊒ Σ` in ASN-0043's sense; the converse need not hold.

**Definition — AddressUniverse.** The substrate's address universe at state Σ is

`A^Σ = dom(Σ.C) ∪ dom(Σ.L)`

By SD (StoreDisjointness, ASN-0093) — equivalently ASN-0043 L14 (DualPrimitive) together with ASN-0093 L0 supplying global `s_C`-residency of content — `A^Σ` is the entirety of stored-entity addresses at Σ; no third category exists.

**Definition — Partition.** Define:

`A_doc^Σ = dom(Σ.C)` &nbsp; — content addresses
`A_rel^Σ = dom(Σ.L)` &nbsp; — relation-tuple addresses

We claim `A^Σ = A_doc^Σ ⊔ A_rel^Σ` (disjoint union). The disjointness is R4 below.

**Definition — GhostAddresses.** The *ghost addresses* at state Σ are the tumblers outside the stored-entity universe:

`T_ghost^Σ = T \ (dom(Σ.C) ∪ dom(Σ.L))`

By L9 (TypeGhostPermission, ASN-0043), ghost addresses may appear in endset spans (including type-endset coverage) without contradiction; they reference tumbler positions that are well-formed under the addressing scheme but carry no stored entity at Σ.

*Notation.* All four sets are state-dependent — `A^Σ`, `A_doc^Σ`, `A_rel^Σ`, and `T_ghost^Σ` grow or shrink as the substrate evolves (the first three monotonically by S1 and L12a; `T_ghost^Σ` shrinks as content and link emissions populate previously-ghost addresses). Where the ambient state is unambiguous, we drop the superscript and write `A`, `A_doc`, `A_rel`, `T_ghost`.

**Definition — AdmissibleTypes.** The set of *admissible types* is

`T_admissible = {K ∈ Endset : K ≠ ∅}`

— non-empty endsets, eligible to serve as a link's type endset by L3 (NEndsetStructure, ASN-0043).

By L4 (EndsetGenerality, ASN-0043) and L9 (TypeGhostPermission, ASN-0043), `T_admissible` is unconstrained by content existence: type endsets may reference any tumbler addresses, including ghosts. We require only that type-equality is decidable by endset comparison — which it is, by L8 (TypeByAddress). Type indices in what follows range over `T_admissible`; membership in a given coverage class `[K]` is then determined per-tuple by `L_K^Σ`'s coverage-equivalence criterion (below).

For the rest of this development we restrict attention to standard-triple links — those with `|Σ.L(a)| = 3`. Higher-arity links (L3, NEndsetStructure, ASN-0043) exist in `dom(Σ.L)` but are not members of any `L_K`; they admit an analogous construction with additional slot positions, which we do not pursue here.

## Allocator Structure

ASN-0093 supplies the sub-allocator structure this note relies on: for each `d ∈ dom(Σ.M)`, ChainDiscipline and FirstEmission (ASN-0093) establish two sub-allocator chains `A_C(d)` (content) and `A_L(d)` (link), anchored respectively at `b_C(d) := [d.0.s_C]` and `b_L(d) := [d.0.s_L]`, with first emissions `[d.0.s_C.1]` and `[d.0.s_L.1]`. We use ASN-0093's names directly throughout.

*Derived chain facts.* By ChainDiscipline (ASN-0093), each `A_C(d)`, `A_L(d)` is an instance of ASN-0040's sibling stream `S(p, d)`. We use two `S(p, d)` postconditions throughout, both holding along the whole `inc(·, 0)` chain: **(UL) uniform length** — `#cₙ = #c₁` for every chain element (from `S(p, d)`'s `#cₙ = #p + d`); and **(UZ) uniform zero-count** — `zeros(cₙ) = zeros(c₁)` (from the stream form `cₙ = [p₁, …, p_{#p}, 0, …, 0, n]`, equivalently B5a SiblingZerosPreservation, ASN-0040).


## The Typed Relation

**Definition — TypeEquivalence.** Two admissible types are *type-equivalent* iff they cover the same address set:

`K ~ K' ≡ coverage(K) = coverage(K')`

This is L8's (TypeByAddress, ASN-0043) notion of `same_type`, lifted from links to type endsets themselves. The quotient `T_admissible / ~` is the set of *coverage classes*; the equivalence class of `K` is written `[K]`.

**Definition — TypedRelation.** For each `K ∈ T_admissible` and state Σ, the *typed relation of type K at Σ* is

`L_K^Σ = {(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a).e₁ = F ∧ Σ.L(a).e₂ = G ∧ coverage(Σ.L(a).e₃) = coverage(K)}`

Each member is a triple of (tuple-address, from-endset, to-endset). The pair `(F, G)` is the *relational content* of the tuple; `a` is the *tuple address*. The substrate's standard-triple link store at state Σ is therefore the disjoint union over coverage classes:

`L^Σ = ⨆_{[K] ∈ T_admissible / ~} L_K^Σ`

We will show (R1) that this disjoint union is well-defined: each tuple address belongs to exactly one coverage-class slice. Note that `L^Σ` collects only the arity-3 links; higher-arity links in `dom(Σ.L)` are outside its scope, as noted above. Where ambient state is clear we drop the superscript and write `L_K`, `L`. Coverage-equivalence at the type slot aligns `L_K` with L8's same-type relation, which also projects through coverage.

*Notation — subscript read modulo `~`.* The membership criterion at slot 3 is `coverage(Σ.L(a).e₃) = coverage(K)`, which is `~`-equivalence between the stored type endset and the index endset `K` (Definition of TypeEquivalence above). Two `K, K' ∈ T_admissible` with `K ~ K'` therefore induce the same slice: `L_K^Σ = L_{K'}^Σ` as sets, by extensional equality of the membership predicates. The subscript `K` is consequently a *coverage-class* index — the slice depends only on `[K]`, not on the literal endset value `K` representing it.

**Definition — TupleAddress.** Define `addr : L^Σ → A_rel^Σ` by `addr(a, F, G) = a`.

*Remark — relation to ℘(A) × ℘(A).* A generic mathematical typed relation is a subset of `℘(A) × ℘(A)` — a set of address-pair-pairs distinguished only by content. Our typed relation is richer: each tuple carries an address that participates in the relation's identity. The projection `(a, F, G) ↦ (coverage(F), coverage(G))` recovers the address-pair view, but it loses information that the substrate retains (R0, R1).


## Tuple Identity (R0, R1, R2)

A generic mathematical relation distinguishes its members only by content: two tuples with identical (F, G) are the same tuple. The substrate's relations do not work that way. Each tuple emission allocates a fresh address (R0), the address-to-pair binding is a function (R1), and the binding is permanent (R2).

**Sub-lemma — FreshLinkKeyDisjointness (L14/L14a fresh-key discharge).** Let `Σ → Σ'` extend the link store by one fresh key `a` with `E(a)₁ = s_L`, leaving `Σ'.C = Σ.C` and `Σ'.M = Σ.M` (the value-preserving single-key form of every K.λ-step). If L14 (DualPrimitive) and L14a (NonTranscludability) hold at Σ, they hold at Σ'. *Proof.* The only new key to check is `a`. By ASN-0093 L0 (SubspacePartition) and SC-NEQ, `E(a)₁ = s_L ≠ s_C` while every content address has `E(·)₁ = s_C`, so `a ∉ dom(Σ.C)|_{s_C}` — discharging L14 at the new key (SD, StoreDisjointness, ASN-0093, delivers `dom(Σ'.L) ∩ dom(Σ'.C) = ∅` directly). For L14a, by S3 `ran(Σ.M) ⊆ dom(Σ.C)`, so every arrangement image carries `E(·)₁ = s_C`, and the same exclusion gives `a ∉ ran(Σ.M) = ran(Σ'.M)`. ∎ This discharge is cited at each fresh-link-emission site (R0, R5, R7a) rather than re-derived.

**R0 — TupleAddressFreshness.** For any state Σ with `dom(Σ.M) ≠ ∅` and any `(F, G, K) ∈ Endset × Endset × T_admissible`, there exists a state Σ' with Σ → Σ' that emits a tuple with content (F, G) of type K at a fresh address:

`(A Σ : dom(Σ.M) ≠ ∅ :: (A F, G ∈ Endset, K ∈ T_admissible :: (E Σ' reached by one →-step from Σ, a : a ∉ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K))))`

*Proof.* R0 is a near-direct consequence of ASN-0093's K.λ contract. Pick any `d ∈ dom(Σ.M)` (precondition `dom(Σ.M) ≠ ∅` is given). We invoke K.λ at home `d` with value `(F, G, K)` ∈ Endset × Endset × T_admissible (which satisfies K.λ's L3-discharge precondition by L3-conformance of the triple: `|·| = 3`, `F, G ∈ Endset`, `K ∈ T_admissible` non-empty).

K.λ's contract supplies the fresh address `a` directly via its first/subsequent emission rule:

- *First emission* (predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅` fires): `a = [d.0.s_L.1]`. By FirstEmission (ASN-0093), this address has `E(a)₁ = s_L`, `origin(a) = d`, `#E(a) = 2`, `zeros(a) = 3`, and is T4-valid by direct inspection. By ChainDiscipline + FirstEmission (ASN-0093), the link sub-allocator chain `A_L(d)` is active at every state with `d ∈ dom(Σ.M)`. By FirstEmissionFreshness, `a ∉ dom(Σ.L) ∪ dom(Σ.C)` at the K.λ-event that commits `a`.
- *Subsequent emission* (predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} ≠ ∅` fires): `a = inc(ℓ_prev, 0)` where `ℓ_prev := max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}`. By ChainEnumerationInjectivity and ChainMembershipForOrigin (ASN-0093), `ℓ_prev` is the T1-max of the contiguous prefix of `A_L(d)`'s realized chain, and `inc(ℓ_prev, 0)` is the next chain element of `A_L(d)`; by (UL)/(UZ) the result keeps `ℓ_prev`'s length and zero count, and by ChainPrefixExtension `b_L(d) ≼ a`, so `origin(a) = d`. Freshness of `a` against `dom(Σ.L) ∪ dom(Σ.C)` is exactly SubsequentEmissionFreshness (ASN-0093), whose three-way split — within-document (ChainEnumerationInjectivity), cross-document (CrossDocDisjointness + T10, PartitionIndependence, ASN-0034), and cross-subspace (DisjointSubAllocatorChains + L0 + SC-NEQ) — discharges K.λ's freshness precondition `a ∉ dom(Σ.L) ∪ dom(Σ.C)` at the K.λ-event committing `a`.

In either branch, K.λ's effect is `Σ'.L = Σ.L ⊕ {a ↦ (F, G, K)}` with `Σ'.C = Σ.C` and `Σ'.M = Σ.M` per K.λ's Frame, witnessing R0's existential conclusion.

*L-invariant preservation across the K.λ-step.* The K.λ-step is a primitive ASN-0093 transition and so preserves the full L/S/M/C invariant catalog (ASN-0036, ASN-0043, ASN-0093) by its own contract: K.λ's Frame fixes `(Σ.C, Σ.M)` pointwise, discharging every S-, M-, and C-invariant by input-substitution, and its first/subsequent emission rule together with ASN-0093's chain-discipline lemmas discharge the L-invariants at the fresh key `a`. The L14/L14a fresh-key obligation is the FreshLinkKeyDisjointness sub-lemma above (`E(a)₁ = s_L` excluded from content and arrangement-image by SC-NEQ).

The only obligation R0's specialization adds beyond K.λ's generic value-precondition is the standard-triple value shape: `Σ'.L(a) = (F, G, K)` has arity 3 with `F, G ∈ Endset` and `K ∈ T_admissible` non-empty — exactly L3 at `a`, which K.λ's `N ≥ 3 ∧ e₃ ≠ ∅` precondition discharges at `N = 3`, `e₃ = K`. ∎

**R0a — FlatLinkDomain.** At every reachable state Σ, `dom(Σ.L)` is a tumbler-prefix antichain:

`(A Σ : Σ reachable from Σ_init :: (A a, a' ∈ dom(Σ.L) :: a ≼ a' ⟹ a = a'))`

R0a is unconditional: K.λ's first/subsequent emission rule, together with ASN-0093's sub-allocator chain lemmas (ChainDiscipline, FirstEmission, and the chain-structure lemmas), enforce the sibling-frontier discipline as part of the substrate's class-(iii) primitive.

*Proof.* The argument decomposes into two cases on `home(a)` vs. `home(a')`, both discharged by ASN-0093's chain machinery (or, equivalently, by T10a's allocator-disjointness lemmas):

*Case 1 — Cross-home (`home(a) ≠ home(a')`).* We show this case directly from L1's element-level constraint plus L1a's NUDE-prefix `home` projection — no chain machinery is required. Let `d = home(a)` and `d' = home(a')` with `d ≠ d'`.

*(Forward direction: `¬(a ≼ a')`.)* Suppose, toward contradiction, that `a ≼ a'`. Then `a' = a · w` for some suffix `w` (the digits appended to `a` to obtain `a'`). Zero counts add along concatenation: `zeros(a') = zeros(a) + zeros(w)`. By L1 (LinkElementLevel, ASN-0043), `zeros(a) = zeros(a') = 3`, so `zeros(w) = 0` — `w` contains no zero positions. By L1a (LinkScopedAllocation, ASN-0043), `home(·) = N(·).0.U(·).0.D(·)` — the prefix of the link extending through the document-field `D(·)` and ending *just before* the third zero. Since `a ≼ a'`, the positions `1..#a` of `a'` agree pointwise with all of `a`; the remaining positions `#a + 1 .. #a'` of `a'` are `w`, which contains no zeros. Therefore every zero of `a'` sits at a position `≤ #a`, and the three zeros of `a'` are *exactly* the three zeros of `a`, at the same positions. In particular, `a'`'s third zero sits at the position of `a`'s third zero — call this position `p₃`, with `p₃ ≤ #a`. The `home` prefix has length `p₃ − 1` (the positions up to and including `D(·)`, which immediately precedes the third zero). Since `p₃ − 1 < p₃ ≤ #a`, the prefix of `a'` of length `p₃ − 1` agrees pointwise with the prefix of `a` of length `p₃ − 1` (by `a ≼ a'` applied at positions `1..#a`); equivalently, `N(a') = N(a)`, `U(a') = U(a)`, and `D(a') = D(a)` — the three NUDE field-components delimited by `a'`'s first three zeros coincide with those of `a` position-by-position. Therefore `home(a') = N(a').0.U(a').0.D(a') = N(a).0.U(a).0.D(a) = home(a) = d`, contradicting `d' ≠ d`. Hence `¬(a ≼ a')`.

*(Reverse direction: `¬(a' ≼ a)`.)* Suppose, toward contradiction, that `a' ≼ a`. Then `a = a' · w'` for some suffix `w'` (the digits appended to `a'` to obtain `a`). By L1, `zeros(a) = zeros(a') = 3`, so `zeros(w') = 0` — `w'` contains no zero positions. Since `a' ≼ a`, the positions `1..#a'` of `a` agree pointwise with all of `a'`, and the remaining positions `#a' + 1 .. #a` of `a` are `w'`, which contains no zeros. The three zeros of `a` therefore sit at positions `≤ #a'` and coincide position-by-position with the three zeros of `a'`. Call the position of `a`'s third zero `p₃'`, with `p₃' ≤ #a'`. The prefix of `a` of length `p₃' − 1` agrees pointwise with the prefix of `a'` of length `p₃' − 1` (by `a' ≼ a` applied at positions `1..#a'`); equivalently, `N(a) = N(a')`, `U(a) = U(a')`, and `D(a) = D(a')`. Therefore `home(a) = N(a).0.U(a).0.D(a) = N(a').0.U(a').0.D(a') = home(a') = d'`, contradicting `d ≠ d'`. Hence `¬(a' ≼ a)`.

Either way, neither `a ≼ a'` nor `a' ≼ a` holds when `home(a) ≠ home(a')`, so the R0a implication `a ≼ a' ⟹ a = a'` holds vacuously in this case.

*Case 2 — Same-home (`home(a) = home(a') = d`).* By ASN-0093's ChainMembershipForOrigin lemma, the set `{a'' ∈ dom(Σ.L) : origin(a'') = d}` is a contiguous initial segment of `A_L(d)`'s chain enumeration `(t_1, t_2, t_3, …)` with `t_1 = [d.0.s_L.1]` and `t_{n+1} = inc(t_n, 0)`. Hence both `a` and `a'` are chain elements: `a = t_i` and `a' = t_j` for some `i, j ≥ 1`. By (UL), `#a = #t_i = #t_1 = #a'` — all chain elements have equal length. If `a ≼ a'`, then by the prefix definition (positions `1..#a` of `a'` agree with `a`) combined with `#a = #a'`, `a` and `a'` coincide pointwise, so `a = a'` by T3 (CanonicalRepresentation, ASN-0034). (Equivalently, by T10a.2 applied to the distinct siblings `a`, `a'` of `A_L(d)`.)

Combining Cases 1 and 2, `a ≼ a' ⟹ a = a'` at every reachable Σ. ∎

**R0a-Cor1 — ContiguousPrefix.** At every reachable state Σ, for every `d ∈ dom(Σ.M)` there exists `J_d^Σ ∈ ℤ_{≥-1}` such that the homed-set is a contiguous initial segment of `A_L(d)`'s chain enumeration, and (when non-empty) admits a unique T1-maximum at chain index `J_d^Σ`:

`(A Σ : Σ reachable from Σ_init :: (A d ∈ dom(Σ.M) :: (E J_d^Σ ∈ ℤ_{≥-1} :: {a ∈ dom(Σ.L) : home(a) = d} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ})))`

(with `J_d^Σ = -1` denoting the empty set when no link is homed at `d`).

*Substantive postconditions.* Beyond the index re-translation `J_d^Σ := n_d − 1`, R0a-Cor1 carries two derived consequences absorbed at this site for downstream use:

(a) *Unique T1-maximum on non-empty homed-sets.* When `J_d^Σ ≥ 0` (equivalently, the homed-set is non-empty), `max{a ∈ dom(Σ.L) : home(a) = d}` under T1 (LexicographicOrder, ASN-0034) is well-defined and equals `inc^{J_d^Σ}(d.0.s_L.1, 0)`, the chain element at chain index `J_d^Σ`. *Derivation:* ChainEnumerationInjectivity (ASN-0093) is stated in the strict-order form `(A m, n ≥ 1 : m < n : t_m < t_n)`, which forces the contiguous chain prefix `{t_1, …, t_{n_d}}` to admit `t_{n_d}` as its unique maximum; under the index re-translation, `t_{n_d} = inc^{J_d^Σ}(d.0.s_L.1, 0)`.

(b) *J_d^Σ = -1 absorbs the empty case.* By convention `J_d^Σ = -1 ⟺` the homed-set is empty (`n_d = 0`).

*Proof.* The contiguous-prefix form is a direct re-expression of ASN-0093's ChainMembershipForOrigin lemma applied to the link store. ChainMembershipForOrigin states that `dom(Σ.L) ∩ {a' ∈ T : origin(a') = d}` is a contiguous initial segment `{s_1, …, s_{n_d}}` of `A_L(d)`'s chain enumeration. Setting `J_d^Σ := n_d − 1`, we have `s_k = inc^{k−1}([d.0.s_L.1], 0)` by FirstEmission (ASN-0093) (`s_1 = t_1^L(d) = [d.0.s_L.1]`) and the sibling recurrence `s_{k+1} = inc(s_k, 0)`. Hence

`{a ∈ dom(Σ.L) : home(a) = d} = {s_1, …, s_{n_d}} = {incʲ([d.0.s_L.1], 0) : 0 ≤ j ≤ J_d^Σ}`

with `J_d^Σ = -1` corresponding to `n_d = 0` (empty homed set). Under ASN-0036, `origin(a)` and `home(a)` coincide on every `a ∈ dom(Σ.L)` because L1 + L1a's NUDE-prefix projection is exactly the `origin(·) = N(·).0.U(·).0.D(·)` projection. The substantive postcondition (a) follows from ChainEnumerationInjectivity's strict-order form chained over the contiguous prefix; postcondition (b) is the integer-extension convention applied at `n_d = 0`. ∎

**R0a-Cor2 — DepthTwoLinkAddresses.** At every reachable state Σ, every link address in `dom(Σ.L)` has an element field (T4b's `E` projection) of length exactly 2:

`(A Σ : Σ reachable from Σ_init :: (A a ∈ dom(Σ.L) :: #E(a) = 2))`

(Here `#E(a)` is the length of the element-field projection — e.g., `E(a₁) = [2, 1]`, `#E(a₁) = 2` at the concrete instantiation. This narrows L1b's substrate-level admission `#E ≥ 2` (ASN-0043) to the tighter `#E = 2` strictly.)

*Proof.* By R0a-Cor1, every `a ∈ dom(Σ.L)` lies on the form `a = incʲ(d.0.s_L.1, 0)` for `d = home(a)` and some `j ≥ 0`. The chain anchor `t_1 = [d.0.s_L.1]` has length `#t_1 = #d + 3` and three zero positions: the two zero positions of `d` (inherited from the prefix `d`), and a third zero at position `#d + 1` (the appended field separator in `d.0.s_L`). Position `#t_1 = #d + 3` carries the non-zero subspace ordinal `1`. The element field `E(t_1)` is the suffix following the third zero (at position `#d + 1`): `E(t_1) = [s_L, 1]` at positions `#d + 2` and `#d + 3`, so `#E(t_1) = 2`. (UL) gives `#t_n = #t_1` for every `n ≥ 1`. We now establish that the zero *positions* of every `t_n` coincide with those of `t_1`, which fixes `#E(t_n) = #E(t_1) = 2` strictly.

By ChainDiscipline (ASN-0093), each `t_{n+1} = inc(t_n, 0)`. By TA5(c) (HierarchicalIncrement, ASN-0034), `inc(·, 0)` modifies *exactly one* position — `sig(t_n)`, the rightmost non-zero position — and preserves all other positions: `(t_{n+1})_i = (t_n)_i` for every `i ≠ sig(t_n)`, with `(t_{n+1})_{sig(t_n)} = (t_n)_{sig(t_n)} + 1`. By ChainElementT4Validity (ASN-0093) — applied to `A_L(d)`, which ChainDiscipline discharges as a T10a-discipline-satisfying chain — every chain element is T4-valid; ChainElementT4Validity itself routes through T10a.4 (T4PreservationUnderDiscipline, ASN-0034) as its underlying ASN-0034 hook. By TA5-SigValid (ASN-0034), `sig(t_n) = #t_n` for every chain element. The single modified position is the terminal position `#t_n = #t_1`, which is non-zero in `t_n` (T4 conjunct iv at `t_n`) and remains non-zero in `t_{n+1}` (incrementing a non-zero ℕ-value stays non-zero: by NAT-addcompat's strict-successor inequality `n < n + 1` and NAT-order's transitivity, `(t_n)_{sig(t_n)} + 1 > (t_n)_{sig(t_n)} ≥ 1 > 0`). Therefore the set of zero positions is identical across `t_n` and `t_{n+1}`; by induction, identical across the whole chain.

T4b's element field `E(·)` is the suffix following the third zero. Since the three zero positions of every `t_n` coincide with those of `t_1`, the third zero sits at position `#d + 1` in every chain element, and the element field's length is `#E(t_n) = #t_n − (#d + 1) = (#d + 3) − (#d + 1) = 2 = #E(t_1)`. Hence `#E(a) = 2`. ∎

**R1 — AddressInjectivity.** The map `addr : L → A_rel` is an injection:

`(A (a, F, G), (a', F', G') ∈ L : a = a' :: F = F' ∧ G = G' ∧ both belong to the same coverage-class slice L_{[K]})`

*Proof.* `Σ.L` is a partial function `T ⇀ Link` (ASN-0043, Definition of LinkStore). Function-ness gives uniqueness of value: if `a = a'`, then `Σ.L(a) = Σ.L(a')`, and that single value determines the triple `(F, G, K'')` stored at `a`. Therefore `F = F'`, `G = G'`, and the third endset `K''` is unique. Since `coverage(·)` is a pure function on endset values, `coverage(K'')` is a single fixed address set, so the coverage class `[K'']` is unique — whence both members of `L` lie in the same `L_{[K'']}`. ∎

**R2 — TupleAddressPermanence.** Once allocated, a tuple address resolves permanently to the same relational content:

`(A Σ → Σ', a ∈ dom(Σ.L), (F, G, K) = Σ.L(a) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K))`

*Proof.* Direct from L12 (LinkImmutability, ASN-0043): for every state transition, every existing link address persists with its value unchanged. ∎

*Consequence.* *Distinct emissions are distinguishable even when content matches.* Two agents independently filing tuples with identical `(F, G)` under identical `K` produce distinct addresses (R0 produces a fresh address regardless of value). By L11b (NonInjectivity, ASN-0043), value-level coincidence is permitted; by R1, address-level identity nevertheless distinguishes them. The substrate does not silently merge them.


## Append-Only Slices (R3)

**R3 — TypedSliceMonotonicity.** Each typed relation grows monotonically:

`(A Σ → Σ', K ∈ T_admissible :: L_K^Σ ⊆ L_K^{Σ'})`

where `L_K^Σ` denotes the typed relation evaluated at state `Σ`.

*Proof.* Let `(a, F, G) ∈ L_K^Σ`. By Definition of `L_K^Σ` (membership at the type slot is by coverage-equivalence, not by literal endset value), `a ∈ dom(Σ.L)` with `Σ.L(a) = (F, G, K'')` for some `K'' ∈ T_admissible` satisfying `coverage(K'') = coverage(K)`. By L12a (LinkStoreMonotonicity, ASN-0043), `dom(Σ.L) ⊆ dom(Σ'.L)`; by R2, `Σ'.L(a) = (F, G, K'')` — the literal value stored at `a` is preserved exactly. The membership test for `L_K^{Σ'}` is `coverage(Σ'.L(a).e₃) = coverage(K)`, i.e., `coverage(K'') = coverage(K)`, which holds by the choice of `K''`. Therefore `(a, F, G) ∈ L_K^{Σ'}`. ∎

*Consequence.* *Retractions are themselves auditable.* When we introduce the retraction type `R` (R6), `L_R` is one of the typed slices and R3 applies to it as well. Every nullification leaves an entry in `L_R` that persists.


## Subspace Disjointness (R4)

**R4 — TupleAddressDisjointness.** Tuple addresses and document-content addresses are disjoint:

`A_doc^Σ ∩ A_rel^Σ = ∅`

*Proof.* SD (StoreDisjointness, ASN-0093) asserts `dom(Σ.C) ∩ dom(Σ.L) = ∅` substrate-wide — its underlying derivation is ASN-0093 L0 + SC-NEQ + T7 (SubspaceDisjointness, ASN-0034). Substituting, `A_doc^Σ ∩ A_rel^Σ = ∅`. ∎


## Self-Reference (R5)

**R5 — TupleSelfTargeting.** A tuple's from-set or to-set may reference tuple addresses. Specifically, for any state Σ and any `a ∈ A_rel^Σ`, the unit-depth span `(a, δ(1, #a))` is well-formed and may appear in the from-set or to-set of an emitted tuple, with `a` in its coverage.

*Proof.* Fix any `a ∈ A_rel^Σ` at any state Σ. By L1a (LinkScopedAllocation, ASN-0043) applied at `a`, `home(a) ∈ dom(Σ.M)`, so `dom(Σ.M) ≠ ∅` — discharging R0's `dom(Σ.M) ≠ ∅` precondition for the home `d` chosen below. (Equivalently, "may appear in the from-set or to-set of an emitted tuple" presupposes a state with at least one document allocated, which `a ∈ A_rel^Σ` itself supplies.)

*(Step 1 — Span well-formedness.)* By L1 (ASN-0043), `zeros(a) = 3`; by L1b (ASN-0043), `#E(a) ≥ 2`, so `#a ≥ 1`. By OrdinalDisplacement (ASN-0034), `δ(1, #a) = [0, …, 0, 1]` is a positive tumbler of length `#a` with action point `#a`. The span `(a, δ(1, #a))` satisfies T12 (SpanWellDefinedness, ASN-0034) — its action point `#a` satisfies `actionPoint(δ(1, #a)) = #a ≤ #a`. By PrefixSpanCoverage (ASN-0043), `coverage({(a, δ(1, #a))}) = {t : a ≼ t}`, which contains `a` by reflexivity of `≼`.

*(Step 2 — Endset admissibility.)* By L4(c) (EndsetGenerality, ASN-0043), endset spans may reference link-subspace addresses. By L13 (ReflexiveAddressing, ASN-0043) applied at `b = a`, the unit-depth span `(a, δ(1, #a))` is the canonical reference span for `a`. The singleton endset `G_self = {(a, δ(1, #a))}` is therefore an admissible `Endset` member at any slot of an emitted link.

*(Step 3 — Self-targeting emission via R0.)* Pick any `d ∈ dom(Σ.M)` and any `K ∈ T_admissible`. The triple `(∅, G_self, K)` is L3-conforming: arity 3, with `∅ ∈ Endset` (the empty endset) and `G_self ∈ Endset` (the singleton built in Step 2), and `K ∈ T_admissible` non-empty by assumption. Apply R0 at this L3-conforming triple and home `d`. R0's emission discharges every L-invariant except L3 on the emitter address alone — K.λ's Frame fixes `(Σ.C, Σ.M)` pointwise, and the L14/L14a fresh-key obligation is the FreshLinkKeyDisjointness sub-lemma — so R0's emission argument is uniform over *any* L3-conforming triple regardless of `coverage(F)`, `coverage(G)`, or `coverage(K)`; the only content-dependent check, L3, is met here by the conformance just verified. R0 therefore produces a fresh emitter `a' ∉ dom(Σ.L)` and conforming post-state Σ' with `Σ'.L(a') = (∅, G_self, K)`. The self-reference is recorded at the substrate level: `a ∈ coverage(Σ'.L(a').e₂)` — the to-set case.

*(Step 4 — From-set case by parallel emission.)* The from-set case is symmetric. The triple `(G_self, ∅, K)` is L3-conforming by the same checks (arity 3, `G_self ∈ Endset` by Step 2, `∅ ∈ Endset` trivially, `K ∈ T_admissible` non-empty by assumption). R0 applied at home `d` yields a fresh emitter address `a''` with conforming post-state Σ'' satisfying `Σ''.L(a'') = (G_self, ∅, K)` and `a ∈ coverage(Σ''.L(a'').e₁)` — the from-set case. The Step 3 uniformity does not inspect which slot the self-targeting endset occupies, so the slot-symmetric discharge is immediate. ∎

*Corollary R5.1 — SelfTargetingEmission.* For any `a ∈ A_rel^Σ`, any slot position, and any caller-supplied home `d ∈ dom(Σ.M)`, R0 emits at a fresh `A_rel` address a triple carrying the unit-depth span `(a, δ(1, #a))` in the chosen slot (by Steps 2–3: the span is an admissible endset member, and R0's invariant-preservation is uniform over L3-conforming triples, inspecting neither slot nor coverage).

*Consequence.* The substantive consequence is that self-targeting enables retraction without mutation: a tuple in a designated relation `L_R` whose to-set contains the address of the tuple being nullified. By Corollary R5.1, the retraction triple `(∅, {(a, δ(1, #a))}, R)` is emitted at a fresh `A_rel` address homed at a caller-supplied `d_retr ∈ dom(Σ.M)`; mutation becomes Emit, and `L_K` is never modified (R3). This is formalized as the Nullify operation below.


## The Active Subset (R6a, R6b, R6c)

The conceptual contribution of this section is the *active/audit distinction*: two coherent views over the same link store — `L_K` (audit trail, monotone per R3) and `A_K` (operational currently-in-effect set, obtained by excluding `nullified(Σ)`). The construction is made possible by R5 (self-referential retraction) and R3 (monotone audit). R6a, R6b, R6c carry the distinction's substantive properties.

**Definition — RetractionType.** Fix a designated coverage class `[R]` reserved for retraction, represented by any `R ∈ T_admissible` whose coverage selects the conventional retraction address set. The corresponding typed relation `L_R^Σ` is the *retraction relation at state Σ*. By L9 (TypeGhostPermission, ASN-0043), `R` need not refer to anything stored — its coverage is an address set, chosen by convention — and `L_R^Σ` is well-defined as a coverage-class slice regardless of whether any literal representative endset has yet been stored. Before the first retraction emission, `L_R^Σ = ∅`; after the first such emission, `L_R^Σ ≠ ∅`. The "has any retraction been emitted yet?" question is exactly `L_R^Σ ≠ ∅`, decided in coverage-class terms. By coverage-equivalence, any emission with a type endset `R'` satisfying `coverage(R') = coverage(R)` contributes to `L_R^Σ` and to `nullified(Σ)` — callers are not required to use a canonical span structure for `R`, only its canonical coverage.

**Convention — RetractionDirectionality.** For the retraction coverage class `[R]`, the to-set carries the retraction's targets — addresses whose tuples are being withdrawn from the active subset — and the from-set is reserved for attribution-bearing endset content (e.g., the retractor's own address, a self-targeting emission by Corollary R5.1) or is left empty for unattributed retractions. L7 (DirectionalFlexibility, ASN-0043) permits this layer-level naming choice.

**Definition — Nullified.** The set of *nullified* tuple addresses at state `Σ` is

`nullified(Σ) = {a ∈ A_rel^Σ : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))}`

The existential checks `coverage(G')` only — the to-set's coverage — and does not inspect `coverage(F')`. This is the Convention RetractionDirectionality exercised at the substrate-level predicate: retraction targets are in `G'` by the layer's adoption (justified above against L7); an `Emit_R` call whose to-span coverage misses `a` does not nullify `a`, regardless of what its from-set covers. By R5, `coverage(G')` may include `A_rel^Σ` addresses, so `nullified(Σ)` is well-defined as a subset of `A_rel^Σ`. The set-builder restriction `a ∈ A_rel^Σ` is intentional: only tuple addresses are eligible for nullification, since `A_K^Σ` (the consumer of `nullified`) ranges over tuple addresses alone. A retraction's `coverage(G')` may nonetheless target content, documents, or ghost addresses (L9, TypeGhostPermission, ASN-0043), but the restriction excludes those from `nullified(Σ)`.

**Definition — ActiveSubset.** For each `K ∈ T_admissible`, the *active subset of type K at state Σ* is

`A_K^Σ = {(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}`

`A_K^Σ` is computable from `Σ.L` alone: `L_K^Σ` is a slice of `Σ.L`, and `nullified(Σ)` is a finite, computable set. Although a single span's `coverage(G')` may be infinite (a prefix span covers an entire subtree), the set-builder `nullified(Σ) = {a ∈ A_rel^Σ : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))}` ranges over the finite domain `A_rel^Σ = dom(Σ.L)` (L-fin); `L_R^Σ` is a finite slice of `Σ.L` (L-fin), so each tuple's `G'` carries finitely many spans; and for each candidate `a` and each such span `(s, ℓ)`, the membership test `s ≤ a < s ⊕ ℓ` underlying `a ∈ coverage(G')` is decidable by T2 (IntrinsicComparison, ASN-0034). Hence `nullified(Σ)` is a finite intersection-and-union of decidable per-address tests, and `A_K^Σ` is computed by excluding it from the finite slice `L_K^Σ`.

**R6a — RetractionStability.** Once a tuple's address is nullified, it stays nullified across all future state transitions:

`(A Σ → Σ', a ∈ A_rel^Σ : a ∈ nullified(Σ) :: a ∈ nullified(Σ'))`

*Proof.* Recall that `coverage : Endset → ℘(T)` is a pure function on endset values, fixed by the substrate model (ASN-0043, Definition of coverage): given an endset value `E`, `coverage(E)` is determined entirely by `E` and the tumbler-order relation `≼`, which itself is state-independent (T1, ASN-0034). The codomain is `℘(T)` — the full tumbler space — not the state-dependent address universe `A^Σ`; coverage may include addresses outside `dom(Σ.C) ∪ dom(Σ.L)` (L9, TypeGhostPermission, ASN-0043). In particular, `coverage(E)` does not depend on the state Σ in which `E` is evaluated.

Suppose `a ∈ nullified(Σ)`. By Definition of `nullified(Σ)`, this entails `a ∈ A_rel^Σ = dom(Σ.L)`, and there exist `b ∈ dom(Σ.L)` and `(b, F', G') ∈ L_R^Σ` with `a ∈ coverage(G')`. By the coverage-equivalence membership criterion of `L_R^Σ`, the literal value stored at `b` in Σ is `Σ.L(b) = (F', G', R'')` for some `R'' ∈ T_admissible` with `coverage(R'') = coverage(R)` — the third entry need not equal `R` literally; only its coverage must. We exhibit the same witness at Σ': by L12a (LinkStoreMonotonicity, ASN-0043) applied to `a ∈ A_rel^Σ`, `a ∈ dom(Σ.L) ⊆ dom(Σ'.L) = A_rel^{Σ'}`, discharging the `a ∈ A_rel^{Σ'}` predicate required by Definition of `nullified(Σ')`. By R3 (applied to the type slice indexed by `R`), `L_R^Σ ⊆ L_R^{Σ'}`, so `(b, F', G') ∈ L_R^{Σ'}`. By R2, `b ∈ dom(Σ'.L)` with `Σ'.L(b) = (F', G', R'')` — the literal stored value is preserved exactly, so in particular `G'` is preserved. Since `coverage` is a pure function on endset values, `coverage(G')` is a single fixed set, and `a ∈ coverage(G')` is a state-independent proposition once `G'` has been fixed. Therefore `a ∈ nullified(Σ')`. ∎

**R6b — SingleDepthRetraction (Consequence of Definition `nullified`).** Retraction-of-retraction is not a fixpoint operation: an `Emit_R` call whose to-coverage targets a retractor `b` does not "undo" `b`'s nullifying effect on its prior targets. The decision procedure for `a ∈ nullified(Σ)` is *flat* — a single set-membership test independent of any retraction-chain depth in `L_R^Σ`, and unaffected by whether any witnessing retractor `b` is itself nullified.

*Justification.* The Definition of `nullified` quantifies its existential over the audit slice `L_R^Σ`, not the active subset `A_R^Σ`: `a ∈ nullified(Σ) ⟺ (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))`. Because membership ranges over `L_R^Σ` rather than `A_R^Σ`, it is a flat single-pass test — enumerate `L_R^Σ` and test `a ∈ coverage(G')` for each tuple — that is witness-status-independent: it never consults whether the witness `b` is itself nullified. Consequently, "un-nullifying" `a` by emitting `Nullify(b)` for the retractor `b` has no effect: `b` may itself become nullified, but the original tuple `(b, F', G')` persists in `L_R^Σ ⊆ L_R^{Σ'}` (by R3), and `a ∈ coverage(G')` still witnesses `a ∈ nullified(Σ')`. Restoration must proceed by fresh emission at a distinct address. ∎

**R6c — RestorationByReemission.** Once retracted, a tuple stays out of every active subset at any state reachable from Σ:

`(A Σ, K, (a, F, G) ∈ L_K^Σ : a ∈ nullified(Σ) : (A Σ' : Σ →* Σ' :: (a, F, G) ∉ A_K^{Σ'}))`

*Proof.* Induction on the `→`-chain length `n` witnessing `Σ →* Σ'`. *Base* (`n = 0`): `Σ_0 = Σ`, so `(a, F, G) ∈ L_K^{Σ_0}` and `a ∈ nullified(Σ_0)` are the precondition restated at `Σ_0`; by Definition of `A_K`, `a ∈ nullified(Σ_0)` jointly with `(a, F, G) ∈ L_K^{Σ_0}` give `(a, F, G) ∉ A_K^{Σ_0}`. *IH at `Σ_k`:* `(a, F, G) ∈ L_K^{Σ_k}` and `a ∈ nullified(Σ_k)`. *Step:* R6a gives `a ∈ nullified(Σ_{k+1})`; R3 gives `(a, F, G) ∈ L_K^{Σ_{k+1}}`. *Conclusion at `Σ_n = Σ'`:* by Definition of `A_K`, `(a, F, G) ∉ A_K^{Σ'}`. ∎

To "restore" content, emit a fresh tuple with the desired value (R0). The new tuple receives a fresh address; the retracted tuple keeps its address (R2) and stays out of `A_K` (R6a).

*Consequence.* *`A_K` is not monotone; `L_K` is.* R3 (TypedSliceMonotonicity) makes the audit slice monotone — `Σ →* Σ' ⟹ L_K^Σ ⊆ L_K^{Σ'}` — but the same is *not* true of the active subset: a single retraction emission strictly shrinks `A_K` at every type whose tuple address it covers (witnessed by R6c's set-difference: `(a, F, G) ∈ A_K^Σ ∩ (L_K^{Σ'} \ A_K^{Σ'})` for the retracted tuple), and a subsequent re-emission of the same `(F, G)` strictly grows `A_K` again at a *different* address (R0's fresh-address guarantee). Neither `⊆` nor `⊇` holds in general between `A_K^Σ` and `A_K^{Σ'}` for `Σ →* Σ'`; the active subset is therefore *not* a monotone function of `Σ` under either inclusion direction, while the audit slice `L_K` is monotone under `⊆`. Predicates and observation views over `A_K` must accommodate non-monotone evolution as a substrate-level fact, not assume monotonicity inherited from `L_K`'s audit semantics.


## Three Operations

The six properties yield three operations that suffice to span all visible substrate change.

**Definition — Emit_K.** `Emit_K` is a family of state-transforming operations indexed by `K ∈ T_admissible`. K is a type-index (subscript), not a value argument; each fixed K gives a distinct operation with the same shape:

`Emit_K : Σ × dom(Σ.M) × Endset × Endset → Σ' × A_rel^{Σ'}`

Where Σ is the substrate's state space (every state reachable from `Σ_init`); `Emit_K` is a function over Σ (Lemma — Emit_K function-ness, below).

`Emit_K` is operationally `K.λ` of ASN-0093, restricted to the standard-triple link value `(F, G, K)`. K.λ accepts a value `(e₁, …, e_N)` with `N ≥ 3` and `e₃ ≠ ∅`; `Emit_K` specializes to `N = 3` and `e₃ = K`, so K.λ's contract carries over directly.

*Precondition.* `K ∈ T_admissible` (discharged at the type-index, not at the value-argument list). The R0 precondition `dom(Σ.M) ≠ ∅` is enforced by parameter typing: a `d ∈ dom(Σ.M)` argument cannot be supplied unless the document-allocation domain is non-empty.

*Effect.* Given input state Σ, caller-supplied home document `d ∈ dom(Σ.M)`, and finite endsets `F, G ∈ Endset`, `Emit_K(Σ, d, F, G)` invokes K.λ at home `d` with value `(F, G, K)`. K.λ's first/subsequent emission rule fixes the fresh address `a`: *first emission* (predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅`) gives `a = [d.0.s_L.1]`; *subsequent emission* (predicate negated) gives `a = inc(ℓ_prev, 0)` where `ℓ_prev := max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}`. The returned `(Σ', a)` satisfies `a ∉ dom(Σ.L)`, `a ∈ dom(Σ'.L)`, `home(a) = d`, and `Σ'.L(a) = (F, G, K)`. By R2, this binding is permanent across all subsequent transitions.

*Frame.* `Σ'.C = Σ.C` and `Σ'.M = Σ.M` (K.λ's frame).

(The address-returning convention `Emit_K(d, F, G) → A_rel` used in the rest of this note is metonymic: the state is ambient, `d` is the caller-supplied home document, and `Σ'` is the post-emission state in which the returned address resides.)

**Lemma — Emit_K function-ness.** `Emit_K` is a function: given `(Σ, d, F, G, K)`, the output `(Σ', a)` is uniquely determined.

*Proof.* K.λ's first/subsequent emission rule is deterministic in `(Σ, d)`: the first/subsequent predicate is itself a function of `Σ` and `d` (it checks whether `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` is empty), and each branch produces a unique `a`. In the first-emission branch, `a = [d.0.s_L.1]` is a deterministic projection of `d`. In the subsequent-emission branch, `ℓ_prev` is `max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` — a unique extremum because, by R0a-Cor1, the homed set is a contiguous prefix of `A_L(d)`'s chain enumeration and so admits a unique maximum under T1 (LexicographicOrder, ASN-0034). The value `Σ'.L(a) = (F, G, K)` is fixed by the caller-supplied arguments, and K.λ's Frame fixes the rest of Σ'. ∎

**Definition — Observe_K.** For `K ∈ T_admissible`, a pattern `(F̂, Ĝ) ∈ ℘_fin(T) × ℘_fin(T)`, and a view selector, Observe is a pure read with signature

`Observe_K : Σ × ℘_fin(T) × ℘_fin(T) × View → ℘_fin(L_K^Σ)`

where `View ∈ {hist, oper}` selects between `L_K^Σ` (audit) and `A_K^Σ` (operational). It returns

`{(a, F, G) ∈ view : F̂ ⊆ coverage(F) ∧ Ĝ ⊆ coverage(G)}`

with `view = L_K^Σ` if `View = hist` and `view = A_K^Σ` if `View = oper`. Observe leaves Σ unchanged.

*Pattern domain — `T`, not `A^Σ`.* Patterns range over the full tumbler space `T`, not the state-dependent address universe `A^Σ = dom(Σ.C) ∪ dom(Σ.L)`. The reason is `coverage(·)`: by L9 (TypeGhostPermission, ASN-0043) and L4 (EndsetGenerality, ASN-0043), endset spans may target ghost tumblers — tumblers in `T_ghost^Σ = T \ A^Σ` — and `coverage(F)` is consequently a subset of `T`, not of `A^Σ`. A pattern `F̂` restricted to `A^Σ` would be unable to express the canonical "does this tuple's from-endset cover ghost address `g`?" query, which is well-defined on `Σ.L` and operationally meaningful (e.g., for typed retraction targeting a not-yet-allocated coverage class representative, per L9 + R6 Definition of `nullified`). The signature's `℘_fin(T)` admits ghost-targeting patterns without restriction; the substrate-level match relation `F̂ ⊆ coverage(F)` remains decidable in `℘_fin(T)` because `F̂ ∈ ℘_fin(T)` is finite and each membership test `t ∈ coverage(F)` is decidable — by T2 (IntrinsicComparison, ASN-0034) applied to each of the finitely many spans of `F` — so the finite conjunction `(A t : t ∈ F̂ : t ∈ coverage(F))` is decidable regardless of `coverage(F)`'s cardinality. Note `coverage(F)` is in general *infinite*: a single well-formed span covers a lexicographic interval, and PrefixSpanCoverage exhibits `coverage({(x, δ(1, #x))}) = {t : x ≼ t}`, the entire prefix-subtree of `x`. T12 supplies order-convexity and well-formedness, not finiteness; decidability rests on the finiteness of `F̂` and per-span intrinsic containment, not on any finiteness of `coverage(F)`.

The match relation is `F̂ ⊆ coverage(F)` (and `Ĝ ⊆ coverage(G)`), decidable in `℘_fin(T)` by the finiteness of `F̂` and per-span intrinsic containment.

**Definition — Nullify.** Nullify has three preconditions: (P0) `d_retr ∈ dom(Σ.M)` — the caller-supplied home document for the retraction tuple itself; (P1) `a ∈ A_rel^Σ` — the target tuple's address; (P2) `|Σ.L(a)| = 3` — `a` is the address of a standard-triple link.

Under these preconditions, Nullify is the composition

`Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`

That is, emit a tuple into the retraction relation with empty from-set and a unit-depth to-span targeting `a`, with the retraction itself homed at the caller-supplied `d_retr ∈ dom(Σ.M)`. By Corollary R5.1, R0 at `d_retr` emits the retraction triple `(∅, {(a, δ(1, #a))}, R)`, depositing a fresh emitter address `b` with `Σ'.L(b) = (∅, {(a, δ(1, #a))}, R)`. By PrefixSpanCoverage (ASN-0043), `coverage({(a, δ(1, #a))}) = {t : a ≼ t}`, which contains `a`. Let `(Σ', _) = Nullify(Σ, d_retr, a)`. By Definition of `nullified`, `a ∈ nullified(Σ')`. By R6a, `a` remains nullified thereafter.

*Single-tuple scope, absolute under R0a.* The to-span's coverage `{t : a ≼ t}` is in principle the entire prefix-subtree of `a` within `T`; restricted to `A_rel^Σ = dom(Σ.L)`, however, R0a's unconditional antichain gives `{a' ∈ dom(Σ.L) : a ≼ a'} = {a}` directly. The class-(iii) `→` step taken by `Emit_R` adds the fresh emitter address `b` produced by K.λ at `d_retr`: `b ∉ dom(Σ.L)` by K.λ's freshness postcondition; `b ≠ a` because K.λ deposits `b` at `[d_retr.0.s_L.1]` (first-emission case) or at `inc(ℓ_prev, 0)` (subsequent-emission case), neither of which can equal `a` — both are fresh against `dom(Σ.L)`, and `a ∈ dom(Σ.L)` by P1; `a ⊀ b` by R0a applied to `dom(Σ'.L) = dom(Σ.L) ∪ {b}`. Therefore `{a' ∈ dom(Σ'.L) : a ≼ a'} = {a}` after the step, and `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`: Nullify's `→` step contributes exactly `a` to `nullified(Σ')`, never a sub-tree of `A_rel`. Single-tuple scope is *absolute* — a substrate-level guarantee, by R0a.

The arity-3 restriction matches this note's scope. `A_K^Σ` is defined only over standard-triple links (Definition of `L_K^Σ`), so the active-subset effect of Nullify is meaningful only on arity-3 addresses. Nullifying a higher-arity address (`|Σ.L(a)| > 3`) would be a well-formed Emit_R, and would deposit `a` into `nullified(Σ')`, but no `A_K^{Σ'}` would feel the effect under the present definitions.

**Definition — Unit-depth retraction discipline.** A layer satisfies the *unit-depth retraction discipline* iff every `L_R^Σ` tuple, in every state Σ the layer reaches, has a to-endset of the form `{(b, δ(1, #b))}` for some target `b ∈ A_rel^Σ` — equivalently, every `L_R^Σ` tuple was produced by a `Nullify(Σ, d_retr, b)` call. Because K.λ constrains every emission *address* to the sibling-frontier chain but leaves the *shape* of a link's endsets unconstrained, the discipline is a layer commitment, not a substrate guarantee — a crafted broader-coverage retraction such as `Emit_R(Σ, d_retr, ∅, {(d, δ(1, #d))})` is L-invariant-conforming yet violates it.

**Definition — substrate-conforming layer.** A layer is *substrate-conforming* iff every operation it publishes over `(Σ.C, Σ.M, Σ.L)` satisfies both of the following at every step. Clause (a) enumerates the propositional invariants it must preserve; clause (b) is a step-local emission condition on each fresh link key.

*(a) Invariant Catalog.* The full L/S/M/C invariant list of ASN-0036, ASN-0043, and ASN-0093, together with the `Link`-record value-shape commitments L5 (EndsetSetSemantics), L6 (SlotDistinction), and L8 (TypeByAddress).

*(b) Chain Discipline Catalog.* Every fresh link key is emitted at its home document's sibling frontier — i.e., the layer preserves the ASN-0093 sub-allocator chain-discipline lemmas. Clause (b) is not implied by clause (a): the tumbler `a* = [d.0.s_L.1.1]` is T10a-conforming and L-invariant-admissible (reachable by an L1c-admissible chain `d → d.0.1 → d.0.2 → d.0.2.1 → d.0.2.1.1`, satisfying L0/L1/L1a/L1b/L1c) yet lies off `A_L(d)`'s sibling-frontier chain, whose outputs have `#E = 2`, not `a*`'s `#E = 3` (R0a-Cor2). Clause (b)'s frontier condition is what excludes such off-frontier keys.

**R7a — NoExtraClassAffectsL.** For any state-affecting transition `Σ ↝ Σ'` issued by a substrate-conforming layer (per the Definition above) with `Σ.L ≠ Σ'.L`, there exists a finite sequence `Σ = Σ_0 → Σ_1 → … → Σ_m` (`m ≥ 1`) of `→`-steps, each of class (i) (K.σ) or class (iii) (K.λ), with `Σ_m.L = Σ'.L`, `dom(Σ_m.M) ⊆ dom(Σ'.M)`, and `dom(Σ_m.C) = dom(Σ.C) ⊆ dom(Σ'.C)`. The `Σ.L`-affecting effect decomposes into class-(iii) K.λ-steps, each prefixed if needed by the class-(i) K.σ-step its L1a home-precondition requires; no class-(ii) content-emission step is introduced (L1a constrains only `home(a_k) ∈ dom(·.M)`, not any content address).

When an `↝`-step is itself a primitive adding a single fresh key (Frame conditions `Σ'.C = Σ.C`, `Σ'.M = Σ.M`), the step *is* a K.λ-step and the sequence has length 1; a composite that simultaneously adds fresh document and link keys decomposes into K.λ-extensions, each prefixed by the K.σ-step its `home(a_k) ∈ dom(Σ_{k-1}.M)` precondition requires at emission.

*Proof.* By substrate-conformance (per the Definition above), every `Σ ↝ Σ'` in scope preserves L12, L12a, L-fin, S0, and S1 at each step — the facts the decomposition consumes. The proof has two structural phases: a monotonicity argument establishing the Δ-enumeration of fresh link addresses, and a K.σ/K.λ replay reconstructing them as `→`-steps.

Under this conformance, every `Σ ↝ Σ'` in scope satisfies `dom(Σ.L) ⊆ dom(Σ'.L)` (L12a), `Σ'.L(a) = Σ.L(a)` for every `a ∈ dom(Σ.L)` (L12), `dom(Σ.C) ⊆ dom(Σ'.C)` (S1), and `Σ'.C(a) = Σ.C(a)` for every `a ∈ dom(Σ.C)` (S0). Therefore any `Σ ↝ Σ'` with `Σ.L ≠ Σ'.L` must extend `dom(Σ.L)` by at least one fresh address: modification of existing entries is forbidden by L12, and removal is forbidden by L12a, so the only remaining mechanism for changing `Σ.L` is a strict extension `dom(Σ'.L) ⊋ dom(Σ.L)`. Let `Δ := dom(Σ'.L) \ dom(Σ.L)`; by L-fin (LinkStoreFiniteness, ASN-0043), both `dom(Σ.L)` and `dom(Σ'.L)` are finite, so `Δ` is a finite, non-empty set of fresh addresses. Enumerate `Δ` in any order as `a_1, …, a_n` (`n ≥ 1`).

At the substrate-model interface, the State transition relation paragraph commits K.σ/K.α/K.λ (classes (i)/(ii)/(iii)) as the *complete* primitive vocabulary of `→`. K.λ's admission requires `home(a_k) ∈ dom(·.M)` (L1a), which K.λ itself does not extend. K.σ's admission requires only freshness against `dom(·.M)` plus S7d's structural commitments (`T4-valid(d) ∧ zeros(d) = 2`).

We construct the replay sequence by interleaving: for each `k ∈ {1, …, n}`, set `d_k := home(a_k)` (computed from the fresh address `a_k` alone, by L1a's home-projection) and `(F_k, G_k, K_k) := Σ'.L(a_k)` (the literal value stored at `a_k` in Σ', well-defined since `a_k ∈ dom(Σ'.L)`). At each iteration `k`, if `d_k ∉ dom(Σ_{prev}.M)` for the running predecessor state `Σ_{prev}`, prefix a K.σ-step `Σ_{prev} → Σ_{prev}'` extending `dom(Σ_{prev}.M)` with `d_k` (K.σ's Frame guarantees `Σ_{prev}'.L = Σ_{prev}.L` and `Σ_{prev}'.C = Σ_{prev}.C`, so this prefix step does not advance `Σ.L` or `Σ.C`). The K.σ-step's preconditions discharge as follows: `d_k ∈ dom(Σ'.M)` (by L1a applied to `a_k` at Σ' in the original `↝`-step), so Σ' satisfies S7d at `d_k`, giving `T4-valid(d_k) ∧ zeros(d_k) = 2` — the structural commitments K.σ requires; freshness against `Σ_{prev}.M` is the case hypothesis `d_k ∉ dom(Σ_{prev}.M)`. Then K.λ admits a class-(iii) `→`-step `Σ_{prev}' → Σ_k` emitting `(F_k, G_k, K_k)` at `a_k`. K.λ requires (1) `a_k ∉ dom(Σ_{prev}'.L)`, (2) L0/L1/L1a/L1b at `a_k`, (3) `origin(a_k) = d_k` per K.λ's scoped-allocation precondition, and (4) the first/subsequent emission rule selects `a_k`. We discharge each:

- *(1) Freshness `a_k ∉ dom(Σ_{prev}'.L)`*: the K.σ-prefix held `Σ_{prev}'.L = Σ_{prev}.L`, with `Σ_{prev}.L = Σ.L ∪ {a_1, …, a_{k-1}}` from prior iterations and `a_k` distinct from each by Δ-enumeration and `a_k ∉ dom(Σ.L)` by Δ-membership.
- *(2) L0/L1/L1b at `a_k`*: these are purely structural properties of the address `a_k` itself — `E(a_k)₁ = s_L`, `zeros(a_k) = 3`, `#E(a_k) ≥ 2` — depending only on `a_k`'s tumbler structure, not on any state. The original `↝`-step's post-state Σ' satisfies all three L-invariants at `a_k` (Σ' is a reachable conforming state); since L0/L1/L1b are state-independent predicates over `a_k`, they hold at `a_k` regardless of which state evaluates them. They transfer to `Σ_{prev}'` without further argument.
- *(2/3) L1a at `a_k` (origin/home discharge)*: requires `home(a_k) = origin(a_k) ∈ dom(Σ_{prev}'.M)`. By construction `d_k = home(a_k)` and the K.σ-prefix (if needed) inserted `d_k` into `dom(Σ_{prev}'.M)`; if no prefix was needed, `d_k ∈ dom(Σ_{prev}.M) ⊆ dom(Σ_{prev}'.M)` by the case hypothesis. Either way, `home(a_k) ∈ dom(Σ_{prev}'.M)`.
- *(4) First/subsequent emission rule selects `a_k`*: ASN-0093's K.λ contract deterministically selects the next link address for home `d_k` based on the predicate `{ℓ' ∈ dom(Σ_{prev}'.L) : origin(ℓ') = d_k} = ∅`. We must show that the rule, applied at `Σ_{prev}'`, produces precisely `a_k`. The argument has three parts:
  - *(i) Chain-order existence within each home.* By clause (b) of substrate-conformance (the *Definition — substrate-conforming layer*), every key in `dom(Σ'.L)` was emitted at its home's sibling frontier; ChainMembershipForOrigin — the ASN-0093 theorem that frontier emission yields contiguous homed-sets — therefore holds at Σ' as a *consequence* of conformance, not as a separately imposed step-local invariant. This ASN's R0a-Cor1 re-expresses it for the link store: for each `d_k` the homed set `{a ∈ dom(Σ'.L) : home(a) = d_k}` is `{incʲ(d_k.0.s_L.1, 0) : 0 ≤ j ≤ J_{d_k}^{Σ'}}` — a contiguous initial segment of `A_L(d_k)`'s chain enumeration. This contiguous-prefix structure pins down a canonical chain-order on the home `d_k`'s realized link addresses: each address has a unique chain index `j`, and chain indices totally order the homed set.
  - *(ii) Cross-home iteration order is immaterial under K.λ's per-home determinism.* K.λ's first/subsequent emission predicate at home `d_k` is `{ℓ' ∈ dom(Σ_{prev}'.L) : origin(ℓ') = d_k} = ∅` — *origin-scoped* to `d_k`, depending only on those elements of `dom(Σ_{prev}'.L)` whose origin equals `d_k` and ignoring all other elements. Consequently, the rule's outcome at iteration `k` is a function of `(d_k, {ℓ' ∈ dom(Σ_{prev}'.L) : origin(ℓ') = d_k})` alone; emissions homed at other documents in earlier iterations contribute to `dom(Σ_{prev}'.L)` but not to the origin-scoped homed-set at `d_k`, so they do not alter K.λ's outcome at `d_k`. Cross-home interleaving in the Δ-enumeration is therefore immaterial — any iteration order produces the same outcome at each home, provided within-home chain-order is respected.
  - *(iii) Iteration in chain-order at each home selects `a_k`.* Re-order the Δ-enumeration so that fresh addresses homed at the same `d_k` appear in chain-order from least to greatest chain index. The re-enumeration is permissible by (ii) since Δ is finite, and within-home chain-order is well-defined as a total order on each home's fresh addresses: by R0a-Cor1 at Σ' (a consequence of (i)) each homed-set is a contiguous initial segment of `A_L(d_k)`'s chain enumeration, and by ChainEnumerationInjectivity (ASN-0093) each address corresponds to a *unique* chain index — the chain-index-to-address map is injective, so distinct addresses at the same home occupy distinct chain indices and within-home ordering by chain index is total. Under this ordering, each `a_k` is the chain element at the next available chain index past the prior realized prefix at the same home; K.λ's first/subsequent rule, evaluated against the origin-scoped homed-set at `Σ_{prev}'`, produces exactly this chain element. The discharge of "first occurrence at `d_k`" splits by whether `d_k` was introduced by a K.σ-prefix at this iteration or was already in `dom(Σ.M)`; "subsequent occurrence at `d_k`" reduces to a single chain-extension step common to both cases.
    - *Case A — fresh `d_k` (K.σ-prefix fired at this iteration's start; `d_k ∉ dom(Σ_{prev}.M)` before the prefix).* The K.σ-prefix extended `dom(Σ_{prev}.M)` with `d_k`, and K.σ's Frame fixed `Σ_{prev}'.L = Σ_{prev}.L`. Before the prefix, `d_k ∉ dom(Σ_{prev}.M)`; by L1a, no element of `dom(Σ_{prev}.L)` had `home(·) = d_k`. Therefore at `Σ_{prev}'`, the origin-scoped homed-set `{ℓ' ∈ dom(Σ_{prev}'.L) : origin(ℓ') = d_k} = ∅`, K.λ's first-emission branch fires, and the deposit address is `[d_k.0.s_L.1]` — the chain element at chain index 0 of `A_L(d_k)`. R0a-Cor1 at Σ' places this `a_k` at chain index 0 of the homed prefix at `d_k`, so the deposit equals `a_k`.
    - *Case B — existing `d_k` (no K.σ-prefix needed; `d_k ∈ dom(Σ_{prev}.M)` from the outset of the replay).* The homed-set at `d_k` in `Σ_{prev}'` already contains the pre-existing realized prefix `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_k}`, which R0a-Cor1 at Σ gives as `{inc^j(d_k.0.s_L.1, 0) : 0 ≤ j ≤ J_{d_k}^Σ}` for some `J_{d_k}^Σ ∈ ℤ_{≥-1}`. *Sub-case B1 (`J_{d_k}^Σ = -1`, pre-existing homed-set empty):* the first-emission branch fires, and the deposit `[d_k.0.s_L.1]` equals `a_k` at chain index 0 — discharged identically to Case A. *Sub-case B2 (`J_{d_k}^Σ ≥ 0`, pre-existing homed-set non-empty):* the subsequent-emission branch fires with `ℓ_prev = inc^{J_{d_k}^Σ}(d_k.0.s_L.1, 0)` (the T1-max of the pre-existing prefix by ChainEnumerationInjectivity), and `inc(ℓ_prev, 0)` lands at chain index `J_{d_k}^Σ + 1` of `A_L(d_k)` — the next chain index past the pre-existing prefix, which R0a-Cor1 at Σ' assigns to this `a_k` by the contiguous-extension structure.
    - *Subsequent occurrences (both cases).* At each subsequent occurrence of `d_k` in the re-ordered enumeration, the prior iteration has just emitted the immediately preceding chain element of `A_L(d_k)`. K.λ's subsequent-emission branch fires with `ℓ_prev` equal to that prior chain element, and `inc(ℓ_prev, 0)` lands at the next chain index of `A_L(d_k)` — exactly the position R0a-Cor1 at Σ' assigns to this `a_k` by the contiguous-extension structure.

Discharges (1)–(4) cover each replay step's preconditions; each replay step is a primitive K-op (a K.σ-prefix or a K.λ-emission) and preserves the full invariant and chain-discipline catalog by its own ASN-0093 contract. The only step-specific obligations are the L14/L14a fresh-key obligation at each K.λ-emission (FreshLinkKeyDisjointness, SC-NEQ exclusion of `a_k`) and the chain-membership obligation of discharge (4).

After all `n` iterations (interleaved with at most `n` K.σ-prefixes when home documents were not already in `dom(Σ.M)`), the running `Σ_m.L = Σ.L ⊕ {a_1 ↦ (F_1, G_1, K_1), …, a_n ↦ (F_n, G_n, K_n)} = Σ'.L`, and `dom(Σ_m.M) ⊆ dom(Σ'.M)` because each K.σ-prefix introduced only a `d_k ∈ dom(Σ'.M)`. The construction introduces no K.α (class-(ii)) content-emission steps: L1a's precondition on each K.λ-emission depends only on `home(a_k) ∈ dom(Σ_{prev}.M)`, not on any content address, so `dom(Σ_m.C) = dom(Σ.C)` throughout, and `dom(Σ.C) ⊆ dom(Σ'.C)` follows from S1 on the original `↝`-step. ∎

The single-fresh-home case is the `n = 1` collapse: a composite that allocates one fresh document `d_new` and emits one link `a_new = d_new.0.s_L.1` homed at it decomposes into the length-2 sequence (one K.σ-prefix discharging L1a, then one first-emission K.λ). The interleaving structure below subsumes it.

*Worked example — composite create-two-fresh-documents-each-with-initial-link (length-4 decomposition).* The decomposition's interleaving structure is exercised non-trivially when a single `↝`-step affects multiple fresh home documents. Consider a higher-layer operation `CreateTwoDocsAndLinks` that, in a single atomic `↝`-step, allocates two fresh documents `d_A`, `d_B` and emits one initial link homed at each. Concretely: `Σ` has `dom(Σ.M) = ∅` and `dom(Σ.L) = ∅`. The composite `↝`-step `Σ ↝ Σ'` produces `Σ'` with `dom(Σ'.M) = {d_A, d_B}` and `dom(Σ'.L) = {a_A, a_B}` where `home(a_A) = d_A`, `home(a_B) = d_B`, `a_A = d_A.0.s_L.1`, `a_B = d_B.0.s_L.1`, and `Σ'.L(a_X) = (F_X, G_X, K_X)` for `X ∈ {A, B}` (each an L3-conforming triple).

R7a's construction decomposes this composite into a length-4 `→`-sequence `Σ → Σ_1 → Σ_2 → Σ_3 → Σ_4 = Σ_m` (so `m = 4`):

- *Step 1 (K.σ at d_A):* `Σ → Σ_1` extending `dom(Σ.M)` from `∅` to `{d_A}`. K.σ's Frame fixes `Σ_1.L = Σ.L = ∅` and `Σ_1.C = Σ.C = ∅`.
- *Step 2 (K.λ at a_A under d_A):* `Σ_1 → Σ_2` emitting `(F_A, G_A, K_A)` at `a_A = d_A.0.s_L.1` (K.λ's first-emission case at `d = d_A` against `{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = d_A} = ∅`). After Step 2: `dom(Σ_2.M) = {d_A}`, `dom(Σ_2.L) = {a_A}`.
- *Step 3 (K.σ at d_B):* `Σ_2 → Σ_3` extending `dom(Σ_2.M)` to `{d_A, d_B}`. K.σ's Frame fixes `Σ_3.L = Σ_2.L = {a_A}` and `Σ_3.C = Σ_2.C = ∅`.
- *Step 4 (K.λ at a_B under d_B):* `Σ_3 → Σ_4` emitting `(F_B, G_B, K_B)` at `a_B = d_B.0.s_L.1` (K.λ's first-emission case at `d = d_B` against `{ℓ' ∈ dom(Σ_3.L) : origin(ℓ') = d_B} = ∅` — `a_A` is homed at `d_A ≠ d_B`, so the homed-set at `d_B` is empty). After Step 4: `dom(Σ_4.M) = {d_A, d_B} = dom(Σ'.M)`, `dom(Σ_4.L) = {a_A, a_B} = dom(Σ'.L)`.

The Δ-enumeration is `a_1 = a_A, a_2 = a_B` (or, equivalently, `a_1 = a_B, a_2 = a_A` — the algorithm independently triggers a K.σ-prefix per fresh home regardless of the iteration order). The home-precondition discharge fires twice (once per iteration), each time triggering a K.σ-prefix for a distinct fresh document. The class-(iii) emissions are then issued at the new homes in order. This decomposition exhibits the interleaved K.σ–K.λ–K.σ–K.λ structure that R7a's iteration loop produces when multiple fresh home documents are emitted simultaneously — the iteration's home-document precondition discharge fires across distinct fresh home documents, not just at iteration 1.

**Definition — relational layer.** The relational layer's operations are `{Emit_K, Observe_K, Nullify}`, with `Nullify` a definitional alias for `Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` — `Emit_K` instantiated at three argument positions: `K := R`, `F := ∅`, `G := {(a, δ(1, #a))}`. The layer commits to `Emit_K` (operationally K.λ specialized to standard-triple value `(F, G, K)`) as its sole state-affecting class-(iii) emission, and admits no composites that touch `Σ.L` indirectly. *Nullify-as-sole-`R`-producer discipline:* the layer further commits that callers may invoke `Emit_K` only at type indices `K` satisfying `K ≁ R` (i.e., `coverage(K) ≠ coverage(R)`); every `R`-typed emission is routed through the `Nullify` alias, whose argument shape is fixed to the unit-depth retraction form `(∅, {(a, δ(1, #a))})` by Definition of `Nullify`. Together these two commitments make the layer satisfy the *unit-depth retraction discipline* (per the named Definition above) by construction for all layer-initiated state, rather than as a separately-tracked caller obligation. `Observe_K` is state-preserving, taking no `→`-step.

*Corollary (reduction to Emit_K).* The relational layer's state-affecting operations reduce to `{Emit_K}` (with `Nullify` as alias).

*Proof.* The layer admits no composites that bundle document allocation with link emission, so R7a's multi-step branch with class-(i) prefix never fires for relational-layer-initiated operations. The layer issues `Emit_K` only when its `d ∈ dom(Σ.M)` precondition is already established, so R7a's replay sequence collapses to length 1: each relational-layer state-affecting operation is itself a single-step class-(iii) `→`-step. By the layer's commitment, every such step is an `Emit_K` call.


## Weakest-Precondition Analysis

The operations' postconditions admit explicit weakest-precondition (wp) computations in two operationally-relevant cases — Nullify's single-tuple scope and Emit_K's membership of the fresh tuple in the active subset. Both cases use the standard wp notation `wp(S, R)`: the weakest predicate over the prior state Σ that guarantees the post-state Σ' satisfies R after S executes.

*Case 1 — wp(Nullify(Σ, d_retr, a), "single-tuple scope holds at Σ'").* The "single-tuple scope" postcondition is `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` (the to-span's `A_rel`-intersection at Σ' is exactly `a`, with no other link address falling within the prefix-subtree of `a`). Working backward through Nullify's definition `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`:

`wp(Nullify(Σ, d_retr, a), single-tuple scope at Σ') ≡ P0(Σ, d_retr) ∧ P1(Σ, a)`

where P0: `d_retr ∈ dom(Σ.M)` and P1: `a ∈ A_rel^Σ`. *Sufficiency:* P1 combined with L12a discharges `a ∈ A_rel^{Σ'}`, and the only other requirement — that no other link address fall within `{t : a ≼ t}` at Σ' — is `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`, a purely *address-prefix* property of `a` against `dom(Σ'.L)`. It is discharged by R0a's antichain on `dom(Σ.L)` together with `a ∈ A_rel^{Σ'}`: the internal Emit_R's fresh emitter `b` is prefix-incomparable with `a` at Σ' (`b ∉ {t : a ≼ t}`) by R0a applied to `dom(Σ'.L)`.

*Necessity (each conjunct is load-bearing):* dropping P1 admits `a ∉ A_rel^Σ`; the only new key at Σ' is the fresh emitter `b ≠ a`, so by L12a's pointwise agreement `a ∉ dom(Σ'.L) = A_rel^{Σ'}`, whence `a ∉ {t : a ≼ t} ∩ A_rel^{Σ'}` and the intersection cannot equal `{a}`. Dropping P0 admits `d_retr ∉ dom(Σ.M)`, leaving the internal `Emit_R`'s K.λ home-precondition undischarged: Nullify does not execute, no post-state Σ' is produced, and the postcondition is unreachable. Hence `P0 ∧ P1` is weakest, not merely sufficient.

Single-tuple scope is therefore *arity-independent*: nullifying an arity-4 address would establish `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` identically, since the argument consults only `a`'s tumbler prefix and the antichain, never `|Σ.L(a)|`. Nullify's third precondition P2: `|Σ.L(a)| = 3` is carried only because Nullify's contract restricts the operation to standard-triple addresses — a *meaningfulness* guard for the downstream active-subset effect (only arity-3 addresses populate some `A_K`), not a correctness obligation for this postcondition. Accordingly P2 is absent from the wp above. The wp likewise does *not* include any conjunct on whether the internal emitter `b` is itself nullified — that is a property of `A_R^{Σ'}`, not of single-tuple scope on `a`, and is outside this wp's postcondition.

*Case 2 — wp(Emit_K(Σ, d, F, G), "(a, F, G) ∈ A_K^{Σ'}").* The Definition of `Emit_K` guarantees `(a, F, G) ∈ L_K^{Σ'}` for the fresh emission unconditionally (K.λ deposits `(F, G, K)` at the chain-deterministic address `a`, which is then a member of `L_K^{Σ'}` by coverage-equivalence membership), but is silent on `(a, F, G) ∈ A_K^{Σ'}`, which turns on whether `a ∈ nullified(Σ')`. The post-state retraction slice depends on the K-relation: `L_R^{Σ'} = L_R^Σ ∪ {(a, F, G)}` when `K ~ R`, and `L_R^{Σ'} = L_R^Σ` when `K ≁ R`. We compute the wp for a *direct K.λ caller* — the most permissive scope, in which the substrate imposes no shape constraint on retraction to-spans and no restriction on the type index. Under this scope all three regimes below are live; the relational layer's specialization is noted afterward. Three regimes are operationally relevant — two characterize the pre-state retraction landscape, and a third orthogonal one handles self-nullification under `K ~ R`:

(i) *Unit-depth retraction discipline.* If every `L_R^Σ` tuple is the result of a `Nullify` call — i.e., every retraction has a unit-depth to-span of the form `{(b, δ(1, #b))}` for some target `b ∈ A_rel^Σ` — then each retraction's coverage `{t : b ≼ t}` intersected with `A_rel^{Σ'}` reduces to `{b}` by R0a's antichain on `dom(Σ'.L)`. The fresh `a` produced by Emit_K is, by K.λ's first/subsequent emission rule together with R0a, prefix-incomparable with every `b ∈ A_rel^Σ`. Therefore `a` is not in `coverage(G')` for any `(_, _, G') ∈ L_R^Σ`, hence the pre-state retractions do not nullify `a`.

(ii) *Crafted-span retractions admitted.* Although K.λ enforces the sibling-frontier discipline on emission *addresses*, it does not constrain the *shape* of a link's endsets — in particular, a caller may emit an `R`-typed retraction with a broader-coverage to-span via direct K.λ, e.g. `Emit_R(Σ, d_retr, ∅, {(d, δ(1, #d))})`, whose coverage `{t : d ≼ t}` intersected with `A_rel^Σ` covers every link sited under `d` (and propagates to every link subsequently emitted under `d`, since R3 preserves the retraction tuple). If any `L_R^Σ` tuple has such a crafted span, a fresh `a` emitted under a covered home falls within `coverage(L_R^Σ)` immediately upon emission: `a ∈ nullified(Σ')` at the very step that allocates `a`, and `(a, F, G) ∈ L_K^{Σ'} \ A_K^{Σ'}` — the audit slice records the emission, but the active subset excludes it from emission onward.

(iii) *Self-nullifying R-typed emission.* Orthogonal to (i)/(ii): when `K ~ R`, the fresh emission enters `L_R^{Σ'}` and its own to-set coverage participates in the nullification check at Σ'. If `a_emit(Σ, d) ∈ coverage(G)` — the fresh emitter's address lies within its own to-set coverage — then `a ∈ nullified(Σ')` via the just-emitted tuple itself, independent of any pre-existing retractions, and `(a, F, G) ∈ L_K^{Σ'} \ A_K^{Σ'}` at the very step that allocates `a`. When `K ≁ R`, the fresh tuple is not in `L_R^{Σ'}` and contributes nothing to `nullified(Σ')`; this regime is vacuous.

To back the postcondition through Emit_K's behavior we name the fresh address that K.λ will deposit:

*Definition — `a_emit(Σ, d)`.* For `d ∈ dom(Σ.M)`, the *fresh emission address* `a_emit(Σ, d)` is the address K.λ would deposit at home `d` in state Σ, per K.λ's first/subsequent emission rule:

`a_emit(Σ, d) = [d.0.s_L.1]` when `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅` (first-emission branch);
`a_emit(Σ, d) = inc(ℓ_prev, 0)` otherwise, where `ℓ_prev := max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` (subsequent-emission branch).

By the Lemma — Emit_K function-ness, the rule's outcome is uniquely determined by `(Σ, d)`, so `a_emit` is a function. The address `a` that `Emit_K(Σ, d, F, G)` deposits is exactly `a_emit(Σ, d)` (the type-index `K` parameterizes the slot-3 value, not the address selection).

*Definition — `NoCraftedSpanReachesD(Σ, d)`.* The predicate "no pre-existing retraction's to-span coverage contains the address Emit_K is about to deposit under `d`" is

`NoCraftedSpanReachesD(Σ, d) ≡ (A (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∉ coverage(G'))`

— a universal over the audit-slice retraction tuples, asserting that none of their to-set coverages contains the fresh sibling-frontier address. With these auxiliaries the wp reads:

`wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ NoCraftedSpanReachesD(Σ, d) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`

*Sufficiency.* The first three conjuncts characterize the pre-state retraction landscape (regimes (i)/(ii) jointly): `d ∈ dom(Σ.M)` and `K ∈ T_admissible` are Emit_K's own preconditions, and `NoCraftedSpanReachesD(Σ, d)` rules out nullification by any pre-existing `L_R^Σ` tuple. The final conjunct excludes regime (iii): either `K ≁ R` (so the fresh tuple is not in `L_R^{Σ'}` and cannot self-nullify) or `a_emit(Σ, d) ∉ coverage(G)` (so the self-targeting precondition for self-nullification fails). With all four conjuncts in force, no `L_R^{Σ'}` tuple — pre-existing or just-emitted — has to-coverage containing `a = a_emit(Σ, d)`, so `a ∉ nullified(Σ')`, and since `(a, F, G) ∈ L_K^{Σ'}` holds unconditionally for the fresh emission, `(a, F, G) ∈ A_K^{Σ'}`.

*Necessity (each conjunct is load-bearing):* dropping `d ∈ dom(Σ.M)` leaves Emit_K's K.λ home-precondition undischarged: Emit_K does not execute, no post-state Σ' is produced, and the postcondition is unreachable. Dropping `K ∈ T_admissible` admits `K = ∅` (the sole non-admissible endset), so the value `(F, G, ∅)` violates K.λ's `e₃ ≠ ∅` precondition (L3); again Emit_K does not execute and no Σ' exists. Dropping `NoCraftedSpanReachesD(Σ, d)` admits a state with some `(b, F', G') ∈ L_R^Σ` such that `a_emit(Σ, d) ∈ coverage(G')` (the regime-(ii) crafted-span witness, e.g. an `L_R^Σ` tuple with to-span `{(d, δ(1, #d))}` covering the whole subtree under `d`); by R3, `(b, F', G') ∈ L_R^{Σ'}`, so `a = a_emit(Σ, d) ∈ coverage(G')` puts `a ∈ nullified(Σ')`, whence `(a, F, G) ∈ L_K^{Σ'} \ A_K^{Σ'}` — the postcondition fails. Dropping the final disjunct admits its negation `K ~ R ∧ a_emit(Σ, d) ∈ coverage(G)`: the fresh emission enters `L_R^{Σ'}` (since `K ~ R`) as a tuple with to-set `G`, and `a = a_emit(Σ, d) ∈ coverage(G)` makes it self-witness `a ∈ nullified(Σ')`, again falsifying `(a, F, G) ∈ A_K^{Σ'}` (regime (iii)). Hence the four-conjunct conjunction is weakest, not merely sufficient.

Under the unit-depth retraction discipline (regime (i) holds for the pre-state), `NoCraftedSpanReachesD` is automatic — every `L_R^Σ` tuple has to-span coverage `{t : b ≼ t}` for some `b ∈ A_rel^Σ`, and R0a's antichain on `dom(Σ'.L)` puts `a_emit(Σ, d) ∉ {t : b ≼ t} ∩ A_rel^{Σ'}` for every such `b` — and the wp simplifies to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`.

*Relational-layer specialization.* When the caller is the relational layer rather than direct K.λ, its Nullify discipline narrows this wp by construction: Nullify emits only unit-depth to-spans, so `NoCraftedSpanReachesD(Σ, d)` holds at every call site by R0a (regime (i)), and the Nullify-as-sole-`R`-producer rule keeps every direct `Emit_K` at `K ≁ R`, so the final disjunct holds trivially. The wp then specializes to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`. The full four-conjunct form above remains the honest precondition for direct K.λ callers, which the substrate does not preclude.

The Nullify operation scopes its retraction to the unit-depth-span form (regime (i)); whether the wider crafted-span form (regime (ii)) or self-nullifying R-typed emission (regime (iii)) is admitted is a discipline-level property of caller retraction practice, not a K.λ guarantee.

## Worked Sketch

We illustrate the structure of a retraction cycle in the relational vocabulary, building on the ASN-0043 worked example. Concrete tumbler values are fixed up front; the cycle proceeds in four steps: first, a first-emission step establishing the initial state `Σ_0` from a link-empty precursor `Σ_{-1}` (Step 0); then a retraction (Step 1), a restoration (Step 2), and a retraction-of-the-retractor exhibiting R6b's non-fixpoint semantics (Step 3). Step 0 exercises K.λ's first-emission branch (predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅`); Steps 1, 2, and 3 each exercise the subsequent-emission branch (predicate negated).

*Setup.* Fix:

- `s_L = 2` (link subspace identifier — matching ASN-0093 SubspaceConventionAxiom and the ASN-0043 worked example).
- `d = 1.0.1.0.1` — document address, `zeros(d) = 2`, length `5`, T4-valid; `d ∈ dom(Σ_{-1}.M)` (already allocated by some prior K.σ step at or before `Σ_{-1}`).
- `c₁ = 1.0.1.0.1.0.1.1`, `c₂ = 1.0.1.0.1.0.1.2` — two content addresses in `dom(Σ_{-1}.C)`, both with `subspace_I = 1 = s_C`, `zeros = 3`, depth `8`. Both result from prior K.α invocations at home `d`: `c₁` is the first emission of `A_C(d)` per FirstEmission (ASN-0093) (concretely `c₁ = [d.0.s_C.1]` with `s_C = 1`), and `c₂ = inc(c₁, 0)` is the second per the sibling recurrence — placing the example state in the substrate's K-operation vocabulary, parallel to Step 0's K.λ first-emission of `a₁` from `A_L(d)`.
- `k = 3`, `r = 4` — single-component ghost addresses for the classification type `K = {(k, δ(1, 1))}` and the retraction coverage class `[R]` with `R = {(r, δ(1, 1))}`. By construction `coverage(K) ∩ coverage(R) = ∅` (first components 3 and 4 differ; no tumbler extends both prefixes); `K` and `R` lie in distinct coverage classes. *T4-validity note.* Type-endset ghost addresses (per L9, TypeGhostPermission, ASN-0043) need not satisfy T4 — `T4-valid(·)` is required only of allocator outputs under T10a (S7d for documents, ASN-0093 L1c for links). We choose single-component tumblers here to keep the worked sketch's ghosts T4-valid by inspection, but deeper non-T4 tumblers (e.g., `3.0.0.0.1`) would also be admissible.
- `F₁ = {(c₁, δ(1, 8))}`, `G₁ = {(c₂, δ(1, 8))}` — singleton-span endsets covering `c₁` and `c₂` respectively (by PrefixSpanCoverage).
- `Σ_{-1}.L = ∅`, so `L_K^{Σ_{-1}} = ∅`, `L_R^{Σ_{-1}} = ∅`, `nullified(Σ_{-1}) = ∅`, `A_K^{Σ_{-1}} = ∅`.

*Step 0 — first-emission case: K.λ at `d` from empty homed-set, exhibiting `a₁`.* `Σ_{-1} → Σ_0` via `K.λ` (equivalently `Emit_K(Σ_{-1}, d, F₁, G₁)`) emitting `(F₁, G₁, K)` at home `d`. ASN-0093's K.λ first-emission predicate `{ℓ' ∈ dom(Σ_{-1}.L) : origin(ℓ') = d} = ∅` fires (`dom(Σ_{-1}.L) = ∅`), so K.λ deposits at `[d.0.s_L.1]`. Computing concretely: `d = 1.0.1.0.1`, so `d.0` extends `d` with a zero at position 6 to give `1.0.1.0.1.0`; `d.0.s_L = 1.0.1.0.1.0.2`; and `d.0.s_L.1 = 1.0.1.0.1.0.2.1`. So `a₁ := [d.0.s_L.1] = 1.0.1.0.1.0.2.1` (`= t_1^L(d)` by FirstEmission, ASN-0093).

K.λ's effect at this step deposits `Σ_0.L = {a₁ ↦ (F₁, G₁, K)}` with `Σ_0.M = Σ_{-1}.M` and `Σ_0.C = Σ_{-1}.C` per K.λ's Frame. Verification at `a₁`: `zeros(a₁) = 3`, `E(a₁) = [2, 1]`, `E(a₁)₁ = 2 = s_L`, `#E(a₁) = 2` (witnessing R0a-Cor2), T4-valid, `origin(a₁) = home(a₁) = 1.0.1.0.1 = d`. ✓ FirstEmissionFreshness (ASN-0093) gives `a₁ ∉ dom(Σ_{-1}.L) ∪ dom(Σ_{-1}.C)` at the K.λ-event committing `a₁`. By R0 (TupleAddressFreshness) and R1 (AddressInjectivity), `a₁` is a fresh, distinct tuple address.

After Step 0: `L_K^{Σ_0} = {(a₁, F₁, G₁)}` (witnessing R3 over the empty `L_K^{Σ_{-1}}`); `L_R^{Σ_0} = ∅`; `nullified(Σ_0) = ∅`; `A_K^{Σ_0} = L_K^{Σ_0} = {(a₁, F₁, G₁)}`. By R0a-Cor1 at Σ_0 with `J_d^{Σ_0} = 0`, the homed-link set at `d` is the singleton prefix `{a₁} = {inc⁰(d.0.s_L.1, 0)}` of `A_L(d)`'s chain enumeration. ✓

*Step 1: Nullify a₁.* `Σ_0 → Σ_1` via `Nullify(Σ_0, d, a₁) = Emit_R(Σ_0, d, ∅, {(a₁, δ(1, 8))})` — the retractor here happens to share `a₁`'s home document, so the caller supplies `d_retr = d`; a different caller homed at `d' ∈ dom(Σ_0.M)` with `d' ≠ d` would supply `Nullify(Σ_0, d', a₁)` instead, with identical effect on `nullified(Σ_1)`. This emission's to-set `{(a₁, δ(1, 8))}` references the link address `a₁` — witnessing *R5* (TupleSelfTargeting): the to-set of an `L_R` tuple refers to another link's address.

Emit_R invokes K.λ at home `d`. The first/subsequent emission predicate fires *subsequent* (since `{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = d} = {a₁} ≠ ∅`); `ℓ_prev := max{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = d} = a₁`; K.λ deposits at `inc(a₁, 0) = 1.0.1.0.1.0.2.2`. Set `b₁ = 1.0.1.0.1.0.2.2` — by ChainEnumerationInjectivity (ASN-0093), `b₁` is the second chain element of `A_L(d)` (the first being `a₁ = t_1^L(d)`). By T10a.2 (NonNestingSiblingPrefixes, ASN-0034), `a₁` and `b₁` are distinct siblings of `A_L(d)` and are therefore prefix-incomparable; in particular `a₁ ⊀ b₁` — witnessing *R0* (TupleAddressFreshness): `b₁ ∉ dom(Σ_0.L)` is fresh by FirstEmissionFreshness's generalization through subsequent emissions (chain elements are distinct, and the realized prefix is `{a₁}` at Σ_0, so `b₁` is the next chain index not yet realized).

*L-invariant verification at `b₁`.* R0 verifies each L-invariant against an arbitrary K.λ-emitted address; the concrete `b₁ = 1.0.1.0.1.0.2.2` admits the same checks by direct inspection: L0 (`E(b₁)₁ = 2 = s_L`), L1 (`zeros(b₁) = 3` by (UZ)), L1a (`origin(b₁) = home(b₁) = d`), L1b (`#E(b₁) = 2` by (UL)), L1c (the structural chain from `d` through `b_L(d)` through `a₁` to `b₁` exists by ChainDiscipline + FirstEmission, ASN-0093). ✓ The remaining L-invariants (L2, L3, L4(c), L11a, L12, L12a, L12b, L14, L14a, L-fin) discharge by R0's generic argument applied with the concrete `b₁`.

Emit the retraction: `Σ_1.L = Σ_0.L ∪ {b₁ ↦ (∅, {(a₁, δ(1, 8))}, R)}`. Now compute:

- `coverage({(a₁, δ(1, 8))})`: by PrefixSpanCoverage with `#a₁ = 8`, `= {t : a₁ ≼ t}`. Membership: `a₁ ∈ coverage` by reflexivity of `≼`; `b₁ ∉ coverage` since `a₁` and `b₁` agree on positions `1..7` (both `1.0.1.0.1.0.2`) but differ at position `8` (`1` vs `2`) at equal length — neither is a prefix of the other. ✓
- `L_K^{Σ_1} = {(a₁, F₁, G₁)}` — unchanged. Witnesses *R3* (TypedSliceMonotonicity): `L_K^{Σ_0} = {(a₁, F₁, G₁)} ⊆ L_K^{Σ_1}` since the emission targets `L_R`, not `L_K`. Also witnesses *R2* (TupleAddressPermanence): `Σ_1.L(a₁) = Σ_0.L(a₁) = (F₁, G₁, K)`. ✓
- `L_R^{Σ_1} = {(b₁, ∅, {(a₁, δ(1, 8))})}` — the only retraction tuple; no other tuple has type slot coverage-equivalent to `R` (the tuple at `a₁` has type `K` with `coverage(K) ≠ coverage(R)`). Also witnesses *R3* applied to the `R` coverage class: `L_R^{Σ_0} = ∅ ⊆ L_R^{Σ_1}`. ✓
- `nullified(Σ_1) = {a ∈ {a₁, b₁} : a ∈ coverage({(a₁, δ(1, 8))})} = {a₁}`. By Definition of `nullified`, the existential ranges over `L_R^{Σ_1}` (audit slice), so the test is whether `(b₁, ∅, {(a₁, δ(1, 8))}) ∈ L_R^{Σ_1}` directly witnesses `a₁ ∈ coverage(G')` — yes — without recursive evaluation of `b₁`'s status. Witnesses *R6b* (SingleDepthRetraction). ✓
- `A_K^{Σ_1} = L_K^{Σ_1} \ {(a, F, G) : a ∈ nullified(Σ_1)} = ∅`. ✓

The audit predicate `(a₁, F₁, G₁) ∈ L_K` remains true forever (witnessing *R3*); the operational predicate `(a₁, F₁, G₁) ∈ A_K` flips to false at `Σ_1`.

*Step 2: Restore by re-emission.* To restore the classification, we do *not* attempt to nullify the retraction (which by R6b would be ineffective — single-depth checking ignores it). Instead, `Σ_1 → Σ_2` via `Emit_K(d, F₁, G₁)`, re-using the same home `d` as `a₁`. K.λ at home `d` evaluates the subsequent-emission predicate: `{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = d} = {a₁, b₁} ≠ ∅`; `ℓ_prev := max{a₁, b₁} = b₁` (by T1 lexicographic order, `b₁ > a₁` since they share prefix `1.0.1.0.1.0.2` and differ at position 8 by `2 > 1`); K.λ deposits at `inc(b₁, 0) = 1.0.1.0.1.0.2.3`. Set `a₂ = 1.0.1.0.1.0.2.3` — `A_L(d)`'s third chain element. *R0* witness: `a₂ ∉ dom(Σ_1.L)` is fresh; *R1* (AddressInjectivity) witness: the new tuple address `a₂` is distinct from both `a₁` and `b₁`, so the map `addr` remains injective. L-invariants at `a₂` discharge by R0 applied with substitutions of `a₂` for `b₁`; by R0a-Cor1 at Σ_2, `a₂ = inc²(d.0.s_L.1, 0)` and `a₁, b₁, a₂` are `A_L(d)`'s first three chain elements in order.

Then `Σ_2.L = Σ_1.L ∪ {a₂ ↦ (F₁, G₁, K)}` and:

- `L_K^{Σ_2} = {(a₁, F₁, G₁), (a₂, F₁, G₁)}` — two coverage-class members with identical `(F, G)` at distinct addresses. Witnesses *R3* (monotone extension `L_K^{Σ_1} ⊆ L_K^{Σ_2}`), *R1* (distinct addresses for the two tuples), and *L11b/R2 Consequence* (distinct emissions distinguishable even when content matches). ✓
- `nullified(Σ_2) = {a₁}` — unchanged. Witnesses *R6a* (RetractionStability): `a₁ ∈ nullified(Σ_1) ⟹ a₁ ∈ nullified(Σ_2)`. The only `L_R` tuple is still at `b₁`, whose `coverage(G')` contains `a₁` but not `a₂` since `a₁` and `a₂` are distinct siblings in `A_{a₁}`. *R6b* witnessed again: deciding `a₂ ∈ nullified(Σ_2)` requires only the single-pass check over `L_R^{Σ_2}`, which finds no witnessing tuple. ✓
- `A_K^{Σ_2} = {(a₂, F₁, G₁)}` — the new tuple is active; `a₁` remains in `L_K` but excluded from `A_K` by *R6c* (RestorationByReemission: `(a₁, F₁, G₁) ∈ L_K^{Σ_2} \ A_K^{Σ_2}` for the retracted historical record, and the restoration is the fresh `(a₂, F₁, G₁) ∈ A_K^{Σ_2}` at a different address). ✓

The relational content `(F₁, G₁)` is again present in `A_K`, but at a different tuple address. Provenance and audit cleanly distinguish the two emissions: `a₁` is the historical record, `a₂` is the current assertion.

*Step 3 — Retracting the retractor exhibits R6b's non-fixpoint semantics.* `Σ_2 → Σ_3` via `Nullify(Σ_2, d, b₁) = Emit_R(Σ_2, d, ∅, {(b₁, δ(1, 8))})` — a retraction whose to-set targets the retractor `b₁` itself. Emit_R invokes K.λ at home `d`. The first/subsequent emission predicate fires *subsequent* (since `{ℓ' ∈ dom(Σ_2.L) : origin(ℓ') = d} = {a₁, b₁, a₂} ≠ ∅`); `ℓ_prev := max{a₁, b₁, a₂} = a₂` (by T1 lex order on the shared prefix `1.0.1.0.1.0.2` with last components `1 < 2 < 3`); K.λ deposits at `inc(a₂, 0) = 1.0.1.0.1.0.2.4`. Set `b₂ = 1.0.1.0.1.0.2.4` — `A_L(d)`'s fourth chain element, fresh against `dom(Σ_2.L)` by ChainEnumerationInjectivity. (We use `b₂` for this retraction-of-retractor tuple — consistent with `b₁` for the original retractor — keeping `c₁`/`c₂` reserved for the Setup's content addresses.) L-invariants at `b₂` discharge by R0's generic argument with the concrete `b₂` substituted (L0: `E(b₂)₁ = 2 = s_L`; L1: `zeros(b₂) = 3` by (UZ); L1a: `home(b₂) = d`; L1b: `#E(b₂) = 2` by (UL); L1c: the structural chain extends one step further by ChainDiscipline + FirstEmission, ASN-0093).

Then `Σ_3.L = Σ_2.L ∪ {b₂ ↦ (∅, {(b₁, δ(1, 8))}, R)}` and:

- `L_K^{Σ_3} = {(a₁, F₁, G₁), (a₂, F₁, G₁)}` — unchanged from Σ_2; the new emission targets `L_R`, not `L_K`. Witnesses *R3*. ✓
- `L_R^{Σ_3} = {(b₁, ∅, {(a₁, δ(1, 8))}), (b₂, ∅, {(b₁, δ(1, 8))})}` — both retraction tuples persist (*R3* applied to the `R` coverage class; *R2* preserves the original retraction tuple at `b₁`). ✓
- *Deciding `a₁ ∈ nullified(Σ_3)`.* The tuple `(b₁, ∅, {(a₁, δ(1, 8))}) ∈ L_R^{Σ_3}` has `coverage(G') = {t : a₁ ≼ t}` ∋ `a₁` by reflexivity of `≼`; witness found, so `a₁ ∈ nullified(Σ_3)` — by R6b's single-pass check over the audit slice `L_R^{Σ_3}`, independent of `b₁`'s own status. ✓
- *Deciding `b₁ ∈ nullified(Σ_3)`.* The new tuple `(b₂, ∅, {(b₁, δ(1, 8))})` has `coverage(G') = {t : b₁ ≼ t}`; `b₁ ∈ coverage(G')` by reflexivity. Witness found. `b₁ ∈ nullified(Σ_3)`. ✓
- Computing `nullified(Σ_3) = {a ∈ A_rel^{Σ_3} : (E witness)}`: by inspection on each member of `A_rel^{Σ_3} = {a₁, b₁, a₂, b₂}`:
  - `a₁`: witness `(b₁, …)` above ⟹ `a₁ ∈ nullified(Σ_3)`.
  - `b₁`: witness `(b₂, …)` above ⟹ `b₁ ∈ nullified(Σ_3)`.
  - `a₂`: neither retraction tuple's to-coverage contains `a₂` (a₁ ⋠ a₂ via R0a; b₁ ⋠ a₂ via R0a) ⟹ `a₂ ∉ nullified(Σ_3)`.
  - `b₂`: neither retraction tuple's to-coverage contains `b₂` (a₁ ⋠ b₂ via R0a; b₁ ⋠ b₂ via R0a) ⟹ `b₂ ∉ nullified(Σ_3)`.
  Therefore `nullified(Σ_3) = {a₁, b₁}`. *R6a* witnessed: `a₁ ∈ nullified(Σ_2) ⟹ a₁ ∈ nullified(Σ_3)`. ✓
- `A_K^{Σ_3} = L_K^{Σ_3} \ {(a, F, G) : a ∈ nullified(Σ_3)} = {(a₂, F₁, G₁)}` — *unchanged from `A_K^{Σ_2}`*. The retraction of the retractor `b₁` has no operational effect on the active subset of `K`: `(a₂, F₁, G₁)` remains active because `a₂ ∉ nullified(Σ_3)`, and `(a₁, F₁, G₁)` remains excluded because the original retraction tuple at `b₁` still witnesses `a₁ ∈ nullified(Σ_3)` independently of `b₁`'s own status. ✓
- `A_R^{Σ_3} = L_R^{Σ_3} \ {(a, F, G) : a ∈ nullified(Σ_3)} = {(b₂, ∅, {(b₁, δ(1, 8))})}` — the original retractor at `b₁` is excluded (`b₁ ∈ nullified(Σ_3)`) yet, per R6b, still witnesses `a₁ ∈ nullified(Σ_3)` because `nullified` ranges over the audit slice `L_R^{Σ_3}`, not `A_R^{Σ_3}`. ✓

The retraction of the retractor leaves `A_K^{Σ_3}` unchanged (R6b): restoring `(F₁, G₁)` to active assertion requires fresh emission at a fresh address (Step 2's pattern), not retraction-of-retraction, which only grows `L_R`.

*R0a-Cor1/Cor2 verification at Σ_2 and Σ_3.* The set of link addresses homed at `d` is `{a₁, b₁, a₂} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ 2}` at Σ_2 — a contiguous prefix of `A_L(d)`'s chain enumeration (by ASN-0093 ChainMembershipForOrigin) — so R0a-Cor1 holds at Σ_2 with `J_d^{Σ_2} = 2`. At Σ_3, the homed set extends contiguously to `{a₁, b₁, a₂, b₂} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ 3}`, so R0a-Cor1 holds at Σ_3 with `J_d^{Σ_3} = 3`. ✓ Each of `a₁ = 1.0.1.0.1.0.2.1`, `b₁ = 1.0.1.0.1.0.2.2`, `a₂ = 1.0.1.0.1.0.2.3`, `b₂ = 1.0.1.0.1.0.2.4` has element-field projection of length 2 (E = `[2, 1]`, `[2, 2]`, `[2, 3]`, `[2, 4]` respectively) by (UL), so R0a-Cor2 holds at both Σ_2 and Σ_3. ✓


## Properties Introduced

| Label | Type | Statement |
|-------|------|-----------|
| A^Σ | DEF | Address universe at state Σ: `dom(Σ.C) ∪ dom(Σ.L)` |
| A_doc^Σ, A_rel^Σ | DEF | Partition of `A^Σ` into content addresses (`dom(Σ.C)`) and tuple addresses (`dom(Σ.L)`) |
| T_ghost^Σ | DEF | Ghost addresses at Σ: `T \ (dom(Σ.C) ∪ dom(Σ.L))` — tumblers outside the stored-entity universe, admissible in endset spans by L9 |
| T_admissible | DEF | Admissible types: `{K ∈ Endset : K ≠ ∅}` — the indexing domain for typed relations |
| ~ | DEF | TypeEquivalence: `K ~ K' ≡ coverage(K) = coverage(K')` — coverage-equivalence on admissible types (= L8 lifted) |
| L_K^Σ | DEF | Typed relation (coverage-class slice): `{(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a).e₁ = F ∧ Σ.L(a).e₂ = G ∧ coverage(Σ.L(a).e₃) = coverage(K)}` |
| L^Σ | DEF | Standard-triple link store: `⨆_{[K] ∈ T_admissible / ~} L_K^Σ` |
| addr | DEF | Map `(a, F, G) ↦ a : L^Σ → A_rel^Σ` |
| nullified(Σ) | DEF | Tuple addresses targeted by some `L_R^Σ` to-set |
| A_K^Σ | DEF | Active subset: `{(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}` |
| → | DEF | Dom-extending state transition relation, identified as `K.σ ∪ K.α ∪ K.λ` from ASN-0093; each class-(iii) step is a K.λ-step with its first/subsequent emission rule and its associated frame conditions. Under ASN-0093's M2 (EmptyArrangement) there are no arrangement-modifying transitions, so `→` is the complete dom-extending vocabulary |
| Unit-depth retraction discipline | COMMITMENT | (Three Operations) Layer-level convention: every `L_R^Σ` tuple has to-endset of the form `{(b, δ(1, #b))}` for some target `b ∈ A_rel^Σ` — i.e., every retraction came from a `Nullify` call. The substrate (K.λ) does not enforce this; the relational layer does, by definition of Nullify |
| R0 | LEMMA | TupleAddressFreshness — under precondition `dom(Σ.M) ≠ ∅`, every emission allocates a fresh address. Discharged via ASN-0093 K.λ's first/subsequent emission rule, plus FirstEmissionFreshness (first-emission branch), SubsequentEmissionFreshness (subsequent-emission branch's three-part freshness against same-home chain, cross-home links, and content), L-invariant preservation under K.λ's frame, and ASN-0093 L0 + SC-NEQ for L14/L14a |
| R0a | LEMMA | FlatLinkDomain — `dom(Σ.L)` is an antichain in `≼`. Unconditional under ASN-0093's K.λ contract (= Case 1 cross-home via L1 + L1a; Case 2 same-home via ASN-0093 ChainMembershipForOrigin + (UL) + T3, equivalently via T10a.2) |
| R0a-Cor1 | LEMMA | ContiguousPrefix — `{a ∈ dom(Σ.L) : home(a) = d} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ}` for some `J_d^Σ ∈ ℤ_{≥-1}`; direct re-expression of ASN-0093's ChainMembershipForOrigin lemma |
| R0a-Cor2 | LEMMA | DepthTwoLinkAddresses — `#E(a) = 2` strictly for every `a ∈ dom(Σ.L)`; tightens L1b's `#E ≥ 2` admission to depth-2 strictly (= R0a-Cor1 + (UL) + (UZ) + zero-position stability via TA5(c) + TA5-SigValid + ChainElementT4Validity (ASN-0093) — routing through T10a.4 (ASN-0034) as its underlying hook) |
| R1 | LEMMA | AddressInjectivity — `addr` is an injection (= function property of `Σ.L`) |
| R2 | LEMMA | TupleAddressPermanence — addresses persist with values intact (= L12) |
| R3 | LEMMA | TypedSliceMonotonicity — each `L_K^Σ` is monotone (= L12a + R2) |
| R4 | LEMMA | TupleAddressDisjointness — `A_doc^Σ ∩ A_rel^Σ = ∅` (= SD (StoreDisjointness, ASN-0093), whose underlying derivation is ASN-0093 L0 + SC-NEQ + T7 (SubspaceDisjointness, ASN-0034)) |
| R5 | LEMMA | TupleSelfTargeting — for any `a ∈ A_rel^Σ`, the span `(a, δ(1, #a))` is admissible as an endset member (= L4(c) + L13 + R0's invariant-preservation argument, which imposes no restriction on endset target content) |
| R6a | LEMMA | RetractionStability — once nullified, always nullified (= R3 + R2 + purity of coverage) |
| R6b | DEF-Consequence | SingleDepthRetraction — deciding `a ∈ nullified` is a single flat existential pass over `L_R^Σ` (the audit slice, not the active subset `A_R^Σ`), checking only direct targeting; the witness retractor's own status does not enter the test |
| R6c | LEMMA | RestorationByReemission — formal claim on `→*` (reflexive-transitive closure of dom-extending `→`): restoration is fresh emission, never retraction-of-retraction (= R6a + Reachability definition) |
| R7a | LEMMA | NoExtraClassAffectsL — for any state-affecting `Σ ↝ Σ'` issued by a substrate-conforming layer with `Σ.L ≠ Σ'.L`, the `Σ.L`-affecting effect decomposes into K.λ-steps interleaved with K.σ-setup steps for L1a's home-precondition: `Σ = Σ_0 → Σ_1 → … → Σ_m` (`m ≥ 1`) with `Σ_m.L = Σ'.L`, `dom(Σ_m.M) ⊆ dom(Σ'.M)`, `dom(Σ_m.C) = dom(Σ.C) ⊆ dom(Σ'.C)` (= L12 + L12a + L-fin + L1a + S7d + ASN-0093 K-op frame conditions + ChainDiscipline + FirstEmission + ChainMembershipForOrigin + ChainEnumerationInjectivity for replay determinism + per-step discharge of the full ASN-0036 / ASN-0043 / ASN-0093 invariant-and-chain-discipline catalog) |
| Relational layer | COMMITMENT | Operation set `{Emit_K, Observe_K, Nullify}` + reduction corollary; see Definition — relational layer |
| Emit_K | OP | State-transforming: `Σ × dom(Σ.M) × Endset × Endset → Σ' × A_rel^{Σ'}`, operationally K.λ specialized to value `(F, G, K)`. Function-ness over the full state space follows from K.λ's deterministic first/subsequent emission rule (R0a-Cor1 fixes the unique max element under T1). Caller-supplied home document `d ∈ dom(Σ.M)` and `K ∈ T_admissible`; the `dom(Σ.M) ≠ ∅` precondition of R0 is enforced by parameter typing |
| Observe_K | OP | Pure read: `Σ × ℘_fin(T) × ℘_fin(T) × View → ℘_fin(L_K^Σ)`, selecting `L_K^Σ` or `A_K^Σ`. Patterns range over the full tumbler space `T` (not `A^Σ`) to admit ghost-targeting queries per L9 + L4 |
| Nullify | OP | `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` for caller-supplied `d_retr ∈ dom(Σ.M)` and `a ∈ A_rel^Σ` with `|Σ.L(a)| = 3`. Single-tuple scope is *absolute* as a substrate-level guarantee from R0a; not a per-call obligation (= R5 + R0 + R0a + R6a + L12) |

## Open Questions

- What invariants must hold between `L_K` and the arrangements `Σ.M` when relational predicates depend on whether the from-set or to-set content is currently visible in some document?
- Should multi-arity links (`|Σ.L(a)| > 3`) define multiple binary projections, or be regarded directly as elements of higher-arity typed relations `L_K^{(n)} ⊆ A_rel × ℘(A)^n`?
- Under what conditions is `Nullify(b)` for `b ∈ L_R` operationally meaningful, given that R6b makes single-depth checking ignore the second-order retraction?
- What ordering, if any, must the substrate guarantee on Observe results — by emission cycle, by tuple address, or unordered as set semantics suggest?
- Must Emit be atomic with respect to concurrent Observe, and if so, what is the consistency model under which `A_K` transitions are observed?
- What guarantees does the substrate provide about the cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)` — is unbounded retraction permitted, or must some structural ratio hold?
- Should L1b's substrate-level admission `#E ≥ 2` (ASN-0043) be tightened to `#E = 2` to match Nelson's design intent at the substrate layer? R0a-Cor2 establishes `#E = 2` unconditionally within the substrate via ASN-0093's K.λ contract; the question is whether L1b itself should reflect the intent more strictly (closing the substrate-level gap at the source) or whether retaining `#E ≥ 2` in L1b is the right design point — leaving room for higher-arity or future variants while the standard-triple links of this note remain depth-2 by R0a-Cor2.
- Should the relational layer's unit-depth retraction discipline (per the Definition in Three Operations) be elevated to a substrate-level guarantee on `L_R` to-spans — e.g., by introducing a designated K-operation for retraction with a unit-depth shape constraint — or is it correctly a layer convention that callers may bypass via direct K.λ with crafted retraction spans? WP Case 2 makes the consequence of the latter explicit; the design tradeoff is whether the substrate should expose any value-shape constraint on retraction tuples.
- Can higher layers introduce new admissible types `K ∈ T_admissible` dynamically without coordination, given L9 (TypeGhostPermission), and what happens when two layers independently choose colliding type addresses?