## Link Survival After Content "Deletion"

### The Central Architectural Point

The question contains a premise that Xanadu's architecture deliberately makes impossible: content is never truly deleted. What users call "deletion" is a V-space operation only — content is removed from the document's current arrangement but remains permanently in I-space.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Must the System Preserve the Link?

**Yes, unconditionally.** Two independent reasons guarantee this:

**First**, links point to I-space content, and I-space is permanent. V-space deletion cannot affect I-space:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Since I-space content is never destroyed, the bytes referenced by the link's endsets always exist. The link's survivability condition — "if anything is left at each end" [LM 4/43] — is permanently satisfied because the I-space content is permanently there.

**Second**, only the link's owner can delete a link — content deletion by the target document's owner cannot cause link deletion:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

Alice's deletion of content from her document cannot destroy Bob's link to that content. Bob's link lives at Bob's address, under Bob's ownership. The two operations — content deletion (V-space) and link deletion (ownership action) — are entirely independent.

### What Must the System Report?

Nelson does not specify exact front-end behavior for this scenario, but the architecture constrains what is possible and what must be true:

**The content is always retrievable.** The append-only storage guarantee means the I-space bytes are still there:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

**The front-end handles presentation.** Nelson explicitly places navigation decisions at the front-end layer:

> "None of these commands are to be seen by the user. The user's concerns are to be seen on the screen; the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." [LM 4/61]

**Version-following provides the model.** The closest scenario Nelson directly addresses is following a link to content in a superseded version:

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." [LM 2/43]

The phrase "if it's still there" acknowledges that content may not appear in the current version. The front-end's job is to navigate this gracefully — perhaps showing the content in its historical context, or noting that it has been removed from the current arrangement.

**Refractive following across versions applies.** Since deleted content still exists in prior versions:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

A link to content deleted from version N still resolves in version N-1 (where the content existed). The front-end can present the content from the version where it last appeared.

### Summary

| Question | Answer |
|----------|--------|
| Is the link preserved? | Yes — always. I-space content is permanent; only the link owner can delete the link. |
| Can the content be retrieved? | Yes — always. I-space content is never destroyed. |
| What is the system obligated to report? | Not specified at the front-end level, but the back-end must make the I-space content available. |
| What should the front-end do? | Nelson's model suggests: show the content from the version where it last appeared, offer to show historical context. |

### What Nelson Does NOT Specify

Nelson leaves unspecified the exact UX for "this link points to content removed from all current V-space arrangements." The architecture guarantees the content exists and is retrievable, but the presentation — whether to show it automatically, flag it as historically deleted, or offer a choice — is a front-end design decision. The back-end's obligation is to make the bytes available; the front-end's obligation is to present them intelligibly.

NEED_RAW: [4/9, 4/58-4/59] — to check whether the link search operations (FINDLINKSFROMTOTHREE) specify behavior when endset content has been removed from V-space, which would clarify whether the back-end filters or includes such links in search results.