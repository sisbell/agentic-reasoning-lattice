## Question 8 [nelson]

> What preconditions must hold before a node is permitted to enter — must all nodes it references already exist, or can forward references be admitted?

## Forward References Are Explicitly Admitted

Nelson's architecture imposes **no precondition that referenced nodes must already exist**. The system is designed from the ground up to permit references to addresses where nothing is stored. This is not an edge case or oversight — it is a named, deliberate design feature called **ghost elements**.

### Ghost Elements: The Definitive Statement

From Literary Machines 4/23:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

This is unambiguous: you can create a link whose endset points to an address that has no stored content. The link is valid. The address is valid. The referenced entity simply doesn't exist yet (or may never exist).

### The Span Guarantee Reinforces This

Spans — the fundamental unit for referencing content — are explicitly designed to tolerate emptiness:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

A span is not a count of items. It designates a region of tumbler-space. Whether that region is populated is orthogonal to whether the span is valid.

### Link Types Depend on Forward References

The link type system is built on ghost elements as a core design pattern, not an exception:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

Link types are matched by **address**, not by content. An address can designate a type even if nothing is ever stored there. This means the system's type taxonomy itself operates through forward (or permanently vacant) references.

### The Docuverse Is Sparse by Design

Only two kinds of entities are actually stored: content bytes and links. Everything else — servers, accounts, documents — are positions on the tumbler line with no corresponding stored object:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." [LM 4/23]

> "The docuverse is the occupied tumbler-space--as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

The address space is conceptually infinite and mostly empty. Requiring pre-existence of referenced nodes would contradict the fundamental architecture.

### Why This Must Be So

The forking mechanism makes pre-existence requirements impractical. Addresses are created by subdivision — the owner of address 2 can create 2.1, 2.2, 2.3 at will [LM 4/20]. In a decentralized system with no central coordinator, there is no way to atomically verify that a target address is populated before creating a reference to it. Nelson's design sidesteps this entirely: **all addresses are valid; population is optional.**

### Summary

No preconditions on referenced node existence. The architecture admits forward references, permanently vacant references, and references to the entire unpopulated subtree beneath any address. Ghost elements are the mechanism; address-based (not content-based) resolution is the principle.
