# ASN-0086: Typed Relations on Address Sets

*Drawing the link model forward into a relational vocabulary*

ASN-0043 establishes the link as a primitive: an addressed, owned, typed connection between spans of content. ASN-0093 wraps that primitive (along with content and document allocation) in three K-operations — K.σ, K.α, K.λ — that fix the sibling-frontier emission discipline and the sub-allocator chain structure. This note layers on top of ASN-0093's K-operations, adopting a different vocabulary for the link store: where ASN-0043 speaks of *links* and *endsets*, we speak of *tuples* and *typed relations*. The two vocabularies describe one object — a standard-triple link `(F, G, Θ)` at address `a ∈ dom(Σ.L)` is a tuple in a typed relation indexed by `Θ`.

We are looking for what a relation algebra over the link store affords. The answer is that predicates compose more cleanly over typed relations than over endsets, and several substrate-level guarantees — most centrally the *active/audit distinction* between the audit trail and the operational currently-in-effect set — become easier to state and prove in this form. (Document allocation (K.σ) and content emission (K.α), the other two primitive transitions in `→`, are inherited from ASN-0093; the reduction below concerns only the link store `Σ.L`.)


## The Two Foundational Sets

**Foundation.** We work in systems satisfying ASN-0093 (and therefore ASN-0043, ASN-0036, ASN-0034). ASN-0093 owns the K-operation contract — the three primitive emissions K.σ (DocumentRegistration), K.α (ContentAllocation), K.λ (LinkAllocation) — together with the sub-allocator chain lemmas making T10a's runtime activation chain explicit, and the SubspaceConventionAxiom fixing `s_C = 1 ∧ s_L = 2` with named consequence `SC-NEQ: s_C ≠ s_L`.

**Assumption — EmptyInitialLinkStore.** This note takes the system's initial state `Σ_init` to be the *fresh-system root*, with all three stores empty: `dom(Σ_init.C) = ∅`, `dom(Σ_init.M) = ∅`, and in particular `dom(Σ_init.L) = ∅`. This is the fresh-system boot condition: Gregory's `initmagicktricks` constructs both the content (granf) and link (spanf) enfilades empty via `createenf` whenever no persistent store exists, so no link address is allocated before the first link emission.

**State transition relation.** We write `Σ → Σ'` for the substrate's *dom-extending* one-step transition relation, which we identify exactly with the union of ASN-0093's three K-operations: `→ ≡ K.σ ∪ K.α ∪ K.λ`. A K.σ-step extends `dom(Σ.M)` (registering `M'(d) = ∅` at a document-level `d`), a K.α-step extends `dom(Σ.C)`, and a K.λ-step extends `dom(Σ.L)`, each at a fresh key per its ASN-0093 contract; ASN-0093's frame conditions leave the other two components unchanged, and the substrate exposes no removal, replacement, or in-place mutation transition that touches `(dom(Σ.C), dom(Σ.M), dom(Σ.L))`.

*Arrangement modification is out of scope.* None of the three K-operations modifies any document's arrangement `M(d)` beyond K.σ's empty-initialization `M'(d) = ∅`. Hence the substrate admits no arrangement-modifying transition; persistence claims (R6c) are stated and proved against `→` alone. ASN-0093's M2 (EmptyArrangement) — `(A d ∈ dom(M) :: M(d) = ∅)` — is the invariant that results: empty initialization plus the absence of any arrangement-modifying operation keeps every arrangement empty at every reachable state.

*Categorical transition relation `↝`.* We write `↝` for the *categorical* state-transition relation: the union of `→` with every state-transition relation any higher-layer operation may admit over `(Σ.C, Σ.M, Σ.L)`. Every `→`-step is an `↝`-step; `Σ ↝ Σ'` holds iff some admissible operation in some layer carries Σ to Σ'.

**Definition — Reachability.** `Σ' is →-reachable from Σ`, written `Σ →* Σ'`, is the reflexive-transitive closure of `→`.

**Definition — Categorical reachability.** `Σ' is ↝-reachable from Σ`, written `Σ ↝* Σ'`, is the reflexive-transitive closure of the categorical relation `↝`. The `↝*`-reachable states from `Σ_init` include every `→*`-reachable state but also states produced by higher-layer operations that need not preserve the L/S/M/C invariant catalog or the ASN-0093 chain discipline.

By the K.σ/K.α/K.λ frame conditions stated above, `Σ →* Σ'` entails `dom(Σ.C) ⊆ dom(Σ'.C)`, `dom(Σ.M) ⊆ dom(Σ'.M)`, `dom(Σ.L) ⊆ dom(Σ'.L)`, with `Σ'.C|_{dom(Σ.C)} = Σ.C`, `Σ'.M|_{dom(Σ.M)} = Σ.M`, `Σ'.L|_{dom(Σ.L)} = Σ.L`. Equivalently, `Σ →* Σ'` implies `Σ' ⊒ Σ` in ASN-0043's sense; the converse need not hold.

**Definition — substrate-conforming state.** A state Σ is *substrate-conforming* iff it is reachable from `Σ_init` by transitions that each satisfy three clauses:

- (a) **invariant preservation** — preserve the full L/S/M/C invariant catalog (ASN-0036, ASN-0043, ASN-0093);
- (b) **at-most-one-key-per-home** — deposit at most one fresh link key per home: each K.λ primitive emits a single key, and a composite `↝`-step may touch several homes but contributes at most one fresh key to any single home;
- (c) **frontier-landing** — a step that adds a fresh link key at home `d` adds exactly the key `inc(ℓ_prev, 0)`, where `ℓ_prev` is the prior T1-maximum of `d`'s homed-set `{a ∈ dom(Σ.L) : home(a) = d}` (well-defined and finite by L-fin), or the key `[d.0.s_L.1]` if that homed-set is empty.

**Lemma — K-Step Conformance Preservation.** If Σ is substrate-conforming and Σ → Σ' (or Σ ↝ Σ') is a *conformance-preserving step* — one satisfying clauses (a)–(c) above — then Σ' is substrate-conforming; and by induction, every state reached from a substrate-conforming state by conformance-preserving steps is substrate-conforming. Every K-op `→`-step (K.σ, K.α, K.λ) is conformance-preserving, by its ASN-0093 contract; in particular, since `Σ_init` is substrate-conforming, every `→*`-reachable state is substrate-conforming, and the converse fails.

*Proof.* Substrate-conformance is, by *Definition — substrate-conforming state*, closure of `{Σ_init}` under conformance-preserving (`↝_c`) steps, so appending one more `↝_c`-step stays within the closure and induction lifts this to any conformance-preserving trajectory — this half is definitional. The substantive content is the K-op claim, which we discharge by clause: every K.σ/K.α/K.λ `→`-step satisfies (a) by its ASN-0093 invariant-preservation contract; (b) because each K.λ emits a single key at one home; and (c) because K.λ's first/subsequent emission rule deposits exactly `[d.0.s_L.1]` (empty homed-set) or `inc(ℓ_prev, 0)` (the prior T1-maximum), which is precisely the frontier-landing key. Since `Σ_init` is substrate-conforming, every `→*`-reachable state is substrate-conforming; the converse fails (Remark — NestedLinkWitness). ∎

**Remark — NestedLinkWitness.** A higher layer may emit `a'' = inc(a, 1)` at the same home as an existing link address `a`: the `k = 1` step appends `[1]`, preserving `zeros = 3` (L1) and giving `#E(a'') = #E(a) + 1 ≥ 2` (L1b), so the nested pair `a ≼ a''` (with `a'' ≠ a`) has both addresses L0/L1/L1a/L1b/L1c-conforming, with no S-invariant disturbed. The resulting state therefore preserves the entire state-local L/S-invariant catalog (catalogued in the next definition) yet contains a nested, non-frontier link pair: it violates the tumbler-prefix antichain that R0a establishes for substrate-conforming states (clause (c)'s frontier-landing requirement fails — its `a''` is not the frontier successor `inc(ℓ_prev, 0)`).

**Definition — state-local-conforming state.** A state Σ is *state-local-conforming* iff it preserves ASN-0043's state-local L- and S-invariant catalog (its `StateLocalInvariants` — in particular L0, L1, L1a, L1b, L1c, L3, L-fin and ASN-0036's S0–S3), but need *not* satisfy the ASN-0093 chain discipline (substrate-conformance clauses (b)–(c) above) or R0a's antichain. No reachability requirement is attached. This is strictly weaker than substrate-conforming: the containment `{→*-reachable} ⊆ {substrate-conforming} ⊆ {state-local-conforming}` holds with the rightmost inclusion strict, witnessed by the NestedLinkWitness construction above (Remark — NestedLinkWitness).

**Definition — AddressUniverse.** The substrate's address universe at state Σ is

`A^Σ = dom(Σ.C) ∪ dom(Σ.L)`

By SD (StoreDisjointness, ASN-0093) — equivalently ASN-0043 L14 (DualPrimitive) together with ASN-0093 L0 supplying global `s_C`-residency of content — `A^Σ` is the entirety of stored-entity addresses at Σ; no third category exists.

**Definition — Partition.** Define:

`A_doc^Σ = dom(Σ.C)` &nbsp; — content addresses
`A_rel^Σ = dom(Σ.L)` &nbsp; — relation-tuple addresses

We claim `A^Σ = A_doc^Σ ⊔ A_rel^Σ` (disjoint union); the disjointness is `dom(Σ.C) ∩ dom(Σ.L) = ∅`, i.e. SD (StoreDisjointness, ASN-0093).

**Definition — GhostAddresses.** The *ghost addresses* at state Σ are the tumblers outside the stored-entity universe:

`T_ghost^Σ = T \ (dom(Σ.C) ∪ dom(Σ.L))`

By L9 (TypeGhostPermission, ASN-0043), ghost addresses may appear in endset spans (including type-endset coverage) without contradiction; they reference tumbler positions that are well-formed under the addressing scheme but carry no stored entity at Σ.

*Notation.* All four sets are state-dependent — `A^Σ`, `A_doc^Σ`, `A_rel^Σ`, and `T_ghost^Σ` grow or shrink as the substrate evolves (the first three monotonically by S1 and L12a; `T_ghost^Σ` shrinks as content and link emissions populate previously-ghost addresses). Where the ambient state is unambiguous, we drop the superscript and write `A`, `A_doc`, `A_rel`, `T_ghost`.

**Definition — AdmissibleTypes.** The set of *admissible types* is

`T_admissible = {K ∈ Endset : K ≠ ∅}`

— non-empty endsets, eligible to serve as a link's type endset by L3 (NEndsetStructure, ASN-0043).

By L4 (EndsetGenerality, ASN-0043) and L9 (TypeGhostPermission, ASN-0043), `T_admissible` is unconstrained by content existence: type endsets may reference any tumbler addresses, including ghosts. We require only that type-equality is decidable by endset comparison: L8 (TypeByAddress, ASN-0043) supplies the *criterion* — same-type iff equal coverage — and Lemma CoverageEqualityDecidable (below) supplies its decidability, as a finite comparison of half-open T1-intervals. (L8 itself speaks only to the equivalence relation, not to its decidability.) Type indices in what follows range over `T_admissible`; membership in a given coverage class `[K]` is then determined per-tuple by `L_K^Σ`'s coverage-equivalence criterion (below).

For the rest of this development we restrict attention to standard-triple links — those with `|Σ.L(a)| = 3`. Higher-arity links (L3, NEndsetStructure, ASN-0043) exist in `dom(Σ.L)` but are not members of any `L_K`; they admit an analogous construction with additional slot positions, which we do not pursue here.

## Allocator Structure

ASN-0093 supplies the sub-allocator structure this note relies on: for each `d ∈ dom(Σ.M)`, ChainDiscipline and FirstEmission (ASN-0093) establish two sub-allocator chains `A_C(d)` (content) and `A_L(d)` (link), anchored respectively at `b_C(d) := [d.0.s_C]` and `b_L(d) := [d.0.s_L]`, with first emissions `[d.0.s_C.1]` and `[d.0.s_L.1]`. We use ASN-0093's names directly throughout.

*Derived chain facts.* By ChainDiscipline (ASN-0093), each `A_C(d)`, `A_L(d)` is an instance of ASN-0040's sibling stream `S(p, d)`. We use two `S(p, d)` postconditions throughout, both holding along the whole `inc(·, 0)` chain: **(UL) uniform length** — `#cₙ = #c₁` for every chain element (from `S(p, d)`'s `#cₙ = #p + d`); and **(UZ) uniform zero-count** — `zeros(cₙ) = zeros(c₁)` (from the stream form `cₙ = [p₁, …, p_{#p}, 0, …, 0, n]`, equivalently B5a SiblingZerosPreservation, ASN-0040).

**Definition — `a_emit(Σ, d)`.** For any `d ∈ dom(Σ.M)`, the *fresh emission address* `a_emit(Σ, d)` is the address K.λ deposits at home `d` in state Σ, per its first/subsequent emission rule:

`a_emit(Σ, d) = [d.0.s_L.1]` when `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅` (*first-emission* branch);
`a_emit(Σ, d) = inc(ℓ_prev, 0)` otherwise, where `ℓ_prev := max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` (*subsequent-emission* branch).

The max is the unique T1-extremum of a finite (L-fin, ASN-0043) non-empty set, by T1 (LexicographicOrder, ASN-0034) trichotomy. The outcome is determined by `(Σ, d)` alone, so `a_emit` is a function of `(Σ, d)`.


## The Typed Relation

**Definition — TypeEquivalence.** Two admissible types are *type-equivalent* iff they cover the same address set:

`K ~ K' ≡ coverage(K) = coverage(K')`

This is L8's (TypeByAddress, ASN-0043) notion of `same_type`, lifted from links to type endsets themselves. The quotient `T_admissible / ~` is the set of *coverage classes*; the equivalence class of `K` is written `[K]`.

