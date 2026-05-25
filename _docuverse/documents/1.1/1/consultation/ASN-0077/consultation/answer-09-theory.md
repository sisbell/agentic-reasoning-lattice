## Question 9 [theory]

> Does the design treat origin as a property of the content itself or as a property of the document containing it?

# Origin as Property of Content, Not Container

In Xanadu, **origin is a property of the content itself**, encoded structurally in the byte's permanent Istream address—not a property of the document that happens to contain it at any given moment.

## The Structural Encoding

Every byte has a permanent I-address of the form `Node.0.User.0.Document.0.Element`. The Document field encodes which document *originally created* that byte. This origin travels with the content forever, regardless of what other documents later transclude it.

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

## Why a Document Cannot Own Origin

Documents in Xanadu are arrangements (Vstream views) over content (Istream). A containing document holds *references* to bytes—it does not own them in any sense that could change their origin:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Non-native bytes are as much a logical part of a document as native bytes." [LM 4/11]

A document's contents may be a mixture of native bytes (born here) and inclusions (born elsewhere). The container does not redefine where its borrowed bytes came from.

## The User-Facing Guarantee

This structural property surfaces as a fundamental guarantee:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Note the precision: *any specific word or character*—not "of any document." Origin resolves at the byte level, not the container level.

## Why This Design Matters

If origin were a property of the containing document, copying content into a new document would relocate its origin—exactly the attribution failure Xanadu exists to prevent. By making origin structural to the byte (via I-address), the system makes attribution unstrippable:

- Transcluded content keeps pointing to its home document
- Copying within the system doesn't sever the link (the copy is a reference, not a duplicate)
- Royalties can flow to true authors automatically
- Two documents that independently created identical text have *different* I-addresses; transcluded content *shares* the I-address

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

## Summary

The document is a **container**; origin is **content-intrinsic**. The I-address—specifically its Document field—is the structural carrier of origin. A document containing content does not own that content's origin any more than a quoting paragraph owns the source it cites; it merely arranges references to bytes whose home is recorded permanently in their own addresses.
