## Question 9 [nelson]

> If content is removed from a document and later the same content is re-inserted, must the system recognize it as the same content returning rather than treating it as new content?

## No — INSERT Creates New Content; COPY Restores the Same Content

The architecture answers this unambiguously through the I-space/V-space separation.

### DELETE Does Not Destroy Content

When content is deleted, it is removed from V-space (the document's current arrangement) but **remains permanently in I-space**:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The content never "left." It is still at its original I-address, still accessible through old versions, still present in any document that transcludes it.

### INSERT Always Creates New Content

The INSERT operation appends fresh bytes to I-space:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

New bytes get new I-addresses. Even if the character sequence is identical to what was deleted, **content identity is based on creation, not value**:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."

So if you delete "hello world" and then type "hello world" again via INSERT, the system treats the re-typed text as entirely new content — different I-addresses, different origin, no structural relationship to the deleted bytes.

### COPY Is How You Restore the Same Content

The COPY operation is the mechanism for preserving identity:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This is transclusion — the copy shares I-addresses with the source. To restore deleted content *as the same content*, you would COPY from the still-existing I-space bytes (reachable through a previous version or another document that includes them), not INSERT new text that happens to match.

### Why This Matters

The distinction has real consequences:

| Scenario | I-Addresses | Links to original | Royalties | Correspondence |
|----------|-------------|-------------------|-----------|----------------|
| DELETE then INSERT same text | New addresses | Do NOT attach to new text | Flow to new I-address owner | Not recognized as same |
| DELETE then COPY from old version | Original addresses | Still resolve | Flow to original creator | Recognized as same |

Links that pointed to the original content survive deletion (they point to I-space), but they will NOT automatically attach to re-inserted text that merely has the same character values. They WILL resolve if the content is restored via COPY, because COPY preserves I-space identity.

### The Deeper Point

The system doesn't need a mechanism to "recognize returning content" because **content never leaves I-space**. The append-only storage model means:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Delete is a V-space operation. Restoration is also a V-space operation — re-mapping the document's virtual byte stream to point back at the still-existing I-space content. The correct tool for this is COPY (or version restoration), not INSERT.
