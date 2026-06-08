## Question 3 [theory]

> Must the content already in the document remain immutable through an insertion, such that nothing existing is altered and only the document's arrangement of positions changes?

Yes. Under Nelson's model, an insertion never alters existing content — it only changes the document's arrangement (the Vstream), while the underlying content (Istream) is immutable.

## The mechanism

INSERT operates by adding content and shifting *positions*, not by modifying any existing bytes. From the operation definition:

> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

Note precisely what changes: the **v-stream addresses** of following characters increase. The characters themselves are untouched — only their position in the current arrangement shifts.

## Why existing content is immutable

This follows from the Istream/Vstream separation. Content lives permanently in Istream at immutable addresses; the document is a Vstream arrangement (a view) over that content:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

The byte's *Vstream* position may change with editing, but its *Istream* identity never does. Insertion adds new bytes to Istream and re-maps Vstream positions; it does not rewrite or destroy anything already present.

## Consequence for links

The immutability of existing content is exactly why links survive insertion. Because links attach to bytes (via Istream identity), not to positions:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

And the survivability guarantee explicitly lists insertion:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

## Summary

An insertion changes only the document's arrangement of positions — the Vstream mapping. Existing content is immutable: nothing already in the document is altered, no bytes are rewritten or destroyed, and the only effect on prior content is that its Vstream addresses shift to accommodate the new material. This is a direct consequence of the principle that content (Istream) is permanent while arrangement (Vstream) is flexible.
