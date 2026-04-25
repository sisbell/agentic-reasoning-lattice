# Claim Convergence Protocol

The protocol that drives formalized claims to convergence. Expressed as operations on a link graph — documents and typed links as the only primitives. The protocol defines when convergence is reached. How to get there is choreography. How the choreography executes is the algorithm.

This document has three layers: the **protocol** (§1–§5, what must hold), the **algorithm** (§6, how convergence is driven), and **correctness** (§7, why the algorithm satisfies the protocol). Following the modular formalism of Cachin (*Reliable and Secure Distributed Programming*).

---

## 1 Document model

Everything the protocol manipulates is either a document (content) or a link (typed relationship between documents). There are no intrinsic document roles — a document's role comes from the classifier links attached to it.

### Document types

| Classifier | What the document is |
|---|---|
| `claim` | A claim document. Contains an assertion (prose, and optionally a formal contract). |
| `review` | A review document. Records findings from one review session. |

A document acquires its role by having the classifier link attached. No classifier, no role.

### Link types

| Type | Subtypes | Role |
|---|---|---|
| `claim` | (flat, one-sided) | Classifier: document is a claim |
| `review` | (flat, one-sided) | Classifier: document is a review |
| `contract` | `axiom`, `definition`, `theorem`, `corollary`, `lemma`, `consequence`, `design-requirement` | Formal structure attached to a claim. Subtypes name structural kinds. |
| `citation` | (flat) | Claim depends on claim |
| `comment` | `revise`, `observe` | Finding observes a claim. Subtypes classify the finding. |
| `resolution` | `edit`, `reject` | Closes a comment. Edit: the claim was changed. Reject: the finding was refused. |

Six link types. Two are document classifiers (`claim`, `review`). One attaches structure (`contract`). Three express relationships (`citation`, `comment`, `resolution`).

Subtypes are valid when they change the structure or invariants of what the link carries. `contract.axiom` has different required fields than `contract.theorem`. `comment.revise` requires resolution; `comment.observe` does not. `resolution.edit` means the claim was changed. `resolution.reject` means the claim was not changed — the finding was addressed by refusal, with a rationale document.

### Two layers on one graph

The `citation` link is the lattice edge. The lattice — the dependency structure of claims — is the citation subgraph of the link graph. Meets and joins are operations on this subgraph:

- **Meet** (extract): a new claim is created below two consumers that independently derived the same concept. Both get `citation` links pointing to it. The shared concept has a home.
- **Join** (scope promotion): a new claim is created above existing foundations. It gets `citation` links pointing down to what it builds on.

The other five link types are protocol machinery operating on the lattice. Reviews observe claims. Comments target them. Resolutions close comments. Contracts attach formal structure. None of these change the dependency structure — they check whether the existing structure is sound.

The two layers interact when the reviser creates a new claim as part of closing a comment — apparatus extraction promotes inline reasoning to a named claim. The `resolution.edit` that closes the comment also adds a node to the lattice (new `claim` classifier, new `citation` links). Protocol activity produces lattice growth.

### No versioning primitive

Documents are referenced by path, not by version. The protocol carries no versioning primitive. Git provides history as an operational concern. When Xanadu arrives, versioning re-enters as a native primitive with tumblers doing the identity work.

The absence of versioning is deliberate. A predicate that tracks "latest version" lets unresolved comments silently evaporate when the claim is edited — the old version is no longer "latest" and comments targeting it stop blocking convergence without being addressed. The simpler predicate — every `comment.revise` on a claim must have a resolution, regardless of when it was filed — closes this footgun.

---

## 2 Modules used

### 2.1 Substrate

A persistent, append-only graph of documents and typed links between them.

**Operations.**

- ⟨ MakeLink | from, to, types ⟩ — append a new link with the given endsets and type set, return its address.
- ⟨ FindLinks | home, from, to, types ⟩ — return the set of links matching the constraint conjunction. A constraint of `None` matches anything.
- ⟨ FindNumLinks | home, from, to, types ⟩ — return the count of links matching the constraints.

**Properties relied upon.**

- SUB1 (Permanence). No link is ever removed once created.
- SUB2 (Query soundness). FindLinks returns exactly the links satisfying the constraint conjunction.
- SUB3 (Count consistency). FindNumLinks(args) = |FindLinks(args)|.

### 2.2 Structural validation

A mechanical checker that evaluates claim documents against a structural contract and produces violation reports.

**Properties relied upon.**

- SV1 (Completeness). Every violation of the structural contract is reported.
- SV2 (Soundness). Every reported violation is a genuine violation.
- SV3 (Determinism). Given the same input, the validator produces the same output. No LLM, no judgment.

