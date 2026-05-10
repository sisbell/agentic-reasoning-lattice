# Consultation Answers — Arrangements

**Inquiry:** What structural properties does a document's arrangement have? How do contiguous mappings decompose, and what invariants govern the shape of the arrangement domain?
**Date:** 2026-03-19 22:31
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> Must every document's content occupy a single unbroken sequence of positions, or can a document's address space contain gaps where no content exists?

### Nelson's Answer

The answer depends on which address space you mean. Xanadu has two, and they behave differently.

---

## V-Space: No Gaps — Always a Contiguous Stream

A document's **virtual byte stream** (V-space) is always a single unbroken sequence with no gaps. Nelson consistently describes it as a "stream" with ordinal positions:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

The editing operations confirm this — they maintain contiguity structurally:

- **INSERT**: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66] — Insertion shifts everything after it; no gap is created.
- **DELETEVSPAN**: "This removes the given span from the given document." [LM 4/66] — Deletion closes the gap; remaining bytes renumber to stay contiguous.

If a document has 100 bytes, V-addresses run 1 through 100 with no holes. Delete bytes 20–30 and you have 89 bytes at addresses 1 through 89.

---

## I-Space: Permanent, Append-Only — No Gaps by Construction

A document's native content in I-space is stored append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Since content is only appended, never overwritten or removed, the I-space addresses for a document's native bytes form a contiguous, growing sequence. There are no gaps because nothing is ever removed from I-space — "deleted" content merely loses its V-space mapping:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

---

## Tumbler Address Space: Gaps Are Normal and Expected

At the broader level of the tumbler address space — spanning servers, accounts, documents — gaps are the norm, not the exception. Nelson explicitly defines **ghost elements**:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "The docuverse is the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it." [LM 4/23]

And spans can cover empty regions:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

So the docuverse-wide address space is inherently sparse.

---

## Link Subspace: Gaps Possible After Deletion

One subtle case: links within a document occupy the `0.2.N` subspace and are numbered by **permanent order of arrival**:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

Unlike bytes (which renumber in V-space when edited), link addresses are permanent. If you delete link `0.2.5`, links `0.2.6` through `0.2.N` do not renumber. The gap in the link numbering persists — that address becomes a "deleted link" awaiting historical backtrack, analogous to deleted bytes in I-space.

---

## Summary

| Address Space | Gaps? | Why |
|---|---|---|
| **V-Space** (virtual byte stream) | **Never** | Insert shifts; delete closes gaps. Always a contiguous stream. |
| **I-Space** (native content) | **Never** | Append-only; nothing is removed. |
| **Tumbler space** (docuverse-wide) | **Always** | Ghost elements; address space is sparse by design. |
| **Link subspace** (within a document) | **After deletion** | Link addresses are permanent; deleted links leave gaps. |

The key architectural insight: V-space is the user's view, and it is always dense and contiguous. The permanent address spaces (I-space, tumbler space) can have gaps, but this is either invisible to users (I-space) or intentional by design (ghost elements in the broader docuverse).

---

## Question 2 [nelson]

> When a document maps several consecutive positions to content that originates from different sources, is there a unique way to split that mapping into the fewest contiguous pieces that each reference one original span?

### Nelson's Answer

## Yes — the minimal span decomposition is unique

The uniqueness follows from three structural properties of the system that I specified:

### 1. V-space is a dense linear sequence

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

V-positions form a contiguous sequence 1, 2, 3, ..., n with no gaps. Every position maps to exactly one I-address.

### 2. I-space addresses are totally ordered on the tumbler line

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse, (or merely to a series of elements of the same type, which is a degenerate case of a subtree)." [LM 4/24]

The tumbler line imposes a total order. Two I-addresses are either adjacent on this line or they are not. There is no ambiguity — content from different documents cannot be adjacent because the document boundary creates a gap on the tumbler line.

### 3. Content identity is based on creation, not value

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Two independently created bytes with identical content have *different* I-addresses. Transcluded bytes *share* the original's I-address. The V→I mapping is therefore a well-defined function.

### Why uniqueness follows

Given the mapping V→I, define a **break** at V-position *v* whenever I(*v*) is not the tumbler-successor of I(*v*−1). A break is **forced** at every such point: no single contiguous I-span can bridge a discontinuity in the I-address sequence. Conversely, where I(*v*) *is* the successor of I(*v*−1), introducing a break would only *increase* the piece count without necessity.

The minimal decomposition therefore has exactly one span per maximal run of V-consecutive positions whose I-addresses are also consecutive on the tumbler line. The break points are determined entirely by the mapping — there is no choice involved.

This is, in mathematical terms, the unique run decomposition of the V→I mapping's first difference. It is the same reason that run-length encoding of a sequence is unique: runs are maximal by definition, and maximality leaves no room for alternative groupings.

### Architectural significance

This uniqueness is load-bearing. The POOM enfilade maps V→I, and spans are the currency of every FEBE operation:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

If the span decomposition were ambiguous, two representations of the same document could disagree on how to partition the V-stream, which would make COPY, RETRIEVEV, FINDDOCSCONTAINING, and SHOWRELATIONOF2VERSIONS produce inconsistent results. The system depends on a canonical representation of document structure as a span list — and the uniqueness of the minimal decomposition is what makes that canonical form possible.

---

## Question 3 [nelson]

> If two adjacent pieces in a document both reference content from the same original, and that original content was itself contiguous, must those two pieces be merged into one?

### Nelson's Answer

# Must Adjacent Spans Be Merged?

**No.** Literary Machines does not require merging, nor does it address this question. It operates at a level below what I specified.

## The V-Stream Is Bytes, Not Spans

The document's virtual byte stream is defined at the **byte level**, not the span level. Each byte has a V-address and maps to an I-address:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

The V-stream is a sequence of bytes. Spans are a **reference mechanism** — how you point at regions of that stream — not a storage format that the system must canonicalize.

## Spans Are for Pointing, Not for Mandating Internal Structure

Spans describe what you want to talk about:

> "A request set is a set of spans, or spanset, presented to the back end in the FEBE protocol... The manipulation of request sets is an important aspect of what front-end functions do." [LM 4/37]

Whether the enfilade machinery internally represents the V→I mapping as one merged span or two adjacent spans covering contiguous I-space is an implementation concern. The user sees an identical byte stream either way. RETRIEVEV returns the same bytes. FINDDOCSCONTAINING returns the same origin document. SHOWRELATIONOF2VERSIONS returns the same correspondence.

## The Enfilade Handles This

The internal representation is the province of the enfilade structures, which maintain "canonical order" as an internal mandate:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

But "canonical order" here refers to the enfilade data structure remaining valid after mutations — not to a requirement that adjacent spans be merged. Whether the POOM enfilade (which maps V→I) coalesces adjacent entries pointing to contiguous I-space is an optimization choice, not a semantic requirement.

## Why It Doesn't Matter Semantically

Consider: you COPY bytes from I-space 100–105 into your document at V-position 5, then separately COPY bytes from I-space 106–110 at V-position 11. Two editorial acts producing adjacent V-space content referencing contiguous I-space.

Every user-visible operation produces identical results regardless of internal span count:

| Operation | One span (100–110) | Two spans (100–105, 106–110) |
|-----------|---------------------|-------------------------------|
| RETRIEVEV | Same bytes | Same bytes |
| FINDDOCSCONTAINING | Same origin | Same origin |
| SHOWRELATIONOF2VERSIONS | Same correspondence | Same correspondence |
| Link survivability | Same I-addresses | Same I-addresses |

The V-stream is what users see. How the system represents the V→I mapping internally is invisible to them.

## Summary

I designed Xanadu at the level of **what the system does** — permanent addresses, surviving links, traceable origins, version comparison. The question of whether adjacent references to contiguous I-space must be represented as one span or may remain as two is an **implementation optimization** below my specification. The enfilade machinery handles it. The user never knows the difference.

---

## Question 4 [nelson]

> Can a single piece within a document's arrangement map to content of any length, or is there a maximum or minimum size that the design imposes on one contiguous mapping?

### Nelson's Answer

## No Minimum or Maximum Size on a Contiguous Mapping

The design imposes **no size constraint** on a single contiguous piece within a document's arrangement. A span — the unit that describes a contiguous region — can range from one byte to the entire docuverse.

Nelson states this explicitly:

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." [LM 4/24]

