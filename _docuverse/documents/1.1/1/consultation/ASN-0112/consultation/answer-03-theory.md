## Question 3 [theory]

> What relationship must hold between the extent the document reports and the content currently arranged within that document?

## The Invariant

The extent a document reports (via `RETRIEVEDOCVSPAN`) must **exactly cover the content currently arranged in the document's Vstream** — no more, no less. The reported extent measures the *current arrangement* (Vstream), not the permanent content store (Istream).

This follows from two facts in the curated sources:

**1. The extent is over the V-stream, not the I-stream.**

> "RETRIEVEDOCVSPAN: 'This returns a span determining the origin and extent of the V-stream of document <doc id>.' (4/68)" — from the operations source

So what is reported is the extent of the document's *virtual byte stream* — the current arrangement the user sees — not everything ever stored.

**2. The Vstream is dense and contiguous, so the extent and the arranged content cannot diverge.**

The v-space-addresses source establishes that V-addresses always form a gapless sequence:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

Because every edit keeps the Vstream contiguous (INSERT shifts following addresses up; DELETE closes the gap), the length of the reported extent must equal the number of bytes currently arranged. There can be no arranged byte that falls outside the reported extent, and no position inside the extent that holds no arranged byte.

## Why deleted content does not count

This is the key consequence. Content removed by DELETE remains permanently in Istream, but it is gone from the Vstream arrangement — and therefore gone from the reported extent. From the delete-semantics source:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

"Not currently addressable" means it is not part of the current Vstream, so it is excluded from the document's reported extent. The extent tracks the *live arrangement*, not the historical accumulation.

## The companion measure

`RETRIEVEDOCVSPANSET` enforces the same correspondence in counted form:

> "RETRIEVEDOCVSPANSET: 'This returns a span-set indicating both the number of characters of text and the number of links in document <doc id>.' (4/68)" — from the operations source

The character and link counts it returns must match exactly the text and links currently arranged in the document.

## Summary

The relationship is one of **exact correspondence over the current arrangement**: the reported extent (and the reported span-set counts) must equal precisely the content presently arranged in the document's Vstream — contiguous, gapless, beginning at the document's V-origin — while content that exists only in Istream (deleted bytes, content native to other documents but not arranged here) is excluded from the report.
