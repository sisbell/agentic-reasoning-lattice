## Question 2 [theory]

> What relationship must the positions that shift to make room bear to the content they were binding before the insertion — does displacing a position preserve the binding between that position and its prior content?

## Short answer

No. Displacing a position does **not** preserve a binding between that position and the content it formerly held — because in Xanadu a V-stream position never *binds* content in the first place. A V-address is an ephemeral ordinal slot, not a container that carries its contents along when it shifts. What actually persists through an insertion is the binding between the *bytes* and their permanent **I-addresses**. The bytes keep their identity; the positions are simply re-labeled around them.

## Why

When content is inserted, Nelson's spec says the positions of following content shift:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

Notice what shifts: the *characters' addresses* increase. The content that was at V-position N is now at V-position N+k. The position N has not "moved with" its old content — the content moved to a new position number. So the old content is no longer bound to position N; position N now denotes whatever sits there in the new arrangement.

This is possible precisely because the durable binding is content-to-I-address, not content-to-V-position. The V-stream is just the current arrangement, and it is explicitly allowed to be relabeled by editing:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

Links and identity therefore attach to bytes (their I-addresses), not to the slots they occupy:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." (4/42)

## The precise distinction

- **What is *not* preserved:** the relation `V-position N ↦ content X`. After an insertion, N may map to different content, and X has moved to a new V-position. Position-to-content is deliberately *not* invariant.
- **What *is* preserved:** the relation `content X ↦ I-address`. The bytes keep their permanent identity, and anything anchored to that identity (links, transclusions, correspondence) stays attached.

So the shifting positions bear no obligation to their prior content. The invariant runs the other way: the content retains its identity, and the V-stream re-coordinates itself around it. This is exactly the Istream/Vstream separation — "Separation of identity from arrangement" (v-space-addresses.md) — that lets editing be non-destructive and lets links survive insertions.