The V-stream (a document's current arrangement) is composed of vspans — contiguous sequences of bytes mapped to I-space content:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

Each vspan can reference native bytes (created in this document) or non-native bytes (transcluded from elsewhere), and there is no distinction in how they participate in the arrangement:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

### Why no constraint exists

The addressing system is built on humbers (arbitrary-precision integers) and tumblers (sequences of humbers). A span is defined by two tumbler boundaries, not by a count:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

Since humbers have no upper limit ("as large as it needs to be when the number is big" [LM 4/13]) and a span is just a pair of tumbler addresses, there is no structural ceiling. And since the smallest addressable unit is a single byte (the element level of the tumbler), one byte is the natural floor.

### Practical illustration

Nelson's Shakespeare example demonstrates both extremes in one document. E.G. Jewett's modified Hamlet consists of a transclusion spanning nearly the entire play (thousands of bytes in one contiguous mapping), then a single word "luge" (a few bytes of native content), then another large transclusion of the remainder. The system handles a mapping of one word and a mapping of most of a play with identical machinery.

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

This reinforces that the design is deliberately unconstrained — spans are defined by boundaries in an ever-growing address space, not by fixed-size units.

---

## Question 5 [nelson]

> Must the pieces that compose a document's arrangement be non-overlapping — that is, can a single document position ever be claimed by more than one piece simultaneously?

### Nelson's Answer

## No — V-stream positions are non-overlapping by design

The V-stream (a document's current arrangement) is explicitly a **byte stream with ordinal positions**. Each position maps to exactly one I-space byte. Nelson describes it as:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

The V-stream is dense and contiguous — no gaps, no overlaps. Every byte (whether native or transcluded) gets exactly one ordinal position:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

### Evidence from the editing operations

The FEBE operations confirm this structurally:

- **INSERT** shifts subsequent addresses: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66] — This only makes sense if each position is occupied by exactly one byte.

- **REARRANGE** uses cuts that partition the stream into non-overlapping regions, then transposes them. [LM 4/67]

- **DELETEVSPAN** removes a span and the stream closes up — no gaps left behind.

All three operations treat the V-stream as a total ordering where each position is uniquely occupied.

### The V→I mapping is a function, not a relation

The POOM enfilade maps V-addresses to I-addresses. A document IS this mapping. Each V-position resolves to exactly one I-position — it is a function, not a many-to-one or many-to-many relation.

### The important converse: I-space CAN be multiply referenced

While each V-position maps to one I-byte, the **same I-byte can appear at multiple V-positions** — both within a single document and across documents. This is transclusion (COPY). Two V-positions pointing to the same I-address is not overlap; it's two distinct positions in the arrangement that happen to reference the same permanent content.

### Summary

A document's V-stream is a sequence. Each position is claimed by exactly one piece. The pieces that compose the arrangement are non-overlapping and contiguous. Overlap is structurally impossible given Nelson's byte-stream model with ordinal addressing.

---

## Question 6 [nelson]

> Does the design require that the pieces of a document's arrangement follow the same order as the document's positions, with no piece's domain preceding another's yet following it in the content sequence?

### Nelson's Answer

No. The design explicitly allows the I-space origins of a document's V-stream spans to appear in any order relative to each other. This is the entire point of separating V-space from I-space.

## Evidence

**The REARRANGE operation produces out-of-order mappings by design:**

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3." [LM 4/67]

After a REARRANGE, the V-stream's constituent I-space spans are no longer in I-space order. Content that was created later (higher I-addresses) now precedes content created earlier (lower I-addresses) in the V-stream.

**V-space order is independent of I-space order by architecture:**

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing." [LM 4/11]

**COPY (transclusion) introduces I-space content from arbitrary locations:**

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

After a COPY, the V-stream contains I-space spans from entirely different documents — their I-addresses bear no ordering relationship to the native content whatsoever.

## What IS required

The V-stream itself must be dense and contiguous — V-addresses form a sequential numbering from 1 with no gaps. But the I-space spans underlying that sequence can appear in any I-space order. This is not a deficiency; it is the fundamental design principle:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version... A document is really an evolving ONGOING BRAID." [LM 2/14]

The "braid" metaphor is apt: strands (I-space content) are woven into arrangements (V-space orderings) that need not follow the chronological order of their creation or their permanent storage addresses.

---

## Question 7 [nelson]

> If a document is edited so that content is inserted in the middle, what happens to the arrangement's existing pieces — must exactly one piece split into two, or can the restructuring be more complex?

### Nelson's Answer

## Insertion and Span Splitting

For the INSERT operation, **at most one existing piece splits into two**. The restructuring is always local and minimal.

### The Architecture

A document's V-stream (its current arrangement) is an ordered sequence of spans, each referencing a contiguous range of I-space content. When you insert at a V-space position, there are exactly two cases:

1. **Mid-span insertion**: The position falls within an existing span. That span splits into the portion before the insertion point and the portion after. The new content goes between them. **Exactly one piece becomes two.**

2. **Boundary insertion**: The position falls at the boundary between two existing spans. The new content is placed between them. **Zero pieces split.**

No other existing pieces are structurally affected. Their I-space references remain identical — only their V-addresses shift upward:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

### Why It Cannot Be More Complex

V-space is linear. Insertion happens at one point. Only the span containing that point can be affected. All other spans continue referencing exactly the same I-space bytes — the content hasn't moved, only the V-addresses have shifted. Since V-addresses are ephemeral ("may be constantly changing; the front-end application is unaware of this" — 4/11), this shift is purely a remapping, not a structural change to other pieces.

The I-space content is untouched by any V-space operation:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

And the new content creates fresh I-space addresses:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

### What About COPY (Transclusion-Insert)?

COPY places existing I-space content at a V-position:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." (4/67)

The spec-set can be multiple spans, so the *inserted* material may arrive as several pieces. But the effect on the *existing* arrangement is identical: at most one existing span splits at the insertion point.

### Where It Gets More Complex: REARRANGE

REARRANGE is a different story. It transposes two regions using multiple cut points:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." (4/67)

Each cut point that falls mid-span splits a piece. With four cuts, up to four existing pieces could split. So REARRANGE *can* produce more complex restructuring — but INSERT cannot.

### A Note on Nelson's Level of Specification

Nelson defines INSERT at the FEBE (semantic) level, not at the span-representation level. He specifies *what happens to V-addresses*, not *how the internal span list changes*. The span-splitting behavior I describe above is the necessary implementation consequence of the architecture (V-space as ordered spans over I-space), but Nelson leaves the mechanics to the enfilade data structure:

> "The Model T enfilade handles the revision of serial data very quickly and very cleanly." (1/33)

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." (1/34)

The "canonical order" guarantee means the enfilade must produce exactly this result — one split, new content inserted, all addresses shifted — and remain structurally valid afterward.

---

## Question 8 [nelson]

> When content is deleted from a document, must the remaining pieces close the gap so the document's positions stay contiguous, or can the deletion leave a hole in the address space?

### Nelson's Answer

## The gap closes. V-space positions are always contiguous.

Deletion in Xanadu removes content from the document's **V-space** (virtual byte stream) — the current arrangement the user sees. The remaining positions close up to maintain a dense, gap-free sequence. Nothing happens to **I-space** — the permanent content store.

### Evidence from the specification

**1. V-space is defined as always contiguous.**

The virtual byte stream is exactly that — a *stream*. Positions always run from 1 through *n* with no holes:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

**2. INSERT explicitly renumbers, so DELETE must too.**

The INSERT operation states:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

If insertion shifts all subsequent addresses *forward*, deletion must shift them *back*. The V-stream is a logical sequence that reflows on every edit — there is no fixed grid with permanent slots.

**3. V-addresses are ephemeral by design.**

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

V-addresses *routinely* change. They are not permanent identifiers — they are positions in the current arrangement. A hole would contradict this: it would mean a V-address persists even after the content it addressed is gone.

**4. Deleted bytes still exist — just not in V-space.**

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The content is *not currently addressable* in this document's V-stream. It hasn't been destroyed — it lives on at its permanent I-address, accessible through old versions, through other documents that transclude it, and through links that point to its I-address.

### Why this matters architecturally

The V-space/I-space separation is precisely what makes gap-closing safe:

- **V-space** is a *view* — a mapping from sequential positions to I-addresses. Edits change the mapping. Gaps in a mapping are meaningless.
- **I-space** is *permanent* — append-only, never rewritten, never compacted. I-addresses never become invalid.
- **Links** point to **I-addresses**, not V-addresses. So closing the V-space gap cannot break any link.

If V-space left holes, it would undermine the entire model. The document would no longer be a coherent byte stream — it would be a sparse array with undefined positions. Front-end applications would need to handle gaps in what is supposed to be sequential text. And there would be no benefit: the content is already preserved in I-space regardless.

### The analogy

Think of it like a reading list. If you remove item 3 from a 5-item list, items 4 and 5 become the new 3 and 4. The list stays dense. The *books themselves* (I-space) haven't moved — they're still on the same shelves. You've only changed the list (V-space).

---

## Question 9 [nelson]

> Is an empty document — one with no content at all — represented by an arrangement with zero pieces, or must every document always contain at least one piece?

### Nelson's Answer

## An Empty Document Has Zero Pieces

An empty document is represented by an arrangement with zero pieces. Nelson explicitly designed the system to accommodate this.

### Direct Evidence

**CREATENEWDOCUMENT creates an empty document:**

> "This creates an empty document. It returns the id of the new document." (4/65)

The operation returns an address — a position on the tumbler line — but stores nothing underneath it. No content bytes, no links.

**Ghost elements establish that addressable emptiness is valid:**

> "While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." (4/23)

> "These elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

An empty document is precisely a ghost element that has been "baptized" — it has a permanent address but no stored contents yet.

**Spans can contain nothing:**

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

If a span over a document's address range can contain nothing, the document's V-stream can be empty.

### Structural Reasoning

The V-stream is a mapping from sequential positions to I-space content. An empty document has an empty mapping — zero entries. RETRIEVEDOCVSPANSET (4/68) would return zero characters and zero links. There is no "minimum occupancy" requirement anywhere in Literary Machines.

The document's identity is its *address*, not its content. The address exists from the moment of creation; content arrives later through INSERT or APPEND. Nelson's append-only model makes this natural: a document begins empty and accumulates content over time.

> "A document is really an evolving ONGOING BRAID." (2/14)

A braid with zero strands is still a braid — it simply hasn't begun to accumulate yet.

---

## Question 10 [nelson]

> When two documents share the same original content, must their arrangements reference that content identically, or can each document's arrangement decompose the shared content into differently sized pieces?

### Nelson's Answer

## Each Document Independently Decomposes Shared Content

No, arrangements need not reference shared content identically. Each document's V-space arrangement is an independent mapping from V-positions to I-space addresses, and there is no requirement that two documents decompose shared I-space content into spans of the same size.

### The V→I Mapping Is Per-Document

The document IS its V→I mapping. From the curated sources on V-space:

> "The mapping V -> I is the essence of document structure. The document IS the mapping from V-addresses to I-addresses. Each version defines a different mapping."

Each document independently defines how it arranges references to I-space content. Two documents that share the same underlying bytes maintain entirely separate V-space arrangements.

### Editing Operations Explicitly Break Span Boundaries

Nelson's editing operations demonstrate that span decomposition changes freely:

**REARRANGE** transposes regions of text [LM 4/67]. If Document A references I-space bytes 100-199 as one contiguous span, and the user rearranges by cutting at byte 150, the single span becomes two spans in a different order. The I-space content is unchanged; only the V-space decomposition differs.

**INSERT** shifts V-addresses and can split a transcluded span in two [LM 4/66]:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text."

If you insert new content in the middle of a transcluded passage, the single I-space reference splits into two separate spans flanking the insertion.

**DELETE** removes from V-space without affecting I-space [LM 4/9]:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

Deleting part of a span shrinks the reference. Document A might reference I:100-199 while Document B (after a partial deletion) references only I:100-149.

### FINDDOCSCONTAINING Confirms Partial Inclusion

The operation that finds shared content explicitly handles partial overlap [LM 4/70]:

> "This returns a list of all documents containing **any portion** of the material included by \<vspec set\>."

The phrase "any portion" means documents routinely contain different-sized pieces of the same I-space content.

### Correspondence Works Across Different Decompositions

SHOWRELATIONOF2VERSIONS returns *pairs* of corresponding spans [LM 4/70]:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond."

If both documents had to use identical span boundaries, a simple list would suffice. Returning *pairs* implies the two documents may decompose shared content differently—span boundaries in one version need not align with span boundaries in the other.

### The Byte-Level Foundation

The fundamental unit of identity is the individual byte, not the span. Spans are a convenience for addressing contiguous ranges, but correspondence and identity operate at the byte level:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, **regardless of their native origin**." [LM 4/11]

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Attribution and identity trace to individual bytes via their I-addresses. How those bytes are grouped into spans in any particular document's V-space is that document's business.

### Concrete Example

Suppose Alice writes "Hello world" in Document A (I-addresses 100-110). Bob transcludes it into Document B as one span [I:100-110]. Carol transcludes it too, but then inserts a comma after "Hello", splitting her reference into [I:100-104], her new comma, [I:105-110]. Dave transcludes only "world" as [I:106-110].

All four documents share I-space content. None are required to use the same span decomposition. Correspondence still works—SHOWRELATIONOF2VERSIONS between any pair will find the shared I-addresses regardless of how each document groups them into spans.

---

## Question 11 [gregory]

> In a well-formed POOM, can two bottom crums ever have overlapping V-displacement ranges, or does `insertpm` guarantee that V-spans are strictly non-overlapping — and if so, which code path enforces this?

### Gregory's Answer

## KB Synthesis

In a well-formed POOM after INSERT operations, bottom crums have strictly non-overlapping V-displacement ranges. There is no explicit overlap check — the invariant is maintained structurally through three cooperating code paths.

---

## The guarantee holds via implicit structural construction

### 1. Interior split: `makegappm` → `slicecbcpm`

When an INSERT point falls strictly inside an existing crum (`whereoncrum` returns `THRUME`, i.e., `crum.grasp < origin < crum.reach`), `makegappm` calls `slicecbcpm` to split the crum into two halves. The local cut offset satisfies `0 < localcut < cwid` with both strict inequalities, so the resulting halves are:

- Original crum retains `[grasp, grasp + localcut)` 
- New crum receives `[grasp + localcut, reach)`

These are non-overlapping by construction. [INV-NO-ZERO-WIDTH-CRUM] formalizes this: `slicecbcpm` is only reachable when `whereoncrum == THRUME`, guaranteeing both halves have strictly positive width. [PRE-DELETE, Finding 0075]

### 2. Post-insertion shift: two-blade knife in `insertcutsectionnd`

After cutting, all crums in the range `[blade[0], blade[1])` have their V-displacement incremented by exactly `insert_width`. This is a **uniform** additive shift — the relative order of crums is preserved, so pre-existing non-overlap is carried forward. Crums outside the knife range are untouched. [SS-TWO-BLADE-KNIFE, ST-INSERT Finding 0054]

The shift operation `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], ...)` at `insertnd.c:162` applies identically to every eligible crum, so no two crums can collide through this step alone.

### 3. Boundary extension: `isanextensionnd`

When the INSERT point equals an existing crum's `reach` (ONMYRIGHTBORDER), `makegappm` exits early without any cut [PRE-INSERT, Finding 0062]. `isanextensionnd` then checks if the new content is contiguous with the existing crum's I-address range and same `homedoc`; if so, the existing crum's width is extended in place. No new crum is created, so no overlap arises.

---

## No explicit overlap check exists

The KB contains no documentation of a runtime assertion or predicate that checks `crum_i.reach <= crum_j.grasp` for all pairs. The invariant is maintained entirely by construction — the split/shift/extend trio ensures new crum boundaries are always placed at positions that cannot collide with survivors.

---

## Caveat: DELETE can break the bijection

[INV-POOM-BIJECTIVITY] (Finding 0053) notes that DELETE's Case 2 shift via `tumblersub` can produce negative V-positions when same-exponent arithmetic underflows. However, [Finding 0055] corrects this: the `strongsub` exponent guard prevents cross-subspace subtraction entirely, so only same-exponent within-subspace deletions can produce negative results. Negative-position crums are invisible to queries but still occupy tree space. A subsequent INSERT into such a state could encounter them during `whereoncrum` traversal — they sort before all valid addresses (per [SS-TUMBLER] Finding 0053), so they would classify as `TOMYLEFT` and not be shifted. They represent a form of leaked state rather than a genuine overlap.

---

**Summary**: The enforcing code path is `insertpm` → `insertnd` → `makegappm` (at `insertnd.c:137`) which either (a) calls `slicecbcpm` for interior insertions, (b) exits early at boundary, or (c) delegates to the extension path. The subsequent `insertcutsectionnd` shift at `insertnd.c:207` preserves ordering for all survivors. Non-overlap is a structural invariant of the INSERT operation, not an explicit predicate check.

---

## Code Exploration

Now I have everything I need. Here is the complete answer.

---

## Answer: V-displacement non-overlap in the POOM

**Short answer:** Two bottom crums in a well-formed POOM cannot have overlapping V-displacement ranges. The guarantee is structural, enforced by a three-step protocol executed on every call to `insertpm`.

---

### The code path that enforces non-overlap

**`insertpm`** (`orglinks.c:75`) is the entry point. For each item in `sporglset`, it packs `vsaptr` into `crumorigin.dsas[V]` and `crumwidth.dsas[V]`, then delegates:

```c
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);   /* advance V-cursor */
```
[`orglinks.c:130-131`]

The `index=V` argument is the key: it tells `insertnd` this is a V-dimension insertion. After each item, `vsaptr` is advanced by `crumwidth.dsas[V]`, so within a single `insertpm` call, consecutive items are packed at non-overlapping V-addresses by construction.

The deeper guarantee — protecting against overlap with *previously existing* crums — is inside `insertnd`.

---

### Step 1: `makegappm` — splitting and shifting

`insertnd` (`insertnd.c:15`) handles POOM by calling `makegappm` **before** `doinsertnd`:

```c
case POOM:
    makegappm(taskptr, fullcrumptr, origin, width);
    ...
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);
```
[`insertnd.c:53-57`]

`makegappm` (`insertnd.c:124`) does three things:

**1a. Guard: skip if origin is outside the current V-range**

```c
if (iszerotumbler(&fullcrumptr->cwid.dsas[V])
|| tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);
```
[`insertnd.c:140-143`]

The comment here is `/* this if for extensions to bc without calling cut */`. If the origin is entirely outside the current V-range (left extension or right append), no existing crums need shifting; non-overlap is trivially preserved.

**1b. Place two knife cuts, then call `makecutsnd`**

```c
movetumbler(&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
knives.dimension = V;
makecutsnd(fullcrumptr, &knives);
```
[`insertnd.c:144-148`]

`findaddressofsecondcutforinsert` (`insertnd.c:174`) computes a second cut position that is "just past" `origin->dsas[V]` in tumbler arithmetic. The purpose of the two-knife bracketing is to ensure that a crum whose V-range straddles exactly `origin->dsas[V]` can be split cleanly.

`makecutsnd` (`ndcuts.c:15`) walks the tree and, for any bottom crum that is THRUME (straddles) a knife, calls `slicecbcpm` (`ndcuts.c:373`):

```c
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);  /* new starts at old's end */
locksubtract(..., &ptr->cwid, &newwid, &new->cwid);   /* old width shrinks */
movewisp(&newwid, &ptr->cwid);
adopt(new, RIGHTBRO, ptr);
```
[`ndcuts.c:444-448`]

After slicing, the left half ends at the knife and the right half starts at the knife — adjacent, strictly non-overlapping.

**1c. Shift all crums at or past `origin->dsas[V]` rightward**

After cutting, `makegappm` traverses children of the intersection ancestor and applies `insertcutsectionnd` (`edit.c:207`) to classify each crum:

- **Case 0**: crum ends before `blades[0]` — no action
- **Case 1**: crum starts between `blades[0]` and `blades[1]` (i.e., at `origin->dsas[V]` or just after) — **shift right**
- **Case 2**: crum starts at or past `blades[1]` — no action (already past the gap)

The shift for case 1 is:

```c
case 1: /*9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified(ptr);
    break;
```
[`insertnd.c:161-164`]

The `9-17-87 fix` comment flags this as a corrected bug — the operand order had been wrong. Every crum whose absolute V-start is ≥ `origin->dsas[V]` gets its relative displacement increased by `width->dsas[V]`, opening an exact gap of width `width->dsas[V]` at `origin->dsas[V]`.

---

### Step 2: `makeroomonleftnd` — the "extend left" case

When the insertion origin is *less* than the current V-start of the POOM (the case `makegappm` skips), `insertmorend` (`insertnd.c:219`) calls `makeroomonleftnd` (`makeroom.c:13`):

```c
if (tumblercmp(&origin->dsas[i], &grasp->dsas[i]) == LESS) {
    tumblersub(&grasp->dsas[i], &origin->dsas[i], &base);
    tumblersub(&origin->dsas[i], &offset->dsas[i], &newdsp.dsas[i]);
    expandcrumleftward((typecorecrum*)father, &newdsp.dsas[i], &base, i);
    ...
}
```
[`makeroom.c:26-42`]

`expandcrumleftward` (`makeroom.c:52`) shifts the parent's V-start leftward to `origin`, grows its V-width by `base`, and shifts all existing children's V-displacements rightward by `base`. This ensures no existing child overlaps with the new left-extension content.

---

### Step 3: `insertcbcnd` — placing the new crum

`insertcbcnd` (`insertnd.c:242`) first tries `isanextensionnd` (`insertnd.c:301`):

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```
[`insertnd.c:301-309`]

This merges only when the new origin exactly equals the existing crum's `reach` (end), with the same `homedoc`. Zero gap, zero overlap — strict adjacency.

If no extension matches, a new bottom crum is created and placed:

```c
new = createcrum(0, (INT)father->cenftype);
reserve(new);
adopt(new, SON, (typecorecrum*)father);
dspsub(origin, grasp, &new->cdsp, (INT)father->cenftype);
movewisp(width, &new->cwid);
```
[`insertnd.c:260-266`]

The new crum's displacement is `origin - grasp` (relative to its parent), and its width is exactly `width`. After step 1 opened the gap, this crum fills it exactly — no overlap with left neighbors (they end ≤ origin) and no overlap with right neighbors (they were shifted to start ≥ `origin + width`).

---

### Does `recombine` preserve the invariant?

Yes. `recombinend` (`recombine.c:104`) may call `takenephewnd` (`recombine.c:235`), which re-parents crums:

```c
disown(nephew);
dspadd(&bro->cdsp, &nephew->cdsp, &nephew->cdsp, bro->cenftype);   /* make absolute */
adopt(nephew, RIGHTMOSTSON, me);
...
dspsub(&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);     /* re-relativize */
```
[`recombine.c:242-248`]

This converts from relative-to-old-parent to absolute, then back to relative-to-new-parent. Absolute V-positions are unchanged. Non-overlap is preserved.

---

### Summary of the enforcement chain

| Step | Function | File | What it does |
|------|----------|------|--------------|
| Split straddling crums | `makecutsnd` → `slicecbcpm` | `ndcuts.c:15`, `ndcuts.c:373` | Splits any bottom crum spanning the insertion point; left half ends at cut, right half starts at cut — no gap, no overlap |
| Open gap (insert within range) | `makegappm` case 1 | `insertnd.c:161-164` | Shifts all crums with V-start ≥ origin rightward by +width |
| Open gap (insert left of range) | `makeroomonleftnd` → `expandcrumleftward` | `makeroom.c:26-42`, `makeroom.c:52-74` | Shifts all existing children rightward by `grasp - origin` |
| Place new crum | `insertcbcnd` | `insertnd.c:242-275` | Places new crum at exactly origin with exactly width |
| Extend adjacent crum | `isanextensionnd` | `insertnd.c:301-309` | Widens existing crum iff `reach == origin` and same `homedoc` — no gap, no overlap |

The structural invariant — bottom crums' absolute V-ranges `[grasp_V, grasp_V + cwid_V)` are strictly non-overlapping and non-adjacent-except-where-merged — is maintained across every insertion. The primary enforcement is in **`makegappm`** (`insertnd.c:124`), which is called exclusively for POOM inserts and whose sole purpose is to open a precise gap at the insertion V-address before the new content is placed.

The suspicious comment at `orglinks.c:114` — `/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/` — concerns the V-*width* calculation (`shift = tumblerlength(vsaptr) - 1`), not the placement logic. A wrong width there would affect how much V-space a crum occupies, but would not by itself create overlap between two crums: `makegappm` would still shift existing crums by whatever width was computed, so the gap would match the new crum's computed width exactly.

---

## Question 12 [gregory]

> When `isanextensionnd` coalesces a new entry with an existing bottom crum, does it always extend the V-width and I-width symmetrically — that is, does a single bottom crum always represent a 1:1 mapping where V-width equals I-width in magnitude?

### Gregory's Answer

## KB Synthesis

Yes, a single bottom crum always represents a 1:1 mapping where V-width and I-width encode the same numeric magnitude, though the tumbler representations differ.

## The invariant holds universally

[INV-WIDTH-VALUE-EQUIVALENCE] states this directly:

> `forall crum c :: tumblerintdiff(c.width.dsas[V], zero) == tumblerintdiff(c.width.dsas[I], zero)`

The V-width and I-width are **not equal as tumblers** (they have different exponents and digit counts — see [SS-POOM-BOTTOM-CRUM] and [SS-INSERT-VWIDTH-ENCODING]), but extracting the integer value from either yields the same count.

## Why this is structurally necessary

Three facts force symmetry:

1. **[INV-SINGLE-CHAR-GRANULARITY]**: Each byte occupies exactly one I-address. V-space width equals byte count; I-space width equals I-address count. Both count the same thing.

2. **[SS-INSERT-VWIDTH-ENCODING]**: V-width is explicitly *derived from* the I-width integer value at crum creation. The construction `inc = tumblerintdiff(lwidth, zero)` extracts the I-width's count, then `tumblerincrement(zero, shift, inc, &crumwidth.dsas[V])` re-encodes that same count at V-space exponent precision. They start equal by construction.

3. **[ST-INSERT, Finding 0062]**: `isanextensionnd` checks that `new_content.origin == existing_crum.reach` in both V and I dimensions (the condition is contiguity in both spaces simultaneously). A single character added via extension contributes exactly +1 to both widths' numeric value, preserving the invariant.

## What the asymmetry actually is

The asymmetry is purely representational: I-widths use 6–9 tumbler digits (full I-space precision), while V-widths use 2 digits (V-address precision, with exponent = `tumblerlength(vsaptr) - 1`). A crum covering 11 bytes has:

```
V-width: exp=-1, mantissa[0]=11  →  tumbler 0.11
I-width: 0.0.0.0.0.0.0.0.11      →  same value, 9-digit tumbler
```

Comparing with `tumblercmp` would show them unequal; comparing with `tumblerintdiff` shows them equal. Any code performing width comparisons across the two dimensions must use the integer extraction path, not raw tumbler comparison.

The KB does not document what happens if `vsaptr` is the zero tumbler during V-width encoding — [EC-VWIDTH-ZERO-ADDRESS] flags this as a suspected edge case — but for all normal INSERT paths where V-addresses are positive and non-zero, the 1:1 magnitude relationship holds unconditionally.

---

## Code Exploration

Now I have everything I need for a complete answer.

---

## Answer

**No. A single bottom crum does not always have V-width equal to I-width in magnitude.** The extension check in `isanextensionnd` enforces 2D adjacency — not 2D symmetry — and the widths added during coalescing are constructed with deliberately different formulas for each dimension.

---

### 1. `isanextensionnd` checks adjacency in both dimensions simultaneously

`isanextensionnd` [insertnd.c:301-309]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`prologuend` [retrie.c:334-339] computes:
- `grasp = offset + crum->cdsp` (in both I and V dimensions)
- `reach = grasp + crum->cwid` (in both I and V dimensions)

via `dspadd` → `lockadd` over `dspsize(POOM) = DSPSIZEPM = 2` tumblers [wisp.h:26, wisp.c:17].

Then `lockeq` [wisp.c:261-266] checks `reach.dsas[0] == origin.dsas[0]` AND `reach.dsas[1] == origin.dsas[1]` — that is, I-reach == new I-origin **and** V-reach == new V-origin simultaneously. This is a 2D contiguity gate, not a symmetry assertion.

---

### 2. When coalescing fires, both widths are added independently

`insertcbcnd` [insertnd.c:250-251]:

```c
if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
    dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
```

`dspadd` [wisp.c:15-18] calls `lockadd` over `dspsize(POOM) = 2` tumblers:
- `ptr->cwid.dsas[I] += width->dsas[I]`
- `ptr->cwid.dsas[V] += width->dsas[V]`

No assertion is made that these increments are equal. Whatever relationship (or mismatch) exists between the I and V components of `width` is simply preserved.

---

### 3. The V-width is constructed differently from the I-width

The only caller of `insertnd` for POOM is `insertpm` [orglinks.c:75-134]. The critical width-construction block [orglinks.c:105-117]:

```c
movetumbler (&lstream, &crumorigin.dsas[I]);    // I-origin = I-span start
movetumbler (&lwidth, &crumwidth.dsas[I]);      // I-width = raw I-span width
movetumbler (vsaptr, &crumorigin.dsas[V]);      // V-origin = current vsa
/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

`lwidth` is the raw I-span width from `unpacksporgl` [sporgl.c:178-203] — a full tumbler with its own `exp` and mantissa.

`tumblerincrement(&zero, shift, inc, result)` [tumble.c:599-607] with a zero `aptr` produces:

```c
cptr->exp = -rightshift;   // = -(shift)
cptr->mantissa[0] = bint;  // = inc = lwidth.mantissa[0] only
```

So the V-width tumbler is `inc × base^(-shift)` where:
- `inc = tumblerintdiff(&lwidth, &zero)` extracts only `lwidth.mantissa[0]` (the leading digit — sub-integer digits in `lwidth` are discarded)
- `shift = tumblerlength(vsaptr) - 1 = nstories(vsaptr) - vsaptr->exp - 1` depends on the depth of the V-address

The I-width is the full `lwidth` (all digits, its own `exp`). The V-width discards sub-integer I-space precision and rescales by V-address depth.

**Example**: If `lwidth` is a simple integer tumbler `{exp=0, mantissa=[5,0,0...]}` (N=5 characters) and `vsaptr` has `tumblerlength=3` (a three-story address like `1.0.3`):

- I-width: `{exp=0, mantissa=[5,0,0...]}` — represents 5 at the top level
- V-width: `tumblerincrement(&zero, 2, 5, ...)` → `{exp=-2, mantissa=[5,0,0...]}` — represents 5 at depth 2

These are not equal tumblers. The V-width is two decimal places "deeper" in the tumbler hierarchy.

If `vsaptr` has `tumblerlength=1` (top-level address, `shift=0`), the V-width would equal the I-width for simple integer tumblers — the 1:1 case holds **only for top-level V-addresses with no sub-integer I-width precision**.

---

### 4. The developers tracked this divergence explicitly

`widdiffs` [insertnd.c:114-122]:

```c
static INT widdiffs(typecuc *crumptr)
{
    INT i,v;
    if(crumptr->cenftype != POOM)
        return(0);
    i = lastdigitintumbler(&crumptr->cwid.dsas[I]);    
    v = lastdigitintumbler(&crumptr->cwid.dsas[V]);    
    return(i-v);
}
```

This function exists precisely to measure the difference between the last digit of I-width and V-width. It is called before and after every POOM insertion [insertnd.c:46, 78], and a disabled diagnostic [insertnd.c:80-85] prints "possible error" when the diff changes:

```c
if(FALSE&&(fullcrumptr->cenftype==POOM)&&olddiff != newdiff){      
    fprintf(stderr,"insertnd  possible error dumping widdiffs%d %d\n\r",olddiff,newdiff);
```

The `FALSE&&` disablement tells us: the developers knew this could diverge, investigated it, and ultimately decided not to treat it as fatal. The comment `/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/` at orglinks.c:114 further shows that the V-width shift calculation was a known concern from 1985.

---

### Conclusion

**`isanextensionnd` coalescing does not guarantee V-width == I-width.** The function enforces that the new insertion is contiguous with the existing crum in *both* I-space and V-space simultaneously — but this is a condition on positions, not widths. The widths are constructed independently in `insertpm`: I-width from the raw I-span, V-width from the leading digit of that span scaled to the V-address depth. For V-addresses deeper than story 1, the resulting tumblers are structurally different in their `exp` fields, even when they represent the same integer count of characters. The `widdiffs` function and its accompanying disabled diagnostic confirm the developers were aware that POOM bottom crums can carry asymmetric I/V widths and chose not to enforce strict equality at the tumbler level.

---

## Question 13 [gregory]

> After a sequence of INSERT, DELETE, and COPY operations, can gaps exist in the V-address domain of a document's text subspace — positions with no POOM entry — or is the V-domain always a single contiguous interval from minimum to maximum?

### Gregory's Answer

## KB Synthesis

## V-Address Domain Gaps

**Yes, gaps can exist** — but only via deliberate non-adjacent placement, not through normal editing operations.

---

### Why DELETE does not create gaps

DELETE removes the V→I mappings for the deleted range (Case 1: crums entirely within the range are `disown`ed and freed) and shifts all following crums leftward by the deletion width (Case 2: `tumblersub` on V-displacement) [ST-DELETE]. The post-deletion V-domain is `[min, a) ∪ [a+w, max]` where the latter segment shifts to `[a, max−w]`, producing a contiguous result. The `strongsub` exponent guard [SS-TUMBLER] means cross-exponent (cross-subspace) entries are not shifted, but within the text subspace `1.x` all entries share the same exponent, so the shift closes the hole cleanly.

---

### Why INSERT within the existing domain does not create gaps

The two-blade knife [SS-TWO-BLADE-KNIFE] with blades `[insertion_point, next_subspace_boundary)` ensures all crums *after* the insertion point within the same subspace shift rightward by the insertion width [ST-INSERT]. Content placed at position P fills exactly that position; nothing is left unoccupied. Consecutive inserts at adjacent boundaries coalesce via `isanextensionnd` [ST-INSERT Finding 0062], and the enfilade consolidates contiguous regions into a single span [INV-VSPAN-CONSOLIDATION].

---

### How gaps arise

The backend accepts **any** V-position for INSERT or COPY — `acceptablevsa()` unconditionally returns `TRUE` [PRE-INSERT]. The two-blade knife shift only affects crums in `[blade[0], blade[1])`. If you INSERT at V `1.10` when the document's content ends at V `1.5`:

- Existing crums at `[1.1, 1.5]` are all `TOMYLEFT` of blade[0] `= 1.10` → classified case 0, **no shift**
- New content lands at `[1.10, 1.10+w]`
- V-domain becomes `[1.1, 1.5+something] ∪ [1.10, 1.10+w]` — **gap from ~1.5 to 1.10**

The same applies to COPY/VCOPY at an arbitrary non-adjacent target position. The backend does not validate that the target is adjacent to existing content.

When gaps exist, `retrieve_vspanset` returns **multiple spans** within the text subspace rather than one, because `retrievevspansetpm` only consolidates spans that are genuinely contiguous [SS-VSPAN-VS-VSPANSET]. The single-span consolidation in [INV-VSPAN-CONSOLIDATION] is a property of contiguous sequential inserts, not a global guarantee.

---

### Summary

| Operation | Creates gap? | Mechanism |
|-----------|-------------|-----------|
| INSERT within/adjacent to content | No | Shift fills around insertion |
| INSERT beyond content extent | **Yes** | Existing crums TOMYLEFT → no shift; new crum at distant position |
| DELETE | No | Case 2 shift closes the hole |
| COPY within/adjacent | No | Same as INSERT mechanics |
| COPY to non-adjacent position | **Yes** | Same as INSERT beyond extent |

The invariant [INV-VSPAN-CONSOLIDATION] holds only for content that *is* contiguous — it reflects the enfilade's consolidation of adjacent crums, not an enforcement that all insertions produce contiguous output. The backend's gap-prevention is behavioral (callers conventionally insert at the current cursor position) rather than structural.

---

## Code Exploration

Now I have everything I need to give a complete, code-grounded answer.

---

## Answer

The answer is nuanced: **DELETE never creates gaps** — it actively compacts the V-domain. But **INSERT and COPY can create gaps** when given an explicit V-address beyond the current end of content, because the bounds-check guard (`acceptablevsa`) is an unconditional stub.

Here is the full analysis, traced from entry points to leaf operations.

---

### 1. The POOM Data Structure

The POOM (Permutation-Oriented Ordered Map) is a 2D enfilade. Each bottom crum stores:
- `cdsp.dsas[V]` — V-address displacement (position, relative to parent)
- `cwid.dsas[V]` — V-address width (extent)
- `cdsp.dsas[I]`, `cwid.dsas[I]` — corresponding I-space (permascroll) coordinates

The POOM root's `cwid.dsas[V]` encodes the entire V-extent of the document. The question of "gaps" is whether every V-address within that extent maps to a crum entry.

---

### 2. DELETE Does Not Create Gaps — It Compacts

Entry: `dodeletevspan` → `deletevspanpm` → `deletend`

**`dodeletevspan`** [`do1.c:158-167`]:
```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
);
```

**`deletevspanpm`** [`orglinks.c:145-152`]:
```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

**`deletend`** [`edit.c:31-76`] places two knife cuts — one at the deletion start, one at deletion end [`edit.c:40-41`]:
```c
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
```

It then iterates every crum in the intersection zone and classifies it via `deletecutsectionnd` [`edit.c:235-248`]:

| Return | Meaning | Action |
|--------|---------|--------|
| `0` | Crum is **left** of the deletion zone | Do nothing |
| `1` | Crum is **inside** the deletion zone | `disown()` + `subtreefree()` — crum removed |
| `2` | Crum is **right** of the deletion zone | **Shift its V-displacement left by the deleted width** |

The critical case 2 is at [`edit.c:63`]:
```c
tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

**Every crum to the right of the deleted range has its V-address displacement reduced by exactly the deleted width.** The V-domain closes shut — no gap is ever left behind by DELETE.

---

### 3. INSERT Within Existing Range Does Not Create Gaps

Entry: `doinsert` → `docopy` → `insertpm` → `insertnd` → `makegappm`

**`doinsert`** [`do1.c:87-123`] first allocates the I-space content in the granfilade, then calls `docopy` with the target V-address.

**`makegappm`** [`insertnd.c:124-172`] is the V-space preparation step. It first checks whether the insertion point falls within the current V-extent of the POOM [`insertnd.c:140-143`]:
```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

If the insertion point is **within** the current range (between `grasp` and `reach`), it places two cuts at the insertion point and uses `insertcutsectionnd` to classify each crum. Case 1 crums (those to the right of the insertion point) have their V-displacement **shifted up** by the insertion width [`insertnd.c:162`]:
```c
tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
```

New content then fills the opened slot exactly. **No gap.**

---

### 4. INSERT or COPY Beyond the Current End CAN Create Gaps

When the V-address passed to `doinsert` or `docopy` is **at or beyond `reach.dsas[V]`** (the current end of content), `makegappm` hits the third condition above and returns immediately without shifting anything [`insertnd.c:142-143`]:
```c
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

`insertnd` then proceeds directly to `doinsertnd` → `insertcbcnd`, which places the new crum at the explicitly specified V-address. If that address is strictly greater than `reach.dsas[V]`, the parent's `setwispupwards` call will update the root's `cwid.dsas[V]` to span all the way to the new crum's end — **but no content covers the interval between the old reach and the new crum's start.** A gap exists in the V-domain.

The validation function that was supposed to prevent this is **a no-op stub** [`do2.c:110-113`]:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

`docopy` calls `acceptablevsa` before `insertpm` [`do1.c:56`], but since it unconditionally returns `TRUE`, any V-address is accepted — including one that creates a gap.

---

### 5. APPEND Never Creates Gaps

`appendpm` [`orglinks.c:17-27`] always calls `findvsatoappend` to determine the target V-address before calling `doinsert`. The logic [`orglinks.c:44-45`]:
```c
} else if (tumblercmp (&reach.dsas[V], &linkspacevstart) == LESS) {
    movetumbler (&reach.dsas[V], vsaptr); /* no links in doc */
```

inserts new content at exactly `reach.dsas[V]` — the precise end of existing content. This is always contiguous.

---

### Summary

| Operation | V-domain effect | Creates gaps? |
|-----------|----------------|---------------|
| DELETE | Removes crums; shifts all right-side crums left by deleted width [`edit.c:63`] | **No** — compacts |
| INSERT within range | Shifts all right-side crums right by inserted width [`insertnd.c:162`]; new content fills slot | **No** |
| INSERT/COPY at position > current end | `makegappm` skips shifting [`insertnd.c:140-143`]; content placed at explicit position | **Yes** — gap from old `reach` to new crum |
| APPEND | Target is exactly `reach.dsas[V]` [`orglinks.c:45`] | **No** — always contiguous |

**The V-domain is NOT guaranteed to be a single contiguous interval.** DELETE is safe — it compacts aggressively. But INSERT and COPY operate on client-supplied V-addresses, and `acceptablevsa` [`do2.c:110-113`] performs no validation. A client that supplies an explicit V-address beyond the current document end will produce a sparse POOM with unreachable V-addresses between the old end and the new content. The `findvsatoappend` code's awareness of the link subspace boundary [`orglinks.c:39-48`] and its "find the maximum V-address" scan [`orglinks.c:66-67`] further confirm that the system expects V-space can be sparse and navigates it accordingly rather than assuming a single contiguous interval.

---

## Question 14 [gregory]

> Does `slicecbcpm` always produce exactly two pieces when cutting a bottom crum at an interior point, and are both pieces guaranteed to have positive widths, or can degenerate zero-width fragments survive?

### Gregory's Answer

## KB Synthesis

Yes on both counts. The KB gives a complete answer.

**`slicecbcpm` produces exactly two pieces**

When called, `slicecbcpm` splits one bottom crum into two: the original crum retains width `localcut`, and a new sibling crum receives the remainder `cwid - localcut`. There is no code path that produces more or fewer fragments from a single call [INV-NO-ZERO-WIDTH-CRUM].

**Both pieces are guaranteed to have strictly positive widths**

The guarantee comes from the call-site precondition, not from `slicecbcpm` itself. `makecutsbackuptohere()` (`ndcuts.c:77-90`) only invokes `slicecbcpm` when `whereoncrum() == THRUME`, meaning the cut satisfies `grasp < cut < reach` with **strict** inequalities on both sides [PRE-DELETE, Finding 0075].

Given strict interiority:

- `localcut = cut - grasp > 0` (because `cut > grasp`)
- `remaining = cwid - localcut = reach - cut > 0` (because `cut < reach`)

Both strict inequalities are mathematical consequences of the THRUME precondition. The assertions at `ndcuts.c:398` and `ndcuts.c:410` would catch any violation if somehow reached, but they cannot be reached through the normal call path [INV-NO-ZERO-WIDTH-CRUM].

**What happens at crum boundaries**

When a delete boundary aligns exactly with a crum's grasp (`whereoncrum == ONMYLEFTBORDER`) or reach (`whereoncrum == ONMYRIGHTBORDER`), `slicecbcpm` is **not called at all** — the crum is handled whole in Phase 2 classification [PRE-DELETE, Finding 0075]. Boundary alignment produces zero fragments from `slicecbcpm`, not zero-width fragments.

**Formal invariant**

`∀ crum ∈ bottom_crums(enf) : crum.width > 0` — no DELETE Phase 1 cutting operation can produce a degenerate zero-width crum [INV-NO-ZERO-WIDTH-CRUM]. This is enforced structurally by the guard in `makecutsbackuptohere`, making it a caller-enforced precondition on `slicecbcpm` rather than an internal check within `slicecbcpm` itself.

---

## Code Exploration

Now I have enough to give a thorough, cited answer.

---

## `slicecbcpm`: Two Pieces, Zero-Width Analysis

### Does it always produce exactly two pieces?

**Yes, unconditionally.** The function creates the left piece in-place (`ptr`, narrowed) and creates exactly one right piece (`new`), then links it into the tree with a single `adopt(new, RIGHTBRO, ptr)` call [`backend/ndcuts.c:448`]. There is no branching that could produce one piece or three — the split is structurally hardwired to two.

---

### Are both pieces guaranteed to have positive widths?

#### The Cut Dimension (`index`)

**Yes, for the cut dimension.** The chain of reasoning is tight:

**Step 1 — THRUME means strictly interior.**

`whereoncrum` [`backend/retrie.c:345-398`] computes:

```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
// left = offset[index] + cdsp[index]  (crum's absolute start)

tumbleradd(&left, &ptr->cwid.dsas[index], &right);
// right = left + cwid[index]          (crum's absolute end)

// Returns THRUME only when:  left < address < right  (strictly)
```

THRUME is returned only when `address > left && address < right` — both boundary values are excluded. If cut is at the left boundary, `whereoncrum` returns `ONMYLEFTBORDER`; at the right, `ONMYRIGHTBORDER`. Guard 1 [`ndcuts.c:383-388`] aborts with `gerror()` unless the result is exactly `THRUME`.

**Step 2 — `localcut` is therefore strictly positive and strictly less than the crum's width.**

```c
tumblersub(cut, &grasp.dsas[index], &localcut);
// localcut = cut - left
```
[`ndcuts.c:396`]

Since `left < cut < right = left + cwid[index]`, we get `0 < localcut < cwid[index]`.

**Step 3 — The width arithmetic cannot zero out either piece.**

```c
movewisp(&ptr->cwid, &newwid);                          // copy original width
for (i = 0; i < widsize(enftype); i++) {
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0]; // set lowest digit
    tumblerjustify(&newwid.dsas[i]);                    // normalize
}                                                        // [ndcuts.c:438-442]
```

`localcut` is 1-story (enforced by Guard 4, [`ndcuts.c:410-430`]), meaning it has only `mantissa[0]` nonzero. Since `localcut > 0`, `localcut.mantissa[0] != 0`. `tumblerjustify` [`tumble.c:289-313`] returns immediately when `mantissa[0] != 0` — it only shifts leading zeros — so `newwid.dsas[index]` = localcut, which is strictly positive.

```c
locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid,
             (tumbler*)&new->cwid, (unsigned)widsize(enftype));
// new->cwid = ptr->cwid - newwid = cwid - localcut > 0

movewisp(&newwid, &ptr->cwid);
// ptr->cwid = newwid = localcut > 0
```
[`ndcuts.c:444-445`]

Both pieces have strictly positive width in dimension `index`.

---

#### The Non-Cut Dimensions (i ≠ index)

**This is where a latent gap exists.**

The loop at [`ndcuts.c:439-442`] sets `newwid.dsas[i].mantissa[0] = localcut.mantissa[0]` for **every dimension** `i`, not just the cut dimension. The comment at line 439 reads:

```c
for (i = 0; i < widsize(enftype); i++) {/* I really don't understand this loop */
```

For a 2D POOM (widsize = 2, dimensions I and V), both `newwid.dsas[0]` and `newwid.dsas[1]` get set to `localcut.mantissa[0]`. Then `new->cwid[i] = ptr->cwid[i] - localcut.mantissa[0]` for all i via `locksubtract`.

For the non-cut dimension, **nothing in the function explicitly prevents** `ptr->cwid[non-index] == localcut.mantissa[0]`, which would produce `new->cwid[non-index] == 0` via `tumblersub`'s `tumblerclear(cptr)` branch [`tumble.c:416-417`]:

```c
else if (tumblereq(aptr, bptr))
    tumblerclear(cptr);   // zero result — no guard here
```

The function's correctness in non-cut dimensions relies on an **implicit POOM structural invariant**: that all width dimensions are equal (or at least that the I-width is always ≥ the V-width at the cut). This invariant is enforced upstream by the enfilade construction, not within `slicecbcpm` itself.

---

### The Five Guards — What They Actually Protect

| Guard | Location | What it prevents |
|-------|----------|-----------------|
| `whereoncrum != THRUME` | `ndcuts.c:383` | Cut at or outside boundary → prevents zero-width in cut dimension |
| `!lockis1story(ptr->cwid)` | `ndcuts.c:389` | Multi-story widths (complex hierarchical values) |
| `localcut.exp != ptr->cwid.dsas[index].exp` | `ndcuts.c:398` | Exponent mismatch at wrong hierarchy level |
| `!is1story(&localcut)` | `ndcuts.c:410` | Multi-story cut value |
| `tumblerlength(cut) != tumblerlength(cwid)` | `ndcuts.c:431` | Level (precision) mismatch |

None of these guards explicitly check that `ptr->cwid[i] > localcut.mantissa[0]` for dimensions `i ≠ index`.

---

### Conclusion

`slicecbcpm` **always produces exactly two pieces**. For the cut dimension, **both pieces are guaranteed to have strictly positive widths**, enforced by the THRUME precondition (which establishes `0 < localcut < cwid[index]`) combined with the 1-story constraint (which ensures the width arithmetic operates on single-digit values without underflow ambiguity).

For non-cut dimensions, zero-width fragments **are theoretically possible** if the per-dimension width happens to equal `localcut.mantissa[0]`. The code relies on a POOM structural invariant — never locally checked — that all dimensions' widths are consistent relative to the cut. The author's own comment ("I really don't understand this loop") at [`ndcuts.c:439`] acknowledges the multi-dimensional behavior was not fully reasoned through at the time of writing.

---

## Question 15 [gregory]

> When COPY brings in a multi-span specset where some source spans happen to be I-address-contiguous with existing target POOM entries, does `isanextensionnd` coalesce across the specset boundary — merging the last byte of one copied span with the first byte of the next if they are I-adjacent?

### Gregory's Answer

## KB Synthesis

## Short answer: Yes, but only when all three extension conditions coincidentally align

`isanextensionnd` has no awareness of specset structure. It inspects only the current POOM state against the incoming insertion. The check is purely arithmetic [PRE-COPY / Finding 0046]:

1. **Same `homedoc`**: the new content's I-address origin document matches the existing crum's recorded `homedoc`
2. **V-contiguity**: the new content's target V-origin equals the existing crum's V-reach
3. **I-contiguity**: the new content's I-origin equals the existing crum's I-reach

When COPY processes a multi-span specset, `docopy` converts the full specset to I-spans via `specset2ispanset`, then iterates through the resulting I-spans calling `insertpm` for each. After span N is inserted, a POOM crum exists covering it. When span N+1 is subsequently inserted, `isanextensionnd` checks the crum created by span N against the incoming data — the fact that they came from adjacent VSpecs is invisible to it.

Therefore, if span N's last byte maps to I-address `α_k` (reach = `α_{k+1}`) and span N+1's first byte happens to be `α_{k+1}`, AND both are being placed at V-positions such that the target V-addresses are also contiguous, AND both came from the same source document (`homedoc` match) — coalescing fires. The specset boundary is not a barrier.

### Conditions that make cross-boundary coalescing likely

From [ST-VCOPY] (Finding 0046) and [INV-MONOTONIC] (Finding 0033):

- **I-contiguity**: arises naturally when the source spans were originally inserted sequentially with no intervening `CREATELINK` or other non-text allocations between them [INT-LINK-INSERT / Finding 0063]. Spans from fragmented or multi-source content will not be I-contiguous.

- **V-contiguity**: requires that the caller places span N+1 immediately after span N at the target. Since specset order determines insertion order [INV-SPECSET-ORDER], if the VSpecs in the specset describe adjacent target positions, this holds.

- **Same homedoc**: requires both spans originated from the same source document. Cross-document specsets (referencing content from multiple documents) will fail this check [PRE-COPY].

### What the KB does not cover

The KB has no direct experimental evidence for or against cross-specset coalescing. This answer is inferred from the code-level description of `isanextensionnd` in [PRE-COPY / Finding 0046] and [ST-INSERT / Finding 0062] — neither of which mentions specset structure as a factor. If you need a definitive answer, a targeted test (two I-contiguous spans in a single specset copied to contiguous target V-positions, then checking crum count) would confirm it.

---

## Code Exploration

I have all the code I need. Here is the complete analysis with citations.

---

## Answer: Does `isanextensionnd` coalesce across the specset boundary?

**Short answer: Yes — but only when the two consecutive specset spans share the same source document (homedoc). The V-address alignment is automatic and exact; the homedoc check is the decisive gate.**

---

### Call Chain for COPY

`docopy` [do1.c:45–65] converts its specset to an ispanset and calls:

```c
insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   /* do1.c:60 */
```

`insertpm` [orglinks.c:75–134] iterates span-by-span over the sporglset:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);
    movetumbler (&lwidth,  &crumwidth.dsas[I]);
    movetumbler (vsaptr,   &crumorigin.dsas[V]);   // V-origin = current VSA
    // ... compute crumwidth.dsas[V] from lwidth ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);   // advance VSA  [orglinks.c:131]
}
```

The critical line is [orglinks.c:131]: `vsaptr` is advanced by span A's V-width immediately after `insertnd` returns, *before* span B is processed. Span B therefore receives `crumorigin.dsas[V]` = span A's V-end, making B's V-origin exactly equal to A's V-reach.

---

### What `isanextensionnd` Tests

`insertcbcnd` [insertnd.c:242–275] iterates all bottom crums in the father, testing each against:

```c
if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr))  /* insertnd.c:250 */
```

`isanextensionnd` [insertnd.c:301–309]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);                              /* homedoc gate */
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas,
                    (unsigned)dspsize(ptr->cenftype)));
}
```

