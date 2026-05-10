# ASN-0019: Operation Journaling

*2026-02-25*

## The Question

What must the system guarantee about recording and replaying the history of operations performed on content? What properties must an operation log satisfy for faithful state reconstruction?

We are looking for the invariants that govern how a system built on permanent content and mutable arrangement can promise that any prior state is recoverable. The word "journaling" suggests a log of operations — but as we shall discover, the architecture gives a surprising answer: the guarantee is about *reconstruction*, not *replay*, and the deepest question is what separates these two concepts formally.

## The Reconstruction Guarantee

Nelson states the user-facing promise without equivocation:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

Let us state this precisely. We model system state at any moment as a pair Σ = (I, M) where I is the content store and M is a collection of arrangement mappings — one per document. The guarantee is:

**R0 (Reconstruction Guarantee).** For every document d and every moment t at which the system accepted a snapshot command for d, there exists a version identifier v(d,t) such that the system can produce the complete state M(d, t) — the arrangement of d at time t — from its current state alone, without external input.

We write this as: `[snapshot_taken(d, t) ⇒ recoverable(d, t)]`.

The word "moment" requires care. Nelson's vision — "successive instants of time, alive in the space-time vortex" [LM 2/15] — suggests continuous temporal coverage. But his protocol provides only a discrete snapshot command (CREATENEWVERSION). We must separate what is promised from what is mechanised.

## Two Modes of Recovery

Nelson explicitly distinguishes two approaches to historical recovery and rejects one:

> "Being able to go back through changes, and perhaps restore an earlier state, is called the problem of historical backtrack. For simple, linear textual documents this can be done by storing lists of changes and undoing them; and indeed several commercial versioning and backtrack systems are now on the market. But it is rather more difficult to do this for hypertext." [LM 3/13]

This passage names the operation-replay approach, acknowledges it works for linear text, and flags it as insufficient for hypertext. Nelson chose an alternative: permanent content with reconstructible arrangements.

We must formalise both approaches to understand why the choice matters.

**Approach 1: Operation Replay.** Record a sequence of operations o₀, o₁, ..., oₙ. To recover the state after oₖ, start from an initial state Σ₀ and apply o₀ through oₖ in order. This requires:

- A complete, ordered record of every operation
- A well-defined initial state
- Deterministic replay: applying oᵢ to the same state always produces the same result

**Approach 2: Structural Reconstruction.** Store content permanently and take snapshots of arrangements at discrete points. To recover the state at snapshot k, read the snapshot's arrangement mapping directly. This requires:

- Permanent content (I-space never loses data)
- Snapshot fidelity (the arrangement mapping is exactly preserved)
- No replay; recovery is a read, not a computation

Nelson chose Approach 2. We must understand why — and what properties each approach demands.

## Why Replay Fails for This Architecture

Let us examine what replay would require and where it breaks.

### The Non-Invertibility of DELETE

Consider a document d with arrangement mapping m : V → I. DELETE(d, v₁..v₂) removes the V-space interval [v₁, v₂) from d's arrangement, destroying the V→I mappings for that range. The I-space content persists — bytes at those I-addresses are never destroyed — but the *mapping* is gone.

Now suppose we attempt to "undo" this DELETE by re-inserting the same textual content. INSERT allocates *fresh* I-addresses for the new content. Even if the characters are identical, the I-space identity is different. We state this as:

**J0 (Non-Invertibility of DELETE).** Let Σ be the state before DELETE(d, v₁..v₂), and let Σ' be the state after DELETE followed by INSERT of identical text at the same V-position. Then Σ ≠ Σ', because the I-addresses of the re-inserted content differ from the originals.

Formally: let α₁..αₙ be the I-addresses mapped by v₁..v₂ before deletion. After DELETE + INSERT of the same text, the new V-range maps to β₁..βₙ where βᵢ ≠ αᵢ for all i. The content bytes are identical — `content(αᵢ) = content(βᵢ)` — but the *identity* differs.

