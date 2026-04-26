# Note Convergence Protocol

The [convergence protocol](convergence-protocol.md) applied to notes during discovery. Drives a reasoning document toward stability through review/revise cycles, with OUT_OF_SCOPE as the off-ramp that feeds lattice growth through the [maturation protocol](maturation-protocol.md).

Following the modular formalism of Cachin (*Reliable and Secure Distributed Programming*).

---

## 1 Document model

Extends the [convergence protocol](convergence-protocol.md) document model with note-specific classifiers and link types.

### Document types

| Classifier | What the document is |
|---|---|
| `note` | A note document. Narrative prose with embedded reasoning and claims. |
| `review` | A review document (inherited from convergence module). |

### Link types

In addition to the convergence module's `review`, `comment`, and `resolution`:

| Type | Subtypes | Role |
|---|---|---|
| `note` | (flat, one-sided) | Classifier: document is a note |
| `citation` | (flat) | Note depends on note |

The `citation` link is the lattice edge at note scale. The note dependency graph — which notes assume foundations from which — is the citation subgraph. Note convergence operates on individual notes; the citation graph is what maturation traverses to decide what enters convergence next.

### Finding classification

Note convergence extends the convergence module's `comment` subtypes:

| Subtype | Role | Predicate participation |
|---|---|---|
| `comment.revise` | The note's reasoning is wrong, incomplete, or ungrounded. Requires resolution. | Yes |
| `comment.out-of-scope` | The finding is valid but its resolution lies outside the current note. | No |

There is no `comment.observe`. Findings on notes are binary: REVISE (must fix) or OUT_OF_SCOPE (valid concern, belongs elsewhere). The two-class scheme prevents classification drift between an audit-only category and a routing category.

OUT_OF_SCOPE channels the [production drive](../design-notes/production-drive.md) differently from OBSERVE: instead of logging an observation, OUT_OF_SCOPE signals to the [maturation protocol](maturation-protocol.md) that the lattice needs structural work — a new inquiry, an extraction, or an absorption. The production drive is harnessed, not just relieved.

---

## 2 Modules used

### 2.1 Convergence protocol

Provides the predicate, comment/resolution machinery, and core safety and liveness properties. See [convergence protocol](convergence-protocol.md).

**Properties inherited.** S1–S6, L1–L4.

### 2.2 Substrate

Inherited via the convergence module. Provides SUB1 (permanence), SUB2 (query soundness), SUB3 (count consistency).

---

## 3 Participants and events

### Reviewer

Inherited from convergence module. Reads assembled context and produces comment links on notes. Comments classified as `comment.revise` or `comment.out-of-scope`. Operates in the Dijkstra voice.

### Reviser

Inherited from convergence module. Resolves `comment.revise` links via `resolution.edit` (note edited) or `resolution.reject` (finding refused with rationale document). Takes no action on `comment.out-of-scope` — those are non-blocking and handled by the maturation protocol.

### Scope assembler

Constructs the context the reviewer sees. The scope strategy is a choreography decision; the protocol prescribes nothing.

### Events

The events from the [convergence module](convergence-protocol.md) operate identically with note-typed targets. Two additional requests:

- ⟨ RegisterNote | doc ⟩ — attach a `note` classifier to doc.
- ⟨ Cite | source, target ⟩ — create a `citation` link from source note to target note.

All other requests (FileComment, ResolveEdit, ResolveReject, EvaluateConvergence) and indications (CommentFiled, ResolutionFiled, Converged, NotConverged) are inherited unchanged. The `comment.out-of-scope` class in CommentFiled indications is the signal maturation subscribes to for lattice operations.

---

## 4 Convergence

Inherits the predicate from the [convergence protocol](convergence-protocol.md):

> For every `comment.revise` link targeting the note, there exists a matching `resolution` link.

`comment.out-of-scope` links do not participate. A note may converge with arbitrarily many open out-of-scope comments — by design. Out-of-scope comments are not findings against the note; they are signals that the lattice needs structural work.

---

## 5 Properties

### 5.1 Safety

Inherits S1–S6 from the convergence module. Adds:

**N1 (Out-of-scope non-blocking).** A `comment.out-of-scope` link never creates a resolution obligation on the target note. The convergence predicate ignores `comment.out-of-scope` links entirely.

**N2 (Out-of-scope durability).** A `comment.out-of-scope` link, once created, persists until maturation acts on it. The link is the substrate-level record that a question exists outside the current note. Out-of-scope is never silently dropped.

### 5.2 Quality boundary

**Content balance.** Notes hold at roughly 90/10 prose-to-formal — higher prose ratio than claim files (70/30) because discovery is generative. See [The Coupling Principle](../principles/coupling.md).

**Voice discipline.** Both reviewer and reviser operate under the Dijkstra voice. See [The Voice Principle](../principles/voice.md).

### 5.3 Liveness

Inherits L1–L4 from the convergence module.

### 5.4 Deliberate non-guarantees

In addition to the convergence module's:

**No guarantee on out-of-scope routing.** The protocol files `comment.out-of-scope` links but does not guarantee maturation will consume them. Routing is maturation's responsibility.

**No prescription of channel architecture.** This protocol reviews whatever note exists. The two-channel theory/evidence architecture that produces a note's initial draft is a discovery-stage concern, not a note-convergence concern.

---

## 6 Composition

### Within the maturation protocol

The [maturation protocol](maturation-protocol.md) decides when to activate this protocol — on an initial draft, on re-entry after a lattice operation, or on any other condition maturation defines. Maturation deactivates this protocol when the convergence predicate holds and sustained quiet is observed. Activation and deactivation conditions are maturation's responsibility, not this protocol's.

`comment.out-of-scope` indications are the signal surface for maturation's lattice operations — extract, absorb, and scope promotion. The note convergence protocol generates these signals. What maturation does with them is maturation's concern. See [maturation protocol §Lattice operations](maturation-protocol.md#lattice-operations).

---

## Related

- [Convergence Protocol](convergence-protocol.md) — the document-type-neutral module this protocol specializes.
- [Claim Convergence Protocol](claim-convergence-protocol.md) — the sibling specialization at claim scale.
- [Review/Revise Iteration](../patterns/review-revise-iteration.md) — the empirical pattern underlying this protocol. Battle-tested across a dozen ASNs.
- [Maturation Protocol](maturation-protocol.md) — the meta-protocol that activates note convergence and executes lattice operations on its signals.
- [Discovery](../discovery.md) — the broader narrative description of the discovery stage.
- [Production Drive](../design-notes/production-drive.md) — the LLM behavioral force. At note scale, OUT_OF_SCOPE is the off-ramp.
- [Scope Promotion](../patterns/scope-promotion.md) — the lattice operation triggered by out-of-scope signals.
- [Extract/Absorb](../patterns/extract-absorb.md) — lattice operations triggered by structural signals.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.