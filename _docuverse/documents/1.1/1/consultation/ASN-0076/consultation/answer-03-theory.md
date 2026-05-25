## Question 3 [theory]

> Must every document or link that referenced the original link continue to resolve to the unchanged original after an edit occurs?

# Must references continue to resolve to the unchanged original after an edit?

**Yes.** The unchanged original must remain resolvable. This is structural, not optional — it follows from the separation of Istream (permanent content) and Vstream (current arrangement), and it is what makes links survive editing in the first place.

## The Mechanism: Links Attach to Bytes, Not Positions

A link does not point to a position in a document — it points to the bytes themselves, via their permanent Istream addresses. Editing changes the Vstream arrangement, not the underlying content identity:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

## Edits Do Not Destroy

"Deletion" in Xanadu does not remove bytes from Istream. The diagram on page 4/9 explicitly marks deleted bytes as a valid state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And crucially for cross-document references:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So an edit by the owner cannot break references held by other documents — those references continue to resolve to the original content.

## Published Documents Cannot Be Withdrawn

The permanence obligation is explicit. Once others have linked into a document, the original must remain:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

## The Reader's Choice: Original vs. Refraction

The original is *always* available, but a reader (via their front-end) may choose to follow a link forward into a newer version:

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." [LM 2/43]

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

## Time-Fixed vs. Location-Fixed Inclusions

For transclusions specifically, the author chooses the semantics:

> "A quotation--an inclusion window--may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

## Summary

| Aspect | Guarantee |
|--------|-----------|
| Original Istream content | Permanent — never destroyed by editing |
| Old versions | Must remain on the network |
| Links to original | Continue to resolve to the unchanged bytes |
| Transclusions in other documents | Unaffected by owner's edits |
| Reader behavior | May choose to refract forward to newer versions, but the original remains accessible |

The system **must** preserve the unchanged original — that is the bedrock guarantee. What it *additionally* allows is the option to navigate from old to new via correspondence and refractive following, but this is reader-elective navigation layered on top of the permanence guarantee, not a replacement for it.
