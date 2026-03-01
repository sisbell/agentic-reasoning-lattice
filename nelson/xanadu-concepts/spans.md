# Spans

Source: Literary Machines, 2/26-2/28, 4/24-4/25, 4/32-4/39, 4/42

## Semantic Intent

### What It Means

A span is a contiguous region of content within the Xanadu address space. Rather than pointing to a single location, a span designates everything between two addresses - a "from here to there" selection. This is the fundamental unit for referring to content: you don't point at bytes, you indicate ranges.

Spans are how users and systems talk about "this paragraph" or "those three chapters" or "the entire docuverse." The addressing system is designed so that a single span can naturally express selections at any scale - from one character to an entire document to all documents on a server.

### User Guarantee

**Any contiguous selection can be expressed as a single span.** Users can refer to content of any size using the same mechanism. There's no special syntax for "one byte" vs "one document" vs "everything" - it's all spans, just with different boundaries.

**Spans survive editing.** When you designate a span of content, that designation follows the content even as the document is edited. If the content splits, the span may become discontiguous, but it still refers to the same bytes.

### Principle Served

**Uniform reference at all scales.** Nelson designed the tumbler system specifically so that spans work naturally from the smallest to largest units. A "1" in the right position means "all of this level" - all versions, all documents, the entire docuverse. This eliminates the need for different reference mechanisms at different scales.

**Content-focused, not position-focused.** Spans attach to content, not to positions in a document. This is crucial for a system where content can be rearranged, versioned, and transcluded. The span says "this content" not "position 47 to position 52."

### How Users Experience It

- Select any amount of text - that selection is a span
- The same span works whether the content is in its original document or transcluded elsewhere
- A link to "these three paragraphs" stays attached to those paragraphs even if the document is edited
- Request "everything by this author" with a single span
- Request "all documents on this server" with a single span
- The span concept scales from one byte to the entire docuverse

### Request Sets

A request set (or "spanset") is a collection of spans presented to the back end. This is how users express complex selections - not through complicated query languages, but through sets of simple "from-to" ranges. Any set of tumbler addresses can be covered exactly by a series of spans.

### The 1-Positions

Nelson's "1-positions" are a key design insight: a digit of "one" with leading zeroes designates "all of" a given level:

- `0.0.0.1` - the entire docuverse
- `1.2.0.0.1` - all documents on server 1.2
- `1.2.3.4.0.1` - all versions of document 1.2.3.4
- `1.2.3.4.5.0.1` - all elements in version 5 of that document

This means spans can naturally express hierarchical selections without special syntax.

### Spans as Subtrees

At the tumbler level, a span is more than a linear range - it represents a subtree of the docuverse. Nelson describes this as "a zone hanging down from the tumbler line" - a depth-first spanning tree rooted at the first address.

The crucial insight: **the content of a span is implicit in its boundaries**. When you specify a start and end tumbler, everything in between is determined by the tree structure of addresses. You don't enumerate what's inside; the addressing system defines it.

This means a span is not a count of items. It doesn't say "these 47 bytes" - it says "from this address to that address." The span might contain millions of documents, or nothing at all. A span that contains nothing today may contain a million documents tomorrow.

### Span-Sets

For non-contiguous selections (items exactly but nothing else), you use a span-set - a series of spans. This is how you say "these three paragraphs" when they're not adjacent. Each span in the set is a simple from-to range; together they cover exactly what you want.

### Two Representations

A tumbler-span can be specified in two equivalent ways:
1. **Pair of tumblers** - start address and end address
2. **Address + difference tumbler** - start address plus a "width" tumbler

Tumbler arithmetic converts between these forms. The difference representation is more compact when the span is small relative to the addresses.

### Arithmetic Limitations

Nelson notes a limitation: from a given tumbler address, you can only arithmetically reach places "notationally after" that address. You can't reach arbitrary points through tumbler arithmetic alone. This affects how spans can be computed and manipulated.

### Nelson's Words

> "A request set is a set of spans, or spanset, presented to the back end in the FEBE protocol... The manipulation of request sets is an important aspect of what front-end functions do."
> (4/37)

> "Understanding spans is a key to appropriate software design for handling request-sets."
> (4/37)

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse."
> (4/38)

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them."
> (4/42)

> "Essentially, the link seizes a point or span (or any other structure) in the Prismatic Document and holds to it."
> (2/26)

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse, (or merely to a series of elements of the same type, which is a degenerate case of a subtree). Thus we may have spans of characters, spans of links, spans of documents, spans of versions, and spans covering large combinations of them--including spans of servers with all their contents."
> (4/24)

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network."
> (4/24)

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything."
> (4/24)

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree."
> (4/25)

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point."
> (4/25)

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans."
> (4/25)

> "A span that contains nothing today may at a later time contain a million documents."
> (4/25)

> "Starting from a given tumbler address, it may only be possible arithmetically to get to some places in the Docuverse--those notationally after that address."
> (4/25)

---

## Related Concepts

| Concept | Relationship |
|---------|--------------|
| [tumblers](tumblers.md) | Spans are defined by tumbler boundaries |
| [endsets](endsets.md) | Link endsets are span-sets |
| [links](links.md) | Links connect spans, not points - enables survivability |
| [i-space-v-space](i-space-v-space.md) | Can specify spans in either address space |
| [docuverse](docuverse.md) | Spans can range from one byte to entire docuverse |

## FEBE Operations

Spans are the currency of FEBE - nearly every operation uses them:

| Operation | How spans apply |
|-----------|----------------|
| **DELETE** | Target is a span |
| **COPY** | Source is a spec-set (spans) |
| **REARRANGE** | Cut points define spans to transpose |
| **MAKELINK** | Three endsets are span-sets |
| **FINDLINKSFROMTOTHREE** | Search criteria are span-sets |
| **RETRIEVEV** | Request is a spec-set |
| **SHOWRELATIONOF2VERSIONS** | Returns corresponding span pairs |
| **FINDDOCSCONTAINING** | Search target is a vspec-set |

See [Concept-Operation Map](../concept-operation-map.md) for full mapping.