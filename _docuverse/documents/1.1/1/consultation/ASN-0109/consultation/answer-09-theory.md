## Question 9 [theory]

> Must reading a link's endsets be permitted even when the content at those endpoints has been edited, deleted, or made inaccessible to the reader?

## Short Answer

For two of the three cases — **edited** and **deleted** content — yes: reading a link's endsets must remain possible, and this falls directly out of Xanadu's architecture. For the third case — content **made inaccessible to the reader** by privacy/access control — Nelson does not explicitly resolve whether endset-reading is gated, and I flag that below.

The crucial distinction throughout is that **reading an endset returns addresses, not content.** `RETRIEVEENDSETS` "returns a list of all link end-sets that are in <spec set>" (4/70) — it hands back the from-set and to-set as address structures on the tumbler line, not the bytes living at those addresses. So endset-reading and content-retrieval are separate acts, and the accessibility of the content does not, by itself, determine whether the endset addresses can be read.

## Case 1: Content has been edited

Reading endsets must remain permitted, because editing cannot invalidate them. Editing changes a document's **Vstream** arrangement, while links attach to **Istream** addresses, which are permanent:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

The endset addresses point at content identity, not position, so editing leaves them intact (see `link-survivability.md`). The endsets remain readable.

## Case 2: Content has been deleted

Deletion in Xanadu is Vstream removal, not Istream destruction. Deleted bytes persist and remain addressable:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

A link survives "deletions, insertions and rearrangements, **if anything is left at each end**" (4/43). The endset addresses continue to map to permanent Istream locations even after the content is removed from a current version. Indeed, the system tolerates endsets pointing at addresses where *nothing at all* is stored — the ghost-element principle:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

> "What the 'type' designation points to is completely arbitrary... The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

Since the link mechanism operates on addresses regardless of whether content is present there, deletion of the endpoint content cannot prevent reading the endsets.

## Case 3: Content made inaccessible to the reader (privacy/access control)

This is the genuinely unsettled case. The previous two are about *content existence* (and Istream permanence guarantees endset addresses outlive content changes). This case is about *content permission* — e.g., an endset pointing into a private document the reader may not view.

Two architectural facts pull toward "endsets remain readable":

1. Reading endsets returns addresses, not content, so it does not require the reader to access the protected bytes.
2. The link is owned by its **home document**, not by the documents it points into: "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12) The endset structure is the link-owner's property.

But there is a countervailing concern Nelson does not address in the curated material: an endset address pointing into a private document still *reveals that an address exists and that something is linked there*, which leaks structural information about private content. Nelson's privacy commitment is firm but explicitly hard to guarantee — "The network will not, may not monitor what is read or what is written in private documents. But these matters are not easy to guarantee." (2/59) — and the access model is only specified as binary (private = owner and designees; published = everyone), with private documents noted as **not even implemented** in XU.87.1 (4/79). Whether endset-reading bypasses or respects private-document access control is not stated.

NEED_RAW: 2/41-2/48, 4/55-4/60, 4/61-4/64 — to check whether Nelson conditions `RETRIEVEENDSETS` or link-search results on access rights to the endpoint documents, and whether endset visibility for links touching private content is specified.

## Summary

- **Edited content:** Endsets must remain readable — link survivability + Vstream/Istream separation guarantee it (4/42-4/43).
- **Deleted content:** Endsets must remain readable — deleted bytes persist in Istream (4/9), links survive "if anything is left at each end" (4/43), and endsets work by address even with nothing stored there (4/45).
- **Inaccessible-to-reader content:** Architecturally, endset-reading is an address operation distinct from content retrieval, which *suggests* it should remain permitted — but Nelson does not explicitly resolve the privacy interaction, so this part is inference, not a stated guarantee.
