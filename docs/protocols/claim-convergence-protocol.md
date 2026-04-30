# Claim Convergence Protocol

The convergence protocol applied to claims in the lattice. Adds lattice structure (`claim`, `contract`, `citation.{depends, forward}` links), structural validation, citation resolution, and a specific algorithm for driving convergence through reviewer/reviser choreography.

---

## 1 Modules used

### 1.1 Convergence protocol

The [convergence protocol](convergence-protocol.md) provides the predicate, the comment/resolution link types, and the safety/liveness properties. This module inherits all of them. The convergence predicate applied to claims:

> For every document with a `claim` classifier, every active `comment.revise` link targeting that claim has a matching active `resolution` link.

The predicate evaluates against active links (via the substrate's ActiveLinks query). A retracted resolution no longer counts toward closing a comment.

### 1.2 Substrate

The persistent, append-only link graph. See [Substrate Module](../modules/substrate-module.md). This protocol relies on SUB1–SUB3 (inherited via the convergence protocol) and additionally on SUB4–SUB6 (retraction semantics) for citation pruning during proof evolution.

### 1.3 Structural validation

A mechanical checker that evaluates claim documents against a structural contract and produces violation reports.

**Properties relied upon.**

- SV1 (Completeness). Every violation of the structural contract is reported.
- SV2 (Soundness). Every reported violation is a genuine violation.
- SV3 (Determinism). Given the same input, the validator produces the same output. No LLM, no judgment.

### 1.4 Agent module

Claim convergence has multiple within-collective process kinds — cone-review (focused on a dependency cone) and full-review (whole-ASN). Both file `review`-shaped operations into the same substrate within a single asserter's namespace. Without agent attribution, these operations are structurally indistinguishable at the substrate level; with the [agent module](../modules/agent-module.md), each kind has a stable agent identity and the substrate can answer per-process queries (e.g., "what's the latest cone-review on this apex?").

**Operations relied upon.**

- ⟨ EmitAgent | agent_doc ⟩ — file the `agent` classifier on the agent's descriptor doc. Idempotent.
- ⟨ EmitManages | agent_doc, operation ⟩ — file a `manages` link from the agent doc to each operation link the agent produces.

**Properties relied upon.**

- A3 (Manager resolution within an asserter). Per-agent trajectory queries return a deterministic answer within an asserter's allocator.
- A6 (Classifier retraction is well-defined). Decommissioning an agent role retracts its classifier without affecting prior management history.

Implementations of claim convergence MUST emit_agent for each review-producing process at startup and emit_manages for each operation link the process files. These calls live inside the algorithm's event handlers — EmitAgent runs once before §5.2's cycle loop begins; EmitManages runs inside EmitFindings (§5.6) for review/comment links and inside Revise (§5.7) for resolution links. They do not appear as separate steps in the pseudocode, matching the existing pattern for substrate MakeLink calls. The within-cycle algorithm reads "this cycle's reviser" as scoped to the agent currently running the loop; cross-invocation queries (e.g., "did the most recent cone-review on this apex converge?") rely on agent-scoped manages links.

---

## 2 Claim-specific link types

These link types extend the convergence protocol's vocabulary for the claim domain:

| Type | Subtypes | Role |
|---|---|---|
| `claim` | (flat, one-sided) | Classifier: document is a claim |
| `contract` | `axiom`, `definition`, `theorem`, `corollary`, `lemma`, `consequence`, `design-requirement` | Formal structure attached to a claim. Subtypes name structural kinds. |
| `citation` | `depends`, `forward`, `resolve` | Directional link between claims (`depends` / `forward`) plus classifier on citation-resolve outputs (`resolve`). Bare `citation` is invalid — every write must specify a subtype. |
| `provenance` | `derivation` (among others) | Audit chain. Citation-resolve emits `provenance.derivation` from each resolve doc to every citation link (and retraction) it produced, making the resolution traceable end-to-end. |

Combined with the convergence protocol's three link types (`review`, `comment`, `resolution`), the claim convergence protocol works with seven link types total. It also uses substrate-provided `retraction` (per §1.2) to nullify stale `citation.depends` and `citation.forward` links when reasoning evolves.

### Two layers on one graph

The `citation.depends` link is the lattice edge. The lattice — the dependency structure of claims — is the `citation.depends` subgraph of the link graph. Three operations act on this subgraph:

- **Meet** (extract): a new claim is created below two consumers that independently derived the same concept. Both get `citation.depends` links pointing to it. The shared concept has a home.
- **Join** (scope promotion): a new claim is created above existing foundations. It gets `citation.depends` links pointing down to what it builds on.
- **Prune** (retraction): a `citation.depends` link that no longer reflects the current reasoning is nullified by a `retraction` link. The claim and its former dependency both remain. The edge between them no longer counts. (Forward citations are pruned the same way when a claim stops naming a downstream concept; pruning a `citation.forward` is structural cleanup, not lattice reshaping, since forward citations don't participate in the dependency lattice.)

`citation.forward` is the *non-lattice* directional link — a claim names a downstream claim (a refinement, an elaboration, a navigation pointer) without depending on it. Forward citations are scaffolding for the reader, not grounding for the reasoning. They appear in a claim's `*Forward References:*` section and as `citation.forward` links in the substrate, but they do not participate in the dependency lattice. None of meet, join, or prune act on them.

Meet and join grow the lattice — they add nodes and `citation.depends` edges. Prune tightens it — it removes edges without changing any node. All three are structural operations; none affects the convergence predicate, which operates on `comment` and `resolution` links, not citations.

The convergence protocol's link types (`review`, `comment`, `resolution`) are protocol machinery operating on the lattice. Reviews observe claims. Comments target them. Resolutions close comments. None of these change the dependency structure — they check whether the existing structure is sound.

The two layers interact when the reviser creates a new claim as part of closing a comment — apparatus extraction promotes inline reasoning to a named claim. The `resolution.edit` that closes the comment also adds a node to the lattice (new `claim` classifier, new citations). Protocol activity produces lattice growth. And when a `resolution.edit` removes a dependency from a proof, the reviser files a `retraction` link on the corresponding `citation.depends` — protocol activity produces lattice pruning.

### Retraction and proof evolution

When a proof revision removes a use-site for a dependency, the original `citation.depends` link cannot be deleted (SUB1) but should no longer count toward the dependency graph. The protocol uses the substrate's retraction mechanism ([SUB4–SUB5](../modules/substrate-module.md)) to nullify the stale citation. This is the **prune** operation — the lattice loses an edge without changing any node. The same retraction mechanism applies to `citation.forward` when a claim's prose stops naming a downstream concept; pruning a forward citation does not change the dependency lattice but cleans up the substrate's record of who-names-whom.

Retraction of a `resolution` link re-opens the comment it closed. The convergence predicate evaluates against active links, so the retracted resolution no longer counts — the comment becomes unresolved and re-enters the reviser's work queue on the next RetryOpenRevises pass. Retraction semantics (shadow interpretation, idempotence, depth behavior) are specified in the [Substrate Module](../modules/substrate-module.md).

### Retraction tooling

The reviser invokes `scripts/substrate/retract.py --to <label>` to file a retraction during a revision that removes a dependency from a claim's `*Depends:*` section. All consumers that build citation graphs (validator, dependency-graph builder, cone-sweep, citation-resolve) use the substrate's ActiveLinks query rather than FindLinks directly. `emit_citation` itself uses ActiveLinks for its idempotency check — a previously-retracted citation does not block re-emission, so re-typing a label after it was retracted produces a fresh active link.

---

## 3 Claim-specific participants

These extend the convergence protocol's reviewer and reviser with claim-domain behavior:

### Validator

Checks all claim documents against a structural contract before each review. Violations resolve through targeted fix recipes before the reviewer sees the state. Mechanical, no LLM. Instantiates the [validate-before-review](../patterns/validate-before-review.md) pattern.

### Reviewer (claim-specific)

Inherits the convergence protocol's reviewer role. Additionally operates in the Dijkstra voice — speaks only when genuinely compelled. Classifies findings as `comment.revise` or `comment.observe`.

### Reviser (claim-specific)

Inherits the convergence protocol's reviser role. Additionally operates in the Dijkstra voice — every formal statement justified where introduced. On `resolution.edit`, every commitment present before the edit is present after. The reviser is a structural editor: edits change where content lives, promote reasoning into better form. On `resolution.reject`, creates a rejection rationale document — a first-class document in the link graph, addressable and reviewable.

### Scope assembler

Constructs the context the reviewer sees. The scope strategy (adaptive, comprehensive, or any other) is a choreography decision. The protocol defines no scope strategies — only the predicate that any choreography must satisfy.

For dependency-cone reviews specifically, the scope assembler walks the substrate's `citation.depends` graph transitively from the apex, returning the apex plus every same-ASN claim reachable through backward grounding. Cross-ASN deps are delivered separately via curated foundation summaries. `citation.forward` is deliberately not followed — the cone is the apex's grounding chain, not its downstream tree.

### Citation Resolver

A lattice-construction participant. For each claim in scope, types every claim-label reference appearing in the claim's prose into one of two directions:

- `citation.depends` — the claim's correctness rests on the cited claim (backward).
- `citation.forward` — the claim names the cited claim as a downstream concept and stands without it (forward).

Operates per claim, no DAG order — each claim's classifications depend only on its own prose, the substrate's existing classifications for that claim, and the bodies of referenced claims (read on demand). Labels appearing in the prose but absent from the substrate are validated against the cross-ASN label index; invalid labels fail loudly.

Outputs a `citation-resolve` document per claim per run (only when classifications or retractions are produced), classified in the substrate as `citation.resolve`, with `provenance.derivation` links from the resolve doc to every citation/retraction it emitted.

Citation-resolve is the protocol's lattice-builder. The reviewer/reviser pair acts on a typed lattice; citation-resolve produces it. It runs as a distinct stage (§5.X) — not interleaved per cycle — because soundness review and lattice construction are separable concerns.

### Claim-specific events

In addition to the convergence protocol's events:

**Requests.**

- ⟨ RegisterClaim | doc ⟩ — attach a `claim` classifier to doc, admitting it to the lattice.
- ⟨ Cite | source, target, direction ⟩ — create a `citation.<direction>` link from source to target. `direction` ∈ {`depends`, `forward`}.
- ⟨ AttachContract | claim, kind ⟩ — create a `contract` link of subtype kind on claim.
- ⟨ Retract | link_id ⟩ — create a `retraction` link nullifying the referenced link.
- ⟨ ResolveCitations | claim ⟩ — invoke citation-resolve on claim; types every label reference in its prose.

---

## 4 Claim-specific properties

The claim convergence protocol adds the following properties to those inherited from the [convergence protocol](convergence-protocol.md) (S1–S6, L1–L4):

### Safety

**CS1 (Structural soundness).** No `comment` link is created on a claim whose structural validation has not been satisfied since its last edit. This is a protocol-level constraint on all implementations — any algorithm implementing this protocol must validate before review. (Relies on SV1, SV2.)

**CS2 (Retraction idempotence).** A `retraction` link targeting an already-retracted link does not change the computed active-link set. Multiple retractions of the same link are permitted and produce the same graph state as a single retraction.

### Quality boundary

These are content quality targets monitored across review cycles. Unlike safety properties, they are not graph properties evaluable from link state — they require inspection of document content. They are conditions the [principles](../principles/README.md) describe and the choreography monitors.

**Content balance.** Claim files hold at roughly 70/30 prose-to-formal. Divergence signals decoupling. See [The Coupling Principle](../principles/coupling.md).

**Voice discipline.** Both reviewer and reviser operate under positive style structure. See [The Voice Principle](../principles/voice.md).

---

## 5 Algorithm: iterative convergence

Implements: Claim Convergence Protocol (§1–§4) over the [Convergence Protocol](convergence-protocol.md).
Uses: Substrate, Reviewer agent (R), Reviser agent (V), Structural Validation (§1.2).

The algorithm engages a scope — a single claim, a cone, or an entire ASN — and drives the predicate true through cycles of review and revise. Each cycle is a deterministic sequence of agent invocations against the substrate. Convergence is decided by the substrate's predicate, never by an agent's verdict alone.

Agent attribution is bookkeeping at file time, not a control-flow concern of the algorithm. Operation links filed inside EmitFindings (§5.6) and Revise (§5.7) carry `manages` attribution per §1.4; the natural-convergence check in §5.2 counts `comment.revise` filed in this cycle by this cycle's reviser, scoped implicitly because the loop is single-threaded.

### 5.1 State

- scope — the engaged claim set (a single claim, a cone, or an entire ASN).
- N — work-cycle bound. Typical values: 8 for cone-level engagement, 8 for ASN-level. The bound prevents unbounded cost; cross-invocation progress (L4) ensures work resumes where it left off.
- k — current cycle index.
- *naturallyConverged* — boolean; set when a work cycle observes both predicate truth and a quiet review.

### 5.2 Cycle

```
upon ⟨ Engage | scope, N ⟩ do
  k ← 0
  naturallyConverged ← false

  while k < N do
    k ← k + 1
    RetryOpenRevises(scope)             ; §5.3
    Validate(scope)                     ; §5.4
    fs ← Review(scope)                  ; §5.5
    EmitFindings(scope, fs)             ; §5.6
    Revise(scope, fs)                   ; §5.7
    if no comment.revise was filed in this cycle
       and IsConverged?(scope) then
      naturallyConverged ← true
      break

  if not naturallyConverged then
    RetryOpenRevises(scope)
    Validate(scope)
    fs ← Review(scope)                  ; +1 confirmation: review only
    EmitFindings(scope, fs)
    if no comment.revise was filed in the confirmation
       and IsConverged?(scope) then
      indicate ⟨ Converged | scope ⟩
    else
      let O = OpenRevises(scope)
      indicate ⟨ NotConverged | scope, O ⟩
  else
    indicate ⟨ Converged | scope ⟩
```

Natural convergence (the `break` path) avoids a redundant confirmation review. If cycle K's review filed zero revise comments and the predicate is already true, that review just confirmed convergence — running another review to confirm what was just confirmed wastes an invocation. The +1 confirmation only runs when the work loop exhausted N cycles without a quiet review coinciding with predicate truth.

### 5.3 RetryOpenRevises

For every active `comment.revise` on scope without a matching active `resolution`, invoke V on the comment with its finding. V either edits the claim and emits ⟨ ResolveEdit ⟩, or refuses and emits ⟨ ResolveReject ⟩ with rationale document.

### 5.4 Validate

Invoke structural validation on scope. For every violation, apply the corresponding fix recipe. Repeat until SV1 reports zero violations. This enforces CS1 — no review operates on structurally unsound state.

### 5.5 Review

Invoke R on scope with assembled context. R returns the set fs of findings, each classified as `comment.revise` or `comment.observe`.

### 5.6 EmitFindings

Emits the substrate facts for one review event. First, ⟨ FileReview | aggregate_doc ⟩ classifies the aggregate review document. Then, for each finding in fs: invoke ⟨ FileFinding | aggregate_doc, finding_doc, target_claim, class, body ⟩ — writes the finding doc, classifies it as `finding`, files a `comment.<class>` link from the finding doc to the target claim, and files a `provenance.derivation` link from the aggregate to the finding doc. After EmitFindings completes, the substrate carries one `review` link, N `finding` links, N `comment.<class>` links, and N `provenance.derivation` links — each finding is observable both as a standalone substrate citizen and as a derivation of the aggregate review event that produced it.

### 5.7 Revise

For each new `comment.revise` filed in the current cycle, invoke V. V resolves the comment as in §5.3. When a revision removes a dependency from a claim's proof, the reviser files a ⟨ Retract ⟩ on the corresponding `citation.depends` (or `citation.forward`) link — pruning the lattice edge that no longer reflects the reasoning.

### 5.8 ResolveCitations (lattice-builder stage)

Distinct from the iterative cycle of §5.2: a one-pass-per-claim transformation that types every claim-label reference in a claim's prose. Composed with §5.2 — typically run before engaging a scope so the cycle operates on a typed lattice — and not interleaved per cycle.

```
upon ⟨ ResolveCitations | claim ⟩ do
  existing_depends  ← active_links(citation.depends, from=claim)
  existing_forwards ← active_links(citation.forward,  from=claim)

  ⟨ classifications, retractions ⟩ ← Classify(claim, existing_depends, existing_forwards)
                                        ; one focused agent call; outputs structured

  if classifications = ∅ and retractions = ∅ then
    return ⟨ Resolved | claim, no-op ⟩    ; idempotent: no resolve doc, no commit

  validate_labels(classifications, retractions)   ; cross-ASN label index lookup; fail-loud

  apply_md_changes(claim, classifications, retractions)
                                        ; insert bullets in *Depends:* / *Forward References:*;
                                        ; remove bullets for retractions; dedup against
                                        ; labels already in the section
  resolve_doc ← persist_resolve_output(claim, classifications, retractions)

  emit_classifier(citation.resolve, on=resolve_doc)
  for c in classifications:
    link ← Cite(claim, c.label, c.direction)
    emit_provenance(derivation, from=resolve_doc, to=link)
  for r in retractions:
    link ← Retract(active_citation(claim, r.label, r.direction))
    emit_provenance(derivation, from=resolve_doc, to=link)

  indicate ⟨ Resolved | claim, |classifications|, |retractions| ⟩
```

The agent's classification call (Classify) takes the claim's `.md`, the substrate-sourced lists of already-classified labels, and produces the new `(classifications, retractions)`. The orchestrator validates labels against the cross-ASN index, then performs the substrate writes — Cite, Retract, classifier, provenance — atomically per claim. If Sonnet returns a label that doesn't resolve, validation fails before any write.

A no-op call (Sonnet finds nothing to classify and nothing to retract) produces no resolve doc and no substrate writes, by design — the audit trail records changes, not checks.

`Cite(claim, label, direction)` calls `emit_citation` which uses ActiveLinks for its idempotency check (§3 Retraction tooling). A previously-retracted citation does not block a fresh emission — re-typing a label after retraction creates a new active link, with the prior retraction left in place as audit history.

ResolveCitations composes naturally with the iterative cycle: typed citations populate the substrate before §5.2 begins; cycle-internal revisions can then file new ⟨ Cite ⟩ events through the reviser without needing a separate resolve pass — until a revise creates a new claim or substantially restructures references, at which point ResolveCitations on the affected claims keeps the lattice typed.

---

## 6 Correctness

### Safety (S1, S5 — indication soundness)

If ⟨ Converged | scope ⟩ is indicated, the predicate holds at that moment.

*Argument.* The algorithm indicates Converged only after IsConverged?(scope) returns true. By the convergence protocol's S1, every active `comment.revise` on scope has a matching active `resolution` at evaluation time. By SUB1, neither comments nor resolutions are removable; the predicate's truth at indication persists until new comments arrive or a `resolution` is retracted (per SUB4–SUB5).

### Liveness (L1 — reviser responsiveness)

If V always produces a resolution for the comment it is given, then for every open revise comment on scope, eventually a resolution exists.

*Argument.* Open comments persist across invocations (SUB1, S3). At the start of every cycle, RetryOpenRevises (§5.3) re-feeds every open revise comment on scope to V. Under the assumption, V produces a closing resolution. Within at most one cycle per comment, all open comments are resolved.

### Bounded work per engagement

Each Engage performs at most N + 1 review invocations and at most N revise rounds.

*Argument.* The cycle structure (§5.2) bounds work-loop reviews by N. The confirmation contributes one additional review and zero revise rounds.

### Cross-invocation progress (L4)

If Engage i exits NotConverged with k open revise comments, then Engage (i + 1) begins its first retry pass with k re-feedings. Under the responsiveness assumption, all k close within (i + 1)'s first cycle.

*Argument.* By SUB1, the k open comments persist between invocations. RetryOpenRevises is the first action of each cycle.

### Retraction and convergence (CS2)

Retraction of a `citation.depends` or `citation.forward` link does not affect the convergence predicate — citation retraction changes the lattice's dependency structure (for `citation.depends`) or the structural reference record (for `citation.forward`), but doesn't affect any active `comment.revise` or active `resolution`, so the predicate is unchanged.

Retraction of a `resolution` link *does* affect the convergence predicate — the retracted resolution no longer counts (per SUB5, active state evaluation), and the comment it closed becomes unresolved. The predicate goes false. The algorithm handles this through RetryOpenRevises (§5.3), which re-feeds the now-unresolved comment to the reviser on the next cycle.

CS2 (retraction idempotence) inherits from SUB6: multiple retractions of the same link produce the same graph state as a single retraction.

---

## 7 Composition

### Within the maturation protocol

The [maturation protocol](maturation-protocol.md) activates claim convergence when claim derivation's structural contract holds and claim convergence's preconditions are met — structural form satisfies the [Claim Document Contract](../design-notes/claim-document-contract.md).

```
Module: Maturation
  Uses: Discovery, ClaimDerivation, ClaimConvergence, Verification

  Transition: ClaimDerivation → ClaimConvergence
    Precondition: structural validation returns zero violations
    Artifact: claim document set satisfying the Claim Document Contract

  Transition: ClaimConvergence → Verification
    Precondition: ⟨ Converged ⟩ indicated, coverage met
    Artifact: claim documents with formally precise contracts
```

On verification failure, the failing claim re-enters the protocol via a new `comment.revise` carrying the verification failure. The predicate re-evaluates to false until resolved.

### Substrate independence

The protocol's properties are stated in terms of link existence and type, not storage mechanism. Any substrate implementation satisfying SUB1–SUB6 supports the protocol. The current implementation uses a filesystem-backed store. The protocol is unchanged when the substrate is replaced.

---

## 8 Performance

- **Predicate evaluation.** An ActiveLinks query for type `comment.revise` on scope, followed by an ActiveLinks query for type `resolution` against each returned comment. Linear in the number of active revise comments on scope.
- **Cycle cost.** Dominated by R and V invocations. Bounded by N + 1 reviews and N revise rounds per Engage.
- **Substrate query cost.** Logarithmic in substrate size at expected scales.
- **Cross-invocation cost.** Engages iterate only currently open work, not full history.
- **Retraction cost.** ActiveLinks adds one substrate query for `retraction` links beyond what FindLinks would do. Bounded by the number of retracted links, which is small relative to total citations.

---

## Related

- [Convergence Protocol](convergence-protocol.md) — the document-type-neutral module this protocol extends.
- [Substrate Module](../modules/substrate-module.md) — the persistent link graph. Provides retraction semantics (SUB4–SUB6) used for citation pruning.
- [Agent Module](../modules/agent-module.md) — the agent identity and management-attribution layer this protocol depends on (per §1.4). Cone-review and full-review file `agent` and `manages` links so per-process trajectories are queryable from the substrate.
- [Note Convergence Protocol](note-convergence-protocol.md) — the sibling specialization at note scale.
- [Review/Revise Iteration](../patterns/review-revise-iteration.md) — the empirical pattern underlying this protocol. Observed independently across discovery and claim convergence.
- [Validate Before Review](../patterns/validate-before-review.md) — the pattern underlying CS1.
- [The Validation Principle](../principles/validation.md) — structural integrity as a precondition for meaningful review.
- [The Coupling Principle](../principles/coupling.md) — content balance (§4 quality boundary).
- [The Voice Principle](../principles/voice.md) — output quality discipline for reviewer and reviser.
- [Production Drive](../design-notes/production-drive.md) — the LLM behavioral force motivating the revise/observe classification.
- [Maturation Protocol](maturation-protocol.md) — the meta-protocol composing this module with other stage protocols.
- [Claim Convergence](../claim-convergence.md) — rationale: why two scopes, why local was retired, the T3 incident, the multigrid analogy.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.