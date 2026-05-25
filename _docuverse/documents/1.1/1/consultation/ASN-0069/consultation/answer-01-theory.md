## Question 1 [theory]

> When a document is forked, what content must be considered shared between the source and the new version rather than duplicated?

When a document is forked via CREATENEWVERSION, **the Istream content (all actual bytes) is shared**, not duplicated. The new version is a fresh Vstream arrangement that references the same permanent Istream addresses as the source.

Nelson's specification of CREATENEWVERSION confirms this:

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

The mechanism is structural. Content lives permanently at its Istream address; documents are arrangements over Istream:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

This sharing is what enables correspondence — the system can identify which parts of two versions are equivalent precisely because they share Istream addresses. And it's why deletion in one version doesn't destroy content:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

The principle is general: forking is transclusion of an entire document. As Nelson puts it for the broader publishing model:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." (2/45)

So what is shared:
- **All bytes** (Istream content) at their permanent I-addresses
- **Permanent identity** of each byte (its home document of origin, encoded in the I-address)
- **Link survivability** — links to the source's content still resolve in the new version because they point to Istream

What is NOT shared (independent per version):
- The Vstream arrangement (which can diverge through edits)
- The version's own tumbler address (the new version gets a daughter document address indicating ancestry)
- Future edits made to either version
