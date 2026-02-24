# Consultation Answers — Version Semantics

**Inquiry:** What does creating a new version preserve and establish? What is the version fork model — how do versions relate to each other and to shared content?
**Date:** 2026-02-23 21:03
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When a user creates a new version of a document, must the new version initially contain exactly the same content as the original, or only the text content without the links?

### Nelson's Answer

## CREATENEWVERSION: Text Content Only, Not Links

Nelson's specification, combined with his document model, indicates that the new version contains **only the text content** — not the links.

### The Direct Specification

The operation description is terse:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The key word is **"contents."** Nelson explicitly distinguishes contents from links in his document model:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents." [LM 2/31]

"Contents" and "out-links" are separate components. CREATENEWVERSION copies the "contents" — meaning the text/byte content — not the out-links.

### The Ownership Argument

Links belong to their home document:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

CREATENEWVERSION creates a **new document** with its own address. Links from the original are owned by the original — they cannot migrate to a new document without being recreated. The new version starts with no home links.

### The Address Structure Argument

Links and bytes occupy separate subspaces in the document's address space:

| Subspace | Address Pattern | Contents |
|----------|-----------------|----------|
| Bytes | `version.0.1.N` | Text content |
| Links | `version.0.2.N` | Links homed in this document |

When CREATENEWVERSION copies "contents," it creates a new V-space arrangement mapping to the same I-space byte addresses. The link subspace is structurally separate and not included in what Nelson calls "contents."

### What Links Still Work

Importantly, links made **to** the original's content still function for the new version. Because both versions share I-space addresses, any link whose endsets touch that shared content is discoverable from either version:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

So the new version **inherits discoverability of incoming links** through shared I-space, but does not inherit the original's outgoing links as owned objects.

### Summary

| What the new version gets | Source |
|--------------------------|--------|
| Text content (shared I-addresses) | "the contents of document \<doc id\>" [4/66] |
| Ancestry indication in its address | "The new document's id will indicate its ancestry" [4/66] |
| Discoverability via shared I-space | "a link to one version... is a link to all versions" [2/26] |

| What the new version does NOT get | Reason |
|-----------------------------------|--------|
| Original's home links | Links are owned by home document [4/12, 4/31] |
| Original's link subspace | "Contents" excludes "out-links" [2/31] |

NEED_RAW: [4/66] — to verify whether any additional context surrounds the CREATENEWVERSION description on that page beyond the single sentence in the curated source.

---

## Question 2 [nelson]

> Does creating a new version establish a permanent record of which document it was derived from, and is that parentage relationship itself permanent?

### Nelson's Answer

## Yes — in two distinct and complementary ways

### 1. The Tumbler Address Encodes Ancestry

When CREATENEWVERSION is invoked, the system returns a new document whose tumbler address is structurally "under" the parent:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. **The new document's id will indicate its ancestry.**" [LM 4/66]

Because tumbler addresses are permanent and never reassigned, this parentage record is itself permanent:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a **permanent tumbler address**." [LM 4/19]

The version becomes a sub-address of the parent document through forking:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

### 2. An Important Qualification

Nelson adds a caveat about what the address structure *formally* guarantees:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and **strictly implies no specific relationship of derivation**." [LM 4/29]

This means: the tumbler hierarchy is organizational, not a formal proof of derivation. The address *indicates* ancestry (the system places it there during CREATENEWVERSION), but the address format alone doesn't *logically entail* that content was derived. Someone could theoretically use subdocument numbers for other organizational purposes.

### 3. The Deeper Permanence: Shared I-Space

The stronger and irrevocable record of parentage is the shared I-space content. CREATENEWVERSION creates a new V-space arrangement that references the *same* I-addresses as the parent:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

Since I-space content is immutable and permanent, this shared origin cannot be severed. It is what enables the system to compute correspondence:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

SHOWRELATIONOF2VERSIONS exploits this shared I-space origin to return corresponding span pairs [LM 4/70]. The correspondence is not metadata — it is structural, computed from the addresses themselves.

### Summary

| Mechanism | Records parentage? | Permanent? | What it proves |
|-----------|-------------------|------------|----------------|
| Tumbler address | Yes — placed "under" parent | Yes — addresses never change | Indicates ancestry by convention |
| Shared I-space | Yes — same I-addresses | Yes — I-space is immutable | Proves content origin structurally |

The tumbler address tells you *which document this was versioned from*. The shared I-space tells you *which content they share*. Both are permanent. The tumbler indication is conventional (the system puts it there); the I-space sharing is structural (it cannot be otherwise).

---

## Question 3 [nelson]

> If two versions share the same content, does editing one version's content affect what the other version displays, or are they independent after forking?

### Nelson's Answer

# Version Independence After Forking

**Short answer: They are independent after forking.** Editing one version does not affect what the other displays. This independence follows directly from how I-space and V-space work.

## Why Versions Are Independent

Each version has its **own V-space arrangement** — its own mapping from sequential positions to permanent I-space content. When you create a new version via CREATENEWVERSION, the new document gets a fresh V-space that initially references the same I-space bytes as the original. From that point, the two V-spaces evolve independently.

Nelson makes the I-space guarantee explicit:

> "Content at an I-space address never changes." (paraphrased from 4/11)

And on editing:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is the critical point. When you INSERT into version A:
- **New bytes** are created in I-space (at fresh, permanent I-addresses)
- Version A's V-space is updated to include them
- Version B's V-space is **untouched** — it still maps to the original I-space content

When you DELETE from version A:
- Content is removed from version A's **V-space only**
- The I-space bytes remain forever
- Version B's V-space still references them normally

## The Analogy

From the I-space/V-space source, the library analogy captures this precisely:

```
I-Space (Library)              V-Space (Reading Lists)
┌─────────────────────┐        ┌─────────────────────┐
│ Shelf A: "hello"    │        │ Version 1:          │
│ Shelf B: " world"   │   ──►  │   [ref A, ref B]    │  → "hello world"
│ Shelf C: "!"        │        │                     │
│                     │        │ Version 2:          │
│ (never changes)     │   ──►  │   [ref A, ref C]    │  → "hello!"
└─────────────────────┘        └─────────────────────┘
```

The library stacks (I-space) never change. Each reading list (V-space) can be rearranged independently.

## Shared Content Enables Comparison, Not Coupling

The fact that versions share I-space content is not a liability — it is what makes correspondence possible:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

The shared I-addresses are how the system **detects** what two versions have in common. SHOWRELATIONOF2VERSIONS exploits this:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

Sharing I-space origin is a **read-only relationship** — it tells the system "these positions contain the same content" without creating any write-coupling between versions.

## Nelson's Foundational Principle

The entire storage model is built on non-destruction:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

And on modifications:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

The phrase "without damaging the originals" is the version independence guarantee stated as a user-facing promise.

## One Nuance: Windowing vs. Forking

Nelson describes a second way to create derivative documents — **versioning by inclusion** (windowing/transclusion), where a new document contains transparent windows into the original. In this case, if the window is **location-fixed** (floating in time), changes to the original's arrangement could be visible through the window:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

But this is a different mechanism from CREATENEWVERSION. It's transclusion, where one document deliberately references another's live V-space. Even here, the I-space bytes themselves are never modified — only the V-space arrangement of the windowed-to document changes.

## Summary

| Operation on Version A | Effect on Version B |
|------------------------|---------------------|
| INSERT new text | None — new I-space bytes, only A's V-space updated |
| DELETE a passage | None — A's V-space shrinks, B's unchanged |
| REARRANGE content | None — pure V-space operation on A only |
| COPY into A | None — A's V-space gains references, B's unchanged |

Versions share I-space **content** (immutable bytes), not I-space **arrangement** (V-space mappings). Each version's V-space is fully independent after forking.

---

## Question 4 [nelson]

> When a new version is created, do the links attached to the original document carry over into the new version, or does the new version start with no links?

### Nelson's Answer

## Links and CREATENEWVERSION

**Short answer:** The new version most likely starts with no links. Nelson's text is not fully explicit, but the weight of evidence from Literary Machines points strongly in this direction.

### The Specification

Nelson defines CREATENEWVERSION as:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The key word is **"contents."** Nelson distinguishes "contents" from "out-links" elsewhere:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents." [LM 2/31]

If "contents" and "out-links" are separate concepts, then copying "the contents" does not include copying the links.

### Structural Reasons Links Cannot Simply "Carry Over"

Links have permanent addresses in their home document's link subspace:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

> "A document includes only the links of which it is the home document." [LM 4/31]

A new version is a **new document** with a new tumbler address. The original's links live at the original's addresses. They cannot "move" to the new document — they would need to be freshly created copies with new addresses in the new document's link subspace. Nelson does not describe such copying.

### Why This Works: Version-Spanning Links

The seeming loss is illusory. Links made to the original version effectively reach the new version through **correspondence**:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Because the new version shares I-space content with the original, any link pointing to that content can be "refractively followed" into the new version. The link doesn't need to be copied — the shared I-space origin makes it discoverable from either version.

### What CREATENEWVERSION Does Copy

The operation copies the **text content arrangement** — the V-space mapping over shared I-space addresses. This is what enables correspondence and intercomparison between versions. The new version sees the same text through a new V-space arrangement that can then be independently edited.

### Summary

| Aspect | Carries Over? | Why |
|--------|--------------|-----|
| Text content (I-space) | Yes — shared | Shared I-addresses; no new content allocated |
| V-space arrangement | Yes — copied | New V-stream maps to same I-addresses |
| Out-links (home links) | No | Links are addressed in original's subspace |
| In-links (from others) | Effectively yes | Refractive following through correspondence |
| Correspondence | Automatic | Shared I-space origin |

The design is elegant: you don't need to copy links because the I-space sharing that makes versions meaningful also makes links to one version discoverable from any other version. The new version starts clean — a fresh document with inherited text but its own link space, ready for its own annotations and connections.

NEED_RAW: [4/66 (page 233), 4/9 (page 176)] — to verify whether Nelson's diagram of document contents treats links as part of "contents" in the CREATENEWVERSION context specifically.

---

## Question 5 [nelson]

> Can a user create a new version of someone else's document, or must version creation be restricted to the document's owner?

### Nelson's Answer

# Can a Non-Owner Create a New Version?

**Yes.** Nelson explicitly supports non-owners creating versions of documents they don't own. This is not merely permitted — it is a central design principle.

## The Direct Evidence

From the windowing section:

> "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion." [2/38, windowing concept]

From the publishing section:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

> "This means a whole new pluralistic publishing form. If anything which is already published can be included in anything newly published, any new viewpoint can be freely presented by an easily-made annotated collage. (The old viewpoint is still present too — you can always say, 'Show me what this originally was.')" [LM 2/45]

## The Ownership Distinction

Nelson draws a clear line between **modifying** a document (owner only) and **creating a version** (anyone):

> "Every document has an owner... Only the owner has a right to withdraw a document or change it." [LM 2/29]

The key word is "change it" — meaning alter the existing document in place. Creating a *new* version is creating a *new* document. The new version belongs to whoever created it, not to the original owner.

## Writing Always Succeeds

Nelson's deepest principle here is that access denial produces a fork, never a dead end:

> "Thus users may also republish documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

The session model extraction captures this principle: if you cannot modify the original, you create a version. The system should never produce a permanent "permission denied" — only a redirect to a fresh document under your ownership.

## Two Mechanisms

Nelson describes two ways this works in practice:

**1. Formal versioning (CREATENEWVERSION):** The FEBE command "creates a new document with the contents of document `<doc id>`. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]. No ownership restriction is stated in the command specification.

**2. Versioning by inclusion:** A user creates a new document that transcludes (windows) the parts they want to keep and adds their own modifications. Nelson calls this a "derivative document" — "one which consists explicitly of an original and changes to it — which may be made by anyone." [LM 2/38]

## Royalty Implications

When a non-owner's version is read, royalties split automatically:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

This confirms that the system anticipates and supports non-owner versioning as a normal, economically integrated operation.

## Summary

| Action | Who May Do It |
|--------|--------------|
| **Modify** a document (INSERT, DELETE, REARRANGE) | Owner only |
| **Withdraw** a document | Owner only (with due process) |
| **Create a new version** | Anyone |
| **Transclude and annotate** (versioning by inclusion) | Anyone |
| **Link to** a published document | Anyone |

The entire pluralistic publishing model depends on non-owners being able to create versions. This is not an edge case — it is the system working as intended.

---

## Question 6 [nelson]

> After a version fork, if both versions are edited independently, is there any designed mechanism for merging them back together, or do versions only diverge?

### Nelson's Answer

# Version Merging in Xanadu: Divergence Only

**Versions in Xanadu are designed to diverge, not converge. There is no merge operation.**

## What Nelson Provides

The FEBE protocol includes exactly two version-related operations:

- **CREATENEWVERSION** — forks a document into a new version
- **SHOWRELATIONOF2VERSIONS** — "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]

The first creates divergence. The second enables *comparison*. Neither produces convergence.

## The Design Philosophy

Nelson frames versions as equal, co-existing arrangements — not as a tree with a trunk to merge back into:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

He calls this **prismatic storage** — content refracts into different versions like light through a prism. The metaphor is revealing: a prism splits light; it does not recombine it.

The entire version apparatus is oriented toward **intercomparison**, not reconciliation:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

> "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

## What a User *Could* Do Instead

A user who wants to combine elements from two divergent versions can create a **new compound document** using COPY (transclusion) and INSERT. This would be a third version that windows content from both parents. Nelson explicitly supports this pattern:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

But this is not "merging" in the version-control sense. It produces a *new* divergent version that happens to draw from two sources. The two parent versions remain unchanged and independent. There is no operation that reconciles two V-space arrangements into one, and no concept of "conflict resolution" between competing edits.

## Why This Is Deliberate

The absence of merging follows from Xanadu's core commitments:

1. **Permanence** — every version persists exactly as created. A merge that "resolves" two versions into one would implicitly deprecate the originals, violating the principle that no arrangement is privileged.

2. **Non-destruction** — merging in conventional VCS often involves choosing one side over another, discarding changes. Xanadu never discards.

