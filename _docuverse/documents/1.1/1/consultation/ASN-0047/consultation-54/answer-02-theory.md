## Question 2 [theory]

> How does the design conceive of content vs. link subspace allocation under a document — are they separate allocator structures established at document creation outside the usual inc-based hierarchy, or extensions of a single per-document allocator?

Bytes and links are subspaces within a single per-document address tree, not separate allocator structures. Under each version V, the tumbler forks at the element level into two conventional branches: `V.0.1.N` for byte positions and `V.0.2.N` for links [LM 4/30-4/31].

Both branches arise from the same forking mechanism I designed for the whole docuverse. The owner controls the allocation of numbers under any owned node [LM 4/20]; the byte and link branches are simply two such children of the version node. They differ in *convention*, not in mechanism:

**Byte subspace.** "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address" [LM 4/30]. These positions may shift under editorial operations, "but since the links are to the bytes themselves, any links to those bytes remain stably attached to them" [LM 4/30].

**Link subspace.** Addresses are sequential by arrival and permanent: "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" and "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" [LM 4/31]. "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document" [LM 4/31].

I did not conceive the link subspace as a structure stood up at document creation outside the inc-based hierarchy. It is the inc-based hierarchy — one more fork in the universal address tree. And I left room for it to be subdivided further by the same mechanism: "the subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed" [LM 4/31].

So: one universal allocation principle (baptism by the owner under any owned node), producing two structurally distinct subspaces under each version, each with its own convention for what the next digit means — positional and rearrangeable for bytes, serial and permanent for links.

NEED_RAW: 4/30-4/31 (raw pages 197-198) for the full surrounding discussion of element-field structure, in case I described the subspace conventions there in language that bears directly on the "separate vs. single allocator" framing.
