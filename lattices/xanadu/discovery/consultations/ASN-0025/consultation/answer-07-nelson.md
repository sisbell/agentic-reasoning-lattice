## Question 7 [nelson]

> If two users independently incorporate the same shared passage, must the system guarantee that both users' references resolve to the same address?

## Yes — this is architecturally guaranteed and definitionally required.

When two users both transclude the same passage from a source document, both references **must** resolve to the same I-space address. This is not an optional guarantee — it is the mechanism by which transclusion works at all.

### Why: COPY creates V-space mappings, not new I-space content

The COPY operation in FEBE does not duplicate bytes. It creates a new V-space reference to **existing** I-space content:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Both users' documents contain inclusions — V-space positions that map to the **same** I-space addresses in the source document. The bytes are fetched from their "home locations" at read time. There is only one home.

### The critical distinction: creation vs. transclusion

Content identity is based on **creation**, not **value**:

- If Alice and Bob independently **type** the same words, they get **different** I-addresses (different creation events, different home documents).
- If Alice and Bob both **COPY** (transclude) from the same source passage, they share the **same** I-addresses — because neither created new content; both referenced existing content.

This distinction is stated in the provenance design:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."

### Three system capabilities depend on this guarantee

**1. FINDDOCSCONTAINING** — Finding all documents that include a given passage requires shared I-addresses:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

If two transclusions of the same passage resolved to different addresses, this operation could not work.

**2. Correspondence** — Version comparison depends on shared I-space origin:

> "Correspondence is a RELATION — the relationship between V-space positions that share the same I-space origin."

Shared I-addresses are how the system knows two passages "correspond" without being told.

**3. Automatic royalty** — The original author gets paid whenever their bytes are delivered:

> "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43]

If transclusions created separate I-space content, the royalty would flow to the wrong owner (or to no one).

### Summary

The guarantee is absolute: both users' references resolve to the same I-space address because COPY is reference, not duplication. This is not a design choice that could go either way — it is the foundation on which transclusion, correspondence, discovery, and royalty all depend.
