# ASN-0134 Claim Statements

*Source: ASN-0134-substrate-consistency-and-isolation-model.md (revised 2026-06-13) — Extracted: 2026-06-14*

## Definition — ExecutionSequence

An execution `𝔼` is a single sequence of states

`𝔼 :  Σ₀ → Σ₁ → Σ₂ → ⋯`

in which each `Σ_i → Σ_{i+1}` is one atomic step `σ_i` drawn from the step vocabulary `K = {K.σ, K.α, K.λ_sh}`, i.e. `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh`. The sequence is anchored at `Σ₀ = Σ_init`. Write `idx(σ) = i` for a step's position. `Σ_i →* Σ_j` holds exactly when `i ≤ j`.

## Definition — BatchContiguity

A batch's constituent steps land at indices `i₁ < i₂ < ⋯ < i_m` in `𝔼`. The batch is **contiguous** when `{i₁,…,i_m} = {i₁, i₁+1, …, i₁+m−1}` (no foreign step interleaves); otherwise **split**.

## Definition — FrontierPopulation

For `S ∈ {s_C, s_L}` write `dom_S(Σ)` for `dom(Σ.C)` when `S = s_C` and `dom(Σ.L)` when `S = s_L`. The home's `S`-population and `S`-frontier index are:

`P_S(d, Σ) = {a ∈ dom_S(Σ) : origin(a) = d}`,  `φ_S(d, Σ) = |P_S(d, Σ)|`.

By `ChainMembershipForOrigin`, `P_S(d, Σ)` is a contiguous initial segment of the chain `A_S(d)`, so `φ_S(d, Σ)` is the count of already-emitted slots and the next emission lands at chain slot `φ_S(d, Σ)`, advancing the count by one.

## Definition — MultiReadVerdictComposition

A `p`-read verdict is realized as

`Q = g(c₁(Σ_{r₁}), …, c_p(Σ_{r_p}))`

for a combining function `g` over the `p` *bounded-access constituents* `c₁, …, c_p`, each `c_i` a single-state read taken at its own read index `r_i`, the indices non-decreasing (`r₁ ≤ ⋯ ≤ r_p`, since zero-step reads do not advance `𝔼`). The constituents are not uniformly `Observe_K`-grade: a cross-type join realizes each `c_i` as one type's active-view read `Observe_{K_i}(oper)`, but a `stale` enumeration realizes its constituents as a *single* active-view read `Observe_K(oper)` together with *one per-home frontier descent* `f_{d_i}` per distinct member home. `g` is left *arbitrary*.

## Definition — QAffectingStep

A writer step is **`Q`-affecting**, relative to a read window, when it changes the value of some constituent `c_i` whose read has not yet been taken — i.e. `c_i` evaluated just before the step differs from `c_i` just after, for some such `i`. The quantifier ranges over *every* constituent, frontier descents included: a step that advances a not-yet-read frontier `f_{d_i}` *is* `Q`-affecting even when it disturbs no active view.

---

## A0 — StepAtomicity (AX, axiom)

There is no state strictly between `Σ_i` and `Σ_{i+1}`. The states an observer can ever name are exactly `{Σ_k : k ∈ 𝔼}`.

## A1 — Realization (AX, axiom)

