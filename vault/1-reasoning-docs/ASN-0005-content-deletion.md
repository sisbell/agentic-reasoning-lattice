# ASN-0005: Content Deletion

*2026-02-23*

We wish to understand what deletion means in a system where content is permanent. The word "delete" appears throughout Nelson's design, yet the system's foundational commitment — that every allocated address persists forever and content at that address never changes — seems to forbid the very thing the word denotes. The tension is real, and its resolution is one of the most revealing features of the architecture: deletion is an act of rearrangement, not an act of destruction. We develop this claim formally, derive its consequences for links and transclusions, characterize the sense in which deletion is reversible, and identify the residual effects that make the span index diverge from the live state.


## The state we need

We require a minimal vocabulary. Let the system state Σ contain:

- **ispace**: a partial function from addresses to content, `ispace : Addr ⇀ Content`. This is the permanent store. Once an address enters `dom.ispace`, it remains forever and its content never changes.
- **poom(d)**: for each document d, a function from virtual positions to addresses, `poom(d) : Pos → Addr`. This is document d's current arrangement — which content appears at which virtual position.
- **spanindex**: a relation recording which documents have contained which address ranges, `spanindex ⊆ Addr × DocId`. This index is append-only — entries are added but never removed.
- **links**: a set of link structures, each with three endsets (from, to, type), where endsets reference I-space address ranges.
- **journal**: an append-only sequence of operation records, `journal : Seq(OpRecord)`. Each record names the operation, the document, and the I-addresses affected. The journal is monotone — records are appended but never removed or modified: `(A i : 0 ≤ i < #journal : journal'.i = journal.i)` and `#journal' ≥ #journal`.

We write `dom.ispace` for the set of allocated addresses, `ispace.a` for the content at address `a`, `poom(d).p` for the I-address that document d maps virtual position p to, and `img(poom(d))` for the image of the mapping — the set of I-addresses that d currently references. We use primed names for the state after an operation.

A document's virtual stream has two subspaces: text (positions prefixed by subspace identifier 1) and links (positions prefixed by subspace identifier 2). DELETE operates on positions in one subspace and, as we shall establish, affects nothing outside that subspace.


## The permanence context

Before stating what DELETE does, we must be precise about what it cannot do. The system makes four permanence commitments that constrain every operation:

**P0 (Address irrevocability).** `(A a : a ∈ dom.ispace : a ∈ dom.ispace')` — no operation shrinks the set of allocated addresses.

