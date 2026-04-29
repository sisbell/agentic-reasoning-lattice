# Agent Module

The agent module defines what an agent is and how the substrate identifies it.

An agent is a document. The doc's address is the agent's identity; the doc's content is the agent's definition — what it does, how it reasons, what tools it uses, when it converges. Two link types complete the model: `agent` classifies a doc as an agent (same shape as `claim`, `review`, `contract`), and `manages` declares that one agent is currently responsible for an operation.

The result: each agent is first-class — addressable, readable, portable. Consumers ask "what does this agent do?" by navigating to the agent's address and reading. They ask "who manages this operation?" by querying the substrate.

The module sits above the [Substrate](substrate-module.md) and uses substrate primitives unchanged.

---

## 1 Document and link model

### Agent doc

An agent doc is an ordinary document. The substrate addresses it like any other document and stores its content the same way.

**Agent identity is the agent doc's tumbler.** Operations that reference an agent reference the doc's address. The classifier link (described below) declares the doc is an agent; it carries no identity of its own.

The agent doc carries the agent's defining content — at minimum a description; in practice often the system prompt, tool surface, output expectations, and convergence rules. The substrate imposes no structural conventions on the content; reading conventions are an orchestrator concern.

Agent docs evolve like any other doc. When the agent's definition changes, the doc is edited; the classifier link survives; consumers see the new version on next read.

### `agent` link

Classifies a document as an agent.

```
type_set = ["agent"]
from_set = []
to_set   = [agent_doc]
```

Same shape as `claim`, `review`, `contract` — empty `from_set`, single doc in `to_set`. The link declares "this doc is an agent" and nothing more.

### `manages` link

Declares an agent manages an operation.

```
type_set = ["manages"]
from_set = [agent_doc]
to_set   = [operation_link_id]
```

Doc-to-link shape — same pattern as `resolution.edit`. The operation being managed is referenced by its link id; the operation link itself is never modified.

Multiple `manages` links may accumulate on a single operation. The current manager from one asserter's view is determined by A3 (manager resolution).

### Operation links

Any link a consumer wants attributed to an agent — typically reviews, comments, resolutions, citations. The agent module is agnostic about operation type; `manages` accepts any link as its target.

---

## 2 Modules used

### Substrate

The persistent, append-only link graph. See [Substrate Module](substrate-module.md) for the full specification.

**Operations relied upon.**

- ⟨ MakeLink | from, to, types ⟩ — append a new link, return its address.
- ⟨ FindLinks | from, to, types ⟩ — return all links matching the constraint conjunction.
- ⟨ ActiveLinks | from, to, types ⟩ — return all matching links not retracted (per SUB4, SUB5).
- ⟨ Retract | link_id ⟩ — file a `retraction` link nullifying a prior link (per SUB4–SUB6).

**Properties relied upon.**

- SUB1 (Permanence). Agent classifiers, manages links, and retractions persist.
- SUB2 (Query soundness). Idempotency checks in EmitAgent and EmitManages observe what was filed.
- SUB4–SUB5 (Retraction nullifies, shadow). Management transfer via retract + re-issue is honored by ActiveLinks.
- SUB6 (Retraction idempotence). Repeated transfer attempts are safe.

### Tumbler Algebra

The algebra of substrate addresses. See [`lattices/xanadu/_docuverse/documents/claim/ASN-0034/`](../../lattices/xanadu/_docuverse/documents/claim/ASN-0034/) for the full specification.

**Properties relied upon.**

- **T9 (ForwardAllocation)** — [`T9.md`](../../lattices/xanadu/_docuverse/documents/claim/ASN-0034/T9.md):
  `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`
  Within one allocator's sequential stream, addresses are strictly monotonically increasing. Per-allocator only; T9 makes no claim across allocators.
- **TA5(a) (Increment strict-greater)** — supporting lemma for T9. `inc(t, 0) > t` for any `t ∈ T`.

