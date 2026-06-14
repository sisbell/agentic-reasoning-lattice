## What this is

FINDDOCSCONTAINING is the substrate's **reverse-reading / membership-oracle** capability: given material a reader is holding (regions of documents), it returns every document anywhere in the docuverse whose *current* arrangement includes any portion of that material. It is the inverse of windowing — "who includes this?" rather than "what does this include?" — and the document-containment sibling of the content-region link query (ASN-0127).

## Design commitments

Load-bearing, forced by this note:

- **Containment is present-tense and address-keyed.** A document is a member iff its *current* content arrangement maps some position onto a queried I-address — not value resemblance, not provenance, not content-once-held. This single decision answers every sub-question the note raises, and it is the constraint no downstream design may bend without building a *different* operation.
- **Material is identified by permanent I-address — never by value, never by source.** Independently-authored equal bytes are different material; a sibling address from the same origin is different material. Identity is finer than authorship and blind to value.
- **The answer is a set of bare document identities** — deduplicated, positionless, multiplicity-free. "Which documents," never "where within." Recovering positions is a separate, per-document query and must stay out of this one.
- **Membership is existential ("any portion"), not full containment.** One shared address suffices; coverage is never required. The primitive is OR; every AND-shaped question (full containment, co-occurrence, collage detection) is a *derived* query built by composing single-fragment calls — not a parameter of this one.
- **Completeness is global and unconditional.** The comprehension ranges over the entire document stratum; the signature admits no locality, authority, account, or asker parameter, so no sub-docuverse restriction is even *expressible*. Any scoping you want is a post-filter on the complete answer, not a narrowing of the search.
- **Two phases, cleanly separated.** Phase 1 (resolve) is the *only* phase that reads the asker's documents: it projects named V-regions through their live arrangements to a content I-address set and *flattens* — after resolution, which named region contributed which address is irrecoverable. Phase 2 (find) is a comprehension against that bare I-set. The operation is a pure function of the resolved set.
- **Transclusion reach is flat, not traversed.** Identity propagates at copy time, so by query time there is no chain to follow; one comprehension collects the entire current sharing set. Depth of copying never mints a new identity and never costs a hop.
- **The live answer breathes; the monotone "ever-contained" index is a *different* operation.** finddocs is non-monotone (grows on inclusion, shrinks on deletion); a write-only provenance index answers "has ever contained," which is a superset. An implementation must not let the index *be* the answer.

Merely conventional: the particular presentation of regions as span-sets and their normalization are interchangeable and affect no result; subspace routing and store disjointness are *inherited* from the foundation, not chosen here.

## What must be built

- **A region resolver** that, given a vspec-set (V-regions in named documents), reads each named document's *current* arrangement, projects the regions to their content-subspace images, unions them, and yields a bare, grounded I-address set. (This is ASN-0127's image primitive, content-restricted.)
- **A containment oracle over the whole stratum**: given an I-address set, produce every document whose current content arrangement maps a position onto any address in it — the comprehension, by scan or by index.
- **An inverse association from I-address(-spans) to documents**, if the comprehension is to beat a full scan. Because resolved material is a *span-set*, this wants interval (range-overlap) lookup, not just point lookup.
- **A present-tense soundness filter** — for each candidate, confirm its *current* arrangement still maps onto the queried material — *if and only if* the inverse association can return stale (once-contained-but-not-now) candidates.
- **A recovery/persistence story** for any index: rebuild from the placement journal by replay; optionally snapshot to bound cold start.
- **Result assembly**: dedup to bare identities; no positions, no counts.
- **(Optional, near-free) a historical-query variant** exposing the "ever contained" query — it *is* the raw index, before the filter.

## Implementation approaches

### Resolving regions to material
Read each named document's arrangement (the POOM), project V-region → content I-addresses, union. Reuse ASN-0127's image primitive directly. Two things to decide here:

- **One-shot vs cached resolved set.** Resolution is present-tense and *drifts*: re-running after editing a named document can change the I-set even when no containment fact changed (a reorder of a named doc silently moves the answer). Caching the resolved I-set gives a *frozen* subject matter — sometimes exactly right ("find more like this," stably), sometimes stale. Pick deliberately and document which.
- **Grounding is free.** A raw I-argument needs no validation: unallocated and link-store addresses are inert. The query cannot be poisoned by garbage addresses, so don't write validation code for them.

### The containment comprehension — scan, live index, or monotone index + filter
This is the central choice. The contract (global completeness, present-tense soundness) is fixed; the mechanism is yours.

**A. Brute-force scan.** Iterate the stratum, test each document's current content range against the material. It is literally the spec definition: always correct, no auxiliary state, nothing to recover, no staleness, no ghosts. Cost is O(documents × probe). **Pick this first** — for small docuverses, low query rates, or as the always-right oracle the other approaches are validated against. The simplest thing that honors the spec, with the rare case kept correct by keeping it trivial.

