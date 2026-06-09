## Question 9 [theory]

> What invariant must hold so that a link's residence is fully independent of the content it connects — that connecting two documents never forces the link to live inside either of them?

## The Invariant: Ownership and Application Are Independent

The invariant is that **a link's home document determines only who owns it, never what it connects** — and conversely, the content a link connects never determines where the link must reside. Nelson states this directly:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12, from `documents.md`)

The summary in `documents.md` crystallizes it: **"Ownership and application are independent."**

## Why This Holds: Universal Tumbler Addressing

For residence to be fully decoupled from connected content, links must be **first-class addressable objects in the same universal space as everything else**. A link references its endpoints purely by tumbler address, not by containment:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." (4/45, from `endsets.md`)

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" (4/45, from `endsets.md`)

Because a link has its *own* tumbler address (its home) and its endsets *map* to other addresses, the link's location is one fact and its connections are three separate facts:

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46, from `endsets.md`)

## The Operational Consequence

At creation time, residence is specified *separately* from the endsets — which is precisely why MAKELINK takes the home document as its own argument:

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." (4/63, from `operations.md`)

A single document can therefore be the home of a link whose from-set and to-set both point into entirely different documents. The link lives wherever its owner chooses; the content it connects lives wherever it already is.

## Summary

The invariant has two symmetric halves, both required:

1. **A link need not point into its home** — the connected content does not have to live where the link lives.
2. **A link need not reside in what it connects** — connecting two documents does not force the link into either of them.

Both are guaranteed by the same underlying fact: links are independently-addressed objects on the universal tumbler line, so *home address* and *endset addresses* are orthogonal coordinates. Ownership (home) and application (endsets) are independent (4/12).
