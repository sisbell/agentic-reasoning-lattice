## Question 6 [theory]

> When the same underlying content appears in multiple places within a single document, must a link's endset resolve to all such occurrences, or only the original?

# Endset Resolution Across Multiple Occurrences

**Short answer:** Yes — a link's endset resolves to all occurrences. The link is attached to the *bytes themselves*, not to a particular position. When the same content appears in multiple Vstream positions within a document (via inclusion/transclusion), all those positions are manifestations of the same Istream bytes, and the link reaches them all.

## The Architectural Basis

Links don't attach to positions — they attach to **bytes** with permanent Istream identity:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

The endset designates a set of bytes (identified by Istream address). When you transclude content into multiple places in your document, those places share the same Istream identity:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

## The Refractive Principle

I made this explicit for cross-version cases, and the same logic governs intra-document occurrences:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

The principle is content identity, not positional identity. A link to content X reaches X wherever X resides — across versions, across documents, or repeated within a single document. All these cases are structurally the same: the bytes have one Istream identity, and the link strap holds to those bytes.

## The Discovery Side

The system explicitly supports finding all occurrences of content through FINDDOCSCONTAINING, which returns *all* documents containing any portion of the specified material regardless of native location. The same machinery that finds cross-document occurrences finds intra-document repetitions — there is no architectural distinction between them.

## A Distinction Worth Making

The *endset* is the set of bytes. How a front end *displays* a link's targets — whether it highlights all occurrences, jumps to the first, or lets the user choose — is a presentation matter. But the underlying semantic relationship is unambiguous: the link attaches to content, and the content is wherever it appears.

This is precisely why links can survive editing. If a link only resolved to one positional occurrence, then duplicating the bytes (via COPY/transclusion) would create a distinction the system can't make — because at the Istream level, there *is* no distinction. The bytes are the bytes.

## What I Did Not Explicitly Address

I should be candid: in *Literary Machines*, I worked through this principle for the multi-version case (refractive following) and the multi-document case (FINDDOCSCONTAINING), but I do not address the within-single-document repetition case in so many words. The answer above is what follows necessarily from the design — bytes have unitary Istream identity; endsets bind to bytes; therefore endsets reach all manifestations of those bytes. But a reader looking for a passage where I say *exactly this* about *within-document* repetition won't find one.

NEED_RAW: 4/47, 4/49-4/51 — to confirm whether the link-to-link and Tumbler Square discussions add any explicit treatment of intra-document multiple occurrences that wasn't captured in the curated extracts.
