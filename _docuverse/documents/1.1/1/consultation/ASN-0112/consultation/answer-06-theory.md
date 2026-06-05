## Question 6 [theory]

> Must every document be able to answer this question about itself, or are there documents for which an origin and extent are undefined?

## Short answer

Every document has a defined origin and extent. There are no documents for which these are undefined — even an empty document answers the question, with an extent of zero.

The question is essentially about the FEBE operation **RETRIEVEDOCVSPAN**:

> "This returns a span determining the origin and extent of the V-stream of document `<doc id>`." (4/68)

## Why origin is always defined

A document's origin is structural, not optional. Every document occupies a permanent position on the tumbler line, and its V-stream begins at that position:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

Because the document field of the tumbler determines where the V-stream starts, the origin is fixed the moment the document exists. You cannot have an addressable document without a defined origin — being addressable *is* having an origin.

## Why extent is always defined

The V-stream is dense and contiguous, always beginning at position 1 with no gaps. There is no arrangement in which the extent is ambiguous — it is simply the current width of that contiguous sequence. A span need not contain anything for its boundaries to be well-defined:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

## The edge case: empty documents

`CREATENEWDOCUMENT` "creates an empty document" (4/65). This is the case that might look undefined, but it isn't. An empty document has a defined origin (its tumbler address) and an extent of **zero** — a degenerate but perfectly valid span. Nelson's span model explicitly allows empty extent:

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

So an empty document still answers RETRIEVEDOCVSPAN cleanly: origin = its address, extent = 0.

## On ghost documents

One genuine subtlety: a document *address* can exist as a "ghost element" with nothing stored against it:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

This does not create an exception. A ghost is an address with no stored content — which is the same situation as an empty document: origin defined by position, extent zero. The address is always answerable; "nothing is stored there" is itself a well-defined answer, not an undefined one.

## Conclusion

Yes — every document must be able to answer this about itself. Origin is guaranteed by permanent tumbler addressing, and extent is guaranteed by the dense, contiguous-from-1 nature of the V-stream. The only "empty" cases (newly created documents, ghost positions) resolve to a defined origin with zero extent, not to an undefined result. This is consistent with Nelson's principle that "everything in the system is part of a document" with no "free-floating materials" (2/29).

(Note: the precise return semantics of `RETRIEVEDOCVSPAN`/`RETRIEVEDOCVSPANSET` for the empty case are drawn from the operation definitions at 4/68 and the span model at 4/24–4/25; Nelson does not give a worked empty-document example, so the extent-zero conclusion is inferred from those rules rather than stated verbatim. If you want me to confirm the exact wording on the page, NEED_RAW: 4/68.)
