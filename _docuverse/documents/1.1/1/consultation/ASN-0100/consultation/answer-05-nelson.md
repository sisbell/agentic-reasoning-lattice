## Question 5 [nelson]

> After insertion shifts existing content to later positions in the document stream, must every prior reference to that existing content — by its permanent identity, not by document position — still resolve to exactly the same bytes?

**Yes. Absolutely and unconditionally.**

This is the central architectural invariant of Xanadu. The entire Istream/Vstream separation exists to guarantee exactly this property.

## What INSERT affects

INSERT operates on **Vstream** — the document's current arrangement:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

V-addresses shift. That is their nature — they are ephemeral positions in the current view.

## What INSERT does not affect

INSERT does not touch **Istream** — the permanent identity space where content lives:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

Nelson is explicit: V-addresses "may be constantly changing" through editorial operations, but the permanent identity of the bytes — their I-addresses — is unaffected. The front end doesn't even see the I-addresses changing, because they don't.

## The design principle

The Istream is **append-only**:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content at an I-address never changes. New content gets new I-addresses. INSERT adds new bytes to Istream (the inserted text) and updates the Vstream mapping (shifting positions) — but every prior I-address resolves to exactly the same bytes it always did.

## Why this matters

This invariant is what makes link survivability possible:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Links reference I-addresses. INSERT shifts V-addresses. Therefore links are completely unaffected by insertion. The "strap between bytes" stays attached to the same bytes because those bytes' permanent identities have not changed — only their positions in the current document arrangement have shifted.

## Summary

The permanent identity of content (Istream address) is invariant under all editing operations — INSERT, DELETE, REARRANGE, COPY. This is not a feature bolted onto the system; it is the foundational architectural decision. Vstream is the view that changes; Istream is the identity that does not. Any reference by permanent identity resolves to the same bytes before and after insertion, unconditionally.
