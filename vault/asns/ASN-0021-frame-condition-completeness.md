# ASN-0021: Frame Condition Completeness

*2026-02-25*

## The Problem

We are looking for the *other half* of every operation's specification — the part that says what does NOT change. An operation that inserts content at V-position p must, of course, place the new content there. But it must also guarantee that every link in every other document is untouched, that every address allocated before the operation remains allocated after, that every prior version of every document still resolves to identical content, and that no other document's V-space arrangement has shifted by so much as a single position. The postcondition tells us what the operation achieves; the frame condition tells us what it preserves. Without the frame, correctness is not compositional — we cannot reason about operation A's effect on property P if operation B might silently destroy P as a side effect.

The question is: what frame conditions must hold, and why are they necessary?

We approach this in Dijkstra's manner: not by listing frames for each operation and checking them, but by asking what must be true for the system's invariants to survive the application of any operation. The frame conditions will emerge as *requirements* — they are what we need in order to prove that the invariants are maintained.


## The State

We need a model of system state rich enough to express what can and cannot change. Let Σ be the global state, containing:

- **ispace** : Addr ⇀ Content — the permanent content store. A partial function from I-addresses to content values. Append-only: once a ∈ dom(ispace), it remains forever and ispace(a) never changes.

- **poom(d)** : Pos → Addr — for each document d, the V-to-I mapping. A partial function from V-positions to I-addresses, defining d's current arrangement.

- **links** : LinkId → Link — the set of all links. Each link ℓ has three endsets ℓ.from, ℓ.to, ℓ.type, each being a set of I-address spans; a home document ℓ.home; and a permanent address ℓ.addr.

- **owner(d)** : DocId → UserId — the ownership function. For each document, the user who has modification rights.

- **access(d)** : DocId → AccessPolicy — the access policy (private-with-designees or published).

- **versions(d)** : DocId → DAG(VersionId) — the version history of each document, where each version v has a frozen V-space arrangement frozen(v).

- **addrs** : the set of all allocated tumbler addresses (a superset of dom(ispace), also including document addresses, link addresses, and version addresses).

We write primed names for post-state: ispace' is the content store after the operation, poom'(d) is d's V-space after the operation, and so on.


## Why Frames Are Necessary

Consider the invariant that every link resolves to content:

  **L0.** (A ℓ : ℓ ∈ dom(links) : (A s : s ∈ ℓ.from ∪ ℓ.to ∪ ℓ.type : s ⊆ dom(ispace)))

Every span in every endset of every link references allocated I-space content. This is an invariant — it must hold before and after every operation.

Now suppose we wish to verify that INSERT preserves L0. INSERT allocates new I-addresses and modifies poom(d) for the target document d. If INSERT's specification says only what it *does* — "places content at position p and shifts subsequent positions" — we cannot conclude L0 is preserved. Why? Because the specification is silent about whether INSERT also modifies links, or removes I-addresses, or changes endsets. We need the explicit statement: INSERT does not modify dom(links), does not modify any ℓ.from or ℓ.to or ℓ.type, and does not remove any address from dom(ispace). Only then does the proof go through trivially: L0 held before, and nothing L0 depends on was changed.

This is the frame problem in program verification. Without explicit frame conditions, we must verify every invariant against every operation by examining the operation's full implementation. With explicit frames, we can verify by inspection: "operation O preserves P because O's frame says it does not modify any variable that P mentions."

Nelson states the design principle that makes frames architecturally central:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

"Without damaging the originals" IS a frame condition. It says: the set of things that may change is bounded, and everything outside that set is preserved. The entire Xanadu architecture is structured so that this guarantee can be given.


## The Universal Frames

We begin with frame conditions that hold for EVERY operation in the system. These are the bedrock — the properties so fundamental that no operation may violate them.

### F0: I-Space Content Immutability

