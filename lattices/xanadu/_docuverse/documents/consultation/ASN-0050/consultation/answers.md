# Consultation Answers — DELETE Operation

**Inquiry:** What happens when content is removed from a document's arrangement? What disappears, what survives, and what must the system preserve about content that is no longer visible?
**Date:** 2026-03-18 14:07
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When content is removed from a document's arrangement, does the content itself continue to exist permanently in the system, or can removal ever cause content to cease to exist?

### Nelson's Answer

# Content Removal Never Destroys Content

The answer is unambiguous: **removal from a document's arrangement never causes content to cease to exist.** This is one of Xanadu's deepest architectural commitments.

## The Two Address Spaces

Xanadu separates *where content lives permanently* (I-space) from *how a document arranges content right now* (V-space). DELETE operates exclusively on V-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "not currently addressable" is precise — the bytes are not gone, they are merely unreachable through the current document arrangement.

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This confirms that deletion is local to one V-space arrangement. Every other document that transcludes the same I-space content is unaffected.

## Append-Only Storage

The storage model is explicitly append-only. Content accumulates; it is never overwritten or removed:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte ever stored has a permanent I-space address that will always return that exact content. This is not a backup mechanism bolted on after the fact — it is the fundamental nature of how storage works.

## Historical Backtrack Depends On It

The guarantee that you can reconstruct any previous state requires that nothing is ever truly destroyed:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If removal could destroy content, historical backtrack would be impossible. The two guarantees are structurally linked.

## Modifications Never Damage Originals

Nelson states this as a general principle applying to all editing operations:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And on derivative documents:

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

## What Deletion Affects vs. What It Does Not

| Aspect | Affected by DELETE? |
|--------|---------------------|
| V-space arrangement (current view) | **YES** — content removed from current arrangement |
| I-space content (permanent storage) | **NO** — bytes remain forever |
| Previous versions | **NO** — still contain the content |
| Transclusions in other documents | **NO** — still show the content |
| Links pointing to that content | **NO** — still resolve via I-space |
| Home document traceability | **NO** — I-address still encodes origin |

## Summary

In Xanadu, "delete" means "remove from this arrangement." It never means "destroy." The content persists in I-space, remains accessible through previous versions, continues to appear in any document that transcludes it, and can always be recovered through historical backtrack. This is by design — Nelson built the system specifically to abolish destructive replacement.

---

## Question 2 [nelson]

> If a span of content is removed from one document but that same content is shared by other documents through transclusion, must those other documents remain completely unaffected by the removal?

### Nelson's Answer

## Yes — absolutely and by explicit design.

Nelson states this directly at **4/11**:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."

This is a necessary consequence of the I-space / V-space separation.

### Why architecturally

DELETE operates **only on V-space** — it removes content from a document's current arrangement. It does **not** touch I-space, where the bytes permanently reside.

When document B transcludes content from document A, document B's V-space maps directly to the **I-space addresses** of those bytes — not to document A's V-space positions. So when document A's owner deletes those bytes from A's current version:

- A's V-space mapping is removed (the bytes disappear from A's current view)
- The I-space content is untouched
- B's V-space mapping still points to those same I-space addresses
- B is completely unaffected

Nelson's diagram annotation at **4/9** confirms the state of deleted content:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

"May remain included in other versions" — and by extension, in other documents that transclude the same I-space content.

### The deeper principle

This follows from Nelson's rejection of destructive storage:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals." [LM 2/45]

The non-destruction guarantee means that no editing operation in one document can damage content visible through another document. DELETE changes **your view**, not the underlying reality.

### One nuance: window modes

Nelson describes two transclusion modes [LM 2/37]:

> "A quotation—an inclusion window—may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically."

A **location-fixed window** that tracks the current V-space of the source document could reflect the deletion — the window would show the source document's updated arrangement. But this is about what the *window shows of the source's view*, not about destruction of the underlying content. The I-space bytes still exist, previous versions still contain them, and any direct transclusion (COPY operation) remains intact.

### Summary

| What happens when A deletes content | Effect on document B (which transcludes it) |
|--------------------------------------|---------------------------------------------|
| A's V-space mapping removed | B's V-space mapping unchanged |
| I-space bytes untouched | B still resolves to same I-space content |
| A's previous versions still show it | B shows it as before |
| Links to those I-space bytes survive | B's attribution to source intact |

The answer is unambiguous from Nelson's text: transclusion in other documents **must** remain completely unaffected by removal from the source document's current version.

---

## Question 3 [nelson]

> Must every prior version of a document — including versions that contained the now-removed content — remain permanently retrievable?

### Nelson's Answer

# Yes — Every Prior Version Must Remain Permanently Retrievable

This is one of Xanadu's firmest guarantees, established through multiple interlocking design commitments.

## The Direct Statement

Nelson states the guarantee explicitly:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

The user can request **any part** of **any version** at **any point in time**, and the system must deliver it.

## Why This Is Architecturally Inevitable

The guarantee is not a policy choice bolted onto the system — it falls out structurally from the I-space/V-space separation.

**I-space is append-only.** Content, once stored, lives at its I-address forever:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**A version IS a V-space arrangement.** Each version is nothing more than a mapping from V-addresses to I-addresses. Since I-space content is permanent, any prior mapping can be reconstructed. There is no way to make a version "unretrievable" without destroying I-space content — which the architecture forbids.

**Deletion is V-space only.** When content is removed from a document, it disappears from the current arrangement but remains in I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The phrase "awaiting historical backtrack functions" is telling — the deleted bytes are preserved *specifically so that* prior versions containing them can be reconstructed.

## The Published-Version Obligation

For published documents, the requirement is even stronger. Prior versions must remain not merely reconstructible but actively available, because other users' links depend on them:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

The logic chain: others link to version N → you publish version N+1 → version N **must remain** → because links to it are other users' property and cannot be broken by your editorial decisions.

## No "Basic" Version

Nelson explicitly rejects the idea that any version is privileged over others:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

All versions have equal standing. The current version is simply the most recent V-space arrangement; it does not supersede prior versions in terms of existence or retrievability.

## The Braid Metaphor

Nelson's central metaphor reinforces this:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

A braid does not destroy its earlier strands when new ones are added. The entire history is structural — you can examine any cross-section at any point in time.

## One Qualification: Implementation Status

Nelson acknowledges that XU.87.1 did not fully implement historical backtrack:

> "Being able to go back through changes, and perhaps restore an earlier state, is called the problem of historical backtrack. For simple, linear textual documents this can be done by storing lists of changes and undoing them; and indeed several commercial versioning and backtrack systems are now on the market. But it is rather more difficult to do this for hypertext." [LM 3/13]

The 4/9 annotation — "awaiting historical backtrack functions" — confirms that full version reconstruction was designed-for but not yet built in 87.1. The *architecture* preserves everything needed (append-only I-space, V-space mappings); the *implementation* of reconstruction was still in progress.

## Summary

Every prior version must remain permanently retrievable. This follows from:

1. **Append-only I-space** — content is never destroyed [LM 2/14]
2. **Versions are V-space arrangements** — reconstructible from permanent I-space [LM 4/10-4/11]
3. **Deletion is V-space only** — deleted bytes await historical backtrack [LM 4/9]
4. **Published versions cannot be withdrawn** — others' links depend on them [LM 2/43]
5. **No version is privileged** — all arrangements have equal standing [LM 2/19]
6. **The user guarantee is explicit** — "a given part of a given version at a given time" [LM 2/15]

---

## Question 4 [nelson]

> When content is removed from a document, what must happen to links whose endpoints fall within the removed content?

### Nelson's Answer

## Link Behavior When Content Is Removed

The answer has two layers: what happens to the *link itself*, and what happens to the *bytes it points to*.

### 1. The Bytes Are Never Destroyed

DELETE in Xanadu removes content from V-space (the document's current arrangement) but **not** from I-space (permanent storage):

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes still exist at their permanent I-addresses. They are merely absent from the document's current V-stream.

### 2. Links Point to I-Space, Not V-Space

Links attach to bytes by their permanent identity (I-address), not by their current position (V-address):

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

Since deletion removes content from V-space but leaves I-space intact, **links whose endpoints fall within removed content still have valid targets**. The I-space bytes are still there; the link's endset still resolves.

### 3. The Survivability Condition

The explicit survivability rule from page 4/43:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"

In Xanadu's architecture, this condition is *always* met after a DELETE, because DELETE never removes I-space content. The bytes the link points to still exist — they are simply no longer part of the document's current view.

### 4. Where the Linked Content Can Still Be Found

After deletion, the bytes referenced by a link's endset remain accessible through:

- **Previous versions** of the document (historical backtrack)
- **Other documents** that transclude the same I-space content
- **The I-space itself** — the permanent home location

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

### 5. What the Front End Must Handle

Nelson envisions that links made to older versions "reach through" into newer versions:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

> "When a document is updated, a reader will ordinarily want to see the new version — but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version — if it's still there." [LM 2/43]

The front end detects that the linked content no longer appears in the current version and can:
- Show the content from the version where it last appeared
- Navigate to the I-space origin directly
- Indicate to the user that the passage was removed from the current version

### Summary

**Nothing must "happen" to links when content is removed.** This is by design. Links are straps between bytes identified by permanent I-addresses. DELETE only changes V-space arrangement. The linked bytes persist in I-space, in previous versions, and in any documents that transclude them. The link's endsets remain valid. The front end handles presentation — showing the user where the content can still be found — but the link itself is architecturally unaffected.

---

## Question 5 [nelson]

> Must the system preserve the fact that specific content was once part of a document's arrangement at a particular version, even after removal?

### Nelson's Answer

## Yes — Unambiguously

Nelson requires that the system preserve the complete arrangement history of every version. This is not optional; it is the core of what he calls **historical backtrack**.

### The Direct Evidence

The strongest statement comes from the DELETE semantics diagram on page 4/9:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Content removed from a document's current V-space arrangement enters a specific state: **not currently addressable, but preserved and awaiting recall**. The phrase "awaiting historical backtrack functions" means the system must retain enough information to reconstruct the arrangement that included those bytes.

Nelson makes the reconstruction guarantee explicit:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

This is a **three-dimensional request** — part, version, and time — and it requires the system to know what content belonged to which arrangement at which point. If the system discarded the fact of prior membership, it could not fulfill this guarantee.

### Why Preserving Content Alone Is Insufficient

I-space permanence guarantees the bytes survive forever. But that only answers "does this content exist?" It does not answer "was this content part of document D at version V?" — which is what historical backtrack requires.

The V-space arrangement is the document. Two documents can reference entirely different I-space content but present the same text. What makes a version *that version* is its specific V→I mapping. Nelson's system must preserve these mappings, not just the I-space content they point to.

This is confirmed by the version comparison operation:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70, on SHOWRELATIONOF2VERSIONS]

To return corresponding span pairs between two versions, the system must know the full V-space composition of both — including content that may have been removed from one but not the other.

### The Append-Only Foundation

Nelson's storage model makes this architecturally inevitable:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." [LM 2/15]

The append-only model means V-space mappings accumulate — they are never overwritten. Each version's arrangement is a permanent record. The "historical trace enfilade" [LM 1/36] exists specifically to support this: reconstructing any prior arrangement from the accumulated changes.

### The Ownership Dimension

Nelson adds a cross-document constraint:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This means deletion is purely local to the V-space of the document being edited. Other documents that transclude the same I-space content are unaffected. But even within the originating document, the prior version's arrangement — which included those bytes — must remain reconstructable.

### The Braid Metaphor

Nelson's metaphor captures the design intent precisely:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

A braid does not lose its earlier twists when new ones are added. The prior shape remains visible in the structure. This is the point: the system preserves not just content but the **history of arrangement**.

### Summary

The system must preserve three things:

1. **The content itself** — I-space permanence (bytes never deleted)
2. **The fact of membership** — which content belonged to which version's V-space arrangement
3. **The ordering** — the V-space positions within each version

Without all three, the fundamental guarantee — "when you ask for a given part of a given version at a given time, it comes to your screen" — cannot be met.

---

## Question 6 [nelson]

> Does removing content from a document's arrangement cause the remaining content to close the gap and form a new contiguous sequence, or must the system preserve the position where content once appeared?

### Nelson's Answer

## The Gap Closes: V-Space Is Always Contiguous

The remaining content closes the gap. This is fundamental to how V-space works.

### Direct Evidence

The V-space design intent states explicitly that V-addresses are **dense** — they "always form a contiguous sequence starting at 1." There are no holes in a virtual byte stream.

Nelson's description of INSERT confirms the mechanism:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

INSERT shifts subsequent addresses **up** by the insertion length. By the same logic, DELETEVSPAN shifts subsequent addresses **down**, closing the gap. The virtual byte stream remains contiguous after both operations.

### Why This Must Be So

V-space is defined as a **virtual byte stream** — a logical sequence:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

A "sequence of bytes" with holes in it is not a sequence. The V-stream is the document as the user sees it right now — position 1 is the first byte, position N is the last, and everything in between is occupied.

### V-Addresses Are Ephemeral by Design

Nelson is explicit that V-addresses change constantly and nobody should care:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

And:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

This is the key architectural insight: **links point to I-space, not V-space**. V-addresses can shift freely because nothing depends on their stability. Links attach to bytes (I-addresses), not positions (V-addresses). So when DELETE closes the gap and shifts every subsequent V-address, no links break — they were never pointing at V-addresses in the first place.

### The Two-Space Separation Makes This Work

The whole point of the I-space/V-space separation is that:

- **I-space is permanent**: content lives there forever, addresses never change
- **V-space is ephemeral**: the current arrangement, freely rearrangeable

DELETE removes bytes from V-space (the current view) while leaving them intact in I-space (permanent storage). The V-stream contracts; the I-stream is untouched. Previous versions still have their own V-arrangements that include the "deleted" content. Other documents that transclude the content still show it.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" means not in the current V-stream — but still present in I-space, recoverable through historical backtrack, and visible in other documents.

### Summary

DELETE causes the V-stream to close the gap. Position preservation would contradict the definition of V-space as a contiguous byte stream. The system can afford this because nothing of value depends on V-address stability — links, transclusions, and version correspondence all operate through I-space addresses, which are permanent and unaffected by V-space rearrangement.

---

## Question 7 [nelson]

> Can the owner of a document remove content that was originally created by a different author, and if so, does the original author's identity remain attached to that content elsewhere in the system?

### Nelson's Answer

## Yes — and the original author's identity is permanently preserved

### The owner can remove transcluded content from their document

