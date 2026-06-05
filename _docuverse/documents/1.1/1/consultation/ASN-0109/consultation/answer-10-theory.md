## Question 10 [theory]

> What must the read reveal about the type or meaning of the relationship the link records, beyond merely naming its endpoints?

The read must reveal the link's **type** — its third endset (the "three-set"). Naming the endpoints requires only the from-set and to-set; what *kind* of relationship those endpoints stand in is a separate, third component that the read must surface.

## The from/to pair names endpoints; the type names the relationship

A Xanadu link is a three-way structure, not a two-way one:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" (4/42)

The from-set and to-set establish *what* is connected. But that alone is mute about meaning — note Nelson's parenthetical that what "from" and "to" mean "depend on the specific case." The disambiguator is the type:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

So beyond naming endpoints, a read must reveal this type endset, because that is where the relationship's meaning lives. Without it, a citation, a comment, a refutation, and a counterpart link are structurally identical — same two endpoints, different significance. As the curated `three-endset-links` source puts it: "The from-set and to-set establish WHAT is connected. The third endset (type) establishes WHAT KIND of connection it is."

## What "type" carries — and how it is read

Crucially, the type is read as an **address**, not as stored content:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44–4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

So what the read must reveal about the relationship's meaning is the *type endset's address(es)* — which may be several pointers, and may point to "ghost elements" where nothing is stored. The meaning is carried by the identity of the address (matched by convention/agreement), not by dereferencing it.

Because types are open-ended, this is also how a read distinguishes user-defined relationships:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." (4/43)

## In protocol terms

The operation that retrieves a link's connective information is **RETRIEVEENDSETS** — "This returns a list of all link end-sets that are in <spec set>." (4/70). A complete read of a link therefore returns all three endsets, and it is the third (the type / three-set) that records the relationship's category — e.g., whether it is a Comment Link, Counterpart Link, Quote-Link, Citation Link, or Suggested-Threading Link (from the type listings at 4/52–4/55), as well as any user-defined type.

## Summary

Beyond naming endpoints (from-set, to-set), the read must reveal the **type endset** — the third endset that records *what kind* of relationship the link asserts. It is symmetrical with the other endsets, points anywhere in the docuverse (even to ghost addresses), and is interpreted by its address rather than its contents. That third endset is precisely the part of a link that carries meaning rather than mere connection.
