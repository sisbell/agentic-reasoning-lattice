## Question 8 [nelson]

> Must the mapping from a document's arrangement back to the permanent content be exact — byte-for-byte correspondence — or can a document transform or excerpt content in ways that break that correspondence?

## The mapping must be exact — byte-for-byte, no transformation

The V→I mapping in Xanadu is a strict, exact correspondence: each position in V-space maps to precisely one byte in I-space, with no transformation, summarization, or modification permitted at the mapping level.

### The evidence is structural

**I-space content is immutable.** Content at an I-space address never changes after creation. The entire I-space is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**V-space is a view, not a transform.** The document IS the mapping from V-addresses to I-addresses. Non-native bytes appear "just as if they were native":

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The word "just as if" is critical — the bytes appear identically, not in altered form.

### No transformation operation exists

The FEBE protocol defines exactly five editing operations. None performs transformation:

| Operation | What it does to I-space | What it does to V-space |
|-----------|------------------------|------------------------|
| **INSERT** | Creates new bytes (new I-addresses) | Adds positions, shifts subsequent |
| **APPEND** | Creates new bytes at end | Extends V-stream |
| **COPY** | Nothing — shares existing I-addresses | Adds positions referencing existing I-content |
| **DELETEVSPAN** | Nothing — bytes remain | Removes positions from view |
| **REARRANGE** | Nothing | Transposes regions |

COPY is the transclusion operation, and it explicitly shares I-addresses with the source:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This is reference, not duplication. The copied bytes retain their original I-addresses. There is no operation that says "take these I-space bytes, apply function F, and show the result."

### Excerpting is supported — but it's still exact

You can include a subset of another document's bytes (a span from position 47 to 92, say). This is excerpting. But the bytes you include are the exact original bytes — you select which ones, but you don't alter them. Nelson's Shakespeare example illustrates this:

> "Very well, if Hamlet is already on the system, then E.G. Jewett could publish his own Hamlet very easily: a quote-link to the first part of the original, just up to 'in the soliloquy'; then the word 'luge'; then a quote-link to the rest of the play."

Jewett's document has three V-space regions: a span of Shakespeare's I-bytes, a new I-byte ("luge"), and another span of Shakespeare's I-bytes. Each region maps exactly to its I-space source.

### Correspondence depends on exactness

The entire correspondence mechanism relies on this exactness:

> "Correspondence is a RELATION — the relationship between V-space positions that share the same I-space origin. If two V-positions in different documents (or different versions of the same document) map to the same I-address, those positions CORRESPOND."

If transformation were possible, shared I-addresses would no longer prove correspondence — the same I-bytes could appear differently in different V-space contexts. The version comparison operation SHOWRELATIONOF2VERSIONS returns "ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70], which only works if shared I-address means identical content.

### Attribution depends on exactness

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This guarantee — that you can trace any character to its origin — requires that the character at a V-position IS the character at the corresponding I-position. If transformation were allowed, you'd trace back to different content than what you're seeing.

### Content identity is creation-based, not value-based

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."

This means I-addresses are identity tokens, not content hashes. The system doesn't ask "do these bytes have the same value?" — it asks "are these the same bytes?" Transformation would sever identity while preserving some relationship to the original, but Xanadu has no mechanism for that intermediate state.

### Front-end rendering is separate

The front end may render the same bytes differently — display them in a different font, zoom into a bitmap, play audio at a different speed. But this is display-level interpretation, not a change to the V→I mapping. The bytes flowing from back end to front end are exact.

### Summary

The V→I mapping is a strict bijection at the byte level. Each V-position maps to exactly one I-byte, and that I-byte is delivered unchanged. The architecture provides three things you can do with content: **create** it (INSERT/APPEND → new I-addresses), **reference** it (COPY → shared I-addresses), or **hide** it (DELETE → V-space removal, I-space unchanged). There is no fourth option of "transform it." This exactness is not incidental — it is the foundation on which correspondence, attribution, link survivability, and royalty tracking all depend.
