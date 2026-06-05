## Question 7 [theory]

> Once creation completes, what must remain permanently true about the document's identity for as long as the system endures?

## The Permanent Address Is the Permanent Identity

Once a document is created, the one thing that must remain permanently true is that its **tumbler address remains valid, unique, and unchanged for as long as the system endures**. The address assigned at creation (its "baptism") is the document's identity, and that identity can never be altered, reused, or invalidated.

### The Core Guarantee

Nelson states this directly:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

The critical property is that growth of the docuverse never disturbs existing identities:

> "Tumbler addressing is concerned with the management of storage--the spontaneous creation of places to put things, and remembrance of where they are." (4/16)

And from the forking model, the relationship of an address to its parent is fixed at creation and never reorganized:

> "Every piece of content, no matter how small, has its place in the universal tree... No reorganization ever happens - once an address is forked, its relationship to its parent is permanent." (forking concept, summarizing 4/18-4/21)

### Why Identity Must Be Immutable

The address is not merely a label that *points* to the document — it structurally encodes the document's identity and provenance. An Istream address has the form `Node.0.User.0.Document.0.Element`, where the Document field permanently records the entity that created the content:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." (4/26)

This is why attribution and origin are guaranteed: identity is structural, not metadata that could drift:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

### What Stays Fixed vs. What May Change

A crucial distinction: the document's *identity* (its I-address) is permanent, even though its *arrangement* (Vstream) and physical storage location may change continuously:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

So the document may be edited, versioned, rearranged, moved between servers, even have its content "deleted" from the current view — but the permanent tumbler address that names it must remain valid and resolve to that same identity forever.

### The Obligation This Creates

This permanence is not just a technical fact but a binding guarantee, because others come to depend on the identity:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." (2/43)

Note one boundary Nelson explicitly draws: **time is not part of the identity**. The address says *where* in the docuverse, never *when*:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

### Summary

For as long as the system endures, the document's tumbler address — assigned at creation and never reused or revoked — must continue to uniquely identify that document and resolve to it. Content, arrangement, versions, and storage location may all evolve, but the permanent address that *is* the document's identity must remain invariant. This is the foundation on which every other guarantee (permanent links, citations, transclusion, attribution, and version history) depends.
