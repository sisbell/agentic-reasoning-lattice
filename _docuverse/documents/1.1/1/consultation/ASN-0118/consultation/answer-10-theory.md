## Question 10 [theory]

> What makes transclusion a sharing of one identity across documents rather than the manufacture of a separate copy — what is the boundary the design must hold?

## The boundary is the I-address

What makes transclusion *sharing one identity* rather than *manufacturing a copy* is that the transcluded bytes keep their original **Istream address**. Identity in Xanadu is not the visible text — it is the permanent home location where content was first created. Two documents containing the same words typed independently have *different* I-addresses; transcluded content has the *same* I-address as its source. The sporgl-provenance note states the rule directly: "Content identity is based on creation, not value... Transcluded content SHARES the same I-address."

So the design boundary is the **Istream / Vstream separation**. A document is a Vstream arrangement — an ordering of references — laid over permanent Istream content. Transclusion adds a Vstream reference pointing at someone else's Istream bytes. A copy, by contrast, would mint *new* native bytes with a *new* I-address, severing identity.

## What holds the boundary: native vs. non-native bytes

Nelson draws the line at whether bytes are "native":

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

The crucial guarantee is that the inclusion is *fully a part* of the document semantically while remaining *not stored* in it:

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

> "Non-native bytes are as much a logical part of a document as native bytes." (4/11)

Because non-native bytes must be "obtained by... requests to their home locations," the connection to source cannot be dropped — the fetch mechanism *requires* it. That is what makes attribution structural rather than metadata:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

## Why this matters — the two failure modes a copy would cause

The transclusion concept names exactly what is lost when the boundary breaks and content is copied instead of referenced:

> "1. Copies diverge from originals
> 2. Copies lose attribution
> 3. Copies break the living connection"

And Nelson's water analogy frames the same boundary as live-vs-dead:

> "Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage... Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." (2/48)

A copy gets a new identity and is therefore frozen out of the source's future linkage and updates; a transclusion, sharing identity, stays live.

## The operational boundary: COPY must not duplicate identity

The design holds this boundary even at the level of the editing operation. The FEBE `COPY` command is transclusion — and the operations note is explicit that "the copy shares I-addresses with the source." So even the act named "copy" must not manufacture a separate identity: it produces a Vstream mapping back to the original Istream content, which is also why `FINDDOCSCONTAINING` can find every document that includes a given span "regardless of where the native copies are located" (4/63).

## Summary

The single boundary the design must hold is: **including content must never create new native (Istream) bytes — it must only add a Vstream reference to existing home-location bytes.** Identity lives in the I-address; sharing the I-address is sharing the thing itself. The moment a system stores fresh native bytes for included material, it has minted a second identity — a copy — and forfeited divergence-protection, attribution, and live connection all at once.
