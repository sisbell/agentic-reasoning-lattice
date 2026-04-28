# ASN-0026: I-Space and V-Space

*2026-03-07*

We are looking for the invariants that connect permanent content storage to mutable document arrangement. The system maintains two address spaces and a mapping between them. Every guarantee the system offers — permanence, transclusion, attribution, version correspondence, link survivability — depends on specific properties of this mapping. We want to know exactly what those properties are and why they must hold.

---

## The Tension

A content system that permits editing faces an irreconcilable demand: content must be *permanent* (for citation, attribution, linking) and simultaneously *rearrangeable* (for editing, versioning, quotation). If content and arrangement live in the same space, editing destroys permanence and permanence prevents editing. The resolution is to separate them entirely.

We posit two spaces. **I-space** is the space of content identity — where bytes live permanently, addressed by tumblers (ASN-0001). **V-space** is the space of content arrangement — where a document's current presentation is defined as a mapping from virtual positions to I-space addresses. Nelson states the principle directly: "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations."

The critical phrase is "home locations." Content has a *home* — a permanent I-space address that encodes where, when, and by whom it was created. A document does not contain content; it *arranges references* to content that lives elsewhere. Nelson's glass-pane metaphor: "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely."

The glass pane is the V-space arrangement. The writing visible through the glass — wherever it originated — lives in I-space. We want to formalize this separation and derive its consequences.

---

## The State

Let `Sigma` denote the system state. We introduce three components.

**Sigma.I** `Sigma.I : Addr rightharpoonup Byte` is a partial function from I-space addresses (tumblers per ASN-0001) to content bytes. The domain `dom(Sigma.I)` is the set of all allocated I-addresses. Each I-address has the hierarchical form `N.0.U.0.D.0.E` where the fields encode node, user, document, and element (T4 from ASN-0001). The element field's first component identifies the subspace: `1` for text content. We restrict attention to text content in this ASN.

**Sigma.V** For each document `d`, `Sigma.V(d) : [1..n_d] -> Addr` is a total function from positions (positive naturals) to I-space addresses, where `n_d = |Sigma.V(d)|` is the document's current length. The domain is the dense interval `{1, ..., n_d}` with no gaps. Operations mutate `Sigma.V(d)` in place — INSERT adds mappings, DELETE removes them, REARRANGE reorders them. Nelson: "A document is really an evolving ONGOING BRAID." The braid is re-twisted, not replaced. CREATENEWVERSION is the explicit act that forks a new document `d'` with its own tumbler address and its own V-space, initially identical to `d`'s current state.

**Sigma.D** `Sigma.D` is the set of all documents that currently exist. The V-space function is defined exactly on this set: `Sigma.V(d)` is defined if and only if `d in Sigma.D`. Properties that quantify over `Sigma.D` — P2, P5, P7 — presuppose this connection.

*Document permanence (provisional).* We treat `Sigma.D` as monotonically growing: once a document enters `Sigma.D`, it remains. Nelson confirms that published documents are permanent by design — "It is in the common interest that a thing once published stay published" — and that tumbler addresses are never reused even when a document is withdrawn. Private documents may be withdrawn by their owner, and anonymous defamatory content may be removed by peremptory challenge, but in all cases the tumbler address remains permanently occupied and I-space content persists. The full lifecycle (withdrawal, "privashing," peremptory challenge) is deferred to a document lifecycle ASN. For the remainder of this ASN, P7's universal quantifier over `Sigma.D` assumes all documents in the pre-state survive the operation.

The asymmetry is already visible in the definitions. `Sigma.I` is global — one I-space for the entire system. `Sigma.V` is per-document — each document has its own mutable arrangement. And the relationship between them — that `Sigma.V(d)` points only into `Sigma.I` — is the central invariant we are after.

---

## The Axioms

We now state the properties that connect the two spaces. These are not implementation constraints but architectural commitments: any system claiming to implement this design must satisfy them.

### P0 — I-Space Immutability

Content at an I-address never changes:

    [a in dom(Sigma.I)  ==>  Sigma'.I(a) = Sigma.I(a)]

for any state transition `Sigma -> Sigma'`. Nelson: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." Once a byte is stored at address `a`, that byte is frozen forever.

