# Versions

Source: Literary Machines, 2/13-2/22, 2/45-2/47, 3/12-3/13

## Semantic Intent

### What It Means

A version is not a copy of a document—it is a particular arrangement of content at a particular moment in time. Xanadu treats documents as evolving entities where every state is permanently accessible. When you edit, you are not destroying the old version and creating a new one; you are adding to the document's history of arrangements while the original content remains intact.

This is fundamentally different from conventional file systems where "saving" overwrites the previous state. In Xanadu, the document accumulates versions the way a braid accumulates strands: the history is structural, not just metadata.

Nelson calls this **prismatic storage**—content refracts into different versions the way light refracts through a prism. There is no "basic" or "main" version; all arrangements are equally valid views of the same underlying material. The retrieval mechanism is called **part-pounce**: you request a specific part of a specific version and it materializes instantly, constructed on-demand from stored fragments. Nelson names the complete system a **hyperfile**—a storage structure that supports not just content but its full version history and the ability to navigate through time.

### User Guarantee

**Every version you ever created still exists.** You can navigate backward through time to any previous state of your document. You can compare any two versions side by side. The system tracks what changed between versions automatically.

More precisely: you can ask for "a certain part of a certain version at a certain point in time" and receive exactly that.

### Principle Served

Versions serve multiple purposes that Nelson sees as deeply connected:

1. **Safety**: Mistakes are reversible. Nothing you do can destroy previous work.
2. **Historical backtrack**: Writers need to reconsider old choices, undo decisions, look at former states. This is fundamental to creative work.
3. **Showing commonalities**: Multiple versions of the same material (successive drafts of a novel, alternative arrangements of data) can be compared to see what is the same and what differs.

Nelson frames this as solving "the nature of creative work"—writers need to reach back to former conditions, and conventional systems fail them.

### Publishing Modified Versions

Xanadu solves the "publishing modified versions" problem through a radical approach: **modifications never damage originals**. When you publish an annotated or edited version of someone else's work, you create a new document that [windows (transcludes)](transclusion.md) the parts you keep unchanged while adding your own modifications. The original remains intact, and the system handles this by "inclusion links"—your new version includes the original by reference, not by copy.

This means:
- The original author's work is preserved exactly as they wrote it
- Your modifications exist as new material alongside the windowed original
- Readers see your version as a coherent whole
- The original still exists and can be retrieved unchanged
- Royalties flow appropriately—the original author for their content, you for yours

Nelson calls this a "whole new pluralistic publishing form." Anyone can publish a modified version that includes any already-published content. The new version can be "freely presented by an easily-made annotated collage." But the original is still present—"you can always say, 'Show me what this originally was.'"

### The Hypertext Problem

Versioning is already difficult for simple linear text, but hypertext makes it far harder. Nelson explicitly addresses this challenge: conventional versioning systems work by storing lists of changes and undoing them, which works for "simple, linear textual documents." But hypertext documents have complex interconnections that must also be tracked through time.

The key insight is that **correspondence** matters as much as content. When comparing versions, users need to see not just what text changed, but how the parts relate to each other across versions. This "highlighting the corresponding parts" is essential for meaningful intercomparison—without it, you just have two disconnected snapshots.

### How Users Experience It

- Edit freely knowing nothing is ever lost
- Scroll through time as well as space—watch a passage evolve through successive modifications
- Ask for any past version of any part of the document
- See what changed between versions automatically highlighted
- Navigate four ways within a document: forward/back in text, between hypertext links, between layers of wide-viewing text, and forward/back historically

### Nelson's Words

> "Under many circumstances the writer, or 'text user', needs to reach back to a former condition. This is in the nature of creative work." (2/14)

> "Virtually all of computerdom is built around the inadequate convention of making whole copies of each current version ... A document is really not just a block of text ... it is an ongoing changing file ... an evolving braid." (2/14)

> "A document is really an evolving ONGOING BRAID" (2/14, diagram)

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." (2/15)

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." (2/16)

> "This system is built around the assumption that you are reading from a screen, not from paper. When you 'go to' a certain part of a document, the whole document is not ready to show; yet the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." (2/16)

> "We call this pounce. You pounce like a cat on a given thing, and it seems to be there, having been constructed while you are, as it were, in midair. Unlike things which dematerialize when you pounce on them, like cotton candy, this materializes when you pounce on it." (2/16)

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." (2/19)

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another. We believe our Prismatic storage can support virtually instantaneous retrieval of any portion of any version (historical or alternative)." (2/19)

> "SHOWING COMMONALITIES: What Is the Same, What Is Different. Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them to find out, in other word, what parts of two versions are the same." (2/20)

> "Let us call such a storage system a hyperfile." (2/22)

> "Perhaps most important, these facilities provide a building-block for what is to be described in what follows." (2/22)

> "We often have to keep similar files organized in several different ways: for instance, the same program set up for different computers. Or it is desirable to maintain several possible designs or plans at once. These are examples of the versioning problem." (3/12)

> "Being able to go back through changes, and perhaps restore an earlier state, is called the problem of historical backtrack. For simple, linear textual documents this can be done by storing lists of changes and undoing them; and indeed several commercial versioning and backtrack systems are now on the market. But it is rather more difficult to do this for hypertext." (3/13)

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." (3/13)

On publishing modified versions:

> "This users may also republish documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." (2/45)

> "This means a whole new pluralistic publishing form. If anything which is already published can be included in anything newly published, any new viewpoint can be freely presented by an easily-made annotated collage. (The old viewpoint is still present too—you can always say, 'Show me what this originally was.')" (2/45)

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." (2/45)

---

## Related Concepts

| Concept | Relationship |
|---------|--------------|
| [i-space-v-space](i-space-v-space.md) | Each version is a V-space arrangement over shared I-space |
| [documents](documents.md) | Versions are the "ongoing braid" of document evolution |
| [correspondence](correspondence.md) | Matching parts across versions enables comparison |
| [transclusion](transclusion.md) | New versions effectively transclude content from source |
| [hypertext](hypertext.md) | Version tracking is harder for hypertext than linear text |
| [forking](forking.md) | Alternative versions branch from common ancestors |

## FEBE Operations

| Operation | How versions apply |
|-----------|-------------------|
| **CREATENEWVERSION** | Creates new version (new V-space, same I-space) |
| **SHOWRELATIONOF2VERSIONS** | Compares versions, returns corresponding spans |
| **INSERT, DELETE, REARRANGE** | Modify current version; old versions unaffected |
| **RETRIEVEV** | Can retrieve from specific version |

See [Concept-Operation Map](../concept-operation-map.md) for full mapping.
