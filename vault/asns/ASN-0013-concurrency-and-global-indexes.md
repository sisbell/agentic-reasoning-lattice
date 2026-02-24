# ASN-0013: Concurrency and Global Indexes

*2026-02-24*

We wish to understand what a system with multiple concurrent users must
guarantee when those users modify separate documents that share content
identity through transclusion. The question is sharpened by the presence
of global indexes — a content-location index that tracks where every
piece of content appears, and a link index that maps content addresses to
the links that reference them. These indexes span the entire docuverse;
they are not scoped to any single document. When two users
simultaneously modify their own documents, both modifications may touch
regions of the global indexes that overlap — because the users' documents
share I-space addresses through transclusion. We must determine what
consistency this shared state requires.

The investigation is motivated by a tension between two design
principles. On one hand, the system is built for independent operation:
each document has a single owner, the addressing scheme gives each owner
a disjoint subtree of the address space, and the protocol is stateless
at the command level. On the other hand, transclusion creates genuine
shared state: when document A transcludes content from document B, both
documents' arrangement mappings point to the same I-space addresses, and
the global link index may contain entries that reference those shared
addresses from either document. Independence and sharing are both
foundational. We seek the formal properties that reconcile them.


## State model

We need enough state to reason about concurrency. Let Σ denote the
system state. We assume a set of *sessions* S, each associated with
exactly one user, and a set of *documents* D, each owned by exactly one
account. We write owner(d) for the account that owns document d, derived
structurally from d's tumbler address.

