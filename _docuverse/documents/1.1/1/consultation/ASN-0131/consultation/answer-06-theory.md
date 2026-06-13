## Question 6 [theory]

> For an endset that touches the region through transcluded content, what must the returned span describe — the place in the region where the borrowed content now appears, or the original home of that content?

## Answer: the original home of that content

The returned span must describe the borrowed content at its **native (Istream) home** — not the Vstream position in the region where the window currently displays it.

This follows necessarily from two architectural facts: how endsets attach to content, and what transclusion actually is.

### 1. Endsets attach to bytes by identity, not by position

A Xanadu link does not seize a place; it seizes content. Its endsets are arbitrary sets of *bytes*:

> "A Xanadu link is not between points, but between spans of data." (`links`, 4/42)

> "This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (`endsets`, 4/42)

Because the attachment is to bytes rather than positions, the endset is expressed in the permanent identity space (Istream). That is precisely what gives links their survivability:

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, the link remains on them." (`links`, 4/42)

A Vstream position — "where the borrowed content now appears" — is exactly the kind of address that is *not* stable: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing" (`i-space-v-space`, 4/11). An endset cannot be that, or links would break on every edit.

### 2. Transcluded content has its home elsewhere — and is addressed there

The bytes touched through a transclusion are not a local copy. They are *native elsewhere*, fetched from their home:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (`i-space-v-space`, 4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (`i-space-v-space`, 4/11)

Transclusion creates a Vstream mapping to *existing* Istream content — the copy shares the source's I-addresses (`transclusion`, `sporgl-provenance`). So there is only one instance of the content, living at one home. An endset touching that content in the region is, by identity, an endset on the home bytes. There is no separate "in-the-region" identity for it to describe.

### Why this is the only coherent answer

The whole point of pointing endsets at the home/Istream is what the spec calls survivability — endsets "point to Istream (enables survivability)" (`endsets`, related-concepts table). Describing the home rather than the window is what makes three downstream guarantees hold:

- **Survivability** — the link is unaffected when the region (or the home) is edited and Vstream positions shift.
- **Refractive reach** — a link made against borrowed content automatically holds on the original and on every other document that windows the same bytes, because they share the address (the same mechanism by which "a link to one version of a Prismatic Document is a link to all versions," `correspondence`, 2/26).
- **Discoverability** — `FINDDOCSCONTAINING` finds material "regardless of where the native copies are located" (`operations`, 4/63), and link search matches on endset addresses; both work only if the endset is keyed to the content's home identity, not to a transient local slot.

If the span instead described the place in the region, the link would be anchored to a shifting Vstream coordinate, would be invisible from the home document and from co-transcluders, and would silently break the moment the region was re-edited — contradicting every link guarantee Nelson states.

### One scoping caveat

Nelson states each premise explicitly — endsets attach to bytes (4/42), transcluded bytes are native elsewhere and addressed at their home (4/11), and links point to identity so they survive editing (4/42). The specific *composition* of those premises ("therefore an endset touching transcluded content returns the home span") is an entailment of the architecture rather than a single sentence I can quote verbatim. If you want a passage that addresses endsets-on-inclusions head-on, that would be in the links/endsets technical run:

NEED_RAW: 4/42–4/47