A *single* state-changing operation — one not issued as a batch — is realized as *exactly one* atomic step, at a unique index; distinct such operations occupy distinct indices. (A multi-step *batch* (`m ≥ 2`) — a `retract_stale` issuing one `Nullify_Binary` per stale event, a definition's content run issuing one `K.α` per atom — is *not* a single operation in this sense: it is realized as *many* steps and is **not** atomic. The *degenerate* batch sizes: an `m = 1` fire is realized as *exactly one* step, atomic and indistinguishable from a single state-changing operation; an `m = 0` fire is realized as *zero* steps, vacuously atomic.) An operation that leaves the state unchanged is realized as *zero* steps — it reads a state and returns — and this happens in four ways: a *read-only query* — an `Observe_K`, or any of ASN-0128's behavioral reads `members`, `is_K`, `targets_of`, `succs`, `chain`, `tip`, `is_in_chain`, `sources_to`, `target_of`, `targets_keyed`, `age`, `stale`, `is_filtered` (D1–D4, BH1–BH4) — the zero-step property holds uniformly; an idempotent `Emit_K` hit; the hit branch of a `Nullify_Binary`; and a *rejected* call. The zero-step count holds for *every* such read, but single-*index* read-atomicity must be argued per read, by *access count*:

- Single-type `Observe_K`-grade reads have it by type-confinement.
- BH4's `age` has it as a *home-relative*, one-access read of the single-state frontier `f_d` (a cross-type link chain, *not* `Observe_K`-grade): `age(a) = f_d^Σ − 1 − j` where `d = home(a)` is recovered in one bounded granfilade descent over the home's link subspace.
- Cross-type joins (`targets_keyed`, default-view `members`/`targets_of`) are §8 multi-reads pinned to one index only by clause 7.
- `stale(h) = {a ∈ A_K^Σ : age(a) > h}` is a §8 multi-read at *every* member-home count `N ≥ 1`, single-home included: its realization is one type-`K` active-view read (global, consulting `L_R`) *plus one granfilade frontier descent per distinct member home* — `N + 1 ≥ 2` bounded accesses whose read indices may drift.

Whether a would-be state-changing operation realizes as one step or is rejected to zero can itself depend on the state it meets, hence on the linearization.

## A2 — LinearizationPoint (AX, axiom)

A state-changing operation `op` realized as step `σ` has linearization point `lin(op) = idx(σ)`; its *entire* effect is the single transition `Σ_{lin(op)} → Σ_{lin(op)+1}`. A zero-step operation has `lin(op)` equal to the index of the state it reads, and its effect on state is the identity.

## A3 — SnapshotRead (AX, axiom)

An `Observe` realized at index `k` is a total function of the single state `Σ_k`. Its result depends on no other state.

## A4 — NoTornStep (LEMMA, lemma)

No `Observe` witnesses a partial step. For an `Observe` at index `k` and a state-changing `op` with `lin(op) = i`: if `k ≤ i` the `Observe` sees none of `op`'s effect; if `k ≥ i+1` it sees all of it. There is no third case.

*Proof.* `op`'s effect is precisely the transition `Σ_i → Σ_{i+1}` (A2). The reader's state `Σ_k` is either at-or-before `Σ_i` (`k ≤ i`, effect absent) or at-or-after `Σ_{i+1}` (`k ≥ i+1`, effect present). The excluded middle — a state strictly between `Σ_i` and `Σ_{i+1}` — does not exist (A0). ∎

## A5 — NoBatchIsolation (AX, axiom)

A multi-step batch (`m ≥ 2`) is not atomic, in two independent senses.

*(Partial visibility — always.)* For *any* batch, contiguous or split, an `Observe` at an interior index `k` with `i₁ < k ≤ i_m` (e.g. `k = i₁+1`) witnesses a strict, non-empty *prefix* of the batch's own effects: a reader may land at any index (A0, A3), and the batch's first atom is committed at `Σ_{i₁+1}` while its last is not committed until `Σ_{i_m+1}`. This needs no foreign step — it follows from `m ≥ 2` alone.

*(Foreign interleaving — when split.)* If the batch is *additionally* split, some foreign step at index `j` with `i₁ ≤ j < i_m` interleaves, so an interior `Σ_{j+1}` also carries effects *not* belonging to the batch.

Either way the batch's partial effects are observable; the substrate's all-or-nothing guarantee stops at the single step (A0). The bound `m ≥ 2` is essential, not cosmetic: an `m = 1` fire is a single step, indivisible by A0 exactly as a lone operation is, and an `m = 0` fire commits no step, so there is no interior index to land on and the partial-visibility argument has no foothold. Non-atomicity is a strictly `m ≥ 2` phenomenon.

## A6 — CanonicalState (AX, axiom)

Call a state *structurally canonical* iff it satisfies the *per-state canonicity package* of the `→_sh` stack — *every* invariant of the stack that is a predicate of a single state, each evaluated *at* that state. This package is the conjunction of:

- ASN-0093's per-state store invariants (inherited by ASN-0086): store disjointness `SD`, element-level and field-depth invariants `C1`/`C1b`/`L1`/`L1b`, allocator conformances `C1c`/`L1c`, chain-contiguity invariants `ChainMembershipForOrigin` (each home's content and link populations form a gapless initial segment of their sub-allocator chains) and its link-store form `L-ContiguousPrefix`, home-scoping invariants `C2`/`L1a` (each store address homed at an allocated document), subspace partition `L0`, link-structure invariant `L3`, document well-formedness `M0` and empty-arrangement `M2`, store-finiteness invariants `C-fin`/`L-fin`.
- ASN-0126's `P6` (ReachableConformance).
- The *registry-fixity predicate* `Σ_k.registry = R₀`, where `R₀ := Σ_init.registry`.

The stability invariants `P2`/`R2` ("`shape(K)` (resp. `idem(K)`) takes the same value at every reachable state") are *not* conjuncts of this package — each quantifies over the *set* of reachable states and asserts a value constant *across* them. They are cross-state corollaries of registry-fixity.

