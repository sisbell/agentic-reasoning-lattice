## Question 1 [theory]

> When a document is named by its identity alone, what must the system guarantee it returns about the size of each distinct kind of content it holds?

## Answer

When a document is named by its identity alone (its `doc id`), the system must guarantee, through the **RETRIEVEDOCVSPANSET** operation, that it returns the size of **each of the two distinct kinds of content** a Xanadu document holds: its **text (characters/bytes)** and its **links**.

From the FEBE operation set:

> **RETRIEVEDOCVSPANSET**: "This returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." (4/68)

This is distinct from the related operation that returns only the document's overall extent:

> **RETRIEVEDOCVSPAN**: "This returns a span determining the origin and extent of the V-stream of document `<doc id>`." (4/68)

### Why two distinct kinds

A Xanadu document is not a single undifferentiated blob — its contents divide into two element types occupying separate subspaces in the document-local address space:

| Subspace | Address pattern | Contents |
|----------|-----------------|----------|
| Bytes | `version.position` (0.1.x) | Text content |
| Links | `version.0.2.N` | Links the document is home to |

Because text bytes and links live in separate subspaces, a single count cannot describe the document. The span-set returned by RETRIEVEDOCVSPANSET therefore reports **both** sizes — character count and link count — so that a front end knows the magnitude of each kind of content before retrieving it.

This reflects the foundational principle that "there is essentially nothing in the Xanadu system except documents and their arbitrary links" (4/41) — so the size of a document is fully characterized by exactly these two quantities.

(Note: the count of links is specifically the links *of which the document is home* — "A document includes only the links of which it is the home document" (4/31) — not in-links pointing to it from elsewhere.)