**B. Live inverse index (eager delete).** Maintain I-address → currently-arranging-documents, updated on every arrangement change: add on content extension, **remove on contraction**. The query becomes a pure interval lookup + union, no filter. The cost and the risk move onto editing: every contraction must delete the right entries, transactionally. The failure mode is the worst kind — a missed deletion returns a ghost, a *silent soundness violation* with nothing to catch it — and you are now maintaining authoritative duplicate state that must stay perfectly in sync with the arrangements. Reach for this only when query latency dominates, writes are comparatively rare, and you can make delete-on-contract bulletproof. I would resist it: it stakes a correctness property on never dropping a maintenance step.

**C. Monotone (append-only) inverse index + present-tense filter — recommended default.** Record `(address, document)` whenever material enters a document's content range; **never erase**. The index over-approximates — it answers "ever contained," a superset — and you recover the live answer by filtering each candidate through its current arrangement (a per-candidate I→V probe of that document's POOM, *not* a re-search). Why this is the right shape:

- The index is a **hint**, not authority. A stale entry is harmless because the filter removes it; the authoritative truth stays in the arrangements, where it belongs, and is never duplicated.
- The index is **append-only** — no deletion path means no torn-update race and no "forgot to remove" ghost bug. It recovers by replay of the placement journal, exactly this repo's `links.jsonl`/`paths.json` pattern, and is a pure function of the placement events: it can be discarded and rebuilt.
- **Concerns separate and each lands where it's cheap.** The index owns *completeness* (never omit a container), which is structural — guaranteed by recording on every placement (the J1★ coupling). The filter owns *soundness* (no ghosts), which is local and testable. Contrast B, where one structure must guarantee both and soundness rides on never missing a delete.
- **Common case fast, rare case correct.** On growing histories (no contraction → no ghosts) the filter confirms everything and is nearly free; under heavy deletion it strips many ghosts — slower, still exactly right. The filter's total cost is proportional to the over-approximation, which is bounded to "documents that have deleted queried material."
- **One mechanism, two contracts.** The raw index *is* the historical "ever contained" query; the filtered index is the live "contains" query. The filter is the only difference — so you get the historical query for free and the live one for a single extra local check.

This is precisely the udanax-green spanfilade strategy — *minus the filter*. Green's document-containment index is verifiably write-only: deletion touches only the per-document arrangement, never the index, so green's FINDDOCSCONTAINING returns ghost documents and, in this note's terms, computes the historical query rather than the live one. Green is the cautionary proof that the filter is the *whole* difference between the two — and that the I→V check it needs is machinery green already runs on its link-following path and merely omits here.

**Index structure.** Resolved material is a span-set over I-address space and "any portion" is interval intersection, so the index wants **range-overlap lookup keyed by I-address**, document identity as payload. The proven structure is the **spanfilade** — a multidimensional range tree (enfilade) over (origin-class, I-span) — which green uses for exactly this, discriminating document-content entries from link-endpoint entries by a type tag in the origin dimension and matching by half-open interval overlap (deliberately admitting single-point boundary contact). A fresh build can use any interval index (interval tree, range tree, or an I-address-ordered B-tree of spans); the enfilade earns its keep mainly when you also want the link-endpoint queries (ASN-0127) and the version/transclusion span operations over the *same* structure. With persistent (structurally-shared) maps, the index is an immutable value threaded through states, so retaining old versions costs little.

**Key the index by I-address only — never by V-position.** This is green's "stability by representation," and it is *why* positional edits are free: if the index carries no V-coordinate, a V-shift from an insert is structurally invisible — nothing to update, no per-edit proof obligation. Choose the representation so the invariant costs nothing.

**Filter cost** is a per-candidate I→V probe of the candidate's live arrangement — cheap *iff* that arrangement supports inverse (I→V) lookup. If it is only V→I, you need a per-document inverse index or you pay a scan. Either way it is a lookup, not a re-search.

### Recovery and the historical summary
The append-only index recovers by replaying the placement journal; snapshots bound cold start. Worth seeing clearly: the foundation's provenance relation *is* this index, and its real justification is economy. With persistent state values you could answer "ever contained" by retaining every past boundary and unioning finddocs over them — but that keeps all of history. The provenance index is the compact digest that lets you discard the boundaries; the note's compaction open question is exactly "how small can the digest get while still witnessing every once-live container."

### Result assembly
Dedup to bare identities at emission. Stream or batch freely; the codomain forbids positions and counts, so there is nothing to join or aggregate. A caller wanting "where within each returned document" issues a second, per-document content-region query (ASN-0127 territory) — keep it out of here.

## Guarantees to uphold

Hold **by construction** (from the address model and the comprehension, given a correctly-keyed index):

