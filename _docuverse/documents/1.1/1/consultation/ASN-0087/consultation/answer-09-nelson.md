## Question 9 [nelson]

> Must the system guarantee that creating a link has no effect whatsoever on the content it references — that the referenced content remains byte-identical before and after link creation?

## Yes — Link Creation Cannot Affect Referenced Content

This is guaranteed by multiple independent architectural principles, all of which converge on the same answer.

### 1. Links Live in the Creator's Document, Not the Target

Links are stored in their **home document**, which belongs to the link's creator — not in the documents they reference.

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

In-links — links created by others that point INTO your document — are stored elsewhere and are not under your control. They are also not part of your document's contents. They have no mechanism by which to alter your content.

### 2. Istream Content Is Immutable

Content at an Istream address never changes after creation. Links reference I-addresses. There is nothing a link can do to modify what lives at those addresses.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The Istream is append-only. New bytes are added; existing bytes are never altered. A link is a separate object stored at its own address — it references I-addresses but cannot write to them.

### 3. Only the Owner Can Modify a Document

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

If link creation modified the target document, then anyone linking to your published work would be modifying your document — a direct violation of the ownership guarantee. The architecture forbids this.

### 4. MAKELINK Operates on the Home Document

The MAKELINK operation specifies a home document for the link, not a target document:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>. It returns the id of the link made." [LM 4/68]

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." [LM 4/63]

The `<doc id>` is where the link is *stored*. The `<from set>` and `<to set>` are addresses that *reference* content — they do not write to it.

### 5. Links Are a Separate Layer

Nelson describes links as existing alongside content, not modifying it:

> "The Xanadu link is a meta-virtual structure connecting parts of documents (which are themselves virtual structures)." [LM 4/41]

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." [LM 4/41]

Documents and links are the two kinds of things. Links connect documents; they do not alter them.

### Summary

The guarantee follows necessarily from the architecture:

| Principle | Why it prevents modification |
|-----------|------------------------------|
| Link home ≠ link target | Link storage is in the creator's space, not the target's |
| Istream immutability | Referenced bytes cannot be altered after creation |
| Owner-only modification | Non-owners cannot change a document; linking is a non-owner action on the target |
| MAKELINK semantics | The operation writes to the home document only |
| Separate layer | Links are meta-structures over content, not modifications to content |

Nelson never needed to state this guarantee as a standalone principle because it is an inevitable consequence of the architecture. A system where links could modify their targets would violate ownership, break Istream immutability, and collapse the distinction between content and connection that is fundamental to the entire design.
