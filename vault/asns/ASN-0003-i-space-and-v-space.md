# ASN-0003: I-Space and V-Space

*2026-02-23*

We are looking for the invariant that connects permanent content storage to mutable document arrangement. The system maintains two address spaces — one for content identity, one for content presentation — and the relationship between them is the architectural foundation. We want to know: what must be true of this relationship for permanence, transclusion, link survivability, and version reconstruction to hold?

---

## The Problem

A content system that permits editing faces a tension: content must be both *permanent* (for citation, attribution, and link survivability) and *rearrangeable* (for editing, versioning, and quotation). These are contradictory if content and arrangement occupy the same space. The resolution is to separate them.

We posit two spaces. **I-space** is the space of content identity — where bytes live permanently. **V-space** is the space of content arrangement — where a document's current presentation is defined. The central question is: what properties must the I-space/V-space separation satisfy for the system's guarantees to hold?

We proceed by deriving these properties from what the system must guarantee.

---

## The State

We need a model of what the system *is*, before we can reason about what it *maintains*.

Let `Σ` denote the system state. We introduce three components:

**IV-Σ1.** `Σ.I : Addr → Byte` is a partial function from I-space addresses to content bytes. The domain `dom(Σ.I)` is the set of all allocated I-addresses.

**IV-Σ2.** For each document-version `d`, `Σ.V(d) : Nat⁺ → Addr` is a total function from positive natural numbers (V-positions) to I-space addresses. The domain is `{1, ..., #Σ.V(d)}` where `#Σ.V(d)` is the document-version's current length.

**IV-Σ3.** `Σ.docs` is the set of all document-versions that currently exist.

The distinction is already visible: `Σ.I` grows monotonically (we shall prove this), while each `Σ.V(d)` changes freely under editing. But the connection between them — the fact that `Σ.V(d)` only ever points *into* `Σ.I` — is the invariant we are after.

---

## The Fundamental Invariant

We begin with the property that makes the system coherent. Every V-position in every document must resolve to content that actually exists:

