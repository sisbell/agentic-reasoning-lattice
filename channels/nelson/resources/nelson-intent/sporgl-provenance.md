# Content Provenance

Source: Literary Machines 4/10-4/11

## Terminology

**The term "sporgl" does NOT appear in Literary Machines.** It is an implementation term from udanax-green (Span + Orgl). Nelson's corresponding concepts:
- "Virtual byte stream"
- "Inclusions" or "virtual copies"
- "Native bytes" vs "bytes native elsewhere"

## What It Means

A document's content comes from two sources: bytes created natively in the document, and bytes included from other documents (transclusions). For any content in the docuverse, you can determine where it originated.

Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. This is how the system distinguishes "wrote the same words" from "quoted from the original."

## User Guarantee

- For any content, you can determine its permanent I-address (identity)
- You can determine which document originally created it
- You can find all documents that contain it (via transclusion)
- Attribution is automatic and permanent

## Principle Served

Attribution through identity. Because I-addresses track content origin, the system always knows where content came from. This enables automatic attribution, royalty tracking, finding all uses of content, and version comparison.

## Nelson's Words

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Non-native bytes are as much a logical part of a document as native bytes." (4/11)
