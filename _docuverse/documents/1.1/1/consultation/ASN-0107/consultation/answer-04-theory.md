## Question 4 [theory]

> If two links share identical from, to, and type descriptions but were authored separately, must the count treat them as one or as two?

Two. The count must treat them as two distinct links.

## Why identity, not description, individuates links

A Xanadu link is a concrete, owned object with its own address — not a description that could collapse with an identical one. From the links source:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end..." (4/41)

Each link lives at its own home address, assigned in permanent order of arrival:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" ... "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Two separately authored links have different home documents (or at least different serial positions), hence different addresses. They are two objects that happen to describe the same three endsets — identical *content of description*, distinct *identity*.

## Why the count returns two

Counting (FINDNUMOFLINKSFROMTOTHREE) and the underlying search use a per-link satisfaction test, applied to each link independently:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

Both links independently satisfy the from/to/type criteria, so both are counted. The retrieval form makes the same point — it returns a *list of links*, enumerating each as a separate entry:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

> "If the home-set is the whole docuverse, all links between these two elements are returned." (4/63)

"All links" means every distinct link object, including duplicates-by-description.

## The deeper reason: type is matched by address, and links are owned

Nothing in the system deduplicates by endset value. Even the type endset is matched by *address*, never by inspecting stored content:

> "The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

And because links are owned property, merging two authors' separately-made links into one count would erase one author's link — contradicting the ownership guarantee:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

So if Alice and Bob each independently assert the same connection, the docuverse holds two links, each discoverable and attributable to its author, and the count reflects two — not one.

NEED_RAW: 4/58-4/60 (to confirm whether Nelson anywhere discusses duplicate-description links explicitly in the count/search discussion; the curated sources support the "two" answer but do not contain a passage addressing identical-description duplicates head-on).