**`prologuend`** [retrie.c:334–339] computes:

```
grasp = offset + ptr->cdsp          (absolute start)
reach = grasp  + ptr->cwid          (absolute end)
```

**`dspsize(POOM) = DSPSIZEPM = 2`** [wisp.h:26], meaning a POOM displacement contains two tumblers: `dsas[I]` and `dsas[V]`.

**`lockeq`** [wisp.c:261–267] iterates over exactly `loxize` tumblers:

```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize)
{
    while (loxize--)
        if (!tumblereq (lock1++, lock2++))
            return(FALSE);
    return(TRUE);
}
```

With `loxize = 2`, it requires `reach.dsas[I] == origin.dsas[I]` **AND** `reach.dsas[V] == origin.dsas[V]` simultaneously. There is no way to satisfy only the I-dimension.

---

### The Specset-Boundary Scenario

Suppose the ispanset contains two consecutive spans A and B that are I-adjacent:
- Span A: I-range = `[Ia, Ia+wa)`, inserted at V-start `Vs`
- Span B: I-range = `[Ia+wa, Ia+wa+wb)` — I-adjacent to A

After `insertnd` for A:
- A's POOM crum has reach: `(I: Ia+wa, V: Vs+wa)`
- `vsaptr` is advanced to `Vs+wa`

