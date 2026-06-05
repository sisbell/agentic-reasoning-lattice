## Question 1 [theory]

> Is the document's origin intended to be a permanent anchor at the content start for the document's life, or is it the minimum occupied V-position — such that fully deleting content while links survive legitimately moves the reported origin into link space?

I was unable to access the raw page scans in this environment (the `resources/literary-machines/raw/` files returned empty), so my answer rests on the verified curated extractions. I flag one spot where the raw wording would help confirm.

## Short answer

Nelson's design intent points to **a permanent structural anchor at the document's content start**, not a floating "minimum occupied V-position." Fully deleting the text while links survive should **not** legitimately migrate the reported origin into link space. That interpretation would conflate two architecturally distinct subspaces and break the contract the operation exists to serve.

## Why

**1. "V-stream" means the byte stream specifically — links are a separate subspace.**

`RETRIEVEDOCVSPAN` is defined narrowly: "This returns a span determining the origin and extent of the V-stream of document `<doc id>`." (4/68). Nelson consistently uses "V-stream" / "virtual byte stream" to mean the *text* arrangement: "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11). Links are not bytes in that stream — they live in their own document-local subspace:

```
version.position   → bytes (1.x subspace)
version.0.2.N      → links (2.x subspace)
```

So "origin of the V-stream" is the origin of the *byte* content. The link subspace is not part of what this operation measures, which is precisely why an emptied byte stream should report a zero-extent byte span at the content origin — not a span re-anchored onto a surviving link.

**2. The sibling operation proves bytes and links are reported as distinct quantities, not a single merged range.**

`RETRIEVEDOCVSPANSET` "returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." (4/68). The architecture deliberately reports text-count and link-count as *separate* components of a span-*set*. If the system models text and link extents as distinct measurements, then `RETRIEVEDOCVSPAN`'s single span is not meant to be a min-occupied→max-occupied sweep that crosses from byte space into link space. Surviving links are surfaced through the link component / link-search, not by relocating the byte-stream origin.

**3. Byte space and link space have incompatible ordering semantics — merging them under one floating origin is architecturally unsound.**

Bytes are dense and rearrangeable in V-space: "The digit after the one indicates the byte position in the current ordering of bytes... Note that this order may be continually altered by editorial operations." (4/30). Links, by contrast, are fixed: "The links designated by a tumbler address are in their permanent order of arrival." (4/31). A "minimum occupied position" origin that can sit in either subspace would have to span two regions with different mutability rules under one boundary — exactly the kind of conflation Nelson keeps separate via the 1.x / 2.x distinction.

**4. Deletion does not destroy the document's positional frame; it empties the arrangement.**

Deleted bytes leave the V-arrangement but remain in Istream: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9). The document still exists with its content frame intact; an emptied text stream is legitimately a zero-extent span at the content origin. Nelson's "1-position" convention gives a fixed, occupancy-independent way to name that frame — "A digit of 'one' may be used to designate... all elements in a given version" (4/38) — reinforcing that the document's content origin is a structural designator, not a probe of what currently happens to be occupied.

**5. The purpose of the operation depends on a stable byte-space origin.**

A front end calls `RETRIEVEDOCVSPAN` to learn where the document's text lives and how long it is, so it can then issue byte-retrieval requests (`RETRIEVEV`) against that range. If the origin floated into link space on full deletion, the front end would compute text requests against link addresses — defeating the operation's role.

## The counter-argument, and why it's weaker

One could lean on the pure span abstraction — "A span that contains nothing today may at a later time contain a million documents... There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25) — to argue a span is simply first-occupied to last-occupied, so a migrating origin is "just span mechanics." But that describes *how to represent* a range; it does not establish *what* `RETRIEVEDOCVSPAN` measures. The measured thing is the byte V-stream (points 1, 2, and 4 above), so the span-occupancy rule should be applied *within* the byte subspace, not across the byte→link boundary.

## Caveat / verification gap

Nelson does not explicitly adjudicate the exact edge case — "all bytes deleted, links survive, what does `RETRIEVEDOCVSPAN` report as origin?" My conclusion is an inference from (a) the byte-stream meaning of "V-stream," (b) the separate text/link reporting in `RETRIEVEDOCVSPANSET`, and (c) the 1.x/2.x subspace separation. The pivotal unverified point is whether `RETRIEVEDOCVSPAN`'s single span is ever intended to *encompass* links at all; the one-line gloss at 4/68 does not fully disambiguate.

NEED_RAW: 4/68 (precise wording of RETRIEVEDOCVSPAN / RETRIEVEDOCVSPANSET and any surrounding note on whether the doc-vspan covers links), and 4/30–4/32 (byte vs. link subspace layout) to confirm the byte-only reading of "origin and extent of the V-stream."
