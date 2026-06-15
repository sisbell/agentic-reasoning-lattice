## What this is

ASN-0134 defines the substrate's **consistency and isolation model**: the contract — the Minimal Isolation Contract (MIC) — that bridges the spec's sequential, totally-ordered, atomic-step semantics to the concurrent clients that actually use it. It adds no mechanism (no lock, transaction, or scheduler); it states the *weakest* discipline an implementation must honor so the singular sequential definition is faithfully presented to a plural world, and it pins exactly where that discipline must be **per-home** versus **global**.

## Design commitments

**Forced — downstream design cannot violate these:**

- **The step is the atom; the total order is the *meaning*, not the implementation.** Each state-changing operation has exactly one linearization point, and its entire effect is one indivisible transition — never half-applied, never dribbled across states. An implementation may *produce* the order however it likes but must *present* this.
- **The unit of contention is the `(home, subspace)` sub-allocator — not the store, not the document.** Conflicts exist only within one `(d, S)`; everything across homes, and across a home's content/link subspaces, commutes (H1). This is the spine of the whole note.
- **Per-home serialization suffices; global serialization over-satisfies.** Every interleaving of a per-home-serial schedule reaches the same committed state and preserves every invariant (G1). Design may not assume global ordering is *required*.
- **Reads see only committed state; the snapshot is the only honest referent.** No observation witnesses a partial step (A4). A verdict is a statement about one committed state and nothing later (V1).
- **Batches are not atomic** (A5). All-or-nothing stops at the single step; every multi-step batch's interior states exist and carry a strict prefix of its effects, but whether a reader *witnesses* that partial turns on subspace. A *link-store* batch (a `retract_stale`) is read-observable partially — an `Observe_K` returns some events retracted and others not; a *content* run is non-atomic only *structurally* — its mid-batch state exists and is canonical, but no read the note models witnesses its prefix. Batch atomicity must be built *above* the substrate.
- **Canonical ≠ settled** (A6). Every reachable state, including a mid-batch one, satisfies every per-state invariant; there is no "incomplete" marker. Incompleteness is a relation between a state and a spanning batch, invisible from inside the snapshot.
- **Content is immutable and append-only; a step only changes which addresses are *present*.** This is *why* torn reads are impossible.
- **Commit before acknowledge** (A7). A response must not precede its committing step. (The udanax reference violates this — response-before-check for INSERT/DELETEVSPAN/REARRANGE — and the note flags it as a defect, not a model.)
- **The order is logical, not temporal** (G0): per-home arrival order, no global clock. The substrate presents *serializability*, not sequential consistency, and only real-time-precedence-only linearizability under A7. The level is *client-model-dependent*: a *pipelining* client (operations in flight before prior acknowledgments return) gets only serializability; a *sequential* client recovers SC by its own acknowledgment discipline — issuing each operation after the prior's response — not by any substrate promise.
- **Two obligations are genuinely global; one exceeds per-step granularity but stays per-home.** Contiguous runs (clause 5) need a per-run critical section — wider than per-step, yet still per-`(home, subspace)` in scope, strictly weaker than any cross-home exclusion. Multi-read verdicts (clause 6, a *global* reader snapshot) and `idem=⊤` de-duplication (clause 7, a *global*, per-coverage-class serialization of dedup-read-and-deposit) are the two that genuinely *exceed* per-home discipline.

**Conventional — fixed by the realization, not the spec:**

- Whether document registration contends *at all*: a shared per-account frontier makes same-account creations collide (account-tier clause 2); a collision-free fresh-address scheme incurs no such obligation.
- Whether a link allocation can fragment a content run: it can iff the two subspaces share one allocator (fused, as in the reference) rather than being disjoint.

## What must be built