A3 (manager resolution) cites T9 to use address comparison as a proxy for allocation order within an asserter's link allocator. The agent module makes no cross-allocator ordering claim; that would violate T9's stated scope.

---

## 3 Participants and events

The agent module describes how a single role — the **asserter** — files agent classifiers and manages links into the substrate. An asserter is whoever owns an allocator filing links — typically one collective acting through a single allocator. Multiple asserters may co-exist and operate concurrently; each manages its own classifications and attributions independently.

### Events

**Requests (input from above).**

- ⟨ EmitAgent | agent_doc ⟩ → link_id — file an `agent` classifier on the agent doc. Idempotent on the doc target (active classifiers only).
- ⟨ EmitManages | agent_doc, operation ⟩ → link_id — file a `manages` link from the agent doc to the operation. Idempotent on the (agent, operation) pair (active links only).
- ⟨ TransferManagement | operation, prior_manages, new_agent_doc ⟩ → link_id — retract `prior_manages` and file a fresh `manages` from `new_agent_doc` to `operation`. Composed of substrate's ⟨ Retract ⟩ followed by ⟨ EmitManages ⟩. Not atomic; see non-guarantees.

**Indications (output upward).**

- ⟨ AgentClassified | agent_doc, link_id ⟩ — an agent classifier exists.
- ⟨ ManagesFiled | agent_doc, operation, link_id ⟩ — a manages link exists.
- ⟨ ManagementTransferred | operation, from_agent, to_agent ⟩ — management of operation has moved from one agent to another within the asserter's view.

The agent module does not itself indicate convergence, completion, or any higher-level state. Consumers querying "who currently manages this?" do so via FindLinks/ActiveLinks plus the resolution rule defined in A3.

---

## 4 Properties

### 4.1 Safety

**A1 (Identity stability).** For an agent doc D, repeated invocations of ⟨ EmitAgent | D ⟩ return the same `link_id` so long as no intervening retraction has nullified the classifier.

**A2 (Operation immutability under management transfer).** For any operation link O and any sequence of TransferManagement calls targeting O, the content (from/to/types) and address of O are unchanged. No module operation writes to O.

**A3 (Manager resolution within an asserter).** Let A be an asserter with link allocator α, and O an operation link. Define the *current manager from A's view* as the agent doc identified by the `manages` link satisfying:

- the link is active (not retracted),
- the link is in α (filed by A's allocator),
- the link's `to_set` is `[O]`,
- the link's address is maximal among all links satisfying the above.

By T9, within α's sequential stream this maximal-address link is the most-recently-allocated active manages — equivalently, the most-recently-filed by A. If no link satisfies the conditions, A has no view of O's current manager.

**A4 (Cross-asserter non-resolution).** When `manages` links targeting O exist in multiple distinct allocators, the substrate does not resolve to a single current manager. ActiveLinks returns all active manages across all allocators; resolution is undefined cross-asserter because T9 is scoped per-allocator. Consumers requiring a single answer must scope their query to a chosen asserter's allocator.

**A5 (Append-only consistency).** All module operations reduce to substrate operations (MakeLink, FindLinks, ActiveLinks, Retract). The agent module inherits SUB1–SUB6 unchanged; it introduces no additional substrate-layer guarantees.

**A6 (Classifier retraction is well-defined).** Retracting an `agent` classifier link removes the agent doc from `active_links(type=["agent"])` queries (per SUB4–SUB5). Existing `manages` links with the doc as `from_set` remain active and continue to satisfy A3 unchanged. A retracted-classifier agent is no longer in the asserter's "current agents" set; its management history is preserved. Re-emitting the classifier later files a fresh `agent` link with a new id (per A1's retraction caveat); the prior retracted classifier persists in the substrate but is excluded from active queries.

### 4.2 Liveness

**LA1 (Operation responsiveness).** If ⟨ EmitAgent | D ⟩, ⟨ EmitManages | a, o ⟩, or ⟨ TransferManagement | … ⟩ is invoked, the operation returns. Each request reduces to one ActiveLinks call and at most one MakeLink (plus, for transfer, one Retract); all are synchronous substrate calls.

