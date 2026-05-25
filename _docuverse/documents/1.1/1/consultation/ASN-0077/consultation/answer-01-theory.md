## Question 1 [theory]

> What must the system guarantee about a span's ability to identify the document where its content originated?

# What the System Must Guarantee About a Span's Origin Identification

The system must guarantee that **a span's content origin is structurally identifiable from the address itself**—not as metadata that can be stripped, but as an inherent property of how content is addressed.

## The Core Guarantee

For any span anywhere in the docuverse, the system must allow you to determine which document originally created its content. This is non-negotiable and absolute:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is the guarantee. Every byte traces back. Period.

## Why It Is Structural, Not Metadata

The Istream address (a tumbler) directly encodes origin through its Document field:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

The four-field structure—`Node.0.User.0.Document.0.Element`—means the Document field of any byte's I-address IS the identifier of its origin. A span, being defined by its tumbler boundaries, carries this origin information in the addresses themselves.

This is fundamentally different from attribution-as-metadata. In conventional systems, a citation or author field is a property attached to content that can be copied without the attribution. In my system, the fetching mechanism itself requires the home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

## Spans That Cross Documents (Transclusion)

When a span appears in a compound document but its content was created elsewhere, the system must still identify the true origin:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The Vstream position is local to the containing document, but the Istream address—which the system must preserve—points back to the home document. A transcluded span is NOT a copy; it is a reference whose origin is permanently traceable.

## What This Guarantee Enables

This guarantee is the foundation for several user-facing promises:

1. **Attribution**: Authors get credit automatically because every byte's origin is structural
2. **Royalties**: The system knows whom to pay because the I-address tells it
3. **Verification**: Readers can check sources by following the address back
4. **Integrity of the docuverse**: The web of literature cannot be broken by copying within the system

## What Implementations Must Preserve

Any implementation claiming to be Xanadu must guarantee:

- A span's Istream addresses (not just its Vstream positions) are always retrievable
- The Document field of those I-addresses correctly identifies the originating document
- Operations within the system (copy, transclusion, version creation, rearrangement) cannot sever this connection
- The home document can be reached by following the address—the bytes are obtained "by front-end or back-end requests to their home locations" [LM 4/11]

The deepest principle: **origin is identity**. Two documents with identical text written independently have different I-addresses; the same text quoted from a source has a shared I-address. The system distinguishes "wrote the same words" from "quoted from the original" because origin is built into the address structure itself.

This is what makes literature in my system different from literature in a file system. In a file system, copying severs origin. In Xanadu, origin is conserved as a law of the system.