`insertnd` for B uses:
- `crumorigin.dsas[I]` = `Ia+wa`
- `crumorigin.dsas[V]` = `Vs+wa` (the advanced vsaptr)

So B's origin = `(I: Ia+wa, V: Vs+wa)` = A's reach exactly.

`isanextensionnd` now checks:
1. **Homedoc:** from `unpacksporgl` [sporgl.c:184–187], if both are SPORGLID items, `infoptr->homedoc` = `sporglptr->sporgladdress`. If A and B came from the same source document, the homedoc tumblers match → passes. If from different source documents → returns `FALSE` immediately, no coalescence.
2. **`lockeq(reach, origin, 2)`:** as shown above, `reach == origin` in both dimensions → `TRUE`.

**When the homedoc check passes, `isanextensionnd` fires and `dspadd(&ptr->cwid, width, &ptr->cwid, ...)` [insertnd.c:251] widens A's crum to absorb B** — the two POOM entries are merged into one.

---

### Interaction with Pre-Existing POOM Entries

For an existing crum C with V-reach = `V_old`:
- C's reach = `(I: some_I_end, V: V_old)`
- First copied span's origin = `(I: A.I.start, V: vsaptr)`

The V-contiguity condition `V_old == vsaptr` is **not generally true** — it holds only if COPY's insertion VSA happens to land at exactly the V-end of C. This is coincidental, not structural. The systematic coalescence effect described above is exclusive to *intra-loop* span pairs within a single `insertpm` call.

