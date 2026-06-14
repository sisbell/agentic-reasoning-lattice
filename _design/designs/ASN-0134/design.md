## What this is

ASN-0134 defines the **consistency and isolation model** of the substrate: the contract between the substrate's sequential semantics (a single total order of atomic steps) and the concurrent clients raised on top of it. It is not a mechanism — no lock, transaction manager, or scheduler — but the specification (the *Minimal Isolation Contract*, MIC) that any concurrency-control mechanism must honor so the sequential meaning is faithfully presented to a crowd.

## Design commitments

These are locked in for everything built above this layer.

- **The step is the atom — and *only* the step.** A single operation realizes as exactly one atomic state transition whose *entire* effect is that one transition (A0/A1/A2). Downstream may not assume any sub-step is visible, and — crucially — may not assume any *larger* unit is atomic. A multi-step batch (a content run, a `retract_stale`) is **not** atomic (A5): all-or-nothing stops at the single step. *Forced.*
- **Execution is a single total order, serializable but not sequentially consistent (G0).** There is one logical order `𝔼`; it preserves no agent's program order, and it carries no wall-clock — order is *per-home arrival sequencing*, not a global timeline. Two cross-home operations of one agent may be reordered; an agent that needs its own ordered must self-serialize via acknowledgments. *Forced.*
- **Contention is per sub-allocator `(home, subspace)`; everything else commutes (H1/G1).** This is the load-bearing liberation. Cross-home and cross-subspace operations are independent and need *zero* coordination. The one-sentence form of the whole note: **the only thing a concurrent writer must wait for is another writer reaching into the very same sub-allocator.** *Forced (it is a theorem, not a convention).*
- **Canonical ≠ settled (A6).** Every observable state is *fully* structurally canonical — there is no "mid-batch" marker anywhere in a state. Incompleteness is a *relation* between a state and a batch spanning it, invisible from inside the snapshot. A reader is never *corrupted*, but canonicity does not certify *final*. *Forced.*
- **Permanence is operation-intrinsic, not order-dependent (W0).** Append-only, no overwrite, no key removal — true under *any* interleaving because of the shape of the operations, not because of a discipline. Nelson's point, and it survives concurrency for free. *Forced.*
- **Reads are snapshots; verdicts are retrospective (A3/V0/V1).** A read is a total function of one committed state. Soundness is about that one index and nothing later; **durability is not a substrate guarantee** and must never be read off a snapshot. *Forced.*
- **Two disciplines are genuinely *not* per-home and must be honored separately.** Reader-side multi-read verdict pinning (clause 7) and idempotent (`idem=⊤`) de-duplication (clause 8). The per-home thesis is a *writer-side* result; these two carve-outs are reader- and operation-level and span all homes. *Forced — these are the note's sharpest corrections.*
- **The type/shape/idem registry is immutable at runtime (W6); home registration grows monotonically (M1).** *Forced.*

