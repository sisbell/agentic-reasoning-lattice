## Question 7 [nelson]

> Can the owner of a document remove content that was originally created by a different author, and if so, does the original author's identity remain attached to that content elsewhere in the system?

## Yes — and the original author's identity is permanently preserved

### The owner can remove transcluded content from their document

The document owner has absolute editorial control over their V-space arrangement. Since transclusion places another author's content into the owner's V-stream, the owner can DELETE that content — meaning remove it from their document's current view.

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

DELETE is a V-space operation. It changes the document's arrangement, not the underlying content:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And critically:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### The original author's identity is structurally permanent

This is where Xanadu's I-space/V-space separation does its deepest work. The original author's identity is encoded in the **I-address itself** — it is not metadata that can be stripped but part of the address structure:

```
Node.0.User.0.Document.0.Element
```

The **User** and **Document** fields permanently record who created the content and in which document. This address never changes regardless of what any other document owner does with their V-space.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

### What survives the deletion

When document owner Alice removes Bob's transcluded content from her document:

| Aspect | Affected? |
|--------|-----------|
| Alice's current V-stream | Yes — content no longer appears |
| Bob's original document | No — completely untouched |
| I-space content | No — bytes remain at Bob's permanent I-address |
| Previous versions of Alice's document | No — still contain the transclusion |
| Other documents transcluding the same content | No — still show it |
| Links pointing to Bob's I-address | No — still resolve |
| Bob's royalty entitlement | No — any future delivery of those bytes still pays Bob |

### The deeper principle

Nelson designed the system so that **no editorial operation by anyone can sever attribution**. Because transclusion is inclusion by reference (not copy), and because I-addresses encode origin permanently, the connection between content and creator is an invariant of the system — not a convention that participants must honor but a structural property that cannot be violated from within the architecture.

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

The content lives at Bob's I-address forever. Alice's deletion merely says "I no longer wish to show this in my arrangement." It says nothing about Bob's content, Bob's identity, or anyone else's use of that content.
