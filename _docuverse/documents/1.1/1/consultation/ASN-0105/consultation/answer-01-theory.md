## Question 1 [theory]

> When a continuous span of a document is read at once, what must the returned content faithfully preserve about the order in which those contents appear in the document?

## Answer

When a continuous span is read at once, the returned content must faithfully preserve the document's **virtual byte stream order (Vstream order)** — the sequence in which those bytes appear in the document's *current arrangement* — regardless of where the bytes physically live in storage.

This is the crux of the Istream/Vstream separation. A document is a Vstream arrangement, and a continuous span designates a contiguous run of positions in that virtual byte stream. The content fetched back may be assembled from many scattered native origins (the document's own native bytes plus transcluded/included bytes whose home is elsewhere), but it must come back in the **ordinal sequence dictated by the Vstream**, exactly as the reader sees it in the document.

Nelson is explicit that this virtual ordering is what governs:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

And critically, included (non-native) bytes occupy positions in this order *as if* they were native:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

> "Non-native bytes are as much a logical part of a document as native bytes." (4/11)

The physical/Istream addresses are irrelevant to this returned ordering — they may even be shifting underneath:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

So the faithful preservation is of the **logical V-stream sequence**: the ordinal positions in the document's current virtual arrangement, with native and transcluded content interleaved in exactly the order the document specifies — not the order or grouping of their underlying storage. This is the order that `RETRIEVEV` honors when delivering "the material (text and links) determined by `<spec set>`" (4/67).

One scope note: the curated sources establish the *ordering* guarantee for content within a span via the Vstream model, but they do not separately spell out tie-breaking between co-located text and links at the same position when a span containing both is retrieved. If you need that finer-grained delivery-ordering detail, NEED_RAW: 4/61-4/67.
