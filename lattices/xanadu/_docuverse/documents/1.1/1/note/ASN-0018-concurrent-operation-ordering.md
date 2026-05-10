# ASN-0018: Concurrent Operation Ordering

*2026-02-25*

We are looking for the invariants that the system must maintain when multiple operations target the same or overlapping content simultaneously. The question is: what determines the final state, and what must any resolution satisfy? We shall discover that the architecture answers this question in a surprising way — not by specifying a resolution mechanism, but by making the conflict structurally impossible at the design level, while still requiring precise serialization guarantees for the residual cases that survive the architectural barriers.

**Scope.** This ASN addresses same-document concurrency: what happens when multiple operations (possibly from different sessions) target a single document or overlapping content within a document. Cross-document concurrency — where operations on distinct documents interact through global indexes or transclusion — is a separate concern with a different structure.

---

## The Problem

The conventional framing of concurrent modification asks: given two operations op₁ and op₂ that modify overlapping state, how should the system resolve the conflict? This framing presupposes that concurrent modification *occurs* and asks about the resolution.

We shall discover that Xanadu's architecture asks a different question: under what conditions can concurrent modification arise at all? The answer — almost never, by design — transforms the specification task. Instead of specifying a conflict resolution algebra, we must specify the *barriers* that prevent conflicts and the *serialization guarantees* for the narrow cases that remain.

There are three distinct barriers, each operating at a different level. We develop them in order.

---

## State

We need a model of the state components that concurrent operations might contest. Let Σ denote the system state.

**CO-Σ1 (ownership).** `Σ.owner : DocId → UserId` assigns each document to exactly one user. We write `owner(d)` for `Σ.owner(d)`.

**CO-Σ2 (content store).** `Σ.I : IAddr ⇀ Byte` is the global permanent content store. The domain grows monotonically; values are immutable once assigned.

**CO-Σ3 (arrangement).** For each document `d`, `Σ.V(d) : VPos ⇀ IAddr` maps virtual positions to I-space addresses. This is the mutable layer — editing operations modify `Σ.V(d)`.

**CO-Σ4 (write access).** `Σ.W : DocId ⇀ SessionId` is a partial function recording which session, if any, currently holds write access to each document. When `d ∈ dom(Σ.W)`, exactly one session may issue mutating operations on `d`.

**CO-Σ5 (version DAG).** `Σ.vers : DocId → Set(DocId)` records the derivation relation. If `d' ∈ Σ.vers(d)`, then `d'` was created as a version of `d`. Versions are independent documents — `d' ≠ d`, `owner(d')` may differ from `owner(d)`, and `Σ.V(d')` is entirely independent of `Σ.V(d)` after creation.

---

## The First Barrier: Single-Writer Ownership

The first and strongest barrier is that each document has exactly one owner, and only the owner may issue mutating operations. Nelson is unambiguous: "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it."

We state this as an invariant.

**CO0 (Single-writer ownership).** For every mutating operation `op` applied to document `d` by session `s`:

    [owner(session(s)) = owner(d)]

where `session(s)` returns the user associated with session `s`. No mutating operation — INSERT, DELETE, REARRANGE, APPEND, or COPY-into — may be issued by a session whose user is not the document's owner.

The immediate consequence is devastating for the concurrency problem:

**Theorem (No cross-user write conflicts).** For any two sessions `s₁` and `s₂` belonging to different users, and any document `d`:

    [owner(session(s₁)) ≠ owner(session(s₂))  ⇒  ¬(s₁ writes d ∧ s₂ writes d)]

*Proof.* By CO0, `s₁ writes d` requires `owner(session(s₁)) = owner(d)`, and `s₂ writes d` requires `owner(session(s₂)) = owner(d)`. Transitivity gives `owner(session(s₁)) = owner(session(s₂))`, contradicting the antecedent. ∎

This is not an access control policy layered on top of the system. It is a structural invariant of the architecture. The FEBE protocol provides no mechanism for granting write access to non-owners — no access control lists, no collaborative editing mode, no shared locks. Nelson provides 17 commands and none of them include a permission grant for mutating operations.

