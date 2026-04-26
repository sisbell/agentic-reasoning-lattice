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

## 6 Algorithm: iterative convergence

Implements: Note Convergence Protocol (§1–§5) over the [Convergence Protocol](convergence-protocol.md).
Uses: Substrate, Reviewer agent (R), Reviser agent (V).

The algorithm engages a note and drives the predicate true through cycles of review and revise. Each cycle is a deterministic sequence of agent invocations against the substrate. Convergence is decided by the substrate's predicate, never by an agent's verdict alone.

### 6.1 State

- *note* — the engaged note.
- N — work-cycle bound. Implementation-defined; typical values reflect empirical convergence depth (notes converge in 15–30 cycles).
- k — current cycle index.
- *naturallyConverged* — boolean; set when a work cycle observes both predicate truth and a quiet review.

### 6.2 Cycle

```
upon ⟨ Engage | note, N ⟩ do
  k ← 0
  naturallyConverged ← false

  while k < N do
    k ← k + 1
    RetryOpenRevises(note)              ; §6.3
    fs ← Review(note)                   ; §6.4
    EmitFindings(note, fs)              ; §6.5
    Revise(note, fs)                    ; §6.6
    if no comment.revise was filed in this cycle
       and IsConverged?(note) then
      naturallyConverged ← true
      break

  if not naturallyConverged then
    RetryOpenRevises(note)
    fs ← Review(note)                   ; +1 confirmation: review only
    EmitFindings(note, fs)
    if no comment.revise was filed in the confirmation
       and IsConverged?(note) then
      indicate ⟨ Converged | note ⟩
    else
      let O = OpenRevises(note)
      indicate ⟨ NotConverged | note, O ⟩
  else
    indicate ⟨ Converged | note ⟩
```

Same shape as the claim convergence algorithm (§5 of [Claim Convergence Protocol](claim-convergence-protocol.md)). Differences: no Validate step (notes have no structural-contract analog at this scale), and the scope is a single note rather than a configurable claim set.

Natural convergence (the `break` path) avoids a redundant confirmation review. If cycle K's review filed zero revise comments and the predicate is already true, that review just confirmed convergence — running another review to confirm what was just confirmed wastes an invocation. The +1 confirmation only runs when the work loop exhausted N cycles without a quiet review coinciding with predicate truth.

### 6.3 RetryOpenRevises

For every `comment.revise` on note without a matching `resolution`, invoke V on the comment with its finding. V either edits the note and emits ⟨ ResolveEdit ⟩, or refuses and emits ⟨ ResolveReject ⟩ with rationale document. `comment.out-of-scope` links are not retried — they are non-blocking and handled by maturation, not by V.

### 6.4 Review

Invoke R on note with assembled context (the note plus its citation foundations). R returns the set fs of findings, each classified as `comment.revise` or `comment.out-of-scope`.

### 6.5 EmitFindings

For each finding in fs: register the finding document, file the corresponding comment via ⟨ FileComment ⟩, and record the review event. After EmitFindings, every finding is observable through the substrate. `comment.out-of-scope` links are filed but do not enter the predicate; they are visible to maturation as signals (per N2).

### 6.6 Revise

For each new `comment.revise` filed in the current cycle, invoke V. V resolves the comment as in §6.3. `comment.out-of-scope` links filed in the current cycle are not acted on — they accumulate as signals for maturation.

---

## 7 Correctness

### Safety (S1, S5 — indication soundness)

If ⟨ Converged | note ⟩ is indicated, the predicate holds at that moment.

*Argument.* The algorithm indicates Converged only after IsConverged?(note) returns true. By the convergence protocol's S1, every revise comment on note has a matching resolution at evaluation time. By SUB1, neither comments nor resolutions are removable; the predicate's truth at indication persists until new comments arrive. `comment.out-of-scope` links do not participate in the predicate (N1), so their presence at any count does not affect the indication.

### Liveness (L1 — reviser responsiveness)

If V always produces a resolution for every `comment.revise` it is given, then for every open revise comment on note, eventually a resolution exists.

*Argument.* Open revise comments persist across invocations (SUB1, S3). At the start of every cycle, RetryOpenRevises (§6.3) re-feeds every open revise comment to V. Under the assumption, V produces a closing resolution. Within at most one cycle per comment, all open comments are resolved. `comment.out-of-scope` links are skipped per protocol — they are non-blocking and don't generate work for V.

### Bounded work per engagement

Each Engage performs at most N + 1 review invocations and at most N revise rounds.

*Argument.* The cycle structure (§6.2) bounds work-loop reviews by N. The confirmation contributes one additional review and zero revise rounds.

### Cross-invocation progress (L4)

If Engage i exits NotConverged with k open revise comments, then Engage (i + 1) begins its first retry pass with k re-feedings. Under the responsiveness assumption, all k close within (i + 1)'s first cycle.

*Argument.* By SUB1, the k open comments persist between invocations. RetryOpenRevises is the first action of each cycle.

### Out-of-scope persistence

`comment.out-of-scope` links accumulate across cycles and across invocations. They do not block convergence (N1) but remain visible to maturation indefinitely (N2). The algorithm files them but does not consume them. Whether maturation acts on them is outside this protocol's scope.

---

## 8 Composition

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