---

## 3 Participants and events

### Validator

Checks all claim documents against a structural contract before each review. Violations resolve through targeted fix recipes before the reviewer sees the state. Mechanical, no LLM. Instantiates the [validate-before-review](../patterns/validate-before-review.md) pattern.

### Reviewer

Reads assembled context and produces comment links on claim documents it observes. Operates in the Dijkstra voice — speaks only when genuinely compelled. Each comment is classified:

- `comment.revise` — the claim is wrong, incomplete, or ungrounded. Requires resolution.
- `comment.observe` — the claim is correct but the reviewer noticed something. Recorded, no resolution required.

OBSERVE is the off-ramp for the [production drive](../design-notes/production-drive.md). The convergence predicate tracks only REVISE comments; OBSERVE accumulates as audit trail without blocking convergence.

### Reviser

Observes unresolved `comment.revise` links and responds in one of two ways. If the finding is valid, the reviser edits the affected claim and creates a `resolution.edit` link to the comment. If the finding is incorrect — the reviewer misread the claim, applied a check wrongly, or flagged something that is actually correct — the reviser creates a rejection rationale document explaining why the finding was refused, and a `resolution.reject` link binding the comment, the claim, and the rationale. The rationale is a first-class document in the link graph — addressable and reviewable like any other artifact. Either way the comment is closed. The reviser operates in the Dijkstra voice — every formal statement justified where introduced. On edit, every commitment present before the edit is present after.

### Scope assembler

Constructs the context the reviewer sees. The scope strategy (adaptive, comprehensive, or any other) is a choreography decision. The protocol defines no scope strategies — only the predicate that any choreography must satisfy.

### Events

**Requests (input from above).**

- ⟨ RegisterClaim | doc ⟩ — attach a `claim` classifier to doc, admitting it to the lattice.
- ⟨ Cite | source, target ⟩ — create a `citation` link from source to target.
- ⟨ AttachContract | claim, kind ⟩ — create a `contract` link of subtype kind on claim.
- ⟨ FileComment | review, claim, class, finding ⟩ — create a `comment` link of subtype class from review to claim, with finding as content.
- ⟨ ResolveEdit | comment, claim ⟩ — create a `resolution.edit` link closing comment. The claim document has been edited.
- ⟨ ResolveReject | comment, claim, rationale ⟩ — create a `resolution.reject` link closing comment. The rationale is a document linked to both the comment and the claim.
- ⟨ EvaluateConvergence ⟩ — evaluate the convergence predicate.

**Indications (output upward).**

- ⟨ CommentFiled | claim, comment, class ⟩ — a comment has been created on claim.
- ⟨ ResolutionFiled | comment, resolution, subtype ⟩ — a comment has been closed.
- ⟨ Converged ⟩ — the convergence predicate holds.
- ⟨ NotConverged | open_comments ⟩ — the predicate does not hold.

---

## 4 Convergence

**Convergence is a predicate on the link graph, not an event.** Any participant can evaluate it at any time.

### The predicate

> For every document with a `claim` classifier, every `comment.revise` link targeting that claim has a matching `resolution` link.

No scope qualifiers. The protocol doesn't know or care what scope strategy produced the comments. It knows whether they're resolved — by edit or by rejection.

No "latest version." Every revise comment ever filed on a claim blocks until explicitly resolved. No comment drops off silently because the claim was edited.

### What convergence is not

- Not "enough cycles ran."
- Not "last pass had no findings" — a comment from three cycles ago still blocks if unresolved.
- Not "reviewer said OBSERVE" — `comment.observe` links don't participate in the predicate.
- Not "latest version is clean" — there is no "latest version."

### Choreography vs predicate

The predicate defines WHAT convergence is. Choreography — which scope strategy to use, what order to review claims in, how to assemble context, when to alternate strategies — defines HOW the protocol tries to make the predicate true. Different choreographies satisfy the same predicate.

**The protocol IS the predicate. Everything else is optimization.**

**Coverage is the choreography's responsibility.** The predicate is trivially satisfied when no reviews have happened — zero `comment.revise` links means zero unresolved concerns. This is correct: the predicate says "all filed concerns are addressed," not "sufficient examination has occurred." The choreography must ensure that reviews actually happen before treating predicate satisfaction as meaningful.

Scope strategies (adaptive scope that expands on demand, comprehensive scope that preloads everything) are properties of the choreography, recorded as content within review documents. The protocol's link vocabulary does not include scope — because the predicate doesn't need to distinguish how a comment was produced, only whether it's resolved.

---

## 5 Properties

### 5.1 Safety

These properties hold at every state. They are unconditional.