- A **sequencer/linearizer** realizing each state-changing operation as exactly one atomic step at a unique index, with a single linearization point.
- **Per-`(home, subspace)` mutual exclusion** over the frontier-read-and-deposit of allocations (same-home uniqueness).
- A **register-before-allocate ordering**: an allocation into a document `d` (a `K.α`/`K.λ_sh`) must be sequenced after `d`'s registration (`K.σ`). This `≺`-ordering binds *every* realization unconditionally — it is the one obligation attaching to `K.σ` independent of the shared-frontier conditional (which decides only whether `K.σ` *itself* contends), a genuine dependency rather than a freshness artifact.
- A **frontier discipline**: each allocation reads the home's current sub-allocator frontier and deposits at it — the frontier *recoverable from the store*, not necessarily stored.
- **Snapshot reads**: each bounded access pinned to one committed state.
- **Commit-before-acknowledge** ordering in the request/response path.
- A **per-run critical section** for multi-atom content runs (contiguity).
- A **global reader snapshot** for multi-read verdicts / quiescence predicates (all constituent reads at one committed index).
- A **per-coverage-class serialization** of the `idem=⊤` dedup-read-and-deposit.
- A **clean rejection path** for precondition-failed / out-of-order operations (no dangling state).
- A **recovery mechanism** reconstructing the canonical state from the journal of committed steps. *(Not a MIC obligation: ASN-0134 is silent on durability and a purely in-memory realization honors all of MIC. This is a cross-cutting builder concern, motivated by the reference's weak durability and licensed by A6.)*

## Implementation approaches

**The organizing insight first.** A single run-to-completion loop satisfies all seven MIC clauses *for free* — it *is* a global serialization — once each logical operation (a run included) maps to one dispatch, with *two* exceptions you must handle by hand. First, commit-before-acknowledge, which you must order correctly. Second, clause 6: the substrate exposes no whole-state read — only the per-type `Observe_K` (§8) — so a multi-read verdict is "one dispatch" only if the handler bundles all its constituent reads into a single compound access. A recognizer that instead issues them as separate requests drifts across indices *even under the single loop* (the §8 pathology needs no per-home concurrency at all), so clause 6's real cost lives in that compound-read construction, not solely the per-home transition below. The reason to abandon the single loop is throughput. The moment you move to the per-home concurrency G1 blesses, the free ride ends for clauses 2, 4, 5, 6, and 7: **per-home serialization** (clause 2, the defining move), **per-run contiguity** (clause 5, local), **snapshot reads at both access counts** (clauses 4 and 6 — one obligation: a single bounded access [clause 4] and a multi-read verdict [clause 6, global] each must land on one committed state, since even a lone `Observe_K`'s sub-reads over `L_K` and the global `nullified` slice can straddle a cross-home commit), and **`idem=⊤` dedup** (clause 7, global). Clauses 1 and 3 you then maintain by discipline. Everything below follows that fault line.

**Sequencing.**
- *Single loop* — simplest, proven. The udanax reference is exactly this: one request runs to completion, the in-memory enfilade *is* the shared canonical state, a write becomes visible at dispatch completion. Bounded by one core; a slow client can stall it. Pick this first — it is the simplest thing that honors the spec.
- *Per-home actors / single-writer-per-home* — cross-home work runs concurrently, matching G1's confluence. More machinery; must enforce register-before-allocate for `K.σ` and add the global clauses 6/7.
- *Optimistic frontier-CAS with retry* — no held lock: read frontier, compute deposit, install if frontier unchanged, else retry. Wins when same-home contention is rare; retry termination is the open question (OQ1).

**State representation & snapshots — the biggest lever.**
- *Persistent (structurally-shared) immutable state* (a persistent immutable-collection library): the shared canonical state is an immutable root; a write produces a new root, structurally shared. This makes A0/A4 (no torn read), clause 4 (per-call snapshot), and clause 6 (per-verdict snapshot) nearly free — a reader captures one root and reads everything off it, with no lock held against writers. The root's identity *is* the version coordinate the substrate otherwise lacks (a design inference, but a clean answer to OQ2). Strongly recommended. **The win is read-side only**, though: concurrent per-home *writers* sharing one root still contend on root installation, so persistent state alone does not deliver the write concurrency G1 blesses — that comes from the sequencing mechanism (per-home actors with per-home roots plus a merge, or a single applier). Do not pair persistent state with per-home actors and expect free concurrent writes.
- *Mutable store + locks*: needs explicit reader exclusion or a version stamp for snapshots; against the grain.

**The frontier as derived state.**
- The frontier is recomputable from the store, so keep no authoritative duplicate of it. Recompute by query-and-increment against the live store — `max+1` under the home's prefix, the reference recovering the equivalent by a bounded descent. This is derived-*exact* — always correct by construction, never stale — so there is no cache to invalidate and no recovery problem.
- Optionally maintain an aggregate frontier at the home node, but be clear which kind. An *eagerly-maintained authoritative-derived* aggregate — propagated on every deposit, so always exact and never stale — buys O(1) reads at the cost of the maintenance write on every allocation. The reference demonstrates the technique, though at coarser granularity: an O(1) width aggregate at the enfilade *apex*, whole-store rather than per-type, maintained after each insert, with the per-`(home,subspace)` frontier recovered by bounded descent. A *Lampson hint* — a value *retained* across calls, possibly stale, verified against the store on use and recomputed when wrong — is a different thing and buys little for a frontier: the coupled allocator needs the exact maximum at deposit time, and verifying a retained value against the population costs about as much as recomputing it fresh. (This is *not* the optimistic frontier-CAS recommended under Sequencing: that reads the frontier *fresh* each attempt and CAS-detects concurrent change, retaining nothing across attempts.) Add the eager aggregate only if allocation latency demands it.
- **Load-bearing:** use the *population-coupled* `inc(max,·)` allocator. It makes chain contiguity model-intrinsic — gapless under *any* interleaving. A counter-style allocator that hands out increasing indices without consulting the population preserves uniqueness and monotonicity but *loses contiguity* whenever allocations interleave (confirmed against the reference). Pick the coupled allocator.

