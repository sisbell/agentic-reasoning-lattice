# Origin Traceability

Source: Literary Machines, 2/40, 4/11, 4/26-4/30

## What It Means

Origin traceability is the guarantee that you can always determine where any piece of content came from. This is not metadata that can be stripped - it is structural, encoded in the address itself.

Every byte in Xanadu has a permanent Istream address - a tumbler with the form:

```
Node.0.User.0.Document.0.Element
```

The **Document field** directly encodes which document originally created that byte. When you see content anywhere in the docuverse - even transcluded into a compound document - you can examine its I-address and immediately determine:

1. **Which server** it lives on (Node field)
2. **Which user/account** owns it (User field)
3. **Which document** it was born in (Document field)
4. **Which element** within that document (Element field)

## Why This Is Structural, Not Metadata

In conventional systems, attribution is a property attached to content - an author field, a copyright notice, a citation. These can be copied without the attribution, stripped, or falsified.

In Xanadu, the origin IS the address. To fetch the content, the system must request it from its home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

When you transclude content, you do not copy it - you include a reference to its permanent I-address. The content is fetched from its home. The connection cannot be severed because the fetching mechanism requires it.

## User Guarantee

**You can always ascertain the home document of any content.**

More specifically:
- Every byte traces back to its original document
- Windowed (transcluded) content maintains connection to source
- Attribution cannot be severed by operations within the system
- The Document field of the I-address is the proof of origin

## Principle Served

Origin traceability preserves the web of intellectual connection that makes literature meaningful. When you quote someone, when you build upon their work, when you critique them - the connection to the source MUST be preserved.

In the paper world, quotation marks and citations serve this purpose imperfectly - they can be stripped, falsified, or simply omitted. In Xanadu, the connection is inherent in the address structure itself.

This serves:
1. **Attribution**: Authors get credit automatically
2. **Royalties**: The system knows whom to pay
3. **Verification**: Readers can check sources
4. **Integrity**: The web of literature remains intact

## How Users Experience It

When viewing a compound document that includes content from multiple sources:
- Each piece is visually identifiable as coming from somewhere
- Clicking or querying reveals the home document instantly
- The path through transclusions is always traceable
- You can always say "Show me the original context"

> "This world nevertheless remains simple in design. The virtuality is simple in structure and regular in layout. You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

## Nelson's Words

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." (4/26)

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

Note: The last quote clarifies that the V-address (position in current arrangement) may change, but the I-address (permanent identity including home document) never changes.