Merely *conventional* (the contract's choices, not theorems): MIC clause 7 adopts "all reads at one index" though a weaker condition suffices — chosen for constructibility, not necessity; clause 6 is kept though not load-bearing, so the contract names every obligation a builder might fear.

## What must be built

Described functionally — what each must *do*.

- **A step applier + publisher.** Apply one step indivisibly and make it the next committed state in the order; expose to each reader *exactly one* committed state, never an intermediate.
- **A per-`(home, subspace)` allocation serializer.** Make the frontier-read-and-deposit of two same-`(d,S)` allocations mutually exclusive; leave cross-`(d,S)` uncoordinated. (Document registration `K.σ` is *not* a sub-allocator emission — out of scope here; freshness of fresh `d` is an assumed upstream precondition, see *How it fits*.)
- **A frontier oracle.** Given `(home, subspace)` and a state, yield the next deposit slot and the current population count. Recoverable by construction; a candidate for caching.
- **An emission path with idempotent de-duplication.** For `idem=⊤` types, consult the *global* active set by coverage class and either return the incumbent (hit, zero steps) or deposit (miss) — as **one atomic action** per coverage class.
- **A nullification path.** Check the target precondition at the nullify's *own* linearization state; record the retraction (growing `nullified`); reject out-of-order retractions cleanly rather than dangling.
- **A read surface.** Per-type active-view reads; the home-relative age/frontier read (one bounded access); and — separately — a way to take a *multi-read verdict against one committed state*.
- **A contiguous-run mechanism** (only if a consumer needs consecutive addresses): hold a sub-allocator against foreign same-subspace writes for a run's duration.
- **An acknowledgment path** that fires only at or after the committing step.
- **Recovery.** Rebuild all derived state from the authoritative record.

## Implementation approaches

**1 — Applying and publishing a step; free snapshot reads (clauses 1, 4; the foundation).**

Treat `𝔼` as what it literally is: a **journal**. The authoritative record is an append-only log of step records (`K.σ`, `K.α`, `K.λ_sh`) — exactly this repo's `links.jsonl` mechanism, with home registration recovered by replay the way `paths.json` is. One append = one atomic step, which *is* clause 1, and append-only *is* W0 (monotonicity, no overwrite) by construction. Recovery is a fold/replay. This is plain write-ahead-logging discipline and I would not deviate from it: the journal is the source of truth, everything else is a hint over it.

For the *current* state, hold it as a **single immutable, structurally-shared value** (the `im` crate's whole purpose). A step builds Σ′ from Σ sharing structure, and you publish by an atomic root-pointer swap (RCU-style). A reader loads the root once and gets a free, tear-proof snapshot (A3/clause 4). This route makes the rare case correct *and* the common case fast.

The decisive payoff is **clause 7**. The note frames the multi-read verdict as needing a *global* reader-side critical section — but that cost is an artifact of a per-type read API that re-reads live state between calls. **Hand the reader a snapshot handle (a captured immutable root) and run all `p` constituent reads against it; clause 7 collapses into clause 4 and costs nothing.** This is the single biggest Lampson win in the design: the "global" expense was misplaced in the API, not inherent in the contract.

Weigh against udanax-green: Green holds *mutable* in-memory enfilades and gets snapshot isolation by being single-threaded run-to-completion — no concurrent observer can witness a mid-mutation state because no concurrent observer runs at all (verified). That is cheaper (no structural-sharing overhead) but caps you at one reader-at-a-time. Pick Green's route if a single thread's throughput suffices; pick persistent-structure + atomic publish when you want real read concurrency, which is this corpus's stated target.

One durability decision rides here. If "commit" = journal append, then commit-before-ack (A7) *also* gives durable-before-ack. Green decouples these — visible at mutation time, durable only at a checkpoint (`writeenfilades` at shutdown/quiescence), so a crash loses in-RAM mutations and there is no startup validation. I would couple append-and-commit; the decoupling is precisely the rare-case-incorrect that the journal exists to avoid.

**2 — Per-home allocation serialization (clause 2).**

The frontier is the contended resource, and there is a clean spectrum:

- *Single global writer* (fold the journal on one thread). Trivially serializes everything, over-satisfies the contract — this is Green's loop. Simplest and bulletproof; bounded by one writer's throughput. **Start here.**
- *Per-home owner (lock or actor-per-home).* Route every `(d,S)` op to one owner; distinct homes run in parallel. This is exactly what G1 licenses. Costs a home→owner routing map and message passing. Reach for it only when the single writer is the *proven* bottleneck.
- *Optimistic frontier-CAS with retry.* Read the frontier hint, compute the slot, append-if-unchanged, retry on conflict (the note's Open Question). No held lock; excellent when same-home contention is rare; retry termination needs a bound.

The note's weakest-precondition statement is the precise contract for whichever you pick: *no other emission into this `(d,S)` is realized between this emission's frontier-read and its deposit* — and it quantifies over *this* `(d,S)` only.

Frontier representation is itself a hint decision. Green stores **no** next-counter; it recomputes by bounded tree descent (`findpreviousisagr` + 1), while maintaining an aggregate *total* width at the enfilade apex readable in one access — but that aggregate is total, so the *type-under-home* frontier still costs an O(log n) descent. For this build I would cache per-`(home, subspace)` population counts as a **hint over the journal**, rebuilt by replay on a miss — authoritative state is the chain, the count is recomputable cache. Dense contiguity, note well, is a *serialization artifact* (W3, and Green confirms a concurrent allocator keeps uniqueness and monotonicity but *loses* contiguity); so the count-hint is only valid under clause 2's serialization, which is fine because that is exactly when contiguity is promised.

**3 — Idempotent de-duplication (clause 8) — your one non-per-home writer obligation.**

If you have `idem=⊤` types at all, build a **coverage-class-keyed dedup index** (a content-addressed map from coverage class → active address) and make *get-or-insert atomic per class* (compute-if-absent). The atomicity of check-and-insert *is* the clause; keying by coverage class keeps it fine-grained — you serialize within a class, not globally across classes. Note the index tracks the *active* slice, not the audit slice: a nullified incumbent must make the next coverage-equal emit a *miss* (deliberate resurrection), so drop the entry on nullify or derive the index from `A_K = L_K ∖ nullified`.

The honest framing for the builder: a single writer dissolves clause 8 (no race). It only bites once you take per-home concurrency *and* have idempotent types. So the first real question is **do you need `idem=⊤` types?** If the layer above never asserts "the same edge, idempotently," drop the index and the clause with it.

**4 — Multi-read verdicts / quiescence (clause 7).**

Root-capture (approach 1) makes this free; take it. Avoid a global reader lock (coarse, defeats the per-home liberation). If you are *forced* into mutable state, the root pointer is the natural version coordinate for an optimistic read-then-revalidate loop (Open Question 2). I would not try to exploit the weaker "no Q-affecting step between reads" condition — classifying which steps affect a verdict is more code than just pinning to one snapshot.

**5 — Contiguous runs (clause 5).**

Only pay for this if a consumer genuinely needs *consecutive* addresses (addressing-by-origin alone does not). If it does, hold the per-home content serializer across the whole run — and there is no cheaper realization of clause 5. **Pre-reserving a block of `m` frontier slots does *not* shorten the exclusive window.** The frontier *is* the population count (H0: `φ_S = |P_S|`), and contiguity (W3) requires the populated slots to be a *gapless* prefix; so if you reserve `[φ, φ+m)` but let a foreign same-`(d,s_C)` writer advance — the one writer that can threaten the run — it either collides on slot `φ` (the count hasn't moved) or, if your serializer skips it to `φ+m`, leaves `φ..φ+m−1` empty while `φ+m` is filled: a gap, i.e. a non-canonical state (violates W3 *and* A6). The only gap-free option is to keep that writer out for the whole run — which *is* holding the lock. Pre-reservation can still save the `m−1` redundant frontier reads (a per-step-overhead win, easy given the frontier hint), but the exclusion span cannot drop below the run's duration; shrinking *that* would require batch read-atomicity, strictly stronger than clause 5 and explicitly Open Question 5. Remember the scope is razor-thin — only same-subspace, same-home writes threaten a run; link allocations and other homes cannot (the abstract subspace partition). Green *fused* the subspaces, so a link allocation there *does* fragment a text run; honoring the partition avoids that coarser obligation.

**6 — Nullification and the active/audit slice (W5).**

Derive `active = audit ∖ nullified`; don't keep a second authoritative copy (cache the active view as a hint if reads are hot). Check the target precondition at the nullify's own linearization state. The precondition is a *disjunction* — `P-tgt = a ∈ A_rel^Σ ∨ a = a_emit(Σ, d_retr)` — so the rejection rule is "target absent **and** not the retractor's own next emit slot → reject," not "absent → reject." A nullify of the retractor's own frontier slot (absent from the store yet equal to `a_emit`) *fires*, depositing its R-tuple on that slot and self-nullifying (W5 case 2); only a target that is both absent and not that slot is rejected. A genuine out-of-order retraction (absent target, not self-emit) is *rejected cleanly* (record nothing), never left dangling — and I would **surface the rejection** so the coordination layer can re-order rather than silently lose the intent (Open Question 9).

## Guarantees to uphold

**Hold by construction** (given the journal + immutable-publish or single-thread):
- No torn read (A4) — clause 1 plus atomic publish.
- Permanence: append-only, no overwrite, no removal (W0) — operation shape, any interleaving.
- Cross-home / cross-subspace uniqueness (W1) — distinct origins, order-independent.
- Active = audit ∖ nullified, always coherent (W5).
- Registry stability (W6); per-call snapshot (A3); every observable state fully canonical (A6) — but *on a valid `𝔼`*: A6's chain-contiguity conjuncts (ChainMembershipForOrigin / L-ContiguousPrefix) are exactly W3, *serialization-borne*, holding only because clause 2 produces a gapless `𝔼` under per-home concurrency; only A6's *non*-contiguity conjuncts hold from A0 (the atomic step) alone.

**Require active enforcement:**
- Same-home uniqueness and dense chain contiguity (W2/W3) — clause 2 per-home serialization.
- Run contiguity (W4) — clause 5, *if* needed.
- Commit-before-acknowledge (A7) — clause 3. (Green's response-before-check for INSERT/DELETEVSPAN/REARRANGE is exactly the bug to avoid.)
- Multi-read verdict soundness (V2) — clause 7; *free* under root-capture, else enforced.
- Idempotent uniqueness (`idem=⊤`) — clause 8; the one non-per-home writer discipline.

**Explicitly given up (state these to consumers):** sequential consistency / program order; batch atomicity (A5); verdict *durability* (V1); de-duplication of `idem=⊥` emissions (content-equal tuples are by design). A7 orders responses but does *not* cancel a lost-then-retried non-idempotent emission. And even under clause 8, an `idem=⊤` emit's *outcome* stays order-dependent: a lone idempotent emit racing a `Nullify` of its coverage-equal active incumbent reaches different committed states (`∅` vs `{A'}`) by order — reduced by *neither* clause 8 (which governs racing *emits*; this race has only one emit) *nor* emit-before-retract (vacuous, since the incumbent is already emitted). Clause 8 suppresses only the *duplicate* of two racing emits; this which-survivor / present-vs-absent non-confluence is benign for uniqueness but persists, so consumers must not over-rely on idempotent determinism.

## How it fits

This is a thin **contract layer sitting directly on the allocation substrate**, below all coordination. It leans on: ASN-0093 (sub-allocators, frontiers, chains, the SequentialTransitionAxiom, the per-state/transition invariant package), ASN-0086 (`Observe`, the active/audit slice, the link store), ASN-0126 (registry, shape, frontier unification), ASN-0128 (the gated relation, `Emit`/`Nullify`/`Observe`, `idem`, the behavioral reads). It hands the *snapshot* up to the predicate-evaluation, quiescence, and termination layers (V0/V1/V2). It deliberately excludes — and names as someone else's job — the scheduler and fairness (the source of `𝔼`), the coordination layer's emit-before-retract and extinction disciplines, rule bodies, inter-server replication, and **document registration** (`K.σ`): MIC has *no* registration clause, because document-address freshness — distinct agents proposing distinct fresh `d` — is an *assumed upstream precondition* supplied by the excluded entity-allocation layer, not an obligation this contract undertakes. A same-`d` registration race is therefore resolved not by a frontier-style serializer (there is no document frontier to advance) but by *cleanly rejecting the loser*, structurally like the out-of-order-nullify rejection — so a builder should neither serialize registration as an allocation nor mishandle the collision. **G1 is the explicit seam for replication:** per-home independence is exactly what would let homes live on different servers with no inter-server coordination.

## Decisions for the builder

- **Single logical writer vs. per-home concurrent writers** — the master fork. G1 *proves* the concurrent version sound, but does not say to build it. Start single-writer (everything is free); move to per-home owners only against a measured bottleneck.
- **Where authority lives** — journal-as-truth with in-memory state as a recomputable fold (recommended) vs. in-memory-as-truth with periodic checkpoint (Green; weaker recovery).
- **State representation** — immutable/persistent + atomic publish (makes clauses 4 and 7 free for many readers) vs. mutable + single-thread (Green; cheaper, one reader at a time).
- **Frontier** — cached count-as-hint vs. recompute-by-descent vs. maintained aggregate; and at what granularity (the abstract model wants per-subspace).
- **Clause-2 primitive** — per-home lock, actor-per-home, or optimistic frontier-CAS with a retry bound.
- **Do you have `idem=⊤` types at all?** — decides whether clause 8 and its dedup index exist; if so, pick the index representation and its atomic get-or-insert.
- **Do you need contiguity?** — decides whether clause 5 exists; if so, hold-the-lock vs. pre-reserve-a-block.
- **Durability coupling** — append-before-ack (durable) vs. visible-then-checkpoint (Green's crash-loses-data behavior).
- **Read API shape** — expose a whole-state snapshot handle (root capture) vs. per-type reads only; this single choice determines whether clause 7 is free or global.
- **Out-of-order retraction** — silent rejection vs. surfaced rejection (recommend surfacing).
