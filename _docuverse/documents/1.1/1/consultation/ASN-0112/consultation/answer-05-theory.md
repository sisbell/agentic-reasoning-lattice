## Question 5 [theory]

> What does a caller learn from the returned origin and extent that the document's identity alone does not already make known?

## What the span tells you that identity does not

A document's **identity** is its tumbler address (`N.0.U.0.D`). That address is a pure locator: it tells you *where* the document sits in the docuverse tree and *who* owns it, but nothing about its contents. Nelson is explicit that tumblers "impose no categorization and no structure on the contents of a document" (4/17-4/18), and that "time is not included in the tumbler. Time is kept track of separately." (4/18)

`RETRIEVEDOCVSPAN` "returns a span determining the origin and extent of the V-stream of document `<doc id>`." (4/68) From that span the caller learns two things identity cannot supply:

- **Origin** — the actual starting V-address of the document's current arrangement, the anchor for further addressing.
- **Extent** — how far the live V-stream reaches *right now*, i.e., the bounds of what is presently addressable.

Because the V-stream "may be continually altered by editorial operations" (4/30) while the address stays permanent, the span reflects the *current* shape of the version — the operational bounds you need before issuing retrieve, delete, or rearrange requests. The identity says the document exists and where; the span says how much is in it at this moment.

One caution: the extent is a span, not a count — "a tumbler-span is not a conventional number, and it does not designate the number of bytes contained." (4/24) For an actual character/link count you would call `RETRIEVEDOCVSPANSET`, which "returns a span-set indicating both the number of characters of text and the number of links" (4/68).