3. **Pluralism** — Nelson explicitly envisions "a whole new pluralistic publishing form" [LM 2/45] where multiple viewpoints coexist. Merging presupposes that divergence is a problem to be solved. Nelson treats it as a feature.

4. **Correspondence as relation, not operation** — shared I-space origin lets the system *show* what corresponds across versions. The human decides what to do with that information. The system does not decide for them.

## Summary

| Capability | Provided? |
|-----------|-----------|
| Fork a version | Yes (CREATENEWVERSION) |
| Compare divergent versions | Yes (SHOWRELATIONOF2VERSIONS, correspondence) |
| Navigate between corresponding parts | Yes (refractive link following) |
| Merge two versions into one | **No** |
| Manually compose a new version from two sources | Yes (COPY/transclusion) |

Nelson designed a system where versions proliferate and can be compared in fine detail, but never collapse back together. Merge is a front-end semantic concern — if someone wants it, they build a new version by hand. The system provides the comparison tools to make that tractable, but the editorial judgment of what to keep and what to discard remains with the human.

---

## Question 7 [nelson]

> Does the identity of content shared between two versions remain the same — that is, can the system recognize that two versions contain the identical original material?

### Nelson's Answer

# Yes — Shared Content Identity Is the Foundation of the System

The recognition that two versions contain the same original material is not merely possible in Xanadu — it is **structural and automatic**. It falls directly out of the two-address-space architecture.

## The Mechanism: Shared I-Space Origin

Content lives permanently in I-space. A version is a V-space arrangement that *references* I-space content. When a new version is created, it does not copy the content — it creates a new V-space mapping over the **same** I-space addresses.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The CREATENEWVERSION operation makes this explicit:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The new version shares I-addresses with the original. The system doesn't duplicate bytes — it creates a new arrangement pointing to the same permanent content.

## Correspondence: The Relation That Emerges

Nelson names the resulting relation **correspondence**. It is not metadata attached after the fact — it is an inherent structural property computed from shared I-addresses:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

> "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." [LM 3/13]

The FEBE protocol provides a dedicated operation for this:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

That is SHOWRELATIONOF2VERSIONS — it returns exactly which spans in version A match which spans in version B, because they share I-space origin.

## Content Identity Is Based on Creation, Not Value

A critical distinction: two independently typed copies of the word "hello" have **different** I-addresses. But content that was created once and then versioned or transcluded retains its **single** I-address across all appearances.

This means the system distinguishes between "wrote the same words independently" and "this IS the same content." The latter is what versions share.

## Discovery Across All Documents

The shared-identity principle extends beyond versions to the entire docuverse:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

That is FINDDOCSCONTAINING — given any content, find every document anywhere in the docuverse that contains it (via transclusion or shared versioning). This works precisely because identity is tracked through I-addresses, not by content comparison.

## Version-Spanning Links

The practical consequence is that links work across versions automatically:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

A link made to version 1 resolves in version 5 because the system traces the I-address through whatever V-space arrangement the reader is viewing.

## Summary

The identity of shared content is not merely "recognized" — it is the **architectural primitive** on which versions, correspondence, transclusion, link survivability, and cross-document discovery all depend. Two versions share the same I-space content by construction. The system computes correspondence from this shared identity. No separate tracking mechanism is needed because identity IS the address.

---

## Question 8 [nelson]

> Must every version of a document be independently permanent, or can a version's existence depend on the continued existence of its parent?

### Nelson's Answer

## Every Version Is Independently Permanent

The short answer: each version is an independently permanent document. A version's existence does not depend on its parent's continued existence as a version. However, versions share I-space content, which creates a structural dependency on that content's permanence — a dependency satisfied by the same guarantee that makes all content permanent.

### Versions Are Documents

Nelson is explicit that CREATENEWVERSION produces a new, independent document:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The new document has its own tumbler address, its own V-space arrangement, and its own identity. The ancestry is recorded in the address structure — but Nelson is careful to note that address hierarchy is naming, not dependency:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

### No Version Is Privileged

Nelson explicitly rejects the idea that any version has special status:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

If no version is "basic," then no version can be the foundation on which others depend. They are all equal arrangements over the same I-space content.

### The Shared Content Layer

Where the question gets subtle is at the I-space level. Both parent and child version reference the same permanent I-space content. The child version's V-space mapping points to bytes whose "home location" is the parent document:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

This creates a runtime fetch dependency — the child version retrieves shared content from the parent's home location. But this is the **same dependency that all transclusion creates**. It is not specific to versions. Any compound document that windows content from another document has this same relationship.

### Permanence Resolves the Dependency

The dependency on shared I-space content is resolved by the permanence guarantee itself:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The I-space content is in the append-only store. Nelson's storage model is explicitly designed to never destroy content:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The content that parent and child both reference lives permanently in I-space. Neither version "owns" it in a way that makes the other dependent. Both are views over permanent content.

### The Key Distinction

There are two senses of "depend on":