This non-invertibility is not a deficiency. It is the direct consequence of append-only I-space allocation: every INSERT allocates fresh addresses, and no mechanism exists to "reclaim" a previously used address. The invariant that makes the system trustworthy — permanent I-space identity — is the same invariant that prevents naive undo.

Why does this matter for replay? Because a replay mechanism that attempts to reconstruct a state by "undoing" operations backward from the current state will produce the wrong I-addresses. And I-addresses are not mere implementation detail — they are the foundation of attribution, correspondence, royalty calculation, transclusion identity, and link survivability. A state with the right characters at the right positions but the wrong I-addresses is *not* the same state.

### The I-Space Identity Conservation Law

This leads us to a fundamental property that any reconstruction mechanism must respect:

**J1 (I-Space Identity Conservation).** Any faithful reconstruction of a prior state must preserve the I-space identity of every piece of content. Specifically, if content at V-position v in the reconstructed state maps to I-address α, then in the original state content at the same V-position v also mapped to I-address α.

This is not an arbitrary requirement. Every guarantee that depends on shared I-space origin — and there are many — would break without it:

1. **Correspondence.** Two versions of a document can be compared "word for word" [LM 2/20] because they share I-addresses. SHOWRELATIONOF2VERSIONS computes correspondence by examining shared I-space origin. If reconstruction assigns different I-addresses, correspondence is destroyed.

2. **Attribution.** "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. The I-address encodes the originating document and user. Different I-address, different attribution.

3. **Transclusion identity.** When content is transcluded (COPY), the target document's V-space maps to the *same* I-addresses as the source. FINDDOCSCONTAINING searches by I-address to find all documents sharing content. New I-addresses sever this connection.

4. **Royalty calculation.** "The original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" [LM 2/45]. "Who wrote what" is determined by I-addresses. Wrong addresses, wrong royalties.

5. **Link refractive following.** "A link to one version of a Prismatic Document is a link to all versions" [LM 2/26] because links reference I-space bytes and correspondence tracks those bytes across versions. Break the I-addresses, break the refractive following.

J1 tells us that replay mechanisms face a stringent correctness criterion: they must not merely reproduce the same *text* at the same *positions* — they must reproduce the same *identity* at the same positions. This immediately rules out naive undo/redo based on re-executing INSERT and DELETE, since INSERT always mints fresh identity.

### The Distinction Between INSERT and COPY

A faithful replay mechanism must also preserve the distinction between operations that create new I-space content and operations that create new V-space mappings to existing I-space content:

**J2 (Creation-Reference Distinction).** An operation log must distinguish between INSERT (which allocates new I-addresses) and COPY (which maps V-positions to existing I-addresses). Conflating these in replay would violate J1: replaying a COPY as an INSERT would create fresh I-addresses where the original state had shared ones.

Implementation evidence confirms this distinction matters: INSERT calls `inserttextingranf` to allocate fresh I-addresses before passing them to `docopy`, while COPY calls `specset2ispanset` to resolve existing source content to its I-addresses and passes those to `docopy`. Both paths produce structurally identical entries in the downstream index (DOCISPAN records `(document, I-address-range)` with no operation-type flag) — but the I-addresses themselves differ, and that difference is the semantic content.

## The Architecture's Answer: Structural Reconstruction

Nelson's architecture avoids the replay problem entirely by storing enough information to reconstruct any snapshotted state without replaying anything. The mechanism rests on a three-layer permanence model.

### The Three-Layer Model

The system maintains three persistent structures, each with distinct mutability:

| Layer | Contents | Mutability |
|-------|----------|------------|
| Content store (I-space) | I-address → content bytes | Append-only: content is added, never modified or removed |
| Membership index | (Document, I-address-range) pairs | Write-only: entries accumulate, never removed |
| Arrangement mapping (V-space) | V-address → I-address, per document | **Mutable**: INSERT, DELETE, REARRANGE modify this |

We can state the permanence properties of the first two layers:

**J3 (I-Space Permanence).** `(A α : α ∈ dom(I) : content(α) is immutable)`. Once an I-address is allocated and its content stored, that content never changes and the address is never reused.

