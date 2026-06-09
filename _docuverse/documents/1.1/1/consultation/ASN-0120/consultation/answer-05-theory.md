## Question 5 [theory]

> Once a link is created, must it be discoverable by search from every content region that any of its endsets references, regardless of where the link itself resides?

# Answer: Yes — link discoverability is by endset, independent of link residence

Nelson's design makes link search **endset-driven**, and the location where a link physically resides (its home document) is deliberately decoupled from what its endsets reference. A link is discoverable from any content region touched by any of its three endsets, no matter where the link itself lives.

## The two decoupled facts

**1. A link's home (residence) is independent of what it points to.**

From the documents concept (4/12):

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document."

So residence determines ownership, not discoverability.

**2. The system indexes links by all three endsets, enabling search from any direction.**

The three-endset-links design note states the guarantee directly:

> "**Structural bidirectional discovery.** The system indexes links by ALL three endsets. You can find links starting from any direction - what links FROM here, what links TO here, what links OF THIS TYPE."

And from the links concept: "Links are bidirectional in discovery. The system indexes links by all their endsets. You can search from any direction."

## The operation that proves it

`FINDLINKSFROMTOTHREE` lets you constrain the home-set, from-set, to-set, and three-set independently. Critically (4/63):

> "If the home-set is the whole docuverse, all links between these two elements are returned."

Setting the home-set to the whole docuverse means residence imposes no restriction — every link satisfying the endset criteria is returned regardless of where it lives. The satisfaction rule (4/58) is:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request."

Because the from-set, to-set, **and type-set** are all searchable endsets, a link is reachable from each of the content regions any of those endsets references. The type endset is searched the same way — by address, not content (4/44-4/45):

> "The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address."

## Why this matters to the design

This is the backlinks guarantee. A reader at any spot can ask "what connects here?" and find links authored and owned by anyone, anywhere:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'-- and be shown all these outside connections without appreciable delay." (publishing, 2/46)

And search remains efficient regardless of clutter (4/60):

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS."

## Summary

Yes. By intent, a link must be discoverable from every content region referenced by any of its endsets (from, to, or type), and the link's own residence is irrelevant to that discoverability — residence only fixes ownership. This is what makes Xanadu's "bidirectional discovery" and the solved-backlinks property work.

One nuance to flag: Nelson's guarantee is about *searchability* — that the link *can* be found via any endset when you query that region. Whether a given front end *displays* a particular link is a separate filtering/sieving concern ("sieving," 2/47), and the type endset is matched by address rather than stored content. But at the back-end retrieval level, the discoverability invariant holds across all endsets regardless of where the link resides.
