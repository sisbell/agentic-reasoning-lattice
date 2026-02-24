# ASN-0014: Distributed Replication Consistency

*2026-02-24*

We are looking for the consistency guarantees a multi-server Xanadu deployment must provide. The docuverse is, by design, a single unified address space distributed across many servers, each holding a subset. What must be true of each subset? What must be true of their union? Under what conditions can servers operate independently without risking contradiction?

The question sounds like it belongs to distributed systems theory — consensus protocols, vector clocks, conflict resolution. But Xanadu's structural commitments narrow the problem so dramatically that much of that apparatus turns out to be unnecessary. We shall see why.

---

## The permanent layer as grow-only set

We begin with the fundamental structural fact. The docuverse's permanent layer — the content stored at I-space addresses and the provenance records in the DOCISPAN index — admits only one operation: addition. Content, once stored at an I-address, is never modified or removed. A DOCISPAN record, once created, is never deleted. Let us state this precisely.

Let *S* be the set of all servers. For each server *s ∈ S*, let *ispace_s* denote the set of (address, content) pairs known to *s*, and let *spanf_s* denote the set of DOCISPAN records known to *s*. We require:

**REP0** (Permanent-layer monotonicity). For every server *s* and every pair of times *t₁ < t₂*:

    ispace_s(t₁) ⊆ ispace_s(t₂)    ∧    spanf_s(t₁) ⊆ spanf_s(t₂)

That is, each server's permanent layer only grows. Content is never retracted. Provenance records are never erased.

The global permanent layer is then simply the union across all servers:

    ispace = (∪ s : s ∈ S : ispace_s)
    spanf  = (∪ s : s ∈ S : spanf_s)

And the critical observation: *this union is always well-defined*. There are no conflicts to resolve. If two servers both know about address *a*, they must agree on its content — because content at an I-address is immutable once created. Let us state this as a property.

**REP1** (Content agreement). For all servers *s, s' ∈ S* and every address *a*:

    (a, v) ∈ ispace_s  ∧  (a, v') ∈ ispace_s'   ⟹   v = v'

This is not a protocol requirement — it is a structural consequence of two deeper properties working together: address uniqueness (no two independent creations can produce the same address) and content immutability (once stored, a value never changes). We shall derive each in turn.

---

## The partition principle

How can two servers, acting independently and possibly disconnected, allocate addresses without collision? The answer lies in the tumbler hierarchy.

Every tumbler address encodes a path through an ownership tree. The first field identifies the server node; the second, the user account; the third, the document; the fourth, the content element. Crucially, each level of the hierarchy is independently controlled: the owner of a given prefix controls allocation of all addresses beneath it.

Let us define this partitioning. For each server *s*, let *prefix(s)* denote the node-level tumbler prefix assigned to *s* at provisioning time (e.g., `1.1`, `1.2`, ...). We require:

**REP2** (Prefix disjointness). For all servers *s, s' ∈ S*:

    s ≠ s'   ⟹   prefix(s) ≠ prefix(s')

and every address allocated by *s* begins with *prefix(s)*.

The allocation of node-level prefixes is the *sole* coordination point in the entire system. It occurs once, at server provisioning, when a parent node assigns a fresh prefix to a new child. After that initial "baptism," the server operates independently forever.

Within its prefix, a server allocates addresses by monotonic sequential extension — appending the next integer at the appropriate level of the hierarchy. Account 3 under node `1.1` creates documents `1.1.0.3.0.1`, then `1.1.0.3.0.2`, then `1.1.0.3.0.3` — the counter advances and never retreats.

**REP3** (Monotonic allocation). For each server *s*, the sequence of addresses allocated by *s* is strictly increasing in the tumbler ordering.

