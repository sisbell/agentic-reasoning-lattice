## Question 1 [theory]

> When content is placed into a document by transclusion, what must remain identical between the placed material and its source — and what does the destination record as newly its own?

## What Transclusion Preserves vs. What the Destination Owns

Transclusion is "inclusion by reference, not copy" (transclusion design note). This split — reference vs. copy — is exactly the answer to your question. The **identity** of the material stays fixed at the source; the **arrangement** is what the destination makes newly its own.

### What must remain identical: the Istream address (content identity)

The placed material keeps the very same permanent I-address it has at its home. Nothing is duplicated:

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

Because the I-address is shared, three things remain identical with the source:

1. **The bytes themselves** — they are fetched from the home location, never copied. The destination holds a reference, "obtained by front-end or back-end requests to their home locations" (4/11).
2. **Origin / home document** — attribution is structural. As the `sporgl-provenance` note records: "Transcluded content SHARES the same I-address." You can "at once ascertain the home document of any specific word or character" (2/40).
3. **Ownership of the source content** — "Document A can include Document B, even though Document B is owned by someone else" (2/35). The original owner retains control and continues to receive royalties.

The `operations` note makes the mechanism explicit for the COPY command: "This is transclusion — the copy shares I-addresses with the source."

### What the destination records as newly its own: the Vstream position

The including document assigns the material a fresh **ordinal position in its own virtual byte stream** — a Vstream arrangement layered over the unchanged Istream content:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

> "Non-native bytes are as much a logical part of a document as native bytes." (4/11)

So while the *identity* (I-address) is borrowed unchanged, the *placement* (V-address, the "where it appears here") is the destination's own creation. The COPY operation lands the material "at the address determined by `<doc vsa>`" (4/67) — a Vstream address belonging to the destination.

The destination also owns the compound document as a whole, including its own royalty accounting:

> "Each compound document is like the other documents: it has an owner and receives royalties." (2/33)

And when read, the value split follows authorship automatically: "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" (2/45).

### Summary

| Aspect | Stays identical to source | Newly the destination's own |
|--------|---------------------------|-----------------------------|
| Content bytes | Yes — referenced, not copied (4/11) | — |
| I-address (identity) | Yes — shared (4/10–4/11) | — |
| Home document / origin | Yes — traceable (2/40) | — |
| Ownership of the *content* | Yes — original owner retains it (2/35) | — |
| V-address (ordinal position) | — | Yes — assigned in its own byte stream (4/11) |
| The compound document & its cash register | — | Yes — its own owner, its own royalties (2/33) |

In short: **the identity (Istream address, bytes, origin, source-ownership) must remain identical; the arrangement (Vstream position) and the surrounding compound document, with its own ownership and royalty register, are what the destination records as newly its own.**
