# Design Digest — ASN-0131: RETRIEVEENDSETS

## What this is

RETRIEVEENDSETS is a **pure, read-only query over the link subsystem**: given a content region (a set of content-subspace V-positions in one document), it reports the link *anchoring* that touches that region — the endsets, and the spans where links attach, each tagged by role (from / to / type / higher) — while deliberately **withholding the identity of the links those endsets belong to**. It is the "show me how this content is bound" sibling of the link-discovery query (`findlinks`, ASN-0127); it shares that query's selection *index* and differs in what it reads out *and* in reporting only the addressable population.

## Design commitments

Marked **[forced]** (follows from the data model, or is forced by faithful reporting — a violation misreports the anchoring) or **[chosen]** (this note's design decision, defensible otherwise).

- **Anchoring is keyed to content identity — never to position, and never to the link's home.** [forced] The region resolves to I-addresses through the present arrangement; endsets are matched by I-address overlap. A link reaching the region through transcluded/borrowed content is surfaced *identically* to one on native content. Where the link lives and which document "owns" the content are invisible to the match.
- **The answer is a set of (role, endset) pairs, and nothing more.** [chosen — this is the defining commitment] Identity is withheld; value-identical endsets in the same slot from distinct links collapse to one pair. You cannot count links, recover an address, or pair a surfaced from-end with its link's to-end. Withholding names is the whole point — restore it and you have rebuilt `findlinks`.
- **Overlap, not containment, is the match.** [forced] One shared I-address is contact; an endset straddling the region boundary is surfaced (it is exactly what you want to see). This forces *interval-overlap*, not subset, in any index.
- **Surfaced spans are reported at full recorded extent — never clipped to the region.** [forced] Clipping would misreport the link's grip; the unclipped extent holds under every reading.
- **The query is discovery-anchored: present-tense and non-monotone.** [forced, given resolution through the arrangement] It reports what is reachable through the region *as the document is now arranged*. A zero answer is a statement about the present, not about history.
- **Pure and local.** [forced] It reads exactly the queried document's arrangement fiber and the link store (with the nullified set); it never touches content *values*, the entity set, or provenance, and it changes no state.
- **Only addressable (present, non-withdrawn) links contribute.** [chosen] Retraction marks, never deletes; the report is over the live population.
- **Whole-endset surfacing is adopted but provisional.** [chosen, provisional] A surfaced endset is returned in full — all its spans, including those pointing outside the region. The alternative (return only the touching spans) is left open and is *not cosmetic*: it decides whether the query distributes over unions of regions.

## What must be built

Functionally — what each capability must do:

- **A region resolver** (borrowed, not built here): map a finitely-presented set of content-subspace V-positions in `d` to the I-addresses they *currently* occupy, through `d`'s present arrangement. Must yield only currently-arranged addresses — this is what makes the query present-tense.
- **An endset-touch matcher / index**: given a set of content I-addresses, find every (addressable link, slot) whose endset covers at least one of them. Must be role-aware (per-slot) and support interval-overlap, not containment.
- **An endset-value recovery**: for each matched (link, slot), produce the endset's *full* value (all its spans) from the authoritative link store — needed only if whole-endset surfacing is adopted.
- **An addressability filter**: exclude withdrawn/nullified links. Derivable wholly from the link store (the retraction links).
- **A projection-and-dedup**: drop link identity, tag each endset with its slot, and collapse duplicate (slot, endset) *values* to one. The output is a set.
- **A touch test**: decide `coverage(e) ∩ region-image ≠ ∅` as interval-overlap over the half-open address space.

The only durable artifact this motivates is the **index**, and even that is a derived hint (below). The query itself stores nothing.

## Implementation approaches

**The spine (Lampson):** RETRIEVEENDSETS is a *different read-out of the same selection index `findlinks` uses* (`sel = findlinks_V ∩ addressable`). Build the index **once**, as a **recomputable hint** that over-approximates, and restore correctness at read time by (a) resolving through the *live* arrangement and (b) filtering to addressable links. This is precisely how the udanax-green reference works: a **write-only spanfilade** (a content-address-keyed endset index that is never pruned) whose staleness is cancelled at read time by POOM resolution.

**1. The endset index — the central new structure.**
- *Content-address-keyed interval index → (slot, link)*, role-banded by from/to/type. Realize as an interval/range index over the half-open address space; an overlap query per slot answers the touch test directly. Green's spanfilade is exactly this (keyed by content I-address, with the endpoint-role as a separate index dimension) — an enfilade designed for logarithmic access over a large address space. The same index serves `findlinks` (project to identity) and RETRIEVEENDSETS (project to (slot, endset), dedup) — **do not build two.**
- *Index lifecycle — three options:*
  - **(a) Rebuild-by-replay (default).** Treat the index as a pure function of the link journal: persist only an append-only journal of link/endset records (this repo's `links.jsonl` + `paths.json`, recovered by replay), and rebuild the interval index on load. *Pro:* no separate durability or consistency burden, no index corruption possible, completeness for free (the rebuilt index cannot miss a stored endset). *Con:* startup cost proportional to journal length.
  - **(b) Persistent, structurally-shared index.** Maintain the index incrementally as an immutable value (the `im` crate's structural sharing), threading a new version per link emission. *Pro:* cheap snapshots, lock-free readers, point-in-time queries. *Con:* more machinery; worth it only for concurrent reader-versions or historical queries.
  - **(c) Snapshot/checkpoint.** Periodically checkpoint the rebuilt index to bound replay. A middle path when (a)'s startup latency is measured to matter.
  - *When to pick which:* default to **(a)** — the spec demands no durability of the index's own, so don't give it any; add **(c)** when replay-on-load becomes a real cost; reach for **(b)** only when one engine serves many concurrent versions.
- *The hint discipline that makes append-only safe:* the index may carry **stale entries** — content orphaned by contraction, links since withdrawn. Tolerate them. The region resolver yields *nothing* for unarranged content, and the addressability filter drops withdrawn links, so stale index entries never reach the answer. **The index therefore needs no deletion path and no compaction urgency** — this is Green's write-only spanfilade recovered by live intersection, and it is the cheapest mechanism that meets the contract.

**2. Endset-value recovery — the live design fork.** A per-span index naturally finds only the *touching* spans (each at full extent — honoring no-clipping). Whole-endset surfacing needs the spans the region *didn't* touch, so it requires a **join back to the authoritative link store** keyed by the matched link. So: adopt whole-endset ⇒ after the index locates the link, read its full endset value from the store; adopt touching-spans ⇒ return what the index found and skip the join. This is the one genuine cost/semantics tradeoff, and it decides union-distributivity (approach note below).

**3. Addressability filter.** Maintain a **cached nullified set as a hint** — mark links nullified as retractions are applied; recompute from the journal on any doubt. *Pro:* O(1) per-link filter; retractions are rare and queries frequent, so cache the answer. *Con:* must track the journal — but as a hint, drift is recoverable by replay. A structural fact simplifies this: non-retraction emissions are always addressable and withdrawal is permanent, so the mark-set grows **monotonically** — append-only, no un-mark path, matching the index's own discipline. The alternative (scan retraction links per query) is simpler but pays O(retractions) every read; prefer the cache.

**4. Projection and dedup.** The answer is a *set* of (slot, endset). Dedup must be by **structural endset equality**, not by link identity — the link store is non-injective, so two distinct links can bear the same endset value, and RE-UNIT requires they collapse. Canonicalize each endset (sort/normalize its spans) and hash into a set. Keying dedup by identity would both leak names and fail to collapse value-twins.

**5. Caching the *answer* (for a live "what's anchored here" view).** The note's stability theorems double as an exact **cache-invalidation contract**: a materialized RE answer is invalidated *only* by content-subspace arrangement edits to *this* document, by link emission, and by retraction — and is left fixed by edits to other documents, content allocation, provenance recording, entity creation, and link-subspace-only edits. That the contract folds user-facing insert/delete into "arrangement edits" rests on a modelling assumption the note adopts explicitly — the *conservative lift*: shift-based insert/delete (ASN-0082 displacement) touch `Σ.M(d)` alone, framing the link store, entities, provenance, and content. If your insert/delete also mutate the link store, the addressability half of this contract must be re-derived. The contraction-stability weakest precondition (RE-CWP) is even checkable *before* a deletion, so a reactive view can skip recompute when it holds. If you build incremental/reactive anchoring views, these results tell you precisely when to recompute and when not to.

**6. Search scope.** Default to a **single global index** spanning all links regardless of home document — simplest, matches Green (whose search is global, not home-scoped), and honors transclusion-blindness directly. Partition by store only if links are physically distributed; then completeness (RE-CMP) forces a cross-store fan-out (the note's Open Question 5).

## Guarantees to uphold

- **Permanence / content-identity invariance (RE-IDENT)** — by construction (links immutable, coverage fixed forever). The only active duty: **never clip or mutate** an endset value on the way out.
- **Purity (Σ′ = Σ)** and **finiteness (RE-FIN)** — by construction (read-only; finite store), with finite region presentation as a *caller obligation*.
- **Name-withholding and value-dedup (RE-UNIT)** — active: the projection must drop identity and collapse value-equal pairs; by construction of the output if identity is never carried through.
- **Overlap, not containment (RE-OVL)** — active: the index and test must be interval-overlap.
- **No clipping (RE-CLIP)** — active: return full recorded extent; choose the non-clipping read path (Green has both a clipping path, used for content retrieval, and a non-clipping path, used for endsets — use the latter).
- **Soundness / completeness (RE-SND / RE-CMP)** — completeness = the index has no false negatives (rebuild-by-replay guarantees this); soundness = no fabrication (filter to addressable, require real overlap, dedup by true value).
- **Present-tense / discovery-anchoring (RE-SEL, RE-EDIT)** — active: resolve through the *live* arrangement on every query; never answer from the index alone (that would report historical anchoring).
- **Union-distributivity (RE-UDIST)** — holds **by construction iff the return value is region-independent** (whole-endset). It is forfeited under the touching-spans reading. Be explicit about which you give up; if region queries are composed from sub-regions, you need whole-endset.
- **Intersection does *not* compose (RE-UDIST-∩)** — `RE(W₁∩W₂) ⊆ RE(W₁)∩RE(W₂)` is one-sided and unconditional, but the reverse fails *even under an injective arrangement* (split witnesses: one shared address drawn from each region's exclusive part), so **never compute an intersection-region answer by intersecting sub-answers**. Equality's exact condition — and a structural sufficient form — is left open (the note's OQ4).

## How it fits

- **Leans on the arrangement subsystem** (POOM; ASN-0058 / 0082 / 0047) for present-tense region resolution V→I — the source of discovery-anchoring. (Green: the querying document's POOM; this repo: a persistent ordered V→I map.)
- **Leans on the link store** (ASN-0043) for endset values, immutability, and coverage; on **coverage / span algebra** (ASN-0098, ASN-0043) for the touch test over half-open prefix-intervals; on **nullification** (ASN-0086) for addressability.
- **Shares its selection index with the discovery query** (`findlinks`, ASN-0127): one index, two read-outs — identities for `findlinks`, (slot, endset) for RETRIEVEENDSETS.
- **Relies on generalized referential integrity** (S3★, ASN-0047) and content allocation (ASN-0093 / 0036): the caller obligation `W ⊆ s_C` is what guarantees the region resolves into content and what the cross-subspace disjointness lemma (RE-NCD) buys.
- **Sits behind the API/FEBE boundary** as a read-only query and hands its answer to a client/UI that renders "this content is bound here." It hands to no store.

## Decisions for the builder

- **Whole-endset vs touching-spans** (mirrors the note's OQ1, but as a build choice): join back to the authoritative link store to recover full endsets (preserves union-distributivity, costs a lookup) vs return only the touching spans the index found (cheaper, region-dependent, breaks RE-UDIST). Pick whole-endset if you compose region queries.
- **Index lifecycle**: rebuild-by-replay (default) vs incrementally-maintained persistent value vs periodic checkpoint — driven by your startup-latency budget and whether you need concurrent or historical reads.
- **Index granularity**: per-span entries (cheap overlap, natural touching-spans) vs per-endset entries (one lookup yields the whole value).
- **Nullified set**: cached monotonic mark (default) vs recompute-on-read.
- **Endset equality for dedup**: the canonical form and hashing scheme for finite span-sets.
- **Region presentation**: a single span vs an arbitrary set of spans (Green accepts a multi-span, multi-document SpecSet). Whatever you choose must keep membership decidable — i.e., finitely presented.
- **Answer rendering** (the note's OQ3, but you must pick a wire format now): return the **content-identity answer** (I-addresses — the note's mode, permanent and clean) vs **render into the querying document's V-positions** (Green's mode). Rendering is a *separate, lossy layer*: it silently drops endset addresses the querying document no longer arranges (ghost-filtering) and can fragment a contiguous endset into multiple V-spans under reordering. Keep rendering layered *on top of* the content-identity answer — don't bake it into the core query, as Green effectively did.
- **Type-slot handling** (the note's OQ6, as a build choice): treat all slots uniformly and carry the "type coverage is disjoint from content" hypothesis (simplest, what the note does) vs special-case the type slot to guard against a wide type span that reaches content.
