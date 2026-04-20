## Question 2 [nelson]

> Does placing content into a document add any new bytes to permanent storage, or does it solely change the document's arrangement?

## It depends on the operation.

Xanadu has two address spaces, and the answer differs sharply depending on which operation places the content:

### Operations that ADD new bytes to permanent storage (Istream)

**INSERT** and **APPEND** create new content — bytes the user types or provides. These bytes are appended to the Istream (the permanent, append-only store) and simultaneously mapped into the document's Vstream (current arrangement).

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

New bytes get permanent I-addresses encoding their home document. Those addresses never change.

### Operations that ONLY change arrangement (Vstream)

**COPY** is transclusion — it creates a Vstream mapping to *existing* Istream content. No new bytes are created in permanent storage. The included bytes share the same I-addresses as the originals:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Content identity is based on creation, not value. Two users typing identical text independently produce different I-addresses. But COPY shares the original's I-address — that's how the system distinguishes "wrote the same words" from "quoted from the original."

**REARRANGE**, **DELETE**, and **CREATENEWVERSION** also change only the Vstream arrangement. DELETE doesn't remove bytes from Istream; it removes them from the current view:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

CREATENEWVERSION creates a new Vstream arrangement over the same Istream content — effectively a whole-document transclusion.

### Summary

| Operation | New Istream bytes? | Vstream change? |
|-----------|-------------------|-----------------|
| INSERT | Yes | Yes |
| APPEND | Yes | Yes |
| COPY | No — shares existing I-addresses | Yes |
| REARRANGE | No | Yes |
| DELETE | No | Yes (removal) |
| CREATENEWVERSION | No | Yes (new arrangement) |

The architectural insight: a document IS its Vstream-to-Istream mapping. Only operations that bring genuinely new content into existence touch the permanent store. Everything else — quoting, rearranging, versioning, deleting — is purely a change of arrangement over content that already exists and will exist forever.