**LA2 (Cross-invocation persistence).** Agent classifiers and manages links persist across invocations of any process that reads them. Discoverable via FindLinks/ActiveLinks at any later time. (Inherited from SUB1.)

### 4.3 Deliberate non-guarantees

**No global ordering.** Cross-asserter manages links are not comparable for resolution. T9 holds per-allocator; the substrate exposes no cross-allocator ordering primitive.

**No transfer atomicity.** TransferManagement is composed of ⟨ Retract ⟩ followed by ⟨ EmitManages ⟩. Between these two substrate calls, the prior manages link is retracted and the new one does not yet exist. During this window, A3 resolves to either the next-largest prior active manages (if any existed) or to "no manager" (if the retracted link was the only one). Concurrent readers may observe this transient state. Asserters that need atomic transfer must serialize their own operations; the substrate does not provide a transaction primitive.

**No spoof prevention is needed.** Substrate addresses carry the producing asserter's prefix structurally. Cross-asserter forgery is prevented by the address scheme, not by an enforcement layer the substrate must add.

**No discipline enforcement.** If an asserter fails to retract prior manages before re-issuing (transfer discipline failure), the substrate stores both as active. A3 still resolves to the address-maximal within the asserter's view; the asserter is responsible for its own allocator integrity.

**No coverage guarantee.** The agent module does not require that any agent has ever been classified, that any operation is managed, or that any orchestrator runs. Coverage is a choreography concern.

---

## 5 Correctness arguments

The properties trace through substrate guarantees and the tumbler algebra. The arguments are short; their value is making the dependency on each cited property explicit.

**A1 (Identity stability).** ⟨ EmitAgent | D ⟩ first calls ActiveLinks on `type=["agent"], to=[D]`. By SUB2 (query soundness), this returns exactly the active classifier links targeting D. By SUB4–SUB5 (retraction nullifies), retracted classifiers are excluded. If a classifier is found, EmitAgent returns its link_id without further writes — idempotent. If none is found, MakeLink files a new one; by SUB1 the new link persists and is observable to any future ActiveLinks call. A concurrent or subsequent EmitAgent therefore observes the just-created classifier and returns its id. Idempotency holds across calls so long as no intervening retraction has nullified the classifier.

**A2 (Operation immutability under management transfer).** Every operation in this module either creates a new link (MakeLink) or retracts an existing one (Retract). MakeLink produces a fresh link with a fresh address; it does not alter prior links. Retract files a `retraction` link whose `to_set` is the link being nullified — by SUB4 this nullifies for ActiveLinks queries but does not modify the targeted link. In TransferManagement, the link being retracted is a prior `manages` link, and the link being created is a new `manages` link; neither references O via `from_set` or `to_set` in any operation that writes to O. The operation link's content and address are therefore stable across any sequence of module operations.

**A3 (Manager resolution within an asserter).** ActiveLinks on `type=["manages"], to=[O]` returns all non-retracted manages links targeting O (by SUB2 + SUB4–SUB5). Filtering to allocator α restricts the result to links produced by asserter A. Within α, T9 guarantees `same_allocator(a, b) ∧ allocated_before(a, b) ⟹ a < b`. The contrapositive lets us use address comparison as a proxy for allocation order: if `a > b` and both are in α, then `a` was allocated after `b`. Therefore the address-maximal element of the filtered set is the most-recently-allocated active manages link in α, which is the asserter's most recent attribution of management to an agent for O.

**A4 (Cross-asserter non-resolution).** T9 is stated and proved per-allocator only. The note explicitly disclaims cross-allocator ordering: addresses from different allocators interleave by hierarchical position, not by allocation time. The address-comparison argument used in A3 therefore does not extend across allocators, and the module makes no resolution claim there.