---

### Summary

| Condition | Result |
|-----------|--------|
| Consecutive spans in specset, same source document, I-adjacent | **Coalesced** into one POOM crum — V-alignment is guaranteed by `vsaptr` advancement at [orglinks.c:131] |
| Consecutive spans in specset, different source documents, I-adjacent | **Not coalesced** — homedoc check at [insertnd.c:305] fails first |
| New span I-adjacent to a pre-existing POOM crum | **Not systematically coalesced** — requires V-contiguity too, which is not guaranteed |

`isanextensionnd` tests both I and V dimensions atomically via `lockeq(..., dspsize(POOM))` = `lockeq(..., 2)` [insertnd.c:308, wisp.h:26, wisp.c:263–265]. The VSA-advancement loop in `insertpm` [orglinks.c:131] is precisely what creates automatic V-adjacency between successive spans, making the I-adjacency condition both necessary and sufficient for intra-specset coalescence (same homedoc).

---

## Question 16 [gregory]

> Is there an ordering invariant on sibling bottom crums within a single POOM loaf — must their V-displacements be sorted left-to-right, or does `incontextlistnd` compensate for arbitrary physical ordering during retrieval?

### Gregory's Answer

## KB Synthesis

**Physical sibling order in POOM loafs does not need to be V-sorted. `incontextlistnd` compensates by performing insertion-sort at retrieval time.**

## The Core Answer

[SS-CONTEXT-LIST] makes the distinction explicit:

- **POOM (2D)** uses `incontextlistnd()` — **insertion-sort**, because "tree order does not guarantee V-order"
- **GRAN (1D)** uses `oncontextlistseq()` — **sequential append**, because "sequential order is maintained by tree structure"

The choice of accumulation function is precisely the acknowledgment that POOM sibling order carries no V-ordering guarantee.

## Why Physical Order Is Arbitrary

Three mechanisms contribute to unordered physical sibling sequences in a POOM loaf:

**1. Insertion order (right-brother append)**
[SS-ENFILADE-TREE Finding 0041]: New entries are adopted as the `RIGHTBRO` of the retrieval position — chronological append, not V-position order. Sequential inserts at arbitrary V-positions produce siblings in insertion-time order, not address order.

**2. Rebalancing sorts by diagonal, not V-address**
[SS-ENFILADE-TREE Finding 0071]: `getorderedsons` during `recombinend` sorts children by `cdsp.dsas[0] + cdsp.dsas[1]` (L1 norm / diagonal). For a POOM where dimension 0 is I-space (ORGLRANGE) and dimension 1 is V-space (SPANRANGE), this diagonal ordering is not equivalent to V-address ordering.

**3. Split distributes by diagonal, not by V-address**
[ST-SPLIT-2D Finding 0071]: `splitcrumpm` peels off the child with the largest `dsas[SPANRANGE]` only (ignoring the ORGLRANGE), while `recombinend` uses the diagonal key — further divergence between physical order and V-order.

## How `incontextlistnd` Compensates

[INV-RETRIEVAL-V-SORTED Finding 0078]:

> `incontextlistnd()` performs explicit insertion-sort by V-address as contexts are discovered during B-tree traversal. Each leaf node found by `findcbcinarea2d()` is inserted into a linked list at the position that maintains ascending order of `totaloffset.dsas[index]`

[INV-RETRIEVAL-TREE-INDEPENDENCE Finding 0078] states this as an invariant:

> The V-ordering of retrieval results is independent of the internal B-tree structure … Tree structure affects storage and traversal efficiency, but not the ordering of results.

So the postcondition `contexts[j].totaloffset.dsas[V] ≤ contexts[k].totaloffset.dsas[V]` for all `j < k` holds regardless of physical sibling arrangement.

## Contrast With GRAN

For the 1D granfilade, `oncontextlistseq` simply appends in tree traversal order. This works because GRAN inserts always append as right-brothers in address order (allocation is monotonically increasing [INV-MONOTONIC]), so the left-to-right sibling walk of `findcbcseqcrum` [SS-ENFILADE-TREE Finding 0041] naturally yields sequential order.

POOM lacks this property because V-positions are not monotonically increasing across operations — inserts, rearrangements, and transclusions place content at arbitrary positions — so no insertion discipline could maintain physical V-order in siblings.

---

## Code Exploration

I now have all the evidence needed. Here is the full answer:

---

## Ordering Invariant on POOM Loaf Siblings

**Answer: There is no V-ordering invariant on sibling bottom crums within a POOM loaf.** Physical left-to-right sibling position in a loaf is completely independent of V-displacement. `incontextlistnd` explicitly compensates during area retrieval, and single-point retrieval (`findcbcnd`) also works correctly under arbitrary physical ordering.

---

### 1. `cdsp` Is an Absolute Displacement from the Parent's Grasp — Not Sequential

In a GRAN (sequential) enfilade, the running offset across siblings is cumulative: each sibling's absolute position depends on the widths of all predecessors. POOM is fundamentally different.

From `wisp.h:19-20`:
```c
#define I  0
#define V  1
```

Every POOM crum stores `cdsp.dsas[V]` as an **absolute displacement from its parent's grasp position** in V-space. The position formula, from `whereoncrum` [`retrie.c:356`]:
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
```
is `left = parent_grasp + crum_cdsp`, with no dependence on any sibling's width or position. Sibling crums are independently positioned.

---

### 2. Insertion Always Places New Bottom Crums at the Physical Left

`insertcbcnd` [`insertnd.c:260-263`]:
```c
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);          /* SON == LEFTMOSTSON */
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
```
`SON` is `LEFTMOSTSON` [`enf.h:137`]. Every newly inserted bottom crum is physically prepended to the loaf regardless of its V-displacement. A crum with V-address 1000 could be the first child in the loaf while a crum with V-address 1 sits at the rightmost position.

---

### 3. `incontextlistnd` Explicitly Re-Sorts by V During Area Retrieval

The function's own comment is definitive [`context.c:74`]:
```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
```

Its body performs an insertion-sort into the output list [`context.c:90-111`]:
```c
if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
    /* on beginning */
    c->nextcontext = clist;
    *clistptr = c;
    return(0);
} else {
    for (; nextc = clist->nextcontext; clist = nextc) {
        /* in middle */
        if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
            && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
            c->nextcontext = nextc;
            clist->nextcontext = c;
            return(0);
        }
    }
}
/* on end */
clist->nextcontext = c;
```
Using `whereoncontext`, which for POOM compares against `totaloffset.dsas[index]` and `contextwid.dsas[index]`, it inserts each discovered bottom crum into the correct position in the sorted output list.

---

### 4. Area Retrieval Traverses Siblings in Physical Order, Then Sorts on Output

`findcbcinarea2d` [`retrie.c:252-265`] iterates siblings physically left-to-right:
```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, ...)) continue;
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, ...);
        findcbcinarea2d (findleftson (...), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);    /* ← sorts here */
    }
}
```

`makecontextfromcbc` computes the crum's absolute V-position internally [`context.c:167`]:
```c
dspadd(&context->totaloffset, &crumptr->cdsp, &context->totaloffset, (INT)crumptr->cenftype);
```
After this, `incontextlistnd` places the new context in the correct sorted position. The traversal order is irrelevant to output correctness.

---

### 5. Single-Point Retrieval (`findcbcnd`) Also Requires No Ordering

`findcbcnd` [`retrie.c:208-227`] does a linear scan of all children:
```c
for (ptr = findleftson ((typecuc*)father); ptr; ptr = getrightbro (ptr))
    if (retr = findcbcnd (ptr, &grasp, address, index))
        break;
```
At the top of each recursive call it checks:
```c
if ((cmp = whereoncrum (father, offsetptr, address, index)) < ONMYLEFTBORDER || cmp > THRUME)
    return (NULL);