**S1 (Predicate definition).** ⟨ Converged ⟩ is indicated iff for every `comment.revise` link targeting any claim in the lattice, there exists at least one `resolution` link (of either subtype) closing it. Per-claim convergence is the predicate restricted to one claim. Lattice-wide convergence is the conjunction.

**S2 (Resolution permanence).** Once a `resolution` link exists closing a `comment`, it is never removed. A resolved comment stays resolved. (Inherited from SUB1.)

**S3 (Accumulation).** Claims, citations, contracts, comments, and resolutions accumulate. None is retracted. (Inherited from SUB1.)

**S4 (Comment integrity).** A `comment.observe` link never creates a resolution obligation. Only `comment.revise` participates in the convergence predicate.

**S5 (Indication soundness).** If ⟨ Converged ⟩ is indicated, the predicate defined by S1 holds at the moment of indication. Convergence may later become false if new `comment.revise` links are filed.

**S6 (Structural soundness).** No `comment` link is created on a claim whose structural validation has not been satisfied since its last edit. This is a protocol-level constraint on all implementations — any algorithm implementing this protocol must validate before review. (Relies on SV1, SV2.)

**S7 (Commitment preservation).** On `resolution.edit`, every commitment present in the claim before the edit is present after. Edits change form, not meaning. On `resolution.reject`, the claim is unchanged.

### 5.2 Quality boundary

These are content quality targets monitored across review cycles. Unlike safety properties S1–S7, they are not graph properties evaluable from link state — they require inspection of document content. They are conditions the [principles](../principles/README.md) describe and the choreography monitors.

**Content balance.** Claim files hold at roughly 70/30 prose-to-formal. Divergence signals decoupling. See [The Coupling Principle](../principles/coupling.md).

**Voice discipline.** Both reviewer and reviser operate under positive style structure. See [The Voice Principle](../principles/voice.md).

### 5.3 Liveness

These properties hold given progress assumptions. They are conditional on agents being active.

**L1 (Reviser responsiveness).** If a `comment.revise` link exists without a matching `resolution`, and a reviser agent is active, then eventually a `resolution` link (edit or reject) is created closing it.

**L2 (Reviewer responsiveness).** If an ⟨ EvaluateConvergence ⟩ request is made and a reviewer agent is active, then eventually either ⟨ Converged ⟩ or ⟨ NotConverged | open_comments ⟩ is indicated.

**L3 (Progress).** If agents are active and the claim set is finite, then the number of `comment.revise` links without matching `resolution` links is eventually non-increasing. Does not guarantee convergence — new reviews may file new comments. Guarantees that existing comments are addressed.

**L4 (Cross-invocation progress).** Unresolved `comment.revise` links persist across protocol invocations (from SUB1, S3). An invocation that exits with open comments leaves them for the next invocation. No work is lost between invocations.

### 5.4 Deliberate non-guarantees

**No coverage guarantee.** The protocol does not require that any review has been performed. It constrains only links that have been filed. Coverage is a choreography obligation.

**No convergence guarantee.** The protocol does not guarantee that ⟨ Converged ⟩ is eventually indicated. A reviewer may file new `comment.revise` links indefinitely. A reviser may reject comments that the reviewer re-files. The protocol guarantees progress on existing comments (L3), not termination. Termination depends on choreography decisions and the finiteness of correctness issues.

**No ordering guarantee.** The protocol does not prescribe the order in which claims are reviewed, comments are resolved, or scopes are assembled. Any ordering that satisfies the properties is valid.

**Operational monitoring.** Detecting non-convergence in practice — oscillation (reviser fixes generate new revise comments cycling without progress), reject cycling (reviser rejects findings the reviewer re-files), systematic classification bias — is a choreography and monitoring concern, not a protocol property. See [Claim Convergence Design Note](../design-notes/claim-convergence.md) for detection strategies.

---

## 6 Algorithm: iterative convergence

Implements: Claim Convergence Protocol (§1–§5).
Uses: Substrate (§2.1), Reviewer agent (R), Reviser agent (V), Structural Validation (§2.2).

The algorithm engages a scope — a single claim, a cone, or an entire ASN — and drives the predicate true through cycles of review and revise. Each cycle is a deterministic sequence of agent invocations against the substrate. Convergence is decided by the substrate's predicate, never by an agent's verdict alone.

### 6.1 State

- scope — the engaged claim set (a single claim, a cone, or an entire ASN).
- N — work-cycle bound. Typical values: 8 for cone-level engagement, 8 for ASN-level. The bound prevents unbounded cost; cross-invocation progress (L4) ensures work resumes where it left off.
- k — current cycle index.
- *naturallyConverged* — boolean; set when a work cycle observes both predicate truth and a quiet review.