1. **Structural dependency** (does the child's definition reference the parent?) — Yes, the child's V→I mapping points to I-addresses that happen to be native to the parent. But this is shared reference, not dependency.

2. **Existential dependency** (if the parent ceases to exist, does the child break?) — No. The I-space content is permanent regardless of what happens to any particular V-space arrangement. Even if somehow the parent's V-space arrangement were removed (equivalent to "deleting" the parent version), the I-space bytes remain:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Summary

Every version is independently permanent as a document — with its own address, its own arrangement, and no privileged relationship to its parent. The I-space content they share is permanent by virtue of the append-only storage model (P0), not by virtue of any version's continued existence. A version's permanence derives from the permanence of I-space content, not from the permanence of any other version.

---

## Question 9 [nelson]

> When content is transcluded from a document into another document, and the source document is then versioned, which version does the transclusion point to — the original, the new version, or both?

### Nelson's Answer

# Transclusion and Versioning: Which Version Does It Point To?

## The Short Answer

**Neither, both, or either — depending on the level of analysis.**

At the storage level, transclusion points to **I-space addresses**, which are permanent and version-independent. At the user-experience level, Nelson specifies **two explicit modes** that determine what the reader sees when the source evolves.

## The I-Space Foundation

Transclusion in Xanadu is not a pointer to a document or a version — it is a V-space mapping to permanent I-space content. When you COPY (the transclusion operation), your document's V-stream gains entries that reference I-space addresses belonging to the source document. Those I-space addresses are **immutable and eternal**:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When CREATENEWVERSION is performed on the source document, the new version **shares the same I-space content**. No bytes are copied; the new version is a new V-space arrangement over identical I-space addresses. So the transclusion resolves to the same bytes regardless of how many versions exist — because it points to the content itself, not to any particular version's arrangement of it.

## The Two Window Modes

Nelson explicitly addresses what happens when the source document **changes** (not just versions, but actual edits that alter the V-space arrangement). He specifies two modes:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

### Time-Fixed (Frozen Reference)
- Shows the content as it existed at the moment of transclusion
- Changes to the source are invisible unless the reader explicitly asks
- The reader can query: "What has this passage become?"
- Use case: scholarly citation to a specific historical state

### Location-Fixed (Floating in Time)
- Tracks the source as it evolves
- Updates propagate automatically
- Solves the "distributed update" problem
- Use case: living reference to evolving content

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

## The Versioning Scenario Specifically

Consider the sequence:
1. Document B contains text "The cat sat on the mat"
2. Document A transcludes that passage from B
3. B is versioned to create B' (CREATENEWVERSION)
4. B' is then edited — say, "cat" is changed to "dog"

At step 3, nothing changes for A. B and B' share identical I-space content. A's transclusion resolves to the same bytes it always did.

At step 4, the two modes diverge:
- **Time-fixed**: A still shows "The cat sat on the mat" — the I-space bytes haven't moved
- **Location-fixed**: A could show the updated content from B', if B' is the "current" version being tracked

The critical insight is that "cat" still exists at its I-space address forever. The edit in B' created new I-space content ("dog") and changed B's V-space mapping. A's transclusion to the original I-space bytes remains valid in either mode.

## Refractive Following Across Versions

Nelson also describes a third capability — **correspondence-based navigation** — which applies to links but illuminates the versioning model:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

This means a reference to content in version 1 can be "refracted" through correspondence to find the same content (or its evolved form) in any other version. The system's knowledge of shared I-space origins makes this possible:

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

## Summary

| Level | What Transclusion Points To |
|-------|---------------------------|
| **I-space (storage)** | Permanent bytes — version-independent |
| **Time-fixed mode** | Original arrangement at moment of inclusion |
| **Location-fixed mode** | Current arrangement, updates automatically |
| **Refractive following** | Any version, via correspondence |

The fundamental answer is that transclusion points to **content, not versions**. Versions are different arrangements of the same underlying content. The two window modes determine how the user experiences the evolution of that arrangement, but the underlying I-space content that the transclusion references is permanent and shared across all versions.

---

## Question 10 [nelson]

> Is there a limit to how many times a document can be versioned, and do all versions form a tree structure, or can a version have multiple parents?

### Nelson's Answer

## No Limit on Versioning; Structure Is a Tree (Single Parent)

### No Upper Bound on Versions

There is no limit. The tumbler addressing system uses humbers — arbitrary-precision integers that expand as needed:

> "Humbers are numbers we have designed for this system, a notation for positive integers... an accordion-like notation, very short when a number is small, and as large as it needs to be when the number is big." [LM 4/13]

Versions are created by forking new digits under a document's address, and forking has no upper bound:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

A document at address `1.0.2.0.5` can spawn versions `1.0.2.0.5.1`, `1.0.2.0.5.2`, ..., `1.0.2.0.5.N` without limit. Each of those can in turn spawn sub-versions indefinitely.

### Versions Form a Tree (Single Parent Only)

The CREATENEWVERSION operation takes exactly one source document:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The tumbler address encodes this single-parent ancestry structurally. If document `1.0.2.0.5` spawns version `1.0.2.0.5.3`, the address itself records that `5.3` descends from `5`. This is inherently a tree — each version has exactly one parent.

### No Merge Operation

Nelson provides **divergence** (forking) and **comparison** (SHOWRELATIONOF2VERSIONS), but no convergence operation that would create a version with two parents:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

The system lets you compare any two versions to see what corresponds, but combining them into a single merged version is not a primitive operation. (From the project's prior analysis: "Version merging deliberately absent — Nelson envisions divergence + comparison, not convergence; merge is front-end semantic concern.")

### Multi-Source Content Without Multi-Parent Ancestry

While the version *address tree* is strictly single-parent, a document's *content* can draw from multiple sources through transclusion:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

So you could create version `5.3` from document `5`, then COPY content into it from documents `7`, `12`, and `99`. The result has content from four sources but only one *parent* in the version tree. Nelson calls this "versioning by inclusion":

> "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion." [LM 2/38]

### An Important Caveat on Address vs. Derivation

Nelson explicitly warns against reading too much into the address structure:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

The tree shape of addresses is a consequence of the addressing mechanism, not necessarily a claim about intellectual derivation. Two documents might be deeply related (one inspired by the other) without being in the same address subtree. Conversely, a version created under a document's address might diverge radically from its parent.

### Summary

| Question | Answer |
|----------|--------|
| Version count limit? | None — humbers and forking are unbounded |
| Version graph shape? | Tree — each version has exactly one parent address |
| Multi-parent merge? | Not provided — divergence and comparison only |
| Multi-source content? | Yes, via transclusion (COPY), but address ancestry stays single-parent |

---

## Question 11 [gregory]

> When CREATENEWVERSION copies the text subspace POOM, is the new POOM a structurally independent B-tree (deep copy of all crums), or does it share any tree nodes with the source document's POOM?

### Gregory's Answer

## KB Synthesis

The KB is definitive on this: CREATENEWVERSION creates a **structurally independent B-tree** for the version's POOM. No crum nodes are shared.

## The Copy Path

The call chain documented in [ST-VERSION] (Finding 0077) and [ST-VERSION-CREATE] (Findings 0043, 0046) is:

```
docreatenewversion
  → createorglingranf          (allocates new document address)
  → doretrievedocvspanfoo      (retrieves source text V-span)
  → docopyinternal
      → specset2ispanset       (converts V-spans → I-spans via source POOM)
      → insertpm               (builds NEW POOM crums in version's enfilade)
      → insertspanf            (records SPAN entries)
```

The critical step is `specset2ispanset`: it reads the source document's POOM to convert V-positions to I-addresses, producing a fresh `ispanset`. Then `insertpm` uses those I-addresses to insert new bottom crums into the **version's own enfilade tree** via the standard insertion mechanism — the same path used by INSERT and COPY [ST-INSERT].

## What IS Shared vs. What Is NOT

| Layer | Shared? | Notes |
|-------|---------|-------|
| I-addresses (content identity) | **Yes** | The whole point of versioning |
| POOM crum nodes | **No** | New crums allocated by `insertpm` |
| Enfilade tree structure | **No** | Version has its own independent tree |
| Spanfilade entries | New entries added | `insertspanf` records under new doc address |

## Confirmation from Frame Conditions

[FC-VERSION-ISOLATION] (Finding 0072) states explicitly:

> "The original and version are separate tree structures — editing one does not affect the other."
> "There are no copy-on-write semantics, no shadow copies."

[SS-POOM-MUTABILITY] (Finding 0072) reinforces this: the POOM is modified in-place by INSERT/DELETE/REARRANGE with no shared structure between documents.

The operational consequence is stated in [FC-VERSION-ISOLATION]: after `CREATENEWVERSION(D)`, `∀ op applied to D : poom(V) unchanged` and `∀ op applied to V : poom(D) unchanged` — this isolation guarantee requires structurally independent trees.

## Implication

The version starts with a freshly populated POOM tree whose crums encode the same I-address mappings as the source's text subspace, but as new allocations. The source's enfilade tree is only read (via `specset2ispanset`), never copied at the node level.

## Code Exploration

Now I have the complete picture. Let me write the full answer.

---

## Answer: POOM Structural Independence in CREATENEWVERSION

The new POOM produced by CREATENEWVERSION is **structurally independent** — every tree node is freshly allocated. No POOM crum pointers are shared with the source document. However, the new POOM is not a deep copy of the source POOM's structure either: it is a **newly constructed B-tree built by re-inserting the same I-coordinate data** (permascroll addresses) into a blank enfilade.

---

### The Execution Path, Step by Step

**Entry point: `fns.c:289-300`** — `createnewversion()` calls:
```c
docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa)
```

**`do1.c:260-299`** — `docreatenewversion()` does three things:

**Phase 1 — Create a blank POOM for the new document** (`do1.c:277`):
```c
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) return FALSE;
```

`createorglingranf` → `createorglgr` (`granf2.c:111-128`):
```c
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);    // granf2.c:120
```

`createenf(POOM)` at `credel.c:492-516`:
```c
fullcrumptr = (typecuc *) createcrum(1, enftype);           // credel.c:497
fullcrumptr->isapex = TRUE;
adopt(ptr = createcrum(0, enftype), SON, (typecorecrum*)fullcrumptr);  // credel.c:501
```

`createcruminternal` (`credel.c:541-596`) allocates each crum via `ealloc()` — raw heap memory — and zero-initializes all fields including `cdsp`, `cwid`, `c2dinfo`, pointers (`leftbroorfather = NULL`, `rightbro = NULL`, `leftson = NULL`). **No source document data or pointers are involved.** The result is an empty POOM with one apex `typecuc` and one bottom `type2dcbc`.

---

**Phase 2 — Read the source document's V-span** (`do1.c:281-283`):
```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) return FALSE;
```

`doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm` (`orglinks.c:155-162`):
```c
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
```
This just reads two tumblers from the source POOM root's fields — a bounding-box query. No traversal of the source tree, no pointer copies.

---

**Phase 3 — Copy content into the new POOM** (`do1.c:293`):
```c
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

`docopyinternal` (`do1.c:66-82`) does:
```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)   // new doc's POOM
insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
```

**`specset2ispanset` (`do2.c:14-46`)** is called with the `VSPECID` referring to the *source* document. It calls `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` on the **source** POOM to walk its tree and extract I-coordinate spans. The output is a linked list of `typeispan` items (itemid `ISPANID`) holding permascroll addresses (tumblers). These are value copies — no pointers into the source POOM tree.

---

**`insertpm` (`orglinks.c:75-134`)** iterates over each I-span:
```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);  // orglinks.c:101
    movetumbler (&lstream, &crumorigin.dsas[I]);
    movetumbler (&lwidth,  &crumwidth.dsas[I]);
    movetumbler (vsaptr,   &crumorigin.dsas[V]);
    // ... compute crumwidth.dsas[V] ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
}
```

**`unpacksporgl` (`sporgl.c:178-203`)** with `ISPANID` items:
```c
movetumbler (&((typeispan *)sporglptr)->stream, streamptr);   // I-coord value
movetumbler (&((typeispan *)sporglptr)->width, widthptr);     // width value
tumblerclear (&infoptr->homedoc);                             // sporgl.c:183
```
`linfo.homedoc` is set to **zero**. The I-coordinates are copied as data values (tumblers), not as pointers to source crums.

---

**`insertnd` / `insertcbcnd` (`insertnd.c:242-275`)** creates new POOM bottom crums:
```c
new = createcrum (0, (INT)father->cenftype);     // insertnd.c:260 — fresh heap alloc
reserve (new);
adopt (new, SON, (typecorecrum*)father);
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
movewisp (width, &new->cwid);
move2dinfo (infoptr, &((type2dcbc *)new)->c2dinfo);   // copies homedoc tumbler = 0
```

Every bottom crum in the new POOM is allocated by `createcrum` (which calls `ealloc` for a fresh `type2dcbc` struct). Its `cdsp.dsas[I]` holds the permascroll address (same value as in the source POOM crums), but it is a **distinct heap object** with no aliasing to the source POOM.

---

### What Is and Is Not Shared

| Thing | Shared? | Explanation |
|---|---|---|
| POOM apex crum (`typecuc`) | **No** | Created fresh by `createenf` / `createcrum` (`credel.c:497`) |
| POOM bottom crums (`type2dcbc`) | **No** | Created fresh by `insertcbcnd` / `createcrum` (`insertnd.c:260`) |
| Tree pointer linkage (`leftson`, `rightbro`, etc.) | **No** | Wired by `adopt` into the new tree only |
| I-coordinate values (permascroll addresses in `cdsp.dsas[I]`) | **Same values** | The new POOM bottom crums store the same I-address tumblers as the source — but in separate memory |
| Text content in granfilade | **Permanently shared** | The granfilade is append-only; text is looked up by I-address and never duplicated |
| `c2dinfo.homedoc` | **Zero** | Set by `unpacksporgl` (`sporgl.c:183`) when processing ISPANID items |

---

### Conclusion

CREATENEWVERSION builds the new POOM from scratch. `createenf(POOM)` (`granf2.c:120`, `credel.c:492`) allocates a completely blank enfilade. Each content crum is then added by `insertnd` → `insertcbcnd` → `createcrum` (`insertnd.c:260`), allocating independent heap memory. The source POOM is consulted only to **read** permascroll addresses (I-coordinates); those addresses are stored as tumbler values in the new POOM's freshly created crums.

There is **no structural sharing** — no pointer from any new POOM crum points into the source POOM's tree. Subsequent edits to either document's POOM (insertions, deletions, rearrangements) affect only that document's independent tree. The underlying permascroll content in the granfilade is shared by I-address reference, as it must be in any Xanadu-style transclusion model.

---

## Question 12 [gregory]

> After CREATENEWVERSION, if the original document is edited (INSERT or DELETE), does the version's POOM remain completely unchanged — same V-addresses, same I-address mappings, same tree structure?

### Gregory's Answer

## KB Synthesis

Yes. After CREATENEWVERSION, edits to the original document leave the version's POOM — V-addresses, I-address mappings, and tree structure — completely unchanged.

## The direct answer from the KB

**[FC-VERSION-ISOLATION]** (`Finding 0072`) states this explicitly:

> Once a version is created via CREATENEWVERSION, it is a fully independent document with its own POOM tree. Edits to the original document (INSERT, DELETE, REARRANGE) modify only the original's POOM. Edits to the version modify only the version's POOM. Neither affects the other.

## Why this holds mechanically

**INSERT on the original** (`[ST-INSERT]`, `[SS-POOM-MUTABILITY]`): `insertpm` → `insertnd` → `makegappm` all operate on the orgl handle passed to them — the original's orgl. The version has a distinct orgl (allocated by `createorglingranf` during CREATENEWVERSION). No code path in the INSERT chain touches any other document's orgl.

**DELETE on the original** (`[FC-DELETE-CROSS-DOC]`, Finding 0064): `dodeletevspan` → `deletevspanpm` → `deletend` operates on a single document's orgl. The KB states directly: "DELETE in one document has zero effect on any other document's POOM mappings." Documents that transclude the same I-addresses remain unaffected because DELETE only modifies the target document's POOM tree, not the granfilade or any other POOM.

**Tree structure is also isolated**: Splits, rebalancing (`recombinend`), and `levelpush` triggered by INSERT on the original operate on the original's in-memory crum tree. The version's crums are entirely separate allocations. `[SS-POOM-MUTABILITY]` confirms there are no copy-on-write semantics or shared structure between document POOMs.

## What IS shared (and unchanged)

The granfilade (I-addresses, content bytes) is append-only and shared. INSERT on the original allocates new I-addresses into the shared granfilade and advances the allocation counter. The version's POOM gets no new entries pointing to these new I-addresses — that would require an explicit `insertpm` on the version's orgl. The shared granfilade grows, but the version's view of it (its POOM mappings) is frozen at creation time.

## Summary

| Component | After INSERT on original | After DELETE on original |
|-----------|--------------------------|--------------------------|
| Version POOM (V→I mappings) | **Unchanged** | **Unchanged** |
| Version POOM tree structure | **Unchanged** | **Unchanged** |
| Shared granfilade | Grows (new I-addrs added) | Unchanged (append-only) |
| Shared spanfilade | New DOCISPAN for original | Unchanged |

The version is a snapshot — its POOM is a separate tree whose nodes are neither referenced by nor modified by any subsequent operation on the original. `[FC-VERSION-ISOLATION]` and `[FC-DELETE-CROSS-DOC]` together provide the complete guarantee.

## Code Exploration

The finding was denied. Here is my full answer.

---

## Answer: Yes — the version's POOM is completely unchanged after editing the original

The isolation is absolute, by construction. Here is the complete code trace.

---

## 1. CREATENEWVERSION allocates a fresh POOM root for the version

`docreatenewversion` [do1.c:260-299] first calls:

```c
createorglingranf(taskptr, granf, &hint, newisaptr)   // do1.c:277
```

→ `createorglgr` [granf2.c:111-128]:

```c
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // granf2.c:120
```

→ `createenf(POOM)` [credel.c:492-516]:

```c
fullcrumptr = (typecuc *) createcrum(1, enftype);   // credel.c:497 — brand new fullcrum
adopt(ptr = createcrum(0, enftype), SON, ...);      // credel.c:501 — brand new bottom crum
```

`createcrum` calls `eallocwithtag` [credel.c:518-532] — a fresh `malloc`/`falloc` heap allocation each time. The version gets its own `typecuc*` POOM root, zero-initialized, **with zero connection to the original's POOM**.

---

## 2. Version POOM is populated with fresh nodes — not shared pointers

`docreatenewversion` then calls [do1.c:293]:

```c
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

This flows through `insertpm` [orglinks.c:75] → `insertnd` [insertnd.c:15] → `insertcbcnd` [insertnd.c:242]:

```c
new = createcrum(0, (INT)father->cenftype);   // insertnd.c:260 — fresh allocation
reserve(new);
adopt(new, SON, (typecorecrum*)father);        // insertnd.c:262 — into VERSION's POOM
```

`father` is the version's own POOM fullcrum. The original's POOM nodes are never referenced.

---

## 3. All edits on the original go through `findorgl` — which does a per-document lookup

**INSERT** [do1.c:87-123]:

```c
docopy(taskptr, docisaptr, vsaptr, ispanset)
```

→ `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)` [do1.c:55]
→ `fetchorglgr(taskptr, granfptr, isaptr)` [granf2.c:22-81]:

```c
context = retrievecrums((typecuc*)fullcrumptr, address, WIDTH);   // granf2.c:34
if (!tumblereq((tumbler*)&context->totaloffset, address)) { return NULL; }  // granf2.c:37-40
ret = context->corecrum->cinfo.granstuff.orglstuff.orglptr;       // granf2.c:62
```

This looks up the POOM **by exact ISA (tumbler) address**. The original's ISA and the version's ISA are different tumblers. Each `findorgl` call fetches a different, independent `typecuc*`.

**DELETE** [do1.c:158-167]:

```c
findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)   // fetches ORIGINAL's POOM
deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
```

→ `deletevspanpm` [orglinks.c:145-152]:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

→ `deletend` [edit.c:31-76], for removed crums:

```c
disown((typecorecrum*)ptr);      // edit.c:59
subtreefree((typecorecrum*)ptr); // edit.c:60
```

→ `subtreefree` [credel.c:413-432] recursively `efree`s only nodes reachable from `ptr`, which are all under the original's POOM tree. The version's POOM nodes are different heap objects and are completely unreachable from the original's `docorgl`.

---

## 4. What IS shared (and why it's safe)

The **granfilade I-addresses** pointing to content bytes are shared. The version's POOM crums store in `cdsp.dsas[I]`/`cwid.dsas[I]` the same I-addresses the original had at version-creation time. This is intentional transclusion — both POOMs point to the same immutable permascroll content.

The granfilade is append-only in normal operation. A DELETE removes POOM entries (V→I mappings) but does not physically overwrite granfilade text. So the shared I-addresses remain valid in the version's POOM even after the original is extensively edited.

---

## Summary

| Property | After editing original |
|---|---|
| Version POOM root (`typecuc*`) | **Unchanged** — separate heap object |
| Version POOM crum nodes | **Unchanged** — separate allocations |
| Version V-addresses | **Unchanged** — version's POOM not modified |
| Version I-address mappings | **Unchanged** — version's crums not touched |
| Granfilade content bytes | **Unchanged** — append-only storage |
| Original POOM | Modified as expected |

**The Frame Axiom holds completely for version POOMs.** CREATENEWVERSION produces a snapshot that is structurally decoupled from the original. The isolation mechanism is simple and airtight: each document has its own `typecuc*` POOM root stored at a unique ISA address in the granfilade, and every edit operation does an exact-ISA lookup to get the right POOM — and only that POOM — before operating on it.

---

## Question 13 [gregory]

> When you version a version (CREATENEWVERSION of document `1.1.0.1.0.1.0.1`), is the new version allocated as a child of the version (`1.1.0.1.0.1.0.1.0.1`) or as a sibling under the original (`1.1.0.1.0.1.0.2`)?

### Gregory's Answer

## KB Synthesis

**Child of the version, not sibling under the original.**

From [SS-VERSION-ADDRESS] Finding 0068, `CREATENEWVERSION` uses a context-sensitive hint based on **ownership of the source document**:

- If the user **owns** the source document, `makehint(DOCUMENT, DOCUMENT, depth=1, ...)` places the new version as a child of that source — no `.0.` boundary is crossed.
- If the user **does not own** the source, `makehint(ACCOUNT, DOCUMENT, depth=2, ...)` places it under the creating user's account instead.

The concrete example in Finding 0068 shows this produces unbounded-depth version trees:

```
1.1.0.1.0.1              (doc1)
├── 1.1.0.1.0.1.1        (version1 of doc1)
│   └── 1.1.0.1.0.1.1.1  (version of version1)
└── 1.1.0.1.0.1.2        (version2 of doc1)
```

Applying this to your address: assuming the user owns `1.1.0.1.0.1.0.1`, `CREATENEWVERSION` would allocate the new version as **`1.1.0.1.0.1.0.1.1`** (child of the versioned document), not as `1.1.0.1.0.1.0.2` (which would be a second sibling version of the original).

