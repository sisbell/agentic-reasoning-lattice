# Claim Convergence Protocol

The convergence protocol applied to claims in the lattice. Adds lattice structure (`claim`, `contract`, `citation` links), structural validation, and a specific algorithm for driving convergence through reviewer/reviser choreography.

---

## 1 Modules used

### 1.1 Convergence protocol

The [convergence protocol](convergence-protocol.md) provides the predicate, the comment/resolution link types, and the safety/liveness properties. This module inherits all of them. The convergence predicate applied to claims:

> For every document with a `claim` classifier, every `comment.revise` link targeting that claim has a matching `resolution` link.

### 1.2 Structural validation

A mechanical checker that evaluates claim documents against a structural contract and produces violation reports.

**Properties relied upon.**

- SV1 (Completeness). Every violation of the structural contract is reported.
- SV2 (Soundness). Every reported violation is a genuine violation.
- SV3 (Determinism). Given the same input, the validator produces the same output. No LLM, no judgment.

---

## 2 Claim-specific link types

These link types extend the convergence protocol's vocabulary for the claim domain:

| Type | Subtypes | Role |
|---|---|---|
| `claim` | (flat, one-sided) | Classifier: document is a claim |
| `contract` | `axiom`, `definition`, `theorem`, `corollary`, `lemma`, `consequence`, `design-requirement` | Formal structure attached to a claim. Subtypes name structural kinds. |
| `citation` | (flat) | Claim depends on claim |

Combined with the convergence protocol's three link types (`review`, `comment`, `resolution`), the claim convergence protocol operates with six link types total.

### Two layers on one graph

The `citation` link is the lattice edge. The lattice — the dependency structure of claims — is the citation subgraph of the link graph. Meets and joins are operations on this subgraph:

- **Meet** (extract): a new claim is created below two consumers that independently derived the same concept. Both get `citation` links pointing to it. The shared concept has a home.
- **Join** (scope promotion): a new claim is created above existing foundations. It gets `citation` links pointing down to what it builds on.

The convergence protocol's link types (`review`, `comment`, `resolution`) are protocol machinery operating on the lattice. Reviews observe claims. Comments target them. Resolutions close comments. None of these change the dependency structure — they check whether the existing structure is sound.

The two layers interact when the reviser creates a new claim as part of closing a comment — apparatus extraction promotes inline reasoning to a named claim. The `resolution.edit` that closes the comment also adds a node to the lattice (new `claim` classifier, new `citation` links). Protocol activity produces lattice growth.

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

### Claim-specific events

In addition to the convergence protocol's events:

**Requests.**

- ⟨ RegisterClaim | doc ⟩ — attach a `claim` classifier to doc, admitting it to the lattice.
- ⟨ Cite | source, target ⟩ — create a `citation` link from source to target.
- ⟨ AttachContract | claim, kind ⟩ — create a `contract` link of subtype kind on claim.

---

## 4 Claim-specific properties

These extend the convergence protocol's safety and liveness properties:

### Safety

**CS1 (Structural soundness).** No `comment` link is created on a claim whose structural validation has not been satisfied since its last edit. This is a protocol-level constraint on all implementations — any algorithm implementing this protocol must validate before review. (Relies on SV1, SV2.)

### Quality boundary

These are content quality targets monitored across review cycles. Unlike safety properties, they are not graph properties evaluable from link state — they require inspection of document content. They are conditions the [principles](../principles/README.md) describe and the choreography monitors.

**Content balance.** Claim files hold at roughly 70/30 prose-to-formal. Divergence signals decoupling. See [The Coupling Principle](../principles/coupling.md).

**Voice discipline.** Both reviewer and reviser operate under positive style structure. See [The Voice Principle](../principles/voice.md).

---

## 5 Algorithm: iterative convergence

Implements: Claim Convergence Protocol (§1–§4) over the [Convergence Protocol](convergence-protocol.md).
Uses: Substrate, Reviewer agent (R), Reviser agent (V), Structural Validation (§1.2).

The algorithm engages a scope — a single claim, a cone, or an entire ASN — and drives the predicate true through cycles of review and revise. Each cycle is a deterministic sequence of agent invocations against the substrate. Convergence is decided by the substrate's predicate, never by an agent's verdict alone.

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

For every `comment.revise` on scope without a matching `resolution`, invoke V on the comment with its finding. V either edits the claim and emits ⟨ ResolveEdit ⟩, or refuses and emits ⟨ ResolveReject ⟩ with rationale document.

### 5.4 Validate

