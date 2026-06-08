## Question 4 [theory]

> What does deleting a span — rather than a single position — reveal about the distinction between an arrangement ceasing to bind content and that content ceasing to exist?

Deleting a span is the operation where Xanadu's two-layer architecture becomes visible, because a span is the smallest unit that has *both* an arrangement aspect and a content aspect at once.

## A position has no content; a span does

A single position in the virtual byte stream is a boundary — a place between bytes. It designates no content. A span, by contrast, has extent: it covers actual bytes, and every one of those bytes has a permanent Istream address that exists independently of where (or whether) any document arranges it. Nelson defines the span by its endpoints, with the content between them *implicit*:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

So a span is precisely the place where an *arrangement feature* (a from-here-to-there in Vstream) and an *existence fact* (the I-addressed bytes it covers) coincide. Deleting it pulls the two apart.

## The operation deletes a *vspan*, not bytes

The command name itself encodes the distinction:

> "DELETEVSPAN: This removes the given span from the given document." (4/66)

It is a *V*-span that is removed — a feature of the virtual byte stream, the document's current arrangement:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

What is removed is the document's binding of those V-positions to content. The content's home is untouched, and indeed the byte's native address "may be constantly changing" (4/11) regardless — arrangement was never where the bytes *lived*.

## What "deleted" actually means

Nelson's own annotation for the deleted state makes the difference explicit. Deletion produces:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

Three clauses, three proofs that arrangement ceased to bind while content did not cease to exist:

1. **"not currently addressable"** — the loss is to *this arrangement's* reach, not to the bytes.
2. **"awaiting historical backtrack"** — prior arrangements still bind the same content; you can reconstruct them.
3. **"may remain included in other versions"** — other Vstreams still bind it:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

If deleting the span destroyed the content, transclusions of it would break. They don't — which demonstrates that one document's arrangement releasing a span is not the same act as the span ceasing to be.

## Links are the witness

The clearest demonstration is that links to deleted content still resolve. Because a link is anchored to bytes, not positions —

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." (4/42)

— deleting the span from an arrangement leaves the strap attached:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

A link could not survive deletion if deletion annihilated the bytes. Its survival is direct evidence that the deletion removed a *binding* (the V-extent that placed the content in this document now) and left the *existence* (the I-addressed bytes) intact.

## What the span reveals

A position-deletion would reveal nothing, because a position binds no content — there is nothing underneath it that could "still exist." Only when you delete something with extent — a span — do you witness the separation: the arrangement's grip on a stretch of content is released, the V-addresses close up, and yet the bytes persist at their permanent home, recoverable by backtrack, still bound by other versions, still held by every link strapped to them. The span is the seam between *binding* and *being*; deleting it is what shows the seam was there all along.