The document owner has absolute editorial control over their V-space arrangement. Since transclusion places another author's content into the owner's V-stream, the owner can DELETE that content — meaning remove it from their document's current view.

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

DELETE is a V-space operation. It changes the document's arrangement, not the underlying content:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And critically:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### The original author's identity is structurally permanent

This is where Xanadu's I-space/V-space separation does its deepest work. The original author's identity is encoded in the **I-address itself** — it is not metadata that can be stripped but part of the address structure:

```
Node.0.User.0.Document.0.Element
```

The **User** and **Document** fields permanently record who created the content and in which document. This address never changes regardless of what any other document owner does with their V-space.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

### What survives the deletion

When document owner Alice removes Bob's transcluded content from her document:

| Aspect | Affected? |
|--------|-----------|
| Alice's current V-stream | Yes — content no longer appears |
| Bob's original document | No — completely untouched |
| I-space content | No — bytes remain at Bob's permanent I-address |
| Previous versions of Alice's document | No — still contain the transclusion |
| Other documents transcluding the same content | No — still show it |
| Links pointing to Bob's I-address | No — still resolve |
| Bob's royalty entitlement | No — any future delivery of those bytes still pays Bob |

### The deeper principle

Nelson designed the system so that **no editorial operation by anyone can sever attribution**. Because transclusion is inclusion by reference (not copy), and because I-addresses encode origin permanently, the connection between content and creator is an invariant of the system — not a convention that participants must honor but a structural property that cannot be violated from within the architecture.

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

The content lives at Bob's I-address forever. Alice's deletion merely says "I no longer wish to show this in my arrangement." It says nothing about Bob's content, Bob's identity, or anyone else's use of that content.

---

## Question 8 [nelson]

> Must a removal operation produce a new version of the document, or can a document's history ever lose record of what it previously contained?

### Nelson's Answer

## Answer

**No, a removal operation need not produce a formal new version via CREATENEWVERSION. But a document's history can never lose record of what it previously contained. This is architecturally impossible.**

These are two distinct guarantees that operate at different levels.

---

### DELETE Does Not Require CREATENEWVERSION

In the FEBE protocol, DELETEVSPAN and CREATENEWVERSION are separate operations. DELETEVSPAN modifies the current document's V-stream directly:

> "This removes the given span from the given document." [LM 4/66]

There is no specification that DELETE must first fork a version. It operates on the document in place — but "in place" means something radically different in Xanadu than in conventional systems, because the storage model is append-only.

---

### History Can Never Be Lost

This is guaranteed by three interlocking mechanisms:

**1. I-space permanence.** DELETE only removes content from V-space (the current arrangement). The bytes themselves remain permanently in I-space:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

**2. The DELETED BYTES state.** Nelson's diagram on page 4/9 explicitly shows "DELETED BYTES" as a valid system state with the annotation:

> "(not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "awaiting historical backtrack functions" is critical — deleted content is not gone, it is *waiting to be asked for*.

**3. Append-only storage.** The entire storage paradigm rejects destructive replacement:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

Every change — including every deletion — is recorded. Every previous instant is reconstructible.

---

### The Historical Trace Records All Changes

While DELETE does not create a formal version, the historical trace enfilade captures every modification. Nelson describes the document as:

