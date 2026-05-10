## Question 4 [nelson]

> Must the address of shared content remain identical across every document that includes it, or may each document assign its own address to the same content?

## The I-address is identical; the V-address differs

Xanadu's two-address architecture answers this question directly. Shared content has **one permanent identity** (I-space) but **many positions** (V-space, one per including document).

### I-Space: Identity is universal and immutable

When document B transcludes content from document A, B's virtual byte stream references the **same I-space addresses** as A. The content is not copied — it is included by reference to its permanent home location.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The I-address encodes the originating server, user, document, and element position. It is permanent and never changes. Content identity is based on creation, not on value — two documents with identical text created independently have **different** I-addresses, while transcluded content **shares** the same I-address.

### V-Space: Position is per-document and ephemeral

Each document assigns its own V-space addresses to the same content. If document A has "hello" at V-positions 1–5 and document B transcludes that same "hello" at V-positions 47–51, the V-addresses differ but the I-addresses are identical.

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses shift with every insertion, deletion, and rearrangement. They are dense (no gaps), sequential, and local to the document's current version. The document **is** its V→I mapping.

### Why shared I-addresses are essential

Three system capabilities depend on I-address identity being preserved across all including documents:

**1. FINDDOCSCONTAINING** — finds all documents that include specified content by searching shared I-addresses:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

If each document assigned its own identity to shared content, this operation would be impossible.

**2. Correspondence** — the ability to compare versions and find matching parts depends on shared I-space origin:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

**3. Origin traceability** — attribution is structural because the I-address encodes who created the content:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

### The COPY operation makes this explicit

The FEBE COPY command is the transclusion primitive. It places content into a new document at a specified V-position while preserving I-address identity:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This creates a new V-space mapping (the `<doc vsa>` is a V-address in the target document) pointing to existing I-space content. No new I-addresses are created.

### Summary

| Address type | Shared across documents? | Purpose |
|---|---|---|
| **I-address** | **Yes — must be identical** | Permanent identity, attribution, origin tracing |
| **V-address** | **No — each document assigns its own** | Current position in this document's arrangement |

The entire architecture rests on this separation. I-space permanence enables permanent citation, link survivability, automatic attribution, and royalty tracking. V-space flexibility enables editing, versioning, and per-document arrangement. The document is the mapping between the two.
