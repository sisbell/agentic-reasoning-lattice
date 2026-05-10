# Stigmergic Coordination

How the protocol stack handles agents with overlapping write resources.

## The principle

Stigmergic coordination — the substrate-mediated pattern this system runs on — uses pheromones as its primary signaling mechanism. In the biological precedent ([Grassé 1959](#references); also [Theraulaz & Bonabeau 1999](#references)), termites coordinate mound construction through pheromone fields deposited in the environment. Other termites read the field and decide locally what to do. No central plan, no direct messaging, no agent-to-agent coordination. Only environment-mediated signals.

Termite biology — and the broader social-insect literature — recognizes that pheromones come in **at least two polarities**:

- *Attractive* pheromones — call other agents IN. Cement-pheromone, nest-mark pheromone. The signal says "build here," "feed here," "join."
- *Repellent* pheromones — push other agents OUT. Alarm pheromones in some contexts; aggregation-saturation signals; territorial markers. The signal says "leave this area," "this is occupied," "yield."

Both are necessary for stigmergic coordination to work in any non-trivial setting. Without attractants, agents can't recruit collaborators to work-in-progress. Without repellents, agents collide on overlapping work.

This document captures how that two-polarity model shows up in our substrate, why we already use attractants, and what the addition of repellents looks like.

## What we already have: attractive pheromones

Our substrate has been using attractive pheromones from the beginning, even though we don't usually call them that. The core attractive pheromone is `comment.revise`.

When a reviewer (cone-review, full-review, note-review) finds a problem with a doc, it emits `comment.revise(F=[review_doc], G=[claim_or_note])` — a substrate fact that says "this doc needs revision." Refiner agents (claim-revise, note-revise) read the link as their initiation condition. They fire. They emit `resolution.edit/reject` to close the comment. The link has run its lifecycle.

This is structurally identical to how nest-mark pheromone works in termites:
- A signal (link / pheromone) is emitted into the environment (substrate).
- Other agents (refiners / builders) read it as a call to action.
- Their response leaves further substrate effects (resolution / cement).
- Closure is explicit (resolution emitted) rather than time-decayed.

The pattern generalizes:

| Attractive pheromone | What it calls in | Closure |
|---|---|---|
| `comment.revise` | Refiner agents (revisers) | `resolution.edit` / `resolution.reject` |
| `comment.violation` | Structural-revise refiner | `resolution` (same family) |

Both are emit-then-explicit-close lifecycles. Distinguished from biological pheromones by replacing time-decay with explicit closure-as-emission. Pure stigmergic semantics otherwise: the substrate carries the signal; agents read; coordination emerges from local rules.

## The problem: agents with overlapping writes

Some agents do not just emit findings — they perform substantial filesystem-level edits during their fire, and their edits overlap with other agents' edits.

Concretely: `full_review` and `cone_review` both produce reviews that flow through `claim_findings` → `claim_revise`. The reviser closes findings by editing claim md bodies. If both reviewers fire concurrently against the same ASN, their findings hit `claim_revise` from two sources, and revise fires step on each other's edits to the claim file. The substrate-link emissions are idempotent (link types are append-only, retraction is itself an emission), but **the file edits are not**. Two writers modifying the same `.md` file race each other; one's writes overwrite the other's.

This pattern is not unique to the review pair. Any future agent that performs claim-md edits — verification refining a claim against Dafny output, scheduled re-formalization, off-spine patch agents — will collide with the same reviser machinery if it fires concurrently.

Pure attractive pheromones do not solve this. `comment.revise` calls refiners IN; it doesn't keep two reviewers from emitting on the same scope at the same time. The conflict isn't "who responds to a finding" — it's "who creates findings against this scope right now."

### Considered: partition the write surface

Before adding a coordination primitive, the prior question is whether the conflict exists by design rather than necessity. The motivating instance is `full_review` and `cone_review` both fanning their findings out into per-claim md edits via `claim_revise`. Could `full_review` instead emit findings to a note-level artifact, leaving claim mds to `cone_review`?

**Ruled out for this conflict pair.** Once `claim_decompose` runs, the source note is retired — its content moves into the per-claim md files and the claims-statements aggregate. There is no live note-level artifact for `full_review` to file findings against. The claims-statements aggregate is a derived/rendered view; revising it to fix a finding still means revising the underlying claims, which lands the conflict back on `claim_revise`. The live write surface is per-claim by structural necessity, post-decompose.

Coordination via the new primitive is the right answer for this conflict pair. The partitioning consideration remains worth applying case-by-case to future agent pairs (verification, patch agents, etc.) — some may be partitionable; the primitive handles those that aren't.

## Repellent pheromones

Add a substrate primitive whose semantic is "I am currently active on this resource, stay out." Other agents in conflict positions read the marker and yield. When the agent's fire completes, it emits a closure that returns the resource to a quiescent state.

Concretely, the new primitive:

```
holding(F=[agent_doc], G=[resource_addr])
```

Lifecycle:
- Agent emits `holding` at fire start.
- Agent emits a `retraction` of the `holding` link at fire end (success or failure).
- `session.active_links("holding", to_set=[resource])` returns the set of currently-held resources.

The lifecycle is identical to `comment.revise` — emit, then explicit close. The polarity is the only thing that flips. Where `comment.revise` calls refiners IN to address a finding, `holding` keeps other agents OUT until the firing agent's work completes.

### What this primitive really is

`holding` is an **advisory lock** implemented via stigmergic primitives. Both framings are accurate and serve different purposes:

- The *pheromone* framing connects the primitive to the substrate's existing coordination patterns (`comment.revise`, `comment.violation`) and shows it composes the same emit-then-explicit-close mechanism with opposite polarity.
- The *advisory lock* framing surfaces engineering questions that aren't visible from the pheromone analogy alone: atomicity of acquire, lock ordering, fairness, advisory-vs-enforced semantics.

This document uses the pheromone framing for vocabulary continuity (the substrate's coordination patterns are pheromone-shaped) but treats the engineering questions as the lock questions they are. Both are load-bearing.

## Pairing with quiescence

The substrate already has a vocabulary for "no work pending here": **quiescence**. A claim is `is_claim_quiescent` when there are no unresolved revises against it. An ASN is `is_asn_quiescent` when no claim under it has open work.

`holding` extends quiescence to also cover in-flight agent fires. A resource is **quiescent** iff:

1. No unresolved findings target it (existing semantics), AND
2. No agent has emitted a `holding` link against it (new semantics).

In code:

```python
def is_claim_quiescent(session, claim_addr):
    if has_unresolved_comments(session, claim_addr):
        return False
    if is_held(session, claim_addr):
        return False
    return True
```

The substrate's existing quiescence predicates absorb the new check. Triggers that already gate on quiescence (cone_review, full_review, claim_revise, etc.) automatically respect the new pheromone — no per-trigger predicate change needed beyond extending the quiescence definition.

`holding` is conceptually a *quiescence-breaker*: it temporarily takes a resource out of quiescent state for the duration of a fire. Its closure (retraction) returns the resource to quiescence.

## Agent-side resource declaration

To enforce mutex correctly, the agent base class needs to know **what to hold** when it fires. For `cone_review` firing on a claim, the resource it should hold isn't the claim itself but the parent ASN (because cone work conflicts at the ASN level, not just the apex). For `claim_revise` firing on a comment, the resource is the claim the comment targets.

This per-agent resolution is itself substrate-encoded via a classifier on the agent doc:

```
agent.scope.note    — agent holds at note (ASN) scope
agent.scope.claim   — agent holds at claim scope
agent.scope.inquiry — agent holds at inquiry scope
```

These are subtype classifications on the agent doc, parallel to how `review.content` / `review.structural` partition `review`. Each agent doc carries one (or more) `agent.scope.<type>` classifier.

The base class reads the scope at fire time, resolves the input addr to a resource of that type, and emits the `holding` link against that resource:

```python
def __call__(self, session, addr, **kwargs):
    with agent_context(str(agent_doc_path(self.role))):
        scope_type = read_scope_classifier(session, agent_doc)
        hold_addr = resolve_to_scope(session, addr, scope_type)
        if hold_addr is None:
            raise RuntimeError(
                f"agent {self.role}: addr {addr} could not be resolved "
                f"to declared scope {scope_type!r}; "
                f"agent cannot fire without a hold target"
            )
        with hold_context(session, agent_doc, hold_addr):
            return self.run(session, addr, **kwargs)
```

**Failure to resolve is a hard error, not a silent fall-through.** An agent whose addr can't be mapped to its declared scope must not fire — running without a hold defeats the mutex guarantee. The error surfaces immediately rather than producing the kind of bug that's discovered months later when "two fires collided that the doc says can't."

`resolve_to_scope` is a small dispatch keyed on the scope type name:

| scope_type | addr is | hold_addr is |
|---|---|---|
| note | note address | addr |
| note | claim address | walk `provenance.derivation` reverse to source note |
| note | comment address | walk to comment's targeted claim, then to source note |
| claim | claim address | addr |
| claim | comment address | comment's targeted claim |
| inquiry | inquiry address | addr |

The resolver dispatch is code-side (small per-scope-type helpers), but the SCOPE DECLARATION itself lives in substrate. New agents added later get classified with their scope; the resolver and base class machinery accommodate them automatically.

**Comment-target single-target assumption.** The comment-resolution path uses the comment's first target. The substrate convention is that a `comment.revise` / `comment.violation` link has a single target doc — the comment is about one claim or one note. If multi-target comments are ever introduced, the resolver dispatch needs adjustment.

## Mutex semantics

With `holding` and `agent.scope.<type>` in place, the mutex is a single substrate query:

```python
def is_held(session, resource_addr):
    """True iff any agent has an active holding against this resource."""
    return bool(session.active_links("holding", to_set=[resource_addr]))
```

Two agents firing on the same scope (both holding the same note, say) cannot both have a `holding` simultaneously — the second's predicate sees the first's link and skips. Quiescence is broken until the first agent's retraction returns the resource to quiescent state.

There is no cohort-group lookup. There is no `CONFLICT_GROUPS` registry. Conflicts emerge naturally from agents holding the same resource.

When an agent's scope is at note level, it cannot fire while ANOTHER agent at note scope holds that note. When an agent's scope is at claim level, it cannot fire while ANOTHER agent holds that specific claim. The mutex granularity is the agent's declared scope.

### Mutex is advisory, not enforced

This is yield-coordination, not a true mutex. Specifically:

- An agent that respects the predicate yields when another holding is active. The cooperative case.
- An agent that bypasses the predicate (operator-forced fires, force-pass mode, manual invocation) will fire regardless. **Operator force always wins.** When the operator overrides into a held resource, both fires emit holdings, both run, and both write to the file during overlap. The substrate stays internally consistent (each holding is properly opened and closed) but the underlying file races. That's the operator's problem by design — manual override is by definition a concurrent-write state.
- Two agents whose predicate evaluations interleave with their emits could theoretically both fire (see Atomicity below).

This is a design choice, not an oversight: the substrate is a public bus, not a kernel mutex. Cooperative discipline is the enforcement mechanism. An agent that refuses to cooperate cannot be forced to yield by the substrate alone.

### Predicates read open holdings only

The substrate is monotonic at the storage layer: closed `holding` links (those with retractions) persist as substrate facts forever. That history is, de facto, a log of "which agent touched which resource when" — exactly the workflow-tracking information the convention against verb-flag classifiers prohibits.

The **predicate-layer view** of the substrate is non-monotonic — `active_links` excludes retracted links by construction. This non-monotonic projection is what makes the workflow-state prohibition meaningful: predicates see a "currently active" view, never a "has ever been active" view. Both layers exist; the workflow-state prohibition lives at the predicate-layer.

To prevent drift, the convention is:

> **Predicates over `holding` read only open links** — those returned by `active_links("holding", ...)`. Closed holdings are completion data; predicates do not read them as "this agent has held this resource at some point."

The predicate library exposes only `active_links`-shaped accessors for this purpose (`is_held`, `held_by_other`, etc.). Raw substrate-history access via `links_history` or equivalent is for audit and observability tooling, not predicates. New code that wants to ask "has agent X ever held resource Y" is asking the wrong question for predicate purposes — that's audit, not predicate logic.

### Stale-holding observability

Every substrate link's emission record (in `links.jsonl`) carries a `ts` field — the emit timestamp. A `holding` link is no exception: the timestamp lives on the persistence record.

**Implementation note:** the in-memory `Link` object does not currently carry `ts` — the timestamp lives only on the persisted JSONL record, not the Python class. So a stale-holding observability tool can be built two ways:

- Operator-side script that reads `links.jsonl` directly and surfaces holdings with `ts` older than a threshold. Slow but doesn't touch substrate code.
- Substrate extension: add `ts` to the `Link` dataclass so predicates and other in-memory consumers can read it. Then a predicate-layer `stale_holdings` becomes a one-line query.

For v1, neither is implemented — manual operator inspection of the JSONL log handles stuck-state detection. The first non-trivial stuck-state incident is the right time to choose between (1) and (2). Lease semantics (`until_ts` field with auto-expiry) is the further enhancement on top of either.

## Atomicity

The predicate (`is_held(R)`) and the emit (`holding(agent, R)`) are not a single atomic operation by themselves. In a concurrent setting, two agents could each evaluate predicates at t=0, both see no holdings, both emit at t=1, and both proceed to fire. The naive design is racy.

**Critically, this is a single-node intra-process question, not a multi-node distributed-systems question.** Under Xanadu's content-immutability model, other nodes/users cannot modify our claims directly — they make copies. Each node operates on its own substrate; cross-node interaction is via copy-and-merge protocols at the substrate level, not concurrent shared-write access. There is no scenario in this architecture where two nodes contend for write access to the same `holding`. The "distributed atomicity" framing common in distributed-systems literature does not apply.

The atomicity question reduces to: **within one node's runtime, can two agents' predicate-check + emit interleave?** The answer depends on the runner's concurrency model:

### v1: single-process sequential runner

In the current runtime, the runner walks triggers serially within a pass. For each trigger, the predicate is evaluated, the agent fires (synchronously), and the session is reloaded before the next trigger's predicate evaluates. The agent's `holding` emit happens **inside** the agent's run, before the LLM call.

- Trigger A's predicate runs → sees no holding → fires.
- Inside A's `__call__`, the holding is emitted.
- A runs to completion (LLM call, emissions, etc.).
- A retracts the holding.
- Runner moves to trigger B → predicate runs after session reload → sees A's retraction → fires safely.

Atomicity is provided by sequential dispatch: only one agent runs at a time, the runner doesn't move to the next trigger until the current one finishes. Predicate-check + emit are not atomic at the substrate level, but they're atomic by serialization at the runner level.

**This is incidental, not designed-in. The single-fire-at-a-time dispatch is load-bearing for `holding` mutex correctness.** If the runner is parallelized for performance, the `holding` mutex breaks silently. This invariant should be documented in `scripts/lib/runner/run.py` itself with a comment cross-referencing this design doc — otherwise it's a tripwire for future contributors who don't see the connection between runner concurrency and mutex correctness.

### Future: in-process multi-threaded or async runner

If we later parallelize the runner within a single process (multi-threaded dispatch, async event loop), atomicity needs explicit coordination. The standard answer is straightforward in-process locking:

- Wrap `emit_holding` in an in-process lock (Python `threading.Lock` or `asyncio.Lock`). The lock serializes the predicate-check + emit pair.
- Predicate evaluation outside the critical section (cheap, frequent) reads substrate normally.
- The actual `is_held → emit_holding` sequence runs inside the lock.

This is in-process locking, not distributed CAS. It's a code-level addition to the agent base class with no substrate-spec impact.

### Multi-node Xanadu deployment

Multi-node coordination in Xanadu is **not** shared-substrate concurrent-write. Each node has its own substrate; cross-node sharing is via copy-and-merge protocols (when those exist), governed by Xanadu's transclusion model. A `holding` link emitted on Node A is local to Node A's substrate; Node B never sees it directly nor needs to coordinate against it. Cross-node `holding` semantics simply don't apply, because cross-node concurrent-write doesn't happen by design.

Operations that span nodes — e.g., a copy made at Node B from Node A's content — are governed by Xanadu's copy semantics, not by `holding`. The primitive is per-node; the architecture handles the rest.

## Why the existing patterns suffice

A useful test of this design: can it be expressed using existing substrate primitives plus the one new link type, or does it require additional plumbing?

| Capability | Mechanism |
|---|---|
| Repellent signal emission | `holding` link |
| Closure / quiescence-restoration | `retraction` of the `holding` link (existing primitive) |
| Substrate-side group membership | `agent.scope.<type>` classifier (subtyping pattern; existing) |
| Predicate over held state | `active_links` query (existing primitive) |
| Stale-holding detection | `ts` on JSONL persistence record (in-memory `Link` doesn't carry ts in v1; observability is JSONL-side) |
| Quiescence-aware gating | Existing `is_*_quiescent` predicates extended |
| Crash recovery | Manual operator intervention v1 (existing convention for stuck `comment.revise`) |

The substrate-spec change is minimal: one new link type (`holding`), one new classifier subtype family (`agent.scope.<type>`). Everything else composes existing primitives.

## Crash recovery

If an agent crashes mid-fire, its `holding` link is not retracted. The resource stays non-quiescent indefinitely. Other agents skip forever.

For v1, recovery is manual: the operator notices the stuck state (typically via a stale-holding query against the existing `ts` field), identifies the abandoned `holding` link, and emits a retraction. Same convention as recovering from a stuck `comment.revise` whose reviser failed. The `ts`-based stale-holding query gives operators an alarmable observable from day one.

If manual recovery becomes painful in practice (long-running agents, frequent crashes), the next enhancement is a **lease** — add an `until_ts` field on the `holding` link marking the lease expiry. Predicates check `current_time < until_ts` and disregard expired leases. This is the standard distributed-systems leases pattern ([Gray & Cheriton 1989](#references); [Burrows 2006](#references) on Chubby for production-scale advisory locks). Note that the lease here is intra-process crash-safety, not cross-node coordination — the multi-node story remains copy-and-merge per Xanadu. Since `ts` (emit time) is already on every link, the migration to lease semantics is a schema extension on `holding` plus a predicate update — not a backfill problem.

## Why this matches the protocol architecture

The protocol stack (per [`docs/protocols/README.md`](../protocols/README.md)) classifies the substrate as a stigmergic message bus: durable, queryable, monotonic, public. Agents coordinate through it, not through direct calls. The core mechanism is pheromone-shaped emissions with explicit closure rather than time-decay.

`holding` is consistent with that architecture:

- **Durable.** The link persists in `links.jsonl` until retraction. Both emission and retraction are durable.
- **Queryable.** Standard `active_links` interface; predicates compose normally.
- **Monotonic at the storage layer.** Retraction is itself an emission. The link history grows monotonically. The predicate-layer view via `active_links` is non-monotonic by projection; that distinction is what makes the workflow-state prohibition meaningful (predicate logic operates on the non-monotonic view; audit tooling on the monotonic view).
- **Public within a node.** Every agent on a node reads the same substrate state. Multi-node sharing is via copy-and-merge per Xanadu, not via shared substrate.

## Spec

### Substrate types

| Type | Shape | Idempotent? | Closure |
|---|---|---|---|
| `holding` | F=[agent_doc], G=[resource_addr] | No | Retraction at fire end |
| `agent.scope.note` | classifier on agent doc | Yes | Permanent declaration |
| `agent.scope.claim` | classifier on agent doc | Yes | Permanent declaration |
| `agent.scope.inquiry` | classifier on agent doc | Yes | Permanent declaration |

### Predicates

```python
def is_held(session, resource_addr) -> bool:
    """True iff any agent has an active holding against this resource."""

def held_by_other(session, resource_addr, my_agent_doc) -> bool:
    """True iff any agent OTHER than my_agent_doc has an active holding."""

def is_claim_quiescent(session, claim_addr) -> bool:
    """Existing predicate, extended: also False when is_held returns
    True for the claim or its parent ASN."""

def is_asn_quiescent(session, note_addr) -> bool:
    """Existing predicate, extended: False when is_held returns True
    for the note or any derived claim."""

```

(Stale-holding observability is not a v1 predicate — see *Stale-holding observability* above.)

Convention: predicate code reads `active_links` (open holdings only). Closed holdings are completion data; predicate-layer code does not consult them. Audit and observability tooling reads the full link history via separate accessors.

### Integration points

- `lib/backend/types.py` — register `holding` and `agent.scope.<type>` allocator slots.
- `lib/backend/shapes.py` — declare shapes (holding link; agent.scope classifier).
- `lib/backend/emit.py` — `emit_holding(store, agent_doc, resource)`, `emit_agent_scope(store, agent_doc, scope_type)`.
- `lib/predicates/quiescence.py` — extend existing `is_*_quiescent` predicates with `is_held` check.
- `lib/predicates/agents.py` (new) — `is_held`, `held_by_other`, `agent_scope_for`, `resolve_to_scope`, `stale_holdings`.
- `lib/agents/base.py` — `__call__` wraps `run()` in `hold_context(session, agent_doc, hold_addr)`. Raises on unresolved scope.
- `lib/runner/run.py` — add comment marking single-fire-at-a-time dispatch as load-bearing for `holding` mutex correctness; cross-reference this design doc.
- Per-agent: tag agent doc with `agent.scope.<type>` classifier (one-time substrate emission, can run as part of agent registration or a setup script).

### Resource resolver

```python
def resolve_to_scope(session, addr, scope_type):
    if scope_type == "note":
        return _addr_to_note(session, addr)
    if scope_type == "claim":
        return _addr_to_claim(session, addr)
    if scope_type == "inquiry":
        return _addr_to_inquiry(session, addr)
    return None  # caller treats as a hard error
```

Each helper walks substrate to find the addr's containing resource of the requested type. Walks use existing primitives: `provenance.derivation` reverse for note resolution, comment-target for revise → claim, etc.

### Operator-gated agents

Agents that fire on operator command (e.g., `claim_decompose`, `note_patch`, `note_extract`) participate in the mutex naturally — their `__call__` wrapper emits `holding` like any other agent. An operator-fire on an ASN that's currently held by another agent will skip if the predicate is run, or will be operator-overridden if invoked manually. Operator force always wins; the mutex is advisory, not enforced (see *Mutex is advisory* above). Operator override is by definition a concurrent-write state.

### Substrate growth

A back-of-envelope estimate: ~10 active agents × ~50 fires/day system-wide × 2 emissions per fire (open + close) × ~200 bytes per link entry ≈ 200 KB/day, or roughly 70 MB/year at current operating scale. MB-level, not GB. Pruning policy is not a v1 concern; if scale grows by 10× or more, revisit.

## Open questions

- **Lock-ordering convention for v2 multi-resource holds.** When agents legitimately hold multiple resources in one fire (a meta-operation editing both note and a claim), without an ordering rule, deadlocks are possible: A holds R1 wants R2; B holds R2 wants R1. Standard candidate: **resource-address ordering** — agents acquire holdings in canonical address order; if mid-fire an agent finds it needs a resource whose address sorts earlier than what it currently holds, it must yield (release current holdings, retry from clean state). v1 doesn't see this because every agent holds exactly one resource, but v2 (claim-level granularity, cross-resource ops) needs an explicit rule. The work-loss semantics of the "abort and retry" half deserve thought before implementation — for LLM-driven agents, mid-fire retract means throwing away an LLM call.
- **Partition vs coordinate (case-by-case).** The `full_review`/`cone_review` partition was ruled out by the post-decompose write-surface structure. Future agent pairs (verification-vs-revise, patch-vs-revise) deserve the same case-by-case review: is the conflict structurally forced, or could output surfaces be partitioned to avoid it?
- **Shared-vs-exclusive locking.** Current proposal is mutex (any active holding excludes any other). A future read-write distinction could allow read-only agents to share. Probably not needed v1.
- **Granularity v1: note-level for review-group.** Both `cone_review` and `full_review` declared `agent.scope.note`. Sequentializes cone fires across apexes too. Future fine-grained version (cone holds individual claims, full holds the union of claims) is achievable without substrate change — the cross-resource-holds answer ("emit multiple `holding` links, one per held resource") is the same mechanism. Predicate-only migration when needed.
- **In-process locking shape if/when the runner parallelizes.** v1 sequential dispatch handles atomicity. If the runner gains thread-pool or async dispatch later, the predicate-check + emit pair needs an in-process lock. Cheap addition; not a v1 concern but the runner-comment tripwire mentioned above ensures the question gets asked at the right time.
- **Starvation under extended quiescence.** Quiescence is now defined as "no open findings AND no agent currently holding." If something always holds a note (high fire-rate, long-running fires), tiers that gate on `is_asn_quiescent` never fire — quiescence becomes structurally unreachable. Not a current concern at single-operator tempo, but worth modeling if fire-rate climbs above roughly one fire per note per N minutes, where N depends on average fire duration. Possible mitigations: lease semantics with a max-hold cap, or a starvation-detection predicate that surfaces "this resource has been held continuously for > T."

## References

- Grassé, P.-P. (1959). *La reconstruction du nid et les coordinations interindividuelles chez Bellicositermes natalensis et Cubitermes sp.* Insectes Sociaux 6, 41–80. The original stigmergy paper.
- Theraulaz, G., & Bonabeau, E. (1999). *A Brief History of Stigmergy.* Artificial Life 5(2), 97–116.
- Bonabeau, E., Theraulaz, G., & Deneubourg, J.-L. (1996). *Quantitative study of the fixed threshold model for the regulation of division of labour in insect societies.* Proceedings of the Royal Society B, 263(1376), 1565–1569. Response thresholds in social insects.
- Holland, O., & Melhuish, C. (2000). *Stigmergy, self-organization, and sorting in collective robotics.* Artificial Life 5(2), 173–202. Engineering-grounded stigmergic coordination.
- Gray, C., & Cheriton, D. (1989). *Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency.* SOSP. Time-bounded distributed locks. Cited here for the lease pattern (intra-process crash-safety enhancement); the cross-node usage in the original paper does not apply to our Xanadu architecture.
- Burrows, M. (2006). *The Chubby lock service for loosely-coupled distributed systems.* OSDI. Production-scale advisory locks. Cited for vocabulary; the cross-node coordination problem Chubby solves is not present here.
- Lampson, B. (1983). *Hints for Computer System Design.* SOSP. General principles for system-design tradeoffs (primitive vs restructure, etc.).

## Cross-references

- [Maturation Stigmergic Protocol](../protocols/maturation/note-to-claim.md) — the protocol this coordination supports.
- [Substrate spec](../protocols/substrate/) — the foundation the new primitives compose against.
- Predicate-audit memory entries (`feedback_full_and_cone_review_must_not_run_concurrently.md`) — the constraint that motivated this design.
