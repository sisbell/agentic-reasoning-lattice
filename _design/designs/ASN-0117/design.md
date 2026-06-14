## What this is

ASN-0117 defines the **DELETE operation**: removing a span of content from one document's *arrangement* (its Vstream / POOM) while leaving the permanent *content store* (Istream / granfilade / permascroll) entirely untouched. It is the arrangement-*contraction* half of the editing pair — the exact symmetric inverse of INSERT — and its whole subtlety is that "delete" here means *de-arrange*, never *destroy*.

## Design commitments

These are forced on the rest of the system; downstream design cannot violate them.

- **Delete means de-arrange, not destroy.** DELETE removes a document's *placement* of content, not the content. The bytes survive at their I-addresses permanently. This is load-bearing: backtrack, transclusion, and link survival all presume the bytes endure — freeing them breaks all three at once while *appearing* to honor "the span is gone."
- **DELETE writes nothing to the content layer — not even an append.** It is append-only taken to its limit. The content store is a strict *frame* of the operation: never consulted, never written, never reclaimed.
- **Two layers, one touched.** State is (a) an append-only content store `C : I-address ⇀ Value` whose identity is by origin, and (b) a per-document arrangement `M(d) : V-position ⇀ I-address`. DELETE mutates only `M(d)`.
- **Positions are slots, not containers.** A V-position never *binds* content; it is an ordinal coordinate. Survivors keep their I-address; only their V-slot is relabeled. The arrangement re-coordinates itself around fixed content identities.
- **The arrangement must stay a dense, gap-free canonical run.** Closing the gap is mandatory: after deleting `c` slots from a run of `N`, the result is the contiguous run `q_1…q_{N−c}`. No holes, no overlap, no degenerate/zero-width positions.
- **The effect is confined to one subspace of one document.** A text delete cannot move link positions; a delete in `d` cannot perturb any other document. This is principled (the displacement acts only within the target subspace's ordinal run), *not* incidental.
- **Links anchor on I-addresses, so they survive by construction.** What a deletion *can* change is a link's **discoverability from this one document** — never the link itself, never its coverage, never its discoverability from other documents that still arrange the content.
- **Containment is a precondition of the core operation.** DELETE is defined only for spans lying inside the arranged run. Totalizing over ill-formed spans (reject vs. clip) is a separate, caller-facing obligation — not part of the contraction.

## What must be built

- An **arrangement-contraction operation**: drop the `c` mapped slots, shift the surviving suffix left to close the gap, scoped to a single (document, subspace). Realized as a prefix-retention truncation plus, when a suffix survives, a re-placement of survivors at the closed-up positions.
- A **precondition validator**: span well-formedness (positive width, matching depth, boundary-aligned endpoints) *and* containment within the document's current arranged extent.
- A **cheap suffix-shift mechanism** that re-coordinates survivors while carrying each survivor's I-address unchanged.
- A **content store that the delete path cannot reach to reclaim** — i.e., structural separation between arrangement-delete and any content-layer reclamation, so NonDestruction holds even under bugs.
- A **discovery-index reconciliation strategy**, because any content→document index *will* go stale on delete.
- **Backtrack support**: enough retained arrangement history to reconstruct a prior placement, given that the bytes (but not the old mapping) persist in the store.
- A **durable record of the operation and a recovery path** that replays arrangement edits without re-touching content.

## Implementation approaches

**1. Position representation and the suffix shift (the central choice).**
The abstract effect is "renumber the dense run." Three concrete realizations:

- *Persistent ordered map, absolute keys (`im::OrdMap`-style).* DELETE drops the `c` deleted keys, then removes-and-reinserts each suffix key at its shifted coordinate. Dead simple, mirrors `M'(d)` directly, and structurally shares the untouched prefix. Cost: a delete near the front re-keys nearly the whole suffix — O(suffix·log N) work and O(suffix) freshly path-copied nodes, which defeats structural sharing for the suffix. **Pick this** for the first correct implementation, small documents, or when simplicity dominates.
- *Relative-displacement balanced tree (the udanax enfilade).* Store each node's V-displacement relative to its parent; absolute position is the cumulative sum down the path. A uniform suffix shift then adjusts the displacement of one boundary subtree rather than every leaf — Green realizes exactly this (shift applied to boundary crums, then rebalance), giving O(log N) work and O(log N) new nodes under persistence. It also makes "carry the I-address along" automatic: the leaf is untouched, only a V-coordinate offset moves. **Pick this** at scale, especially with frequent edits near the front, and because it makes retained-version snapshots cheap (below). Cost: substantially more machinery (cut/slice at boundaries, recombine, the displacement algebra).
- *Journal-native materialization.* Treat the durable truth as an append-only operation journal (DELETE = one record `(d, p, w)`, **no content record**) and the in-memory arrangement as a recomputable materialized view, rebuilt by replay on load — exactly the repo's `links.jsonl` + `paths.json`-recovered-by-replay model. The materialized view uses option 1 or 2 internally. This is the Lampson "log for atomicity and recovery" hint taken fully, and it gives backtrack for free (replay to a prefix). **Frame the system this way regardless**, and choose 1 or 2 for the live view.

My recommendation: structure as *journal-of-arrangement-edits + in-memory view*, start the view as an absolute-key persistent map, and migrate hot documents to the relative-displacement tree when shift cost or version retention demands it.

**2. Content-store frame (NonDestruction by construction).**
Make the guarantee structural, not a discipline. The content store is a separate, append-only module with **no reclamation entry point reachable from the arrangement-delete path** — Green's own architecture enforces NonDestruction this way, keeping two distinct delete primitives and routing document-span delete only to the one that operates on the arrangement enfilade. Replicate that separation: the arrangement-delete API should have no capability to free content, so even a buggy delete cannot violate P0.

**3. Discovery index (content → arranging documents).**
This index is a *hint*, not ground truth, and DELETE makes it stale (it will name `d` for addresses `d` no longer arranges). Options:
- *Maintain it on delete* (a `deletespanf` analogue). Rejected: an address may still be arranged elsewhere in `d` (within-document sharing) or by overlapping spans, so knowing when to retract an entry requires reference counting and re-derivation on the write path — expensive and error-prone.
- *Treat it as a hint: never retract on delete, post-filter on read.* The query returns a superset; verify each candidate against the authoritative arrangement (resolve the address back through the document's live mapping) and drop misses. Cheap writes, correct reads, fully recomputable. **This is the right default** — it is precisely Green's behavior (the index is append-only; callers post-filter via I→V resolution).
- *Lazy/opportunistic cleanup* (retract stale entries you happen to touch on query, or rebuild periodically) as an optional accelerator layered on the hint approach.

**4. Durability and backtrack.**
The content store alone reconstructs the *bytes* but not the *placement*. To make backtrack exact you need retained arrangement history:
- *Journal replay* (from approach 1's framing): replay arrangement edits to any prefix → any prior arrangement. Natural fit, and the content store needs no DELETE record at all.
- *Retained persistent-map roots*: with structurally-shared maps, each DELETE yields a new root sharing nodes with the old; keep the old root as a version handle for O(1) access to the prior arrangement at O(delta) memory. This is why version comparison works in Green — the prior version's mapping still resolves those addresses. Pairs especially well with the relative-displacement tree.
- *Periodic snapshots* to bound replay cost. Combine: snapshot + journal tail.

**5. Totalization, validation, and acknowledgment ordering.**
Validate *before* mutating, against the live arranged extent — not just a non-zero-width check. Green's delete path is the cautionary tale: it gates only on non-zero width, has no containment check, shifts in-range survivors by the full out-of-range width, and *acknowledges success before doing the work* — turning an out-of-bounds span into silent corruption (negative, unreachable positions). So: (a) reject by default on a containment failure with no state change, or offer clip-to-extent as an explicit opt-in; (b) never acknowledge until the mutation is computed and durable.

**6. Link survival.**
Get this for free by **indexing links on content identity (I-address), not on V-position** — Green's choice, and the reason links persist, become merely undiscoverable from `d`, and *re-discover* automatically when the same I-addresses are re-arranged (via identity-preserving copy/transclusion, not via fresh-content insert). DELETE then needs to do nothing to the link store; coverage invariance is automatic.

**7. Empty and degenerate states.**
At the whole-unit abstraction, endpoints fall on position boundaries, so no zero-width slot is ever produced — preserve that by only ever cutting at existing boundaries (boundary-aligned cuts need no splitting at all). Make the **empty arrangement a first-class, reusable state**: Green's delete-everything path leaves a structurally "tall" empty tree that later *crashes on re-insertion* because height-collapse was disabled — a warning to either keep the empty state canonical or ensure the insert path accepts whatever empty shape delete leaves behind.

## Guarantees to uphold

- **NonDestruction (content permanence + address permanence).** Store unchanged in domain and value; every deleted I-address survives. *By construction* if the delete path has no reachable content-reclamation capability (structural separation). Active enforcement: keep that separation airtight.
- **Gap closure / canonical order.** Survivors form the dense run `q_1…q_{N−c}`. *By construction* once the operation is the contraction — **but** requires *active enforcement of containment* to avoid the corruption (negative/unreachable positions) that an out-of-range span produces.
- **Order preservation.** The suffix shifts uniformly by `c`; relative order is exact. *By construction* (the shift is an order-preserving injection).
- **Subspace confinement.** Other subspaces (notably links) are untouched by a text delete. Must be made *principled* — scope the shift explicitly to the target subspace. Do **not** lean on arithmetic happenstance: Green achieves this only *accidentally* (an exponent guard makes cross-subspace subtraction a no-op), which is fragile.
- **Document isolation.** Every other document's arrangement and resolved content are invariant, including transcluders. *By construction* if each document's arrangement is a separate object and the operation is scoped to one resolved document handle (Green's isolation is emergent from exactly this — there is no path from one document's mapping to another's).
- **Link survival / coverage invariance.** Links and their coverage are unchanged. *By construction* if links anchor I-addresses and the delete path never touches the link store. Per-document *discoverability* is the only thing that may shrink — and that is a derived read-time fact, not stored state.

## How it fits

- **Leans on the content store / Istream foundation** (the ContentStoreFrame of ASN-0082): provides the immutable, append-only content layer DELETE holds in frame.
- **Leans on the arrangement model** (ASN-0036 / ASN-0047): supplies the well-formedness package — zero-free positions, common depth, the dense canonical run — that the post-state must re-establish.
- **Leans on the contraction algebra** (ASN-0082): provides the displacement, the three-region (prefix/deleted/suffix) partition, the order-preserving left-shift, and exact gap-closure. DELETE is literally a realization of that family with the content store framed.
- **Leans on the link/coverage foundation** (ASN-0098): coverage invariance, the discoverability characterization, per-document undiscoverability, and resurrection-on-re-arrangement.
- **Is the inverse of INSERT** (the arrangement-expansion operation); they should share the position-representation and journaling machinery.
- **Hands concurrency to the consistency/isolation model** (ASN-0134): this note assumes a single coherent pre-state and leaves "delete plus a concurrent op without a serializing authority" open.
- **The content→document discovery index is a downstream consumer** that must absorb staleness (post-filter), not a dependency DELETE updates.

## Decisions for the builder

- **Position representation:** absolute-key persistent ordered map (simple, O(suffix) re-key) vs. relative-displacement balanced tree / enfilade (O(log N) shift, cheap version snapshots, heavier) vs. deferred-renumber view over a journal. Pick by document size and edit locality; the journal framing is orthogonal and worth adopting either way.
- **Totalization policy:** reject an out-of-extent span (fail-closed, no state change) vs. clip it to the arranged run. Reject is the safer default because clip silently does something other than asked; the spec leaves this genuinely open. Whichever you choose, *validate before mutating* and *never acknowledge before the work is durable*.
- **Discovery-index strategy:** maintain-on-delete vs. hint + post-filter vs. hint + lazy cleanup. Recommend hint + post-filter, with lazy cleanup as an optional accelerator.
- **Backtrack mechanism:** journal replay, retained persistent-map roots, periodic snapshots, or a combination. Decide what "exact prior arrangement" must cost in memory vs. replay time.
- **Concurrency unit:** per-document (or per-document-per-subspace) serialization is the natural domain since the effect is so confined; alternatives are optimistic version-check-and-retry or finer-grained locking. Defer the cross-operation semantics to the consistency layer, but pick a serialization unit now.
- **Empty-arrangement handling:** how delete-everything is represented and whether re-insertion into an emptied document is safe. Make the empty state canonical and re-usable (heed the disabled-collapse crash as a concrete failure mode).
- **Within-document sharing:** decide whether the model allows one document to arrange the same I-address at multiple V-positions; if so, the discovery post-filter and any index retraction must reason about "last witness," not per-pair removal.
