## Question 2 [theory]

> What is the design difference between the set that bounds where a link resides and the sets that bound what its endpoints reference, and why must residence be treated separately from endpoints?

## The Two Kinds of Bounding Sets

A Xanadu link is described by **four** span-sets, which fall into two categories serving fundamentally different purposes:

**1. The home-set — bounds residence.** This is *where the link lives* and, by extension, *who owns it*. In the FEBE operation `MAKELINK`, "The document must be specified because that determines the actual residence of the link" (4/63). In link search (`FINDLINKSFROMTOTHREE`), the home-set is "where desired links are to be found."

**2. The three endsets — bound the endpoints.** The from-set, to-set, and three-set (type) bound *what the link references*. Each "may be an arbitrary collection of spans, pointing anywhere in the docuverse" (4/43). A link "has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to'" (4/42), plus a type endset that categorizes it.

Nelson's "Tumbler Square" visualization captures the asymmetry: "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46) Residence sits on one side; the three references map outward to the other three.

## Why Residence Must Be Separate from Endpoints

The decisive statement is from 4/12:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

Several design guarantees depend on this separation:

**Ownership independence.** A link "is owned by a user" (4/41), and ownership is fixed by *where the link resides*, not by *what it touches*. The endpoints can reach into documents owned by other people. If residence were conflated with the endpoints, you could only link content you already own — destroying the ability to comment on, cite, or annotate others' work. Because the home is distinct, "your link lives at your address" while pointing into someone else's published document (`links.md`).

**A document can hold links between two other documents.** As `MAKELINK` notes, residence must be named explicitly "since a document may contain a link between two other documents" (4/63). The link's home need not be either endpoint.

**Independent searchability.** The search model treats the four sets as orthogonal constraints. `FINDLINKSFROMTOTHREE` "returns a list of all links which are (1) in `<home set>`, (2) from all or any part of `<from set>`, and (3) to all or any part of `<to set>` and `<three set>`" (4/69). You can constrain *who owns / where it resides* separately from *what it connects*. Critically: "If the home-set is the whole docuverse, all links between these two elements are returned" (4/63) — i.e., you can ask for *all* links between two passages regardless of who made them, precisely because residence is a separate axis.

**Different permanence behavior.** Endpoints attach to bytes that move under editing — links "survive editing" because they hold to spans, not positions (4/42). Residence, by contrast, is stable: a link "is owned by a user" and keeps its creation-order address permanently in its home document. The two sets evolve under different rules, which only works if they are modeled separately.

## Summary

| Set | Bounds | Determines | Mutability |
|-----|--------|-----------|------------|
| **home-set** | residence | ownership; where the link is found | fixed, permanent order of arrival |
| **from / to / three** | endpoints | what is connected and how it's typed | follow the bytes; survive editing |

Residence answers *whose link is this and where does it live*; the endsets answer *what does it connect*. Nelson keeps them separate because ownership, permanence, and the freedom to link into content you don't own all collapse if a link can only reside where it points — and his own rule makes the independence explicit: the home "indicates who owns it, and not what it points to" (4/12).
