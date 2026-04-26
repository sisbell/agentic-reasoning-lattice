# Substrate Module

The persistent, append-only graph that every protocol reads from and writes to. Documents are content nodes. Links are typed relationships between them. The substrate stores both, answers queries about links, and provides retraction as a structural operation for nullifying links without removing them.

The substrate knows nothing about what links mean. It does not know what a "claim" is, what "convergence" requires, or what "review" does. Protocols bring their own link types and interpret them. The substrate stores them uniformly and provides the operations that make them queryable and durable.

Following the modular formalism of Cachin (*Reliable and Secure Distributed Programming*).

---

## 1 Model

### Documents

Content nodes referenced by path. The substrate stores documents but does not interpret their content. A document's role comes from the classifier links protocols attach to it — the substrate sees a path and a blob, not a "claim" or a "note."

### Links

Typed relationships between documents (or between a document and a link). Each link has:

- **id** — unique identifier assigned at creation. Immutable.
- **from** — source document path.
- **to_set** — target document path(s) or, for retraction links, a target link ID.
- **type_set** — one or more type strings (e.g., `["comment", "comment.revise"]`). Subtypes include their parent: a link with type `comment.revise` matches queries for `comment`.

Links are the substrate's primitive. The graph is a set of links. Everything protocols build — dependency structures, review trails, provenance records — is links in the substrate.

### Link immutability

Once created, a link's id, from, to_set, and type_set are fixed. Links are never modified. They are never removed. The graph only grows. This is the foundation the protocols rely on: a comment filed in cycle 3 is still there in cycle 30. A citation from the original decomposition is still there after twenty revisions. Nothing vanishes.

---

## 2 Operations

### 2.1 MakeLink

⟨ MakeLink | from, to_set, type_set ⟩ → link_id

Append a new link to the graph. Returns the link's unique ID. The link is immediately visible to subsequent queries.

### 2.2 FindLinks

⟨ FindLinks | home, from, to, type_set ⟩ → links

Return all links matching the constraint conjunction. Each constraint is optional; omitted constraints are unconstrained. Type matching uses prefix semantics: querying for `comment` returns links with type `comment`, `comment.revise`, and `comment.observe`.

FindLinks returns every matching link, including retracted ones. It is the raw query — it does not filter by active state. Protocols that need the active set use ActiveLinks (§2.5).

### 2.3 FindNumLinks

⟨ FindNumLinks | home, from, to, type_set ⟩ → count

Return the count of links matching the constraints. Same semantics as FindLinks but returns only the count.

### 2.4 Retract

⟨ Retract | link_id ⟩ → retraction_link_id

Create a `retraction` link whose `to_set` holds the target link's ID. The target link remains in the substrate — it is not removed, not modified, not hidden from FindLinks. The retraction is itself a link, subject to the same immutability guarantees as any other link.

Retraction is the substrate's only link type. All other link types (`claim`, `citation`, `comment`, `resolution`, `contract`, `review`, `note`, `synthesis`, `decomposition`) are defined by the protocols that use the substrate.

### 2.5 ActiveLinks

⟨ ActiveLinks | home, from, to, type_set ⟩ → links

Return all links matching the constraints that are not retracted. A link is retracted if any `retraction` link in the substrate targets its ID. This is a single-depth check, not a recursive chain walk — whether the retraction itself is retracted does not restore the original link (see §4, shadow semantics).

ActiveLinks is the query protocols use when they need the current state of the graph. FindLinks is the query protocols use when they need the full history.

---

## 3 Properties

### Permanence

**SUB1 (Permanence).** No link is ever removed once created. The graph is append-only. This is the property every protocol's safety arguments depend on — comments persist across invocations, resolutions once filed cannot vanish, citations survive proof revisions.

### Query soundness

**SUB2 (Query soundness).** FindLinks returns exactly the links satisfying the constraint conjunction. No false positives, no false negatives. The query is a faithful view of the graph.

### Count consistency

**SUB3 (Count consistency).** FindNumLinks(args) = |FindLinks(args)|. The count operation agrees with the enumeration operation.

### Retraction semantics

