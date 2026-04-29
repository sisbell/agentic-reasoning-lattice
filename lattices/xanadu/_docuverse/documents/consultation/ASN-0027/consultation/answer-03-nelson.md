## Question 3 [nelson]

> If the same content appears in multiple documents through inclusion, must it be reachable through a single stable address regardless of how many documents reference it?

**Yes.** This is not merely a feature but a foundational architectural property. Content lives at exactly one permanent I-space address, and every inclusion references that same address.

## The Architecture

Xanadu separates content identity (I-space) from document arrangement (V-space). When content is created, it gets a permanent I-address. When another document includes that content, it creates a V-space mapping that points to the *same* I-address — it does not create a second copy.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The COPY operation (which implements transclusion) explicitly shares I-addresses with the source. It does not duplicate content into a new I-space location.

## Why This Must Be So

Three guarantees depend on it:

**1. Origin traceability.** The I-address encodes which document created the bytes. If inclusion created new addresses, origin would be lost.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

**2. Content discovery.** FINDDOCSCONTAINING works by searching for shared I-addresses:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

If each inclusion had its own address, this operation would be impossible — there would be no structural link between the "same" content in different documents.

**3. Automatic royalties.** The system pays the original author when their bytes are delivered. This requires knowing that bytes in document B are the *same bytes* as those in document A — which is determined by shared I-address, not by content comparison.

## The Fetching Mechanism Enforces It

When a front end requests content from a compound document, non-native bytes are "obtained by front-end or back-end requests to their home locations" [LM 4/11]. The content is fetched from its single permanent location. The connection cannot be severed because the retrieval mechanism *requires* the I-address to function.

Content identity in Xanadu is based on creation, not on value. Two documents with identical text created independently have *different* I-addresses. Transcluded content *shares* the same I-address. This distinction — same-content-by-reference vs. same-content-by-coincidence — is only possible because there is one stable address per piece of created content, regardless of how many documents include it.

## Summary

The single stable I-address is not just reachable — it is the *only* address for that content. Each including document has its own V-address for where that content appears in its arrangement, but the underlying identity is always the one permanent I-space address. Ten thousand documents can include the same paragraph; there is still exactly one I-address for it, and that address resolves to the same bytes forever.
