## Question 4 [theory]

> When the requested spans draw on content that is shared by transclusion across documents, what does delivering them together reveal that delivering one span at a time would conceal?

## Short answer

Delivering the spans **together** lets the addresses be compared, and that comparison reveals **commonality** — the fact that the spans resolve to the *same* Istream content, i.e., that they are transclusions of one origin rather than independent text that merely happens to read alike. Delivered one at a time, each span arrives as a self-contained stretch of bytes; the *relationship between them* — their shared home — is what stays concealed.

## Why this is so

Transclusion is inclusion by reference, not copy. Content has a permanent Istream address, and a transcluded span carries that same I-address wherever it appears:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

Identity in Xanadu is by *creation*, not by *value*. As the provenance notes put it: two documents with identical text created independently have **different** I-addresses; transcluded content **shares** the same I-address. So "the same words" and "the same bytes" are distinguishable only by looking at addresses — which requires having both spans in hand at once.

This is exactly the commonality Nelson promises the system will surface:

> "It will also reveal and clarify commonalities between documents and among versions, simplifying both storage and comprehensibility." (3/4)

A single span delivered alone still lets you trace its origin — "you always know where you are, and can at once ascertain the home document of any specific word or character" (2/40) — but origin-of-one is not the same as overlap-between-two. The *overlap* (this passage in document A is the very same byte-stream as that passage in document B) becomes visible only when the spans are co-delivered and their I-addresses can be set side by side.

## What specifically gets revealed

- **Shared origin / true overlap.** Co-delivery shows that two spans are one content seen twice, not two coincidentally-similar contents. The correspondence machinery is built on exactly this: `SHOWRELATIONOF2VERSIONS` "returns a list of ordered pairs of the spans of the two spec-sets that correspond" (4/70) — correspondence being defined by shared Istream origin.
- **The web of inclusion.** `FINDDOCSCONTAINING` "returns a list of all documents containing any portion of the material... regardless of where the native copies are located" (4/63). Seeing the spans together is what lets you perceive a quotation as a quotation and locate its place in that web.
- **Live connection vs. inert text.** The shared link is what keeps transcluded material "live" — "the free-flowing, live documents on the network are subject to constant new use and linkage" (2/48). Delivered in isolation and treated as standalone, a span loses the visible fact that it is the *same* live content as another, which is "a considerable deprivation" (2/48).
- **Compression/storage economy.** Nelson assigns the middle end the job of "back-comparison between versions" and "finding commonalities for compression" (FEBE design, 4/72 region) — work that is only possible when the overlapping spans are present together.

## Caveat

Nelson does not, in the curated sources, give a single passage that directly answers "what does *batched* span delivery reveal that *serial* delivery conceals" in those words. The answer above is assembled from his statements about transclusion sharing I-addresses (4/11), commonality (3/4), correspondence (4/70), and home-document traceability (2/40). If you want a passage that speaks directly to delivery batching versus single-span delivery, that would be in the protocol/retrieval discussion:

NEED_RAW: 4/61–4/67 (RETRIEVEV and spec-set delivery), 4/72 (middle-end commonality/compression)
