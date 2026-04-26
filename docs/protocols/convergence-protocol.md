# Convergence Protocol

A document-type-neutral module that defines convergence for any review/revise process. The protocol specifies when a set of documents has converged — every concern raised has been addressed. What documents are reviewed, how context is assembled, and when reviews happen are choreography decisions outside this module.

Following the modular formalism of Cachin (*Reliable and Secure Distributed Programming*).

---

## 1 Document model

Everything the protocol manipulates is either a document (content) or a link (typed relationship between documents). There are no intrinsic document roles — a document's role comes from the classifier links attached to it.

### Link types

| Type | Subtypes | Role |
|---|---|---|
| `review` | (flat, one-sided) | Classifier: document is a review |
| `comment` | `revise`, `observe` | Finding observes a document. Subtypes classify the finding. |
| `resolution` | `edit`, `reject` | Closes a comment. Edit: the document was changed. Reject: the finding was refused. |

Three link types. One classifier (`review`). Two express relationships (`comment`, `resolution`).

Subtypes are valid when they change the structure or invariants of what the link carries. `comment.revise` requires resolution; `comment.observe` does not. `resolution.edit` means the document was changed. `resolution.reject` means the document was not changed — a rationale document explains the refusal.

The convergence module does not file `retraction` links itself, but the substrate vocabulary supports them — a `retraction` link points at the id of a previously-filed link to nullify it without violating SUB1 permanence. This module's predicate operates on `comment.revise` and `resolution`; retraction is used by claim convergence (for stale citations) and is documented there. Specializations are responsible for using an `active_links`-style helper when computing graph state if they care about retraction, since the substrate's `find_links` query does not subtract retractions automatically.

### No versioning primitive

Documents are referenced by path, not by version. The protocol carries no versioning primitive.

The absence is deliberate. A predicate that tracks "latest version" lets unresolved comments silently evaporate when the document is edited — the old version is no longer "latest" and comments targeting it stop blocking convergence without being addressed. The simpler predicate — every `comment.revise` must have a resolution, regardless of when it was filed — closes this footgun.

---

## 2 Modules used

### Substrate

A persistent, append-only graph of documents and typed links between them.

**Operations.**

- ⟨ MakeLink | from, to, types ⟩ — append a new link, return its address.
- ⟨ FindLinks | home, from, to, types ⟩ — return links matching the constraint conjunction.
- ⟨ FindNumLinks | home, from, to, types ⟩ — return the count matching the constraints.

**Properties relied upon.**

- SUB1 (Permanence). No link is ever removed once created.
- SUB2 (Query soundness). FindLinks returns exactly the links satisfying the constraint conjunction.
- SUB3 (Count consistency). FindNumLinks(args) = |FindLinks(args)|.

---

## 3 Participants and events

Reviewer and reviser are roles in the protocol, not necessarily distinct agents. In some contexts they are separate LLMs under different prompts. In others they may be the same actor switching modes. The protocol constrains the roles — what each produces and what properties must hold — not the mapping of roles to agents.

### Reviewer

Reads assembled context and produces comment links on documents it observes. Each comment is classified:

- `comment.revise` — the document is wrong, incomplete, or ungrounded. Requires resolution.
- `comment.observe` — the document is correct but the reviewer noticed something. Recorded, no resolution required.

OBSERVE is the off-ramp for the [production drive](../design-notes/production-drive.md). The convergence predicate tracks only REVISE comments; OBSERVE accumulates as audit trail without blocking convergence.

### Reviser

Observes unresolved `comment.revise` links and responds in one of two ways. If the finding is valid, the reviser edits the affected document and creates a `resolution.edit` link to the comment. If the finding is incorrect, the reviser creates a rejection rationale document explaining why and a `resolution.reject` link binding the comment, the document, and the rationale. The rationale is a first-class document in the link graph — addressable and reviewable. Either way the comment is closed.

### Events

**Requests (input from above).**

- ⟨ FileComment | review, document, class, finding ⟩ — create a `comment` link of subtype class from review to document, with finding as content.
- ⟨ ResolveEdit | comment, document ⟩ — create a `resolution.edit` link closing comment. The document has been edited.
- ⟨ ResolveReject | comment, document, rationale ⟩ — create a `resolution.reject` link closing comment. The rationale is a document linked to both.
- ⟨ EvaluateConvergence | document_set ⟩ — evaluate the convergence predicate over a set of documents.

