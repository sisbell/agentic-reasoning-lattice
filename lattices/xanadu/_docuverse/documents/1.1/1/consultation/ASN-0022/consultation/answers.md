# Consultation Answers — Ghost Link Discoverability

**Inquiry:** What must the system guarantee about discovering links whose target content no longer appears in any document's V-space? How does link discoverability interact with content deletion?
**Date:** 2026-02-26 08:40
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> Must a link remain permanently discoverable even after the content it targets has been removed from every document that once included it?

### Nelson's Answer

# Must Links Remain Discoverable After Target Content Is Removed?

## Short Answer

Yes — but the question contains a premise that Xanadu's architecture makes nearly impossible. In Xanadu, content is never truly removed. The system is designed so that the scenario you describe cannot fully arise.

## Why the Premise Doesn't Hold

Xanadu uses **append-only storage**. I-space content is permanent:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

DELETE in Xanadu removes content from **V-space** (the document's current arrangement) but never from **I-space** (permanent storage):

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So "removed from every document that once included it" means, at most, that no current V-space arrangement references those bytes. The bytes themselves still exist at their permanent I-addresses. They are "awaiting historical backtrack functions."

## Links Point to I-Space, Not V-Space

This is the critical architectural fact. Links attach to **bytes identified by their permanent content addresses**, not to positions in any document's current view:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Since I-space is append-only, the bytes a link references **always exist**. The link's endsets always map to real content. There is no state in which the target bytes cease to exist.

## Link Survivability Guarantees

Nelson's survivability condition is:

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

In I-space, the bytes are always "left" — they cannot be removed. V-space deletion doesn't destroy I-space content. Therefore the survivability condition is permanently satisfied for any link whose endsets point to content that was ever created.

## Links Are Independent Objects

Even setting aside the I-space permanence argument, links exist independently of the documents they connect:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

A link lives at its own tumbler address in its home document. Its existence and discoverability depend on its own home document, not on the state of its targets. The link search mechanism indexes links by their endsets:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

Link search matches on endset **addresses** — not on whether content currently appears in some V-space view. The search finds the link because the link exists at its address; the target content's V-space status is irrelevant to that search.

## Only the Link's Owner Can Remove It

The only way a link ceases to be discoverable is if its **owner explicitly deletes it**:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

No action on the target content — deletion, rearrangement, withdrawal — can destroy someone else's link. The link is the linker's property, stored at the linker's address.

## The Ghost Element Principle

Nelson even supports linking to addresses where **nothing has ever been stored**:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

If links can point to addresses with no content at all ("ghost elements") and still be valid and discoverable, then links certainly remain valid when pointing to I-space content that merely lacks a current V-space arrangement.

## Summary

| Scenario | Link discoverable? | Why |
|----------|-------------------|-----|
| Target content in current V-space | Yes | Normal case |
| Target deleted from current V-space but in older versions | Yes | I-space bytes permanent; link points to I-space |
| Target deleted from all V-space views of all documents | Yes | I-space bytes still exist; link is independent object |
| Target address is a ghost element (nothing ever stored) | Yes | Links can point to ghost elements [LM 4/23] |
| Link owner explicitly deletes the link | No (current) | But even deleted links await "historical backtrack functions" [LM 4/9] |

The architecture is designed so that **links are permanent, independent objects whose discoverability depends on their own existence, not on the state of their targets.** And in a system with append-only storage, both the link and its target content persist in I-space forever.

---

## Question 2 [nelson]

> Does the system guarantee that link discovery operates on content identity rather than on document membership, so that a link to content persists regardless of which documents currently display that content?

### Nelson's Answer

# Link Discovery on Content Identity

**Yes.** The system guarantees that links operate on content identity (I-space addresses), not on document membership. This is structural, not a feature — it follows necessarily from how links, endsets, and the address space are designed.

## Links Attach to I-Space, Not Documents

Links connect spans of bytes identified by their permanent I-space addresses on the tumbler line:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" [LM 4/45]

The endsets map to the tumbler line — which is the I-space, the permanent address space. A link's from-set, to-set, and type are all spans on this line. They reference content by its permanent identity, not by its current location in any document's V-space arrangement.

## Link Search Operates on I-Space Addresses

The core search operation confirms this:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

These parameters are span-sets on the tumbler line. When a front end wants to find links relevant to content the user is viewing, it resolves the V-space positions to I-space addresses, then searches by those I-addresses. The search doesn't ask "what links point into this document?" — it asks "what links point to these bytes?"

> "If the home-set is the whole docuverse, all links between these two elements are returned." [LM 4/63]

## Transclusion Preserves Content Identity

When content is transcluded from Document A into Document B, both documents reference the same I-space bytes:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The transcluded bytes in Document B share the same I-addresses as the original in Document A. A link whose endset points to those I-addresses is discoverable from either document, because both documents display the same I-space content, and link search operates on I-space.

## Explicit Across Versions

Nelson states this most directly for the version case, where CREATENEWVERSION creates a new V-space arrangement over the same I-space content:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Versions are structurally transclusions of the entire prior document. The principle that makes "refractive following" work is shared I-space origin — and that principle applies identically to any transclusion, not only to versions.

## FINDDOCSCONTAINING Confirms the Inverse

The system can also go from content identity to all documents displaying it:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

This confirms the architecture: content identity (I-space address) is the primary key. Documents are views over I-space content. Links attach to I-space content. Discovery flows through content identity, not through document containment.

## The Front End Handles Translation

Users work in V-space (selecting text, scrolling documents). The front end translates V-space selections to I-space addresses before creating or searching for links. This is invisible to users:

> "None of these commands are to be seen by the user. The user's concerns are to be seen on the screen; the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." [LM 4/61]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

## Summary

The guarantee holds: a link to content persists and is discoverable regardless of which documents currently display that content. This is not an implementation choice but a structural consequence of three design decisions:

1. **Endsets point to I-space** (permanent byte identity on the tumbler line)
2. **Transclusion shares I-addresses** (same bytes, multiple documents)
3. **Link search matches on I-space spans** (not on document membership)

A link created to a passage in Document A is discoverable when viewing that same passage transcluded into Document B, Document C, or any future document — because the search mechanism matches the I-space addresses that all these documents share.

---

## Question 3 [nelson]

> When content is removed from a document, must the system distinguish between the content ceasing to appear in that document and the content ceasing to exist in storage?

### Nelson's Answer

# Yes — This Distinction Is the Architectural Foundation of Xanadu

The system does not merely distinguish between these two operations. It makes the first routine and the second **impossible by design**. This separation — content disappearing from a document's arrangement versus content disappearing from storage — is the entire point of the I-space/V-space architecture.

## The Two Address Spaces

Xanadu maintains two fundamentally different address spaces:

**I-Space (Invariant Space)** is where content permanently lives. Addresses are absolute and immutable. Content at an I-space address never changes.

**V-Space (Virtual Space)** is a document's current arrangement of content — a view that references I-space content and can be rearranged across versions.

When a user "deletes" content from a document, they are modifying V-space only. The I-space content is untouched. Nelson's diagram on page 4/9 explicitly shows "DELETED BYTES" as a valid system state with the annotation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "not currently addressable" means: not reachable via this document's current V-space arrangement. The phrase "may remain included in other versions" confirms the bytes still exist in I-space.

## Nelson Is Explicit About This

Nelson further clarifies:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is unambiguous. Deletion is a V-space operation. I-space is unaffected. Other documents that transclude that content continue to show it. Links to those I-space addresses continue to resolve. Previous versions of the deleting document still contain the content.

## The Rejection of Destructive Replacement

Nelson designed this distinction specifically to abolish what he calls "destructive replacement":

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The append-only model means I-space only grows. Nothing is ever removed from it. This is what makes historical backtrack possible:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

## What Each Operation Affects

| Aspect | Affected by V-space removal? | Content ceases to exist in storage? |
|--------|------------------------------|-------------------------------------|
| Current document view | Yes — content disappears from arrangement | N/A — this operation does not exist |
| I-space content | No — bytes remain forever | Would violate append-only invariant |
| Previous versions | No — still contain the content | Would destroy version history |
| Transclusions in other documents | No — still show it | Would break other users' documents |
| Links to the content | No — still resolve to I-space | Would break the permanence guarantee |
| Home document traceability | No — I-address encodes origin | Would destroy attribution |

## The Deeper Principle

Nelson frames this as essential to what a document IS:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

The braid metaphor is precise. When you remove a strand from a braid's current pattern, the strand still exists — it's woven into earlier sections. Destroying the strand would unravel the entire history.

This also serves the non-destruction guarantee for publishing:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

If deletion could destroy I-space content, it would damage originals. The guarantee that "you can always say, 'Show me what this originally was'" [LM 2/45] depends entirely on I-space permanence.

## Summary

The system does not merely distinguish between "content ceasing to appear" and "content ceasing to exist." It makes the first a normal editing operation (V-space rearrangement) and the second architecturally impossible (I-space is append-only). This is not a policy choice — it is the structural foundation on which permanence, version history, transclusion, link survivability, and attribution all depend.

---

## Question 4 [nelson]

> If a user retrieves content that no document currently includes, must the system still return all links whose source or target spans overlap that content?

### Nelson's Answer

# Yes — Links Must Still Be Discoverable

The architecture requires it. Here's why.

## Links Attach to I-Space, Not V-Space

Links are "straps between bytes" [LM 4/42] — they attach to content at its permanent I-space address, not to any particular document's V-space arrangement:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" [LM 4/45]

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

The tumbler line is I-space — the permanent address space. Link endsets map to it. Not to any document's current V-stream.

## DELETE Does Not Destroy I-Space Content

When content is "deleted," it is removed from V-space only. The bytes remain at their permanent I-addresses:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

"Not currently addressable" means not addressable in the V-space of the deleting document — not that the I-address ceases to exist. The bytes are explicitly described as "awaiting historical backtrack functions," which means the system still knows about them and can reconstruct access to them.

## Link Search Operates on Endsets, Not V-Space Inclusion

The FINDLINKSFROMTOTHREE operation searches by matching endsets on the tumbler line:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

The satisfaction model is purely about endset overlap:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

There is no condition requiring that the content at those addresses be currently included in any document's V-space. The search matches addresses against addresses — not against active document views.

Furthermore, Nelson emphasizes that irrelevant links do not impede search:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This tells us the search mechanism is designed to work over the entire link population efficiently, without filtering by document-inclusion status.

## The Survivability Guarantee Demands It

The whole point of span-based linking is survivability:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

"If anything is left at each end" refers to the bytes themselves existing in I-space — not to whether any document currently displays them. If the system stopped returning links merely because content left all V-spaces, the survivability guarantee would be hollow. A link that "survives" deletion but becomes undiscoverable is indistinguishable from a broken link.

## The Ghost Elements Principle Reinforces This

The system explicitly supports references to addresses where nothing is even stored:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

If links to *completely empty* addresses are valid and discoverable, then links to addresses where content *does* exist (just not in any current V-space) must certainly be discoverable.

## How This Works in Practice

The scenario: content exists at I-address X. It was once in Document A's V-space but has been deleted from all documents. Links L1, L2, L3 have endsets pointing to spans that overlap X.

1. The user retrieves the content at X through historical backtrack — "when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15]
2. The user (or front end) issues FINDLINKSFROMTOTHREE with a span covering X
3. The system matches L1, L2, L3 because their endsets overlap X on the tumbler line
4. All three links are returned

Note the contrast with FINDDOCSCONTAINING, which explicitly searches for documents that *currently include* specified material [LM 4/70]. That operation would return nothing if no document includes the content. But FINDLINKSFROMTOTHREE has no such V-space-inclusion filter — it operates purely on the tumbler line.

## Summary

The system **must** return all links whose endsets overlap the content, regardless of whether any document currently includes it, because:

- Link endsets map to the I-space tumbler line, not to V-space
- DELETE removes from V-space only; I-space content persists
- Link search matches endset addresses, with no V-space-inclusion condition
- The survivability guarantee requires links to remain discoverable after deletion
- Even ghost elements (no content at all) support valid, discoverable links

The content's absence from all V-spaces is irrelevant to link discovery. The bytes exist. The links exist. The endsets match. The system returns them.

---

## Question 5 [nelson]

> Must the system guarantee that no editing operation on any document can destroy a link, given that links connect content spans rather than document locations?

### Nelson's Answer

# No — But the Architecture Makes It Nearly Impossible

The system does **not** guarantee that no editing operation can ever destroy a link. Nelson states the survivability property with an explicit conditional:

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"
> — [LM 4/43]

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived."
> — [LM 4/42]

The conditional "if anything is left at each end" is deliberate. It acknowledges the logical possibility that a link could lose all referenced bytes at one end, at which point the link has nothing to attach to.

## Why Editing Cannot Destroy Links in Practice

However, the I-space/V-space architecture makes this scenario effectively unreachable through normal editing operations:

**1. Links attach to I-space bytes, not V-space positions.**

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."
> — [LM 4/30]

**2. I-space is append-only. Content is never destroyed.**

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically."
> — [LM 2/14]

**3. DELETE removes content from V-space only — not I-space.**

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"
> — [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."
> — [LM 4/11]

The chain of reasoning is:

- Links point to I-space bytes (permanent content addresses)
- INSERT, DELETE, REARRANGE, and COPY all modify V-space arrangements
- V-space operations never destroy I-space content
- Therefore, the I-space bytes a link references always exist
- Therefore, there is always "something left at each end"

This means Nelson's conditional is satisfied by construction. The architecture guarantees that editing operations produce the conditions under which links survive.

## The Distinction: Survivability vs. Indestructibility

Nelson promises **survivability**, not **indestructibility**. The difference matters:

**Survivability** means links are resilient to the normal operations users perform (inserting, deleting, rearranging text). The design ensures this structurally — links attach to content identity, not to positions that shift during editing.

**Indestructibility** would mean links can never be removed under any circumstances. Nelson does not promise this. Two scenarios exist where links cease to be active:

1. **The link owner explicitly deletes it.** Links are owned objects. The owner has the administrative right to delete their own link, just as they can delete their own content. This is documented as a valid state: "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

2. **The logical edge case** where all bytes at one end truly cease to exist — which, as shown above, cannot happen through editing in the append-only model, but which Nelson acknowledges as a theoretical boundary condition.

## Summary

| Question | Answer |
|----------|--------|
| Can editing destroy links? | No — I-space permanence prevents it |
| Does Nelson guarantee this absolutely? | No — he states the conditional "if anything is left at each end" |
| Is the conditional ever violated by editing? | No — editing modifies V-space; I-space bytes persist |
| Can links be destroyed at all? | Yes — by the link owner's explicit deletion |
| Are deleted links truly gone? | No — they await "historical backtrack functions" |

The guarantee is architectural rather than absolute. Nelson does not say "links are indestructible." He says links attach to bytes, bytes survive editing, and therefore links survive editing. The conditional phrasing is honest about the logical structure: the guarantee holds because the precondition (something remains at each end) is maintained by the append-only storage model — not because the system prohibits link destruction as a rule.

---

## Question 6 [nelson]

> When a user follows a link whose target content appears in no current document, what must the system present — the raw content alone, a prior version of a document that once contained it, or something else?

### Nelson's Answer

This is a precise architectural question that sits at the intersection of several Xanadu principles. Let me trace through what Literary Machines specifies.

## The Scenario

A link's endset points to I-space content that has been removed from every document's current V-space arrangement. The user follows the link. The bytes exist permanently in I-space — nothing in Xanadu is ever truly destroyed. But no living V-stream currently presents them.

## What the Architecture Guarantees

**The content is always retrievable.** I-space is append-only and permanent:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The link itself survives because it attaches to I-space bytes, not V-space positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

So the link is valid and the target bytes exist. The question is what the user *sees*.

## Nelson's Explicit Status for This Content

The diagram on 4/9 gives deleted bytes a specific system status:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Three things to note here:

1. **"Not currently addressable"** — in V-space. The content has no position in any current document view. But it remains in I-space.

2. **"Awaiting historical backtrack functions"** — this is the intended recovery path. The system preserves all versions, and deleted content exists in prior versions.

3. **"May remain included in other versions"** — other documents that transclude this content may still show it. The FINDDOCSCONTAINING operation finds "all documents containing any portion of the material" [LM 4/70].

## What Nelson Says About Following Links Through Versions

Nelson directly addresses the case of following a link when the target document has changed:

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—**if it's still there.**" [LM 2/43]

That conditional — *if it's still there* — is the crux. Nelson describes the happy path (content found in the current version via correspondence) but does not explicitly describe what happens when the content is *not* still there.

However, the version-spanning link mechanism works in both directions:

> "Links may be refractively followed from a point or span in one version to corresponding places in **any other version**. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

"Any other version" includes prior versions. If the content exists only in an older version, refractive following can locate it there.

## What the System Must Present

Nelson does not specify a single definitive presentation for this edge case. But the architecture constrains the answer tightly:

**Raw content alone is insufficient.** Xanadu emphasizes context and navigability. The user must always know where they are:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

**A prior version is the natural answer.** Since "There is thus no 'basic' version of a document set apart from other versions" [LM 2/19], a prior version is not a degraded experience — it is a fully valid document state. The system reconstructs it on demand:

> "We call this pounce. You pounce like a cat on a given thing, and it seems to be there, having been constructed while you wait, as it were, in midair." [LM 2/16]

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

**Other documents may still contain the content.** If the bytes were transcluded elsewhere and those transclusions survive, FINDDOCSCONTAINING would locate them. Following the link could land you in a living document that still presents the content.

## My Answer

The system must present the content **in the context of a version that contains it** — not as raw bytes alone. The architecture provides two paths, and the front end should try both:

1. **Find a current document that transcludes the content** (via FINDDOCSCONTAINING). If one exists, present the content in that living context.

2. **Reconstruct a prior version of the home document** (via historical backtrack). The content was "deleted" from V-space but exists in earlier versions. The system reconstructs that version and presents the content in its original document context — with a supersession indicator showing the user they are viewing a historical state.

The front end mediates this. Nelson explicitly makes presentation a front-end responsibility:

> "None of these commands are to be seen by the user. The user's concerns are document content and links, and the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." [LM 4/61]

What the system must **never** do is return a broken link or "not found." The content exists. The link is valid. The I-space guarantee means this scenario is architecturally impossible to produce a true failure — only a presentation challenge for the front end.

## What Nelson Does Not Specify

Nelson does not explicitly address:
- Whether the system should *prefer* a living transclusion over a historical version
- Whether the user should be told "this content has been removed from the current version" before seeing the historical state
- Whether the front end should offer both paths (historical version *and* living transclusions) simultaneously

These are front-end design decisions. The back end provides the primitives (FINDDOCSCONTAINING, SHOWRELATIONOF2VERSIONS, version retrieval); the front end composes them into a coherent experience.

NEED_RAW: 4/9 (the full deleted-bytes diagram may show additional status transitions or recovery paths beyond what the OCR captured)

---

## Question 7 [nelson]

> Must the system provide a way to enumerate all links that have become "orphaned" — whose target content exists in permanent storage but appears in no document's current version?

### Nelson's Answer

# No — and the concept itself is foreign to Nelson's architecture

Nelson does not specify such an operation, and the premise — that links can become "orphaned" — rests on a misunderstanding of how links relate to content in Xanadu.

## Links point to I-space, not V-space

The critical architectural fact: **links attach to permanent I-space addresses, not to ephemeral V-space positions.**

> "A Xanadu link is not between points, but between spans of data." [LM 4/42]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

I-space content is permanent and append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

A link's target bytes **always exist** in I-space. They cannot be removed. The concept of an "orphaned" link — one pointing to something that has vanished — is structurally impossible.

## "Deletion" does not create orphans

DELETE removes content from V-space only. Nelson's own diagram annotation makes this explicit:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

When content disappears from a document's current V-space arrangement:

| What changes | What doesn't change |
|---|---|
| Current V-space arrangement | I-space content (permanent) |
| Where the bytes appear "now" | Where the bytes permanently live |
| — | Links to those I-space bytes |
| — | Previous versions containing the content |

The content is still at its I-space address. The link still points to a valid, retrievable address. There is no orphan.

## Historical versions always preserve access

Even if content is removed from every *current* V-space arrangement, the version where it was originally created still contains it. Nelson's model is that every previous state is permanently accessible:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

And version-spanning links handle the traversal:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

A link to content that no longer appears in the current version can be "refractively followed" to the version where it does appear. The system already has this mechanism.

## The 17 FEBE commands include no such operation

Nelson specifies exactly 17 operations in XU.87.1 [LM 4/61-4/70]. None performs "find links whose targets are absent from all current V-space arrangements." The link search operation is:

> "FINDLINKSFROMTOTHREE: This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

This searches by I-space address constraints. It will find links to deleted-from-V-space content the same way it finds links to anything else — because the I-space addresses are valid either way. There is no distinction to make.

## What the system *does* provide instead

If a user wants to know "does anyone link to this content that I removed from my current version?", the existing operations suffice:

1. **FINDLINKSFROMTOTHREE** — specify the I-space address of the removed content as the to-set; get back all links pointing to it
2. **FINDDOCSCONTAINING** — "returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70] — find whether any other documents still transclude it

These work regardless of V-space status because they operate on I-space identity.

## Summary

The question assumes a failure mode that Nelson's architecture eliminates by design. In systems where targets can be destroyed (the web, file systems), orphaned references are a real problem requiring maintenance. In Xanadu:

- I-space content is **permanent** — targets cannot disappear
- Links attach to **I-space bytes** — not to positions that shift
- Historical versions **always preserve** the arrangement where content appeared
- Version-spanning links **refractively follow** through to wherever the content still appears
- Existing search operations find links to any I-space address **regardless of V-space status**

There is nothing to enumerate because there are no orphans. The system's answer to "what about links to deleted content?" is not "find and flag them" but rather: **deletion doesn't destroy content, so links remain valid.** This is the entire point of separating I-space from V-space.

---

## Question 8 [nelson]

> If content is later re-included in a new or existing document, must the system guarantee that all original links to that content become discoverable again within the new document context without any re-linking step?

### Nelson's Answer

# Yes — Links Follow Content, Not Containers

The system guarantees that links remain discoverable wherever their target content appears, without any re-linking step. This is not a special feature but a structural consequence of how Xanadu's addressing works.

## The Mechanism

Links attach to **I-space spans** (permanent content addresses), not to V-space positions or document containers. When content is re-included in any document via transclusion (the COPY operation), the new document's V-space maps to the **same I-space addresses** as the original. Since link endsets reference those I-space addresses, they are automatically discoverable in any document context where that content appears.

Three architectural properties combine to guarantee this:

**1. Links attach to bytes, not positions.**

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

**2. Transcluded content retains its I-space identity.**

> "Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

The content doesn't get new I-space addresses when re-included. It is the same content, viewed through a different V-space arrangement.

**3. Link search operates on span overlap, not document membership.**

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

The search mechanism finds links whose endsets overlap with specified spans — regardless of which document those spans currently appear in.

## The Explicit Precedent: Version-Spanning Links

Nelson states this principle most directly in the context of versions, which are structurally identical to transclusion (both create V-space arrangements over shared I-space content):

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

If a link to one **version** is automatically a link to all versions (because of shared I-space), then by the same logic, a link to content in one **document** is automatically discoverable in any other document that transcludes that content. The mechanism is identical: shared I-space origin.

## The User-Facing Guarantee

Nelson specifies that readers should be able to discover all connections to any content they're viewing:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

This applies to **any** document or place — including documents that contain re-included content. The links are discoverable because they point to I-space, and the content retains its I-space identity regardless of which V-space arrangement displays it.

## The "Deletion" Step Is Irrelevant

The intermediate "deleted" state doesn't affect link discoverability because deletion only touches V-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

During the period content is "deleted" from all V-space arrangements, the links still exist — they're just not reachable through any current document view. The moment that content reappears in any V-space (through re-inclusion), those links become reachable again through that context. No new links need to be created; the original links never stopped pointing to those I-space addresses.

## Summary

The answer is **yes**: when content is re-included in a new or existing document, all original links to that content are automatically discoverable in the new document context. No re-linking step is required. This falls directly out of three design choices:

1. Links point to I-space (content identity), not V-space (position)
2. Transclusion preserves I-space identity (same addresses, new arrangement)
3. Link search matches on span overlap (finds links regardless of which document hosts the content)

Nelson's own words confirm the principle: "a link to one version of a Prismatic Document is a link to all versions" [LM 2/26]. The same logic extends to any transclusion context — a link to content is a link to that content wherever it appears.

---

## Question 9 [nelson]

> Does the permanence guarantee for content imply that there is no true deletion, and therefore that every link always has retrievable target content even if no document chooses to display it?

### Nelson's Answer

# Permanence, Deletion, and Link Target Retrievability

This is a precisely framed question with a nuanced answer. The short version: **conceptually yes, but with important qualifications Nelson himself introduces.**

## The I-Space Permanence Argument

Nelson's architecture is built on append-only storage. Content in I-space is permanent and immutable:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

DELETE in Xanadu is a V-space operation only — it changes a document's current arrangement, not the underlying content:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Links attach to I-space content, not V-space positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

So the chain of reasoning holds: I-space is append-only → DELETE only affects V-space → links point to I-space → therefore link targets should always exist.

## But Nelson Himself Introduces the Breaking Condition

Despite the append-only model, Nelson explicitly states links CAN break:

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/42-4/43]

This creates a tension. If I-space bytes are truly permanent, how can there ever be "nothing left at each end"? There are two possible readings:

1. **Nelson is describing the conceptual editing model**, where "deletion" means removal from the current arrangement. In this reading, the qualification is about V-space visibility — the link is technically intact in I-space but has no V-space manifestation in the current version. The link "survives" only in the sense that it remains navigable.

2. **Nelson acknowledges a scenario where bytes could genuinely be absent** — perhaps through document withdrawal, server failure, or storage funding lapse. In this reading, the append-only model is an aspiration with practical limits.

## Published vs. Private: Two Different Guarantees

Nelson draws a hard line for **published** content — and links are the explicit justification for that line:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it." [LM 2/43]

The reasoning is circular in the best sense: links create permanence obligations, and permanence enables reliable links. Published content MUST remain **because** others have linked to it.

For **private** documents, the guarantee is weaker. The owner can withdraw a private document at will [LM 2/29]. If anyone had linked to private content (within the scope of their access), those links would lose their targets upon withdrawal.

## The "Not Currently Addressable" State

Nelson's language about deleted bytes is precise and revealing:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" means the bytes exist in I-space but have no V-space mapping in the current version. They are reachable through:
- **Historical backtrack** — navigating to a previous version where they appeared
- **Other documents** — any document that transcludes the same I-space content
- **Direct I-space reference** — if a link points to the I-address (though Nelson says I-addresses are "of no concern to the user or to the front end" [LM 4/11])

So there is a middle state between "displayed in a current document" and "gone forever." Content can be in limbo — existing, addressable by its I-address, reachable through old versions, but not shown in any current V-space arrangement.

## The Practical Gap: Storage Economics

Nelson introduces a significant practical qualification through his economic model:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

He does NOT specify what happens when storage rental lapses. And in the user contract:

> "User acknowledges that due to possible unreliability of the software, unreliability and vulnerability of transmission systems, and myriad possibilities for intrusion and malicious mischief by unseen parties throughout the universe, all storage, and transmission of contents and links, and attempts to deliver such material, are at User's risk." [LM 5/18]

This means the conceptual guarantee (I-space is permanent) and the operational reality (content requires funded storage) do not perfectly align.

## Conclusion

The answer to your question breaks into three parts:

**1. Is there true deletion?** No. DELETE is a V-space operation. I-space content persists. Nelson designed this explicitly to abolish "destructive replacement" [LM 2/14].

**2. Does every link therefore have retrievable target content?** In the conceptual model, yes — I-space bytes never vanish, so link endpoints always exist. For published content, Nelson makes this an explicit contractual obligation justified by the existence of links themselves [LM 2/43]. For private content, the owner can withdraw, breaking the chain.

**3. Is "exists" the same as "retrievable"?** Not necessarily. Content can be "not currently addressable" [LM 4/9] — present in I-space but not in any current V-space arrangement. It exists but requires historical backtrack or I-space navigation to reach. And operationally, storage funding and server availability constrain what is practically deliverable, regardless of the conceptual permanence model.

The deep insight is that Nelson designed links and permanence as **mutually reinforcing**: links create the obligation to preserve content, and permanent content makes links reliable. The system works only when both halves hold. His willingness to state that links break "if nothing is left at each end" suggests he recognized the gap between the ideal (everything permanent forever) and the operational reality (everything depends on funded, functioning infrastructure).

---

## Question 10 [nelson]

> Must the system inform a user viewing a document that linked content exists beyond what the document currently shows — that is, must it reveal links to content the document once contained but no longer includes?

### Nelson's Answer

# Must the System Reveal Links to Content No Longer in the Current View?

This question sits at the intersection of several core Xanadu mechanisms: link survivability, I-space/V-space separation, bidirectional discovery, and front-end responsibility. Nelson does not address this exact scenario explicitly, but the architecture and principles provide a clear answer in two parts.

## The Architecture Makes This Discoverable — Always

Links point to **I-space addresses**, not V-space positions. When content is "deleted" from a document, it is removed from the current V-space arrangement but **remains permanently in I-space**:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Any link made to that content still resolves — it points to an I-address that still exists. The link doesn't know or care whether the target is currently visible in some document's V-stream. The FEBE operation `FINDLINKSFROMTOTHREE` searches by span constraints and can locate links to any I-space content, whether or not that content appears in any current V-space arrangement.

So the system **can always find** links to content a document once contained. The machinery guarantees this structurally.

## But Must It Proactively Inform the Reader?

Nelson specifies bidirectional discovery as a **capability the reader can invoke**, not as an automatic notification:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

The phrase "should be able to ask" frames this as a reader's right, not a system-initiated alert. Nelson places presentation decisions squarely with the front end:

> "None of these commands are to be seen by the user. The user's concerns are to be seen on the screen; the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." [LM 4/61]

The closest thing to a "must inform" pattern is the supersession link check:

> "A front-end request for supersession links is normally expected before starting to read a new document." [LM 4/52-4/53]

Even here, Nelson says "normally expected" — a strong convention, not an absolute mandate. For general in-links, no equivalent expectation is stated.

## The "If It's Still There" Clause

Nelson explicitly contemplates the case where a link reaches into a version where the target content no longer exists:

> "When a document is updated, a reader will ordinarily want to see the new version — but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version — **if it's still there.**" [LM 2/43]

That conditional — "if it's still there" — acknowledges that content may NOT be in the current version. Nelson doesn't say the system must alert the current-version reader that such orphaned links exist. He says the system must handle the case where someone *follows* such a link by resolving to the old version where the content remains.

## The Distinction Between Native and Transcluded Content

The answer differs subtly depending on whether the removed content was native or transcluded:

**Native content deleted from V-space:** The I-address is under the document's ownership. Links point to that document's I-space. A search for "links into this document" could in principle surface these — the I-address identifies this document as the content's home.

**Transcluded content removed from V-space:** The I-address belongs to the *source* document, not the one that windowed it. Links to this content point to the source's I-space. Removing the transclusion from the viewing document has no effect on the links — they were never "into" this document in the I-space sense. They were always into the source.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

## What the Principles Favor

While Nelson doesn't mandate proactive notification, his principles favor **transparency over concealment**:

1. **"You always know where you are"** — Nelson's guarantee that users can "at once ascertain the home document of any specific word or character" [LM 2/40] reflects a deep commitment to navigational transparency.

2. **Links justify permanence** — The reason published content cannot be withdrawn is precisely because others have linked to it. If those links become invisible because of V-space editing, the social contract around link freedom is undermined.

3. **The printing press analogy** — A book that removes a chapter doesn't make the footnotes citing that chapter disappear from other books. Similarly, removing content from a document's current version shouldn't make the links invisible.

4. **Link freedom is bidirectional** — "each user is free to link to anything" and the author "is relinquishing the right to control links into that work" [LM 2/43]. If deleting content from V-space effectively hides others' links, the author has de facto regained control over incoming connections.

## Summary

| Question | Answer |
|----------|--------|
| **Can** the system reveal links to removed content? | **Yes** — always. I-space is permanent; links resolve; FEBE operations support the query. |
| **Must** the system proactively inform the reader? | **Not explicitly specified.** Nelson frames bidirectional discovery as a reader-invocable capability, not an automatic notification. |
| **Should** a well-designed front end surface this? | **The principles strongly favor it.** Link freedom, transparency, and the social contract around in-links all argue that a front end should make these discoverable, even if the exact UX is left to the designer. |
| **Must** the system resolve such links when followed? | **Yes.** The old version "must remain on the network" [LM 2/43], and the link resolves there. |

The system is not required to volunteer that a ghost web of connections surrounds deleted content. But it must never make those connections **unfindable**. A reader who asks "what links exist to content this document once contained?" must be able to get an answer. Whether the front end asks that question on the reader's behalf is a design judgment — but one that Nelson's principles clearly favor.

---

## Question 11 [gregory]

> When all V→I mappings for a link's target I-addresses are deleted from every document's POOM, does `findlinksfromtothreesp` still return that link when searching the spanfilade directly by those I-addresses?

### Gregory's Answer

## KB Synthesis

## Answer: Yes — The Spanfilade Still Returns the Link

When all V→I mappings for a link's target I-addresses are deleted from every document's POOM, `findlinksfromtothreesp` **would still return the link** if called with those I-addresses directly. But the practical `find_links` operation produces empty results through the normal call path. Here is why both statements are true simultaneously.

---

### The Spanfilade Is Permanently Append-Only

[INV-SPANF-WRITE-ONLY] (Finding 0057) establishes the core fact: no delete function exists anywhere in `spanf1.c` or `spanf2.c`. Inspection of the codebase finds `insertspanf`, `findlinksfromtothreesp`, `retrieveendsetsfromspanf`, and other query functions — but no `deletespanf`, `removespanf`, or removal mechanism of any kind. This is a structural property of the implementation, not a convention.

When `CREATELINK` ran, it called `insertendsetsinspanf()` to index the link's endpoint I-addresses into the spanfilade [ST-CREATE-LINK, Finding 0012]. Those entries are permanent. No subsequent operation removes them.

---

### DELETE Modifies Only the POOM

[ST-DELETE] (Finding 0057) traces the `dodeletevspan` call chain explicitly:

```
dodeletevspan → findorgl → deletevspanpm → deletend + logbertmodified
```

There is no call to any spanf function. `deletevspanpm` operates solely on the document's orgl enfilade (granf/POOM layer). The spanfilade is untouched. This produces the divergence documented in [INT-DELETE-SPANF-DIVERGENCE]:

> After DELETE, the POOM no longer contains the mapping, but the spanfilade still claims the document contains those I-addresses. This divergence is permanent — no mechanism exists to reconcile the two layers.

[SS-THREE-LAYER-MODEL] (Finding 0040) formalizes the three-layer independence: CREATELINK writes to all three layers (I-space, spanfilade, POOM). `DELETEVSPAN` removes only the POOM entry. The link orgl in I-space and the spanfilade entries are unchanged.

---

### The Practical `find_links` Path Still Returns Empty

Here is the subtlety. Normal `find_links` operation does not query the spanfilade directly with raw I-addresses. The call chain is:

1. Caller provides a V-specset (V-addresses in a document)
2. `specset2sporglset` converts V-addresses → I-addresses via the document's **POOM**
3. `findlinksfromtothreesp` searches the spanfilade with those I-addresses

When all V→I mappings for the target I-addresses have been deleted from every document's POOM, step 2 produces **empty I-spans** — no document can translate those V-addresses to those I-addresses anymore. The spanfilade search receives nothing to search for and returns empty.

This is exactly what [EC-ORPHANED-LINK] (Finding 0024) documents in its behavior matrix:

| Deleted Content | `find_links` | `follow_link` source | `follow_link` target |
|----------------|-------------|----------------------|----------------------|
| Both source & target | Empty | Empty | Empty |

The `find_links` result is empty — but the emptiness comes from the V→I conversion failing, not from the spanfilade losing the entries.

---

### If Called Directly With the I-Addresses

`findlinksfromtothreesp` itself performs the spanfilade search. If it were called with the target I-addresses directly as its span-dimension input (bypassing the V→I conversion step), it would find them — the spanfilade still indexes those I-addresses to the link's ISA. [EC-STALE-SPANF-REFERENCE] (Finding 0057) confirms the same pattern for `find_documents`:

> `actual_docs(i) ⊆ find_documents(i)` — the spanfilade returns a superset of documents currently containing the queried I-addresses.

The same superset relationship holds for link endpoints: the spanfilade still maps those I-addresses to the link, regardless of whether any POOM currently references them. Direct spanfilade query → link returned. POOM-mediated query → empty conversion → nothing passed to spanfilade → link not returned.

---

### Summary

The spanfilade retains the link's target I-address entries permanently, because [INV-SPANF-WRITE-ONLY] holds and DELETE never touches the spanfilade [ST-DELETE, Finding 0057]. `findlinksfromtothreesp` searching directly by those I-addresses would return the link.

In practice, the normal `find_links` operation fails to reach those spanfilade entries because the V→I conversion step (POOM lookup) produces empty output once all POOM mappings are gone. The link is "invisibly present" in the spanfilade — structurally intact but unreachable through the standard query path. This is precisely the "deeply stale" state that [INT-DELETE-SPANF-DIVERGENCE] and [INV-LINK-PERMANENCE] together describe: the link exists in permanent storage and remains indexed, but content-identity-based discovery is blocked by the empty POOM.

---

## Code Exploration

I now have the full execution trace. Here is my complete answer.

---

## Answer: Does `findlinksfromtothreesp` return the link after V→I mappings are deleted from the POOM?

**Short answer**: It depends on the type of the input specset items.
- Searching via **I-addresses directly (ISPANID items)**: **yes**, the link is still returned.
- Searching via **V-specs (VSPECID items)**: **no**, the result is empty.

Here is the full code trace.

---

### 1. Entry point: `dofindlinksfromtothree` → `findlinksfromtothreesp`

`do1.c:348-353`:
```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset, ...)
{
  bool findlinksfromtothreesp();
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, linksetptr);
}
```

Everything flows through `findlinksfromtothreesp` in `spanf1.c:56-103`.

---

### 2. The two forks in `specset2sporglset`

`findlinksfromtothreesp` first calls `specset2sporglset` for each non-null endpoint set [`spanf1.c:70-75`]. This is where the answer diverges.

`sporgl.c:14-33`:
```c
bool specset2sporglset(typetask *taskptr, typespecset specset, typesporglset *sporglsetptr, int type)
{
    *sporglsetptr = NULL;
    for (; specset; specset = ...) {
        if (((typeitemheader *)specset)->itemid == ISPANID) {
            *sporglsetptr = (typesporglset)specset;          // ← passes I-span through directly
            sporglsetptr = (typesporglset *)&((typeitemheader *)specset)->next;
        } else if (((typeitemheader *)specset)->itemid == VSPECID) {
            if (!(sporglsetptr = vspanset2sporglset (taskptr, &..., ..., sporglsetptr, type))) {
                return (FALSE);
            }
        }
    }
    *sporglsetptr = NULL;
    return (TRUE);
}
```

**Fork A (ISPANID)**: The I-span item is assigned directly to the output sporgl set. No POOM lookup. No `findorgl`, no `vspanset2ispanset`. The I-address goes straight to the spanfilade query.

**Fork B (VSPECID)**: Calls `vspanset2sporglset`, which requires the POOM:

`sporgl.c:35-65`:
```c
typesporglset *vspanset2sporglset(...) {
    if (!findorgl (taskptr, granf, docisa, &orgl, type)) { return (NULL); }
    for (; vspanset; vspanset = vspanset->next) {
        (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);  // ← POOM lookup
        for (; ispanset; ispanset = ispanset->next) {
            // builds sporgl from ispanset entries
        }
    }
    return (sporglsetptr);
}
```

`vspanset2ispanset` (`orglinks.c:397-401`) calls `permute`, which calls `span2spanset` (`orglinks.c:425-453`):

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) { ... }
if (!context) {
    return(targspansetptr);   // ← returns unchanged (empty) pointer when POOM has no match
}
```

When all V→I mappings for those V-addresses have been deleted from the POOM, `retrieverestricted` returns NULL. The loop never runs. `targspansetptr` — still pointing at the initial NULL — is returned. The `ispanset` remains empty, so the inner loop in `vspanset2sporglset` never runs, and `fromsporglset` ends up NULL.

---

### 3. What happens with a NULL sporglset

Back in `findlinksfromtothreesp` [`spanf1.c:76-83`]:

```c
if (fromvspecset) {
    sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) {
        *linksetptr = NULL;
        return (TRUE);    // ← early return, link NOT found
    }
}
```

`sporglset2linkset` → `sporglset2linksetinrange` (`sporgl.c:239`):
```c
for (; sporglset; sporglset = ...) { ... }   // loop never runs if sporglset is NULL
```

With NULL `fromsporglset`, `fromlinkset` stays NULL. The early-return fires, and `*linksetptr = NULL` is returned. **The link is not found when the query uses V-specs and the POOM mappings are gone.**

---

### 4. Why the spanfilade search works with I-addresses directly

When `ISPANID` items are passed (Fork A), `sporglset2linksetinrange` (`sporgl.c:239-269`) runs with the raw I-spans:

```c
// sporgl.c:256-262
if (orglrange) {
    prefixtumbler(&orglrange->stream, spantype, &range.stream);
    prefixtumbler (&orglrange->width, 0, &range.width);
    context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
} else {
    context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, (typespan*)NULL, ORGLRANGE, (typeisa*)infoptr);
}
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist (taskptr, linksetptr, &linksa);
}
```

The cast `(typespan*)sporglset` works because `typeispan` IS `typespan` (same struct, `xanadu.h:75`: `typedef typespan typeispan`), and `typesporglitem` is a union of `typeispan` and `typesporgl` (`xanadu.h:123-127`). The `stream` and `width` fields of the I-span map exactly to the SPANRANGE coordinates used by `retrieverestricted`.

This is a **pure enfilade traversal** of the spanfilade — it never consults the POOM or the granfilade. It finds any crums stored during link creation whose SPANRANGE overlaps the query I-spans.

Also note `sporgl.c:251`:
```c
if (FALSE/*trying to kluge links followable thru versions */&&...) { infoptr = ...; }
else  infoptr = NULL;
```
The `FALSE` short-circuits all homedoc filtering; `retrieverestricted` is called with `infoptr = NULL`, so it searches globally across all documents.

---

### 5. The spanfilade is populated at link creation, independently of the POOM

`docreatelink` (`do1.c:195-221`) does this at creation time:

```c
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)   // V→I via POOM, once
&& specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`insertendsetsinspanf` (`do2.c:116-128`) calls `insertspanf` (`spanf1.c:15-54`) for each endpoint, writing I-address crums into the spanfilade. **The I-addresses are baked into the spanfilade at creation time.** Subsequent deletion of V→I mappings from the POOM does not touch these spanfilade entries.

