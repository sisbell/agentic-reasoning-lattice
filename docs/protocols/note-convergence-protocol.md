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

This protocol also uses substrate-provided `retraction` (per §2.2) to nullify stale `citation` links left behind by [maturation](maturation-protocol.md) operations.

The `citation` link is the lattice edge at note scale. The note dependency graph — which notes assume foundations from which — is the citation subgraph. Note convergence operates on individual notes; the citation graph is what maturation traverses to decide what enters convergence next.

### Retraction after absorb and extract

The [maturation protocol](maturation-protocol.md)'s lattice operations restructure note content without removing the substrate links from prior states:

- **Absorb** moves material from one note into another. The source note's outbound citations may become stale — claims that depended on a now-departed prefix no longer have a use-site for those citations.
- **Extract** spins claims out into a new foundation note. The original note retains a citation to the new foundation but loses the citations it had into the now-redundant claims that were extracted.

The protocol uses the substrate's retraction mechanism ([SUB4–SUB5](substrate.md)) to nullify these stale citations. The reviser during a re-entry note-convergence cycle (which the maturation protocol triggers after each operation) inspects the note's prose, identifies citations no longer supported by use-sites, and files retractions via ⟨ Retract ⟩. Retraction of a `resolution` link re-opens the comment it closed — the convergence predicate evaluates against active links, so the retracted resolution no longer counts. Retraction semantics (shadow interpretation, idempotence, depth behavior) are specified in the [Substrate Module](substrate.md).

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

Provides the predicate, comment/resolution machinery, and core safety and liveness properties. See [convergence protocol](convergence-protocol.md). The predicate evaluates against active links.

**Properties inherited.** S1–S6, L1–L4.

### 2.2 Substrate

The persistent, append-only link graph. See [Substrate Module](substrate.md). This protocol relies on SUB1–SUB3 (inherited via the convergence protocol) and additionally on SUB4–SUB6 (retraction semantics) for stale citation handling after lattice operations.

### 2.3 Agent module

Note convergence currently has a single within-collective process kind (note-review). The protocol carries the agent-attribution requirement to keep the substrate structurally unambiguous against future expansion — e.g., adding a focused-review kind, or running side-by-side with another note-revising activity within the same collective. Pre-instrumenting avoids retrofit; the single-process current state trivially satisfies the per-agent trajectory contract.

**Operations relied upon.**

- ⟨ EmitAgent | agent_doc ⟩ — file the `agent` classifier on the note-review agent's descriptor doc. Idempotent.
- ⟨ EmitManages | agent_doc, operation ⟩ — file a `manages` link from the agent doc to each operation link the agent produces.

**Properties relied upon.**

- A3 (Manager resolution within an asserter). Per-agent trajectory queries return a deterministic answer within an asserter's allocator.
- A6 (Classifier retraction is well-defined).

Implementations of note convergence MUST emit_agent for the note-review process at startup and emit_manages for each operation link it files. These calls live inside the algorithm's event handlers — EmitAgent runs once before §6.2's cycle loop begins; EmitManages runs inside EmitFindings (§6.5) for review/comment links and inside Revise (§6.6) for resolution links. They do not appear as separate steps in the pseudocode, matching the existing pattern for substrate MakeLink calls.

---

## 3 Participants and events

### Reviewer

Inherited from convergence module. Reads assembled context and produces comment links on notes. Comments classified as `comment.revise` or `comment.out-of-scope`. Operates in the Dijkstra voice.

### Reviser

Inherited from convergence module. Resolves `comment.revise` links via `resolution.edit` (note edited) or `resolution.reject` (finding refused with rationale document). Takes no action on `comment.out-of-scope` — those are non-blocking and handled by the maturation protocol. During re-entry cycles after lattice operations, the reviser also identifies stale citations and files retractions.

### Scope assembler

Constructs the context the reviewer sees. The scope strategy is a choreography decision; the protocol prescribes nothing.

### Events

