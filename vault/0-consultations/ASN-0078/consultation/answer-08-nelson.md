## Question 8 [nelson]

> When two endsets of a link reference content in different documents owned by different users, who owns the link and what are the system's guarantees about each party's ability to discover it?

## Link Ownership Across Documents

### Who Owns the Link

**The link's home document determines ownership — not what the link points to.** This is one of the most explicitly stated principles in the link architecture:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

The MAKELINK operation makes this concrete:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>." [LM 4/68]

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." [LM 4/63]

So if User C creates a link in their Document Z, with the from-set pointing into User A's Document X and the to-set pointing into User B's Document Y — **User C owns the link**. Neither A nor B controls it. Only C can delete it.

### In-Links vs Out-Links

Nelson draws a sharp ownership boundary:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

User A and User B see the link as an **in-link** to their respective documents. They cannot control it. The link creator sees it as an **out-link** from their home document. They have full control.

### Discovery Guarantees

**Both parties (and everyone else) can discover the link.** The system indexes links by all three endsets, enabling bidirectional search:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

The FINDLINKSFROMTOTHREE operation searches by any combination of home-set, from-set, to-set, and type:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

> "If the home-set is the whole docuverse, all links between these two elements are returned." [LM 4/63]

And critically:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

So User A can query "what links touch my content?" and discover the link. User B can do the same. Neither needs the link creator's cooperation. Discovery is a system guarantee, not dependent on the link owner.

### The Asymmetry by Design

This creates a deliberate asymmetry:

| Capability | Link Owner (C) | Referenced Doc Owners (A, B) |
|---|---|---|
| Create the link | Yes | No (it's not their link) |
| Delete the link | Yes | No — can only delete content the link points to |
| Discover the link | Yes | Yes, via bidirectional search |
| Prevent the link | N/A | No — publication relinquishes this right |

The last point is crucial. Publishing a document contractually surrenders control over in-links:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

### The Only Recourse

If User A or B dislikes the link, their only structural recourse is to **delete the content the link points to** from their current version. Since links attach to spans of bytes, removing all referenced bytes at one end breaks the link. But the bytes still exist in Istream and in previous versions — so this is a Vstream-level action, not true destruction.

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

### Summary

The design separates **ownership** (who controls the link), **reference** (what the link connects), and **discovery** (who can find the link). Ownership lives with the creator. Reference crosses document and user boundaries freely. Discovery is universal and bidirectional. This is what makes the "socially self-constructing" literature Nelson envisions possible — anyone can annotate, connect, and comment on anyone else's published work, without permission and without modifying the target.