**CΣ1 (content store).** Σ.ispace : IAddr ⇀ Content is the global,
permanent content store. Content is immutable once allocated:

    (A a : a ∈ dom(Σ.ispace) : Σ'.ispace(a) = Σ.ispace(a))

for all subsequent states Σ'. The domain only grows:

    dom(Σ.ispace) ⊆ dom(Σ'.ispace)

**CΣ2 (arrangement mappings).** For each document d, Σ.poom(d) : VPos ⇀
IAddr maps virtual positions in d to permanent content addresses. This
is the mutable layer — editing operations modify poom(d).

**CΣ3 (link index).** Σ.linkidx : IAddr → Set(LinkEntry) maps I-space
address ranges to the set of link entries whose endsets overlap those
ranges. This is the global index used by link discovery operations. A
LinkEntry records the link's identity and endpoint type (from, to,
three-set).

**CΣ4 (content-location index).** Σ.locidx : IAddr → Set(DocId) maps
I-space addresses to the set of documents whose arrangement mappings
currently reference those addresses. This is the global index used by
FINDDOCSCONTAINING.

Both CΣ3 and CΣ4 are derived state — they can be computed from the
arrangement mappings and the link store — but they are maintained
incrementally for efficiency. The question is what consistency the
system must guarantee between these derived indexes and the authoritative
arrangement mappings.


## The write domain

The central structural property of this system is that each document
owner writes to a region of the state that no other owner touches. We
make this precise.

**Definition (write domain).** The *write domain* of an operation on
document d, written wd(d), is the set of state components that the
operation may modify. For a mutating operation (INSERT, DELETE,
REARRANGE) on document d:

    wd(d) = { Σ.poom(d) } ∪ { fresh I-space entries under d's subtree }
             ∪ { Σ.linkidx entries created by d's operations }
             ∪ { Σ.locidx entries reflecting d's arrangement }

For CREATELINK in document d:

    wd(d) = { Σ.poom(d) } ∪ { fresh link I-space entries under d's subtree }
             ∪ { Σ.linkidx entries for the new link's endsets }

We now identify the components of this write domain that are truly
disjoint across owners, and those that are shared.

**CON0 (Arrangement isolation).** For distinct documents d₁ ≠ d₂:

    Σ.poom(d₁) and Σ.poom(d₂) are disjoint state components

An operation on d₁ modifies poom(d₁) and never touches poom(d₂). This
is not a convention but a structural consequence: the FEBE protocol
scopes every mutating command to a single document identified by its
tumbler address. Nelson specifies no operation that modifies two
documents' arrangements simultaneously.

Gregory's implementation confirms this at the code level: `deletend`,
`insertnd`, and the rearrangement functions each receive a single tree
root pointer — the target document's POOM — and all mutations traverse
exclusively within that tree. The frame axiom is enforced by
construction: no code path from one document's POOM reaches another
document's POOM.

**CON1 (Allocation disjointness).** For documents d₁, d₂ under
different accounts:

    alloc_range(d₁) ∩ alloc_range(d₂) = ∅

where alloc_range(d) is the set of I-space addresses that operations on
d may allocate. Each document allocates I-space addresses within a
subrange of the global address space determined by the document's own
tumbler prefix. The address-allocation function searches for the
highest existing address below an upper bound derived solely from the
target document's address, then increments. Since two documents under
different accounts have different tumbler prefixes, their upper bounds
fall in non-overlapping regions of the address space. The search ranges
are disjoint by the prefix-freeness of tumbler addresses.

Nelson states the principle directly: "the owner of a given item
controls the allocation of the numbers under it." Gregory's
implementation confirms the mechanism: `findisatoinsertmolecule`
computes an upper bound from the target document's ISA and searches only
below that bound. Two documents at addresses d₁ and d₂ produce upper
bounds in different, non-overlapping subtrees of the global content
store.

CON0 and CON1 together establish that the *authoritative* state modified
by operations on different documents is disjoint. The arrangement
mappings are separate by CΣ2. The newly allocated I-space addresses are
separate by CON1. The difficulty, as we shall see, lies entirely in the
*derived* state — the global indexes CΣ3 and CΣ4.


## I-space immutability and read conflicts

Transclusion creates the one apparent threat to isolation: document d₂
may reference I-space addresses that were originally allocated by
operations on d₁. When d₂ transcludes content from d₁, both documents'
arrangement mappings contain entries pointing to the same I-space
addresses. If an operation on d₁ could alter the content at those
addresses, d₂ would observe a change it did not initiate — a read-write
conflict across document boundaries.

The system eliminates this threat unconditionally through CΣ1 (I-space
immutability). Content at an I-space address never changes. An operation
on d₁ may alter d₁'s arrangement mapping — removing, reordering, or
extending the virtual positions that reference those I-space addresses —
but the bytes at the addresses themselves are permanent. Document d₂'s
transclusion of those addresses always resolves to the same content,
regardless of what d₁'s owner does.

**CON2 (Transclusion read stability).** For any operation op on
document d₁ taking the system from state Σ to Σ', and any document
d₂ ≠ d₁ with a transclusion referencing I-space addresses A:

    (A a : a ∈ A ∩ dom(Σ.ispace) : Σ'.ispace(a) = Σ.ispace(a))
    ∧  Σ'.poom(d₂) = Σ.poom(d₂)

The first conjunct follows from CΣ1 (I-space immutability). The second
follows from CON0 (arrangement isolation). Together they establish that
d₂'s view of its transcluded content is completely unaffected by any
operation on d₁. The transclusion relationship creates a read dependency
on immutable data — and reads of immutable data require no coordination.

Nelson frames this as the architectural solution to the update problem:
"No copying operations are required among the documents throughout the
system, and thus we solve the problems of update — especially the
problem of updating documents which depend on other documents." The
absence of copies is the key: there is nothing to fall out of sync
because there was never a second copy. The system does not maintain
consistency between copies; it achieves consistency by not having copies.

We can now state the main isolation theorem.

**Theorem (Writer independence).** For any two operations op₁ on
document d₁ and op₂ on document d₂ where d₁ ≠ d₂:

    op₁ does not write to any component that op₂ reads as authoritative state
    op₂ does not write to any component that op₁ reads as authoritative state

*Proof.* op₁ writes to Σ.poom(d₁) and allocates in alloc_range(d₁). op₂
writes to Σ.poom(d₂) and allocates in alloc_range(d₂). By CON0,
poom(d₁) ≠ poom(d₂). By CON1, alloc_range(d₁) ∩ alloc_range(d₂) = ∅.
The only authoritative state op₁ reads from outside wd(d₁) is I-space
content — and I-space content is immutable (CΣ1), so op₂ cannot modify
what op₁ reads. Symmetrically for op₂. ∎

This theorem establishes that at the authoritative-state level, no
coordination between writers of different documents is ever needed. The
writers operate on disjoint mutable state and read only immutable shared
state. The result is stronger than mere serializability — the operations
are truly independent, as if they executed in separate universes.


## The global index question

Writer independence holds at the authoritative-state level. But the
system also maintains global indexes (CΣ3, CΣ4) that aggregate
information from all documents. When op₁ creates a new link whose
endsets reference I-space addresses that also appear in d₂'s
arrangement, both op₁'s link creation and op₂'s subsequent link query
touch the same region of the link index. When op₁ inserts new content,
the content-location index must be updated to reflect that d₁ now
contains content at new I-space addresses — and a concurrent
FINDDOCSCONTAINING query from another session must decide whether to
include d₁ in its results.

We observe that these global indexes have a crucial property: they are
*append-only with respect to document operations*. Links are added to the
index when CREATELINK executes; no document operation removes a link from
the index. Content-location entries are added when INSERT or COPY
extends a document's arrangement; DELETE removes the document's POOM
entry but — critically — does not remove the link index entries that
reference the deleted content's I-space addresses.

Gregory's implementation confirms this forcefully: no function in the
spanfilade (link index) codebase performs deletion. The spanfilade is
structurally append-only — entries are inserted and never removed.
DELETE on a document calls `deletend` on the document's POOM tree and
nothing else; the global link index is untouched.

**CON3 (Link index append-only).** For any document operation op taking
the system from Σ to Σ':

    Σ.linkidx ⊆ Σ'.linkidx

where the subset relation means: every entry present in Σ.linkidx is
also present in Σ'.linkidx with the same content. The link index only
grows. No document operation — not even DELETE — removes entries from
the link index.

This property has a profound consequence: link discovery through
transclusion survives content deletion in the source document. If
document d₁ contains content at I-space addresses A, and links exist
whose endsets reference A, and d₁'s owner deletes content at virtual
positions covering A — then A remains in the link index (by CON3), and
d₂'s arrangement still maps virtual positions to A (by CON0), so a link
query on d₂ still discovers the links (by resolving d₂'s V-positions to
I-addresses and searching the unchanged link index).

**CON4 (Cross-document link survival).** For any DELETE on document d₁
removing virtual positions whose I-space addresses are A, and any
document d₂ ≠ d₁ that transcludes addresses in A:

    links_discoverable(Σ', d₂, A) = links_discoverable(Σ, d₂, A)

where links_discoverable(Σ, d, A) = { ℓ ∈ Σ.linkidx(A) } for
I-addresses A reachable through d's arrangement.

*Proof.* By CON0, Σ'.poom(d₂) = Σ.poom(d₂), so d₂'s V-to-I resolution
is unchanged. By CON3, Σ.linkidx ⊆ Σ'.linkidx, so every link entry
present before the DELETE is still present after. Since both the query
path (d₂'s POOM → I-addresses → link index) and the index itself are
unchanged by the operation on d₁, the set of discoverable links is
identical. ∎

The asymmetry is revealing: after the DELETE, links become
*undiscoverable from d₁* (because d₁'s POOM no longer maps virtual
positions to A) but *remain discoverable from d₂* (because d₂'s POOM is
untouched). The link entries exist in the global index regardless; what
changes is which documents provide a path to reach them.


## Before-or-after atomicity

We have established that writers of different documents do not conflict
at the authoritative-state level. But what about a reader who queries
global state while a writer is mid-operation? A session executing
FINDDOCSCONTAINING or FINDLINKSFROMTOTHREE accesses the global indexes
while another session's INSERT or CREATELINK may be modifying them. What
must the reader observe?

Nelson is precise about the constraint without prescribing the
mechanism. Each FEBE command is defined as acting on a consistent, complete
state. FINDDOCSCONTAINING "returns a list of all documents containing any
of the material specified." FINDLINKSFROMTOTHREE returns "all links"
satisfying the search criteria. The word "all" presumes a definite state
against which the query is evaluated.

Nelson also requires that each server maintain "a continuously valid
model or subrepresentation of the entire docuverse" and remain in
"canonical operating condition" at all times. "Continuously valid" and
"canonical operating condition" are the language of *before-or-after
atomicity*: every observation of the system must be consistent with some
complete, settled state.

**CON5 (Before-or-after atomicity).** For any query Q executing
concurrently with a mutation M, the result of Q must be consistent with
a state that is either:

    (a) the state before M's effects are visible, or
    (b) the state after M's effects are fully applied

No query may observe a state in which M's effects are partially applied.

Formally, let Σ₀ be the state before M, and Σ₁ = M(Σ₀) the state
after. Then:

    result(Q, observed_state) ∈ { result(Q, Σ₀), result(Q, Σ₁) }

CON5 does *not* require that the reader see the latest state. A reader
may observe a state that is one, two, or many operations behind the
latest — as long as the observed state is a consistent snapshot. This is
a deliberate design choice: Nelson's distributed architecture envisions
servers with incomplete knowledge that improves incrementally. "From the
null case on up, at all times unified and operational."

CON5 also does *not* require global serialization. It does not demand
that all queries across all sessions agree on the order in which
mutations occurred. It requires only that each individual query sees a
consistent state. Two queries from different sessions may observe
different consistent states — one seeing M's effects and the other not
— without violating CON5, as long as each individually sees a
before-or-after snapshot.

Gregory's implementation provides a stronger property than CON5
requires: total serialization through a single-threaded event loop. The
backend processes one complete FEBE operation at a time; no two
operations ever execute concurrently. This trivially satisfies CON5 —
every query sees the state after the last completed operation and before
the next — but it is far stronger than necessary. An implementation with
genuine concurrency (multi-threaded, multi-process, distributed) could
satisfy CON5 through snapshot isolation, read-write locks, or any other
mechanism that prevents observation of partial states.


## The link index and access control

A subtle question arises at the intersection of concurrency and access
control. When session A holds exclusive write access to document D (a
write-lock in the cooperative access protocol), and session B performs a
link query whose search addresses overlap with D's content, must
session B's link query be blocked by A's write-lock?

The answer is no, and the reason is architectural. The access-control
protocol governs access to a document's *arrangement mapping* (the
POOM), not to the global indexes. Link queries operate through the
global link index, which maps I-space addresses to link entries. The
query path is:

    1. Convert session B's search specification to I-addresses
       (using B's own document's POOM, not D's)
    2. Search the global link index for entries at those I-addresses
    3. Return matching link entries

At no point does this path access D's POOM or require D to be opened.
Session A's write-lock on D is irrelevant — it protects D's arrangement
mapping, which the link query never touches.

**CON6 (Link index access independence).** Link discovery operations do
not require access authorization for any document other than the
querying session's own document (used only for V-to-I address
conversion). Specifically:

    link_query(session, search_spec)

requires only that session's own document(s) be accessible for V-to-I
conversion. The global link index is queried unconditionally, regardless
of what access-control state any other session holds on any other
document.

This separation is a consequence of the dual-index architecture. The
content store (per-document POOMs in the granfilade) is
access-controlled. The link index (global spanfilade) is not. Links are
indexed by I-space addresses — permanent content identity — not by
document identity or virtual position. Since I-space addresses are
immutable, there is no data-consistency reason to gate link queries on
document access state. A write-lock on document D prevents modification
of D's arrangement while another session uses it; it does not and need
not prevent discovery of links whose endsets reference content that
happens to reside in D.

Gregory's implementation confirms this with the constant
`NOBERTREQUIRED`: link query functions pass this constant when resolving
V-to-I addresses, causing the access-control check to return immediately
without consulting the access table. The access-control mechanism exists
but is explicitly bypassed for the link index path.


## Per-document ordering suffices

We are now in a position to state the ordering requirement. Must the
system enforce a total ordering of all operations across all documents?

No. Per-document ordering is sufficient. The argument follows from
writer independence and the structure of cross-document interactions.

**CON7 (Per-document ordering sufficiency).** The system requires a
total ordering of operations within each document. It does not require
any ordering relationship between operations on different documents.

We justify CON7 by enumerating all forms of cross-document interaction
and showing that none requires ordering:

*Transclusion (COPY).* When document d₂ transcludes from d₁, the COPY
operation reads I-space addresses from d₁ (immutable by CΣ1) and writes
to d₂'s POOM (isolated by CON0). No lock on d₁ is needed because the
data read is permanent.

*Link creation (CREATELINK).* A link's endsets reference I-space
addresses. The link is stored in its home document's address space (by
CON1) and indexed in the global link index (by CON3, append-only).
Creating a link in d₁ whose endsets reference content in d₂ does not
modify d₂ in any way.

*Link query.* By CON6, link queries bypass per-document access control.
By CON5, the query observes a consistent snapshot. The query reads the
global link index (append-only) and the querying session's own POOM
(which is not being modified by other sessions, by CON0).

*Content-location query (FINDDOCSCONTAINING).* Searches the
content-location index by I-space address. Like link queries, this reads
global derived state and requires no access to any specific document.

*Version creation (CREATENEWVERSION).* Reads the source document's
arrangement mapping and creates a new document with the same content
references. The new version shares I-space addresses with the original
but has its own POOM. The read of the source POOM and the write of the
new POOM are both operations on the version-creating session's behalf;
they require per-document ordering within the source document's
operation stream but no ordering relative to operations on unrelated
documents.

In every case, the cross-document interaction reads only immutable state
(I-space content) or append-only derived state (link index,
content-location index). No cross-document interaction involves a
read-write conflict on mutable authoritative state. The per-document
ordering ensures that operations within a single document are well-
ordered; the structural properties (CΣ1, CON0, CON1) ensure that
operations on different documents cannot interfere.

Nelson confirms this architectural intent: "An ever-growing network,
instantaneously supplying text and graphics to millions of simultaneous
users, would be impossible if it slowed down too fast as it grew." A
system requiring global ordering of all operations across all documents
cannot serve millions of simultaneous users — the ordering bottleneck
would produce the linear slowdown Nelson explicitly prohibits. Per-
document ordering scales with the number of documents; global ordering
does not.

**Corollary (No cross-document blocking).** No operation on document d₁
can block or delay an operation on document d₂, where d₁ ≠ d₂. The
owner of a document is never impeded by activity on another document.

*Proof.* By CON7, operations on d₁ and d₂ have no ordering requirement.
By CON0, they modify disjoint authoritative state. By CΣ1, shared
content is immutable. By CON3, the global link index is append-only and
requires no coordination for reads. No mechanism exists by which op₁
could cause op₂ to wait. ∎

The sole exception is infrastructure availability: if d₁ and d₂ reside
on different servers and the network connection between them fails, a
transclusion from d₁ into d₂ cannot be resolved. This is a failure of
the network, not a consequence of d₁'s operations. Nelson addresses this
through the BEBE forwarding protocol and the subrepresentation model:
each server maintains "a continuously valid model" that works "from the
null case on up."


## Operation atomicity and the global indexes

We have stated CON5 (before-or-after atomicity) as a requirement on
observation. We must also specify what constitutes an atomic unit of
state change.

**CON8 (Operation atomicity).** Each FEBE operation constitutes a single
atomic state transition. The system transitions directly from the
pre-operation state Σ to the post-operation state Σ' = op(Σ). No
intermediate state between Σ and Σ' is observable by any session.

CON8 is stronger than CON5. CON5 says queries see consistent snapshots;
CON8 says mutations produce consistent snapshots in one step. Together
they ensure that the system is always in a state where all invariants
hold — the arrangement mappings, the global indexes, and the derived
relationships between them are all mutually consistent at every
observable instant.

For operations that modify both authoritative state and derived indexes,
CON8 requires that *all* effects become visible simultaneously. An
INSERT that appends to I-space, updates a POOM, and creates a
content-location index entry must make all three changes atomically. A
CREATELINK that allocates a link address, stores the link structure, and
indexes the endsets in the link index must make all these changes
atomically.

Nelson expresses this as "canonical operating condition" — the system
never presents a state where content is visible but its index entry is
not, or where a link exists but its endsets are not yet indexed. He
does not specify the mechanism; he specifies the contract.

The contract implies a specific consistency requirement on the global
indexes:

**CON9 (Index-arrangement consistency).** At every observable state Σ:

    (a) Σ.locidx(a) ⊇ { d : (E v : v ∈ dom(Σ.poom(d)) : Σ.poom(d)(v) = a) }
    (b) Σ.linkidx(a) ⊇ { ℓ : ℓ is a link with an endset spanning a }

The indexes are *at least* as complete as the authoritative state
implies. They may contain entries for documents that have since deleted
the content from their arrangement (by CON3, the link index does not
remove entries on DELETE), but they must never be missing an entry that
the current arrangement implies should be present.

The ⊇ rather than = in CON9 is deliberate. The link index is
append-only (CON3), so after DELETE it may contain entries for I-space
addresses that no document's current POOM references. The
content-location index may similarly contain stale entries. These
over-approximations are safe — a query that returns a superset of the
true answer is conservative, not incorrect. The requirement is that the
indexes never under-approximate: every link and every content-location
relationship that currently exists in the authoritative state must be
discoverable through the indexes.

Nelson's eventual-consistency model for the distributed case relaxes
even this: each server's indexes reflect what that server knows, which
may lag behind the global truth. But the local model must be
"continuously valid" — internally consistent even if incomplete. CON9 is
the local consistency requirement; global completeness is an aspiration
achieved through BEBE forwarding and replication.


## DELETE locality

We have observed that DELETE is V-space-local. This deserves its own
property because it interacts critically with concurrency.

**CON10 (DELETE locality).** For DELETE on document d₁ removing virtual
positions whose I-space addresses are A:

    (a) Σ'.poom(d₁) = Σ.poom(d₁) with virtual positions for A removed
    (b) (A d : d ≠ d₁ : Σ'.poom(d) = Σ.poom(d))
    (c) Σ'.ispace = Σ.ispace
    (d) Σ'.linkidx = Σ.linkidx

Part (a) is the effect. Part (b) follows from CON0 (arrangement
isolation). Part (c) follows from CΣ1 (I-space immutability) — deletion
removes content from a document's virtual view, not from existence. Part
(d) follows from CON3 (link index append-only) — the link index does not
track which documents currently reference an I-space address, only which
links have endsets at that address.

The combination of (b), (c), and (d) means that DELETE on d₁ is
completely invisible to any operation on d₂. Not merely serializable,
not merely isolated — *invisible*. Document d₂'s arrangement, the
content it references, and the links discoverable through it are all
identical before and after d₁'s DELETE. The operation might as well not
have happened, from d₂'s perspective.

This is the strongest possible form of cross-document isolation for
DELETE, and it follows directly from the architecture: DELETE modifies
one component of state (a single document's POOM), and that component is
structurally isolated from all other documents.


## Link creation and the shared index

CREATELINK presents a subtler case than DELETE. When session A creates a
link in document d₁ whose endsets reference I-space addresses that also
appear in d₂'s arrangement, the link index is extended with new entries
at those shared addresses. A subsequent link query from session B on d₂
will discover the new link — even though d₂ was never modified.

Is this a concurrency hazard? No. The link index is append-only (CON3),
so the new entries cannot interfere with any existing entries. The link
query observes either the pre-CREATELINK state (link not yet visible) or
the post-CREATELINK state (link discoverable) — never a torn state where
some endset entries exist but others don't. CON5 (before-or-after
atomicity) ensures that the link either fully appears in the index or
does not appear at all.

**CON11 (Link creation atomicity).** CREATELINK on document d with
endsets E_from, E_to, E_three creates link index entries for all three
endsets atomically. For any concurrent query Q:

    either (A e ∈ {E_from, E_to, E_three} : entries for e absent from Q's view)
    or     (A e ∈ {E_from, E_to, E_three} : entries for e present in Q's view)

A query never observes a link with some endsets indexed and others not.

CON11 is a consequence of CON8 (operation atomicity) applied
specifically to CREATELINK. It prevents a scenario where a link query
discovers a link from A to B but not the corresponding three-set entry,
which would produce inconsistent link-search results depending on which
endset the query specifies.

Nelson's principle that links attach to content identity, not document
position, means that link creation in one document genuinely affects the
discoverability of content in all documents that share those I-space
addresses. This is not a concurrency anomaly — it is the intended
semantic of bidirectional linking in a shared content space. "Each user
is free to link to anything privately or publicly." The link index is the
mechanism by which this freedom is realised: it is a global, shared
structure precisely because linking is a global, shared capability.


## The crash boundary

The properties above (CON0–CON11) describe the system's guarantees
during normal operation. We must acknowledge where these guarantees
break down.

**CON12 (Crash atomicity gap).** The operation atomicity guarantee
(CON8) holds only for operations that complete without process-level
interruption. If the process is terminated (by signal, power failure, or
hardware fault) during an operation's execution, the resulting persistent
state may violate CON8 — some of the operation's effects may be
persistent while others are not.

The specific vulnerability is the gap between writing to the content
store and updating the arrangement mapping. An INSERT that has appended
new content to I-space but has not yet updated the document's POOM
leaves orphaned I-space entries: addresses allocated and populated with
content but unreferenced by any document's arrangement. By CΣ1 (I-space
immutability) and the monotonic growth of the address space, these
orphaned entries are permanent — no subsequent operation will reclaim
them or reuse their addresses.

The consequence for allocation is that subsequent operations observe the
orphaned entries and allocate above them, creating a permanent gap in
the address sequence. This violates no correctness property — the gap
is indistinguishable from a legitimate allocation followed by deletion
from all virtual views — but it does represent a deviation from CON8's
ideal of atomic state transitions.

Gregory's implementation lacks the mechanisms (write-ahead logging,
journaling, fsync) that would close this gap. The content store and
arrangement mapping are modified in sequence within a single function
call, with no durability barrier between them. A crash at any point in
this sequence produces a persistent state that may not correspond to any
complete operation's output.

CON12 is not a property to be *satisfied* but a *boundary* to be
acknowledged. The abstract specification requires CON8 for normal
operation and CON5 for all observations; CON12 states that these
guarantees have no force during catastrophic failure. An implementation
that closes the crash-atomicity gap (through journaling, write-ahead
logging, or other persistence mechanisms) would strengthen the system;
the abstract specification does not require it but does not forbid it.


## The flush boundary

A related concern arises from the global nature of the persistent-state
flush. When modified state is written to persistent storage, the flush
encompasses all modified state across all sessions — there is no
per-session or per-document scoping of the flush.

**CON13 (Flush globality).** The persistence flush writes all modified
state components, regardless of which session or operation produced the
modification. There is no mechanism to flush one document's modifications
independently of another's.

This has a subtle consequence for the crash boundary. If session A has
performed operations op₁ and op₂, and session B has performed op₃, and
a flush occurs followed by a crash, the persistent state reflects the
effects of op₁, op₂, and op₃ together — not just the session that
triggered the flush. The flush is not a per-session commit; it is a
global snapshot of all in-memory state.

CON13 is an implementation characteristic that the abstract
specification need not require. An alternative implementation could
provide per-document or per-session persistence. The abstract
specification requires only CON8 (operation atomicity during normal
execution) and is silent on the granularity of persistence.


## Derivability

We have introduced thirteen properties. Not all are independent. Let us
identify the derivability relationships.

CON2 (transclusion read stability) follows from CΣ1 (I-space
immutability) and CON0 (arrangement isolation). It is a theorem, not an
axiom.

CON4 (cross-document link survival) follows from CON0, CON3, and the
structure of link queries. It is a theorem.

The writer-independence theorem follows from CΣ1, CON0, and CON1. It is
a theorem.

The no-cross-document-blocking corollary follows from CON7, CON0, CΣ1,
and CON3. It is a theorem.

CON11 (link creation atomicity) is an instance of CON8 (operation
atomicity). It is a theorem.

The independent properties — those not derivable from others in this
note — are:

- CΣ1 (I-space immutability) — axiomatic
- CON0 (arrangement isolation) — follows from protocol structure
- CON1 (allocation disjointness) — follows from addressing architecture
- CON3 (link index append-only) — follows from operation definitions
- CON5 (before-or-after atomicity) — axiomatic
- CON7 (per-document ordering sufficiency) — derived from the above, but
  stated as a design principle
- CON8 (operation atomicity) — axiomatic, implies CON5 for single-server
- CON10 (DELETE locality) — follows from operation definition and CON0/CΣ1/CON3

Of these, the truly axiomatic properties — those that cannot be derived
from anything more primitive in this note — are CΣ1, CON5, and CON8.
CON0 and CON1 are structural consequences of the addressing architecture.
CON3 is a consequence of the operation definitions. The remaining
properties are theorems.


## What is not required

We must be explicit about what this specification does *not* demand.

**Not required: global serialization.** CON5 requires before-or-after
atomicity, not total ordering of all operations. Two operations on
different documents need not be serializable; they need only produce
individually consistent states. Gregory's single-threaded implementation
provides global serialization, but this is a stronger property than the
specification demands.

**Not required: real-time consistency of global indexes.** CON9 requires
that indexes not under-approximate the authoritative state, but it
permits lag. Nelson's subrepresentation model explicitly contemplates
servers with incomplete knowledge. An implementation in which the link
index lags behind CREATELINK by a bounded interval, provided no query
observes a torn state, satisfies CON5 and CON9.

**Not required: coordination between writers.** The writer-independence
theorem establishes this: no protocol for coordinating writers of
different documents is necessary or desirable. The system achieves
isolation through structural separation (CON0, CON1) and content
immutability (CΣ1), not through locking, message-passing, or consensus.

**Not required: crash recovery.** CON12 acknowledges the crash boundary
but does not require the system to recover from it. An implementation
with write-ahead logging could provide crash atomicity; the
specification does not demand it.

**Not required: session-scoped persistence.** CON13 describes flush
globality as an observation, not a requirement. Per-session or
per-document persistence boundaries are implementation choices.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CΣ1 | ispace content is immutable once allocated; dom(ispace) only grows | introduced |
| CΣ2 | each document d has its own arrangement mapping poom(d) : VPos ⇀ IAddr | introduced |
| CΣ3 | linkidx : IAddr → Set(LinkEntry) is the global link index | introduced |
| CΣ4 | locidx : IAddr → Set(DocId) is the global content-location index | introduced |
| CON0 | poom(d₁) and poom(d₂) are disjoint state components for d₁ ≠ d₂ | introduced |
| CON1 | alloc_range(d₁) ∩ alloc_range(d₂) = ∅ for documents under different accounts | introduced |
| CON2 | transclusion read stability: operations on d₁ leave d₂'s transcluded content and arrangement unchanged (theorem from CΣ1 + CON0) | introduced |
| CON3 | link index is append-only: Σ.linkidx ⊆ Σ'.linkidx for any document operation | introduced |
| CON4 | cross-document link survival: DELETE on d₁ does not affect link discoverability from d₂ (theorem from CON0 + CON3) | introduced |
| CON5 | before-or-after atomicity: every query observes a state consistent with some complete pre- or post-operation state | introduced |
| CON6 | link index access independence: link queries require no access authorization for documents other than the querying session's own | introduced |
| CON7 | per-document ordering sufficiency: total ordering within each document suffices; no cross-document ordering required | introduced |
| CON8 | operation atomicity: each FEBE operation is a single atomic state transition; no intermediate state is observable | introduced |
| CON9 | index-arrangement consistency: global indexes never under-approximate the authoritative state (may over-approximate) | introduced |
| CON10 | DELETE locality: DELETE modifies only the target document's poom; ispace, linkidx, and all other pooms are unchanged | introduced |
| CON11 | link creation atomicity: CREATELINK indexes all three endsets atomically (instance of CON8) | introduced |
| CON12 | crash atomicity gap: CON8 holds only for operations that complete without process-level interruption | introduced |
| CON13 | flush globality: persistence flush writes all modified state globally, not per-session or per-document | introduced |


## Open Questions

Must the content-location index (CΣ4) eventually converge to equality with the authoritative state, or is permanent over-approximation (stale entries from deleted arrangements) acceptable?

What consistency must CREATENEWVERSION guarantee when the source document is being concurrently modified by its owner — must the version snapshot a consistent pre- or post-operation state of the source arrangement?

Does the append-only property of the link index (CON3) extend to the content-location index, or may content-location entries be removed when a document deletes content from its arrangement?

If the system is extended to support multiple servers with BEBE replication, what convergence guarantee must the global indexes satisfy — eventual consistency, bounded staleness, or causal consistency?

What must the system guarantee about the ordering of link-index updates relative to the mutations that produce them — must CREATELINK's index entries be visible before the operation's acknowledgment reaches the client?

Under what conditions, if any, may orphaned I-space entries from crash-interrupted operations be reclaimed without violating CΣ1's permanence guarantee?

Must CON5 (before-or-after atomicity) hold across multi-operation sequences — for instance, must a session that performs INSERT followed by CREATELINK present both effects atomically to other sessions, or may the INSERT be visible before the CREATELINK?
