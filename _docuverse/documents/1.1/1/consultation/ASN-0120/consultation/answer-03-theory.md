## Question 3 [theory]

> In which document does a newly created link reside, and must a link always have a home document just as ordinary content does?

A newly created link resides in the **home document specified at creation time** — the `<doc id>` argument to MAKELINK — and yes, every link must have a home document, just as all content must belong to a document.

## Where the link resides

When you create a link, you must name the document it lives in:

> "MAKELINK: This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. It returns the id of the link made." (4/68)

Nelson is explicit that the home document is the link's *residence*, and that this matters because a link's home need not be either endpoint:

> "The document must be specified because that determines the actual residence of the link--since a document may contain a link between two other documents." (4/63)

This residence is what establishes **ownership**. The home document tells you who owns the link, independent of what the link points at:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

So a link from document A to document B can have its home in document C (or A, or B) — and whoever owns the home document owns the link.

## Must a link always have a home?

Yes. Nelson's universal convention is that nothing exists outside a document — there are no free-floating materials:

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist. Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." (2/29)

The endset geometry reinforces this — a link is an object that sits at a home on one side of the "tumbler square," with its three endsets reaching out to the other sides:

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46)

Because the home document gives the link its tumbler address (the link instance addresses live in the document's `0.2.N` subspace — e.g. `N.0.U.0.D.V.0.2.1` for the first link), a link without a home would have no address and no owner. Like ordinary content, a link is therefore always part of some document.

## Summary

- A new link resides in the home document named in the MAKELINK call.
- That home need not be either document the link connects — it determines *residence and ownership*, not endpoints.
- Every link must have a home document, since "no free-floating materials exist" — links are first-class document contents just like bytes.
