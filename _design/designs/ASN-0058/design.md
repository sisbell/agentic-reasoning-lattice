## What this is

The arrangement-representation layer — the POOM. This note defines the *mapping block* as the atomic unit of V→I correspondence, the algebra by which a document's arrangement decomposes into blocks (split / merge / canonicalize), and *resolution*: turning a named V-span into the I-address runs that back it. It is the bridge between how a document is arranged (Vstream) and where its content permanently lives (Istream).

## Design commitments

These are forced on all downstream design:

- **The arrangement is the truth; the choice of block boundaries is free** (M3). M3 forces only representation-independence of the *decomposition*: any two block sets denoting the same (V, I) pairs are interchangeable, so block boundaries may be normalized or re-represented at will. The *mapping information* itself — the actual (V, I) pairs of `M(d)` — is authoritative wherever it is stored; absent a separately-designated durable form it lives *in* the POOM, and losing the POOM with no journal loses `M(d)`. Whether the live tree is merely a recomputable *hint* in Lampson's sense is contingent on the persistence choice below (designate an on-disk canonical set + journal as truth) — a builder decision, not a forced consequence.
- **A unique, history-free normal form exists** (M12 + M8). The maximally-merged decomposition is unique — independent of *merge* order, i.e. of which equivalent decomposition you start canonicalizing from; it is *not* independent of edit order, since `M(d)` itself depends on that — and *deliberately forgets* internal boundaries. So there is one canonical form that doubles as storage format and equality test; edit history/provenance is explicitly *not* recoverable from the POOM and must live elsewhere.
- **Mapping is unit-ratio, monotone, positional** (M0, M1). One V-position ↔ one I-byte; no compression, expansion, or transform; reversal requires multiple blocks. No transformation logic ever belongs in the mapping.
- **Width is coupled across both dimensions** (M0). V-width = I-width = n — one conceptual width, equal cardinality in both projections. M0 forces the *coupling* (no operation can change the unit ratio), not any particular storage; whether to hold it as one scalar count or two equal width tumblers is a representation choice (see approaches).
- **Origin rides in the I-address prefix; ordinal increment never crosses it** (M16a). *Every* block — not only canonical ones — is single-origin (M16b): by construction, not by enforcement — *given* M16a's standing precondition that the content store allocates element I-addresses as document-prefix extensions (T10a: each `a ∈ dom(C)` T4-valid, `zeros = 3`). Under a content store that hands out I-addresses without that prefix structure, M16/M16a/M16b break (see the input contracts under Guarantees).
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
- *Ordered index keyed by V-start*, each entry carrying the block's I-start and width. Point lookup is a predecessor search; resolution is a range scan. Simplest, and it honors V-ordering directly. Over a *persistent, structurally-shared* ordered map, readers are snapshot-consistent and lock-free, and a new version shares most nodes with its predecessor *across this note's surface* — split/merge/resolve never shift downstream V-positions. But absolute V-start tumbler keys make that sharing collapse under *edits*: a mid-document insert re-keys and re-creates every downstream block, so the edit is O(n) and an insert near the document start shares almost nothing with its predecessor version.
- *The enfilade* (Green's POOM): a 2-D (I × V) range tree carrying a cumulative width and displacement per dimension at each node. Its primary payoff is O(log n) bulk address-shifting on insert/delete — shift a whole downstream region by adjusting one ancestor's displacement, exactly the case the absolute-keyed ordered map does in O(n). Within-document I-indexed queries are a secondary benefit.
- **Pick:** the V-keyed ordered index is right *for this note's surface* — read, split, merge, resolve, none of which shift downstream V-positions. But the enfilade is warranted as soon as edits (insert/delete/copy) arrive — its justification is edit-time bulk shift, with within-document I-indexing only a secondary benefit. Global back-following — every document and V-position referencing a given content I-address — is a *separate, cross-document* structure (the spanfilade), which no single per-document enfilade delivers.

**Width.** Carry a scalar count plus the two start tumblers; coupling is then free, and `v+k` / `a+k` are single ordinal shifts — each applied at its *own* tumbler's depth (OrdinalShiftBase), so V-start and I-start may sit at different depths (`#v` need not equal `#a`; Green encodes the same integer count at different hierarchical depths). That differing-depth freedom is exactly why one scalar `n` advances both correctly. Green's enfilade instead carries a width tumbler in *each* dimension (the crum holds I- and V-width separately) and keeps them equal — faithful to the enfilade's cumulative-sum mechanics, but it stores the count redundantly. (Green's dual form does not drift: its coupling is held by *immutability* — no operation writes an existing crum's width fields — not by single-storage.) Choose the scalar unless you are committing to the full 2-D cumulative enfilade; storing the count once means there is no second copy to keep equal.

**Split.** Pure: drop one entry, insert two; the boundary tumblers are single ordinal shifts; structural sharing leaves the rest of the tree untouched.

**Merge / canonicalize.** Only *consecutive* (V-ordered) blocks can ever merge (no-overlap, plus canonical = the maximal runs), so canonicalization is a single linear coalescing pass, and it is confluent (M12) — order and parallelism are irrelevant to the result.
- *Eager local coalesce on edit* (check just the two neighbors of the touched point) keeps the structure always canonical at O(1) coalescing *beyond the edit's own O(log n) locate* — and only because the decomposition was canonical before the edit, so a new adjacency can appear only at the touched boundary. Recommended — it makes the common case fast. (This reasoning lives in the out-of-scope edit layer.)
- *Lazy global coalesce on snapshot/resolve* makes edits cheaper but pushes work onto resolution (which canonicalizes its slice anyway, per C1a).
- The bidimensional adjacency test alone is sufficient: I-adjacency already excludes both cross-origin (M16) and shared-I-extent (M14a) merges. As an optimization, compare origins first to short-circuit the full I-adjacency check — origin is a *prefix* of the I-address (Green encodes ownership exactly as a tumbler prefix, tested by prefix-match), so this is a verified-cheap pre-filter, not extra stored state.

**Resolution.** A well-formed content reference is necessarily an *ordinal* displacement (C0): its action point equals its depth `m`, so the resolve input reduces to `(start u, scalar count ℓₘ)` at depth `m` — the same (start, scalar-count) shape as a block, not an arbitrary span. Range-scan the V-span; clip the first and last blocks to the span boundary *on the output only* (never mutate the store — a read stays pure and snapshot-consistent). Validate well-formedness (the span range is fully covered) as a precondition, or treat it as a caller contract. Width preservation (C2) is a cheap postcondition assert. Composite resolution is per-document and independent (M15) — embarrassingly parallel; just preserve sequence order on concatenation (the note leaves cross-reference reordering open, so do not rely on it).

**Persistence / recovery.** The canonical block set is the unique compact serialization (M12) — make it both the on-disk format and the equality test, and (this being the choice that makes it so) treat the live tree as a derived hint. For durability between snapshots, keep an append-only journal of arrangement writes (Green's permascroll/granfilade is the analogous append-only substrate for the content itself), replayed on load and then canonicalized; periodic snapshots of the canonical set bound replay length. Replay must preserve journal order — M12's order-independence governs *merge* order on a fixed arrangement, not the order of journal *edits*; insert/delete/copy do not commute (cf. M15's byte deletion), so replaying them out of order yields a different `M(d)`. Partial-tail robustness comes instead from append-only writes with atomic records; canonicalizing after replay remains correct (and order-independent in the M12 sense).

**Multi-subspace layout.**
- *One POOM per document, subspace by leading digit* (Green): a single object, but edits must not disturb sibling subspaces — Green needs explicit isolation machinery (the two-blade "knife" guards sibling-subspace entries living in the same tree).
- *One POOM per (document, subspace)*: isolation is structural and free, at the cost of more objects and cross-subspace coordination.
- Resolution is per-subspace regardless and edit-time isolation is the hard part, so per-subspace trees look like the simpler thing for a fresh build — *but the "unless you need atomic cross-subspace edits" caveat is the actual driver behind Green's unified tree, not a rare exception*. Link creation — a core Xanadu operation — writes from/to/three endpoints into one link POOM and writes the link-reference subspace of the document POOM; Green unified the tree (with the knife for isolation) precisely to make those cross-subspace writes atomic in one structure. So weight cross-subspace atomicity first — in practice, are you building links? — and default to per-subspace trees only if you are not.

## Guarantees to uphold

By construction:
- **Functionality (S2)** — one I-address per V-position: holds as long as coverage stays a disjoint partition (B1 + B2).
- **Width coupling (M0), in-block order (M1)** — from scalar width + monotone shift.
- **Content permanence/immutability** — upstream (append-only content store); the POOM only re-points, never rewrites content.
- **Origin traceability and cross-origin non-merge (M16a/b, M16)** — from tumbler-prefix arithmetic, *given* the upstream prefix-allocation input contract below; absent that contract they break.
- **Transclusion independence (M14)** — merge requires I-disjointness; never dedup by I.
- **Document independence (M15)** — per-document object, framed operations.

Requires active enforcement:
- **Canonical uniqueness (M12)** — you must actually run canonicalization to hold the stored form in normal form; otherwise it is only derivable, not maintained.
- **Resolution integrity (C1)** — holds only if blocks never reference dead content; referential integrity (S3) is an input contract on whatever writes the POOM, enforced at the edit boundary.
- **Element I-addresses extend the document prefix (M16a's T10a precondition)** — an input contract on the *upstream allocator*, alongside S3, not enforced in the POOM: the content store must allocate each element I-address as a document-prefix extension (T4-valid, `zeros = 3`). The origin guarantees (M16a/b, M16) are by construction *only given* this. It does not propagate for free — in Green it holds because `tumblerincrement` builds element ISAs by extending the document ISA, but the discipline must actually hold at element allocation; a content store without prefix structure breaks the cross-origin guarantee.

## How it fits

- **Leans on ASN-0034** (tumbler algebra): the `+k` ordinal shift, lexicographic order, and origin-as-prefix that make blocks, monotonicity, and cross-origin non-merge work at all.
- **Leans on ASN-0036** (the arrangement `M(d)`): S2 functionality, S3 referential integrity, S5 unbounded sharing, S8 correspondence-run partition (M2 *is* S8 restated), S8a/S8-depth well-formedness. This note is the algebra *of* `M(d)`.
- **Leans on ASN-0053** (span algebra): content references are level-uniform V-spans; `reach(σ)`, level-uniformity, and the split↔S4 / merge↔S3 analogy — though merge maps only to S3's *adjacent-only* sub-case (M7 forbids the overlap that general S3 admits).
- **Hands to**: the retrieval/display layer (resolve → I-runs → read bytes from the content store); the operation layer (insert/delete/copy drive split/merge); the spanfilade / back-reference index (a sibling structure keyed by I, out of scope here).
- **Upstream**: the content store `C` (Istream / permascroll / granfilade) that I-addresses point into.

## Decisions for the builder

- **Store shape**: V-keyed ordered index vs. full 2-D enfilade — this decides *edit-time* cost (the enfilade does mid-document insert/delete by O(log n) bulk shift where the absolute-keyed ordered map is O(n)) and, secondarily, whether *within-document* I-indexed queries are cheap later (global back-following is the separate spanfilade either way).
- **Width representation**: scalar count vs. dual per-dimension tumblers. (Open per the note: whether the tumbler-depth relationship between a block's V-start and I-start is constrained at all — the scalar form assumes nothing about it.)
- **Canonicalization timing**: eager local coalesce on edit vs. lazy on snapshot/resolve.
- **What is durable**: a canonical-block snapshot as truth, vs. an edit journal replayed into a derived POOM, vs. both (snapshot + tail journal).
- **Subspace layout**: one unified per-document tree (needs isolation machinery) vs. per-subspace trees (free isolation, more objects).
- **Multi-source resolution**: whether to exploit per-reference parallelism, and whether cross-reference order may be relaxed (the note leaves this open — default to preserving sequence order).
- **Boundary handling in resolution**: clip on the output vs. transiently split-and-restore — clip-on-output is simpler and keeps reads pure.
