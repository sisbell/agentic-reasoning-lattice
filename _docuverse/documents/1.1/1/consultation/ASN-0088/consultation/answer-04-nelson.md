## Question 4 [nelson]

> If the same content appears in multiple documents through sharing, must a query against one appearance discover links attached to every other appearance of that identical content?

# Yes — This Is a Structural Consequence, Not an Optional Feature

The answer is an unqualified **yes**. A query against any appearance of shared content must discover links attached to every other appearance. This falls directly out of three architectural properties that Nelson specifies:

## 1. Links Attach to I-Addresses, Not V-Positions

Links are "straps between bytes" — they bind to content identity (Istream addresses), not to positions in any particular document's arrangement (Vstream):

> "A Xanadu link is not between points, but between spans of data." [LM 4/42]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

The endsets of a link map to the universal tumbler line — the Istream address space:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

## 2. Transclusion Shares I-Addresses

When content is transcluded (via the COPY operation), the new document's Vstream maps to the **same** Istream addresses as the original. No new bytes are created:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The included bytes have the same I-addresses in every document where they appear. Content identity is based on origin, not on which document currently displays it.

## 3. Link Search Operates on I-Address Ranges

FINDLINKSFROMTOTHREE searches by constraining endsets against span ranges on the tumbler line:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

These constraints are I-address ranges. A link satisfies the search if its endsets overlap the specified ranges:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

## The Consequence

If content at I-address range [X, X+100] appears in Document A (natively) and Document B (via transclusion), and a link's endset points to [X, X+50], then:

- Querying from Document A finds the link (the I-addresses match)
- Querying from Document B finds the **same** link (the I-addresses are **identical** — they are the same bytes)

The query doesn't ask "what links to this document?" It asks "what links to these bytes?" The bytes are the same bytes regardless of which document's arrangement you're viewing them through.

Nelson provides a dedicated operation that makes this explicit:

> "FINDDOCSCONTAINING: This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

The phrase "regardless of where the native copies are located" confirms that content identity transcends document boundaries.

## The Critical Distinction

This applies **only to structurally shared content** — content that shares I-addresses through transclusion. Two authors who independently type "to be or not to be" create content at **different** I-addresses. Their content is identical in value but distinct in identity. Links to one do not appear on the other.

This is by design. As Nelson's architecture dictates: identity comes from origin (which document created the bytes), not from value (what the bytes happen to say).

## Why This Matters

This property is what makes the "two-way reading" guarantee work:

> "It must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/40]

If links did not follow content across transclusions, a reader viewing a passage in a compound document would see a different set of connections than a reader viewing the same passage in its home document. The web of literature would fragment at every transclusion boundary. Nelson's entire vision of interconnected literature depends on links following content, not positions.
