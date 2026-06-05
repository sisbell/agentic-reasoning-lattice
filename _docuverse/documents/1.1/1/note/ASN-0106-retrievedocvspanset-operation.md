# ASN-0106: The Combined Read — RETRIEVEDOCVSPANSET Over a Span-Set

*2026-06-04*

## The problem

We are asked what happens when several spans of one document are read *together*. The word "together" is doing real work. We could imagine reading each span by a separate request and laying the answers side by side ourselves. The question is whether the system, asked for a *set* of spans in one act, must return something more than the loose concatenation we could have assembled by hand — and if so, what that surplus is, and what it must be faithful to.

The named operation is RETRIEVEDOCVSPANSET. Nelson's gloss (4/68) is terse: it "returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." Read narrowly, that is the single act of asking a document for its own extent. But the same machinery answers the general question — *give me these several regions of this document, as one* — and it is the general act we must specify, with the document-extent reading falling out as the instance where the requested spans are the full extents of each subspace.

We must establish four things. *What* is returned. What *relationship* the returned fragments bear to one another and to the document's arrangement. What the combined act *reveals* that span-by-span reading would not. And what *invariants* the operation must maintain across the combined result. We will find that all four answers turn on a single design commitment: the result is a structured object that retains addresses, ordered by the document's arrangement, not a flattened stream of content.

We work over the foundations. A document `d` carries an arrangement `M(d) : T ⇀ T` (ASN-0036, ASN-0047) mapping V-positions to I-addresses; `subspace(v) = v₁` projects the subspace identifier (ASN-0036), with `s_C = 1` for text and `s_L = 2` for links (ASN-0047). A span `σ = (s, ℓ)` denotes `⟦σ⟧ = {t : start(σ) ≤ t < reach(σ)}` (ASN-0053). A mapping block `β = (v, a, n)` denotes `⟦β⟧ = {(v + k, a + k) : 0 ≤ k < n}` (ASN-0058), with V-extent `V(β)` and I-extent `I(β)`.

---

## What is returned

We must first reject the loosest possible answer. Nelson is explicit that the unit of designation, when one wants several separated regions exactly, is the **span-set**: "if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans" (4/25). The request travels as one set, and the answer travels as one set. So the result is not a bag of disconnected pieces; it is a single structured collection.

But a collection *of what*? Here we depart from a naive reading. If the operation returned only content bytes — a flat concatenation — then much of what we are about to claim would be impossible, because bytes carry no address. Gregory's evidence is decisive on this point: the content-retrieval path discards I-addresses before the result leaves the back end, so two distinct regions returning identical text are indistinguishable from one region read twice. RETRIEVEDOCVSPANSET is the *other* kind of operation. It returns **spans**, each of which is an address-bearing description: a region of the document's arrangement together with the content identity it points to.

We therefore take the returned object to be a sequence of mapping blocks. Given a span `σ` over `d`, let `f = M(d)|⟦σ⟧` be the arrangement restricted to the requested positions. By ASN-0058 (C1a, M11, M12) this restriction admits a *unique maximally-merged* block decomposition; list its blocks in increasing V-start order and call the list `blocks(d, σ)`. For a span-set `Σ = ⟨σ₁, …, σₚ⟩` define

> **read(d, Σ) = blocks(d, σ₁) ⌢ blocks(d, σ₂) ⌢ … ⌢ blocks(d, σₚ)**,

the concatenation of the per-span decompositions. Each block `(v, a, n)` records simultaneously *where in the document* the fragment sits (its V-start `v`) and *what content* it names (its I-start `a`). This is the surplus the combined act delivers and the loose concatenation cannot: a structure in which both coordinates survive.

The canonical RETRIEVEDOCVSPANSET of 4/68 is the instance `read(d, Σ_full)` where `Σ_full = ⟨σ_text, σ_link⟩` designates the full V-extent of each subspace. By the subspace argument below the result is then exactly two blocks — the text extent and the link extent — which is precisely Nelson's "number of characters of text and number of links." We record this as a claim (R0) but spend our reasoning on the general act, of which it is a special case.