> "an evolving ONGOING BRAID" [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

The user can then:

> "go back in time to any previous version. The user must also be able to find his or her notes, look back through time, and study its previous states." [LM 2/15]

This is not optional or best-effort. It is the fundamental storage paradigm:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

---

### Summary

| Question | Answer |
|----------|--------|
| Must DELETE produce a new version? | No — it is a separate FEBE operation from CREATENEWVERSION |
| Does the historical trace record the deletion? | Yes — append-only storage records every change |
| Can deleted content be recovered? | Yes — bytes remain in I-space, "awaiting historical backtrack" |
| Can a document's history lose record? | **Never** — this is architecturally impossible in append-only storage |

The deepest principle here is Nelson's rejection of "destructive replacement" [LM 2/14]. In conventional systems, deletion destroys. In Xanadu, deletion *rearranges the view*. The content endures. The history endures. Nothing is ever truly lost.

---

## Question 9 [nelson]

> If content is removed from a document and later the same content is re-inserted, must the system recognize it as the same content returning rather than treating it as new content?

### Nelson's Answer

## No — INSERT Creates New Content; COPY Restores the Same Content

The architecture answers this unambiguously through the I-space/V-space separation.

### DELETE Does Not Destroy Content

When content is deleted, it is removed from V-space (the document's current arrangement) but **remains permanently in I-space**:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The content never "left." It is still at its original I-address, still accessible through old versions, still present in any document that transcludes it.

### INSERT Always Creates New Content

The INSERT operation appends fresh bytes to I-space:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

New bytes get new I-addresses. Even if the character sequence is identical to what was deleted, **content identity is based on creation, not value**:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."

So if you delete "hello world" and then type "hello world" again via INSERT, the system treats the re-typed text as entirely new content — different I-addresses, different origin, no structural relationship to the deleted bytes.

### COPY Is How You Restore the Same Content

The COPY operation is the mechanism for preserving identity:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This is transclusion — the copy shares I-addresses with the source. To restore deleted content *as the same content*, you would COPY from the still-existing I-space bytes (reachable through a previous version or another document that includes them), not INSERT new text that happens to match.

### Why This Matters

The distinction has real consequences:

| Scenario | I-Addresses | Links to original | Royalties | Correspondence |
|----------|-------------|-------------------|-----------|----------------|
| DELETE then INSERT same text | New addresses | Do NOT attach to new text | Flow to new I-address owner | Not recognized as same |
| DELETE then COPY from old version | Original addresses | Still resolve | Flow to original creator | Recognized as same |

Links that pointed to the original content survive deletion (they point to I-space), but they will NOT automatically attach to re-inserted text that merely has the same character values. They WILL resolve if the content is restored via COPY, because COPY preserves I-space identity.

### The Deeper Point

The system doesn't need a mechanism to "recognize returning content" because **content never leaves I-space**. The append-only storage model means:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Delete is a V-space operation. Restoration is also a V-space operation — re-mapping the document's virtual byte stream to point back at the still-existing I-space content. The correct tool for this is COPY (or version restoration), not INSERT.

---

## Question 10 [nelson]

> When content is removed from a document, must the system preserve enough information for any holder of a link to the removed content to discover both that the content once appeared in that document and where the content still resides?

### Nelson's Answer

## Yes — and this falls out structurally from multiple interlocking guarantees

Nelson does not state this as a single explicit guarantee, but the system's architecture makes it unavoidable. Three mechanisms combine to ensure that a link holder can always discover both that content once appeared in a document and where it still resides.

### 1. The content is never destroyed

DELETE in Xanadu removes content from V-space (the document's current arrangement) but never from I-space (permanent storage). Nelson's diagram on page 4/9 shows "DELETED BYTES" as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Since I-space is append-only, the bytes a link points to **always exist**. The link never loses its target.

### 2. The link itself always survives

Links attach to I-space bytes, not V-space positions. A link doesn't care whether the bytes currently appear in any document's V-stream — it cares only that the bytes exist in I-space:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Since DELETE never removes I-space bytes, "anything is left at each end" is always true after a V-space deletion. The link survives unconditionally.

### 3. The I-address encodes where the content resides

Every byte's permanent I-address has the form `Node.0.User.0.Document.0.Element` [LM 4/26]. The Document field directly encodes which document originally created that byte. A link holder can inspect the I-address of the bytes their link points to and immediately determine the home document.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is structural, not metadata:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

### 4. Historical backtrack reveals past presence

Previous versions of the document still contain the deleted content in their V-streams. The system preserves the complete version history:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

So a link holder can reconstruct that the content *was* in document D by examining D's version history.

### 5. FINDDOCSCONTAINING locates current appearances

The FEBE operation FINDDOCSCONTAINING lets you find all documents that currently include specific content:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

A link holder can use their link's I-space target to query for every document that currently transcludes that content — discovering not just the home document but everywhere the content appears *right now*.

### Two cases worth distinguishing

**Native content** (bytes created in document D, then deleted from D's V-stream): The I-address encodes D as home. The bytes are still physically stored under D's control. Previous versions of D show the content. The link resolves directly to D's I-space.

**Transcluded content** (bytes from document E, included in D, then removed from D's V-stream): The I-address encodes E as home. The content still exists at E. Previous versions of D show the transclusion. FINDDOCSCONTAINING finds E and any other documents still transcluding it.

### Summary

The answer is **yes**, and it is not a separate guarantee but an emergent consequence of three structural properties: I-space permanence (content is never destroyed), I-address encoding (origin is always readable from the address), and historical backtrack (all previous arrangements are reconstructible). A link holder's link always resolves, always reveals the content's home document, and can always be used to find every document that currently contains that content.

---

## Question 11 [gregory]

> When `deletend` removes a POOM entry entirely within the deleted span, does `subtreefree` reclaim only the enfilade tree nodes (crums), or does it also touch the granfilade content those crums pointed to via I-address?

### Gregory's Answer

## KB Synthesis

`subtreefree` reclaims only the POOM enfilade tree nodes (in-memory crum structs). It does not touch the granfilade content those crums referenced via I-address.

The KB is explicit on this at multiple levels:

**POOM nodes are freed; granfilade is untouched**

[ST-DELETE] Finding 0064 states directly:

> DELETE operates exclusively on the POOM enfilade — it removes V-to-I mappings by pruning bottom crums (height-0 nodes) via `disown` + `subtreefree`. The I-addresses themselves continue to exist in the granfilade (which is append-only) and in the spanfilade (which has no delete operation).

The code reference confirms: `backend/credel.c:413-436` — `subtreefree`: recursive memory deallocation. This is deallocation of the in-memory `typecorecrum` structs managed by the grim reaper cache [SS-CACHE-MECHANISM], not any granfilade operation.

**The granfilade is append-only; DELETE cannot modify it**

[FC-GRANF-ON-DELETE] Finding 0061 establishes the frame condition:

> DELETE and REARRANGE are frame-condition-preserving with respect to the granfilade. These operations modify only the spanfilade (V-to-I mappings) and leave the granfilade (I-space content storage) completely unchanged.

[INV-IADDR-IMMUTABILITY] reinforces this:

> DELETE frees the POOM bottom crums that *reference* I-addresses, but the I-addresses themselves persist in the granfilade unconditionally.

**What `deletend` Case 1 actually does**

[ST-DELETE] Finding 0072 describes the mechanism: nodes within the deletion range are `disown`ed (removed from parent/sibling pointer chains) and then `subtreefree`d (recursively freed from the in-memory cache). This is purely structural surgery on the POOM tree topology. The I-addresses stored in those crums are just tumbler values — freeing the crum struct that held them has no effect on the granfilade entries at those addresses.

**Consequence: permanent I-space residue**

The granfilade content remains at its I-addresses after DELETE. This is what makes [INV-NO-IADDR-REUSE] hold — the next allocation via `findpreviousisagr` will find those I-addresses still present and allocate above them, never reusing them. It is also why [EC-STALE-SPANF-REFERENCE] occurs: the spanfilade's DOCISPAN entries (pointing to a document that no longer maps those I-addresses in its POOM) persist because neither `subtreefree` nor `deletend` touches the spanfilade.

---

## Code Exploration

Now I have the complete picture. Here is the full answer.

---

## Answer

**`subtreefree` reclaims only enfilade tree nodes (crums). It does not touch granfilade content via I-address.** The POOM crum's I-address information is simply dropped with the crum — no granfilade content is accessed, evicted, or freed.

---

### Execution Path

#### 1. `deletend` — the entry point [`edit.c:31`]

```c
case 1:
    disown ((typecorecrum*)ptr);      /* edit.c:59 */
    subtreefree ((typecorecrum*)ptr); /* edit.c:60 */
    break;
```

`deletecutsectionnd` returns `1` when the crum lies entirely within the deleted span [`edit.c:235–248`]. `disown` unlinks it from its parent in the tree. Then `subtreefree` is called on the orphaned root of that sub-tree.

---

#### 2. `subtreefree` — the definition [`credel.c:413`]

```c
/* assumes crum is disowned */
void subtreefree(typecorecrum *ptr)
{
    if (ptr->height > 0) {
        for (p = ((typecuc *)ptr)->leftson; p; p = right) {
            right = p->rightbro;
            disown (p);
            subtreefree (p);           /* credel.c:427 — recurse */
        }
    } else if (ptr->cenftype == GRAN
            && ((typecbc *)ptr)->cinfo.infotype == GRANORGL
            && ((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglincore)
        orglfree (((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglptr); /* credel.c:430 */
    freecrum (ptr);                    /* credel.c:431 */
}
```

The logic has two branches:

- **Interior node** (`height > 0`): recurse into all children, then free this node. No content access.
- **Leaf node** (`height == 0`): check for the special GRAN/GRANORGL case, then always call `freecrum`.

---

#### 3. Why the GRAN/GRANORGL branch never fires for POOM crums

The guard at `credel.c:429` requires:

```c
ptr->cenftype == GRAN    /* enf.h:12: GRAN=1, POOM=2 */
```

A POOM crum has `cenftype == POOM` (2), not `GRAN` (1) [`enf.h:12–13`]. The condition is always false for any node in a POOM enfilade. The granfilade access branch is dead code from `deletend`'s perspective.

---

#### 4. What `orglfree` does (for completeness, for GRAN crums)

Even when `orglfree` is reached (only for GRAN leaf crums, not POOM), it does not delete granfilade content:

```c
void orglfree(typecuc *ptr)          /* credel.c:470 */
{
    /* assert: diskorglptr was written to disk */
    ((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglincore = FALSE;
    ((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglptr = NULL;
    subtreefree ((typecorecrum*)ptr); /* credel.c:489 */
}
```

It asserts the on-disk copy exists (guarded by the `DISKPTRNULL` check at `credel.c:481`), then simply **clears the in-core pointer** — it evicts the cache, but leaves the disk-resident granfilade block untouched. The disk content is intentionally preserved.

---

#### 5. Corroborating comment in `corediskout.c`

```c
/*subtreefree(ptr);*/ /*12/04/86*/   /* corediskout.c:410 */
```

In the disk-write path, `subtreefree` was explicitly commented out as of December 1986. This is consistent with a design where granfilade content outlives the in-memory crum tree that references it.

---

### Summary

| What gets freed | What does not get freed |
|-----------------|------------------------|
| POOM crum tree nodes (all heights), via `freecrum` → `efree` | Granfilade content (disk blocks) |
| In-core GRAN orgl pointer (if `GRANORGL` leaf) | I-address slots referenced by deleted POOM crums |
| The crum's own heap allocation | On-disk granfilade blocks pointed to by I-addresses |

The I-address fields in the POOM crum's dimension span (`cdsp`) are carried along and dropped when the crum struct is freed by `efree` [`credel.c:452`]. Nothing traverses those I-addresses to notify the granfilade. The granfilade has no reference count decremented. The content it holds survives the deletion intact.

---

## Question 12 [gregory]

> After DELETE shifts surviving POOM entries left via `tumblersub`, is there any mechanism that detects when two formerly non-adjacent entries become I-address-contiguous and merges them via `isanextensionnd`, or do they remain as separate crums permanently?

### Gregory's Answer

## KB Synthesis

**No, there is no such mechanism. Crums that become I-address-contiguous after DELETE remain permanently separate.**

Here is why:

**`isanextensionnd` is INSERT-only**

From [ST-INSERT] (Finding 0062), `isanextensionnd` at `insertnd.c:293-301` fires exclusively during the INSERT code path when new content is being placed. It checks two conditions: same `homedoc` AND `new_content.origin == existing_crum.reach`. This is a guard on *new incoming content*, not a post-hoc scan of existing crums. The DELETE code path never calls `isanextensionnd` or anything equivalent.

**`recombinend` after DELETE is structural, not I-space-aware**

From [ST-DELETE] (Finding 0058), after `deletend` removes and shifts crums, it calls `setwispupwards` and `recombinend`. From [ST-REBALANCE-2D] (Finding 0071), `recombinend` merges tree nodes based on `ishouldbother`, which tests combined `numberofsons` against the branching limit — a pure B-tree occupancy criterion. It has no awareness of I-address ranges. When `eatbrossubtreend` consolidates two sibling nodes, it moves their *children* together; bottom crums (height-0 leaves) are moved as opaque units. Their `origin` and `width` fields are never compared for contiguity.

**The consequence**

Consider "ABXCD" where "AB" and "CD" are separate crums because "X" was inserted between them (paying the +2 crum cost from [ST-CRUM-BOUND]). After DELETE removes "X", the two crums are shifted and become I-address-adjacent in V-space, but they remain as two distinct POOM entries indefinitely. The crum count decreases only by the number of crums that fell entirely within the deletion range (Case 1: `disown` + `subtreefree` from [ST-DELETE] Finding 0064), never by post-shift contiguity detection.

This also means the crum bound `c ≤ 1 + 2C + 2L + 3R + 3P` from [ST-CRUM-BOUND] is monotonically non-decreasing with respect to interior insertion events, and DELETE does not recover the +2 penalty paid for each cursor repositioning.

---

## Code Exploration

Here is the full answer.

---

## Answer: No Contiguity-Based Merging Occurs After DELETE

The short answer is: **after `tumblersub` shifts surviving POOM crums left, there is no mechanism that detects newly-contiguous I-addresses and merges the crums. They remain as separate bottom crums permanently.** `isanextensionnd` is exclusively an INSERT-path function and is never invoked during delete or recombine.

---

### 1. The DELETE Path

Entry: `fns.c:deletevspan()` → `do1.c:dodeletevspan()` [do1.c:158–167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr) );
}
```

`deletevspanpm` ultimately calls `deletend()` in `edit.c:31–76`, which handles the 2D (SPAN/POOM) case.

Inside `deletend()`, after cuts are placed and the intersection region is found, each surviving crum that lies entirely to the right of the deleted region gets **case 2**:

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```
[edit.c:63–65]

This shifts the crum's displacement left by `width`. After all crums are processed:

```c
setwispupwards (father,1);
recombine (father);          // edit.c:74–75
```

---

### 2. What `recombine()` Does — and Does NOT Do

`recombine()` [recombine.c:22–34] dispatches on enfilade type. For POOM it calls `recombinend()`:

```c
int recombine(typecuc *father)
{
    switch (father->cenftype) {
      case GRAN:  recombineseq (father); break;
      case SPAN:  recombinend (father);  break;
      case POOM:  recombinend (father);             // ← POOM goes here
    }
}
```

`recombinend()` [recombine.c:104–131]:

```c
int recombinend(typecuc *father)
{
    if (father->height < 2  || !father->modified)
        return(0);
    for (ptr = getleftson (father); ptr; ...)
        recombinend (ptr);                          // recurse on children

    getorderedsons (father, sons);
    n = father->numberofsons;
    for (i = 0; i < n-1; i++) {
        for (j = i+1; sons[i] && j < n; j++) {
            if(i != j && sons[j] && ishouldbother(sons[i],sons[j])){
                takeovernephewsnd (&sons[i], &sons[j]);
            }
        }
    }
    if (father->isapex)
        levelpull (father);
}
```

`ishouldbother()` [recombine.c:150–163] is the gate:

```c
bool ishouldbother(typecuc *dest, typecuc *src)
{
    ...
    return (dest->numberofsons + src->numberofsons <=
            (dest->height>1 ? MAXUCINLOAF : MAX2DBCINLOAF)
            && randomness(.3));
}
```

And `randomness()` [recombine.c:132–147] **always returns TRUE** — the probabilistic body is commented out:

```c
bool randomness(float probability)
{
  static float i = 0;
  return(TRUE);
  /* i += probability; ... */
}
```

**Critical observation**: `ishouldbother` decides whether to merge two internal nodes based solely on **capacity** (whether the combined son-count fits within `MAXUCINLOAF`/`MAX2DBCINLOAF`). It does not inspect the I-address layout of the content at the leaves. The subsequent `takeovernephewsnd()` / `eatbrossubtreend()` re-parents children between internal nodes — this is tree **rebalancing**, not content **consolidation**.

The bottom crums (the actual POOM leaf entries holding `homedoc`, `cdsp`, `cwid`) are moved between internal nodes but are **never merged into one another** by `recombine`.

---

### 3. Where `isanextensionnd` Is Called — And Is Not

`isanextensionnd` [insertnd.c:301–309]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

It computes the crum's `reach` (absolute end address) and compares it against the `origin` of incoming new content. If they are equal **and** the homedoc matches, the new content is an I-address-contiguous extension — so no new crum is created; instead the existing crum's width is widened in place.

`isanextensionnd` has exactly **one call site** in the entire codebase:

```c
// insertnd.c:249–258
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified (ptr);
        setwispupwards (father,1);
        ...
        return(FALSE);
    }
}
```

This is inside `insertcbcnd()` [insertnd.c:242–275], reachable only through the `insertmorend()` → `insertcbcnd()` call chain, which is called from `insertnd()` [insertnd.c:15], which is called from the INSERT operation. It is **not** on any path reachable from `deletend()`, `recombine()`, `recombinend()`, `takeovernephewsnd()`, or `eatbrossubtreend()`.

---

### 4. Summary

| Step | What Happens |
|------|-------------|
| DELETE issued | `dodeletevspan()` [do1.c:158] → `deletevspanpm()` → `deletend()` [edit.c:31] |
| Surviving crums shifted | `tumblersub(&ptr->cdsp.dsas[index], width, ...)` [edit.c:63] per crum |
| Post-delete hook | `recombine(father)` [edit.c:75] |
| `recombine` for POOM | `recombinend()` [recombine.c:32, 104] — merges **internal tree nodes** by capacity |
| I-contiguity check | **Never happens** — `isanextensionnd` is INSERT-only [insertnd.c:250] |
| Result | Two formerly non-adjacent crums that are now I-address-contiguous **remain as separate crums permanently** |

The `recombine` step is a tree-balance operation over internal enfilade nodes, not a content-level compaction of leaf crums. Nothing in the delete path looks at whether the I-address `reach` of one surviving crum now equals the I-address `origin` of its neighbor. That adjacency check (`isanextensionnd`) is wired only into the insertion code path, where it prevents creating a redundant new crum when an extension is being appended.

**The POOM enfilade therefore accumulates permanent leaf-level fragmentation through repeated delete/insert cycles.** Each contiguous run that was once a single crum can be split into arbitrarily many separate crums, and no compaction ever re-merges them except when new content is appended at exactly the right address during a subsequent insert.

---

## Question 13 [gregory]

> When `slicecbcpm` splits a bottom crum at a DELETE boundary classified as THRUME, does the surviving fragment's I-width get recomputed from the new V-width, or is it sliced independently — and can the two ever diverge in tumbler exponent?

### Gregory's Answer

## KB Synthesis

The KB documents the pre/post conditions of `slicecbcpm` but not its internal mechanics directly. Here is what can be synthesized with confidence, and where the KB is silent.

---

## What the KB establishes

**The cut is identified in V-space.** `makecutsbackuptohere` calls `whereoncrum()` on V-addresses, and the THRUME guard fires only when `grasp_V < cut < reach_V` (strict inequalities). The local offset is then `localcut = tumblersub(cut, &grasp)` — a V-dimension subtraction [PRE-DELETE, `ndcuts.c:396`].

**Both pieces must have positive width in both dimensions.** [INV-NO-ZERO-WIDTH-CRUM] proves this from the strict interiority of the cut: `0 < localcut < cwid`. `locksubtract` at `ndcuts.c:444` computes the remainder, also guaranteed positive. These invariants hold for each piece independently, but the KB proves them only via V-space reasoning — it does not separately prove the I-dimension widths are positive.

**V-width and I-width encode the same integer at different precisions.** [SS-POOM-BOTTOM-CRUM] and [SS-INSERT-VWIDTH-ENCODING] establish that at INSERT time, V-width is produced by extracting `inc = tumblerintdiff(I_width, zero)` and re-encoding as `tumblerincrement(zero, shift, inc)` where `shift = tumblerlength(V_address) - 1`. The two representations have structurally different exponents by design — I-width uses ~9 tumbler digits, V-width uses ~2 — but `tumblerintdiff` on either always returns the same integer. [INV-WIDTH-VALUE-EQUIVALENCE] requires this to hold after every operation that creates or modifies bottom crums.

---

## The question the KB cannot answer

The KB does not contain `slicecbcpm` source code or a finding that directly documents its internal cut-point computation. Two plausible implementations both satisfy [INV-WIDTH-VALUE-EQUIVALENCE]:

1. **V-first, then I derived.** Compute `localcut_V` in V-space arithmetic. Extract its integer value via `tumblerintdiff`. Re-encode at I-precision for the I-width. This mirrors the [SS-INSERT-VWIDTH-ENCODING] pattern exactly.

2. **Independent slicing.** Compute `localcut_V` for the V-dimension and `localcut_I` for the I-dimension separately using each space's arithmetic. Since the crum represents a 1-to-1 V-to-I mapping across a contiguous range, the same integer count falls out of both calculations naturally.

Either path produces pieces where `tumblerintdiff(new_V_width) == tumblerintdiff(new_I_width)`.

---

## Can the exponents diverge?

They were already asymmetric before the split — this is structural, not pathological [SS-POOM-BOTTOM-CRUM]. After a THRUME split:

- The new V-width exponent is determined by the V-address precision of the cut (`shift = tumblerlength(cut_V) - 1`), consistent with [SS-INSERT-VWIDTH-ENCODING].
- The new I-width exponent is determined by I-address arithmetic, which operates at a much finer precision.

A *pathological* divergence — where the two representations encode *different integers* — cannot occur as long as [INV-WIDTH-VALUE-EQUIVALENCE] holds as a maintained invariant. The KB gives no evidence that `slicecbcpm` violates this invariant; [INV-NO-ZERO-WIDTH-CRUM] is proved specifically assuming the cut is THRUME, which is the same precondition under which `slicecbcpm` is invoked [PRE-DELETE, `ndcuts.c:77-90`].

The edge case in [EC-VWIDTH-ZERO-ADDRESS] — `shift = tumblerlength(vsaptr) - 1` producing anomalous exponents when `vsaptr` is zero — does not apply here because `slicecbcpm` is only reached from non-zero cut positions strictly interior to a non-zero-width crum.

---

## Summary

The KB establishes that `slicecbcpm` is called only for THRUME cuts, produces two pieces of strictly positive width, and must preserve [INV-WIDTH-VALUE-EQUIVALENCE]. Whether V and I dimensions are sliced independently or one is derived from the other is not documented — the KB is silent on `slicecbcpm` internals. What is documented is the invariant that must be maintained: integer value equality across representations, with a pre-existing and permanent exponent asymmetry that is a structural property of POOM bottom crums, not something the split can introduce or repair.

---

## Code Exploration

I now have all the code I need. Here is the complete answer:

---

## `slicecbcpm` at a THRUME DELETE boundary: I-width vs V-width

### The function and its invariants

`slicecbcpm` lives at `backend/ndcuts.c:373`. Its signature:

```c
int slicecbcpm(typecorecrum *ptr, typewid *offset, typecorecrum *new,
               tumbler *cut, INT index)
```

`ptr` is the crum being split; `new` will become the right fragment; `cut` is the cut address; `index` is the single dimension on which the THRUME test was applied.

**THRUME** is defined at `backend/common.h:88`:

```c
#define THRUME 0
```

It means `cut` lies strictly inside `[grasp, grasp + cwid)` in the `index` dimension. The guard at `ndcuts.c:383` fires a `gerror` if the cut is not THRUME before proceeding.

**Precondition on widths**: `ndcuts.c:389` runs:

```c
if (!lockis1story (ptr->cwid.dsas, (unsigned)widsize(enftype)))
    gerror ("Not one story in POOM wid\n");
```

`lockis1story` (`wisp.c:298-304`) checks every dimension in `cwid` for `is1story`, which (`tumble.c:237-247`) verifies `mantissa[1..NPLACES-1]` are all zero. So before any split, **every dimension of the crum width must be a single-digit tumbler** — i.e., of the form `{exp: E, mantissa[0]: M, rest 0}`.

For POOM crums, `widsize(POOM) = WIDSIZEPM = 2` (`wisp.h:27`, `wisp.h:60`), so `cwid.dsas` has two tumblers: `[0]` = V-space width, `[1]` = I-space width.

---

### Computing `localcut`

```c
tumblersub (cut, &grasp.dsas[index], &localcut);   // ndcuts.c:396
```

`grasp.dsas[index]` is the left boundary of the crum in the `index` dimension (computed by `prologuend` at `retrie.c:334-339` as `offset + ptr->cdsp`). So `localcut` is the cut's offset within the crum — but **only in the `index` dimension** (typically V, the dimension where THRUME was established for a delete).

Two further guards on `localcut`:

- `ndcuts.c:398`: `localcut.exp == ptr->cwid.dsas[index].exp` — same tumbler exponent as the V-width
- `ndcuts.c:410`: `is1story(&localcut)` — `localcut` is itself a single-digit tumbler

So `localcut = {exp: E_v, mantissa[0]: L, rest 0}` where `0 < L < M_v` (strictly inside by THRUME).

---

### The split loop — the key section

```c
movewisp (&ptr->cwid, &newwid);                          // ndcuts.c:438
for (i = 0; i < widsize(enftype); i++) {   /* I really don't understand this loop */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];   // ndcuts.c:440
    tumblerjustify (&newwid.dsas[i]);                     // ndcuts.c:441
}
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid,
              (tumbler*)&new->cwid, (unsigned)widsize(enftype)); // ndcuts.c:444
movewisp (&newwid, &ptr->cwid);                          // ndcuts.c:445
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);   // ndcuts.c:446
```

The comment at line 439 — **`/* I really don't understand this loop */`** — is in the original source.

Step by step:

1. `movewisp` copies all of `ptr->cwid` into `newwid`, both dimensions.
2. The loop runs for `i = 0` (V-dim) and `i = 1` (I-dim).
   - **For both**, it overwrites `newwid.dsas[i].mantissa[0]` with `localcut.mantissa[0]` (= `L`).
   - The exponent is **not touched** — each `newwid.dsas[i].exp` remains whatever the original crum width's exponent was for that dimension.
   - `tumblerjustify` normalizes leading zeros (shifts mantissa and decrements exp if `mantissa[0] == 0`).
3. `locksubtract` (`wisp.c:275-279`) calls `tumblersub` independently on each dimension:
   - right V-width: `tumblersub(&ptr->cwid.dsas[0], &newwid.dsas[0], &new->cwid.dsas[0])`
   - right I-width: `tumblersub(&ptr->cwid.dsas[1], &newwid.dsas[1], &new->cwid.dsas[1])`
4. `movewisp` installs `newwid` as `ptr->cwid` (the left fragment).

**The I-width is sliced independently.** It is not recomputed from the V-width. The same `localcut.mantissa[0]` value is injected into both `newwid.dsas[0]` and `newwid.dsas[1]`, but the subtraction that produces each fragment's width runs separately per dimension, with no cross-dimension awareness.

---

### What each fragment gets

Let the original crum have:
- V-width: `{exp: E_v, mantissa[0]: M_v, rest 0}`
- I-width: `{exp: E_i, mantissa[0]: M_i, rest 0}`
- Cut localcut: `{exp: E_v, mantissa[0]: L}`, with `0 < L < M_v`

After the loop, `newwid`:
- dim 0: `{exp: E_v, mantissa[0]: L}`
- dim 1: `{exp: E_i, mantissa[0]: L}`  ← **same L, but original I-exponent**

**Left fragment** (`ptr->cwid = newwid`):
- V-width: `{exp: E_v, mantissa[0]: L}`
- I-width: `{exp: E_i, mantissa[0]: L}`

**Right fragment** (`new->cwid = ptr->cwid - newwid` via `strongsub`):

`strongsub` (`tumble.c:534-565`) with two 1-story tumblers of the same exponent and `M ≠ L`:

```c
answer.exp = aptr->exp;              // tumble.c:548
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {
    --answer.exp;                    // tumble.c:550
    ...
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];  // tumble.c:556
```

Because `M_v ≠ L` (THRUME ensures strict interior), the first digit comparison at line 549 fails immediately — zero iterations — so:
- right V-width: `{exp: E_v, mantissa[0]: M_v - L}`
- right I-width: `{exp: E_i, mantissa[0]: M_i - L}`

---

### Can V and I exponents diverge?

**The split cannot create new exponent divergence where none existed.**

If the original crum had `E_v == E_i`, both fragments will also have equal exponents in V and I after the split. The `strongsub` exponent logic (`tumble.c:548-554`) only decrements exp when *matching leading digits* are found — and with `M ≠ L`, the very first comparison fails, so `answer.exp = aptr->exp` (the original dimension's exponent, unchanged).

**Pre-existing divergence is preserved.** If `E_v ≠ E_i` in the original crum, both output fragments will have `E_v` in their V-widths and `E_i` in their I-widths. The split makes no attempt to equalize them.

**One edge case that can produce I-width zero**: THRUME is tested only in the `index` dimension (V). There is no guard that `L < M_i`. If `M_i == L`, then `M_i - L = 0` and after `tumblerjustify` inside `tumblersub` (`tumble.c:289-313`), the right fragment's I-width becomes the zero tumbler (`{exp: 0, sign: 0, mantissa: all 0}`). If the V-width is non-zero with exponent `E_v`, this produces `E_v ≠ 0 = E_i` — exponent divergence introduced by the split itself. There is no code guard against this scenario; only the application-layer invariant that POOM crums maintain equal V-span and I-span (a 1:1 content mapping) prevents it in practice.

---

### Summary

| Question | Answer |
|---|---|
| Is I-width recomputed from new V-width? | **No.** The same `localcut.mantissa[0]` is injected into both dimensions' `newwid.dsas[i]` in the loop at `ndcuts.c:439-442`, then each is subtracted independently via `locksubtract`. |
| Are they sliced independently? | **Yes.** `locksubtract` calls `tumblersub` once per dimension with no inter-dimension coordination (`wisp.c:275-279`). |
| Can exponents diverge from the split? | **Not from the arithmetic itself** — `strongsub` preserves each dimension's original exponent when the 1-story precondition holds. Pre-existing divergence (`E_v ≠ E_i`) is passed through unchanged. The one true divergence risk is if `L == M_i` (I-width right-fragment goes to zero), but THRUME only guards `L < M_v`, not `L < M_i`. |
| Programmer's confidence in the loop? | Low — it is annotated `/* I really don't understand this loop */` at `ndcuts.c:439`. |

---

## Question 14 [gregory]

> If a document has content transcluded into three other documents and that content is DELETEd from the source, do the DOCISPAN entries in the spanfilade for the source document remain searchable by `findlinksfromtothreesp`, and does the source document still appear in `find_documents_containing` results despite having no current POOM mapping?

### Gregory's Answer

## KB Synthesis

Yes on both counts, and the two mechanisms are distinct sub-indices within the same append-only spanfilade.

**DOCISPAN entries persist after DELETE**

DELETE modifies only the document's POOM in the granfilade. `dodeletevspan` → `deletevspanpm` → `deletend` — none of these functions call any spanfilade function. [ST-DELETE] (Finding 0057) states the frame condition explicitly: `delete(D, vspan) ⟹ spanf_entries_after = spanf_entries_before`. The spanfilade has no delete operation anywhere in `spanf1.c` or `spanf2.c`. [INV-SPANF-WRITE-ONLY] formalizes this: the set of spanfilade entries is monotonically non-decreasing, forever.

**`find_documents_containing` still returns the source document**

This is confirmed by [EC-STALE-SPANF-REFERENCE] and [INV-IADDRESS-PERMANENT]. The DOCISPAN entries created when those I-addresses were first inserted into the source document remain in the spanfilade. `finddocscontainingsp` queries these entries and returns the source document alongside the three transcluding documents — even though the source's POOM no longer maps those I-addresses to any V-position. The correct invariant is:

```
actual_docs(i) ⊆ find_documents(i)
```

where `actual_docs(i) = {D | ∃ v : poom.D(v) = i}`. The reverse does not hold. [INT-DELETE-SPANF-DIVERGENCE] labels this the permanent divergence between POOM and spanfilade state.

**A note on `findlinksfromtothreesp` specifically**

`findlinksfromtothreesp` does not search DOCISPAN entries. It searches the link endset sub-index (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3 in the ORGLRANGE dimension), not the type-4 DOCISPAN sub-index. [SS-DOCISPAN] and [SS-SPANF-OPERATIONS] distinguish these as separate sub-structures within the spanfilade. If links were created on those I-addresses, their endset entries also persist (same write-only guarantee), so `findlinksfromtothreesp` continues to discover them — including from the three transcluding documents, whose POOMs are completely unaffected by the source DELETE per [FC-DELETE-CROSS-DOC].

**The three transcluding documents are entirely unaffected**

DELETE is strictly per-document POOM surgery. [FC-DELETE-CROSS-DOC] confirms: `∀ D' ≠ D : delete(D, vspan) ⟹ poom(D') = poom_before(D')`. The transcluding documents' POOMs still map those I-addresses to V-positions, their DOCISPAN entries persist, and link discovery via `find_links` on any of those three documents continues to work normally.

---

## Code Exploration

I now have everything I need. Here is the full answer.

---

## Answer

### The Two Relevant Structures

- **Granfilade (`granf`)**: Per-document POOMs (Permutation Object Ordering Matrices) that map virtual V-addresses to I-addresses (permascroll positions).
- **Spanfilade (`spanf`)**: A single global 2D enfilade indexed by `(SPANRANGE, ORGLRANGE)`. The `ORGLRANGE` dimension encodes both a document ISA and a **span type** prefix. Four span types are defined [xanadu.h:36-39]:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

---

### What Happens When Content Is Transcluded (COPY)

`docopy` [do1.c:45-65] calls both:
1. `insertpm(...)` — writes a crum into the destination document's POOM (granfilade)
2. `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` — writes an entry into the spanfilade

`insertspanf` [spanf1.c:22] encodes the entry:
```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
// ...
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

The **ORGLRANGE key is `4.docISA`** (spantype=4 prefixed to the document address). The **SPANRANGE key is the ispan** (permascroll address of the content). This DOCISPAN entry permanently records: *"document `docISA` contains ispan `I`."*

When source doc **S** has content (at ispan I, vspan V), and that content is transcluded into docs **A**, **B**, **C** — each `docopy` writes a DOCISPAN entry for the respective transclusion target (A, B, or C), embedding the same ispan I in SPANRANGE. S itself also has its own DOCISPAN entry written during its original `doinsert` → `docopy` chain.

---

### What `dodeletevspan` Actually Modifies

```c
// do1.c:158-167
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

```c
// orglinks.c:145-152
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` [edit.c:31] operates on `docorgl` (a handle into the **granfilade**). It removes the V→I mapping from S's POOM.

**The spanfilade (`spanf`) is never touched.** A grep over the entire backend for `deletend.*spanf`, `spanf.*delete`, and `removefromspan` returns zero matches. There is no code path anywhere in the system that removes DOCISPAN (or any other) spanfilade entries when content is deleted.

---

### Q1: Do the DOCISPAN Entries for S Remain Searchable by `findlinksfromtothreesp`?

**First, a structural clarification**: `findlinksfromtothreesp` does **not** search DOCISPAN entries at all. It operates on LINKFROMSPAN (1), LINKTOSPAN (2), and LINKTHREESPAN (3) entries — which are in an entirely different numeric range of the ORGLRANGE dimension of the spanfilade (keys `1.x`, `2.x`, `3.x` vs. DOCISPAN's `4.x`).

`findlinksfromtothreesp` [spanf1.c:56-103] drives through `sporglset2linkset` → `sporglset2linksetinrange` [sporgl.c:239-269]:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
// spantype = 1, 2, or 3 — never 4
prefixtumbler (&orglrange->width, 0, &range.width);
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
```

DOCISPAN entries never appear in any `retrieverestricted` call issued by this path. They are invisible to `findlinksfromtothreesp` regardless of whether they persist or not.

**What `findlinksfromtothreesp` does require** is resolving the input specset to an ispan via S's POOM. The path is:

`findlinksfromtothreesp` → `specset2sporglset` → `vspanset2sporglset` [sporgl.c:35-65] → `findorgl(granf, S)` + `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted(S's POOM, vspanptr, V, NULL, I, NULL)`

Since `dodeletevspan` removed the V→I mapping from S's POOM, `retrieverestricted` on that POOM returns an empty context. The ispan lookup yields nothing. The sporglset is empty. `sporglset2linksetinrange` loops over nothing. `findlinksfromtothreesp` returns `*linksetptr = NULL`.

**Conclusion for Q1**: After deleting S's content at vspan V:
- The DOCISPAN entries for S in the spanfilade **do persist** (they are never removed).
- They are **not searchable by `findlinksfromtothreesp`** — not because they disappear, but because that function never queries DOCISPAN entries. If the specset is expressed as a vspec in terms of S, the POOM resolution step fails silently and the function returns no links. If the specset is expressed in terms of A, B, or C (which still have valid POOM mappings to ispan I), `findlinksfromtothreesp` still works and returns any links attached to that ispan.

---

### Q2: Does S Still Appear in `find_documents_containing` Results?

`dofinddocscontaining` [do1.c:15-23]:
```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
  typeispanset ispanset;
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && finddocscontainingsp (taskptr, ispanset, addresssetptr));
}
```

`finddocscontainingsp` [spanf1.c:151-188]:
```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                   ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        // add document to result set
    }
}
```

This function queries the spanfilade **directly** for DOCISPAN entries in `ORGLRANGE` that intersect the given ispanset in `SPANRANGE`. It does **not** consult any document's POOM. The DOCISPAN entry for S (recording that S once contained ispan I) was written when S's content was originally inserted and was **never removed** by `dodeletevspan`.

**Conclusion for Q2**: **Yes.** Source document S will still appear in `find_documents_containing` results, even though S's POOM has no current mapping for that content. The spanfilade retains the phantom DOCISPAN entry from S's original content insertion, and `finddocscontainingsp` finds it directly without any POOM consultation.

---

### The Structural Inconsistency

This reveals a fundamental post-delete inconsistency in udanax-green's storage model:

| Data structure | After `dodeletevspan` |
|---|---|
| S's POOM (granfilade) | V→I mapping removed; S no longer maps vspan V to ispan I |
| Spanfilade DOCISPAN entries | S's entry `(4.S, I)` remains permanently |
| Spanfilade link endpoint entries | Entries for any links referencing S's content remain, but are unreachable if the specset is expressed as an S vspec, because POOM lookup fails |

The spanfilade is an **append-only** structure from the perspective of content operations. DELETE removes content from the POOM but leaves all spanfilade traces intact. Any query path that routes through the spanfilade directly (like `finddocscontainingsp`) will observe S as a containing document. Any query path that must first resolve a vspec through S's POOM (like `findlinksfromtothreesp`) will silently fail to map the now-deleted vspan and return empty results — but not because the spanfilade was cleaned up; rather because the POOM resolution step upstream of the spanfilade query returns nothing.

---

## Question 15 [gregory]

> When a link's source endset spans I-addresses `[.0.1.3, .0.1.7]` and a DELETE removes the V-mapping for `[.0.1.4, .0.1.6]` from the only document containing that content, does `span2spanset` during FOLLOWLINK return two disjoint V-spans for the surviving fragments, or does it return an empty result because the I→V conversion finds no current POOM entry covering the interior range?

### Gregory's Answer

## KB Synthesis

## Answer: Two Disjoint V-Spans

`span2spanset` returns **two disjoint V-spans** — one for each surviving I-address fragment. It does not return empty.

### Mechanism

FOLLOWLINK converts endset I-addresses to V-addresses via `link2sporglset()` → `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` [SS-FOLLOWLINK]. The critical behavior is in `span2spanset`: it queries the POOM for every I-address in the endset range, and **silently drops** those with no current POOM mapping [INV-ITOV-FILTERING].

After DELETE removes V-mappings for `[.0.1.4, .0.1.6]`:

- The POOM crums for those I-addresses are freed via `disown` + `subtreefree` [ST-DELETE, Finding 0064]
- The granfilade retains the bytes at those I-addresses — only the POOM is mutated [INV-IADDR-IMMUTABILITY]
- POOM entries for `.0.1.3` and `.0.1.7` survive (the latter at a shifted V-position due to DELETE's Case 2 shift) [ST-DELETE, Finding 0053/0055]

When `findcbcinarea2d` traverses the POOM with I-range `[.0.1.3, .0.1.7]` [SS-POOM-MULTIMAP]:

- `.0.1.3` → found, contributes V-span
- `.0.1.4`–`.0.1.6` → not found (freed), silently dropped
- `.0.1.7` → found, contributes V-span

The two contexts are accumulated via `incontextlistnd` in V-sorted order [INV-RETRIEVAL-V-SORTED], producing two separate entries.

### Why Not Consolidated

Although `.0.1.3` and `.0.1.7` may now be V-adjacent (deletion closed the gap), they are **not I-adjacent** — there is a gap between I:.0.1.4 and I:.0.1.7. The `isanextensionnd` consolidation requires contiguity in **both** V and I dimensions [ST-VCOPY, Finding 0046]. Without I-contiguity, the POOM retains two separate crums, and `span2spanset` reports one V-span per contiguous I-region [SS-LINK-ENDPOINT, Finding 0037]:

> "one per contiguous I-region"

### Why Not Empty

Empty results only occur when **all** endset I-addresses lack POOM mappings [EC-GHOST-LINK]. Here, two I-addresses survive. This is partial survival: the link is not orphaned, only fragmentary [EC-LINK-PARTIAL-SURVIVAL].

This is also consistent with [EC-ORPHANED-LINK] (Finding 0005): full orphaning requires deleting the content from *all* documents that reference those I-addresses. Deleting the middle fragment leaves the endpoints live.

### Summary

| I-address | POOM entry after DELETE | FOLLOWLINK result |
|-----------|------------------------|-------------------|
| `.0.1.3` | Exists (V-mapped) | Contributes V-span |
| `.0.1.4`–`.0.1.6` | Freed (`subtreefree`) | Silently dropped |
| `.0.1.7` | Exists (V-shifted) | Contributes V-span |

**Result: two disjoint V-spans.** The deletion creates a gap in the endset's V-space representation without orphaning the link.

---

## Code Exploration

I now have everything I need. Here is the complete answer with all code citations.

---

## Answer: `span2spanset` Returns Two V-Spans — Not Empty, and Not Disjoint

The answer is **neither** of the two alternatives as stated. `span2spanset` returns **two V-span objects**, but they are **adjacent in V-space** (not disjoint with a gap), because `deletend` collapses the V-address range at deletion time. Here is the full trace.

---

### Step 1 — How the Endset is Stored (`docreatelink`)

`docreatelink` [do1.c:195] converts the from/to V-specs to sporglsets via `specset2sporglset` [sporgl.c:14], which calls `vspanset2sporglset` [sporgl.c:35]:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        movetumbler(docisa, &sporglset->sporgladdress);
        movetumbler(&ispanset->stream, &sporglset->sporglorigin);   // I-span start
        movetumbler(&ispanset->width,  &sporglset->sporglwidth);    // I-span width
```

The I-address equivalent of the V-span is stored permanently in the sporgl. Then `insertendsetsinorgl` [do2.c:130] → `insertpm` [orglinks.c:75] stores those I-spans in the link's own POOM at V-positions `1.1` (from-end) and `2.1` (to-end). The stored endset is **I-span `[.0.1.3, width=4]`** in the link's POOM.

---

### Step 2 — `deletend` Collapses V-Space

`dodeletevspan` [do1.c:158] → `deletevspanpm` [orglinks.c:145]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

`deletend` [edit.c:31] sets up `knives.blades[0] = .0.1.4` and `blades[1] = .0.1.6`, calls `makecutsnd` to split crums at those V-positions, then for each child of the intersection node calls `deletecutsectionnd` [edit.c:235]:

```c
INT deletecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    for (i = knives->nblades-1; i >= 0; --i) {
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME)               return (-1);   // spans a knife — error
        else if (cmp <= ONMYLEFTBORDER)  return (i+1);  // returns 1 or 2
    }
    return (0);   // entirely left of deletion — no change
}
```

Assuming the document originally had a single identity-mapped POOM leaf I:`[.0.1.3,.0.1.7]` ↔ V:`[.0.1.3,.0.1.7]`, after `makecutsnd` splits it into three:

| Crum | V-range | I-range | `deletecutsectionnd` result | Action |
|------|---------|---------|----------------------------|--------|
| A | `[.0.1.3,.0.1.4)` | `[.0.1.3,.0.1.4)` | 0 (left of deletion) | unchanged |
| B | `[.0.1.4,.0.1.6)` | `[.0.1.4,.0.1.6)` | 1 (inside deletion) | **disowned + freed** |
| C | `[.0.1.6,.0.1.7)` | `[.0.1.6,.0.1.7)` | 2 (right of deletion) | **V-displacement shifted** |

Case 2 [edit.c:63]:
```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

Crum C's V-displacement: `.0.1.6 − .0.0.2 = .0.1.4`.

**Post-delete POOM state:**
- Crum A: I:`[.0.1.3,.0.1.4)` ↔ V:`[.0.1.3,.0.1.4)` (unchanged)
- Crum C: I:`[.0.1.6,.0.1.7)` ↔ V:`[.0.1.4,.0.1.5)` (shifted left by deleted width)

The V-space is now **contiguous** — the hole has been collapsed.

---

### Step 3 — FOLLOWLINK Retrieves the Stored I-Spans

`followlink` [fns.c:114] → `dofollowlink` [do1.c:223] → `link2sporglset` [sporgl.c:67]:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);   // V-position for from-end
tumblerincrement (&zero, 0, 1, &vspan.width);
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
        contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
```

`contextintosporgl` [sporgl.c:205] extracts `context->totaloffset.dsas[I]` (the stored I-origin) and `context->contextwid.dsas[I]` (the stored I-width). Result: sporgl with `sporglorigin = .0.1.3`, `sporglwidth = .0.0.4`.

---

### Step 4 — I→V Conversion: `sporglset2vspanset` → `ispan2vspanset` → `span2spanset`

`linksporglset2specset` [sporgl.c:97] → `linksporglset2vspec` → `sporglset2vspanset` [sporgl.c:141]:

```c
findorgl (taskptr, granf, homedoc, &orgl, type);
movetumbler (&sporglptr->sporglorigin, &ispan.stream);   // .0.1.3
movetumbler (&sporglptr->sporglwidth, &ispan.width);     // .0.0.4
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

`ispan2vspanset` [orglinks.c:389] → `permute` [orglinks.c:404] → `span2spanset` [orglinks.c:425]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex=I,
                              (typespan*)NULL, targindex=V, (typeisa*)NULL);
```

---

### Step 5 — `retrieverestricted` Finds Both Surviving Crums

`retrieverestricted` [retrie.c:56] sets:
- `span1start = .0.1.3`, `span1end = .0.1.7` (I-restriction)
- `span2start = zero`, `span2end = zero` (V, unconstrained — NULL input)

→ `retrieveinarea` → `findcbcinarea2d` [retrie.c:229] → `crumqualifies2d` [retrie.c:270]:

```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) return(FALSE);
startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return(FALSE);

endcmp = iszerotumbler(span2end) ? TOMYRIGHT : whereoncrum(..., span2end, index2);
if (endcmp < ONMYLEFTBORDER) return(FALSE);
startcmp = whereoncrum(crumptr, offset, span2start, index2);   // zero vs positive V → TOMYLEFT
if (startcmp > THRUME) return(FALSE);                          // TOMYLEFT < THRUME → pass
```

For the V dimension: `iszerotumbler(span2end=0)` → `TOMYRIGHT` (always passes), and `whereoncrum(crum, zero, V)` returns `TOMYLEFT` for any crum with positive V-displacement, and `TOMYLEFT < THRUME` so the second guard never fires. **The V dimension is entirely unconstrained.**

For the I dimension: both Crum A (I:`[.0.1.3,.0.1.4)`) and Crum C (I:`[.0.1.6,.0.1.7)`) overlap with the restriction `[.0.1.3,.0.1.7]`. **Both qualify.** There is no crum for I:`[.0.1.4,.0.1.6)` — Crum B was freed by `deletend`.

---

### Step 6 — `context2span` Extracts Two V-Spans

`context2span` [context.c:176] clips each context's V-range to the I-restriction:

```c
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
    // adjust V-start by the I-overhang
}
if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
    // adjust V-end by the I-overhang
}
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

