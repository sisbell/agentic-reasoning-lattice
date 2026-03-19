## Question 5 [nelson]

> Does a link have its own unique, permanent identity within the system, distinct from the identities of the content it connects?

## Yes — Links Are First-Class Addressable Objects

A link has its own unique, permanent tumbler address in the docuverse, completely distinct from the addresses of the content its endsets connect. This is not an incidental property but a foundational architectural decision.

### The Link's Own Address

Links occupy the **2.x subspace** within their home document and are addressed by permanent creation order:

```
N.0.U.0.D.V.0.2.1      → first link created in this document
N.0.U.0.D.V.0.2.755    → 755th link created in this document
```

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

This address is permanent. Deleting link 2.5 does not renumber 2.6 through 2.N.

### Links Are Stored Entities, Not Metadata

Of everything in the docuverse, only two kinds of entities are actually stored in tumbler-space — and links are one of them:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

Servers, accounts, and documents are "ghost elements" — conceptual positions with no stored representation. Links, by contrast, are concrete objects with real storage.

### The Link's Identity Is Separate from What It Connects

The Tumbler Square visualization [LM 4/46-4/47] makes the separation explicit. A link sits at its **home** position on the tumbler line, and its three endsets (from-set, to-set, type) **reach out** to other positions:

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." [LM 4/46]

The link's address encodes **where it lives and who owns it**. The endsets encode **what it connects**. These are independent.

### Why This Matters: Links Can Be Linked To

Because links have their own addresses, other links can point at them — no special mechanism required:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." [LM 4/49]

> "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only." [LM 4/49]

If links did not have their own distinct addresses, link-to-link would be impossible.

### Why This Matters: Ownership

The link's home address determines its owner — not what it points to:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

This separation of identity from reference is what makes it possible for you to annotate someone else's document without modifying it. Your link lives at your address, under your control, even though its endsets reach into their content.

### Summary

A Xanadu link is a **connective unit** [LM 4/41] with:
- Its own permanent tumbler address (identity)
- Its own home document (determines ownership)
- Three endsets that reach into the docuverse (what it connects)

The link's identity, the content it connects, and the content at its type address are three fully independent things unified by one object.