The events from the [convergence module](convergence-protocol.md) operate identically with note-typed targets. Three additional requests:

- ⟨ RegisterNote | doc ⟩ — attach a `note` classifier to doc.
- ⟨ Cite | source, target ⟩ — create a `citation` link from source note to target note.
- ⟨ Retract | link_id ⟩ — create a `retraction` link nullifying the referenced link.

All other requests (FileComment, ResolveEdit, ResolveReject, EvaluateConvergence) and indications (CommentFiled, ResolutionFiled, Converged, NotConverged) are inherited unchanged. The `comment.out-of-scope` class in CommentFiled indications is the signal maturation subscribes to for lattice operations.

---

## 4 Convergence

Inherits the predicate from the [convergence protocol](convergence-protocol.md):

> For every active `comment.revise` link targeting the note, there exists a matching active `resolution` link.

`comment.out-of-scope` links do not participate. A note may converge with arbitrarily many open out-of-scope comments — by design. Out-of-scope comments are not findings against the note; they are signals that the lattice needs structural work.

Retraction of a `citation` link does not affect the convergence predicate — citation retraction changes the note's dependency graph but doesn't affect any active `comment.revise` or active `resolution`, so the predicate is unchanged. Retraction of a `resolution` link does affect the predicate — the retracted resolution no longer counts, and the comment it closed becomes unresolved again.

---

## 5 Properties

### 5.1 Safety

The note convergence protocol adds the following safety properties to those inherited from the [convergence protocol](convergence-protocol.md) (S1–S6) and relies on [substrate](substrate.md) properties SUB4–SUB6 for retraction:

**N1 (Out-of-scope non-blocking).** A `comment.out-of-scope` link never creates a resolution obligation on the target note. The convergence predicate ignores `comment.out-of-scope` links entirely.

**N2 (Out-of-scope durability).** A `comment.out-of-scope` link, once created, persists until maturation acts on it. The link is the substrate-level record that a question exists outside the current note. Out-of-scope is never silently dropped.

**N3 (Retraction idempotence).** A `retraction` link targeting an already-retracted link does not change the computed active-link set. Multiple retractions of the same link are permitted and produce the same graph state as a single retraction.

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

Agent attribution is bookkeeping at file time, not a control-flow concern of the algorithm. Operation links filed inside EmitFindings (§6.5) and Revise (§6.6) carry `manages` attribution per §2.3; the natural-convergence check in §6.2 counts `comment.revise` filed in this cycle by this cycle's reviser, scoped implicitly because the loop is single-threaded.

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

Same shape as the claim convergence algorithm (§5 of [Claim Convergence Protocol](claim-convergence-protocol.md)). Differences: no Validate step, and the scope is a single note rather than a configurable claim set.

Notes have no structural-contract analog at this scale. Claim files have the [Claim File Contract](../design-notes/claim-file-contract.md) — one body per file, filename matches label, references resolve, metadata agrees. Notes are prose-dominated documents whose structure is deliberately informal during discovery. Imposing a structural contract on notes would constrain the generative process that discovery depends on. Structural validation enters at note decomposition, when the representation changes to per-claim files.

Natural convergence (the `break` path) avoids a redundant confirmation review. If cycle K's review filed zero revise comments and the predicate is already true, that review just confirmed convergence — running another review to confirm what was just confirmed wastes an invocation. The +1 confirmation only runs when the work loop exhausted N cycles without a quiet review coinciding with predicate truth.

### 6.3 RetryOpenRevises

For every active `comment.revise` on note without a matching active `resolution`, invoke V on the comment with its finding. V either edits the note and emits ⟨ ResolveEdit ⟩, or refuses and emits ⟨ ResolveReject ⟩ with rationale document. `comment.out-of-scope` links are not retried — they are non-blocking and handled by maturation, not by V.

### 6.4 Review

Invoke R on note with assembled context. The scope strategy is a choreography decision (§3); typically the note plus its citation foundations. R returns the set fs of findings, each classified as `comment.revise` or `comment.out-of-scope`.

