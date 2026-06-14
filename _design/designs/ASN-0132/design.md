## What this is

The link-census **count** operation, `FINDNUMOFLINKSFROMTOTHREE`: given a four-set link description `q = (H, F, G, Θ)` — home, from, to, type — return how many distinct links in the store match it. It is the cardinality-only sibling of the enumeration operation (ASN-0121): identical matching criterion, returns a number instead of the links.

## Design commitments

These are the locks downstream design cannot violate. I mark each *forced* (by the spec) versus *conventional*.

- **The count is the cardinality of a *set* of link identities, never a tally of matches.** One satisfying link contributes exactly `1` regardless of how many spans its endsets seize, how many documents transclude its content, or how many places it surfaces. *Forced* (CN-UNIT, CN-DEF). Consequence: any realization that can emit one identity twice is wrong.
- **It is a pure observation — reads `Σ`, writes nothing, and no state component records a count.** *Forced* (CN-DEF, CN-SNAP). "The count" exists only as the result of evaluating it now; it is not a stored quantity.
- **The answer is a function of the link store `Σ.L` alone.** Content, arrangements, entities, provenance never move the number. *Forced as a theorem* (CN-LOC) — but it imposes a prohibition the builder must honor: do not let those components leak into the count. Folding arrangement-resolution into the operation changes its meaning (see Guarantees).
- **It counts the active view, `addressable = dom(Σ.L) \ nullified`.** Retracted links are excluded immediately and permanently while persisting in the store (*forced*, CN-RETRACT); orphaned links — matching, addressable, surfaced nowhere — are counted (*forced*, CN-ORPHAN). This is an **existence** census, not a reachability one.
- **The matching predicate `sat` is shared with enumeration; count = |enumeration| at one state.** *Forced* (CN-ENUM). There must be exactly one definition of "matches," consumed by both.
- **The count is a snapshot of the instant taken; recompute-on-read, not cache-as-truth.** *Forced at the state level* (CN-SNAP). A cache is permitted, but it is a hint, not state.
- **Only link creation/retraction (a `K.λ` step) can change the count.** Content insert/delete/rearrange leave it invariant. *Forced* (CN-STAB, CN-MONO). This tiny invalidation surface is what makes caching cheap.
- **The request arrives already phrased over addresses.** Resolving a reader's content-pointings into address sets (V→I, against the live arrangement) is upstream and not part of this operation. *Forced by framing* — and load-bearing for orphan semantics.

## What must be built