**Crum A** (I:`[.0.1.3,.0.1.4)`, V:`[.0.1.3,.0.1.4)`):
- `grasp.I = .0.1.3 == lowerbound .0.1.3` → no V-start adjustment
- `reach.I = .0.1.4 < upperbound .0.1.7` → no V-end adjustment
- **Output:** V-span `{stream=.0.1.3, width=.0.0.1}`

**Crum C** (I:`[.0.1.6,.0.1.7)`, V:`[.0.1.4,.0.1.5)`):
- `grasp.I = .0.1.6 > lowerbound .0.1.3` → no V-start adjustment
- `reach.I = .0.1.7 == upperbound .0.1.7` → no V-end adjustment
- **Output:** V-span `{stream=.0.1.4, width=.0.0.1}`

---

### Step 7 — `onitemlist` Appends Without Merging

`span2spanset` [orglinks.c:444]:
```c
nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
```

`onitemlist` [orglinks.c:464] just allocates and appends items. Unlike `putvspaninlist` [orglinks.c:329], it has **no adjacency-merging logic**. Both V-spans are appended as separate objects.

---

## Conclusion

`span2spanset` returns **two V-span objects**, not empty. The I→V conversion succeeds for both surviving I-ranges. The "interior" I-range `[.0.1.4, .0.1.6)` has no POOM entry, so it contributes nothing to the output — but the two flanking I-ranges `[.0.1.3,.0.1.4)` and `[.0.1.6,.0.1.7)` do, and they produce valid V-spans.

