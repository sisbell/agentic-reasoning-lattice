## Question 1 [theory]

> Does Nelson's link model intend that no link address ever be a prefix of another — i.e., is the flat-link-domain property a designed semantic constraint, or an emergent consequence of the allocator's implementation?

The flat-link-domain property is **emergent from the allocator, not a designed semantic constraint**.

The current implementation (XU.87.1) assigns link addresses sequentially by arrival order within a document:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

So `N.0.U.0.D.V.0.2.1`, `2.2`, `2.755` are siblings on the 2.x subspace — none is a prefix of another. The flat domain emerges because the sequential allocator never subdivides an existing link address.

But I explicitly left the door open:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

If link `2.5` were ever subdivided into `2.5.1`, `2.5.2`, then `2.5` would be a prefix of `2.5.1`. This is consistent with the general tumbler principle of forking ("baptism"): any owned address may designate sub-addresses by adding digits to the right. Links live in tumbler-space alongside everything else, and tumbler-space is universally subdivisible. The flat-link-domain is therefore an artifact of the allocator, not a semantic invariant of the model.

The link-to-link mechanism reinforces this. To point at a link, you use "the actual link address in the tumbler line, with a span of 1 to designate that unit only" [LM 4/49]. The "span of 1" convention is needed precisely because a link address is a position in a subdivisible space — you have to be explicit when you mean only the link itself, not anything that might hang below it.

**Practical implication:** treat flatness as a property of the present allocator, not an invariant of the architecture. Code that relies on "no link address is a prefix of another" will break the day sub-link addressing is turned on, and I designed the address space to permit that day.