**Lemma — CoverageEqualityDecidable.** For any two endsets `e, e' ∈ Endset`, the predicate `coverage(e) = coverage(e')` is decidable, using only T2 comparisons and TumblerAdd. *Proof.* By `Endset = 𝒫_fin(Span)` (ASN-0043), `e` and `e'` are finite, so `coverage(e)` and `coverage(e')` are finite unions of half-open T1-intervals `[s, s ⊕ ℓ) = {t : s ≤ t < s ⊕ ℓ}` (T12, SpanWellDefinedness, ASN-0034), each upper endpoint `s ⊕ ℓ` computed by TumblerAdd (ASN-0034). Let `P = {s : (s, ℓ) ∈ e ∪ e'} ∪ {s ⊕ ℓ : (s, ℓ) ∈ e ∪ e'}`, a finite endpoint set; sort it under T1 via T2 (IntrinsicComparison, ASN-0034) into the distinct values `c₁ < … < c_m`. *Base case `m = 0`:* this occurs exactly when `e = e' = ∅` (any non-empty span `(s, ℓ)` has `ℓ > 0`, so `s < s ⊕ ℓ` by TA-strict (ASN-0034), contributing two distinct endpoints and forcing `m ≥ 2`); then `coverage(e) = coverage(e') = ∅`, so the predicate holds and is decided affirmatively. Assume henceforth `m ≥ 2`. Every interval's endpoints lie in `P`, so each interval is a union of consecutive *cells* of the partition `{c₁}, (c₁, c₂), {c₂}, …, {c_m}` (points and open gaps); no endpoint falls strictly inside an open gap, so each coverage is constant — wholly in or wholly out — on every cell. An interval `[s, s ⊕ ℓ)` covers the point `c_k` iff `s ≤ c_k ∧ c_k < s ⊕ ℓ`, and covers the gap `(c_k, c_{k+1})` iff `s ≤ c_k ∧ c_{k+1} ≤ s ⊕ ℓ` — each a finite conjunction of T2 comparisons evaluated without exhibiting any interior tumbler. The membership *test* therefore never enumerates a gap's interior; but the *soundness* of reading set-equality off the gap-indicators does rest on each gap being non-empty as a set of tumblers — were some gap empty, both coverages would restrict to `∅` there regardless, yet their boolean gap-indicators could differ, falsely reporting equal coverage sets as unequal. We discharge non-emptiness: for every consecutive pair `c_k < c_{k+1}`, the zero-extension `c_k.0` witnesses `c_k < c_k.0 < c_{k+1}`. The left inequality is T1 case (ii) — `c_k` is a proper prefix of `c_k.0`. For the right inequality, `c_k < c_{k+1}` holds either by T1 case (i) — a divergence at some position `j ≤ #c_k` with `c_{k,j} < c_{k+1,j}` — which `c_k.0` inherits at the same `j` (it agrees with `c_k` on positions `1..#c_k`), giving `c_k.0 < c_{k+1}`; or by T1 case (ii) — `c_k` a proper prefix of `c_{k+1}` — whence at position `#c_k + 1` either `c_{k+1}` carries a positive component, so `c_k.0 < c_{k+1}` by case (i), or a zero component, so `c_k.0 ≼ c_{k+1}` with `c_k.0 ≠ c_{k+1}` (the endpoints are distinct), giving `c_k.0 < c_{k+1}` by case (ii). Each gap thus contains at least `c_k.0`, and each point cell `{c_k}` is non-empty by construction; gap-indicator equality therefore faithfully reflects equality of the coverage sets restricted to that gap, since a coverage-set agreement together with an indicator disagreement would place the witness `c_k.0` in one coverage and not the other — a contradiction. Both coverages lie within `[c₁, c_m)` (every interval's endpoints are in `P`, so no interval reaches below `c₁` or at-or-above `c_m`), hence agree trivially on the exterior cells `(−∞, c₁)` and `[c_m, ∞)`; equality on the listed cells therefore suffices. Computing each coverage's indicator over the finitely many cells (a finite disjunction over `e`, resp. `e'`) and comparing the two indicator vectors decides `coverage(e) = coverage(e')`. ∎

**Definition — TypedRelation.** For each `K ∈ T_admissible` and state Σ, the *typed relation of type K at Σ* is

`L_K^Σ = {(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a).e₁ = F ∧ Σ.L(a).e₂ = G ∧ coverage(Σ.L(a).e₃) = coverage(K)}`

Each member is a triple of (tuple-address, from-endset, to-endset). The pair `(F, G)` is the *relational content* of the tuple; `a` is the *tuple address*. The substrate's standard-triple link store at state Σ is therefore the disjoint union over coverage classes:

`L^Σ = ⨆_{[K] ∈ T_admissible / ~} L_K^Σ`

The union is disjoint in place: `Σ.L` is a partial function `T ⇀ Link` (ASN-0043, Definition of LinkStore), so a tuple address `a` carries a single value `Σ.L(a)`, hence a single slot-3 endset `Σ.L(a).e₃` and a single coverage class `[Σ.L(a).e₃]`; thus `a` indexes exactly one slice `L_K^Σ` and no tuple lies in two slices. Where ambient state is clear we drop the superscript and write `L_K`, `L`. Coverage-equivalence at the type slot aligns `L_K` with L8's same-type relation, which also projects through coverage.

*Notation — subscript read modulo `~`.* Since the slot-3 criterion tests `coverage(Σ.L(a).e₃) = coverage(K)`, any `K ~ K'` induces `L_K^Σ = L_{K'}^Σ`; the subscript is a *coverage-class* index, depending only on `[K]`.

**Definition — TupleAddress.** Define `addr : L^Σ → A_rel^Σ` by `addr(a, F, G) = a`. The address component `a` is what distinguishes this structure from the set-theoretic typed relation (a subset of `℘(A) × ℘(A)`, distinguished only by content): each tuple carries an address that participates in the relation's identity, which the content-only projection `(a, F, G) ↦ (coverage(F), coverage(G))` discards.


## Tuple Identity (R0, R1, R2)

Each tuple emission allocates a fresh address (R0), the address-to-pair binding is a function (R1), and the binding is permanent (R2).

**Sub-lemma — FreshLinkKeyDisjointness (L14/L14a fresh-key discharge).** Let `Σ → Σ'` extend the link store by one fresh key `a` with `E(a)₁ = s_L`, leaving `Σ'.C = Σ.C` and `Σ'.M = Σ.M` (the value-preserving single-key form of every K.λ-step). If L14 (DualPrimitive) and L14a (NonTranscludability) hold at Σ, they hold at Σ'. *Proof.* The only new key to check is `a`. By ASN-0093 L0 (SubspacePartition) and SC-NEQ, `E(a)₁ = s_L ≠ s_C` while every content address has `E(·)₁ = s_C`, so `a ∉ dom(Σ.C)|_{s_C}` — discharging L14 at the new key (SD, StoreDisjointness, ASN-0093, delivers `dom(Σ'.L) ∩ dom(Σ'.C) = ∅` directly). For L14a, by S3 (ReferentialIntegrity, ASN-0036) `ran(Σ.M) ⊆ dom(Σ.C)`, so every arrangement image carries `E(·)₁ = s_C`, and the same exclusion gives `a ∉ ran(Σ.M) = ran(Σ'.M)`. ∎

**L-ContiguousPrefix — ContiguousPrefix.** At every substrate-conforming state Σ, for every `d ∈ dom(Σ.M)` there exists `J_d^Σ ∈ ℤ_{≥-1}` such that the homed-set is a contiguous initial segment of `A_L(d)`'s chain enumeration, and (when non-empty) admits a unique T1-maximum at chain index `J_d^Σ`:

`(A Σ : Σ substrate-conforming :: (A d ∈ dom(Σ.M) :: (E J_d^Σ ∈ ℤ_{≥-1} :: {a ∈ dom(Σ.L) : home(a) = d} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ})))`

(with `J_d^Σ = -1` denoting the empty set when no link is homed at `d`).

*Unique T1-maximum on non-empty homed-sets.* When `J_d^Σ ≥ 0` (equivalently, the homed-set is non-empty), `max{a ∈ dom(Σ.L) : home(a) = d}` under T1 (LexicographicOrder, ASN-0034) is well-defined and equals `inc^{J_d^Σ}(d.0.s_L.1, 0)`, the chain element at chain index `J_d^Σ`. *Derivation:* ChainEnumerationInjectivity (ASN-0093) is stated in the strict-order form `(A m, n ≥ 1 : m < n : t_m < t_n)`, which forces the contiguous chain prefix `{t_1, …, t_{n_d}}` to admit `t_{n_d}` as its unique maximum; under the index re-translation, `t_{n_d} = inc^{J_d^Σ}(d.0.s_L.1, 0)`.

*Proof.*

*Reachable case (= ChainMembershipForOrigin).* For every `→*`-reachable Σ, the statement is exactly ChainMembershipForOrigin (ASN-0093) in its link form: `dom(Σ.L) ∩ {ℓ' : origin(ℓ') = d}` is a contiguous initial segment `{s_1, …, s_{n_d}}` of `A_L(d)`'s chain enumeration, with anchor `s_1 = [d.0.s_L.1]` (FirstEmission, ASN-0093) and sibling recurrence `s_{k+1} = inc(s_k, 0)`. Under ASN-0036, `origin(a)` and `home(a)` coincide on every `a ∈ dom(Σ.L)` because L1 + L1a's NUDE-prefix projection is exactly the `origin(·) = N(·).0.U(·).0.D(·)` projection. Hence the homed-set `{a ∈ dom(Σ.L) : home(a) = d}` is this same prefix, `{incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ}` with `J_d^Σ = n_d − 1` (and `J_d^Σ = -1` the empty homed-set).

*Extension to substrate-conforming states.* The same contiguity holds at every substrate-conforming state — including the `↝*`-reachable-but-not-`→*`-reachable states reached by conformance-preserving `↝`-steps that are not K-op `→`-steps (Definition — substrate-conforming state; this inclusion's strictness is recorded at Definition — state-local-conforming state). Write `H_d^Σ := {a ∈ dom(Σ.L) : home(a) = d}` and induct on the conformance-witnessing transition sequence `Σ_init = Σ_0, Σ_1, …, Σ_N = Σ`. *Base:* By the EmptyInitialLinkStore assumption (Foundation, above), `dom(Σ_init.L) = ∅`, so every `H_d^{Σ_init} = ∅` and contiguity holds with `J_d^{Σ_init} = -1`. *Step:* assume `H_d^{Σ_k} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J}` is a contiguous initial segment for every `d` (the IH), with `J = J_d^{Σ_k}`. Fix a home `d`. By clause (b) (at-most-one-key-per-home), the step adds at most one fresh key homed at `d`. If it adds none, `H_d^{Σ_{k+1}} = H_d^{Σ_k}` and contiguity is preserved with `J_d^{Σ_{k+1}} = J`. Otherwise clause (c) (frontier-landing) places the single fresh key at chain index `J + 1`, so `H_d^{Σ_{k+1}} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J + 1}` with `J_d^{Σ_{k+1}} = J + 1` — again a contiguous initial segment. Since `d` was arbitrary, contiguity is preserved at every home, hence at the terminal Σ. The unique T1-maximum is derived above. ∎

**L-ContiguousPrefix-Cor1 — DepthTwoLinkAddresses.** (Corollary of L-ContiguousPrefix.) At every substrate-conforming state Σ, every link address in `dom(Σ.L)` has an element field (T4b's `E` projection) of length exactly 2:

`(A Σ : Σ substrate-conforming :: (A a ∈ dom(Σ.L) :: #E(a) = 2))`

(Here `#E(a)` is the length of the element-field projection — e.g., the chain anchor `t_1 = [d.0.s_L.1]` has `E(t_1) = [s_L, 1]`, so `#E(t_1) = 2`.)

*Proof.* By L-ContiguousPrefix, every `a ∈ dom(Σ.L)` lies on the form `a = incʲ(d.0.s_L.1, 0)` for `d = home(a)` and some `j ≥ 0`. The chain anchor `t_1 = [d.0.s_L.1]` has length `#t_1 = #d + 3` and three zero positions: the two zero positions of `d` (inherited from the prefix `d`), and a third zero at position `#d + 1` (the appended field separator in `d.0.s_L`). Position `#t_1 = #d + 3` carries the non-zero subspace ordinal `1`. The element field `E(t_1)` is the suffix following the third zero (at position `#d + 1`): `E(t_1) = [s_L, 1]` at positions `#d + 2` and `#d + 3`, so `#E(t_1) = 2`. (UL) gives `#t_n = #t_1` for every `n ≥ 1`. We now establish that the zero *positions* of every `t_n` coincide with those of `t_1`, which fixes `#E(t_n) = #E(t_1) = 2` strictly.

By ChainDiscipline (ASN-0093), each `t_{n+1} = inc(t_n, 0)`. By TA5(c) (HierarchicalIncrement, ASN-0034), `inc(·, 0)` modifies *exactly one* position — `sig(t_n)`, the rightmost non-zero position — and preserves all other positions: `(t_{n+1})_i = (t_n)_i` for every `i ≠ sig(t_n)`, with `(t_{n+1})_{sig(t_n)} = (t_n)_{sig(t_n)} + 1`. By ChainElementT4Validity (ASN-0093) — applied to `A_L(d)`, which ChainDiscipline discharges as a T10a-discipline-satisfying chain — every chain element is T4-valid. By TA5-SigValid (ASN-0034), `sig(t_n) = #t_n` for every chain element. The single modified position is the terminal position `#t_n = #t_1`, which is non-zero in `t_n` (T4 conjunct iv at `t_n`) and remains non-zero in `t_{n+1}` (incrementing a non-zero ℕ-value stays non-zero: by NAT-addcompat's strict-successor inequality `n < n + 1` and NAT-order's transitivity, `(t_n)_{sig(t_n)} + 1 > (t_n)_{sig(t_n)} ≥ 1 > 0`). Therefore the set of zero positions is identical across `t_n` and `t_{n+1}`; by induction, identical across the whole chain.

T4b's element field `E(·)` is the suffix following the third zero. Since the three zero positions of every `t_n` coincide with those of `t_1`, the third zero sits at position `#d + 1` in every chain element, and the element field's length is `#E(t_n) = #t_n − (#d + 1) = (#d + 3) − (#d + 1) = 2 = #E(t_1)`. Hence `#E(a) = 2`. ∎

**R0 — TupleAddressFreshness.** For any substrate-conforming state Σ with `dom(Σ.M) ≠ ∅` and any `(F, G, K) ∈ Endset × Endset × T_admissible`, there exists a state Σ' with Σ → Σ' that emits a tuple with content (F, G) of type K at a fresh address, and the resulting post-state Σ' is itself substrate-conforming:

`(A Σ : Σ substrate-conforming ∧ dom(Σ.M) ≠ ∅ :: (A F, G ∈ Endset, K ∈ T_admissible :: (E Σ' reached by one →-step from Σ, a : a ∉ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K) ∧ Σ' substrate-conforming)))`

*Proof.* R0 is a near-direct consequence of ASN-0093's K.λ contract. Pick any `d ∈ dom(Σ.M)` (precondition `dom(Σ.M) ≠ ∅` is given). We invoke K.λ at home `d` with value `(F, G, K)` ∈ Endset × Endset × T_admissible (which satisfies K.λ's L3-discharge precondition by L3-conformance of the triple: `|·| = 3`, `F, G ∈ Endset`, `K ∈ T_admissible` non-empty).

K.λ's contract supplies the fresh address `a` directly via its first/subsequent emission rule.

In both branches, freshness against `dom(Σ.C)` is shared and immediate: once `E(a)₁ = s_L` and T4-validity of `a` are established (per branch, below), every `b ∈ dom(Σ.C)` has `E(b)₁ = s_C` (L0, ASN-0093) with `s_L ≠ s_C` (SC-NEQ, ASN-0093), and both `a` and `b` are element-level (`zeros = 3`) and T4-valid, so T7 (SubspaceDisjointness, ASN-0034) gives `a ≠ b`, hence `a ∉ dom(Σ.C)`. It remains, in each branch, to discharge freshness against `dom(Σ.L)`.

*Cross-home distinctness (shared sub-lemma).* The home projection `home(·) = N(·).0.U(·).0.D(·)` is a function of the address alone (T4b field extraction, ASN-0034); hence for any tumblers `x, y`, `home(x) ≠ home(y) ⟹ x ≠ y` (were `x = y`, the projection would force `home(x) = home(y)`). Each branch below establishes `home(a) = d` and invokes this with `home(ℓ') = d' ≠ d`:

- *First emission* (`a_emit`'s first-emission branch fires): `a = a_emit(Σ, d) = [d.0.s_L.1]`. By FirstEmission (ASN-0093), this address has `E(a)₁ = s_L`, `origin(a) = d` (hence `home(a) = d`), `#E(a) = 2`, `zeros(a) = 3`, and is T4-valid by direct inspection — discharging the shared `dom(Σ.C)` exclusion above. By ChainDiscipline + FirstEmission (ASN-0093), the link sub-allocator chain `A_L(d)` is active at every state with `d ∈ dom(Σ.M)`. *Freshness against `dom(Σ.L)`.* Suppose `ℓ' ∈ dom(Σ.L)`. If `home(ℓ') = d`, then `ℓ'` is a link homed at `d`, contradicting the first-emission predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅` (`origin` and `home` coincide on link addresses by L1 + L1a's NUDE-prefix projection). If `home(ℓ') = d' ≠ d`, then since `home(a) = d` (established above), Cross-home distinctness gives `a ≠ ℓ'`. Either way `a ≠ ℓ'`, so `a ∉ dom(Σ.L)`. Together with the shared `dom(Σ.C)` exclusion, this discharges K.λ's freshness precondition `a ∉ dom(Σ.L) ∪ dom(Σ.C)` at the K.λ-event committing `a`.
- *Subsequent emission* (`a_emit`'s subsequent-emission branch fires): `a = a_emit(Σ, d) = inc(ℓ_prev, 0)` with `ℓ_prev := max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}`. By Definition — `a_emit` (Allocator Structure), this max is well-defined. We discharge K.λ's gating precondition and freshness against `dom(Σ.L)` as follows:
  - *On-chain admissibility (K.λ's "produced by `A_L(d)`" gating precondition).* Σ is substrate-conforming, so L-ContiguousPrefix (ContiguousPrefix, established above) gives that the homed-set `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` is a contiguous initial segment `{incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ}` of `A_L(d)`'s chain enumeration, with `J_d^Σ ≥ 0` in this branch (the homed-set is non-empty). Its T1-maximum is therefore the chain element `ℓ_prev = inc^{J_d^Σ}(d.0.s_L.1, 0) ∈ A_L(d)`, and the emission `a = inc(ℓ_prev, 0) = inc^{J_d^Σ + 1}(d.0.s_L.1, 0)` is the next element of `A_L(d)` — so `a` is produced by `d`'s link sub-allocator, discharging K.λ's gating precondition and establishing that a legitimate K.λ-edge exists at this home.
  - *Well-formedness of `a`.* `ℓ_prev ∈ dom(Σ.L)` is T4-valid: L1c (LinkAllocatorConformance, ASN-0043) holds at Σ (a state-local invariant); hence `ℓ_prev` is the terminus of a T10a-conforming allocation chain and T10a.4 (ASN-0034) gives `T4-valid(ℓ_prev)`. By TA5-SigValid (ASN-0034), `sig(ℓ_prev) = #ℓ_prev`, so `inc(ℓ_prev, 0)` (TA5(c), ASN-0034) advances only the terminal component: `#a = #ℓ_prev` and `zeros(a) = zeros(ℓ_prev) = 3`, with `a` agreeing with `ℓ_prev` on positions `1..#ℓ_prev − 1`. Hence `origin(a) = origin(ℓ_prev) = d`, `E(a)₁ = E(ℓ_prev)₁ = s_L`, and `a` is itself T4-valid (TA5a at `k = 0`, ASN-0034) — discharging the shared `dom(Σ.C)` exclusion above.
  - *Within-home freshness.* By TA5(a) (ASN-0034), `a = inc(ℓ_prev, 0) > ℓ_prev`; and `ℓ_prev ≥ ℓ'` under T1 for every `ℓ' ∈ dom(Σ.L)` with `origin(ℓ') = d`, since `ℓ_prev` is their maximum. T1 transitivity gives `a > ℓ'`, hence `a ≠ ℓ'`, for every same-home link — contiguity of the realized chain notwithstanding.
  - *Cross-home freshness.* For `ℓ' ∈ dom(Σ.L)` with `origin(ℓ') = d' ≠ d`: the *well-formedness* bullet established `home(a) = origin(a) = d`, and `home(ℓ') = origin(ℓ') = d'` by hypothesis. Since `d ≠ d'`, Cross-home distinctness gives `a ≠ ℓ'` directly — no prefix relationship between `d` and `d'` is assumed.
  Together with the shared `dom(Σ.C)` exclusion above, these discharge K.λ's freshness precondition `a ∉ dom(Σ.L) ∪ dom(Σ.C)` at the K.λ-event committing `a`.

In either branch, K.λ's effect is `Σ'.L = Σ.L ∪ {a ↦ (F, G, K)}` with `Σ'.C = Σ.C` and `Σ'.M = Σ.M` per K.λ's Frame, witnessing R0's existential conclusion.

*L-invariant preservation across the K.λ-step.* The emission above is a valid K.λ `→`-step — its on-chain gating and freshness preconditions discharged in the freshness bullets — taken from the substrate-conforming pre-state Σ. By K-Step Conformance Preservation, Σ' is therefore substrate-conforming, which discharges the full state-local L/S/M/C invariant catalog at the fresh key `a` in one stroke: the frame-fixed S/M/C-invariants, L-fin, L12/L12a, and the L14/L14a fresh-key obligation transfer as that contract's ASN-0093 results, and the address-structural L0/L1/L1a/L1b hold at `a` as state-independent predicates over the tumbler, already exhibited in the freshness bullets above.

Two facts are specific to R0's emission, which the generic contract does not specialize; we record them explicitly. First, **L1c (LinkAllocatorConformance)** — that `a` is the T4-valid terminus of a T10a-conforming allocation chain seeded at its document-level prefix `home(a) = d` — admits an explicit per-address chain in each branch, using only the per-address chain recurrence (state-independent), never store-wide contiguity:

- *Subsequent branch.* `ℓ_prev` satisfies L1c at Σ (a state-local invariant), so there is a T10a-conforming chain `d = t_0, t_1, …, t_N = ℓ_prev` with each `t_i = inc(t_{i-1}, k_i)`, `k_1 = 2`, satisfying T10a's per-step admissibility. Append one sibling step `t_{N+1} = inc(ℓ_prev, 0) = a` (`k_{N+1} = 0`). A `k = 0` step is unconditionally T10a-admissible and preserves T4 (TA5a at `k = 0`, ASN-0034), so the extended sequence is a T10a-conforming chain from `d` to `a`; hence `a` satisfies L1c, with `home(a) = d` as its seed. The argument consults only `ℓ_prev`'s *own* L1c chain — not the contiguity of the homed-set around `ℓ_prev`.
- *First branch.* `a = [d.0.s_L.1]` is the first emission of `A_L(d)`, and ASN-0093 already delivers the conforming chain and its T4-validity directly: FirstEmission (ASN-0093) constructs `a` as the anchor-chain terminus `d, inc(d, 2), inc(inc(d, 2), 0), inc(·, 1)` — the `k = 2` step seats the field-separating zero and content anchor `b_C(d) = inc(d, 2) = [d.0.s_C]`; the `k = 0` sibling step advances to the link anchor `b_L(d) = [d.0.s_L]` (`s_L = s_C + 1`); and the final `k = 1` child step yields `[d.0.s_L.1] = a` — and ChainElementT4Validity (ASN-0093) gives that every element of `A_L(d)`, hence `a`, is T4-valid. Both lemmas have as their standing precondition that `d` is a well-formed document address; M0 (DocumentTumblerWellFormed, ASN-0093) — equivalently S7d (DocumentAllocationDiscipline, ASN-0036) — supplies `zeros(d) = 2` from `d ∈ dom(Σ.M)`, which is exactly the zero-count that makes the anchoring `k = 2` step T4-preserving (`zeros(d) = 2 ≤ 2`, TA5a's tight bound for `k = 2`, ASN-0034) and propagates to `zeros(b_L(d)) = 3` (B5: `zeros(inc(d, 2)) = 2 + 1 = 3`, preserved by the intervening `inc(·, 0)`) for the final `k = 1` step (`zeros(b_L(d)) = 3 ≤ 3`, TA5a's tight bound for `k = 1`). Hence `a` satisfies L1c, with seed `d`.

In both branches the chain is reconstructed from `a` and `d` alone — its existence does not depend on which other addresses populate `dom(Σ.L)`.

Second, the **standard-triple value shape**, the obligation R0's specialization adds beyond K.λ's generic value-precondition: `Σ'.L(a) = (F, G, K)` has arity 3 with `F, G ∈ Endset` and `K ∈ T_admissible` non-empty — exactly L3 at `a`, which K.λ's `N ≥ 3 ∧ e₃ ≠ ∅` precondition discharges at `N = 3`, `e₃ = K`. The remaining `StateLocalInvariants` conjuncts L5 (EndsetSetSemantics) and L6 (SlotDistinction) hold at `a` by the emitted value's construction alone: `(F, G, K)` is a member of the `Link` type — a finite sequence of three `Endset` members — so its set/slot structure (each slot an unordered endset, slots addressable by position) is supplied by the `Link` type definition (ASN-0043), with no per-state argument required. This completes the final conjunct of R0's conclusion: Σ' is substrate-conforming. ∎

**R0a — FlatLinkDomain.** At every substrate-conforming state Σ, `dom(Σ.L)` is a tumbler-prefix antichain:

`(A Σ : Σ substrate-conforming :: (A a, a' ∈ dom(Σ.L) :: a ≼ a' ⟹ a = a'))`

*Proof.* The argument decomposes into two cases on `home(a)` vs. `home(a')`.

*Case 1 — Cross-home (`home(a) ≠ home(a')`).* Let `d = home(a)` and `d' = home(a')` with `d ≠ d'`.

Suppose, toward contradiction, that `a ≼ a'`. Then `a' = a · w` for some suffix `w` (the digits appended to `a` to obtain `a'`). Zero counts add along concatenation: `zeros(a') = zeros(a) + zeros(w)`. By L1 (LinkElementLevel, ASN-0043), `zeros(a) = zeros(a') = 3`, so `zeros(w) = 0` — `w` contains no zero positions. By L1a (LinkScopedAllocation, ASN-0043), `home(·) = N(·).0.U(·).0.D(·)` — the prefix of the link extending through the document-field `D(·)` and ending *just before* the third zero. Since `a ≼ a'`, the positions `1..#a` of `a'` agree pointwise with all of `a`; the remaining positions `#a + 1 .. #a'` of `a'` are `w`, which contains no zeros. Therefore every zero of `a'` sits at a position `≤ #a`, and the three zeros of `a'` are *exactly* the three zeros of `a`, at the same positions. In particular, `a'`'s third zero sits at the position of `a`'s third zero — call this position `p₃`, with `p₃ ≤ #a`. The `home` prefix has length `p₃ − 1` (the positions up to and including `D(·)`, which immediately precedes the third zero). Since `p₃ − 1 < p₃ ≤ #a`, the prefix of `a'` of length `p₃ − 1` agrees pointwise with the prefix of `a` of length `p₃ − 1` (by `a ≼ a'` applied at positions `1..#a`); equivalently, `N(a') = N(a)`, `U(a') = U(a)`, and `D(a') = D(a)` — the three NUDE field-components delimited by `a'`'s first three zeros coincide with those of `a` position-by-position. Therefore `home(a') = N(a').0.U(a').0.D(a') = N(a).0.U(a).0.D(a) = home(a) = d`, contradicting `d' ≠ d`. Hence `¬(a ≼ a')`.

With `¬(a ≼ a')`, the R0a implication `a ≼ a' ⟹ a = a'` holds vacuously in this case.

*Case 2 — Same-home (`home(a) = home(a') = d`).* By L-ContiguousPrefix (ContiguousPrefix, established above), the set `{a'' ∈ dom(Σ.L) : origin(a'') = d}` is a contiguous initial segment of `A_L(d)`'s chain enumeration `(t_1, t_2, t_3, …)` with `t_1 = [d.0.s_L.1]` and `t_{n+1} = inc(t_n, 0)`. Hence both `a` and `a'` are chain elements: `a = t_i` and `a' = t_j` for some `i, j ≥ 1`. By (UL), `#a = #t_i = #t_1 = #a'` — all chain elements have equal length. If `a ≼ a'`, then by the prefix definition (positions `1..#a` of `a'` agree with `a`) combined with `#a = #a'`, `a` and `a'` coincide pointwise, so `a = a'` by T3 (CanonicalRepresentation, ASN-0034).

Combining Cases 1 and 2, `a ≼ a' ⟹ a = a'` at every substrate-conforming Σ. ∎

**R1 — AddressInjectivity.** The map `addr : L → A_rel` is an injection:

`(A (a, F, G), (a', F', G') ∈ L : a = a' :: F = F' ∧ G = G')`

*Proof.* `Σ.L` is a partial function `T ⇀ Link` (ASN-0043, Definition of LinkStore). Function-ness gives uniqueness of value: if `a = a'`, then `Σ.L(a) = Σ.L(a')`, and that single value determines the from-endset `F` and to-endset `G` stored at `a`. Therefore `F = F'` and `G = G'`. (Slice well-definedness — that `a` indexes exactly one coverage-class slice — was discharged in place at the *Definition — TypedRelation* union above.) ∎

**R2 — TupleAddressPermanence** is L12 (LinkImmutability, ASN-0043) in tuple vocabulary: an allocated tuple address resolves permanently to the same relational content.

*Consequence.* *Distinct emissions are distinguishable even when content matches.* Two agents independently filing tuples with identical `(F, G)` under identical `K` produce distinct addresses (R0 produces a fresh address regardless of value). By L11b (NonInjectivity, ASN-0043), value-level coincidence is permitted; by R1, address-level identity nevertheless distinguishes them. The substrate does not silently merge them.


## Append-Only Slices (R3)

**R3 — TypedSliceMonotonicity.** Each typed relation grows monotonically:

`(A Σ → Σ', K ∈ T_admissible :: L_K^Σ ⊆ L_K^{Σ'})`

where `L_K^Σ` denotes the typed relation evaluated at state `Σ`.

*Proof.* Let `(a, F, G) ∈ L_K^Σ`. By Definition of `L_K^Σ` (membership at the type slot is by coverage-equivalence, not by literal endset value), `a ∈ dom(Σ.L)` with `Σ.L(a) = (F, G, K'')` for some `K'' ∈ T_admissible` satisfying `coverage(K'') = coverage(K)`. By L12a (LinkStoreMonotonicity, ASN-0043), `dom(Σ.L) ⊆ dom(Σ'.L)`; by R2, `Σ'.L(a) = (F, G, K'')` — the literal value stored at `a` is preserved exactly. The membership test for `L_K^{Σ'}` is `coverage(Σ'.L(a).e₃) = coverage(K)`, i.e., `coverage(K'') = coverage(K)`, which holds by the choice of `K''`. Therefore `(a, F, G) ∈ L_K^{Σ'}`. ∎


## Subspace Disjointness (R4)

**R4 — TupleAddressDisjointness** is SD (StoreDisjointness, ASN-0093: `dom(Σ.C) ∩ dom(Σ.L) = ∅`) under the partition aliases `A_doc^Σ = dom(Σ.C)`, `A_rel^Σ = dom(Σ.L)`, giving `A_doc^Σ ∩ A_rel^Σ = ∅`.


## Self-Reference (R5)

**R5 — TupleSelfTargeting.** A tuple's from-set or to-set may reference tuple addresses. Specifically, for any substrate-conforming state Σ and any `a ∈ A_rel^Σ`, the unit-depth span `(a, δ(1, #a))` is well-formed and may appear in the from-set or to-set of an emitted tuple, with `a` in its coverage.

*Proof.* Fix any `a ∈ A_rel^Σ` at any substrate-conforming state Σ. By L1a (LinkScopedAllocation, ASN-0043) applied at `a`, `home(a) ∈ dom(Σ.M)`, so `dom(Σ.M) ≠ ∅` — discharging R0's `dom(Σ.M) ≠ ∅` precondition for the home `d` chosen below; Σ's substrate-conformance discharges R0's conformance precondition. (Equivalently, "may appear in the from-set or to-set of an emitted tuple" presupposes a state with at least one document allocated, which `a ∈ A_rel^Σ` itself supplies.)

*(Step 1 — Span well-formedness.)* By L1 (ASN-0043), `zeros(a) = 3`; by L1b (ASN-0043), `#E(a) ≥ 2`, so `#a ≥ 1`. By OrdinalDisplacement (ASN-0034), `δ(1, #a) = [0, …, 0, 1]` is a positive tumbler of length `#a` with action point `#a`. The span `(a, δ(1, #a))` satisfies T12 (SpanWellDefinedness, ASN-0034) — its action point `#a` satisfies `actionPoint(δ(1, #a)) = #a ≤ #a`. By PrefixSpanCoverage (ASN-0043), `coverage({(a, δ(1, #a))}) = {t : a ≼ t}`, which contains `a` by reflexivity of `≼`.

*(Step 2 — Endset admissibility.)* By L4(c) (EndsetGenerality, ASN-0043), endset spans may reference link-subspace addresses. By L13 (ReflexiveAddressing, ASN-0043) applied at `b = a`, the unit-depth span `(a, δ(1, #a))` is the canonical reference span for `a`. The singleton endset `G_self = {(a, δ(1, #a))}` is therefore an admissible `Endset` member at any slot of an emitted link.

*(Step 3 — Self-targeting emission via R0.)* Pick any `d ∈ dom(Σ.M)` and any `K ∈ T_admissible`. The triple `(∅, G_self, K)` is L3-conforming: arity 3, with `∅ ∈ Endset` (the empty endset) and `G_self ∈ Endset` (the singleton built in Step 2), and `K ∈ T_admissible` non-empty by assumption. Apply R0 at this L3-conforming triple and home `d`. R0's emission discharges every L-invariant except L3 on the emitter address alone — K.λ's Frame fixes `(Σ.C, Σ.M)` pointwise, and the L14/L14a fresh-key obligation is the FreshLinkKeyDisjointness sub-lemma — the only content-dependent check, L3, is met here by the conformance just verified. R0 therefore produces a fresh emitter `a' ∉ dom(Σ.L)` and conforming post-state Σ' with `Σ'.L(a') = (∅, G_self, K)`. The self-reference is recorded at the substrate level: `a ∈ coverage(Σ'.L(a').e₂)` — the to-set case.

*(Step 4 — From-set case by parallel emission.)* The from-set case is symmetric. The triple `(G_self, ∅, K)` is L3-conforming by the same checks (arity 3, `G_self ∈ Endset` by Step 2, `∅ ∈ Endset` trivially, `K ∈ T_admissible` non-empty by assumption). R0 applied at home `d` yields a fresh emitter address `a''` with conforming post-state Σ'' satisfying `Σ''.L(a'') = (G_self, ∅, K)` and `a ∈ coverage(Σ''.L(a'').e₁)` — the from-set case. ∎

*Corollary R5.1 — SelfTargetingEmission.* For any `a ∈ A_rel^Σ`, any slot position, and any caller-supplied home `d ∈ dom(Σ.M)`, R0 emits at a fresh `A_rel` address a triple carrying the unit-depth span `(a, δ(1, #a))` in the chosen slot (by Steps 2–3: the span is an admissible endset member, and R0's emission at the L3-conforming triple discharges the chosen-slot placement).

*Consequence.* The substantive consequence is that self-targeting enables retraction without mutation: a tuple in a designated relation `L_R` whose to-set contains the address of the tuple being nullified. By Corollary R5.1, the retraction triple `(∅, {(a, δ(1, #a))}, R)` is emitted at a fresh `A_rel` address homed at a caller-supplied `d_retr ∈ dom(Σ.M)`; mutation becomes Emit, and `L_K` is never modified (R3).


## The Active Subset (R6a, R6b, R6c)

**Definition — RetractionType.** Fix a designated coverage class `[R]` reserved for retraction, represented by any `R ∈ T_admissible` whose coverage selects the conventional retraction address set. The corresponding typed relation `L_R^Σ` is the *retraction relation at state Σ*. By L9 (TypeGhostPermission, ASN-0043), `R` need not refer to anything stored — its coverage is an address set, chosen by convention — and `L_R^Σ` is well-defined as a coverage-class slice regardless of whether any literal representative endset has yet been stored. By coverage-equivalence, any emission with a type endset `R'` satisfying `coverage(R') = coverage(R)` contributes to `L_R^Σ` and to `nullified(Σ)` — callers are not required to use a canonical span structure for `R`, only its canonical coverage.

**Convention — RetractionDirectionality.** For the retraction coverage class `[R]`, the to-set carries the retraction's targets — addresses whose tuples are being withdrawn from the active subset — and the from-set is reserved for attribution-bearing endset content (e.g., the retractor's own address, a self-targeting emission by Corollary R5.1) or is left empty for unattributed retractions. L7 (DirectionalFlexibility, ASN-0043) permits this layer-level naming choice.

**Definition — Nullified.** The set of *nullified* tuple addresses at state `Σ` is

`nullified(Σ) = {a ∈ A_rel^Σ : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))}`

The existential checks `coverage(G')` only — the to-set's coverage — and does not inspect `coverage(F')`, per Convention RetractionDirectionality; an `Emit_R` call whose to-span coverage misses `a` does not nullify `a`, regardless of what its from-set covers. The set-builder restriction `a ∈ A_rel^Σ` confines `nullified(Σ)` to tuple addresses: ghost, content, and document addresses in `coverage(G')` — which by R5/L9 may include link, content, document, or ghost addresses — are not collected.

**Definition — ActiveSubset.** For each `K ∈ T_admissible`, the *active subset of type K at state Σ* is

`A_K^Σ = {(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}`

`A_K^Σ` is computable from `Σ.L` alone. The slice `L_K^Σ` is selected from the finite store `Σ.L` (L-fin) by the per-address test `coverage(Σ.L(a).e₃) = coverage(K)`, decidable by Lemma CoverageEqualityDecidable; and `nullified(Σ)` is selected from the same finite domain `A_rel^Σ = dom(Σ.L)` (L-fin) by the test `(E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))`, whose per-span membership `s ≤ a < s ⊕ ℓ` is decidable by T2 (IntrinsicComparison, ASN-0034) even though a single span's `coverage(G')` may be infinite (a prefix span covers an entire subtree). `A_K^Σ` is then the finite slice `L_K^Σ` with `nullified(Σ)` excluded.

**R6a — RetractionStability.** Once a tuple's address is nullified, it stays nullified across all future state transitions:

`(A Σ → Σ', a : a ∈ nullified(Σ) :: a ∈ nullified(Σ'))`

*Proof.* `coverage(G')` depends on `G'` alone (ASN-0043, Definition of coverage — a pure function on endset values), and `G'` is preserved by R2; the stability argument turns on these two facts.

Suppose `a ∈ nullified(Σ)`. By Definition of `nullified(Σ)`, this entails `a ∈ A_rel^Σ = dom(Σ.L)`, and there exist `b ∈ dom(Σ.L)` and `(b, F', G') ∈ L_R^Σ` with `a ∈ coverage(G')`. By the coverage-equivalence membership criterion of `L_R^Σ`, the literal value stored at `b` in Σ is `Σ.L(b) = (F', G', R'')` for some `R'' ∈ T_admissible` with `coverage(R'') = coverage(R)` — the third entry need not equal `R` literally; only its coverage must. We exhibit the same witness at Σ': by L12a (LinkStoreMonotonicity, ASN-0043) applied to `a ∈ A_rel^Σ`, `a ∈ dom(Σ.L) ⊆ dom(Σ'.L) = A_rel^{Σ'}`, discharging the `a ∈ A_rel^{Σ'}` predicate required by Definition of `nullified(Σ')`. By R3 (applied to the type slice indexed by `R`), `L_R^Σ ⊆ L_R^{Σ'}`, so `(b, F', G') ∈ L_R^{Σ'}`. By R2, `b ∈ dom(Σ'.L)` with `Σ'.L(b) = (F', G', R'')` — the literal stored value is preserved exactly, so in particular `G'` is preserved. Since `coverage` is a pure function on endset values, `coverage(G')` is a single fixed set, and `a ∈ coverage(G')` is a state-independent proposition once `G'` has been fixed. Therefore `a ∈ nullified(Σ')`. ∎

**R6b — SingleDepthRetraction.** A retractor's tuple nullifies its targets through a single-pass check over the audit slice, with no regard to the retractor's own status:

`(A Σ, a, b, F', G' : a ∈ A_rel^Σ ∧ (b, F', G') ∈ L_R^Σ ∧ a ∈ coverage(G') : a ∈ nullified(Σ))`

All clauses are evaluated at the single state Σ.

*Proof.* By Definition of `nullified`, `a ∈ nullified(Σ) ⟺ a ∈ A_rel^Σ ∧ (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))`. The three hypotheses `a ∈ A_rel^Σ`, `(b, F', G') ∈ L_R^Σ`, and `a ∈ coverage(G')` discharge this biconditional's right-hand side directly, with `(b, F', G')` as the witness. The membership test consults the audit slice `L_R^Σ`, which retains `b`'s tuple regardless of `b`'s active-subset status — so the result holds even when `b` is itself nullified, making retraction-of-retraction a non-fixpoint operation: nullifying a retractor `b` does not "undo" `b`'s nullifying effect on its prior targets. ∎

**R6c — RestorationByReemission.** Once retracted, a tuple stays out of every active subset at any state reachable from Σ:

`(A Σ, K, (a, F, G) ∈ L_K^Σ : a ∈ nullified(Σ) : (A Σ' : Σ →* Σ' :: (a, F, G) ∉ A_K^{Σ'}))`

*Proof.* Induction on the `→`-chain length `n` witnessing `Σ →* Σ'`. *Base* (`n = 0`): `Σ_0 = Σ`, so `(a, F, G) ∈ L_K^{Σ_0}` and `a ∈ nullified(Σ_0)` are the precondition restated at `Σ_0`; by Definition of `A_K`, `a ∈ nullified(Σ_0)` jointly with `(a, F, G) ∈ L_K^{Σ_0}` give `(a, F, G) ∉ A_K^{Σ_0}`. *IH at `Σ_k`:* `(a, F, G) ∈ L_K^{Σ_k}` and `a ∈ nullified(Σ_k)`. *Step:* R6a gives `a ∈ nullified(Σ_{k+1})`; R3 gives `(a, F, G) ∈ L_K^{Σ_{k+1}}`. *Conclusion at `Σ_n = Σ'`:* by Definition of `A_K`, `(a, F, G) ∉ A_K^{Σ'}`. ∎

To "restore" content, emit a fresh tuple with the desired value (R0). The new tuple receives a fresh address; the retracted tuple keeps its address (R2) and stays out of `A_K` (R6a).

*Consequence — `A_K` is not monotone, though `L_K` is.* R3, lifted along `→*` by the same induction as R6c, makes the audit slice monotone (`Σ →* Σ' ⟹ L_K^Σ ⊆ L_K^{Σ'}`); the active subset is not — a retraction shrinks `A_K` while a later re-emission grows it at a fresh address (R0), so neither `⊆` nor `⊇` holds in general between `A_K^Σ` and `A_K^{Σ'}`. Worked Sketch Step 3 exhibits the witness. Predicates and observation views over `A_K` must therefore treat its evolution as non-monotone, not inherit monotonicity from `L_K`.

R6d (RetractionStabilityUnderConformingLayer) lifts R6a and R6c from `→`/`→*` to the `↝`-steps of a substrate-conforming layer; it is stated after its dependencies R7a and *Definition — substrate-conforming layer* (Three Operations).


## Three Operations

The six properties yield three operations that suffice to span all visible substrate change.

**Definition — Emit_K.** `Emit_K` is a family of state-transforming operations indexed by `K ∈ T_admissible`. K is a type-index (subscript), not a value argument; each fixed K gives a distinct operation with the same shape:

`Emit_K : Σ × dom(Σ.M) × Endset × Endset → Σ' × A_rel^{Σ'}`

Where Σ ranges over the state-local-conforming sub-space (Definition — state-local-conforming state). `Emit_K` is defined over substrate-conforming Σ (R0) and partial over the broader state-local-conforming sub-space. Over a merely state-local-conforming Σ the emission can be undefined because the chain frontier may be ill-formed: were a non-frontier nested key (Remark — NestedLinkWitness) the apparent `ℓ_prev` at home `d`, the subsequent-emission `inc(ℓ_prev, 0)` would be off-chain — a child of the nested key rather than a chain sibling — so no legitimate K.λ-edge exists at `d` and `Emit_K(Σ, d, F, G)` is undefined there. Where it is defined, it is a function (Lemma — Emit_K function-ness, below).

`Emit_K` is operationally `K.λ` of ASN-0093, restricted to the standard-triple link value `(F, G, K)`. K.λ accepts a value `(e₁, …, e_N)` with `N ≥ 3` and `e₃ ≠ ∅`; `Emit_K` specializes to `N = 3` and `e₃ = K`, so K.λ's contract carries over directly.

*Precondition.* `K ∈ T_admissible`. The R0 precondition `dom(Σ.M) ≠ ∅` is enforced by parameter typing: a `d ∈ dom(Σ.M)` argument cannot be supplied unless the document-allocation domain is non-empty.

*Effect.* Given input state Σ, caller-supplied home document `d ∈ dom(Σ.M)`, and finite endsets `F, G ∈ Endset`, `Emit_K(Σ, d, F, G)` invokes K.λ at home `d` with value `(F, G, K)`. The fresh address is `a = a_emit(Σ, d)` (Definition — `a_emit`, Allocator Structure). The returned `(Σ', a)` satisfies `a ∉ dom(Σ.L)`, `a ∈ dom(Σ'.L)`, `home(a) = d`, and `Σ'.L(a) = (F, G, K)`. By R2, this binding is permanent across all subsequent transitions.

*Frame.* `Σ'.C = Σ.C` and `Σ'.M = Σ.M` (K.λ's frame).

**Lemma — Emit_K function-ness.** `Emit_K` is a function: given `(Σ, d, F, G, K)`, the output `(Σ', a)` is uniquely determined.

*Proof.* The address component is `a = a_emit(Σ, d)`, a function of `(Σ, d)` by Definition — `a_emit` (Allocator Structure); that well-definedness, established there, holds over the operations' domain (Definition — Emit_K). The value `Σ'.L(a) = (F, G, K)` is fixed by the caller-supplied arguments, and K.λ's Frame fixes the rest of Σ'. ∎

**Definition — Observe_K.** For `K ∈ T_admissible`, a pattern `(F̂, Ĝ) ∈ ℘_fin(T) × ℘_fin(T)`, and a view selector, Observe is a pure read with signature

`Observe_K : Σ × ℘_fin(T) × ℘_fin(T) × View → ℘_fin(L_K^Σ)`

where `View ∈ {hist, oper}` selects between `L_K^Σ` (audit) and `A_K^Σ` (operational). It returns

`{(a, F, G) ∈ view : F̂ ⊆ coverage(F) ∧ Ĝ ⊆ coverage(G)}`

with `view = L_K^Σ` if `View = hist` and `view = A_K^Σ` if `View = oper`. Observe leaves Σ unchanged.

*Pattern domain — `T`, not `A^Σ`.* Patterns range over the full tumbler space `T`, not the state-dependent address universe `A^Σ = dom(Σ.C) ∪ dom(Σ.L)`, so they can express ghost-targeting queries — by L9 (TypeGhostPermission, ASN-0043) and L4 (EndsetGenerality, ASN-0043), endset spans may target ghost tumblers, so a pattern restricted to `A^Σ` could not express the canonical "does this tuple's from-endset cover ghost address `g`?" query. The match relation `F̂ ⊆ coverage(F)` (and `Ĝ ⊆ coverage(G)`) is decidable because `F̂` is finite and each per-span membership test `t ∈ coverage(F)` is decidable by T2 (IntrinsicComparison, ASN-0034).

**Definition — Nullify.** Nullify has a single *execution precondition* — **P0**: `d_retr ∈ dom(Σ.M)` (the home document must be allocated, discharging the internal `Emit_R`'s K.λ home-precondition). Whenever P0 holds, Nullify executes and produces a post-state Σ'. The two further conditions — **P1**: `a ∈ A_rel^Σ` and **PC**: Σ substrate-conforming — are *not* execution gates; they condition the single-tuple-scope postcondition R-Scope: P1 places the target in the active relation so the retraction lands on a real tuple, and PC supplies the antichain R-Scope reads off. Execution is governed by P0 alone.

Nullify is the composition

`Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`

That is, emit a tuple into the retraction relation with empty from-set and a unit-depth to-span targeting `a`, homed at the caller-supplied `d_retr ∈ dom(Σ.M)` (P0). The to-span `(a, δ(1, #a))` is T12-well-formed for *any* tumbler `a` (`#a ≥ 1` by T0, `actionPoint(δ(1, #a)) = #a ≤ #a`), so R0 at `d_retr` emits the retraction triple `(∅, {(a, δ(1, #a))}, R)`, depositing a fresh emitter address `b` with `Σ'.L(b) = (∅, {(a, δ(1, #a))}, R)`. On the P1 path (`a ∈ A_rel^Σ`) this emission is exactly the instance of Corollary R5.1 at slot 2. By PrefixSpanCoverage (ASN-0043), `coverage({(a, δ(1, #a))}) = {t : a ≼ t}`, which contains `a`; under P1, L12a (ASN-0043) gives `a ∈ A_rel^{Σ'}`, so by Definition of `nullified`, `a ∈ nullified(Σ')`, and by R6a `a` remains nullified thereafter.

**R-Scope — SingleTupleScope.** At every substrate-conforming state Σ, for any `a ∈ A_rel^Σ` and any caller-supplied `d_retr ∈ dom(Σ.M)`, the `→`-step taken by `Nullify(Σ, d_retr, a) = Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` contributes exactly `a` to the nullified set:

`{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`

where `(Σ', _) = Nullify(Σ, d_retr, a)`. The result is *arity-independent*: it holds regardless of `|Σ.L(a)|`.

*Proof.* By hypothesis Σ is substrate-conforming, and the K.λ `→`-step carries this to Σ' (K-Step Conformance Preservation), so R0a applies at each end. The to-span's coverage `{t : a ≼ t}` is in principle the entire prefix-subtree of `a` within `T`; restricted to `A_rel^Σ = dom(Σ.L)`, however, R0a's antichain at Σ gives `{a' ∈ dom(Σ.L) : a ≼ a'} = {a}` directly. The K.λ `→` step taken by `Emit_R` adds the fresh emitter address `b` produced by K.λ at `d_retr`: `b ∉ dom(Σ.L)` by K.λ's freshness postcondition; `b ≠ a` because K.λ deposits `b` at `[d_retr.0.s_L.1]` (first-emission case) or at `inc(ℓ_prev, 0)` (subsequent-emission case), neither of which can equal `a` — both are fresh against `dom(Σ.L)`, and `a ∈ dom(Σ.L)` by P1; `a ⊀ b` by R0a at Σ' applied to `dom(Σ'.L) = dom(Σ.L) ∪ {b}`. Therefore `{a' ∈ dom(Σ'.L) : a ≼ a'} = {a}` after the step, and `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`: Nullify's `→` step contributes exactly `a` to `nullified(Σ')`, never a sub-tree of `A_rel`. The argument consults only `a`'s tumbler prefix and R0a's antichain, never the arity `|Σ.L(a)|`, so the conclusion is arity-independent — it holds equally when `a` is a higher-arity address. ∎

**Definition — Unit-depth retraction discipline.** A state Σ is *unit-depth-disciplined* iff every `(b, F', G') ∈ L_R^Σ` has to-endset `G' = {(t, δ(1, #t))}` for some target `t ∈ A_rel^Σ` — equivalently, every `L_R^Σ` tuple was produced by a *P1-satisfying* `Nullify(Σ, d_retr, t)` call (one whose target satisfies P1, `t ∈ A_rel^Σ`). A *layer* satisfies the *unit-depth retraction discipline* iff every state it reaches is unit-depth-disciplined. The per-state predicate constrains both to-span shape and target membership; a layer satisfies the discipline only by confining its `R`-typed emissions to such P1-satisfying Nullify calls (the relational layer does so — Definition — relational layer).

**Definition — substrate-conforming layer.** A layer is *substrate-conforming* iff every operation it publishes over `(Σ.C, Σ.M, Σ.L)` carries substrate-conforming states to substrate-conforming states — i.e., satisfies clauses (a)–(c) of *Definition — substrate-conforming state* at every step. Consequently, by K-Step Conformance Preservation, every `↝`-reachable post-state of a substrate-conforming layer is itself a substrate-conforming state.

**R7a — NoExtraClassAffectsL.** For any state-affecting transition `Σ ↝ Σ'` issued by a substrate-conforming layer (per the Definition above) from a substrate-conforming pre-state Σ (equivalently, Σ reachable from `Σ_init` via conforming steps) with `Σ.L ≠ Σ'.L`, there exists a finite sequence `Σ = Σ_0 → Σ_1 → … → Σ_m` (`m ≥ 1`) of `→`-steps, each a K.σ-step or K.λ-step, such that `Σ_m.L = Σ'.L`, with `dom(Σ_m.M) ⊆ dom(Σ'.M)` and `dom(Σ_m.C) = dom(Σ.C) ⊆ dom(Σ'.C)`. The `Σ.L`-affecting effect decomposes into K.λ-steps, each prefixed if needed by the K.σ-step its L1a home-precondition requires; no K.α content-emission step is introduced (L1a constrains only `home(a_k) ∈ dom(·.M)`, not any content address).

*Proof.* The pre-state Σ is substrate-conforming by hypothesis. The `Σ ↝ Σ'` step in scope is issued by a substrate-conforming layer, hence conformance-preserving; by K-Step Conformance Preservation the post-state Σ' is itself substrate-conforming. By substrate-conformance, every `Σ ↝ Σ'` in scope preserves L12, L12a, L-fin, S0, and S1 at each step — the facts the decomposition consumes.

Under this conformance, every `Σ ↝ Σ'` in scope satisfies `dom(Σ.L) ⊆ dom(Σ'.L)` (L12a), `Σ'.L(a) = Σ.L(a)` for every `a ∈ dom(Σ.L)` (L12), `dom(Σ.C) ⊆ dom(Σ'.C)` (S1), and `Σ'.C(a) = Σ.C(a)` for every `a ∈ dom(Σ.C)` (S0). Therefore any `Σ ↝ Σ'` with `Σ.L ≠ Σ'.L` must extend `dom(Σ.L)` by at least one fresh address: modification of existing entries is forbidden by L12, and removal is forbidden by L12a, so the only remaining mechanism for changing `Σ.L` is a strict extension `dom(Σ'.L) ⊋ dom(Σ.L)`. Let `Δ := dom(Σ'.L) \ dom(Σ.L)`; by L-fin (LinkStoreFiniteness, ASN-0043), both `dom(Σ.L)` and `dom(Σ'.L)` are finite, so `Δ` is a finite, non-empty set of fresh addresses. Enumerate `Δ` in any order as `a_1, …, a_n` (`n ≥ 1`).

At the substrate-model interface, the State transition relation paragraph commits K.σ/K.α/K.λ as the *complete* primitive vocabulary of `→`. K.λ's admission requires `home(a_k) ∈ dom(·.M)` (L1a), which K.λ itself does not extend. K.σ's admission requires only freshness against `dom(·.M)` plus S7d's structural commitments (`T4-valid(d) ∧ zeros(d) = 2`).

We construct the replay sequence by interleaving: for each `k ∈ {1, …, n}`, set `d_k := home(a_k)` (computed from the fresh address `a_k` alone, by L1a's home-projection) and `(F_k, G_k, K_k) := Σ'.L(a_k)` (the literal value stored at `a_k` in Σ', well-defined since `a_k ∈ dom(Σ'.L)`). At each iteration `k`, if `d_k ∉ dom(Σ_{prev}.M)` for the running predecessor state `Σ_{prev}`, prefix a K.σ-step `Σ_{prev} → Σ_{prev}'` extending `dom(Σ_{prev}.M)` with `d_k` (K.σ's Frame guarantees `Σ_{prev}'.L = Σ_{prev}.L` and `Σ_{prev}'.C = Σ_{prev}.C`, so this prefix step does not advance `Σ.L` or `Σ.C`). The K.σ-step's preconditions discharge as follows: `d_k ∈ dom(Σ'.M)` (by L1a applied to `a_k` at Σ' in the original `↝`-step), so Σ' satisfies S7d at `d_k`, giving `T4-valid(d_k) ∧ zeros(d_k) = 2` — the structural commitments K.σ requires; freshness against `Σ_{prev}.M` is the case hypothesis `d_k ∉ dom(Σ_{prev}.M)`. Then K.λ admits a `→`-step `Σ_{prev}' → Σ_k` emitting `(F_k, G_k, K_k)` at `a_k`. K.λ requires (1) `a_k ∉ dom(Σ_{prev}'.L)`, (2) L0/L1/L1a/L1b at `a_k`, (3) `origin(a_k) = d_k` per K.λ's scoped-allocation precondition, and (4) the first/subsequent emission rule selects `a_k`. We discharge each:

- *(1) Freshness `a_k ∉ dom(Σ_{prev}'.L)`*: the K.σ-prefix held `Σ_{prev}'.L = Σ_{prev}.L`, with `Σ_{prev}.L = Σ.L ∪ {a_1, …, a_{k-1}}` from prior iterations and `a_k` distinct from each by Δ-enumeration and `a_k ∉ dom(Σ.L)` by Δ-membership.
- *(2) L0/L1/L1b at `a_k`*: state-independent structural properties of the tumbler `a_k` (`E(a_k)₁ = s_L`, `zeros(a_k) = 3`, `#E(a_k) ≥ 2`) — consequences of `a_k`'s membership in `A_L(d_k)` (discharge (4)) rather than separate K.λ preconditions. They hold at `a_k` in the conforming post-state Σ', and being state-independent transfer to `Σ_{prev}'` without further argument.
- *(2/3) L1a at `a_k` (origin/home discharge)*: requires `home(a_k) = origin(a_k) ∈ dom(Σ_{prev}'.M)`. By construction `d_k = home(a_k)` and the K.σ-prefix (if needed) inserted `d_k` into `dom(Σ_{prev}'.M)`; if no prefix was needed, `d_k ∈ dom(Σ_{prev}.M) ⊆ dom(Σ_{prev}'.M)` by the case hypothesis. Either way, `home(a_k) ∈ dom(Σ_{prev}'.M)`.
- *(4) First/subsequent emission rule selects `a_k`*: the address K.λ deposits at home `d_k` in state `Σ_{prev}'` is `a_emit(Σ_{prev}', d_k)` (Definition — `a_emit`, Allocator Structure). We must show `a_emit(Σ_{prev}', d_k) = a_k`. The argument has three parts:
  - *(i) Chain-order existence within each home.* Σ' is substrate-conforming (derived at the head of this proof from Σ's conformance and the layer's preservation property), so L-ContiguousPrefix (ContiguousPrefix) — which holds at every substrate-conforming state — applies at Σ': every key in `dom(Σ'.L)`, including those already present in `dom(Σ.L)`, lies at its home's sibling frontier, and for each `d_k` the homed set `{a ∈ dom(Σ'.L) : home(a) = d_k}` is `{incʲ(d_k.0.s_L.1, 0) : 0 ≤ j ≤ J_{d_k}^{Σ'}}` — a contiguous initial segment of `A_L(d_k)`'s chain enumeration. This contiguous-prefix structure pins down a canonical chain-order on the home `d_k`'s realized link addresses: each address has a unique chain index `j`, and chain indices totally order the homed set.
  - *(ii) K.λ's emission predicate at `d_k` is origin-scoped.* The first/subsequent emission predicate at home `d_k` is `{ℓ' ∈ dom(Σ_{prev}'.L) : origin(ℓ') = d_k} = ∅`, depending only on those elements of `dom(Σ_{prev}'.L)` whose origin equals `d_k`; emissions homed at other documents in earlier iterations do not perturb K.λ's outcome at `d_k`.
  - *(iii) Each home occurs once; the single occurrence at `d_k` selects `a_k`.* By clause (b) (at-most-one-key-per-home, Definition — substrate-conforming state), `Δ = dom(Σ'.L) \ dom(Σ.L)` contains at most one address per home, so no home `d_k` repeats in the Δ-enumeration. Each `d_k` therefore occurs exactly once; by the frontier-landing requirement (clause (c), Definition — substrate-conforming state) together with L-ContiguousPrefix at Σ', the single deposit at `d_k` extends `d_k`'s pre-existing chain prefix by one index and is assigned to `a_k`. (By (ii)'s origin-scoping, emissions at other homes do not perturb the outcome at `d_k`.) Whether K.λ's first- or subsequent-emission branch fires is determined by the same index: when `J_{d_k}^Σ = -1` (no link homed at `d_k` in `Σ_{prev}'`, whether because a K.σ-prefix just introduced `d_k` or because `d_k`'s pre-existing homed-set was empty) the first-emission branch deposits `[d_k.0.s_L.1] = a_k` at chain index 0; when `J_{d_k}^Σ ≥ 0` the subsequent-emission branch advances `inc(ℓ_prev, 0)` from the pre-existing T1-max `ℓ_prev = inc^{J_{d_k}^Σ}(d_k.0.s_L.1, 0)` (by ChainEnumerationInjectivity, ASN-0093) to `a_k`.

Discharges (1)–(4) cover each replay step's preconditions; each replay step is a primitive K-op (a K.σ-prefix or a K.λ-emission) and preserves the full invariant and chain-discipline catalog by its own ASN-0093 contract. The only step-specific obligations are the L14/L14a fresh-key obligation at each K.λ-emission (FreshLinkKeyDisjointness, SC-NEQ exclusion of `a_k`) and the chain-membership obligation of discharge (4).

After all `n` iterations (interleaved with at most `n` K.σ-prefixes when home documents were not already in `dom(Σ.M)`), the running `Σ_m.L = Σ.L ∪ {a_1 ↦ (F_1, G_1, K_1), …, a_n ↦ (F_n, G_n, K_n)} = Σ'.L`, and `dom(Σ_m.M) ⊆ dom(Σ'.M)` because each K.σ-prefix introduced only a `d_k ∈ dom(Σ'.M)`. The construction introduces no K.α content-emission steps: L1a's precondition on each K.λ-emission depends only on `home(a_k) ∈ dom(Σ_{prev}.M)`, not on any content address, so `dom(Σ_m.C) = dom(Σ.C)` throughout, and `dom(Σ.C) ⊆ dom(Σ'.C)` follows from S1 on the original `↝`-step. ∎

*Implementation note.* In udanax-green every link-writing operation adds exactly one fresh link key: CREATELINK is the only operation that writes links, and although it issues several spanf writes per call, all but one are endpoint *index* entries (LINKFROMSPAN/LINKTOSPAN), not new link keys — so the decomposition runs at `m = 1` for every present operation.

**R6d — RetractionStabilityUnderConformingLayer.** R6a and R6c are proved against `→` and `→*` (The Active Subset), but the substrate's operational evolution is `↝`. Both extend to the `↝`-steps of a substrate-conforming layer (Definition — substrate-conforming layer, above): for any state-affecting `Σ ↝ Σ'` issued by a substrate-conforming layer from a substrate-conforming pre-state Σ,

`(A a : a ∈ nullified(Σ) :: a ∈ nullified(Σ'))`,

and for any `(a, F, G) ∈ L_K^Σ` with `a ∈ nullified(Σ)`, `(a, F, G) ∉ A_K^{Σ'}`. No conforming higher-layer operation can un-nullify a tuple.

*Proof.* Both `nullified(·)` and each `A_K(·)`, `L_K(·)` slice are pure functions of the `.L` store (Definition — Nullified, ActiveSubset, TypedRelation), since `A_rel^Σ = dom(Σ.L)` and `L_R^Σ`, `L_K^Σ` are slices of `Σ.L`. If `Σ.L = Σ'.L` the claims hold trivially. Otherwise R7a (NoExtraClassAffectsL, above) decomposes the `Σ.L`-affecting effect into a finite `→`-chain `Σ = Σ_0 → … → Σ_m` of K.σ/K.λ-steps with `Σ_m.L = Σ'.L`. R6a applies across each `→`-step, so by transitivity `a ∈ nullified(Σ)` gives `a ∈ nullified(Σ_m) = nullified(Σ')` (the last equality by `.L`-purity and `Σ_m.L = Σ'.L`). For the R6c clause, R6c along the `→*`-chain `Σ →* Σ_m` gives `(a, F, G) ∉ A_K^{Σ_m}`, and `A_K^{Σ'} = A_K^{Σ_m}` by `.L`-purity. ∎

**Definition — relational layer.** The relational layer's operations are `{Emit_K, Observe_K, Nullify}`, with `Nullify` a definitional alias for `Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` — `Emit_K` instantiated at `K := R`, `F := ∅`, `G := {(a, δ(1, #a))}`. The layer's sole discipline commitment: `Emit_K` is invoked only at type indices `K ≁ R`, every `R`-typed emission is routed through the `Nullify` alias at a P1 target (`a ∈ A_rel^Σ`), and no composite touches `Σ.L` indirectly — so the layer satisfies the *unit-depth retraction discipline* (Definition — Unit-depth retraction discipline). `Observe_K` is state-preserving, taking no `→`-step.

*Corollary (reduction to Emit_K).* The relational layer's state-affecting operations reduce to `{Emit_K}` (with `Nullify` as alias).

*Proof.* The reduction follows directly from the layer's *Definition*, without invoking R7a: its only state-affecting operations are `Emit_K` and its alias `Nullify`, each *already* a single K.λ `→`-step specialized to a standard-triple value, while `Observe_K` takes no transition. So every `Σ.L`-affecting step the layer takes simply *is* an `Emit_K` call — at `m = 1`, with nothing to decompose. ∎


## Weakest-Precondition Analysis

The operations' postconditions admit explicit precondition analyses in two operationally-relevant cases that differ in kind: Case 1 (Nullify's single-tuple scope) is a sufficient-precondition and load-bearingness analysis, while Case 2 (Emit_K's membership of the fresh tuple in the active subset) is a genuine weakest precondition, written in the standard wp notation `wp(S, R)` — the weakest predicate over the prior state Σ that guarantees the post-state Σ' satisfies R after S executes.

*Case 1 — a sufficient precondition for Nullify(Σ, d_retr, a) establishing "single-tuple scope at Σ'".* The "single-tuple scope" postcondition is `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` (the to-span's `A_rel`-intersection at Σ' is exactly `a`, with no other link address falling within the prefix-subtree of `a`). Working backward through Nullify's definition `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`, the conjunction

`P0(Σ, d_retr) ∧ P1(Σ, a) ∧ PC(Σ)`

— where P0: `d_retr ∈ dom(Σ.M)`, P1: `a ∈ A_rel^Σ`, and PC: `Σ substrate-conforming` — is a *sufficient* precondition for the postcondition, with each conjunct load-bearing. It is **not** the weakest precondition: PC is a *global* conformance condition, while the postcondition is *local* to `a`'s prefix-subtree, so PC is strictly stronger than the postcondition requires.

*Domain of quantification.* This analysis ranges over the state-local-conforming sub-space (Definition — Emit_K); since the internal `Emit_R` is partial there and total only over the substrate-conforming sub-domain (Definition — Emit_K), the wp is read with the standard partial-operation convention — at a Σ where the operation does not execute, no Σ' is produced and the postcondition is unreachable, exactly the "dropping P0" mode below. PC is supplied at every layer-issued call by the relational layer's usage discipline — not by the operation's executable domain.

*Sufficiency:* P1 combined with L12a discharges `a ∈ A_rel^{Σ'}`. The only other requirement — that no other link address fall within `{t : a ≼ t}` at Σ' — is exactly R-Scope (SingleTupleScope): `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`. That result is conditioned on conformance at Σ and Σ'; PC supplies it at Σ, and the K.λ `→`-step carries it to Σ' (K-Step Conformance Preservation).

*Load-bearingness (each conjunct):* dropping any single conjunct admits a counterexample, so none is redundant. For P1, choose `a ∉ A_rel^Σ` distinct from the fresh emitter `a_emit(Σ, d_retr)` — such an `a` exists because `A_rel^Σ ∪ {a_emit(Σ, d_retr)}` is finite while `T` is infinite (T0(b), ASN-0034). The only new key at Σ' is `a_emit(Σ, d_retr)`, so by L12a's pointwise agreement `dom(Σ'.L) = dom(Σ.L) ∪ {a_emit(Σ, d_retr)}`; with `a ∉ dom(Σ.L) = A_rel^Σ` and `a ≠ a_emit(Σ, d_retr)`, we get `a ∉ dom(Σ'.L) = A_rel^{Σ'}`, whence `a ∉ {t : a ≼ t} ∩ A_rel^{Σ'}` and the intersection cannot equal `{a}`. (We do not assert `b ≠ a` as a generic fact: when P1 is dropped `a` is arbitrary, and nothing prevents `a = a_emit(Σ, d_retr)`; the counterexample simply selects an `a` for which they differ.) Dropping P0 admits `d_retr ∉ dom(Σ.M)`, leaving the internal `Emit_R`'s K.λ home-precondition undischarged: Nullify does not execute, no post-state Σ' is produced, and the postcondition is unreachable. Dropping PC admits the non-conforming nested link pair `a ≼ a''` (`a'' ≠ a`, both in `dom(Σ.L)`) of Remark — NestedLinkWitness: it preserves L0–L1c (so it lies in the operations' domain) yet violates R0a's antichain. The witness Σ carries this nested pair at `a`'s home `d` *together with* a distinct clean document `d_retr ∈ dom(Σ.M)`, `d_retr ≠ d`, whose link chain has a well-formed frontier — so the internal `Emit_R` at `(Σ, d_retr)` is defined and Nullify produces a Σ'. (Without such a `d_retr`, e.g. if `dom(Σ.M) = {d}`, the off-chain `inc(ℓ_prev, 0)` at `d`'s nested frontier leaves `Emit_R` undefined and no Σ' is produced — the "dropping P0" mode rather than a postcondition failure.) With the clean `d_retr` supplied, P0 ∧ P1 holds, the Nullify executes, yet `a''` persists by L12a and `{t : a ≼ t} ∩ A_rel^{Σ'} ⊇ {a, a''} ≠ {a}`, so the postcondition fails. Each conjunct is therefore load-bearing for the *conjunction's* sufficiency.

The scope condition P2 (`|Σ.L(a)| = 3`) is consequently absent from the wp, by R-Scope's arity-independence (SingleTupleScope).

*Case 2 — wp(Emit_K(Σ, d, F, G), "(a, F, G) ∈ A_K^{Σ'}").* The Definition of `Emit_K` guarantees `(a, F, G) ∈ L_K^{Σ'}` for the fresh emission unconditionally (K.λ deposits `(F, G, K)` at the chain-deterministic address `a`, which is then a member of `L_K^{Σ'}` by coverage-equivalence membership), but is silent on `(a, F, G) ∈ A_K^{Σ'}`, which turns on whether `a ∈ nullified(Σ')`. The post-state retraction slice depends on the K-relation: `L_R^{Σ'} = L_R^Σ ∪ {(a, F, G)}` when `K ~ R`, and `L_R^{Σ'} = L_R^Σ` when `K ≁ R`. We recall `a_emit(Σ, d)` (Definition — `a_emit`, Allocator Structure): the address K.λ deposits at home `d` in Σ, well-defined as a function of `(Σ, d)` by its Definition; the address `a` that `Emit_K(Σ, d, F, G)` deposits is exactly `a_emit(Σ, d)`.

*Result.* For this note's operation set `{Emit_K, Observe_K, Nullify}`, and over the sub-space of pre-states Σ that are both substrate-conforming *and* unit-depth-disciplined (the domain restriction stated below), the weakest precondition is

`wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`   (over substrate-conforming, unit-depth-disciplined Σ)

The index membership `K ∈ T_admissible` is presupposed in naming `Emit_K` (there is no operation `Emit_∅`), not a wp conjunct: the wp's free variables are `(Σ, d, F, G)`, and the type-index K enters the body only through the genuinely call-dependent relation `K ≁ R`.

The second conjunct is a *disjunction*, and it constrains the *call* — its type index `K` and to-set `G` — not solely the pre-state. It captures exactly the self-nullification boundary. The fresh tuple `(a, F, G)` lands in the retraction slice `L_R^{Σ'}` only when `K ~ R`; once there, it nullifies its own address `a = a_emit(Σ, d)` only when its to-set covers `a`, i.e. when `a_emit(Σ, d) ∈ coverage(G)`. The fresh emission therefore self-nullifies iff `K ~ R ∧ a_emit(Σ, d) ∈ coverage(G)`, and the disjunction is precisely the negation of that conjunction.

*The disjunction is load-bearing (necessity of both branches together).* Since `a = a_emit(Σ, d)` is a deterministic, caller-computable function of `(Σ, d)`, a caller invoking `Emit_K` at a type `K ~ R` with `G = {(a_emit(Σ, d), δ(1, #a_emit(Σ, d)))}` deposits a tuple that enters `L_R^{Σ'}` with `a ∈ coverage(G)` (the unit-depth self-span covers its own root), so `a ∈ nullified(Σ')` and `(a, F, G) ∉ A_K^{Σ'}` — while `d ∈ dom(Σ.M)` holds and *both* disjuncts fail (`K ~ R` and `a_emit(Σ, d) ∈ coverage(G)`). The home-precondition thus does not suffice; the disjunction cannot be dropped. Note the self-targeting span here is itself unit-depth, so the discipline does not exclude it — only the disjunction's collapse to falsity records it. The escape branch is genuinely required for weakestness, not redundant: an `Emit_K` call with `K ~ R` but `a_emit(Σ, d) ∉ coverage(G)` — e.g. `G = ∅`, whose coverage is empty, or a to-span rooted away from `a` — deposits an `L_R^{Σ'}` tuple that does not cover `a`, so `a ∉ nullified(Σ')` and the postcondition holds. A bare `K ≁ R` would wrongly reject these pre-states; admitting them via the escape disjunct is what makes the precondition weakest rather than merely sufficient. The Nullify-as-sole-`R`-producer rule satisfies the first disjunct (`K ≁ R`) for the relational layer's own callers, collapsing the disjunction to true there; a direct K.λ caller at `K ~ R` must instead establish `a_emit(Σ, d) ∉ coverage(G)` explicitly.

*Domain restriction.* This wp is asserted only over pre-states Σ that are both (i) substrate-conforming and (ii) unit-depth-disciplined (Definition — Unit-depth retraction discipline) — in particular, this includes every Σ reached using only the relational layer's operations (the layer is substrate-conforming and commits to the discipline); this inclusion is strict per Definition — state-local-conforming state. Both restrictions are load-bearing, and the `a ∉ nullified(Σ')` step of the derivation below consumes both: (i) substrate-conformance, via R0a's antichain; (ii) the unit-depth retraction discipline. Neither restriction alone suffices, and the two failure modes are distinct. A direct K.λ caller voids both disciplines — it can craft a non-unit-depth retraction span and reach an antichain-violating state — so the result does not extend to such callers.

*Substrate-conformance alone is insufficient (discipline necessary).* The discipline is a layer commitment, not a substrate guarantee: because K.λ fixes emission *address* but not endset *shape* (the address-vs-shape gap), a direct K.λ caller can emit a crafted-span retraction that is L-invariant-conforming yet violates the unit-depth retraction discipline. Hence a substrate-conforming Σ may carry a crafted non-unit-depth retraction span emitted by a direct K.λ caller. A crafted span `(s, ℓ)` has coverage the lexicographic interval `{t : s ≤ t < s ⊕ ℓ}` (T12, SpanWellDefinedness, ASN-0034), *not* a prefix-subtree, so prefix-incomparability of the fresh `a` against `s` does not exclude `a`: a wide span rooted near `d`'s link chain can satisfy `s ≤ a < s ⊕ ℓ`, putting `a ∈ coverage(G')` and hence `a ∈ nullified(Σ')`, while `d ∈ dom(Σ.M)` holds. This is exactly the case the unit-depth discipline excludes.

*The discipline alone is insufficient (substrate-conformance necessary).* Over the broader state-local-conforming domain of Emit_K (Definition — Emit_K, which admits antichain-violating non-conforming states), the home-precondition again fails to suffice even when every retraction is unit-depth. Witness a state-local-conforming but non-substrate-conforming Σ of the kind Remark — NestedLinkWitness constructs — a proper nested pair `b' ≺ ℓ_prev` at home `d`, with `b'` the target of a pre-existing unit-depth retraction. The subsequent-branch emission `a = a_emit(Σ, d) = inc(ℓ_prev, 0)` inherits the nesting `b' ≼ a`: the `k = 0` step advances only the terminal component (TA5(c) + TA5-SigValid, ASN-0034), preserving positions `1..#ℓ_prev − 1` with `#a = #ℓ_prev`, and since `#b' < #ℓ_prev` (proper prefix, by PrefixRelation, ASN-0034) the agreement of `b'` with `ℓ_prev` on positions `1..#b'` carries to `a`. Hence `b' ≼ a`, whence `a ∈ coverage({(b', δ(1, #b'))})` (PrefixSpanCoverage, ASN-0043) and `a ∈ nullified(Σ')`; then `(a, F, G) ∉ A_K^{Σ'}` though `d ∈ dom(Σ.M)` holds. The two restrictions together exclude exactly these two failure modes.

*Derivation (both directions).* `d ∈ dom(Σ.M)` is Emit_K's home-precondition, and it is load-bearing: dropping it leaves K.λ's home-precondition undischarged, so no post-state Σ' is produced. With the home-precondition established and the index admissible (per the Result statement above), Σ' exists and `(a, F, G) ∈ L_K^{Σ'}` holds unconditionally (Definition of Emit_K), so the postcondition `(a, F, G) ∈ A_K^{Σ'}` is equivalent to `a ∉ nullified(Σ')`. It therefore suffices to show, over the restricted domain, that `a ∉ nullified(Σ')` is equivalent to the second conjunct `K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G)`.

The domain restriction supplies, via (i), substrate-conformance of Σ, so R0a's antichain holds at Σ; the K.λ `→`-step carries it to Σ' (K-Step Conformance Preservation), so R0a's antichain on `dom(Σ'.L)` is available. By unit-depth-disciplinedness of Σ (domain precondition (ii)), every *pre-existing* `L_R^Σ` tuple has a unit-depth to-span `{(b, δ(1, #b))}` with coverage `{t : b ≼ t}` for some `b ∈ A_rel^Σ`; the fresh `a = a_emit(Σ, d)` is prefix-incomparable with every such `b` by K.λ's emission rule together with R0a, so `a ∉ coverage(G')` for any pre-existing retraction `(_, _, G') ∈ L_R^Σ`. Thus no pre-existing retraction nullifies `a`, and whether `a ∈ nullified(Σ')` is decided entirely by the fresh emission. Now `L_R^{Σ'} = L_R^Σ ∪ {(a, F, G)}` when `K ~ R`, and `L_R^{Σ'} = L_R^Σ` when `K ≁ R`. The fresh tuple lies in `L_R^{Σ'}` iff `K ~ R`, and — when it does — its to-coverage contains `a` iff `a = a_emit(Σ, d) ∈ coverage(G)`. Hence `a ∈ nullified(Σ') ⟺ (K ~ R ∧ a_emit(Σ, d) ∈ coverage(G))`. Negating both sides, `a ∉ nullified(Σ') ⟺ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` — exactly the second conjunct. Both the necessary and the sufficient direction are thereby established, and with `(a, F, G) ∈ L_K^{Σ'}` unconditional, the stated formula is the weakest precondition over the restricted domain.

## Worked Sketch

We illustrate the structure of a retraction cycle in the relational vocabulary, building on the ASN-0043 worked example. Concrete tumbler values are fixed up front; the cycle proceeds in five steps: first, a first-emission step establishing the initial state `Σ_0` from a link-empty precursor `Σ_{-1}` (Step 0); then a retraction (Step 1), a restoration (Step 2), a retraction-of-the-retractor exhibiting R6b's non-fixpoint semantics (Step 3), and a self-nullifying emission exhibiting the wp Case 2 false branch (Step 4). Step 0 exercises K.λ's first-emission branch (predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅`); Steps 1, 2, 3, and 4 each exercise the subsequent-emission branch (predicate negated).

*Setup.* Fix:

- `s_L = 2` (link subspace identifier — matching ASN-0093 SubspaceConventionAxiom and the ASN-0043 worked example).
- `d = 1.0.1.0.1` — document address, `zeros(d) = 2`, length `5`, T4-valid; `d ∈ dom(Σ_{-1}.M)` (already allocated by some prior K.σ step at or before `Σ_{-1}`).
- `c₁ = 1.0.1.0.1.0.1.1`, `c₂ = 1.0.1.0.1.0.1.2` — two content addresses in `dom(Σ_{-1}.C)`, both with `subspace_I = 1 = s_C`, `zeros = 3`, depth `8`. Both result from prior K.α invocations at home `d`: `c₁` is the first emission of `A_C(d)` per FirstEmission (ASN-0093) (concretely `c₁ = [d.0.s_C.1]` with `s_C = 1`), and `c₂ = inc(c₁, 0)` is the second per the sibling recurrence — placing the example state in the substrate's K-operation vocabulary, parallel to Step 0's K.λ first-emission of `a₁` from `A_L(d)`.
- `k = 3`, `r = 4` — single-component ghost addresses for the classification type `K = {(k, δ(1, 1))}` and the retraction coverage class `[R]` with `R = {(r, δ(1, 1))}`. By construction `coverage(K) ∩ coverage(R) = ∅` (first components 3 and 4 differ; no tumbler extends both prefixes); `K` and `R` lie in distinct coverage classes. *T4-validity note.* Type-endset ghost addresses (per L9, TypeGhostPermission, ASN-0043) need not satisfy T4 — `T4-valid(·)` is required only of allocator outputs under T10a (S7d for documents, ASN-0093 L1c for links). We choose single-component tumblers here to keep the worked sketch's ghosts T4-valid by inspection, but deeper non-T4 tumblers (e.g., `3.0.0.0.1`) would also be admissible.
- `F₁ = {(c₁, δ(1, 8))}`, `G₁ = {(c₂, δ(1, 8))}` — singleton-span endsets covering `c₁` and `c₂` respectively (by PrefixSpanCoverage).
- `Σ_{-1}.L = ∅`, so `L_K^{Σ_{-1}} = ∅`, `L_R^{Σ_{-1}} = ∅`, `nullified(Σ_{-1}) = ∅`, `A_K^{Σ_{-1}} = ∅`.

*Step 0 — first-emission case: K.λ at `d` from empty homed-set, exhibiting `a₁`.* `Σ_{-1} → Σ_0` via `K.λ` (equivalently `Emit_K(Σ_{-1}, d, F₁, G₁)`) emitting `(F₁, G₁, K)` at home `d`. ASN-0093's K.λ first-emission predicate `{ℓ' ∈ dom(Σ_{-1}.L) : origin(ℓ') = d} = ∅` fires (`dom(Σ_{-1}.L) = ∅`), so K.λ deposits at `[d.0.s_L.1]`. Computing concretely: `d = 1.0.1.0.1`, so `d.0` extends `d` with a zero at position 6 to give `1.0.1.0.1.0`; `d.0.s_L = 1.0.1.0.1.0.2`; and `d.0.s_L.1 = 1.0.1.0.1.0.2.1`. So `a₁ := [d.0.s_L.1] = 1.0.1.0.1.0.2.1` (`= t_1^L(d)` by FirstEmission, ASN-0093).

K.λ's effect at this step deposits `Σ_0.L = {a₁ ↦ (F₁, G₁, K)}` with `Σ_0.M = Σ_{-1}.M` and `Σ_0.C = Σ_{-1}.C` per K.λ's Frame. Verification at `a₁`: `zeros(a₁) = 3`, `E(a₁) = [2, 1]`, `E(a₁)₁ = 2 = s_L`, `#E(a₁) = 2` (witnessing L-ContiguousPrefix-Cor1), T4-valid, `origin(a₁) = home(a₁) = 1.0.1.0.1 = d`. ✓ FirstEmissionFreshness (ASN-0093) gives `a₁ ∉ dom(Σ_{-1}.L) ∪ dom(Σ_{-1}.C)` at the K.λ-event committing `a₁`. By R0 (TupleAddressFreshness) and R1 (AddressInjectivity), `a₁` is a fresh, distinct tuple address.

After Step 0: `L_K^{Σ_0} = {(a₁, F₁, G₁)}` (witnessing R3 over the empty `L_K^{Σ_{-1}}`); `L_R^{Σ_0} = ∅`; `nullified(Σ_0) = ∅`; `A_K^{Σ_0} = L_K^{Σ_0} = {(a₁, F₁, G₁)}`. By L-ContiguousPrefix at Σ_0 with `J_d^{Σ_0} = 0`, the homed-link set at `d` is the singleton prefix `{a₁} = {inc⁰(d.0.s_L.1, 0)}` of `A_L(d)`'s chain enumeration. ✓

*Step 1: Nullify a₁.* `Σ_0 → Σ_1` via `Nullify(Σ_0, d, a₁) = Emit_R(Σ_0, d, ∅, {(a₁, δ(1, 8))})` — the retractor here happens to share `a₁`'s home document, so the caller supplies `d_retr = d`; a different caller homed at `d' ∈ dom(Σ_0.M)` with `d' ≠ d` would supply `Nullify(Σ_0, d', a₁)` instead, with identical effect on `nullified(Σ_1)`. This emission's to-set `{(a₁, δ(1, 8))}` references the link address `a₁` — witnessing *R5* (TupleSelfTargeting): the to-set of an `L_R` tuple refers to another link's address.

Emit_R invokes K.λ at home `d`. The first/subsequent emission predicate fires *subsequent* (since `{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = d} = {a₁} ≠ ∅`); `ℓ_prev := max{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = d} = a₁`; K.λ deposits at `inc(a₁, 0) = 1.0.1.0.1.0.2.2`. Set `b₁ = 1.0.1.0.1.0.2.2` — by ChainEnumerationInjectivity (ASN-0093), `b₁` is the second chain element of `A_L(d)` (the first being `a₁ = t_1^L(d)`). By T10a.2 (NonNestingSiblingPrefixes, ASN-0034), `a₁` and `b₁` are distinct siblings of `A_L(d)` and are therefore prefix-incomparable; in particular `a₁ ⊀ b₁` — witnessing *R0* (TupleAddressFreshness): `b₁ ∉ dom(Σ_0.L)` is fresh by SubsequentEmissionFreshness (ASN-0093), the subsequent-emission branch the realized prefix `{a₁}` at Σ_0 selects (matching R0's own subsequent-branch discharge).

*L-invariant verification at `b₁`.* R0 verifies each L-invariant against an arbitrary K.λ-emitted address; the concrete `b₁ = 1.0.1.0.1.0.2.2` admits the same checks by direct inspection: L0 (`E(b₁)₁ = 2 = s_L`), L1 (`zeros(b₁) = 3` by (UZ)), L1a (`origin(b₁) = home(b₁) = d`), L1b (`#E(b₁) = 2` by (UL)), L1c (the structural chain from `d` through `b_L(d)` through `a₁` to `b₁` exists by ChainDiscipline + FirstEmission, ASN-0093). ✓ The remaining state-local L-invariants (L3, L4(c), L12, L12a, L14, L14a, L-fin) discharge by R0's generic argument applied with the concrete `b₁`.

Emit the retraction: `Σ_1.L = Σ_0.L ∪ {b₁ ↦ (∅, {(a₁, δ(1, 8))}, R)}`. Now compute:

- `coverage({(a₁, δ(1, 8))})`: by PrefixSpanCoverage with `#a₁ = 8`, `= {t : a₁ ≼ t}`. Membership: `a₁ ∈ coverage` by reflexivity of `≼`; `b₁ ∉ coverage` since `a₁` and `b₁` agree on positions `1..7` (both `1.0.1.0.1.0.2`) but differ at position `8` (`1` vs `2`) at equal length — neither is a prefix of the other. ✓
- `L_K^{Σ_1} = {(a₁, F₁, G₁)}` — unchanged. Witnesses *R3* (TypedSliceMonotonicity): `L_K^{Σ_0} = {(a₁, F₁, G₁)} ⊆ L_K^{Σ_1}` since the emission targets `L_R`, not `L_K`. Also witnesses *R2* (TupleAddressPermanence): `Σ_1.L(a₁) = Σ_0.L(a₁) = (F₁, G₁, K)`. ✓
- `L_R^{Σ_1} = {(b₁, ∅, {(a₁, δ(1, 8))})}` — the only retraction tuple; no other tuple has type slot coverage-equivalent to `R` (the tuple at `a₁` has type `K` with `coverage(K) ≠ coverage(R)`). Also witnesses *R3* applied to the `R` coverage class: `L_R^{Σ_0} = ∅ ⊆ L_R^{Σ_1}`. ✓
- `nullified(Σ_1) = {a ∈ {a₁, b₁} : a ∈ coverage({(a₁, δ(1, 8))})} = {a₁}`. By Definition of `nullified`, the existential ranges over `L_R^{Σ_1}` (audit slice), so the test is whether `(b₁, ∅, {(a₁, δ(1, 8))}) ∈ L_R^{Σ_1}` directly witnesses `a₁ ∈ coverage(G')` — yes — without recursive evaluation of `b₁`'s status. This exercises the audit-slice quantification (Definition of `nullified`) on which R6b rests. ✓
- `A_K^{Σ_1} = L_K^{Σ_1} \ {(a, F, G) : a ∈ nullified(Σ_1)} = ∅`. ✓

The audit predicate `(a₁, F₁, G₁) ∈ L_K` remains true forever (witnessing *R3*); the operational predicate `(a₁, F₁, G₁) ∈ A_K` flips to false at `Σ_1`.

*Step 2: Restore by re-emission.* To restore the classification, we do *not* attempt to nullify the retraction (which by R6b would be ineffective — single-depth checking ignores it). Instead, `Σ_1 → Σ_2` via `Emit_K(d, F₁, G₁)`, re-using the same home `d` as `a₁`. K.λ at home `d` evaluates the subsequent-emission predicate: `{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = d} = {a₁, b₁} ≠ ∅`; `ℓ_prev := max{a₁, b₁} = b₁` (by T1 lexicographic order, `b₁ > a₁` since they share prefix `1.0.1.0.1.0.2` and differ at position 8 by `2 > 1`); K.λ deposits at `inc(b₁, 0) = 1.0.1.0.1.0.2.3`. Set `a₂ = 1.0.1.0.1.0.2.3` — `A_L(d)`'s third chain element. *R0* witness: `a₂ ∉ dom(Σ_1.L)` is fresh by SubsequentEmissionFreshness (ASN-0093); *R1* (AddressInjectivity) witness: the new tuple address `a₂` is distinct from both `a₁` and `b₁`, so the map `addr` remains injective. L-invariants at `a₂` discharge by R0 applied with substitutions of `a₂` for `b₁`; by L-ContiguousPrefix at Σ_2, `a₂ = inc²(d.0.s_L.1, 0)` and `a₁, b₁, a₂` are `A_L(d)`'s first three chain elements in order.

Then `Σ_2.L = Σ_1.L ∪ {a₂ ↦ (F₁, G₁, K)}` and:

- `L_K^{Σ_2} = {(a₁, F₁, G₁), (a₂, F₁, G₁)}` — two coverage-class members with identical `(F, G)` at distinct addresses. Witnesses *R3* (monotone extension `L_K^{Σ_1} ⊆ L_K^{Σ_2}`), *R1* (distinct addresses for the two tuples), and *L11b/R2 Consequence* (distinct emissions distinguishable even when content matches). ✓
- `nullified(Σ_2) = {a₁}` — unchanged. Witnesses *R6a* (RetractionStability): `a₁ ∈ nullified(Σ_1) ⟹ a₁ ∈ nullified(Σ_2)`. The only `L_R` tuple is still at `b₁`, whose `coverage(G')` contains `a₁` but not `a₂` since `a₁` and `a₂` are distinct siblings in `A_L(d)`. Deciding `a₂ ∈ nullified(Σ_2)` again requires only the single-pass audit-slice check over `L_R^{Σ_2}` (Definition of `nullified`), which finds no witnessing tuple. ✓
- `A_K^{Σ_2} = {(a₂, F₁, G₁)}` — the new tuple is active; `a₁` remains in `L_K` but excluded from `A_K` by *R6c* (RestorationByReemission: `(a₁, F₁, G₁) ∈ L_K^{Σ_2} \ A_K^{Σ_2}` for the retracted historical record, and the restoration is the fresh `(a₂, F₁, G₁) ∈ A_K^{Σ_2}` at a different address). ✓

The relational content `(F₁, G₁)` is again present in `A_K`, but at a different tuple address. Provenance and audit cleanly distinguish the two emissions: `a₁` is the historical record, `a₂` is the current assertion.

*Step 3 — Retracting the retractor exhibits R6b's non-fixpoint semantics.* `Σ_2 → Σ_3` via `Nullify(Σ_2, d, b₁) = Emit_R(Σ_2, d, ∅, {(b₁, δ(1, 8))})` — a retraction whose to-set targets the retractor `b₁` itself. Emit_R invokes K.λ at home `d`. The first/subsequent emission predicate fires *subsequent* (since `{ℓ' ∈ dom(Σ_2.L) : origin(ℓ') = d} = {a₁, b₁, a₂} ≠ ∅`); `ℓ_prev := max{a₁, b₁, a₂} = a₂` (by T1 lex order on the shared prefix `1.0.1.0.1.0.2` with last components `1 < 2 < 3`); K.λ deposits at `inc(a₂, 0) = 1.0.1.0.1.0.2.4`. Set `b₂ = 1.0.1.0.1.0.2.4` — `A_L(d)`'s fourth chain element, fresh against `dom(Σ_2.L)` by SubsequentEmissionFreshness (ASN-0093). (We use `b₂` for this retraction-of-retractor tuple — consistent with `b₁` for the original retractor — keeping `c₁`/`c₂` reserved for the Setup's content addresses.) L-invariants at `b₂` discharge by R0's generic argument with the concrete `b₂` substituted (L0: `E(b₂)₁ = 2 = s_L`; L1: `zeros(b₂) = 3` by (UZ); L1a: `home(b₂) = d`; L1b: `#E(b₂) = 2` by (UL); L1c: the structural chain extends one step further by ChainDiscipline + FirstEmission, ASN-0093).

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

*Step 4 — a self-nullifying emission verifies the wp Case 2 false branch.* The wp of Case 2 (`wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'})`) collapses to false exactly when an `Emit_K` call at a type `K ~ R` lands its own deterministic emission address in its to-coverage; the Result's load-bearingness argument asserts this abstractly, and we now instantiate it. The fresh emission address at `d` in Σ_3 is `a_emit(Σ_3, d)`: the subsequent-emission branch fires (`{ℓ' ∈ dom(Σ_3.L) : origin(ℓ') = d} = {a₁, b₁, a₂, b₂} ≠ ∅`), `ℓ_prev := max{a₁, b₁, a₂, b₂} = b₂` (shared prefix `1.0.1.0.1.0.2`, last components `1 < 2 < 3 < 4`), so `a_emit(Σ_3, d) = inc(b₂, 0) = 1.0.1.0.1.0.2.5`. Set `a₃ = 1.0.1.0.1.0.2.5` — `A_L(d)`'s fifth chain element, with `#a₃ = 8`. Because `a₃` is caller-computable from `(Σ_3, d)` *before* the emission commits, a caller can target it: `Σ_3 → Σ_4` via `Emit_R(Σ_3, d, ∅, {(a₃, δ(1, 8))})` — i.e. `Emit_K` at `K := R`, `F := ∅`, `G := {(a₃, δ(1, #a₃))}`, the to-set rooted at the call's own emission address. (This is *not* a relational-layer `Nullify`: Nullify is P1-confined to a pre-existing target `a ∈ A_rel^Σ`, whereas `a₃ ∉ dom(Σ_3.L)`. The call is admissible to a direct K.λ caller. Σ_3 lies within the wp's domain by its own pre-state properties: Σ_3 is `→*`-reachable (hence substrate-conforming), and its pre-existing retraction tuples `L_R^{Σ_3}` target live links `a₁, b₁` via unit-depth to-spans (hence unit-depth-disciplined). The new call's to-span shape is irrelevant to pre-state domain membership; we note only, separately, that the call does not itself break the discipline — its to-span `{(a₃, δ(1, #a₃))}` is likewise unit-depth — yet it drives the disjunction false.)

K.λ deposits `(∅, {(a₃, δ(1, 8))}, R)` at `a₃ = a_emit(Σ_3, d)`, so `Σ_4.L = Σ_3.L ∪ {a₃ ↦ (∅, {(a₃, δ(1, 8))}, R)}`. Compute:

- *Both disjuncts of the wp's second conjunct fail.* `K = R`, so `K ~ R` holds — the first disjunct `K ≁ R` fails. And `coverage({(a₃, δ(1, 8))})`: by PrefixSpanCoverage with `#a₃ = 8`, `= {t : a₃ ≼ t}`, which contains `a₃` by reflexivity of `≼` — so `a_emit(Σ_3, d) = a₃ ∈ coverage(G)`, and the second disjunct `a_emit(Σ_3, d) ∉ coverage(G)` fails. Meanwhile the home-precondition `d ∈ dom(Σ_3.M)` holds. ✓
- `L_R^{Σ_4} = L_R^{Σ_3} ∪ {(a₃, ∅, {(a₃, δ(1, 8))})}` — the fresh tuple is type-`R` (its slot-3 coverage equals `coverage(R)`), so it joins the very retraction slice it can witness against.
- *Self-nullification.* The fresh tuple `(a₃, ∅, {(a₃, δ(1, 8))}) ∈ L_R^{Σ_4}` has `coverage(G') ∋ a₃`, witnessing `a₃ ∈ nullified(Σ_4)` by the single-pass audit-slice check (Definition of `nullified`). The emission nullifies its own address. ✓
- `A_R^{Σ_4} = L_R^{Σ_4} \ {(a, F, G) : a ∈ nullified(Σ_4)}`: since `a₃ ∈ nullified(Σ_4)`, the fresh tuple `(a₃, ∅, {(a₃, δ(1, 8))}) ∉ A_R^{Σ_4}`. The emission is born inactive. ✓

Thus the fresh tuple lies in `L_R^{Σ_4}` (audit) but not in `A_R^{Σ_4}` (operational): for this `Emit_R` call the wp postcondition `(a, F, G) ∈ A_K^{Σ'}` *fails* though its home-precondition `d ∈ dom(Σ_3.M)` is met. This is the concrete instance of the disjunction's false branch — the home-precondition alone does not suffice — exactly as the Result's load-bearingness paragraph asserts.

*L-ContiguousPrefix/L-ContiguousPrefix-Cor1 verification at Σ_2 and Σ_3.* Both Σ_2 and Σ_3 are `→*`-reachable (each is built by a chain of `Emit_K`/K.λ `→`-steps), so L-ContiguousPrefix here is its reachable case, which coincides with ChainMembershipForOrigin (ASN-0093). The set of link addresses homed at `d` is `{a₁, b₁, a₂} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ 2}` at Σ_2 — a contiguous prefix of `A_L(d)`'s chain enumeration — so L-ContiguousPrefix holds at Σ_2 with `J_d^{Σ_2} = 2`. At Σ_3, the homed set extends contiguously to `{a₁, b₁, a₂, b₂} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ 3}`, so L-ContiguousPrefix holds at Σ_3 with `J_d^{Σ_3} = 3`. ✓ Each of `a₁ = 1.0.1.0.1.0.2.1`, `b₁ = 1.0.1.0.1.0.2.2`, `a₂ = 1.0.1.0.1.0.2.3`, `b₂ = 1.0.1.0.1.0.2.4` has element-field projection of length 2 (E = `[2, 1]`, `[2, 2]`, `[2, 3]`, `[2, 4]` respectively) by (UL), so L-ContiguousPrefix-Cor1 holds at both Σ_2 and Σ_3. ✓


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
| → | DEF | Dom-extending state transition relation `→ ≡ K.σ ∪ K.α ∪ K.λ` |
| Unit-depth retraction discipline | COMMITMENT | Layer-level convention: every `L_R^Σ` tuple has to-endset of the form `{(b, δ(1, #b))}` for some target `b ∈ A_rel^Σ` (Three Operations) |
| R0 | LEMMA | TupleAddressFreshness — over substrate-conforming Σ with `dom(Σ.M) ≠ ∅`, every emission allocates an address fresh against `dom(Σ.L)`, on-chain in `A_L(d)` (K.λ's gating precondition), in both the first- and subsequent-emission branches, and yields a substrate-conforming post-state Σ' |
| L-ContiguousPrefix | LEMMA | ContiguousPrefix — `{a ∈ dom(Σ.L) : home(a) = d} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ}` for some `J_d^Σ ∈ ℤ_{≥-1}`, with unique T1-maximum at chain index `J_d^Σ` when non-empty |
| R0a | LEMMA | FlatLinkDomain — `dom(Σ.L)` is an antichain in `≼` at every substrate-conforming state |
| L-ContiguousPrefix-Cor1 | LEMMA | DepthTwoLinkAddresses — `#E(a) = 2` strictly for every `a ∈ dom(Σ.L)` (corollary of L-ContiguousPrefix) |
| R1 | LEMMA | AddressInjectivity — `addr` is an injection (= function property of `Σ.L`) |
| R2 | ALIAS | TupleAddressPermanence — addresses persist with values intact (definitional alias of L12) |
| R3 | LEMMA | TypedSliceMonotonicity — each `L_K^Σ` is monotone (= L12a + R2) |
| R4 | ALIAS | TupleAddressDisjointness — `A_doc^Σ ∩ A_rel^Σ = ∅` (definitional alias of SD, StoreDisjointness, ASN-0093) |
| R5 | LEMMA | TupleSelfTargeting — for any `a ∈ A_rel^Σ`, the span `(a, δ(1, #a))` is admissible as an endset member (= L1 + L1b + OrdinalDisplacement + T12 + PrefixSpanCoverage + L4(c) + L13) |
| R-Scope | LEMMA | SingleTupleScope — at a substrate-conforming Σ, `Nullify(Σ, d_retr, a)`'s `→`-step gives `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`; arity-independent (= R0a antichain + K.λ freshness + P1 + L12a) |
| R6a | LEMMA | RetractionStability — once nullified, always nullified (= R3 + R2) |
| R6b | DEF-Consequence | SingleDepthRetraction — `nullified` quantifies over the audit slice `L_R^Σ`, not `A_R^Σ`, so a retractor nullifies its targets independent of its own status (retraction-of-retractor is a non-fixpoint); per R6b |
| R6c | LEMMA | RestorationByReemission — formal claim on `→*` (reflexive-transitive closure of dom-extending `→`): restoration is fresh emission, never retraction-of-retraction (= R6a + R3) |
| R6d | LEMMA | RetractionStabilityUnderConformingLayer — R6a/R6c extend to the `↝`-steps of a substrate-conforming layer; no conforming higher-layer op un-nullifies a tuple (= R7a decomposition + R6a/R6c + `.L`-purity of `nullified`/`A_K`) |
| R7a | LEMMA | NoExtraClassAffectsL — for any state-affecting `Σ ↝ Σ'` issued by a substrate-conforming layer from a substrate-conforming pre-state Σ with `Σ.L ≠ Σ'.L`, the `Σ.L`-affecting effect decomposes into K.λ-steps interleaved with K.σ-setup steps for L1a's home-precondition: `Σ = Σ_0 → Σ_1 → … → Σ_m` (`m ≥ 1`) with `Σ_m.L = Σ'.L`, `dom(Σ_m.M) ⊆ dom(Σ'.M)`, `dom(Σ_m.C) = dom(Σ.C) ⊆ dom(Σ'.C)` |
| Relational layer | COMMITMENT | Operation set `{Emit_K, Observe_K, Nullify}` + reduction corollary; see Definition — relational layer |
| Emit_K | OP | State-transforming: `Σ × dom(Σ.M) × Endset × Endset → Σ' × A_rel^{Σ'}`, operationally K.λ specialized to value `(F, G, K)`; caller-supplied home `d ∈ dom(Σ.M)` and `K ∈ T_admissible` (Three Operations) |
| Observe_K | OP | Pure read: `Σ × ℘_fin(T) × ℘_fin(T) × View → ℘_fin(L_K^Σ)`, selecting `L_K^Σ` or `A_K^Σ` (Three Operations) |
| Nullify | OP | `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`; per Definition — Nullify |

## Open Questions

- What invariants must hold between `L_K` and the arrangements `Σ.M` when relational predicates depend on whether the from-set or to-set content is currently visible in some document?
- Should multi-arity links (`|Σ.L(a)| > 3`) define multiple binary projections, or be regarded directly as elements of higher-arity typed relations `L_K^{(n)} ⊆ A_rel × ℘(A)^n`?
- Under what conditions is `Nullify(b)` for `b ∈ L_R` operationally meaningful, given that R6b makes single-depth checking ignore the second-order retraction?
- What ordering, if any, must the substrate guarantee on Observe results — by emission cycle, by tuple address, or unordered as set semantics suggest?
- Must Emit be atomic with respect to concurrent Observe, and if so, what is the consistency model under which `A_K` transitions are observed?
- What guarantees does the substrate provide about the cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)` — is unbounded retraction permitted, or must some structural ratio hold?
- Should L1b's substrate-level admission `#E ≥ 2` (ASN-0043) be tightened to `#E = 2` at the source, or does retaining `#E ≥ 2` leave needed room for higher-arity or future variants?
- Should the relational layer's unit-depth retraction discipline (Definition, Three Operations) be elevated to a substrate-level guarantee on `L_R` to-spans — e.g., by introducing a designated K-operation for retraction with a unit-depth shape constraint — or is it correctly a layer convention? The design tradeoff is whether the substrate should expose any value-shape constraint on retraction tuples.
- Can higher layers introduce new admissible types `K ∈ T_admissible` dynamically without coordination, given L9 (TypeGhostPermission), and what happens when two layers independently choose colliding type addresses?