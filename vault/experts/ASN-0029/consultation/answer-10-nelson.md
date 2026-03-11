## Question 10 [nelson]

> What is the smallest thing that qualifies as a document — can a document be empty at creation, or must it contain at least some content?

## A Document Can Be Empty at Creation

The answer is explicit in the FEBE protocol. The `CREATENEWDOCUMENT` operation is defined as:

> "This creates an empty document. It returns the id of the new document." [LM 4/65]

A document can be created with zero bytes and zero links. The system assigns it a permanent tumbler address and returns that address. The document exists from that moment — empty but real.

## Why This Makes Architectural Sense

Three points from the design reinforce this:

**1. Documents are positions, not objects.** The ghost elements discussion makes clear that a document is a location in tumbler-space, not a stored thing:

> "While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." [LM 4/23]

An empty document is a valid position with nothing yet stored beneath it.

**2. Documents can contain only links.** Nelson explicitly says a document of nothing but links is valid:

> "Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." [LM 2/29]

If a document can be pure links with no text, emptiness is just the degenerate case.

**3. Documents are containers, not contents.** The document is the owned unit — an address under which content accumulates over time:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

A braid with zero strands is still a braid. You create the document first, then populate it with `INSERT` or `APPEND` operations.

## The Lifecycle

The intended workflow is clear from the protocol: `CREATENEWDOCUMENT` creates the empty container and returns its ID, then `INSERT` or `APPEND` adds content to it. Creation and population are separate operations — the document exists before it has content.