**J4 (Membership Monotonicity).** The membership index only grows. If at time t the index records that document d references I-address range [α, α+w), then at all times t' > t this entry persists. (Note: this means the index may contain stale entries — it asserts "document d once referenced this content" even after DELETE removes the V-space mapping.)

**J5 (Arrangement Mutability).** The arrangement mapping for a document d — call it m_d : V → I — is the sole locus of destructive mutation. INSERT, DELETE, and REARRANGE modify m_d. No other layer is destructively modified.

This asymmetry — permanent content, permanent membership, mutable arrangement — is the key insight. The content (what) is never lost. The arrangement (where) is mutable. Recovery means recovering the arrangement, because the content it arranges is always there.

### How CREATENEWVERSION Provides Reconstruction

The system provides exactly one mechanism for preserving arrangement state:

**J6 (Version Snapshot).** CREATENEWVERSION(d) creates a new document d' whose arrangement mapping m_{d'} is a copy of d's current arrangement mapping m_d at the moment of the call. The new document receives a fresh permanent identifier whose address encodes its derivation from d. After the snapshot, edits to d do not affect m_{d'}, and vice versa — the two arrangement mappings are independent.

Formally: let t be the moment CREATENEWVERSION(d) executes, producing d'. Then:

`(A v : v ∈ dom(m_d(t)) : m_{d'}(t) .v = m_d(t) .v)`

And for all t' > t:

`(A v : v ∈ dom(m_{d'}(t')) : m_{d'}(t') .v = m_{d'}(t) .v)` — provided no operations modify d'.

