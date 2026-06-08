## Question 7 [theory]

> Can content that one document has deleted still be retrieved and shared as living content through any other document that continues to arrange it?

Yes. Deletion in Xanadu removes content from one document's *arrangement* (Vstream), but never from permanent storage (Istream). Any other document that continues to arrange that content keeps showing it as live, retrievable material.

## Why deletion doesn't destroy

DELETE is a Vstream operation, not an Istream destruction. Nelson explicitly marks "deleted bytes" as a valid state that survives:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, **may remain included in other versions**.)" [LM 4/9]

And he states the persistence-in-other-documents case directly:

> "Note that the owner of a document may delete bytes from the owner's current version, but **those bytes remain in all other documents where they have been included**." [LM 4/11]

So the bytes are "not currently addressable" *in the deleting document*, but they persist everywhere else that arranges them.

## Why the other document's copy is "living," not frozen

Transclusion is inclusion by reference, not copy. A document that windowed the content points at the original Istream bytes, not a detached duplicate:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Because non-native bytes are fetched from their home location and remain "as much a logical part of a document as native bytes" [LM 4/11], the transcluding document continues to deliver them as live content — still linkable, still part of the network. This is precisely what distinguishes a transclusion from a dead copy:

> "Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

## The underlying guarantee

This follows from the Istream/Vstream separation: content is permanent (Istream), arrangement is flexible (Vstream). A "delete" changes only the deleting document's Vstream mapping; the Istream content — and every other Vstream that references it — is untouched. Links also continue to resolve to the deleted bytes, since "links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them" [LM 4/42].

**In short:** retrieving and sharing the content through another arranging document is exactly what the system guarantees. The deletion is local to one document's view; the content remains living wherever else it is included, and remains recoverable even in the deleting document through historical backtrack.
