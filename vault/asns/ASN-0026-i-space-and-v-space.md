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

**Sigma.V** For each document-version `d`, `Sigma.V(d) : [1..n_d] -> Addr` is a total function from positions (positive naturals) to I-space addresses, where `n_d = |Sigma.V(d)|` is the document-version's current length. The domain is the dense interval `{1, ..., n_d}` with no gaps.

**Sigma.D** `Sigma.D` is the set of all document-versions that currently exist.

The asymmetry is already visible in the definitions. `Sigma.I` is global — one I-space for the entire system. `Sigma.V` is per-document — each document-version has its own arrangement. And the relationship between them — that `Sigma.V(d)` points only into `Sigma.I` — is the central invariant we are after.

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

The V-to-I mapping delivers content without transformation:

    [Sigma.V(d)(p) = a  ==>  content delivered at position p is Sigma.I(a)]

The byte at V-position `p` is *exactly* the byte stored at I-address `a`. There is no function `f` applied between the mapping and the delivery — no summarization, no excerpting within the byte, no encoding transformation. The mapping is identity at the content level.

This is not a vacuous statement. One could imagine a system where a document arranges "transformed views" of content — say, excerpts or summaries computed from I-space. Nelson rejects this categorically. The FEBE protocol defines exactly five editing operations (INSERT, APPEND, COPY, DELETEVSPAN, REARRANGE). None performs transformation. Content is created (INSERT/APPEND), referenced (COPY), hidden (DELETE), or repositioned (REARRANGE). There is no sixth option of "transform."

Nelson: "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." The phrase "just as if" is critical — the bytes appear identically, not in altered form.

Why must this hold? Consider the correspondence operation, which compares two versions to find shared content. Correspondence is defined as `correspond(d_1, p_1, d_2, p_2) == Sigma.V(d_1)(p_1) = Sigma.V(d_2)(p_2)`. This definition assumes that shared I-address means identical content. If transformation were permitted — if document `d_1` showed a transformed version of the content at address `a` — then shared I-addresses would no longer prove correspondence. Two V-positions mapping to the same I-address could show different content. The correspondence guarantee collapses.

Similarly, attribution requires that the character you see at a V-position IS the character at the corresponding I-position. Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character." If transformation were allowed, you would trace back to different content than what you are seeing.

*Note.* The front end may *render* the same bytes differently — different fonts, zoom levels, audio playback speeds. This is display-level interpretation, not a change to the V-to-I mapping. The bytes flowing from back end to front end are exact. P3 constrains the mapping, not the presentation.

### P4 — Creation-Based Identity

Content identity is determined by the act of creation, not by the value of the content:

    [a =/= b  ==>  the content at a and the content at b are distinct identities]

regardless of whether `Sigma.I(a) = Sigma.I(b)` (the bytes happen to be the same). Two users who independently type the identical passage receive different I-space addresses. The system does not recognize them as sharing origin — because they don't. They were created independently.

This is a fundamental semantic choice. The alternative — value-based identity, where identical byte sequences receive the same address — would make the system a content-addressable store (like a hash table). Nelson explicitly rejects this. Shared origin means "derived from the same act of creation," not "happens to contain the same bytes." The system preserves *provenance*, not *textual coincidence*.

Only transclusion (the COPY operation) produces shared I-space addresses between documents. CREATENEWVERSION also shares I-space addresses (the new version initially maps to the same I-content as the source). Independent creation never does.

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

### P6 — V-Operations Preserve I-Space