For every operation O:

  **F0.** (A a : a ∈ dom(ispace) : ispace'(a) = ispace(a))

Content at an allocated address never changes. This is the deepest invariant — it is what makes the system a *permanent* store rather than a mutable one. Nelson:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Gregory confirms at the implementation level: the only function that sets the `modified = TRUE` flag on content nodes (triggering eventual disk write-back) is `ivemodified`, and it is called exclusively after INSERT — never during retrieval, deletion, or rearrangement of existing content. The read path through `findcbcinarea2d` is a pure traversal that accumulates contexts into a sorted list without writing to any structural field. The content store is physically write-once.

F0 is the strongest possible frame: no operation changes any pre-existing content at any address. Combined with address permanence (F1 below), it ensures that any reference to I-space content made at any point in the system's history remains valid and returns identical content forever.

### F1: Address Monotonicity

For every operation O:

  **F1.** dom(ispace) ⊆ dom(ispace') ∧ dom(addrs) ⊆ dom(addrs')

The set of allocated addresses grows monotonically. No operation removes an address from the space. Nelson designed the tumbler addressing system specifically for this property:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The tumbler forking mechanism — "one digit can become several by a forking or branching process" [LM 4/20] — guarantees that new allocations subdivide existing space without displacing existing addresses. F1 is a consequence: if the allocation scheme is purely additive, no address can be removed.

### F2: Ownership Structural Permanence

For every operation O that is not an explicit ownership transfer:

  **F2.** (A d : d ∈ dom(owner) : owner'(d) = owner(d))

Ownership is encoded in the tumbler address itself — the User field [LM 4/26]. Since addresses are permanent (F1), ownership is permanent. Nelson:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

A content operation on document A cannot change the User field of document B's tumbler address, because tumbler addresses do not change. Period. F2 is not a separate constraint that must be enforced — it falls out of address permanence. An implementation that somehow allowed content operations to modify ownership would have violated F1 first.

### F3: Link Endset Immutability

For every operation O:

  **F3.** (A ℓ : ℓ ∈ dom(links) : ℓ'.from = ℓ.from ∧ ℓ'.to = ℓ.to ∧ ℓ'.type = ℓ.type)

No operation modifies any existing link's endsets. Links are "self-contained packages" [LM 4/41] with permanent addresses pointing to immutable I-space content. Since endsets reference I-addresses, and I-addresses are permanent (F1) with immutable content (F0), the endsets themselves need never change — and must not, since other users depend on them:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The endsets are part of the link's *identity*. Modifying them would be changing which content the link connects, which is creating a different link, not modifying the existing one. Nelson:

> "Each link is a self-contained 'package.' Its endsets are its own data, stored at its own address, under its owner's control. No other user's link creation can modify your link's endsets or meaning." [LM 4/41]

Gregory confirms: the link's orgl structure in the granfilade — containing the endset I-spans and type reference — is byte-identical after any `deletevspanpm` operation. The deletion path is confined to the document's POOM subtree and cannot reach the link's orgl by any path in the call graph. The type guard `cenftype == POOM` on every crum in the deletion path categorically prevents traversal into GRAN-type crums where link orgls reside.


## The Cross-Document Frame

We now derive the frame condition that makes compositional reasoning possible across documents. This is where the frame problem becomes most acute: when a user modifies document A, what can we say about documents B, C, ..., Z?

### F4: Cross-Document V-Space Isolation

For every operation O that targets document d:

  **F4.** (A e : e ≠ d ∧ e ∈ dom(poom) : poom'(e) = poom(e))

An operation on document d does not modify any other document's V-space arrangement — not the bottom-level V-to-I mappings, not the intermediate displacement values at any tree level, nothing. This is the isolation property that makes independent authorship possible.

Nelson establishes this through multiple reinforcing principles. The ownership model requires it:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

If INSERT on document A could modify document B's V-space, it would constitute an unauthorized modification of B. The I-space/V-space separation also requires it: since each document has its own V-space arrangement over shared I-space content, modifications to one arrangement need not (and must not) propagate to others.

Gregory provides the implementation evidence that makes this concrete. Each document owns a completely separate POOM tree, created by `createenf(POOM)` and stored under that document's granfilade entry. All POOM mutation functions — `makegappm`, `doinsertnd`, `insertcbcnd`, `recombine`, `setwispupwards` — receive the target document's POOM root pointer and traverse only within that tree. No traversal can cross POOM boundaries because the trees share no node pointers.

The proof of F4 for INSERT is instructive. `makegappm` opens a gap in the target document's V-space by shifting displacements rightward. The loop in `insertnd.c:151` iterates `findleftson(father) → findrightbro(ptr)` over siblings within the target POOM. Since `father` is an intermediate node inside document d's POOM, and `findleftson` and `findrightbro` follow pointers that are internal to that tree, the loop cannot reach any node belonging to document e ≠ d. The displacement write `ptr→cdsp.dsas[V] += width` at `insertnd.c:162` therefore touches only d's nodes. `setwispupwards` propagates upward, stopping at d's POOM root (`isfullcrum`). No pointer from d's POOM leads to e's POOM.

This extends to transclusion. Two documents that transclude the same I-address range each hold their own POOM mapping to those addresses. INSERT in one shifts that document's V-positions; the other document's V-positions are untouched. The shared content (in I-space) is immutable (F0), and each document's *view* of that content is independent.

### F5: Cross-Document I-Space Isolation

For every operation O that targets document d:

  **F5.** (A a : a ∈ dom(ispace) ∧ a was allocated by document e ≠ d : ispace'(a) = ispace(a))

This is actually a special case of F0 (which says ALL I-space content is immutable), but it is worth stating separately because it captures a specific design guarantee that Nelson articulates directly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Deletion in document A removes content from A's V-space. The I-space content itself — including content transcluded into other documents — is untouched. Gregory confirms: `deletend` calls `subtreefree` on orphaned POOM crums (the V→I mapping records), but the I-address content entries in the granfilade are "unreachable from the delete code path." The granfilade is a frame condition of DELETE:

> `granf_after(DELETE) = granf_before(DELETE)` — the granfilade content region is unchanged.

The I-space layer and the V-space layer are structurally disjoint in the delete path. `dodeletevspan` calls `findorgl` (one granfilade read to locate the document's POOM) and then `deletevspanpm`, which operates exclusively on POOM crums. No granfilade write function is called. No spanfilade function is called. The call chain is bounded by construction.


## The Version Frame

Versions introduce a temporal dimension to frame conditions. When a user edits a document — creating, in effect, a new version — all prior versions must remain intact.

### F6: Version Content Preservation

For every editing operation O on document d producing version v:

  **F6.** (A w : w ∈ versions(d) ∧ w ≠ v : frozen'(w) = frozen(w))

Every prior version's frozen V-space arrangement, and therefore its content, is unchanged. Nelson states this as the foundational invariant of the storage architecture:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

And emphatically: "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

F6 is guaranteed by the conjunction of F0 (I-space immutability) and the per-version independence of V-space. Each version has its own V-space arrangement. Editing the current version creates a new V-space mapping; prior versions' mappings are preserved:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

DELETE in a version removes content from that version's V-stream only:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The "may remain included" is understated — the bytes MUST remain in prior versions, because those versions' V-space mappings reference I-space content that is immutable (F0) and permanent (F1). F6 is not an additional guarantee; it follows from F0 + F1 + the structural independence of per-version V-spaces. But stating it explicitly is essential for verification: it allows us to check version preservation by inspection rather than by re-deriving it from first principles for each operation.


## The Link Frame

Links introduce the most intricate frame conditions because they are *independent objects* that interact with content through I-space references. Creating, deleting, or modifying content must preserve link structure; conversely, creating links must preserve content structure.

### F7: Link Address Permanence

For every operation O:

  **F7.** dom(links) ⊆ dom(links')

No operation removes a link from the system. Links, like content, are permanent. Each link occupies a position in its home document's link subspace, numbered by creation order:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

Creating link 2.756 does not renumber links 2.1 through 2.755. The address scheme for links is append-only. Nelson extends the permanence guarantee to the harder case — what happens when content is edited:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

This is actually a statement about F3 (endset immutability) combined with F0 (content immutability): links reference I-space bytes, bytes never move, therefore links survive editing. But F7 adds the separate claim that the link objects themselves persist even when their resolution status might change (e.g., all bytes in one endset have been deleted from every V-space — the link still exists, though it may not resolve in any current version).

### F8: Link Independence

For every MAKELINK operation creating link ℓ:

  **F8.** (A m : m ∈ dom(links) ∧ m ≠ ℓ : links'(m) = links(m))

Creating a link does not modify any existing link's addresses, endsets, or home document association. Nelson:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

Each link is self-contained. Link creation is purely additive — one new entry in the home document's link subspace. The one thing that changes is discoverability: link searches over the relevant region will now return one additional result. But Nelson explicitly guarantees that this does not impede existing searches:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

Gregory confirms the mechanism: `insertendsetsinspanf` writes new entries into the spanfilade (the link index) alongside whatever already exists. It may merge contiguous entries for the same link (an optimization), but it never modifies entries belonging to other links. The underlying B-tree insertion via `insertnd` adopts new crums as siblings of the retrieval position without altering existing crums' semantic content. The extension-merging optimization in `insertcbcnd` (`isanextensionnd`) fires only when the new entry and existing entry share the same `homedoc` AND are perfectly contiguous — that is, it only merges entries belonging to the same link.


## Per-Operation Frame Analysis

We now state the complete frame condition for each operation. The universal frames (F0–F3) apply to all operations; here we specify the additional per-operation frames and verify that each operation's frame is *complete* — that it covers every component of the state.

### INSERT

**Effect**: Allocates new I-addresses, adds them to poom(d) at position p, shifts positions > p in poom(d).

**Frame**: F0 (I-space immutable) + F1 (addresses monotone) + F4 (other documents' POOMs unchanged) + F3 (link endsets unchanged) + F2 (ownership unchanged) + the following operation-specific frame:

  **F-INSERT.** (A q : q ∈ dom(poom(d)) ∧ q < p : poom'(d)(q) = poom(d)(q))

Content *before* the insertion point retains its position and identity. Content at or after p shifts rightward by the inserted width. The I-addresses themselves are unchanged — only the V-positions that map to them are modified.

Gregory confirms: `makegappm` adds `width.dsas[V]` to the `cdsp` of every crum classified as case 1 (between the two blades, i.e., at or after the insertion point). Case 0 crums (before the insertion) are untouched. The blade classification via `insertcutsectionnd` deterministically separates these two sets. The second blade, placed at the next subspace boundary by `findaddressofsecondcutforinsert`, ensures that link-subspace entries (at `2.x`) are classified as case 2 (after the second blade) and left unmoved.

We can now verify L0 after INSERT. Link endsets reference I-addresses. INSERT does not remove any I-address from dom(ispace) (F1). INSERT does not modify any I-address's content (F0). INSERT does not modify any endset (F3). Therefore every span in every endset still references allocated, unchanged content. L0 is preserved. ∎

### DELETE

**Effect**: Removes I-addresses from poom(d) at positions within [p, p + w), shifts positions ≥ p + w in poom(d) leftward by w.

**Frame**: F0 + F1 + F4 + F3 + F2 + F6 (version preservation) + the following:

  **F-DELETE.** (A q : q ∈ dom(poom(d)) ∧ q < p : poom'(d)(q) = poom(d)(q))

And critically:

  **F-DELETE-ISPACE.** dom(ispace') = dom(ispace)

DELETE does not remove content from I-space. This is the subtlest frame condition and the one most commonly misunderstood. Nelson is explicit:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

DELETE removes the V→I mapping record — the POOM crum that said "V-address p maps to I-address α." The I-space content at α persists unconditionally. Gregory confirms: `deletend` calls `subtreefree` on orphaned POOM crums (freeing the mapping records from memory), but the granfilade entries for the corresponding I-addresses are "never examined, modified, or freed." The `subtreefree` function has a GRAN-specific branch that could call `orglfree`, but it requires `cenftype == GRAN` — and every crum in the delete path has `cenftype == POOM`, making that branch dead code for this call path.

We also verify F4 for DELETE. The delete path is: `dodeletevspan → findorgl (one granfilade read) → deletevspanpm → deletend`. Every pointer touched by `deletend` descends from `fullcrumptr`, which is document d's POOM root. All crums in d's POOM have `cenftype == POOM`. No pointer into the granfilade's content region or into any other document's POOM is ever dereferenced.

An important subsidiary frame: DELETE on document d does not modify the granfilade, the spanfilade, or any link's orgl structure. The link orgl's endset I-spans, type reference, and internal structure remain byte-identical. Gregory traces the full call chain and confirms that `deletevspanpm` is "strictly bounded to the document's POOM and cannot reach the link's orgl by any path in the call graph."

### REARRANGE

**Effect**: Permutes V-positions within poom(d) by transposing two regions.

**Frame**: F0 + F1 + F4 + F3 + F2 + plus:

  **F-REARRANGE.** (A a : a ∈ range(poom(d)) : a ∈ range(poom'(d)))

The multiset of I-addresses in d's V-space is invariant under REARRANGE. Only the V-positions change; the I-addresses do not. This is a stronger frame than DELETE's because REARRANGE does not remove any V→I mapping — it only permutes them. Nelson: "Rearrange transposes two regions of text" [LM 4/67].

However, there is a critical caveat regarding subspace isolation. Gregory documents that REARRANGE uses `tumbleradd` on V-displacements, and `tumbleradd` has no exponent guard. Unlike DELETE, where `strongsub` returns entries with higher exponents unchanged, REARRANGE can move content across subspace boundaries — potentially placing text content at link-subspace V-positions. The subspace convention `{1.x for text, 2.x for links}` is enforced by INSERT's two-blade mechanism but not by REARRANGE. This is an asymmetry in the frame: INSERT preserves subspace structure; REARRANGE does not.

We state this as a conditional frame:

  **F-REARRANGE-SUBSPACE.** ¬[(A d : : subspace-structure of poom(d) is preserved by REARRANGE)]

This is a *negative result* — the subspace frame does NOT hold for REARRANGE. An abstract specification should either strengthen the precondition (require that REARRANGE cuts not cross subspace boundaries) or acknowledge the gap. The implementation evidence shows this is a known architectural fragility, not a design intent.

### COPY (Transclusion)

**Effect**: Adds entries to poom(d) mapping new V-positions to existing I-addresses from the source.

**Frame**: F0 + F1 + F4 + F3 + F2 + plus:

  **F-COPY-SOURCE.** poom'(source) = poom(source)

The source document's POOM is guaranteed completely unmodified by the copy operation — including all intermediate tree node displacements. Gregory confirms: `specset2ispanset` (the read step) traverses the source POOM via `findcbcinarea2d`, which is a pure B-tree walk. No `ivemodified` is called on any source crum. No `makegappm` runs on the source. The source POOM's logical content — widths, displacements, and the disk-dirty flag — is guaranteed unmodified.

The one physical side-effect: the LRU `age` field is written on every source crum traversed (by `rejuvinateifnotRESERVED`), and `findleftson` may fault in children from disk (populating `leftson` and `numberofsons` pointers). These are cache-management effects that do not alter the logical state. An abstract specification should note: COPY reads the source without logical modification, though physical cache state may change.

COPY also writes to the spanfilade — specifically, DOCISPAN entries registering the target document as containing the copied I-addresses. This is an index update, not a content modification. The source document's spanfilade entries are untouched.

### MAKELINK

**Effect**: Creates a new link ℓ with endsets referencing specified I-address spans. Adds ℓ to dom(links). Adds a V-space entry in ℓ.home's link subspace.

**Frame**: F0 + F1 + F4 + F8 (link independence) + plus:

  **F-MAKELINK-CONTENT.** (A d : : poom'(d) text subspace = poom(d) text subspace)

MAKELINK does not touch any document's text-subspace V-positions. It adds an entry in the link subspace (`2.x`) of the home document only.

MAKELINK does modify the spanfilade — adding index entries for the new link's endsets so that link searches can discover it. Gregory confirms that `insertendsetsinspanf` writes new entries alongside existing ones, with two caveats: (1) extension merging may widen an existing crum if the new entry is contiguous with the same link's existing entry, and (2) `expandcrumleftward` may shift existing crums' coordinate offsets when the insertion point lies to the left of the current tree extent. Both are internal to the spanfilade's B-tree structure and do not affect the logical content of existing link index entries — they are structural reorganizations, not semantic modifications.

### CREATENEWDOCUMENT

**Effect**: Allocates a new document address, creates an empty POOM.

**Frame**: F0 + F1 + F2 + F3 + F4 + F6 + plus:

  **F-NEWDOC.** (A d : d ∈ dom(poom) before O : poom'(d) = poom(d) ∧ versions'(d) = versions(d) ∧ access'(d) = access(d))

Creating a document does not alter any existing document's content, structure, permissions, or version history. Nelson:

> "CREATENEWDOCUMENT: This creates an empty document. It returns the id of the new document." [LM 4/65]

The operation is purely additive in every component of the state.

### CREATENEWVERSION

**Effect**: Creates a new document whose POOM is initialized with the source's text-subspace content.

**Frame**: F0 + F1 + F4 + F3 + F2 + plus:

  **F-VERSION-SOURCE.** poom'(source) = poom(source) ∧ links'(source) = links(source)

The source document is unmodified. Gregory traces the full execution: `docreatenewversion` calls `createorglingranf` (allocates a new granfilade entry for the version), then `docopyinternal`, which reads the source POOM (pure read via `specset2ispanset`), writes to the new version's POOM (via `insertpm`), and registers DOCISPAN entries in the spanfilade (via `insertspanf`). No code path writes to the source document's POOM.

The granfilade content region is a frame condition: `docopyinternal` reads it (to convert V-spans to I-spans) but never writes it. No new I-addresses are allocated — the existing I-addresses from the source are simply referenced. The content store grows only by a new POOM subtree for the version document and new spanfilade index entries.

### Access Policy Changes (Sharing / Publishing)

**Effect**: Modifies access(d) for a single document d.

**Frame**: F0 + F1 + F3 + plus:

  **F-ACCESS.** (A e : e ≠ d : access'(e) = access(e)) ∧ poom'(d) = poom(d) ∧ addrs' = addrs

Changing a document's access policy does not modify any other document's access, does not modify the document's own content or arrangement, and does not modify the address space. Nelson:

> "A document may be private or published." [LM 2/42]

The access policy is a property of the document's ownership and publication status — not of its address, content, or structure. Each user's relationship to content is structurally independent. Nelson's privacy constraint reinforces this:

> "The network will not, may not monitor what is read or what is written in private documents." [LM 2/59]

A system that coupled one user's access to another's would require tracking both users' states in relation to the same document — precisely the kind of monitoring Nelson prohibits.


## The Frame Composition Theorem

We can now state the central result. Let P be any invariant of the system that depends only on the components of Σ. Let O be any operation. If the frame conditions of O cover every component that P mentions — that is, if O's frame explicitly states that each component appearing in P is either unchanged or modified in a way consistent with P — then O preserves P.

More precisely, let `mentions(P)` be the set of state components referenced by predicate P. Let `frame(O)` be the set of state components that O guarantees unchanged. Let `effect(O)` be the set of state components that O modifies, together with the specification of how they are modified.

  **R0 (Frame Completeness).** An operation O has a *complete* frame if and only if:

  mentions(P) ⊆ frame(O) ∪ effect(O) for every system invariant P.

That is, every component of the state either has an explicit preservation guarantee (frame) or an explicit modification specification (effect). No component is left unspecified.

We observe that the frames established above achieve R0 for the Xanadu operations. For each operation, we can partition the state components:

| Component | INSERT | DELETE | REARRANGE | COPY | MAKELINK | NEWDOC | NEWVERSION |
|-----------|--------|--------|-----------|------|----------|--------|------------|
| ispace content | F0 | F0 | F0 | F0 | F0 | F0 | F0 |
| ispace domain | effect (+) | F-DEL-I | F1 | F1 | F1 | F1 | F1 |
| poom(d) | effect | effect | effect | effect | effect (2.x) | — | effect |
| poom(e≠d) | F4 | F4 | F4 | F4 | F4 | F4 | F4 |
| links | F3 | F3 | F3 | F3 | effect (+) | F3 | F3 |
| owner | F2 | F2 | F2 | F2 | F2 | F2 | F2 |
| access | frame | frame | frame | frame | frame | frame | frame |
| versions | F6 | F6 | F6 | F6 | F6 | frame | F6 |
| addrs | effect (+) | F1 | F1 | F1 | effect (+) | effect (+) | effect (+) |

Every cell is either "effect" (explicitly specified modification), "F*" (explicit preservation by named frame condition), or "frame" (preserved, covered by a general frame). No cell is blank. This is what frame completeness means: the specification is total over the state space.


## The Negative Space

We have derived the positive frame conditions — what IS preserved. We should also note what is NOT guaranteed by the frame conditions, because the boundaries of the frame are as informative as the frame itself.

**F0 does not guarantee content accessibility.** Content at I-address a always exists and never changes (F0 + F1), but it may not be reachable through any current V-space. DELETE removes V→I mappings. A byte can be permanently stored yet currently invisible — "DELETED BYTES (not currently addressable, awaiting historical backtrack functions)" [LM 4/9]. The frame preserves existence, not accessibility.

**F4 does not guarantee V-position stability within the target document.** INSERT at position p shifts all positions > p. The frame explicitly allows this: content "after" the insertion point moves. A reference to V-position 5 in document d may point to different content after an INSERT at position 3. Only I-space references are stable; V-space references within the target document are deliberately mutable.

**F8 does not guarantee link discovery stability.** Creating a new link adds one result to relevant link searches. The set of links returned by FINDLINKSFROMTOTHREE grows monotonically — existing results remain, but the total set changes. The frame preserves existing links' content (F3, F8) but not the cardinality of search results.

**REARRANGE does not guarantee subspace preservation.** As noted in F-REARRANGE-SUBSPACE, the implementation permits REARRANGE to move content across the text/link subspace boundary. This is a gap in the frame — the subspace convention is a convention, not an invariant enforced by REARRANGE.


## The Architectural Foundation

We conclude by observing why Xanadu's frame conditions are so clean. The fundamental architectural decision — separating content (I-space) from arrangement (V-space) — creates a natural partition of the state that makes frame conditions almost trivial to state and verify.

Every editing operation modifies V-space. No editing operation modifies I-space. Therefore:
- Every I-space property (content immutability, address permanence, link endset stability) is automatically a frame condition of every editing operation.
- Every V-space property (arrangement, positions, document boundaries) is local to one document. Therefore cross-document isolation (F4) follows from the per-document structure of V-space.

The one layer that bridges I-space and V-space is the spanfilade (the link index), which maps I-addresses to link associations for efficient discovery. The spanfilade is monotonically growing (write-only in its logical content, per Gregory's analysis) — entries are added but never removed. This monotonicity means the spanfilade's growth can never invalidate an existing query result; it can only add new results. The frame for the spanfilade is not "unchanged" but "superset" — a weaker but sufficient guarantee.

Nelson designed the architecture so that frame conditions would hold by construction:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

"No copying operations" is itself a frame condition — it means that updates are non-propagating. When document A includes content from document B, and B is modified, A does not need to be updated because A references I-space content that never changes (F0). The "problem of update" is the frame problem, and Xanadu solves it at the architectural level by making I-space immutable.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| F0 | (A a : a ∈ dom(ispace) : ispace'(a) = ispace(a)) — content at an allocated address never changes, for any operation | introduced |
| F1 | dom(ispace) ⊆ dom(ispace') ∧ dom(addrs) ⊆ dom(addrs') — allocated addresses grow monotonically, never shrink | introduced |
| F2 | (A d : d ∈ dom(owner) : owner'(d) = owner(d)) — ownership is unchanged by non-transfer operations | introduced |
| F3 | (A ℓ : ℓ ∈ dom(links) : ℓ'.from = ℓ.from ∧ ℓ'.to = ℓ.to ∧ ℓ'.type = ℓ.type) — no operation modifies existing link endsets | introduced |
| F4 | (A e : e ≠ d : poom'(e) = poom(e)) — operations on document d leave all other documents' V-spaces unchanged | introduced |
| F5 | (A a : a ∈ dom(ispace) ∧ allocated-by(a) ≠ d : ispace'(a) = ispace(a)) — cross-document I-space isolation (special case of F0) | introduced |
| F6 | (A w : w ∈ versions(d) ∧ w ≠ v : frozen'(w) = frozen(w)) — editing preserves all prior versions | introduced |
| F7 | dom(links) ⊆ dom(links') — no operation removes a link from the system | introduced |
| F8 | (A m : m ∈ dom(links) ∧ m ≠ ℓ : links'(m) = links(m)) — link creation does not modify any existing link | introduced |
| R0 | Frame completeness: mentions(P) ⊆ frame(O) ∪ effect(O) for every invariant P and operation O | introduced |
| L0 | (A ℓ : ℓ ∈ dom(links) : (A s : s ∈ ℓ.from ∪ ℓ.to ∪ ℓ.type : s ⊆ dom(ispace))) — every link endset references allocated content | introduced |
| F-INSERT | (A q : q < insertion-point : poom'(d)(q) = poom(d)(q)) — content before insertion point unchanged | introduced |
| F-DELETE-ISPACE | dom(ispace') = dom(ispace) — DELETE does not remove I-space content | introduced |
| F-REARRANGE | multiset(range(poom(d))) is invariant under REARRANGE — same I-addresses, different V-positions | introduced |
| F-REARRANGE-SUBSPACE | REARRANGE does NOT preserve subspace structure — a known gap in the frame | introduced |
| F-COPY-SOURCE | poom'(source) = poom(source) — source POOM is logically unmodified by COPY | introduced |
| F-MAKELINK-CONTENT | text subspace of every poom(d) is unchanged by MAKELINK | introduced |
| F-NEWDOC | creating a document alters no existing document's content, structure, permissions, or version history | introduced |
| F-VERSION-SOURCE | poom'(source) = poom(source) ∧ links'(source) = links(source) — version creation does not modify source | introduced |
| F-ACCESS | access policy changes do not modify content, arrangement, addresses, or other documents' access | introduced |
| Σ.ispace | ispace : Addr ⇀ Content — the permanent content store | introduced |
| Σ.poom | poom : DocId → (Pos → Addr) — per-document V-to-I mappings | introduced |
| Σ.links | links : LinkId → Link — the link store with from/to/type endsets | introduced |
| Σ.owner | owner : DocId → UserId — the ownership function | introduced |
| Σ.access | access : DocId → AccessPolicy — per-document access policy | introduced |
| Σ.versions | versions : DocId → DAG(VersionId) — version history with frozen arrangements | introduced |
| Σ.addrs | addrs : Set(Addr) — all allocated tumbler addresses | introduced |


## Open Questions

- Must the spanfilade's logical content be strictly monotone (entries only added, never removed), or could a compaction operation merge entries without violating frame conditions?
- What frame conditions must ownership transfer satisfy beyond preserving link resolution and content accessibility?
- Must access policy changes be atomic with respect to concurrent read operations, or can a partially-applied access change be observable?
- What must the frame condition for REARRANGE guarantee about subspace boundaries to close the gap identified in F-REARRANGE-SUBSPACE?
- Must historical backtrack (retrieving prior versions) guarantee zero side-effects on the current version's state?
- What invariants must a garbage collection or compaction operation preserve if I-space content that is unreachable from any V-space is ever reclaimed?
- Must link discovery results be monotone with respect to the set of created links, or can index reorganization temporarily hide a recently-created link?
- What frame conditions must hold for operations that span multiple documents simultaneously (e.g., transclusion that reads one and writes another)?
- Under what conditions can an operation's cache-management side-effects (LRU age updates, child faulting) violate frame conditions in a concurrent or crash-recovery context?
- Must the frame condition for CREATENEWVERSION guarantee that the source document's link subspace is excluded from the copy, or is this an implementation choice?