### 6.2 Cycle

```
upon ⟨ Engage | scope, N ⟩ do
  k ← 0
  naturallyConverged ← false

  while k < N do
    k ← k + 1
    RetryOpenRevises(scope)             ; §6.3
    Validate(scope)                     ; §6.4
    fs ← Review(scope)                  ; §6.5
    EmitFindings(scope, fs)             ; §6.6
    Revise(scope, fs)                   ; §6.7
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

### 6.3 RetryOpenRevises

For every `comment.revise` on scope without a matching `resolution`, invoke V on the comment with its finding. V either edits the claim and emits ⟨ ResolveEdit ⟩, or refuses and emits ⟨ ResolveReject ⟩ with rationale document.

### 6.4 Validate

Invoke structural validation on scope. For every violation, apply the corresponding fix recipe. Repeat until SV1 reports zero violations. This enforces S6 — no review operates on structurally unsound state.

### 6.5 Review

Invoke R on scope with assembled context. R returns the set fs of findings, each classified as `comment.revise` or `comment.observe`.

### 6.6 EmitFindings

For each finding in fs: register the finding document, file the corresponding comment via ⟨ FileComment ⟩, and record the review event. After EmitFindings, every finding is observable through the substrate.

### 6.7 Revise

For each new `comment.revise` filed in the current cycle, invoke V. V resolves the comment as in §6.3.

---

## 7 Correctness

### Safety (S1, S5 — indication soundness)

If ⟨ Converged | scope ⟩ is indicated, the predicate holds at that moment.

*Argument.* The algorithm indicates Converged only after IsConverged?(scope) returns true. By S1, every revise comment on scope has a matching resolution at evaluation time. By SUB1, neither comments nor resolutions are removable; the predicate's truth at indication persists until new comments arrive.

### Liveness (L1 — reviser responsiveness)

If V always produces a resolution for the comment it is given, then for every open revise comment on scope, eventually a resolution exists.

*Argument.* Open comments persist across invocations (SUB1, S3). At the start of every cycle, RetryOpenRevises (§6.3) re-feeds every open revise comment on scope to V. Under the assumption, V produces a closing resolution. Within at most one cycle per comment, all open comments are resolved.

### Bounded work per engagement

Each Engage performs at most N + 1 review invocations and at most N revise rounds.

*Argument.* The cycle structure (§6.2) bounds work-loop reviews by N. The confirmation contributes one additional review and zero revise rounds.

### Cross-invocation progress (L4)

If Engage i exits NotConverged with k open revise comments, then Engage (i + 1) begins its first retry pass with k re-feedings. Under the responsiveness assumption, all k close within (i + 1)'s first cycle.

*Argument.* By SUB1, the k open comments persist between invocations. RetryOpenRevises is the first action of each cycle.

---

## 8 Composition

### Within the maturation protocol

The [maturation protocol](../design-notes/maturation-protocol.md) activates claim convergence when a claim set's blueprinting transition condition is met — structural form satisfies the [Claim File Contract](../design-notes/claim-file-contract.md). The maturation protocol deactivates claim convergence when the convergence predicate holds and the choreography's coverage obligation is met.

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

## 9 Performance

- **Predicate evaluation.** A FindLinks query for type `comment.revise` on scope, followed by a FindNumLinks query for type `resolution` against each returned comment. Linear in the number of revise comments on scope.
- **Cycle cost.** Dominated by R and V invocations. Bounded by N + 1 reviews and N revise rounds per Engage.
- **Substrate query cost.** Each FindLinks and FindNumLinks operates against the indexed substrate; cost is logarithmic in substrate size at expected scales.
- **Cross-invocation cost.** Substrate state size grows with cumulative comment and resolution counts (SUB1). Engages iterate only currently open work, not full history.

---

## Related

- [Validate Before Review](../patterns/validate-before-review.md) — the pattern underlying S6.
- [The Validation Principle](../principles/validation.md) — structural integrity as a precondition for meaningful review.
- [The Coupling Principle](../principles/coupling.md) — content balance (§5.2 quality boundary).
- [The Voice Principle](../principles/voice.md) — output quality discipline for reviewer and reviser.
- [Production Drive](../design-notes/production-drive.md) — the LLM behavioral force motivating the revise/observe classification (S4).
- [Maturation Protocol](../design-notes/maturation-protocol.md) — the meta-protocol composing this module with other stage protocols.
- [Claim Convergence Design Note](../design-notes/claim-convergence.md) — rationale: why two scopes, why local was retired, the T3 incident, the multigrid analogy, the shift from algorithm to protocol.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.