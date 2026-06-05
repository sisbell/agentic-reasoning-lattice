## Question 1 [theory]

> When a document is asked only by its identity to report where its content begins and how far it extends, what must that answer describe about the document as a whole?

This question maps to a specific FEBE operation: **RETRIEVEDOCVSPAN**, the command that takes only a document's identity (its tumbler `<doc id>`) and reports the boundaries of its content.

## The Answer: The Document's Entire V-Stream as a Single Span

When a document is asked only by its identity to report where its content begins and how far it extends, the answer must describe the **document's complete Vstream (virtual byte stream) arrangement** — expressed as a single span with two components: an **origin** (where the content begins) and an **extent** (how far it reaches).

From the operations reference:

> **RETRIEVEDOCVSPAN**: "This returns a span determining the origin and extent of the V-stream of document <doc id>." (4/68)

## What "the document as a whole" means here

Three things follow from this being a *span* and being over the *V-stream*:

**1. It describes the current arrangement, not the permanent content.** The answer is in Vstream — the document's present ordering as the user sees it — not Istream (where the bytes permanently live). The Vstream is dense and contiguous, always forming an unbroken sequence:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

Because the Vstream is contiguous, a single origin-plus-extent span can describe the whole document — there are no gaps to enumerate.

**2. It is a boundary, not a count.** Critically, the span returned does *not* tell you "how many bytes" in the conventional sense. A span designates "from here to there":

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

So the answer describes the document as a whole *implicitly* — by fixing its starting boundary and its width, everything between is determined.

**3. It spans only the document's own content, regardless of where that content natively lives.** The Vstream may include transcluded bytes from other documents, but the span still describes this document's arrangement as one coherent extent:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

## Contrast with a related operation

Note the distinction between reporting *boundaries* versus reporting *quantities*. RETRIEVEDOCVSPAN gives the origin/extent boundary. A separate operation reports counts:

> **RETRIEVEDOCVSPANSET**: "This returns a span-set indicating both the number of characters of text and the number of links in document <doc id>." (4/68)

The question — "where its content begins and how far it extends" — is precisely the origin-and-extent framing of RETRIEVEDOCVSPAN, not the character/link tally of RETRIEVEDOCVSPANSET.

## Summary

The answer must describe the document's **entire virtual byte stream as a single contiguous span** — giving its **origin** (the starting position in Vstream where content begins) and its **extent** (the width reaching to the end). This is a boundary description of the document's current arrangement as a whole, not a byte count, and it holds whether the content is natively stored or transcluded from elsewhere.
