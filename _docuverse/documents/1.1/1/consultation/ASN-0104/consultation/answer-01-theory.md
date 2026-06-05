## Question 1 [theory]

> When a fragment is requested by its address, what exactly must the system return — the content itself, or a reference to it?

## What the System Returns: Content, Not a Reference

When you request a fragment **by RETRIEVEV** — the one operation concerned with content delivery — the system returns **the actual content itself**, not a reference to it. But the design depends crucially on a *separation* between operations that hand back content and operations that hand back addresses.

### RETRIEVEV delivers actual content

Nelson is explicit that content delivery is isolated into a single command:

> "Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments." (4/61)

And what RETRIEVEV returns:

> "This returns the material (text and links) determined by `<spec set>`." (4/67)

So when you pounce on a fragment by its address, you get the material — the bytes themselves.

### The content materializes on demand ("part-pounce")

This delivery is not a pre-assembled blob; the fragment is *constructed when you ask for it*. Nelson calls this **pounce**:

> "When you 'go to' a certain part of a document, the whole document is not ready to show; yet the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." (2/16)

> "We call this pounce. You pounce like a cat on a given thing, and it seems to be there, having been constructed while you are, as it were, in midair." (2/16)

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." (2/16)

So the answer to "content or reference?" is: **content** — but content assembled on the fly from the underlying fragments.

### Why this isn't a contradiction with transclusion

Here is the subtlety. A document's Vstream may include **non-native bytes** (transclusions) that physically live in another document. From the *requesting front end's* perspective, those bytes still come back as content — their remote origin is invisible:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." (4/11)

The reference-following happens *internally*, on the back end's side:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

In other words, addresses point to permanent Istream locations (references under the hood), but the act of *retrieving* resolves those references and delivers the actual bytes to the user. The front end "is unaware of this" address-resolution (4/11).

### The contrast: most operations return references, only RETRIEVEV returns content

This is the clearest way to answer your question. Nearly every *other* FEBE operation hands back **references/addresses**, not content:

- `RETRIEVEDOCVSPAN` — "returns a span determining the origin and extent of the V-stream" (4/68) — a reference
- `RETRIEVEENDSETS` — "returns a list of all link end-sets" (4/70) — references
- `FINDDOCSCONTAINING` — "returns a list of all documents containing any portion of the material" (4/70) — references
- `FINDLINKSFROMTOTHREE` — returns "a list of all links" (4/69) — references

Only **RETRIEVEV** crosses the line into delivering actual content (4/61).

## Summary

When a fragment is requested by its address via RETRIEVEV, the system **returns the content itself** — materialized on demand from its stored fragments (part-pounce). The *addresses* (tumblers/spans) are permanent references that the system resolves internally, including following transclusion references to remote home locations, but what reaches the user is the actual material. The architecture deliberately confines content delivery to that one operation, while every other retrieval operation returns references (spans, link IDs, document lists) rather than content.
