## Question 8 [nelson]

> Must two links that connect the same two spans of content be distinguishable as separate objects, or does the system treat identical connections as a single link?

## Two Links, Same Spans: Always Distinct Objects

Yes, two links connecting the same spans are always distinguishable as separate objects. The architecture makes this unavoidable — and intentional.

### Every link gets a unique address

Links occupy the `0.2.N` subspace of their home document, addressed sequentially by creation order:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

Each call to MAKELINK produces a new link with a new sequential address:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>. It returns the id of the link made." [LM 4/68]

There is no "find-or-create" — MAKELINK always creates and always returns a fresh ID.

### Identity comes from home address, not endsets

A link's identity is its tumbler address, not what it connects:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

Two links with identical from-sets, to-sets, and type endsets are still distinct objects if they have different home addresses. Even two links in the *same* home document with identical endsets would get different sequential positions (`0.2.5` vs `0.2.6`).

### Link search returns all matches

FINDLINKSFROMTOTHREE returns "a list of all links" satisfying the search criteria [LM 4/69]. If two identical-endset links exist, both appear in results. There is no collapsing.

### Why this matters

Each link is an independent assertion of connection, owned by its creator:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

If Alice and Bob both create a comment link from paragraph P to annotation Q, those are two separate owned objects — different home documents, different owners, independently deletable, independently targetable by link-to-link. Merging them would violate ownership semantics.

Even if the *same* user creates two links with identical endsets (perhaps with different type endsets, or even the same type), they remain distinct. Nothing in the specification suggests deduplication, uniqueness constraints, or identity-by-endset. The system is explicitly designed for open-ended, unrestricted link creation — the only constraint is ownership of the home document.