**Critically, the V-spans are adjacent, not disjoint.** `deletend` [edit.c:63] performs `tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])` on every POOM node to the right of the deletion, collapsing V-space. Content originally at V:`[.0.1.6,.0.1.7)` is shifted left by the 2-unit deleted width and lands at V:`[.0.1.4,.0.1.5)` — immediately adjacent to the surviving V:`[.0.1.3,.0.1.4)`. The two returned spans tile contiguously:

```
Span 1: stream=.0.1.3, width=.0.0.1  ← from I:[.0.1.3,.0.1.4)
Span 2: stream=.0.1.4, width=.0.0.1  ← from I:[.0.1.6,.0.1.7) (shifted)
```

The second alternative — "empty result because the I→V conversion finds no current POOM entry covering the interior range" — is incorrect. `findcbcinarea2d` does not require a single contiguous POOM entry spanning the entire restriction. It independently qualifies each surviving leaf crum against the restriction range and collects them all. The absence of a POOM entry for I:`[.0.1.4,.0.1.6)` silently produces no output for that sub-range; it does not abort or suppress output for the ranges that do have entries.

---

## Question 16 [gregory]

> In the `strongsub` exponent guard that provides DELETE's subspace isolation — if a document has text entries at `V:1.x` with `exp=0` and a deletion width also at `exp=0` (say, deleting a range wider than 1.0), does the exponent guard still fire, or does isolation fail because the width and position share the same exponent class?

### Gregory's Answer

## KB Synthesis

## Analysis: strongsub Guard Under Same-Exponent Conditions

The guard fails and subspace isolation breaks. Here is why.

### How the protection normally works

The `strongsub` exponent guard is: if `b.exp < a.exp`, return `a` unchanged. From [FC-SUBSPACE] Finding 0055's concrete example:

```
Text crum:  V-displacement 0.4  (exp = -1)
Link crum:  V-displacement 2.1  (exp =  0)   ← relative to root
Width:                     0.3  (exp = -1)

strongsub(link.cdsp=2.1, width=0.3): b.exp(-1) < a.exp(0) → TRUE → returns 2.1 unchanged
strongsub(text.cdsp=0.4, width=0.3): b.exp(-1) < a.exp(-1) → FALSE → subtracts → 0.1
```

Isolation holds because the link crum's relative displacement (exp=0) exceeds the deletion width's exponent (exp=-1). This is accidental — DELETE constructs its knife blades as `[origin, origin + width]` with no subspace-boundary computation [INT-DELETE-SUBSPACE-ASYMMETRY].

### What happens when width.exp = crum.exp

The guard condition is **strictly** less-than. From [FC-SUBSPACE] Finding 0055's corrected postcondition:

> `∀ entry ∈ poom(doc) : entry.vpos > delete_end ∧ entry.vpos.exp = width.exp =⟹ entry.vpos' = entry.vpos - delete_width`

If both text crum displacement and deletion width are exp=0, then `b.exp(0) < a.exp(0)` is **FALSE**. The guard does not fire. Subtraction proceeds. If link crums also have displacement at exp=0 (which they typically do, since `2.1 - root.cdsp` is often `1.0` or similar), those crums are also shifted. Subspace isolation fails for both.

### When does a width reach exp=0?

Normal character deletions produce widths like `0.11`, `0.100` — these stay at exp=-1 regardless of character count. An exp=0 width requires a deletion span that crosses a hierarchical unit boundary. For example, deleting from `1.1` to `3.1` (spanning the text and link subspaces) yields width `3.1 − 1.1 = 2.0` (exp=0). The backend imposes no precondition against this — `deletevspanpm` only checks for zero width [PRE-DELETE].

### Why this matters for spec

[INT-DELETE-SUBSPACE-ASYMMETRY] explicitly flags this:

> DELETE's protection is accidental — there is no comment suggesting awareness of the exponent guard as a subspace protection mechanism. If `strongsub` were modified to handle cross-exponent subtraction correctly, DELETE would break subspace isolation while INSERT would remain safe.