The transition invariants `C0`/`L12` and ASN-0093's `M1` (document-set monotonicity) are *not* in this package; they are carried by a companion *transition clause*: for every `k ≥ 1`, the step `Σ_{k-1} → Σ_k` on `𝔼` preserves `C0`, `L12`, and ASN-0093's `M1`.

*Every* state on `𝔼` is structurally canonical. Every `Σ_k` on `𝔼` is `→_sh*`-reachable: the base `Σ₀ = Σ_init` is `→_sh*`-reachable from itself, and since each `Σ_i → Σ_{i+1}` is a `→_sh` step, the prefix `Σ₀ → ⋯ → Σ_k` witnesses `Σ_init →_sh* Σ_k`. No weaker "boundary-only" class of property exists: a `→_sh` state is either fully per-state-canonical or unreachable.

## A7 — CommitBeforeAcknowledge (AX, axiom)

For the linearization point of A2 to be presentable to a concurrent client, an operation's response/return value must be produced only at or after `lin(op)`. An acknowledgment emitted before the committing step is unsound: it lets a caller act on an effect that is not yet (and may never be) in the order.

## H0 — FrontierDiscipline (LEMMA, lemma)

Along `𝔼`, for fixed `(d, S)`, `φ_S(d, ·)` is non-decreasing, increases by exactly one at each `S`-allocation to `d`, and is left unchanged by every other step.

*Proof.* An `S`-allocation to `d` adjoins one fresh address with `origin = d` and subspace `S` (ASN-0093 K.α / ASN-0128 K.λ_sh effect), so `|P_S(d, ·)|` rises by one. Any other step is either a `K.σ`, which registers a document and frames both stores (`C' = C ∧ L' = L`), leaving every `dom_S` fixed; or an allocation into a different `(d', S') ≠ (d, S)`, which adjoins one fresh address `a'` with `origin(a') = d'`.

*If `S' ≠ S`* (whether or not `d' = d`): the step writes only `dom_{S'}` and leaves `dom_S` framed, so `P_S(d, ·) ⊆ dom_S` is untouched outright.

*If `S' = S`* (which forces `d' ≠ d`): the step does add `a'` to `dom_S`, but `origin(a') = d' ≠ d` fails the `origin = d` filter, so `P_S(d, ·)` is again unchanged.

These two cases exhaust `(d', S') ≠ (d, S)`. In every case `P_S(d, ·)` is unchanged. ∎

## H1 — CrossHomeIndependence (LEMMA, lemma)

Two allocation steps into distinct `(d, S) ≠ (d', S')` *commute*: neither reads or writes state the other touches, and applying them in either order yields the same state.

*Proof.* The first reads `φ_S(d,·)` and writes one address on chain `A_S(d)`; the second reads `φ_{S'}(d',·)` and writes on `A_{S'}(d')`. We show the two chains are disjoint as address sets:

