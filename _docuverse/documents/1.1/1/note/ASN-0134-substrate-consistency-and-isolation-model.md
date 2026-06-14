# ASN-0134: Substrate Consistency and Isolation Model

*2026-06-13*

*What the sequential substrate promises a concurrent client: the step is the atom, the home is the unit of contention, and the snapshot is the only honest referent for a verdict.*

**Depends:** ASN-0086 (Typed Relations on Address Sets), ASN-0093 (Allocation Substrate), ASN-0126 (Substrate Shape Framework), ASN-0128 (Substrate Type Operational Semantics).

We are handed a substrate whose entire dynamics is a *sequence*. The governing axiom — `SequentialTransitionAxiom`, asserted in ASN-0093 and inherited verbatim by ASN-0128's gated relation `→_sh` — says that transitions `Σ → Σ'` are atomic, uninterruptible, and totally ordered, and that `Σ →* Σ'` is the reflexive-transitive closure of single steps. The operation surface of ASN-0128 is defined the same way: `Emit_K`, `Nullify_Binary`, `Observe_K` are specified by what one step does to one state. And yet every layer raised on this substrate presumes a crowd. A predicate may be evaluated by an *arbitrary* observer. Quiescence — "is everyone done?" — must be recognizable *while writers may still be active*. A definition's content must be allocated as one contiguous run *even as other agents allocate*. The very corpus this note belongs to was produced by a runner driving many workers against one store. So the question is forced upon us: a definition written in the singular is being *used* in the plural, and we must say exactly what survives the translation.

This note does not add a concurrency-control mechanism — no lock, no transaction manager, no scheduler. Nelson never specified one (his own consultations are candid that "no locking protocol... no concurrent-editing semantics" appears in *Literary Machines*, and that the back end was left to supply it), and Gregory's `udanax-green` supplies exactly one realization (a single-threaded event loop) rather than a contract. What we owe is the *contract* that sits between them: the weakest discipline an implementation must honour so that the sequential semantics is faithfully presented to concurrent clients. We will find that the contract is much weaker than the global serialization Gregory's loop happens to provide — it is *per-home*, not global — and that this is not an accident of engineering but precisely Nelson's design intent, where "order is always local, fixed at one home, by order of arrival," never "a synchronous agreement reached among all observers."

## What this note commits

