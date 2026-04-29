## Question 5 [nelson]

> When a new version of a document is created, must content retained from the prior version keep its original address, or may versioning introduce new addresses for the same material?

## Answer: Retained Content Must Keep Its Original I-Space Addresses

This is not a design choice left to implementors — it is architecturally required. The entire Xanadu model collapses without it.

### The Direct Evidence

CREATENEWVERSION is described as:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The new document gets a **new document address** (with ancestry encoded in the tumbler), but its content — its V-space — maps to the **same I-space bytes** as the original. The operation creates a new arrangement, not new content.

This is confirmed by the COPY operation, which explicitly shares I-addresses:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

COPY is transclusion — inclusion by reference to existing I-space content. CREATENEWVERSION is effectively a COPY of the entire document's content into a new document shell.

### Why This Is Required, Not Optional

**1. Correspondence depends on it.**

Correspondence — the ability to identify which parts of two versions are the same — is defined as a structural relation based on shared I-space origin:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

SHOWRELATIONOF2VERSIONS:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

If versioning introduced new I-addresses for retained material, this operation would have **nothing to match on**. The system identifies corresponding parts by finding V-space positions in different versions that map to the same I-space addresses. No shared I-addresses means no correspondence, which means no version comparison.

**2. Content identity is based on origin, not value.**

Two documents with identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address. This is how the system distinguishes "wrote the same words independently" from "quoted from the original." If versioning created new I-addresses, the system would lose the provenance chain — it could no longer tell whether version 2 retained content from version 1 or merely happened to contain the same words.

**3. Non-destruction requires it.**

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Versions share I-space content. Deleting from one version's V-space does not affect other versions because they all reference the same permanent I-space bytes. If each version had its own I-space copy, this guarantee would require a completely different (and far more complex) mechanism.

**4. The append-only model implies it.**

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is written once to I-space and never duplicated. Each version is a different V-space arrangement over the same I-space content. Only genuinely **new** content (insertions, additions) gets new I-space addresses.

**5. Refractive link following requires it.**

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

A link made to version 1 "reaches through" to version 2 because both versions' V-spaces map to the same I-space bytes. The link targets I-space; the system traces which V-space positions in any version correspond to those I-space addresses. Without shared I-addresses, refractive following would be impossible.

### Summary

When CREATENEWVERSION is called:

| What gets a new address | What keeps its original address |
|---|---|
| The document itself (new tumbler with ancestry) | All retained content (same I-space bytes) |
| New V-space arrangement | I-space addresses of every retained byte |

The new version is a **new view** (V-space) over **existing content** (I-space). Only content that is genuinely new — inserted or appended after versioning — receives fresh I-space addresses. Everything retained from the prior version keeps its original address. This is not an optimization; it is the mechanism by which correspondence, attribution, link survivability, and version comparison all function.