This is not operation replay. It is direct preservation: the mapping is copied whole. Reconstruction of the state at time t means reading m_{d'}, which contains the exact V→I associations that m_d held at time t — including the correct I-addresses, satisfying J1 automatically.

The crucial observation: **J6 is the only mechanism.** If no CREATENEWVERSION was called before a destructive operation, the pre-operation arrangement is irrecoverably lost. We state this as:

**J7 (Reconstruction Completeness Bound).** `recoverable(d, t) ⟺ (E v : v = CREATENEWVERSION(d) at time t' ≤ t : m_v preserves m_d(t))`. A document's arrangement state at time t is recoverable if and only if a version snapshot was taken at or before t that captures that state.

This is a strong claim. Let us verify it by examining whether any other path could reconstruct the arrangement.

### What the Permanent Layers Cannot Recover

After DELETE(d, v₁..v₂), the V→I mappings for the deleted range are destroyed. Can we recover them from the permanent layers?

**The content store:** It maps I-addresses to bytes. Given an I-address α, we can retrieve its content. But the content store does not record which V-address α was mapped from — the V→I direction is exclusively the arrangement mapping's responsibility. The content store answers "what is at this I-address?" but cannot answer "where was this I-address in document d's V-space?"

**The membership index:** It records (document, I-address-range) pairs. After DELETE, the entry persists — we can determine that document d once contained content at I-addresses α₁..αₙ. But the index records no V-position: it answers "did this document ever reference this content?" not "at what V-position?"

**Neither layer, nor both together, can recover V-position.** This is not an oversight but a structural consequence of J5: V-position is the mutable layer's exclusive information. There is no shadow copy, no redundant encoding, no way to infer V-position from I-address and membership alone.

## The Unimplemented Historical Trace

The implementation evidence reveals something remarkable: the designers did intend a richer history mechanism than CREATENEWVERSION alone. A protocol opcode (NAVIGATEONHT, opcode 9) was assigned for navigating a "historical trace" — an addressable entity with its own ISA (permanent identity address) and a navigation path type (`typehtpath`). Every mutating operation in the implementation layer had a hook site — `/* ht stuff */` — where the historical trace would have been updated as a side effect of each mutation.

The hook sites were deliberately designed. At the INSERT operation, a comment notes: "no ht stuff here, 'cause it's taken care of in docopy" — the author had reasoned about where the hooks should fire and where they were redundant. This is not a forgotten placeholder but an unfinished feature with conscious architectural allocation.

The feature was never implemented. The protocol opcode routes to an error message. The navigation type `typehtpath` was declared but never defined. Every layer of the stack — input parsing, implementation, output formatting — has a comment placeholder and nothing more.

What would this historical trace have provided? We can infer from its structure:

1. It had its own **permanent address** (htisa) — making it a first-class entity in the address space, not metadata.
2. It had **navigation instructions** (typehtpath) — it was traversable, not merely a flat log.
3. It was built **incrementally** as a side effect of mutations — each edit would have extended the trace.
4. It was per-document (the hook sites are inside per-document operations).

This suggests a mechanism that would have strengthened J7: a document whose historical trace was maintained could have been reconstructed to *any* prior state, not just to snapshotted states. The trace would have recorded enough information to reverse arrangement mutations — not by "undoing" them (which J0 shows is impossible for I-space identity) but by recording the V→I mappings that each mutation destroyed.

We cannot specify what the historical trace would have guaranteed, because it was never completed. But its existence as a design artifact tells us that J7's limitation — recovery only at snapshot boundaries — was understood to be a limitation, not a feature. The designers intended continuous recoverability and allocated architecture for it, then shipped with discrete snapshots as the available mechanism.

## What an Operation Journal Must Preserve

We are now in a position to state what properties an operation log must satisfy, should an implementation choose to provide one. These properties are consequences of J0–J7.

**J8 (Identity Preservation).** If a journal records an operation that created I-space content (INSERT, APPEND), the journal must record the I-addresses allocated. If a journal records an operation that references existing I-space content (COPY, CREATENEWVERSION), the journal must record which I-addresses were referenced. Replaying from the journal must produce the same I-address assignments as the original execution. This follows from J1.

This is the most demanding property. It means a journal cannot simply record "INSERT 'hello' at V-position 5" — it must record "INSERT 'hello' at V-position 5, allocated I-addresses α₁..α₅." Without the I-addresses, replay would mint new ones, violating J1.

**J9 (Arrangement Capture).** For any operation that destroys V→I mappings (DELETE, REARRANGE), the journal must record the pre-operation V→I associations for the affected range. This is the information J5 tells us is mutable and J7 tells us is otherwise irrecoverable.

Together, J8 and J9 ensure that the journal captures what the permanent layers cannot: the V-position of content before it was moved or removed, and the I-identity of content when it was created.

**J10 (Per-Document Ordering).** Operations within a single document must be journaled in the order they were applied. This follows from the fact that the arrangement mapping is the cumulative result of sequential operations — the state after operation k depends on the state after operation k−1.

We observe that global ordering across documents is not required. I-address allocation is per-document — the allocation for document d₁ and the allocation for document d₂ are in disjoint address ranges and do not interact. The ownership model (only the owner modifies a document) prevents concurrent mutations to the same document. Thus operations on different documents are independent and need not be globally ordered.

**J11 (Link-Content Parity).** Links must be journaled with equal fidelity to content. Nelson explicitly gives deleted links identical treatment to deleted bytes — both are "not currently addressable, awaiting historical backtrack functions, may remain included in other versions" [LM 4/9]. Links have permanent creation-order addresses within their document's link subspace. A journal that records content operations but omits link operations would fail to reconstruct the complete document state.

This extends to metadata, because most metadata in this architecture IS links — title, author, and supersession are all link types [LM 4/52]. Journaling "content changes" without "metadata changes" is a false distinction: the metadata is content.

**J12 (Journal Permanence).** The journal itself must be permanent and append-only. Since the journal records information (pre-deletion V→I mappings) that exists nowhere else in the system, losing journal entries makes the corresponding states irrecoverable. Revising entries would violate the reconstruction guarantee for the affected states. This follows from the same reasoning that makes I-space append-only: information that is the sole record of a fact must not be destroyed.

## The Boundary Between Continuous and Discrete Recovery

We can now state precisely where the system's recovery capability lies on the continuum between "recover any instant" and "recover only snapshots":

**Without a journal or historical trace:** Recovery is limited to version snapshots (J7). Between snapshots, arrangement state is mutable and unrecoverable after destruction. The system satisfies R0 only at snapshot boundaries.

**With a journal satisfying J8–J12:** Recovery extends to every journaled operation. The state after any prefix of the journal can be reconstructed: start from the nearest prior snapshot and replay forward, or start from the journal's beginning and replay the full sequence. R0 holds at every operation boundary.

**With the intended historical trace (never implemented):** Recovery would have been navigable — not merely sequential replay but indexed access to any prior state, traversable by a path type. This would have made R0 hold at every operation boundary with efficient random access rather than sequential replay.

The current design chose discrete snapshots. The user is responsible for calling CREATENEWVERSION before any edit whose prior state might need recovery. The system provides no triggering mechanism, no automatic journaling, and no undo facility. This is an explicit delegation of responsibility to the client — a design choice, not an oversight, given that the historical trace mechanism was architected but not completed.

## On the Permanence of the Journal Itself

We note a subtle circularity in J12. The journal must be permanent — but the system's permanence guarantees (J3, J4) apply to I-space and the membership index. The journal is neither of these. Where does the journal live?

One option: the journal is itself content in I-space. Operations on document d produce journal entries that are stored as content in a dedicated journal document. Since I-space is append-only, the journal inherits J3's permanence. Since the journal document has a permanent address and ownership, it inherits the attribution model.

Another option: the journal is a separate mechanism outside the content model — a log file, a write-ahead log, a separate database. This is architecturally simpler but places the journal outside the system's permanence guarantees. The journal's durability becomes an additional requirement, not a consequence of existing invariants.

Nelson does not prescribe either approach. The implementation evidence shows a session-scoped replay log (`interfaceinput`) that records raw FEBE protocol bytes for mutating operations — but this log is forensic, session-scoped, and not integrated into any recovery machinery. It records the wire format of commands but does not capture the I-addresses allocated by INSERT (violating J8) or the pre-deletion V→I mappings (violating J9). It is a diagnostic trace, not a recovery journal.

**J13 (Journal Self-Consistency).** If the journal is stored within the system's own content model (as I-space content), then the act of journaling is itself an operation that extends I-space. The journal must not record its own extension — this would create an infinite regress. The journal records operations on *user documents*; the journal's own growth is infrastructure, not user operation.

## A Calculational Derivation: What Replay Requires

Let us derive, by weakest precondition, what must hold for replay of a single INSERT to be faithful. Let the postcondition be:

R: m_d(v) = α ∧ α ∈ dom(I) ∧ content(α) = text ∧ (A v' : v' ≠ v ∧ v' ∈ dom(m_d) : m_d(v') = m_d₀(v'))

That is: the insertion placed text at V-position v, mapping to I-address α, the content at α is the given text, and all other V-positions are unchanged (frame condition).

We compute wp(INSERT(d, v, text), R):

wp(INSERT(d, v, text), R)
= { INSERT allocates a fresh α, stores text at α, maps v to α, shifts later positions }
  (E α : α ∉ dom(I) : content_new(α) = text ∧ m_d_new(v) = α ∧ frame)

For replay to produce the same result, we need the *same* α. But α was chosen by the allocator as the next unused I-address in d's subrange at the time of the original operation. For replay to allocate the same α, one of two conditions must hold:

(a) The allocator state at replay time is identical to the allocator state at original time — which requires all prior operations to have been replayed with the same allocations.

(b) The journal records α explicitly, and the replay mechanism uses the recorded α rather than the allocator.

Condition (a) is achievable but fragile: it requires exact correspondence of all prior operations. Condition (b) is robust: it makes each operation's replay independent of allocator state. J8 mandates condition (b).

We observe that under condition (b), the allocator itself becomes irrelevant during replay. The journal substitutes for it. This means the replay mechanism is simpler than original execution: it does not allocate, it places. The cost is that the journal is larger — each INSERT entry must carry its I-addresses.

## The Frame Problem

Every operation specification must state not only what it changes but what it preserves. For journaling, the frame problem manifests as: what *other* state must be preserved when an operation is journaled and replayed?

**J14 (Journal Frame Condition).** Replaying an operation from the journal must produce exactly the same effects and exactly the same non-effects as the original execution. Specifically:

For INSERT: (a) content at all I-addresses other than the newly allocated ones is unchanged; (b) V→I mappings at all V-positions other than the insertion point and the shifted region are unchanged; (c) the membership index gains exactly the entries it gained originally.

For DELETE: (a) I-space is unchanged (DELETE does not modify I-space); (b) V→I mappings outside the deleted range are unchanged (though positions may shift); (c) the membership index is unchanged (DELETE does not remove entries).

For COPY: (a) I-space is unchanged (COPY references existing content, does not create new content); (b) V→I mappings outside the insertion point are unchanged; (c) the membership index gains entries for the target document's reference to the copied I-addresses.

For MAKELINK: (a) content I-space is unchanged; (b) a new link with permanent address is created in the document's link subspace; (c) the link is discoverable by all link search operations that match its endsets.

The frame conditions for COPY deserve emphasis. COPY and INSERT produce identical downstream index entries (DOCISPAN records are structurally indistinguishable). But COPY does not allocate I-addresses — it references existing ones. A journal entry for COPY must record that this was a reference, not a creation, so that replay does not accidentally allocate fresh I-addresses (violating J1 and J2).

## Per-Document Temporal Ordering

We established that J10 requires per-document ordering. Let us examine why global ordering is unnecessary.

I-address allocation is scoped to a document's subrange within the address space. Each document d has a prefix p(d), and all I-addresses allocated for d's content lie in the range [p(d).1.0.1, p(d).2). The allocation function finds the current maximum I-address in this range and increments: `next(d) = max(I ∩ [p(d).1.0.1, p(d).2)) + 1`. Two documents d₁ and d₂ with different prefixes allocate from disjoint ranges — their allocations cannot interfere.

The ownership model provides the second guarantee: only the owner may modify a document. There is no scenario where two users simultaneously edit the same document. When a user wants to modify another's content, they create their own version — a new document under their own ownership. This turns potential conflicts into independent creations.

Together, these structural properties mean:

**J15 (Per-Document Independence).** The journal for document d₁ and the journal for document d₂ are independent. No entry in d₁'s journal depends on any entry in d₂'s journal. Replay of d₁ need not consult d₂'s journal, and vice versa.

This has a practical consequence: a distributed implementation can journal each document independently, at the owning node, without cross-node coordination. The absence of global ordering is not a limitation but a designed property that enables distribution.

There is one exception worth noting. Links can reference content across document boundaries — a link in document d₁ can point to content in document d₂. But links are stored in their *home* document (d₁), not in the referenced document (d₂). The link's creation is an operation on d₁ and appears in d₁'s journal. The link's *effect* on d₂ (making d₂'s content discoverable through a new link) is a query-time phenomenon, not a state mutation of d₂. Thus even cross-document links do not create journal dependencies between documents.

## On What the System Does Not Journal

Certain categories of state change are explicitly outside the journaling requirement:

**Reading.** "The network will not, may not monitor what is read or what is written in private documents" [LM 2/59]. Read operations leave no trace by design. The journal records only mutations.

**Administrative state.** Passwords, accounting data, and cash registers live in a "system area" architecturally distinct from document content [LM 5/13]. No historical backtrack is specified for these.

**Permission transitions.** Publication is a one-way, essentially permanent transition from private to published [LM 2/43]. There is no concept of toggling permissions over time, and the one transition that exists ("private → published") is meant to be irreversible. Journaling permission changes is nearly moot because there are essentially no reversible permission changes to journal.

## Summary of Requirements

We can now state the complete set of requirements for an operation journal, ordered by logical dependency:

The foundation is the I-Space Identity Conservation Law (J1): reconstruction must preserve I-addresses, not merely text content. This follows from the system's dependence on shared I-space origin for correspondence, attribution, transclusion, royalties, and link following.

Non-Invertibility (J0) tells us that naive undo cannot achieve J1, because INSERT always mints fresh identity. This rules out backward replay from the current state.

The Three-Layer Model (J3–J5) identifies the arrangement mapping as the sole locus of destructive mutation, making it the only layer that needs journaling — the other two are self-preserving.

The Version Snapshot Mechanism (J6) provides discrete reconstruction without journaling, but only at snapshot boundaries (J7). A journal extends reconstruction to every operation boundary.

The journal's own properties — Identity Preservation (J8), Arrangement Capture (J9), Per-Document Ordering (J10), Link-Content Parity (J11), Journal Permanence (J12), Self-Consistency (J13), Frame Conditions (J14), and Per-Document Independence (J15) — follow from the combination of J1 with the architectural constraints.

The deepest insight is that Nelson's architecture does not need an operation journal to fulfil its promises — it needs permanent content and explicit snapshots. The journal is an *optimisation* that extends the recovery window from snapshot boundaries to operation boundaries. The unimplemented historical trace would have extended it further, to navigable random access. But the foundational guarantee — that any snapshotted state is exactly recoverable — rests on the three-layer permanence model and the version mechanism, not on journaling.

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| R0 | For every snapshot taken of document d at time t, the system can reconstruct d's complete arrangement state from its current state alone | introduced |
| J0 | DELETE followed by INSERT of identical text does not restore the original state: I-addresses differ | introduced |
| J1 | Any faithful reconstruction must preserve the I-space identity (I-address) of every piece of content at every V-position | introduced |
| J2 | An operation log must distinguish INSERT (new I-addresses) from COPY (existing I-addresses) | introduced |
| J3 | I-space content is immutable once allocated and I-addresses are never reused | introduced |
| J4 | The membership index (document, I-address-range) only grows; entries are never removed | introduced |
| J5 | The arrangement mapping (V→I, per document) is the sole locus of destructive mutation in the system | introduced |
| J6 | CREATENEWVERSION creates an independent copy of a document's arrangement mapping at the moment of the call | introduced |
| J7 | A document's arrangement state is recoverable if and only if a version snapshot was taken that captures it | introduced |
| J8 | A journal must record I-addresses allocated by INSERT and I-addresses referenced by COPY | introduced |
| J9 | For operations that destroy V→I mappings (DELETE, REARRANGE), the journal must record the pre-operation mappings | introduced |
| J10 | Operations within a single document must be journaled in the order they were applied | introduced |
| J11 | Links must be journaled with equal fidelity to content; most metadata IS links | introduced |
| J12 | The journal itself must be permanent and append-only | introduced |
| J13 | If the journal is stored as I-space content, it must not record its own growth (no infinite regress) | introduced |
| J14 | Replaying a journaled operation must produce exactly the same effects and non-effects as the original | introduced |
| J15 | Journals for different documents are independent; no cross-document ordering is required | introduced |

## Open Questions

Must the system provide a mechanism for the user to request "the state of document d between snapshots," or is the snapshot-only recovery window (J7) a sufficient guarantee?

What must the system guarantee about the granularity of journaling — must every atomic operation be individually recoverable, or may the journal batch operations?

If the journal records pre-deletion V→I mappings (J9), must it also record the V-positions of content that was shifted (but not deleted) by an INSERT, or is the shift amount sufficient?

Must the system guarantee that journal entries are written atomically with the operations they record, or may a crash between operation and journal entry leave a gap?

What must the system guarantee about journal size relative to the content it describes — is there an upper bound on journal growth per operation?

What invariants must a navigable historical trace (as distinct from a sequential journal) satisfy to support efficient random access to any prior state?

Must the journal preserve the ordering of link creation within a document's link subspace, or is unordered link recovery sufficient given that link search is constraint-based rather than position-based?

What must the system guarantee about cross-document provenance when a COPY's source document is journaled on a different node than the COPY's target document?