*If `d ≠ d'`:* The address the first step deposits carries `origin = d`; the second's deposit carries `origin = d'`. Since `origin` is a structural projection fixed per address — a function of the address alone — `a = a'` would force `d = origin(a) = origin(a') = d'`, contradicting `d ≠ d'`. Hence the two deposits are distinct and `A_S(d) ∩ A_{S'}(d') = ∅`, *regardless of subspace and regardless of nesting*.

*If `d = d'`* (which forces `S ≠ S'`): the sibling-subspace anchors `[d.0.s_C]` and `[d.0.s_L]` diverge at the subspace digit, so by T10 (PartitionIndependence) the chains are disjoint — `DisjointSubAllocatorChains`.

In every case the deposits are distinct and the chains disjoint. By H0 neither step changes the other's frontier population. So each step's precondition (its frontier value) and effect (its deposited key) are on state disjoint from the other's; they commute. ∎

## H2 — SameHomeConflict (LEMMA, lemma)

Two allocation steps into the *same* `(d, S)` conflict: each reads `φ_S(d,·)`, and the first to commit increments it (H0), so the two *cannot* read the same frontier value without colliding. If both read frontier `φ`, both deposit at chain slot `φ` — the *same address* — violating freshness.

*Proof.* Two emissions into `(d, S)` against a common pre-state `Σ_pre` read the same population `P_S(d, Σ_pre)`, and the emission rule is a function of that population, so they compute the same deposit address — in *either* of its two branches.

*Interior case* (`P_S(d, Σ_pre) ≠ ∅`): `SubsequentEmissionFreshness` gives `a = inc(a_prev, 0)` with `a_prev = max P_S(d, Σ_pre)`; both read the same `a_prev`, hence compute the same `a`.

*First-emission boundary* (`P_S(d, Σ_pre) = ∅`): `max P_S(d, Σ_pre) = max ∅` is undefined and the subsequent rule does not apply. Instead both emissions satisfy ASN-0093's *first-emission* predicate `{a' : origin(a') = d} = ∅` and both compute the determinate first slot `a = [d.0.S.1]` (`FirstEmission`).

In either case the two compute one address; whichever commits first deposits it, and the second's freshness precondition — `a ∉ dom_S`, discharged in the interior case by `SubsequentEmissionFreshness` and at the boundary by `FirstEmissionFreshness` — then fails. The conflict is identical at the boundary and in the interior. ∎

## H3 — RegistrationIndependence (LEMMA, lemma)

Under this section's document-address freshness hypothesis (distinct agents propose distinct fresh `d`), a `K.σ` registering `d_new` *commutes* with every `→_sh` step other than an allocation into `d_new` itself.

*(a)* Against an allocation `K.α`/`K.λ_sh` into a home `d ≠ d_new`: `K.σ` writes only `dom(M)` (adjoining `d_new`) and frames the stores (`C' = C ∧ L' = L`), while the allocation writes only `dom(C)`/`dom(L)` and frames `M` — disjoint components — and each precondition survives the other (the allocation's `d ∈ dom(M)` under `dom(M)`'s growth, `K.σ`'s `d_new ∉ dom(M)` under the allocation's frame on `M`).

*(b)* Against a `K.σ` registering `d'_new ≠ d_new`: each adjoins a distinct fresh document and frames the stores, and `d'_new ≠ d_new` preserves both freshness preconditions across the swap.

The lone *non*-commuting pair is `K.σ(d_new)` against an allocation into `d_new`, whose `d_new ∈ dom(M)` holds only *after* the registration — the register-before-allocate dependency, hence `≺`-comparable (registration first) and never transposed. Two registrations of the *same* `d_new` collide, resolved by rejecting the loser; freshness excludes them from one schedule.

*Proof.* *(a)* is a disjoint-write commutation — `K.σ` writes only `dom(M)` while the allocation writes only a store and frames `M`, so the two touch disjoint components, each precondition surviving the other. *(b)* is *not* a disjoint-write: both `K.σ` steps read `dom(M)` (the precondition `d_new ∉ dom(M)`) and write `dom(M)`. They commute instead by *distinct-element non-interference*: a membership-test-and-insert of `d_new` and one of `d'_new` do not interfere precisely because `d_new ≠ d'_new`, so each step's `dom(M)`-read verdict and inserted element are unchanged by the other's insertion. ∎

## W0 — MonotonicityStepLocal (INV, predicate)

Append-only monotonicity and value-immutability — `C0` (ContentImmutability) and `L12` (LinkImmutability), together with document-set monotonicity (ASN-0093's `M1`, ArrangementMonotonicity, `dom(M) ⊆ dom(M')`) — are model-intrinsic. Each step's effect either adjoins a fresh key — a fresh document under `K.σ`, a fresh content or link address under `K.α`/`K.λ_sh` — or frames the store; no step removes a key (`dom(M)` included) or rewrites a value. So under any interleaving of atomic steps, `dom(C)`, `dom(L)`, and `dom(M)` only grow and existing values never change. Needs A0, nothing more.

## W1 — CrossHomeUniquenessStructural (INV, predicate)

Uniqueness of addresses allocated in *distinct* homes (or distinct subspaces of one home) is model-intrinsic.

For `d ≠ d'` the two deposits carry distinct origins (`origin = d` vs `origin = d'`) and so are unequal *regardless of subspace and regardless of whether the homes nest* — the origin argument of H1, which needs no anchor incomparability and is therefore immune to the nesting homes (`d ≼ d'`) the ASN-0093 stack admits; this settles the cross-document, cross-subspace pair as well, not only the same-subspace instance `CrossDocumentDisjointness` names.

For `d = d'` (which forces distinct subspaces) the chains diverge at the subspace digit — `DisjointSubAllocatorChains`.

Either way `a ≠ a'` holds *independent of order* (H1). Needs no serialization at all.

## W2 — SameHomeUniquenessSerial (INV, predicate)

Uniqueness of two allocations into the *same* `(d, S)` is serialization-borne. By H2 it holds iff the two emissions read distinct frontier values, i.e. iff they are serialized within `(d, S)`. Without per-home ordering, two emissions collide on one address.

## W3 — ChainContiguitySerial (INV, predicate)

Dense chain contiguity — `ChainMembershipForOrigin`'s property that `P_S(d, ·)` is a gapless initial segment of `A_S(d)` — is serialization-borne in the same per-home sense as W2. Given per-home ordering, every emission lands at the unique current frontier slot (H0), so the segment stays gapless; without it, two emissions either collide (a repeated slot) or, if an implementation "fixed" collisions by skipping, leave a hole.

## W4 — RunContiguityCritical (INV, predicate)

A multi-atom content run for a definition in home `d` (a batch of `K.α` steps into `(d, s_C)`) occupies a contiguous block of `A_{s_C}(d)` iff no foreign allocation into `(d, s_C)` is interleaved between the run's first and last step. This is a *per-`(home, subspace)` critical section spanning the run* — strictly stronger than the per-step per-home serialization of W2/W3, strictly weaker than any cross-home exclusion.

*Proof.* By H0 each `s_C`-allocation to `d` lands at the then-current frontier and advances it by one. If the run's `m` steps are the only `s_C`-allocations to `d` in the index interval they span, they land at consecutive slots `φ, φ+1, …, φ+m−1`: a contiguous block. If a foreign `s_C`-allocation to `d` lands at some interior index, it consumes a frontier slot between two of the run's atoms, and the run's remaining atoms land *past* it — the run's slots are `{φ, …}` with a foreign slot embedded, no longer an interval. By H1, a foreign allocation into any *other* `(d', S')` leaves `φ_{s_C}(d, ·)` fixed and cannot break the run. ∎

## W5 — ActiveSliceStepLocal (INV, predicate)

The relationship between the audit slice `L_K` (every type-`K` tuple ever emitted) and the active subset `A_K` (`L_K` minus `nullified`) is model-intrinsic. Both are *pure functions* of the state read; an `Observe` at index `k` computes both from `Σ_k` consistently (A3). Nullification only grows `nullified` (R6a, RetractionStability), and each `Nullify` evaluates its target precondition `P-tgt` — `a ∈ A_rel^Σ ∨ a = a_emit(Σ, d_retr)` — at *its own* linearization state. `P-tgt` sorts every target into three *exhaustive* cases:

*(1) `a ∈ A_rel^Σ` — normal nullify.* The first disjunct holds; the call fires and nullifies an address already resident in the store, so no absent address is targeted.

*(2) `a ∉ A_rel^Σ ∧ a = a_emit(Σ, d_retr)` — self-emit, self-nullify.* Only the second disjunct holds; the nullify fires and deposits its R-tuple at exactly `b = a_emit(Σ, d_retr) = a`, so the tuple lands on `a` and nullifies itself (a self-nullified retraction, not a dangling one).

*(3) `a ∉ A_rel^Σ ∧ a ≠ a_emit(Σ, d_retr)` — declined.* Both disjuncts fail, so the call takes no step and deposits nothing. This rejection arm subsumes *both* the cross-home pre-target (a nullify ordered before another home's not-yet-emitted address) *and* the retractor's own not-yet-emitted non-frontier slot `a = chain_{d_retr}(j)` at `j > f`.

Across the trichotomy no retraction is ever left targeting an absent address: cases (1) and (2) deposit onto a resident address, and case (3) deposits nothing. At every state, `A_K = L_K ∖ nullified` exactly. Needs only A0.

## W6 — RegistryRaceFree (INV, predicate)

The registry is immutable across all runtime steps (`RegistryInvariance` / P1 of ASN-0126, R1 of ASN-0128: `Σ.registry = Σ_init.registry` at every reachable state). No step in `K` writes it. Registry writes are confined to the single, pre-execution construction of `Σ_init` (`R-VAL`), which is not a step of `𝔼`. Runtime registry access is pure read of an immutable structure — always consistent, never torn, by definition. The write-write race is *vacuously absent*.

## G0 — Serializability (AX, axiom)

The substrate realizes a single total order of atomic steps (`SequentialTransitionAxiom`), each operation appearing atomic at its `lin`; so every execution is *serializable* — equivalent to the serial order `𝔼`. The order is logical (a per-home arrival sequencing), carrying no global temporal coordinate that observers must agree on.

This note names this *serializability*, and pointedly *not* *sequential consistency*. SC is strictly stronger: it requires the serial order to preserve each agent's *program order* — the order in which one agent issued its own operations. This note neither models per-agent program order nor discharges any obligation to preserve one. G1 frees every pair of `≺`-incomparable cross-home steps to be reordered, and two operations a single agent issues into distinct homes are exactly such a pair, so a valid linearization may serialize them in either order. Cross-home operations of one agent therefore carry *no* program-order obligation; an agent that needs its own cross-home operations ordered must serialize them itself (A7). With program order unconstrained across homes, SC degenerates to bare serializability here.

## G-PO — PartialScheduleModel (DEF, definition)

A *schedule* over a reachable start state `Σ` is a finite set `O` of allocation steps (`K.α`, `K.λ_sh`) into homes already registered at `Σ` — no `K.σ` is scheduled *in this base model*, the register-before-allocate dependency discharged in advance; `H3` lifts the result to schedules that do register documents — equipped with a partial order `≺` — the order the implementation *forces* — such that for every `(d, S)` the `S`-allocations to `d` in `O` are pairwise `≺`-comparable (*per-home serialization*), while steps into distinct `(d, S) ≠ (d', S')` need not be. A *linearization* of `(O, ≺)` is any total order extending `≺`; run from `Σ`, each linearization is one execution `𝔼`. The total order of §1 is the special case in which `≺` is itself total.

## G1 — PerHomeSerializabilitySuffices (LEMMA, lemma)

Let `(O, ≺)` be any per-home-serialized schedule over a reachable `Σ`. Then (i) *every* linearization of `(O, ≺)` is a valid execution preserving every per-state invariant at every state and every allocation invariant in its final state; and (ii) all linearizations are *confluent* — they reach one and the same final state, with the same address at every chain slot of every home. The cross-home order is free to vary, and no invariant and no committed address depends on how a linearization resolves it.

*Proof.* (i) Per-state invariants are preserved by every single step (A6), hence hold at every state of every linearization with no appeal to a global order. The allocation invariants (same-home uniqueness, dense chain contiguity) depend only on each `S`-allocation to `d` reading the current frontier: per-home comparability totally orders `(d, S)`'s allocations, so by H0 each reads the frontier its predecessor left and lands at the next slot — gapless, collision-free — and by H1 no cross-`(d, S)` step disturbs that frontier wherever the linearization places it. Every allocation's home precondition `d ∈ dom(M)` survives once met, since `G-PO` schedules only into homes already registered at `Σ` and ASN-0093's `M1` (document-set monotonicity) admits no document removal. Each step's precondition is thus met at its position, so the linearization is a valid execution. (ii) Any two linearizations of a finite partial order differ by a finite sequence of transpositions of adjacent `≺`-incomparable steps; incomparable steps here are into distinct `(d, S)` (per-home comparability makes same-`(d, S)` steps comparable), so each transposed pair commutes (H1), leaving the surrounding states and every committed address unchanged. Confluence to a single final state follows. ∎

*Via H3:* Augment `G-PO`'s `O` to admit `K.σ` steps, under two `≺`-constraints — *register-before-allocate* (`K.σ(d_new) ≺` every allocation into `d_new`) and pairwise comparability of any same-target registrations (vacuous under freshness) — leaving registration/allocation pairs into distinct homes and registration/registration pairs of distinct targets `≺`-incomparable. G1 extends verbatim: two linearizations differ by transpositions of three kinds — allocation/allocation into distinct `(d, S)` (H1), registration/allocation into distinct homes, and registration/registration of distinct targets (H3) — so each transposition leaves states and addresses unchanged. Confluence to one committed final state holds for the *full* execution.

## V0 — VerdictSnapshotLocal (AX, axiom)

A verdict obtained by a *single bounded access* — a single `Observe_K` (a predicate on one type's active view), or equally an `age` read of one home's single-state frontier `f_d` (A1) — is `Q(Σ_r)` for the one index `r` that access reads (A3): it is a sound statement *about the one state* `Σ_r`, and about no `Σ_{r'}` with `r' ≠ r`. The discriminator is *access count*, not type-confinement: what makes the verdict snapshot-local is that its lone access lands on one index, whether that access reads a type's active view or a home's cross-type frontier (A1). Because every state on `𝔼` is structurally canonical (A6), `Σ_r` is always a coherent referent — there is always a well-defined "single frozen view" to evaluate `Q` against.

## V2 — VerdictReaderSnapshot (LEMMA, lemma)

For a multi-read verdict — `p ≥ 2` constituent bounded-access reads composing one `Q`, whether `Observe_K` calls across types or the active-view read and per-home frontier descents of a `stale` enumeration (A1) — three conditions stand in a chain of *strict* implications, not in equivalence:

`[all p reads at one committed index Σ_r] ⟹ [no Q-affecting step linearizes between the first and last read] ⟹ [the verdict is sound about a single state].`

The middle condition — *no `Q`-affecting step between the reads* — is the weakest *sufficient* condition this note establishes, **not** a necessary one: the implication to soundness is genuinely *strict*, since a verdict may come out sound by other routes even when a `Q`-affecting step does fall between the reads.

*The first implication is strict:* a non-`Q`-affecting step falsifies `[all reads at one index]` (it advances the index) while preserving soundness (every banked `v_i` still equals `c_i(Σ_{r₁})` since the step disturbs no not-yet-read constituent). Witness: the trace-minus-nullify from §8, where the `K₁`-emit moves the index but leaves soundness intact.

*The second implication is strict:* a short-circuit combiner `g(v₁, v₂) = (v₁ ≠ ∅) ∨ (v₂ = ∅)` over two active-view reads, at a start state with `A_{K₁} = {T₁} ≠ ∅`, yields `g({T₁}, {T₂}) = ⊤ = Q(Σ_{r₁})` *sound about `Σ_{r₁}`* even with an intervening `Q`-affecting `K₂`-emit, because `g`'s short-circuit discards the disturbed constituent.

The banking argument: for each `i`, any `Q`-affecting step in `[r₁, r_i)` is precluded by the middle condition, so `c_i` is constant on `[r₁, r_i]` and the captured value is `v_i = c_i(Σ_{r_i}) = c_i(Σ_{r₁})`; this holds for frontier constituents `c_i = f_{d_i}` no less than for active-view constituents; so `g(v₁, …, v_p) = g(c₁(Σ_{r₁}), …, c_p(Σ_{r₁})) = Q(Σ_{r₁})`.

The one-index condition is *role*-dual to W4 (reader-side vs writer-side) but *global* in scope, not per-home: any writer step at any home advances the index, so pinning `p` reads to one index excludes *all* writers for the read's duration, unlike the local per-`(d,S)` exclusions of clauses 2 and 5. Even V2's weaker middle condition is not per-home: type-scoped for a cross-type join (ranging across all homes carrying `Q`'s types), and home-scoped over the member homes for a `stale` enumeration (any link emit into a member home moves its frontier constituent).

## V1 — VerdictRetrospective (AX, axiom)

A verdict `Q(Σ_r)` is retrospective: it asserts `Q` of `Σ_r` and of nothing later. For `r' > r`, `Q(Σ_{r'})` may differ — any step at index `j` with `r ≤ j < r'` may falsify `Q`. Extending a verdict from "held at `r`" to "holds through `r'`" requires an *additional* hypothesis the substrate does not supply: that no `Q`-falsifying step is linearized in the interval `[r, r')`. That hypothesis is a constraint on writers' linearization points relative to the observer's read — a coordination-layer obligation (extinction discipline, fair scheduling, bounded work — the coordination layer's named hypotheses), not a substrate guarantee.

## MIC — MinimalIsolationContract (DEF, definition)

A faithful realization of the substrate's consistency model must honour:

1. **Per-step atomicity (A0).** Each atomic transition is applied indivisibly; no observer reads a state strictly between `Σ_i` and `Σ_{i+1}`.

2. **Per-home allocation serialization (H0, W2, W3).** For each `(home, subspace) (d, S)`, the frontier-read-and-deposit of any two `S`-allocations to `d` are mutually exclusive. Cross-`(d,S)` allocations need no coordination (H1).

3. **Commit-before-acknowledge (A7).** An operation's response is produced only at or after its linearization point.

4. **Per-call snapshot reads (A3, A1).** Each individual *single-bounded-access* read — an `Observe_K`, and equally BH4's `age`, the one read A1 places outside the `Observe_K`-grade camp yet shows recovers one home's single-state frontier `f_d` in *one* bounded access — is evaluated against a single committed state `Σ_k`, and never witnesses a partial step. The discriminator is *access count*, not `Observe_K`-grade-ness (A1): one bounded access lands on one index, whether it reads a type's active view or a home's cross-type link frontier. The *several*-access reads — cross-type joins and `stale` (whose global active-membership filter makes it a multi-read at every member-home count, single-home included) — are clause 7's, not this clause's.

5. **Per-run critical section for contiguous runs (W4).** A definition's multi-atom content run holds exclusion on its `(d, s_C)` for the run's duration; no foreign content allocation to `d` interleaves.

6. **Registry write confinement (W6).** Registry writes occur only in the construction of `Σ_init`; the runtime relation has no registry-write step.

7. **Per-verdict reader snapshot (V2).** A verdict composed of two or more bounded-access reads — several `Observe_K` calls, a cross-type join, or a `stale` enumeration (A1) — must have all its constituent reads pinned to one committed index — a reader-side critical section holding the read sequence against any interleaving writer step. This exclusion is *global*, not per-home: any writer step at any home advances the index, so pinning `p` reads to one index excludes *all* writers for the read's duration, unlike the local per-`(d,S)` exclusions of clauses 2 and 5. Even V2's weaker sufficient condition — no `Q`-affecting step between the reads — is not per-home: type-scoped for a cross-type join, home-scoped over the member homes for a `stale` enumeration. A *single-bounded-access* verdict — a single `Observe_K`, or an `age` read (A1) — discharges this clause for free under clause 4.

8. **Per-coverage-class idem=⊤ de-duplication serialization (I1a, I4).** For each coverage class `[K]` of an `idem(K) = ⊤` type, the dedup-read of the *global* active subset `A_K` and the consequent deposit form **one atomic action**, pinned to the operation's linearization index — so an `Emit_K` that misses does so against its *own* deposit's pre-state, never a stale earlier state. This is a *per-coverage-class* serialization: since the dedup-read of `A_K` is global (ASN-0128 I1), it is **non-per-home** — strictly stronger on its own axis than clause 2's per-home exclusion, and orthogonal to it (clause 2 still governs the deposit's allocation freshness). Drop it and per-home MIC permits the duplicate *regardless of home*: two coverage-equal `idem = ⊤` emits may each read a stale `A_K` and both miss, then deposit at *distinct* addresses — cross-home at their two home frontiers (no allocation collision, H1), same-home at consecutive slots `φ, φ+1` that clause 2's own deposit-spacing supplies.

## M1 — SafetyUnderMIC (LEMMA, lemma)

Under MIC:

*(a) No torn effect.* Any single emission or nullification is one step; by clause 1 (A0) the reader's state is before or after it, never within (A4). A batch's constituents are each whole, and clause 4 ensures each read is one canonical snapshot (A6) — fully structurally canonical, never corrupt (though, by §2, possibly mid-batch).

*(b) No single operation's effect observed twice; idempotent emission admits no duplicate under clause 8.* *(i)* Each state-changing operation is realized at one unique index (A1), so its effect appears exactly once in the order; no single operation is double-applied. *(ii)* Under `idem(K) = ⊤` and *clause 8*, the active subset holds at most one tuple per coverage class at every state a `K`-surface-emitted derivation reaches (ASN-0128 I1a, ActiveIdemUniqueness). Per-home MIC clauses 1–7 *alone* do not place an `idem = ⊤` execution in that scope — I1a's single-survivor rests on each deposit being a genuine *miss against its own pre-state* (the operative sense), and clause 4 pins the dedup-read only to *some* committed state, never to the deposit's own linearization index; the both-miss interleaving is `K`-surface-emitted under I1a's *literal* clause but *not* in the operative sense. Clause 8 restores the coincidence: by fusing each `idem = ⊤` dedup-read to its own deposit's pre-state, every deposit is a genuine miss-against-its-own-pre-state, I1a applies, and `A_K` carries at most one tuple per coverage class. A second `Emit_K` with coverage-equal `(F, G)` is a zero-step hit only while the incumbent is active; if the incumbent was nullified, the second emit is a *miss* depositing a fresh tuple (deliberate resurrection, ASN-0128 I2; ASN-0086 R6c). *(iii)* `idem(K) = ⊥` duplicates by design: two `Emit_K` calls with identical `(F, G, K)` produce *distinct* addresses, and both appear in the active subset (ASN-0128 I5). MIC neither prevents nor intends to prevent this.

*(c) No allocation collision.* Two sub-allocator emissions `K.α`/`K.λ_sh` conflict only when into the same `(d, S)` (H1, H2); clause 2 serializes exactly those, so each reads a distinct frontier (H0) and deposits a fresh, unique address (W2); clause 5 extends this to whole runs (W4). Cross-home writers never collide (H1). Document registration `K.σ` falls outside this clause; same-`d` racing registrations are resolved by rejecting the loser.

*(d) No multi-read verdict straddles a write.* A *single-bounded-access* verdict — a single `Observe_K`, or an `age` read of one home's frontier `f_d` (A1) — reads one canonical state by clause 4 (A3, A6, V0). A multi-read verdict — `p ≥ 2` accesses: a cross-type join, or a `stale` enumeration (single- or multi-home) — under clause 7 has its `p` constituent reads pinned to one committed index `Σ_r` (V2), so it is a statement about one coexisting state. Durability past `r` remains V1's separate hypothesis, which no MIC clause supplies. ∎