**P1 (Content immutability).** `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — content at an address never changes.

**P2 (Index monotonicity).** `(A (a, d) : (a, d) ∈ spanindex : (a, d) ∈ spanindex')` — the span index never loses an entry.

**P3 (Journal monotonicity).** `(A i : 0 ≤ i < #journal : journal'.i = journal.i)` and `#journal' ≥ #journal` — the journal never loses or modifies an existing record.

These four properties hold for every operation, including DELETE. We do not prove them here — we take them as the context within which DELETE must be defined. The question is: what can DELETE mean if it must satisfy P0, P1, P2, and P3?


## DELETE as V-space surgery

The answer is that DELETE operates exclusively on V-space. It modifies a single document's arrangement, removing a contiguous span of virtual positions. What happens to the remaining positions depends on which subspace the deletion targets — a distinction we will develop carefully.

Let DELETE(d, p, w) denote the deletion of w positions starting at position p in document d. We require that the entire span [p, p ⊕ w) is confined to exactly one subspace of d — that is, there exists `s ∈ {text, link}` such that `[p, p ⊕ w) ⊆ subspace(d, s)`. The subspace s determines which effect clause applies. A deletion that straddles the text/link boundary is ill-formed: it would require the specification to simultaneously compact (DEL1) and not compact (DEL1a) the surviving positions, which is contradictory.

**DEL0 (I-space frame).** DELETE does not modify ispace:

  `dom.ispace' = dom.ispace` and `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

Nelson is direct: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." And the diagram on Literary Machines 4/9 labels the result: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" The phrase "not currently addressable" is precise — the bytes are no longer reachable through this document's virtual stream, but they remain at their permanent I-space addresses.

DEL0 is not a safety net or an optimization opportunity. It is forced by P0 and P1. Any operation that attempted to remove content from I-space would violate address irrevocability; any operation that attempted to overwrite it would violate content immutability. DELETE can modify only the mutable layer — V-space.

A corollary deserves explicit statement. Because I-space includes the content storage layer (what Gregory's implementation calls the granfilade), and DELETE does not modify I-space, **the allocation high-water mark is unaffected by DELETE**. After DELETE removes all text from a document, a subsequent INSERT still allocates fresh I-addresses continuing monotonically from the previous maximum. The counter advances; it never retreats. This follows directly from DEL0 — the content storage retains every previously allocated entry, and allocation queries this storage for the maximum.

**DEL1 (V-space effect — text subspace).** After DELETE(d, p, w) targeting the text subspace, the V-space mapping of document d loses the positions in [p, p ⊕ w) and surviving text positions beyond the deletion shift leftward by w. We specify this in two parts — the new domain, and the new mapping:

  *Domain (text subspace):* `dom.poom'(d) ∩ text = {q : q < p, q ∈ dom.poom(d)} ∪ {q ⊖ w : q ≥ p ⊕ w, q ∈ dom.poom(d)}`

  *Mapping:* `(A q : q < p ∧ q ∈ dom.poom(d) : poom'(d).q = poom(d).q)` and `(A q : q ≥ p ⊕ w ∧ q ∈ dom.poom(d) : poom'(d).(q ⊖ w) = poom(d).q)`

where `⊕` and `⊖` denote position arithmetic (tumbler addition and subtraction within a subspace). The first mapping clause says content before the deletion is untouched. The second says content after the deletion shifts left, preserving its I-address mapping. The domain definition captures what was previously a contradictory third clause: deleted positions disappear not by explicit exclusion but implicitly — they are simply absent from the union that defines the new domain. There is no position in [p, p ⊕ w) that appears in either branch of the union, and no shifted position collides with a preserved one, so the domain is well-defined.

Nelson describes this compaction as the inverse of INSERT's expansion: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text" — DELETE decreases them by the length of the deleted text.

**DEL1a (V-space effect — link subspace).** When DELETE targets the link subspace, the targeted link's V→I mapping is removed, but surviving links at higher V-positions do **not** shift leftward. Gaps persist:

  `(A q ∈ link_subspace(d) : q ∉ [p, p ⊕ w) ⟹ poom'(d).q = poom(d).q)`

Gregory's evidence is definitive. The V-shift arithmetic in the delete path subtracts the deletion width from each surviving entry's V-displacement. But an exponent guard in the subtraction prevents the operation when the subtrahend's exponent is smaller than the minuend's: link positions have depth-2 tumbler structure while link widths have depth-3, so the guard fires and returns the position unchanged. The golden test confirms: after deleting the link at position 2.2, the link at 2.3 remains at 2.3. The gap at 2.2 is permanent.

The asymmetry between text and link subspaces is architectural: text positions and text widths have matching exponent depth, so subtraction proceeds normally and gaps close. Link positions and link widths have mismatched depths, so the guard activates and gaps persist. Link V-positions are effectively stable after creation — they do not shift even when other links are deleted from the same document.


## The frame conditions

An operation is not specified until we state what it does NOT change. DELETE's frame conditions are as important as its effects.

**DEL2 (Cross-document isolation).** DELETE on document d does not affect any other document's POOM:

  `(A d' : d' ≠ d : poom'(d') = poom(d'))`

No operation on document d₁ may modify the V-space mapping of d₂ ≠ d₁. Gregory's implementation evidence confirms this with structural finality: the delete function takes a document handle and operates on that document's enfilade tree alone. No other document's tree is opened, read, or modified. The isolation is not a check — it is a consequence of the operation receiving exactly one document's data structure as input.

**DEL3 (Subspace confinement).** DELETE at a position in subspace s of document d shifts only V-positions in subspace s:

  `(A q ∈ other_subspace(d, s) : poom'(d).q = poom(d).q)`

A text deletion does not shift link positions. A link deletion does not shift text positions. Gregory confirms the mechanism: an exponent guard in the shift arithmetic makes cross-subspace subtraction a no-op. The abstract guarantee is that the document's two subspaces are independently arranged.

We observe that DEL3 and DEL1a together reveal a layered protection structure. The exponent guard serves double duty: it prevents cross-subspace shifts (DEL3), and it also prevents within-link-subspace shifts (DEL1a). The text subspace is the only context where V-compaction occurs normally.

**DEL4 (Span index frame).** DELETE does not remove entries from the span index:

  `(A (a, d) : (a, d) ∈ spanindex : (a, d) ∈ spanindex')`

This follows from P2, but we state it explicitly because it has a non-obvious consequence: after DELETE removes I-addresses from document d's POOM, the span index still claims that d "contains" those addresses. The forward direction of the correspondence breaks — the index over-approximates the current state. We return to this point below.

**DEL5 (Link structure frame).** DELETE does not modify any link structure:

  `(A L ∈ links : L ∈ links' ∧ endsets'(L) = endsets(L))`

Links are stored by I-space addresses in their endsets. DELETE operates on V-space. No operation that modifies only V-space can reach into the link structures, which live in I-space. The endset addresses of every link are unchanged after any DELETE.


## I-dimension invariance in surviving entries

The V-space compaction merits closer inspection. When DELETE shifts surviving entries leftward (in the text subspace), what exactly changes? The question matters because each entry in the POOM maps a V-range to an I-range, and we need to confirm that the shift is a pure V-translation for entries that survive intact and that partially-overlapping entries are split correctly.

**DEL6 (I-dimension invariance under compaction).** For every surviving POOM entry that is entirely outside the deleted range, the I-address mapping is preserved: the same byte of content appears at the shifted V-position as appeared at the original V-position. Only the V-displacement field is modified; the I-displacement and I-width are invariant:

  `(A entry ∈ surviving_intact(poom(d)) : entry'.iaddr = entry.iaddr ∧ entry'.iwidth = entry.iwidth)`

Gregory provides definitive evidence. The shift operation modifies `cdsp.dsas[V]` (V-displacement) and touches no other field. The three untouched fields are: I-displacement (the starting I-address), V-width (the virtual extent), and I-width (the I-address extent). The modification is a single subtraction — the deletion width is subtracted from the V-displacement of every entry beyond the deletion point. The I-address components are never read, never written, never passed as arguments to any arithmetic. DELETE's compaction is a pure V-translation that leaves all I-space information intact in surviving entries.

When a deletion partially overlaps an entry — removing only part of the content it maps — three geometries arise. Let the entry map V-range [v₁, v₂) to I-range [i₁, i₂), and let the deletion target [p, p ⊕ w). We require a structural property of POOM entries: within a single entry, the correspondence is positional — V-position `v₁ + k` maps to I-address `i₁ + k` for `0 ≤ k < v₂ − v₁` — and the widths are equal: `v₂ − v₁ = i₂ − i₁`. This is the span model: each entry represents a contiguous, order-preserving, unit-stride mapping from a V-range to an I-range. All three split formulas below depend on it.

**(a) Head removal** — the deletion covers the beginning of the entry: `p ≤ v₁` and `v₁ < p ⊕ w < v₂`. The first `k = (p ⊕ w) − v₁` positions of the entry are deleted. The surviving entry maps V-range [p ⊕ w, v₂) to I-range [i₁ + k, i₂). After V-compaction (shifting by w), the surviving entry appears at [p ⊕ w ⊖ w, v₂ ⊖ w) = [p, v₂ ⊖ w). The I-displacement is offset by k to skip the deleted head; the I-width decreases from (i₂ − i₁) to (i₂ − i₁ − k).

**(b) Tail removal** — the deletion covers the end of the entry: `v₁ < p` and `p ⊕ w ≥ v₂`. The last `k = v₂ − p` positions of the entry are deleted. The surviving entry maps V-range [v₁, p) to I-range [i₁, i₁ + (p − v₁)). No V-shift is needed for this fragment (it is entirely before the deletion point). The I-displacement is unchanged; the I-width decreases from (i₂ − i₁) to (p − v₁).

**(c) Middle split** — the deletion is strictly interior to the entry: `v₁ < p` and `p ⊕ w < v₂`. One entry produces two surviving fragments. The left fragment maps [v₁, p) → [i₁, i₁ + (p − v₁)), with I-displacement unchanged and width (p − v₁). The right fragment maps [p ⊕ w, v₂) → [i₁ + ((p ⊕ w) ⊖ v₁), i₂), with I-displacement offset by ((p ⊕ w) ⊖ v₁) and width (v₂ ⊖ (p ⊕ w)). After V-compaction, the right fragment shifts left by w to [p, v₂ ⊖ w). Middle split produces a net increase of one in the POOM entry count: one entry becomes two. The I-displacement for each fragment is computed independently from the original entry's I-displacement plus the appropriate offset.

In all three cases the fundamental invariant holds: for every surviving position q with pre-deletion mapping poom(d).q = a, the post-deletion state satisfies poom'(d).q' = a where q' is the compacted V-position. This is a *correspondence preservation* property — each surviving V-position maps to the same I-address it mapped to before, at a shifted V-coordinate — which is the conjunction of DEL1 (the mapping clauses for positions before and beyond the deletion) and DEL6's invariance of I-displacement fields. We do not claim bijectivity: the POOM is a function from positions to addresses, and two positions may map to the same I-address (as happens with intra-document transclusion). What DELETE preserves is not a bijection but the faithfulness of the mapping — no surviving position's I-address assignment changes. Gregory confirms that the split function produces new entries whose I-displacements equal the original plus the cut offset, independently for each fragment.

This is the formal expression of Nelson's dictum that deletion is rearrangement. The "arrangement" lives in the V-dimension of the POOM entries. The "content identity" lives in the I-dimension. DELETE modifies the former and leaves the latter untouched.


## Transclusion independence

We are now in a position to derive a property that the consultation answers confirmed empirically: deletion in one document cannot affect content visible in another.

**Theorem (Transclusion survives deletion).** If document B transcludes content at I-addresses A from document D, and D deletes that content, then B still references A and can resolve every address in A.

*Proof.* D's DELETE modifies only `poom(D)` (by DEL2, no other document's POOM is affected). The I-addresses in A remain in `dom.ispace` (by DEL0, DELETE does not modify ispace). Therefore `poom(B)` still maps V-positions to addresses in A, and `ispace.a` is well-defined for every `a ∈ A`. The transclusion is intact. ∎