**Indications (output upward).**

- ⟨ CommentFiled | document, comment, class ⟩ — a comment has been created.
- ⟨ ResolutionFiled | comment, resolution, subtype ⟩ — a comment has been closed.
- ⟨ Converged | document_set ⟩ — the convergence predicate holds over the set.
- ⟨ NotConverged | document_set, open_comments ⟩ — the predicate does not hold.

---

## 4 Convergence

**Convergence is a predicate on the link graph, not an event.** Any participant can evaluate it at any time.

### The predicate

> For every document in the set, every `comment.revise` link targeting that document has a matching `resolution` link.

No scope qualifiers. The protocol doesn't know what scope strategy produced the comments. It knows whether they're resolved — by edit or by rejection.

No "latest version." Every revise comment ever filed blocks until explicitly resolved.

### What convergence is not

- Not "enough cycles ran."
- Not "last pass had no findings" — a comment from three cycles ago still blocks if unresolved.
- Not "reviewer said OBSERVE" — `comment.observe` links don't participate in the predicate.
- Not "latest version is clean" — there is no "latest version."

### Choreography vs predicate

The predicate defines WHAT convergence is. Choreography defines HOW the protocol tries to make the predicate true. Different choreographies satisfy the same predicate.

**The protocol IS the predicate. Everything else is optimization.**

**Coverage is the choreography's responsibility.** The predicate is trivially satisfied when no reviews have happened. This is correct: the predicate says "all filed concerns are addressed," not "sufficient examination has occurred." The choreography must ensure reviews actually happen before treating predicate satisfaction as meaningful.

---

## 5 Properties

### 5.1 Safety

**S1 (Predicate definition).** ⟨ Converged | D ⟩ is indicated iff for every `comment.revise` link targeting any document in D, there exists at least one `resolution` link (of either subtype) closing it. Per-document convergence is the predicate restricted to one document. Set-wide convergence is the conjunction.

**S2 (Resolution permanence).** Once a `resolution` link exists closing a `comment`, it is never removed. (Inherited from SUB1.)

**S3 (Accumulation).** Comments and resolutions accumulate. None is retracted. (Inherited from SUB1.)

**S4 (Comment integrity).** A `comment.observe` link never creates a resolution obligation. Only `comment.revise` participates in the convergence predicate.

**S5 (Indication soundness).** If ⟨ Converged | D ⟩ is indicated, the predicate holds at the moment of indication. Convergence may later become false if new `comment.revise` links are filed.

**S6 (Commitment preservation).** On `resolution.edit`, every commitment present in the document before the edit is present after. Edits change form, not meaning. On `resolution.reject`, the document is unchanged.

### 5.2 Liveness

**L1 (Reviser responsiveness).** If a `comment.revise` link exists without a matching `resolution`, and a reviser agent is active, then eventually a `resolution` link is created closing it.

**L2 (Reviewer responsiveness).** If an ⟨ EvaluateConvergence | D ⟩ request is made and a reviewer agent is active, then eventually either ⟨ Converged | D ⟩ or ⟨ NotConverged | D, open_comments ⟩ is indicated.

**L3 (Progress).** If agents are active and the document set is finite, then the number of `comment.revise` links without matching `resolution` links is eventually non-increasing.

**L4 (Cross-invocation progress).** Unresolved `comment.revise` links persist across protocol invocations (from SUB1, S3). No work is lost between invocations.

### 5.3 Deliberate non-guarantees

**No coverage guarantee.** The protocol does not require that any review has been performed. Coverage is a choreography obligation.

**No convergence guarantee.** The protocol does not guarantee that ⟨ Converged ⟩ is eventually indicated. Termination depends on choreography decisions and the finiteness of issues in the documents.

**No ordering guarantee.** The protocol does not prescribe the order in which documents are reviewed or comments are resolved.

**Operational monitoring.** Detecting non-convergence — oscillation, reject cycling, classification bias — is a choreography and monitoring concern, not a protocol property.

---

## Related

- [Review/Revise Iteration](../patterns/review-revise-iteration.md) — the empirical pattern this protocol formalizes. Excavation stages, convergence dynamics, stall conditions.
- [Production Drive](../design-notes/production-drive.md) — the LLM behavioral force that OBSERVE channels safely.
- [Claim Convergence Protocol](claim-convergence-protocol.md) — uses this module for claims, adding lattice structure, structural validation, and a claim-specific algorithm.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.