**Journal & recovery** *(a cross-cutting builder concern, not a MIC clause — ASN-0134 reasons only about the abstract sequence `𝔼` and is silent on durability; a purely in-memory realization satisfies all of MIC).*
- The total order is an append-only journal of steps — Lampson's log for atomicity and recovery (an append-only step journal + replay). Recovery = replay; every prefix is a canonical reachable state (A6), so no separate consistency check is needed *provided each step is journaled atomically*.
- Caution from the reference: each abstract step touches *one* store, but a builder who maintains a *derived index* (the reference's spanfilade) alongside the authoritative store turns one logical step into two physical writes, and a crash *between* them diverges the index from the store — the reference has no startup validation to catch it. Honor per-step atomicity across whatever derived-index layout you choose by writing one journal record per step and replaying it as a unit (WAL discipline). A6/W3 assume this atomicity; delivering it across an authoritative store plus its derived indexes is the builder's job.

**Contiguous runs (clause 5) — writer-side only.**
- Clause 5 buys the writer-side half of run-atomicity and no more: a perfectly contiguous run still *passes through* every interior state, each canonical (A6) yet carrying a strict prefix of the run's atoms (A5/W2). For a *content* run specifically, that partial is structural and witnessed by no read the note models (§8's read surface is link-only), so the reader hazard is forward-looking — it bites only a future read surface that *would* witness content population, which could then land mid-run on a valid-looking partial state. Making the run appear all-or-nothing *to a reader* is the separate, harder contract of OQ4, above the substrate.
- The clause-5 mechanism is to hold a per-`(d, s_C)` critical section for the run's duration; readers may still land mid-run (clause 5 excludes only foreign writers). Keep content and link subspaces on *disjoint* allocators so a link emit cannot fragment a content run (the tight exclusion scope); fusing them, as the reference does, inherits a coarser whole-home exclusion.
- A stronger option *over-satisfies* clause 5 and must not be mistaken for a cheaper substitute: reserve `m` consecutive slots and fill them as *one indivisible m-step*. Because the frontier *is* the population (`φ_S = |P_S|`), advancing it by `m` *means* depositing `m` addresses, so the only sound realization commits all `m` together — which is exactly the run-atomic-to-readers contract of OQ4 (no reader observes the interval until it is full), strictly stronger than clause 5, not cheaper. A non-atomic fill that leaves reserved-but-empty slots produces states not on `𝔼`, contradicting A0/A6 — so there is no middle "reserve cheaply, fill lazily" path here.

**Multi-read verdicts / quiescence (clause 6).**
- With persistent state: capture one root, read all `p` constituents off it — no writer exclusion at all. This dissolves the "global" cost.
- With a mutable store: optimistic read-then-revalidate against a version stamp, or a held global reader lock (correct but expensive).
- Either way respect V1: a verdict is *retrospective*. Never let a quiescence layer read "quiescent now" as "quiescent and will stay so" — durability is a separate coordination-layer hypothesis.

**`idem=⊤` de-duplication (clause 7) — the one genuinely global, operation-level obligation.**
- Maintain a coverage-class index over the active set (a hint, recomputable) so the dedup-read is cheap, and serialize check-and-deposit *per coverage class* (lock striping by class) rather than globally. Optimistic check-and-deposit with retry is viable if `idem=⊤` emits are rare (OQ3).
- Under the single loop this is free; under per-home concurrency it is the price of correctness for `idem=⊤` types *specifically* — two cross-home emits can otherwise both miss against a snapshot neither sees the other in, and both deposit a duplicate. Persistent state does *not* solve this (the snapshots are individually consistent yet mutually stale); only serializing the check-and-deposit does.
- Scope it tightly: clause 7 binds only `idem=⊤` types. `idem=⊥` emits duplicate *by design* — do not suppress. And commit-before-ack does not dedup a lost-acknowledgment retry of an `idem=⊥` emit; that needs client-supplied idempotency keys, not a substrate clause.

**Rejection path.**
- An out-of-order retraction whose target isn't yet present must reject cleanly (no dangling retraction). The reference silently skips and — worse — has already sent success (the response-before-check gap). Prefer a *surfaced* typed rejection so a coordination layer can re-order or retry rather than lose intent and mislead the caller (OQ8).

## Guarantees to uphold

