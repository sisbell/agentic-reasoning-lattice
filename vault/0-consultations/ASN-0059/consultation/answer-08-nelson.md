## Question 8 [nelson]

> Does the design distinguish between inserting content that is entirely new to the system versus inserting content that already exists elsewhere — and if so, must the operation produce different guarantees for each case?

## Yes — the distinction is fundamental, and the operations are explicitly separate

Xanadu's design draws a sharp line between inserting new content and incorporating existing content. These are **different FEBE operations** with **different Istream consequences** and **different guarantees**.

### The Two Operations

**INSERT** (and APPEND) — for content new to the system:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

**COPY** — for content that already exists elsewhere:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

Note the parameter difference: INSERT takes a `<text set>` (raw content). COPY takes a `<spec set>` (addresses of existing content).

### Different Istream Guarantees

The consequences for Istream are opposite:

| Guarantee | INSERT | COPY |
|-----------|--------|------|
| **New I-addresses created?** | Yes — fresh, unique | No — references existing ones |
| **Home document** | The inserting document | The *original* document |
| **Native bytes?** | Yes — "native bytes of a document are those actually stored under its control" [LM 4/11] | No — "Non-native byte-spans are called inclusions or virtual copies" [LM 4/11] |
| **Attribution** | You are the originator | Original author retains attribution |
| **Royalties** | Accrue to you | Accrue to original owner |

Nelson is explicit about the native/non-native distinction:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

### Identity Is Based on Creation, Not Value

This is the deepest consequence. Two INSERTs of identical text produce **different I-addresses**. A COPY of existing text produces a reference to the **same I-addresses**. The system distinguishes "wrote the same words independently" from "quoted from the original."

This matters for:

- **FINDDOCSCONTAINING** — finds all documents containing content from the same Istream origin. Independent INSERTs of identical text are invisible to each other. COPYs (transclusions) are all discoverable.

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

- **Correspondence** — shared Istream origin is the structural basis for version comparison. COPY preserves correspondence; INSERT creates content with no correspondence to anything.

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

- **Origin traceability** — I-addresses encode the home document. INSERT makes you the home. COPY preserves the original home.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

### The Vstream Is Identical

From the user's perspective, both operations produce the same Vstream effect: content appears at the specified position. The document reads the same either way. But the *structural* properties — attribution, royalties, discoverability, correspondence — differ completely based on which operation was used.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The front end doesn't need to care about the distinction at display time. But the back end must maintain it permanently.

### CREATENEWVERSION as the Extreme Case

The version operation is essentially a whole-document COPY:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The new version shares all I-addresses with the source. No new Istream content is created. This is what enables version comparison — the shared I-addresses ARE the correspondence.

### The Compound Document Model

Nelson's compound document model depends entirely on this distinction:

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

A compound document is a mix of INSERTed content (the author's new words) and COPYed content (transclusions from other documents). The system must distinguish these permanently because:

1. The original owners get royalties for their COPYed portions
2. The compound document owner gets royalties for INSERTed portions
3. Attribution for each byte traces to its actual originator

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

### Summary

The design does not merely distinguish these cases — the distinction is **architecturally load-bearing**. INSERT creates new Istream content with the inserting document as home. COPY creates Vstream mappings to existing Istream content with the original document remaining as home. Every downstream guarantee — attribution, royalties, discoverability, correspondence, version comparison — depends on which operation was used. The Vstream presentation is identical; the Istream identity is fundamentally different.