The allocation mechanism per [ST-ADDRESS-ALLOC] Finding 0068 is stateless query-and-increment: `findpreviousisagr` searches for the highest existing address below `tumblerincrement(source_doc, depth-1=0, 1)` (the next sibling of the source document), checks containment, and if no children exist yet allocates `source_doc.1`. So the first version of `1.1.0.1.0.1.0.1` would be `1.1.0.1.0.1.0.1.1`.

## Code Exploration

I now have everything needed for a complete, fully-cited answer. The golden test at `golden/versions/version_address_allocation.json` provides the empirical proof, and Finding 0068 already documents this. Let me compose the full answer:

---

## Answer: The New Version Is Allocated as a Child — `1.1.0.1.0.1.0.1.1`

Neither option in the question is precisely correct, but the **child** characterization is right in spirit. The version is NOT a sibling. Here is the full code trace.

---

### Step 1: FEBE dispatch — `fns.c:289-300`

```c
void createnewversion(typetask *taskptr)
{
  typeisa originaldocisa, newdocisa;
  ...
  if (
     getcreatenewversion (taskptr, &originaldocisa)
  && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
```

`wheretoputit` is set to `&originaldocisa` — **the same pointer as the document being versioned**. Both the second and third arguments are the source document's address.

---

### Step 2: Ownership check and hint selection — `do1.c:260-299`

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
        makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
    } else {
        makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
    }
```

Since both `isaptr` and `wheretoputit` point to the same document (`1.1.0.1.0.1.0.1`), `tumbleraccounteq` finds two zeros in the document's mantissa and returns `TRUE`. For a user versioning their own document, `isthisusersdocument` also returns `TRUE`. The **ownership branch** is taken:

```c
makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
//        ^^^^^^^^^  ^^^^^^^^^
//        supertype  subtype   ← both DOCUMENT
//                             hintisa = 1.1.0.1.0.1.0.1
```

`makehint` [do2.c:78-84] simply stores these three fields:
```c
hintptr->supertype = DOCUMENT;
hintptr->subtype   = DOCUMENT;
hintptr->hintisa   = 1.1.0.1.0.1.0.1;
```

---

### Step 3: Dispatch to `findisatoinsertnonmolecule` — `granf2.c:130-156`

`createorglgr` → `findisatoinsertgr` [granf2.c:130]:

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        findisatoinsertmolecule (...);     // text/link atoms
    } else {
        findisatoinsertnonmolecule (...);  // ← documents, accounts, nodes
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

---

### Step 4: Query-and-increment allocation — `granf2.c:203-242`

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
    //      DOCUMENT          == DOCUMENT            → depth = 1
```

**`depth = 1`** is the key. For `ACCOUNT → DOCUMENT` (e.g., `docreatenewdocument`), depth would be 2. For `DOCUMENT → DOCUMENT` (versioning), it's 1. This single digit difference governs the whole address structure.

```c
    hintlength = tumblerlength(&hintptr->hintisa);
    // 1.1.0.1.0.1.0.1 has 8 digits → hintlength = 8

    tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);
    // depth-1 = 0 → add 1 to last digit of hintisa
    // 1.1.0.1.0.1.0.1 + 1 at position 7 → upperbound = 1.1.0.1.0.1.0.2
```

```c
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    // Find highest granfilade address < 1.1.0.1.0.1.0.2
    // If no versions yet: lowerbound = 1.1.0.1.0.1.0.1 (the doc itself)
```

```c
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
    // truncate(1.1.0.1.0.1.0.1, 8) = 1.1.0.1.0.1.0.1
    // equals hintisa? YES → lowerbound_under_hint = TRUE
```

No prior version exists → falls into the **first-version branch**:
```c
    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
        // Add 1 at position idx + depth = 7 + 1 = 8
        // mantissa[8] = 1
        // Result: 1.1.0.1.0.1.0.1.1
```

[`tumblerincrement`, tumble.c:599]:
```c
for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
// idx = 7 (last non-zero digit of 1.1.0.1.0.1.0.1)
cptr->mantissa[idx + rightshift] += bint;
// mantissa[7 + 1] += 1 → mantissa[8] = 1
// Result mantissa: [1,1,0,1,0,1,0,1,1,0,...] = 1.1.0.1.0.1.0.1.1
```

---

### Step 5: Empirical confirmation — `golden/versions/version_address_allocation.json`

The golden test directly answers this, showing the complete pattern:

| Source document | Operation | Result address | Pattern |
|----------------|-----------|----------------|---------|
| `1.1.0.1.0.1` | create_document | `1.1.0.1.0.1` | first doc |
| `1.1.0.1.0.2` | create_document | `1.1.0.1.0.2` | second doc |
| `1.1.0.1.0.1` | create_version → **version1** | **`1.1.0.1.0.1.1`** | child of doc1 |
| `1.1.0.1.0.1` | create_version → **version2** | **`1.1.0.1.0.1.2`** | second child of doc1 |
| `1.1.0.1.0.2` | create_version → version3 | `1.1.0.1.0.2.1` | child of doc2 |
| `1.1.0.1.0.1.1` | create_version → **version_of_version** | **`1.1.0.1.0.1.1.1`** | child of version1 |

The `version_of_version` row is the closest analogue to the question's scenario. Versioning `1.1.0.1.0.1.1` gives `1.1.0.1.0.1.1.1`. Applying the same rule, versioning `1.1.0.1.0.1.0.1` gives **`1.1.0.1.0.1.0.1.1`**.

---

### Final Answer

**The new version is allocated as a child of the versioned document**, specifically `1.1.0.1.0.1.0.1.1` — **not** `1.1.0.1.0.1.0.2` (sibling).

However, neither of the two options in the question is exactly right:

| Option | Address | Correct? | Why |
|--------|---------|---------|-----|
| **Child** (as offered) | `1.1.0.1.0.1.0.1.0.1` | ❌ Near-miss | Uses `depth=2` (`.0.1` suffix = two extra digits). Only ACCOUNT→DOCUMENT uses depth=2. |
| **Sibling** | `1.1.0.1.0.1.0.2` | ❌ Wrong | Would require using the **parent document** as the hint — but the code uses `isaptr` (the document itself) as `hintisa`. |
| **Actual result** | `1.1.0.1.0.1.0.1.1` | ✅ | Uses `depth=1` (one appended digit `.1`). The version's address is a sub-address of the original — lexicographically nested within the source document's namespace. |

The critical mechanism is `depth = (supertype == subtype) ? 1 : 2` [granf2.c:209]. When `makehint(DOCUMENT, DOCUMENT, ...)` is called, both types are DOCUMENT, giving `depth=1`. This allocates exactly one digit beyond the source document's address, making the version's address a **depth-1 child**.

The resulting version tree structure is:
```
1.1.0.1.0.1.0.1       (source document)
├── 1.1.0.1.0.1.0.1.1  (first version)
│   ├── 1.1.0.1.0.1.0.1.1.1  (version of version)
│   └── 1.1.0.1.0.1.0.1.1.2
└── 1.1.0.1.0.1.0.1.2  (second version)
```

---

## Question 14 [gregory]

> Does CREATENEWVERSION create DOCISPAN entries in the spanfilade for the new version document, and if so, are they per-I-span entries matching the source's text content — or a single entry covering the entire I-address range?

### Gregory's Answer

## KB Synthesis

## CREATENEWVERSION and DOCISPAN Creation

Yes, CREATENEWVERSION does create DOCISPAN entries for the new version document. The entries are per-I-span, matching the source's text content structure.

### Mechanism

The call chain for CREATENEWVERSION is [ST-VERSION]:

> `docreatenewversion` → `createorglingranf` (doc address) → `doretrievedocvspanfoo` (get d's V-span) → `docopyinternal` → `specset2ispanset` (convert V-spans to I-spans from source) → `insertpm` (update POOM) → `insertspanf` (record SPAN entries)

`docopyinternal` at `do1.c:66-82` calls `insertspanf` — not `findisatoinsertgr` — meaning it registers existing I-addresses under the new document ISA rather than allocating new ones [INT-LINK-VERSION, Finding 0046]. This creates DOCISPAN entries for the version document pointing to the same I-addresses as the source.

### Scope: Text Subspace Only

CREATENEWVERSION copies only the text subspace (V-positions `1.x`). `doretrievedocvspanfoo` delegates to `retrievedocumentpartofvspanpm`, which extracts only the V-dimension displacement and width — covering the text subspace only [ST-VERSION-CREATE, Finding 0046]. Link subspace entries (`2.x`) are not copied, so no DOCISPAN entries are created for link I-addresses.

### Granularity: Per-I-Span

DOCISPAN entries have per-span granularity [SS-DOCISPAN, Finding 0047]:

> When `insertspanf` is called, it iterates over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct.

The `specset2ispanset` step reads the source's POOM to produce the I-span list. The number of resulting DOCISPAN entries equals the number of contiguous I-address regions in the source's text content:

- **Simple source** (single INSERT, no interleaved CREATELINK): 1 contiguous I-span → 1 DOCISPAN entry for the version
- **Fragmented source** (multiple inserts with interleaved CREATELINK calls that broke I-address contiguity [INT-LINK-INSERT, Finding 0063]): N I-spans → N DOCISPAN entries

Notably, CREATENEWVERSION does NOT break I-address contiguity for subsequent INSERTs on the original, unlike CREATELINK. VERSION allocates only a document address in a separate tumbler range; the content allocation counter is unaffected [INV-MONOTONIC, Finding 0077].

### Summary

| Property | Value |
|----------|-------|
| Creates DOCISPAN entries? | Yes |
| Via | `docopyinternal` → `insertspanf` |
| Covers | Text subspace only (`1.x`) |
| Granularity | Per contiguous I-address region (same as COPY) |
| Entries for simple source | 1 (single contiguous I-span) |
| New I-addresses allocated? | No |

## Code Exploration

Now I have all the pieces to give a complete, fully-cited answer. Let me compile the full execution trace.

---

## Answer

### Does CREATENEWVERSION create DOCISPAN entries in the spanfilade?

**Yes.** `docreatenewversion` creates DOCISPAN entries for the new document. They are **per-I-span** — one entry per contiguous permascroll segment referenced by the source document's content. The number of entries is not fixed at one; it depends on the source document's internal structure.

---

### Full Execution Trace

#### 1. `docreatenewversion` — do1.c:260

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
```

After creating the new document via `createorglingranf`, it calls:

```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {    // do1.c:281
    return FALSE;
}

vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);      // source document's ISA
vspec.vspanset = &vspan;                 // single V-span from source

addtoopen(newisaptr, user, TRUE, WRITEBERT);
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // do1.c:293
```

#### 2. `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm` — do1.c:301, orglinks.c:155

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // orglinks.c:159
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);   // orglinks.c:160
    return (TRUE);
}
```

This reads the **root node** of the source document's POOM enfilade directly, extracting its `cdsp` (start) and `cwid` (width) in the V dimension. The result is always exactly **one `typevspan`** — a single span covering the entire V-address range of the source document. This is the "kluge" noted in the comment.

#### 3. `docopyinternal` — do1.c:66

```c
bool docopyinternal(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    typeispanset ispanset;
    typeorgl docorgl;
    ...
    if (!specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE;  // do1.c:74
    if (!findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)) return FALSE;  // do1.c:75
    ...
    if (!insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;         // do1.c:78
    if (!insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;      // do1.c:79
    ...
}
```

The `ispanset` produced by `specset2ispanset` drives both the POOM insert and the spanfilade insert.

#### 4. `specset2ispanset` — do2.c:14

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
    ...
    for (; specset; specset = ...) {
        ...
        } else if (((typeitemheader *)specset)->itemid == VSPECID) {   // do2.c:27
            if (!(
              findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
            && (ispansetptr = vspanset2ispanset (taskptr, docorgl,      // do2.c:36
                    ((typevspec *)specset)->vspanset, ispansetptr)))) {
                return (FALSE);
            }
        }
    }
    ...
}
```

Since the vspec has `itemid == VSPECID`, it calls `vspanset2ispanset` on the **source document's orgl** (POOM) to convert the single V-span to I-spans.

#### 5. `vspanset2ispanset` → `permute` → `span2spanset` — orglinks.c:397, 404, 425

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspan vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);  // orglinks.c:401
}
```

`permute` iterates over the input V-spans (just one, from step 2) and calls `span2spanset` once [orglinks.c:414-416]:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
}
```

`span2spanset` [orglinks.c:425] queries the source document's POOM via `retrieverestricted`, then **iterates over every context entry** and creates one I-span for each:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);  // orglinks.c:435
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);  // orglinks.c:443
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);  // orglinks.c:444
}
```

Each context entry from `retrieverestricted` corresponds to one contiguous block in the enfilade. For a document assembled from N contiguous permascroll segments, `retrieverestricted` returns N context entries, and the output `ispanset` contains **N `typeispan` nodes**.