The frame condition `∀ op ∈ {DELETE} on subspace s, ∀ entry: entry.vpos.mantissa[0] ≠ s ⟹ entry.vpos' = entry.vpos` from [FC-SUBSPACE] therefore rests on an invariant that deletion widths are *always* at a lower exponent class than cross-subspace crum displacements. A cross-subspace deletion (width exp=0) violates this assumption, and isolation fails — both text and link crums at exp=0 would be shifted.

INSERT has no such fragility: its second blade is structurally computed at `(N+1).1` by `findaddressofsecondcutforinsert`, placing all cross-subspace entries in case-2 (no-shift) before any arithmetic occurs [SS-TWO-BLADE-KNIFE].

---

## Code Exploration

---

## Analysis: The `strongsub` Exponent Guard and DELETE Subspace Isolation

### The Guard in Question

`strongsub` at `tumble.c:544–547`:

```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);
    return(0);
}
```

This is the only exponent check in the function. It fires when the subtrahend `b` is at a *strictly lower* (more negative) exponent than `a`. When it fires, it returns `a` unchanged — the effect is "a fine-grained subtrahend cannot shift a coarse-grained address."

### When Both Are `exp=0`: The Guard Does Not Fire

The `exp` field is a `short` [`common.h:63`], validated by `tumblercheckptr` to always be `<= 0` [`tumble.c:174–178`]:

```c
if (ptr->exp > 0){
    fprintf(stderr,"bad exp ");
    wrong = TRUE;
}
```

When a text entry's position is at `V:1.x` with `exp=0`, and the deletion width is also `exp=0` (e.g., `mantissa[0]=2`, representing a width greater than 1.0):

- The guard condition: `bptr->exp < aptr->exp` evaluates to `0 < 0` = **FALSE**
- The guard does **not** fire

Execution falls straight through to line 548:

```c
answer.exp = aptr->exp;
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {   // line 549
    --answer.exp;
    ...
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];  // line 556
```

Plain mantissa-level subtraction proceeds.

---

### Tracing the DELETE Call Path

`dodeletevspan` → `deletevspanpm` [`orglinks.c:145–152`] → `deletend` [`edit.c:31`].

Inside `deletend`, two things happen that touch `strongsub`:

**1. Computing the deletion boundary** [`edit.c:40–41`]:

```c
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
```

`tumbleradd` is the macro `functiontumbleradd` [`common.h:197`]. Because both `origin` and `width` are positive (`sign=0`), this takes the `aptr->sign == bptr->sign` branch at `tumble.c:374` → calls `absadd`. **`strongsub` is not invoked here at all.**

**2. Shifting survivors after deletion** [`edit.c:63`]:

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

`tumblersub` negates `width` and calls `tumbleradd(displacement, -width, ...)` [`tumble.c:406–430`]. Now signs differ. If `|displacement| > |width|`:

```c
} else if (abscmp (aptr, bptr) == GREATER) {
    strongsub (aptr, bptr, cptr);   // tumble.c:385
```

`strongsub` IS called here. For a crum at `V:3.5 = {exp=0, mantissa=[3,5,...]}` after a deletion of width `2 = {exp=0, mantissa=[2,...]}`:

- Guard: `bptr->exp(0) < aptr->exp(0)` → `0 < 0` = **FALSE** — guard bypassed
- Loop at line 549: compare `mantissa[0]`: `3 ≠ 2`, no matching prefix
- `answer.mantissa[0] = 3 - 2 = 1`, then digits from `a` copied: `answer.mantissa[1] = 5`
- Result: `{exp=0, mantissa=[1,5,...]}` = `V:1.5`

Correct arithmetic — the crum moves from `V:3.5` to `V:1.5`.

---

### What the Guard Actually Isolates (and What It Cannot)

The guard fires when `b->exp < a->exp` — i.e., when the subtrahend is at a **deeper level** than the minuend. Example:

- `a = V:5` — `{exp=0, mantissa=[5]}`
- `b = V:0.3` — `{exp=-1, mantissa=[3]}`

Condition: `-1 < 0` = TRUE → guard fires, returns `V:5` unchanged.

This prevents a sub-level width (e.g., a deletion whose width is expressed as a fractional V-amount at `exp=-1`) from erroneously displacing a main-level (`exp=0`) crum address. That is the isolation property: **sub-level deletions don't shift main-level addresses**.

But this protection is predicated entirely on an **exponent difference**. When both position and width are at `exp=0`, the guard has no basis to discriminate between them. It sees two values at the same level and performs normal subtraction.

---

### Isolation Failure in the `exp=0 / exp=0` Scenario

The V-space subspace structure, visible in `orglinks.c`:

- Text crums: `mantissa[1] == 0` (addresses like `V:1`, `V:2`, `V:3` — single-story) [`orglinks.c:247–252`]
- Link crums: `mantissa[0]==1 && mantissa[1]!=0` (addresses like `V:1.1`, `V:1.2`, ... — two-story starting with 1) [`orglinks.c:255–261`]

Both kinds have `exp=0`. The deletion range boundaries are computed in V-space via address arithmetic, and `deletecutsectionnd` [`edit.c:235–248`] classifies crums purely by whether their V-address falls inside `[blade[0], blade[1])`:

```c
for (i = knives->nblades-1; i >= 0; --i) {
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME) return (-1);
    else if (cmp <= ONMYLEFTBORDER) return (i+1);
}
```

There is no exponent-based fast-path in this classification. A link crum at `V:1.5` and a text crum at `V:2.5` are indistinguishable at this layer — both are `exp=0`, both are `THRUME` inside a range `[V:1, V:3)`, both get classified as `case 1` and deleted.

**The strongsub exponent guard plays no role in preventing this.** It only acts on the displacement arithmetic for `case 2` crums — those *after* the deletion range — and it is only operative when the width has a smaller exponent than the displacement. When both are `exp=0`, the guard is inoperative and deletion arithmetic is flat mantissa subtraction with no subspace awareness.

---

### Summary

| Condition | Guard fires? | What happens |
|---|---|---|
| `b->exp = -1`, `a->exp = 0` | **YES** | Guard returns `a` unchanged — sub-level width cannot shift main-level address |
| `b->exp = 0`, `a->exp = 0` | **NO** | Falls through to mantissa loop at `tumble.c:549`; plain digit subtraction |

When both position (`V:1.x`, `exp=0`) and deletion width (`exp=0`) share the same exponent class, the guard at `tumble.c:544` evaluates to `0 < 0 = FALSE` and does not fire. Isolation does not come from this guard in that scenario — it requires an exponent difference to exist. The guard is a cross-level arithmetic safety valve, not a V-subspace discriminator. In the equal-exponent case, `deletecutsectionnd` treats text and link crums identically, and the `strongsub` path performs straightforward digit-by-digit subtraction with no subspace protection.

---

## Question 17 [gregory]

> After DELETE removes all text content from a document but leaves links in the `0.2.x` subspace untouched, what does `retrievevspansetpm` return — an empty specset, a specset containing only the link subspace spans, or a bounding span that incorrectly implies text content exists?

### Gregory's Answer

## KB Synthesis

After deleting all text (1.x subspace), `retrievevspansetpm` returns a specset containing **only the link subspace spans**, reported at their actual internal `2.x` positions — not the normalized `0.x` form that appears when text is also present.

The evidence for this is direct:

**[SS-DUAL-ENFILADE], Finding 0038** documents the exact behavior:
> `retrievedocvspanset` output (document has links only, no text):
> ```
> [{"start": "2.1", "width": "0.1"}]
> Links reported at actual internal position 2.x
> ```
> Contrast with the mixed case:
> ```
> [{"start": "0", "width": "0.1"}, {"start": "1", "width": "1"}]
> Links normalized from 2.x → 0.x when document also has text
> ```

**[SS-ADDRESS-SPACE], Finding 0024** confirms with a concrete scenario:
> After deleting all text from a document containing a link:
> ```
> vspanset: [{start: "2.1", width: "0.1"}]   # link still present
> retrieve_contents: [{"link_id": "1.1.0.1.0.1.0.2.1"}]
> ```

The mechanism: `retrievevspansetpm()` calls `is1story()` to detect multi-subspace content. When text is absent, the text extent is zero and the output path that normalizes link positions to `0.x` (via `maxtextwid()`) is bypassed. The link span is reported at its raw stored position `2.x`.

This rules out both alternative answers:
- Not an **empty specset** — the link subspace is unaffected by text deletion ([SS-THREE-LAYER-MODEL], [FC-SUBSPACE], Finding 0055)
- Not a **bounding span** — that's the behavior of `RETRIEVEDOCVSPAN` (opcode 14), not `retrievevspansetpm` ([SS-VSPAN-VS-VSPANSET], Finding 0035)

One practical implication: the same link appears as `"start": "0"` when the document has text and as `"start": "2.1"` when all text is deleted ([EC-VSPAN-NORMALIZATION]). Code that hardcodes the `0.x` address for a link will break after the document's text is fully deleted.

---

## Code Exploration

Now I have a complete picture. Here is the full analysis.

---

## What `retrievevspansetpm` Returns After All Text Is Deleted

### Setup: the two subspaces

**`istextcrum`** (`backend/orglinks.c:246–253`) identifies text crums as those whose V-displacement has `mantissa[1] == 0` (a simple, single-story address) and whose width is also single-story:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0  && is1story(&crumptr->cwid.dsas[V])){
        return TRUE;
    }
    return FALSE;
}
```

**`islinkcrum`** (`backend/orglinks.c:255–261`) identifies link crums as those at V-displacements of the form `1.n` (mantissa[0]==1, mantissa[1]!=0):

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){
        return TRUE;
    }
    return FALSE;
}
```

**`is1story`** (`backend/tumble.c:237–247`) returns TRUE only when all `mantissa[1..NPLACES-1]` are zero — i.e. the tumbler is a simple integer with no sub-digits:

```c
bool is1story(tumbler *tumblerptr)
{
    INT i;
    for (i = 1; i < NPLACES; i++)
        if (tumblerptr->mantissa[i] != 0)
            return (FALSE);
    return (TRUE);
}
```

### What DELETE does to the POOM

`dodeletevspan` (`backend/do1.c:158–167`) calls through to `deletevspanpm` → `deletend` (`backend/edit.c:31–76`). Inside `deletend`, every child crum in the deleted range gets classified by `deletecutsectionnd`:

```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);   // edit.c:59–60
    break;
```

After the loop, `setwispupwards(father, 1)` propagates updated widths to the root, and `recombine(father)` restructures. When ALL text crums have been freed this way, only link crums (with their `1.n` V-addresses) remain as children of the root POOM crum. The root's `cwid.dsas[V]` is now recomputed to span only those link crums' extents.

### The branch decision in `retrievevspansetpm`

`retrievevspansetpm` (`backend/orglinks.c:173–221`) first checks:

```c
if (is1story (&ccptr->cwid.dsas[V])) { /* if it is just text return that */
```

With only link crums remaining, the root's `cwid.dsas[V]` must encode their positions, which have non-zero `mantissa[1]` (they are `1.n` addresses). Therefore `is1story` returns **FALSE**, and the function always enters the `else` branch — regardless of how much text content has been deleted.

### Inside the `else` branch: two spans are always produced

**Link span (lines 195–204):** Built directly from the root POOM's `cwid.dsas[V]` by zeroing `mantissa[1]` and justifying:

```c
linkvspan.itemid = VSPANID;
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.stream);
linkvspan.stream.mantissa[1] = 0;
tumblerjustify(&linkvspan.stream);
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.width);
linkvspan.width.mantissa[1] = 0;
tumblerjustify(&linkvspan.width);
```

This correctly extracts the link subspace portion of the total V-width. It is non-zero and reflects the actual links.

**Text span (lines 207–216):** `maxtextwid` is called with `&maxwid`:

```c
maxtextwid(taskptr, ccptr, &voffset, &maxwid);
vspan.itemid = VSPANID;
tumblerclear (&vspan.stream);
movetumbler (&maxwid, &vspan.width);
vspan.width.mantissa[0] = 0;
```

`maxwid` is declared at line 176 (`tumbler maxwid;`) but **never initialized** — only `voffset` receives a `tumblerclear` at line 182. Inside `maxtextwid` (`orglinks.c:224–244`), the root is not a text crum, so the function traverses its children:

```c
for(ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro (ptr)){
    if(ptr && !islinkcrum(ptr)){/* only look for text or overlapping stuff */
        maxtextwid(taskptr, ptr, &localvoffset, maxwidptr);
    }
}
```

All remaining children are link crums, so `islinkcrum(ptr)` is true for every one of them. The `maxwidptr` accumulator is **never written**. `maxwid` retains whatever uninitialized stack contents it had. Then `vspan.width.mantissa[0]` is forced to `0`, but `mantissa[1..NPLACES-1]` remain as garbage.

**Both spans are unconditionally added** (`orglinks.c:216–217`):

```c
putvspaninlist (taskptr, &vspan, vspansetptr);
putvspaninlist (taskptr, &linkvspan, vspansetptr);
return (TRUE);
```

### Answer

After DELETE removes all text content but leaves link crums in the `0.2.x` subspace, `retrievevspansetpm` returns **neither an empty specset, nor just the link subspace spans**. It returns:

> **A two-element specset: (1) a link span correctly representing the link subspace, plus (2) a broken text span derived from the uninitialized local variable `maxwid`.**

The decisive code path is:

| Step | Location | Effect |
|------|----------|--------|
| `is1story(ccptr->cwid.dsas[V])` → FALSE | `orglinks.c:184` | Link content's multi-level address forces `else` branch |
| `maxtextwid(...)` | `orglinks.c:207` | Traverses tree, skips all link crums, never writes `maxwid` |
| `maxwid` never initialized | `orglinks.c:176` | `vspan.width` is uninitialized stack data |
| `vspan.width.mantissa[0] = 0` | `orglinks.c:211` | Only the first mantissa slot is zeroed; others remain garbage |
| `putvspaninlist` × 2 | `orglinks.c:216–217` | Both the garbage text span and the valid link span are appended |

The third option — **a bounding span that incorrectly implies text content exists** — is the closest of the three offered answers: the text span has `stream=0` and a width with `mantissa[0]=0` but potentially non-zero garbage in `mantissa[1+]`, which, depending on stack contents, could encode a non-zero width and falsely imply text content at V-address 0. This is a defect in `retrievevspansetpm`: there is no guard or base case for the situation where `maxtextwid` finds nothing, and the accumulator tumbler is left uninitialized.

---

