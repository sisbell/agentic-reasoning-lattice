## Question 1 [theory]

> When content over a span is deleted, what is removed from the document's current arrangement and what must survive permanently in the content store?

When content over a span is deleted in Xanadu, the operation removes that content from the document's **Vstream** (its current arrangement) while the content itself survives permanently in the **Istream** (the content store / permascroll). DELETE does not mean what it means in conventional systems—it never destroys content.

## What Is Removed: The Vstream Mapping

The DELETEVSPAN operation removes the span from the document's current arrangement only. As the operations reference states:

> "DELETEVSPAN: This removes the given span from the given document." (4/66)

What this actually affects is the *arrangement*, not the stored bytes. The deleted content becomes "not currently addressable" in that document's present view. Nelson's diagram on 4/9 labels this state explicitly:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

The Vstream is dense and re-flows after the deletion—surrounding V-addresses close the gap—but the underlying content identity is untouched.

## What Must Survive Permanently: The Istream Content

The bytes themselves remain in Istream forever. This is the foundation of the non-destruction guarantee. From the i-space/v-space material:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

Crucially, deleted bytes persist not only for historical backtrack but for any other document that transcluded them:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

## What Survives the Delete

| Aspect | Affected by DELETE? |
|--------|---------------------|
| Vstream arrangement | **YES** — content removed from current view |
| Istream content | **NO** — bytes remain forever |
| Previous versions | **NO** — still contain the content |
| Transclusions | **NO** — other documents still show it |
| Links to content | **NO** — still resolve to Istream |

Because links attach to spans of bytes (via permanent Istream addresses) rather than positions, they survive deletion as long as any referenced bytes remain at each end:

> "A Xanadu link is not between points, but between spans of data... If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

## The Underlying Principle

This reflects Xanadu's append-only storage model, which rejects "destructive replacement":

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." (2/14)

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

Because the content survives, any prior arrangement can be reconstructed on demand:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)

**In summary:** deleting a span removes the Vstream mapping that places those bytes in the document's current arrangement; the bytes themselves must survive permanently in Istream so that historical backtrack works, transclusions in other documents remain intact, and links continue to resolve. `[LM 4/9, 4/11, 4/66, 2/14-2/15]`
