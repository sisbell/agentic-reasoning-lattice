## Question 10 [theory]

> Must the extents reported for the separate parts be consistent with one another and with the document as a whole, and what would a violation of that consistency mean?

## Short answer

Yes. The extent reported for the document as a whole and the extents of its separate parts (text bytes vs. links) must be mutually consistent — the whole must account for exactly the parts, with no gaps and no orphans. A violation would mean the back end's index is corrupt: content that either exists but cannot be addressed, or is addressable but does not exist.

## What the operations report

Two FEBE operations report extents, and they report them at different granularities:

- **RETRIEVEDOCVSPAN** — "This returns a span determining the origin and extent of the V-stream of document `<doc id>`." (4/68) This is the whole-document extent.
- **RETRIEVEDOCVSPANSET** — "This returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." (4/68) This is the per-part breakdown.

So the single V-span (the whole) and the span-set (text-part + link-part) are two views of the same document. Internally these parts live in distinct subspaces of the document's address space: text bytes in the `1.x` (version.position) subspace and links in the `2.x` (`version.0.2.N`) subspace (see the links concept, 4/31). The whole-document extent must cover precisely those two regions.

## Why consistency is forced, not optional

Nelson's span definition makes the relationship structural rather than something the system separately tracks:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

Because what lies *between* the endpoints is implicit, the whole-document span's boundaries *determine* what parts it contains. The parts cannot independently disagree with the whole — the whole is defined by its extent, and the parts are what that extent resolves to.

This is reinforced by the Vstream density guarantee (per the curated v-space-addresses notes): V-addresses "always form a contiguous sequence starting at 1," and "if you have 100 bytes, you have addresses 1 through 100." If RETRIEVEDOCVSPANSET reports 100 characters and 5 links, the whole-document extent from RETRIEVEDOCVSPAN must resolve to exactly those 100 contiguous text positions plus 5 links — no more, no fewer.

This consistency is what Nelson calls the enfilade's *canonical order*, treated as a hard system rule rather than a nicety:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." (1/34)

## What a violation would mean

A mismatch between the whole and its parts would be an internal invariant breach, not a user error. Concretely:

1. **Orphaned content** — the part counts exceed what the whole extent covers, so some bytes or links exist in storage but fall outside the addressable V-stream. They cannot be retrieved or linked to.
2. **Phantom extent / gaps** — the whole extent claims more than the parts contain, so positions within the reported extent resolve to nothing. This breaks the density guarantee (no gaps in V-addressing) and breaks "part-pounce": "THE PART YOU WANT COMES WHEN YOU ASK FOR IT" (2/16) would fail, returning emptiness for an address the document claims to contain.
3. **Broken downstream guarantees** — since links attach to bytes and "survive editing … if any of the bytes are left to which a link is attached" (4/42), an extent that disagrees with the actual byte population would corrupt link survivability and the V→I mapping that the POOM enfilade maintains.

In short, the reported extents are different projections of one canonical structure; their agreement is the observable signature that the document's index is intact. Disagreement signals storage/index corruption.

---

A caveat on scope: Nelson specifies *what* RETRIEVEDOCVSPAN and RETRIEVEDOCVSPANSET return (4/68) and the structural nature of spans (4/25), but he does not, in the curated sources, give an explicit statement that the system *validates* whole-vs-part agreement or what it does on detecting a mismatch. My characterization of a "violation" as index corruption is inference from the canonical-order mandate (1/34) and the span/density semantics, not a verbatim rule. NEED_RAW: 4/68, 4/30-4/31 if you want me to confirm whether Nelson states an explicit validation/consistency check on these operations.