## Question 18 [gregory]

> When CREATENEWVERSION is called on a document that has had significant content DELETEd, does the version capture the current (post-delete) POOM state, and are the I-addresses of the deleted content permanently unreachable from the version's perspective even though they persist in the granfilade?

### Gregory's Answer

## KB Synthesis

Yes to both parts. Here is the synthesis:

---

## What CREATENEWVERSION Captures

CREATENEWVERSION reads the source document's **current POOM state** at call time. The call chain is:

`docreatenewversion` → `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm` → reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the root node → `docopyinternal` → `specset2ispanset` → `insertpm` + `insertspanf`

The critical step is `specset2ispanset`, which converts the *current* V-span of the source document to I-spans by walking the source's POOM. Since DELETE removes bottom crums from the POOM via `disown` + `subtreefree` [ST-DELETE, Finding 0064, 0072], those V-to-I mappings simply do not exist when `specset2ispanset` executes. The version therefore receives only the surviving content's I-address mappings. [ST-VERSION-CREATE, Finding 0032, 0046]

Additionally, CREATENEWVERSION copies only the text subspace (1.x V-positions) — the link subspace is excluded because `retrievedocumentpartofvspanpm` returns the displacement pointing to position 1. [ST-VERSION-CREATE, Finding 0043]

---

## Are Deleted I-Addresses Permanently Unreachable from the Version?

**From the version's POOM:** Yes, permanently. The version's POOM was built by copying only the post-delete V-to-I mappings. The version has no entries mapping any V-position to the deleted I-addresses. [INV-IADDR-IMMUTABILITY], [FC-GRANF-ON-DELETE]

**From the granfilade:** The I-addresses persist unconditionally. The granfilade is append-only — DELETE never touches it. [FC-GRANF-ON-DELETE, Finding 0061, 0064] The content bytes remain at those I-addresses indefinitely.

**From the spanfilade (DOCISPAN):** The version's `insertspanf` call only registers DOCISPAN entries for the surviving content's I-addresses. The deleted I-addresses are not registered under the version's ISA. The *source* document retains stale DOCISPAN entries for the deleted I-addresses [INV-SPANF-WRITE-ONLY], so `find_documents(deleted_iaddr)` would still return the source document (as a ghost reference [EC-STALE-SPANF-REFERENCE]) — but not the version.

**Practical consequence:** `compare_versions(version, other_doc)` cannot report shared content for the deleted material, because the version's POOM has no I-span entries to intersect against. The version has no path from V-space to those I-addresses. [SS-COMPARE-VERSIONS]

---

## The One Exception: Reconstitution via VCOPY

The deleted I-addresses are unreachable **from the version as-is**, but not permanently destroyed. If another document (e.g., the source document before deletion, or any transclusion of it) still has POOM entries for those I-addresses, a VCOPY from that document into the version would restore the V-to-I mappings and make those I-addresses reachable again — because VCOPY shares existing I-addresses rather than allocating new ones. [ST-COPY, Finding 0064], [INV-DELETE-NOT-INVERSE]

This is precisely why CREATENEWVERSION before editing is the only identity-preserving snapshot mechanism: a version created post-delete cannot reconstruct pre-delete identity. [ST-VERSION-CREATE, Finding 0072]

---

## Code Exploration

I now have all the source data needed. Let me write the complete answer.

---

## Answer: CREATENEWVERSION After DELETE — POOM Snapshot and Granfilade Persistence

### Short Answer

**Yes** — CREATENEWVERSION captures the current post-delete POOM state. The new version's POOM contains only V→I mappings for content that survived the deletion. The deleted content's I-addresses remain orphaned in the granfilade, permanently unreachable from the new version (or from the original document itself) through any normal operation.

---

### 1. What DELETE Does to the POOM

**Call chain:**

`fns.c:333` `deletevspan()` → `do1.c:158` `dodeletevspan()` → `orglinks.c:145` `deletevspanpm()` → `edit.c:31` `deletend()`

```c
// orglinks.c:145-152
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend()` [edit.c:31-76] places "knives" at the region boundaries, splits any straddling crums, then iterates over the POOM children and applies two cases:

```c
// edit.c:58-64
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);   // ← physically frees POOM crum
    break;
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    // ← shifts right-side crums' displacement left (closes the V-gap)
    break;
```

- **Case 1**: Any POOM crum that lies entirely within the deleted V-range is `disown()`ed and `subtreefree()`d — permanently removed from the enfilade tree and freed from memory. The V→I mapping it encoded is gone.
- **Case 2**: Crums to the right of the deleted region have their V-displacement reduced by `width`, closing the gap.

After the loop, `setwispupwards(father, 1)` [edit.c:74] propagates corrected aggregate widths up to the apex crum.

**Critical observation:** `deletend()` operates only on `docorgl` — the document's POOM enfilade. It never touches `granf`. There is no `deletend()` or `subtreefree()` call on the granfilade during a delete. The actual content bytes and their I-addresses in the granfilade are entirely untouched.

---

### 2. What CREATENEWVERSION Reads From the Post-Delete POOM

**Call chain:**

`fns.c:289` `createnewversion()` → `do1.c:260` `docreatenewversion()`

```c
// do1.c:260-299
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    typevspan vspan;
    typevspec vspec;
    ...
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) ...  // new empty POOM
    if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) ...      // read source V-span
    
    vspec.docisa = *isaptr;          // line 287: source doc ISA
    vspec.vspanset = &vspan;         // current (post-delete) V-span
    
    addtoopen(newisaptr, user, TRUE, WRITEBERT);
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);     // copy into new version
    logbertmodified(newisaptr, user);
    doclose(taskptr, newisaptr, user);
    return (TRUE);
}
```

`doretrievedocvspanfoo` [do1.c:301-309] calls `retrievedocumentpartofvspanpm`:

```c
// orglinks.c:155-162
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // apex displacement
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);   // apex width
    return (TRUE);
}
```

This reads the apex crum's `cwid.dsas[V]` directly. After `deletend()` + `setwispupwards()`, this width reflects the **current post-delete V-extent** — the deleted V-range has been subtracted. So `vspan` describes only the surviving content's V-space.

---

### 3. How V→I Translation Excludes Deleted Content

`docopyinternal` [do1.c:66-82] is the workhorse. It calls `specset2ispanset` [do2.c:14-46]:

```c
// do2.c:34-38
if (!(
  findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)))){
       return (FALSE);
}
```

This finds the **original document's** orgl (the post-delete POOM), then calls `vspanset2ispanset` [orglinks.c:397-402]:

```c
// orglinks.c:397-402
typeispanset *vspanset2ispanset(..., typeorgl orgl, typevspanset vspanptr, ...)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-453] → `retrieverestricted()` — which traverses the POOM enfilade looking for crums that overlap the given V-span restriction, collecting their corresponding I-coordinates.

**The key**: because `deletend()` physically removed the POOM crums encoding the deleted V→I mappings, `retrieverestricted()` finds no crums in those V-ranges. No I-spans are produced for the deleted content. Only the surviving crums — with their shifted V-displacements — yield I-spans.

`insertpm` [orglinks.c:75-134] then writes those I-spans into the new version's POOM, at the surviving V-addresses. The new version's POOM is a faithful copy of the post-delete POOM of the source.

---

### 4. Granfilade Persistence of Deleted I-Addresses

When `inserttextgr` [granf2.c:83-109] originally inserted text, it allocated a permanent I-address in the granfilade and stored the bytes there:

```c
// granf2.c:83-109
bool inserttextgr(..., typetextset textset, typeispanset *ispansetptr)
{
    findisatoinsertgr (..., &lsa);   // find I-address to insert at
    movetumbler (&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        locinfo.infotype = GRANTEXT;
        locinfo.granstuff.textstuff.textlength = textset->length;
        movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);  // put in granfilade
        tumblerincrement (&lsa, 0, textset->length, &lsa);
    }
    // record ispanset of the allocated I-range
}
```

These granfilade crums hold the content permanently. Nothing in the delete path removes them. After deletion:

- The **POOM** (document enfilade) no longer contains crums encoding V→I mappings for the deleted V-range.
- The **granfilade** still contains the GRANTEXT crums for those I-addresses.
- No document — including the new version — has a POOM crum pointing to those I-addresses.
- `ispan2vstuffset` [granf2.c:286-318], the only other way to access granfilade content, takes an I-span and retrieves text; but without a POOM to map V→I, no client operation naturally produces those I-spans.

The deleted content is **orphaned**: its I-addresses are permanently allocated and occupy storage in the granfilade, but are semantically invisible — unreachable through any document's V→I lookup chain.

---

### Summary Table

| Question | Answer | Key Lines |
|---|---|---|
| Does CREATENEWVERSION snapshot post-delete state? | **Yes** — reads apex `cwid.dsas[V]` which was updated by `setwispupwards` after delete | `orglinks.c:159-160`, `edit.c:74` |
| Are deleted V→I mappings in the new version's POOM? | **No** — `retrieverestricted` finds no POOM crums for freed V-ranges | `edit.c:59-61`, `orglinks.c:435` |
| Does deleted content persist in the granfilade? | **Yes** — `deletend` touches only POOM, never `granf` | `edit.c:31-76`, `orglinks.c:149` |
| Are the orphaned I-addresses reachable from the new version? | **No** — no POOM crum in either original or new version maps to them | `do2.c:34-38`, `orglinks.c:404` |
| Are the orphaned I-addresses reachable from the *original* document? | **No** — the source document's POOM also had those crums freed | `edit.c:59-61` |

### Implication

The architecture makes DELETE semantically permanent from a document perspective, even though the granfilade is structurally append-only. The POOM is the sole indexing structure for V→I navigation; once a POOM crum is `subtreefree()`d, its content becomes granfilade dark matter — present in storage, indexed by a permanent I-address, but unreachable through any versioned document view. CREATENEWVERSION faithfully inherits this darkness: it copies the current (reduced) POOM state, not any historical snapshot.

---

## Question 19 [gregory]

> If content at I-address range `[.0.1.1, .0.1.5]` is DELETEd from document A, then later a COPY transcludes those same I-addresses from document B (which still holds them) back into document A, does `find_links` rediscover links whose endsets reference that I-address range, and does document A's stale DOCISPAN entry in the spanfilade coexist with the new DOCISPAN entry from the re-transclusion?

### Gregory's Answer

## KB Synthesis

## After DELETE + Re-transclusion COPY

### Part 1: `find_links` Rediscovery

**Yes — links are fully rediscovered after the COPY.**

The key is that DELETE never touched either the link index (spanfilade) or the link orgls themselves [FC-LINK-DELETE-ISOLATION], [INV-SPANF-WRITE-ONLY]. The link endset entries mapping `[.0.1.1, .0.1.5]` → link ISAs were written when the links were created and persist unconditionally — the spanfilade is append-only.

The intermediate state after DELETE but before COPY: `find_links` on doc A would *not* find those links, because `find_links` converts a V-specset to I-addresses via the POOM before searching the spanfilade [INT-SPORGL-LINK-INDEX]. With the V→I mappings deleted from doc A's POOM, the conversion yields nothing — there are no V-positions in doc A that resolve to those I-addresses.

After COPY re-transcludes from doc B: `docopy` calls both `insertpm` (restores V→I mappings in doc A's POOM) and `insertspanf(..., DOCISPAN)` [ST-COPY], [ST-INSERT]. Doc A's POOM once again maps V-positions to `[.0.1.1, .0.1.5]`. Now `find_links` with a query covering those V-positions converts them to the I-addresses, intersects against the still-intact link index, and returns the links. Discovery is fully restored.

This follows from [FC-LINK-PERSISTENCE]: links exist independently of any document's POOM state. [INT-TRANSCLUSION-LINK-SEARCH] confirms: transclusion restores discoverability because it restores I-address presence in the POOM.

---

### Part 2: DOCISPAN Coexistence

**Yes — both DOCISPAN entries coexist.**

The spanfilade is strictly write-only [INV-SPANF-WRITE-ONLY]. DELETE calls only `deletend` on the POOM and never touches the spanfilade [ST-DELETE], [INT-DELETE-SPANF-DIVERGENCE]. The original DOCISPAN entry `[.0.1.1, .0.1.5]` → doc A survives as a stale reference.

When COPY re-transcludes from doc B, `insertspanf(..., DOCISPAN)` inserts a new entry via `insertnd` [SS-DOCISPAN]. There is no deduplication check — `isanextensionnd` checks contiguity, not existence [PRE-COPY]. The result: the spanfilade contains (at minimum) two entries:

- **Stale entry** (pre-DELETE): `[.0.1.1, .0.1.5]` → doc A
- **Fresh entry** (post-COPY): `[.0.1.1, .0.1.5]` → doc A

This is non-pathological. As [EC-STALE-SPANF-REFERENCE] documents, `find_documents` returns a *superset* of documents with live POOM mappings: `actual_docs(i) ⊆ find_documents(i)`. Duplicate entries may cause doc A to appear twice in raw results, but [INV-ITOV-FILTERING] handles the rest — I-to-V conversion at query time filters through the current POOM state, so only live V-positions are returned regardless of how many spanfilade entries point there.

---

### Summary

| Layer | After DELETE | After COPY from B |
|-------|-------------|-------------------|
| Doc A POOM | I-addresses removed | I-addresses restored (at new V-positions) |
| Spanfilade DOCISPAN | Stale entry persists | Stale + fresh entry coexist |
| Link index (LINKFROMSPAN etc.) | Unchanged | Unchanged |
| `find_links` on doc A | Not found (V→I fails) | **Rediscovered** (V→I restored) |

---

## Code Exploration

Now I have everything I need. Here is the complete, cited answer.

---

## Full Answer: DELETE + re-COPY, link rediscovery, and DOCISPAN coexistence

### Background: Two separate data structures

The backend maintains two independent persistent structures:

- **Permutation matrix** (`granf`, per-document orgl): the V→I address mapping. It is mutable — content can be inserted and deleted.
- **Spanfilade** (`spanf`): a global, write-only append index of which I-spans live in which documents, and which I-spans are link endpoints. Nothing is ever deleted from it.

---

### The DELETE path touches only the permutation matrix

`dodeletevspan` [do1.c:158–167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

`deletevspanpm` [orglinks.c:145–152]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` operates on `docorgl`, which is the document's permutation matrix node found via `granf`. The global `spanf` (spanfilade) is never referenced. There is no call to anything touching `spanf` anywhere in the delete chain. The spanfilade receives no write of any kind during a DELETE.

---

### The COPY path writes to BOTH structures