#### 6. `insertspanf` — spanf1.c:15

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr, typesporglset sporglset, INT spantype)
{
    typedsp crumorigin;
    typewid crumwidth;
    ...
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // spanf1.c:22 — DOCISPAN=4 prefixed to new doc ISA
    tumblerclear (&crumwidth.dsas[ORGLRANGE]);                      // spanf1.c:23 — zero width (point)
    clear (&linfo, sizeof(linfo));
    for (; sporglset; sporglset = ...) {
        if (((typeitemheader *)sporglset)->itemid == ISPANID) {
            movetumbler (&((typeispan *)sporglset)->stream, &lstream);  // spanf1.c:27 — I-address
            movetumbler (&((typeispan *)sporglset)->width, &lwidth);    // spanf1.c:28 — I-width
            movetumbler (isaptr, &linfo.homedoc);                       // spanf1.c:29 — new doc ISA
        }
        ...
        movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);  // spanf1.c:49
        movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);    // spanf1.c:50
        insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // spanf1.c:51
    }
    return (TRUE);
}
```

**One `insertnd` call per loop iteration — one per I-span in the input.** There is no coalescence at this level.

The spanfilade node structure for each DOCISPAN entry:
- **ORGLRANGE key**: `prefixtumbler(newDocISA, 4, ...)` = `4.newDocISA` — same for all entries from this operation, with **zero width** (a point — used for lookup, not range)
- **SPANRANGE key**: the I-span's stream (start address in permascroll space), with **non-zero width** equal to the I-span's extent
- **Payload** (`linfo.homedoc`): the new document's ISA — [spanf1.c:29]

`DOCISPAN = 4` is defined in `xanadu.h:39`. The span type constants are: `LINKFROMSPAN=1` [xanadu.h:36], `LINKTOSPAN=2`, `LINKTHREESPAN=3`, `DOCISPAN=4`.

---

### Summary

| Question | Answer |
|---|---|
| Does CREATENEWVERSION create DOCISPAN entries? | **Yes** |
| How many entries? | **One per contiguous I-span segment** in the source document's content |
| Are they per-I-span matching source text content? | **Yes** — each entry covers one contiguous block of permascroll (I-space) |
| Is it a single entry covering the entire I-address range? | **No** — unless the source document's text happens to be one contiguous permascroll run |

The path is: `docreatenewversion` [do1.c:260] → `doretrievedocvspanfoo` produces a single V-span covering the source document's full V-extent [orglinks.c:159-160] → `docopyinternal` [do1.c:66] → `specset2ispanset` → `vspanset2ispanset` → `permute` → `span2spanset` [orglinks.c:435-444] queries the source POOM and returns one I-span per contiguous permascroll segment → `insertspanf` [spanf1.c:51] calls `insertnd` once per I-span.

For a newly-written document where all text was inserted in a single `doinsert` call into one contiguous region of permascroll, there will be exactly **1 DOCISPAN entry**. For a document assembled from multiple inserts or from text transcluded from different permascroll locations, there will be **one DOCISPAN entry per distinct I-span segment**.

---

## Question 15 [gregory]

> When a document contains transcluded content (I-addresses originating from another document's allocation range), does CREATENEWVERSION preserve those cross-document I-address references in the version's POOM, maintaining the transclusion chain?

### Gregory's Answer

## KB Synthesis

Yes. CREATENEWVERSION preserves all cross-document I-address references in the version's POOM, maintaining the transclusion chain.

## Mechanism

`docreatenewversion` calls `docopyinternal`, which calls `insertspanf` with the source document's I-spans as direct parameters — no new I-addresses are allocated [ST-VERSION, Finding 0077]. The postcondition is:

```
poom(new_version) = { (v, i) ∈ poom(source) | v.subspace = 1 }
```

This projection copies **all** text-subspace V→I mappings from the source POOM verbatim — including I-addresses that originated in third-party documents via prior transclusion [ST-VERSION-CREATE, Finding 0046].

## Empirical Confirmation

[INT-VERSION-TRANSCLUSION, Finding 0032] provides the concrete example:

```
Doc A: "Hello"       (I-addresses α₁..α₅, native to A)
Doc B: "Hello world" (α₁..α₅ transcluded from A, β₁..β₆ native to B)
Version of B:        (same α₁..α₅ and β₁..β₆)

compare_versions(Version_of_B, A) → "Hello" shared (via α₁..α₅)
```

The version inherits both native B content and cross-document A content. The `homedoc` provenance field in POOM crums correctly records that α₁..α₅ originated in A, not B — but this does not prevent them from being copied [INV-IADDR-PROVENANCE].

## Invariant Basis

This behavior follows from [INV-TRANSITIVE-IDENTITY]: identity is preserved transitively through version chains. Since VERSION operates by sharing (not copying) I-addresses, and transclusion also shares I-addresses, mixed chains of versioning and transclusion all reduce to the same mechanism. The version becomes another document sharing those I-addresses, enabling the same link discovery and compare_versions results as the original [INT-LINK-VERSION, Finding 0046].

## One Caveat

CREATENEWVERSION copies **only the text subspace (1.x)**. Any link-subspace entries (2.x) from the source POOM are not reproduced in the version's POOM [ST-VERSION-CREATE, Finding 0043]. However, links remain **discoverable** from the version via the spanfilade's I-address index, because the shared text I-addresses are indexed there. The transclusion chain for text content is fully preserved; the version simply has no link-subspace POOM entries of its own.

## Code Exploration

I now have everything I need for a complete, citation-grounded answer. Let me synthesize the full trace.

---

## Answer: Does CREATENEWVERSION Preserve Cross-Document I-Address References?

**Short answer: Yes — the I-addresses are faithfully copied into the new version's POOM. The transclusion chain is structurally intact. However, one piece of provenance metadata (the POOM crum's `homedoc` field) is lost — the same loss that occurs during a plain COPY operation.**

---

### 1. Entry Point: `docreatenewversion` [do1.c:260–299]

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr,
                        typeisa *wheretoputit, typeisa *newisaptr)
{
    ...
    createorglingranf(taskptr, granf, &hint, newisaptr);  // allocate new doc address

    doretrievedocvspanfoo (taskptr, isaptr, &vspan);      // get source doc V-extent

    vspec.next = NULL;
    vspec.itemid = VSPECID;
    movetumbler(isaptr, &vspec.docisa);    // source doc ISA
    vspec.vspanset = &vspan;

    addtoopen(newisaptr, user, TRUE, WRITEBERT);
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // copy
    logbertmodified(newisaptr, user);
    doclose(taskptr, newisaptr, user);
}
```

The crucial detail is `movetumbler(isaptr, &vspec.docisa)` at [do1.c:287] — the vspec names the **source document** as the place to look up V-addresses, not the new version. Then `docopyinternal` is called with that vspec.

---

### 2. Getting the Source V-Extent: `doretrievedocvspanfoo` [do1.c:301–309]

This calls `retrievedocumentpartofvspanpm` [orglinks.c:155–162]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge */
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This reads the root POOM crum's displacement and width in V-space. Per Finding 0043, this returns the **text subspace** (starting at V ≈ 1.0), not the link subspace (0.x). So only text-subspace POOM entries are copied.

---

### 3. V-Address to I-Address Conversion: `specset2ispanset` [do2.c:14–46]

`docopyinternal` [do1.c:66–82] calls:

```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
```

This converts the vspec `{docisa=sourceDoc, vspanset=V-range}` to raw I-spans by walking the source document's POOM:

```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)
```

`vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d` [retrie.c:229]:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, ...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson(...), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

Each leaf crum in the source POOM within the V-range is visited. `context2span` [context.c:176–212] then extracts its I-coordinate:

```c
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);  // I-address from crum
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
foundspanptr->itemid = index2itemid(idx2, context);  // ISPANID
```

**Key**: The I-address extracted here is **whatever I-address was stored in that POOM crum** — including cross-document I-addresses from transcluded content. If document A's text (I-address space `1.1.0.1.0.1.3.x`) was COPYied into document B, then document B's POOM has crums mapping B's V-positions → A's I-addresses. `specset2ispanset` on B faithfully extracts those I-addresses. The result `ispanset` is a list of ISPANID items carrying A's I-addresses.

---