**Frame.** The combined read is a pure query. It reads `M(d)` and `Σ`; it allocates no address, changes no arrangement, and writes nothing back: `C' = C`, `L' = L`, `(A d' :: M'(d') = M(d'))`, `Σ` unchanged. Every claim below is about a *state observed*, not a state transformed. We label this **R-FRAME**.

---

## The relationship among fragments, and to the arrangement

### Ordering authority

Within a single span's contribution, the blocks are listed by ascending V-start. This is not an arbitrary convenience; it expresses Nelson's claim that the order is a property of the document's *arrangement* (the Vstream), never of storage: "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document" (4/11). The arrangement is the authority. A returned fragment occupies the ordinal position the document assigns it, regardless of where its content physically lives or which other document it was transcluded from.

The subtlety is *inter*-span order. The document's arrangement gives a single canonical order to all of `dom(M(d))`; but the request enumerated its spans in some sequence that need not respect that order. We resolve the tension by appeal to ASN-0053's normalized form. Say `Σ` is **normalized** when its spans are sorted and separated (N1, N2 of ASN-0053): `start(σᵢ) < start(σᵢ₊₁)` and `reach(σᵢ) < start(σᵢ₊₁)`. For normalized `Σ`, the per-span concatenation order coincides with V-order, and so

> **R-ORDER.** For normalized `Σ`, `read(d, Σ)` is globally ordered by V-position, and this order is the document's arrangement order — independent of how the request happened to enumerate the spans.

This is the abstract content of Nelson's repeated insistence (4/25, 4/30) that the request *selects* content but does not *redefine* its arrangement: "There is no choice as to what lies between; this is implicit in the choice of first and last point." An alternative implementation that delivered a normalized request in request-order rather than arrangement-order would still have to sort, because the arrangement is canonical; the only freedom is whether to require the caller to normalize first or to normalize internally.

### Dual traceability

Each fragment is traceable along two independent axes, and both must survive into the result. This is forced by the block structure and by the foundations.

> **R-TRACE.** For every block `(v, a, n) ∈ read(d, Σ)` and every `0 ≤ k < n`: the pair `(v + k, a + k)` satisfies `M(d)(v + k) = a + k` (ASN-0058 B3), so `v + k` is a genuine V-position of `d` and `a + k ∈ dom(C)` is its content identity (ASN-0036 S3).

The first axis (`v`) places the fragment in the whole — "you always know where you are" (2/40). The second axis (`a`) identifies its content by origin; by ASN-0058 M16a/M16b every I-address in a block shares one origin document, so each fragment carries, intrinsically, the home of its content — "you can at once ascertain the home document of any specific word or character" (2/40). Neither axis is metadata bolted on after the fact; both are constitutive of the block. A result that dropped `v` could not be ordered; a result that dropped `a` could not reveal correspondence (below). RETRIEVEDOCVSPANSET keeps both precisely because it returns spans, not bytes.

### Subspace partition

The returned fragments do not mix text and links within a single run. The reason is structural, not stylistic. By T7 (ASN-0034, subspace disjointness) two element-level addresses differing in their subspace component are distinct, and `subspace(v) = v₁` (ASN-0036) makes the subspace identifier the leading component of every V-position. By the lexicographic order T1 (ASN-0034), `s_C = 1 < 2 = s_L`, so every text position precedes every link position. A block cannot straddle the boundary: a contiguous run `(v + k)` shares all components above the last (ASN-0058 M-int), in particular `subspace(v + k) = subspace(v)`. Hence

> **R-SUBSPACE.** Every block of `read(d, Σ)` lies wholly in one subspace; in the arrangement order the text blocks precede the link blocks; no block spans both subspaces.

This is exactly the shape Gregory found: the operation reports the text extent and the link extent as *separate* spans, never one bounding value across both — and indeed a single bounding value across the two subspaces would be meaningless, because the gap between `s_C` and `s_L` is filled by no content of either kind. The two-VSpec result of 4/68 is this claim at the full-extent instance.