**A5 (Append-only consistency).** EmitAgent reduces to ActiveLinks + at-most-one MakeLink. EmitManages reduces to ActiveLinks + at-most-one MakeLink. TransferManagement reduces to one Retract + EmitManages. Every operation is a substrate call; the agent module introduces no substrate-layer state of its own. SUB1–SUB6 hold for the operations the module performs because they hold for the substrate operations the module composes.

**A6 (Classifier retraction is well-defined).** Each substrate link has its own retraction status; retracting link X has no effect on any other link Y (a structural consequence of SUB4–SUB5 — the `retraction` link's `to_set` references X specifically, and ActiveLinks evaluates retraction status per-link). The `agent` classifier and the `manages` links with the same `from_set = [agent_doc]` are distinct links of distinct types. Retracting the classifier therefore affects only `active_links(type=["agent"])` results: by SUB4 the classifier is excluded from the active set; by SUB5 it remains visible as a shadow under raw FindLinks. ActiveLinks queries on `type=["manages"], from=[agent_doc]` are unaffected by the classifier's retraction, so A3's resolution is unchanged. Re-emitting the classifier files a fresh link by EmitAgent's behavior under A1's retraction caveat — the active-set check finds no active classifier and proceeds to MakeLink, producing a new id.

**LA1 (Operation responsiveness).** Each request maps to a fixed-bounded number of synchronous substrate calls (no loops, no waits). The substrate's operations terminate by their own specifications. Therefore each agent-module operation terminates.

**LA2 (Cross-invocation persistence).** Inherited directly from SUB1: links filed in one invocation persist to subsequent invocations and are returned by any matching FindLinks/ActiveLinks call.

---

## 6 Composition

```
Substrate
  ↑ used by
  │
  ├─── Agent module
  │       ↑ used by protocols when operations need attribution
  │
  └─── Convergence Protocol ─── Note Convergence, Claim Convergence
       Consultation Protocol
       Claim Derivation Module
       Maturation Protocol
```

The agent module sits as a service layer over the substrate: it uses substrate primitives (links, retraction, queries) to provide doc-layer agent identity and operation attribution. Protocols use the substrate directly for their core machinery, and use the agent module on top of that when they need to attribute operations to a specific agent — without protocol identity leaking into the substrate's type system.

A protocol that wants its operations attributed:

1. Once per agent role: author an agent doc (description, prompt, tool surface, convergence rules) and call ⟨ EmitAgent ⟩ to classify it. Idempotent.
2. After filing each operation link: ⟨ EmitManages | agent_doc, operation ⟩.
3. Convergence checks query the agent layer: "what's the latest review managed by my cone-review agent?" returns the cone-scoped trajectory without full-review work polluting it.

### Distributed coordination

Each asserter files its own `agent` classifiers and `manages` links from its own allocator. Cross-asserter queries return all assertions; the substrate does not resolve conflicts. Within-asserter queries scoped to the asserter's allocator return a deterministic view (per A3 + T9).

Asserter identity is structural in the address: an agent doc's address carries its producing asserter's prefix, so the asserter that filed any given agent is recoverable from the agent's address alone. Different asserters' cone-review agents are different agents — different addresses, potentially divergent defining content. No global registry needed.

Agent docs are also portable artifacts. An asserter adopting another asserter's agent role can fork the agent doc — the substrate sees a new doc, classified as an agent at its own address. Forks are independent of the original.

### Decommissioning

To deprecate an agent role, retract its `agent` classifier link (per A6). The classifier no longer appears in `active_links(type=["agent"])`, so discovery queries no longer offer it as a current option. Existing `manages` links from the agent doc remain active; A3 still resolves attribution for operations that were managed by the agent. Management history is preserved.

To reactivate, call ⟨ EmitAgent | agent_doc ⟩ again. By A1's retraction caveat the call files a fresh classifier with a new id; the prior retracted classifier persists in the substrate but stays excluded from active queries.

This pattern lets asserters retire agents from current use without losing the ability to answer "who managed this old operation?" — a real operational need that falls out of the property set without additional machinery.

---

## 7 Current implementation

### Schema

```python
# scripts/lib/store/schema.py
VALID_TYPES = {
    ...,
    "agent",
    "manages",
}
```

No subtypes. Subtyping `agent` by role would re-introduce the protocol-identity-in-types leak that motivates this module's existence. Subtyping `manages` by what's managed would duplicate information already in `to_set` (the targeted operation's own type reveals what's being managed).

### Library

`scripts/lib/store/agent.py`. Both operations use ActiveLinks (not raw FindLinks) for their idempotency check, so a retracted classifier or manages link does not falsely satisfy the existence check.

```python
def emit_agent(store, agent_doc_path):
    """Classify a doc as an agent. Idempotent on active classifiers."""
    candidates = active_links(store, "agent", to_set=[agent_doc_path])
    for link in candidates:
        if link["from_set"] == [] and link["to_set"] == [agent_doc_path]:
            return link["id"], False
    link_id = store.make_link(
        from_set=[], to_set=[agent_doc_path], type_set=["agent"],
    )
    return link_id, True

def emit_manages(store, agent_doc_path, operation_link_id):
    """Idempotent on active (agent, operation) manages links."""
    candidates = active_links(
        store, "manages",
        from_set=[agent_doc_path],
        to_set=[operation_link_id],
    )
    for link in candidates:
        if (link["from_set"] == [agent_doc_path]
                and link["to_set"] == [operation_link_id]):
            return link["id"], False
    link_id = store.make_link(
        from_set=[agent_doc_path],
        to_set=[operation_link_id],
        type_set=["manages"],
    )
    return link_id, True
```

### Agent docs

Stage-1 placement: `lattices/<lattice>/_docuverse/documents/agent/<role>.md`. Agent docs live under `_docuverse/documents/` because their lifecycle is substrate-managed (classified, retracted, re-emitted via the agent module's operations) — same convention as the other substrate-classified documents under `_docuverse/documents/` (inquiry, campaign, claim, note, review, finding, …). Loop work products that aren't substrate-typed — pipeline caches, intermediate prose, scratch state — live in the parallel workspace area `_workspace/` alongside `_docuverse/`. Examples:

- `lattices/xanadu/_docuverse/documents/agent/cone-review.md` — focused review of a dependency cone.
- `lattices/xanadu/_docuverse/documents/agent/full-review.md` — whole-ASN review.
- `lattices/xanadu/_docuverse/documents/agent/note-review.md` — review of a discovery note.

### Wall-clock timestamps as a bridge

The current substrate stage-1 implementation stores wall-clock timestamps on every link. **Timestamps are not a substrate property and are not cited by this module's specification.** They serve as a stage-1 implementation convenience that approximates per-allocator monotonic ordering on a single host, where the JSONL log's append order tracks system clock order closely enough for practical use.

The specification's ordering claim (A3) cites T9, not timestamps. As link IDs become tumbler-allocated per the tumbler algebra, T9 will hold structurally and the wall-clock bridge can be retired without revising the spec. Consumers that read timestamps directly are reading an implementation detail and will need to migrate to tumbler-order queries when the bridge is removed.

---

## Related

- [Substrate Module](substrate-module.md) — the data layer the agent module is built on.
- [Tumbler Algebra (ASN-0034)](../../lattices/xanadu/_docuverse/documents/claim/ASN-0034/) — the algebraic foundation for substrate addresses. T9 and TA5(a) are cited by A3 and §5.
- [Substrate Migration Trajectory](../design-notes/substrate-migration-trajectory.md) — the forward-portability commitment. The agent module's links are ordinary substrate links; they migrate the same way every other link does at the Xanadu cut.
- [Convergence Protocol](../protocols/convergence-protocol.md) — defines `review`, `comment`, `resolution`. Convergence protocols use the agent module to attribute their work.
