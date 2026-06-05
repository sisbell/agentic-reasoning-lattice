## Question 2 [theory]

> What does each member of the returned span-set describe about its corresponding part of the document?

The question concerns the **RETRIEVEDOCVSPANSET** operation, whose return value is a span-set with two members.

## Answer

Each member of the returned span-set describes a **count of one kind of content** in the document:

- One member indicates the **number of characters of text**
- The other member indicates the **number of links**

From Nelson's specification of the operation:

> "This returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." (4/68)

So the two members partition the document's contents by subspace: the text/byte subspace and the link subspace. This mirrors the document-local address structure, where bytes and links occupy distinct subspaces (bytes at `version.position`, links at `version.0.2.N`). The span-set's members each report the extent of one of those subspaces — how much text the document holds and how many links it is home to.

This contrasts with the related **RETRIEVEDOCVSPAN** (singular), which returns a single span describing "the origin and extent of the V-stream of document `<doc id>`" (4/68) — i.e., where the document's virtual byte stream begins and how far it runs, rather than the two-part text/link counts.
