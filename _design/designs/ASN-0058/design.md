## What this is

The arrangement-representation layer — the POOM. This note defines the *mapping block* as the atomic unit of V→I correspondence, the algebra by which a document's arrangement decomposes into blocks (split / merge / canonicalize), and *resolution*: turning a named V-span into the I-address runs that back it. It is the bridge between how a document is arranged (Vstream) and where its content permanently lives (Istream).

## Design commitments

These are forced on all downstream design:

- **The arrangement is the truth; the choice of block boundaries is free** (M3). M3 forces only representation-independence of the *decomposition*: any two block sets denoting the same (V, I) pairs are interchangeable, so block boundaries may be normalized or re-represented at will. The *mapping information* itself — the actual (V, I) pairs of `M(d)` — is authoritative wherever it is stored; absent a separately-designated durable form it lives *in* the POOM, and losing the POOM with no journal loses `M(d)`. Whether the live tree is merely a recomputable *hint* in Lampson's sense is contingent on the persistence choice below (designate an on-disk canonical set + journal as truth) — a builder decision, not a forced consequence.
- **A unique, history-free normal form exists** (M12 + M8). The maximally-merged decomposition is unique, independent of edit order, and *deliberately forgets* internal boundaries. So there is one canonical form that doubles as storage format and equality test; edit history/provenance is explicitly *not* recoverable from the POOM and must live elsewhere.
- **Mapping is unit-ratio, monotone, positional** (M0, M1). One V-position ↔ one I-byte; no compression, expansion, or transform; reversal requires multiple blocks. No transformation logic ever belongs in the mapping.
- **Width is a single count, coupled across both dimensions** (M0). V-width = I-width = n. Store the count once and the coupling holds by construction.
- **Origin rides in the I-address prefix; ordinal increment never crosses it** (M16a). *Every* block — not only canonical ones — is single-origin (M16b): by construction, not by enforcement.
- **Transclusion is first-class, unbounded, and its occurrences are permanently independent** (M13, M14). The same I-extent at multiple V-positions is multiple blocks; *never dedup or coalesce by I-address*.
- **Documents are independent** (M15). Each POOM is its own object; split/merge name and touch only the one decomposition.
- **Resolution is V-ordered and drops V-coordinates** (C1b, C2). Output order is by V-start (not I-value), and total width is preserved.

Merely conventional: subspace-by-leading-tumbler-digit in one tree (Green's choice) versus per-subspace trees — resolution is per-subspace either way.

## What must be built

Functionally (not as types):

- **A per-document arrangement store (the POOM)** — holds the V→I mapping as a block decomposition; answers point lookup `M(d)(v)` and ordered iteration over a V-span.
- **Split** — given a block and an interior cut, yield two blocks denoting the same pairs.
- **Merge** — given two blocks that are both V-adjacent and I-adjacent, combine into one.
- **Canonicalize (coalesce)** — reduce any decomposition to the unique maximally-merged form.
- **Resolve** — given a document and a level-uniform V-span (by C0 necessarily an ordinal displacement: a start position plus a scalar count at depth `m`), return the I-runs `(a, n)` in V-order that cover the span; concatenate per-reference for composite resolution over a reference sequence.
- **A subspace-scoped V-range selector** — resolution restricts to a single subspace.

Edits (insert/delete/copy) are *not* in this note — they are the operation layer. This note's surface is store + split + merge + canonicalize + resolve.

## Implementation approaches

**The store.**
- *Ordered index keyed by V-start*, each entry carrying the block's I-start and width. Point lookup is a predecessor search; resolution is a range scan. Simplest, and it honors V-ordering directly. Realized over a *persistent, structurally-shared* ordered map, each document *version* shares nodes with its predecessor — cheap versioning (central to Xanadu) and snapshot-consistent, lock-free readers.
- *The enfilade* (Green's POOM): a 2-D (I × V) range tree carrying a width and displacement per dimension at each node. It earns its complexity only when you also need I-indexed queries (within a single document).
- **Pick:** the V-keyed ordered index for the POOM itself — forward resolution needs only V-keying. A 2-D enfilade buys *within-document* I-indexed queries, so build it when intra-document I-lookups come into scope. Global back-following — every document and V-position referencing a given content I-address — is a *separate, cross-document* structure (the spanfilade), which no single per-document enfilade delivers.

**Width.** Carry a scalar count plus the two start tumblers; coupling is then free, and `v+k` / `a+k` are single ordinal shifts — each applied at its *own* tumbler's depth (OrdinalShiftBase), so V-start and I-start may sit at different depths (`#v` need not equal `#a`; Green encodes the same integer count at different hierarchical depths). That differing-depth freedom is exactly why one scalar `n` advances both correctly. Green's enfilade instead carries a width tumbler in *each* dimension (the crum holds I- and V-width separately) and keeps them equal — faithful to the enfilade's cumulative-sum mechanics, but it stores the count redundantly. (Green's dual form does not drift: its coupling is held by *immutability* — no operation writes an existing crum's width fields — not by single-storage.) Choose the scalar unless you are committing to the full 2-D cumulative enfilade; storing the count once means there is no second copy to keep equal.

**Split.** Pure: drop one entry, insert two; the boundary tumblers are single ordinal shifts; structural sharing leaves the rest of the tree untouched.

**Merge / canonicalize.** Only *consecutive* (V-ordered) blocks can ever merge (no-overlap, plus canonical = the maximal runs), so canonicalization is a single linear coalescing pass, and it is confluent (M12) — order and parallelism are irrelevant to the result.
- *Eager local coalesce on edit* (check just the two neighbors of the touched point) keeps the structure always canonical at O(1) per edit. Recommended — it makes the common case fast.
- *Lazy global coalesce on snapshot/resolve* makes edits cheaper but pushes work onto resolution (which canonicalizes its slice anyway, per C1a).
- The bidimensional adjacency test alone is sufficient: I-adjacency already excludes both cross-origin (M16) and shared-I-extent (M14a) merges. As an optimization, compare origins first to short-circuit the full I-adjacency check — origin is a *prefix* of the I-address (Green encodes ownership exactly as a tumbler prefix, tested by prefix-match), so this is a verified-cheap pre-filter, not extra stored state.

**Resolution.** A well-formed content reference is necessarily an *ordinal* displacement (C0): its action point equals its depth `m`, so the resolve input reduces to `(start u, scalar count ℓₘ)` at depth `m` — the same (start, scalar-count) shape as a block, not an arbitrary span. Range-scan the V-span; clip the first and last blocks to the span boundary *on the output only* (never mutate the store — a read stays pure and snapshot-consistent). Validate well-formedness (the span range is fully covered) as a precondition, or treat it as a caller contract. Width preservation (C2) is a cheap postcondition assert. Composite resolution is per-document and independent (M15) — embarrassingly parallel; just preserve sequence order on concatenation (the note leaves cross-reference reordering open, so do not rely on it).

**Persistence / recovery.** The canonical block set is the unique compact serialization (M12) — make it both the on-disk format and the equality test, and (this being the choice that makes it so) treat the live tree as a derived hint. For durability between snapshots, follow this repo's own substrate: an append-only journal of arrangement writes (the `links.jsonl` + `paths.json` model; Green's permascroll/granfilade for the content itself), replayed on load and then canonicalized; periodic snapshots of the canonical set bound replay length. Replay must preserve journal order — M12's order-independence governs *merge* order on a fixed arrangement, not the order of journal *edits*; insert/delete/copy do not commute (cf. M15's byte deletion), so replaying them out of order yields a different `M(d)`. Partial-tail robustness comes instead from append-only writes with atomic records; canonicalizing after replay remains correct (and order-independent in the M12 sense).

