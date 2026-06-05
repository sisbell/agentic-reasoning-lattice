## Question 5 [theory]

> What identity guarantee must the returned content carry, so that a reader can know which underlying content each returned piece corresponds to?

## The Identity Guarantee: Each Piece Must Carry Its Istream (I-Address) Identity

The guarantee is **origin traceability through the permanent Istream address**. Every returned piece of content must carry — or be resolvable to — its permanent I-address, so the reader can determine exactly which underlying content (and which home document) it corresponds to.

### Why the I-address is the identity

Xanadu separates two address spaces. The **Vstream** is the document's current arrangement (ephemeral, shifts during editing). The **Istream** is where content permanently lives, with addresses that never change. Identity lives in Istream, not Vstream:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

Because the V-position is unstable, it cannot serve as identity. The stable, content-identifying address is the I-address, whose Document field encodes the originating document.

### The guarantee Nelson states

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

This is the user-facing form of the guarantee: for *any* returned character, you can ascertain its home document. That only works if each piece carries (or resolves to) its I-address identity.

### Why this matters for retrieval specifically

`RETRIEVEV` "returns the material (text and links) determined by `<spec set>`" (4/67). When a document transcludes content from elsewhere, the returned stream mixes native and non-native bytes:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

So a returned piece looks positionally identical whether it was authored here or quoted from another document. Without an identity tag, the reader could not tell apart "this author's words" from "a transcluded quotation." The I-address is what distinguishes them — it is how the system knows which underlying content each piece corresponds to, and how it attributes, finds transclusions, and compares versions.

### Summary

The returned content must carry its **permanent Istream identity (I-address)** for each piece. The Vstream position alone is insufficient because it changes with editing. The I-address is the invariant that lets a reader resolve any returned byte to its underlying content and home document — satisfying Nelson's guarantee that you can "at once ascertain the home document of any specific word or character" (2/40).

NEED_RAW: 4/61-4/70 — to confirm whether Nelson specifies that `RETRIEVEV`'s return value *explicitly* tags each returned span with its I-address (vs. the identity being recoverable via a separate operation). The curated FEBE/operations sources describe what `RETRIEVEV` returns but do not state the exact form of the per-piece identity in the response.
