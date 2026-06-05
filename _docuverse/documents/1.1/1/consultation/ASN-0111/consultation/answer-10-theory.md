## Question 10 [theory]

> Is a link a first-class document in its own right, such that reading it shares the same permanence guarantees as reading content?

# Is a Link a First-Class Document?

Short answer: A link is a **first-class object** in the docuverse — it has its own permanent address, an owner, and can itself be linked to — and it shares the same permanence and delivery guarantees as content. But Nelson does not treat an *individual link* as a standalone "document." Links are elements that live within a **home document**, and a *set* of links can constitute a separate document.

## Links are first-class objects with their own addresses

Nelson is explicit that links are not embedded markup but independent, addressable, owned units:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." (4/41)

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." (4/41)

Because they live in the universal tumbler-space, links have permanent addresses and can even be the *targets* of other links:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link." (4/49)

Link addresses occupy a document's `2.x` subspace and, unlike bytes, keep their creation-order addresses permanently:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

## But a link is an element *within* a document, not itself a document

That last quote is the key distinction. A link is *homed* in a document; it does not float free:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

Nelson's "everything is a document" convention applies to *collections* of links, not to a single link:

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist. Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." (2/29)

So the unit that rises to "document" status is a *set* of links (which has its own owner and address), while an individual link is an addressable element residing in a home document.

## Reading a link carries the same permanence guarantees as reading content

On the dimension your question targets — permanence — links and bytes are treated symmetrically:

**1. Links survive editing**, attaching to spans rather than positions:

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

**2. Deleted links persist in Istream**, exactly as deleted bytes do. Nelson's technical-contents diagram lists "DELETED LINKS" as a valid state parallel to "DELETED BYTES":

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

**3. Links are delivered and accounted like content.** The per-byte royalty/cash-register mechanism counts link delivery alongside byte delivery (per the enforcement model, the cash register "increments whenever bytes or links are delivered out of the document," 5/13), and RETRIEVEENDSETS retrieves a link's endsets just as RETRIEVEV retrieves bytes (4/70).

## Conclusion

A link is a genuine first-class citizen of the docuverse: permanently addressed, owned, retrievable, royalty-bearing, survivable across edits, and itself link-able. In all the ways that matter for *permanence*, reading a link enjoys the same guarantees as reading content. What it is *not* is a self-standing "document" — it is an element homed in a document, though a *set* of links does qualify as a separate document under Nelson's convention (2/29).

One caveat: the symmetry of the *royalty/delivery* accounting for links versus bytes rests on the enforcement-model summary (5/13) rather than a verified verbatim quote about reading links specifically. If you need that exact wording confirmed: NEED_RAW: 5/13.