The independence is structural, not temporal. It does not depend on the order of operations, the timing of access, or whether B "noticed" the deletion. B's POOM is a separate data structure from D's POOM. D's operation cannot reach B's state. This is the force of DEL2 — cross-document isolation is not a feature to be maintained but an architectural consequence of the operation's scope.

Nelson states it without qualification: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." And more broadly: "users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals."

A further consequence concerns version comparison. If two documents share I-addresses (as happens after CREATENEWVERSION, where both the original and the new version reference the same I-addresses), and one version subsequently deletes some shared content, a comparison of the two versions reflects the **current** state: overlap is reported as reduced. The comparison converts each document's current V-stream to I-addresses via its POOM, then intersects the results. Deleted content contributes no I-addresses from the deleting document's POOM, so it falls out of the intersection. Gregory confirms this directly — compare_versions operates on current POOM state, not on historical sharing relationships.


## Link survival

Links in the system attach to I-space addresses — to the bytes themselves, not to their virtual positions. Nelson calls this the "strap between bytes" design: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing."

We can now derive link survival after deletion:

**Theorem (Links survive deletion).** If link L has an endset referencing I-address a, and a is deleted from document d, then L's endset still references a and a remains a valid I-space address.

*Proof.* By DEL5, DELETE does not modify L's endsets. By DEL0, `a ∈ dom.ispace'`. Therefore `a` is still referenced by L and `ispace.a` is still defined. ∎

The derivation has exactly two premises: DELETE doesn't touch links (DEL5), and DELETE doesn't touch I-space (DEL0). No special-case link protection is needed.

What changes after deletion is not the link's validity but its *discoverability* through the document that performed the delete. Link discovery works by converting a document's V-spans to I-addresses and querying for links whose endsets overlap. After DELETE removes the V→I mapping for address a from document d, a query through d will not find L — there are no V-positions in d that map to a, so the query never generates a as a search term. But the link is still discoverable through any other document whose POOM maps to a.

This leads us to a taxonomy of link discoverability states.


## Ghost links and partial resolution

Discoverability is fundamentally a per-document property — resolution always proceeds through a specific document's POOM. We define the per-document classification first, then derive the global one.

**DEL7 (Link discoverability classification).** Let L be a link with endset referencing I-addresses A. Relative to a specific document d:

- **Live in d**: `(A a ∈ A : (E q : poom(d).q = a))` — every address in A is mapped by d's POOM. The entire endset is resolvable through d.
- **Partial in d**: `(E a ∈ A : (E q : poom(d).q = a)) ∧ (E a' ∈ A : ¬(E q : poom(d).q = a'))` — some addresses in A are mapped by d, others are not. The endset is partially resolvable through d.
- **Ghost in d**: `¬(E a ∈ A, q : poom(d).q = a)` — no address in A is mapped by d's POOM. The endset is not discoverable through d.

From the per-document classification we derive the global state:

- **Live (global)**: `(A a ∈ A : (E d, q : poom(d).q = a))` — every address in A is mapped by some document's POOM (not necessarily the same document for each address).
- **Partial (global)**: `(E a ∈ A : (E d, q : poom(d).q = a)) ∧ (E a' ∈ A : ¬(E d, q : poom(d).q = a'))` — some addresses in A are globally reachable, others are not.
- **Ghost (global)**: `¬(E a ∈ A, d, q : poom(d).q = a)` — no document's current POOM maps to any address in A. The link exists (its I-space structure is permanent) but is not discoverable through any document's V-space query.

We observe that a link can be globally live yet ghost in every individual document except one. The global classification aggregates over all documents; the per-document classification determines what a specific resolution query returns. A link can transition through these states as documents delete and re-introduce content. The transition is not a property of the link — which is immutable — but of the surrounding documents' arrangements.

**DEL8 (Endset resolution is a two-step filtering projection).** When an endset's I-addresses are resolved through a document's POOM, the resolution proceeds in two stages. First, the set of live positions is computed by filtering: each I-address in the endset is independently checked against the document's POOM, and only positions whose I-address maps to an endset member are retained:

  `resolve_addrs(L, endset, d) = {p ∈ dom.poom(d) : poom(d).p ∈ endset(L)}`

This yields a set of individual positions. Second, maximal contiguous subsequences of `resolve_addrs` are grouped into spans:

  `resolve(L, endset, d) = maximal_spans(resolve_addrs(L, endset, d))`

where `maximal_spans(S)` partitions S into the fewest contiguous runs — a set of spans `{[s₁, e₁), [s₂, e₂), ...}` such that each `[sₖ, eₖ)` is a maximal contiguous subset of S and the spans are pairwise disjoint.

The two-step decomposition makes each part independently verifiable: the filtering is correct if every position in the result maps to an endset address and no qualifying position is omitted; the grouping is correct if the resulting spans exactly cover `resolve_addrs` with no gaps within a span and no contiguous positions split across spans.

Gregory confirms this precisely. When a deletion removes the middle portion of a contiguous I-range from a document's POOM, endset resolution produces **two disjoint V-spans** for the surviving portions — not one contiguous span, and not an error. The resolution function walks the POOM looking for each I-address in the endset. For addresses that have been deleted, the POOM search returns NULL and the address is silently dropped. For addresses that survive, the POOM search returns V-positions, which are grouped into V-spans in the result. The output is exactly the set of V-spans that currently map to endset addresses.

The distinction between DEL7's per-document states is now precise in terms of DEL8's resolution. An endset that is live in d has `resolve_addrs(L, endset, d)` non-empty for every address in the endset — every I-address maps to some V-position in d, though the resulting V-positions may form multiple disjoint spans (editing can scatter originally contiguous I-addresses across non-contiguous V-positions). An endset that is partial in d resolves to a subset — `resolve_addrs` returns positions for some endset addresses but not others, and `resolve` groups the surviving positions into one or more spans. An endset that is ghost in d resolves to the empty set: `resolve_addrs(L, endset, d) = ∅`. In all three cases the operation succeeds; no error is raised.

Nelson acknowledges the partial case: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." The words "if anything is left at each end" describe the boundary between partial and ghost — the link becomes navigable when at least some bytes at each endset remain arranged in some document's V-space.


## The span index divergence

We now address a consequence of P2 (span index monotonicity) combined with DELETE's asymmetry. When content is placed in a document — by INSERT or COPY — the span index records the association between the I-addresses and the document:

  `(A a ∈ newly_placed : (a, d) ∈ spanindex')`

When content is later deleted from that document's POOM, the span index entry persists (by P2). This creates a divergence:

**DEL9 (Span index over-approximation).** After DELETE, the span index may contain entries `(a, d)` for which `a ∉ img(poom(d))`:

  `(E a, d : (a, d) ∈ spanindex ∧ ¬(E p : poom(d).p = a))`

The forward inclusion holds — every live reference is indexed:

  `(A d, a : (E p : poom(d).p = a) ⟹ (a, d) ∈ spanindex)`

We must verify that DELETE preserves this forward inclusion. Two cases arise:

*Case d' = d (the document being deleted from).* DELETE removes entries from `poom(d)`, which weakens the antecedent: fewer positions p satisfy `poom'(d).p = a`. For any `(a, d)` where the antecedent still holds — that is, some p still satisfies `poom'(d).p = a` — the entry `(a, d)` was in `spanindex` before the deletion (by the pre-DELETE forward inclusion) and remains in `spanindex'` (by P2/DEL4, the span index does not lose entries). So the forward inclusion holds for d after DELETE.

*Case d' ≠ d.* By DEL2, `poom'(d') = poom(d')`, so the antecedent is unchanged. By DEL4, `spanindex ⊆ spanindex'`, so any entry that satisfied the forward inclusion before still satisfies it after. The forward inclusion holds for all d' ≠ d.

Therefore DELETE preserves the forward inclusion. ∎

But the reverse does not hold:

  `(a, d) ∈ spanindex ⇏ (E p : poom(d).p = a)`

Gregory provides the structural explanation. The span index has insertion functions but no deletion functions. No `deletespanf` exists. When DELETE removes content from a document's POOM, no corresponding removal from the span index occurs. The index is write-only.

This means any query that consults the span index — such as FINDDOCSCONTAINING, which returns all documents associated with a set of I-addresses — returns a **superset** of the documents that currently contain those addresses:

**DEL10 (FINDDOCSCONTAINING is approximate).** The result of FINDDOCSCONTAINING(A) satisfies:

  `{d : (E a ∈ A, p : poom(d).p = a)} ⊆ FINDDOCSCONTAINING(A)`

but not necessarily equality. Documents that previously contained the I-addresses but have since deleted them appear as stale results.

The caller cannot distinguish stale from current results at query time. The distinction emerges only when attempting to resolve the I-addresses through each candidate document's POOM: a stale result yields an empty V-span set; a current result yields actual positions. This filtering — querying the span index for candidates, then validating each candidate against its POOM — is the specified access pattern. The span index provides breadth (which documents might be relevant); the POOM provides precision (which documents actually reference the content now).

We observe that this is not a defect. It is the price of P2. An index that could retract entries would be exact but would violate monotonicity. An append-only index is monotone but over-approximate. The architecture chooses monotonicity, consistent with the broader principle: the permanent layer never retracts a claim. The span index is a historical record — it answers "which documents have ever contained these addresses?" rather than "which documents currently contain them?"


## Weakest precondition: span-index forward inclusion

We now compute the weakest precondition for DELETE to preserve the span-index forward inclusion. This is the first non-trivial wp analysis in our treatment of DELETE, and it reveals what must hold before the operation for the index to remain a valid superset afterward.

Let the postcondition R be the forward inclusion:

  R: `(A d', a : (E q : poom'(d').q = a) ⟹ (a, d') ∈ spanindex')`

We seek `wp(DELETE(d, p, w), R)` — the weakest condition on the pre-state such that R holds after the deletion.

DELETE modifies two state components: `poom(d)` (removing entries and shifting survivors) and `journal` (appending a record). It does not modify `spanindex` (by DEL4), so `spanindex' = spanindex`. It does not modify `poom(d')` for `d' ≠ d` (by DEL2).

Substituting the post-state expressions into R, we split by whether `d' = d`:

For d' ≠ d: `poom'(d') = poom(d')` and `spanindex' = spanindex`, so the conjunct becomes `(A a : (E q : poom(d').q = a) ⟹ (a, d') ∈ spanindex)` — identical to the pre-state forward inclusion restricted to d'.

For d' = d: `poom'(d)` is obtained from `poom(d)` by removing entries in [p, p ⊕ w) and shifting survivors. Crucially, no new I-addresses enter `poom'(d)` that were not already in `poom(d)` — DELETE only removes and shifts, it does not introduce. Therefore `img(poom'(d)) ⊆ img(poom(d))`. The conjunct for d becomes: `(A a : (E q : poom'(d).q = a) ⟹ (a, d) ∈ spanindex)`. Since `img(poom'(d)) ⊆ img(poom(d))`, any a satisfying the antecedent also satisfies `(E q : poom(d).q = a)`, which by the pre-state forward inclusion gives `(a, d) ∈ spanindex = spanindex'`.

Combining both cases:

  `wp(DELETE(d, p, w), R) = (A d', a : (E q : poom(d').q = a) ⟹ (a, d') ∈ spanindex)`

That is, the weakest precondition is exactly the pre-state forward inclusion. The result is clean but not trivial: it depends on the observation that DELETE's POOM transformation only shrinks the image (removing or narrowing entries, never adding), so the antecedent can only weaken. If the forward inclusion held before, it holds after. No additional precondition is needed.

This contrasts with INSERT, where `wp(INSERT, R)` would require that the newly allocated I-addresses be added to the span index — a genuine strengthening of the precondition. DELETE's wp is the weakest possible precisely because it is a subtractive operation on V-space.


## A concrete example

We ground the specification by tracing a deletion through named values. Let document d have a text-subspace POOM with five positions mapping to five I-addresses:

  `poom(d).1 = a₁, poom(d).2 = a₂, poom(d).3 = a₃, poom(d).4 = a₄, poom(d).5 = a₅`

Suppose `ispace.aₖ = cₖ` for each k (five characters of content), and `spanindex` contains `{(a₁,d), (a₂,d), (a₃,d), (a₄,d), (a₅,d)}`. Further suppose a link L has `endset(L) = {a₂, a₃, a₄}`.

We apply DELETE(d, 3, 2) — deleting 2 positions starting at position 3 (removing positions 3 and 4, which map to a₃ and a₄).

**Checking DEL0 (I-space frame).** `dom.ispace' = dom.ispace` — all five addresses a₁ through a₅ remain allocated. `ispace'.a₃ = c₃` and `ispace'.a₄ = c₄` — the "deleted" content is unchanged. No content is destroyed.

**Checking DEL1 (V-space effect).** The new domain is `{q : q < 3, q ∈ dom.poom(d)} ∪ {q ⊖ 2 : q ≥ 5, q ∈ dom.poom(d)} = {1, 2} ∪ {5 ⊖ 2} = {1, 2, 3}`. The mapping: for positions before the deletion, `poom'(d).1 = a₁` and `poom'(d).2 = a₂` — unchanged. For positions at or beyond p ⊕ w = 5: `poom'(d).(5 ⊖ 2) = poom'(d).3 = poom(d).5 = a₅`. So `poom'(d) = {1 ↦ a₁, 2 ↦ a₂, 3 ↦ a₅}`. Position 3 is in the new domain (via the shift of old position 5), consistent with DEL1 — there is no contradiction because the domain is defined by the union, not by separate exclusion of [p, p ⊕ w).

**Checking DEL6 (I-dimension invariance).** The entries at positions 1 and 2 survived intact — their I-addresses are unchanged (a₁ and a₂ respectively). The entry originally at position 5 survived intact and shifted to position 3 — its I-address a₅ is preserved. No partial overlap occurred in this example (each position is a single-position entry), so no splitting was needed.

**Checking DEL9 (Span index over-approximation).** `spanindex' = spanindex` (by DEL4 — no entries removed). So `spanindex'` contains `(a₃, d)` and `(a₄, d)`, even though `a₃ ∉ img(poom'(d))` and `a₄ ∉ img(poom'(d))`. FINDDOCSCONTAINING({a₃}) returns {d}, but resolving a₃ through d's POOM yields no V-position — a stale result.

**Checking link state.** Link L's endset {a₂, a₃, a₄} is unchanged (DEL5). Resolving L through d: `resolve_addrs(L, endset, d) = {q ∈ dom.poom'(d) : poom'(d).q ∈ {a₂, a₃, a₄}} = {2}` (only position 2 maps to a₂; a₃ and a₄ have no V-mapping in d). The endset is *partial in d* (DEL7) — a₂ is mapped, a₃ and a₄ are not.

**Boundary case: DELETE(d, 1, 5) — deleting all content.** Every position is removed: `dom.poom'(d) = ∅`. Yet `dom.ispace' = dom.ispace` (DEL0 — all five addresses persist), `spanindex'` still contains all five (a, d) pairs (DEL4), and link L's endset is unchanged (DEL5). L's endset is now *ghost in d* (DEL7) — `resolve_addrs(L, endset, d) = ∅`. But if another document B transcludes a₂, then L's endset is *partial in B* (a₂ is mapped, a₃ and a₄ are not), and globally the endset is partial rather than ghost. Document d appears as a stale result in FINDDOCSCONTAINING queries for any of a₁ through a₅.


## Reversibility

We now address the central question: in what sense is deletion reversible? The answer has two parts, and the distinction between them is the deepest consequence of the I-space/V-space separation.

**DEL11 (Content persistence after deletion).** The content that was "deleted" still exists in I-space. Let A be the set of I-addresses removed from document d's POOM by DELETE. Then:

  `(A a ∈ A : a ∈ dom.ispace' ∧ ispace'.a = ispace.a)`

This follows from DEL0 (DELETE does not modify ispace). The "deleted" content is not gone — it is merely unreferenced by one document's current arrangement. The content is available for re-inclusion at any time.

But re-inclusion comes in two forms, and only one of them constitutes genuine reversal.

**DEL12 (INSERT does not reverse DELETE).** If content at I-addresses A is deleted from document d, and the user subsequently INSERTs text with the same character values, the new content receives fresh I-addresses B where `A ∩ B = ∅`:

  `(A a ∈ B : a ∉ dom.ispace)` (freshness of INSERT)

The document now displays text that looks the same. But every cross-document relationship is severed:

- Links whose endsets reference addresses in A do not discover the content at addresses B.
- Version comparison between d and any document sharing addresses in A finds no correspondence — A and B are disjoint address sets.
- Attribution at addresses in B identifies the current document as creator, not the original creator of content at A.
- The span index for addresses in A still points to d (a stale entry), while the span index for B is new.

INSERT after DELETE is not reversal. It is the creation of textually identical but structurally distinct content. The identity — as encoded in I-space addresses — is different.

**DEL13 (COPY reverses DELETE identity-preservingly).** If content at I-addresses A is deleted from document d, and some source S can supply references to A — either because S is a document whose POOM still maps to A, or because a link's endset provides the I-addresses of A directly as an I-span — then COPY from S to d restores the original I-addresses in d's POOM:

  `after COPY: (E q : poom'(d).q = a)` for each `a ∈ A` supplied by S

After this COPY, d's POOM again maps positions to the original I-addresses in A. The consequences are immediate:

- Links whose endsets reference A become discoverable through d again.
- Version comparison between d and other documents sharing A finds correspondence.
- Attribution at A identifies the original creator (encoded in the I-address).
- The content's identity is fully restored — as if the deletion had never occurred, from the perspective of address-based queries.

Gregory confirms both COPY sources. A POOM-based COPY extracts I-addresses from the source document's V→I mapping and deposits them unchanged in the target. But Gregory also reveals a second path: link endsets store I-addresses directly, and when a link's `sporgladdress` field is zero, the follow-link operation returns a pure I-span. The COPY operation accepts I-spans directly, bypassing V→I conversion entirely and retrieving content from the permanent store by I-address. This means a **ghost link** — one whose endset addresses are not in any document's POOM — can still serve as the source for identity-preserving restoration. The link itself remembers what the documents have forgotten.


## The sources of reversal

Given that DELETE is reversible via COPY, we ask: what must the system retain so that reversal is possible? The answer is more nuanced than initially appears.

**DEL14 (Reversal prerequisites).** For DELETE(d, p, w) to be identity-preservingly reversible, the system must retain:

(a) The I-space content at the deleted addresses — guaranteed by P0 and P1. The content was never destroyed.

(b) Some way to name the deleted I-addresses. Two sources are proven sufficient, either of which alone suffices:

  (i) A document whose POOM still maps to the deleted I-addresses — in the common case, a previous version of d (if one was explicitly created before the DELETE, since DELETE does not create versions automatically) or another document that transcludes the same content. Sufficiency: COPY from such a document extracts the I-addresses from the source's POOM and deposits them in d's POOM, restoring the original V→I mapping (DEL13).

  (ii) A link whose endset references the deleted I-addresses. Even if no POOM anywhere maps to those addresses (the link is fully ghost), the link's endset provides the I-addresses as an I-span, which COPY can consume directly to re-introduce the content. Sufficiency: the endset names exactly the I-addresses needed, and COPY accepts I-spans directly (DEL13).

The operation journal is a plausible third source — journal records name operations and affected I-addresses, and P3 guarantees their persistence — but we have not specified the precise content of a DELETE journal record. Whether the record contains enough detail to serve as a COPY source (minimally: the document id, the deleted I-address range, and sufficient information for COPY to consume) remains an open question. We do not list the journal among proven reversal sources.

(c) Nothing about links beyond what (b.ii) describes. Links remember themselves — their endset I-addresses are unchanged (DEL5). The moment the I-addresses re-enter a document's POOM, links are discoverable again through that document. No "link re-attachment" step is needed.

(d) Nothing about transclusion structure. The V→I mapping restored by COPY carries the transclusion structure implicitly — the I-addresses encode which document created the content (home document is readable from the address). Restoring the mapping restores the provenance.

The architecture does not need a special undo mechanism. The entire design is, in Nelson's phrase, built on an "append-only storage system" where "the file management system automatically keeps track of the changes and the pieces." Deletion is a change of view; the reality underneath is permanent. Reversal is a request for a previous view.


## Deletion is not versioning

We must be precise about the relationship between DELETE and the version mechanism, because conflating them leads to errors about what the system retains.

**DEL15 (DELETE does not create a version).** DELETE modifies the current document's POOM in place. It does not implicitly invoke CREATENEWVERSION. No new document identity is created; no snapshot of the pre-deletion state is automatically preserved as a separate version.

Nelson distinguishes the two mechanisms explicitly. DELETE "removes the given span from the given document" — an operation on the current state. CREATENEWVERSION "creates a new document with the contents of document <doc id>" — a separate, user-initiated action. There is no indication that DELETE implicitly invokes CREATENEWVERSION.

The pre-deletion state IS preserved, but not by versioning. It is preserved by the **append-only storage model**: the I-space content remains (P0, P1), the journal records the operation (P3), and the historical backtrack capability can reconstruct any prior arrangement. Nelson: "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen."

The practical consequence is sharp. If the user deletes content without first creating a version, then the COPY-from-previous-version path (DEL14(b.i)) requires that some other document happens to transclude the deleted I-addresses, or that a link provides them (DEL14(b.ii)). The system does not automatically create a convenient source for reversal. This is deliberate: Nelson's design leaves version creation in the user's hands. The append-only storage guarantees that reversal is *possible*; it does not guarantee that it is *convenient*.


## The trace of deletion

The system can distinguish content that was never present from content that was present but deleted. This distinction is not a feature bolted on — it is an inescapable consequence of the architecture.

**DEL16 (Distinguishability of "deleted" from "never present").** For any document d and set of I-addresses A:

  If A was once in `img(poom(d))` but is no longer, then:
  - `(A a ∈ A : a ∈ dom.ispace)` — the addresses exist in I-space (they were allocated when the content was created)
  - `(A a ∈ A : (a, d) ∈ spanindex)` — the span index records d's former association with A

  If A was never in `img(poom(d))`, then (assuming A was never placed in d):
  - It is possible that `a ∉ dom.ispace` (the addresses may never have been allocated)
  - `(a, d) ∉ spanindex` for all `a ∈ A` (the span index never recorded the association)

The combination of I-space permanence and span index monotonicity creates a permanent structural trace of deletion. The trace is not hidden — users can observe it through version comparison (SHOWRELATIONOF2VERSIONS reveals what content was shared between versions), through the span index (FINDDOCSCONTAINING reports the former association), and through content retrieval from earlier versions (historical backtrack surfaces the deleted content in its pre-deletion arrangement).

Nelson is explicit about this visibility: "Not currently addressable, awaiting historical backtrack functions, may remain included in other versions." The "DELETED BYTES" state is a recognized system category, not merely an internal bookkeeping detail.


## Deletion of links

The preceding analysis focused on text deletion — removing content from the text subspace of a document's V-space. We must also consider link deletion, and here we must correct a superficial symmetry.

Nelson's design treats deleted links and deleted bytes as occupying the same conceptual state. The Literary Machines 4/9 diagram labels both: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)" and, in parallel, "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)."

**DEL17 (Link deletion is V-space surgery on the link subspace).** Deleting a link from a document's link subspace removes the V→I mapping for the link's position within that document. The link's I-space structure (its endsets, type, content) is unaffected:

  `(A L : L.iaddr ∈ deleted_addrs : L ∈ links' ∧ endsets'(L) = endsets(L))`

A "deleted" link is not destroyed — it is removed from one document's link arrangement. The link's I-space structure persists permanently. Previous versions of the document (which include the link in their link subspace) can still resolve it. Other documents that reference the link are unaffected.

But the symmetry with text deletion has an important caveat: as established in DEL1a, link deletion does **not** compact surviving link positions. After a link is deleted from position 2.2, the link at position 2.3 stays at 2.3 — the gap persists. This contrasts with text deletion (DEL1), where surviving positions shift to close the gap. The two subspaces have different compaction behavior under DELETE.


## The economic frame

Nelson's system attaches royalty obligations to byte delivery from I-space. We observe, without developing a full economic model, that DELETE has no effect on these obligations.

**DEL18 (Economic obligations persist).** Because DELETE does not modify I-space (DEL0), and royalty attaches to delivery of I-space bytes, deletion changes nothing about royalty:

  Transclusions in other documents still deliver the original I-space bytes. Previous versions still deliver them. Historical backtrack still delivers them. In each case the original owner's cash register increments.

  Storage obligations also persist — the owner continues to bear storage costs for I-space content, since the bytes are never removed.

Nelson: "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." Since the bytes survive deletion, the royalty mechanism is unaffected.


## The boundary of irreversibility

The preceding analysis establishes that standard DELETE is always reversible within the system's normal operation. We should be honest about the edge cases where Nelson's own writing suggests limits.

**Published document withdrawal.** A published document may be withdrawn, but only through "lengthy due process." Even then, "the former version must remain on the network." Nelson does not specify whether withdrawal removes I-space content or merely blocks access to it. The latter interpretation is consistent with the architecture; the former would violate P0.

**Peremptory challenge.** For anonymous libelous content, Nelson states that "the affected individual must be able to effect removal of the materials by peremptory challenge." This is the strongest deletion language in the entire corpus. Whether "removal" means I-space destruction or access blocking is unspecified — and it represents a genuine tension with the permanence guarantee.

**Storage payment lapse.** Nelson requires that "ALL SERVICES MUST BE SELF-SUPPORTING." What happens when storage payment lapses is not specified. Content could become inaccessible ("dark") without being destroyed, or it could be truly removed. This is a gap in the specification.

These boundary cases share a structure: they are social or economic interventions that may override the architectural permanence guarantee. The architecture provides no mechanism for true I-space destruction; the question is whether the system's social layer is permitted to violate its own architectural invariants. Nelson does not resolve this tension.


## Formal summary

We collect the specification of DELETE. The operation `δ(Σ, DELETE(d, p, w)) = Σ'` is defined by:

*Precondition:* Position p is valid in document d's virtual stream, the span [p, p ⊕ w) lies within the existing content, and the entire span is confined to a single subspace of d. Formally: `(A q : p ≤ q < p ⊕ w : q ∈ dom.poom(d))`, the width w is nonzero, and `(E s ∈ {text, link} : [p, p ⊕ w) ⊆ subspace(d, s))`. The subspace s determines which effect clause applies: DEL1 for text, DEL1a for link.

*Effect on text subspace:* Document d's POOM is modified. The entries mapping positions in [p, p ⊕ w) to I-addresses are removed. Entries at positions beyond p ⊕ w are shifted leftward by w, with their I-address fields unchanged (DEL1, DEL6). Partial overlaps produce splits: head removal offsets the I-displacement, tail removal truncates the I-width, middle split produces two fragments with independently computed I-displacements (DEL6 cases a, b, c). The virtual stream contracts by w positions.

*Effect on link subspace:* The targeted link's V→I mapping is removed. Surviving links retain their original V-positions; no compaction occurs (DEL1a). Gaps persist permanently in the link subspace.

*Frame:* I-space is unchanged (DEL0). All other documents' POOMs are unchanged (DEL2). The other subspace of d is unchanged (DEL3). The span index is unchanged (DEL4). All link structures are unchanged (DEL5).

*Journal:* A record naming d, p, w, and the deleted I-addresses is appended to the journal. The journal's monotonicity (P3) ensures this record persists.

*Invariants preserved:* P0, P1, P2, P3, subspace independence, cross-document isolation, link permanence, span-index forward inclusion — all trivially or by the two-case argument in the span-index divergence section.

*Residual effects:* The span index retains entries for the deleted I-addresses associated with document d (DEL9). Queries consulting the span index may return d as a stale result (DEL10). Link discoverability through d is reduced; links whose endsets reference only deleted addresses become ghosts relative to d (DEL7, DEL8). Version comparison reflects the current state — overlap with other versions is reduced (Transclusion independence section).

*Reversibility:* Content persists in I-space (DEL11). Identity-preserving restoration is possible via COPY from any source that can name the deleted I-addresses — a document whose POOM still maps to them, or a link whose endset references them (DEL13, DEL14). The journal is a plausible but unproven third source, pending specification of DELETE record contents. Re-typing the same text via INSERT does not restore identity — it creates new addresses (DEL12). DELETE does not create versions; the availability of a convenient COPY source depends on explicit user action (DEL15).


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| DEL0 | DELETE does not modify ispace: `dom.ispace' = dom.ispace` and `ispace'.a = ispace.a` for all `a ∈ dom.ispace` | introduced |
| DEL1 | Text subspace DELETE: new domain is `{q < p} ∪ {q ⊖ w : q ≥ p ⊕ w}` (restricted to pre-state domain); mapping preserves I-addresses for positions before p, shifts positions at/beyond p ⊕ w leftward by w | introduced |
| DEL1a | Link subspace DELETE removes the targeted V→I mapping but does not shift surviving links; gaps persist permanently | introduced |
| DEL2 | DELETE on document d does not modify any other document's POOM: `poom'(d') = poom(d')` for all `d' ≠ d` | introduced |
| DEL3 | DELETE's effect is confined to the subspace of the deletion; the other subspace is unaffected | introduced |
| DEL4 | DELETE does not remove entries from the span index; follows from P2 | introduced |
| DEL5 | DELETE does not modify any link structure: all endsets are unchanged | introduced |
| DEL6 | DELETE's V-compaction modifies only V-displacement of intact entries; partial overlaps produce three cases — head removal (I-offset by k), tail removal (truncated I-width), middle split (two fragments with independent I-offsets) — all preserving correspondence (each surviving position's I-address is unchanged) | introduced |
| DEL7 | Link discoverability is per-document: live/partial/ghost in d depending on how many endset addresses d's POOM maps; global classification derived by existential quantification over all documents | introduced |
| DEL8 | Endset resolution is a two-step filtering projection: first collect positions `{p ∈ dom.poom(d) : poom(d).p ∈ endset(L)}`, then group maximal contiguous runs into spans | introduced |
| DEL9 | After DELETE, the span index may contain stale entries `(a, d)` where `a ∉ img(poom(d))` | introduced |
| DEL10 | FINDDOCSCONTAINING returns a superset of documents currently referencing the queried I-addresses; stale results require POOM validation | introduced |
| DEL11 | "Deleted" content persists in I-space; `a ∈ dom.ispace'` for all deleted addresses a | introduced |
| DEL12 | INSERT after DELETE creates fresh I-addresses, not the original ones; textual identity ≠ structural identity | introduced |
| DEL13 | COPY from a source naming the original I-addresses restores those addresses in the target's POOM; sources include documents with live POOM mappings or link endset I-spans | introduced |
| DEL14 | Reversal requires: persistent I-space (P0/P1), a way to name deleted I-addresses (proven sources: POOM of another document, link endset I-span), and nothing more; no link re-attachment or structure restoration needed; journal is a plausible but unproven third source | introduced |
| DEL15 | DELETE does not create a version; pre-deletion state preserved by append-only storage and journal, not by automatic versioning | introduced |
| DEL16 | "Deleted" is distinguishable from "never present": deleted addresses exist in I-space and appear in span index; never-present addresses need not | introduced |
| DEL17 | Link deletion is V-space surgery on the link subspace; the link's I-space structure is unaffected; unlike text deletion, no V-compaction occurs (DEL1a) | introduced |
| DEL18 | Economic obligations (royalty, storage) persist after deletion because they attach to I-space byte delivery, and I-space is unchanged by DELETE | introduced |
| Σ.journal | journal : Seq(OpRecord), append-only sequence of operation records naming operations, documents, and affected I-addresses | introduced |
| P0 | (context) Address irrevocability: `dom.ispace ⊆ dom.ispace'` for every operation | context |
| P1 | (context) Content immutability: `ispace'.a = ispace.a` for all `a ∈ dom.ispace`, for every operation | context |
| P2 | (context) Span index monotonicity: `spanindex ⊆ spanindex'` for every operation | context |
| P3 | Journal monotonicity: `journal'.i = journal.i` for all `0 ≤ i < #journal`, and `#journal' ≥ #journal` | introduced |


