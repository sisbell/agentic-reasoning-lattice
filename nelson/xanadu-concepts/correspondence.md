# Correspondence

Source: Literary Machines, 2/20-2/22, 2/26, 3/13, 4/53, 4/70

## Semantic Intent

### What It Means

Correspondence is the relationship between equivalent parts across different versions or related documents. When content evolves through editing, forking, or translation, the system tracks which parts in one version match or derive from parts in another. This is not merely metadata about "what changed"—it is a structural relationship that can be queried and navigated.

Nelson treats correspondence as fundamental to meaningful comparison. Without knowing which parts correspond, you can only place two versions side by side as disconnected wholes. With correspondence tracked, the system can highlight what is the same versus what differs, allow navigation from a passage in one version directly to its counterpart in another, and enable "scrolling through any two versions to see corresponding parts."

### User Guarantee

**The system knows which parts match across versions.** When you compare two versions of a document—whether successive drafts or alternative designs—the system can show you exactly which pieces are the same and highlight what has changed. You can navigate from any part of one version directly to the corresponding part of another.

### Principle Served

Correspondence serves the core goal of **intercomparison**. Nelson argues that storing multiple versions is "not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same."

This applies across domains:
- Lawyers comparing wordings of contract drafts
- Congressmen comparing versions of bills
- Authors tracking how passages evolved between drafts
- Biologists comparing corresponding anatomical structures graphically
- Engineers viewing corresponding parts across product variants (like Boeing 747 models)

Correspondence also enables **version-spanning links**: a link to one version of a document is effectively a link to all versions, because the system can "refractively follow" the link to corresponding places in any other version.

### How Users Experience It

- Scroll through two versions simultaneously with corresponding parts aligned
- Click on a passage in one version to jump to its counterpart in another
- See highlighting of what changed versus what stayed the same
- Follow a link to an old version and have it find the same content in the current version
- Create a "counterpart link" to explicitly mark that two passages in different documents correspond

### Nelson's Words

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." (2/20)

> "The user may scroll through any two versions to see corresponding parts; and much more." (2/21)

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." (3/13)

> "The counterpart link shows that there are correspondences between two equivalent documents, sections or passages. (This has also been called a collateral or correspondence link.)" (4/53)

On the SHOWRELATIONOF2VERSIONS protocol command:
> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70)

---

## Related Concepts

| Concept | Relationship |
|---------|--------------|
| [versions](versions.md) | Correspondence tracks matching parts across versions |
| [i-space-v-space](i-space-v-space.md) | Shared Istream origin is the basis for correspondence |
| [transclusion](transclusion.md) | Transcluded content corresponds to original |
| [counterpart-link](counterpart-link.md) | Explicit link to mark correspondence between passages |
| [spans](spans.md) | Correspondence returns pairs of corresponding spans |
| [links](links.md) | Links can "refractively follow" to corresponding places |

## FEBE Operations

| Operation | How correspondence applies |
|-----------|---------------------------|
| **SHOWRELATIONOF2VERSIONS** | Core operation - returns corresponding span pairs |
| **CREATENEWVERSION** | Establishes correspondence between versions |
| **FINDDOCSCONTAINING** | Uses shared origin to find transclusions |

See [Concept-Operation Map](../concept-operation-map.md) for full mapping.