### 4. Storing into the New Version's POOM: `insertpm` [orglinks.c:75–134]

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset)
{
    for (; sporglset; sporglset = ...) {
        unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
        movetumbler (&lstream, &crumorigin.dsas[I]);   // I-address from source POOM
        movetumbler (vsaptr,   &crumorigin.dsas[V]);   // new V-position in version
        ...
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
        tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
    }
}
```

The I-addresses from the source POOM (including any cross-document I-addresses) are directly stored in the new version's POOM crums at new V-positions. **The transclusion chain is preserved at the I-address level.**

---

### 5. What Is Lost: The `homedoc` Field

`unpacksporgl` [sporgl.c:178–203] handles two item types:

```c
if (itemid == ISPANID) {
    movetumbler (&ispan->stream, streamptr);
    movetumbler (&ispan->width,  widthptr);
    tumblerclear (&infoptr->homedoc);     // ← homedoc zeroed out
} else if (itemid == SPORGLID) {
    movetumbler (&sporgl->sporglorigin,  streamptr);
    movetumbler (&sporgl->sporglwidth,   widthptr);
    movetumbler (&sporgl->sporgladdress, &infoptr->homedoc);  // ← source doc preserved
}
```

Because `specset2ispanset` returns ISPANID items (not sporgls), the `homedoc` field in each new POOM crum is cleared to zero. The new version's POOM crum says "this I-address is here" but not "this I-address originally came from document X."

This is not unique to CREATENEWVERSION — regular `docopy` [do1.c:45–65] follows the identical code path and loses homedoc in the same way.

---

### 6. Spanfilade: A Different Story for homedoc

In `insertspanf` [spanf1.c:26–29]:

```c
if (itemid == ISPANID) {
    movetumbler (isaptr, &linfo.homedoc);  // homedoc = DESTINATION doc (new version)
}
```

When `docopyinternal` calls `insertspanf(..., docisaptr, ispanset, DOCISPAN)`, `isaptr` is the **new version's ISA**. So the spanfilade records the new version as the document containing those I-spans. This is correct for link discovery: it allows `find_links` to find links through the new version's content.

---

### 7. Net Effect on Transclusion

Suppose the content chain is:

```
PermascrollDoc A (I-address X) 
  → COPYied into DocB (DocB POOM: V=p → I=X, homedoc=0)
  → CREATENEWVERSION(DocB) → DocC (DocC POOM: V=p' → I=X, homedoc=0)
```

After CREATENEWVERSION:

| Property | Preserved? | Mechanism |
|---|---|---|
| I-address X is in DocC's POOM | **YES** | `context2span` extracts it; `insertpm` stores it |
| Content retrievable via X | **YES** | Granfilade content at X is unchanged |
| `find_links` works on DocC's transcluded content | **YES** | Spanfilade records `(DocC, X)` via `insertspanf` |
| `compare_versions(DocB, DocC)` finds shared text | **YES** | Both POOMs map to same I-addresses at X |
| POOM crum `homedoc` records "came from DocA" | **NO** | `unpacksporgl` clears it for ISPANID items |
| Original-source provenance distinguishable in POOM | **NO** | Same loss as plain COPY |

---

### 8. Conclusion

**CREATENEWVERSION faithfully preserves cross-document I-addresses in the new version's POOM.** The code path `docreatenewversion` → `doretrievedocvspanfoo` → `docopyinternal` → `specset2ispanset` → `context2span` → `insertpm` extracts the literal I-addresses from every POOM crum in the source document's text subspace and stores them verbatim in the new version's POOM. Since these I-addresses include any cross-document references from prior transclusions, the content identity chain — the essential property of Xanadu transclusion — is intact.

The one thing that is NOT carried through is the `homedoc` field in the POOM bottom crums (`type2dcbc.c2dinfo.homedoc`), which is cleared to zero by `unpacksporgl` [sporgl.c:183] for all ISPANID items. This field would otherwise record "this I-address came from document X." However, this loss is identical to what occurs during a plain COPY operation, and it does not break the semantics of content identity, link discovery, or version comparison — all of which operate on the I-address values themselves, not on the homedoc field in the POOM. The spanfilade (`insertspanf`, spanf1.c:29) compensates by recording the new version as the containing document, enabling link discovery through the version's content.

---

## Question 16 [gregory]

> Does CREATENEWVERSION copy the type subspace (`3.x`) entries from the source POOM, or is only text subspace (`1.x`) copied — and if type entries exist, what happens to them?

### Gregory's Answer

## KB Synthesis

## CREATENEWVERSION and the Type Subspace (3.x)

### What the KB says directly

**[ST-VERSION-CREATE, Finding 0043]** establishes the mechanism precisely. CREATENEWVERSION calls `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm`, which reads only two values from the POOM root:

- `cdsp.dsas[V]` — displacement pointing to the **text subspace start at position 1**
- `cwid.dsas[V]` — width of the **text region only**

The resulting vspan covers `[1.something, 1.something + text_width)`. Both the link subspace and the type endpoint subspace lie outside this range.

**[FC-SUBSPACE, Finding 0054 / Finding 0038]** defines the three-subspace structure:
- `1.x` — text content (digit-0 = 1)
- `2.x` — link orgl references (digit-0 = 2, sometimes displayed as `0.x`)
- `3.x` — link **type** endpoint references (digit-0 = 3), constructed by `setlinkvsas()` which hardcodes digit-0 = 3 for type endpoints

The KB explicitly confirms for the link subspace (`2.x`) that it is not copied **[ST-VERSION-CREATE, Finding 0046]**:

> "CREATENEWVERSION copies ONLY the text subspace (V-dimension 1.x) from the source document's POOM, not the link subspace (2.x)."

### Extension to 3.x

The type subspace (`3.x`) is excluded by the same mechanism as the link subspace (`2.x`): both fall outside the vspan that `retrievedocumentpartofvspanpm` returns. The function performs no special handling for either non-text subspace — it simply returns the root's V-displacement and width, which covers only text.

Concretely: after CREATENEWVERSION, the version's POOM contains no entries with V-position digit-0 = 2 (links) or digit-0 = 3 (type endpoints). The version's vspanset shows only text spans.

### What happens to type entries

The type endpoint entries in the source document's POOM record that a link's type reference lives at `3.x` in that document's V-stream. The version does not inherit these POOM entries. However — as with link discoverability generally **[INT-LINK-TRANSCLUSION, Finding 0043]** — type endpoints that are part of links discoverable via I-address intersection will still be discoverable through the **spanfilade** (I-address based search), not through POOM structure.

### Caveat

The KB has no direct finding that tested type subspace copying specifically in CREATENEWVERSION. The conclusion follows from the mechanism (the same code path that excludes `2.x` necessarily excludes `3.x`), not from an experiment that directly targeted `3.x` entries. If type entries behave differently, it would require either a separate internal path or a modification to `retrievedocumentpartofvspanpm` not described in any finding.

### Summary

| Subspace | Contents | Copied by CREATENEWVERSION? |
|----------|----------|---------------------------|
| `1.x` | Text content | **Yes** |
| `2.x` | Link orgl references | **No** (confirmed [Finding 0043, 0046]) |
| `3.x` | Link type endpoint references | **No** (same mechanism, not directly tested) |

## Code Exploration

Now I have everything I need to give a complete, code-grounded answer.

---

## Answer: CREATENEWVERSION and the Type Subspace

### 1. Premise Correction: There Is No `3.x` in Document POOMs

The `3.x` V-subspace does **not exist in document POOMs**. It exists only in **link POOMs** (the internal ORGLs for link objects). The V-space in document POOMs is:

| V-address | Subspace | Content |
|-----------|----------|---------|
| `1.x` | Text subspace | Permascroll I-addresses (character identity) |
| `2.x` | Link subspace | Link orgl ISAs (link object references) |

The `3.x` subspace belongs to **link POOMs only**, where it holds the third-endpoint (type/annotation) sporgl data. This is set up in `setlinkvsas` [do2.c:169-183]:

```c
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // from-end at 1.1 — in LINK POOM
tumblerincrement (tovsaptr,   0, 2, tovsaptr);    // to-end at 2.1   — in LINK POOM
tumblerincrement (threevsaptr, 0, 3, threevsaptr); // type-end at 3.1 — in LINK POOM
```

These are written into the **link POOM** via `insertendsetsinorgl` [do2.c:130]. `CREATENEWVERSION` never touches link POOMs.

---

### 2. What `CREATENEWVERSION` Actually Copies

The call chain in `docreatenewversion` [do1.c:260-299]:

```c
// Step 1: Get the source document's V-extent
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {  // do1.c:281
    return FALSE;
}

// Step 2: Build vspec spanning the full V-range of the source
vspec.docisa = *isaptr;        // source document ISA
vspec.vspanset = &vspan;       // covers [cdsp.dsas[V], cdsp.dsas[V] + cwid.dsas[V]]

// Step 3: Copy everything in that V-range to the new document
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // do1.c:293
```

`doretrievedocvspanfoo` calls `retrievedocumentpartofvspanpm` [orglinks.c:155-162]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->stream = ((typecuc *) orgl)->cdsp.dsas[V];  // root V-start
    vspanptr->width  = ((typecuc *) orgl)->cwid.dsas[V];  // root V-width (FULL extent)
    return (TRUE);
}
```

This returns the **entire** V-extent of the source POOM root — both the `1.x` (text) and `2.x` (link reference) subspaces — with **no filtering whatsoever**. The author marked it `/* this is a kluge*/` and `doretrievedocvspanfoo` itself is labeled `/* this routine is a kluge not yet kluged*/` [do1.c:302] — meaning the intended filtering was never implemented.

`docopyinternal` [do1.c:66-82] then calls `specset2ispanset` [do2.c:14] → `vspanset2ispanset` → `permute` [orglinks.c:404], which walks the source POOM and returns I-space spans for **all crums** — both text I-spans (permascroll addresses) and link-ISA I-spans.

`insertpm` [orglinks.c:75-134] then packs all those I-spans **sequentially** into the new document POOM, starting at `vsaptr` = `vspan.stream` (the source's `cdsp.dsas[V]`, typically `1.1`):

```c
for (; sporglset; sporglset = sporglset->next) {
    movetumbler (vsaptr, &crumorigin.dsas[V]);   // place at current V
    insertnd (...);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // advance V by content width
}
```

---

### 3. Concrete Effect: Link References Re-packed into 1.x

Confirmed by golden test `version_copies_link_subspace.json` and `version_copies_what.json`:

**Source document** ("Text with link", 14 chars + one link):
- `retrieve_vspanset` → `[{start:"0", width:"0.1"}, {start:"1", width:"1"}]`
- Multi-story vspan: both 1.x (text) and 2.x (link reference)

**Versioned document** (after `CREATENEWVERSION`):
- `retrieve_vspanset` → `[{start:"1.1", width:"0.15"}]`
- **Single 1-story span**: 15 items starting at `1.1` = 14 text chars + 1 link ISA, all packed together

The link reference — which was at V = `2.1` in the source — is placed at V = `1.15` (immediately after the text) in the version. The version POOM becomes 1-story; the link ISA ends up embedded in what looks like the text subspace range.

From `version_copies_what.json`, `retrieve_contents` on the version returns:
```json
["Parent text with link", "1.1.0.1.0.1.0.2.1"]
```
The second entry `"1.1.0.1.0.1.0.2.1"` is the link ISA, confirming the link reference was copied and is retrievable at a `1.x`-region V-address in the version.

`find_links` still returns 1 for the version — link discovery works because `docopyinternal` also calls `insertspanf` [do1.c:79], registering the link ISA's I-address in the spanfilade under the new document.

---

### 4. Summary

| What | Source POOM | Version POOM |
|------|-------------|--------------|
| Text content | V = `1.1` to `1.N` | V = `1.1` to `1.N` (same) |
| Link references | V = `2.1`, `2.2`, … | V = `1.(N+1)`, `1.(N+2)`, … (repacked contiguously) |
| `3.x` entries | **Do not exist in document POOMs** | **Not applicable** |
| Link POOM `3.x` (type endpoint) | In link orgl, V = `3.1` | **Not touched by CREATENEWVERSION** |

**The direct answer:**

- `CREATENEWVERSION` copies the **full V-extent** of the source POOM — not just `1.x` (text) — because `retrievedocumentpartofvspanpm` [orglinks.c:155] is a self-admitted "kluge" that returns the entire root width without subspace filtering.
- `2.x` (link reference) entries **are** copied — packed sequentially after text in the new POOM.
- `3.x` entries **do not exist in document POOMs**. They live only in link POOMs (set via `setlinkvsas` [do2.c:177-181], written via `insertendsetsinorgl` [do2.c:130]), which `CREATENEWVERSION` does not process.
- If a document POOM hypothetically contained `3.x` entries, they would be copied (with no filtering), but this cannot occur through the normal API since only `TEXTATOM` (1) and `LINKATOM` (2) atom types are defined [xanadu.h:145-146] and link references are placed at `2.x` via `findnextlinkvsa` [do2.c:151].

---

## Question 17 [gregory]

> When a non-owner versions a document, the version is allocated under the non-owner's account — does the version's POOM still use the original document's I-addresses, or are fresh I-addresses allocated under the non-owner's I-address range?

### Gregory's Answer

## KB Synthesis

The version's POOM always uses the **original document's I-addresses**. Fresh I-addresses are not allocated regardless of ownership. The ownership distinction affects only the document address allocation, not the content.

## The two-step decomposition

`CREATENEWVERSION` performs exactly two effects [ST-VERSION, Finding 0077]:

1. **Document address allocation**: calls `createorglingranf` with a DOCUMENT hint → `findisatoinsertnonmolecule` allocates a new document address
2. **Content copy**: calls `docopyinternal` → `insertspanf`, which records the source's existing I-spans without any call to `findisatoinsertgr` for content

These two steps are independent. Ownership affects only step 1.

## What ownership changes

For an **owned** document, `makehint(DOCUMENT, DOCUMENT, ...)` allocates the version as a child of the source document (e.g., `1.1.0.1.0.1` → `1.1.0.1.0.1.1`) [SS-VERSION-ADDRESS, Finding 0068].

For an **unowned** document, `makehint(ACCOUNT, DOCUMENT, ...)` allocates the version under the creating user's account instead (e.g., under `1.1.0.2.0.1`) [SS-VERSION-ADDRESS, Finding 0068].

The I-address subspace within a document's content region is determined by the document's own address (e.g., `doc.3.x` for text, `doc.2.x` for links). So the non-owner's version has a different document address, but this is a document-structure address, not a content I-address.

## What ownership does NOT change

The content copy via `docopyinternal` always operates on the source document's existing V-spans → I-spans. No `findisatoinsertgr` call occurs [ST-VERSION, Finding 0077]. The postcondition is identical regardless of ownership:

```
ispans(new_version) = ispans(source_doc)  immediately after VERSION
```

This is confirmed by [FC-GRANF-ON-VERSION]: CREATENEWVERSION does not modify the content portion of the granfilade. The new document address is added to the document granfilade, but zero content I-addresses are allocated.

## Consequence for content identity

Because the version shares the source's I-addresses, `compare_versions`, `find_links`, and `find_documents` all operate on the shared I-addresses identically whether the versioning user owns the document or not [INV-TRANSITIVE-IDENTITY, INT-LINK-VERSION]. A non-owner's version inherits full content identity from the source — it can discover the same links and participates in the same comparison relationships.

**Summary**: The non-owner's version POOM uses the original document's I-addresses. The ownership check [SS-VERSION-ADDRESS, Finding 0068] is a pure address-allocation policy; the content copy mechanism [ST-VERSION-CREATE, ST-VERSION] is ownership-invariant.

## Code Exploration

I now have enough to give a complete, code-cited answer. Let me synthesize the full execution trace.

---

## Answer

### The premise needs correcting first

The question states "the version is allocated under the non-owner's account." The code does **not** do this. Let me show what actually happens, then address the POOM I-address question.

---

### Step 1: The FEBE handler always passes `originaldocisa` as `wheretoputit`

**`fns.c:289-300`:**
```c
void createnewversion(typetask *taskptr)
{
    typeisa originaldocisa, newdocisa;
    if (
       getcreatenewversion (taskptr, &originaldocisa)
    && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
```

Both the first argument (`isaptr`) and second argument (`wheretoputit`) are `&originaldocisa`. The caller never provides a separate account address for the non-owner.

---

### Step 2: The ownership branch in `docreatenewversion`

**`do1.c:268-276`:**
```c
/* ECH 7-13 introduced test for ownership to do right thing for explicit creation
   of new version of someone else's document */
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    /* This does the right thing for new version of someone else's document, as it
       duplicates the behavior of docreatenewdocument */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

`isthisusersdocument` is defined in `socketbe.c:197-201` (and `be.c:171-176`) as:
```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &(player[user].account));
}
```

And `tumbleraccounteq` (`tumble.c:38-70`) does a prefix match stopping when it finds two consecutive zeros in the "account" argument. For a non-owner: `tumbleraccounteq(originaldocisa, currentUser.account)` returns FALSE because the account prefixes differ.

**For the non-owner path:** the hint is `ACCOUNT, DOCUMENT` with `hintisa = wheretoputit = originaldocisa` (the **original document's full ISA**, not the current user's account).

---

### Step 3: Where the new ISA is actually allocated

`createorglingranf` → `createorglgr` → `findisatoinsertgr` (**`granf2.c:130-156`**) calls `findisatoinsertnonmolecule` for non-ATOM types.

**`granf2.c:203-242`:**
```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
    // ACCOUNT != DOCUMENT → depth = 2
    hintlength = tumblerlength (&hintptr->hintisa);
    // hintisa = originaldocisa, e.g. length 4

    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
    ...
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    ...
    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        /* first child */
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
        // isaptr = hintisa + 1 at depth=2 position
        // e.g., originaldocisa.0.1
    }
}
```

With `hintisa = originaldocisa` (e.g., `1.1.0.1.0.1`) and `depth = 2`, the new version's ISA is `originaldocisa.0.1`, `originaldocisa.0.2`, etc.

**Correction to the premise:** The non-owner's version is NOT allocated under the non-owner's account. It is allocated **under the original document's ISA** — i.e., still within the original owner's account namespace. The comment "duplicates the behavior of docreatenewdocument" is only accurate in the sense that it uses the same hint type (`ACCOUNT, DOCUMENT`); the hint ISA used is the original doc's address, not the current user's account.

---

### Step 4: The POOM content — do I-addresses come from the original or are they fresh?

After allocating the new ISA, `docreatenewversion` builds the content:

**`do1.c:281-296`:**
```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {
    return FALSE;
}

vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);     // docisa = ORIGINAL document's ISA
vspec.vspanset = &vspan;               // V-span from original doc's POOM root

addtoopen(newisaptr, user, TRUE, WRITEBERT);
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

`doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm` (**`orglinks.c:155-162`**) reads the V-space extent straight from the original POOM's root node:
```c
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
```

Then `docopyinternal` (**`do1.c:66-82`**):
```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // (1)
&& findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED) // (2)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)       // (3)
```

**(1) `specset2ispanset` — `do2.c:14-46`:**
```c
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    if (!(
      findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
    && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))))
```

`specset->docisa` = `originaldocisa`. So `docorgl` is the **original document's POOM**. `vspanset2ispanset` walks that POOM to convert V-addresses → I-addresses (permascroll spans). The result is an `ispanset` of **`ISPANID` items** containing the original document's permascroll addresses.

**(2) `findorgl`** returns the new version's POOM (target).

**(3) `insertpm` — `orglinks.c:75-134`:**
```c
for (; sporglset; sporglset = ...) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);  // I-address from original doc
    movetumbler (&lwidth, &crumwidth.dsas[I]);
    movetumbler (vsaptr, &crumorigin.dsas[V]);    // V-address from original doc
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
}
```

`unpacksporgl` for `ISPANID` items (**`sporgl.c:180-183`**):
```c
if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglptr)->stream, streamptr);
    movetumbler (&((typeispan *)sporglptr)->width, widthptr);
    tumblerclear (&infoptr->homedoc);   // homedoc = zero
}
```

The I-coordinates (`crumorigin.dsas[I]`, `crumwidth.dsas[I]`) are copied **verbatim** from the original document's permascroll I-spans. No new I-addresses are generated. The POOM crums of the new version store:
- `cdsp.dsas[I]` = original permascroll address
- `cdsp.dsas[V]` = same V-address as in the original document
- `c2dinfo.homedoc` = zero (since `ISPANID` items produce zero homedoc)

---

### Summary

**On ISA allocation:** The question's premise is incorrect. In the non-owner path (`fns.c:296` passes `&originaldocisa` as `wheretoputit`), `docreatenewversion` uses `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` with `hintisa = originaldocisa`. `findisatoinsertnonmolecule` then allocates the new version's granfilade node at `originaldocisa.0.1` (or `.0.2`, etc.) — **still within the original owner's account namespace**, not the non-owner's.

**On POOM I-addresses:** The new version's POOM uses **the original document's I-addresses verbatim**. The path is:
1. `doretrievedocvspanfoo` reads the original POOM's V-extent [orglinks.c:155-162]
2. `specset2ispanset` uses the original POOM to map V → I, yielding `ISPANID` items [do2.c:34-38]
3. `insertpm` inserts these I-spans unchanged into the new POOM [orglinks.c:105-130]