`docopy` [do1.c:45–65]:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  ...
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && asserttreeisok(docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)    // line 60 — writes permutation matrix
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) // line 62 — writes spanfilade
    && asserttreeisok(docorgl));
}
```

`insertspanf` [spanf1.c:15–54] appends a new leaf crum to the spanfilade:

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]); // line 22 — key prefix
    ...
    movetumbler (isaptr, &linfo.homedoc);          // line 29 — stamps home document
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); // line 51
}
```

`insertnd` appends a new leaf. **There is no counterpart `deletend` on the spanfilade anywhere in the codebase.** The spanfilade is write-only.

---

### Question 2: Do the stale and new DOCISPAN entries coexist?

**Yes, unconditionally.**

Timeline:
1. **Original COPY/INSERT of I-range `[.0.1.1, .0.1.5]` into doc A** → `insertspanf(..., DOCISPAN)` writes leaf crum L1 to spanfilade.
2. **DELETE of that range from doc A** → `deletend` on doc A's permutation matrix only. L1 remains in spanfilade, untouched.
3. **Re-COPY of same I-range from doc B into doc A** → `insertspanf(..., DOCISPAN)` writes a second leaf crum L2 to spanfilade.

Both L1 and L2 are now leaf crums in the enfilade tree rooted at `spanf`. The enfilade is never pruned. Both crums carry the same I-address range in their `SPANRANGE` dimension and doc A's ISA in their `ORGLRANGE` dimension (prefix) and `linfo.homedoc` field.

---

### Question 1: Does `find_links` rediscover links referencing that I-range?

**Yes, unconditionally.**

Link endpoints are stored in the spanfilade via `insertendsetsinspanf` [do2.c:116–128], called from `docreatelink` [do1.c:219]:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
                           typesporglset fromsporglset, typesporglset tosporglset,
                           typesporglset threesporglset)
{
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
    && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
    [optional LINKTHREESPAN]
}
```

These `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` crums are permanent spanfilade entries. DELETE never removes them.

The link search path is:

`dofindlinksfromtothree` [do1.c:348–353] → `findlinksfromtothreesp` [spanf1.c:56–103]:

```c
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr, ...)
{
    ...
    if (fromvspecset)
        sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN); // line 77
    if (tovspecset)
        sporglset2linkset (taskptr, (typecuc*)spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);       // line 85
    ...
    intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr); // line 100
}
```

`sporglset2linkset` queries the spanfilade for crums whose `SPANRANGE` intersects the query I-addresses and whose `ORGLRANGE` prefix matches the appropriate span type (`LINKFROMSPAN`, etc.). Since those crums were never deleted, they are found. Document A's permutation matrix state is irrelevant to this search.

---

### The home-document filter is structurally disabled in spanfilade queries

`crumqualifies2d` [retrie.c:270–280] has a filter for home document:

```c
if ((crumptr->height == 0) && infoptr &&
    !tumblereq (&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

But `findcbcinarea2d` [retrie.c:229–251] treats a non-NULL `infoptr` as a fatal error:

```c
if(infoptr){
    fprintf(stderr,"not NULL infoptr ... shouldent happen...\n");
    gerror("findcbcinarea2d");
}
```

And all spanfilade calls pass `(typeisa*)NULL` as the `docisaptr` parameter — see for example `finddocscontainingsp` [spanf1.c:171]:

```c
context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
```

Which propagates through `retrieverestricted` [retrie.c:77–82]:

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;  // always taken for spanfilade queries
}
```

So `infoptr` is always `NULL` in spanfilade traversals, the home-document guard in `crumqualifies2d` never fires, and **both the stale L1 and the new L2 DOCISPAN crums — and all link endpoint crums — are returned by any I-address range query regardless of which document they nominally belong to.**

---

### Summary

| Operation | Permutation matrix (`granf/docorgl`) | Spanfilade (`spanf`) |
|-----------|--------------------------------------|----------------------|
| Original COPY/INSERT of `[.0.1.1, .0.1.5]` into doc A | Written (V→I mapping) | DOCISPAN crum L1 written permanently |
| DELETE of that range from doc A | `deletend` removes V→I entries | **Untouched** |
| Re-COPY of same I-range from doc B into doc A | Written again (new V→I mapping) | DOCISPAN crum L2 written permanently |
| `find_links` query on `[.0.1.1, .0.1.5]` | Not consulted | Finds all `LINKFROMSPAN`/`LINKTOSPAN` crums (permanent); rediscovers all links |

**Both DOCISPAN entries (L1 stale, L2 new) coexist permanently** in the spanfilade enfilade tree with no mechanism to distinguish or evict the stale one. **`find_links` fully rediscovers any link** whose endpoint I-addresses overlap `[.0.1.1, .0.1.5]`, because link records are written once to the spanfilade and never deleted, and the spanfilade search ignores document permutation matrix state entirely.

---

## Question 20 [gregory]

> When `deletend` constructs knives via `makecutsbackuptohere` for a DELETE spanning multiple bottom crums, are the intermediate crums (those entirely consumed by the delete range) freed in a single pass through `disownnd`, or does each one require a separate tree traversal to locate and remove?

### Gregory's Answer

## KB Synthesis

The KB does not provide enough low-level detail about `deletend`'s internal loop structure to answer definitively, but what it does say strongly implies a **single traversal pass**.

## What the KB establishes

**[ST-DELETE Finding 0075]** describes a two-phase structure:

- **Phase 1** (cutting): `makecutsbackuptohere()` runs only at boundaries where a cut falls strictly interior to a crum (`whereoncrum() == THRUME`). At boundaries that align exactly with crum edges, no cut is made.
- **Phase 2** (classify and remove/shift): each crum encountered during traversal is classified into cases — Case 1 (entirely within deletion range) triggers `disown` + `subtreefree`.

**[ST-DELETE Finding 0064]** confirms the inline case-dispatch model:

> nodes falling entirely within the deletion range are `disown`ed (removed from parent/sibling pointers) and then `subtreefree`d

This language describes per-crum action during traversal, not a collect-then-free two-pass pattern.

**[ST-DELETE Finding 0058]** shows that `setwispupwards` and `recombine` are called **once** on the father node *after* the removal loop — consistent with a single traversal that handles all consumed crums inline, then rebalances.

## Conclusion

The KB supports a **single traversal**: as `deletend` descends and walks the tree, each bottom crum classified as Case 1 (entirely within the deletion range) is immediately `disown`ed and `subtreefree`d as the traversal encounters it. No separate re-traversal per consumed crum is described or implied. After all crums are processed in this single pass, `setwispupwards` and `recombine` restore tree invariants once.

The KB does not contain the actual `deletend` loop code at sufficient granularity to prove this unambiguously — it would require reading `edit.c:31-76` directly. What is documented is consistent with single-pass inline processing; nothing in the findings describes a multi-pass or per-crum separate-traversal pattern.

---

## Code Exploration

---

## Answer: Intermediate Crum Removal in `deletend`

The question has two distinct sub-parts: (1) how `makecutsbackuptohere` constructs the knives, and (2) how intermediate crums are freed. Here is a precise account based on source.

---

### Phase 1: Knife Construction via `makecutsbackuptohere`

`deletend` [edit.c:44] calls `makecutsnd(fullcrumptr, &knives)`:

```c
// edit.c:40-44
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
knives.nblades = 2;
knives.dimension = index;
makecutsnd (fullcrumptr, &knives);
```

`makecutsnd` [ndcuts.c:15-31] calls `makecutsdownnd`, which descends and then calls `makecutsbackuptohere` [ndcuts.c:54]:

```c
// ndcuts.c:33-67
int makecutsdownnd(typecuc *fullcrumptr, typewid *offset, typeknives *knives) {
    ...
    makecutsbackuptohere(ptr, offset, knives);
    if (toomanysons(ptr)) { levelpush(ptr); makecutsnd(...); }
}
```

Inside `makecutsbackuptohere` [ndcuts.c:69-140], **at height == 0** (bottom crums), each knife that passes through (`THRUME`) the crum causes a split:

```c
// ndcuts.c:77-91
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum(...) == THRUME) {
            new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
            ivemodified((typecorecrum*)ptr);
            ivemodified((typecorecrum*)new);
        }
    }
    return(0);
}
```

`slicecbcpm` [ndcuts.c:373-450] cuts the bottom crum in two and calls:

```c
// ndcuts.c:448
adopt(new, RIGHTBRO, ptr);
```

So the new half is inserted as a right brother inline — no tree traversal, just a pointer splice. Both knives are processed in **one pass** through the `for (i = 0; i < knives->nblades; i++)` loop at the bottom level.

At height > 0, `makecutsbackuptohere` [ndcuts.c:92-116] calls `cutsons` → `makecutsbackuptohere` recursively downward into children, then may call `peelsoncorrectly` to reorganize. The outer `makecutsnd` loop [ndcuts.c:24-27] re-runs `makecutsdownnd` from the fullcrum until `sonsarecut` returns false.

---

### Phase 2: Finding the "Father"

`deletend` [edit.c:45] calls `newfindintersectionnd`:

```c
// ndinters.c:38-42
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives, typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;
    clear (offset, sizeof(*offset));
}
```

**This is a stub.** The old `findintersectionnd` (commented out at ndinters.c:18-37) would have descended the tree to find the narrowest common ancestor of both cut points. The live `new` version unconditionally sets `father = fullcrumptr` — the root. The offset is zeroed. This means the subsequent loop always operates over the **direct children of the root**.

---

### Phase 3: The Deletion Loop — One Pass, Not Per-Crum Tree Traversals

`deletend` [edit.c:47-73]:

```c
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    next = (typecuc *) findrightbro((typecorecrum*)ptr);   // save next BEFORE modifying
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 1:
        disown ((typecorecrum*)ptr);
        subtreefree ((typecorecrum*)ptr);
        break;
      case 2:
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
        break;
    }
}
```

The `deletecutsectionnd` classifier [edit.c:235-248] works by iterating knives right-to-left, returning `i+1` for the first knife to the right of the crum:
- **0**: crum is to the left of knife 0 (before the delete range — left alone)
- **1**: crum is between knife 0 and knife 1 (inside the delete range — deleted)
- **2**: crum is to the right of knife 1 (after the delete range — displacement adjusted)
- **−1**: a knife passes through the crum (shouldn't happen after `makecutsnd` has split all such crums)

The loop makes **one left-to-right pass** through all direct children of `father` (the fullcrum). `next` is saved at [edit.c:48] before the switch, so the sibling chain is not corrupted when an intermediate crum is unlinked.

---

### What `disown` Actually Does

For each case-1 (intermediate) crum, `disown` is called [genf.c:349-371]:

```c
// genf.c:349-371
int disown(typecorecrum *crumptr) {
    typecuc *father;
    if (!(father = weakfindfather(crumptr))) { gerror(...) }
    disownnomodify(crumptr);
    ivemodified((typecorecrum*)father);
}
```

`weakfindfather` [genf.c:120-138]:

```c
typecuc *functionweakfindfather(typecorecrum *ptr) {
    ...
    for (; ptr && !ptr->isleftmost; ptr = ptr->leftbroorfather)
        ;
    if (ptr) {
        return ((typecuc *)ptr->leftbroorfather);
    }
    ...
}
```

This walks **laterally leftward** through the `leftbroorfather` chain until it finds a crum where `isleftmost == TRUE`, then follows one upward pointer. This is **not a tree traversal from the root** — it is a linked-list walk within a single level. Its cost is O(left siblings), bounded by the fan-out of the parent, not by tree depth or size.

`disownnomodify` [genf.c:373-413] then performs pure pointer surgery:

```c
// genf.c:394-411
right = findrightbro(crumptr);
father->numberofsons -= 1;
if (crumptr->isleftmost) {
    father->leftson = right;
    if (right) { right->leftbroorfather = (typecorecrum *)father; right->isleftmost = TRUE; }
} else {
    left = findleftbro(crumptr);
    left->rightbro = right;
    if (right) { right->leftbroorfather = left; }
}
```

After disowning the leftmost crum, `right->isleftmost` is set to `TRUE` and `right->leftbroorfather = father`. This means the next intermediate crum in the iteration becomes the leftmost child, so the next `weakfindfather` call returns `father` in O(1). For non-leftmost intermediates, `weakfindfather` must walk leftward past any surviving case-0 crums, but still never ascending above the father level.

---

### `subtreefree` for Intermediate Crums with Children

`subtreefree` [credel.c:413-432]:

```c
// credel.c:412-432  (comment: "assumes crum is disowned")
void subtreefree(typecorecrum *ptr) {
    if (ptr->height > 0) {
        for (p = ((typecuc *)ptr)->leftson; p; p = right) {
            right = p->rightbro;
            disown (p);
            subtreefree (p);
        }
    } else if (...GRAN/ORGL...) {
        orglfree(...);
    }
    freecrum(ptr);
}
```

For intermediate crums with height > 0, `subtreefree` recurses into the subtree. It uses `p->rightbro` [credel.c:425] to advance — it does **not** restart from the root. Each recursive level does one pass through that crum's children. This recursive descent is within the subtree of the already-located intermediate crum; it is not a new search from the root.

---

### Conclusion

**The intermediate crums are freed in a single linear pass, not via separate tree traversals.**

1. **Knife construction** (`makecutsbackuptohere`): both blades are handled in one descent. Bottom crums are split inline via `slicecbcpm`/`adopt`; no per-blade tree traversal.

2. **Intersection** (`newfindintersectionnd`): the live version is a stub that unconditionally returns `father = fullcrumptr` (the root) [ndinters.c:38-42]. This flattens the problem: the deletion loop always operates at the first level below the root.

3. **Deletion loop** (`deletend` [edit.c:47-73]): one left-to-right sweep through the children of `father`. Intermediate crums (case 1) are removed inline as they are encountered. The loop pre-fetches `next` [edit.c:48] before any modification, so no restart is needed.

4. **`disown`** [genf.c:349-371]: uses `weakfindfather` [genf.c:120-138] which is a **lateral leftward chain walk** to find the parent pointer — not a root-to-leaf tree search. After the leftmost child is disowned, its successor inherits `isleftmost = TRUE`, keeping subsequent `weakfindfather` calls O(1) for the initial crums in the sweep.

5. **`subtreefree`** [credel.c:413-432]: for intermediate crums with height > 0, recursively descends into the subtree. This descent is within the already-located subtree, not a new search from the root. It iterates via `p->rightbro` without restarting.

The design is: `makecutsnd` pre-splits the enfilade so that every intermediate crum at the level below `father` is a clean, whole-crum deletion target; then `deletend`'s loop sweeps once through those children, removing each in place.
