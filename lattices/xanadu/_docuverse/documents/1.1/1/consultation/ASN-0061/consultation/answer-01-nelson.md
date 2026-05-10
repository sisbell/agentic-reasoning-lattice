## Question 1 [nelson]

> When content is removed from a position in a document, does the content itself continue to exist in the system's permanent storage, or can deletion ever destroy content?

# Deletion Never Destroys Content

The answer is absolute: **deletion in Xanadu removes content from a document's current arrangement but never destroys the content itself.** This is not a policy choice — it is architectural. The system is built so that destruction of content is impossible by design.

## The Two Address Spaces

The key is the separation between Istream (permanent storage) and Vstream (current arrangement). When you "delete," you are modifying the Vstream — removing a mapping — while the Istream content remains untouched.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The Istream is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

## Nelson's Explicit Diagram

The diagram on page 4/9 shows "DELETED BYTES" as a named system state with this annotation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" — not gone. "Awaiting historical backtrack" — recoverable. "May remain included in other versions" — still visible elsewhere.

## What Deletion Affects and Does Not Affect

The owner's delete operation changes the Vstream mapping only:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This means:

| Aspect | Affected by DELETE? |
|--------|---------------------|
| Vstream arrangement (current view) | **Yes** — content removed |
| Istream content (permanent storage) | **No** — bytes remain forever |
| Previous versions | **No** — still contain the content |
| Transclusions in other documents | **No** — still show it |
| Links pointing to the content | **No** — still resolve to Istream |

## Why This Must Be So

This is not cautious engineering. It flows from the fundamental rejection of destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

The storage system preserves every state so that any previous arrangement can be reconstructed:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

And modifications to content — including deletion — must never damage what others depend on:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

## The Deeper Point

Deletion that destroys content would violate nearly every guarantee the system makes: permanence of addresses, historical backtrack, link survivability, transclusion integrity, and the rights of others who have linked to or transcluded that content. If I delete a paragraph from my essay, and you had transcluded that paragraph into your commentary, your document must not break. The paragraph still exists at its Istream address; my document simply no longer includes it in its current arrangement.

This is what I meant by calling the storage system a **hyperfile** [LM 2/22] — a structure where safety and backtrack are not separate problems bolted on after the fact, but emerge naturally from the architecture itself.
