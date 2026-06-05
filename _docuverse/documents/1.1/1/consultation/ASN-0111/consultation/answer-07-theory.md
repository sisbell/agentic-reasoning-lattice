## Question 7 [theory]

> What invariant ensures that the endsets a link reports actually correspond to existing content regions?

## The Invariant: Span-Based Attachment + Istream Permanence

The invariant is **link survivability**: a Xanadu link attaches to *spans of bytes* (identified by their permanent Istream addresses), not to positions, and it remains valid exactly as long as bytes remain at each end. Because content is never destroyed in Istream, the regions an endset references continue to exist.

### Why links attach to content, not positions

Nelson's foundational design choice is that links bind to bytes:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

The survivability annotation states the invariant directly:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" (4/43)

This conditional — *if anything is left at each end* — is the invariant. A link's endsets correspond to existing content precisely because the link persists only while some referenced bytes survive.

### Why the referenced content always exists

The endsets point into **Istream** (permanent storage), and Istream content is never destroyed. "Deletion" is a Vstream-only operation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

So even editing that removes content from a document's current arrangement does not invalidate a link's endset — the bytes still exist at their permanent I-addresses. This is why endsets reliably correspond to real content regions.

### Important caveat: the type endset is exempt

The invariant applies to the **from-set and to-set**, which point to actual bytes. The **type endset (three-set)** is deliberately *not* required to correspond to stored content:

> "What the 'type' designation points to is completely arbitrary... The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

So the guarantee that "endsets correspond to existing content regions" is a property of the connective endsets (from/to), not the categorizing type endset.

### Summary

| Mechanism | Role in the invariant |
|-----------|----------------------|
| Span-based attachment (4/42) | Links bind to bytes, so they track content rather than positions |
| Survivability condition (4/43) | Link persists iff bytes remain at each end |
| Istream permanence (4/9, 4/11) | Deletion is Vstream-only; referenced bytes never vanish |
| Ghost-element exemption (4/45) | Type endset may point to nothing — the invariant covers from/to only |

The invariant, in one line: **a link's connective endsets reference Istream byte-spans, and the link survives only while bytes remain at each end — and since Istream never destroys content, those regions continue to exist.**