---

### Conclusion

| Search method | POOM consulted? | Link found after POOM deletion? |
|---|---|---|
| `VSPECID` specset (V-address query) | Yes — via `vspanset2ispanset` → `retrieverestricted` on POOM | **No** — empty context → empty sporglset → `fromlinkset = NULL` → early return `*linksetptr = NULL` |
| `ISPANID` specset (I-address query) | **No** — `specset2sporglset` bypasses POOM at `sporgl.c:20-22` | **Yes** — I-spans go directly to `retrieverestricted` on spanfilade, which retains the link's entries unconditionally |

When the question asks about "searching the spanfilade directly by those I-addresses," the answer is **yes**: `findlinksfromtothreesp` does still return the link. The spanfilade is a separate persistent enfilade from the POOM; the V→I mappings in the POOM are needed only to translate V-addresses into I-addresses at query time. If you supply the I-addresses directly (as `ISPANID` items in the specset), the POOM is entirely bypassed [`sporgl.c:20-22`], `retrieverestricted` finds the link's crums in the spanfilade, and the link I-address is returned via `beheadtumbler` on `c->totaloffset.dsas[ORGLRANGE]` [`sporgl.c:264`].

---

## Question 12 [gregory]

> After DELETE removes content referenced by a link endpoint, do the DOCISPAN entries for that content persist unchanged in the spanfilade, and does `find_documents_containing` still report the document as containing that content?