- **Subject-matter permanence** — resolved material stays grounded forever; content addresses are never deallocated or overwritten. The thing you searched for cannot be destroyed under you.
- **Poison-immunity** — unallocated and link-store addresses in the query are inert; no validation of a raw I-argument is needed.
- **Identity-keying / value-blindness** — equal bytes and same-origin siblings never match.
- **Locality and non-impedance** — a document's membership depends only on its own arrangement; growing the docuverse elsewhere can never add or remove it. Answers don't degrade as unrelated material accumulates.
- **Flat transclusion reach** — the whole current sharing set is found in one pass, path-free, and severing a chain's middle leaves its ends co-listed.
- **Origin-neutrality** — no privilege or penalty for the document that allocated the material.
- **Positional-edit stability** — *provided the index carries no V-coordinate.* Inserts that shift positions never move the answer. By construction of the representation — which is therefore a design constraint, not an accident.

Require **active enforcement**:

- **Soundness (no ghosts).** The one guarantee a monotone index does *not* give you: you must run the present-tense filter. This is the difference between this operation and the historical query, and the single thing green gets wrong.
- **Completeness (no omission).** Holds by construction *given the coupling discipline*: every path that gives a document content must record into the index. Enforce that there is no silent-omission channel — no placement route that skips the recording. (Green's evidence is that every placement funnels through the recording pair; replicate that discipline.)
- **Global reach under distribution.** If the unified state is realized across servers, completeness must be backed by either state coherence or an *explicit* availability qualification. "Temporarily unreachable" must never silently become "absent from the answer."
- **Bare, deduplicated codomain.** Trivially enforced at assembly — but it is a contract: don't leak positions or multiplicity.

## How it fits

- **Stands on the transition-model foundation (ASN-0047)**: the unified state (content store, link store, entity set, per-document arrangement family, provenance relation), the editing vocabulary it characterizes but does not define, and the couplings — notably record-on-placement (J1★) and the containment-bounds-provenance invariant (P4★) — that make the provenance relation a sound historical index.
- **Shares machinery with the content-region link query (ASN-0127)**: the same image primitive and the same resolution-drift result. The two are siblings — link discovery vs document discovery — with *inverted* stability: link endsets are immutable store values, so 0127's fixed query only grows; document arrangements are mutable, so this one breathes. A build can share the resolution front-end and the interval-index structure between them (green does, via one type-tagged spanfilade).
- **Consumes the address/allocation model (ASN-0036, ASN-0093)**: subspace routing, address identity and injectivity, monotone allocation, store disjointness, origin — all inherited, none re-derived here.
- **Leans on span-sets (ASN-0053)** for the finite presentation and normalization of regions, and on the gap-shift (ASN-0082) and reorder (ASN-0098) results for its edit-stability characterization.
- **Hands to the per-document arrangement (POOM) layer twice**: for resolution (V→I) and for the soundness filter (I→V). Hands to the content store only for grounding. Hands *nothing* downstream but answers — it is a leaf read-capability, not a foundation.
- **Adjacent, out of scope**: the editing operations upstream (they move the answer), inter-server replication/BEBE downstream (it stresses the completeness contract), and per-document position-recovery alongside (a different query).

## Decisions for the builder

Genuine implementation forks the spec leaves open, distinct from the note's spec-level open questions:

- **Comprehension strategy: scan vs live index vs monotone-index-plus-filter.** Start with scan; adopt the monotone index + filter (C) as the docuverse grows; reach for the eager-delete live index (B) only under query-latency pressure with bulletproof delete-on-contract.
- **Expose the historical "ever contained" query as first-class?** The monotone index answers it for free, the filter being the only thing between it and the live query. If users want "every document that ever quoted this," surface both.
- **One index or two?** Unify document-containment with the link-endpoint index into a single type-tagged interval structure (green's choice — shares code and the version/transclusion span operations), or keep them separate for "do one thing well." The structures are genuinely the same shape; decide by how much you value shared machinery vs isolation.
- **Interval-index data structure** — enfilade / range-tree / interval-tree / I-ordered B-tree. The enfilade pays off mainly if you also run link and version span queries over it.
- **How the per-document arrangement supports the filter** — native I→V inverse lookup vs a per-document inverse index vs scan. This sets the filter's per-candidate cost.
- **Resolve once or re-resolve per query** — cache the frozen resolved I-set (stable subject matter, blind to later edits of named documents) or re-resolve each time (tracks drift). Different products want different answers, and the two genuinely differ.
- **Persistence and recovery** — replay-only vs snapshot+replay; whether the index is a discardable cache over the journal or a durably-maintained store.
- **Distribution and availability** — if multi-server, pick the coherence/availability model that keeps completeness honest, and make any incompleteness an explicit *qualified* result rather than a silent omission.
- **"Any-portion" boundary semantics** — half-open interval overlap, and whether single-point boundary contact counts as containment (green deliberately admits it). Pick it and document it.