**Multi-subspace layout.**
- *One POOM per document, subspace by leading digit* (Green): a single object, but edits must not disturb sibling subspaces — Green needs explicit isolation machinery (the two-blade "knife" guards sibling-subspace entries living in the same tree).
- *One POOM per (document, subspace)*: isolation is structural and free, at the cost of more objects and cross-subspace coordination.
- Since resolution is per-subspace regardless and edit-time isolation is the hard part, per-subspace trees are the simpler thing for a fresh build — unless you need atomic edits spanning subspaces.

## Guarantees to uphold

By construction:
- **Functionality (S2)** — one I-address per V-position: holds as long as coverage stays a disjoint partition (B1 + B2).
- **Width coupling (M0), in-block order (M1)** — from scalar width + monotone shift.
- **Content permanence/immutability** — upstream (append-only content store); the POOM only re-points, never rewrites content.
- **Origin traceability and cross-origin non-merge (M16a/b, M16)** — from tumbler-prefix arithmetic.
- **Transclusion independence (M14)** — merge requires I-disjointness; never dedup by I.
- **Document independence (M15)** — per-document object, framed operations.

Requires active enforcement:
- **Canonical uniqueness (M12)** — you must actually run canonicalization to hold the stored form in normal form; otherwise it is only derivable, not maintained.
- **Resolution integrity (C1)** — holds only if blocks never reference dead content; referential integrity (S3) is an input contract on whatever writes the POOM, enforced at the edit boundary.
- **Resolution width preservation (C2)** — a checkable postcondition.

## How it fits

- **Leans on ASN-0034** (tumbler algebra): the `+k` ordinal shift, lexicographic order, and origin-as-prefix that make blocks, monotonicity, and cross-origin non-merge work at all.
- **Leans on ASN-0036** (the arrangement `M(d)`): S2 functionality, S3 referential integrity, S5 unbounded sharing, S8 correspondence-run partition (M2 *is* S8 restated), S8a/S8-depth well-formedness. This note is the algebra *of* `M(d)`.
- **Leans on ASN-0053** (span algebra): content references are level-uniform V-spans; `reach(σ)`, level-uniformity, and the split↔S4 / merge↔S3 analogy — though merge maps only to S3's *adjacent-only* sub-case (M7 forbids the overlap that general S3 admits).
- **Hands to**: the retrieval/display layer (resolve → I-runs → read bytes from the content store); the operation layer (insert/delete/copy drive split/merge); the spanfilade / back-reference index (a sibling structure keyed by I, out of scope here).
- **Upstream**: the content store `C` (Istream / permascroll / granfilade) that I-addresses point into.

## Decisions for the builder

- **Store shape**: V-keyed ordered index vs. full 2-D enfilade — this decides whether *within-document* I-indexed queries are cheap later (global back-following is the separate spanfilade either way).
- **Width representation**: scalar count vs. dual per-dimension tumblers. (Open per the note: whether the tumbler-depth relationship between a block's V-start and I-start is constrained at all — the scalar form assumes nothing about it.)
- **Canonicalization timing**: eager local coalesce on edit vs. lazy on snapshot/resolve.
- **What is durable**: a canonical-block snapshot as truth, vs. an edit journal replayed into a derived POOM, vs. both (snapshot + tail journal).
- **Subspace layout**: one unified per-document tree (needs isolation machinery) vs. per-subspace trees (free isolation, more objects).
- **Multi-source resolution**: whether to exploit per-reference parallelism, and whether cross-reference order may be relaxed (the note leaves this open — default to preserving sequence order).
- **Boundary handling in resolution**: clip on the output vs. transiently split-and-restore — clip-on-output is simpler and keeps reads pure.
