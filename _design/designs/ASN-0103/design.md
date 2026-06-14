# Design Digest — ASN-0103: CREATENEWDOCUMENT

## What this is

This note defines the **document-creation operation**: how the substrate baptises a new, empty, permanently-addressable document under an account on behalf of a principal who owns that account. It is the canonical example of allocating a *place* without storing any *content* — the operation that turns "an account" into "an account with one more addressable, ownable, empty document."

## Design commitments

These are the locks. Downstream design cannot violate them.

- **A document is a place, not a value.** Documents live in the entity set; they are never content. Creation touches the entity set and *nothing else* — content, links, and provenance stores are not opened. This seam is forced by the foundation's two-store split, and it is what makes "create" a *stores-nothing* operation: its only cost is a bounded prefix-scan plus one index insert into the registry (logarithmic in registry size), and no content is written.
- **Identity is the address, assigned once, permanent for the life of the system.** The returned id *is* the document — immutable even as its arrangement, content, and storage location later evolve. There is no rename, no re-id, no value-based identity.
- **The address is allocated by baptism under the account.** `parent(d) = A` and `d` has the form `[A, 0, j]`. The new document is structurally beneath the account that owns it. This is not metadata; it is the address.
- **The allocator must be level-aware — the document chain is not "all children of A."** Versions are forked off documents one level deeper, yet satisfy the same `Document(·) ∧ parent(·) = A` predicate. Selecting the next address by predicate-and-parent alone will eventually re-mint an address a future version fork also claims, violating uniqueness. The allocator is *forced* to separate the document frontier from the version frontier (the note does it by length `#e = #A+2`; udanax-green does it by truncating any found descendant back to document depth — both are valid, the requirement is not).
- **Ownership is structural — no side table.** `owns(π, d)` is a pure prefix predicate over the address (`pfx(π) ≼ d`), derived from `pfx(π) ≼ A` and `A ≼ d`. The owned-number tree *is* the ownership record. There is no ACL, no ownership index that must be kept consistent.
- **Uniqueness is decentralised — no central coordination.** Because `d` is minted under a subtree `π` already owns, no other owner can produce the same address. Allocation consults no central registry and needs no cross-owner uniqueness authority — though the *local* baptismal record is still read to find the frontier.
- **Referability attaches to the address, not the content.** A link may target `d` the instant it exists, before a single byte is stored (the ghost-element principle). The empty document is fully a first-class reference target.
- **The document is born empty and cannot dangle.** Its arrangement is the empty function; no default text, no placeholder, zero V-addresses occupied. Referential integrity holds vacuously.
- **The operation is a single atomic transition.** No observable intermediate state; every invariant holds throughout. There is no partial document.
- **Strictly additive.** The entity population grows by exactly one; every existing entity, document arrangement, and stored value is untouched.

What is *merely conventional* (not forced): the specific allocation arithmetic (`inc(A,2)` vs `inc(max(D_A),0)`) — that's a consequence of the sibling-stream definition, not a free choice — and, *only if you keep a cached per-account counter*, when that counter is created (at account-creation time, or lazily at first document creation). The note's `CND.A-act` assumes an activated allocator already exists; the stateless default needs no such per-account object at all, so the timing is moot — observable behavior is identical either way.

## What must be built

- A **document-address allocation contract** `next_document_address(A)` — emitting an address that is fresh, monotone, permanent, unique, and *level-distinct from the version chain* — realizable with no per-account state at all (the stateless default holds none).
- An **entity registry** (the baptismal record) that records allocated organisational addresses, is append-only, and never reuses an address.
- An **arrangement map** able to hold an empty entry for the new document, leaving every other document's arrangement bit-identical.
- A **place/content firewall**: document allocation must be structurally incapable of advancing the content store's high-water mark or writing the link/provenance stores.
- An **ownership oracle** that answers `owns(π, x)` by prefix comparison over the address alone — no maintained ownership table.
- **Atomic commit + crash recovery** of the baptism, so the returned id is durable and can never be re-minted.
- **Logical activation of the document's content and link subspaces** — defined and addressable, but materialised only on first use.

## Implementation approaches

### Document-address allocation (the core)

The allocator's job is `next_document_address(A) = (max document under A) + 1`, with the version chain excluded. There are two axes of choice.

**Where the "next number" lives.**