No fresh I-addresses are allocated for the version's content. This is Xanadu's fundamental transclusion principle: content lives in the permascroll once, and documents point into it. Creating a version of a document — regardless of ownership — copies the POOM structure that references the same permascroll I-addresses. The `homedoc` field on the POOM crums is zero for content (vs. non-zero for link endpoint mappings, which use `SPORGLID` items through `specset2sporglset`).

---

## Question 18 [gregory]

> If you INSERT new text into a version and then call FINDDOCSCONTAINING with a specset from the original, does the original appear in the results — and does the version also appear because of the shared I-addresses from the initial copy?

### Gregory's Answer

## KB Synthesis

## FINDDOCSCONTAINING after INSERT into a version

**Short answer:** Both the original and the version appear.

---

### Step 1: Setup after CREATENEWVERSION

When `CREATENEWVERSION(D)` runs, `docopyinternal` is called, which invokes `insertspanf(..., DOCISPAN)`. This creates DOCISPAN entries mapping the shared I-addresses (α₁..αₙ from the original) to the new version V — the same mechanism as an ordinary COPY. [ST-VERSION, Finding 0077; SS-DOCISPAN, Finding 0036]

So immediately after version creation, the spanfilade contains:
```
α₁..αₙ → {D}    (from original INSERT)
α₁..αₙ → {V}    (from CREATENEWVERSION via docopyinternal)
```

### Step 2: INSERT new text into V

INSERT into V allocates fresh I-addresses β₁..βₘ — strictly greater than all existing addresses in the granfilade — and creates new DOCISPAN entries β₁..βₘ → {V}. [ST-INSERT, Findings 0033, 0036; INV-MONOTONIC] These are **new** addresses with no relationship to α₁..αₙ.

### Step 3: Query FINDDOCSCONTAINING with specset from original

The specset from the original resolves to I-addresses α₁..αₙ. The spanfilade now contains entries for α₁..αₙ pointing to both D and V.

- **Original D appears** — DOCISPAN entries α₁..αₙ → D were created when content was first inserted into D.
- **Version V appears** — DOCISPAN entries α₁..αₙ → V were created by `docopyinternal` during CREATENEWVERSION.
- **New text in V (β₁..βₘ)** has no effect on this query — those I-addresses are not referenced by the original's specset.

### Why this is permanent

The spanfilade is write-only; no deletion function exists. [INV-SPANF-WRITE-ONLY, Finding 0057] Even if content were deleted from D or V, both would continue to appear in FINDDOCSCONTAINING for α₁..αₙ. [INV-IADDRESS-PERMANENT, Finding 0023]

---

**Concrete example:**
```
INSERT "Hello" into D   →  α₁..α₅ → D   (DOCISPAN created)
CREATENEWVERSION(D) → V →  α₁..α₅ → V   (DOCISPAN created via docopyinternal)
INSERT "World" into V   →  β₁..β₅ → V   (fresh addresses, new DOCISPAN)

FINDDOCSCONTAINING(specset from D covering "Hello"):
  Queries α₁..α₅ in spanfilade
  → returns {D, V}

FINDDOCSCONTAINING(specset from V covering "World"):
  Queries β₁..β₅ in spanfilade
  → returns {V} only (original has no entry for β addresses)
```

## Code Exploration

I now have everything needed. Let me compile the complete code-traced answer.

---

## Answer: FINDDOCSCONTAINING After Version INSERT

**Both the original and the version appear in the results.** Here is the full trace.

---

### Step 1 — INSERT text into original `d`

