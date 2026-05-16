## Question 6 [nelson]

> Must every link belong to a document, or can links exist as independent first-class objects outside the document model?

## Every Link Must Belong to a Document

Nelson is unambiguous: **links cannot exist outside the document model.** They are always housed in a home document that determines their ownership and address.

### The No-Free-Floating Rule

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist. Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." [LM 2/29]

That last clause is the key. Even a collection of links whose sole purpose is to connect *other* documents is itself "a separate document." The document is the universal container. There is no alternative.

This is reinforced at the system level:

> "The Xanadu document is the unit of the system. There is almost nothing in the Xanadu system but Xanadu documents." [LM 4/6]

### Home Document = Ownership, Not Target

While every link must live in a document, the relationship is purely administrative—about *who owns* the link, not *what it connects*:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

This is a subtle but critical point. A link connecting passages in documents X and Y might live in document Z, which has nothing to do with either X or Y. The home document is the ownership address, not a topical container.

### Address Structure Confirms This

Links occupy the **2.x subspace** within their home document's tumbler address:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" [LM 4/31]

A link's tumbler address *contains* a document field. There is no address form for a link that lacks a document component. The addressing system itself makes document-less links structurally impossible.

### Why This Matters

The design serves three purposes:

1. **Ownership is always determinable.** Every link has an owner because every link has a home document, and every document has an owner. There is no orphan link problem.

2. **Links are first-class but not free-standing.** Links have their own addresses in tumbler-space, can be targets of other links, and persist independently of the documents they connect—but they still need a home for ownership and addressing purposes.

3. **Link-only documents are a feature, not a workaround.** Nelson explicitly envisions documents whose entire content is links. A scholar's annotations on someone else's work, a curated set of connections across a corpus—these are documents in their own right, owned by the annotator.

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

### Summary

Links are first-class citizens with their own permanent addresses, their own survival guarantees, and the ability to be targets of other links. But they are not *independent* objects. Every link lives in a home document that gives it an address and an owner. A "bag of links" is simply a document whose content happens to be entirely links. Nelson's architecture has no concept of a free-floating link—and by design, no mechanism to create one.