---

## What the combined act reveals

We now reach the heart of the question. A span read alone tells you only "from here to there"; its contents are "implicit in the choice of first and last point" (4/25). It says nothing about what lies outside it. Reading spans *together* turns the silence between and across them into information. Three things become legible that no single span could show.

### Gaps and adjacency

Consider two adjacent blocks `β, β'` in the result with `β` preceding `β'`. Either `reach`-of-`β`'s V-extent equals `start`-of-`β'`'s — they abut, no document position lies between them — or it does not, and the V-positions strictly between are *unrequested content the document holds but the request excluded*. By ASN-0053's classification (SC) this distinction is decidable from the boundaries alone. So:

> **R-GAP.** From `read(d, Σ)` one may decide, for each consecutive pair of fragments, whether they abut in the arrangement or are separated by document content the request omitted; the size and location of each omission is recoverable from the block boundaries.

A lone span cannot expose this, because a lone span has no neighbour to abut or be separated from. The gap is "an active exclusion" (Nelson, on "including nothing else", 4/25) — and it is only visible once two fragments are placed side by side with their V-coordinates intact. This is why the surplus of the combined act is real: the relationship *between* fragments is information the fragments do not individually carry.

### Correspondence — shared content within the document

Here is the deepest reveal, and the one that justifies returning addresses rather than bytes. Two distinct V-positions of a document may map to the *same* I-address — self-transclusion, internal sharing. The arrangement permits this (ASN-0058 M13): `(E d, a :: |{v : M(d)(v) = a}| > 1)`. Content identity in Xanadu is by *origin* (shared I-address), not by value (4/10–4/11); two regions that merely read alike are not "the same content" unless they trace to one I-address.

Now observe what the combined read does. If span `σᵢ` covers one such V-position and `σⱼ` covers the other, then `read(d, Σ)` contains two blocks whose I-extents overlap. By ASN-0058 M14a such blocks *cannot* be merged — a shared I-extent defeats I-adjacency — so both survive in the result, each displaying the shared I-address `a`. The reader, comparing the two blocks' I-coordinates, sees that the regions are the same content, not coincidentally identical content.

> **R-CORR.** Distinct V-positions of `d` that share an I-address are exposed by `read(d, Σ)` as distinct blocks carrying that common I-address; this sharing is legible only when both positions are read together, and only because the result retains I-addresses.

This is precisely what Gregory found *fails* for the byte-returning retrieval and *holds* for the span-returning one: text bytes discard the I-address, so equal text cannot be distinguished from shared content; the span-set form keeps the address, so the correspondence is structural rather than inferred. Nelson frames correspondence as the whole point of intercomparison — "show you, word for word, what parts of two versions are the same" (2/20), "highlighting the corresponding parts is a vital aspect of intercomparison" (3/13). The combined read over one document is the smallest instance of that machinery: the shared I-address *is* the correspondence.

### Forced fragmentation at I-boundaries

A single requested V-span may come back as *several* blocks. This happens exactly when the span's content, though contiguous in the arrangement, was assembled from non-contiguous regions of content-space — for instance, two stretches transcluded from different sources, or from different insertions of the same source. By ASN-0058 M14a (shared/adjacent I-extents) and M16 (cross-origin), fragments drawn from non-adjacent or differently-originated I-regions *cannot* be coalesced into one faithful block. The split is therefore not an implementation accident but a forced consequence of content identity:

> **R-SPLIT.** A requested V-span yields more than one block exactly when its content spans non-contiguous I-regions; such fragmentation is forced — the maximally-merged faithful result (ASN-0058 M12, unique) cannot merge across a non-contiguous or cross-origin I-boundary.

Reading the span alone would still split it; but reading several spans together is what lets the reader see that the fragmentation pattern is the *shape of the editing and transclusion history* — "the discontinuity itself is the trace of the operation" (Nelson, on broken endsets, 4/42–4/43).

---

## The invariants across the combined result

We now state what the operation must maintain, and derive the preconditions under which it can. The governing postcondition is *fidelity*: the combined result must reproduce the document, as it stands, over exactly the requested region — nothing added, dropped, duplicated, or reordered. Let `⟦Σ⟧ = ⋃ᵢ ⟦σᵢ⟧` be the designated V-region and `V_req = dom(M(d)) ∩ ⟦Σ⟧` the requested positions actually present.

We reason backward, in the manner of `wp`. We want

> **R-FID** (the postcondition): `⋃_{β ∈ read(d,Σ)} ⟦β⟧ = {(v, M(d)(v)) : v ∈ V_req}`, with each pair appearing exactly once and the blocks listed in V-order.

What must hold for this to be provable? Decompose the obligation into four conjuncts, following the structure of a faithful partition.

*Coverage (no loss).* Every `v ∈ V_req` must appear in some block. For one span this is ASN-0058 B1 (coverage of the restriction `M(d)|⟦σ⟧`). Across spans, the union of the per-span domains is `V_req` because `⟦Σ⟧` is the union of the `⟦σᵢ⟧`. So coverage needs nothing beyond the decomposition's own coverage.

*No reorder.* The pairs must be delivered in V-order. Within a span this is the listing convention; across spans it requires `Σ` normalized (R-ORDER). So the precondition contributes: **`Σ` is normalized** for global order to equal arrangement order.

*No duplication.* No pair may appear twice. Within a span the blocks are V-disjoint (ASN-0058 B2). Across spans, two blocks from different `σᵢ, σⱼ` could share a V-position iff `⟦σᵢ⟧ ∩ ⟦σⱼ⟧ ≠ ∅`. Normalization's separation condition (N2) makes the spans V-disjoint, so no V-position is covered twice. Precondition: **`Σ` disjoint** (subsumed by normalized).

*Well-definedness of the mapping.* Each `v ∈ V_req` must have exactly one image (else "reproduce `M(d)`" is ill-posed) lying in the content store. These are ASN-0036 **S2** (functionality) and **S3** (referential integrity). And for V-order to be a well-founded total order with the minimal position the document expects, the positions must be well-formed — **S8a** (every component positive, no zeros). Under S8a the arrangement order is exactly the lexicographic order with `[1,…,1]` minimal (ASN-0036 D-MIN), and there are no negative or degenerate positions to disturb it.

Assembling the conjuncts, the fidelity invariant holds under a clean precondition:

> **R-FID holds** when `Σ` is normalized over `d`, each `σᵢ` is level-uniform within one subspace, and `M(d)` satisfies S2, S3, S8a. Then `read(d, Σ)` is an order-preserving, duplication-free, gap-free reproduction of `M(d)` over `V_req` — a bijection of `V_req` onto its image, carried by the blocks.

This is the abstract form of Nelson's "partition the document's V-extent": disjoint spans whose images, concatenated in V-order, equal the requested content with nothing altered. An alternative implementation, whatever its internal mechanism, must satisfy R-FID to be called a faithful combined read; the decomposition machinery merely *realizes* it.

### Version coherence

One invariant is so basic it is easy to miss. Every fragment in the combined result must refer to the *same* arrangement of the *same* version. The result is reconstructed on demand from scattered storage ("materializing it for you from the many fragments", 2/16), yet it must be self-consistent. The guarantee rests on two foundation facts: the arrangement `M(d)` is read at one observed state (R-FRAME — no transition occurs during the read), and content at an I-address is immutable (ASN-0036 S0, ASN-0047 P0). Hence

> **R-VERSION.** Every fragment of `read(d, Σ)` resolves through one and the same arrangement snapshot, and every I-address it names is permanent; a later combined read of the same `Σ` against the same arrangement returns identical V↔I pairs.

No fragment can silently drift to a newer revision, because the arrangement is fixed at the observed state and content never mutates.

### The degenerate designation

A zero-width or empty designation contributes nothing. If `σ` denotes `∅` (the degenerate limit of a span — note ASN-0053 S2: no well-formed span denotes `∅`, so this is a boundary input), then `M(d)|∅ = ∅` and `blocks(d, σ)` is empty. The combined result simply omits it; no empty placeholder fragment appears.

> **R-EMPTY.** A requested span designating no positions contributes no block to `read(d, Σ)`; the result is as if that span were absent.

This is the right abstract reading of the boundary case: faithfulness "to exactly what is designated, including nothing else" (4/25) means a designation of nothing yields nothing.

### The overlap question — a genuine open boundary

We have proved R-FID for *disjoint* `Σ`. What if the request overlaps — two spans covering a common V-region? Nelson's "exactly, including nothing else" language leans toward set semantics: the region is designated, hence returned, *once*. Gregory's evidence is that the back end, processing each span independently, returns the overlap region *once per covering span* — the deduplication machinery exists but is disabled. These are two different contracts, and the foundations do not force one. We therefore decline to elevate either to a claim. The invariant R-FID pins behavior precisely on the disjoint case; on the overlapping case the operation has a real degree of freedom — return the shared region once (a set) or once per covering span (a sequence with multiplicity). We record this as the principal open question, not a settled invariant.

---

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| read(d, Σ) | `read(d, Σ) = blocks(d, σ₁) ⌢ … ⌢ blocks(d, σₚ)`, the per-span maximally-merged block decompositions of `M(d)\|⟦σᵢ⟧` concatenated in request order | introduced |
| R0 | The document-extent instance `read(d, Σ_full)` returns exactly one text block and one link block — the two subspace extents | introduced |
| R-FRAME | The combined read is a pure query: `C'=C`, `L'=L`, `(A d' :: M'(d')=M(d'))`, `Σ` unchanged | introduced |
| R-ORDER | For normalized `Σ`, `read(d, Σ)` is globally ordered by V-position, and that order is the document's arrangement order, independent of request enumeration | introduced |
| R-TRACE | Every returned fragment carries both its V-position and its I-address; each `(v+k, a+k)` satisfies `M(d)(v+k)=a+k` with `a+k ∈ dom(C)` | introduced |
| R-SUBSPACE | Every block lies wholly in one subspace; text blocks precede link blocks; no block spans both subspaces | introduced |
| R-GAP | From the result one may decide, for each consecutive fragment pair, abutment vs. separation by unrequested content, recovering each omission from the boundaries | introduced |
| R-CORR | Distinct V-positions sharing an I-address are exposed as distinct blocks carrying that common I-address; visible only when read together and only because addresses are retained | introduced |
| R-SPLIT | A V-span yields multiple blocks exactly when its content spans non-contiguous I-regions; the split is forced — no faithful merge crosses a non-contiguous or cross-origin I-boundary | introduced |
| R-FID | For normalized `Σ` of level-uniform single-subspace spans, with `M(d)` satisfying S2, S3, S8a, `read(d, Σ)` reproduces `M(d)` over `V_req` with no loss, duplication, or reorder — a bijection of `V_req` onto its image | introduced |
| R-VERSION | Every fragment resolves through one arrangement snapshot; every I-address named is permanent; repeating the read against the same arrangement returns identical pairs | introduced |
| R-EMPTY | A span designating no positions contributes no block; the result is as if that span were absent | introduced |

## Open Questions

When two requested spans overlap, must the shared V-region appear once or once per covering span in the combined result?

What must the combined read guarantee about its result when the underlying arrangement violates V-position well-formedness, so that V-order is no longer well-founded?

Must the operation mark shared content as explicitly common, or is exposing the repeated I-address across distinct blocks a sufficient revelation of correspondence?

What must a faithful result guarantee about per-fragment subspace tagging, so a reader can distinguish a text extent from a link extent without external context?

Under what conditions may a faithful combined result merge fragments across span boundaries, and when is such merging forbidden?

What must the operation guarantee about the total designated width relative to the sum of requested span widths when the request is not a partition of the V-extent?