- A shared evaluator for `sat(a, q, Σ)`: the AND-of-ORs over four slots, with **coverage-overlap** (`touch`) for from/to/three and **home-prefix membership** (`athome`) for the home slot, wildcards dropping out. The home slot is structurally different — a membership test on the address *projection* `home(a)`, not an endset overlap — and must be *genuinely* evaluated, reading `home(a)` off the permanent address rather than from arrangement presence: a reverse-orphaned link (its own home-arrangement entry deleted) still satisfies a home-bounded `q`, so **do not implement the home filter as an arrangement-presence test** — that would silently violate CN-LOC and CN-STAB. (Green's home filter fails the other way: dead-coded off via a `TRUE||` guard, so its "home-bounded" counts are not actually home-bounded — a cautionary deviation, not a model.)
- A way to determine the active view: `dom(Σ.L)` minus `nullified` (links covered by a retraction tuple).
- A way to produce the result as a **distinct-by-address cardinality** — set semantics, dedup guaranteed.
- A recompute path that re-evaluates against the live state on every call (the contract baseline).
- Optionally, candidate-narrowing indexes so the operation need not scan the whole store.

## Implementation approaches

**1. Evaluating the count — scan vs. index.**
- *Full scan of `Σ.L`*: for each address evaluate `sat`, filter to `addressable`, accumulate into a set, take its size. Always correct, O(|L|), zero index maintenance, trivially correct after recovery. This is the *simplest* contract-faithful baseline — though it is not what Green does; Green indexes (next bullet). Simple and proven-correct, but it examines every link to answer "how many."
- *Per-slot coverage index*: maintain indexes mapping endset-coverage → link addresses (from/to/three) plus a home-prefix index over the address projection. A constrained slot yields candidates whose endset touches its coverage; intersect across constrained slots, subtract `nullified`, count. This is exactly Green's **spanfilade** — an enfilade (range tree over tumbler space) with from/to/three sub-indices — a proven structure. It *could* make counting cheaper than enumeration, but Green exploits no such asymmetry: its count runs this indexed search to full materialization and then *walks the resulting list*, so counting costs exactly as much as enumerating. The index is a *hint*: rebuildable, and it must stay consistent with `Σ.L`. The natural analog is a persistent ordered map keyed by tumbler with range scans, or a tumbler-prefix trie (closest to the enfilade, since tumblers are hierarchical/prefix-ordered).
- *Pick*: build the scan first — it *is* the contract. Add the per-slot index only when query volume justifies it, and keep it as a rebuildable hint, never the source of truth. (This build-order is the builder's choice, not a model of Green: Green's spanfilade was present from the start, not bolted onto a prior scan.)

**2. Dedup / identity semantics — the load-bearing choice.**
The spec is a set cardinality. Green realized it as a list walk over a deduplication routine with an off-by-one (it never checks the list's last element), so a link whose endset is fragmented across two or more matching address regions is counted **twice** — a documented deviation from CN-UNIT. The fix is structural, not a patch: materialize candidates into a set keyed by link address before taking size. With a persistent/hash set keyed by address, dedup is idempotent and free — "2 for one identity" becomes impossible by construction, and it directly answers the note's open question 4. **Do not count by walking a list.**

**3. The active view (`nullified`).**
`nullified` is derived from the retraction relation inside `Σ.L` and only grows (R6a). Either recompute it from the retraction tuples each query (simple, O(retractions)), or maintain it as a derived set appended to on each retraction step — monotone growth makes incremental maintenance safe, and it is a hint rebuildable by replay. Maintain it if retractions are frequent; otherwise recompute. Apply it as a filter before taking cardinality.

**4. The all-wildcard fast path.**
`q* = (∗,∗,∗,∗)` counts the whole active view, `|addressable|`. A running cardinality makes `q*` O(1) — but maintain it correctly: increment for every freshly created *addressable* link (ordinary *or* retraction — a retractor is itself addressable unless it self-nullifies, and is counted under `q*`), and decrement for every link newly moved into `nullified` (a retraction's targets). A retraction step does both — `+1 − k`, net `0` in the common single-target case. The naïve "up on creation, down on retraction" rule drops the retractor and drifts low by one per retraction. `q*` is the trivial active-view-size boundary case, cheap to special-case.

**5. Caching a count (answers open question 3 structurally).**
CN-STAB + CN-MONO say a count changes *only* on a `K.λ` step, so a cached count is valid across any transition that neither creates nor retracts a link. Cheapest correct mechanism: a global **link-store epoch** bumped on every `K.λ`; cache entries tagged with the epoch at compute time; on read, epoch match ⇒ the cached number is still the true cardinality, epoch miss ⇒ recompute. This treats the cache as a Lampson hint — recomputable on miss, never authoritative — exactly what CN-SNAP demands. Per-query invalidation (test whether the created/retracted link satisfies `q`) buys precision at real complexity cost; the global epoch is the simple thing and usually enough.

**6. Cost asymmetry (open question 5).**
The spec fixes the value, not the cost. Green pays full enumeration cost to answer "how many" (the indexed path above). A builder is free to make count cheaper (a counting index, or maintained aggregate counts per region) **because CN-OBT says the count need not deliver the links**. This is the "make the common case fast" move; weigh it against maintenance cost and the snapshot-invalidation discipline above.

**7. Persistence and recovery.**
The operation writes nothing, so it needs no journal of its own; the durable thing is the link store. The standard approach is to journal link creations and retractions to an append-only log and recover by replay — and the layers here are not all alike. The **log is durable**, the authoritative record. The **in-memory link store `Σ.L` is its working materialization**: authoritative working state, rebuilt by replay on load, but not a *hint*. The `nullified` set, the per-slot indexes, and any count cache are the **discardable accelerators** — genuine hints, derived, rebuildable, never the source of truth. Nothing about the count survives a restart; it is recomputed.

## Guarantees to uphold

- **Identity uniqueness** (count = distinct addresses): requires **active enforcement** — dedup by address. Free with set semantics; broken by list/multiset walks (Green's off-by-one). The one to watch.
- **No mutation / frame = Σ**: by construction if the operation only reads.
- **Locality (function of `Σ.L`)**: by construction *if you consult only the link store*. The subtle trap: if your only query channel is content-pointing resolved through current arrangements (as Green's is), a deeply-orphaned link — endpoint content removed from every arrangement — becomes unreachable, because resolution collapses the request to empty coverage. That returns `0`, but it is the **empty-request** zero (the request names nothing), not the **empty-store** zero (no such link exists) — and the spec is explicit these differ in meaning though not in the number. To preserve the existence census in practice, offer an **address-direct** query path so a caller can name permanent endset addresses the arrangements no longer surface.
- **Zero is a store verdict, not an exhaustion artifact (CN-ZERO)**: a returned `0` asserts that *no addressable link satisfies `q`*, decided over the whole addressable store — not that the search gave up amid irrelevant links. Non-impedance (FL-JUNK) means junk volume cannot displace a match; the full-scan baseline holds this by construction, and an indexed path must not early-bail or heuristically narrow in any way that could skip a satisfying link among non-matching ones. (The "nothing displayed" misreading is excluded by Locality; the empty-request vs. empty-store split is handled there.)
- **Active-view correctness**: exclude `nullified` (active enforcement); include orphans (free, *provided* indexes key on stored endset addresses, not on arrangement-reachable content).
- **Count = |enumeration| at one state**: by construction if both share `sat` and both yield a set. Holding it *across two separate calls* is **not** free — it needs a shared snapshot (see concurrency, below).
- **Snapshot / present-tense**: by construction under recompute; under caching, requires correct epoch invalidation.
- **Each counted identity is a permanent handle (CN-OBT)**: by construction from address permanence. The count warrants `N` durable handles "in principle," not on-demand delivery — keep delivery a separate operation.

## How it fits

- Sits directly atop the **four-set matching machinery** (ASN-0121): the request shape `q`, `sat`, `lift`/`touch`/`liftH`/`athome`, `addressable`, and the enumeration `findlinks_FTT`. The count is a thin observer — `|findlinks_FTT|` — and must reuse the same `sat`.
- Leans on the **retraction model** (ASN-0086) for the active view and the monotone `nullified` set; on **address permanence/finiteness** (ASN-0093) for well-definedness and CN-OBT's durable handles; on **coverage/home/L12** (ASN-0043) for the geometry of matching; and on **link-store preservation** (F-PRES, ASN-0127) for stability under editing, inheriting ASN-0127's present-tense reading of a zero.
- Deliberately does **not** use **discoverability** (ASN-0098) — it names `discoverable_from` only to exclude it.
- **Single-store scope.** This counts one store's `Σ.L` (the note's single-`Σ` framing). A *federated* count — a single four-set cardinality reflecting links homed in independently administered stores other than the one receiving the inquiry — is a separate, open design (note open question 6), not addressed here.
- **Upstream**: a front-end resolution layer turns content-pointings into the address sets of `q`. **Downstream**: a delivery/enumeration boundary (CN-OBT) fetches the actual links when asked.
- Placement: a read-side query in the link-census family, sibling to enumeration (ASN-0121) and the discovery census (ASN-0127), at the top of the read path over the link store.

## Decisions for the builder

(Distinct from the note's spec-level open questions, though several touch them.)

- **Scan or index, and which index.** Full scan (contract baseline) vs. spanfilade-style per-slot coverage index; if indexing, enfilade/tumbler-trie vs. persistent ordered map with range scan. You decide the structure and the fall-back-to-scan threshold.
- **How you guarantee distinct-by-identity.** Set materialization vs. streaming distinct-count — pick one that *cannot* emit a duplicate. The result is non-negotiable; the mechanism is yours.
- **`nullified`: maintain incrementally or recompute.**
- **Whether to carve out the all-wildcard fast path** with a running active-view cardinality.
- **Caching policy:** none vs. epoch-tagged hint, and invalidation granularity (global epoch vs. per-query). Decide whether to cache at all.
- **Cost target:** accept count-costs-like-enumeration (simple) or invest in a count-cheaper path (counting index), since delivery isn't required.
- **Query channel and zero disambiguation:** whether to expose an address-direct query path alongside content-pointing (needed to count deeply-orphaned links), and whether to signal request-degeneracy out of band so an empty-request zero is distinguishable from an empty-store zero.
- **Concurrency exposure:** whether to offer a snapshot/epoch token a caller passes to both a count and a later enumeration so the pair observes one state. The drastic alternative Green took — disabling count entirely in multi-session mode — is a reminder that "accept the race" is itself a choice; make it deliberately.
