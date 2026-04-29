# Convergence Protocol

A document-type-neutral module that defines convergence for any review/revise process. The protocol specifies when a set of documents has converged — every concern raised has been addressed. What documents are reviewed, how context is assembled, and when reviews happen are choreography decisions outside this module.

Following the modular formalism of Cachin (*Reliable and Secure Distributed Programming*).

---

## 1 Document model

Everything the protocol manipulates is either a document (content) or a link (typed relationship between documents). There are no intrinsic document roles — a document's role comes from the classifier links attached to it.

### Link types

| Type | Subtypes | Role |
|---|---|---|
| `review` | (flat, one-sided) | Classifier: document is an aggregate review (the reviewer's full output) |
| `finding` | (flat, one-sided) | Classifier: document is one finding extracted from a review |
| `comment` | `revise`, `observe` | Finding observes a document. Subtypes classify the finding. |
| `resolution` | `edit`, `reject` | Closes a comment. Edit: the document was changed. Reject: the finding was refused. |

Four link types. Two classifiers (`review`, `finding`). Two express relationships (`comment`, `resolution`).

A review event produces one aggregate review document and N finding documents (one per individual finding the reviewer surfaced). The aggregate carries the reviewer's full output — title, scope, verdict, summary table; it is classified by `review`. Each finding doc carries one finding's prose; it is classified by `finding`, holds the from-side of a `comment.<class>` relation to the document being commented on, and carries a `provenance.derivation` link from the aggregate review documenting the decomposition. The aggregate-to-finding relationship is many-to-one logically and N-to-1 in the substrate; a finding has exactly one aggregate, an aggregate has zero or more findings.

Subtypes are valid when they change the structure or invariants of what the link carries. `comment.revise` requires resolution; `comment.observe` does not. `resolution.edit` means the document was changed. `resolution.reject` means the document was not changed — a rationale document explains the refusal.

### No versioning primitive

Documents are referenced by path, not by version. The protocol carries no versioning primitive.

The absence is deliberate. A predicate that tracks "latest version" lets unresolved comments silently evaporate when the document is edited — the old version is no longer "latest" and comments targeting it stop blocking convergence without being addressed. The simpler predicate — every `comment.revise` must have a resolution, regardless of when it was filed — closes this footgun.

---

## 2 Modules used

### Substrate

The persistent, append-only link graph. See [Substrate Module](../modules/substrate-module.md) for the full specification.

**Operations relied upon.**

- ⟨ MakeLink | from, to, types ⟩ — append a new link, return its address.
- ⟨ FindLinks | home, from, to, types ⟩ — return all links matching the constraint conjunction.
- ⟨ ActiveLinks | home, from, to, types ⟩ — return all matching links that are not retracted (per SUB4, SUB5).

**Properties relied upon.**

- SUB1 (Permanence). No link is ever removed once created.
- SUB2 (Query soundness). FindLinks returns exactly the links satisfying the constraint conjunction.
- SUB3 (Count consistency). FindNumLinks(args) = |FindLinks(args)|.

The convergence protocol does not itself file retraction links. Specializations that extend it (claim convergence, note convergence) may retract resolution links, which affects the predicate — a retracted resolution no longer counts toward closing a comment. The predicate evaluates against active links to handle this correctly.

---

## 3 Participants and events

Reviewer and reviser are roles in the protocol, not necessarily distinct agents. In some contexts they are separate LLMs under different prompts. In others they may be the same actor switching modes. The protocol constrains the roles — what each produces and what properties must hold — not the mapping of roles to agents.

### Reviewer

Reads assembled context and produces (a) one aggregate review document classified by `review`, and (b) per-finding documents — one per finding — each classified by `finding`, each carrying a `comment.<class>` link to the document the finding is about and a `provenance.derivation` link from the aggregate. Each comment is classified:

- `comment.revise` — the document is wrong, incomplete, or ungrounded. Requires resolution.
- `comment.observe` — the document is correct but the reviewer noticed something. Recorded, no resolution required.

OBSERVE is the off-ramp for the [production drive](../design-notes/production-drive.md). The convergence predicate tracks only REVISE comments; OBSERVE accumulates as audit trail without blocking convergence.

### Reviser

Observes unresolved `comment.revise` links and responds in one of two ways. If the finding is valid, the reviser edits the affected document and creates a `resolution.edit` link to the comment. If the finding is incorrect, the reviser creates a rejection rationale document explaining why and a `resolution.reject` link binding the comment, the document, and the rationale. The rationale is a first-class document in the link graph — addressable and reviewable. Either way the comment is closed.

### Events

**Requests (input from above).**

- ⟨ FileReview | aggregate_doc ⟩ — emit the `review` classifier on the aggregate review document.
- ⟨ FileFinding | aggregate, finding_doc, document, class, finding_text ⟩ — write the finding doc with content `finding_text`; emit the `finding` classifier on the finding doc; emit a `comment.<class>` link from the finding doc to the document being commented on; emit a `provenance.derivation` link from `aggregate` to `finding_doc`. All four substrate operations execute together as a single decomposition step; partial failure leaves the substrate in a consistent (no-half-finding) state.
- ⟨ ResolveEdit | comment, document ⟩ — create a `resolution.edit` link closing comment. The document has been edited.
- ⟨ ResolveReject | comment, document, rationale ⟩ — create a `resolution.reject` link closing comment. The rationale is a document linked to both.
- ⟨ EvaluateConvergence | document_set ⟩ — evaluate the convergence predicate over a set of documents.

**Indications (output upward).**

- ⟨ ReviewFiled | aggregate_doc ⟩ — an aggregate review document has been classified.
- ⟨ FindingFiled | aggregate, finding_doc, comment_id, document, class ⟩ — one finding has been decomposed from `aggregate` into `finding_doc`, with a `comment.<class>` linking it to `document`.
- ⟨ CommentFiled | document, comment, class ⟩ — a comment has been created. (Equivalent to FindingFiled with the finding-doc and aggregate fields elided; retained for backwards compatibility with consumers that subscribe at the comment level.)
- ⟨ ResolutionFiled | comment, resolution, subtype ⟩ — a comment has been closed.
- ⟨ Converged | document_set ⟩ — the convergence predicate holds over the set.
- ⟨ NotConverged | document_set, open_comments ⟩ — the predicate does not hold.

---

## 4 Convergence

**Convergence is a predicate on the link graph, not an event.** Any participant can evaluate it at any time.

### The predicate

> For every document in the set, every active `comment.revise` link targeting that document has a matching active `resolution` link.

The predicate evaluates against active links (via the substrate's ActiveLinks query, per [SUB4–SUB5](../modules/substrate-module.md)). A retracted resolution no longer counts toward closing a comment — the comment becomes unresolved. A retracted comment no longer creates a resolution obligation. In practice, the convergence protocol itself does not file retractions; specializations that do (claim convergence, note convergence) rely on this active-link evaluation to keep the predicate correct after retraction.

No scope qualifiers. The protocol doesn't know what scope strategy produced the comments. It knows whether they're resolved — by edit or by rejection.

No "latest version." Every active revise comment blocks until explicitly resolved.

### What convergence is not

- Not "enough cycles ran."
- Not "last pass had no findings" — an active comment from three cycles ago still blocks if unresolved.
- Not "reviewer said OBSERVE" — `comment.observe` links don't participate in the predicate.
- Not "latest version is clean" — there is no "latest version."

### Choreography vs predicate

The predicate defines WHAT convergence is. Choreography defines HOW the protocol tries to make the predicate true. Different choreographies satisfy the same predicate.

**The protocol IS the predicate. Everything else is optimization.**

**Coverage is the choreography's responsibility.** The predicate is trivially satisfied when no reviews have happened. This is correct: the predicate says "all filed concerns are addressed," not "sufficient examination has occurred." The choreography must ensure reviews actually happen before treating predicate satisfaction as meaningful.

---

## 5 Properties

### 5.1 Safety

**S1 (Predicate definition).** ⟨ Converged | D ⟩ is indicated iff for every active `comment.revise` link targeting any document in D, there exists at least one active `resolution` link (of either subtype) closing it. Per-document convergence is the predicate restricted to one document. Set-wide convergence is the conjunction.

**S2 (Resolution permanence).** Once a `resolution` link exists closing a `comment`, it is never removed from the substrate. (Inherited from SUB1.) A resolution may be retracted by a specialization protocol, making it inactive for predicate evaluation — but the link itself persists in the substrate and remains visible to FindLinks.

**S3 (Accumulation).** Comments and resolutions accumulate in the substrate. None is removed. (Inherited from SUB1.) The convergence protocol itself does not retract comments or resolutions. Specializations may retract resolutions (re-opening a comment) using the substrate's retraction mechanism; the predicate handles this correctly by evaluating against active links.

**S4 (Comment integrity).** A `comment.observe` link never creates a resolution obligation. Only `comment.revise` participates in the convergence predicate.

**S5 (Indication soundness).** If ⟨ Converged | D ⟩ is indicated, the predicate holds at the moment of indication. Convergence may later become false if new `comment.revise` links are filed or if an existing resolution is retracted.

**S6 (Commitment preservation).** On `resolution.edit`, every commitment present in the document before the edit is present after. Edits change form, not meaning. On `resolution.reject`, the document is unchanged.

### 5.2 Liveness

**L1 (Reviser responsiveness).** If an active `comment.revise` link exists without a matching active `resolution`, and a reviser agent is active, then eventually a `resolution` link is created closing it.

**L2 (Reviewer responsiveness).** If an ⟨ EvaluateConvergence | D ⟩ request is made and a reviewer agent is active, then eventually either ⟨ Converged | D ⟩ or ⟨ NotConverged | D, open_comments ⟩ is indicated.

**L3 (Progress).** If agents are active and the document set is finite, then the number of active `comment.revise` links without matching active `resolution` links is eventually non-increasing.

**L4 (Cross-invocation progress).** Unresolved `comment.revise` links persist across protocol invocations (from SUB1, S3). No work is lost between invocations.

### 5.3 Deliberate non-guarantees

**No coverage guarantee.** The protocol does not require that any review has been performed. Coverage is a choreography obligation.

**No convergence guarantee.** The protocol does not guarantee that ⟨ Converged ⟩ is eventually indicated. Termination depends on choreography decisions and the finiteness of issues in the documents.

**No ordering guarantee.** The protocol does not prescribe the order in which documents are reviewed or comments are resolved.

**No retraction guarantee.** The convergence protocol does not retract links. Specializations that use retraction (via the [substrate](../modules/substrate-module.md)) are responsible for the consequences — a retracted resolution re-opens its comment; the predicate evaluates accordingly.

**Operational monitoring.** Detecting non-convergence — oscillation, reject cycling, classification bias — is a choreography and monitoring concern, not a protocol property.

---

## Related

- [Substrate Module](../modules/substrate-module.md) — the persistent link graph this protocol operates on. Provides permanence, query operations, and retraction semantics.
- [Review/Revise Iteration](../patterns/review-revise-iteration.md) — the empirical pattern this protocol formalizes. Excavation stages, convergence dynamics, stall conditions.
- [Production Drive](../design-notes/production-drive.md) — the LLM behavioral force that OBSERVE channels safely.
- [Note Convergence Protocol](note-convergence-protocol.md) — uses this module for notes, adding OUT_OF_SCOPE classification and lattice growth signals.
- [Claim Convergence Protocol](claim-convergence-protocol.md) — uses this module for claims, adding lattice structure, structural validation, and a claim-specific algorithm.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.