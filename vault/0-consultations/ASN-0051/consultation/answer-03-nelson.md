## Question 3 [nelson]

> Must a link created against one version of a document remain meaningful when the document reaches a later version, or is a link bound to the version in which it was made?

## Links Are Not Bound to Their Version

A link made against one version of a document remains meaningful across all versions. This is not a secondary feature but a direct consequence of the architecture, and Nelson states the principle explicitly:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

### Why This Works: Istream Attachment

Links attach to **Istream addresses** (permanent content identity), not **Vstream addresses** (ephemeral arrangement positions). Since different versions of a document are different Vstream arrangements over shared Istream content, a link to specific bytes works wherever those bytes appear — in any version, past or future.

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

The link is a "strap between bytes." The bytes have permanent I-addresses. Versions rearrange which bytes appear and where, but the bytes themselves don't change identity. The strap holds.

### The Correspondence Mechanism

What makes cross-version link following possible is **correspondence** — the system's ability to identify which parts of different versions share the same Istream origin:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

The FEBE operation `SHOWRELATIONOF2VERSIONS` computes this:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

Correspondence is structural — it falls out of shared I-addresses, not from metadata or tracking. If two V-positions in different versions map to the same I-address, they correspond. The system can therefore trace a link from version 1 to the "same place" in version 5.

### The Supersession Case

Nelson explicitly addresses what happens when a document is updated and someone follows a link made to the old version:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

> "When a document is updated, a reader will ordinarily want to see the new version — but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version — if it's still there." [LM 2/43]

Note the caveat: "if it's still there." If the newer version deleted the bytes the link pointed to, there is no corresponding content to follow to. The link still resolves against the old version (which must remain on the network), but it cannot "reach through" to content that no longer exists in the new version.

### The Condition for Cross-Version Validity

A link remains meaningful across versions **if any of the bytes it references survive** in the target version. The condition is the same as for editing survivability:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

This applies across versions because versions are just different arrangements of the same content pool. The link doesn't know or care which version it's being resolved against — it only cares whether the referenced I-addresses appear in that version's V-stream.

### Summary

| Question | Answer |
|----------|--------|
| Is a link bound to its version? | **No.** |
| Can it follow to other versions? | **Yes**, via correspondence (shared I-addresses). |
| Does this require explicit action? | **No** — it's structural, computed from the addresses. |
| When does it fail? | When the linked bytes are absent from the target version. |
| Nelson's principle | "A link to one version is a link to all versions." [LM 2/26] |
