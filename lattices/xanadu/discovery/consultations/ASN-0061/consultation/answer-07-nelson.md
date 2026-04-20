## Question 7 [nelson]

> Does the document retain the same identity after a removal, or does removing content produce a distinct document with its own identity?

## The document retains its identity after removal.

DELETE is an in-place modification of the document's Vstream arrangement, not a creation of a new entity. The document's tumbler address, ownership, and history persist through the operation.

### Evidence from the FEBE operations

DELETEVSPAN operates *on* a document — it does not produce a new one:

> "This removes the given span from the given document." (4/66)

Contrast this with CREATENEWVERSION, which explicitly creates a *new* document with a *new* identity:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

DELETE has no "returns the id of the new document" — it modifies the existing one.

### The "ongoing braid" model

Nelson's document model is fundamentally one of identity-preserving evolution:

> "A document is really an evolving ONGOING BRAID." (2/14)

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." (2/15)

Editing — including removal — is re-twisting the braid, not cutting it and starting a new one. The document accumulates history; each state is recoverable:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)

### What DELETE actually affects

From the system state diagram on 4/9:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

And explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

DELETE removes bytes from the **Vstream** (current arrangement) but leaves **Istream** (permanent storage) untouched. The document's identity is rooted in its tumbler address, which is permanent. The Vstream is merely the document's current face — one cross-section of the evolving braid.

### Vstream changes don't alter document identity

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

Editorial operations — INSERT, DELETE, REARRANGE — alter V-addresses freely. The document absorbs these changes as part of its ongoing evolution. Links survive because they point to I-addresses, not V-addresses. The document's identity is the container for this evolution, not any particular arrangement within it.

### Summary

In Nelson's model, a document is not a snapshot but a *trajectory*. Removal changes the trajectory's current state without altering which trajectory it is. To get a distinct identity, you must explicitly invoke CREATENEWVERSION. All other editing operations — including DELETE — evolve the document in place.