### Gregory's Answer

## KB Synthesis

Yes on both counts. The KB is explicit and consistent across multiple findings.

## DOCISPAN Entries Persist Unchanged

**[INV-SPANF-WRITE-ONLY]** is the governing invariant. The spanfilade has no deletion mechanism at all. Inspection of `spanf1.c` and `spanf2.c` reveals only insertion and query functions — no `deletespanf`, `removespanf`, or any removal operation exists. The set of spanfilade entries is monotonically non-decreasing: `∀ t₁ < t₂ : spanf_entries(t₁) ⊆ spanf_entries(t₂)`.

**[ST-DELETE]** (Finding 0057) makes the frame condition explicit. The DELETE call chain is `dodeletevspan` → `deletevspanpm` → `deletend`, with no call to any spanf function anywhere in that path. Formally: `delete(D, vspan) ⟹ spanf_entries_after = spanf_entries_before`. The `dodeletevspan` implementation confirms this — it calls only `deletevspanpm` (which modifies the POOM in granf) and `logbertmodified`, never touching spanf.

## `find_documents_containing` Still Returns the Document

**[INV-IADDRESS-PERMANENT]** (Finding 0023) states this directly: "Once an I-address is associated with a document (via insert or vcopy), `find_documents` continues to report that document even after the content is deleted from the document's V-stream." The invariant is `∀ D, α: α ∈ I-addresses-ever(D) ⟹ D ∈ FINDDOCSCONTAINING(α)` — monotonically accumulating, never shrinking.

**[EC-STALE-SPANF-REFERENCE]** (Finding 0057) confirms this with a concrete worked example:

```
Source doc S has content at I-addresses α₁..α₅
Target doc T COPYs that content → spanf registers T for α₁..α₅

After DELETE from T:
  FIND_DOCUMENTS(α₁..α₅) → {S, T}   (T is stale)
  I-to-V(α₁, T) → ∅                  (no V-position in T)
```

## For Link Endpoints Specifically

**[INT-DELETE-SPANF-DIVERGENCE]** (Finding 0057) names the resulting state precisely: after DELETE, POOM and spanfilade diverge permanently. The POOM correctly reflects the deletion; the spanfilade continues to assert the document contains those I-addresses. The asymmetric invariant that holds is: `∀ D, i : (∃ v : poom.D(v) = i) ⟹ i ∈ spanf_index(D)`, but the converse fails after DELETE.

The content identity referenced by the link endpoint occupies the same DOCISPAN entries as any other content — there is no special link-endpoint pathway. So DELETE of content that happens to be a link endpoint produces the same outcome: DOCISPAN entries persist, `find_documents_containing` still returns the document, but the POOM no longer maps those I-addresses to V-positions.

**[SS-THREE-LAYER-MODEL]** (Finding 0040) provides the architectural frame: DELETE affects only the POOM layer. The I-space (link orgl with permanent endset I-addresses) and spanfilade (DOCISPAN entries) are both frame conditions of DELETE.

The practical consequence for callers querying `find_documents_containing` after DELETE: the result is a **superset** of documents currently containing the queried I-addresses in their V-stream. Consumers must post-filter via I-to-V conversion to distinguish live from stale results — the I-to-V layer silently drops unresolvable I-addresses ([INV-ITOV-FILTERING]).

---

## Code Exploration

I have all the information needed. Here is the complete answer:

---

## Answer: DOCISPAN Entries After Deleting Link-Endpoint Content

### Short answer

**Yes** — DOCISPAN entries for deleted content persist unchanged in the spanfilade, and `find_documents_containing` continues to report the document as containing that content even after it has been deleted. The connection to a link endpoint is irrelevant; the behavior is unconditional.

---

### The DELETE execution path

`deletevspan` in `fns.c:333-347` calls `dodeletevspan` in `do1.c:158-167`:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```

`deletevspanpm` in `orglinks.c:145-152` calls `deletend` only on the document's POOM (the `docorgl` argument, found in `granf`):

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` in `edit.c:31-76` operates exclusively on the enfilade node passed as its first argument (`docorgl`), which is the document's permutation matrix (POOM). It cuts that enfilade in V-space, removing the V→I mapping for the deleted region.

**There is no call to `spanf` anywhere in this path.** The spanfilade is not touched.

---

### How DOCISPAN entries are created

Compare against `docopy` in `do1.c:45-65`, which is called by every INSERT and COPY operation:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   /* do1.c:60 — POOM update */
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) /* do1.c:62 — spanf update */
```

`insertspanf` in `spanf1.c:15-54` calls `insertnd` on `spanf` (not `granf`) with `spantype = DOCISPAN = 4` (`xanadu.h:39`). This records, in the global spanfilade, that the document (`docisaptr`) contains the given I-addresses (`ispanset`).

---

### No deletion function exists for the spanfilade

Searching `spanf1.c` and `spanf2.c` completely: the available functions are `insertspanf`, `findlinksfromtothreesp`, `finddocscontainingsp`, `findnumoflinksfromtothreesp`, `retrieveendsetsfromspanf`, `retrievesporglsetinrange`. **There is no `deletespanf`, no `removespanf`, no cleanup path of any kind.** The spanfilade is write-only.

---

### How `finddocscontainingsp` queries the spanfilade

`finddocscontainingsp` in `spanf1.c:151-188`:

```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);   /* spanf1.c:168 */
tumblerincrement (&docspace.width, 0, 1, &docspace.width);             /* spanf1.c:169 */
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                  ispanset, SPANRANGE, (typeisa*)NULL);  /* spanf1.c:171 */
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        ...
        addresssetptr = (typelinkset *) onitemlist(...);
    }
}
```

It queries `spanf` in the DOCISPAN (4) lane for any crum whose SPAN dimension overlaps the given I-address range. Because those crums are never removed, any document that ever held the deleted I-addresses will be returned.

---

### The link endpoint angle makes no difference

When a link is created pointing at content in document D, `docreatelink` in `do1.c:195-221` calls `insertendsetsinspanf` (`spanf2.c:116-128`), which records three additional spanfilade entries in lanes `LINKFROMSPAN` (1), `LINKTOSPAN` (2), and `LINKTHREESPAN` (3). These are **separate** from the DOCISPAN (4) entries.

The DOCISPAN entries were placed in the spanfilade earlier — when the content was originally inserted or copied into D. The link creation does not create new DOCISPAN entries and does not change the existing ones. When D later deletes the content:

- `deletend` on `docorgl` (in `granf`) removes the V→I mapping from D's POOM — `orglinks.c:149`.
- The DOCISPAN entry in `spanf` is left intact — the same code path, the same absence of cleanup.
- The link's LINKFROMSPAN / LINKTOSPAN entries are **also** left intact (same write-only spanfilade design, consistent with Finding 0024).

---

### Call trees in summary

**COPY / INSERT — creates DOCISPAN:**
```
fns.c:insert()  or  fns.c:copy()
  → do1.c:doinsert() / docopy()
      → orglinks.c:insertpm()          ← POOM update (granf)
      → spanf1.c:insertspanf(..., DOCISPAN)  ← spanf update
```

**DELETE — no spanfilade update:**
```
fns.c:deletevspan()
  → do1.c:dodeletevspan()
      → orglinks.c:deletevspanpm()
          → edit.c:deletend(docorgl, …, V)  ← POOM update only (granf)
      ← returns; spanf never touched
