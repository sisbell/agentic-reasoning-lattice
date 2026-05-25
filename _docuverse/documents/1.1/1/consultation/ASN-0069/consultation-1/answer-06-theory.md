## Question 6 [theory]

> When `CREATENEWVERSION` is invoked on a source with no content, does the design intent require rejection, require producing an empty new version, or treat this case as outside the operation's specified domain?

Looking at the operation specification and the design principles around documents and versions.

**Direct answer:** Producing an empty new version. Nothing in my specification gates `CREATENEWVERSION` on the source having content.

**The operation specification (4/66):**

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry."

The semantics are: copy whatever contents exist (zero or more bytes) and establish ancestry. There is no precondition on content existence.

**Why empty is a valid result, not a degenerate case:**

Empty documents are first-class. `CREATENEWDOCUMENT` produces one by design (4/65):

> "This creates an empty document. It returns the id of the new document."

If empty documents are valid as freshly created entities, they are valid as versioned outputs.

**Why rejection contradicts the design:**

A document is "an evolving ONGOING BRAID" (2/14) — a trajectory through time, not a content threshold. Forking the braid at a point where it carries zero bytes is still a meaningful act: it establishes ancestry and creates a writable surface. Rejecting would also conflict with the principle that the version mechanism exists so that "users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals" (2/45). An empty source has nothing to damage and nothing to forbid copying.

**The two things `CREATENEWVERSION` must accomplish both work on empty input:**

1. Content copying — zero bytes copied is well-defined
2. Ancestry — "The new document's id will indicate its ancestry" (4/66) is a property of the address (a tumbler fork), not of the content. Forking happens in tumbler-space regardless of what is stored

**Caveat on scope:** My specification text in Literary Machines does not explicitly call out the empty-source edge case. The answer above is the natural reading of the operation's wording combined with the standing principles (empty documents are valid; non-destruction; ancestry as an address property). NEED_RAW: 4/65-4/66 if you want me to verify there is no qualifier in the surrounding paragraphs I haven't reproduced in the curated source.
