## Question 1 [theory]

> What must the system guarantee about which content a link's endsets identify when the document being viewed is a different version than the one the link was originally attached to?

# What Endsets Must Identify Across Versions

The system must guarantee that endsets continue to identify **the same permanent bytes** (Istream content), not positions in any particular version's arrangement. This is the foundation that makes cross-version linking possible.

## The Core Guarantee

A link's endsets are anchored to bytes via permanent I-addresses, not to positions in the Vstream of the version where the link was made. When viewing a different version, the endsets identify whatever portion of those same bytes survives in that version.

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. **This also works for alternative versions in which part of each end has survived.**" (4/42)

## Refractive Following

Because shared Istream origin creates structural correspondence between versions, the system can trace endsets from the original version to corresponding locations in any other version:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. **Thus a link to one version of a Prismatic Document is a link to all versions.**" (2/26)

## What the Reader Experiences

The front end can present the link as if it were made against the version being viewed:

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." (2/43)

## The Survival Rule

The guarantee is conditional on byte survival, not byte stability of position:

- **If bytes from each endset survive in the viewed version**: the endset identifies that surviving content (possibly relocated, possibly partial)
- **If all bytes at one endset are absent from the viewed version**: the link does not apply to that version, but is not destroyed — it still applies to versions where the content remains

This is why deletion is non-destructive in Istream: a "deleted" passage may still exist in other versions, and links to it remain valid there.

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

## Why This Matters

The endsets do NOT identify "whatever is at position N in this version." They identify a specific identity of content. Two versions of a paragraph that look identical but were independently typed are NOT the same to a link — only shared Istream origin (transclusion ancestry or shared editing history) creates the correspondence the link can refractively follow.

For correspondence between independently-created equivalent passages, users must explicitly assert it with a counterpart link (4/53) — the system cannot infer it from content resemblance.
