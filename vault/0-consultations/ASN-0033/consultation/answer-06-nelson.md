## Question 6 [nelson]

> Can links created within one node reference content held in a different node, and if so, must the target node participate in establishing that link?

## Yes — and no, the target node does not participate

Links can absolutely reference content on any node in the docuverse, and the target node plays no role in establishing the link. This falls out from several reinforcing design principles.

### Endsets reach across the entire docuverse

Nelson is explicit that link endpoints are not constrained to any single node or document:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." [LM 4/43]

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" [LM 4/45]

The tumbler address space is unified across all nodes. A link's endset is just a set of tumbler addresses — the system draws no distinction between "local" and "remote" addresses at the link-creation level.

### Link creation is a unilateral, local operation

The MAKELINK operation creates a link in a specified home document. Nelson notes:

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." [LM 4/63]

The home document determines ownership. The target documents — wherever they physically reside — are not consulted. This is reinforced by the ownership principle:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

### Published content cannot refuse incoming links

Authors who publish explicitly relinquish control over incoming links:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

If the target *author* cannot control incoming links, the target *node* certainly has no veto power either.

### You can even link to nodes where nothing exists

Ghost elements make the point most starkly:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

If you can link to an address where nothing is stored, you obviously don't need the target's participation — there may be no target to participate.

### The target node participates only at retrieval time

The target node becomes involved only when someone *follows* the link (content delivery) or *searches* for links pointing to content on that node. This is handled by BEBE:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space. This is done basically in two ways." [LM 4/70]

> "First, by the forwarding of requests as they fan out from users to servers able to supply." [LM 4/70]

Retrieval is when cross-node communication happens. Link *creation* is purely local to the home document's node. The contractual framework ensures that when retrieval does occur, the target vendor must cooperate:

> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors." [LM 5/14]

### Summary

Creating a link is a one-sided act. You write the link into your document at your address on your node. Its endsets specify tumbler addresses that may point to any node in the docuverse. The target node neither knows nor consents. The unified address space and the publication contract together guarantee that link creation requires no coordination — only link *traversal* requires inter-node communication.
