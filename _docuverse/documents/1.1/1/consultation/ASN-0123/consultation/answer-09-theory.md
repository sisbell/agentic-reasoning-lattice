## Question 9 [theory]

> When the new version transcludes content to which links were anchored in the source, must those links carry through and remain followable from the version's context, and what guarantee secures that carry-through?

Yes. When a new version transcludes content to which links were anchored in the source, those links must carry through and remain followable from the version's context. This is not an incidental convenience — it is one of the load-bearing guarantees of the whole design. Let me be precise about *why* it holds and *what* secures it, distinguishing the structural guarantee from its user-facing realization.

## The principle: a link to one version is a link to all versions

The intent is stated directly:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

That last sentence is definitional, not aspirational. A link is *not* the property of a single arrangement. Because a new version is built by transclusion — `CREATENEWVERSION` "creates a new document with the contents of document <doc id>" [LM 4/66] — the version does not *copy* the source's bytes; it *shares* them. The transcluded content carries the same Istream identity it had in the source. And links anchor to that identity.

## What secures the carry-through: spans bound to immutable Istream

The deepest guarantee is that a link is fastened to *bytes*, not to *positions*:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. **This also works for alternative versions in which part of each end has survived.**" [LM 4/42]

I wrote that final clause deliberately. Survivability was never just about insert/delete inside one document — it was about versions. When the new version transcludes the anchored content, the bytes at the link's end *have survived* (they are present in the version, sharing their home location). The strap therefore stays fastened.

The reason this works is the separation of content from arrangement. The link's endset points at the byte's permanent home, not at where it currently sits in any reading order:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

So the chain is: links bind to Istream addresses → transclusion preserves Istream addresses → the version contains the very bytes the link grips → the link is still gripping them. The carry-through is structural and automatic, not a feature that must be re-established per version.

## Why I made this a *must*, not a *may*

The obligation runs the other way too — link carry-through is the reason a superseded version cannot be discarded:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

"Reach through" is exactly your phrase "carry through." Other people's links — which they own, at their own addresses — depend on this reaching-through. That dependency is why permanence is obligatory rather than optional.

## The condition, and the back-end / front-end division of labor

There is one honest condition, and it is the one stated at 4/42: carry-through holds "in which part of each end has survived." Since you stipulate that the version transcludes the anchored content, the anchored end *does* survive, so the condition is met. (If the content at an end were *not* carried into the version and existed nowhere, there would be nothing left to grip — but transclusion is precisely what keeps it gripped.)

Distinguish two layers, because "followable from the version's context" touches both:

- **Back end (the guarantee):** The link remains indexed against the Istream addresses the version now contains. A reader in the version who asks "what connects here?" [LM 2/46] resolves that context to its home addresses and is handed the link. This is guaranteed and automatic.
- **Front end (the realization):** Presenting the traversal so the reader lands on the corresponding passage *within the version they are reading* is the front end's job:

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." [LM 2/43]

Note "if it's still there" — that caveat is just the survivability condition restated in user terms.

## Summary

- **Must they carry through and stay followable?** Yes — refractively, by the rule that "a link to one version of a Prismatic Document is a link to all versions" [LM 2/26].
- **What secures it?** A single underlying guarantee with two faces: (1) links are *straps between bytes*, anchored to immutable Istream addresses rather than to positions [LM 4/42, 4/30]; and (2) transclusion — which is what creating a new version *is* [LM 4/66] — preserves those Istream addresses [LM 4/11], so the version contains the same bytes the link already grips. Survivability ("if anything is left at each end," [LM 4/42]) is therefore satisfied by construction, and the front end "reaches through" to present the link in the version's context [LM 2/43].

In short: I did not design links to live in documents. I designed them to live on *content*, in a permanent address space that versions share by reference. Carry-through is then unavoidable — which is the point.