```
Each child is tested independently against the target address using its own `cdsp`. No binary search, no ordering assumption — pure linear scan with independent position tests.

---

### 6. The Split Criterion Is V-Magnitude, Not V-Rank — and Doesn't Reorder

`splitcrumpm` [`split.c:117-128`] selects the child with the **largest** `cdsp.dsas[SPANRANGE]` (= V) to peel off:
```c
for(correctone=ptr=findleftson(father); ptr; ptr = findrightbro(ptr)) {
    if (tumblercmp (&ptr->cdsp.dsas[SPANRANGE], &correctone->cdsp.dsas[SPANRANGE]) == GREATER)
        correctone = ptr;
}
peelcrumoffnd(correctone);
```
`peelcrumoffnd` [`split.c:151-155`] then creates a new sibling UC and adopts the selected crum as its `LEFTMOSTSON`. The remaining siblings stay in whatever physical order they had — they are not re-sorted.

`recombinend` uses `getorderedsons` → `shellsort` [`recombine.c:270-310`], which sorts by the **diagonal sum** `cdsp[0] + cdsp[1]`, not by V alone. This ordering is used only to select recombination candidates, not to impose a persistent storage invariant.

---

### 7. `findsontoinsertundernd` Confirms No Ordering Assumption

When finding which UC subtree to descend into for insertion [`insertnd.c:284-298`]:
```c
for (; ptr; ptr = findrightbro(ptr)) {
    tumbleradd(&grasp->dsas[index], &ptr->cdsp.dsas[index], &sonstart);
    if (tumblercmp (&sonstart, &origin->dsas[index]) != GREATER
     && tumblercmp (&ptr->cdsp.dsas[index], &nearestonleft->cdsp.dsas[index]) != LESS) {
        nearestonleft = ptr;
    }
    if (whereoncrum(ptr, grasp, &origin->dsas[index], index) >= ONMYLEFTBORDER
     && whereoncrum(ptr, grasp, &spanend, index) <= ONMYRIGHTBORDER)
        return (ptr);
}
return (nearestonleft);
```
This is a full scan of all siblings; it does not binary-search or short-circuit based on any sorted-order assumption.

---

### Summary

| Claim | Evidence |
|-------|----------|
| No V-ordering invariant maintained during insert | `adopt(new, SON=LEFTMOSTSON, ...)` in `insertcbcnd` [insertnd.c:262] |
| `cdsp` is absolute, not relative to previous sibling | `whereoncrum` [retrie.c:356], POOM case |
| Area retrieval output is V-sorted regardless of storage | `incontextlistnd` called per bottom crum in `findcbcinarea2d` [retrie.c:263], comment "put c on clist in index order" [context.c:74] |
| Single-point retrieval scans all siblings linearly | `findcbcnd` loop [retrie.c:220-222] |
| Split selects by V-magnitude, doesn't reorder | `splitcrumpm` [split.c:122-125] |
| Recombine uses diagonal sort, not V-sort | `shellsort` by `cdsp[0]+cdsp[1]` [recombine.c:296-310] |

**Physical ordering of sibling bottom crums in a POOM loaf is arbitrary and operationally irrelevant.** All position information is self-contained in each crum's `cdsp`. `incontextlistnd` is not a workaround for a broken invariant — it is the intended and sufficient mechanism for producing ordered output from unordered storage.

---

## Question 17 [gregory]

> After REARRANGE with a 3-cut pivot, can a single pre-existing bottom crum that straddled a cut boundary end up split into two non-contiguous entries in V-space while still referencing a contiguous I-address range — and if so, is there any post-rearrange coalescing pass?

### Gregory's Answer

## KB Synthesis

## Short Answer

No — REARRANGE does not split bottom crums at cut boundaries. A crum that straddles a cut moves as a whole unit and remains a single contiguous entry. There is no post-rearrange coalescing pass.

---

## Detailed Analysis

### REARRANGE has no pre-cutting phase

DELETE uses a two-phase algorithm: Phase 1 runs `slicecbcpm` to split any bottom crum whose interior is touched by a cut boundary (only when `whereoncrum == THRUME`), then Phase 2 classifies and removes/shifts the resulting clean crums [PRE-DELETE, Finding 0075].

REARRANGE has no equivalent Phase 1. The full algorithm described in [ST-REARRANGE] (Finding 0056) is:

1. `sortknives()` — sort cut points ascending
2. `makeoffsetsfor3or4cuts()` — compute a displacement vector per region
3. `rearrangecutsectionnd()` — assign each crum to a region (0, 1, 2, or 3)
4. `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], &ptr->cdsp.dsas[V])` — apply displacement in-place

No slice, no copy, no content creation. Each POOM bottom crum is displaced as an atomic unit.

### What happens to a straddling crum

Say a crum covers V-range [1.3, 1.5) → {I_C, I_D}, and the pivot cuts are at [1.2, 1.4, 1.6]:

- Region 1 = [1.2, 1.4): `diff[1] = +0.2`
- Region 2 = [1.4, 1.6): `diff[2] = -0.2`

The crum's grasp (1.3) falls in region 1, so `rearrangecutsectionnd` classifies the whole crum as region 1. The entire crum is displaced by +0.2, landing at [1.5, 1.7). The bytes I_C and I_D remain in one contiguous crum. They do **not** get split into two entries.

The trade-off: I_D, which conceptually belongs to region 2 (its grasp 1.4 equals `cut1`), ends up at V 1.6 instead of V 1.2. The V-I mapping is distorted for the bytes that straddle the boundary, but the crum structure stays intact — one crum, contiguous in both V-space and I-space.

This is consistent with [INV-REARRANGE-IDENTITY]: "The code modifies only `ptr->cdsp.dsas[index]`... No I-addresses are touched, no content is copied." Identity is preserved; correctness of placement for straddling bytes is not.

### Source of the fragmentation in EC-PIVOT-LINK-FRAGMENTATION

The four-span endset fragmentation observed in [EC-PIVOT-LINK-FRAGMENTATION] comes from a different mechanism: *separate* crums that originally held adjacent bytes land at non-contiguous V-positions after pivot. For example, if "C" (in region 1) and "D" (in region 2) were in separate crums, C moves to V 1.5 and D moves to V 1.2 — previously adjacent, now disjoint. The link endset then reflects two separate V-ranges for what were originally contiguous I-addresses.

A single straddling crum, by contrast, moves together and never fragments internally.

### No post-rearrange coalescing pass

There is no documented coalescing step after REARRANGE. The `isanextensionnd` check that merges adjacent inserts fires during the INSERT path's `insertnd` flow [ST-INSERT, Finding 0062]; REARRANGE never calls this path — it only calls `tumbleradd` on existing crums. The structural rebalancer `recombinend` [ST-REBALANCE-2D] is a B-tree occupancy balancer, not a content-coalescing pass. Adjacent crums that happen to land at contiguous V- and I-positions after displacement are **not** automatically merged.

---

## Code Exploration

Now I have everything needed. Let me compile the complete answer.

---

## Answer

### Short Answer

**Yes** — a pre-existing bottom crum straddling a cut boundary is split into two by `slicecbcpm`, and after rearrangement those two halves receive different V-space displacement offsets, placing them at non-contiguous V-space addresses while their I-address content remains contiguous. **No** — there is no post-rearrange coalescing pass that redetects and merges them.

---

### Step 1 — Entry Point: `rearrangend` [edit.c:78–160]

`rearrangend` for a 3-cut rearrange:

1. Fills `knives` with 3 blades (A < B < C after sort) [edit.c:102–107]
2. Computes per-section displacement offsets [edit.c:108]:
3. **Makes the cuts**: `makecutsnd(fullcrumptr, &knives)` [edit.c:110]
4. Finds the intersection (trivially the fullcrum itself): `newfindintersectionnd` [edit.c:111, ndinters.c:38–42] just does `*ptrptr = fullcrumptr`
5. Iterates over all sons of the fullcrum, calls `rearrangecutsectionnd` [edit.c:113–136]
6. Applies `diff[section]` to V-displacement of each son [edit.c:125]
7. `setwispupwards(father, 1)` [edit.c:137]
8. `recombine(fullcrumptr)` [edit.c:139]
9. `splitcrumupwards(fullcrumptr)` [edit.c:141]

---

### Step 2 — Cutting Phase Splits the Straddling Crum

In `makecutsbackuptohere` [ndcuts.c:69–91], when `ptr->height == 0` (bottom crum):

```c
for (i = 0; i < knives->nblades; i++) {
    if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
        new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
        slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
```

`THRUME = 0` [common.h:88] means the knife address falls **strictly inside** the crum — it straddles the cut. `whereoncrum` [retrie.c:345–398] for SPAN/POOM computes `left = offset[index] + cdsp[index]`, `right = left + cwid[index]`, and returns THRUME when `left < address < right`.

#### What `slicecbcpm` does [ndcuts.c:373–450]

```c
tumblersub(cut, &grasp.dsas[index], &localcut);        // cut pos relative to crum start
// build newwid = left portion's width (up to cut)
locksubtract(&ptr->cwid, &newwid, &new->cwid, ...);    // new->cwid = remainder
movewisp(&newwid, &ptr->cwid);                          // ptr truncated to left portion
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);   // new starts right after
move2dinfo(&((type2dcbc*)ptr)->c2dinfo,
           &((type2dcbc*)new)->c2dinfo);                // same home-doc
adopt(new, RIGHTBRO, ptr);                              // new inserted to right
```

After `slicecbcpm`:

| Half | cdsp (V-origin) | cwid (V-width) | I-space |
|------|----------------|----------------|---------|
| Left (`ptr`) | original cdsp | `localcut` (up to cut) | same home-doc, first sub-range |
| Right (`new`) | `ptr->cdsp + localcut` | `original cwid - localcut` | same home-doc, second sub-range (contiguous) |

The two halves are **V-adjacent** (right-bro relationship) and reference **contiguous I-addresses** (same `c2dinfo.homedoc`, width split at the cut point).

---

### Step 3 — Rearrangement Displaces the Two Halves Differently

`makeoffsetsfor3or4cuts` [edit.c:177–183] for 3 blades:

```c
tumblersub(&knives->blades[2], &knives->blades[1], &diff[1]);  // diff[1] = C - B
tumblersub(&knives->blades[1], &knives->blades[0], &diff[2]);  // diff[2] = B - A
diff[2].sign = !diff[2].sign;                                   // negate → diff[2] = -(B-A)
tumblerclear(&(diff[3]));                                       // diff[3] = 0
```

`rearrangecutsectionnd` [edit.c:191–204] determines the section by iterating from the rightmost knife downward:

```c
for (i = knives->nblades-1; i >= 0; --i) {
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME) return(-1);           // ERROR — must never happen post-cut
    else if (cmp <= ONMYLEFTBORDER) return(i+1);  // crum is at or right of this blade
}
return(0);
```

`ONMYLEFTBORDER = -1` [common.h:87], so `cmp <= ONMYLEFTBORDER` is true when the cut address is at or to the left of the crum.

For a crum originally straddling blade `k`, after cutting:

- **Left half** (ends exactly at blade[k]): `whereoncrum(..., blades[k])` → `ONMYRIGHTBORDER` (cut is on its right border, not ≤ ONMYLEFTBORDER). Loop continues to k-1, where the cut is to the left → returns **section k**.
- **Right half** (starts exactly at blade[k]): `whereoncrum(..., blades[k])` → `ONMYLEFTBORDER` (cut is on its left border, ≤ ONMYLEFTBORDER) → returns **section k+1**.

Then [edit.c:124–128]:
```c
case 1: case 2: case 3:
    tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