```

---

### Behavioral consequence

After the delete:

1. `finddocscontainingsp` queries `spanf` for DOCISPAN crums covering the deleted I-addresses. It still finds D. It returns D in the document set. `find_documents_containing` reports D as containing that content.

2. If a caller then tries to convert those I-addresses back to V-addresses in D (via `vspanset2ispanset` / `permute` in `orglinks.c:397-402`, which walks D's POOM in `granf`), the permutation table has no entries for that V-range — the lookup returns empty.

So: **DOCISPAN entries persist unchanged** (`spanf` is write-only), **`find_documents_containing` still returns the document** (it queries only `spanf`), and the stale reference is only exposed as empty when a subsequent retrieve on that document is attempted. This is confirmed by Finding 0057 (code inspection) and Finding 0023 (golden test observation).

---

## Question 13 [gregory]

> When `FOLLOWLINK` retrieves endsets for an orphaned link (no V-space references to endpoint I-addresses), does `span2spanset` return empty specsets, partial specsets, or does it error — and what exact filtering occurs during I→V conversion?

### Gregory's Answer

## KB Synthesis

## FOLLOWLINK with Orphaned Links: I→V Filtering Behavior

The KB answers this precisely across several entries. Here's the synthesis:

### The Call Chain

From [SS-FOLLOWLINK] (Finding 0048), FOLLOWLINK operates in two phases:

1. **Phase 1 — I-address extraction:** `link2sporglset()` reads the link orgl at the requested endset position (0.1, 0.2, or 0.3) via `retrieverestricted()`. **No POOM check occurs here.** This phase always succeeds if the link orgl exists.

2. **Phase 2 — I→V conversion:** `linksporglset2specset()` converts the extracted I-addresses to V-addresses by looking them up in the specified `homedoc`'s POOM via `span2spanset()`. This is where filtering occurs.

### The Exact Filtering Mechanism

From [INV-ITOV-FILTERING] (Finding 0048), the filtering is at `span2spanset()` in `backend/orglinks.c:425-449`:

> If `retrieverestricted()` returns NULL (I-address not found in POOM), the I-address is **silently dropped** — no V-span is added to the result.

No error is raised. No placeholder is inserted. The I-address simply disappears from the output.

This is a **universal invariant** — not behavior specific to FOLLOWLINK:

> `∀ op returning V-addresses: v ∈ result(op) → ∃ d, i : poom.d(v) = i ∧ i ∈ dom.ispace`

### The Three Observable Cases

From [EC-GHOST-LINK] (Finding 0048):

| Endset I-addresses | Result |
|---|---|
| All have POOM mappings | Full specset returned |
| Some have POOM mappings | **Partial specset** — only live addresses converted, rest silently dropped |
| None have POOM mappings | **Empty specset `[]`** — operation still succeeds with `works: true` |

Golden test `golden/links/orphaned_link_target_all_deleted.json` confirms the empty-but-successful case.

### No Error in Any Case

From [PRE-FOLLOWLINK] (Finding 0048):

> There is no precondition requiring that endset I-addresses be currently referenced in any POOM. The operation succeeds even when all endset I-addresses are unreferenced, returning an empty result rather than an error.

The precondition is strictly about **link existence** (the link orgl must exist in the granf), not about liveness of the content it points to.

### One Anomaly

From [EC-ORPHANED-LINK] (Finding 0024), there is one unexplained behavior in the behavior matrix:

| Deleted content | SOURCE result | TARGET result | TYPE result |
|---|---|---|---|
| Both source + target | `[]` | `[]` | `[]` ← **unexpected** |

When both endpoints are deleted, `follow_link(link_id, LINK_TYPE)` also returns empty even though the type endset references the bootstrap document (which was not deleted). This is noted as either a bug or an undocumented dependency of type resolution on endpoint resolution. The KB does not resolve this.

### Summary

- **Empty specset** when all I-addresses are unreferenced — no error, succeeds
- **Partial specset** when some I-addresses are unreferenced — unreferenced ones silently dropped
- **Full specset** when all I-addresses are live
- The filtering is performed by `span2spanset()` → `retrieverestricted()` → NULL check at `orglinks.c:446-448`
- This filtering is the same mechanism used by RETRIEVEENDSETS [SS-RETRIEVE-ENDSETS]
- The key invariant: `actual_V_results ⊆ link_endset_I_addresses` — you can only get back V-spans for I-addresses that currently have POOM mappings

---

## Code Exploration

I have all the code I need. Here is the complete answer.

---

## FOLLOWLINK on Orphaned Links: I→V Filtering Analysis

### Execution Path Overview

```
followlink()          [fns.c:114]
  └─ dofollowlink()   [do1.c:223]
       ├─ link2sporglset()        [sporgl.c:67]   ← retrieve endset I-spans from link's POOM
       └─ linksporglset2specset() [sporgl.c:97]   ← convert I-spans → V-spans
            └─ linksporglset2vspec()  [sporgl.c:127]
                 └─ sporglset2vspanset() [sporgl.c:141]
                      └─ ispan2vspanset()   [orglinks.c:389]
                           └─ permute()        [orglinks.c:404]
                                └─ span2spanset() [orglinks.c:425]  ← I→V filtering
                                     └─ retrieverestricted() [retrie.c:56]
                                          └─ findcbcinarea2d() / crumqualifies2d() [retrie.c:229,270]
```

---

### Stage 1: `link2sporglset` — Retrieving Endset I-Spans from the Link's Own POOM

`sporgl.c:67-95`:

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type)
{
    if (!findorgl (taskptr, granf, linkisa, &orgl, type))
        return (FALSE);
    tumblerincrement (&zero, 0, whichend, &vspan.stream);
    tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);
    if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
        for (c = context; c; c = c->nextcontext) {
            contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
            ...
        }
        return (TRUE);
    } else {
        return (FALSE);   ← *** CRITICAL: returns FALSE if no endsets in link POOM ***
    }
}
```

This call looks inside the **link's own POOM** at V-space position `whichend` (1 = FROM, 2 = TO) to retrieve the I-spans stored there at link creation by `insertendsetsinorgl`.

**For a properly created but later-orphaned link**: the link's POOM still has its endset I-spans at those V-positions (they were written by `insertpm` [orglinks.c:75] and are never cleared). `retrieverestricted` finds them, `context` is non-NULL, `link2sporglset` returns **TRUE** with a populated sporglset.

**For a link with no endsets in its POOM** (different failure mode, not the orphaned case): `context` is NULL → `link2sporglset` returns **FALSE** → `dofollowlink` short-circuits to FALSE → `followlink` calls `putrequestfailed` [fns.c:126]. **This is the only path that errors.**

---

### Stage 2: `linksporglset2specset` — Building the Specset

`sporgl.c:97-123`:

```c
bool linksporglset2specset(typetask *taskptr, typeisa *homedoc, typesporglset sporglset, typespecset *specsetptr, int type)
{
    *specsetptr = NULL;
    for (; sporglset; sporglset = ...) {
        specset = (typespecset) taskalloc(taskptr, sizeof(typevspec));
        if (iszerotumbler(&sporglset->sporgladdress)) {
            // raw I-span: copy directly as ISPANID
        } else {
            linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
        }
        *specsetptr = specset;       ← always appended, regardless of vspanset content
        ...
    }
    return (TRUE);                   ← always returns TRUE
}
```

For each endset sporgl (which has a non-zero home document address), it calls `linksporglset2vspec`.

`sporgl.c:127-137`:
```c
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc, typesporglset *sporglsetptr, typevspec *specptr, int type)
{
    specptr->itemid = VSPECID;
    specptr->next = NULL;
    movetumbler(homedoc, &specptr->docisa);
    specptr->vspanset = NULL;        ← initialized to NULL
    sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```

`vspanset` is set to NULL *before* the conversion. If the conversion adds nothing, it stays NULL. The function has no return value and no error path.

---

### Stage 3: `sporglset2vspanset` → `ispan2vspanset` → `permute` → `span2spanset`

`sporgl.c:141-176` calls `ispan2vspanset` [orglinks.c:389], which calls `permute` [orglinks.c:404]:

```c
typespanset *permute(typetask *taskptr, typeorgl orgl, typespanset restrictionspanset, INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    typespanset *save = targspansetptr;    ← saves pointer to vspanset field
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
    }
    return (save);   ← returns the saved pointer (pointing to the vspanset field)
}
```

`permute` returns `save` — the original pointer, which points to `specptr->vspanset`. If `span2spanset` adds nothing, `*save` remains NULL.

---

### Stage 4: `span2spanset` — The Exact I→V Filtering

`orglinks.c:425-454`:

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr, INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    typecontext *context, *c, *retrieverestricted();
    typespan foundspan;
    typespan *nextptr;

    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                                  (typespan*)NULL, targindex, (typeisa*)NULL);
    ←  ^^^^ looks up the I-span in the home document's POOM, requesting V-space mapping

    for (c = context; c; c = c->nextcontext) {
        context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
        nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
    }

    if (!context) {              ← [orglinks.c:446]
        return (targspansetptr); ← returns pointer unchanged — NO entries added
    }
    contextfree(context);
    return (&nextptr->next);
}
```

For an **orphaned I-span** (no V-space coverage in the home document's POOM):

1. `retrieverestricted` calls `retrieveinarea` [retrie.c:87] → `findcbcinarea2d` [retrie.c:229].
2. `findcbcinarea2d` walks the POOM tree, calling `crumqualifies2d` [retrie.c:270] on each crum. `crumqualifies2d` checks whether the crum's **I-space range** (`dsas[index1]`) overlaps the requested I-span, and whether the crum's **V-space range** (`dsas[index2]`) satisfies any constraints.
3. For an orphaned I-span (its content was deleted from V-space), no POOM crums have an I-space range covering that I-address — those crums were removed by `deletend` during the delete operation. `crumqualifies2d` returns FALSE for all crums.
4. `findcbcinarea2d` appends nothing to the context list.
5. `retrieverestricted` returns **NULL**.
6. Back in `span2spanset`: `!context` is TRUE at `orglinks.c:446`. The function returns `targspansetptr` unchanged. **`nextptr` is never assigned** — the early return via the `if(!context)` guard avoids any undefined access.
7. No V-spans are added to the target spanset.

---

### Final Result: What FOLLOWLINK Returns

For an orphaned link (properly created, endsets exist in link's POOM, but those I-addresses have no V-space coverage in the home document):

| Layer | Result |
|---|---|
| `link2sporglset` [sporgl.c:67] | **TRUE** — endset I-spans found in link's POOM at `whichend` position |
| `linksporglset2specset` [sporgl.c:97] | **TRUE** — always returns TRUE |
| `span2spanset` [orglinks.c:446] | Returns `targspansetptr` unchanged — **zero V-spans added** |
| `specptr->vspanset` | Remains **NULL** |
| `dofollowlink` [do1.c:228] | **TRUE** |
| `followlink` [fns.c:123] | Calls `putfollowlink(taskptr, specset)` — **success response sent** |

**Answer**: `span2spanset` returns **partial (empty) specsets** — not an error. The returned specset contains one or more `typevspec` items (one per home document referenced by the endsets), each with the correct `docisa` field but with `vspanset = NULL`. No error is signaled.

The filtering is entirely silent: `retrieverestricted` / `crumqualifies2d` [retrie.c:270] finds no POOM crums whose I-space range covers the orphaned I-address, returns NULL, and `span2spanset` returns early at `orglinks.c:446` without adding any V-span to the target spanset. The containing `linksporglset2specset` never checks whether `vspanset` is populated — it always returns TRUE.

The only scenario that produces `putrequestfailed` is if `link2sporglset` itself returns FALSE [sporgl.c:92], which happens only when the link has **no endsets stored in its POOM at the requested endpoint position** — a structurally different case from a properly-created link whose endpoints have since been deleted from V-space.

---

## Question 14 [gregory]

> If orphaned content at I-address range `[.0.1.3, .0.1.5]` is later transcluded into a new document via COPY, does `find_links` on that new document immediately discover the previously orphaned link without any re-indexing step?

### Gregory's Answer

## KB Synthesis

## Answer: Yes — Immediate Re-discoverability, No Re-indexing Required

The orphaned link becomes immediately discoverable from the new document the moment COPY places those I-addresses into its POOM. Here is the chain of evidence:

---

### Why the Link Was Undiscoverable (Orphaned State)

From [EC-ORPHANED-LINK] (Findings 0005, 0024): A link is undiscoverable via `find_links` when "no document contains content identities matching its endpoints." Specifically, the link object itself is intact in I-space, and critically, **its spanfilade entries were never removed**.

From [INV-SPANF-WRITE-ONLY] (Finding 0057): The spanfilade is append-only. `deletespanf` does not exist anywhere in the codebase. DELETE operations modify only the POOM and never touch the spanfilade. The link's endpoint entries — mapping `[.0.1.3, .0.1.5]` → link ISA — have been sitting in the spanfilade intact since link creation.

From [ST-DELETE] (Finding 0057): `dodeletevspan` calls only `deletevspanpm` (granf POOM) and `logbertmodified`. No spanf call exists in that path.

---

### What COPY Does

From [ST-VCOPY] / [ST-COPY]: COPY shares existing I-addresses — it calls `insertpm` to create new POOM entries in the target document mapping V-positions to the **same I-addresses** (`[.0.1.3, .0.1.5]`). No new I-addresses are allocated.

From [FC-CONTENT-SPANF-ISOLATION] (Finding 0036, refined): COPY also calls `insertspanf(..., DOCISPAN)`, creating new DOCISPAN entries in the spanfilade. These are the document-discovery index — separate from the link discovery index (LINKFROMSPAN/LINKTOSPAN).

---

### Why find_links Works Immediately

From [SS-FIND-LINKS] (Finding 0028): `find_links(search_specset)` operates as:
1. Convert search specset → I-addresses (via the new document's POOM)
2. Search the spanfilade's **link index** (LINKFROMSPAN/LINKTOSPAN entries) for those I-addresses
3. Return links where `I-addresses(search) ∩ I-addresses(link.endpoint) ≠ ∅`

After COPY into the new document:
- The new document's POOM maps V-positions → `[.0.1.3, .0.1.5]`
- Step 1 above recovers those I-addresses
- Step 2 finds the link's spanfilade entries, which were **never deleted**
- The intersection is non-empty → link returned

No re-indexing is needed because the link's spanfilade entries function as a **permanent historical journal** [INV-SPANF-WRITE-ONLY]. The orphaned state was never about those entries disappearing — it was only about the POOM having no entries for those I-addresses.

---

### Confirmatory Evidence

From [INT-LINK-TRANSCLUSION] (Finding 0028): "Transclusion creates shared content identity between documents. The only link-relevant effect of transclusion is sharing I-addresses, which enables link discovery from the destination document."

This principle applies equally to the orphaned case: the mechanism is identical whether the link was previously orphaned or has always been active. The spanfilade entry is the permanent record; POOM membership determines whether conversion from V-space to I-space can reach it.

From [INT-TRANSCLUSION-LINK-SEARCH] (Finding 0029): "When content is transcluded to another document, the copy retains the original content identity. If the original content is deleted, links remain discoverable from the copy." This scenario — delete from source, still findable from copy — is the same mechanism in reverse. Here, content was deleted from all documents (orphaned), then re-introduced via COPY; the result is identical discoverability.

---

### Summary

| State | POOM has I-addresses | Spanfilade link entry | find_links result |
|-------|---------------------|----------------------|-------------------|
| Link created | Yes | Yes | Found |
| Content deleted (orphaned) | No | Yes | Not found |
| Content COPYed into new doc | Yes (new doc) | Yes (unchanged) | **Found immediately** |

The re-discoverability is automatic, instantaneous, and requires no re-indexing — the spanfilade link entries have been waiting intact the entire time.

---

## Code Exploration

Now I have everything I need. Let me trace the complete execution path.

---

## Answer: Yes — `find_links` Discovers the Orphaned Link Immediately, Without Re-Indexing

### The Architectural Invariant

The spanfilade (`spanf`) is a **globally-persistent, I-address-keyed index**. Link endpoints are inserted into it at the moment a link is created, keyed by permascroll I-address — not by which documents currently include that content. The key insight: the POOM (permutation matrix enfilade, `granf`) maintains the V↔I mapping per document, while `spanf` records the link-endpoint-to-I-address association independently.

---

### Step 1: Link Creation Writes to the Spanfilade by I-Address

When `docreatelink` runs (`do1.c:195–221`), the link endpoints are written to `spanf` via `insertendsetsinspanf`:

```c
// do1.c:219
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

This calls `insertspanf` (`spanf1.c:15`):

