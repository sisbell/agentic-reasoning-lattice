## Question 1 [theory]

> When the system is asked to deliver the actual content named by a set of spans, what exactly must come back — the bytes of content themselves, or some description of where they live?

The actual bytes of content must come back — not a description of where they live.

## The answer: RETRIEVEV delivers content fragments

Nelson is explicit that exactly one command in the protocol is responsible for delivering real content, and it returns the material itself:

> "This returns the material (text and links) determined by `<spec set>`." (4/67) — RETRIEVEV

And critically, Nelson singles this command out from all the others:

> "Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments." (4/61)

So when you hand the system a spec-set (a set of spans) and ask it to deliver what those spans name, RETRIEVEV returns the **bytes of content** — the text and links themselves — not addresses, not pointers, not a manifest of locations.

## The contrast that makes this clear

The reason Nelson bothers to flag RETRIEVEV as "the only one" is that nearly every *other* retrieval-style command returns descriptions of *where* things are, not the things themselves:

- **FINDDOCSCONTAINING** — "returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (4/63) → returns *locations* (document IDs), not content.
- **RETRIEVEDOCVSPAN** — "returns a span determining the origin and extent of the V-stream of document `<doc id>`." (4/68) → returns an *address/extent*, not content.
- **FINDLINKSFROMTOTHREE** — "returns a list of all links which are..." (4/69) → returns link *identities*, not their byte content.

These commands traffic in tumbler addresses and spans — descriptions of where content lives. Only RETRIEVEV crosses the line from naming to delivering.

## Why this separation matters

This reflects the Istream/Vstream design. A spec-set names content by its position; resolving that name to actual bytes may require fetching from home locations:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

So delivering the bytes named by a span-set can mean the back end pulls non-native (transcluded) bytes from wherever they actually live — but what comes *back* to the requester is the resolved content itself, "as much a logical part of a document as native bytes" (4/11). The whole point of the part-pounce model is that "THE PART YOU WANT COMES WHEN YOU ASK FOR IT" (2/16) — materialized as actual content, not a forwarding address.

## Summary

The bytes of content themselves must come back. RETRIEVEV is the single command "concerned with delivery of the actual content fragments" (4/61), and it "returns the material (text and links)" (4/67). The span-set is the *name* of what you want; RETRIEVEV is what turns that name into delivered bytes. Every other command that takes spans returns descriptions of *where* content lives — only RETRIEVEV returns the content.
