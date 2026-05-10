## Question 2 [nelson]

> If a document includes shared content from another document, must the origin of that content always be traceable back to the document where it was first created?

# Yes — Origin Traceability Is Structural and Absolute

This is one of the most fundamental guarantees of the entire system. The origin of shared content is **always** traceable to the document where it was first created, and this traceability **cannot be severed** by any operation within the system.

## The Mechanism: I-Space Addresses

Every byte ever created in Xanadu receives a permanent I-Space address — a tumbler of the form:

```
Node.0.User.0.Document.0.Element
```

The **Document field** directly encodes which document originally created that byte. This is not metadata attached to content — it IS the address. To fetch the content at all, the system must request it from its home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When you transclude content into your document, you do not copy it. You create a V-space reference to the same I-space address. The fetching mechanism itself requires knowing the origin.

## The User-Facing Guarantee

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is stated as a permanent structural property — not a feature that might be turned off, but a consequence of how the system works.

## Why This Cannot Be Severed

Content identity in Xanadu is based on **creation**, not value. Two documents containing identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address as the original. This is how the system distinguishes "wrote the same words independently" from "quoted from the original."

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The inclusion is structurally a reference to the original's I-address. The connection is the address itself — there is no way to "strip" it without destroying the reference entirely.

## The Layered Glass Metaphor

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

No matter how many layers deep the transclusion goes, each layer is transparent — you can always trace through to the original source. The glass panes don't obscure origin; they preserve it.

## What This Serves

Origin traceability is load-bearing for several other guarantees:

- **Attribution**: Authors get credit automatically because the system knows whose I-space the bytes live in
- **Royalties**: The system knows whom to pay because the Document field identifies the owner
- **Non-destruction**: Others can build upon your work "without damaging the originals" [LM 2/45] precisely because they reference your content rather than copying it
- **Verification**: Readers can always say "Show me what this originally was" and follow the reference back

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

## Summary

Yes — not merely "must" but "necessarily." The system is designed so that traceability is not a policy but a structural consequence of the addressing scheme. The I-address of every byte encodes its origin document. Transclusion works by referencing that address. The origin cannot be hidden, stripped, or falsified within the system because it is the address itself.