**By construction:**
- Content permanence/immutability; append-only stores.
- Cross-home and cross-subspace address uniqueness, order-independent — by two distinct mechanisms: cross-home (`d ≠ d'`) by distinct origins; cross-subspace (same `d`, shared origin) by the subspace-digit divergence of the sibling anchors `[d.0.s_C]`/`[d.0.s_L]` (DisjointSubAllocatorChains / T10), since origin cannot separate the chains.
- Chain contiguity / no holes — *given the population-coupled allocator*.
- Registry stability (immutable at runtime; the write-write race is vacuously absent).
- No torn read — *given snapshot reads*; near-automatic with persistent state.

**By active enforcement:**
- Same-home uniqueness (per-home serialization, clause 2) — else a collision, with one allocation rejected.
- Per-operation exactly-once effect (sequencer + commit-before-ack).
- `idem=⊤` no-duplicate (clause 7, global) — per-home discipline alone permits a duplicate. *But clause 7 buys no-duplicate, not a unique outcome:* a lone `idem=⊤` emit racing a nullify of its coverage-equal incumbent (§4 instance (ii)) still resolves order-dependently (`∅` vs `{A'}`, one step vs two); MIC delivers serializability, not outcome-determinism, and this emit-vs-nullify instability is inherent, not a duplicate.
- Multi-read verdict soundness (clause 6, one-index reads).
- Run contiguity (clause 5, per-run exclusion).

**Explicitly *not* a substrate guarantee:**
- Verdict durability (retrospective only; needs a coordination-layer hypothesis).
- `idem=⊥` duplicate suppression (duplicates are by design).
- Any temporal / sequential-consistency promise (serializability only; the order is logical). SC is *recoverable by a sequential client* via its own ack-before-next discipline — at the client/coordination layer, not the substrate.

## How it fits

**Leans on:**
- **ASN-0093 (Allocation Substrate)** — the sub-allocators, frontier discipline, `inc(max,·)`, and the SequentialTransitionAxiom. H0/H1/H2 are read directly off it.
- **ASN-0128 (Substrate Type Operational Semantics)** — the step vocabulary (`K.σ`, `K.α`, `K.λ_sh`), `Emit`/`Nullify`/`Observe`, `idem`, the gate, and the I1a surface-emit induction (clause 7 repairs its concurrent reading).
- **ASN-0126 (Substrate Shape Framework)** — registry fixity, shape conformance, `FrontierUnification`.
- **ASN-0086 (Typed Relations)** — `Observe_K` and the active subset `A_K = L_K ∖ nullified`.
- **ASN-0047 (Transition Model)** — the account's document sub-allocator `A_doc`, for the shared-frontier conditional on `K.σ`.

**Hands to / sits beneath:**
- The **scheduler/protocol layer** (places proposals into the order — out of scope here).
- The **coordination layer** (fairness, extinction discipline, and the durability hypothesis that promotes a sound verdict to a durable one).
- The **termination/quiescence layer** (consumes the snapshot verdict).
- The **rule-governance layer** (agent activation, rule bodies — opaque here).
- A future **multi-server/BEBE layer**: G1's per-home independence is the natural seam — homes that never contend could live on different servers — but cross-server uniqueness under home migration is unaddressed (OQ6).

## Decisions for the builder

1. **Sequencing mechanism** — single loop vs per-home actors vs optimistic CAS. (Explicitly out of scope in the note.)
2. **State representation** — persistent/immutable (makes clauses 1/4/6 near-free) vs mutable + locks. Recommend persistent.
3. **Frontier** — recompute as derived-exact vs maintain an eager aggregate. Recommend recompute first.
4. **Allocator family** — population-coupled `inc(max,·)` (free contiguity) vs counter (loses it). Pick coupled.
5. **Subspace layout** — disjoint content/link allocators (tight run-exclusion) vs fused (coarse). Pick disjoint.
6. **Document-registration realization** — shared per-account frontier (incurs account-tier clause 2) vs collision-free fresh addresses (no same-account contention). This single choice decides whether `K.σ` contends at all.
7. **Run allocation** — hold a critical section across `m` deposits (clause 5, readers may land mid-run) vs reserve `m` slots and fill as one indivisible m-step (OQ4, run atomic to readers — over-satisfies clause 5).
8. **`idem=⊤` dedup** — per-coverage-class index + striped serialization vs scan `A_K` vs optimistic retry.
9. **Rejection semantics** — silent skip vs surfaced typed rejection. Recommend surfaced.
10. **Multi-store atomicity** — one journal record per step (WAL) vs independent store-plus-derived-index writes; the latter risks crash divergence with no startup validation.
11. **Same-home partition (optional)** — statically partition a home's sub-allocator among agents, proving independent some allocations the model treats as same-home conflicts and weakening clause 2 below per-home exclusion (OQ7), vs plain per-home serialization. Default to the latter; reach for partition only under measured same-home contention.