```c
// spanf1.c:22–23
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
// ...
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

For the link targeting `[.0.1.3, .0.1.5]`, this writes one entry to `spanf`:
- **SPANRANGE** axis = `[.0.1.3, .0.1.5]` (the I-address range)
- **ORGLRANGE** axis = `link_ISA` prefixed with `LINKFROMSPAN` (or `LINKTOSPAN`)

This entry is **permanent**. It is never deleted when the content becomes "orphaned" (unreferenced by any living document). There is no orphan-detection or index-maintenance code anywhere in `do1.c`, `do2.c`, or `spanf1.c`.

---

### Step 2: COPY Updates the POOM — Not the Spanfilade

`docopy` (`do1.c:45–65`) does exactly two structural writes:

```c
// do1.c:60–62
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // ← updates new doc's POOM (V→I)
&& insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) // ← records doc-contains-I in spanf
```

1. `insertpm` maps the destination document's new V-address (`vsaptr`) onto the source I-addresses `[.0.1.3, .0.1.5]` in `granf`.
2. `insertspanf` with `DOCISPAN` records "document `D_new` contains I-addresses `[.0.1.3, .0.1.5]`" in `spanf` — entirely separate from the `LINKFROMSPAN`/`LINKTOSPAN` entries.

Crucially, `docopy` does **not** scan the existing link entries in `spanf`, does not re-index them, and does not write any new `LINKFROMSPAN`/`LINKTOSPAN` entries. Those already exist from link creation time.

---

### Step 3: `find_links` Translates V→I Through the POOM, Then Queries Spanfilade by I-Address

`dofindlinksfromtothree` (`do1.c:348`) calls `findlinksfromtothreesp` (`spanf1.c:56`):

```c
// spanf1.c:71–77
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
// ...
if (fromvspecset) {
    sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

**First:** `specset2sporglset` (`sporgl.c:14`) converts the query V-specset (addresses in `D_new`) to I-addresses. It calls:

```c
// sporgl.c:44, 48
findorgl (taskptr, granf, docisa, &orgl, type)          // get new doc's POOM
vspanset2ispanset (taskptr, orgl, vspanset, &ispanset)  // V → I via POOM
```

Since COPY already inserted `[.0.1.3, .0.1.5]` into `D_new`'s POOM via `insertpm`, this translation will return exactly `[.0.1.3, .0.1.5]`.

**Second:** `sporglset2linkset` → `sporglset2linksetinrange` (`sporgl.c:239`) queries `spanf`:

```c
// sporgl.c:257–259
prefixtumbler(&orglrange->stream, spantype, &range.stream);  // spantype = LINKFROMSPAN
prefixtumbler (&orglrange->width, 0, &range.width);
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

This searches the spanfilade for any ORGLRANGE entry (link ISA prefixed with `LINKFROMSPAN`) that overlaps SPANRANGE `[.0.1.3, .0.1.5]`. The orphaned link's entry — written at creation time and never removed — is found here.

```c
// sporgl.c:263–265
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist (taskptr, linksetptr, &linksa);
}
```

The link ISA is extracted and added to the result set.

---

### Summary

| Event | What Changes |
|---|---|
| Link created on `[.0.1.3, .0.1.5]` | `spanf` gets `LINKFROMSPAN/TOSPAN` entry keyed by I-address — permanently |
| Content becomes "orphaned" (no active transclusion) | Nothing changes in `spanf`; entry persists |
| `docopy` into new document | `granf` (POOM) of `D_new` updated: new V-address → I `[.0.1.3, .0.1.5]`; `spanf` gets one new `DOCISPAN` entry |
| `find_links` on `D_new` | `specset2sporglset` maps query V→I through `D_new`'s POOM; `sporglset2linkset` finds the pre-existing link entry in `spanf` |

**The previously orphaned link is found immediately, without any re-indexing step.** This is by design: the spanfilade records link associations to content identity (I-address/permascroll position), not to document membership. The POOM provides the V→I translation layer on demand. As soon as COPY establishes the V→I mapping in the new document's POOM, `find_links` can traverse that mapping to reach the I-address, which has held the link association all along.

---

## Question 15 [gregory]

> In `sporglset2linkset`, given the `TRUE||!homeset` override that makes link search global, does an orphaned link whose endpoint I-addresses match the query spans still appear in the result set even though no POOM currently maps to those I-addresses?

### Gregory's Answer

## KB Synthesis

## Synthesis: Orphaned Links and the `TRUE||!homeset` Override

The question touches three separate mechanisms. Pulling them together:

---

### Layer 1: The spanfilade is append-only and retains all link endpoint entries

From [INV-SPANF-WRITE-ONLY], no deletion function exists in `spanf1.c` or `spanf2.c`. When a link is created, `insertendsetsinspanf()` permanently records the mapping `I-address range → link ISA`. This entry survives all subsequent document mutations including DELETE. The spanfilade does not know or care whether any POOM currently maps to those I-addresses.

### Layer 2: The spanfilade search is purely an I-address intersection — POOM state is not consulted

From [SS-THREE-LAYER-MODEL] and [FC-LINK-DELETE-ISOLATION]/Finding 0040:

> `find_links(source_specs)` → still finds the link (spanfilade intact)

after `DELETEVSPAN(2.1)` removes the link from the POOM. The three layers are independent. `find_links` routes through the spanfilade only; no `findorgl` call checks the POOM during discovery.

So the structural answer is: **if the query produces I-addresses that intersect the link's stored endpoint I-addresses in the spanfilade, the orphaned link WILL appear in results** — no POOM mapping is required at query time.

### Layer 3: The `TRUE||!homeset` override is orthogonal

From [EC-FIND-LINKS-GLOBAL]/Finding 0069, the `TRUE||!homeset` guard disables orgl-dimension filtering. The orgl dimension scopes which *documents or link orgls* are searched. This affects **who owns the indexed entries**, not **which I-addresses can be matched**.

The orphaned-link question lives entirely in the span dimension: do the query's I-addresses intersect the link's stored I-addresses? The `TRUE||!homeset` override does not expand what I-addresses are reachable — it only ensures no orgl-range filter culls them afterward.

The override therefore has no special effect on orphaned link discoverability. With or without it, a spanfilade hit on the span dimension returns the link.

---

### The Practical Barrier: V-to-I conversion

The reason orphaned links cannot be found through normal `find_links` usage is not the spanfilade — it is the *query construction* step. From [SS-FIND-LINKS]/Finding 0029 and [PRE-FIND-LINKS]/Finding 0029:

> `find_links()` requires that the searched endpoint content exists in the V-stream (visible view) to discover a link.

The call chain is: user provides a specset → `specset2ispanset` converts V-spans to I-addresses via the queried document's POOM → those I-addresses are searched in the spanfilade. If no POOM currently maps any V-position to the orphaned link's endpoint I-addresses, `specset2ispanset` returns an empty I-span set. Empty query → empty spanfilade search → empty results.

This is precisely what [EC-ORPHANED-LINK]/Finding 0005 describes:

> "it cannot be discovered via `find_links()` because no document contains content identities matching its endpoints"

The content identities (I-addresses) still exist in the granfilade [INV-IADDR-IMMUTABILITY] and the spanfilade entries still exist [INV-SPANF-WRITE-ONLY]. What fails is the V-to-I conversion that would produce a non-empty query.

---

### Definitive Answer

**Structurally yes; practically no; the override is irrelevant.**

| Question | Answer | KB basis |
|----------|--------|----------|
| Does the spanfilade still hold the orphaned link's entry? | Yes | [INV-SPANF-WRITE-ONLY] |
| Would the spanfilade return the link if given matching I-addresses? | Yes | [SS-THREE-LAYER-MODEL], [FC-LINK-DELETE-ISOLATION] |
| Does the `TRUE||!homeset` override create a new discovery path? | No — wrong dimension | [EC-FIND-LINKS-GLOBAL] |
| Can standard `find_links(specset)` reach those I-addresses when all POOMs are cleared? | No | [PRE-FIND-LINKS], [EC-ORPHANED-LINK] |
| Is the POOM consulted during the spanfilade search? | No | [SS-THREE-LAYER-MODEL] |

The override makes the search global in the orgl dimension; orphaned link inaccessibility is a span-dimension problem caused by the V-to-I conversion bottleneck. A truly orphaned link becomes accessible again only when at least one document's POOM re-acquires a mapping to those I-addresses — which is possible via COPY from the granfilade (since the bytes are permanent at their I-addresses per [INV-IADDR-IMMUTABILITY], and COPY can restore POOM mappings per [ST-COPY]/Finding 0064).

---

## Code Exploration

The file write needs permission, but the full answer is ready. Here is the complete analysis:

---

## Answer: Yes — orphaned links appear in the result set

The `sporglset2linkset` / `sporglset2linksetinrange` pipeline queries **the spanfilade only** — it has no dependency on any current POOM state. Here is the full code trace:

---

### 1. The `TRUE||!homeset` override [`sporgl.c:227`]

```c
if (TRUE||!homeset) {
    tumblerclear(&nullhomeset.stream);
    tumblerclear(&nullhomeset.width);
    nullhomeset.width.mantissa[0] = 100;   // sporgl.c:230
    nullhomeset.next = NULL;
    homeset = &nullhomeset;
}
```

`TRUE||anything` is unconditionally true. `homeset` is always replaced by a synthetic ispan with stream=0 and width=100. After `prefixtumbler(&orglrange->stream, spantype, &range.stream)` [`sporgl.c:257`], this becomes an ORGLRANGE covering `{spantype}.0` to `{spantype}.100` — effectively all link ISAs of that endpoint type. The search is global.

---

### 2. Homedoc filtering is permanently dead code [`sporgl.c:251-255`]

```c
if (FALSE/*trying to kluge links followable thru versions */
    && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    movetumbler(&((typesporgl*)sporglset)->sporgladdress, &linfo.homedoc);
  } else
    infoptr = NULL;   // sporgl.c:255 — ALWAYS reached
```

The `FALSE&&...` short-circuits unconditionally. `infoptr` is **always `NULL`** for every sporgl in the loop. The `sporgladdress` of the query sporgl is never loaded into `linfo.homedoc`.

---

### 3. The spanfilade is queried directly [`sporgl.c:259`]

```c
context = retrieverestricted(
    spanfptr,               // the SPANFILADE — not the POOM
    (typespan*)sporglset,   // query I-address span → SPANRANGE
    SPANRANGE,
    &range,                 // prefixed link-type range → ORGLRANGE
    ORGLRANGE,
    (typeisa*)infoptr       // always NULL
);
```

`spanfptr` is the spanfilade (`typespanf` / `typecuc *`), the independent 2D enfilade that was written at link creation time. The POOM is not consulted here at all.

---

### 4. NULL `infoptr` propagates through `retrieverestricted` [`retrie.c:77-83`]

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;   // docisaptr is NULL → no homedoc to filter on
}
temp = retrieveinarea(fullcrumptr, ..., (typebottomcruminfo*)infoptr);
```

`docisaptr` is NULL (from `(typeisa*)infoptr` above), so `infoptr` stays NULL all the way into `retrieveinarea` → `findcbcinarea2d` [`retrie.c:229`].

---

### 5. The homedoc guard in `crumqualifies2d` requires non-NULL `infoptr` [`retrie.c:274-280`]

```c
if ((crumptr->height == 0) && infoptr &&
    !tumblereq(&infoptr->homedoc,
               &(((type2dcbc*)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

The guard fires only when `infoptr != NULL`. Since it is always NULL on this path, **there is no document filtering**. The function proceeds to check only whether the crum's I-address range intersects the query range.

The debug build comment at `retrie.c:244-251` confirms this is by design — a non-NULL `infoptr` would call `gerror("findcbcinarea2d")`:

```c
#ifndef DISTRIBUTION
if(infoptr){
    fprintf(stderr,"not NULL infoptr versions mumble specialcase 11/27/84 "
                   "shouldent happen till we try something fancier\n");
    gerror("findcbcinarea2d");
}
```

---

### 6. The spanfilade is a permanent, independent index [`spanf1.c:22,51`]

At link creation time, `insertspanf` writes each endpoint's I-address permanently into the spanfilade:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // link ISA, prefixed
...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);   // endpoint I-address
movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

There is no code that removes spanfilade entries when content is deleted or when a POOM stops mapping to those I-addresses (see Finding 0057). The spanfilade and POOM are entirely independent structures. Content deletion (`deletend` on the POOM) removes POOM entries; it does not touch the spanfilade.

---

### Conclusion

The execution path is:

> `sporglset2linkset` → synthetic global `nullhomeset` → `sporglset2linksetinrange` → `infoptr = NULL` (dead code) → `retrieverestricted(spanfptr, query_ispan, ...)` → `findcbcinarea2d` → `crumqualifies2d` (no homedoc check, `infoptr` is NULL) → match on I-address range intersection alone → `onlinklist` adds link ISA to result

**The POOM plays no role anywhere in this chain.** The spanfilade records each link endpoint's I-address at creation time and that record persists indefinitely. An orphaned link — one whose endpoint I-addresses no longer have any POOM mapping — is indistinguishable from a live link in the spanfilade. If its stored I-addresses overlap the query spans, it appears in the result set.

The disabled `sporgladdress`-branch kluge at `sporgl.c:251` (commented "trying to kluge links followable thru versions") was apparently a planned mechanism to add per-document homedoc filtering to the spanfilade search, but it was frozen out with `FALSE&&` and never completed. Its absence is the structural reason dangling link references survive in results.

---

## Question 16 [gregory]

> When a link has three endsets (source, target, type) and only the target content is deleted from all V-streams while source content remains live, does `find_links` from the source document still discover the link — and if so, what does the returned target endset contain?

### Gregory's Answer

## KB Synthesis

## Answer

### Does `find_links` from the source still discover the link?

**Yes.** `find_links` searches the spanfilade by I-address intersection on whichever endpoint is specified. When called with source specs and NOSPECS for target, it only requires that the source endpoint's I-addresses appear in the spanfilade — the target content state is irrelevant to the query.

The behavioral matrix from [SS-FIND-LINKS] / Finding 0029 is explicit:

| Source State | Target State | Search by Source | Search by Target |
|---|---|---|---|
| Intact | Deleted | **Found** | Not found |

The spanfilade link-endpoint entries are permanent — content DELETE never removes them ([INV-SPANF-WRITE-ONLY]). So the I-address intersection between the source query and the link's source endpoint continues to succeed.

---

### What does the returned target endset contain?

**Empty** (`[]`), but the operation succeeds without error.

The mechanism is the I-to-V filtering layer ([INV-ITOV-FILTERING]):

1. The link orgl still permanently stores the target's I-addresses — they are immutable in I-space ([INV-LINK-PERMANENCE], [INV-IADDR-IMMUTABILITY]).
2. `follow_link(link, TARGET)` calls `link2sporglset()` to extract those I-addresses, then `linksporglset2specset()` to convert them to V-addresses by querying each document's POOM ([SS-FOLLOWLINK]).
3. Since target content was deleted from all documents, no POOM maps those I-addresses to any V-position.
4. At `span2spanset()` / `retrieverestricted()`, a NULL return means the I-address is silently dropped from the result — no V-span is emitted, no error is raised.
5. Result: `[]`.

This is the "ghost link" state documented in [EC-GHOST-LINK]: the link object is structurally intact and followable, but its target endpoint has no current V-position anywhere.

The orphaned-link behavior matrix from [EC-ORPHANED-LINK] / Finding 0024 confirms this directly:

| Deleted Content | `find_links` | source | target | type |
|---|---|---|---|---|
| Target text only | Works | Works | **Empty** | Works |

Note that `follow_link(link, SOURCE)` and `follow_link(link, TYPE)` continue to work normally — only the target endset is empty. The type endset goes empty only when *both* source and target are deleted (a separate anomaly noted as potentially a bug in Finding 0024).

---

### Why the endset is empty but discoverable — the architectural explanation

This behavior reflects the three-layer model ([SS-THREE-LAYER-MODEL]): link existence (I-space), link discoverability (spanfilade), and link endpoint resolution (POOM) are three independent predicates. Content DELETE operates only on the POOM layer of the target documents. It does not touch the spanfilade's link-endpoint index, so source-based discovery continues. But endpoint resolution uses the POOM of the queried document, and once all target POOMs lack those I-addresses, resolution yields empty — not an error, just no current V-positions.

---

## Code Exploration

I'll deliver the full answer directly. You can approve writing finding 0079 separately if desired.

---

## Answer: `find_links` After Target Deletion — Mechanism and Result

### Short answer

1. **Yes — `find_links` from the source document still discovers the link.** Deleting target content has no effect on the spanfilade LINKFROMSPAN entries that index the link by source content.

2. **`follow_link(link, LINK_TARGET)` returns a VSpec with the target document's ISA and an empty span list** — serialized as `[]` on the wire. The link orgl still holds the target I-spans, but I-to-V conversion silently yields nothing because the target document's POOM has no mapping for those I-spans.

---

### Part 1: Why `find_links` is unaffected

#### The deletion path (`do1.c:158-167`, `orglinks.c:145-152`)

```c
// do1.c:158
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
  );
}

// orglinks.c:145
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr,
                   typeorgl docorgl, typevspan *vspanptr)
{
  if (iszerotumbler(&vspanptr->width)) return (FALSE);
  deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
  logbertmodified(docisaptr, user);
  return (TRUE);
}
```

`deletevspanpm` calls `deletend` on `docorgl` — the **target document's POOM** — with dimension `V`. This removes the V→I mapping entry for the deleted content. **Nothing else is touched.** There is no call to any spanfilade function. No `deletespanf` function exists anywhere in `spanf1.c` or `spanf2.c` (Finding 0057).

#### What `find_links` actually queries (`spanf1.c:56-103`)

When `create_link` is called, `docreatelink` (`do1.c:195-221`) stores three groups of entries in the spanfilade via `insertendsetsinspanf`:

```
LINKFROMSPAN entry:
  ORGLRANGE (dim 0) = prefixtumbler(linkISA, LINKFROMSPAN=1) = "1.linkISA"
  SPANRANGE (dim 1) = I-span of SOURCE content
  homedoc           = source document ISA

