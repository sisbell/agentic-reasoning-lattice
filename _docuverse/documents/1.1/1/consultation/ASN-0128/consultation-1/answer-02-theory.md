## Question 2 [theory]

> In the design, is a link's identity tied to the document it lives in — i.e., are two links with identical endsets homed in different documents two distinct links, or the same assertion stated twice?

**Two distinct links.** In my design a link's identity is its tumbler address, and the home document is literally the prefix of that address. Two links with identical endsets, homed in different documents, are two separate connective units — owned by different parties, deletable separately, searchable separately, payable separately. The system has no notion of "the same assertion stated twice," because the back end does not model assertions; it models owned objects. Identity is positional and historical, never derived from endset content.

## The mechanics: home is part of the name

A link is stored in the 2-subspace of its home document, and its full address runs through node, account, document, and version:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

MAKELINK makes this explicit — you cannot create a link without naming where it will live, and every creation mints a fresh identity:

> "This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. It returns the id of the link made." [LM 4/68]

> "The document must be specified because that determines the actual residence of the link--since a document may contain a link between two other documents." [LM 4/63]

Note the consequence: distinctness doesn't even require different homes. Issue MAKELINK twice with identical endsets in the *same* document and you get links 2.1 and 2.2 — two units, in permanent order of arrival. The system never deduplicates by endset value. This parallels how bytes work: two authors who independently type the same sentence own different bytes at different I-addresses. Identity comes from the act of creation, not from content.

## Why I designed it this way

**The home carries ownership, and ownership is the point.**

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

If two structurally identical links were "the same link," whose would it be? Who could delete it? "Only the owner has a right to withdraw a document or change it" [LM 2/29] — and that applies to links as parts of documents. Your marginal note and my marginal note may say the same thing, but yours is yours and mine is mine.

**Identical structure, different authority.** The same three endsets asserted by different parties mean different things socially. I noted this for metalinks: "Note that the Author link can also be used from outside a document to claim that the author is really someone else." [LM 4/52]. The original author's supersession link is a declaration; a third party's identical supersession link is merely a claim to be evaluated. You evaluate it by checking *whose link it is* — which only works because the home individuates it. Collapse identical-endset links into one and you destroy the ability to ask "who said this?"

**Accounting requires it.** "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document." [LM 5/13]. Link deliveries are credited to the home document. Merged links would have no determinate cash register.

**Links are themselves linkable, so they must be individuated.** "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only." [LM 4/49]. If two identical-endset links were one object, a comment on *Bob's* link versus *Alice's* link could not be expressed.

## The search side: equivalence is computed, not stored

The query model confirms the plurality. The home-set is a fourth search dimension alongside the three endsets:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." [LM 4/69]

> "If the home-set is the whole docuverse, all links between these two elements are returned." [LM 4/63]

"All links between these two elements" — plural by design. The system expects many links connecting the same material, and FINDNUMOFLINKSFROMTOTHREE exists precisely to count them; a count is meaningless over deduplicated propositions but very meaningful over independent acts of connection (how many readers disputed this passage?). The Tumbler Square shows the same picture: "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." [LM 4/46] — home is one of the four faces of a link's existence, not incidental storage.

So: if a front end wishes to notice that two links are *equivalent in what they connect*, it may compute that from search results — that's a fine front-end function. But the back end never merges them. The docuverse is pluralistic. When two people independently draw the same connection, that is two facts about the literature, not one — and both deserve to survive, attributed, in their permanent order of arrival.
