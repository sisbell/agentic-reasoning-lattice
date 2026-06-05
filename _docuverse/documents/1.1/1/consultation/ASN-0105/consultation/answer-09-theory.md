## Question 9 [theory]

> What must the result preserve about the boundaries between distinct pieces of content within the span, or must the span appear as a single undifferentiated whole?

## Answer

The result must **preserve the boundaries** between distinct pieces of content. A span in Xanadu is never an undifferentiated whole — it carries internal structure at multiple levels.

### A span is a subtree, not a flat range

At the tumbler level, a span is explicitly a structured object — a depth-first spanning tree of the docuverse hanging from the tumbler line, not a linear count of bytes:

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." (4/25)

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

The contents are *implicit in the boundaries* — but that implicitness is precisely the tree structure between the endpoints, which preserves the distinct elements within:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

So a span can span "characters, links, documents, versions, and... large combinations of them--including spans of servers with all their contents" (4/24) — and the distinctions among those nested elements are retained, not flattened.

### Every byte retains its home document

Even when content is assembled or retrieved, each piece keeps its origin. Boundaries between content drawn from different sources are always recoverable because attribution is structural (encoded in the I-address), not metadata laid over an undifferentiated blob:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

Non-native (transcluded) bytes "have an ordinal position in the byte stream just as if they were native to the document" (4/11) — they sit in sequence, yet remain distinguishable by their home location.

### Non-contiguous boundaries use span-sets

When the distinct pieces are *not* adjacent, the boundary between them is preserved by representing the selection as a span-set — a series of spans — rather than collapsing them into one range:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

This is the same reason link endsets are span-sets: "one end of a link may be on a broken, discontiguous set of bytes" (4/42), and those breaks are part of the structure, not erased.

### Where boundaries are returned explicitly

Operations that compare or discover content return the boundaries as first-class results rather than a merged whole:

- **SHOWRELATIONOF2VERSIONS** returns "a list of ordered pairs of the spans of the two spec-sets that correspond" (4/70) — distinct corresponding spans, preserved as pairs.
- **FINDDOCSCONTAINING** returns "a list of all documents containing any of the material" — the per-document boundaries are reported, not dissolved.

## Summary

A span never appears as a single undifferentiated whole. Internally it is a depth-first spanning tree that preserves the distinct elements (servers, documents, versions, characters, links) between its endpoints; every byte retains its home-document identity via its I-address; and discontiguous pieces are kept separate through span-sets. The boundaries between distinct pieces of content are always preserved and recoverable.