LINKTOSPAN entry:
  ORGLRANGE (dim 0) = prefixtumbler(linkISA, LINKTOSPAN=2)   = "2.linkISA"
  SPANRANGE (dim 1) = I-span of TARGET content
  homedoc           = target document ISA
```

`findlinksfromtothreesp` (`spanf1.c:56-103`) converts the source V-spec to I-spans via `specset2sporglset`, then calls `sporglset2linkset` searching `spanf` for LINKFROMSPAN entries whose SPANRANGE intersects those I-spans:

```c
// spanf1.c:56-103 (condensed)
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr,
                             typespecset fromvspecset, ...)
{
    if (fromvspecset)
        specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
    if (fromvspecset) {
        sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset,
                          &fromlinkset, orglrange, LINKFROMSPAN);
        if (!fromlinkset) { *linksetptr = NULL; return (TRUE); }
    }
    // ... intersect from/to/three link sets ...
}
```

The query searches by **source content I-spans** in the `LINKFROMSPAN` region of the spanfilade. Deleting target content modifies the **target document's POOM** only. The source document's V→I mapping is unchanged. Source I-spans are unchanged. LINKFROMSPAN entries in the spanfilade are unchanged. The link is found.

**Empirical confirmation** from Finding 0029:

| Source State | Target State | Search by Source | Search by Target |
|---|---|---|---|
| Intact | Deleted | **Found** | Not found |

---

### Part 2: What the target endset contains

#### `dofollowlink` (`do1.c:223-232`)

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr,
                  typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  return (
     link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
  && linksporglset2specset (taskptr,
       &((typesporgl *)sporglset)->sporgladdress,
       sporglset, specsetptr, NOBERTREQUIRED));
}
```

#### Step 1: `link2sporglset` reads the link orgl, not the target POOM (`sporgl.c:67-95`)

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa,
                    typesporglset *sporglsetptr, INT whichend, int type)
{
  if (!findorgl (taskptr, granf, linkisa, &orgl, type)) return (FALSE);

  tumblerclear (&zero);
  tumblerincrement (&zero, 0, whichend, &vspan.stream);  // V = 0.2 for LINK_TARGET
  tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);

  if (context = retrieverestricted((typecuc*)orgl, &vspan, V,
                                    (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
      contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
      // sporglptr->sporgladdress = target_doc ISA   (homedoc)
      // sporglptr->sporglorigin  = I-span start of target content
      // sporglptr->sporglwidth   = I-span width
    }
    return (TRUE);
  } else { return (FALSE); }
}
```

`findorgl` locates the **link orgl** in granf under the link's own ISA — not the target document's orgl. The link orgl is a POOM storing endsets at V-positions 0.1 (from), 0.2 (to), 0.3 (three). Deleting target content does not modify the link orgl. `link2sporglset` returns the target I-spans and `homedoc=target_doc` successfully.

#### Step 2: I-to-V conversion through target's empty POOM (`sporgl.c:141-176` → `orglinks.c:425-454`)

`linksporglset2specset` → `linksporglset2vspec` → `sporglset2vspanset`:

```c
// sporgl.c:141 (condensed)
int sporglset2vspanset(typetask *taskptr, typeisa *homedoc,
                       typesporglset *sporglsetptr, typevspanset *vspansetptr, int type)
{
  (void) findorgl (taskptr, granf, homedoc, &orgl, type);  // target_doc's POOM
  movetumbler (&sporglptr->sporglorigin, &ispan.stream);
  movetumbler (&sporglptr->sporglwidth, &ispan.width);
  vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
  // ...
}
```

`ispan2vspanset` (`orglinks.c:389`) calls `permute(orgl, ispanptr, I, vspansetptr, V)` → `span2spanset` (`orglinks.c:425-454`):

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl,
                          typespanset restrictionspanptr, INT restrictionindex,
                          typespanset *targspansetptr, INT targindex)
{
  context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                                restrictionindex, (typespan*)NULL,
                                targindex, (typeisa*)NULL);
  for (c = context; c; c = c->nextcontext) {
    context2span(c, ...);
    nextptr = (typespan *)onitemlist(taskptr, ...);
  }

  if (!context) {
    return (targspansetptr);   // ← no V-spans added; pointer returned unchanged
  }
  contextfree(context);
  return (&nextptr->next);
}
```

After target content deletion, the target document's POOM has no V→I mapping for those I-spans. `retrieverestricted` returns `NULL`. `span2spanset` returns `targspansetptr` unchanged — no V-spans added. `vspanset=NULL` propagates up through `sporglset2vspanset` → `linksporglset2vspec`.

#### Step 3: What gets serialized

The resulting `typevspec` is:

```
typevspec {
  itemid   = VSPECID         (xanadu.h:VSPECID=3)
  docisa   = target_doc ISA  (still present — from link orgl's homedoc field)
  vspanset = NULL            (no current V-positions for those I-spans)
}
```

`putitem` for VSPECID (putfe.c): `VSPECFLAG + target_doc_ISA + putitemset(NULL)`. `putitemset(NULL)` writes count=0. The client receives and returns `[]`.

**Empirical confirmation** (Finding 0048, golden test `orphaned_link_target_all_deleted.json`):

```json
{"op": "follow_link", "end": "target", "result": [], "works": true}
```

---

### Part 3: `retrieve_endsets` — always `[]` for target, regardless

`doretrieveendsets` (`do1.c:369-374`) calls `retrieveendsetsfromspanf` (`spanf1.c:190-235`), which searches the spanfilade for all three span types whose SPANRANGE intersects the **source content I-spans** from the input specset.

- LINKFROMSPAN entries have **source** content I-spans as SPANRANGE → intersect → source endset found
- LINKTOSPAN entries have **target** content I-spans as SPANRANGE → no intersection with source I-spans → target always `[]`

This is structurally independent of deletion. `retrieve_endsets` called with a source specset will always return `target=[]` for any link — confirmed in Finding 0019 §6 and in `golden/endsets/retrieve_endsets.json` and `golden/endsets/endsets_compare_link_ends.json`.

---

### Complete picture

```
Deletion of target content:
  dodeletevspan() [do1.c:158]
    -> deletevspanpm() [orglinks.c:145]
         -> deletend(target_doc_orgl, V)    # V→I mapping gone from target POOM only
       # Spanfilade untouched (no deletespanf exists — Finding 0057)

find_links(source_spec) — unaffected:
  findlinksfromtothreesp() [spanf1.c:56]
    source V-spans → I-spans (source POOM intact)
    → LINKFROMSPAN entries in spanf (indexed by source I-spans, untouched)
    → link ISA recovered via beheadtumbler
    → link found

follow_link(link, LINK_TARGET) — empty V result:
  link2sporglset(link, 2) [sporgl.c:67]
    → retrieverestricted(link_orgl, V=0.2)     # link orgl intact
    → returns target I-spans + homedoc=target_doc
  linksporglset2specset() [sporgl.c:97]
    → sporglset2vspanset(target_doc_orgl) [sporgl.c:141]
         → ispan2vspanset → span2spanset [orglinks.c:425]
              → retrieverestricted(target_doc_orgl, I-span, I)
              → context = NULL (target POOM cleared)
         → vspanset = NULL
    → typevspec{docisa=target_doc, vspanset=NULL}
    → wire: []
```

Two invariants make this so:

1. **Spanfilade is write-only** (`insertspanf` exists, `deletespanf` does not — Finding 0057). LINKFROMSPAN entries are permanent. `find_links` from any intact endpoint always works regardless of what happens to other endpoints.

2. **Link orgl is independent of document POOMs**. The link's I-spans are stored in the link's own POOM entry in granf, not in the referenced documents' POOMs. Document deletion cannot retroactively alter the link orgl. The I-spans remain there; they simply have no current V-position to map to after the target content is deleted, so the query returns empty rather than failing.

---

## Question 17 [gregory]

> Does `vspanset2sporglset` ever encounter orphaned I-addresses during its POOM walk, or is it only called on V-spans known to have live POOM entries — meaning orphaned links can only be missed at the V→I conversion stage, not at the spanfilade search stage?

### Gregory's Answer

## KB Synthesis

## `vspanset2sporglset` and Orphaned I-Addresses

Short answer: `vspanset2sporglset` operates in the **V→I direction** and will not encounter orphaned I-addresses during its POOM walk. Orphaned links can only be missed at the **I→V conversion stage** — the reverse path. Here is the full reasoning.

---

### What `vspanset2sporglset` actually does

From [SS-VSPAN-TO-SPORGL] (Finding 0013) and [ST-LINK-CREATE] Finding 0037, the call chain is:

```
V-span → vspanset2ispanset → permute → span2spanset → retrieverestricted
```

`retrieverestricted` queries the document's POOM by V-position range, returning the I-addresses currently mapped there. It reads **live POOM entries only** — whatever V→I mappings currently exist in the tree.

This is a V→I lookup. The function starts from a caller-provided V-span representing a position in current V-space, walks the POOM tree, and returns the I-addresses mapped to those positions. It has no mechanism to "see" I-addresses that are no longer in the POOM, because those were removed from the tree by [ST-DELETE] (via `disown` + `subtreefree` on the relevant bottom crums — [SS-POOM-MUTABILITY]).

---

### Why orphaned I-addresses are invisible to this path

From [INV-IADDR-IMMUTABILITY] (Findings 0030, 0064): I-addresses in the granfilade are permanent. But from [ST-DELETE] (Finding 0064): DELETE removes the V→I mappings from the POOM. An "orphaned" I-address is one that still exists in the granfilade but is no longer mapped to any V-position in any POOM.

When `vspanset2sporglset` queries the POOM for a given V-span, it can only find what is currently mapped. Deleted I-addresses are absent from the POOM tree — `retrieverestricted` will return nothing for those positions. The orphaned I-addresses are not "encountered and rejected"; they are simply absent from the query's result set.

The one edge-case exception would be the negative-V-position scenario from [EC-DEEPLY-ORPHANED-LINK]: if DELETE shifted a POOM entry to a negative V-position (theoretically possible for same-exponent, same-subspace cases per Finding 0053, though cross-subspace cases are protected by `strongsub`'s exponent guard per Finding 0055), such entries exist in the POOM tree but are unreachable by any positive V-span query. `vspanset2sporglset` with a positive V-span would still not encounter them.

---

### Where orphaned links ARE filtered

The filtering happens in the **opposite direction**: I-addresses → V-addresses, in the FOLLOWLINK / RETRIEVEENDSETS path.

From [INV-ITOV-FILTERING] (Finding 0048): both FOLLOWLINK and RETRIEVEENDSETS share the path:

```
link endset I-addresses → linksporglset2specset → sporglset2vspanset →
  ispan2vspanset → permute → span2spanset → retrieverestricted
```

At `span2spanset`, `retrieverestricted` is called on the **target document's POOM** looking up I-addresses. If an I-address has no current POOM mapping (because the content was deleted), `retrieverestricted` returns NULL, and `span2spanset` silently drops that I-address without adding any V-span to the result ([SS-FOLLOWLINK], `orglinks.c:446-448`).

This is the universal filtering invariant: **unreferenced I-addresses are silently excluded from V-address results** ([INV-ITOV-FILTERING]).

---

### The stale spanfilade is a separate concern

There is a related but distinct stale-data problem at the spanfilade search stage ([EC-STALE-SPANF-REFERENCE], [INT-DELETE-SPANF-DIVERGENCE]): FIND_DOCUMENTS can return documents that no longer contain content at those I-addresses, because spanfilade entries are never deleted ([INV-SPANF-WRITE-ONLY]). But this is about the I-address → document index, not about `vspanset2sporglset`'s POOM walk.

---

### Summary

| Stage | Direction | Orphaned I-addresses |
|-------|-----------|---------------------|
| `vspanset2sporglset` (link creation, `find_links` input) | V → I (POOM read) | Never encountered — deleted content is absent from POOM |
| `linksporglset2specset` (FOLLOWLINK, RETRIEVEENDSETS) | I → V (POOM read) | Silently dropped via NULL check in `span2spanset` |
| `finddocscontainingsp` (FIND_DOCUMENTS) | I → doc (spanfilade read) | Stale entries returned — spanfilade is write-only |

`vspanset2sporglset` is only called on V-spans from the current document state. Those V-spans either map to live POOM entries (producing I-addresses) or fall outside the document's current extent (producing empty results). The orphaned-link filtering exclusively belongs to the I→V conversion stage, enforced by [INV-ITOV-FILTERING] as an architectural invariant of the `retrieverestricted` → `span2spanset` path.

---

## Code Exploration

Now I have all the code I need to answer definitively. Here is the full analysis:

---

## Answer: `vspanset2sporglset` and Orphaned I-Addresses

### The Short Answer

`vspanset2sporglset` **does not encounter orphaned I-addresses during its POOM walk**. The POOM is structurally clean — when a V-span is deleted, its crums are fully removed. If a V-span has no POOM entry, the function returns an empty sporgl set silently, without producing any I-address at all. **Orphaned links are missed exclusively at the V→I conversion stage, never at the spanfilade search stage.**

---

### Code Trace

#### Entry Point: `specset2sporglset` [sporgl.c:14–33]

```c
bool specset2sporglset(typetask *taskptr, typespecset specset, typesporglset *sporglsetptr, int type)
{
    for (; specset; specset = ...) {
        if (itemid == ISPANID) {
            *sporglsetptr = (typesporglset)specset;          // raw I-span: pass through
            ...
        } else if (itemid == VSPECID) {
            if (!(sporglsetptr = vspanset2sporglset(         // V-spec: convert V→I
                taskptr, &vspec->docisa, vspec->vspanset, sporglsetptr, type))) {
                return (FALSE);
            }
        }
    }
    ...
}
```

This is the only caller of `vspanset2sporglset`. It passes the user-supplied vspec directly, with **no precondition that the V-spans are live**.

`specset2sporglset` is called from:
- `domakelink` [do1.c:187–188] and `docreatelink` [do1.c:214–216] — link creation, with user-provided from/to specsets
- `findlinksfromtothreesp` [spanf1.c:71–75] — link search queries
- `retrieveendsetsfromspanf` [spanf1.c:222] — link endset retrieval

None of these callers validate that the V-spans exist in the POOM before passing them in.

---

#### The POOM Walk: `vspanset2sporglset` [sporgl.c:35–65]

```c
typesporglset *vspanset2sporglset(typetask *taskptr, typeisa *docisa, typevspanset vspanset, ...)
{
    ispanset = NULL;
    if (!findorgl(taskptr, granf, docisa, &orgl, type)) {   // [sporgl.c:44] get document's POOM
        return (NULL);
    }
    for (; vspanset; vspanset = vspanset->next) {
        (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // [sporgl.c:48] V→I via POOM
        for (; ispanset; ispanset = ispanset->next) {
            sporglset = taskalloc(taskptr, sizeof(typesporgl));
            movetumbler(docisa, &sporglset->sporgladdress);       // doc ISA
            movetumbler(&ispanset->stream, &sporglset->sporglorigin);   // I-address
            movetumbler(&ispanset->width,  &sporglset->sporglwidth);
            ...
        }
    }
    return (sporglsetptr);
}
```

`vspanset2ispanset` [orglinks.c:397–402] is a thin wrapper:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, ...)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

---

#### The POOM Tree Walk: `permute` → `span2spanset` → `retrieverestricted`

`permute` [orglinks.c:404–422] iterates each span and calls `span2spanset` [orglinks.c:425–454]:

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr, ...)
{
    context = retrieverestricted((typecuc*)orgl, restrictionspanset, V,
                                 (typespan*)NULL, I, (typeisa*)NULL);  // [orglinks.c:435]
    for (c = context; c; c = c->nextcontext) {
        context2span(c, ...);
        nextptr = (typespan *)onitemlist(taskptr, ...);
    }
    if (!context) {
        return (targspansetptr);     // [orglinks.c:446] silently returns unchanged pointer
    }
    contextfree(context);
    return (&nextptr->next);
}
```

`retrieverestricted` [retrie.c:56–85] → `retrieveinarea` [retrie.c:87–110] → `findcbcinarea2d` [retrie.c:229–268]:

```c
int findcbcinarea2d(typecorecrum *crumptr, ..., typecontext **headptr, ...)
{
    for (; crumptr; crumptr = getrightbro(crumptr)) {
        if (!crumqualifies2d(crumptr, ...)) {
            continue;                // V-span doesn't overlap this crum: skip
        }
        if (crumptr->height != 0) {
            findcbcinarea2d(findleftson((typecuc*)crumptr), ...);   // descend
        } else {
            context = makecontextfromcbc((typecbc*)crumptr, ...);   // leaf: add to context
            incontextlistnd(headptr, context, index1);
        }
    }
}
```

**Key observation**: If the V-span has no matching crum in the POOM, no context is returned, `span2spanset` hits the `if (!context)` branch [orglinks.c:446], and returns `targspansetptr` unchanged. The `ispanset` stays NULL. No sporgl is created. Nothing goes to the spanfilade search stage.

---

#### Why There Are No Orphaned I-Addresses Inside the POOM

When `dodeletevspan` [do1.c:158–167] removes content:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`deletevspanpm` [orglinks.c:145–152] calls `deletend` [edit.c:31–76]:

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    for (ptr = findleftson(father); ptr; ptr = next) {
        switch (deletecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 1:
            disown((typecorecrum*)ptr);
            subtreefree((typecorecrum*)ptr);      // [edit.c:59–61] crum completely removed
            break;
          case 2:
            tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
            break;                                // [edit.c:63] crum shifted (not stale)
        }
    }
    setwispupwards(father, 1);
    recombine(father);
}
```

