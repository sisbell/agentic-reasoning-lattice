## Question 8 [theory]

> Must the reported extent account for all content the document has ever held, or only the content presently belonging to it?

## Answer: Only the content presently belonging to the document

The reported extent describes the document's **V-stream** — its *current* arrangement — not the totality of everything it has ever held. Content that has been deleted is no longer part of the V-stream and therefore falls outside the reported extent, even though it persists permanently in the I-stream.

### The operation reports V-stream extent

The relevant FEBE operations are explicit that they measure the V-stream:

- **RETRIEVEDOCVSPAN**: "This returns a span determining the origin and extent of the V-stream of document `<doc id>`." (4/68)
- **RETRIEVEDOCVSPANSET**: "This returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." (4/68)

Both report on the V-stream — the document as currently arranged — not on its accumulated history.

### Deletion removes content from the V-stream, not the I-stream

This is the decisive point. DELETE is a V-stream operation. Deleted bytes leave the current arrangement but remain in permanent storage. Nelson's own diagram annotation marks deleted bytes as a distinct state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

The phrase **"not currently addressable"** is what settles the question. Deleted content is not part of the document's present addressable V-stream, so it does not contribute to the reported extent. Yet it is not destroyed:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

### Why this is the correct semantics

The V-stream is, by definition, the present view over permanent I-stream content. Each version defines its own V-stream arrangement:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

So the extent of "the document" depends on *which version* you ask about. The current version's extent reflects only what currently belongs to it. The full history is not lost — it remains reachable through historical backtrack and through prior versions — but a request for the document's extent reports the present V-stream, not the cumulative all-time content.

### Summary

| What you ask about | What the extent reflects |
|---|---|
| Current V-stream (RETRIEVEDOCVSPAN) | Only content presently belonging to the document |
| Deleted content | Excluded — "not currently addressable" (4/9) |
| Historical states | Available separately via backtrack / prior versions, not folded into current extent |

The reported extent accounts for **only the content presently belonging to the document**, not everything it has ever held.