No operation that modifies V-space alters I-space content:

    [(A a : a in dom(Sigma.I) : Sigma'.I(a) = Sigma.I(a))]

for any V-space operation (DELETE, REARRANGE, COPY) applied to any document. Nelson: "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."

INSERT is the only operation that extends I-space (allocating new addresses for inserted content). But even INSERT satisfies P6 for all *pre-existing* I-addresses. We can state this precisely. For any operation `op`:

    Sigma'.I = Sigma.I +_ext fresh

where `+_ext` denotes extension: `Sigma'.I` agrees with `Sigma.I` on all of `dom(Sigma.I)` and may additionally be defined on new addresses `fresh` where `fresh intersection dom(Sigma.I) = emptyset`. For DELETE, REARRANGE, and COPY, `fresh = emptyset`. For INSERT, `fresh` is the set of newly allocated I-addresses.

Gregory provides striking confirmation from the implementation. REARRANGE modifies only V-displacements in the POOM — `ptr->cdsp.dsas[V]` is written, while `ptr->cdsp.dsas[I]` is never touched. No function in the REARRANGE code path reads or writes I-displacement fields. The asymmetry is architectural: V-space is the "editable" dimension; I-space represents the permanent provenance record.

### P7 — Cross-Document V-Independence

An operation on document `d` does not modify `Sigma.V(d')` for any `d' =/= d`:

    [op applied to d  ==>  (A d' : d' =/= d : Sigma'.V(d') = Sigma.V(d'))]

Each document's V-space is independent of every other's. Documents are coupled only through shared I-space content, never through shared V-space state.

Gregory confirms: DELETE operates exclusively on the source document's POOM. There is no cross-document notification, no reference-count decrement, no invalidation of remote mappings. After a COPY creates shared I-addresses between two documents, the documents are structurally independent — modifications to one cannot affect the other's mapping.

---

## The Lifecycle Asymmetry

We have stated the axioms. Now we derive their most striking consequence: I-space has no lifecycle management.

### P8 — No Reference Counting

The persistence of content in I-space is unconditional — it does not depend on whether any V-space mapping currently references it:

    [a in dom(Sigma.I)  ==>  a in dom(Sigma'.I)]

regardless of the cardinality of `refs(a)`. Content persists even when `refs(a) = emptyset`.

Gregory confirms this emphatically from the implementation: there is no reference-count field in any POOM or granfilade data structure. DELETE frees the POOM crums that *reference* I-addresses but never touches the granfilade entries where I-content lives. There is no garbage-collection pass. There is no liveness predicate. The granfilade is append-only; I-addresses are eternal.

This is a consequence of P0 + P1, but it deserves explicit statement because it is so contrary to the conventions of most systems. In conventional file systems, deleting the last reference to content frees the storage. In this system, content persists independently of reference count. Nelson calls this state "not currently addressable, awaiting historical backtrack functions, may remain included in other versions."

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

The content has not been destroyed. It has been made *unreachable from this specific document version*. This is not conventional deletion — it is the removal of a *view* of content, not the destruction of content itself.

*Observation.* DELETE is not the inverse of INSERT. If we INSERT content (allocating I-addresses `F`), then DELETE it, then INSERT identical bytes, the second INSERT allocates *fresh* I-addresses `F' =/= F` (by NO-REUSE). The V-space looks the same. The I-space identity is different. All links, transclusions, and correspondence relationships that attached to `F` do not attach to `F'`. The identity has been severed.

This is not a deficiency. It is a consequence of P4 (creation-based identity). The second creation is a *different act*, producing a *different identity*, even though the bytes are identical. The only way to restore a severed I-space identity is through COPY from a document that still references the original I-addresses.

---

## Operations and the Mapping

We now define the five text-content operations in terms of their effect on the V-to-I mapping, and verify that each preserves the axioms.

### INSERT(d, p, b_1 ... b_k)

Insert `k` bytes at position `p` in document `d`.

*Preconditions.* `d in Sigma.D`, `k >= 1`, `1 <= p <= n_d + 1`.

*Effect on I-space.* Allocates fresh addresses `F = {f_1, ..., f_k}` with `F intersection dom(Sigma.I) = emptyset`, and defines `Sigma'.I(f_i) = b_i` for `1 <= i <= k`. All pre-existing I-content is unchanged (P6).

*Effect on V-space.* The new mapping `Sigma'.V(d)` has domain `{1, ..., n_d + k}`:

    Sigma'.V(d)(q) = Sigma.V(d)(q)       for 1 <= q < p         (unshifted)
    Sigma'.V(d)(q) = f_{q-p+1}           for p <= q <= p+k-1    (new content)
    Sigma'.V(d)(q) = Sigma.V(d)(q-k)     for p+k <= q <= n_d+k  (shifted right)

*Frame.* `Sigma'.V(d') = Sigma.V(d')` for all `d' =/= d` (P7).

*P2 verification.* New positions: `Sigma'.V(d)(q) = f_{q-p+1} in F subset dom(Sigma'.I)` by construction. Shifted positions: `Sigma'.V(d)(q) = Sigma.V(d)(q-k) in dom(Sigma.I) subset dom(Sigma'.I)` by P2 on `Sigma` and P1. Unshifted: same reasoning.

Nelson specifies that this is operationally atomic — I-space allocation and V-space mapping happen as one indivisible step. Gregory confirms the ordering: fresh I-addresses are allocated (via `inserttextingranf`) before the POOM mapping is created (via `insertpm`). If the V-space mapping were created first, there would be a transient state violating P2. The logical dependency flows from the definition: V-space is a *mapping into* I-space, so the codomain must be established before the mapping.

### DELETE(d, p, k)

Remove `k` bytes starting at position `p` from document `d`.

*Preconditions.* `d in Sigma.D`, `k >= 1`, `1 <= p`, `p + k - 1 <= n_d`.

*Effect on I-space.* None. `Sigma'.I = Sigma.I`.

*Effect on V-space.* The new mapping `Sigma'.V(d)` has domain `{1, ..., n_d - k}`:

    Sigma'.V(d)(q) = Sigma.V(d)(q)       for 1 <= q < p         (below deletion)
    Sigma'.V(d)(q) = Sigma.V(d)(q+k)     for p <= q <= n_d - k  (closed gap)

Positions `p` through `p+k-1` are removed; positions above shift down by `k`.

*Frame.* `Sigma'.V(d') = Sigma.V(d')` for all `d' =/= d`. `Sigma'.I = Sigma.I`.

*P2 verification.* Below deletion: unchanged, valid by P2 on `Sigma`. At or above `p`: `Sigma'.V(d)(q) = Sigma.V(d)(q+k)` where `q+k <= n_d`, so `Sigma.V(d)(q+k) in dom(Sigma.I) = dom(Sigma'.I)`.

Gregory reveals an important structural point: when DELETE removes a V-span that covers only part of an existing mapping entry, the entry is split. The split exactly partitions the underlying I-span with no gaps or overlaps. The surviving portions retain their I-addresses — the I-displacement of the left portion is preserved verbatim, while the right portion's I-displacement is recomputed as `original_I_start + split_offset`. This partitioning preserves P2 because every surviving V-position still maps to the same I-address it mapped to before the deletion.

### REARRANGE(d, c_1, c_2, c_3)

Swap two adjacent regions in document `d`. (We present the three-cut form; the four-cut form is analogous.)

*Preconditions.* `d in Sigma.D`, `1 <= c_1 < c_2 < c_3 <= n_d + 1`.

Let `a = c_2 - c_1` (width of region 1), `b = c_3 - c_2` (width of region 2).

*Effect on I-space.* None. `Sigma'.I = Sigma.I`.

*Effect on V-space.* The mapping `Sigma'.V(d)` has domain `{1, ..., n_d}` (length preserved):

    Sigma'.V(d)(q) = Sigma.V(d)(q)              for 1 <= q < c_1           (before)
    Sigma'.V(d)(q) = Sigma.V(d)(q + a)          for c_1 <= q < c_1 + b    (region 2)
    Sigma'.V(d)(q) = Sigma.V(d)(q - b)          for c_1 + b <= q < c_3    (region 1)
    Sigma'.V(d)(q) = Sigma.V(d)(q)              for c_3 <= q <= n_d       (after)

REARRANGE is a permutation of V-positions. It changes the *order* in which I-addresses appear in V-space but does not change *which* I-addresses are in the mapping. The multiset `{Sigma.V(d)(q) : 1 <= q <= n_d}` is preserved.

*Frame.* `Sigma'.V(d') = Sigma.V(d')` for all `d' =/= d`. `Sigma'.I = Sigma.I`.

*P2 verification.* Every position `q` in `Sigma'.V(d)` maps to some position `q'` in `Sigma.V(d)` with `1 <= q' <= n_d`. By P2 on `Sigma`, `Sigma.V(d)(q') in dom(Sigma.I) = dom(Sigma'.I)`.

Gregory's implementation evidence is particularly illuminating here. REARRANGE modifies `cdsp.dsas[V]` (V-displacements) but never touches `cdsp.dsas[I]` (I-displacements). A comprehensive audit of the codebase finds that no function in the REARRANGE path reads or writes I-displacement fields. The I-dimension is structurally invisible to REARRANGE. This is the architectural expression of P6: I-space is inert under V-operations.

### COPY(d_s, p_s, k, d_t, p_t)

Copy `k` bytes from source document `d_s` to target document `d_t`. This is transclusion: no new I-addresses are allocated.

*Preconditions.* `d_s, d_t in Sigma.D`, `k >= 1`, `1 <= p_s`, `p_s + k - 1 <= n_{d_s}`, `1 <= p_t <= n_{d_t} + 1`. Self-transclusion (`d_s = d_t`) is permitted.

*Effect on I-space.* None. `Sigma'.I = Sigma.I`.

*Effect on V-space (target).* Let `m = n_{d_t}`. The new mapping `Sigma'.V(d_t)` has domain `{1, ..., m + k}`:

    Sigma'.V(d_t)(q) = Sigma.V(d_t)(q)                for 1 <= q < p_t           (unshifted)
    Sigma'.V(d_t)(q) = Sigma.V(d_s)(p_s + q - p_t)    for p_t <= q <= p_t+k-1    (transcluded)
    Sigma'.V(d_t)(q) = Sigma.V(d_t)(q-k)              for p_t+k <= q <= m+k      (shifted)

*Frame.* Source is unchanged: if `d_s =/= d_t`, `Sigma'.V(d_s) = Sigma.V(d_s)`. If `d_s = d_t`, the copied positions reference the I-addresses that existed in `Sigma.V(d_s)` before the shift — the copy reads from the pre-operation state.

*P2 verification.* Transcluded positions: `Sigma'.V(d_t)(q) = Sigma.V(d_s)(p_s + q - p_t) in dom(Sigma.I) = dom(Sigma'.I)` by P2 on `Sigma`. Shifted and unshifted: same reasoning as INSERT.

COPY is where P5 (non-injectivity) becomes operationally relevant. After COPY, the target document's V-space contains I-addresses that also appear in the source document's V-space. The same I-content is now arranged in two places without duplication. Gregory confirms that no overlap checking occurs during COPY — the system unconditionally accepts the insertion of I-addresses that already exist at other V-positions, because the multimap property is by design.

The contrast with INSERT is precise:

| | INSERT | COPY |
|---|---|---|
| I-space effect | Extends `dom(Sigma.I)` | None |
| Source of I-addresses | Freshly allocated | Existing (from source) |
| V-space structure | Identical insertion mechanics | Identical insertion mechanics |

Both operations use the identical V-space insertion path. The only difference is the source of I-addresses.

### CREATENEWVERSION(d)

Create a new document-version `d'` from document `d`.

*Preconditions.* `d in Sigma.D`.

*Effect on I-space.* None (for text content). `Sigma'.I = Sigma.I`.

*Effect on V-space.* `Sigma'.V(d')(p) = Sigma.V(d)(p)` for all `1 <= p <= n_d`. The new version initially has the same V-to-I mapping — no content is duplicated.

*Frame.* `Sigma'.V(d) = Sigma.V(d)`. All other document-versions unchanged.

Nelson: "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." All versions reference the same I-space content pool; they differ only in their V-space arrangements.

Gregory reveals that CREATENEWVERSION does not clone the internal tree structure. The source POOM's contents are read as I-spans (via `specset2ispanset`) and re-inserted into a fresh POOM (via `insertpm`). Adjacent entries with contiguous I-addresses may be coalesced into fewer entries. The resulting POOM is *semantically equivalent* (same V-to-I mapping) but may differ structurally (different tree height, different entry count). This confirms that the abstract mapping is the specification; the tree is mechanism.

---

## The Exactness of Partition

We have stated the operations. Now we derive a property that connects V-space structure to I-space structure: when a mapping entry is split, the split exactly partitions the underlying I-span.

### P9 — Partition Exactness

When an INSERT operation splits an existing V-to-I mapping entry at position `p`, producing two entries covering `[v_1, v_1 + w_L)` and `[v_1 + w_L + k, v_1 + w_L + k + w_R)` in V-space, the I-space spans of the two entries satisfy:

    (a)  I_L = [i_1, i_1 + w_L)          (left portion)
    (b)  I_R = [i_1 + w_L, i_1 + w)      (right portion)
    (c)  w_L + w_R = w                    (total coverage preserved)
    (d)  I_L intersection I_R = emptyset  (no overlap)
    (e)  I_L union I_R = [i_1, i_1 + w)  (no gap)

where `w` is the original entry's width and `i_1` is its I-start.

Why must this hold? Consider what happens if the split introduced a gap — some I-address `a` that was reachable before the split but is reachable through neither portion afterward. This would mean that a V-position previously mapping to `a` now maps to nothing or to a different I-address. But the bytes at positions below and above the insertion point must retain their original I-addresses (this is the *meaning* of INSERT: new content is placed between existing content; existing content is preserved). A gap in the I-partition would silently destroy a mapping — violating P2.

Similarly, an overlap would mean two portions claim the same I-address, creating duplicate mappings where only one existed before — a problem for accounting and consistency.

Gregory confirms the exact partition property from the implementation's `slicecbcpm` function. The split applies the V-space cut offset to both dimensions uniformly. A `1-story` invariant — enforced by a fatal error guard — ensures that V-width and I-width encode the same integer count for every mapping entry. The left portion's width becomes `localcut` in both V and I dimensions; the right portion's width becomes `original_width - localcut` in both. The right portion's I-start is computed as `left_I_start + left_I_width` by element-wise addition. This is algebraically exact: `left.I_width + right.I_width = original_width`, and `right.I_start = left.I_start + left.I_width`. No gap, no overlap, by construction.

### P10 — Coalescing Requires Exact Adjacency

When two mapping entries are candidates for merging (coalescing into a single entry), the system requires that the second entry's I-start equals the first entry's I-end exactly:

    coalesce(entry_1, entry_2)  requires  I_start(entry_2) = I_start(entry_1) + I_width(entry_1)

There is no tolerance for "close but not strictly adjacent." Gregory confirms this from the `isanextensionnd` function, which performs field-by-field bitwise equality of tumbler representations. The check uses `lockeq` across all dimensions — both V and I must be exactly adjacent. An I-address that is `existing_I_end + 2` (a gap of one) causes the check to fail, and a new entry is created instead.

P10 is an abstract property, not an implementation detail: any system that coalesces mappings must preserve the exact I-span coverage. Approximate coalescing would introduce either gaps (lost mappings) or overlaps (duplicate mappings), violating P9.

---

## The Document as Mapping

We are now in a position to state a central claim: a document-version IS its V-to-I mapping. Two document-versions with the same mapping are, from the system's perspective, the same arrangement.

### P11 — Viewer Independence

The mapping `Sigma.V(d)` is a property of the document-version, not the viewer:

    (A viewers u_1, u_2 : Sigma.V(d) as seen by u_1 = Sigma.V(d) as seen by u_2)

The back-end operation RETRIEVEV takes a document-version and V-spans; it returns the corresponding I-space content deterministically. No viewer parameter exists in the protocol. Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" — where "you" is universal.

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

*Theorem (REF-STABILITY).* Let `Sigma` be a state where documents `d_s` and `d_t` share I-addresses (i.e., `(E a : a in range(Sigma.V(d_s)) intersection range(Sigma.V(d_t)))`). After any operation on `d_s` producing `Sigma'`:

    (A p : 1 <= p <= n_{d_t} : Sigma'.V(d_t)(p) in dom(Sigma'.I))

*Proof.* By P7, `Sigma'.V(d_t) = Sigma.V(d_t)`. The target's V-space is unchanged. By P1, `dom(Sigma.I) subset dom(Sigma'.I)`. Every I-address referenced by `d_t` before the operation is still allocated afterward. By P2 on `Sigma` and P1, P2 holds on `Sigma'` for `d_t`.

Gregory confirms from implementation: there is no reference-counting or liveness check. DELETE operates on a single document's POOM only. The granfilade entries at shared I-addresses remain valid and retrievable. The target's RETRIEVEV resolves identically before and after the source's delete.

---

## The Empty Document and the Allocation Ordering

We briefly consider two boundary questions.

**Can a V-position reference unstored content?** No. Every V-position must satisfy P2 — it maps to an I-address in `dom(Sigma.I)`. There is no mechanism for a V-position to reference "future" or "pending" content. Nelson: native bytes are "found directly in storage"; non-native bytes are "obtained by front-end or back-end requests to their home locations." Both must exist.

However, the *addressing and linking layers* are more permissive. Link endsets can reference addresses where nothing is stored (ghost elements). Spans can designate empty ranges. But these are not V-space positions — they are references in the connection layer, which has different rules. The content layer and the connection layer have different referential requirements.

**Must I-space allocation precede V-space mapping?** Logically, yes — V-space is a mapping *into* I-space, so the codomain must exist before the mapping can reference it. Operationally, Nelson treats this as a single atomic command. The user provides text and a V-position; the system handles I-space commitment internally. The ordering is an implementation concern that Nelson deliberately hides behind the protocol abstraction.

---

## Preservation of the Invariant System

We have defined five operations and eleven properties. We should verify that the invariant system is jointly satisfiable and preserved.

*Theorem (PRES).* If `Sigma` satisfies P0 through P11, and `Sigma -> Sigma'` is a valid operation, then `Sigma'` satisfies P0 through P11.

The per-operation verification of P2 was given above with each operation definition. P0 and P1 hold because no operation modifies existing I-space content or removes I-addresses (verified by inspecting each operation's I-space effect: INSERT extends, all others leave unchanged). P3 holds because no operation introduces transformation — the mapping at every V-position is either unchanged, freshly allocated (INSERT), or directly copied (COPY/CREATENEWVERSION). P4 holds because INSERT allocates fresh addresses (by NO-REUSE) and COPY shares existing ones — no operation creates false identity between independently created content. P5 is a non-constraint (no injectivity requirement to violate). P6, P7, and P8 hold by the frame conditions stated with each operation. P9 is preserved because the only operation that splits entries (INSERT via gap-making) applies the exact partition arithmetic. P10 is preserved because the adjacency check is applied at every coalescing opportunity. P11 is structural — the back-end protocol has no viewer parameter in any state.

---

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Sigma.I | `Sigma.I : Addr rightharpoonup Byte` — partial function, I-space content store | introduced |
| Sigma.V | `Sigma.V(d) : [1..n_d] -> Addr` — total function per document-version, V-space arrangement | introduced |
| Sigma.D | `Sigma.D` — set of all document-versions | introduced |
| P0 | I-space immutability: content at an I-address never changes | introduced |
| P1 | I-space monotonicity: `dom(Sigma.I)` never shrinks | introduced |
| NO-REUSE | Address reuse is impossible (from P0 + P1) | introduced |
| P2 | Referential completeness: every V-position maps to an allocated I-address | introduced |
| P3 | Mapping exactness: V-to-I delivers content without transformation | introduced |
| P4 | Creation-based identity: identity is by creation event, not by byte value | introduced |
| P5 | Non-injectivity: same I-address may appear at multiple V-positions (multimap) | introduced |
| refs(a) | `{(d, p) : d in Sigma.D, 1 <= p <= n_d, Sigma.V(d)(p) = a}` — referent set of an I-address | introduced |
| P6 | V-operations preserve I-space: editing never alters existing I-space content | introduced |
| P7 | Cross-document V-independence: editing `d` does not affect `Sigma.V(d')` for `d' =/= d` | introduced |
| P8 | No reference counting: I-content persists independently of `|refs(a)|` | introduced |
| P9 | Partition exactness: splitting a mapping entry exactly partitions the I-span | introduced |
| P10 | Coalescing exactness: merging entries requires exact I-address adjacency | introduced |
| P11 | Viewer independence: `Sigma.V(d)` is viewer-invariant | introduced |
| REF-STABILITY | Cross-document reference stability: source operations cannot invalidate target mappings | introduced |
| PRES | All operations preserve P0 through P11 | introduced |

---

## Open Questions

Must the system guarantee that unreferenced I-content (`refs(a) = emptyset`) is reachable through a bounded number of historical backtracks, or is unbounded search permitted?

What invariants must the correspondence relation `correspond(d_1, p_1, d_2, p_2)` satisfy when both versions have been independently edited after forking — must correspondence remain decidable even after arbitrary edit sequences?

When CREATENEWVERSION shares I-addresses between source and copy, must the system preserve an explicit record of the derivation relationship, or is the shared I-content sufficient to reconstruct it?

What must the system guarantee about the ordering of I-addresses within a single document's V-space — can the V-to-I mapping be arbitrarily non-monotone, or does the allocation discipline impose partial ordering constraints?

Must the system provide a mechanism to enumerate all documents in `refs(a)` for a given I-address, or only to answer existence queries ("does any document reference this content")?

Under what conditions can `Sigma.V(d)` have length zero — must every document-version contain at least one V-position, or are empty documents well-formed states?

What must the system guarantee about the atomicity boundary of compound operations — if INSERT requires both I-allocation and V-mapping, must both succeed or neither, and what state does a partial failure leave?

What invariants must hold between the content index (which maps I-spans to documents for discovery) and the V-space mappings when V-space restructuring fragments the internal representation but does not change the logical I-span coverage?