Crums in the deleted V-range are either **fully removed from the tree** (`disown + subtreefree`) or **shifted in V-space** (adjusting their displacement). There is no case where a crum is left in the tree with a stale or dangling I-address. The POOM is structurally clean after every deletion.

Additionally, `findcbcinarea2d`'s `infoptr` argument is `NULL` when called from `span2spanset` [orglinks.c:435] — no homedoc filtering is applied. All crums found in the POOM are returned. None of them are "orphaned" in the sense of having invalid I-addresses: the permascroll (granfilade) is immutable. Once an I-address is written there by `inserttextgr`, it persists permanently. Any I-address the POOM maps to is valid.

---

### Where Orphaned Links *Are* Missed

The miss happens **before any I-address is produced**, not after:

```
V-span deleted from POOM
    → findcbcinarea2d finds no qualifying crums
    → context = NULL
    → span2spanset returns unchanged ispansetptr
    → ispanset remains NULL
    → sporgl loop in vspanset2sporglset does not execute
    → sporglset returned is empty
    → sporglset2linkset is never called with the relevant I-address
    → link is silently missed
```

The spanfilade is never queried. The spanfilade itself **still contains** the link endpoint I-addresses at their immutable location (Finding 0057: spanfilade is append-only, no delete function exists). The information to find the link is in the spanfilade — but the V→I bridge (POOM) has been broken, so `vspanset2sporglset` produces no sporgl, and the spanfilade is never asked.

---

### The Asymmetry This Creates

| Query method | After source V-span deleted | After source V-span intact |
|---|---|---|
| `find_links(source_vspec)` | **Miss** — POOM has no V→I mapping | **Hit** — V→I→sporgl→spanfilade works |
| `follow_link(link_id, SOURCE)` | **Hit** — goes I→V via link orgl in granf | **Hit** — same path |
| `find_documents(I-address)` | **Hit** (stale) — spanfilade retains the entry | **Hit** — live entry |

Finding 0024 (Orphaned Link Behavior Matrix) confirmed this empirically:
- "Source text only deleted": `find_links` → empty; `follow_link` SOURCE → empty; `follow_link` TARGET → works.

The *discovery* path (`find_links` → `vspanset2sporglset`) breaks at the V→I conversion. The *direct access* path (`follow_link`) bypasses the POOM and hits the link orgl directly. The *spanfilade* never forgets.

---

### Conclusion

**`vspanset2sporglset` cannot encounter orphaned I-addresses during its POOM walk because there are none to encounter.** The POOM is structurally consistent: `deletend` [edit.c:31–76] either completely removes crums or shifts them; it never leaves stale entries. Every I-address a POOM crum references is valid in the immutable granfilade.

However, `vspanset2sporglset` **is freely called on V-spans that have no POOM entries** — it has no precondition requiring live entries. When this happens, the POOM walk returns nothing, the ispanset stays empty, no sporgl is created, and the spanfilade search stage is never reached.

**Orphaned links are therefore missed exclusively at the V→I conversion stage** [sporgl.c:48 / orglinks.c:446], not at the spanfilade search stage. The structural reason: the POOM and the granfilade are both clean (one is consistently maintained, one is immutable). The conceptual asymmetry — that the spanfilade retains all historical I-addresses while the POOM only contains current mappings — means the information *exists* in the system but is unreachable via the V-addressed query path.

---

## Question 18 [gregory]

> If a link's target spans two I-address ranges and only one range is deleted from all POOMs while the other remains live in some document, does `find_links` discover the link through the surviving range, and does `RETRIEVEENDSETS` return just the surviving portion or both ranges?

### Gregory's Answer

## KB Synthesis

## Partial endset survival: find_links and RETRIEVEENDSETS

This scenario — a link target split across two I-address ranges, one fully deleted — is addressed directly and indirectly by several KB entries.

---

### Does `find_links` discover the link through Range B?

**Yes.** Here is why each layer behaves this way:

**Spanfilade is write-only.** When the link was created, `insertendsetsinspanf` populated the spanfilade with entries mapping *both* Range A's I-addresses → link_id and Range B's I-addresses → link_id. [INV-SPANF-WRITE-ONLY] confirms these entries are permanent — no delete operation touches the spanfilade. Range A's entry persists even though Range A is no longer in any POOM.

**Discovery is by I-address intersection in the spanfilade.** From [SS-FIND-LINKS] Finding 0028, `find_links` converts the search specset to I-addresses and checks for spanfilade matches. The specset is a V-span in a specific document, so it can only map to I-addresses that exist in some document's POOM. Since Range B is still live in doc_X, a specset targeting doc_X's Range B content maps to Range B I-addresses → spanfilade lookup → link found.

**Range A is not searchable via V-specsets.** Because Range A is deleted from all POOMs, no V-specset can be constructed that maps to Range A's I-addresses. The stale spanfilade entry for Range A is unreachable by V-address queries — but this has no effect on Range B's discoverability. The two I-spans in the endset are indexed independently. [EC-LINK-PARTIAL-SURVIVAL] states this directly: "each I-span in a link endset independently tracks its content."

---

### Does `RETRIEVEENDSETS` return just Range B, or both ranges?

**Just Range B** (when querying from a document with Range B in its POOM).

The mechanism is the I-to-V conversion filter. From [SS-FOLLOWLINK] Finding 0048 and [INV-ITOV-FILTERING]:

> unreferenced I-addresses are silently excluded from V-address results

The call chain for RETRIEVEENDSETS ends with `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()`. When `retrieverestricted` searches the querying document's POOM for Range A's I-addresses and finds nothing (no POOM entry exists anywhere, since all POOMs deleted it), it returns NULL and that I-span is **silently dropped** — no error, no partial result, just omission. [EC-LINK-PARTIAL-SURVIVAL] confirms: "the I-span for 'AA' becomes unresolvable. The link survives partially — it still points to the 'BB' content."

**Caveat on query document scope.** [SS-RETRIEVE-ENDSETS] Finding 0035 establishes that endsets are resolved in terms of the *querying document's* V-space. If the querying document doesn't contain Range B in its own POOM, Range B is also silently dropped — even though it exists in doc_X. You must query from (or via) a document that has Range B mapped. This is consistent with the general FOLLOWLINK behavior documented in [SS-FOLLOWLINK] Finding 0048: "FOLLOWLINK requires ... there is no precondition requiring that endset I-addresses be currently referenced in any POOM. The operation succeeds even when all endset I-addresses are unreferenced, returning an empty result rather than an error."

---

### Summary table

| Layer | Range A (deleted from all POOMs) | Range B (live in doc_X) |
|-------|----------------------------------|-------------------------|
| Spanfilade index | Entry persists permanently [INV-SPANF-WRITE-ONLY] | Entry persists permanently |
| `find_links` reachability | Unreachable (no V-specset maps to it) | Reachable from doc_X |
| `find_links` result | Not a viable search path | Discovers the link |
| RETRIEVEENDSETS result | Silently dropped [INV-ITOV-FILTERING] | Returned (if querying from doc with Range B) |

The link structure itself is unchanged throughout — only the observable portions of its endset vary depending on which POOM entries survive. [EC-LINK-PARTIAL-SURVIVAL], [INV-LINK-PERMANENCE], [INV-SPANF-WRITE-ONLY], [INV-ITOV-FILTERING].

---

## Code Exploration

Now I have everything I need. Let me trace the full execution paths with precise line citations.

---

## Answer

### Setup: How a link with two target I-ranges is stored

`docreatelink` [do1.c:195-221] calls `specset2sporglset` on the target specset [do1.c:215], which calls `vspanset2sporglset` [sporgl.c:35]. That function runs `vspanset2ispanset` [orglinks.c:397] → `permute` [orglinks.c:404] → `retrieverestricted` on the document POOM to find all contiguous I-address regions. Per [sporgl.c:47-58], **a separate `typesporgl` is created for each I-range**:

```c
// sporgl.c:47-58
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc(taskptr, sizeof(typesporgl));
        ...
        movetumbler(docisa, &sporglset->sporgladdress);
        movetumbler(&ispanset->stream, &sporglset->sporglorigin);
        movetumbler(&ispanset->width, &sporglset->sporglwidth);
```

These two sporgls are then indexed in the spanfilade by `insertendsetsinspanf` [do2.c:116-128] → `insertspanf` [spanf1.c:15-54], which calls `insertnd` once per sporgl [spanf1.c:51]:

```c
// spanf1.c:49-51
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);  // I-address
movetumbler(&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

Each spanfilade crum stores `(I-range → linkISA)` independently, under the `LINKTOSPAN` ORGLRANGE dimension.

---

### `find_links` — **discovers the link through the surviving range**

Call chain: `findlinksfromtothree` [fns.c:189] → `dofindlinksfromtothree` [do1.c:348-353] → `findlinksfromtothreesp` [spanf1.c:56].

In `findlinksfromtothreesp` [spanf1.c:70-102]:

```c
// spanf1.c:73-82
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
...
if (tovspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
    if (!tolinkset) {
        *linksetptr = NULL;
        return (TRUE);      // short-circuit: return empty if nothing found
    }
}
```

**Step 1 — specset → sporgls:** `specset2sporglset` [sporgl.c:14] → `vspanset2sporglset` [sporgl.c:35] → `vspanset2ispanset` [orglinks.c:397] → `permute` → `retrieverestricted` on the searched document's POOM. If the search targets V-positions in the **document that still contains the surviving I-range**, the POOM has crums for that range → those I-addresses are successfully extracted into sporgls.

**Step 2 — sporgls → link set:** `sporglset2linkset` [sporgl.c:222] → `sporglset2linksetinrange` [sporgl.c:239]:

```c
// sporgl.c:256-266
prefixtumbler(&orglrange->stream, spantype, &range.stream);
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, NULL);
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist(taskptr, linksetptr, &linksa);
}
```

The spanfilade is **write-only** — there is no `deletespanf` [confirmed spanf1.c, spanf2.c: no delete function exists, Finding 0057]. Both I-range entries persist. The surviving I-range's entry is found by `retrieverestricted` on the spanfilade (2D intersection: SPANRANGE = surviving I-addresses, ORGLRANGE = LINKTOSPAN prefix). The link's ISA is extracted via `beheadtumbler` [sporgl.c:264] and added to the result set.

**Conclusion for `find_links`:** The link is discovered through the surviving I-range. The deleted range cannot contribute to discovery via V-position searches (its POOM crums have been freed by `deletend` [edit.c:76-84, Finding 0064]), but the surviving range's spanfilade entry is intact and sufficient. `intersectlinksets` [spanf2.c:46] with only a `tolinkset` (no `fromlinkset`) passes it straight through [spanf2.c:64-71]:

```c
// spanf2.c:64-71  — single non-null linkset case
if (linkset1 && !linkset2 && !linkset3)
    *linkset4ptr = linkset1;
else if (!linkset1 && linkset2 && !linkset3)
    *linkset4ptr = linkset2;
```

---

### `RETRIEVEENDSETS` — **returns only the surviving portion**

Call chain: `retrieveendsets` [fns.c:350] → `doretrieveendsets` [do1.c:369-374] → `retrieveendsetsfromspanf` [spanf1.c:190].

**Step 1 — find all registered target sporgls:** `retrievesporglsetinrange` [spanf1.c:237-267] searches the spanfilade for crums in the `LINKTOSPAN` ORGLRANGE that overlap the link's own I-span (the search key):

```c
// spanf1.c:244-265
for (; sporglptr; sporglptr = ...) {
    context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                                  whichspace, ORGLRANGE, NULL);
    for (c = context; c;) {
        sporglset = taskalloc(taskptr, sizeof(typesporgl));
        contextintosporgl((type2dcontext*)c, NULL, sporglset, SPANRANGE);
        // sporglset->sporgladdress = context->context2dinfo.homedoc (content's home doc)
        // sporglset->sporglorigin  = I-address start
        // sporglset->sporglwidth   = I-address width
```

Because the spanfilade is write-only, **both** I-ranges appear here — the deleted one's crum was never removed.

**Step 2 — convert sporgls back to V-positions:** `linksporglset2specset` [sporgl.c:97] → `linksporglset2vspec` [sporgl.c:127] → `sporglset2vspanset` [sporgl.c:141] → `ispan2vspanset` [orglinks.c:389] → `permute` [orglinks.c:404] → `span2spanset` [orglinks.c:425]:

```c
// orglinks.c:434-448
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              NULL, targindex, NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
if (!context) {
    return(targspansetptr);   // ← adds NOTHING if no POOM context found
}
```

For the **deleted I-range**: `retrieverestricted` on the POOM finds no bottom crum (the crum was freed by `deletend` [edit.c:76-84]). It returns NULL. `span2spanset` returns `targspansetptr` unchanged — no V-span is added.

For the **surviving I-range**: `retrieverestricted` finds a live crum in the POOM. `context2span` extracts the V-position. `onitemlist` appends a `typevspan` to the result.

**Caveats on POOM selection:** There is an acknowledged kluge at [sporgl.c:134, 152] where the code uses `homedoc` (the link's home document) instead of `sporglptr->sporgladdress` (the content's original document) when converting I-addresses to V-positions. If the surviving content lives in a document other than the link's home document, and the link's home document no longer has the I-addresses in its POOM, the surviving V-span would still come back empty through that code path. In the common case where both endpoint ranges were in the link's home document, the surviving range is correctly returned.

---

### Summary

| Question | Answer | Key mechanism |
|----------|--------|---------------|
| Does `find_links` discover the link through the surviving range? | **Yes** | Surviving I-range → spanfilade entry persists (write-only); `sporglset2linksetinrange` [sporgl.c:239] finds it via `retrieverestricted` on spanf. |
| Does `RETRIEVEENDSETS` return both ranges or just the surviving portion? | **Just the surviving portion** | `retrievesporglsetinrange` [spanf1.c:237] retrieves both I-ranges from the write-only spanfilade, but `ispan2vspanset` [orglinks.c:389] → `retrieverestricted` on the POOM finds no crum for the deleted range (`deletend` freed it [edit.c:76-84]), so `span2spanset` [orglinks.c:446-448] adds nothing for it. Only the surviving range maps to a V-position. |

The key asymmetry is: **the spanfilade (link index) is write-only**, so discovery queries can still reach the link through any of its surviving indexed I-spans. But **V-position conversion goes through the POOM**, which has had the deleted I-range pruned out, so the endset view reflects only what is currently live.

---

## Question 19 [gregory]

> When `deletevspanpm` removes a link orgl's V→I entry from the POOM (reverse orphaning), does the link's discoverability through `find_links` depend solely on whether the endpoint content I-addresses still exist in some document's POOM, completely independent of the link orgl's own V-space presence?

### Gregory's Answer

## KB Synthesis

Yes. The link orgl's own V-space presence (its 2.x POOM entry in the home document) is **completely irrelevant** to `find_links` discoverability. The two mechanisms operate on entirely separate layers.

## How `find_links` actually works

`find_links` does not consult the link subspace (2.x) of any document's POOM at all. The search path is:

1. Query specset → I-addresses (via the **querying** document's POOM)
2. I-addresses → spanfilade lookup (maps content I-addresses to link ISAs)
3. Return matching link ISAs

[INT-SPORGL-LINK-INDEX] describes the indexing: at link creation, `insertendsetsinspanf()` writes endpoint content I-addresses into the spanfilade. The spanfilade entry is: `I-address range → (link ISA, endpoint type)`.

## Why the link orgl's V-space presence is irrelevant

[EC-REVERSE-ORPHAN] confirms this directly with an empirical test:

> After `DELETEVSPAN(2.1)` on a document:
> - `find_links(source_specs)` → still finds the link (spanfilade intact)
> - `follow_link(link_id, LINK_SOURCE)` → still works (link orgl intact)

[FC-LINK-DELETE-ISOLATION] Finding 0040 explains the mechanism:

> `DELETEVSPAN(2.x)` affects ONLY the POOM layer. It does not modify the link orgl in I-space, the DOCISPAN entries in the spanfilade, or the link's endset references.

[INV-SPANF-WRITE-ONLY] seals this: the spanfilade is append-only. No operation removes spanfilade entries. The endpoint I-address → link ISA mapping written at creation time persists unconditionally.

## What `find_links` discoverability actually depends on

Discoverability depends on exactly one thing: **whether the query specset's V-spans resolve to I-addresses that intersect with the link's indexed endpoint I-addresses**.

This means:

**The query document's POOM must contain the relevant I-addresses** — i.e., the query content must currently exist in some document's V-stream. If *all* documents have deleted the endpoint content, the query yields no I-addresses to intersect, and the link is undiscoverable via content search (the orphaned link state [EC-ORPHANED-LINK]).

But as long as *any* document's POOM still maps V-positions to the endpoint I-addresses, `find_links` will discover the link from that document — regardless of whether the link orgl itself appears anywhere in any POOM. This is confirmed by [INT-TRANSCLUSION-LINK-SEARCH]: a transcluded copy retaining the I-addresses continues to discover the link even after the original source document deletes its content.

## The three-layer summary

[SS-THREE-LAYER-MODEL] lays this out cleanly:

| Layer | Written by | Removed by | Role in `find_links` |
|-------|-----------|-----------|---------------------|
| I-space (link orgl) | CREATELINK | Nothing | Contains endset I-addresses |
| Spanfilade | CREATELINK | Nothing | **Index**: content I-addr → link ISA |
| POOM (2.x entry) | CREATELINK | DELETEVSPAN | Not consulted |

`find_links` operates entirely in layer 2 (spanfilade) via content I-addresses. The link orgl's POOM presence in layer 3 determines whether `retrieve_vspanset` shows the link and whether the home document visually "contains" the link — but it has zero effect on whether the link is findable.

---

## Code Exploration

Now I have everything I need to give a complete, code-grounded answer.

---

## Answer

**Yes — completely independent.** After `deletevspanpm` removes the link orgl's V→I entry from the host document's POOM, the link remains permanently discoverable through `find_links` because the two structures are entirely separate and deletion only touches one of them. Here is the full code trace.

---

### 1. What link creation writes — three distinct data structures

`docreatelink` [do1.c:195–221] writes to **three separate places**:

**A. Host document's POOM** (the V→I entry the question is about)

```c
// do1.c:211-212
&& findnextlinkvsa (taskptr, docisaptr, &linkvsa)
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)
```

`docopy` → `insertpm` → `insertnd(..., V)` places the link's I-address (`linkisa`) at V-position `linkvsa` inside the host document's POOM. This is the "V→I entry" that `deletevspanpm` removes.

**B. Link orgl's own POOM** (endpoints stored inside the link)

```c
// do1.c:217-218
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
```

`insertendsetsinorgl` [do2.c:128–146] calls `insertpm` twice, writing the endpoint I-spans into the **link orgl's own POOM** at V-addresses `fromvsa=(1,1)` and `tovsa=(2,1)`. This is what `dofollowlink` reads — but it is irrelevant to `find_links`.

**C. Global spanfilade** (the link index)

```c
// do1.c:219
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`insertendsetsinspanf` [do2.c:114–126] calls `insertspanf` [spanf1.c:15–54] for each endpoint set. This writes into the global `spanf` enfilade keyed by the endpoint I-spans (SPANRANGE axis) and the link ISA prefixed by endpoint type (ORGLRANGE axis):

