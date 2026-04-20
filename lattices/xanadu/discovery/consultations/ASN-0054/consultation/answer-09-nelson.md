## Question 9 [nelson]

> Is an empty document — one with no content at all — represented by an arrangement with zero pieces, or must every document always contain at least one piece?

## An Empty Document Has Zero Pieces

An empty document is represented by an arrangement with zero pieces. Nelson explicitly designed the system to accommodate this.

### Direct Evidence

**CREATENEWDOCUMENT creates an empty document:**

> "This creates an empty document. It returns the id of the new document." (4/65)

The operation returns an address — a position on the tumbler line — but stores nothing underneath it. No content bytes, no links.

**Ghost elements establish that addressable emptiness is valid:**

> "While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." (4/23)

> "These elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

An empty document is precisely a ghost element that has been "baptized" — it has a permanent address but no stored contents yet.

**Spans can contain nothing:**

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

If a span over a document's address range can contain nothing, the document's V-stream can be empty.

### Structural Reasoning

The V-stream is a mapping from sequential positions to I-space content. An empty document has an empty mapping — zero entries. RETRIEVEDOCVSPANSET (4/68) would return zero characters and zero links. There is no "minimum occupancy" requirement anywhere in Literary Machines.

The document's identity is its *address*, not its content. The address exists from the moment of creation; content arrives later through INSERT or APPEND. Nelson's append-only model makes this natural: a document begins empty and accumulates content over time.

> "A document is really an evolving ONGOING BRAID." (2/14)

A braid with zero strands is still a braid — it simply hasn't begun to accumulate yet.