From REP2 and REP3 together we can derive REP1. Suppose *(a, v) ∈ ispace_s* and *(a, v') ∈ ispace_s'*. If *s = s'*, then within a single server the same address cannot be assigned twice (by REP3 — the counter only advances). If *s ≠ s'*, then *a* begins with *prefix(s)* and also with *prefix(s')*, but by REP2 these prefixes are distinct — contradiction. So the case *s ≠ s'* with the same address cannot arise.

This is the key structural insight: **the tumbler hierarchy partitions the address space into disjoint regions, one per server, making content agreement a geometric property of the naming scheme rather than a protocol property of the communication layer.** Two servers cannot contradict each other because they cannot even *name* the same content independently.

---

## What replication reduces to

With the permanent layer established as a union of disjoint grow-only sets, we can now characterize what "replication" means in this context.

When server *s'* receives information from server *s*, every piece of that information falls into exactly one of two categories:

1. Content at an address *s'* has never seen — new knowledge, incorporated without conflict.
2. Content at an address *s'* already knows — necessarily identical by REP1, so a no-op.

There is no third case. There is no "content at an address *s'* knows differently" — REP2 makes this impossible. This means information transfer between servers is *idempotent* and *order-independent*.

**REP4** (Order-independent accumulation). For any set of messages *M₁, M₂, ...* received by server *s* from other servers, the final state *ispace_s* and *spanf_s* are independent of the order in which the messages arrive.

This follows directly from the set-union characterization. Unioning sets is commutative and associative; the order of unions does not affect the result. We have, by construction, a conflict-free replicated data type — specifically, a product of two grow-only sets (G-Sets): one for I-space content, one for DOCISPAN provenance records.

Nelson describes this with striking precision: content "sloshes back and forth dynamically" between servers, each of which maintains "a continuously valid model or subrepresentation of the entire docuverse." The word "assimilated at once" is telling — there is no merge conflict to resolve, no reconciliation protocol to execute. New information simply fills gaps.

---

## Local validity

If each server holds only a subset of the global state, we need a property that characterizes when a subset is "valid." Nelson requires that each server be in "canonical operating condition" at all times — even when its knowledge is severely incomplete.

**REP5** (Local validity). For every server *s* at every time *t*, the subset *(ispace_s(t), spanf_s(t))* satisfies:

(a) *Internal consistency*: for every record in *spanf_s(t)* that references an I-address *a*, if *(a, v) ∈ ispace_s(t)* then *v* is the globally correct value at *a*.

(b) *Structural coherence*: the DOCISPAN records in *spanf_s(t)* correctly describe the provenance relationships among the content in *ispace_s(t)* — no false provenance claims.

(c) *Subset validity*: every true assertion about *(ispace_s(t), spanf_s(t))* is also true of *(ispace, spanf)* — the server's local state is a valid restriction of the global state, never an incorrect extrapolation.

Notice what REP5 does *not* require: completeness. A server may be unaware of vast amounts of content. It may have no knowledge of entire document trees, entire account subtrees, entire server nodes. This is not an error state — it is normal operation. The server's knowledge is *correct but partial*.

This is the subrepresentation model. Each server begins from "the null case" and grows. At every point, its state is a valid subset of the global state. The transition from a smaller subset to a larger one (by receiving new content) preserves validity because new content is only *added* — it cannot contradict what is already known.

---

## The mutable layer: documents and POOMs

So far we have considered only the permanent layer — I-space and DOCISPAN. But documents also have a mutable arrangement layer: the POOM (Permutation Of the Original Material), which maps virtual positions to I-space content. Editing operations — INSERT, DELETE, REARRANGE — modify the POOM. And POOM modifications are *not* commutative: inserting text at position 5 and then deleting at position 3 produces a different arrangement than deleting at 3 and then inserting at 5. The shifts compose non-commutatively.

This is where the distributed problem becomes genuinely interesting. The permanent layer is a solved problem — it is a CRDT by construction. The mutable layer is where conflicts could arise.

Nelson's design resolves this through a principle we might call *authority locality*: each document has a home server determined by its tumbler address, and only the owner (or an authorized user on the home server) can modify its POOM. Let us state this.

**REP6** (Document authority). For each document *d*, there exists exactly one server *home(d)* that is authoritative for *d*'s mutable state. Modifications to *d*'s POOM occur only at *home(d)*.

    home(d) = the server whose prefix matches d's node-level tumbler prefix

Other servers may hold cached copies of *d*'s POOM, but these are read-only snapshots — stale but never contradictory. The home server is the single source of truth for arrangement.

This eliminates the distributed mutable-state problem entirely. There are no concurrent POOM modifications to reconcile because there is only one writer. Within the home server, POOM modifications are serialized (a single-threaded event loop suffices; any serialization mechanism would do). Between servers, POOM state flows one way: from the authoritative home server to read-only caches elsewhere.

Gregory's implementation evidence confirms this architecture emphatically. The BERT (access control) mechanism prevents two connections from holding simultaneous write access to the same document. When a second user attempts to modify a document already open for writing, the system creates a new version — a separate document with its own POOM, under the second user's own address space. The two users diverge into parallel branches rather than competing for the same mutable state.

**REP7** (Divergence by branching). When two users wish to modify the same document concurrently, the system creates independent versions — each under the respective user's address prefix, each with its own POOM — rather than allowing concurrent modification of a single POOM.

This is a profound design choice. It transforms the concurrency problem from "how do we merge conflicting edits?" to "how do we compare parallel versions?" — and Nelson provides exactly the tools for the latter (SHOWRELATIONOF2VERSIONS) without attempting the former. There is no MERGE operation in the protocol. Divergence is the design, not a failure mode.

---

## Links and cross-server reference

Links introduce a cross-cutting concern. A link is a permanent object stored in its home document, but its endsets may reference content on any server in the network. Must the server storing the link coordinate with the servers holding the linked content?

No. Three properties eliminate this need:

1. **Links live at home**: A link is stored in its owner's document, not at the target locations. The creating server has full authority to store the link.

2. **Endsets are pure address references**: A link's endsets are spans on the tumbler line — mathematical designations of address ranges. Constructing and storing an endset requires no round-trip to the target server.

3. **Targets need not exist**: The system explicitly supports "ghost elements" — links to addresses where no content is stored. If a link can validly point to nonexistent content, it can certainly point to content on a currently unreachable server.

**REP8** (Coordination-free link creation). A server may create and store a link whose endsets reference addresses on any other server, without communicating with that server. The link is valid from the moment of creation.

Link *discovery* — finding all links that point to a given piece of content — is a different matter. This requires cross-server search, which the BEBE protocol provides through request forwarding. But the discovery guarantee is *eventual*, not *synchronous*.

**REP9** (Eventual link discovery). For every link *l* and every server *s*, if *s* is asked to discover links pointing to content that *l* references, and *s* can eventually reach *l*'s home server, then *s* will eventually report *l* among its results.

The word "eventually" is load-bearing. If *l*'s home server is disconnected, *s* cannot discover *l* — but the link still exists, still points to the same content, and will become discoverable when connectivity is restored. Nelson designs explicitly for this: "computer networks are always broken."

---

## The subrepresentation model

We can now characterize the full replication model. Each server maintains a *subrepresentation* — a partial but valid model of the entire docuverse.

Let us define the state of server *s* as Σ_s = (ispace_s, spanf_s, pooms_s, map_s) where:

- *ispace_s* ⊆ *ispace* — the permanent content known to *s*
- *spanf_s* ⊆ *spanf* — the DOCISPAN records known to *s*
- *pooms_s* — the set of POOMs for documents homed at *s* (authoritative) plus cached POOMs for documents homed elsewhere (read-only snapshots)
- *map_s* — routing information: for each tumbler prefix, which server to contact

The subrepresentation grows through four mechanisms, as Nelson enumerates: (1) demand-driven content migration — a user's request for remote content causes it to be fetched and cached; (2) index replication — link and DOCISPAN indexes migrate to enable local search; (3) load rebalancing — popular content replicates closer to demand; (4) redundancy — backup copies for resilience.

All four mechanisms are *additive*. No mechanism removes content from a server's knowledge (though cache eviction may reclaim storage, the system can always re-fetch from the authoritative source). This yields the monotonic knowledge property:

**REP10** (Monotonic knowledge). For every server *s* and times *t₁ < t₂*:

    Σ_s(t₁) ⊆ Σ_s(t₂)

where the subset relation is defined component-wise. The server's knowledge of the docuverse only grows.

Combined with REP5 (local validity), this means each server traces a monotonically improving path through the lattice of valid subsets of the global state. It begins with the empty set (still valid — Nelson's "null case") and grows toward the full state, driven by demand. It need never reach the full state; what matters is that what it knows is correct.

---

## What BEBE reduces to

We are now in a position to say what the inter-server protocol must provide, and — more importantly — what it need *not* provide.

BEBE need NOT provide:
- **Distributed consensus** — the permanent layer is conflict-free by construction.
- **Change propagation for existing content** — I-space content never changes.
- **Cache invalidation** — cached content is immutable, so caches never become stale.
- **Conflict resolution** — conflicts cannot arise in the permanent layer, and the mutable layer has single-writer authority.
- **Global ordering** — the final accumulated state is order-independent (REP4).

BEBE MUST provide:
- **Request forwarding** — routing a content request to the server that holds the answer.
- **Content transfer** — moving immutable content between servers on demand.
- **Availability** — published content must remain reachable despite server and network failures.

**REP11** (Replication sufficiency). The inter-server protocol satisfies the convergence requirements of the docuverse if and only if it provides: (a) correct routing of requests to authoritative servers, (b) faithful transfer of immutable content, and (c) eventual reachability of all published content.

The simplicity of this requirement is remarkable. Nelson designed — whether by insight or by instinct — a system in which document-local editing combined with immutable shared content eliminates the hardest problems in distributed systems. The inter-server protocol is not a distributed consistency protocol; it is a distributed caching and forwarding protocol, which is among the easiest kinds to implement correctly.

---

## Availability and the economic tension

There is one domain where the convergence argument grows delicate. Nelson requires that published content remain accessible:

> "It is in the common interest that a thing once published stay published. ... Consequently its author may not withdraw it except by lengthy due process."

This establishes a *social permanence obligation*: the network as a whole must guarantee that content, once published, remains reachable. The mechanisms include: BEBE forwarding across vendor boundaries (contractually required by the franchise license), redundancy and backup replication, and orderly transition of customer data when a vendor ceases operation.

**REP12** (Publication permanence). For every piece of published content at address *a*:

    (E t₀ : published(a, t₀) : (A t : t ≥ t₀ : reachable(a, t)  ∨  temporarily_unavailable(a, t)))

where *temporarily_unavailable* implies eventual restoration. The system must prevent permanent loss of published content, though transient outages are expected.

The gap in this guarantee is economic. Storage requires ongoing payment. If a content owner stops paying, the specification does not fully resolve what happens. Widely transcluded content generates royalties that offset storage costs — a self-sustaining cycle. Rarely-referenced content has no such protection. The permanence guarantee for published content is socially and contractually strong, but the economic sustainability requirement introduces a tension that the design acknowledges without fully resolving.

---

## The convergence theorem

We can now state the overall convergence guarantee. It is not a protocol property but a structural consequence of the architectural commitments.

**Theorem** (Convergence). *If REP0 through REP4 hold, then for any two servers s, s' ∈ S that can eventually communicate, their permanent layers converge:*

    lim(t→∞) ispace_s(t) = lim(t→∞) ispace_s'(t) = ispace
    lim(t→∞) spanf_s(t)  = lim(t→∞) spanf_s'(t)  = spanf

*provided all published content is eventually forwarded to requesting servers.*

The proof is straightforward. By REP0, each server's permanent layer only grows. By REP4, the order of growth is irrelevant. By REP1, the target state (the global union) is well-defined and unambiguous. The only question is whether each server eventually receives all content — and this is exactly what REP11(c) guarantees for published content.

For unpublished content (private documents that have not been made public), convergence is neither required nor expected. A server need not learn about private content on other servers. The convergence guarantee applies to the *published* portion of the docuverse — the shared, accessible, economically sustained layer that constitutes the literary commonwealth.

We observe that this convergence is strictly weaker than "eventual consistency" as the term is used in distributed systems literature. Eventual consistency typically guarantees that *all replicas* converge to the *same state*. Here, convergence is *demand-driven*: a server learns about remote content when someone requests it, not through a background synchronization protocol. A server that nobody ever asks about a particular document may never learn of its existence. Nelson's model is closer to *eventual discovery* than eventual consistency — content becomes known to a server when need drives it there.

---

## Same-document replication: the gap

We have shown that the permanent layer is conflict-free and the mutable layer has single-writer authority. But there is an architectural gap that any implementation must address.

Gregory's evidence reveals that the I-address allocation algorithm — find the current maximum address in the document's subspace, increment by one — is *purely a function of local state*. If two separate processes (or two hypothetical servers) both attempted to allocate I-addresses under the same document, they would compute the same "next available" address from their respective copies of the state and produce a collision.

REP2 (prefix disjointness) prevents this between different servers' documents. REP6 (document authority) prevents this for a single document by ensuring only one server writes to it. But the protection is architectural, not algorithmic — the allocation mechanism itself contains no distributed coordination. An implementation that violated REP6 (e.g., by allowing two servers to accept inserts into the same document) would immediately violate REP1 (content agreement).

This is not a flaw in the design; it is a *consequence* of the design. The tumbler hierarchy provides partition safety between servers. Within a server, serialization provides safety between operations. The combination is complete — but both layers are necessary. The partition alone is insufficient; the serialization alone is insufficient; together they are exact.

**REP13** (Allocation safety composition). The uniqueness of I-address allocation (REP1) depends on both REP2 (inter-server prefix disjointness) and REP6 (intra-server document authority). Neither is independently sufficient.

    REP1  ⟸  REP2 ∧ REP3 ∧ REP6

This decomposition makes explicit what an implementer must provide. A multi-server deployment needs: (a) unique node prefixes assigned at provisioning time, (b) monotonic allocation within each prefix, and (c) single-writer authority for each document's mutable state and address subspace. With all three, I-address uniqueness follows by construction and no distributed consensus protocol is required.

---

## Version divergence and comparison

One final structural consequence deserves attention. When two users on different servers each create a version of the same document, the tumbler system guarantees their versions live at disjoint addresses. The owner's versions are subdocuments under the document's own prefix; other users' derivative versions are independent documents under each user's account prefix. In either case, the addresses are disjoint and the POOMs are independent.

The system provides SHOWRELATIONOF2VERSIONS — a query that computes the I-space intersection of two versions, revealing which content they share. This is a *comparison* tool, not a *merge* tool. It shows where two versions correspond without attempting to reconcile them.

**REP14** (Comparison without convergence). The system provides tools to identify shared content between divergent versions but imposes no mechanism for merging them into a single version. Merge, if desired, is a front-end semantic concern requiring human judgment about the document's meaning.

This design choice has profound implications for replication. In systems that support merge (e.g., version control), replication must eventually converge divergent branches. In Xanadu, divergence is permanent. Two versions created independently remain independent forever, related only through the I-space content they share. This eliminates the hardest problem in replicated document systems — conflict resolution for concurrent edits — at the cost of requiring users to perform explicit comparison and selective incorporation when they wish to combine work.

Nelson envisions a literary landscape of interconnected alternatives, not a linear history converging to a canonical state. The system's tools match this vision: permanent addresses for every version, bidirectional links between versions, I-space identity tracking across transclusions, and exhaustive correspondence analysis. Everything needed to *understand* divergence is provided; nothing to *eliminate* it is offered.

---

## Summary

The Xanadu replication model rests on three pillars:

1. **The permanent layer is a CRDT.** I-space and DOCISPAN form a product of grow-only sets, partitioned by tumbler prefix. Servers add content to disjoint regions of a shared address space. Union is always well-defined, always conflict-free, always order-independent.

2. **The mutable layer has single-writer authority.** Each document's POOM is modifiable only by the home server. Other servers hold read-only snapshots. There are no concurrent modifications to reconcile.

3. **Knowledge is partial and demand-driven.** Each server holds a valid subset of the global state, growing toward completeness through use. The inter-server protocol forwards requests and transfers content — it does not synchronize state or resolve conflicts, because the architecture ensures there are none to resolve.

The result is a distributed system that requires no consensus protocol, no distributed locking, no conflict resolution, and no global ordering. The structural commitments — permanent addressing, immutable content, hierarchical ownership, append-only storage — are so strong that the "distributed" problem largely dissolves. What remains is routing, caching, and availability: important engineering problems, but not fundamental consistency problems.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| REP0 | Each server's permanent layer (ispace, spanf) grows monotonically: ispace_s(t₁) ⊆ ispace_s(t₂) for t₁ < t₂ | introduced |
| REP1 | Content agreement: if two servers both know address *a*, they agree on its content | introduced |
| REP2 | Prefix disjointness: distinct servers have distinct node-level tumbler prefixes; all addresses allocated by *s* begin with prefix(s) | introduced |
| REP3 | Monotonic allocation: within each server, allocated addresses are strictly increasing | introduced |
| REP4 | Order-independent accumulation: the final permanent-layer state is independent of message arrival order | introduced |
| REP5 | Local validity: each server's subset is internally consistent, structurally coherent, and a valid restriction of the global state | introduced |
| REP6 | Document authority: each document has exactly one authoritative server for its mutable state | introduced |
| REP7 | Divergence by branching: concurrent modification requests produce independent versions, not conflicting edits | introduced |
| REP8 | Coordination-free link creation: a link may be stored without communicating with the servers holding the linked content | introduced |
| REP9 | Eventual link discovery: links become discoverable when connectivity to their home server is available | introduced |
| REP10 | Monotonic knowledge: each server's total state (Σ_s) only grows over time | introduced |
| REP11 | Replication sufficiency: the inter-server protocol needs only routing, faithful transfer, and eventual reachability | introduced |
| REP12 | Publication permanence: published content must remain reachable, though transient unavailability is acceptable | introduced |
| REP13 | Allocation safety composition: REP1 depends on both REP2 (inter-server) and REP6 (intra-server); neither alone suffices | introduced |
| REP14 | Comparison without convergence: the system provides version comparison but no merge; divergence is permanent | introduced |
| Σ_s | Server state: (ispace_s, spanf_s, pooms_s, map_s) | introduced |
| home(d) | Function mapping each document to its authoritative server | introduced |
| prefix(s) | Function mapping each server to its node-level tumbler prefix | introduced |


## Open Questions

What availability guarantees must the system provide when a document's home server is permanently lost — must the network reconstruct authority from replicated snapshots?

What must the system guarantee about the freshness of cached POOM snapshots on non-authoritative servers — is there a maximum staleness bound, or is any valid past state acceptable?

What invariants must the prefix allocation mechanism at server provisioning time satisfy to ensure REP2 holds even under concurrent provisioning of sibling nodes?

Must the DOCISPAN index converge globally (every server eventually knows every provenance record) or is demand-driven partial knowledge sufficient for query correctness?

What must the system guarantee about link discovery completeness — must every relevant link eventually be found, or only those whose home servers are reachable at query time?

Under what conditions can the economic failure of a content owner violate REP12 — and what mechanism, if any, serves as a backstop when storage payments lapse?

If a server's cached snapshot of a remote document's POOM is stale, can query results (e.g., FINDDOCSCONTAINING) be silently incomplete, and what must the system disclose about result completeness?

What consistency guarantees must hold between the DOCISPAN index and the I-space content it references — can a server hold provenance records for content it has not yet obtained?
