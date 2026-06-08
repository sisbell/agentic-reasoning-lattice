## Question 1 [theory]

> For INSERT, what does the design require regarding (a) fresh content identity — that inserted content always gets new I-addresses never aliased to existing ones — and (b) cross-document independence — that inserting into one document never alters another document that transcludes its content?

## INSERT: Fresh content identity and cross-document independence

The FEBE specification for INSERT itself describes only the Vstream effect:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

But the two requirements you ask about follow necessarily from the Istream/Vstream architecture in which INSERT operates.

### (a) Fresh content identity

INSERT is *creation* of new content, and Xanadu storage is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes flow into the storage system, filed, as it were, chronologically." (2/14)

In an append-only store, new content is laid down at new, never-reused locations. Content identity in Xanadu is tied to creation, not to value — the design distinguishes "wrote new bytes" from "quoted existing bytes." As the curated provenance source states: *content identity is based on creation, not value; two documents with identical text created independently have DIFFERENT I-addresses, while transcluded content SHARES the same I-address.*

This is exactly why there are two distinct operations. INSERT mints new Istream bytes; COPY (transclusion) is the *only* operation that aliases to existing I-addresses:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." (4/67) — and the copy shares the source's I-addresses.

So the design requires that inserted text receive fresh I-addresses, never aliased to existing content. If aliasing happened, attribution and royalty would misfire: the system "always knows where you are, and can at once ascertain the home document of any specific word or character" (2/40) only because each created byte has its own home.

### (b) Cross-document independence

Because transclusion is *inclusion by reference to immutable Istream content*, editing one document cannot reach into another that references the same bytes. Nelson states this directly for the symmetric case (deletion):

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

The same principle protects INSERT: the operation only (1) appends new Istream bytes and (2) rewrites document A's own Vstream ordering. The specific I-addresses that document B references are untouched, so B's view is unchanged. Nelson frames this as the whole point of reference-based composition:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." (2/36)

And transcluded ("non-native") bytes are addressed independently of A's local arrangement:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

### One nuance worth flagging

Independence holds strictly for *content*-referenced transclusion (a window fixed to specific bytes / a point in time). Nelson also describes a *location*-fixed window mode that deliberately re-resolves to a document's current state and therefore *does* reflect later edits:

> "...at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." (2/37)

That auto-updating behavior is a chosen front-end transclusion semantic, not a violation of the invariant — the underlying Istream bytes B references are still immutable; a location-fixed window simply asks for A's *current* span rather than a fixed one.

### Summary

- **(a)** Required. INSERT creates content, and under append-only storage with creation-based identity, created bytes get fresh I-addresses; only COPY/transclusion aliases existing I-addresses (4/66, 4/67, 2/14).
- **(b)** Required. INSERT touches only A's new Istream bytes and A's Vstream ordering; documents transcluding A reference immutable I-addresses, so they are unaffected (4/11, 2/36) — with the understood exception that a *location*-fixed window intentionally tracks A's current state (2/37).

Note: Nelson gives no single sentence asserting "INSERT mints new, non-aliased I-addresses"; both requirements are derived from the append-only storage model, content immutability, and the COPY-vs-INSERT distinction in the curated sources. The cross-document point is stated explicitly by Nelson only for the deletion case (4/11), from which the INSERT case follows by the same Istream-immutability principle.