```

The displacement applied to each:

| Straddled blade | Left half section | Left half gets | Right half section | Right half gets |
|----------------|-------------------|-----------------|-------------------|-----------------|
| blade[0] = A | 0 | *no change* (case 0) | 1 | diff[1] = C−B |
| blade[1] = B | 1 | diff[1] = C−B | 2 | diff[2] = −(B−A) |
| blade[2] = C | 2 | diff[2] = −(B−A) | 3 | diff[3] = 0 |

In every non-degenerate case, the two halves receive **different offsets**. Their cdsp values diverge. They are no longer V-adjacent after rearrangement.

Their I-address content is unchanged: `move2dinfo` copied the home-doc reference at split time [ndcuts.c:447], and nothing in the rearrangement loop touches `c2dinfo`. The two bottom crums still reference the same underlying document at contiguous sub-ranges.

---

### Step 4 — Post-Rearrange Passes: No Coalescing

`rearrangend` ends with two calls [edit.c:137–141]:

```c
setwispupwards(father, 1);   // wisp bookkeeping only
recombine(fullcrumptr);
(void)splitcrumupwards(fullcrumptr);  /* can we move this before recombine ?*/
```

#### `recombine` [recombine.c:22–34, 104–131]

For SPAN/POOM, dispatches to `recombinend`:

```c
int recombinend(typecuc *father)
{
    if (father->height < 2 || !father->modified) return(0);  // bails on height-1 and leaves
    for (ptr = getleftson(father); ptr; ptr = getrightbro(ptr))
        recombinend(ptr);
    getorderedsons(father, sons);
    for (i = 0; i < n-1; i++)
        for (j = i+1; ...; j++)
            if (ishouldbother(sons[i], sons[j]))
                takeovernephewsnd(&sons[i], &sons[j]);
```

`ishouldbother` [recombine.c:150–163] only checks whether the combined son count fits in a loaf and is not RESERVED. It has **no V-space adjacency check**. `takeovernephewsnd` [recombine.c:165–203] and `eatbrossubtreend` [recombine.c:205–232] move subtrees between upper-level nodes to consolidate partially-full loaves — they operate on **intermediate nodes**, not on bottom crums. The bottom crums themselves are not examined for V-space adjacency.

`getorderedsons` sorts by diagonal magnitude (`cdsp[0] + cdsp[1]`) [recombine.c:296–298], which is a spatial ordering heuristic, not an adjacency check. No merging of bottom crums occurs here.

#### `splitcrumupwards` [split.c:16–44]

```c
bool splitcrumupwards(typecuc *father)
{
    if (father->height <= 0) gerror("splitcrumupwards on bottom crum\n");
    for (; toomanysons(father); father = findfather(father)) {
        ...
        splitcrum(father);
    }
```

This only **splits** overfull nodes. It never merges.

**There is no coalescing pass.** The two fragments of the original crum remain as two separate bottom crums with non-contiguous V-space addresses and contiguous I-address content, indefinitely.

---

### Summary

1. **Splitting happens** in `slicecbcpm` [ndcuts.c:373–450] during the `makecutsnd` phase. A bottom crum straddling a 3-cut blade is bisected into two right-bro sibling crums sharing the same `c2dinfo.homedoc` and complementary widths — contiguous I-address content by construction.

2. **Non-contiguity in V-space follows** because `rearrangecutsectionnd` places the two halves in adjacent sections (k and k+1), and `makeoffsetsfor3or4cuts` assigns them different `diff[k]` and `diff[k+1]` values [edit.c:177–183], which are then applied directly to `cdsp` [edit.c:125].

3. **No coalescing pass exists** post-rearrange. `recombine` [recombine.c:104–131] reorganizes upper-level loaf occupancy using `takeovernephewsnd`/`eatbrossubtreend` but has no V-adjacency awareness and never touches bottom crum `cdsp` fields. `splitcrumupwards` [split.c:16–44] only splits. The comment at edit.c:141 — `/* can we move this before recombine ?*/` — reflects the author's own uncertainty about ordering, but neither ordering introduces coalescing.

---

## Question 18 [gregory]

> When DELETE slices a bottom crum that maps to a contiguous I-span, does the surviving fragment preserve exact I-displacement and I-width corresponding to the surviving V-range, or is there any rounding or alignment to tumbler boundaries?

### Gregory's Answer

## KB Synthesis

## What the KB Tells Us

The KB gives us the V-dimension arithmetic for `slicecbcpm` precisely, but is silent on the I-dimension implementation.

**What is documented:**

[PRE-DELETE/Finding 0075] describes the cut arithmetic in V-space:
- `localcut = tumblersub(cut, grasp)` — strictly positive because the THRUME guard ensures `grasp < cut < reach`
- Original crum retains V-width = `localcut`
- New (right) crum receives V-width = `cwid - localcut` via `locksubtract`
- Both results are strictly positive; no zero-width crums can result

[INV-WIDTH-VALUE-EQUIVALENCE] establishes that V-width and I-width encode the **same integer value**, just at different tumbler precisions. This is a crum-level invariant maintained at insert time.

[INV-SINGLE-CHAR-GRANULARITY] establishes the 1:1 linear mapping: every byte occupies exactly one V-position and one I-position. A POOM bottom crum therefore represents a bijective linear mapping — a contiguous V-range maps to an equally-sized contiguous I-range.

[SS-POOM-BOTTOM-CRUM/Finding 0076] confirms crums store independent `(origin, width)` pairs for both V and I dimensions.

**The gap:**

The KB has no finding that directly documents what `slicecbcpm` (`ndcuts.c:396-444`) does to the I-dimension coordinates. Finding 0075 only describes the V-width arithmetic. There is no finding confirming that when the left fragment's V-width is set to `localcut`, the implementation also:
1. Leaves the left fragment's I-origin unchanged
2. Sets the right fragment's I-origin to `i_origin + localcut` (i.e., `tumbleradd(i_origin, localcut)`)
3. Adjusts the right fragment's I-width to `i_width - localcut`

**What can be inferred:**

Given the linear 1:1 structure, *correct* behavior requires exact I-displacement preservation — any rounding or misalignment would violate [INV-WIDTH-VALUE-EQUIVALENCE] for the resulting fragments. The tumbler arithmetic involved (`tumblersub`, `tumbleradd`) is exact for same-exponent operands [SS-TUMBLER/Finding 0031], and text content at the bottom of a POOM crum is uniformly encoded at the same exponent level. So there is no representational forcing of alignment or rounding.

However, the specific implementation of `slicecbcpm`'s I-dimension handling is not in the KB. This is an answerable question from the source code at `ndcuts.c:396-444` but **not answerable from the KB as documented.**

---

## Code Exploration

Now I have enough to give a complete, precisely cited answer. Let me trace the full execution path.

---

## Answer

**The surviving fragment preserves exact I-displacement and I-width.** No rounding or alignment to tumbler boundaries occurs — the split is character-exact. Here is the full execution trace.

---

### 1. Entry Point: `deletevspanpm` → `deletend`

`dodeletevspan` [do1.c:158-167] calls `deletevspanpm` [orglinks.c:145-152]:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

`deletend` [edit.c:31-76] sets up two knives at `origin` (V) and `origin+width` (V), then calls `makecutsnd` to split any crums that straddle those positions, then iterates over children:

```c
case 1:
    disown((typecorecrum*)ptr);
    subtreefree((typecorecrum*)ptr);          // entirely inside delete range
    break;
case 2:
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);  // index = V only
    break;
```

**Case 2 is critical**: only `cdsp.dsas[V]` is adjusted (V-displacement closes the gap). The I-displacement `cdsp.dsas[I]` of surviving crums is left untouched — correct, because I-addresses are permanent.

---

### 2. Slicing the Bottom Crum: `slicecbcpm`

When a knife lands inside a bottom POOM crum (the `THRUME` case), `makecutsbackuptohere` [ndcuts.c:69-140] calls `slicecbcpm` [ndcuts.c:373-450].

**Step 1** — compute `localcut`, the V-distance from the crum's absolute V-start to the knife:

```c
prologuend(ptr, offset, &grasp, NULL);              // grasp = absolute position of crum
tumblersub(cut, &grasp.dsas[index], &localcut);     // index = V
```
[ndcuts.c:382, 396]

**Step 2** — three guards are asserted before any arithmetic:

```c
if (!lockis1story(ptr->cwid.dsas, (unsigned)widsize(enftype)))
    gerror("Not one story in POOM wid\n");           // crum's width is single-story in ALL dims
if (localcut.exp != ptr->cwid.dsas[index].exp)
    gerror("Oh well, I thought I understood this1"); // cut is at the same level as V-width
if (!is1story(&localcut))
    gerror("Oh well, I thought I understood this2"); // cut has no sub-level components
if (tumblerlength(cut) != tumblerlength(&ptr->cwid.dsas[index]))
    gerror("level mismatch");                        // cut and V-width agree on depth
```
[ndcuts.c:389-436]

These collectively enforce that the V-cut is at a **character boundary** — the smallest tumbler unit stored in this crum. A V-cut that falls mid-character (sub-story address) would fail `is1story`.

**Step 3** — the split loop (the one the programmer himself commented *"I really don't understand this loop"*):

```c
movewisp(&ptr->cwid, &newwid);          // copy both I and V widths into newwid
for (i = 0; i < widsize(enftype); i++) {    // widsize(POOM) = 2 → i=0 (I), i=1 (V)
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
    tumblerjustify(&newwid.dsas[i]);
}
```
[ndcuts.c:438-442]

The result for each dimension:
- `newwid.dsas[i].exp` = `ptr->cwid.dsas[i].exp` (unchanged, from `movewisp`)
- `newwid.dsas[i].mantissa[0]` = `localcut.mantissa[0]` (the V-cut character count)
- `newwid.dsas[i].mantissa[1..]` = 0 (guaranteed by `lockis1story` guard)

**Why this is exact**: From `wisp.h:19-20`, I = index 0, V = index 1. For a POOM crum inserted via `insertpm` [orglinks.c:100-131]:

```c
movetumbler(&lwidth, &crumwidth.dsas[I]);        // I-width = character count N at I-level exp
...
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);  // V-width = same count N at V-level exp
```

The V-width and I-width may have **different exponents** (`V.exp = -shift = -(tumblerlength(vsaptr)-1)`, `I.exp = lwidth.exp`), but they have the **same `mantissa[0]`** — both equal to N, the character count. This is the 1:1 V↔I invariant for text content.

So when the loop sets `newwid.dsas[I].mantissa[0] = localcut.mantissa[0]` while preserving `I.exp`, it produces exactly `localcut.mantissa[0]` I-characters — the same count as the surviving V-range. The differing exponents are not a problem: each exponent encodes the hierarchical address depth of that coordinate space, and the character count is the shared mantissa[0] value.

**Step 4** — assign the new crum's I-displacement:

```c
locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, widsize(POOM));
movewisp(&newwid, &ptr->cwid);
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
```
[ndcuts.c:444-446]

After these three operations:

| Fragment | I-displacement | I-width |
|---|---|---|
| **Left** (`ptr`) | original I-start (unchanged) | `localcut.mantissa[0]` at `I.exp` |
| **Right** (`new`) | original I-start + left I-width = original I-start + K | original I-width − K |

`dspadd` operates element-wise via `lockadd` [wisp.c:15-18, 269-273], adding both I and V components independently. The I-displacement of the right fragment is set to `ptr->cdsp.dsas[I] + ptr->cwid.dsas[I]` (original start plus left fragment width) — exact, no rounding.

---

### 3. The Surviving Fragment's I-coordinates After Delete

After both knife positions have been sliced, `deletend`'s loop removes the crums inside the delete range (case 1) and shifts V-displacements of crums to the right (case 2, V only). The surviving left and right fragments have:

- **I-displacement**: Set exactly by `slicecbcpm`'s `dspadd` at the blade positions. Not modified again by `deletend`.
- **I-width**: Set exactly by the `localcut.mantissa[0]` loop in `slicecbcpm`. Equals the character count of the surviving V-range.
- **No rounding**: The `is1story` and `exp`-match assertions guarantee the cut is at a clean character boundary. The tumbler arithmetic (`tumblersub`, `tumbleradd`, `locksubtract`) is exact integer subtraction with no fractional remainder for 1-story tumblers.

---

### Summary of Guarantees and Preconditions

The code enforces exactness through three assertions in `slicecbcpm` [ndcuts.c:389-436]:

1. **`lockis1story`** on all crum wids — the crum spans a single story in every dimension, so character count is fully captured in `mantissa[0]`.
2. **`localcut.exp == ptr->cwid.dsas[V].exp`** — the knife lands at the same tumbler level as the crum's V-extent.
3. **`is1story(&localcut)`** — the cut position has no sub-character components; the cut is at a whole-character boundary.

If any precondition is violated, `gerror` fires and the process aborts. Within those preconditions, **the surviving fragment preserves exact I-displacement and I-width, with no rounding or alignment whatsoever**.

---

## Question 19 [gregory]

> In the 2D POOM enfilade, does the root's I-displacement track the minimum I-address across all entries via `setwispnd`, and does this minimum ever become stale after DELETE removes the entry that held the minimum?

### Gregory's Answer

## KB Synthesis

Yes on both counts — with one important nuance on staleness.

## Root I-Displacement Tracks the Minimum

The POOM is a 2D enfilade (per [SS-ENFILADE-TREE Finding 0060], POOM uses `is2dcrum = TRUE`). For all 2D enfilades, `setwispnd` at `wisp.c:171-228` maintains the root's `cdsp` as the minimum displacement across all children in **both** dimensions simultaneously [SS-ENFILADE-TREE Finding 0066]:

> `root.cdsp` is the upper-left corner (minimum address), `root.cdsp + root.cwid` is the lower-right corner (maximum extent)

The `cdsp` field is a multi-dimensional displacement struct (`dsas[I]` and `dsas[V]`). So `root.cdsp.dsas[I]` does track the minimum I-address (ORGLRANGE dimension) across all entries, updated after every insertion by `setwispnd`.

## Does DELETE Cause Staleness?

**No — `setwispupwards` corrects it after every deletion.**

DELETE operates via `deletend` which classifies crums by their V-range:
- **Case 1** (fully within deletion range): `disown` + `subtreefree` — physically removes the crum [ST-DELETE Finding 0064]
- **Case 2** (after deletion range): shifts V-displacement via `tumblersub`, **I-dimension unchanged** [ST-DELETE Finding 0055]

After processing, `deletend` calls `setwispupwards` on the father node [SS-ENFILADE-TREE Finding 0058], which propagates `setwispnd` up to the root. `setwispnd` scans all remaining children, finds the new minimum in every dimension, absorbs it into the parent's `cdsp`, and adjusts children to relative displacements. If the minimum-I-address crum was a case-1 deletion, the new minimum is found among survivors.

The key formula from [SS-ENFILADE-TREE Finding 0066]:

```
setwispnd:
  mindsp = min(child.cdsp) across all children   // both dims
  root.cdsp += mindsp
  each child.cdsp -= mindsp                        // remain relative
```

After the bottom-up `setwispupwards` reaches the root, `root.cdsp.dsas[I]` correctly reflects the minimum I-address of surviving entries.

## The One Complication: Disabled `levelpull`

[SS-ENFILADE-TREE Finding 0058] notes that `levelpull` is disabled, so tree height never decreases after deletions. Empty intermediate nodes persist. However, `setwispnd` on an empty node (no remaining children) clears both `cdsp` and `cwid` to zero [`wisp.c:187-189`], so even the fully-deleted case is handled correctly — it doesn't corrupt the I-displacement tracking, it just leaves a taller-than-necessary tree structure.

**Summary:** Root I-displacement is never stale after DELETE. The `setwispupwards` → `setwispnd` chain that follows every structural modification recomputes the minimum across surviving entries. Staleness could only arise if `setwispupwards` were skipped, but `deletend` always calls it on the father before returning.

---

## Code Exploration

I now have all the source I need. Here is my complete answer:

---

## POOM Root I-Displacement: `setwispnd` and DELETE Staleness

### 1. Does `setwispnd` track the minimum I-address in the root's `cdsp`?

**Yes — by construction, through a bottom-up pass.**

`setwispnd` is the "widditive operation for nd" (N-dimensional enfilades, i.e. POOM and SPAN). Its definition is at `backend/wisp.c:171–228`. The key passage:

```c
/* find new upper-left corner */
movewisp (&ptr->cdsp, &mindsp);                                     // wisp.c:193
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr))   {
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp,           // wisp.c:195
             (tumbler*)&mindsp, (unsigned)dspsize(ptr->cenftype));
}
```

Starting from the leftmost child's `cdsp`, it takes the element-wise tumbler minimum (`lockmin`) across all surviving children. For POOM, `dspsize(POOM)` covers both the I and V dimensions simultaneously, so **both components of the minimum are recomputed**.

The result `mindsp` is the minimum child-relative displacement. The new absolute `cdsp` for the father is:

```c
dspadd (&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype); // wisp.c:200
```

Then the children's `cdsp` values are re-relativized by subtracting `mindsp`:

```c
dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);    // wisp.c:211
```

This ensures the invariant: every internal node's `cdsp` is the minimum displacement of its children relative to itself. At the root, `cdsp` therefore encodes the **absolute minimum I-address** (and V-address) of all entries in the tree.

`setwispnd` is reached via `setwisp` [`wisp.c:121–140`], dispatching on `POOM` or `SPAN`:
```c
case POOM:
    return (setwispnd ((typecuc*)ptr));                           // wisp.c:131