- *Stateless recompute (the frontier as a hint).* Hold no counter. On each allocation, query the entity registry for the maximum document-level address under `A` and step past it. This is exactly udanax-green's verified mechanism — `findisatoinsertnonmolecule` does a bounded scan of the granfilade under the account and returns max+1, with *no cached "next" counter*; it is a pure function of current registry state. In Lampson's terms the frontier is a **hint**: never stored authoritatively, always recomputable from the registry. **Pick this by default.** It cannot drift, it needs no recovery logic of its own, and it is naturally correct after a crash because the registry (not a counter) is the authority.
- *Cached per-account frontier counter.* Keep "next document number under `A`" in memory as an accelerator, recomputed on a miss by falling back to the scan. Buys O(1) allocation under hot accounts. **Pick this only when one account sees a high allocation rate** and the scan is measured to hurt. Keep it strictly a cache: the registry remains the authority, and a lost/stale counter is repaired by rescan — never trusted across a crash on its own.

**How the version chain is excluded** (mandatory either way):

- *Level/length filter* (the note's `D_A`): select only addresses at document depth and ignore anything deeper. Clean when your address representation makes length/level cheap to test.
- *Truncate-then-increment* (udanax-green): take the maximum of *all* descendants of `A`, truncate it to document depth, then increment. Robust precisely because it tolerates a version being the current maximum — it normalises any deep address back to the document level before stepping. **Prefer truncate-then-increment** if there's any chance your scan can surface a non-document descendant; it removes a whole class of "I filtered the frontier wrong" bugs. Use the pure level filter if your registry index already keys on level so the deeper addresses never appear in the scan.

To make either scan cheap, index the registry by account prefix. An **ordered, prefix-keyed map** (the abstract shape of the granfilade) gives both the bounded range scan and the max query in one structure. With persistent (structurally-shared) data structures, each baptism produces a cheap new version of that map while prior versions persist — which is the natural fit for immutable-value state and for serving reads concurrently with the write.

### Entity registry and durability

Use an **append-only journal of baptism events, recovered by replay on load** — the discipline udanax-green follows when it makes *allocation immediate insertion* into the index. The in-memory registry and any frontier counter are then **hints rebuilt from the journal**; the journal is the authority.

This directly answers the note's first open question and closes a hazard the green evidence makes explicit: in udanax-green, address-find and index-insert are separate steps, and a crash *between* them could hand a client an id that was never recorded and later re-minted — monotonicity there is a property of normal execution, not a crash-safe invariant. The fix is Lampson-standard: make the baptism a single journal append that is the commit point, and only return the id once that append is durable. Replay on recovery then guarantees the returned id is present and never reissued. Make the registry write atomic so concurrent readers never observe a torn record — that is the concrete pattern for keeping the commit point safe.

### Place/content firewall

Keep document addresses and content addresses in **separate allocation namespaces with separate high-water marks**, even if they share an address representation. udanax-green enforces this with two distinct allocation routines over one granfilade — the structural path provably does *not* advance the content I-address counter ("content granfilade unchanged, document granfilade modified"), so a document baptism is invisible to the next text insert and content addresses stay contiguous. Make the seam *structural* (separate journals/namespaces), not merely conventional (one counter you promise not to touch) — the structural version cannot be violated by a careless future operation.

### Ownership oracle

Implement `owns(π, x)` as a **pure prefix test over the address** — the cheapest mechanism that honors the contract, and the one the foundation forces. Maintain no forward ownership table. If you need the reverse query ("everything `π` owns"), serve it as a **prefix-range scan over the registry** — again a recomputable hint, not stored duplicate state. What you give up by committing here: ownership cannot be reassigned without reassigning the (permanent) address, so reassignment is simply not in this model; and *effective* ownership / delegation is deferred (an explicit open question, and the subject of the entity-set↔baptismal-registry coupling the note flags last).

### Subspace activation (lazy materialisation)

Distinguish two births. The empty **arrangement** is built *eagerly* at baptism — `M(d) = ∅`, realised as the minimal empty structure (in green, an empty POOM of structural height 1 carrying a single zero-width placeholder crum, *not* zero crums). The content, link, and type **subspaces** (1.x / 2.x / 3.x), together with every span-index entry, stay *lazy*: do **not** pre-build them. Their activation is a *logical* fact — the subspaces are well-defined and addressable but hold nothing — realised by materialising them on first INSERT / MAKELINK. The green evidence confirms this minimal birth state: the single zero-width placeholder, no span-index entries, no link/type subspace entries until first use. This is the "common case cheap, rare case correct" discipline: creation stores no content, and the first content operation pays for what it uses.

## Guarantees to uphold

**Hold by construction:**

- *Permanence* — the registry is append-only and never reuses an address; existing addresses stay valid because the operation only adjoins `d`. Entity-permanence (P1) is the lock for *this* operation; whether a created-but-never-populated empty may ever be *reclaimed* is left open (Q4), and any such reclamation would still have to honor no-reuse.
- *Ownership* — structural prefix containment; nothing to maintain, nothing to corrupt.
- *Frame / non-interference* — if you only touch the entity allocator and add one empty arrangement entry, the content/link/provenance stores are literally not opened, so their preservation is automatic.
- *Empty-and-can't-dangle* — an empty arrangement has no reference that could point past the content store; referential integrity is vacuous.
- *Immediate referability* — falls out of identity-by-address.

**Require active enforcement:**

- *Uniqueness + monotonicity across failures* — this is the one that bites. It holds trivially in a single-threaded, never-crashing run, but you must make allocation atomic with durable recording (journal-append-as-commit) or a crash can re-mint a returned id. Enforce it; don't assume it.
- *Version/document separation* — the allocator's selection rule (level filter or truncate-then-increment) must be correct, or a future version fork collides with a future document. This is logic you have to get right, not a property you inherit.
- *The place/content seam* — keep it structural (separate namespaces) so it can't be eroded by later operations.

## How it fits

**Leans on:** the tumbler address algebra (increment, prefix order, length, validity) and the entity/allocator hierarchy that defines `A_doc(A)` and the per-document content/link sub-allocators; the ownership prefix order that makes `owns` a structural predicate; the sequential-transition atomicity axiom that licenses treating creation as one indivisible step; and account provisioning, which is out of scope but *owes this operation* an activated (or emergently-available) document allocator under every account.

**Hands to:** INSERT / COPY / MAKELINK, which populate the empty content and link subspaces this operation only activated; the link layer, which may target `d` immediately; CREATENEWVERSION, which forks versions off `d` and is precisely why the allocator must keep the document and version chains distinct; the attribution layer, which must keep content origins derivable from the address alone (existential coherence, P6) — how a document's creation-time address relates to its eventual content origins is left open (Q5); and session/open-state management (the BERT-like layer), which is a *separate concern* — the green evidence is explicit that bare creation does not register the document as open for the creating connection, and that "open" is a distinct protocol step.

CREATENEWDOCUMENT is the *degenerate* member of the substrate-composite (ValidComposite★) family: the coupling constraints J0, J1★, J1'★ that bind content allocation, placement, and provenance together hold *vacuously here*, because creation does no content, placement, or provenance work. Those same constraints become load-bearing for the INSERT / COPY / MAKELINK this operation hands to — which is exactly why creation is the easy case.

## Decisions for the builder

These are genuinely yours to pick (distinct from the note's spec-level open questions):

- **Frontier strategy.** Stateless recompute (default) vs a cached per-account counter backed by recompute-on-miss. Drive it by measured allocation rate under a single account; don't pay for the counter until you must.
- **Version-exclusion rule.** Length/level filter vs truncate-then-increment. Prefer truncate-then-increment unless your registry index already hides non-document descendants from the scan.
- **Registry index shape.** A prefix-ordered map (enfilade-shaped) that serves both the range scan and the max query, vs a hash plus a separate ordering. The ordered, structurally-shared map is the better fit for this corpus.
- **Commit point.** Exactly where the baptism becomes durable, and the rule that the id is not returned before that point. This is the whole answer to crash-recovery for a "single transition" that nonetheless has an internal find-then-record shape.
- **Allocator materialisation.** Moot under the stateless default — it holds no per-account allocator object, so there is nothing to materialise (CND.A-act is discharged with zero per-account state, and green confirms there is no per-account document allocator: a single flat registry tree with nothing to pre-initialise). The choice arises *only if you adopt the cached counter*: create it at account-creation time (matching the note's standing assumption) or let it emerge at first document creation (udanax-green's lazy way). Observable behavior is identical; the choice is only whether account creation stores anything.
- **Create-and-open coupling.** Whether creation also opens the document write-ready for the creating session (atomic create+open) or leaves "open" as a separate step. The green reference keeps them separate except for one combined copy-mode path — you must decide which contract your sessions expect.
- **Per-account serialization point.** Where concurrent CREATENEWDOCUMENT calls under one account serialise, and thus how the two new addresses are ordered. The green system sidesteps this with a single-threaded loop; a concurrent implementation must name the lock or the ordering authority explicitly.
