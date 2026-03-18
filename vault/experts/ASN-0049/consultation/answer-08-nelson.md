## Question 8 [nelson]

> Can shared content carry its own links, and if so, must those links remain active and visible in every document where that content appears?

# Can Shared Content Carry Its Own Links?

The short answer: content doesn't "carry" links in Xanadu. But through I-space identity, all links connected to shared content remain discoverable everywhere that content appears.

## Links Are Independent Objects

In Xanadu, links are not embedded in content. They are separate first-class objects stored in their own home documents:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

A document has **out-links** (links stored in it) and **in-links** (links stored elsewhere that point to it):

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it." [LM 2/31]

When you transclude content from document A into document B, document A's out-links do not become document B's out-links. They remain in document A.

## But I-Space Identity Makes Links Follow Content

Here is the critical architectural point. Links attach to **I-space addresses** (permanent content identity), not V-space positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

Transclusion preserves I-space identity — the transcluded bytes share the same permanent addresses as the original:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

So when someone creates a link pointing to bytes in document A, and those same bytes appear in document B via transclusion, a link search on those bytes finds the link **regardless of which document the reader is viewing**. The link doesn't travel with the content — the shared I-space address means the search finds the same results from either context.

The FINDLINKSFROMTOTHREE operation searches by I-space span constraints, not by document container. If the home-set is the whole docuverse, it finds all links connected to those bytes wherever they are stored.

## Links "Reach Through" Across Versions and Documents

Nelson explicitly describes this "reaching through" behavior for versions:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

And for prismatic documents generally:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

The mechanism is the same for transclusion: shared I-space origin means links resolve across document boundaries.

## Must They Be Visible?

Nelson says readers **must be able to discover** all connections:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

But **filtering is a front-end responsibility**:

> "This filtering by different attributes we call 'sieving', and it can only be set up for a comparatively small number of traits — say, location and author and time." [LM 2/47]

So the system guarantees **discoverability**, not mandatory display. The back end indexes all links bidirectionally. The front end decides which to show. A reader viewing transcluded content can always ask "what links connect here?" and get the full set — but the front end may filter by type, author, recency, or other criteria.

## Summary

| Question | Answer |
|----------|--------|
| Do links live inside content? | No — links are separate objects in their home documents |
| Does transclusion copy links? | No — nothing is copied; content is referenced |
| Are links discoverable on transcluded content? | Yes — shared I-space addresses mean searches find the same links |
| Must the front end show all links? | No — but it must be *able* to show them; filtering is the front end's job |
| Can links "reach through" to new contexts? | Yes — Nelson explicitly describes this for versions and transclusions |

The design is elegant: by making links point to permanent content identity (I-space) rather than ephemeral arrangement (V-space), and by making transclusion preserve that identity, links automatically follow content wherever it appears — without any special "link carrying" mechanism.
