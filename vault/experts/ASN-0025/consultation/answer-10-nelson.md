## Question 10 [nelson]

> When content is copied rather than shared, must the copy receive a new and distinct address, or may the system treat the copy as the same content at the same address?

## Copy IS Transclusion: Same I-Address, New V-Address

In Xanadu, the COPY operation does **not** create new content. It creates a new V-space mapping that points to the **same** I-space address as the original. The "copy" and the original are the same bytes — viewed from different documents.

### The COPY Operation

The FEBE COPY command is defined as:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This creates what Nelson calls an **inclusion** or **virtual copy** — the copied bytes appear in the target document's V-stream but remain at their original I-space address:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The "copied" bytes are fetched from their **home location** — the original document. They are not duplicated in storage.

### Why This Matters: Content Identity Is Based on Creation

Content identity in Xanadu is determined by where content was **created**, not by its value. Two documents with identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address.

This is the foundation for several guarantees:

1. **Attribution**: You can always trace content back to its origin because the I-address encodes the home document.

2. **Discovery**: FINDDOCSCONTAINING works because copies share I-addresses — "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

3. **Royalties**: The system knows whom to pay because shared I-addresses identify the original owner.

4. **Correspondence**: Version comparison works because shared I-addresses reveal what content two versions have in common.

### The Two Paths to "Same Text"

| Operation | I-Space Effect | V-Space Effect | Identity |
|-----------|---------------|----------------|----------|
| **COPY** | No new bytes created | New V-mapping to existing I-address | Same content (shared identity) |
| **INSERT** | New bytes created at new I-address | New V-mapping to new I-address | Different content (independent identity) |

If you INSERT the text "hello" into document A, and separately INSERT "hello" into document B, those are **different bytes** at different I-addresses — structurally unrelated despite being textually identical.

If you COPY "hello" from document A into document B, document B's V-stream references the **same bytes** at document A's I-address. The system knows they are the same content.

### Nelson's Design Intent

Nelson frames this as the solution to a fundamental problem:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

And the contrast with dead copies:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/48]

### Summary

A copy **must** share the same I-space address as the original. This is not an optimization — it is the architectural foundation of transclusion, attribution, discovery, and royalty. The system has no mechanism for "duplicate content at a new address" through COPY. If you want independent content that happens to have the same value, you INSERT it fresh, creating new I-space bytes with a new address and no structural connection to the original.
