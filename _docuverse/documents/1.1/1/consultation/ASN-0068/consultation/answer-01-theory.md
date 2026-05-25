## Question 1 [theory]

> What must the system guarantee about the identity of a piece of content shared between two documents?

# Content Identity Across Documents: The Core Guarantee

When the same piece of content appears in two documents, the system must guarantee that it is **the same piece of content** — one identity, not two copies that happen to match. This is the heart of transclusion and the reason Xanadu exists.

## What the System Must Guarantee

**1. A single Istream identity (one I-address, one home).**

Shared content has exactly one permanent address in Istream. The content lives in one place — its home document — and is referenced from anywhere else.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

**2. Identity by creation, not by value.**

Two documents that independently contain the same text are NOT sharing content — they have different I-addresses. Only content that was deliberately included (transcluded) shares identity. This distinguishes "quoted from" from "happens to say the same words."

**3. Logical equivalence regardless of origin.**

Within any document that includes shared content, that content is a first-class part of the document — not a degraded reference or footnote.

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Non-native bytes are as much a logical part of a document as native bytes." [LM 4/11]

**4. Permanent traceability to origin.**

The home document of any byte is always discoverable. Attribution is structural, not metadata that can be stripped.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

**5. Ownership preserved across sharing.**

Inclusion does not transfer ownership. The home document's owner retains control of the content even when it appears elsewhere.

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

**6. Address transparency at the user level.**

Users and front-ends work with logical (Vstream) positions; the underlying Istream identity is preserved by the system invisibly.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

## Why This Matters

These guarantees together solve what copying destroys: when content is copied in conventional systems, the copies diverge, lose connection to source, and break attribution. By giving shared content **one identity** rather than duplicated identities, Xanadu preserves the web of intellectual connection that literature actually is. Royalties flow correctly because the system knows whose bytes are being delivered. Versions can be compared because correspondence emerges from shared I-addresses. Links survive editing because they attach to identity, not position.

This is not a feature added on top of storage — it is the storage model. The very meaning of "the same content in two documents" must be **one piece of content referenced twice**, not two pieces that match.