- **The atomic unit is the step.** A single `→_sh` step is the grain of all-or-nothing. A typed emission (`Emit_K` miss, `Nullify_Binary` miss) is *exactly one* step; an idempotent hit and an `Observe` are *zero* steps. A fire/batch (a `retract_stale`, a definition's content run) is *many* steps and is **not** atomic. (A0–A5.)
- **Observations read committed snapshots.** An `Observe` is a total function of one state `Σ_k`. It never witnesses a partial step. It *can* witness the partial effect of a batch. Every state it can land on is structurally canonical. (A3, A4, A5.)
- **Linearization is by construction, and it is local.** Each state-changing operation appears to take effect at one index — its linearization point. Any one execution is globally serial, but the order an implementation must *force* is necessary only within each home; cross-home steps commute, so every linearization of a per-home-serial schedule is valid and they all reach the same committed state. (A1, A2, H0–H2, G0, G-PO, G1.)
- **An invariant partition.** Monotonicity, immutability, cross-home uniqueness, the active/audit-slice relationship, and registry stability are preserved by the model itself (per-step atomicity is enough). Same-home uniqueness, dense chain contiguity, and run contiguity are preserved *only* by serialization — and only per-home serialization is required. (W0–W6.)
- **A minimal isolation contract** with six clauses, and a theorem that under it no reader sees a torn effect, no single operation is double-applied, and no writer collides with a concurrent writer's allocation. (MIC, M1.)
- **Quiescence as a snapshot predicate.** A verdict read by one `Observe` is sound *about its read index* and only about it; durability past that index is a separate hypothesis about writers' linearization points, which the substrate does not supply. (V0, V1.)

---

## 1. The grain: a step, not a batch

We begin by fixing what "an execution" is, because every later claim is a statement about it. By `SequentialTransitionAxiom` the substrate's behaviour under any number of agents is a single sequence of states

`𝔼 :  Σ₀ → Σ₁ → Σ₂ → ⋯`

in which each `Σ_i → Σ_{i+1}` is one atomic step `σ_i` drawn from the step vocabulary of ASN-0128's gated relation, `K = {K.σ, K.α, K.λ_sh}` — that is `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh`: document registration, content allocation, and gated link/tuple emission. (We commit `𝔼` to this one substrate stack — ASN-0093's allocation model carried up through ASN-0086/0126/0128 — rather than mixing in a second foundation's arrangement-and-entity steps; the operation surface every later claim invokes, `Emit_K`/`Nullify_Binary`/`Observe_K`, is defined over exactly this stack.) Write `idx(σ) = i` for a step's position. We index states by their position in this one order; `Σ_i →* Σ_j` holds exactly when `i ≤ j`. This sequence is not a description of how an implementation is built — Gregory's loop builds it one way, a future per-home scheduler might build it another — it is the *meaning* the implementation must present. The agents, the scheduler that places their proposals, the fairness with which it does so: all of that is upstream of `𝔼` and out of scope here (it is the coordination layer's named hypothesis, the implementer's territory). What we reason about is `𝔼` and the states on it.

The first thing to extract is the observational reading of atomicity. The axiom says steps are *uninterruptible*; observationally this means:

> **A0 (StepAtomicity).** There is no state strictly between `Σ_i` and `Σ_{i+1}`. The states an observer can ever name are exactly `{Σ_k : k ∈ 𝔼}`.

A0 is not a new assumption; it is `SequentialTransitionAxiom` read as a constraint on what can be seen. Its force is entirely negative and entirely decisive: a half-applied step is not a state of `𝔼`, so it is not nameable, so it cannot be read. Every consequence below is a cash-out of A0.

Now we connect operations to steps. An agent *proposes* an operation; the substrate *realizes* it as activity on `𝔼`. We must be precise about the realization count, because it is where "the unit of atomicity" is decided.

> **A1 (Realization).** A state-changing operation is realized as *exactly one* atomic step, at a unique index. Distinct state-changing operations occupy distinct indices. A non-state-changing operation — an `Observe`, an idempotent `Emit_K` hit, the hit branch of a `Nullify_Binary` — is realized as *zero* steps; it reads a state and returns.

A1's "exactly one / exactly zero" is read straight off ASN-0128. An `Emit_K` *miss* invokes `K.λ_sh`: one step. An `Emit_K` *hit* under `idem = ⊤` "takes no step: `Σ' = Σ`" (ASN-0128 I1): zero steps. `Nullify_Binary` is `Emit_R(…)`, one `K.λ_sh` on a miss and "no step" on a hit (ASN-0128 S3). `Observe_K` "leaves Σ unchanged" (ASN-0086): zero steps. And distinctness of indices is just the totality of the order: two steps cannot share a position. We have therefore answered the first half of the headline question already, but it is worth saying it as a claim rather than letting it hide inside A1:

> **A2 (LinearizationPoint).** A state-changing operation `op` realized as step `σ` has linearization point `lin(op) = idx(σ)`; its *entire* effect is the single transition `Σ_{lin(op)} → Σ_{lin(op)+1}`. A zero-step operation has `lin(op)` equal to the index of the state it reads, and its effect on state is the identity.

The phrase "its entire effect is the single transition" is the operative content. A typed emission does not dribble its effect across several states; it is in `Σ_{lin}` not at all and in `Σ_{lin+1}` in full. This is what makes the *typed emission* coincide with the *step* as the atomic unit. The third candidate the question offers — "a whole fire/batch" — is a different animal, and we now show it is *not* atomic.

A *batch* (we use the words *fire* and *batch* interchangeably) is a finite collection of operations issued as one logical act by one agent or one rule firing — a `retract_stale` issuing one `Nullify_Binary` per stale event (ASN-0128 BH4, which states outright it is "a sequence of wrapper steps, not an atomic operation"), or a definition's content run, one `K.α` per atom of the definition. Its constituent steps land at some indices `i₁ < i₂ < ⋯ < i_m` in `𝔼`. Call the batch **contiguous** when `{i₁,…,i_m} = {i₁, i₁+1, …, i₁+m−1}`, i.e. no foreign step interleaves; otherwise **split**.

> **A5 (NoBatchIsolation).** The substrate does not guarantee that a batch is contiguous. If a batch is split, then for some foreign step at index `j` with `i₁ ≤ j < i_m`, the state `Σ_{j+1}` lies *between* two of the batch's effects; an `Observe` at any such index witnesses a strict, non-empty subset of the batch's effects. Hence a batch is, in general, *not* atomic: its partial effects are observable.

The contrast with A2 is the whole point. A single step is indivisible by A0; a batch is divisible because the order may place foreign steps among its constituents. The substrate's atom is the step. *Batch atomicity, where a layer needs it, is something the layer must construct* — by making the batch contiguous, which is a critical section, which is a discipline the substrate neither provides nor forbids. We return to the one batch the corpus actually demands be (locally) contiguous — the definition's content run — in §6.

## 2. What an observation witnesses

We can now say exactly what `Observe_K`, evaluated by any agent at any time, sees relative to an `Emit_K` or `Nullify_Binary` in flight. The answer is fixed by A0 and A1, and it is clean.

> **A3 (SnapshotRead).** An `Observe` realized at index `k` is a total function of the single state `Σ_k`. Its result depends on no other state.

This is just the zero-step half of A1 together with the definition of `Observe_K` in ASN-0086 as a function of `Σ`. From A3 and A0 we get the read-isolation theorem:

> **A4 (NoTornStep).** No `Observe` witnesses a partial step. For an `Observe` at index `k` and a state-changing `op` with `lin(op) = i`: if `k ≤ i` the `Observe` sees none of `op`'s effect; if `k ≥ i+1` it sees all of it. There is no third case.
>
> *Proof.* `op`'s effect is precisely the transition `Σ_i → Σ_{i+1}` (A2). The reader's state `Σ_k` is either at-or-before `Σ_i` (`k ≤ i`, effect absent) or at-or-after `Σ_{i+1}` (`k ≥ i+1`, effect present). The excluded middle — a state strictly between `Σ_i` and `Σ_{i+1}` — does not exist (A0). ∎

So the disjunction in the headline question — "only committed state, or can it witness a partial effect?" — resolves to the first horn for any single emission or nullification: **only committed state**. An `Emit_K` "in flight" is, from the snapshot's vantage, either not-yet-linearized (its step has not happened; the reader sees the pre-state) or linearized (its step has happened; the reader sees the full post-effect). "In flight" never means "half-applied," because there is no half-state to be in. This is the formal core of Nelson's intent that "a torn read is impossible": content lives at permanent addresses and is never rewritten in place, so the only thing a step changes is which addresses are *present* in a store (and, for a link tuple, which it relates) — and that change is the step itself, indivisible.

The one honest qualification is A5's: while no *step* is ever torn, a *batch* is not protected. A reader can land between the constituent nullifications of a `retract_stale` and see some events retracted and others not; it can land partway through a definition's content run and see only a prefix of its atoms. We must therefore characterize *what kind of state* a mid-batch snapshot is, so that a reader who lands there is not misled about its validity.

The `→_sh` stack gives a sharp answer — sharper, in fact, than the read-isolation story usually told of a transactional store. Every invariant the stack carries is a *per-state* invariant, preserved by *every* single `→_sh` step, with no class of properties reserved for the boundaries of multi-step composites: the store partition and immutability of ASN-0093 (`C0` content immutability, `L12` link immutability, `SD` store disjointness, the chain conformances `C1c`/`L1c`), the shape and registry stability of ASN-0126 (`P6` ReachableConformance, `P1`, `P2`), and their ASN-0128 liftings (`R1`, `R2`). There is, in this stack, no provenance relation to leave dangling and no arrangement to leave half-coupled — the substrate carries no coupling obligation that a *later* step must discharge.

> **A6 (CanonicalState).** Call a state *structurally canonical* iff it satisfies the per-state invariant package of the `→_sh` stack (ASN-0093's store invariants, ASN-0126's `P6`/`P1`/`P2`, ASN-0128's `R1`/`R2`). *Every* state on `𝔼` is structurally canonical, because each of these invariants is preserved by every single step. No weaker "boundary-only" class of property exists: a `→_sh` state is either fully canonical or unreachable.

A6 is the formal reading of Nelson's "canonical order is an internal mandate of the system" — the property that "all changes, once made, left the file remaining in canonical order," with *nothing* uncanonical in between. There is nothing uncanonical in between because there is no state in between (A0), and every state there *is* satisfies the full package (A6).

But A6 is a statement about *structure*, and it is silent about *settledness* — and the two must not be run together. A reader who lands mid-batch sees a state that is *completely* canonical: addresses partitioned correctly, every stored tuple shape-conformant and registered, every chain gapless and conformant. Nothing in it is marked "mid-batch." A `retract_stale` that has nullified three of its five targets leaves a state indistinguishable, *by every invariant the stack carries*, from a settled state in which only those three were ever to be retracted; a content run halted after two of its atoms is indistinguishable from a settled two-atom definition. Canonicity does not encode "more is coming." So there is no "precise and only sense of incomplete" that a snapshot exposes — incompleteness is not a property of the state at all, but a *relation* between the state and a batch that happens to span it, and that relation is invisible from inside the snapshot. An observation is therefore never *corrupt*, yet its canonicity does not certify that it is *final*. This gap — canonical but possibly mid-batch — is the substrate's actual read-isolation guarantee, the one Nelson left "correctly open" at the multi-step level while the single-step level was closed by construction. It is also the seed of §8's V1: a verdict's *durability* needs a hypothesis about the future of the order that the present snapshot, however canonical, cannot supply.

## 3. Linearization: how independent proposals become one order

The question asks whether there is a linearization point and how independently-proposed operations become positions in the one order. A2 already named the point. What remains is to say what an implementation must do to *honour* it, since the abstract model simply postulates the order while an implementation must produce it from genuinely concurrent proposals.

The model is *sequentially consistent* by construction: there exists a single total order of atomic steps, each operation appears atomic at its `lin`, and — this is the subtle and characteristically Xanadu part — the order is *logical, not temporal*. Nelson is emphatic that "time is not included in the tumbler; time is kept track of separately." The order on `𝔼` carries no wall-clock; it is a sequencing of *arrivals at a home*, not a stamping onto a global timeline. So the abstract guarantee is sequential consistency, and the address space deliberately refuses to encode anything stronger.

> **G0 (SequentialConsistency).** The substrate realizes a single total order of atomic steps (`SequentialTransitionAxiom`); equivalently, it is sequentially consistent. The order is logical (a per-home arrival sequencing), carrying no global temporal coordinate that observers must agree on.

An implementation strengthens G0 to *linearizability* — the order respecting real-time precedence between a response and a subsequent invocation — exactly when it commits the effect before it acknowledges the operation. Gregory's evidence pins the realized linearization point precisely: the in-memory enfilade *is* the shared canonical state, and a write becomes visible to every other session at the completion of the `xanadu(&task)` dispatch — "the mutation is applied at mutation-function-return time, but it is not reachable by any other session until the cooperative event loop returns." That is a clean linearization point at commit. But Gregory also surfaces a place where the realization *under*-honours the contract: for `INSERT`, `DELETEVSPAN`, and `REARRANGE`, the response is emitted *before* the mutation executes ("response-before-check"), so a client can receive "success" for an effect not yet committed (and which may silently fail). An implementation honouring the contract must not do this. We therefore record acknowledgment ordering as a contract clause, not an optional nicety:

> **A7 (CommitBeforeAcknowledge).** For the linearization point of A2 to be presentable to a concurrent client, an operation's response/return value must be produced only at or after `lin(op)`. An acknowledgment emitted before the committing step is unsound: it lets a caller act on an effect that is not yet (and may never be) in the order.

With A7, a reader or caller never observes — never *acts upon* — an uncommitted effect, which is the linearizability strengthening of A4 from "reads" to "the responses agents build their next move on."

How, then, do two independently-proposed operations *become* positions? They are *placed* — by whatever scheduler the implementation runs — into distinct indices (A1). The placement mechanism is out of scope; its *existence and injectivity* is `SequentialTransitionAxiom`. The interesting question is not *that* a placement exists but *how much* the placement is allowed to vary without disturbing the semantics — because that is what tells an implementer how much concurrency they may safely permit. That is the subject of the next two sections, and it is where the global order turns out to be far more freedom than the invariants actually need.

## 4. Where the order must live: per-home, not global

Consider what an allocating step actually reads and writes. By ASN-0093 and the `FrontierUnification` lemma of ASN-0126, an emission into a home `d`'s sub-allocator for subspace `S ∈ {s_C, s_L}` reads the home's current *frontier* and deposits at it. Let us make the frontier uniform across both subspaces. For `S ∈ {s_C, s_L}` write `dom_S(Σ)` for `dom(Σ.C)` when `S = s_C` and `dom(Σ.L)` when `S = s_L`, and define the home's `S`-population and `S`-frontier index

`P_S(d, Σ) = {a ∈ dom_S(Σ) : origin(a) = d}`,  `φ_S(d, Σ) = |P_S(d, Σ)|`.

By `ChainMembershipForOrigin` (ASN-0093), `P_S(d, Σ)` is a *contiguous initial segment* of the chain `A_S(d)`, so `φ_S(d, Σ)` is the count of already-emitted slots and the next emission lands at chain slot `φ_S(d, Σ)`, advancing the count by one. (For `S = s_L` this is exactly ASN-0126's `a_emit(Σ,d) = chain_d(f_d^Σ)`; for `S = s_C` it is `SubsequentEmissionFreshness`'s `inc(a_prev, 0)` with `a_prev` the home's content maximum. The two are one mechanism.)

> **H0 (FrontierDiscipline).** Along `𝔼`, for fixed `(d, S)`, `φ_S(d, ·)` is non-decreasing, increases by exactly one at each `S`-allocation to `d`, and is left unchanged by every other step.
>
> *Proof.* An `S`-allocation to `d` adjoins one fresh address with `origin = d` and subspace `S` (ASN-0093 K.α / ASN-0128 K.λ_sh effect), so `|P_S(d, ·)|` rises by one. Any other step is either a `K.σ`, which registers a document and frames both stores (`C' = C ∧ L' = L`, ASN-0093 K.σ), leaving every `dom_S` fixed; or an allocation into a different `(d', S') ≠ (d, S)` — to another home, or to the sibling subspace of the same home — which by `DisjointSubAllocatorChains` (`S' ≠ S`) and `CrossDocumentDisjointness` (`d' ≠ d`) deposits outside `P_S(d, ·)`. In every case `P_S(d, ·)` is unchanged. ∎

H0 is the lever. It shows that the *only* steps that touch `(d, S)`'s frontier are the `S`-allocations to `d` themselves. From this the conflict structure of allocation falls out immediately.

> **H1 (CrossHomeIndependence).** Two allocation steps into distinct `(d, S) ≠ (d', S')` *commute*: neither reads or writes state the other touches, and applying them in either order yields the same state.
>
> *Proof.* The first reads `φ_S(d,·)` and writes one address on chain `A_S(d)`; the second reads `φ_{S'}(d',·)` and writes on `A_{S'}(d')`. The two chains are disjoint with prefix-incomparable anchors (`DisjointSubAllocatorChains` for `d = d'`, `S ≠ S'`; `CrossDocumentDisjointness` for `d ≠ d'`). By H0 neither step changes the other's frontier population. So each step's precondition (its frontier value) and effect (its deposited key) are on state disjoint from the other's; they commute. ∎

> **H2 (SameHomeConflict).** Two allocation steps into the *same* `(d, S)` conflict: each reads `φ_S(d,·)`, and the first to commit increments it (H0), so the two *cannot* read the same frontier value without colliding. If both read frontier `φ`, both deposit at chain slot `φ` — the *same address* — violating freshness.
>
> *Proof.* Two emissions into `(d, S)` against a common pre-state `Σ_pre` read the same population `P_S(d, Σ_pre)`, and the emission rule is a function of that population, so they compute the same deposit address — in *either* of its two branches.
>
> *Interior case* (`P_S(d, Σ_pre) ≠ ∅`): `SubsequentEmissionFreshness` gives `a = inc(a_prev, 0)` with `a_prev = max P_S(d, Σ_pre)`; both read the same `a_prev`, hence compute the same `a`.
>
> *First-emission boundary* (`P_S(d, Σ_pre) = ∅`): here `max P_S(d, Σ_pre) = max ∅` is undefined and the subsequent rule does not apply. Instead both emissions satisfy ASN-0093's *first-emission* predicate `{a' : origin(a') = d} = ∅` and both compute the determinate first slot `a = [d.0.S.1]` (`FirstEmission`). This is the race for the *first* allocation into a fresh home, and it collides just as squarely.
>
> In either case the two compute one address; whichever commits first deposits it, and the second's freshness precondition — `a ∉ dom_S`, discharged in the interior case by `SubsequentEmissionFreshness` and at the boundary by `FirstEmissionFreshness` — then fails. The conflict is identical at the boundary and in the interior. ∎

H1 and H2 together are the whole answer to "is ordering per-home-independent or globally serialized." The *conflicts* — the places where order matters — are confined to a single `(home, subspace)`. Everything across homes (and across the two subspaces of one home) commutes. This is not our invention; it is Nelson's "owned numbers" made operational. His account of two simultaneous creators is exactly H1+H2: they are "either in different regions (no shared allocator) — and there is no race to lose — or under the same single allocator, which serializes them." The address space is a tree of owned sub-allocators; two writers contend only when they reach into the *same* sub-allocator, and then a single authority sequences them. Collision is "impossible by construction," with "zero coordination" required across regions.

We can now state the equivalence that liberates an implementation from global serialization. To state it *non-vacuously* we must first name an execution model weaker than the total order `𝔼` — for a total order *already* serializes every pair of steps, cross-home included, so against `𝔼` alone "per-home serialization suffices" would collapse into the empty tautology "the total order is total." The content we are after lives one level below `𝔼`, in the *schedule* an implementation commits to before any particular interleaving is realized.

> **G-PO (PartialScheduleModel).** A *schedule* over a reachable start state `Σ` is a finite set `O` of allocation steps (`K.α`, `K.λ_sh`) into homes registered at `Σ`, equipped with a partial order `≺` — the order the implementation *forces* — such that for every `(d, S)` the `S`-allocations to `d` in `O` are pairwise `≺`-comparable (*per-home serialization*), while steps into distinct `(d, S) ≠ (d', S')` need not be. A *linearization* of `(O, ≺)` is any total order extending `≺`; run from `Σ`, each linearization is one execution `𝔼`. The total order of §1 is the special case in which `≺` is itself total.

G-PO admits exactly the schedules an implementer cares about: those that force an order *only within each home* and leave cross-home steps `≺`-incomparable. Against this model the liberation is a genuine claim, not a tautology.

> **G1 (PerHomeSerializabilitySuffices).** Let `(O, ≺)` be any per-home-serialized schedule over a reachable `Σ`. Then (i) *every* linearization of `(O, ≺)` is a valid execution preserving every per-state invariant at every state and every allocation invariant in its final state; and (ii) all linearizations are *confluent* — they reach one and the same final state, with the same address at every chain slot of every home. The cross-home order is free to vary, and no invariant and no committed address depends on how a linearization resolves it.
>
> *Proof.* (i) Per-state invariants are preserved by every single step (A6), hence hold at every state of every linearization with no appeal to a global order. The allocation invariants (same-home uniqueness, dense chain contiguity) depend only on each `S`-allocation to `d` reading the current frontier: per-home comparability totally orders `(d, S)`'s allocations, so by H0 each reads the frontier its predecessor left and lands at the next slot — gapless, collision-free — and by H1 no cross-`(d, S)` step disturbs that frontier wherever the linearization places it. Each step's precondition is thus met at its position, so the linearization is a valid execution. (ii) Any two linearizations of a finite partial order differ by a finite sequence of transpositions of adjacent `≺`-incomparable steps; incomparable steps here are into distinct `(d, S)` (per-home comparability makes same-`(d, S)` steps comparable), so each transposed pair commutes (H1), leaving the surrounding states and every committed address unchanged. Confluence to a single final state follows, and ASN-0093's sequential results, holding along any one linearization, thereby describe them all. ∎

G1 is the practical payload. An implementer is *not* obliged to commit a total schedule — Gregory's single global loop is one such, and a maximally serial one. They may instead commit a schedule that forces an order *only within each home*, leaving agents in different homes `≺`-incomparable and so free to proceed with no coordination whatsoever; by G1(i) every interleaving the runtime then produces is a valid execution, and by G1(ii) they all reach the same committed state — observationally indistinguishable, for all of the substrate's invariants, from the global order the axiom postulates. Gregory's loop over-satisfies the requirement; per-home serialization is the least that meets it. This is exactly Nelson's distributed intent (each server "at all times unified and operational," progress never gated on a global agreement) rescued from the implementation's incidental global lock.

## 5. The invariant partition: what the model keeps, what serialization keeps

We can now answer, invariant by invariant, the question of which guarantees are intrinsic to the model and which are bought only by serialization. The discriminator is the conflict analysis of §4: an invariant is *model-intrinsic* if per-step atomicity (A0) alone preserves it under arbitrary interleaving; it is *serialization-borne* if it additionally requires the per-home ordering of H0/H2.

> **W0 (MonotonicityStepLocal).** Append-only monotonicity and value-immutability — `C0` (ContentImmutability) and `L12` (LinkImmutability), both of ASN-0093 — are model-intrinsic. Each step's effect either adjoins a fresh key or frames the store; no step removes a key or rewrites a value. So under any interleaving of atomic steps, `dom` only grows and existing values never change. Needs A0, nothing more.

W0 is Nelson's deepest point about permanence, and it is worth quoting his reasoning because it *is* the proof: the permanence guarantees "had to be operation-intrinsic, because a guarantee asserted as absolute cannot depend on a reconciliation mechanism the design leaves open." There is no overwrite primitive; therefore "no scheduling of writers can produce an overwrite." Monotonicity is safe from concurrency *because of the shape of the operations*, not because of any ordering discipline.

> **W1 (CrossHomeUniquenessStructural).** Uniqueness of addresses allocated in *distinct* homes (or distinct subspaces of one home) is model-intrinsic. By `CrossDocumentDisjointness` / `DisjointSubAllocatorChains` the chains are disjoint with prefix-incomparable anchors, so `a ≠ a'` holds *independent of order*. Needs no serialization at all.

> **W2 (SameHomeUniquenessSerial).** Uniqueness of two allocations into the *same* `(d, S)` is serialization-borne. By H2 it holds iff the two emissions read distinct frontier values, i.e. iff they are serialized within `(d, S)`. Without per-home ordering, two emissions collide on one address.

> **W3 (ChainContiguitySerial).** Dense chain contiguity — `ChainMembershipForOrigin`'s property that `P_S(d, ·)` is a gapless initial segment of `A_S(d)` — is serialization-borne in the same per-home sense as W2. Given per-home ordering, every emission lands at the unique current frontier slot (H0), so the segment stays gapless; without it, two emissions either collide (a repeated slot) or, if an implementation "fixed" collisions by skipping, leave a hole. Gregory's evidence is decisive here and we adopt his framing as confirmation: the dense chains are "a property of serialization, not the data model — a truly concurrent allocator would preserve uniqueness and global monotonicity but lose contiguity whenever allocations interleave."

> **W5 (ActiveSliceStepLocal).** The relationship between the audit slice `L_K` (every type-`K` tuple ever emitted) and the active subset `A_K` (`L_K` minus `nullified`) is model-intrinsic. Both are *pure functions* of the state read; an `Observe` at index `k` computes both from `Σ_k` consistently (A3). Nullification only grows `nullified` (R6a, RetractionStability), and each `Nullify` evaluates its target precondition `P-tgt` at *its own* linearization state — so a nullify ordered before its target exists is simply rejected (the target is not yet a link address), never producing a dangling retraction. No interleaving can yield an incoherent slice: at every state, `A_K = L_K ∖ nullified` exactly. Needs only A0.

W5 deserves a word, because "audit/active-slice coincidence" is where one might fear a read could see a tuple that is both present and absent. It cannot. At any single `Σ_k` the two sets are derived together, so they are mutually consistent by construction. The only cross-agent subtlety is *which* order a nullify and its target's emission take — and that is resolved soundly by `P-tgt` being checked at the nullify's linearization state (ASN-0086, ASN-0128): if a writer means to retract another's tuple, the coordination layer must order the retraction *after* the emission, or the substrate will (correctly) reject it as targeting a non-existent address. The substrate never loses or duplicates; at worst it declines an out-of-order retraction. That declination is information, not corruption.

> **W6 (RegistryRaceFree).** The registry is immutable across all runtime steps (`RegistryInvariance` / P1 of ASN-0126, R1 of ASN-0128: `Σ.registry = Σ_init.registry` at every reachable state). No step in `K` writes it. Hence the question "may two agents writing the same registry interleave?" has *no realization*: registry writes are confined to the single, pre-execution construction of `Σ_init` (`R-VAL`), which is not a step of `𝔼`. Runtime registry access is pure read of an immutable structure — always consistent, never torn, by definition. The write-write race is *vacuously absent*.

W6 closes the "writing the same registry" horn of the question outright: there is no concurrent registry writing because there is no runtime registry writing. Registration is a single-authority construction act, and its immutability is load-bearing for the entire shape/type framework above it.

Collecting the partition: monotonicity (W0), cross-home uniqueness (W1), the active/audit relationship (W5), registry stability (W6), and the structural canonicity of every state (A6) are *kept by the model itself*. Same-home uniqueness (W2) and dense chain contiguity (W3) are *kept only by per-home serialization*. Nothing on the list requires *global* serialization — which is precisely G1's conclusion, now seen invariant by invariant.

## 6. The contiguous run

A higher layer may ask for something the bare frontier discipline does not give: that a definition's content occupy *one contiguous run* of addresses, even as other agents allocate. We must locate this requirement exactly, because it is stronger than W3 and weaker than a global lock.

Be careful to separate two contiguities. *Chain* contiguity (W3) says `P_S(d, ·)` is a gapless prefix of `A_S(d)` — every frontier slot, whoever filled it, is occupied. It holds under per-home serialization regardless of *which agent owns which slot*. *Run* contiguity is the stronger property a definition needs: that *this definition's* atoms occupy a *consecutive* block of slots, with no foreign atom wedged among them. Chain contiguity is about the chain having no holes; run contiguity is about *one author's* atoms forming an unbroken interval *within* the chain.

> **W4 (RunContiguityCritical).** A multi-atom content run for a definition in home `d` (a batch of `K.α` steps into `(d, s_C)`) occupies a contiguous block of `A_{s_C}(d)` iff no foreign allocation into `(d, s_C)` is interleaved between the run's first and last step. This is a *per-`(home, subspace)` critical section spanning the run* — strictly stronger than the per-step per-home serialization of W2/W3, strictly weaker than any cross-home exclusion.
>
> *Proof.* By H0 each `s_C`-allocation to `d` lands at the then-current frontier and advances it by one. If the run's `m` steps are the only `s_C`-allocations to `d` in the index interval they span, they land at consecutive slots `φ, φ+1, …, φ+m−1`: a contiguous block. If a foreign `s_C`-allocation to `d` lands at some interior index, it consumes a frontier slot between two of the run's atoms, and the run's remaining atoms land *past* it — the run's slots are `{φ, …}` with a foreign slot embedded, no longer an interval. By H1, a foreign allocation into any *other* `(d', S')` leaves `φ_{s_C}(d, ·)` fixed and cannot break the run. ∎

So the run's atomicity requirement is sharply scoped: hold a critical section on `(d, s_C)` for the run's duration; let every other home and the link subspace proceed freely. This is the one place the corpus genuinely needs *batch* contiguity (A5's general denial notwithstanding), and W4 says exactly how much exclusion buys it — no more than a single sub-allocator, for the length of one definition.

One implementation caveat earns a mention because it is a real divergence between the abstract model and Gregory's code, and an implementer must know which they are honouring. In the *abstract* model, content and links inhabit disjoint subspaces `s_C` and `s_L` with separate frontiers (`DisjointSubAllocatorChains`), so a link allocation to `d` *cannot* break a content run's contiguity — it advances `φ_{s_L}(d)`, not `φ_{s_C}(d)`. In Gregory's *implementation*, link orgls and text atoms share one granfilade allocation, so a `CREATELINK` interleaved into a text run *does* break text contiguity (his "insert-link-insert I-address gap"). The abstract claim W4 is the cleaner one and is the contract we specify: content run contiguity is threatened *only* by a concurrent content allocation to the same home. An implementation that, like Gregory's, fuses the subspaces inherits a coarser exclusion obligation; an implementation faithful to the subspace partition does not.

## 7. A worked allocation scenario

The analysis of §4 and §6 runs entirely on a generic `(d, S)`. It is worth grounding it once in explicit addresses — both to make the conflict structure concrete and to exhibit the exact collision a missing serialization produces.

Fix a node `[1]`, an account `[1.0.1]` under it, and two documents under that account:

`d = [1.0.1.0.1]`,  `d' = [1.0.1.0.2]`  — each with `zeros(·) = 2`, hence valid document homes.

By `FirstEmission` (ASN-0093) the content sub-allocator `A_{s_C}(d)` has anchor `b_C(d) = [d.0.s_C] = [1.0.1.0.1.0.1]` (with `s_C = 1`) and enumerates the content slots

`a_k := [d.0.s_C.k] = [1.0.1.0.1.0.1.k]`,  `k = 1, 2, 3, …`,

each successor `a_{k+1} = inc(a_k, 0)` advancing the final digit. Write `a'_k := [d'.0.s_C.k] = [1.0.1.0.2.0.1.k]` for `d'`'s content chain. Every `a_k` has `zeros(a_k) = 3` and `origin(a_k) = d`, as a content address must.

*Same-home collision (H2, interior).* Suppose `φ_{s_C}(d, Σ) = 3` — slots `a_1, a_2, a_3` are filled — and two writers `w₁, w₂` both propose a content allocation into `d` against this *same* `Σ`. By `SubsequentEmissionFreshness` each reads `a_prev = max P_{s_C}(d, Σ) = a_3` and computes its deposit as `inc(a_3, 0) = a_4 = [1.0.1.0.1.0.1.4]`. *Both compute the identical address `a_4`.* Whichever commits first deposits `a_4`; the second now finds `a_4 ∈ dom(C)`, so its freshness precondition `a_4 ∉ dom_{s_C}` fails (H2). Absent a discipline forcing the two to read distinct frontiers, they collide on one address.

*Same-home collision (H2, first-emission boundary).* The same collision occurs at `φ_{s_C}(d, Σ) = 0`. With `P_{s_C}(d, Σ) = ∅`, `max ∅` is undefined and the subsequent rule does not apply; instead both writers fire the first-emission predicate `{a' : origin(a') = d} = ∅` and both compute the determinate first slot `a_1 = [1.0.1.0.1.0.1.1]` (`FirstEmission`). They collide on `a_1` exactly as the interior case collides on `a_4`, now against `FirstEmissionFreshness`.

*Cross-home commutation (H1).* Now let `w₁` allocate into `d` and `w₂` into `d'`, against the same `Σ` with `φ_{s_C}(d, Σ) = 3` and `φ_{s_C}(d', Σ) = 0`. Then `w₁` lands `a_4 = [1.0.1.0.1.0.1.4]` and `w₂` lands `a'_1 = [1.0.1.0.2.0.1.1]`. The two anchors `b_C(d) = [1.0.1.0.1.0.1]` and `b_C(d') = [1.0.1.0.2.0.1]` are prefix-incomparable — they differ at the document digit — so by `DisjointSubAllocatorChains`/`CrossDocumentDisjointness` the deposits are distinct, and by H0 neither writer's frontier read is disturbed by the other. Applying the two in either order — `w₁` then `w₂`, or `w₂` then `w₁` — reaches the identical final state: the steps commute (H1). No coordination between the two writers is needed or useful.

*Run fragmentation (W4).* Finally let one author issue a 3-atom content run into `(d, s_C)` from frontier `φ_{s_C}(d) = 3`, intending the contiguous block `a_4, a_5, a_6`. If the run's three `K.α` steps are the only `s_C`-allocations to `d` in the index interval they span, they land exactly at `a_4, a_5, a_6` — one interval. But suppose a foreign `K.α` into `(d, s_C)` interleaves after the run's first atom: the run deposits `a_4`, the foreign step takes the next frontier slot `a_5 = [1.0.1.0.1.0.1.5]`, and the run's remaining two atoms land *past* it at `a_6, a_7`. The author's run now occupies `{a_4, a_6, a_7}` — fragmented, the foreign `a_5` wedged inside (W4). A foreign allocation into the *link* subspace `(d, s_L)`, or into any *other* home, advances a different frontier (H1) and cannot fragment the run — which is exactly the scope W4 claims for the critical section: `(d, s_C)`, and nothing wider.

These four vignettes are the whole conflict theory in miniature: collisions live at a single `(home, subspace)` (the `a_4`/`a_1` clashes), everything cross-home commutes (the `a_4` vs `a'_1` independence), and a multi-atom run needs exclusion on its own `(home, subspace)` for its duration and on nothing else (the `a_5` intrusion). Under MIC clause 2 the collisions vanish: serializing the two `d`-writers makes `w₁` read frontier 3 and deposit `a_4`, then `w₂` read frontier 4 and deposit `a_5` — distinct, fresh, and gapless (M1(c)).

## 8. Quiescence as a snapshot predicate

We come to the sharpest of the questions, and the one Nelson answered most directly: what does a quiescence verdict mean if it is read while a write is in flight? A higher layer wants quiescence — "is everyone done editing?" — recognizable from inside the predicate language even as writers remain active. We must say when such a verdict is *sound* and when it is a *race*.

A quiescence predicate `Q` is a predicate over states; a verdict is `Q(Σ_r)` for the read index `r` of the `Observe` that evaluates it. The first thing to settle is the *referent*: against what is the verdict taken?

> **V0 (VerdictSnapshotLocal).** A verdict obtained by a single `Observe` is `Q(Σ_r)` for one index `r` (A3): it is a sound statement *about the one state* `Σ_r`. Because every state on `𝔼` is structurally canonical (A6), `Σ_r` is always a coherent referent — there is always a well-defined "single frozen view" to evaluate `Q` against. The verdict is *not* a statement about any `Σ_{r'}` with `r' ≠ r`.

V0 is Nelson's answer made precise, and his framing is the right intuition: the verdict must be "taken against one version of the store at one instant — one cross-section of the space-time vortex." The reason a single-`Observe` verdict is *trustworthy* and a multi-read verdict is *accidental* is exactly his: if you evaluate different conjuncts of `Q` at different indices `r₁ ≠ r₂`, you have "quantified over a collection of states that never coexisted" — you might clear writer A against `Σ_{r₁}` (before its edit) and writer B against `Σ_{r₂}` (after its edit) and report "everyone done" for a configuration that held at *no single instant*. The soundness condition is therefore stark and simple: **all of the verdict's reads must occur at one index**, i.e. the verdict must be one atomic snapshot `Observe`. A6 guarantees that snapshot is always a real, canonical state; A3 guarantees it is read whole; A0 guarantees a concurrent write cannot smear it. So a verdict read "while a write is in flight" is *never corrupted by the write*: the in-flight write linearizes at some index `j`, and relative to `Σ_r` it is either already counted (`j < r`, its effect is in the snapshot — it is *committed*, not "in flight," from the snapshot's vantage) or not yet counted (`j ≥ r`, its effect is absent). The atomicity of the step (A0) forbids any "half-counted" writer. This is what it means for the verdict to be a snapshot rather than a race: it is the truth about the prefix of the order up to `r`.

But V0 says nothing about whether the verdict *stays* true, and here we must be honest about what a quiescence verdict can and cannot promise:

> **V1 (VerdictRetrospective).** A verdict `Q(Σ_r)` is retrospective: it asserts `Q` of `Σ_r` and of nothing later. For `r' > r`, `Q(Σ_{r'})` may differ — any step at index `j` with `r ≤ j < r'` may falsify `Q`. Extending a verdict from "held at `r`" to "holds through `r'`" requires an *additional* hypothesis the substrate does not supply: that no `Q`-falsifying step is linearized in the interval `[r, r')`. That hypothesis is a constraint on writers' linearization points relative to the observer's read — a coordination-layer obligation (extinction discipline, fair scheduling, bounded work — the coordination layer's named hypotheses), not a substrate guarantee.

V1 is the precise statement of the relationship the question asks for — "what relationship must hold between the observer's read and the writers' linearization for the verdict to be sound rather than a race." There are two distinct properties, and conflating them is the error:

- *Soundness* of the verdict needs only that the observer's reads all sit at one index `r` (V0). Given that, the verdict is a true statement about `Σ_r`, full stop, regardless of how many writers are "active." Activity that has linearized by `r` is counted; activity that has not is not; nothing is half-counted.
- *Durability* of the verdict — its remaining true after `r` — needs that no writer linearizes a falsifying step after `r`. This is a relationship the substrate cannot certify, because it concerns the *future* of the order, and the substrate's order carries no promise that the future is empty. To read "the system is quiescent and will stay so" off `Q(Σ_r)` is to add V1's hypothesis silently — which is precisely the smuggling a quiescence layer must refuse.

The practical reading for a quiescence recognizer: a recognizer that evaluates its quiescence condition with one snapshot `Observe` produces a *sound* verdict about that snapshot — it never mistakes a half-applied write for a whole one, and it never quantifies over a state that never existed. Whether that verdict licenses *terminating* the system is the separate, conditional question a termination layer answers with its named hypotheses about who may still fire. The substrate's contribution is exactly and only the snapshot: a single canonical state, read atomically, against which the predicate has a definite truth value. That is the "reached-and-held quiescence" referent; holding it is the layer's job.

## 9. The minimal isolation contract

We can now collect the discipline an implementation must honour. The contract is the conjunction of the clauses we have been forced to by the analysis; nothing in it is a mechanism (no lock, no transaction, no scheduler), only obligations that any mechanism must meet.

> **MIC (MinimalIsolationContract).** A faithful realization of the substrate's consistency model must honour:
>
> 1. **Per-step atomicity (A0).** Each atomic transition is applied indivisibly; no observer reads a state strictly between `Σ_i` and `Σ_{i+1}`.
> 2. **Per-home allocation serialization (H0, W2, W3).** For each `(home, subspace) (d, S)`, the frontier-read-and-deposit of any two `S`-allocations to `d` are mutually exclusive. Cross-`(d,S)` allocations need no coordination (H1).
> 3. **Commit-before-acknowledge (A7).** An operation's response is produced only at or after its linearization point.
> 4. **Snapshot reads (A3).** Each `Observe` — including each quiescence verdict — is evaluated against a single committed state.
> 5. **Per-run critical section for contiguous runs (W4).** A definition's multi-atom content run holds exclusion on its `(d, s_C)` for the run's duration; no foreign content allocation to `d` interleaves.
> 6. **Registry write confinement (W6).** Registry writes occur only in the construction of `Σ_init`; the runtime relation has no registry-write step.

Two clauses are conspicuous by what they *omit*. There is no global-serialization clause — G1 proved per-home suffices. And there is no registry-locking clause — W6 makes runtime registry writes nonexistent, so there is nothing to lock. The contract is genuinely minimal in this sense: removing any clause admits a counterexample (drop 1 and reads tear; drop 2 and same-home allocations collide; drop 3 and callers act on phantom effects; drop 4 and verdicts become accidental; drop 5 and definition runs fragment; drop 6 is vacuous to drop, since the model already forbids the writes).

The contract earns its name by the safety it implies:

> **M1 (SafetyUnderMIC).** Under MIC, (a) no reader observes a torn effect; (b) no *single operation's* effect is observed twice, and idempotent emission admits no duplicate — while non-idempotent emission admits content-equal tuples *by design*, which MIC neither prevents nor intends to; and (c) no writer collides with a concurrent writer's allocation.
>
> *Proof.* (a) *No torn effect.* Any single emission or nullification is one step; by clause 1 (A0) the reader's state is before or after it, never within (A4). A batch is not a single effect; its constituents are each whole, and clause 4 ensures each read is one canonical snapshot (A6) — fully structurally canonical, never corrupt (though, by §2, possibly mid-batch).
>
> (b) *No duplicated effect — scoped to what is actually proved.* Two facts hold, and a third must be stated plainly so the guarantee is not overclaimed. *(i) Per-operation uniqueness.* Each state-changing operation is realized at one unique index (A1), so *its* effect appears exactly once in the order; no single operation is double-applied. *(ii) Idempotent collapse.* Under `idem(K) = ⊤`, a semantic repeat — a second `Emit_K` with coverage-equal `(F, G)` — is a zero-step hit returning the incumbent address (ASN-0128 I1): it adjoins nothing to `A_K`, so it cannot duplicate. *(iii) But `idem(K) = ⊥` duplicates by design, and MIC does not prevent it.* Two `Emit_K` calls with identical `(F, G, K)` under `idem(K) = ⊥` produce *distinct* addresses, and *both* tuples appear in the active subset (ASN-0128 I5; ASN-0086 R2's consequence) — a reader observing `A_K` then sees two tuples of identical content. This is intended: a fresh non-idempotent emission is how the layer expresses a genuinely new instance, and no clause of MIC forbids it. In particular, commit-before-acknowledge (clause 3 / A7) does *not* suppress it: A7 fixes only that a response is produced at-or-after `lin(op)`; it neither detects nor cancels a *lost* acknowledgment, so a client that times out and retries a non-idempotent emission commits a second tuple, and A7 is indifferent to the fact. What collapses semantic repeats is idempotency (ii), not acknowledgment ordering. MIC's (b) guarantee is therefore exactly (i)+(ii). The reference-sharing principle — one permanent address, never a copy (ASN-0086) — governs *transclusion of content*, not two distinct link tuples that happen to carry equal endsets, and must not be invoked to claim more.
>
> (c) *No allocation collision.* Two allocations conflict only when into the same `(d, S)` (H1, H2); clause 2 serializes exactly those, so each reads a distinct frontier (H0) and deposits a fresh, unique address (W2); clause 5 extends this to whole runs (W4). Cross-home writers, by H1, never collide and need no coordination. ∎

We can phrase the allocation half as a weakest precondition, which is the most honest summary of clause 2. For an emission into `(d, S)` with the postcondition `R ≡` "the deposited address is fresh and unique and the `S`-prefix of `d` remains a gapless interval,"

`wp(emit into (d,S), R)  ≡  (no other emission into (d,S) is realized between this emission's frontier-read and its deposit).`

In the totally-ordered model the right-hand side is *automatically true* — there is no "between" two atomic steps to host an interloper. The content of MIC clause 2 is precisely that an implementation, which does not get the total order for free, must *establish* that right-hand side per home. And `wp` makes the scope unmistakable: the precondition quantifies over emissions into *this* `(d, S)` only. It says nothing about other homes — because, by H1, there is nothing to say. The reader who wants the one-sentence form of this entire note can take it from the `wp`: **the only thing a concurrent writer must wait for is another writer reaching into the very same sub-allocator; everything else is free.** That is Nelson's owned-numbers tree and Gregory's run-to-completion loop, reconciled — the loop is one way to guarantee the `wp`, and a coarse one; per-home exclusion is the least that suffices.

## What this note does not cover

- **The scheduler and its fairness.** *Which* agent's proposal is placed at *which* index — the placement that turns a crowd of proposals into the order `𝔼` — is the implementer's and protocol layer's concern. A termination layer may name fairness as a hypothesis; we name it only as the source of `𝔼` and reason about `𝔼` itself, not its construction. No fairness, starvation-freedom, or priority property is asserted here.
- **Agent activation and rule bodies.** What makes an agent fire, and what its firing computes, are opaque — a rule-governance layer leaves rule bodies opaque. We treat a fire only as a batch of operations with linearization points; its internals are not modelled.
- **Inter-server replication / BEBE.** The substrate here is one store. Nelson left the back-end-to-back-end protocol undefined in *Literary Machines* 87.1 ("computer networks are always broken"; each server "at all times unified and operational" but no global agreement). A multi-server consistency model — how per-home orders compose across servers — is a separate note. Our G1 is the natural seam for it (per-home independence is what would let homes live on different servers), but we do not develop it.
- **The concrete concurrency-control mechanism.** MIC is a contract, not an implementation. Whether clause 2 is met by a per-home mutex, an optimistic frontier-CAS with retry, a single global loop (Gregory's choice, which over-satisfies it), or an actor-per-home is unspecified. So is the performance of any of these.
- **Predicate evaluation cost.** The cost of evaluating a verdict's predicate — a predicate-evaluation layer's territory — is not bounded here; we constrain only *when* (one snapshot) it is evaluated, not *how expensively*.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| A0 | StepAtomicity — no state exists strictly between `Σ_i` and `Σ_{i+1}`; observable states are exactly the `Σ_k` | introduced |
| A1 | Realization — a state-changing op is one step at a unique index; an idem-hit / `Observe` / nullify-hit is zero steps | introduced |
| A2 | LinearizationPoint — `lin(op) = idx(σ)`; the op's entire effect is the single transition `Σ_{lin} → Σ_{lin+1}` | introduced |
| A3 | SnapshotRead — an `Observe` at index `k` is a total function of `Σ_k` alone | introduced |
| A4 | NoTornStep — no `Observe` witnesses a partial step; it sees an op's effect in full (`k ≥ lin+1`) or not at all (`k ≤ lin`) | introduced |
| A5 | NoBatchIsolation — a batch (fire) is many steps and is not atomic; if split, its partial effects are observable | introduced |
| A6 | CanonicalState — every state on `𝔼` is *fully* structurally canonical (the per-state invariant package of the `→_sh` stack); no boundary-only invariant class exists, so canonicity does not signal settledness | introduced |
| A7 | CommitBeforeAcknowledge — a response is produced only at or after `lin(op)` | introduced |
| H0 | FrontierDiscipline — `φ_S(d,·)` rises by one at each `S`-allocation to `d` and is framed by every other step | introduced |
| H1 | CrossHomeIndependence — allocations into distinct `(d,S)` commute (disjoint state) | introduced |
| H2 | SameHomeConflict — two allocations into the same `(d,S)` cannot read the same frontier without colliding | introduced |
| W0 | MonotonicityStepLocal — `C0`/`L12` (ASN-0093) are model-intrinsic (need only A0) | introduced |
| W1 | CrossHomeUniquenessStructural — cross-home/subspace address uniqueness is order-independent | introduced |
| W2 | SameHomeUniquenessSerial — same-`(d,S)` uniqueness holds iff per-home serialized | introduced |
| W3 | ChainContiguitySerial — dense chain contiguity is preserved exactly by per-home serialization | introduced |
| W4 | RunContiguityCritical — a definition's content run is contiguous iff `(d,s_C)` is held against foreign content allocation for the run's duration | introduced |
| W5 | ActiveSliceStepLocal — `A_K = L_K ∖ nullified` is coherent at every state under A0; `P-tgt` checked at the nullify's `lin` keeps it sound | introduced |
| W6 | RegistryRaceFree — registry is immutable at runtime (P1/R1); registry write-write races are vacuously absent | introduced |
| G0 | SequentialConsistency — the substrate realizes one total order of atomic steps; the order is logical (per-home arrival), not temporal | introduced |
| G-PO | PartialScheduleModel — a schedule is a partial order on allocation steps, per-`(d,S)`-comparable and cross-`(d,S)` free; `𝔼` is any linearization | introduced |
| G1 | PerHomeSerializabilitySuffices — every linearization of a per-home-serial schedule is invariant-preserving, and all linearizations are confluent (one committed state) | introduced |
| V0 | VerdictSnapshotLocal — a single-`Observe` verdict is sound about its read index `r` and only about it; `Σ_r` is always a canonical referent | introduced |
| V1 | VerdictRetrospective — a verdict is non-durable; durability needs the added hypothesis that no falsifying step linearizes in `[r, r')` (a layer obligation) | introduced |
| MIC | MinimalIsolationContract — the six-clause discipline a faithful realization must honour | introduced |
| M1 | SafetyUnderMIC — under MIC: no torn read; no single operation double-applied (`idem=⊤` admits no duplicate, `idem=⊥` content-duplicates by design); no same-home allocation collision | introduced |

## Open Questions

What is the weakest exclusion primitive that realizes MIC clause 2 — does an optimistic frontier read-and-retry satisfy it without any held lock, and under what condition does retry terminate?

What must an implementation guarantee so that a reader landing inside a split batch is not misled into treating a mid-batch state as settled — since canonicity (A6) cannot itself distinguish the two, must every batch needing all-or-nothing visibility run inside a critical section, or can it instead publish a snapshot-readable completion marker?

When a layer genuinely needs batch atomicity (a definition's content run seen whole, a retraction set applied all-or-nothing), what is the minimal additional contract that makes a multi-step batch appear atomic without reintroducing global serialization?

What relationship between an observer's read index and writers' linearization points must a coordination layer establish to promote a sound quiescence verdict into a durable one, and is that relationship expressible as a substrate-checkable predicate rather than an external assumption?

Does the equivalence of per-home and global serialization (G1) survive across servers, so that homes resident on different servers may progress with no inter-server coordination, and what is the weakest cross-server contract that preserves cross-home uniqueness when home ownership can migrate?

Under what conditions may two allocations the model treats as same-home conflicts be proven independent after all — for instance, if a home's sub-allocator is statically partitioned among agents — thereby weakening MIC clause 2 below per-home exclusion?

What is the soundness obligation on an out-of-order retraction whose target has not yet been emitted at its linearization state — is silent rejection the right semantics, or must the substrate expose the rejection so a coordination layer can re-order rather than lose the intent?