### 6.5 EmitFindings

For each finding in fs: register the finding document, file the corresponding comment via ⟨ FileComment ⟩, and record the review event. After EmitFindings, every finding is observable through the substrate. `comment.out-of-scope` links are filed but do not enter the predicate; they are visible to maturation as signals (per N2).

### 6.6 Revise

For each new `comment.revise` filed in the current cycle, invoke V. V resolves the comment as in §6.3. `comment.out-of-scope` links filed in the current cycle are not acted on — they accumulate as signals for maturation. When a revision removes a dependency from the note's prose, the reviser files a ⟨ Retract ⟩ on the corresponding `citation` link.

---

## 7 Correctness

### Safety (S1, S5 — indication soundness)

If ⟨ Converged | note ⟩ is indicated, the predicate holds at that moment.

*Argument.* The algorithm indicates Converged only after IsConverged?(note) returns true. By the convergence protocol's S1, every active `comment.revise` on note has a matching active `resolution` at evaluation time. By SUB1, neither comments nor resolutions are removable; the predicate's truth at indication persists until new comments arrive or a `resolution` is retracted (per SUB4–SUB5). `comment.out-of-scope` links do not participate in the predicate (N1), so their presence at any count does not affect the indication.

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

### Retraction and convergence (N3)

Retraction of a `citation` link does not affect the convergence predicate — citation retraction changes the note's dependency graph but doesn't affect any active `comment.revise` or active `resolution`, so the predicate is unchanged.

Retraction of a `resolution` link *does* affect the convergence predicate — the retracted resolution no longer counts (per SUB5, active state evaluation), and the comment it closed becomes unresolved. The predicate goes false. The algorithm handles this through RetryOpenRevises (§6.3), which re-feeds the now-unresolved comment to the reviser on the next cycle.

N3 (retraction idempotence) inherits from SUB6: multiple retractions of the same link produce the same graph state as a single retraction.

---

## 8 Composition

### Within the maturation protocol

The [maturation protocol](maturation-protocol.md) decides when to activate this protocol — on an initial draft, on re-entry after a lattice operation, or on any other condition maturation defines. Maturation deactivates this protocol when the convergence predicate holds and sustained quiet is observed. Activation and deactivation conditions are maturation's responsibility, not this protocol's.

`comment.out-of-scope` indications are the signal surface for maturation's lattice operations — extract, absorb, and scope promotion. The note convergence protocol generates these signals. What maturation does with them is maturation's concern. See [maturation protocol §Lattice operations](maturation-protocol.md#lattice-operations).

---

## Related

- [Convergence Protocol](convergence-protocol.md) — the document-type-neutral module this protocol specializes.
- [Substrate Module](substrate.md) — the persistent link graph. Provides retraction semantics (SUB4–SUB6) used for stale citation handling after lattice operations.
- [Agent Module](agent.md) — the agent identity and management-attribution layer this protocol depends on (per §2.3). The note-review process files `agent` and `manages` links to keep the substrate ready for future multi-process expansion.
- [Consultation Protocol](consultation-protocol.md) — the upstream producer. Generates the initial note this protocol refines.
- [Claim Convergence Protocol](claim-convergence-protocol.md) — the sibling specialization at claim scale.
- [Review/Revise Iteration](../patterns/review-revise-iteration.md) — the empirical pattern underlying this protocol. Battle-tested across a dozen ASNs.
- [Maturation Protocol](maturation-protocol.md) — the meta-protocol that activates note convergence and executes lattice operations on its signals.
- [Discovery](../discovery.md) — the broader narrative description of the discovery stage.
- [Production Drive](../design-notes/production-drive.md) — the LLM behavioral force. At note scale, OUT_OF_SCOPE is the off-ramp.
- [Scope Promotion](../patterns/scope-promotion.md) — the lattice operation triggered by out-of-scope signals.
- [Extract/Absorb](../patterns/extract-absorb.md) — lattice operations triggered by structural signals.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.