**IV0 (Referential Integrity).** For all document-versions `d` and positions `p`:

    [d ∈ Σ.docs ∧ 1 ≤ p ≤ #Σ.V(d)  ⇒  Σ.V(d)(p) ∈ dom(Σ.I)]

That is: every position in a document's visible arrangement maps to an I-space address at which content exists. There are no dangling references. No V-position points into the void.

This is not a defensive check bolted on afterward — it is the property from which the system's guarantees flow. Nelson states it through the retrieval guarantee: "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." A system in which some V-positions resolve to nothing violates this unconditionally. The part-pounce model requires that every fragment "actually exists."

We observe that IV0 is a *conjunction* of two things: (i) `Σ.V(d)` is total over its domain, and (ii) its range lies within `dom(Σ.I)`. The first is a property of V-space (no gaps). The second is a property of the relationship between V-space and I-space (no dangling references). We shall derive both.

---

## I-Space Properties

What must be true of I-space for IV0 to be maintained?

**IV1 (Content Permanence).** No operation removes an address from `dom(Σ.I)`:

    [a ∈ dom(Σ.I)  ⇒  a ∈ dom(Σ'.I)]

for any state transition `Σ → Σ'`. This is Nelson's append-only principle: "suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." I-space only grows.

The consequence for IV0 is immediate: if a V-position pointed to a valid I-address before some operation, and the operation does not remove I-addresses, then the V-position still points to a valid I-address afterward. IV1 is the *persistence* half of referential integrity.

**IV2 (Content Immutability).** The content at an I-address never changes:

    [a ∈ dom(Σ.I)  ⇒  Σ'.I(a) = Σ.I(a)]

for any transition `Σ → Σ'`. Once a byte is stored at address `a`, that byte is fixed forever. This is stronger than permanence — not only does the address remain allocated, but its content is frozen.

IV2 is what makes I-addresses meaningful as *identifiers*. If content could change, then knowing the address would not tell you what content you would find. Attribution, link attachment, version correspondence — all depend on the identity between address and content being eternal.

**IV3 (Address Uniqueness).** No I-address is ever assigned to different content:

    [a ∈ dom(Σ.I) ∧ a ∉ dom(Σ₀.I)  ⇒  (A Σ' : Σ' is a successor of Σ : Σ'.I(a) = Σ.I(a))]

where `Σ₀` is the initial (empty) state. Every address is born with one piece of content and keeps it forever. This follows from IV1 and IV2 together: permanence ensures the address persists, immutability ensures its content is fixed. We state IV3 separately because its consequence is distinct: *address reuse is impossible*. Even if content is removed from every document's V-space, the I-address remains occupied. Nelson is explicit: allocation "goes forward. It never retreats."

**IV4 (Fresh Allocation).** When an operation allocates new I-addresses, those addresses are outside the current domain:

    [a ∈ dom(Σ'.I) \ dom(Σ.I)  ⇒  a ∉ dom(Σ.I)]

This is trivially true as stated (it is the definition of set difference), but its operational import is that the allocation mechanism must produce addresses not previously used. The tumbler system achieves this through monotonic counters — each new allocation increments within its document's subtree, never revisiting previous values.

Gregory confirms that allocation is document-isolated: `findisatoinsertmolecule` searches only within the target document's I-address subtree, and the upperbound is computed from the document's own hint address. A concurrent allocation in a different document cannot interfere. This means fresh allocation is a *family of independent functions partitioned by document* — a property that will matter when we consider concurrency.

---

## V-Space Properties

What must be true of V-space for IV0 to hold?

**IV5 (Dense Contiguity).** For each document-version `d`, the V-space is a dense, gap-free sequence:

    [dom(Σ.V(d)) = {1, ..., #Σ.V(d)}]

There are no holes. If a document has 100 bytes, they occupy V-positions 1 through 100. When content is deleted, the gap closes — subsequent positions shift down. When content is inserted, subsequent positions shift up. V-space is always a contiguous interval of natural numbers.

This is critical for the document to be a *stream* rather than a sparse mapping. Nelson defines documents through "logical addressing of the byte stream" and specifies that "V-address 1 is always the first byte of the document right now." The stream metaphor requires contiguity.

**IV6 (V→I is a Total Function).** For each document-version `d`, the mapping `Σ.V(d)` is a total function on its domain:

    [(A p : 1 ≤ p ≤ #Σ.V(d) : (E! a : a ∈ dom(Σ.I) : Σ.V(d)(p) = a))]

Every V-position maps to exactly one I-address. No V-position is unmapped (totality), and no V-position maps to two different I-addresses (functionality). This is the *definitional* property of a document: "The document IS the mapping from V-addresses to I-addresses."

Gregory confirms this at the implementation level: the POOM enfilade enforces non-overlapping V-ranges. The tree traversal function `findcbcnd` breaks on the first match among sibling nodes — it *assumes* each V-address falls in at most one child. The insertion mechanism `makegappm` shifts existing content to prevent overlaps. The classification function `whereoncrum` returns exactly one answer per address. Every layer of the implementation encodes the assumption that V→I is functional.

**IV7 (I→V is a Multimap).** The same I-address may appear at multiple V-positions, both within a single document and across documents:

    [¬ (A d, p, q : p ≠ q ∧ 1 ≤ p,q ≤ #Σ.V(d) : Σ.V(d)(p) ≠ Σ.V(d)(q))]

That is: `Σ.V(d)` is *not* required to be injective. This is the formal basis of transclusion. When content at I-address `a` appears at V-positions 5 and 47 in the same document, both `Σ.V(d)(5) = a` and `Σ.V(d)(47) = a` hold simultaneously. The same content is referenced twice without duplication.

Nelson's "glass pane" metaphor makes this vivid: a document is layers of painted glass with transparent windows. Two windows may look through to the same underlying content. The V-space structure records both references; I-space holds the content once.

Gregory confirms that self-transclusion is supported: the `insertpm` function has no constraint preventing the same I-address at multiple V-positions. The I→V retrieval function `permute` returns *all* V-positions referencing a given I-address — it accumulates every matching leaf node in the POOM tree via `findcbcinarea2d`, which walks all siblings and descends recursively without stopping at the first match.

---

## The Frame Conditions

Having established what the two spaces are, we now ask: what does each operation preserve? The frame conditions are as important as the effects — an operation that establishes its postcondition but silently violates a seemingly-unrelated invariant has not been correctly specified.

**IV8 (V-operations Preserve I-space).** No operation that modifies V-space alters I-space content:

    [(A a : a ∈ dom(Σ.I) : Σ'.I(a) = Σ.I(a))]

for any V-space operation (DELETE, REARRANGE, COPY) applied to any document. These operations modify the arrangement; they never touch the content. Nelson is definitive: "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."

INSERT is special: it both extends I-space (allocating new addresses for the inserted content) and modifies V-space (placing the new content and shifting subsequent positions). But even INSERT satisfies IV8 for all *pre-existing* I-addresses — it adds to `dom(Σ.I)` without changing the content at any existing address.

We can state this more precisely. For any operation `op`:

    Σ'.I = Σ.I ⊕ fresh

where `⊕` denotes extension — `Σ'.I` agrees with `Σ.I` on all of `dom(Σ.I)` and may additionally be defined on new addresses `fresh` where `fresh ∩ dom(Σ.I) = ∅`. For DELETE, REARRANGE, and COPY, `fresh = ∅`. For INSERT, `fresh` is the set of newly allocated I-addresses.

**IV9 (I-space Operations Do Not Exist).** There is no operation that modifies I-space content at an existing address. The only way I-space changes is through extension — the allocation of new addresses with new content. This is the operational meaning of IV1 and IV2 taken together.

**IV10 (Cross-Document V-Independence).** An operation on document `d` does not modify `Σ.V(d')` for any `d' ≠ d`:

    [op applied to d  ⇒  (A d' : d' ≠ d : Σ'.V(d') = Σ.V(d'))]

Each document's V-space is independent of every other's. Deleting content from document A has no effect on document B's arrangement, even if both reference the same I-addresses. This is what makes the system scale: documents are coupled only through shared I-space content, never through shared V-space state.

Gregory confirms this at the implementation level: `makegappm` shifts V-positions only within the target document's POOM. The I-displacement and I-width fields of shifted entries are "guaranteed untouched" — only `ptr->cdsp.dsas[V]` is modified. Other documents' POOMs are never accessed during an edit operation.

---

## The Coherence Theorem

We are now in a position to prove that IV0 is maintained by all operations. The argument is:

*Claim (IV0-PRES).* If `Σ` satisfies IV0 and `Σ → Σ'` is a valid operation, then `Σ'` satisfies IV0.

We reason by cases on the operation type.

**Case: INSERT at position `p` in document `d`.**

INSERT allocates fresh I-addresses `F = {f₁, ..., fₖ}` for the new content and places them at V-positions `p, p+1, ..., p+k-1`, shifting all subsequent positions by `k`.

For the new positions: `Σ'.V(d)(p+i-1) = fᵢ ∈ F ⊆ dom(Σ'.I)` by construction — the content is allocated in I-space before (or simultaneously with) the V-space mapping. Gregory confirms: `inserttextingranf` allocates fresh I-addresses in the granfilade, then `insertpm` creates the POOM mappings. The I-addresses exist because they were just allocated.

For the shifted positions: `Σ'.V(d)(q+k) = Σ.V(d)(q)` for `q ≥ p`. By IV0 on `Σ`, `Σ.V(d)(q) ∈ dom(Σ.I)`. By IV1, `dom(Σ.I) ⊆ dom(Σ'.I)`. Therefore `Σ'.V(d)(q+k) ∈ dom(Σ'.I)`.

For unshifted positions: `Σ'.V(d)(q) = Σ.V(d)(q)` for `q < p`. Same reasoning as above.

For other documents: `Σ'.V(d') = Σ.V(d')` by IV10. Their V-positions pointed to valid I-addresses before, and IV1 keeps those addresses valid.

**Case: DELETE of positions `p` through `p+k-1` in document `d`.**

DELETE removes V-positions and closes the gap. It does not touch I-space. For the remaining positions: those below `p` are unchanged; those above `p+k-1` are shifted down by `k`. In both cases, the I-address they point to is unchanged (the V→I mapping for surviving positions is preserved), and those I-addresses remain in `dom(Σ'.I)` by IV1.

Gregory adds an important observation: after deletion, the POOM completely erases the V→I association — "no structure remains in the POOM that records which I-addresses were once referenced." But the I-addresses themselves persist in the granfilade. The association is erased *from the document's perspective*, not from the system's. This is precisely the separation of concerns: V-space forgets; I-space remembers.

**Case: REARRANGE (transposition of two regions in document `d`).**

REARRANGE permutes V-positions without creating or destroying content. Every V-position in the result maps to some I-address that was mapped before the operation. By IV0 on `Σ`, those addresses are valid. By IV1, they remain valid.

**Case: COPY (transclusion of content into document `d`).**

COPY reads I-addresses from a source document's POOM and creates V-space mappings in the target document. No new I-addresses are allocated — the target gets V-positions pointing to the *same* I-addresses as the source. By IV0 on `Σ`, the source's V-positions point to valid I-addresses. Those same addresses are used in the target. By IV1, they remain valid.

This is where IV7 becomes operationally relevant: COPY may cause the same I-address to appear at multiple V-positions (within the same document or across documents). IV6 is not violated because each V-position still maps to exactly one I-address — it is just that multiple V-positions may share that address.

**Case: CREATENEWVERSION of document `d`, producing document `d'`.**

Version creation produces a new document whose V-space initially references the same I-addresses as the source. No content is duplicated: `Σ'.V(d')(p) = Σ.V(d)(p)` for all positions `p`. By IV0 on `Σ` and IV1, all references remain valid. Nelson: versions are "the same materials" refracted through different arrangements — "there is thus no 'basic' version of a document set apart from other versions."

This completes IV0-PRES. In each case, the argument has the same structure: newly created V-positions point to I-addresses that were just allocated or already existed, and IV1 ensures existing I-addresses persist. The proof is almost disappointingly uniform — which is the sign that the invariant is well-chosen.  ∎

---

## Consequences

Having established the invariant and its preservation, we now derive the properties that motivate the entire design.

### Link Survivability

A link attaches to I-space addresses — not V-positions. When content is deleted from a document, only the V→I mapping is removed. The I-addresses persist (IV1), the content persists (IV2), and the link's endset addresses remain valid.

More precisely, let a link `L` have endset addresses in `S ⊆ dom(Σ.I)`. After any sequence of V-space operations producing `Σ'`, we have `S ⊆ dom(Σ'.I)` by IV1. The link remains well-defined.

Gregory confirms the operational consequence: if content at I-addresses `[X, X+5]` is transcluded into two documents and deleted from one, link discovery through the surviving document continues to work. The surviving document's POOM provides the V→I bridge to the permanent I-space layer where links are indexed. The link discovery function `findlinksfromtothreesp` converts V-specs to I-spans via the document's POOM, then searches the link index (spanfilade) using those I-spans. Because the spanfilade is indexed by I-addresses — not V-positions — it finds the link regardless of which document provides the V→I translation.

Nelson foresaw this precisely: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing."

### Version Correspondence

When two versions share I-addresses (which they always do initially, by the definition of CREATENEWVERSION), the system can determine *which parts correspond* without metadata. Correspondence is structural: V-positions in version `d₁` and version `d₂` correspond when they map to the same I-address.

    correspond(d₁, p₁, d₂, p₂)  ≡  Σ.V(d₁)(p₁) = Σ.V(d₂)(p₂)

This is computable because both sides are deterministic lookups. Nelson: "a facility that holds multiple versions is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same."

If CREATENEWVERSION duplicated content (assigning fresh I-addresses), this correspondence would be impossible to compute — there would be no structural basis for determining which bytes are "the same." The entire version-comparison model depends on I-space sharing.

### Origin Traceability

Because I-addresses encode their origin structurally (the tumbler hierarchy includes node, user, document, and element fields), and because content immutability (IV2) means the address is *the* permanent identifier, the origin of any content is always recoverable.

Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character."

This is not metadata that can be stripped or lost. It is the address itself. To retrieve content, the system must ask the home location. The connection between identity and origin is architectural.

### Attribution and Accounting

The non-duplication property (IV7, combined with COPY producing shared rather than fresh I-addresses) means the system can account for content usage. When document B transcludes content from document A, the shared I-addresses allow the system to trace the content back to A's home location. Nelson's royalty model depends on this: every byte delivered to a reader has a traceable origin, and that origin determines compensation.

---

## The V→I Mapping as Document Identity

We observed that `Σ.V(d)` defines a document-version's content. But we should be more precise: a document-version *is* its V→I mapping. Two document-versions with the same mapping are, from the system's perspective, the same arrangement.

**IV11 (Viewer Independence).** The mapping `Σ.V(d)` is a property of the document-version, not the viewer:

    [(A viewers u₁, u₂ : Σ.V(d) as observed by u₁ = Σ.V(d) as observed by u₂)]

Two users requesting the same V-position in the same version receive the same I-space content. The back-end operation RETRIEVEV takes a document-version and a set of V-spans; it returns the corresponding I-space content deterministically. No viewer parameter exists in the protocol.

Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" — where "you" is universal.

Viewer experience may *diverge* — different users may view different versions (front-end choice), filter links differently (front-end presentation), or render content differently (front-end typography). But the V→I mapping itself, which is the back-end's responsibility, is viewer-invariant. The front end chooses *which* version to request; the back end serves *that* version's mapping deterministically.

This property is architecturally necessary for attribution, correspondence, and accounting to be well-defined. If the mapping varied by viewer, "the home document of any specific word" would be viewer-dependent — an indeterminacy fatal to every guarantee.

---

## Atomicity of State Transitions

We asserted that operations produce coherent new states. We now make this precise.

**IV12 (Transition Atomicity).** Each operation transitions the system from one state satisfying IV0 to another state satisfying IV0, with no observable intermediate state that violates IV0:

    [IV0(Σ) ∧ op(Σ, Σ')  ⇒  IV0(Σ')]

There is no point at which a client can observe a V-position pointing to an unallocated I-address, or a gap in V-space, or an I-address whose content is partially written. Nelson does not use the word "atomic," but his operation descriptions and retrieval guarantees require it.

Consider INSERT: Nelson specifies that the command inserts text at a position *and* shifts all following addresses as part of one operation. If only one happened — content placed but addresses not shifted, or addresses shifted but no content placed — the V-space would be inconsistent (gap or overlap). The canonical order mandate confirms this: "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." The phrase "once made" implies the transition is complete — there is no observable state where the file is not in canonical order.

Gregory reveals that the implementation achieves this through single-threaded execution (a `select()` event loop) rather than through a transactional mechanism. The abstract property (no intermediate state visible to clients) is implementation-independent; the mechanism (single thread vs transactions vs locks) is implementation-specific.

---

## The Monotonicity Theorem

From IV1 (content permanence) and IV4 (fresh allocation), a structural theorem follows.

*Theorem (MON-I).* `dom(Σ.I)` is monotonically non-decreasing:

    [dom(Σ.I) ⊆ dom(Σ'.I)]

for any transition `Σ → Σ'`.

*Proof.* IV1 states that no operation removes addresses from `dom(Σ.I)`. Operations may add addresses (INSERT adds fresh ones; CREATENEWVERSION may allocate structural addresses). Therefore the domain only grows.  ∎

This is a one-line proof, but its consequence is profound: the set of things that exist never shrinks. Every I-address ever allocated, every byte ever stored, every identity ever created — all persist. The system accumulates content monotonically.

Note that V-space has no corresponding monotonicity. Documents grow and shrink freely. V-positions come and go. The total number of V-positions across all documents may decrease (through deletions). Monotonicity is an I-space property, not a system-wide property.

---

## The Deletion Asymmetry

We have shown that DELETE removes V-space mappings while preserving I-space content. But the implications of this asymmetry deserve explicit treatment.

After DELETE of position `p` from document `d`:

1. `Σ'.V(d)` no longer maps any position to `Σ.V(d)(p)` (the V→I association is erased)
2. `Σ.V(d)(p) ∈ dom(Σ'.I)` (the I-address persists by IV1)
3. `Σ'.I(Σ.V(d)(p)) = Σ.I(Σ.V(d)(p))` (the content is unchanged by IV2)

The content has not been destroyed. It has been made *unreachable from this document*. Other documents that reference the same I-address are unaffected (IV10). Links that point to the I-address remain valid (the address is still in `dom(Σ'.I)`). Previous versions of the document still reference the content (their V-spaces are independent snapshots).

Nelson distinguishes this from conventional deletion: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" The bytes are "not currently addressable" in V-space — they have been removed from the document's visible arrangement. But they remain permanently addressable in I-space.

Gregory's evidence sharpens this: after DELETE, the POOM "completely erases" the V→I mapping — "`subtreefree` recursively frees the nodes, no copy of the pre-deletion tree state is preserved." The document has no memory of what it once contained. But the I-space content persists, and the spanfilade (the link index) retains stale references — it still lists the document as containing those I-addresses, even though the document's POOM no longer maps to them. This creates an asymmetry between the document's view (content gone) and the system's view (content still indexed).

We observe that *DELETE is not the inverse of INSERT*. If we INSERT content (allocating I-addresses `F`), then DELETE it, then INSERT identical bytes, the second INSERT allocates *fresh* I-addresses `F' ≠ F` (by IV4). The V-space looks the same, but the I-space identity is different. All links, transclusions, and correspondence relationships that attached to `F` do not attach to `F'`. The identity has been severed.

This is not a deficiency — it is a consequence of the fundamental design. Addresses are permanent and unique (IV3). There is no mechanism to "reuse" an I-address, because that would violate immutability. The only way to restore a severed I-space identity is through COPY from a document that still references the original I-addresses.

---

## The Multimap Structure

We stated in IV7 that `Σ.V(d)` need not be injective — the same I-address may appear at multiple V-positions. We now examine the structure this creates.

For an I-address `a ∈ dom(Σ.I)`, define the *referent set* across the entire system:

    refs(a) = {(d, p) : d ∈ Σ.docs ∧ 1 ≤ p ≤ #Σ.V(d) ∧ Σ.V(d)(p) = a}

This is the set of all (document, position) pairs that currently reference `a`. The set may be empty (the address exists in I-space but no document currently displays it), a singleton (one document at one position), or arbitrarily large (many documents transcluding the same content).

**IV13 (Referent Set Independence).** The referent set of an I-address is independent of any single document's editing:

    [DELETE position p from d  ⇒  refs'(a) = refs(a) \ {(d, p)}]

Deleting content from one document removes exactly one (document, position) pair from the referent set. All other references — in other documents, at other positions in the same document — are unaffected.

This is a direct consequence of IV10 (cross-document V-independence) and the fact that DELETE modifies only the target document's V-space. But stating it explicitly clarifies a crucial design property: *no document has privileged access to the I-address*. Even the document that originally allocated the I-address (the "home document") cannot destroy references from other documents. Permanence is system-wide, not owner-controlled.

Nelson is emphatic: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."

### The Empty Referent Set

When `refs(a) = ∅`, the I-address `a` has no current V-space references. But `a ∈ dom(Σ.I)` by IV1 — the content persists. This is the state Nelson calls "not currently addressable, awaiting historical backtrack functions."

Such addresses are *unreachable* through normal V-space traversal but *reachable* through I-space queries (if you know the address) or historical reconstruction (if a previous version's V-space referenced them). The system never garbage-collects I-space. Gregory confirms: "GRANTEXT content is never garbage collected. Once inserted into the Granfilade, it persists indefinitely."

---

## The Allocation–Mapping Ordering

IV0-PRES relied on a subtle ordering: when INSERT creates new content, the I-space allocation must *precede* (or be simultaneous with) the V-space mapping. If the V-space mapping were created first, there would be a (possibly transient) state violating IV0 — a V-position pointing to an unallocated I-address.

**IV14 (Allocation Before Mapping).** For any operation that extends both I-space and V-space, the I-space extension is established before (or atomically with) the V-space mapping:

    [a ∈ ran(Σ'.V(d)) \ ran(Σ.V(d))  ⇒  a ∈ dom(Σ'.I)]

That is: if a newly-appearing V-position references address `a`, then `a` is in the domain of `Σ'.I`. This is trivially satisfied by atomicity (IV12), but we state it separately because the implementation may have non-atomic internals even when the external transition is atomic.

Gregory confirms the ordering: `inserttextingranf` allocates fresh I-addresses in the granfilade *before* `insertpm` creates the POOM mappings. The I-addresses exist because they were "just allocated." The implementation achieves IV14 through sequencing within a single-threaded event loop, but any alternative implementation must achieve the same external guarantee: no client ever observes a V-position pointing to unallocated I-space.

Gregory also reveals a deeper fact about the implementation's trust model: `insertpm` does not *verify* that the I-addresses exist in the granfilade. It trusts the caller unconditionally. This is a convention — the caller is expected to have allocated the addresses first. If this convention is violated (through a bug or corruption), invalid V→I mappings are created silently, producing failures only at retrieval time. The abstract property IV14 is what the convention is *trying* to achieve; an alternative implementation might enforce it through runtime checks rather than convention.

---

## The Width Invariant

A technical observation from Gregory's evidence deserves formal treatment. In the implementation's POOM, each entry stores both a V-width and an I-width. At creation, these encode the same logical magnitude (the number of bytes in the span). But they use different tumbler exponents — V-width reflects insertion depth in the tumbler hierarchy, while I-width uses flat addressing.

Gregory reveals that after certain operations (specifically, crum extension when crums from different V-depths are combined), the V-width and I-width can *diverge* in their tumbler representation. The I-width remains authoritative for character count; the V-width represents tumbler-space extent, which is a different concept.

This is an implementation observation, not an abstract property. The abstract model has `Σ.V(d) : Nat⁺ → Addr`, which maps positions to addresses without any notion of "width." Width is a compression mechanism in the enfilade — a way to represent many individual mappings as a single (start, width) entry. The abstract model does not need it.

But the observation illuminates why IV6 (V→I is a total function) must be stated as an abstract property: the implementation's internal representation does not trivially guarantee it. The enfilade's width-based compression introduces the possibility of representational divergence. An alternative implementation that uses a different data structure (e.g., a flat array) would not face this issue, but would still need to satisfy IV6.

---

## The Two-Space Architecture as a Design Theorem

We have derived fourteen properties. But they all follow from a single architectural decision: *separate content identity from content arrangement*. If we had one space that served both purposes, we could not have:

- Permanence (because editing would modify content)
- Transclusion (because sharing would require duplication)
- Link survivability (because links would break when content moved)
- Version correspondence (because versions would have independent copies)
- Origin traceability (because addresses would change)

The I-space/V-space separation is not one feature among many — it is the architectural theorem from which all other guarantees follow. Nelson: "This separation is not a feature of Xanadu — it *is* Xanadu."

We can state this as a *separation theorem*:

*Theorem (SEP).* Given IV0 through IV14, the system satisfies:

(a) **Permanence**: content survives all V-space operations (by IV1, IV2, IV8)

(b) **Transclusion**: content sharing without duplication (by IV7, with COPY preserving I-addresses)

(c) **Link survivability**: links survive editing (by IV1, with links attaching to I-addresses)

(d) **Version correspondence**: structural comparison across versions (by shared I-addresses after CREATENEWVERSION)

(e) **Origin traceability**: every byte traceable to its creator (by IV2, IV3, with tumbler-encoded provenance)

(f) **Retrieval guarantee**: every visible position resolves (IV0 directly)

These are not independent features. They are consequences of the two-space architecture, which IV0 through IV14 formalize. An implementation that satisfies these properties — regardless of its data structures, its concurrency model, or its storage format — provides the guarantees Nelson's design requires.

---

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| IV-Σ1 | `Σ.I : Addr → Byte` is a partial function (I-space) | introduced |
| IV-Σ2 | `Σ.V(d) : Nat⁺ → Addr` is a total function per document-version (V-space) | introduced |
| IV-Σ3 | `Σ.docs` is the set of all document-versions | introduced |
| IV0 | Referential Integrity: every V-position maps to an allocated I-address | introduced |
| IV1 | Content Permanence: no operation removes an address from `dom(Σ.I)` | introduced |
| IV2 | Content Immutability: content at an I-address never changes | introduced |
| IV3 | Address Uniqueness: no I-address is ever assigned to different content | introduced |
| IV4 | Fresh Allocation: new I-addresses are outside the current domain | introduced |
| IV5 | Dense Contiguity: V-space is a gap-free sequence `{1, ..., n}` | introduced |
| IV6 | V→I Totality: each V-position maps to exactly one I-address | introduced |
| IV7 | I→V Multimap: the same I-address may appear at multiple V-positions | introduced |
| IV8 | V-operations Preserve I-space: editing never alters I-space content | introduced |
| IV9 | No I-space Mutation: I-space changes only through extension | introduced |
| IV10 | Cross-Document V-Independence: editing `d` does not affect `Σ.V(d')` for `d' ≠ d` | introduced |
| IV11 | Viewer Independence: `Σ.V(d)` is viewer-invariant | introduced |
| IV12 | Transition Atomicity: operations transition between IV0-satisfying states | introduced |
| IV13 | Referent Set Independence: deleting from one document removes exactly one reference | introduced |
| IV14 | Allocation Before Mapping: I-space extension precedes V-space mapping | introduced |
| MON-I | Monotonicity theorem: `dom(Σ.I)` is non-decreasing | introduced |
| IV0-PRES | Coherence theorem: all operations preserve IV0 | introduced |
| SEP | Separation theorem: IV0-IV14 imply permanence, transclusion, link survivability, correspondence, traceability, and retrieval | introduced |

---

## Open Questions

What invariants must the system maintain when I-space content is distributed across multiple storage nodes?

Must the allocation-before-mapping ordering (IV14) be strengthened to a durability guarantee — must the I-space write survive a crash before the V-space mapping becomes visible?

What must the system guarantee about the referent set `refs(a)` when `a` is unreferenced — must it be queryable, or only recoverable through exhaustive search?

Does the V-space contiguity invariant (IV5) extend to the version graph — must the set of versions itself be densely numbered, or can version identifiers have gaps?

What invariant must REARRANGE preserve beyond IV0, given that it permutes V-positions — must the permutation be specified in the operation, or may it be any permutation that maintains IV0?

What must the system guarantee about content at I-addresses that were allocated but never successfully mapped to any V-position (orphaned by a failed INSERT)?

Can two documents that independently INSERT identical byte sequences ever have their content share I-addresses, or must content identity be tied to the originating document?

What invariants must hold between the link index (spanfilade) and the V-space mappings (POOMs) when DELETE creates stale index entries that reference documents no longer containing the content?
