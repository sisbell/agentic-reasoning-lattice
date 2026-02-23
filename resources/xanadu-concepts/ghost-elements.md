# Ghost Elements

Source: Literary Machines, page 4/23 (raw 190)

## Semantic Intent

### What It Means

Ghost elements are addressable positions in tumbler-space that don't correspond to any stored object - they exist conceptually but have no physical representation in storage. The docuverse contains many more addresses than it contains actual data.

In Xanadu, only content bytes and links are actually stored. Everything else - servers, accounts, documents - are just positions on the tumbler line. A document address represents a location in the addressing scheme, not a stored "document object." The document itself is the collection of content stored under that address.

This is a profound architectural insight: the address space is populated by concepts, not objects. You can address a document that exists only as a potential container. You can address an account that has never stored anything. The addressing system is an abstract coordinate space, and storage fills in selected points within that space.

### User Guarantee

**You can link to any address, whether or not anything is stored there.** A link to an account or server node will find all documents under that address. The system doesn't require stored objects to exist before you can reference their position in the address hierarchy.

### Principle Served

Ghost elements enable several important capabilities:

- **Forward references**: You can create links to addresses before content is placed there
- **Hierarchical queries**: A link to an account address implicitly references all content beneath it
- **Sparse storage**: Only actual content needs storage; the address space itself costs nothing
- **Clean separation**: Addressing is purely conceptual; storage is purely operational

This separation allows the docuverse to be conceptually infinite while storage remains finite.

### How Users Experience It

- Links to a user account will find any document they create
- Links to a server node will find any account and document on that server
- You don't need to "create" a document before referencing its address
- Searches can target conceptual positions, not just stored objects
- The address hierarchy implies containment without requiring container objects

### Nelson's Words

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." (4/23)

> "The docuverse is the occupied tumbler-space--as occupied by conceptually assigned positions, even if nothing represents them in storage." (4/23)

> "Thus the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage. Consider what we may call 'ghost elements'." (4/23)

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

> "A link to or search of an account or node will find any of the documents under it." (4/23)