## Open Questions

Must the system provide a mechanism to query the span index for "current" containment (excluding stale entries), or is the two-step pattern (span index query followed by POOM validation) the only specified access method?

What must the system guarantee about the atomicity of DELETE when the deletion spans multiple POOM entries — must all entries be removed in a single observable step, or may intermediate states be visible?

Under what conditions, if any, may a system reclaim span index entries for I-addresses that are provably unreferenced by every document's POOM — and would such reclamation violate the specification or merely an implementation choice?

Must the system guarantee that at least one source for identity-preserving reversal (a POOM, a link endset, or a journal record naming the deleted I-addresses) always exists after any DELETE, or is it permissible for all sources to become unavailable?

What invariants must peremptory challenge satisfy — does "removal" mean I-space destruction (violating P0), access blocking (preserving P0 but breaking content availability), or something else?

What must the system guarantee about content availability when storage payment lapses — must content become "dark" (inaccessible but structurally intact) or may it be truly removed?

What invariants must the system maintain to ensure that the two-step filtering pattern (DEL10) is sound — specifically, must the span index be a superset at every observable state, or only at quiescent states?

Must the span index accumulation be bounded, or may it grow without limit as documents repeatedly INSERT and DELETE the same I-addresses via COPY cycles?

What must the system guarantee about V-position arithmetic when DELETE produces a position less than zero — must the precondition exclude such cases, or must the system handle negative V-positions as unreachable but structurally harmless state?

What must the system guarantee about POOM entry fragmentation after DELETE — may the number of entries in a document's POOM grow without bound through cycles of INSERT and DELETE, even if the document's content size remains constant?

What must a DELETE journal record contain — minimally, the document id, the deleted I-address range, and the original V-positions — for the journal to serve as a sufficient source for identity-preserving reversal via COPY?
