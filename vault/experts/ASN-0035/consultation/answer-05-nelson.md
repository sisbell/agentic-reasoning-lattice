## Question 5 [nelson]

> Does the design distinguish different kinds of nodes (content-bearing, linking, versioning), or is there a single universal node type?

## Single Universal Node Type: The Document

Xanadu does **not** distinguish different kinds of nodes. There is one universal container — the **document** — and exactly two stored primitives within it: **bytes** and **links**.

### The Document Is Everything

Nelson is explicit that the document is the sole organizational unit:

> "The Xanadu document is the unit of the system. There is almost nothing in the Xanadu system but Xanadu documents." [LM 4/6]

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist. Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." [LM 2/29]

A document that contains only links is just as valid as one containing only text. A document of annotations pointing into someone else's work is simply a document whose content happens to be links. There is no "link node" or "annotation node" — there are only documents.

### Two Stored Primitives, Not Two Node Types

At the storage level, exactly two kinds of entities exist:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

These are distinguished by their address subspace within a document — bytes occupy the `0.1.x` subspace and links occupy the `0.2.x` subspace — but both live inside the same universal document container.

### Versioning Is Not a Separate Node Type

Versions are documents. A version's tumbler address indicates ancestry through the document field's subdivision, but Nelson is careful to note this is structural, not categorical:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

Versions are not a special node type. They are documents whose address happens to be "under" another document's address.

### Ghost Elements: Addresses Without Nodes

Servers, accounts, and documents themselves are not even stored objects — they are positions on the tumbler line with no corresponding storage:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

This reinforces the uniformity. The only things that actually exist in storage are bytes and links. Everything else — servers, accounts, documents, versions — is an addressing convention, not a node type.

### Links Are Owned by Documents, Not Separate

A crucial design point: links don't float independently. They live in a "home document" that determines ownership:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

Your annotations on someone else's work are links in **your** document pointing at **their** content. The link's home determines ownership; its endsets determine what it connects. But it is not a separate node — it is an element within a document.

### Summary

The architecture is radically uniform:

| Level | What exists |
|-------|------------|
| **Stored primitives** | Bytes and links (the only things actually in storage) |
| **Container** | Document (the universal, single node type) |
| **Address positions** | Servers, accounts, versions (ghost elements — no storage representation) |

Nelson captures this uniformity in one sentence:

> "So the docuverse is all really one big forking document." [LM 4/18]

And the link mechanism confirms there are only two things:

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." [LM 4/41]