**SUB4 (Retraction nullifies, doesn't remove).** A retraction link makes its target inactive in ActiveLinks queries but does not remove the target from the substrate. Both the original link and the retraction persist. FindLinks returns both; ActiveLinks returns neither the retracted link nor (unless separately queried) the retraction itself.

**SUB5 (Shadow semantics).** The active state of any link L is determined by whether any retraction targeting L exists in the substrate, regardless of whether those retractions are themselves retracted. Retraction is one-way for the original target: once a link is retracted, it stays inactive. To restore a link's role, file a new link to the same target.

This means:
- Retraction of a citation: citation becomes inactive. File a new citation to restore.
- Retraction of a resolution: resolution becomes inactive. The comment it closed is now unresolved. File a new resolution to re-close.
- Retraction of a retraction: the retraction becomes inactive, but the original link it targeted remains inactive. The shadow cast by the first retraction is permanent.

The shadow interpretation makes `active_links` a single-depth check: "does any retraction target this link's ID?" No chain walking, no parity computation, no depth-N reasoning. The computed active set is unambiguous at any point in the graph's history.

### Retraction idempotence

**SUB6 (Retraction idempotence).** Multiple retraction links targeting the same link ID produce the same computed active set as a single retraction. Filing a retraction on an already-retracted link is permitted and is a no-op for graph state.

### Predicate evaluation under retraction

The substrate permits retraction of any link — citations, resolutions, comments, contracts, classifiers. The substrate does not restrict which link types can be retracted because it does not interpret link types.

Protocols that build predicates on the link graph (e.g., the [convergence protocol](convergence-protocol.md)'s predicate: "every `comment.revise` has a matching `resolution`") should evaluate those predicates against active links (via ActiveLinks) rather than all links (via FindLinks). A retracted resolution no longer counts toward closing a comment. A retracted comment would no longer create a resolution obligation — though no protocol currently retracts comments; this case is theoretical.

Which link types a protocol actually retracts is a protocol-level decision, not a substrate-level one. The substrate provides the mechanism; protocols decide when to use it and constrain their own retraction discipline.

---

## 4 The `retraction` link type

Retraction is the only link type the substrate defines. It has a different shape from protocol-defined link types:

| Property | Protocol-defined links | Retraction |
|---|---|---|
| `to_set` contains | Document path(s) | Link ID |
| Defined by | Protocol that uses it | Substrate |
| Affects queries | No (FindLinks treats all links uniformly) | Yes (ActiveLinks subtracts retracted targets) |

This shape divergence is why retraction is a substrate concern rather than a protocol concern. A retraction's `to_set` holds a link ID — a substrate-level address. Protocol-defined links' `to_set` holds document paths — a content-level address. The substrate knows about its own addresses; protocols know about content addresses. Retraction operates at the substrate's level.

### Why not subtypes

There is no `retraction.citation`, `retraction.comment`, or `retraction.resolution`. The semantics are uniform: "this link no longer counts." What was retracted is discoverable from the `to_set` referent — follow the link ID, read the target's type. Subtypes would encode information that's already in the graph without adding any behavioral distinction.

---

## 5 Composition

Every protocol in the system uses the substrate:

```
Substrate
  ↑ used by
Convergence Protocol ─── Note Convergence ─── Claim Convergence
Consultation Protocol
Note Decomposition Protocol
Maturation Protocol
```

Each protocol's "Modules used" section declares the substrate and lists which SUB properties it relies on. The typical declaration:

- Convergence protocol: SUB1 (permanence for comment/resolution accumulation), SUB2 (query soundness for predicate evaluation), SUB3 (count consistency).
- Protocols that use retraction additionally rely on: SUB4 (retraction nullifies), SUB5 (shadow semantics), SUB6 (idempotence).

### What protocols bring

Protocols define their own link types and attach their own semantics. The substrate stores them uniformly. The protocol-defined link types currently in use:

| Link type | Defined by | Purpose |
|---|---|---|
| `review` | Convergence protocol | Classifier: document is a review |
| `comment` (.revise, .observe, .out-of-scope) | Convergence protocol | Finding targeting a document |
| `resolution` (.edit, .reject) | Convergence protocol | Closes a comment |
| `claim` | Claim convergence protocol | Classifier: document is a claim |
| `contract` (.axiom, .definition, .theorem, ...) | Claim convergence protocol | Formal structure on a claim |
| `citation` | Both convergence protocols | Dependency edge (note→note or claim→claim) |
| `note` | Note convergence protocol | Classifier: document is a note |
| `inquiry` | Consultation protocol | Classifier: document is an inquiry |
| `synthesis` | Consultation protocol | Provenance: inquiry produced this note |
| `decomposition` | Note decomposition protocol | Provenance: note produced this claim set |
| `provenance.extract`, `.absorb`, `.reset` | Maturation protocol | Audit trail for lattice operations |

The substrate does not enforce any of these types. It stores whatever type strings a MakeLink call provides. Type semantics are protocol concerns.

---

## 6 Current implementation

The current substrate is filesystem-backed: `lattices/<lattice>/_store/`. Links are YAML files in the store directory. Documents are files in the lattice directory tree. FindLinks and FindNumLinks are implemented as filtered directory scans with type-prefix matching.

The substrate specification is implementation-independent. Any backing store satisfying SUB1–SUB6 supports the protocols. The current filesystem implementation is scaffolding toward a live Xanadu-native link graph (see [Vision](../vision.md)).

### Known gaps

- ActiveLinks is not yet implemented as a substrate operation. The `active_links` helper in `lib.store.queries` performs the retraction subtraction, but it is a protocol-layer utility rather than a substrate-level query. Migration to a substrate operation is straightforward — the helper's logic moves into the substrate's query interface.
- Retract is not yet implemented as a substrate operation. The `scripts/retract.py` script creates retraction links via MakeLink. Migration is the same: the script's logic becomes a substrate operation.

---

## Related

- [Convergence Protocol](convergence-protocol.md) — the first consumer. Uses SUB1–SUB3 for comment/resolution accumulation and predicate evaluation.
- [Claim Convergence Protocol](claim-convergence-protocol.md) — uses retraction for stale citations during proof evolution (prune).
- [Note Convergence Protocol](note-convergence-protocol.md) — uses retraction for stale citations after absorb and extract operations.
- [Architecture](../architecture.md) — the `_store/` directory in the lattice structure.
- [Vision](../vision.md) — the Xanadu-native link graph that replaces the filesystem-backed store.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.