---

## The Second Barrier: Denial as Fork

What happens when a non-owner wants to modify content they did not create? In most systems, access denial is an error. In Xanadu, access denial is a *creative act*.

**CO1 (Denial-as-fork).** When a session `s` with `owner(session(s)) ≠ owner(d)` requests write access to document `d`, the system creates a new document `d'` such that:

    d' ∈ Σ'.vers(d)
    owner(d') = owner(session(s))
    Σ'.V(d') = Σ.V(d)  (initially — a snapshot of d's current arrangement)
    Σ'.V(d) = Σ.V(d)   (d is unmodified)

Session `s` then writes to `d'`, not `d`. The original document `d` is preserved; the non-owner gets their own version. Nelson: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links."

The version DAG grows. No merge is specified. Nelson explicitly provides comparison tools — SHOWRELATIONOF2VERSIONS returns "a list of ordered pairs of the spans of the two spec-sets that correspond" — but no MERGE operation appears among the 17 FEBE commands. The Xanadu model is *diverge-and-compare*, not *diverge-merge-converge*.

**CO2 (No privileged version).** The version DAG imposes no canonical ordering:

    (A d₁, d₂ : d₁ ∈ Σ.vers(d₀) ∧ d₂ ∈ Σ.vers(d₀) : rank(d₁) = rank(d₂))

All versions are co-equal. Nelson: "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." Nelson's chosen metaphor for the version system is a prism — "We may think of a given part, or section, as being prismatically refracted when we pass from one version to another." A prism produces divergence, not convergence.

Together, CO0, CO1, and CO2 eliminate the entire class of multi-user write conflicts. Two users cannot modify the same document; a non-owner who wants to modify is routed to an independent version; versions coexist without merging. The "concurrent modification" problem dissolves into independent, uncoordinated evolution of parallel documents.

---

## The Third Barrier: Content Immutability

Even if the first two barriers were somehow bypassed, a third barrier prevents "modification of shared content" from being a meaningful concept at all. The content that is *shared* across documents through transclusion lives in I-space, and I-space is immutable.

**CO3 (I-space immutability).** For any operation `op` taking `Σ` to `Σ'`:

    (A a : a ∈ dom(Σ.I) : Σ'.I(a) = Σ.I(a))

No operation alters existing I-space content. INSERT adds new addresses to `dom(Σ.I)`; DELETE, REARRANGE, COPY modify only V-space arrangements. Nelson: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." The content that transclusion shares is frozen at creation.

**CO4 (Orthogonality of mutable and shared state).** The mutable state (`Σ.V(d)` for each document) is never shared across documents; the shared state (`Σ.I` for transcluded content) is never mutable. Formally:

    (A d₁ ≠ d₂ : : Σ.V(d₁) and Σ.V(d₂) are disjoint state components)
    ∧ (A a : a ∈ dom(Σ.I) : Σ.I(a) is immutable)

The consequence is that "two users simultaneously modify shared content" is a category error. What is shared (I-space) cannot be modified. What is mutable (V-space) is per-document. The two axes — sharing and mutability — are orthogonal, and the system places all state in the quadrant where at most one axis applies.

This is the deepest of the three barriers. Even in a hypothetical system that relaxed single-owner control and eliminated the version-forking mechanism, CO3 and CO4 would prevent concurrent modification of shared content simply because there is no shared mutable state to contest.

---

## What Remains: Same-Owner, Same-Document Operations

The three barriers — single-writer ownership (CO0), denial-as-fork (CO1), and content immutability (CO3/CO4) — eliminate all cross-user and cross-document conflicts. But they do not address one remaining case: what happens when the *same owner* issues multiple operations against the *same document* in rapid succession?

This is the residual concurrency question. A single user with two frontend sessions open to the same backend, or a single frontend issuing pipelined requests, can produce multiple pending operations on the same document. The first two barriers do not apply — the user owns the document and both sessions are legitimate writers.

We must reason about this case precisely. It turns out there is a further barrier, and then — finally — the irreducible residual.

---

## The Write Access Invariant

The system maintains at most one session with write access to each document version. We refine CO-Σ4.

**CO5 (Write exclusivity).** `Σ.W` is a partial function — each document maps to at most one session:

    (A d : d ∈ dom(Σ.W) : #{ s : Σ.W(d) = s } = 1)

When a second session requests write access to a document already held by another session, the system applies denial-as-fork: the second session receives a new version. This is the same mechanism as CO1, but operating at the session level rather than the user level — even when both sessions belong to the same user.

Gregory's implementation confirms this through the BERT (backend resource table) protocol. When session B attempts to open a document already held for write by session A, the system creates a new version for session B via the BERTMODECOPYIF mode. The two sessions then operate on independent V-space arrangements with no interaction. No code path exists to merge the diverging versions.

The consequence: even for the same owner with two sessions, the system routes them to different document versions. Same-document write contention between sessions is resolved before any mutating operation executes.

**CO6 (Pre-mutation resolution).** All write contention is resolved at document-open time, not at mutation time:

    [s₁ ≠ s₂ ∧ Σ.W(d) = s₁  ⇒  s₂ cannot mutate d]

A mutating operation on document `d` by session `s` requires `Σ.W(d) = s` as a precondition. If this precondition fails, the operation does not execute — it does not partially execute, it does not queue, it does not conflict. The contention is resolved *before* any state change.

This is architecturally significant. In most concurrent systems, conflict detection occurs during or after the operation (optimistic concurrency) or operations block waiting for access (pessimistic concurrency). Xanadu resolves contention by *forking the target* — creating a new document that the second session can write freely. The contention disappears because the two sessions are no longer writing to the same state.

We observe a notable implementation detail that illustrates the strength of the pre-mutation resolution guarantee. Gregory's implementation sends success acknowledgment to the client *before* executing the mutation — the response fires before the data structures change. This means a mutation that fails its write-access check still appears successful to the client. The abstract specification must therefore demand either that write-access checks are infallible for sessions that properly acquired access via CO5, or that the system provides a separate mechanism for detecting silent failures. The pre-mutation resolution model (CO6) satisfies the first option: if you hold write access, your mutations succeed; if you do not, you were already routed to a forked version before you could issue a mutation.

---

## Serialization of Operations Within a Session

Having eliminated cross-user conflicts (CO0), cross-session conflicts (CO5/CO6), and cross-document conflicts (CO4), we arrive at the truly irreducible case: multiple operations issued by the same session against the same document. This is the only scenario where two mutating operations can legitimately target the same `Σ.V(d)`.

Even here, the operations do not execute concurrently. They serialize.

**CO7 (Operation atomicity).** Each mutating operation transforms `Σ.V(d)` atomically. No intermediate state is observable between the beginning and end of any single operation. Formally, for any operation `op` taking `Σ` to `Σ'`:

    [Σ.V(d) transitions directly to Σ'.V(d)]

with no state `Σ''` such that `Σ.V(d) ≠ Σ''.V(d) ≠ Σ'.V(d)` is observable by any other operation.

Gregory's implementation evidence is instructive here. The `makegappm` function, which shifts V-positions during INSERT, performs its entire displacement loop without allocating memory — making it impossible for the cache eviction mechanism to interrupt the shift. The displacement of all affected entries is a single uninterrupted pass over the tree's children. No signal handler touches the data structures during mutation. The atomicity is not achieved through transactions or locks but through the stronger property of non-interruptibility within the single-threaded event loop.

**CO8 (Sequential composition).** When multiple operations `op₁, op₂, ...` target the same document, they compose sequentially. Each operation sees the complete result of all prior operations:

    [Σ₂ = op₁(Σ₁)  ∧  Σ₃ = op₂(Σ₂)]

The second operation's preconditions are evaluated against the post-first-operation state, not the pre-first-operation state. In particular:

- V-positions in `op₂`'s arguments refer to positions in `Σ₂.V(d)`, not `Σ₁.V(d)`.
- I-addresses allocated by `op₁` are visible to `op₂`'s allocation queries.
- Content placed by `op₁` exists in `Σ₂.I` and can be referenced by `op₂`.

Gregory's implementation achieves this through a single-threaded event loop with run-to-completion dispatch. Each operation executes in its entirety — parsing, mutation, response — before the next operation begins. The scheduling is deterministic: when multiple sessions have pending requests, they are processed in a fixed order determined at connection time. But the *abstract* property does not depend on single-threading — it requires only that operations compose as if they executed sequentially, which any serializable execution achieves.

A critical consequence of CO8 is that the system performs no *operational transformation*. When two operations target overlapping V-positions, the second operation's V-address arguments are used as-is against the post-first-operation state. The system does not adjust the second operation's coordinates to account for shifts produced by the first. This means the frontend must either (a) compose its operations knowing the serialization order, or (b) accept that V-position arguments computed before the first operation may refer to different content in the post-first-operation arrangement. Gregory confirms there is no adjustment: the V-address from the protocol message becomes the V-dimension coordinate directly, with no translation.

---

## Consequences of Serialization

We can now derive what the system guarantees about the result of multiple operations targeting the same content.

### Two INSERTs at the same V-position

Let `Σ₁` be the state before either operation. Session issues INSERT(d, p, text₁) followed by INSERT(d, p, text₂). We derive the final state.

After `op₁ = INSERT(d, p, text₁)`, by the definition of INSERT:

    Σ₂.V(d)(v) = Σ₁.V(d)(v)                 for v < p
    Σ₂.V(d)(v) = fresh₁(v − p)              for p ≤ v < p + |text₁|
    Σ₂.V(d)(v) = Σ₁.V(d)(v − |text₁|)      for v ≥ p + |text₁|

After `op₂ = INSERT(d, p, text₂)` operating on `Σ₂`:

    Σ₃.V(d)(v) = Σ₂.V(d)(v)                 for v < p
    Σ₃.V(d)(v) = fresh₂(v − p)              for p ≤ v < p + |text₂|
    Σ₃.V(d)(v) = Σ₂.V(d)(v − |text₂|)      for v ≥ p + |text₂|

Substituting the first into the second, the final arrangement at position p is `text₂` followed by `text₁` followed by the original content shifted right by `|text₁| + |text₂|`. The second insertion prepends to the first at the insertion point — a last-in-first-out ordering.

Two observations. First, the V-space arrangement depends on the order: if `op₂` had executed first, `text₁` would prepend to `text₂`. Second — and this is the crucial invariant — no content is lost regardless of order:

**CO9 (Content preservation under serialization).** For any sequence of operations `op₁, ..., opₖ` on document `d`:

    (A i : 1 ≤ i ≤ k ∧ opᵢ = INSERT(d, pᵢ, textᵢ) :
       (E v : v ∈ dom(Σₖ₊₁.V(d)) : Σₖ₊₁.V(d)(v) maps to fresh addresses for textᵢ))

Every INSERT's content appears *somewhere* in the final arrangement, provided no subsequent DELETE removes it from V-space. Even if a DELETE does remove it from the arrangement, the content persists in I-space by CO3 — it is merely no longer *displayed*, not destroyed.

### DELETE and INSERT at overlapping positions

Consider DELETE(d, [p, p+w)) followed by INSERT(d, p, text). After the DELETE, content formerly at positions `[p, p+w)` is removed from V-space (but persists in I-space by CO3). After the INSERT, new content is placed at position p in the post-deletion arrangement.

If the order were reversed — INSERT first, then DELETE — the DELETE's span `[p, p+w)` would cover different content in the post-insertion arrangement, potentially removing some of the just-inserted text from V-space.

The V-space arrangements differ. But the I-space invariant holds in both cases:

**CO10 (I-space content invariance under ordering).** For any two serialization orders `σ₁` and `σ₂` of the same set of operations, the resulting I-space content sets are identical. Let `content(Σ) = { Σ.I(a) : a ∈ dom(Σ.I) }` be the multiset of content values. Then:

    content(Σ_σ₁) = content(Σ_σ₂)

*Proof.* I-space is append-only (CO3). Each INSERT allocates fresh addresses and appends content; DELETE, REARRANGE, and COPY do not modify I-space. The *addresses* allocated by each INSERT depend on the current maximum I-address, which is order-dependent — if INSERT₁ executes before INSERT₂, their allocated addresses differ from the reverse order. But the *content bytes* stored by each INSERT are determined solely by the INSERT's arguments, not by any prior state. And by CO3, no content is ever removed. Therefore every INSERT's content values appear in the final I-space regardless of ordering, and no other operation adds or removes values. The multiset of stored content is order-invariant. ∎

We must be precise about what is and is not invariant. The *content values* stored in I-space are order-independent. The *addresses* at which those values reside may differ between serialization orders. This distinction matters: links and transclusions reference specific I-addresses, so the address assignment produced by a particular serialization order becomes part of the system's committed state. The content invariance is a guarantee about *what* is preserved; the address assignment is a consequence of *when* each operation executed.

This is an important asymmetry: **I-space content is order-independent; V-space arrangement is order-dependent.** The permanent, shared, citable layer of the system preserves all contributed content regardless of scheduling. The mutable, per-document layer is where ordering determines arrangement.

---

## The Order-Dependent Residual

We have established that I-space content is order-invariant (CO10) and that inserted content is preserved (CO9, subject to subsequent deletion from V-space). What remains order-dependent is precisely and only the V-space arrangement of the document being modified.

**CO11 (V-space order-dependence).** For two operations `op₁` and `op₂` targeting the same document at overlapping V-positions, the final V-space arrangement may depend on the execution order:

    [op₁(op₂(Σ)).V(d) ≠ op₂(op₁(Σ)).V(d)]  is possible

This is not a defect but a well-defined property. The system does not claim that V-space arrangement is order-independent — it claims that the *permanent content store* is order-independent and that each serialization order produces a *valid* arrangement (satisfying referential integrity, dense contiguity, and all V-space invariants).

We ask: what abstract property must the serialization satisfy?

**CO12 (Serialization consistency).** The system must guarantee that the final state is consistent with *some* serial execution of the pending operations. Formally, for any set of operations `{op₁, ..., opₖ}` that are concurrently pending:

    (E π : π is a permutation of {1,...,k} :
       Σ_final = op_{π(k)}(...(op_{π(2)}(op_{π(1)}(Σ_initial)))...))

The implementation chooses a particular serialization order (determined by session connection order in Gregory's implementation). The abstract specification requires only that *some* valid serialization exists and that the final state is consistent with it.

This is *serializability* in the classical sense. It is weaker than requiring a specific ordering (which would be *linearizability with respect to a particular clock*) but stronger than allowing arbitrary interleaving. The system behaves as if operations executed one at a time, in some order.

---

## Version Isolation

When a version is created from a document, it captures the document's current V-space arrangement. After creation, the version and the original are independent.

**CO13 (Version isolation).** For any version `d'` created from document `d` at state `Σ`, and any subsequent operation `op` on `d` producing `Σ'`:

    Σ'.V(d') = Σ.V(d')

Operations on the original do not affect the version. Operations on the version do not affect the original. The version captured whatever arrangement existed at the moment of creation — pre-operation or post-operation, depending on serialization order — but once captured, it is immune.

The version creation operation itself follows CO8 (sequential composition): it reads the live arrangement at the moment it executes and copies that arrangement into the new document's V-space. If an INSERT and a CREATENEWVERSION are both pending, the version captures the pre-INSERT or post-INSERT state depending on which serializes first. Gregory confirms that version creation reads the live V-space state with no snapshot mechanism — consistency is provided by CO7 (atomicity), which prevents any other operation from modifying the arrangement mid-read.

---

## Link Survival

Links attach to I-space content, not V-space positions. We now show that this design decision makes link survival a trivial consequence of I-space immutability, regardless of operation ordering.

**CO14 (Link survival under concurrent operations).** For any link `ℓ` whose endsets reference I-space addresses `A_ℓ ⊆ dom(Σ.I)`, and any sequence of operations (in any order):

    (A a : a ∈ A_ℓ : a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a))

*Proof.* By CO3 (I-space immutability), no operation removes addresses from `dom(Σ.I)` or modifies their content. The link's endset addresses remain valid regardless of what operations execute, in what order, against what documents. ∎

Nelson is explicit that this is architectural: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." The "if anything is left" condition is always satisfied because I-space is append-only — content bytes are never removed.

We observe an important contrast with V-space. A link endset that referenced V-space positions would need to be updated every time an INSERT or DELETE shifted positions. A link endset that references I-space addresses needs no update ever. The design choice to attach links to I-space is what makes link survival order-independent.

Consider the scenario where session A deletes content from V-space while session B simultaneously creates a link to that same content. The operations are orthogonal: DELETE modifies V-space; MAKELINK creates an I-space link structure whose endsets reference I-space addresses. The link survives the deletion because it never depended on the V-space arrangement. The deleted content persists in I-space and remains reachable through the link's endsets, even though no document currently displays it.

---

## Transclusion and the Window Modes

When a document transcludes content from another document, the transclusion's behavior under concurrent editing depends on its *window mode*. Nelson provides two:

**Time-fixed windows.** The transclusion captures the source document's arrangement at a specific moment. Subsequent edits to the source are invisible until the reader explicitly queries "What has this passage become?" Nelson: "A quotation — an inclusion window — may be fixed to another document... at a certain point in time."

**Location-fixed windows.** The transclusion tracks the source document's current arrangement. Edits to the source are reflected automatically. Nelson: "Or second, at a relatively fixed location in the document space, in which case updates are seen automatically."

For time-fixed windows, concurrent operation ordering is irrelevant — the window sees a frozen state. For location-fixed windows, the window reflects whatever arrangement the source document currently has, which depends on the serialization order of operations on the source.

**CO15 (Transclusion independence).** Multiple transclusions of the same content from different documents are independent of each other:

    (A d₁ ≠ d₂ : d₁ transcludes from d₀ ∧ d₂ transcludes from d₀ :
       d₁'s transclusion behavior is independent of d₂'s transclusion behavior)

Each transclusion independently resolves against the source document's state. Two transclusions need not agree, synchronize, or converge. One may be time-fixed while the other is location-fixed. There is no coupling mechanism between them. This follows from the fact that transclusions are V-space structures in the *transcluding* document, and each document's V-space is independent (CO4).

---

## The Architectural Argument

We can now state the complete architectural argument for concurrent operation ordering in Xanadu.

The system addresses concurrent modification through four levels of prevention, each progressively narrower in scope:

1. **Cross-user conflicts** are eliminated by CO0 (single-writer ownership). Two users cannot modify the same document.

2. **Cross-user modification needs** are addressed by CO1 (denial-as-fork). The non-owner gets a new version — a separate document with independent state.

3. **Cross-session conflicts** on the same document are eliminated by CO5/CO6 (write exclusivity, pre-mutation resolution). The second session gets a forked version.

4. **Same-session sequential operations** are governed by CO7/CO8 (atomicity, sequential composition). Each operation sees the complete result of its predecessors.

At every level, the resolution is the same: either the conflict is prevented (by routing to separate state) or it is serialized (by atomic sequential composition). There is no merge, no operational transformation, no conflict resolution algebra. The system never faces a state where two modifications must be combined — it either prevents the situation or serializes it.

The permanent content store (I-space) is immune to all ordering concerns (CO10). The mutable arrangement layer (V-space) depends on serialization order (CO11) but is always consistent with some serial execution (CO12). Links survive regardless of ordering (CO14). Versions capture a consistent snapshot at creation time and are thereafter independent (CO13).

We observe that Nelson did not specify the serialization mechanism — no locking protocol, no session lifecycle, no transaction model appears in his design. He specified the *architectural properties* (single ownership, immutable I-space, versioning by inclusion) that make the concurrent modification problem largely disappear. The residual serialization requirement — that operations within a single session compose sequentially — is left to the implementation. Gregory's implementation satisfies it through a single-threaded event loop with run-to-completion dispatch, but any mechanism that provides CO7 and CO8 suffices.

The system's answer to "what determines the final state?" is therefore: the *architectural barriers* determine that most concurrent modification scenarios cannot arise, and for the narrow residual of same-session operations, *serialization order* determines the V-space arrangement while *content permanence* guarantees that the I-space result is order-invariant. The answer to "what invariants must the resolution satisfy?" is: content is never lost (CO9), permanent storage is order-independent (CO10), every final state corresponds to some serial execution (CO12), and versions are isolated after creation (CO13).

---

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CO-Σ1 | `Σ.owner : DocId → UserId` — each document has exactly one owner | introduced |
| CO-Σ2 | `Σ.I : IAddr ⇀ Byte` — global permanent content store | introduced |
| CO-Σ3 | `Σ.V(d) : VPos ⇀ IAddr` — per-document mutable arrangement | introduced |
| CO-Σ4 | `Σ.W : DocId ⇀ SessionId` — write access is a partial function | introduced |
| CO-Σ5 | `Σ.vers : DocId → Set(DocId)` — version derivation relation | introduced |
| CO0 | Single-writer ownership: only the document owner may issue mutating operations | introduced |
| CO1 | Denial-as-fork: write denial creates a new version for the requesting user | introduced |
| CO2 | No privileged version: all versions in the derivation DAG are co-equal | introduced |
| CO3 | I-space immutability: no operation alters content at existing I-addresses | introduced |
| CO4 | Orthogonality: mutable state (V-space) is per-document; shared state (I-space) is immutable | introduced |
| CO5 | Write exclusivity: at most one session holds write access per document version | introduced |
| CO6 | Pre-mutation resolution: write contention is resolved at open time, before any mutation | introduced |
| CO7 | Operation atomicity: each operation's state transition is unobservable mid-execution | introduced |
| CO8 | Sequential composition: each operation sees the complete result of all prior operations | introduced |
| CO9 | Content preservation: every INSERT's content appears in the arrangement unless subsequently deleted from V-space; persists in I-space unconditionally | introduced |
| CO10 | I-space content invariance: the multiset of content values is identical under all serialization orders | introduced |
| CO11 | V-space order-dependence: final arrangement may depend on execution order for overlapping operations | introduced |
| CO12 | Serialization consistency: the final state is consistent with some serial execution | introduced |
| CO13 | Version isolation: operations on the original do not affect a created version, and vice versa | introduced |
| CO14 | Link survival: link endsets referencing I-space addresses remain valid under all operation sequences | introduced |
| CO15 | Transclusion independence: multiple transclusions of the same content are mutually independent | introduced |

---

## Open Questions

What must the system guarantee about the relationship between version creation time and the set of operations whose effects the version captures?

Must the serialization order be deterministic given the same set of pending operations and system state, or is bounded nondeterminism in serialization order acceptable?

What invariants must the write-access transfer protocol satisfy when ownership of a document changes?

Must the system provide a mechanism for a document owner to observe which versions have been derived from their document?

What must the system guarantee about I-address allocation uniqueness across serialization orders — is address identity or only content identity required to be order-invariant?

What consistency must location-fixed transclusion windows provide when the source document is being actively edited — must reads observe a complete operation's effect or may they observe pre-operation state indefinitely?

What properties must the comparison operation (SHOWRELATIONOF2VERSIONS) satisfy when both versions are being concurrently edited by their respective owners?

Must the system guarantee that denial-as-fork produces a version whose arrangement is identical to the source at the moment of forking, or may it capture an approximate arrangement?