Invoke structural validation on scope. For every violation, apply the corresponding fix recipe. Repeat until SV1 reports zero violations. This enforces CS1 — no review operates on structurally unsound state.

### 5.5 Review

Invoke R on scope with assembled context. R returns the set fs of findings, each classified as `comment.revise` or `comment.observe`.

### 5.6 EmitFindings

For each finding in fs: register the finding document, file the corresponding comment via ⟨ FileComment ⟩, and record the review event. After EmitFindings, every finding is observable through the substrate.

### 5.7 Revise

For each new `comment.revise` filed in the current cycle, invoke V. V resolves the comment as in §5.3.

---

## 6 Correctness

### Safety (S1, S5 — indication soundness)

If ⟨ Converged | scope ⟩ is indicated, the predicate holds at that moment.

*Argument.* The algorithm indicates Converged only after IsConverged?(scope) returns true. By the convergence protocol's S1, every revise comment on scope has a matching resolution at evaluation time. By SUB1, neither comments nor resolutions are removable; the predicate's truth at indication persists until new comments arrive.

### Liveness (L1 — reviser responsiveness)

If V always produces a resolution for the comment it is given, then for every open revise comment on scope, eventually a resolution exists.

*Argument.* Open comments persist across invocations (SUB1, S3). At the start of every cycle, RetryOpenRevises (§5.3) re-feeds every open revise comment on scope to V. Under the assumption, V produces a closing resolution. Within at most one cycle per comment, all open comments are resolved.

### Bounded work per engagement

Each Engage performs at most N + 1 review invocations and at most N revise rounds.

*Argument.* The cycle structure (§5.2) bounds work-loop reviews by N. The confirmation contributes one additional review and zero revise rounds.

### Cross-invocation progress (L4)

If Engage i exits NotConverged with k open revise comments, then Engage (i + 1) begins its first retry pass with k re-feedings. Under the responsiveness assumption, all k close within (i + 1)'s first cycle.

*Argument.* By SUB1, the k open comments persist between invocations. RetryOpenRevises is the first action of each cycle.

---

## 7 Composition

### Within the maturation protocol

The [maturation protocol](maturation-protocol.md) activates claim convergence when blueprinting's predicate holds and claim convergence's preconditions are met — structural form satisfies the [Claim File Contract](../design-notes/claim-file-contract.md).

```
Module: Maturation
  Uses: Discovery, Blueprinting, ClaimConvergence, Verification
  
  Transition: Blueprinting → ClaimConvergence
    Precondition: structural validation returns zero violations
    Artifact: claim file set satisfying the claim file contract
  
  Transition: ClaimConvergence → Verification
    Precondition: ⟨ Converged ⟩ indicated, coverage met
    Artifact: claim files with formally precise contracts
```

On verification failure, the failing claim re-enters the protocol via a new `comment.revise` carrying the verification failure. The predicate re-evaluates to false until resolved.

### Substrate independence

The protocol's properties are stated in terms of link existence and type, not storage mechanism. Any substrate implementation satisfying SUB1, SUB2, SUB3 supports the protocol. The current implementation uses a filesystem-backed store. The protocol is unchanged when the substrate is replaced.

---

## 8 Performance

- **Predicate evaluation.** A FindLinks query for type `comment.revise` on scope, followed by a FindNumLinks query for type `resolution` against each returned comment. Linear in the number of revise comments on scope.
- **Cycle cost.** Dominated by R and V invocations. Bounded by N + 1 reviews and N revise rounds per Engage.
- **Substrate query cost.** Logarithmic in substrate size at expected scales.
- **Cross-invocation cost.** Engages iterate only currently open work, not full history.

---

## Related

- [Convergence Protocol](convergence-protocol.md) — the document-type-neutral module this protocol extends.
- [Review/Revise Iteration](../patterns/review-revise-iteration.md) — the empirical pattern underlying this protocol. Observed independently across discovery and claim convergence.
- [Validate Before Review](../patterns/validate-before-review.md) — the pattern underlying CS1.
- [The Validation Principle](../principles/validation.md) — structural integrity as a precondition for meaningful review.
- [The Coupling Principle](../principles/coupling.md) — content balance (§4 quality boundary).
- [The Voice Principle](../principles/voice.md) — output quality discipline for reviewer and reviser.
- [Production Drive](../design-notes/production-drive.md) — the LLM behavioral force motivating the revise/observe classification.
- [Maturation Protocol](maturation-protocol.md) — the meta-protocol composing this module with other stage protocols.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.