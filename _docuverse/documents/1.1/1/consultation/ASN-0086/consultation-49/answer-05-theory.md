## Question 5 [theory]

> Was the sibling-frontier emission pattern intended as a substrate-level invariant of link allocation, or as an implementation choice on top of a broader address-emission primitive?

# Sibling-Frontier Emission: Substrate Invariant or Implementation Choice?

The sibling-frontier emission pattern, as you frame it, conflates two distinct levels in my design. Let me separate them.

## What IS substrate-level

What I committed to as invariant is **permanence + order-of-arrival** for link addresses, not a specific allocation shape:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

The example addresses I gave illustrate this:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)"
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" [LM 4/31]

These are the canonical depth-1 sibling-frontier addresses — but they illustrate the principle of arrival-ordered, permanent allocation, not a mandate on shape.

## What is implementation choice

I was explicit that further subdivision of the link space is left open to implementors:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

That sentence is the load-bearing one for your question. I deliberately did not foreclose deeper or non-sibling-frontier allocation. Several uses had been discussed; none were specified.

## The broader primitive

The general address-emission primitive — of which sibling-frontier link allocation is one specialization — is owner-controlled forking, applied uniformly across tumbler-space:

> "Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

The crucial phrase is **"on whatever basis the owners choose."** Allocation policy is delegated to owners; the substrate guarantees only that whatever is baptized stays permanent and that the addressing arithmetic works regardless.

## Direct answer

Sibling-frontier emission for links is **the canonical implementation of a broader address-emission primitive (owner-controlled forking)**, not a substrate-level invariant in itself. What is substrate-level is:

1. Link addresses are permanent (the general tumbler permanence guarantee, [LM 4/19]).
2. Link addresses reflect order of arrival ([LM 4/31]).
3. The owner of an address controls baptism of sub-addresses under it ([LM 4/17, 4/20]).

The fact that the diagrammed pattern is "depth-1 sibling under `0.2`, monotonically increasing" is the simplest specialization satisfying those three invariants. I named alternative subdivisions as open at [LM 4/31] precisely because I did not intend to fix the shape.

If your implementation needs deeper subdivision for link facets, sub-typing, or other "uses … discussed," that is within the spirit of the spec, provided permanence and order-of-arrival are preserved.
