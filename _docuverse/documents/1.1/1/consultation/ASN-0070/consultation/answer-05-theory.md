## Question 5 [theory]

> What guarantees must hold about the ordering of resolved endset positions relative to the order of content as it appears to the user?

I'll examine the curated sources for what they say about endset ordering, then check relevant raw pages where needed.

Looking at what the curated sources explicitly state:

**What endsets ARE (from 4/42-4/47):**
- "the from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans" (4/43)
- "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" (4/45, diagram caption)
- "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46)

**The tumbler line as canonical ordering (from spans/tumblers):**
- "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." (4/25)
- "if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)
- "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

Let me check the raw pages on endsets and link search for any explicit ordering guarantees.

Reading page 4/45 (raw 212) on endsets and the tumbler line:

NEED_RAW: 4/45-4/47 (raw 212-214), 4/58-4/60 (raw 225-227)

Based on what IS in the curated sources, here is my analysis:

## What Nelson explicitly establishes

1. **Endsets are sets, but represented as ordered span-sets.** Nelson calls them "an arbitrary collection of spans" (4/43) and "a series of spans" (4/25). "Series" implies sequence.

2. **The tumbler line is a canonical linear ordering.** All addresses — Istream and Vstream — map to positions on a single linear tumbler line. Endsets "map to" this line (4/46).

3. **Within a document, Vstream order IS the user-facing reading order.** "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

4. **The Vstream may be rearranged independently of Istream.** "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing." (4/11)

## What Nelson does NOT explicitly guarantee

The curated sources do not state an explicit invariant that resolved endset positions must be returned/presented in any particular order relative to the user's reading order. The closest the FEBE protocol comes is operations like SHOWRELATIONOF2VERSIONS which "returns a list of **ordered pairs** of the spans" (4/70) — but the ordering basis isn't specified there either.

## What can be inferred from principles

Two natural ordering schemes are available, and they diverge:

**Tumbler order (canonical, address-based):**
- Available everywhere because the tumbler line is universal
- Stable across edits (for Istream spans)
- Does NOT correspond to user reading order across documents
- Does NOT correspond to user reading order even within a document if endset references the Istream (which can be in any creation order, not arrangement order)

**Vstream order (user-facing, arrangement-based):**
- Matches what the user sees when reading
- Well-defined within a single document
- Across documents, requires a meta-ordering Nelson does not specify
- Changes with editing

## The likely intent (flagged as inference)

From Nelson's user-facing principles — "You always know where you are" (2/40), the user works with documents not storage internals (4/11), the front end handles presentation — the user-experiential commitment suggests that when an endset resolves to positions in a document the user is currently viewing, those positions should appear in the order they appear in that document's Vstream. This is the "true shape of information" the user sees.

But Nelson does not codify this as an invariant in the curated material. Pages 4/45-4/47 and 4/58-4/60 may contain more detail — they cover endset mapping to tumbler-space and link search semantics, which are the most likely places for explicit ordering guarantees. NEED_RAW for those pages to verify.