P0 is what makes I-addresses meaningful as *identifiers*. If content could change at an address, then knowing the address would not tell you what content you would find. Attribution, link attachment, version correspondence — all depend on the identity between address and content being eternal.

### P1 — I-Space Monotonicity

No operation removes an address from `dom(Sigma.I)`:

    [a in dom(Sigma.I)  ==>  a in dom(Sigma'.I)]

for any transition `Sigma -> Sigma'`. I-space only grows. Combined with P0, this gives us: once content exists, it exists forever, unchanged.

*Corollary (NO-REUSE).* Address reuse is impossible. Suppose `a in dom(Sigma.I)` with `Sigma.I(a) = c`. By P1, `a in dom(Sigma'.I)` for every successor state. By P0, `Sigma'.I(a) = c`. The address is never freed, and its content never changes. There is no state in which `a` is available for reallocation. Nelson is explicit: allocation "goes forward. It never retreats."

### P2 — Referential Completeness

Every V-position maps to an allocated I-address:

    [d in Sigma.D /\ 1 <= p <= n_d  ==>  Sigma.V(d)(p) in dom(Sigma.I)]

There are no dangling references. No V-position points into the void. Nelson states this through the retrieval guarantee: content comes when you ask for it. A system in which some positions resolve to nothing violates this unconditionally.

P2 is not a defensive check — it is the load-bearing property from which retrieval works. And P1 makes P2 persistent: if a V-position mapped to a valid I-address before some operation, and the operation does not remove I-addresses, then the V-position still maps to a valid I-address afterward (provided the V-position itself survives the operation).

### P3 — Mapping Exactness

Let `RETRIEVE(d, p)` denote the byte the system delivers when position `p` of document `d` is requested. This is an operational function — it captures the system's actual delivery behavior, which is conceptually independent of the state model. P3 constrains it:

    [d in Sigma.D /\ 1 <= p <= n_d  ==>  RETRIEVE(d, p) = Sigma.I(Sigma.V(d)(p))]

The byte delivered is *exactly* the byte stored at the corresponding I-address. No operation in the system interposes a function `f =/= id` between the mapping and the delivery — no summarization, no excerpting within the byte, no encoding transformation.

This is not a vacuous constraint. One could imagine a system where a document arranges "transformed views" of content — say, excerpts or summaries computed from I-space. Nelson rejects this categorically. The FEBE protocol defines exactly five editing operations (INSERT, APPEND, COPY, DELETEVSPAN, REARRANGE). None performs transformation. Content is created (INSERT/APPEND), referenced (COPY), hidden (DELETE), or repositioned (REARRANGE). There is no sixth option of "transform."

Nelson: "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." The phrase "just as if" is critical — the bytes appear identically, not in altered form.

Why must this hold? Consider the correspondence operation, which compares two documents to find shared content. Correspondence is defined as `correspond(d_1, p_1, d_2, p_2) == Sigma.V(d_1)(p_1) = Sigma.V(d_2)(p_2)`. This definition assumes that shared I-address means identical content. If transformation were permitted — if document `d_1` showed a transformed version of the content at address `a` — then shared I-addresses would no longer prove correspondence. Two V-positions mapping to the same I-address could show different content. The correspondence guarantee collapses.

Similarly, attribution requires that the character you see at a V-position IS the character at the corresponding I-position. Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character." If transformation were allowed, you would trace back to different content than what you are seeing.

*Note.* The front end may *render* the same bytes differently — different fonts, zoom levels, audio playback speeds. This is display-level interpretation, not a change to the V-to-I mapping. The bytes flowing from back end to front end are exact. P3 constrains the delivery path, not the presentation.

### P4 — Creation-Based Identity

Content identity is determined by the act of creation, not by the value of the content. We derive this from the allocation discipline established in ASN-0001.

Two I-addresses `a` and `b` arise from *distinct allocation acts* when they were produced by separate applications of the allocator — whether by the same allocator at different times or by different allocators.

*Corollary (P4).* Distinct allocation acts produce distinct I-addresses.

*Derivation.* This is a restatement, in semantic terms, of GlobalUniqueness from ASN-0001: "No two distinct allocations, anywhere in the system, at any time, produce the same address." GlobalUniqueness covers all cases — same allocator (via T9), different allocators with non-nesting prefixes (via T10), and parent/child allocators with nesting prefixes (via T10a's sequential discipline). P4 lifts this address-level guarantee to its semantic meaning: creation-based identity.

The consequence is semantic: two users who independently type the identical passage receive different I-space addresses. The system does not recognize independently created identical content as sharing origin — because it doesn't. This is a fundamental semantic choice. The alternative — value-based identity, where identical byte sequences receive the same address — would make the system a content-addressable store (like a hash table). Nelson explicitly rejects this. Shared origin means "derived from the same act of creation," not "happens to contain the same bytes." The system preserves *provenance*, not *textual coincidence*.

Only transclusion (the COPY operation) produces shared I-space addresses between documents. CREATENEWVERSION also shares I-space addresses (the new document initially maps to the same I-content as the source). Independent creation never does.

We can state this as a table:

| Scenario | Same I-addresses? | Shared origin visible? |
|----------|-------------------|------------------------|
| B transcludes from A (COPY) | Yes | Yes — structural |
| B independently types same text | No | No — different origins |
| B creates version of A (CREATENEWVERSION) | Yes | Yes — structural |

P4 is what makes the I-address an *identity token* rather than a *content hash*. The system does not ask "do these bytes have the same value?" — it asks "are these the same bytes?" These are different questions, and only the latter supports attribution and provenance.

### P5 — Non-Injectivity (The Multimap Property)

The mapping `Sigma.V(d)` is not required to be injective. The same I-address may appear at multiple V-positions within a single document and across documents simultaneously:

    (E d_1, p_1, p_2 : p_1 =/= p_2 : Sigma.V(d_1)(p_1) = Sigma.V(d_1)(p_2))

is permitted (self-transclusion), and

    (E d_1, d_2, p_1, p_2 : d_1 =/= d_2 : Sigma.V(d_1)(p_1) = Sigma.V(d_2)(p_2))

is permitted (cross-document transclusion).

In the reverse direction — given an I-address `a`, what V-positions reference it? — the answer is a *set* of (document, position) pairs:

    refs(a) = {(d, p) : d in Sigma.D /\ 1 <= p <= n_d /\ Sigma.V(d)(p) = a}

This set may be empty (the address exists in I-space but no document currently displays it), a singleton, or arbitrarily large. The system must be able to compute this set — Nelson provides FINDDOCSCONTAINING for exactly this purpose: "This returns a list of all documents containing any portion of the material included by <vspec set>."

Gregory confirms the implementation's behavior: a single traversal of the POOM (the enfilade implementing V-to-I mapping) returns *all* V-positions for a given I-address, sorted by V-address. The search walks all qualifying subtrees and accumulates every matching leaf without deduplication or replacement. The multimap property is not a tolerated edge case but a designed-for capability.

P5 is the formal basis of transclusion. When content at I-address `a` appears at V-positions 5 and 47, both `Sigma.V(d)(5) = a` and `Sigma.V(d)(47) = a` hold simultaneously. The same content is referenced twice without duplication in I-space.

### I-Space Extension Classification (from P0, P1)

P0 and P1 together constrain every operation: existing I-content is preserved and no I-address is freed. The remaining question is which operations *extend* `dom(Sigma.I)`. We classify. For any operation `op`:

    Sigma'.I = Sigma.I +_ext fresh

where `+_ext` denotes extension: `Sigma'.I` agrees with `Sigma.I` on all of `dom(Sigma.I)` and may additionally be defined on new addresses `fresh` where `fresh intersection dom(Sigma.I) = emptyset`.

The freshness condition is not assumed — it follows from the allocation discipline. GlobalUniqueness (ASN-0001) establishes that no two distinct allocations, anywhere in the system, at any time, produce the same address. Every address in `dom(Sigma.I)` was produced by a prior allocation; every address in `fresh` is produced by a new allocation. By GlobalUniqueness, `fresh intersection dom(Sigma.I) = emptyset`.

The operations partition as follows:

- **DELETE, REARRANGE, COPY**: `fresh = emptyset`. These operations modify only V-space. Nelson: "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."
- **INSERT**: `fresh` is the set of newly allocated I-addresses for the inserted content.
- **CREATENEWVERSION**: `fresh = emptyset`. The new document shares the source's I-addresses.

Gregory provides striking confirmation from the implementation. REARRANGE modifies only V-displacements in the POOM — `ptr->cdsp.dsas[V]` is written, while `ptr->cdsp.dsas[I]` is never touched. No function in the REARRANGE code path reads or writes I-displacement fields. The asymmetry is architectural: V-space is the "editable" dimension; I-space represents the permanent provenance record.

### P7 — Cross-Document V-Independence

Each text-content operation modifies the V-space of at most one document in `Sigma.D`. We call that document the *write target* of the operation. For every pre-existing document that is not the write target, V-space is unchanged:

    (A d' : d' in Sigma.D /\ d' =/= target(op) : Sigma'.V(d') = Sigma.V(d'))

The quantifier ranges over `Sigma.D` — documents that exist in the pre-state. This is essential: CREATENEWVERSION creates a new document `d'` whose V-space transitions from undefined to defined. The new document is not in `Sigma.D`, so P7 does not assert its V-space is unchanged — it permits initialization. Every document that *existed* before the operation is protected.

The write targets for the five operations are: INSERT writes `d`; DELETE writes `d`; REARRANGE writes `d`; COPY writes the target document (the source is read-only); CREATENEWVERSION writes no existing document (it initializes a new one outside `Sigma.D`).

Each document's V-space is independent of every other's. Documents are coupled only through shared I-space content, never through shared V-space state.

Gregory confirms: DELETE operates exclusively on the source document's POOM. There is no cross-document notification, no reference-count decrement, no invalidation of remote mappings. After a COPY creates shared I-addresses between two documents, the documents are structurally independent — modifications to one cannot affect the other's mapping.

---

## The Lifecycle Asymmetry

We have stated the axioms. Now we derive their most striking consequence: I-space has no lifecycle management.

### P8 — No Reference Counting (Corollary of P1)

The persistence of content in I-space is unconditional — it does not depend on whether any V-space mapping currently references it. This follows directly from P1: `dom(Sigma.I)` never shrinks, regardless of `|refs(a)|`. Content persists even when `refs(a) = emptyset`.

Gregory confirms this emphatically from the implementation: there is no reference-count field in any POOM or granfilade data structure. DELETE frees the POOM crums that *reference* I-addresses but never touches the granfilade entries where I-content lives. There is no garbage-collection pass. There is no liveness predicate. The granfilade is append-only; I-addresses are eternal.

We state P8 explicitly because it is so contrary to the conventions of most systems. In conventional file systems, deleting the last reference to content frees the storage. In this system, content persists independently of reference count. Nelson calls this state "not currently addressable, awaiting historical backtrack functions, may remain included in other versions."

We observe that `refs(a) = emptyset` can only arise through deletion — because every content-creation operation (INSERT) simultaneously creates a V-space mapping to the new I-content. There is no mechanism to write directly to I-space without placing content in a document. Content is born referenced and may become unreferenced through subsequent deletions, but it never becomes non-existent.

The reachability paths for unreferenced content are:

- **Historical backtrack**: previous versions of the document whose V-space still maps to this content.
- **Transclusion**: other documents that transclude this content still reference it.
- **Links**: links whose endsets reference this I-address still resolve.
- **FINDDOCSCONTAINING**: the discovery operation can locate documents (including historical versions) that contain the content.

### The Deletion Asymmetry

DELETE deserves special treatment because it is the operation where the two spaces diverge most sharply.

After DELETE(d, p, k) removes positions `p` through `p+k-1` from document `d`:

1. `Sigma'.V(d)` no longer maps any position to the I-addresses that were at those positions.
2. Those I-addresses remain in `dom(Sigma'.I)` (by P1).
3. Their content is unchanged (by P0).
4. Other documents referencing the same I-addresses are unaffected (by P7).

The content has not been destroyed. It has been made *unreachable from this document*. This is not conventional deletion — it is the removal of a *view* of content, not the destruction of content itself.

*Observation.* DELETE is not the inverse of INSERT. If we INSERT content (allocating I-addresses `F`), then DELETE it, then INSERT identical bytes, the second INSERT allocates *fresh* I-addresses `F' =/= F` (by NO-REUSE). The V-space looks the same. The I-space identity is different. All links, transclusions, and correspondence relationships that attached to `F` do not attach to `F'`. The identity has been severed.

This is not a deficiency. It is a consequence of P4 (creation-based identity). The second creation is a *different act*, producing a *different identity*, even though the bytes are identical. The only way to restore a severed I-space identity is through COPY from a document that still references the original I-addresses.

---

## Operations Classification

The five text-content operations are classified by their effect on the two spaces. Full definitions are deferred to their respective operation ASNs.

| Operation | I-space effect | V-space effect |
|-----------|---------------|----------------|
| INSERT | Extends `dom(Sigma.I)` with fresh addresses | Inserts new mappings, shifts positions |
| DELETE | None | Removes mappings, shifts positions |
| REARRANGE | None | Permutes positions within document |
| COPY | None | Inserts mappings to existing I-addresses |
| CREATENEWVERSION | None | Creates new document sharing I-addresses |

---

## INSERT Preserves Surviving Mappings

We have stated the operations. Now we derive a property that connects INSERT's V-space effect to I-space identity: positions that survive an insertion retain their I-space addresses exactly.

### P9 — Mapping Preservation Under INSERT

When INSERT introduces `k` new positions at position `p` in document `d`:

*Precondition.* `1 <= p <= n_d + 1` and `k >= 1`. Position `p = 1` inserts before all existing content; `p = n_d + 1` appends after all existing content.

*Postcondition.* Let `fresh` be the set of `k` newly allocated I-addresses, with `fresh intersection dom(Sigma.I) = emptyset` (by the derivation in I-Space Extension Classification above). Then `|Sigma'.V(d)| = n_d + k` and:

    (A j : 1 <= j < p : Sigma'.V(d)(j) = Sigma.V(d)(j))                         (left of insertion)
    (A j : p <= j < p + k : Sigma'.V(d)(j) in fresh)                             (new positions)
    (A j_1, j_2 : p <= j_1 < j_2 < p + k : Sigma'.V(d)(j_1) =/= Sigma'.V(d)(j_2))  (injectivity on new)
    (A j : p <= j <= n_d : Sigma'.V(d)(j + k) = Sigma.V(d)(j))                   (right of insertion, shifted)

The first clause preserves positions left of the insertion point. The second clause establishes that new positions map to freshly allocated I-addresses — content that did not exist before the operation. The third clause requires the mapping from new positions to fresh addresses to be injective: no two new positions map to the same fresh address. Since `|fresh| = k` and the mapping is injective over `k` positions, it is a bijection — every fresh address appears at exactly one new position. This ensures no fresh address is born unreferenced. The fourth clause preserves positions at and right of the insertion point, shifted by `k`. Together with the length assertion `|Sigma'.V(d)| = n_d + k`, these four clauses fully specify the post-state of `Sigma'.V(d)`.

Why must this hold? Consider what happens if a surviving position changed its I-address — some position `j < p` that previously mapped to `a` now maps to `a' =/= a`. The content at position `j` would silently change identity. All links, transclusions, and correspondence relationships that attached to `a` at that position would be severed — not by the user's intent (which was to insert content at `p`), but by a side effect of the insertion. This would violate the guarantee that INSERT places new content between existing content without disturbing existing content.

Gregory confirms this from the implementation's `slicecbcpm` function. When the insertion point falls within a contiguous span, the split applies the V-space cut offset to both dimensions uniformly. A `1-story` invariant — enforced by a fatal error guard — ensures that V-width and I-width encode the same integer count for every mapping entry. The left portion retains the original I-start; the right portion's I-start is computed as `left_I_start + left_I_width` by element-wise addition. No I-address is lost, no I-address is reassigned.

*Observation (Representation Coalescing).* In implementations that represent `Sigma.V(d)` as a span table (mapping contiguous V-ranges to contiguous I-ranges), two adjacent entries may be coalesced into one when their I-ranges are exactly adjacent. Gregory confirms from the `isanextensionnd` function that the check uses field-by-field bitwise equality across all dimensions — both V and I must be exactly adjacent. This is a representational optimization: coalescing does not change the abstract function `Sigma.V(d)` and is therefore not a property of the abstract model.

---

## The Document as Mapping

We are now in a position to state a central claim: a document IS its V-to-I mapping. Two documents with the same mapping are, from the system's perspective, the same arrangement.

### P11 — Viewer Independence

The mapping `Sigma.V(d)` is a property of the document, not the viewer. The state model already encodes this by excluding a viewer parameter from the signature of `Sigma.V` — and it is important to recognize that this exclusion is a design constraint, not an accident.

*Protocol constraint (P11).* RETRIEVE takes a document identifier and a position (or V-span) and returns a deterministic result. No viewer, session, or context parameter exists in the protocol signature:

    RETRIEVE : (DocId, Pos) -> Byte

The back-end operation is a pure function of document and position. Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" — where "you" is universal.

Viewer experience may *diverge* at the front end — different fonts, different link filtering, different version choices. But the V-to-I mapping itself is viewer-invariant. This is architecturally necessary: if the mapping varied by viewer, "the home document of any specific word" would be viewer-dependent — an indeterminacy fatal to attribution and correspondence.

---

## Consequences

### Version Correspondence

When two versions share I-addresses (which they always do initially, by CREATENEWVERSION), correspondence is structurally computable:

    correspond(d_1, p_1, d_2, p_2)  ==  Sigma.V(d_1)(p_1) = Sigma.V(d_2)(p_2)

This requires P3 (exactness): shared I-address must mean identical content. It requires P0 (immutability): the content at the shared address cannot have changed between version creation and comparison. And it requires P4 (creation-based identity): if identity were value-based, correspondence could be spurious (two independently created but textually identical passages would appear to correspond when they have no genealogical relationship).

Nelson: "a facility that holds multiple versions of the same material is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same."

If CREATENEWVERSION duplicated content (allocating fresh I-addresses), correspondence would be impossible to compute. There would be no structural basis for determining which bytes are "the same." The entire version-comparison model depends on I-space sharing.

### Origin Traceability

Because I-addresses encode their origin structurally (the tumbler hierarchy per T4 from ASN-0001 includes node, user, document, and element fields), and because P0 means the address is the permanent identifier, the origin of any content is always recoverable:

    origin(content at V-position p in document d) = fields(Sigma.V(d)(p))

where `fields` extracts the hierarchical components of the I-address. The function is well-defined and computable from the address alone (T4). This is not metadata that can be stripped — it is the address itself. To retrieve content, the system must ask the home location. The connection between identity and origin is architectural.

### Link Survivability (Claim)

A link attaches to I-space addresses — not V-positions. When content is deleted from a document, only the V-to-I mapping is removed. The I-addresses persist (P1), the content persists (P0), and the link's endset addresses remain valid. We state this as a claim rather than a theorem because the link model is not formalized in this ASN.

What we can prove: if a link `L` has endset addresses in `S subset dom(Sigma.I)`, then after any sequence of operations producing `Sigma'`, we have `S subset dom(Sigma'.I)` by P1. The I-addresses the link references continue to exist. Whether the link remains *discoverable* depends on the link index, which is deferred.

Nelson: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing."

### Cross-Document Reference Stability

After COPY creates shared I-address references between two documents, the source document's subsequent operations cannot invalidate the target's mappings:

*Theorem (REF-STABILITY).* Let `Sigma` be a state where documents `d_s` and `d_t` share I-addresses (i.e., `(E a : a in range(Sigma.V(d_s)) intersection range(Sigma.V(d_t)))`). After any operation whose write target is `d_s` (and `d_t =/= d_s`), producing `Sigma'`:

    (A p : 1 <= p <= n_{d_t} : Sigma'.V(d_t)(p) in dom(Sigma'.I))

*Proof.* Since `d_t in Sigma.D` and `d_t` is not the write target, P7 gives `Sigma'.V(d_t) = Sigma.V(d_t)`. The non-target's V-space is unchanged. By P1, `dom(Sigma.I) subset dom(Sigma'.I)`. Every I-address referenced by `d_t` before the operation is still allocated afterward. By P2 on `Sigma` and P1, P2 holds on `Sigma'` for `d_t`.

Gregory confirms from implementation: there is no reference-counting or liveness check. DELETE operates on a single document's POOM only. The granfilade entries at shared I-addresses remain valid and retrievable. The target's RETRIEVEV resolves identically before and after the source's delete.

---

## The Empty Document and the Allocation Ordering

We briefly consider two boundary questions.

**Can a V-position reference unstored content?** No. Every V-position must satisfy P2 — it maps to an I-address in `dom(Sigma.I)`. There is no mechanism for a V-position to reference "future" or "pending" content. Nelson: native bytes are "found directly in storage"; non-native bytes are "obtained by front-end or back-end requests to their home locations." Both must exist.

However, the *addressing and linking layers* are more permissive. Link endsets can reference addresses where nothing is stored (ghost elements). Spans can designate empty ranges. But these are not V-space positions — they are references in the connection layer, which has different rules. The content layer and the connection layer have different referential requirements.

**Must I-space allocation precede V-space mapping?** Logically, yes — V-space is a mapping *into* I-space, so the codomain must exist before the mapping can reference it. Operationally, Nelson treats this as a single atomic command. The user provides text and a V-position; the system handles I-space commitment internally. The ordering is an implementation concern that Nelson deliberately hides behind the protocol abstraction.

---

## Initial State

The initial state `Sigma_0` is:

- `Sigma_0.I = emptyset` (no content stored)
- `Sigma_0.D = emptyset` (no documents exist)
- `Sigma_0.V` is undefined for all arguments (there are no documents)

Verification: P0 and P1 hold vacuously — no I-addresses exist, so the universally quantified implications `[a in dom(Sigma_0.I) ==> ...]` have empty antecedent. P2 holds vacuously — no documents and no positions. P3, P4, P5, P7, P9, P11 hold vacuously. P8 holds vacuously. The state `Sigma_0` satisfies all properties.

---

## Worked Example

Consider document `d` in state `Sigma` with `Sigma.V(d) = {1 -> a, 2 -> b, 3 -> c}` and `Sigma.I = {a -> 'H', b -> 'i', c -> '!'}`.

**INSERT "XY" at position 2.** The system allocates fresh I-addresses `f_1, f_2` with `Sigma'.I(f_1) = 'X'`, `Sigma'.I(f_2) = 'Y'`. The new V-mapping is:

    Sigma'.V(d) = {1 -> a, 2 -> f_1, 3 -> f_2, 4 -> b, 5 -> c}

Verify:

- **P0**: `Sigma'.I(a) = 'H' = Sigma.I(a)`, and similarly for `b`, `c` — all pre-existing content unchanged.
- **P1**: `{a, b, c} subset {a, b, c, f_1, f_2} = dom(Sigma'.I)` — domain grew, nothing removed.
- **P2**: Every V-position maps to an allocated I-address: `a, f_1, f_2, b, c in dom(Sigma'.I)`.
- **P9**: Left of insertion: `Sigma'.V(d)(1) = a = Sigma.V(d)(1)`. Right of insertion, shifted by 2: `Sigma'.V(d)(4) = b = Sigma.V(d)(2)`, `Sigma'.V(d)(5) = c = Sigma.V(d)(3)`.

**DELETE position 3** (removing the 'Y' at `f_2`):

    Sigma''.V(d) = {1 -> a, 2 -> f_1, 3 -> b, 4 -> c}

I-space: `f_2` remains in `dom(Sigma''.I)` with `Sigma''.I(f_2) = 'Y'` — unreferenced but persistent (P1). `refs(f_2) = emptyset`. The content is not destroyed; it is merely no longer arranged in this document.

---

## Preservation Obligation

The properties divide into four categories.

**State invariants** — must hold in every reachable state; the ASN defining each operation must verify preservation: P0 (I-immutability), P1 (I-monotonicity), P2 (referential completeness), P7 (cross-document V-independence).

**Operation postconditions** — constrain specific operations, not all reachable states: P9 (mapping preservation under INSERT). The postcondition binds only the operation it names; operations that do not perform insertion are not subject to P9.

**Structural permissions** — permitted by the model, not obligations to be preserved: P5 (non-injectivity). No operation can "violate" a permission. P5 states that the model allows multiple V-positions to share an I-address; any operation that produces such sharing is exercising a permitted capability.

**Architectural constraints** — verified once against the system architecture, not per-operation: P3 (constrains the retrieval path — no single operation can violate it unless the operation interposes a transformation function), P4 (follows from GlobalUniqueness — operations that do not allocate cannot violate it), P11 (constrains the RETRIEVE protocol signature — no single operation can violate it unless the operation introduces a viewer parameter).

**Corollaries** inherit preservation from their parent axioms: P8 and NO-REUSE follow from P1 (and P0 for NO-REUSE). If P1 is preserved by an operation, P8 and NO-REUSE are preserved automatically.

---

## Properties Introduced

*Note.* Labels P6 and P10 were removed during revision; the numbering gaps are intentional and the labels are not reserved.

| Label | Statement | Status |
|-------|-----------|--------|
| Sigma.I | `Sigma.I : Addr rightharpoonup Byte` — partial function, I-space content store | introduced |
| Sigma.V | `Sigma.V(d) : [1..n_d] -> Addr` — total function per document, mutable V-space arrangement | introduced |
| Sigma.D | `Sigma.D` — set of all documents | introduced |
| RETRIEVE | `RETRIEVE(d, p)` — operational delivery function for position `p` of document `d` | introduced |
| P0 | I-space immutability: content at an I-address never changes | introduced |
| P1 | I-space monotonicity: `dom(Sigma.I)` never shrinks | introduced |
| NO-REUSE | Address reuse is impossible (corollary of P0 + P1) | introduced |
| P2 | Referential completeness: every V-position maps to an allocated I-address | introduced |
| P3 | Mapping exactness: `RETRIEVE(d, p) = Sigma.I(Sigma.V(d)(p))` | introduced |
| P4 | Creation-based identity: distinct allocation acts produce distinct I-addresses (restatement of GlobalUniqueness) | introduced |
| P5 | Non-injectivity: same I-address may appear at multiple V-positions (multimap) | introduced |
| refs(a) | `{(d, p) : d in Sigma.D, 1 <= p <= n_d, Sigma.V(d)(p) = a}` — referent set of an I-address | introduced |
| +_ext | I-space extension classification: `Sigma'.I = Sigma.I +_ext fresh` (derived from P0, P1) | introduced |
| P7 | Cross-document V-independence: each operation modifies at most one document's V-space; all pre-existing non-targets are unchanged | introduced |
| P8 | No reference counting: I-content persists regardless of `|refs(a)|` (corollary of P1) | introduced |
| P9 | INSERT preserves surviving mappings: positions outside insertion retain I-addresses | introduced |
| P11 | Viewer independence: RETRIEVE protocol signature is `(DocId, Pos) -> Byte` with no viewer parameter | introduced |
| REF-STABILITY | Cross-document reference stability: source operations cannot invalidate target mappings | introduced |
| correspond | `correspond(d_1, p_1, d_2, p_2) == Sigma.V(d_1)(p_1) = Sigma.V(d_2)(p_2)` — version correspondence | derived |
| origin | `origin(content at p in d) = fields(Sigma.V(d)(p))` — origin traceability from I-address hierarchy | derived |

---

## Open Questions

Must the system guarantee that unreferenced I-content (`refs(a) = emptyset`) is reachable through a bounded number of historical backtracks, or is unbounded search permitted?

What invariants must the correspondence relation `correspond(d_1, p_1, d_2, p_2)` satisfy when both versions have been independently edited after forking — must correspondence remain decidable even after arbitrary edit sequences?

When CREATENEWVERSION shares I-addresses between source and copy, must the system preserve an explicit record of the derivation relationship, or is the shared I-content sufficient to reconstruct it?

What must the system guarantee about the ordering of I-addresses within a single document's V-space — can the V-to-I mapping be arbitrarily non-monotone, or does the allocation discipline impose partial ordering constraints?

Must the system provide a mechanism to enumerate all documents in `refs(a)` for a given I-address, or only to answer existence queries ("does any document reference this content")?

Under what conditions can `Sigma.V(d)` have length zero — must every document contain at least one V-position, or are empty documents well-formed states?

What must the system guarantee about the atomicity boundary of compound operations — if INSERT requires both I-allocation and V-mapping, must both succeed or neither, and what state does a partial failure leave?

What invariants must hold between the content index (which maps I-spans to documents for discovery) and the V-space mappings when V-space restructuring fragments the internal representation but does not change the logical I-span coverage?