```c
// spanf1.c:49-51
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

---

### 2. What `deletevspanpm` actually touches

```c
// orglinks.c:144-151
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend(..., V)` removes one dimension's worth of data from **one specific orgl's POOM** (the `docorgl` passed in — the host document). It does not touch:
- The global spanfilade (`spanf`)
- Any other orgl's POOM
- The link orgl's own POOM entries (structure B)

The caller `dodeletevspan` [do1.c:158–167] is equally bare:

```c
// do1.c:163-166
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
/*&& TRUE*/ /* ht stuff */ );
```

The comment `/* ht stuff */` [do1.c:166] is the explicit architectural marker: there was a planned (but unimplemented) continuation that would have cleaned up the hypertext/link data structures. That code never existed. The spanfilade entry for the link survives intact.

---

### 3. What `find_links` actually reads

`dofindlinksfromtothree` [do1.c:348–353] → `findlinksfromtothreesp` [spanf1.c:56–103]:

```c
// spanf1.c:70-100
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
...
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
...
sporglset2linkset (taskptr, (typecuc*)spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
...
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

The sole data structure consulted is the **global spanfilade** (`spanfptr` = global `spanf`). The host document's POOM is never opened; the link's own POOM is never opened.

`sporglset2linksetinrange` [sporgl.c:239–269] executes the actual spanfilade query:

```c
// sporgl.c:256-266
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE,
                              &range, ORGLRANGE, (typeisa*)infoptr);
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist (taskptr, linksetptr, &linksa);
}
```

This asks: "what link ISAs (ORGLRANGE) have endpoint content I-spans (SPANRANGE) that intersect the queried sporglset?" The result is a set of link ISAs extracted directly from spanfilade nodes. The POOM is not involved.

---

### 4. The one qualified dependency: V-spec queries

When the caller passes V-specs (not bare I-spans), `specset2sporglset` calls `vspanset2sporglset` [sporgl.c:35–65] which reads the **endpoint content document's POOM** to translate V-spans to I-spans:

```c
// sporgl.c:44-48
if (!findorgl (taskptr, granf, docisa, &orgl, type)) {
    return (NULL);
}
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
```

This is the POOM of the **queried content document** (e.g., docX whose text the link points to), not the POOM of the document that hosts the link. If that content document's POOM no longer maps the queried V-span to the expected I-spans, the V-spec query won't produce the I-span that hits the spanfilade entry — but the spanfilade entry itself is untouched.

---

### Summary

| Structure | Written by | Read by `find_links` | Affected by `deletevspanpm` on host doc |
|---|---|---|---|
| Host doc POOM (link's V→I) | `docopy` → `insertpm` | Never | **Yes — this is what is deleted** |
| Link orgl's own POOM (endpoint V→I) | `insertendsetsinorgl` → `insertpm` | Never (only `dofollowlink` uses this) | No |
| Global spanfilade | `insertendsetsinspanf` → `insertspanf` | **Always — sole source** | No |

The link's discoverability through `find_links` is determined entirely by the global spanfilade, which is keyed on the **endpoint content I-addresses**, not on the link orgl's V-space presence. `deletevspanpm` never touches the spanfilade (`/* ht stuff */` at do1.c:166 marks exactly where that cleanup was planned but never written). The link's discoverability is therefore completely independent of whether its V→I entry exists in any document's POOM.

---

## Question 20 [gregory]

> After a link becomes orphaned through content deletion and then re-discoverable through transclusion, is there any observable difference in the link's endset resolution compared to before orphaning — specifically, do the returned V-addresses reflect the new document's V-space rather than the original document's?

### Gregory's Answer

## KB Synthesis

Yes — there are observable and systematic differences. The resolution is not merely cosmetic.

---

## Core Mechanism: FOLLOWLINK Is Document-Relative

The link's endset stores I-addresses permanently [INV-IADDR-IMMUTABILITY]. What changes across the orphan/re-transclusion lifecycle is not the link itself, but which document's POOM is used to convert those I-addresses back to V-addresses.

From [SS-FOLLOWLINK] (Finding 0048):

> `followlink(link, whichend, homedoc) = { v | ∃ i ∈ endset(link, whichend) : poom.homedoc(v) = i }`

The `homedoc` parameter determines the V-space in which results are expressed. [INV-ITOV-FILTERING] enforces this universally: every I-to-V conversion silently drops I-addresses that have no POOM mapping in the queried document.

---

## The Three-State Lifecycle

**Before orphaning** — content at I-address α exists in Doc A at V-position v₁:
```
followlink(L, SOURCE, DocA) → {v₁}    # expressed in DocA's V-space
```

**After orphaning** — α removed from Doc A's POOM via DELETE:
```
followlink(L, SOURCE, DocA) → []       # no POOM mapping → silently filtered
```
This is the ghost link state [EC-GHOST-LINK]. The link orgl is intact [INV-LINK-PERMANENCE], but resolution against DocA returns empty.

**After re-transclusion** — DocB transcludes the content (COPY shares I-address α), placing it at V-position v₂:
```
followlink(L, SOURCE, DocB) → {v₂}    # expressed in DocB's V-space
followlink(L, SOURCE, DocA) → []       # still empty in DocA
```

[EC-GHOST-LINK] directly addresses this: "Reconstitution: COPY `a` into new document D2 → `poom.D2(1.1) = a` → FOLLOWLINK(L, TO, D2) → `[1.1]`" — the V-address `1.1` is in D2's coordinate system, not the original document's.

---

## Observable Differences

**1. The document reference in the returned SpecSet changes.**

[INT-LINK-VERSION] (Finding 0019) confirms: "The endset docid is rewritten to the queried document's address, even though the link was created against the original. This means endsets are relative to the query context, not absolute." The returned specset references DocB, not DocA.

**2. The V-positions are in the new document's coordinate system.**

The transcluded content in DocB may sit at an entirely different V-position than it occupied in DocA. V-address v₂ ≠ v₁ in general. [SS-FOLLOWLINK] is explicit: "The same link endset can produce different V-address results (or empty results) depending on which document context is used."

**3. RETRIEVE-ENDSETS similarly reflects the querying document's V-space.**

From [SS-RETRIEVE-ENDSETS] (Finding 0035): "endsets are resolved in terms of the querying document's V-space, not the link's home document." The sporgl mechanism [SS-SPORGL] carries the `source_doc` field — after transclusion, the sporgl produced from DocB has `source_doc = DocB` and encodes DocB's V-positions.

---

## What Does NOT Change

The link object itself is invariant [INV-LINK-PERMANENCE]. Its stored I-addresses are immutable [INV-IADDR-IMMUTABILITY]. The link's discoverability via `find_links` is restored through content-identity intersection [SS-FIND-LINKS] — as soon as DocB's POOM maps any V-position to α, the link becomes findable again from DocB.

The `follow_link` client operation (as described in [SS-FOLLOW-LINK], Finding 0028b) is documented as returning "the original SpecSet" — but that observation was made in the context where the original document was still live. The lower-level FOLLOWLINK opcode (Finding 0048) makes explicit that the result is parameterized by `homedoc`. After content deletion from DocA, the "original" SpecSet is effectively unreachable from DocA; DocB's context is the only one that yields non-empty results, and in that context the V-addresses are DocB's.

---

## Summary

| State | `followlink(L, S, DocA)` | `followlink(L, S, DocB)` |
|---|---|---|
| Before orphaning | `{v₁}` in DocA's V-space | `[]` (no POOM mapping) |
| After orphaning | `[]` | `[]` |
| After transclusion to DocB | `[]` | `{v₂}` in **DocB's V-space** |

The V-address v₂ is expressed in DocB's coordinate system, has no guaranteed numerical relationship to v₁, and the returned SpecSet docid is DocB — not DocA. This is the expected behavior given the I-address-based resolution mechanism [SS-FOLLOWLINK], not an anomaly.

---

## Code Exploration

I now have everything needed. Here is the complete answer.

---

## Answer: Link Endset Resolution After Orphaning and Re-Transclusion

The short answer: **No — the returned V-addresses do not reflect the new document's V-space.** After orphaning and re-transclusion, `followlink` returns the original source document's ISA with an empty vspanset. The new document is structurally invisible to the endset resolution path.

Here is the full trace.

---

### Phase 1 — What the Link Stores at Creation Time

`docreatelink` [`do1.c:195–221`] converts the caller's from/to specsets into **sporgls** before storing them:

```c
specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
```

`vspanset2sporglset` [`sporgl.c:35–65`] does the V→I conversion and packages three fields per sporgl:

```c
sporglset->sporgladdress = docisa;             // Source document ISA — locked in forever
sporglset->sporglorigin  = ispanset->stream;   // I-address
sporglset->sporglwidth   = ispanset->width;
```

Those sporgls are then inserted into the **link's own POOM** (via `insertpm` [`orglinks.c:75–134`]) at V-positions 0.1 (from), 0.2 (to), 0.3 (three) — set by `setlinkvsas` [`do2.c:169–183`]. The `linfo.homedoc` field in each POOM crum is written from `sporgladdress`, so the source document ISA is physically embedded in the crum tree.

The same sporgls are also written to the global spanfilade (`insertendsetsinspanf` [`do2.c:116–128`]), which is the index that makes links *discoverable* by content.

**Key invariant established here:** The link's POOM permanently records `(I-address, source_doc_ISA)` for each endset. This pairing is never updated.

---

### Phase 2 — Content Deletion (Orphaning)

`dodeletevspan` [`do1.c:158–167`] calls `deletevspanpm` [`orglinks.c:145–152`]:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

`deletend` [`edit.c:31–60`] calls `makecutsnd` + `deletecutsectionnd` to surgically remove V→I entries from the source document's POOM. The I-addresses in granf are untouched (content is permanent in the permascroll). The spanfilade entries for the link's endsets are not touched either — no `deletespanf` function exists [`spanf1.c`, confirmed in Finding 0057].

After deletion:
- Source doc's POOM: no longer maps those I-addresses to any V-position  
- Link's POOM: unchanged — `(I-addr, source_doc_ISA)` still there  
- Spanfilade: unchanged — still indexes the link's endsets under those I-addresses  

---

### Phase 3 — Re-Transclusion into a New Document

`docopy` [`do1.c:45–65`] into `new_doc`:

```c
insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)      // V→I into new_doc's POOM
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // Register new_doc in spanfilade
```

Now `new_doc`'s POOM maps **new V-addresses → same I-addresses**. The link's POOM is still untouched.

---

### Phase 4 — Following the Link

`dofollowlink` [`do1.c:223–232`]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  return (
     link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
  && linksporglset2specset(taskptr,
        &((typesporgl *)sporglset)->sporgladdress,   // <-- homedoc = stored source_doc_ISA
        sporglset, specsetptr, NOBERTREQUIRED));
}
```

**Step A — `link2sporglset`** [`sporgl.c:67–95`]: Opens the link's POOM, queries at V = `0.whichend`. `contextintosporgl` packages the results, extracting `sporgladdress` from `context->context2dinfo.homedoc` — the value stored at crum creation time:

```c
movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
```

Result: sporgls with `sporgladdress = source_doc_ISA` (original document, not `new_doc`).

**Step B — `linksporglset2specset`** [`sporgl.c:97–123`]: Called with `homedoc = sporgl->sporgladdress = source_doc_ISA`. Since `sporgladdress` is non-zero, branches to `linksporglset2vspec`:

```c
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc,
                        typesporglset *sporglsetptr, typevspec *specptr, int type)
{
  specptr->itemid = VSPECID;
  specptr->next   = NULL;
  movetumbler(homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);  // ← source_doc_ISA
  specptr->vspanset = NULL;
  sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```

The commented-out alternative `/*&sporglset->sporgladdress*/` reveals the original intent — but even under either reading, `homedoc` is the *original source document ISA* in the `dofollowlink` path.

The returned vspec's `docisa` is permanently set to `source_doc_ISA`.

**Step C — `sporglset2vspanset`** [`sporgl.c:141–176`]:

```c
(void) findorgl(taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl, type);
// ...
vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
```

This opens `source_doc`'s POOM and calls `ispan2vspanset` → `permute` → `span2spanset` → `retrieverestricted` on `source_doc`'s POOM tree with the stored I-addresses. Since `deletend` already removed those I-addresses from `source_doc`'s V→I mapping, `retrieverestricted` returns `NULL`. In `span2spanset` [`orglinks.c:425–454`]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, ...);
// context == NULL: nothing contributed to vspanset
if(!context){
    return(targspansetptr);   // returns without modification
}
```

`vspanset = NULL` (empty).

**`new_doc`'s POOM is never consulted** — it is not even referenced in this path. There is no fallback or search across all POOMs.

---

### The Observable Difference

| State | `followlink` result |
|---|---|
| Before orphaning | `{docisa: source_doc_ISA, vspanset: [V₁..Vₙ in source_doc]}` |
| After orphaning (content deleted) | `{docisa: source_doc_ISA, vspanset: []}` |
| After re-transclusion into `new_doc` | `{docisa: source_doc_ISA, vspanset: []}` — **unchanged** |

The returned `docisa` is **always** the original source document ISA stored in the sporgl at link creation time [`sporgl.c:134`]. The V-addresses are **always** computed using that document's POOM [`sporgl.c:152`]. After orphaning, the I→V lookup in the original document silently returns empty because `deletend` removed those V-space entries. After re-transclusion, `new_doc`'s POOM is never queried.

---

### Why the New Document's V-Space Is Never Returned

There is **no mechanism in the code** to remap a link's stored `sporgladdress` to another document:

1. `sporgladdress` is set once in `vspanset2sporglset` at link creation [`sporgl.c:53`] and physically embedded in the link's POOM crum as `linfo.homedoc` [`orglinks.c:105`].
2. `link2sporglset` reads it back via `context->context2dinfo.homedoc` [`sporgl.c:86`] — no rewriting.
3. `dofollowlink` passes `sporgl->sporgladdress` directly as `homedoc` [`do1.c:230`] — no fallback to other documents.
4. `sporglset2vspanset` uses `homedoc` to find exactly one orgl [`sporgl.c:152`] — no cross-document search.

---

### Re-Discoverability vs. Resolution — The Asymmetry

The question's scenario is correct that the link becomes *discoverable* again after transclusion. `findlinksfromtothree` converts `new_doc`'s V-addresses to sporgls `(I-addr, new_doc_ISA)`, queries the spanfilade with those I-addresses, and finds the link (whose endsets' I-addresses were indexed at creation time, and those spanfilade entries were never removed [`spanf1.c`, Finding 0057]).

But *discoverability* through the spanfilade and *endset resolution* through `dofollowlink` are entirely separate paths:

```
FIND path:  new_doc VSpec → I-addresses → spanfilade → link_ISA    (finds the link)
FOLLOW path: link_ISA → link POOM → sporgls(source_doc_ISA, I-addr)
                                  → source_doc POOM → V-addresses   (empty after deletion)
```

Finding the link via `new_doc`'s transcluded content does not update or redirect the link's internally stored `sporgladdress`. The follow operation still bottoms out at the original document, which returns empty.

**There is a definitive observable difference**: after orphaning (with or without re-transclusion), `followlink` returns `{docisa: source_doc_ISA, vspanset: []}`. The new document's V-space is structurally unreachable through this path. The V-addresses returned reflect the original document's V-space — and because the content was deleted from that document, they are absent.