`doinsert` [do1.c:87–123]:

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    ...
    return (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy(taskptr, docisaptr, vsaptr, ispanset));
}
```

- `inserttextingranf` allocates fresh I-addresses — call them **I₁** — in the granfilade for the new bytes.
- `docopy` [do1.c:45–65] calls:
  - `insertpm` → stores (V-address → I₁) in **d's POOM**
  - `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` → stores entry **(d | DOCISPAN, I₁)** in the global spanfilade

---

### Step 2 — CREATENEWVERSION(d) → d'

`docreatenewversion` [do1.c:260–298]:

```c
doretrievedocvspanfoo(taskptr, isaptr, &vspan);   // gets d's text vspan
vspec.vspanset = &vspan;
...
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // newisaptr = d'
```

- `doretrievedocvspanfoo` [do1.c:301–309] calls `retrievedocumentpartofvspanpm` [orglinks.c:155–162], which reads `cdsp.dsas[V]` and `cwid.dsas[V]` — the text subspace span of d's root crum.
- `docopyinternal` [do1.c:66–82] then:
  - `specset2ispanset` → `vspanset2ispanset` → `permute` [orglinks.c:397–422]: walks d's POOM to translate those V-addresses to their stored I-addresses (I₁)
  - `insertpm` → stores (V-address → I₁) in **d''s POOM** (same I-addresses, different document)
  - `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` where `docisaptr = newisaptr` (d') → stores **(d' | DOCISPAN, I₁)** in the spanfilade

After CREATENEWVERSION, the spanfilade contains:

| Entry | Meaning |
|-------|---------|
| (d \| DOCISPAN, I₁) | original's content |
| (d' \| DOCISPAN, I₁) | version's shared I-addresses |

---

### Step 3 — INSERT new text into d'

`doinsert` [do1.c:87–123] is called on d':

- `inserttextingranf` allocates **NEW** I-addresses **I₂** for the new bytes (completely fresh allocation, nothing shared with d).
- `docopy` → `insertpm`: maps V-address → I₂ in d''s POOM
- `docopy` → `insertspanf`: stores **(d' | DOCISPAN, I₂)** in the spanfilade

After the insert, the spanfilade contains:

| Entry | Meaning |
|-------|---------|
| (d \| DOCISPAN, I₁) | original |
| (d' \| DOCISPAN, I₁) | version, shared from CREATENEWVERSION |
| (d' \| DOCISPAN, I₂) | version's new, unique content |

---

### Step 4 — FINDDOCSCONTAINING with d's specset

`dofinddocscontaining` [do1.c:15–23]:

```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
    return (
       specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
    && finddocscontainingsp(taskptr, ispanset, addresssetptr));
}
```

**Step 4a — V → I conversion.**  
`specset2ispanset` [do2.c:14–46] sees a VSPECID for d. It calls `vspanset2ispanset` → `permute` to walk d's POOM and translate d's V-addresses into their I-addresses. Since the specset names content from d's text subspace, it resolves to **I₁**.

**Step 4b — spanfilade search.**  
`finddocscontainingsp` [spanf1.c:151–188]:

```c
tumblerincrement(&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement(&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted(
        (typecuc*)spanf,
        &docspace,   ORGLRANGE,   // restrict ORGLRANGE to DOCISPAN band
        ispanset,    SPANRANGE,   // restrict SPANRANGE to I₁
        NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler(&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler(&docid, &document.address);   // strip DOCISPAN prefix
        ...
    }
}
```

This queries: *find all spanfilade crums where ORGLRANGE is in the DOCISPAN band AND SPANRANGE overlaps I₁.*

Hits:
- **(d | DOCISPAN, I₁)** — `beheadtumbler` strips the DOCISPAN prefix → **d** is added to results
- **(d' | DOCISPAN, I₁)** — `beheadtumbler` → **d'** is added to results

The entry (d' | DOCISPAN, I₂) does **not** hit because I₂ is not in the query's ispanset.

---

### Golden Test Confirmation

The exact scenario is captured in `golden/discovery/find_documents_versions.json`:

```json
{"op": "create_document", "result": "1.1.0.1.0.1"},
{"op": "insert", "text": "Original content"},
{"op": "create_version", "result": "1.1.0.1.0.1.1"},
{"op": "create_version", "result": "1.1.0.1.0.1.2"},   ← version2
{"op": "create_version", "result": "1.1.0.1.0.1.3"},
{"op": "insert", "doc": "version2", "text": " plus v2 additions"},  ← new text in version
{"op": "find_documents", "result": [
    "1.1.0.1.0.1",      ← original ✓
    "1.1.0.1.0.1.1",    ← version1 ✓
    "1.1.0.1.0.1.2",    ← version2 ✓  (even though it has extra text)
    "1.1.0.1.0.1.3"     ← version3 ✓
]}
```

The version chain test `golden/discovery/find_documents_version_chain.json` further confirms: searching v1 for "Base content" finds v1, v2 (which had " plus v2" inserted), and v3 (which had " plus v3" inserted) — all three appear because all share I₁.

---

### Conclusion

**Yes — both the original and the version appear.**

The mechanism is the spanfilade's DOCISPAN index. When `CREATENEWVERSION` runs, `docopyinternal` [do1.c:66–82] writes a second DOCISPAN entry into the spanfilade pointing the version's ISA at the same I-addresses the original holds. That entry persists permanently — the spanfilade is never pruned. `FINDDOCSCONTAINING` [spanf1.c:151–188] searches this index directly by I-address range, so it finds every document whose DOCISPAN entry overlaps the queried I-span, regardless of whether those documents have since had additional content inserted.

The new text inserted into the version gets **fresh I-addresses** (a new `inserttextingranf` allocation), which are not in the original's specset, so they are irrelevant to this particular query — but they would appear if you queried with the version's specset for the new content.

---

## Question 19 [gregory]

> Was the version model intended to support eventual merging of divergent versions back together, or was the design philosophy that versions diverge permanently and are compared (SHOWRELATIONOF2VERSIONS) but never converged?

### Gregory's Answer

## KB Synthesis

The KB is unambiguous on this: the version model was designed for **permanent divergence with comparison**, not convergence. Merging is explicitly a front-end semantic concern.

## Evidence from the KB

**No merge operation exists.** The backend provides no primitive for combining two versions. [EC-CONFLICT-COPY-NO-MERGE] states this explicitly: "Changes made in different sessions are NOT merged... This is a deliberate design boundary, not a bug." [SS-SESSION-STATE]

**Version creation is a branching primitive, not a merge precursor.** [ST-VERSION-CREATE] (Finding 0032) defines CREATENEWVERSION as allocating a new document that starts with shared I-addresses and then diverges independently. [FC-VERSION-ISOLATION] confirms: "Once a version is created, it is a fully independent document... Neither affects the other."

**The access control model explicitly redirects conflicts into divergence.** [INT-BERT-VERSION] states: "access denial is not an error but a redirect into the version-branching workflow." When you cannot write to a document because someone else holds WRITEBERT, the protocol instructs you to create a version — not to wait for a merge opportunity. [PRE-OPEN-DOC]

**SHOWRELATIONOF2VERSIONS is comparison-only.** [SS-COMPARE-VERSIONS] defines the operation as returning pairs of V-spans where documents share I-address ranges. It identifies *what is common* between two documents. It performs no state mutation. [ST-COMPARE-VERSIONS]

## The Front-End Merge Path

The KB does reveal a composable merge capability, but it is entirely at the application layer:

1. Use SHOWRELATIONOF2VERSIONS to identify which content is shared (common origin)
2. Use VCOPY to selectively pull content from one version into another, which preserves I-address identity [ST-VCOPY], [INV-IADDR-IMMUTABILITY]
3. The result is a new document that shares identity with both predecessors, comparable to either via SHOWRELATIONOF2VERSIONS

[INV-TRANSITIVE-IDENTITY] and [INT-VERSION-TRANSCLUSION] confirm that identity chains are preserved through this process — a merged document produced by VCOPY can be compared against either parent and the shared provenance is visible.

## Design Philosophy

The key architectural signal is [INV-DELETE-NOT-INVERSE] (Finding 0064/0072): "DELETE followed by INSERT of identical text does NOT restore the original document state... All I-address-indexed relationships are permanently severed." This is not a limitation to be fixed — it reflects that content history in I-space is canonical, and operations like "undo" or "merge" must be expressed through VCOPY (which preserves identity) rather than delete-then-reinsert (which discards it).

The system is designed around Nelson's principle of permanent, comparable, diverging streams rather than convergent mutable state. SHOWRELATIONOF2VERSIONS answers "what do these two documents share?" — which is the basis for human-driven or application-driven merge decisions, not an automatic confluence mechanism.

## Code Exploration

I now have all the evidence needed. Here is the full answer.

---

## Was the version model intended to support merging, or permanent divergence?

**The implemented design is: permanent divergence with comparison. Merging was not implemented, and the architectural prerequisites for it (history-tree navigation, common-ancestor lookup) were abandoned mid-development.**

Here is the evidence from the code.

---

### 1. The complete protocol has no merge operation

`requests.h` defines every operation the backend supports (40 slots):

```c
#define CREATENEWVERSION       13
#define SHOWRELATIONOF2VERSIONS 10
#define NAVIGATEONHT            9   /* disabled */
```

There is no `MERGEVERSIONS`, `CONVERGE`, `APPLYPATCH`, or any equivalent. A complete exhaustive search of all `.c` files for `merge`, `MERGE`, `converge`, `CONVERGE`, `combine` returns zero matches for any version-merging concept. The operation simply does not exist in the protocol.

---

### 2. `CREATENEWVERSION` creates a branching copy, not a tracked child

`docreatenewversion` in `do1.c:260-298`:

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    /* ECH 7-13 introduced test for ownership ... */
    if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
        makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
    } else {
        makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
    }
    createorglingranf(taskptr, granf, &hint, newisaptr);  // allocates new document ISA
    doretrievedocvspanfoo(taskptr, isaptr, &vspan);       // gets source's full content span
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // copies V→I mapping
    ...
```

The new version gets an independent `typeisa` (tumbler address). Its content is a copy of the source's V→I mapping — both documents now point to the same permascroll I-addresses for the existing text. After this, each version's V-address space evolves completely independently. There is no pointer from new version back to source; no parent-child relationship is stored anywhere in the granfilade.

---

### 3. `SHOWRELATIONOF2VERSIONS` is comparison-only, not merging

`doshowrelationof2versions` in `do1.c:428-449`:

```c
bool doshowrelationof2versions(typetask *taskptr, typespecset version1, typespecset version2, typespanpairset *relation)
{
    filter_specset_to_text_subspace(taskptr, version1);
    filter_specset_to_text_subspace(taskptr, version2);
    return
        specset2ispanset(taskptr, version1, &version1ispans, READBERT)
      && specset2ispanset(taskptr, version2, &version2ispans, READBERT)
      && intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
      && ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation);
}
```

The algorithm:
1. Convert each document's V-spans → I-spans (permascroll addresses) [`do2.c:14-46`]
2. Intersect the two I-span sets — find permascroll addresses present in both [`correspond.c:145-189`]
3. Map those shared I-addresses back to V-positions in both documents [`correspond.c:267-349`]

The result is a `typespanpairset` — a list of `(doc1_v_position, doc2_v_position, width)` triples. This answers: *which chunks in doc1 and doc2 contain content that came from the same permascroll bytes?*

This is a **read-only comparison**. It does not modify either document, does not create a merged document, and crucially does not identify what has *diverged* — only what is *shared*. Without a common ancestor, you cannot compute "A changed this, B didn't" vs. "B changed this, A didn't."

---

### 4. The history tree (`NAVIGATEONHT`) was planned but abandoned

`fns.c:236-248`:

```c
void navigateonht(typetask *taskptr)
{
#ifndef DISTRIBUTION
error (taskptr, "GACK !  (historical trace)\n");
#endif
/*
  typeisa docisa, htisa;
  typehtpath turninginstructions;
  bool getnavigateonht();
    if (getnavigateonht(taskptr, &docisa, &htisa, &turninginstructions))
       donavigateonht(taskptr, &docisa, &htisa, &turninginstructions);
*/
}
```

The implementation is entirely commented out, replaced by a `GACK` error. The operation is also disabled in safe mode at `init.c:73`:

```c
requestfns[NAVIGATEONHT] = nullfun;
```

The commented-out signature shows it would have taken a `docisa`, an `htisa` (history tree identity address), and a `typehtpath turninginstructions`. A `typehtpath` would represent navigation steps through the version lineage — the prerequisite for any three-way merge.

---

### 5. Four "ht stuff" placeholders were never filled in

Every mutating operation in `do1.c` has a stub where history-tree recording was supposed to happen:

- `do1.c:42` — `dorearrange`: `/*&& TRUE*/ /* ht stuff */`
- `do1.c:64` — `docopy`: `/*      &&  ht stuff */`
- `do1.c:69` — `docopyinternal`: `/*  typeisa htisa;      */`
- `do1.c:48` — `docopy`: `/*  typeisa htisa;      */`
- `do1.c:120-121` — `doinsert`: `/* no ht stuff here, 'cause it's taken care of in docopy */`
- `do1.c:166` — `dodeletevspan`: `/*&& TRUE*/ /* ht stuff */`

Every write operation was scaffolded to eventually record provenance in a history tree (`htisa`). None of it was ever implemented. Without these records, the backend cannot answer "which document is the parent of this one," making three-way merge impossible.

---

### 6. Why merge is structurally impossible as implemented

Three-way merge requires:
1. **A common ancestor** — to establish the base for comparison
2. **Two diffs against the base** — "what A changed" and "what B changed"
3. **A combining write operation** — produce a new document from both change sets

None of these are available:
- There is no "find parent of this document" operation
- `SHOWRELATIONOF2VERSIONS` finds *shared* content, not *differences* from a base
- There is no "create document as combination of two other documents" operation; `COPY` copies a vspan from one doc into another, but that requires the client to already know which spans to copy and where

---

### Conclusion

**The implemented design philosophy is that versions diverge permanently.** The architecture supports:

- Creating new versions (`CREATENEWVERSION`) that branch off as independent documents
- Editing each version independently (`INSERT`, `DELETEVSPAN`, `REARRANGE`, `COPY`)
- Identifying shared permascroll content between two versions (`SHOWRELATIONOF2VERSIONS`)

It does not support, and never built:

- Tracking version parentage (the `htisa` and `NAVIGATEONHT` mechanism was abandoned)
- Finding the common ancestor of two versions
- Computing what each version changed relative to a base
- Any merge operation

The `SHOWRELATIONOF2VERSIONS` operation is the capstone of the version model: it answers *which content is in common*, expressed as paired V-positions. This is a diffing/comparison tool for humans (or higher-level clients) to reason about two parallel versions. Merging, if desired, would have to be performed entirely client-side by manually issuing `COPY` operations based on the relationship data — the backend offers no guidance on *how* to combine divergent content.

This is consistent with the Xanadu philosophy of permanent content identity: the permascroll never loses content, documents accumulate rather than overwrite, and parallel versions are linked and compared rather than collapsed.

---

## Question 20 [gregory]

> After CREATENEWVERSION, if a CREATELINK is made on the original document targeting content that was copied to the version, is that new link immediately discoverable via find_links on the version through the shared I-addresses — even though the link was created after the version fork?

### Gregory's Answer

## KB Synthesis

**Yes, the link is immediately discoverable via `find_links` on the version.**

The mechanism has three independent components that combine to produce this result:

**1. The version shares I-addresses with the original**

[ST-VERSION-CREATE] (Finding 0046): CREATENEWVERSION copies text I-addresses from the source document's POOM into the new version. Immediately after the fork, both the original and the version map V-addresses to the same set of permascroll I-addresses α₁..αₙ.

**2. CREATELINK writes to the global spanf, not a per-document index**

[ST-CREATE-LINK] (Finding 0012): `docreatelink` performs three steps: creates a link orgl in granf, places the link's ISA in the document's link subspace, and indexes all link endpoints in the **global** spanf via `insertendsetsinspanf()`. The spanf is not scoped to the document where the link was created — it is a system-wide index.

**3. find_links queries the global spanf at call time by I-address intersection**

[SS-FIND-LINKS] (Finding 0028): `find_links` converts the search specset to I-addresses and searches the spanf for any link whose endpoint I-addresses intersect. The search is purely over I-space; document identity and creation ordering are irrelevant.

**Putting it together:**

After CREATELINK on the original targeting content at I-addresses α₁..αₙ, the global spanf now contains entries `α₁..αₙ → link_id`. When `find_links` is called on the version with a vspan that maps to those same I-addresses (via the version's POOM, which was copied from the original), the I-address conversion yields α₁..αₙ, the spanf lookup succeeds, and the link is returned.

The temporal ordering (link created after fork) does not matter because the spanf is queried at call time against its current state, not snapshotted at version-creation time.

This is confirmed directly by [INV-LINK-GLOBAL-VISIBILITY]: "A link created in any document is discoverable from every document in the system that shares the linked content's identity." And by [INT-LINK-VERSION] (Finding 0008): "Links added to a version are discoverable from the original document, and vice versa" — which by symmetry means links added to the original are discoverable from the version.

The one caveat: the version's own POOM contains no link subspace entries for this new link [ST-VERSION-CREATE] (Finding 0043) — the version only inherited the text subspace. But link *discoverability* via `find_links` does not depend on POOM link entries; it depends solely on shared I-addresses in the spanf index [INT-LINK-VERSION] (Finding 0046).

## Code Exploration

Now I have everything I need. Let me write the complete answer.

---

## Answer

**Yes — a link created on the original after the version fork is immediately discoverable via `find_links` on the version.** This is not accidental: the code has an intentionally disabled document-scope filter with a comment that says exactly this.

---

### Step 1: What I-Addresses Does the Version Inherit?

`docreatenewversion` [`do1.c:260-299`] does:

```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {   // get original's vspan
    return FALSE;
}
vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);         // vspec references the ORIGINAL doc
vspec.vspanset = &vspan;
...
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // copy into new version
```

`docopyinternal` [`do1.c:66-82`] then calls:
1. `specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)` — converts the vspec (original docisa + original vspan) through the original doc's POOM into a set of **I-addresses** (permascroll addresses).
2. `insertpm(taskptr, newisaptr, docorgl, vsaptr, ispanset)` — installs those I-addresses into the **new version's** POOM.
3. `insertspanf(taskptr, spanf, newisaptr, ispanset, DOCISPAN)` — registers those same I-addresses in the global spanfilade under the version's ISA.

**Result:** The version's POOM maps its V-addresses to the exact same I-addresses that the original holds for the same content. The two documents share permascroll identity for the copied text.

---

### Step 2: What Does CREATELINK Store?

`docreatelink` [`do1.c:195-221`]:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
createorglingranf (taskptr, granf, &hint, linkisaptr)           // new link orgl
&& tumbler2spanset (taskptr, linkisaptr, &ispanset)             // link's own I-address
&& findnextlinkvsa (taskptr, docisaptr, &linkvsa)               // next V in ORIGINAL
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)              // link ISA into ORIGINAL's POOM
&& specset2sporglset (taskptr, fromspecset, &fromsporglset,NOBERTREQUIRED)  // V→I for FROM
&& specset2sporglset (taskptr, tospecset, &tosporglset,NOBERTREQUIRED)      // V→I for TO
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`specset2sporglset` → `vspanset2sporglset` [`sporgl.c:35-65`]:

```c
if (!findorgl (taskptr, granf, docisa, &orgl, type))  // look up ORIGINAL's POOM
    return (NULL);
for (; vspanset; vspanset = vspanset->next) {
    vspanset2ispanset (taskptr, orgl, vspanset, &ispanset); // V → I using ORIGINAL's POOM
    ...
    movetumbler (&ispanset->stream, &sporglset->sporglorigin);  // stores I-address
    movetumbler (&ispanset->width, &sporglset->sporglwidth);
}
```

`insertendsetsinspanf` → `insertspanf` [`spanf1.c:15-54`]:

```c
movetumbler (&((typesporgl *)sporglset)->sporglorigin, &lstream);  // I-address → SPANRANGE
...
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

**The spanfilade is indexed by I-addresses on its SPANRANGE axis.** The ORGLRANGE axis stores the link ISA prefixed with the span type (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3). The `docopy` at step 4 goes into the **original doc's POOM only** — it does not touch the version.

---

### Step 3: How Does `find_links` on the Version Search?

`dofindlinksfromtothree` [`do2.c:348-353`] → `findlinksfromtothreesp` [`spanf1.c:56-103`]:

```c
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
...
if (fromvspecset)
    sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

When called with the **version's** V-spec, `specset2sporglset` uses the **version's** POOM to convert V → I. Because the version's POOM holds the same I-addresses as the original (from Step 1), it produces the **identical I-addresses**.

`sporglset2linksetinrange` [`sporgl.c:239-269`] then searches the spanfilade:

```c
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

This finds all entries in the spanfilade where:
- `SPANRANGE` overlaps with the query I-addresses, and  
- `ORGLRANGE` falls in the LINKFROMSPAN range

The link created on the original stored entries at exactly those I-addresses. The query matches.

---

### The Intentionally Disabled Filter

The only way this could fail is if the search filtered by home document. That filter exists in the code — but it is explicitly disabled:

```c
// sporgl.c:251-255
if (FALSE/*trying to kluge links followable thru versions */
    && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
} else
    infoptr = NULL;
```

The `FALSE &&` unconditionally routes to `infoptr = NULL`. The comment is unambiguous: "trying to kluge links followable thru versions." The developer tried adding homedoc filtering, then deliberately disabled it so that links remain discoverable across documents and versions sharing content identity.

Similarly, `sporglset2linkset` [`sporgl.c:227`]:

```c
if (TRUE||!homeset) {         // TRUE makes this unconditional
    nullhomeset.width.mantissa[0] = 100;   // hardcoded wide search
    homeset = &nullhomeset;
}
```

`TRUE||!homeset` overrides any orgl-range restriction with a width-100 ceiling (effectively unbounded). Finding 0069 confirmed this: orgl range filtering is a no-op.

And note how the call site in `fns.c:198` already passes `NULL` for the homeset:

```c
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
                           (typeispan*)NULL/*homeset*/, &linkset)
```

---

### Summary of the Information Flow

```
CREATENEWVERSION(original):
  original POOM: V-range → {I₁, I₂, I₃, ...}
  version  POOM: V-range → {I₁, I₂, I₃, ...}   ← same I-addresses

  spanfilade: {I₁,I₂,I₃} × DOCISPAN → original ISA  (per docopyinternal)
              {I₁,I₂,I₃} × DOCISPAN → version  ISA  (per docopyinternal)

CREATELINK on original (after fork), FROM endpoint = original's V-range:
  specset2sporglset(original V-spec) → {I₁,I₂,I₃} via original POOM
  insertspanf: {I₁,I₂,I₃} × LINKFROMSPAN → link ISA   ← written to global spanfilade

FIND_LINKS on version, query = version's V-range:
  specset2sporglset(version V-spec) → {I₁,I₂,I₃} via version POOM (same!)
  sporglset2linksetinrange: search spanfilade for {I₁,I₂,I₃} × LINKFROMSPAN
  → MATCH: link ISA found
  → link returned
```

---

### Existing Test Coverage

The golden test `version_with_links` [`golden/versions/version_with_links.json`] validates that a link created **before** the fork is discoverable in the version:
```json
{"op": "create_link", ...},
{"op": "create_version", "from": "source", ...},
{"op": "find_links", "doc": "version", "result": ["1.1.0.1.0.1.0.2.1"], "comment": "Links discovered via content identity"}
```

Finding 0007 (§4) and Finding 0026 both validate discovery via shared I-addresses. Finding 0043 confirmed that CREATENEWVERSION copies the text I-address mapping (but not the link POOM subspace), and that find_links still works via the content identity path.

**No existing golden test validates the post-fork case specifically** — where the link is created on the original *after* the version exists. The code paths are identical; only the temporal ordering differs, and the spanfilade is queried dynamically at find_links time, not statically inherited at version creation time. A new scenario (`link_created_after_fork`) would confirm this directly.

---

### Conclusion

**Yes, the link is immediately discoverable.** The spanfilade is indexed by I-addresses (permascroll positions), not by document identity or creation time. The version shares I-addresses with the original for the copied content. `find_links` on the version converts its V-addresses to those same I-addresses via its POOM, queries the spanfilade, and finds the link entry placed there by the post-fork `docreatelink`. The homedoc filter that would have blocked cross-version discovery is permanently disabled at `sporgl.c:251` with the comment "trying to kluge links followable thru versions" — confirming this is intentional Xanadu semantics.
