## Question 9 [nelson]

> Does a node impose any visibility boundary on its content, or is all content within every node universally addressable across the entire docuverse?

## No Visibility Boundary at the Node Level

A node imposes **no visibility boundary** on its content. All published content within every node is universally addressable across the entire docuverse. The node field in a tumbler address indicates *where* content is physically stored, not *who* can see it.

### The Unified Space Guarantee

BEBE exists precisely to eliminate node boundaries from the user's perspective:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space."
> — [LM 4/70]

Each server maintains a model of the whole, not just its own contents:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network."
> — [LM 4/72]

The user experience is explicitly one of location transparency:

> "Perhaps the most important thing, and certainly the hardest part to believe, is that everything on such a network-- any subset, substructure or grouping-- can come to the user immediately, even as the aggregation grows to tremendous size."
> — [LM 2/57]

### Visibility Is Per-Document, Not Per-Node

The access control boundary is the **document**, not the server. A document is either private (owner and designees only) or published (everyone):

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone."
> — [LM 2/42]

A node could contain a mix of private and published documents. The node itself has no "wall" around it.

### Vendors Must Honor Cross-Node Requests

The contractual structure makes this explicit. Storage Vendors are obligated to serve content to users on other vendors' servers:

> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors, and accept material for storage from other Xanadu-licensed vendors within the network."
> — [LM 5/14]

A vendor cannot refuse to serve its published content to outside users. That would break the unified docuverse.

### The Node Address Is Routing, Not Scoping

Tumblers encode the node purely as a storage/routing mechanism:

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document."
> — [LM 4/17-4/18]

The node field tells the network *where to find* the content. Ghost elements reinforce this — you can link to a node address and reach everything beneath it:

> "A link to or search of an account or node will find any of the documents under it."
> — [LM 4/23]

### Summary

The docuverse is one space, not a federation of walled nodes. Nodes are storage locations within that space. The only visibility boundary Nelson specifies is the document-level private/published distinction — and that boundary is orthogonal to which node stores the document.