```

And `setwisp` is called in the upward sweep `setwispupwards` [`wisp.c:83–111`]:
```c
for (changed = TRUE; changed && ptr; ptr = father) {
    father = findfather ((typecorecrum*)ptr);
    changed = setwisp ((typecorecrum*)ptr);                       // wisp.c:97
}
```

---

### 2. Does the minimum become stale after DELETE removes the entry that held it?

**No — the minimum is fully recomputed from surviving children after every delete.**

The delete path is:

```
dodeletevspan()       [do1.c:158]
  → deletevspanpm()  [orglinks.c:145]
    → deletend()     [edit.c:31]
      → setwispupwards(father, 1)   [edit.c:74]
```

`deletevspanpm` calls `deletend` with `index = V` [`orglinks.c:149`]:
```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

Inside `deletend`, the loop over children classifies each child via `deletecutsectionnd` [`edit.c:49`]:
- **Case 1** (fully within the deleted V-range): child is removed via `disown` + `subtreefree` [`edit.c:59–60`]
- **Case 2** (after the deleted V-range): child's V-displacement is decremented [`edit.c:63`]
- **Case 0** (before the deleted V-range): left untouched

After the loop, unconditionally:
```c
setwispupwards (father, 1);    // edit.c:74
recombine (father);            // edit.c:75
```

`setwispupwards` cascades `setwispnd` calls upward to the root. At each level, `setwispnd` does a **full rescan of all surviving children** to find the new minimum — it does not cache or increment from the old minimum. If the deleted child held the minimum I-address, the next minimum among the survivors is found fresh.

There is one special case `setwispnd` handles correctly: if delete removes *all* children of a node, `findleftson(father)` returns `NULL`, and both `cdsp` and `cwid` are zeroed [`wisp.c:185–190`]:
```c
if ((ptr = findleftson (father)) == NULL) {
    clear (&father->cdsp, sizeof(father->cdsp));
    clear (&father->cwid, sizeof(father->cwid));
    ivemodified((typecorecrum*)father);
    return (TRUE);
}
```

---

### Summary

| Question | Answer | Key location |
|----------|--------|--------------|
| Does `setwispnd` track minimum I-address in root `cdsp`? | **Yes** — element-wise `lockmin` over all children, propagated bottom-up | `wisp.c:193–196` |
| Does the minimum go stale after DELETE removes the minimum-holding entry? | **No** — `setwispupwards` triggers a full rescan at every level post-delete | `edit.c:74` → `wisp.c:193–196` |

The system is correct for this case: `setwispnd` is not incremental. It always recomputes from the current child set, so no cached minimum survives a delete. The only way staleness could occur would be if `setwispupwards` were not called after a structural change — and the delete path calls it unconditionally at `edit.c:74`.

---

## Question 20 [gregory]

> When a document contains both text entries (subspace 1.x) and link entries (subspace 0.2.x) in the same POOM tree, are these stored as interleaved siblings in shared loafs sorted by V-displacement, or does the tree naturally partition them into separate subtrees due to the tumbler ordering of `0.2.x < 1.x`?

### Gregory's Answer

## KB Synthesis

The KB does not describe explicit partitioning logic, but the answer emerges from the tumbler total order combined with how the POOM B-tree is built and traversed.

## Natural partitioning via tumbler ordering

Internally, link entries occupy V-positions `2.1`, `2.2`, ... and text entries occupy V-positions `1.1`, `1.2`, .... Since `1.x < 2.x` under the tumbler total order [INV-TUMBLER-TOTAL-ORDER], text entries consistently have smaller displacements than link entries. The POOM 2D enfilade sorts children by displacement, so text and links occupy different regions of the V-space key range. As the tree grows and splits, text entries tend toward left subtrees and link entries toward right subtrees — not by design, but as an emergent consequence of ordering.

The POOM split policy reinforces this: `splitcrumpm` peels off the child with the largest SPANRANGE displacement [ST-SPLIT-2D], which for a mixed document would be a link entry (largest V-position). Over time this pushes links further right.

## Rebalancing can theoretically mix them in a node

The `recombinend` diagonal sort uses `cdsp.dsas[0] + cdsp.dsas[1]` (V + I displacement sum) [ST-REBALANCE-2D]. This means two upper nodes — one covering text-range children, one covering link-range children — could be merged if their diagonal sums happen to be close. The B-tree does not prevent a parent node from holding pointers to both text-range and link-range child subtrees. So while complete subtree isolation is likely in practice (given the systematic gap between 1.x and 2.x), it is not enforced.

## The two-blade knife requires range-efficient traversal

The strongest structural evidence is [FC-SUBSPACE] / [SS-TWO-BLADE-KNIFE]: INSERT at `1.x` constructs a knife with `blade[1] = 2.1`, and `insertcutsectionnd` classifies link entries at `2.x` as case 2 (no shift) because they fall at or beyond `blade[1]`. This only works efficiently if the B-tree can locate entries by V-range without scanning the whole tree — which requires that the displacement ordering puts text entries and link entries in reliably different subtrees, at least above the loaf level.

## Summary

Text (1.x) and link (2.x) entries share the same POOM tree and the same loaf allocation pool [SS-UNIFIED-STORAGE]. They are NOT in structurally separate enfilades. However, tumbler ordering guarantees they occupy different V-ranges, which causes the B-tree to naturally partition them into separate subtrees as it grows. A single upper node (loaf) could theoretically contain pointers to both ranges — the KB has no finding that rules this out — but complete V-range interleaving within a single bottom crum (loaf) is impossible because each bottom crum covers a contiguous V-address interval [SS-POOM-BOTTOM-CRUM], and no single interval spans both `1.x` and `2.x`.

---

## Code Exploration

Now I have sufficient source-level evidence to answer the question definitively. Let me compile the full answer from the actual code.

---

## Storage of Text vs. Link Entries in the Same POOM Tree

### Short Answer

They live in the **same single POOM enfilade**, sorted by V-coordinate. There is no structural enforcement of subspace separation. Tumbler ordering causes the partition to emerge naturally — text entries always sort before link reference entries — but whether they occupy **shared loafs or separate subtrees** depends on document size: small documents share leaf loafs; larger documents partition into separate subtrees after splits.

---

### The V-Address Assignment Scheme

**Text entries** — `doinsert` → `appendpm` → `findvsatoappend` [`orglinks.c:29-48`]:

```c
int findvsatoappend(typecorecrum *ptr, tumbler *vsaptr)
{
  tumbler linkspacevstart;
    tumblerclear (&linkspacevstart);
    tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart); // linkspacevstart = 2
    prologuend (ptr, &offset, &grasp, &reach);
    if (
       iszerolock (...)
    || (tumblercmp (&grasp.dsas[V], &linkspacevstart) != LESS)) {
        tumblerincrement (vsaptr, 0, 1, vsaptr);  // vsaptr = 1
        tumblerincrement (vsaptr, 1, 1, vsaptr);  // vsaptr = 1.1  ← first text position
    } else if (tumblercmp (&reach.dsas[V], &linkspacevstart) == LESS) {
        movetumbler (&reach.dsas[V], vsaptr);     // no links: next = end of text
    } else {
        findnextaddressinvspace (ptr, &grasp, &linkspacevstart, vsaptr);
        // links present: find last text address before boundary at 2
    }
```

The first text append in an empty document goes to V = **1.1** (`{exp=0, mantissa=[1,1]}`). Each subsequent append extends from there (width is computed with `shift = tumblerlength(vsaptr) - 1` in `insertpm` [`orglinks.c:115`], encoding the character count at the second story). Text entries therefore occupy V ∈ **[1.1, 2)**.

**Link reference entries** — `docreatelink` → `findnextlinkvsa` [`do2.c:151-167`]:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);  // firstlink = 2
    tumblerincrement (&firstlink, 1, 1, &firstlink);  // firstlink = 2.1
    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);  // first link → V = 2.1
    else
        movetumbler (&vspanreach, vsaptr); // subsequent links → append after previous
```

The first link reference placed in the document's POOM goes at V = **2.1** (`{exp=0, mantissa=[2,1]}`). Subsequent link references are placed at the current reach (end of the existing V-span), pushing each successive link reference further up into the **[2.1, ...)** range.

**The boundary is hard**: `findvsatoappend` sets `linkspacevstart = 2` and uses it as the cutoff. All V-addresses of text crums are strictly less than `2`; all V-addresses of link crums are `≥ 2.1`. The tumbler comparison `tumblercmp(&x, &y)` in `tumble.c:72-85` operates digit-by-digit, left-to-right, so `1.anything < 2 < 2.1`.

Note: the link's own POOM tree (its orgl) uses `setlinkvsas` [`do2.c:169-183`] to place **from-endpoint** data at V = 1.1 and **to-endpoint** data at V = 2.1 within the link object. This is a separate tree from the document's POOM.

---

### How the POOM Enfilade Actually Sorts Them

Both text crums and link-reference crums land in the **same POOM tree** via `insertnd` → `insertmorend` → `findsontoinsertundernd` [`insertnd.c:277-299`]:

```c
typecorecrum *findsontoinsertundernd(typecuc *father, typedsp *grasp,
                                     typewid *origin, typewid *width, INT index)
{
    tumbleradd (&origin->dsas[index], &width->dsas[index], &spanend);
    ptr = nearestonleft = findleftson (father);
    for (; ptr; ptr = findrightbro(ptr)) {
        tumbleradd(&grasp->dsas[index],&ptr->cdsp.dsas[index],&sonstart);
        if (
          tumblercmp (&sonstart, &origin->dsas[index]) != GREATER
        && tumblercmp (&ptr->cdsp.dsas[index], &nearestonleft->cdsp.dsas[index]) != LESS) {
            nearestonleft = ptr;
        }
        if (
          whereoncrum(ptr,grasp,&origin->dsas[index],index)>=ONMYLEFTBORDER
        && whereoncrum (ptr, grasp, &spanend, index) <= ONMYRIGHTBORDER)
            return (ptr);
    }
    return (nearestonleft);
}
```

When called with `index = V` (the V-dimension), this routes each insertion to the child whose V-interval contains the target address. There is **no check for subspace type** — it is purely a tumbler comparison. A text crum at 1.5 and a link crum at 2.1 are simply two points on the same number line, and the tree routes each to the correct position.

The leaf-level insertion, `insertcbcnd` [`insertnd.c:242-275`], first checks if the new crum is an extension of an existing one:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, ...);  // extend in place
        ...
    }
}
new = createcrum (0, (INT)father->cenftype);
adopt (new, SON, (typecorecrum*)father);              // or create sibling
```

If no extension is possible (different I-stream or non-contiguous), a new sibling crum is created. Text and link crums with different `homedoc` values will never satisfy `isanextensionnd` (line 305: `!tumblereq(&infoptr->homedoc, &ptr->c2dinfo.homedoc)` returns FALSE), so they always become distinct crums.

---

### Loaf Occupancy: Shared vs. Separate Subtrees

A loaf holds up to `MAX2DBCINLOAF` bottom crums (leaf level) or `MAXUCINLOAF` internal crums (checked via `toomanysons` in `genf.c:239-245`). There is no subspace filtering on loaf membership.

**Small document** (e.g., one text crum + one link crum): Both crums sit in the same leaf loaf under the root. They are siblings ordered by V-address, with the text crum on the left and the link crum on the right — interleaved in the same loaf.

**Larger document**: When `splitcrumupwards` fires (triggered from `insertcbcnd` line 272), the loaf splits at its midpoint. Because text crums cluster at V ∈ [1.1, 2) and link crums cluster at V ∈ [2.1, ...) with a genuine gap between them, any split that separates the two groups will produce:
- Left child: contains only text crums (V < 2)
- Right child: contains only link crums (V ≥ 2.1)

This partition then propagates upward through `setwispupwards` and `recombine` [`insertnd.c:76`, `genf.c` recombine]. Once split, subsequent insertions will route text to the left subtree and links to the right subtree — they never need to share a loaf again.

---

### The `istextcrum` / `islinkcrum` Classification

After retrieval, `maxtextwid` in `orglinks.c:224-245` needs to distinguish text from link crums within a POOM traversal. It uses these heuristics [`orglinks.c:246-261`]:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0  && is1story(&crumptr->cwid.dsas[V])){ 
        return TRUE;
    }
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){
        return TRUE;
    }
    return FALSE;
}
```

`istextcrum` checks that the crum's V-displacement has zero second digit and 1-story width — consistent with a single contiguous text run whose width encodes character count in `mantissa[0]`.

`islinkcrum` checks that the crum's V-displacement starts with `1` and has a non-zero second digit (`1.n` for n≠0). This identifies crums within the V-range `1.1–1.∞`, which in the link object's own POOM corresponds to from-endpoint data. Note this is operating on the relative **displacement** (`cdsp`), not the absolute V-address.

These are **detection heuristics**, not enforcement. The POOM tree itself imposes no type constraint.

---

### The `filter_vspanset_to_text_subspace` Guard

`do1.c:386-411` adds an explicit filter when computing version relations:

```c
typevspanset filter_vspanset_to_text_subspace(typetask *taskptr, typevspanset vspanset)
{
    tumblerclear(&text_subspace_start);
    tumblerincrement(&text_subspace_start, 0, 1, &text_subspace_start); // = 1
    for (; vspanset; vspanset = vspanset->next) {
        if (tumblercmp(&vspanset->stream, &text_subspace_start) >= EQUAL) {
            // keep: span is in text subspace (V >= 1)
        }
        // skip: link subspace (V < 1) — not applicable to doc POOM,
        //        but relevant for the link POOM's from-endpoint (V = 0.something)
    }
```

The boundary here is V ≥ 1 (not 2), which confirms that the overall V-space has:
- `V < 1`: some lower subspace (not directly used by either text or doc-level links)
- `V ∈ [1, 2)`: text subspace in the document POOM
- `V ≥ 2.1`: link-reference subspace in the document POOM

---

### Conclusion

**The POOM tree uses a single shared enfilade for both text and link entries.** There is no structural separation — no separate trees, no subspace-aware routing logic in the insertion path.

The **effective partition** arises from the V-address assignment scheme:
- `findvsatoappend` places text at V ∈ [1.1, 2)
- `findnextlinkvsa` places link references at V ≥ 2.1

Because tumbler ordering (`tumblercmp`) is total and consistent, text entries always sort strictly below link entries in the enfilade. In a **small document**, they coexist as siblings in the same leaf loaf — they are genuinely interleaved in a shared loaf, separated only by their V-address ordering. As the document grows and loafs split, they partition into **separate left and right subtrees**, but this is a side-effect of the B-tree mechanics, not an explicit architectural decision. The tree does not "know about" the subspace boundary — it only knows tumbler ordering.
