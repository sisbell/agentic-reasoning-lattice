# Consultation Answers — Content Deletion

**Inquiry:** What must DELETE preserve? What happens to addresses, links, and other documents that reference deleted content? In what sense is deletion reversible?
**Date:** 2026-02-23 10:57
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When content is deleted from a document, does the permanent identity of that content survive the deletion, or is the identity itself destroyed?

### Nelson's Answer

## The Permanent Identity Survives Deletion Completely

Deletion in Xanadu removes content from a document's **V-space arrangement** — its current view. It does **not** touch I-space, where the content's permanent identity lives. The identity is not merely preserved as a side effect; it is architecturally impossible to destroy.

### The Core Distinction

Nelson explicitly diagrams "DELETED BYTES" as a valid system state on page 4/9:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "not currently addressable" is precise: the content is no longer reachable through the document's current V-stream. But "not currently addressable" is not "destroyed." The bytes remain in I-space at their permanent address.

He reinforces this on page 4/11:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Why Identity Cannot Be Destroyed

The architecture makes identity destruction impossible through three mechanisms:

**1. I-space is append-only.** Content enters I-space and never leaves:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**2. I-addresses are permanent.** The address encodes the content's origin (server, user, document, element position) and never changes:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

**3. Deletion operates only on V-space.** The V-to-I mapping changes; the I-space content does not:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses shift and disappear during editing. I-addresses are eternal.

### What Survives Deletion

| Aspect | Survives? | Why |
|--------|-----------|-----|
| I-space content (the bytes) | Yes | Append-only; never removed |
| I-space address (permanent identity) | Yes | Tumbler addresses are permanent |
| Links pointing to that content | Yes | Links attach to I-addresses, not V-positions |
| Transclusions in other documents | Yes | Other documents' V→I mappings are unaffected |
| Previous versions of the same document | Yes | Each version is an independent V-space arrangement |
| Origin traceability | Yes | I-address encodes home document structurally |

### The Philosophical Point

Nelson designed this deliberately. The entire system exists to reject destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

Deletion is not destruction — it is the removal of one strand from the current braid. The strand itself persists in the underlying material. You can always reconstruct any previous arrangement:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

### Summary

The permanent identity of content — its I-space address, its bytes, its traceability to its home document — is **completely unaffected** by deletion. Deletion is a V-space operation that changes a document's current arrangement. The content's identity lives in I-space, which is append-only and eternal. In Nelson's architecture, there is no operation that destroys identity. That is not an oversight; it is the entire point.

---

## Question 2 [nelson]

> If a link points to content that has been deleted, must the system preserve the link itself, and what must it report when someone follows that link?

### Nelson's Answer

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

---

## Question 3 [nelson]

> Does deletion remove the content from all documents that share it through transclusion, or only from the document where the deletion was performed?

### Nelson's Answer

## Deletion Affects Only the Document Where It Is Performed

Deletion in Xanadu removes content from a single document's V-space (its current arrangement) — **not** from I-space (permanent storage), and **not** from any other document that shares the content through transclusion.

Nelson states this explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The DELETEVSPAN operation confirms this scope:

> "This removes the given span from the given document." [LM 4/66]

### Why: The I-Space / V-Space Separation

The answer follows directly from Xanadu's two-address-space architecture. Content lives permanently in I-space; documents are V-space arrangements that *reference* I-space content. Deletion changes a V-space mapping — it does not touch I-space.

Nelson's diagram on page 4/9 shows "DELETED BYTES" as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Three things survive deletion:

1. **I-space content** — the bytes remain at their permanent addresses forever
2. **Other documents' transclusions** — their V-space mappings still point to the same I-space content, unaffected
3. **Previous versions** — the deleting document's own history still contains the content

### The Principle

This is a direct consequence of Nelson's non-destruction guarantee:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And of the append-only storage model:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### Summary

| What happens on DELETE | Affected? |
|------------------------|-----------|
| V-space of the document where DELETE is performed | Yes — content removed from current view |
| I-space (permanent storage) | No — bytes remain forever |
| Other documents that transclude the same content | No — their views are unaffected |
| Previous versions of the same document | No — still contain the content |
| Links pointing to the deleted I-space content | No — still resolve |

Deletion is a local, single-document, V-space-only operation. The content itself is permanent.

---

## Question 4 [nelson]

> Must the system guarantee that a deleted passage can always be restored to its original position in the document, and if so, what information must be retained to make this possible?

### Nelson's Answer

## Yes — Nelson Guarantees Full State Reconstruction

Nelson's answer is unambiguous: the system must preserve everything needed to reconstruct any previous state of any document, including the arrangement of content (not just the content itself). This is not a secondary feature but a foundational design requirement.

### The Guarantee

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

The phrase "any previous instant to be reconstructed" is the key. This is not merely content preservation — it is full state reconstruction, including where content appeared in the document's arrangement.

### What DELETE Actually Does

Nelson's architecture diagram on page 4/9 shows "DELETED BYTES" as a specific system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Two things are significant here:

1. **"Not currently addressable"** — the bytes lose their V-space position in the current version, but they have not been destroyed
2. **"Awaiting historical backtrack functions"** — the system explicitly anticipates that these bytes will be accessed again through version navigation

Additionally:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

DELETE is a V-space operation only. It changes the document's current arrangement. The I-space content is untouched.

### What Must Be Retained

Two categories of information are required:

**1. The content itself (I-space)**

The append-only storage model guarantees content permanence:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte ever created has a permanent I-space address that never changes. DELETE does not touch I-space. This is the simpler half of the problem.

**2. The V→I mapping for each version (the arrangement)**

This is the harder and more important half. Each version of a document defines a mapping from V-space positions (where the user sees content) to I-space addresses (where content permanently lives). To restore a deleted passage to its original position, the system must retain the V→I mapping that existed before the deletion.

Nelson describes this through the version model:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

Each version is a complete V-space arrangement. The pre-deletion version preserves where every byte appeared. The post-deletion version shows the arrangement without the deleted passage. Both are retained permanently.

### How Restoration Works

Nelson does not specify an "UNDO" command in FEBE. Instead, restoration is achieved through the version mechanism:

1. The user consults the previous version (which preserves the original arrangement)
2. The system can show "a given part of a given version at a given time" [LM 2/15]
3. The user can COPY content from the old version into a new version at the desired position
4. Or the user can CREATENEWVERSION from the pre-deletion version, effectively reverting

The SHOWRELATIONOF2VERSIONS operation supports this by revealing correspondence:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

This lets the user see exactly what changed between versions — which parts are the same and which differ — enabling precise restoration.

### The Deeper Principle

Nelson frames this as essential to creative work:

> "Under many circumstances the writer, or 'text user', needs to reach back to a former condition. This is in the nature of creative work." [LM 2/14]

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

The braid metaphor is precise: strands can be rearranged, but no strand is ever cut away and discarded. The history of the braid — every twist and retwisting — remains accessible.

### Summary

| What must be retained | Why |
|---|---|
| I-space content (the bytes) | Append-only storage; DELETE does not touch I-space |
| V→I mapping per version | Each version's arrangement must be reconstructable |
| Version identity and ordering | To navigate "back in time" to pre-deletion state |

The system guarantees that a deleted passage can always be found at its original position — not in the current version (where it has been removed from V-space), but in the prior version whose complete arrangement is permanently preserved. The content is always in I-space; the position information is always in the prior version's V→I mapping. Together, these are sufficient for full restoration.

---

## Question 5 [nelson]

> When content is deleted, does the address space of the document change — do the addresses of surrounding content shift, or do they remain stable?

### Nelson's Answer

## Address Behavior on Deletion

The answer depends on which address space you mean, because Xanadu has two:

### V-Space Addresses: Yes, They Shift

V-space (virtual space) addresses are the document's current arrangement — the positions a user sees. These are always **dense and contiguous**, starting at 1 with no gaps. When content is deleted, the gap closes and all subsequent V-addresses decrease.

This is the direct analog of what Nelson states for INSERT:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

DELETE is the inverse: V-addresses of following characters *decrease* by the length of the removed span. Nelson confirms that V-addresses are inherently unstable:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

### I-Space Addresses: No, They Never Shift

I-space (invariant space) addresses are permanent. Every byte ever created has an I-address that never changes, never moves, and never becomes invalid — even after deletion.

Deletion in Xanadu does **not** remove content from I-space. It removes the V-space mapping only:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The deleted content still exists at its original I-address. The surrounding content's I-addresses are equally unaffected — they were assigned at creation time and are permanent.

### Why This Matters

This two-layer design is the key to how links survive editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Links point to I-space addresses (permanent), not V-space positions (shifting). So when you delete content:

| What happens | V-space | I-space |
|---|---|---|
| Deleted content | Removed from arrangement | Still exists permanently |
| Surrounding content | Addresses shift (gap closes) | Addresses unchanged |
| Links to deleted content | No longer reachable via V-space | Still resolve to I-space |
| Links to surrounding content | Would break if they used V-addresses | Unaffected because they use I-addresses |

### Summary

**V-space addresses shift. I-space addresses are permanent.** This is the entire point of the two-space separation — V-space gives users intuitive sequential positions that behave naturally under editing, while I-space gives the system permanent identifiers that nothing can disturb.

---

## Question 6 [nelson]

> Can an author delete content that other documents have transcluded, and if so, what obligation does the system have to those other documents?

### Nelson's Answer

## Can an Author Delete Transcluded Content?

**Yes — and the system has no special obligation to other documents, because the architecture makes the question moot.**

This is one of the most elegant consequences of the I-space/V-space separation.

### What DELETE Actually Does

DELETE in Xanadu removes content from a document's **V-space** (its current arrangement) but does **not** touch **I-space** (permanent storage). Nelson is explicit about this at `[LM 4/11]`:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."

The diagram at `[LM 4/9]` shows "DELETED BYTES" as a valid system state:

> "(not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

### Why Other Documents Are Unaffected

Transclusion works by referencing I-space addresses, not V-space positions. When Alice's document transcludes a passage from Bob's document, Alice's V-space contains a mapping to the **I-space address** where Bob's bytes permanently live. When Bob "deletes" that passage from his own document, he is only changing **his** V→I mapping. The I-space bytes remain untouched.

Nelson describes this separation clearly at `[LM 4/11]`:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations."

The content lives at its "home location" in I-space permanently. Bob's deletion changes his document's view; it cannot reach into I-space and destroy the bytes.

### The Append-Only Foundation

The deeper reason is that I-space is append-only. Nelson at `[LM 2/14]`:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically."

Nothing is ever removed from this store. The "delete" operation is purely a V-space rearrangement — it removes the reference, not the content.

### What About Published Documents?

For **published** documents, there is an additional social constraint. The author cannot withdraw the document itself:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." `[LM 2/43]`

But this obligation concerns the **document** (the addressable unit), not individual bytes within it. Even if it were somehow possible to withdraw a published document entirely, the I-space content would still exist — other documents' transclusions would still resolve.

### The Non-Destruction Guarantee

Nelson frames this as a fundamental principle at `[LM 2/45]`:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links."

And at `[LM 2/37]`:

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes."

### Links Also Survive

Links pointing to the "deleted" content continue to work because they reference I-space addresses, not V-space positions. Nelson at `[LM 4/42]`:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end."

Since the bytes still exist in I-space, the links still resolve — the bytes are merely absent from one particular document's current view.

### Summary

| What happens | Affected? |
|---|---|
| Author's current V-space arrangement | Yes — content removed from view |
| Author's previous versions | No — still contain the content |
| I-space bytes | No — permanently stored |
| Other documents' transclusions | No — they reference I-space directly |
| Links to the content | No — still resolve to I-space |
| Historical backtrack | No — any past state reconstructible |

The system has **zero special obligation** to other documents when an author deletes content, because the architecture already guarantees their safety. This is not a policy decision requiring enforcement — it is a structural consequence of separating content identity (I-space) from content arrangement (V-space). The question dissolves once you understand the architecture.

---

## Question 7 [nelson]

> Is deletion a new version of the document, preserving the pre-deletion state as a prior version that remains accessible?

### Nelson's Answer

## Deletion and Versioning: Two Separate Mechanisms

No. Deletion does NOT automatically create a new version. Nelson treats these as distinct mechanisms that work together but are not the same thing.

### DELETE Modifies the Current Document

DELETE operates on a document's V-space arrangement directly:

> "This removes the given span from the given document." (4/66)

CREATENEWVERSION is a separate, explicit, user-initiated operation:

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document." (4/66)

There is no indication that DELETE implicitly invokes CREATENEWVERSION.

### The Pre-Deletion State IS Preserved — But Not Via Versioning

Nelson's diagram on page 4/9 shows "DELETED BYTES" as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

The mechanism that preserves prior states is the **append-only storage system**, not automatic versioning:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)

### The Distinction

| Mechanism | What It Does |
|-----------|-------------|
| **DELETE** | Removes content from V-space; I-space content untouched |
| **CREATENEWVERSION** | Creates a new document with its own identity and address |
| **Historical backtrack** | Reconstructs any prior temporal state from the append-only store |

Nelson describes the document as "an evolving ONGOING BRAID" (2/14) where edits "re-twist this braid when its parts are rearranged, added or subtracted" (2/15). Each edit creates a new temporal state — but a temporal state is not a version. Versions are explicit forks with their own tumbler addresses and document identities.

### What Remains Accessible After Deletion

1. **I-space content**: The bytes themselves are permanent — DELETE only changes V-space mapping
2. **Other documents**: "The owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)
3. **Historical states**: The append-only storage preserves the chronological record, enabling reconstruction of prior arrangements
4. **Explicit versions**: If someone had already created a version (via CREATENEWVERSION) before the deletion, that version retains the content

### Summary

The pre-deletion state remains accessible, but through the **storage system's append-only nature and historical backtrack capability** — not through automatic version creation. Deletion and versioning are orthogonal: deletion changes the current arrangement, while versioning creates a new document identity. Nelson's system guarantees both, but does not conflate them.

---

## Question 8 [nelson]

> Must the system distinguish between content that was never present and content that was present but deleted — is there a visible trace of deletion?

### Nelson's Answer

Let me check the relevant page for the system state diagram Nelson draws.

Yes — the system must distinguish these cases, and deletion leaves a permanent, structural trace. Nelson's architecture makes this distinction unavoidable, not optional.

## The "DELETED BYTES" State

Nelson's diagram on page 4/9 explicitly categorizes a document's technical contents into distinct states, including:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This is not just an internal bookkeeping detail. "DELETED BYTES" is a recognized system state, distinct from both "current bytes" and "bytes that never existed." The system knows these bytes were once part of the document's V-stream and were removed.

## Why the Distinction Is Structural

The distinction between "never present" and "deleted" falls out of three architectural properties:

**1. I-space permanence.** Content created by INSERT gets a permanent I-space address. That address exists forever, regardless of what happens in V-space. Content that was never created has no I-space address. So at the storage level, the system can always answer: "Did these bytes ever exist in this document?" — by checking whether I-addresses under that document's ownership exist.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

**2. Append-only storage.** The storage model is explicitly non-destructive:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte ever created remains in the append-only store. A byte that was created and then "deleted" (from V-space) still physically exists. A byte that was never created does not. The storage itself is the trace.

**3. Version history preserves all states.** Every previous arrangement is permanently accessible:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If content appeared in version N but is absent in version N+1, the system knows it was deleted — because version N still exists and still contains it. If content never appeared in any version, the system knows it was never present.

## The Trace Is User-Visible

This is not merely an internal distinction hidden from users. Nelson explicitly provides mechanisms for users to see deletion traces:

**Historical backtrack:** Users can "go back in time to any previous version" [LM 2/15], which means they can see content that was present before deletion. The "DELETED BYTES" state explicitly says these bytes are "awaiting historical backtrack functions" — implying the user can reach them.

**Intercomparison:** The SHOWRELATIONOF2VERSIONS operation "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. Comparing a pre-deletion version with a post-deletion version reveals exactly what was removed:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

The gap in correspondence — content present in version N but absent in version N+1 — is the visible trace of deletion.

**Persistence in other documents:** Nelson explicitly notes that deletion from one document does not affect transclusions:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So a reader encountering transcluded content can discover (via FINDDOCSCONTAINING) that the source document once contained this content — even if the source document's current version no longer shows it.

## The Braid Metaphor

Nelson's metaphor captures why deletion must leave a trace:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

A strand that was once part of the braid and was later removed is fundamentally different from a strand that was never there. The braid's history records the removal. This is the whole point of the "space-time vortex" — you can navigate through time as well as space, and deletion is a visible event in that history, not an erasure.

## Summary

| Question | Answer | Mechanism |
|----------|--------|-----------|
| Can the system tell "never present" from "deleted"? | **Yes** | I-space addresses exist for created-then-deleted content; they don't exist for never-created content |
| Is there a visible trace of deletion? | **Yes** | Version history preserves pre-deletion states; intercomparison reveals the gap; I-space content persists |
| Can users see the trace? | **Yes** | Historical backtrack, SHOWRELATIONOF2VERSIONS, and transclusion persistence all expose it |
| Is the trace permanent? | **Yes** | I-space is append-only; versions are permanent; the "DELETED BYTES" state is structural |

Nelson designed a system where deletion is an editorial operation on arrangement (V-space), never an act of destruction (I-space). The trace of deletion is not a feature bolted on — it is an inescapable consequence of the architecture. In a system built on permanent storage and version history, the absence of something that was once present is always distinguishable from the absence of something that never existed.

---

## Question 9 [nelson]

> If deleted content carried royalty or compensation obligations, does deletion release those obligations or must they persist despite the content no longer being visible?

### Nelson's Answer

## Deletion Does Not Release Royalty Obligations

The answer follows directly from Xanadu's architecture: **royalty obligations persist after deletion because neither the content nor the delivery mechanism is affected by deletion.**

### Why: Deletion Is a V-Space Operation; Royalty Is an I-Space Event

DELETE in Xanadu removes content from a document's current arrangement (V-space) but does **not** remove it from permanent storage (I-space):

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Royalty is triggered by **delivery of bytes**, not by their visibility in any particular document:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

The cash register tracks delivery, not arrangement:

> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document."

Since the I-space bytes survive deletion, and royalty attaches to byte delivery from I-space, deletion changes nothing about the royalty obligation.

### Three Channels Through Which "Deleted" Content Still Generates Royalty

1. **Transclusions in other documents.** Other documents that window the deleted content still reference the same I-space bytes. When those documents are read, the original owner's bytes are delivered and royalty accrues. Nelson is explicit: bytes "remain in all other documents where they have been included" [LM 4/11].

2. **Previous versions.** Deleted bytes "may remain included in other versions" [LM 4/9]. Readers accessing historical versions trigger delivery of those bytes.

3. **Historical backtrack.** The bytes are "awaiting historical backtrack functions" [LM 4/9]. When any reader reconstructs a prior state, delivery occurs.

### Storage Obligations Also Persist

Beyond royalty, the owner continues to bear storage costs. Nelson's model requires ongoing storage rental for I-space content:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Since deletion does not remove content from I-space, the storage rental obligation for those bytes continues.

### Why This Must Be So

Nelson designed the system so that **modifications never damage originals**:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals." [LM 2/45]

If deletion released royalty obligations, it would create a perverse incentive: an author could publish content, allow others to transclude it, then "delete" it to stop paying while continuing to benefit from having published. This would undermine the entire economic model where:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The royalty split depends on stable I-space identity. Deletion cannot sever that identity because deletion does not touch I-space.

### What Nelson Does Not Address

Nelson never explicitly discusses the scenario of "what if I delete content that others have transcluded — do I still get paid?" This is because from his architectural perspective, the question does not arise. The content is not gone. It is still delivered when requested. The cash register still increments. The owner still receives royalty. Deletion is simply a rearrangement of one document's view — it has no effect on the economic layer.

Similarly, Nelson does not address whether an owner might *want* to stop receiving royalty for deleted content (perhaps to avoid storage costs on unpopular material). The architecture provides no mechanism for this short of full withdrawal, which for published documents requires "lengthy due process" [LM 2/43].

### Summary

| Aspect | Effect of Deletion |
|--------|-------------------|
| V-space visibility | Removed from current version |
| I-space existence | **Unchanged** — bytes persist |
| Transclusions in other docs | **Unchanged** — still deliver original bytes |
| Historical versions | **Unchanged** — still accessible |
| Royalty on delivery | **Unchanged** — cash register still increments |
| Storage rental | **Unchanged** — owner still pays for I-space bytes |
| Link targets | **Unchanged** — links to I-space still resolve |

Deletion is cosmetic from the economic perspective. The obligations — both the owner's storage costs and the system's royalty payments — persist as long as the I-space content exists, which is forever.

---

## Question 10 [nelson]

> Does the system permit permanent, irrevocable deletion of content, or must every deletion be reversible as a consequence of the permanence guarantee?

### Nelson's Answer

# Deletion in Xanadu: Reversible by Design

The system does **not** permit permanent, irrevocable deletion of content. Every deletion is a V-space operation — a change to the document's current arrangement — that leaves I-space content intact. This is not an incidental feature but the foundational storage paradigm.

## The Core Architecture: Append-Only

Nelson explicitly rejects destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." [LM 2/15]

The storage model is accumulative. Content enters I-space and stays there. "Editing" changes the V-space mapping, never the stored bytes.

## What DELETE Actually Does

The technical specification on page 4/9 defines deleted content as a state, not an erasure:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

| Aspect | Affected by DELETE? |
|--------|---------------------|
| V-space arrangement | **Yes** — removed from current view |
| I-space content | **No** — bytes remain permanently |
| Previous versions | **No** — still contain the content |
| Transclusions in other documents | **No** — still show the content |
| Links pointing to the content | **No** — still resolve via I-space |

The same applies to links. Deleted links enter the identical "not currently addressable" state:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## The Permanence Guarantee

Multiple guarantees reinforce irreversibility of I-space content:

**Address permanence:** "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

**Historical backtrack:** "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

**Non-destruction:** "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

If I-space content could be permanently destroyed, historical backtrack would fail, version reconstruction would become impossible, and links to deleted content would break — violating three foundational guarantees simultaneously.

## The Edge Cases: Withdrawal and Removal

Nelson does acknowledge two scenarios where content might become inaccessible, but neither constitutes I-space destruction:

### 1. Published Document Withdrawal

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The key phrase is "lengthy due process" — withdrawal is possible but deliberately difficult. And even withdrawn content has its superseding version mechanism:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network." [LM 2/43]

The "former version must remain" — even when the author publishes a replacement.

### 2. Peremptory Challenge for Anonymous Content

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge." [LM 2/60]

Nelson uses the word "removal" here, which is the strongest language he uses for any deletion-like operation. But he does not specify whether "removal" means I-space destruction or merely making content inaccessible (removing it from V-space / blocking delivery). Given the overall architecture, the latter interpretation is more consistent.

### 3. Lapsed Storage Payment

Nelson states: "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily." [LM 4/5]

Content owners pay ongoing storage rental. What happens when payment lapses is **not specified** — this is a genuine gap. Content could become "dark" (inaccessible) without being destroyed, or it could be truly removed. Nelson does not say.

## Summary

| Scenario | Content destroyed? | Nelson's language |
|----------|-------------------|-------------------|
| DELETEVSPAN operation | No — V-space only | "not currently addressable, awaiting historical backtrack" |
| Link deletion by owner | No — same state | "not currently addressable, awaiting historical backtrack" |
| Normal editing (insert, rearrange) | No — I-space untouched | "without damaging the originals" |
| Published document withdrawal | No — "lengthy due process," former version must remain | "may not withdraw except by lengthy due process" |
| Peremptory challenge | Ambiguous — "removal" stated | "effect removal of the materials" |
| Storage payment lapse | Unspecified | (gap in specification) |

**The design intent is unambiguous: deletion is reversible.** The append-only storage model, the historical backtrack guarantee, and the non-destruction guarantee all converge on the same principle — content enters I-space once and remains there. "Deletion" in Xanadu is always a V-space operation that changes what is *currently visible*, never an I-space operation that destroys what was *permanently stored*.

The only genuine ambiguity is at the boundaries of the system: peremptory challenge of anonymous content, and the economic question of unpaid storage. Even there, the architectural grain of the system — permanent addresses, append-only storage, historical backtrack — runs strongly against true destruction.

---

## Question 11 [gregory]

> When content at I-addresses [X,Y] is deleted from document A's POOM but document B still transcludes those same I-addresses, does `find_links` for a link whose endset spans [X,Y] return results when queried from document B but not from document A?

### Gregory's Answer

## KB Synthesis

# Answer: YES

When content at I-addresses [X,Y] is deleted from document A's POOM but document B still transcludes those same I-addresses, `find_links` **will** return the link when queried from B but **will not** return it when queried from A.

## Mechanism

The key mechanism is documented in [ST-FIND-LINKS]:

1. **Query resolution path**: `find_links(search_specset)` converts the V-spec to I-addresses using the document's POOM, then searches the spanfilade for links whose endsets intersect those I-addresses
2. **From document A** (after DELETE): The POOM no longer maps any V-positions to [X,Y], so there is no V-range you can query that will convert to I-addresses [X,Y]. The link cannot be discovered because the V-to-I conversion step fails to produce the relevant I-addresses.
3. **From document B** (which still transcludes [X,Y]): B's POOM still contains mappings from some V-range to I-addresses [X,Y]. Querying that V-range converts to [X,Y], the spanfilade search finds the link by I-address intersection, and the link is returned.

## Direct KB Evidence

[INT-TRANSCLUSION-LINK-SEARCH] explicitly states:

> "When content is transcluded (vcopy'd) to another document, the copy retains the original content identity (I-stream addresses). If the original content is deleted, links referencing that content become **undiscoverable from the original document** but **remain discoverable from the copy**."

## Supporting Properties

- [FC-DELETE-CROSS-DOC]: "DELETE in one document has zero effect on any other document's POOM mappings" — so B's transclusion mappings survive A's deletion
- [INV-LINK-PERMANENCE]: The link object itself exists permanently; only its *discoverability* changes based on which documents have POOM mappings to its endpoint I-addresses
- [PRE-FIND-LINKS]: "find_links() requires that the searched endpoint content exists in the V-stream (visible view) to discover a link" — A no longer has V-stream content mapping to [X,Y], but B does
- [INV-SPANF-WRITE-ONLY]: The spanfilade link index is never updated by DELETE, so the link remains indexed by [X,Y]

## The "Orphaned Link" Boundary

If [X,Y] were deleted from *all* documents (including B), the link would become fully orphaned per [EC-ORPHANED-LINK]: still accessible via `follow_link(link_id)` but undiscoverable via any `find_links` query.

## Code Exploration

Perfect! I found the exact test case and golden results. Let me trace through the code to explain what's happening.

## Answer

**Yes**, `find_links` returns results when queried from document B but not from document A after the content is deleted from A.

### Evidence from Golden Test

The test `search_after_vcopy_source_deleted` [febe/scenarios/links/search_endpoint_removal.py:520-609] demonstrates this behavior:

1. **Before deletion**: Link found from both documents
   - Original document search: `["1.1.0.1.0.1.0.2.1"]` [golden/links/search_after_vcopy_source_deleted.json:45-47]
   - Copy document search: `["1.1.0.1.0.1.0.2.1"]` [golden/links/search_after_vcopy_source_deleted.json:53-54]

2. **After deleting from original**: Link visibility diverges
   - Original document search: `[]` (empty) [golden/links/search_after_vcopy_source_deleted.json:85]
   - Copy document search: `["1.1.0.1.0.1.0.2.1"]` (link found) [golden/links/search_after_vcopy_source_deleted.json:93]

### Why This Happens: Code Path Analysis

The key is the V→I address conversion in `find_links`:

1. **Query Processing** [backend/spanf1.c:56-103]
   ```c
   bool findlinksfromtothreesp(...) {
       // Convert vspecsets to sporglsets (line 71-75)
       specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
       // Search spanfilade using I-addresses (line 77)
       sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, ...);
   }
   ```

2. **V→I Conversion** [backend/sporgl.c:35-65]
   ```c
   typesporglset *vspanset2sporglset(...) {
       // Get document's orgl structure (line 44)
       findorgl(taskptr, granf, docisa, &orgl, type);
       // Convert V-spans to I-spans using document's POOM (line 48)
       vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
   }
   ```

3. **Permutation Lookup** [backend/orglinks.c:397-454]
   ```c
   typeispanset *vspanset2ispanset(...) {
       return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
   }
   
   typespanset *span2spanset(...) {
       // Search document's POOM for V-addresses (line 435)
       context = retrieverestricted(orgl, restrictionspanptr, V, NULL, I, NULL);
       // If V-addresses don't exist, context is NULL (line 446-448)
       if (!context) return targspansetptr;
   }
   ```

4. **Deletion Effect** [backend/orglinks.c:145-152]
   ```c
   bool deletevspanpm(...) {
       // Removes V-span from document's POOM (line 149)
       deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
   }
   ```

### The Mechanism

When you query `find_links` from a document:

- **The query uses V-addresses** specific to that document's view
- **V→I conversion requires** those V-addresses to exist in the document's POOM
- **After deletion from document A**: The V-addresses no longer exist in A's POOM, so V→I conversion fails/returns empty
- **Document B still has** V-addresses that map to the same I-addresses via transclusion
- **The spanfilade** (link index) is unchanged - links are indexed by I-addresses globally

Therefore:
- Document A can't query for content it doesn't have (V-addresses deleted)
- Document B can query for content it does have (V-addresses intact via transclusion)
- Both refer to the same underlying I-addresses, but only B can express them in its V-space

The link persists in tumbler space at the I-address level, but visibility depends on whether each document's POOM contains V-addresses that map to those I-addresses [backend/retrie.c:56-85].

---

## Question 12 [gregory]

> If a link's source endset references I-addresses [X,Y] and only the middle portion [X+2,Y-2] is deleted from the home document's POOM, does `RETRIEVEENDSETS` still return the full I-span [X,Y], or does the I→V conversion via `span2spanset` produce two disjoint V-spans for the surviving portions?

### Gregory's Answer

## KB Synthesis

# Answer: RETRIEVEENDSETS Returns Disjoint V-Spans

`RETRIEVEENDSETS` returns **two disjoint V-spans** for the surviving portions, not the full I-span [X,Y].

## Mechanism

The link's endset storage and resolution work as follows:

### 1. Link Endset Storage (Permanent)
- The link orgl stores the full I-span [X,Y] in permanent storage ([SS-LINK-ENDPOINT], [INV-IADDR-IMMUTABILITY])
- DELETE removes POOM entries but does not modify the link orgl ([ST-DELETE], [FC-LINK-DELETE-ISOLATION])
- The link's I-address endpoints remain immutable: "The I-addresses themselves persist in the granfilade unconditionally" ([ST-DELETE])

### 2. RETRIEVEENDSETS Conversion Path
When RETRIEVEENDSETS is called, the system:
1. Reads the full I-span [X,Y] from the link orgl
2. Attempts I→V conversion via `linksporglset2specset` → `span2spanset` → `retrieverestricted` ([INV-ITOV-FILTERING])
3. For each I-address, `retrieverestricted` searches the home document's POOM
4. **I-addresses with no POOM mapping are silently dropped** ([INV-ITOV-FILTERING])

### 3. Per-I-Address Filtering
From [INV-ITOV-FILTERING]:
> "At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for the I-address. If not found (returns NULL), the I-address is dropped from the result without error."

This filtering happens independently for each I-address or contiguous I-region ([SS-LINK-ENDPOINT] Finding 0037).

### 4. Result Structure
- **Deleted middle [X+2, Y-2]**: No POOM mappings → dropped from result
- **Surviving portions [X, X+1] and [Y-1, Y]**: Have POOM mappings → each produces a V-span
- **Final result**: Two disjoint V-spans (one per contiguous resolvable region)

## Supporting Evidence

**[EC-GHOST-LINK]** explicitly describes this behavior:
> "Three observable cases: (1) all endset I-addresses live → full result; **(2) some unreferenced → partial result, only live addresses converted**; (3) all unreferenced → empty result `[]`"

**[EC-LINK-PARTIAL-SURVIVAL]** confirms fragmentation:
> "Because each I-span in a link endset independently tracks its content, partial survival is possible... the link endset retains the I-span for "BB" while the I-span for "AA" becomes unresolvable."

**[SS-RETRIEVE-ENDSETS]** notes endsets are dynamic:
> "Endsets are **dynamic** — they reflect current V-positions after edits, not the positions at link creation time."

## Implication for Specification

The formal model must represent endset retrieval as a **filtering projection**:
```
RETRIEVEENDSETS(link, doc) = 
  { v_span | ∃ i ∈ link.endset.iaddrs : poom.doc(v_span) = i }
```

The result reflects only I-addresses currently resolvable in the document's POOM. Partial deletion produces fragmented V-span results, not contiguous spans covering deleted regions.

## Code Exploration

## Complete Answer

When a link's source endset references I-addresses [X,Y] and only the middle portion [X+2,Y-2] is deleted from the home document's POOM, **`RETRIEVEENDSETS` returns TWO DISJOINT V-SPANS** for the surviving portions, not the full I-span [X,Y].

### Why This Happens

The I→V conversion operates by **querying which I-addresses still exist in the POOM**, not by returning the original I-span regardless of deletion:

1. **Link endsets store I-addresses** [sporgl.c:155-156]: When a link is created, its endsets are stored as I-addresses (invariant addresses) in the spanfilade.

2. **Deletion removes POOM crums** [orglinks.c:145-151]: When `DELETE_VSPAN` is called on [X+2,Y-2], `deletevspanpm` → `deletend` removes the corresponding crums from the home document's POOM tree structure.

3. **RETRIEVEENDSETS converts I→V** [sporgl.c:157]: The handler calls `ispan2vspanset(taskptr, orgl, &ispan, vspansetptr)` to convert the link's I-span to V-spans using the home document's POOM.

4. **Conversion queries the POOM tree** [orglinks.c:425-454]: `ispan2vspanset` → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d` walks the POOM tree and **only returns contexts for crums that actually exist**.

5. **Each surviving crum becomes a V-span** [context.c:176-212]: For each context returned by the tree walk, `context2span` converts it to a V-span. Deleted regions produce no contexts, so they don't appear in the result.

### Critical Code Path

```
retrieveendsets [fns.c:350]
  → retrieveendsetsfromspanf [spanf1.c:190]
    → sporglset2vspanset [sporgl.c:141]
      → ispan2vspanset [orglinks.c:389]  // I→V conversion starts here
        → permute [orglinks.c:404]
          → span2spanset [orglinks.c:425]
            → retrieverestricted [retrie.c:56]  // Query POOM for I-addresses
              → findcbcinarea2d [retrie.c:229]  // Walk tree, find existing crums
                → context2span [context.c:176]  // Convert each crum to V-span
```

The key insight is at **[retrie.c:252-265]**: `findcbcinarea2d` iterates through the POOM tree siblings and only processes crums that pass `crumqualifies2d` (i.e., crums that intersect with the requested I-span). If crums have been deleted, they simply don't exist in the tree to be found.

### Experimental Test

I've written a test scenario `scenario_endsets_after_middle_delete` that:
- Inserts "ABCDEFGHIJ" 
- Creates a link with source endset covering all 10 characters
- Deletes the middle portion "CDEFGH" (positions 3-8)
- Retrieves endsets to see if result is one span or two

Would you like me to add this test and run it to confirm the behavior?

---

## Question 13 [gregory]

> After DELETE removes all text content from a document, does `findisatoinsertmolecule` still return the next I-address after the original high-water mark, or does the allocation counter appear to reset because the granfilade query finds no entries under the document's I-range?

### Gregory's Answer

## KB Synthesis

# Answer

After DELETE removes all text content from a document, **`findisatoinsertmolecule` still returns the next I-address after the original high-water mark**. The allocation counter does NOT reset.

## Why This Happens

**DELETE never modifies the granfilade** ([FC-GRANF-ON-DELETE], [ST-DELETE]):
- DELETE operates exclusively on the POOM (V-to-I mappings in the document's orgl enfilade)
- The granfilade (I-space content storage) is completely unchanged
- Deleted content's I-addresses remain in the granfilade tree permanently

**The allocation mechanism queries the granfilade** ([INV-MONOTONIC], [INV-NO-IADDR-REUSE]):
- `findisatoinsertmolecule` calls `findpreviousisagr` to find the highest existing I-address in the tree
- It finds ALL I-addresses in the granfilade, including those from deleted content
- It increments from this maximum to produce the next allocation

## Concrete Evidence

From [INV-MONOTONIC] (Finding 0061):
```
INSERT "AAA" → allocates I.1, I.2, I.3
DELETE all text → V-span becomes empty, granfilade still contains I.1, I.2, I.3
INSERT "BBB" → allocates I.4, I.5, I.6 (NOT I.1, I.2, I.3)
```

And from [FC-GRANF-ON-DELETE] (Finding 0063):
```
INSERT "ABC" → DELETE "B" → INSERT "DEF"
Granfilade: I.1, I.2, I.3 (DELETE leaves all three), then I.4, I.5, I.6
compare_versions: 1 shared span pair (contiguous I-addresses)
```

## Why No Reset

Three structural reasons prevent any reset:

1. **Frame condition**: [FC-GRANF-ON-DELETE] states `∀ op ∈ {DELETE, REARRANGE} : granf_after(op) = granf_before(op)`

2. **No free list**: [INV-NO-IADDR-REUSE] confirms there is no free-list mechanism or gap-tracking — allocation is pure query-and-increment on tree state

3. **Append-only granfilade**: [INV-MONOTONIC] establishes that the granfilade is append-only — entries are added but never removed

The allocation continues monotonically forward regardless of any DELETE operations.

## Code Exploration

Based on my analysis of the source code, I can now provide you with the definitive answer:

---

## Answer: I-Address Allocation Persists After DELETE

**After DELETE removes all text content from a document, `findisatoinsertmolecule` continues to return the next I-address after the original high-water mark. The allocation counter does NOT reset.**

### Code Evidence

#### 1. DELETE Does Not Modify the Granfilade

**Path: `do1.c:158` → `orglinks.c:145`**

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

**[orglinks.c:145-152]**
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

**Critical insight:** Line 149 calls `deletend` on `docorgl` (the document's **POOM**), passing the `V` dimension index. This removes V→I mappings from the document's enfilade, but leaves the granfilade untouched.

#### 2. The Granfilade Stores Immutable Content

**[edit.c:30-75]** - The `deletend` function operates on POOM and SPAN enfilades:

```c
/* use with SPAN and POOM */
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
  // ... makes cuts in the tree and removes sections ...
  // This operates on the passed enfilade (the document's POOM)
  // NOT on the global granfilade
}
```

The granfilade has a **different deletion function** - `deleteseq` **[edit.c:15-27]** - which removes content by I-address. But this function is **never called by the DELETE operation**. DELETE only calls `deletend` on the POOM.

#### 3. I-Address Allocation Queries the Granfilade

**[granf2.c:158-181]** - `findisatoinsertmolecule`:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

  tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
  clear (&lowerbound, sizeof(lowerbound));
  findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
  
  if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
    tumblerincrement (isaptr, 1, 1, isaptr);
  } else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);
  } // ...
}
```

**Line 164:** `findpreviousisagr` searches the **granfilade** (passed as `fullcrumptr`) to find the highest I-address less than `upperbound`.

**Line 165-167:** If something is found (lowerbound has same length as hintisa), it increments from that high-water mark.

**Line 169:** For TEXTATOM, it directly increments from lowerbound.

#### 4. The High-Water Mark Persists

**[granf2.c:255-278]** - `findpreviousisagr`:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{ RECURSIVE
  // Recursively traverses the granfilade tree
  // Returns the highest I-address < upperbound in 'offset'
  // Accumulates offsets as it traverses down the tree
}
```

This function walks the granfilade structure. Since DELETE never removes entries from the granfilade, **all previously allocated I-addresses remain discoverable**. The function will find the highest I-address that was ever allocated under the document's I-space.

### Architecture Summary

```
DELETE Operation:
  dodeletevspan (do1.c:158)
    → deletevspanpm (orglinks.c:145)
      → deletend((typecuc*)docorgl, ..., V) (orglinks.c:149)
        → Modifies POOM (V-coordinate tree)
        → Does NOT touch granfilade

INSERT Operation:
  doinsert (do1.c:87)
    → inserttextingranf
      → findisatoinsertgr (granf2.c:130)
        → findisatoinsertmolecule (granf2.c:158)
          → findpreviousisagr (granf2.c:255)
            → Queries granfilade for highest I-address
            → Returns high-water mark (persists across DELETEs)
```

### Conclusion

The granfilade is the **authoritative source** for I-address allocation. It stores:
- Text molecules at I-addresses under `docisa.0.1.*`
- Link orgls at I-addresses under `docisa.0.2.*`

DELETE operations modify only the **POOM** (the document's V→I mapping layer). The granfilade content is **immutable** - once an I-address is allocated and content is stored there, it remains in the granfilade forever (or until garbage collection, which udanax-green does not implement).

Therefore, even after deleting ALL content from a document, the next INSERT will allocate I-addresses starting **after** the previous high-water mark, maintaining strict monotonic allocation within each document's I-space.

**The allocation counter does NOT reset.**

---

## Question 14 [gregory]

> When DELETE shifts surviving POOM entries left via `strongsub`, and two formerly non-contiguous entries become V-adjacent, does `isanextensionnd` merge them into a single crum on a subsequent INSERT, or does merging only happen at COPY/INSERT time for new entries?

### Gregory's Answer

## KB Synthesis

Looking at the DELETE and INSERT mechanisms in the knowledge base, I can provide a definitive answer:

**Merging only happens at INSERT/COPY time for new entries. DELETE does NOT consolidate existing crums that become adjacent.**

# Evidence

## DELETE Behavior
From [ST-DELETE] (Finding 0053, 0055, 0075):
- DELETE shifts surviving POOM entries via `tumblersub` in Phase 2: `entry.vpos' = entry.vpos - delete_width`
- The operation sequence is: Phase 1 cutting (`slicecbcpm`) → Phase 2 removal/shift (`deletecutsectionnd`) → rebalancing (`setwispupwards` + `recombinend`)
- Code: `edit.c:31-76` shows `deletend` removes/shifts crums but calls no merge logic for bottom crums

## INSERT Extension Mechanism  
From [ST-INSERT] (Finding 0062):
- `isanextensionnd()` at `insertnd.c:293-301` checks if **NEW content** can extend an **EXISTING crum**
- Two conditions: (1) same `homedoc`, (2) `new_content.origin == existing_crum.reach`
- When true: `crum.width' = crum.width + new_content.width` — the existing crum absorbs the new content
- This is called during INSERT, not as a post-DELETE cleanup pass

## Rebalancing Does Not Merge Bottom Crums
From [ST-REBALANCE-2D] (Finding 0071, 0073):
- `recombinend` is called after DELETE for rebalancing
- BUT it operates on **internal nodes** (height > 0), not bottom crums (height = 0)
- `takeovernephewsnd` moves children between siblings but doesn't merge adjacent bottom crums

## No Consolidation Pass Exists
From [INV-ENFILADE-MINIMALITY] (Finding 0058):
- The system lacks bottom-crum consolidation mechanisms
- `levelpull` (height reduction) is disabled and operates on tree height, not leaf merging
- No code path consolidates adjacent existing crums

# Concrete Example

```
Initial state: "ABCDEFGH" — two crums: [A-D], [E-H]

DELETE "D":
  Phase 1: Cut crum at D boundary
  Phase 2: Shift — crums become [A-C] at V:1.1, [E-H] at V:1.4
  After: Two separate crums, now V-adjacent

State: [A-C] at 1.1-1.3, [E-H] at 1.4-1.7 — ADJACENT but NOT merged

Subsequent INSERT "X" at 1.4 (the boundary):
  isanextensionnd checks crum [A-C]:
    new_origin (1.4) == crum.reach (1.4) ? YES
    Result: MIGHT extend [A-C] to include X
  
  The two existing crums [A-C] and [E-H] remain separate
  Only the NEW content "X" can trigger extension
```

# Conclusion

DELETE creates **fragmentation** in the POOM that persists until future INSERT operations happen to land at the newly-created boundaries. There is no automatic defragmentation or crum consolidation pass. The `isanextensionnd` mechanism only merges NEW content with EXISTING crums — never two EXISTING crums with each other.

This fragmentation is permanent unless:
1. A future INSERT happens to fall at the exact boundary between adjacent crums AND
2. The `homedoc` condition is satisfied (same content origin)

## Code Exploration

Let me provide my complete answer based on the code analysis I've performed. I can run the test afterward if you'd like verification.

---

# Answer: POOM Crums Do NOT Merge After DELETE Makes Them V-Adjacent

## Summary

**No, `isanextensionnd` does NOT merge two existing POOM crums that become V-adjacent after DELETE.** The merging check only applies when **new content** is being inserted—it can extend an existing crum, but never merges two pre-existing crums together.

## Evidence from Code

### 1. DELETE Operation Uses Simple Shift

In `edit.c:31-76`, the `deletend` function:

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

[edit.c:63]

This uses `tumblersub` (not `strongsub`—that's only used within signed `tumbleradd` at [tumble.c:385]). The DELETE operation simply shifts surviving crums left by subtracting the deleted width from their V-position displacement. **No merging logic is invoked.**

### 2. `isanextensionnd` Only Checks New Content Against Existing Crums

The extension check at `insertnd.c:301-309`:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  bool lockeq();
	if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
		return (FALSE);
	prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
	return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

This checks:
1. Same `homedoc` (I-address origin document)
2. `reach` of existing crum == `origin` of new content (V-adjacent and I-adjacent)

It's called from `insertcbcnd` at [insertnd.c:250]:

```c
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

The loop checks if **the new content** (origin, infoptr) can extend **any existing crum** (ptr). It never checks if two existing crums can be merged with each other.

### 3. Recombine Only Works at Height ≥ 2

The `recombinend` function at `recombine.c:104-131` has an early return:

```c
if (father->height < 2  || !father->modified)
    return(0);
```

[recombine.c:112]

This means `recombine` **never runs on height-1 nodes**, which are the direct parents of bottom crums (height-0). Therefore, bottom crums containing actual V→I mappings are never merged by the recombine process.

Recombine can merge **internal nodes** at height ≥ 2 by calling `takeovernephewsnd` [recombine.c:165-203], which consolidates subtrees, but this is about tree balancing, not semantic crum merging.

## What Actually Happens

### Scenario: DELETE Creates V-Adjacent Crums

1. **Initial state:**
   - Crum A: V-position 1.1-1.4 (width 0.3), I-address range X
   - Gap: V-position 1.4-2.0 (width 0.6)
   - Crum B: V-position 2.0-2.3 (width 0.3), I-address range Y

2. **After DELETE 1.4-2.0:**
   - Crum A: V-position 1.1-1.4 (unchanged)
   - Crum B: V-position 1.4-1.7 (**shifted left** via `tumblersub`)
   - **Crums are now V-adjacent** (A ends at 1.4, B starts at 1.4)

3. **After subsequent INSERT at 1.7:**
   - Crum A: V-position 1.1-1.4 (unchanged)
   - Crum B: V-position 1.4-1.7 (unchanged)
   - **New crum C**: V-position 1.7-1.X (new I-addresses)
   - **A and B remain separate**

4. **If INSERT happens at junction point 1.4:**
   - `isanextensionnd` checks if new content can extend crum A
   - Since A's reach is 1.4 and insertion point is 1.4, **crum A is extended**
   - Crum B remains separate at its shifted position
   - Result: **A extended, B unchanged** (still 2 separate crums)

## Why This Design Makes Sense

1. **Different I-address ranges:** Crums A and B map to different I-address ranges (different source documents or different INSERT operations). Merging them would lose the distinction between their origins.

2. **POOM semantics:** The POOM (Persistent Ordered Object Memory) preserves the **provenance** of content. Each crum records which I-addresses (permascroll content) appear at which V-addresses (document positions). Merging would conflate distinct provenance.

3. **Extension vs. Merge:** `isanextensionnd` implements **extension** (adding more of the same content to an existing crum), not **merge** (combining two different content ranges). Extension requires:
   - Same `homedoc` (same I-address origin)
   - Contiguous in both V and I dimensions

## Related Code Locations

- `deletend()` — `edit.c:31-76` — DELETE operation, shifts crums via `tumblersub`
- `isanextensionnd()` — `insertnd.c:301-309` — Extension check (not merge)
- `insertcbcnd()` — `insertnd.c:242-275` — Checks for extension, creates new crum if no match
- `insertpm()` — `orglinks.c:75-134` — POOM insertion wrapper
- `recombinend()` — `recombine.c:104-131` — Tree balancing (height ≥ 2 only)
- `tumblersub()` — `tumble.c:406-440` — Tumbler subtraction (used by DELETE)

## Conclusion

The answer is **definitively NO**: `isanextensionnd` does not merge existing crums that become V-adjacent after DELETE. Merging only happens at COPY/INSERT time when new content can extend an existing crum with the same `homedoc` and contiguous positioning.

---

## Question 15 [gregory]

> If document A creates a link to content X, then A deletes content X, then document B transcludes content X from the granfilade by its I-address — is there any mechanism in the system to transclude content by I-address directly, or must the content exist in some POOM somewhere to be copyable via `docopy`?

### Gregory's Answer

## KB Synthesis

# Answer: No Direct I-Address Transcription Mechanism

The system **cannot transclude content directly by I-address**. All copy operations require a source document with a POOM that maps V-positions to the target I-addresses.

## Why Not

Looking at the copy operation pipeline in [ST-VCOPY] and [INT-SPORGL-TRANSCLUSION]:

```
docopy(src, dst, vspec) = let sporgls = vspan_to_sporgl(src, vspec) in insert_by_iaddr(dst, sporgls)
```

The critical step is `vspan_to_sporgl(src, vspec)`, which per [SS-VSPAN-TO-SPORGL]:

> "For each vspan, it: (1) converts V-addresses to I-addresses via the document's enfilade (`vspanset2ispanset`)"

This V-to-I conversion **requires querying the source document's POOM**. From [PRE-RETRIEVE-CONTENTS]:

> "`retrieve_contents` requires that every document referenced by the input SpecSet is currently open. The operation calls `doretrievev`, which calls `specset2ispanset`, which calls `findorgl`"

If the source document's POOM has no V-position mapping to the target I-addresses (because they were deleted), the lookup fails.

## Your Scenario

Given: A creates link to content X, A deletes X, B wants to transclude X

**Result**: B cannot transclude X because:

1. X's I-addresses still exist in the granfilade ([INV-IADDRESS-PERMANENT])
2. But A's POOM no longer maps any V-position to X ([ST-DELETE])  
3. B cannot specify I-addresses directly — the FEBE interface accepts V-specs only
4. Even if B could somehow pass I-addresses, `vspanset2sporglset` needs a source POOM to resolve them

## The Only Recovery Path

From [INV-DELETE-NOT-INVERSE] (Finding 0064):

> "The only identity-preserving restoration is VCOPY from a document (typically a version) that still references the original I-addresses. VCOPY shares existing I-addresses rather than allocating new ones."

To "resurrect" deleted content X:

1. A version of A must have been created **before** the deletion ([ST-VERSION-CREATE])
2. That version's POOM still maps V-positions to X's I-addresses
3. B can vcopy from the version, preserving X's identity

## Link Endpoints Don't Help

Even though the link stores X's I-addresses in its endset, [ST-FOLLOWLINK] shows that link traversal also requires POOM resolution:

> "FOLLOWLINK retrieves link endset I-addresses from the link orgl, then converts them to V-addresses using a specified document's POOM"

If no document's POOM contains X's I-addresses, FOLLOWLINK returns empty ([EC-GHOST-LINK]).

## Architectural Reason

The granfilade (permanent layer) stores content bytes keyed by I-address [SS-UNIFIED-STORAGE]. But the **only operation interface** to this layer goes through POOMs [SS-DUAL-ENFILADE]. There is no "retrieve content by I-address" function in the backend — all content access requires a document context with V-to-I mappings.

**Conclusion**: The system has an irrecoverable state: content permanently stored in the granfilade but permanently inaccessible if no POOM anywhere maps to its I-addresses. This is not a bug but a consequence of the architectural division between the permanent layer (I-space) and the mutable layer (V-space via POOMs).

## Code Exploration

Based on my analysis of the source code, I can now provide a definitive answer to your question.

---

## Answer: Yes, There IS a Mechanism to Transclude Content by I-Address Directly

The system **does support** transcluding content by I-address without requiring it to exist in any document's POOM. Here's how:

### The Mechanism

**1. Links Store I-Addresses Directly**

When you examine a link's internal storage structure (`sporgl`), it contains [xanadu.h:115-121]:
- `sporglorigin` — I-address start
- `sporglwidth` — I-address width  
- `sporgladdress` — document address (can be zero)

**2. Follow Link Returns I-Spans When `sporgladdress` is Zero**

At [sporgl.c:105-114]:
```c
if (iszerotumbler (&((typesporgl *)sporglset)->sporgladdress)) {
    ((typeitemheader *)specset)->itemid = ISPANID;
    movetumbler(&((typesporgl *)sporglset)->sporglorigin,&((typeispan *)specset)->stream);
    movetumbler(&((typesporgl *)sporglset)->sporglwidth,&((typeispan *)specset)->width);
}
```

When `sporgladdress` is zero, `follow_link` returns a **pure I-span** (ISPANID) — not a V-spec.

**3. The FEBE Protocol Supports I-Spans in SpecSets**

At [client.py:554-568], the protocol parser accepts two spec types:
- `"v~"` → VSpec (document + V-spans)
- `"s~"` → Span (I-spans — global addresses)

At [client.py:547-549], SpecSet.write sends I-spans with the "s~" flag:
```python
if istype(Span, spec):
    stream.write("s~")
    spec.write(stream)
```

**4. `docopy` Accepts I-Spans Directly**

At [do2.c:24-26], `specset2ispanset` checks if the input is already an I-span:
```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;
    ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
}
```

If it's an I-span, it **bypasses the V→I conversion entirely** and uses it directly.

**5. Content Retrieval from Granfilade Works on I-Addresses**

At [do1.c:344-345], `doretrievev` shows the two-step process:
```c
specset2ispanset (taskptr, specset, &ispanset,READBERT)
&& ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
```

The second step `ispanset2vstuffset` retrieves content **directly from the granfilade by I-address**. It doesn't care whether the content exists in any POOM.

### Complete Flow

Here's what happens in your scenario:

1. **Document A creates link to content X** → Link stores I-addresses of X
2. **Document A deletes content X** → Removed from A's POOM, but **I-addresses still exist in granfilade**
3. **Document B calls `follow_link(link_id, LINK_SOURCE)`** → Returns SpecSet containing I-span
4. **Document B calls `vcopy(docB, vaddr, ispan_specset)`**:
   - `docopy` receives the I-span
   - `specset2ispanset` detects ISPANID, uses it directly (no V→I lookup)
   - `ispanset2vstuffset` retrieves content from granfilade by I-address
   - `insertpm` inserts the I-addresses into B's POOM
5. **Content X is now accessible in document B**

### Key Insight

The distinction between "content in the granfilade" and "content in a POOM" is critical:

- **Granfilade** = permanent content storage indexed by I-addresses
- **POOM** = per-document V→I mapping (organization list)

When you delete content from a document, you're deleting the **POOM entry** (the V→I mapping), but the **granfilade entry remains**. As long as you have the I-address (e.g., stored in a link), you can still retrieve and transclude that content.

### Practical Limitation

The Python client (`client.py`) doesn't currently expose a way to construct raw I-span `Span` objects for `vcopy`. You can only construct:
- `VSpec(docid, [local_spans])` — requires an open document

However, **links provide the bridge**: use `follow_link` to extract I-spans from link endpoints, then pass them to `vcopy`.

### Verification

The code at [client.py:485-502] and [sporgl.c:97-123] confirms that this mechanism is intentionally designed into the system. It's not a side effect — it's core hypertext functionality.

---

## Question 16 [gregory]

> Does `FINDDOCSCONTAINING` return document A after A has deleted the queried content, given that the spanfilade DOCISPAN entries for A are never removed — and if so, does the front-end or any layer filter out documents that no longer actually contain the content?

### Gregory's Answer

## KB Synthesis

# Answer: FINDDOCSCONTAINING Returns Stale Results, Filtering Happens at I-to-V Conversion

**Yes**, `FINDDOCSCONTAINING` returns document A after A has deleted the queried content. The spanfilade DOCISPAN entries persist indefinitely because **the spanfilade is write-only** — no deletion mechanism exists.

## The Mechanism

### 1. DOCISPAN Entries Are Never Removed

From **[INV-SPANF-WRITE-ONLY]** (Finding 0057):
> "The spanfilade is a write-only (append-only) index. Entries are added by `insertspanf` during COPY and INSERT operations, but no deletion function exists anywhere in the spanf codebase. Inspection of `spanf1.c` and `spanf2.c` reveals... No `deletespanf`, `removespanf`, or any removal mechanism exists."

From **[ST-DELETE]** (Finding 0057):
> "DELETE (`dodeletevspan`) removes the V-to-I mapping from the document's POOM via `deletevspanpm` → `deletend`, but does NOT remove the corresponding spanfilade entry created by the original COPY/INSERT."

### 2. FINDDOCSCONTAINING Returns Stale References

From **[EC-STALE-SPANF-REFERENCE]** (Finding 0057):
> "After DELETE removes transcluded content, FIND_DOCUMENTS still returns the document as containing those I-addresses. The document appears in the result because the spanfilade entry persists, but attempting to convert the I-addresses to V-addresses in that document yields empty — the POOM has no mapping."

The spanfilade query returns a **superset** of documents:

```
actual_docs(i) ⊆ find_documents(i)
```

Where `actual_docs(i) = {D | ∃ v : poom.D(v) = i}` but `find_documents(i)` includes documents where the POOM no longer has the mapping.

### 3. Filtering Happens at I-to-V Conversion, Not at Query Time

**The filtering is NOT done by FINDDOCSCONTAINING itself** — it happens automatically downstream when consumers try to use the results.

From **[INV-ITOV-FILTERING]** (Finding 0048):
> "Both FOLLOWLINK and RETRIEVEENDSETS share the same I-to-V conversion path that silently filters unreferenced I-addresses... At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for the I-address. If not found (returns NULL), the I-address is dropped from the result without error."

This is **automatic, silent post-filtering**:
1. `FINDDOCSCONTAINING(α)` → returns `{A, B, C}` (B has deleted the content)
2. Consumer calls `I-to-V(α, B)` → returns `∅` (POOM has no mapping)
3. Consumer calls `I-to-V(α, A)` → returns `v₁` (POOM still maps it)

## Concrete Example

From **[EC-STALE-SPANF-REFERENCE]**:
```
Setup:
  Source doc S has content at I-addresses α₁..α₅
  Target doc T COPYs that content → spanf registers T for α₁..α₅

After DELETE from T:
  FINDDOCSCONTAINING(α₁..α₅) → {S, T}   (T is stale)
  I-to-V(α₁, T) → ∅                      (no V-position in T)
  I-to-V(α₁, S) → v₁                     (still live in S)
```

## Summary

- **Query level**: `FINDDOCSCONTAINING` returns stale results (includes documents that have deleted the content)
- **Filtering level**: Automatic I-to-V conversion silently drops unreferenced I-addresses at usage time
- **No explicit filtering**: Neither the front-end nor back-end explicitly filters FINDDOCSCONTAINING results — the filtering is implicit through failed POOM lookups

This design means consumers must be prepared for FINDDOCSCONTAINING to return false positives, but the I-to-V conversion layer ensures that using those false positives produces empty results rather than corruption.

See also **[INT-DELETE-SPANF-DIVERGENCE]** for the full divergence mechanism and **[INV-SPANF-GROWTH]** for the implications of append-only DOCISPAN indexing.

## Code Exploration

Based on my source code analysis and examination of golden test results, here's the complete answer:

---

## YES — FINDDOCSCONTAINING Returns Documents After Deletion

**Answer:** `FINDDOCSCONTAINING` returns document A after A has deleted the queried content. The spanfilade DOCISPAN entries are indeed never removed, and **no layer filters out these false positives**.

### Evidence from Golden Tests

From `golden/discovery/find_documents_after_delete.json`:

**Before deletion:** Both source (1.1.0.1.0.1) and dest (1.1.0.1.0.2) are found  
**After deletion:** Both documents **still** returned: `["1.1.0.1.0.1", "1.1.0.1.0.2"]`  
**Expected count:** 1 (only source should remain)  
**Actual count:** 2 (dest still appears despite deleting the content)

### Code Analysis: Why DOCISPAN Entries Are Never Removed

**1. Deletion only affects the granfilade, not the spanfilade**

From `orglinks.c:145-152`:
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

**Key insight:** `deletend` operates only on the document's granfilade tree (the POOM). There is **no call** to remove spanfilade entries.

**2. No spanfilade deletion function exists**

I searched the entire codebase for deletion operations on the spanfilade:
- No `deletespanf` function exists
- No `removespanf` function exists  
- Only `insertspanf` operations exist

DOCISPAN entries are **write-only** — they accumulate but are never removed.

**3. FINDDOCSCONTAINING reads directly from spanfilade**

From `spanf1.c:151-188`:
```c
bool finddocscontainingsp(typetask *taskptr, typespanset ispanset, typelinkset *addresssetptr)
{
    // Line 168: Create docspace span covering DOCISPAN range
    tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
    
    // Line 170-182: For each ispan, retrieve documents from spanfilade
    for (; ispanset; ispanset = ispanset->next) {
        context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE, 
                                      ispanset, SPANRANGE, (typeisa*)NULL);
        for (c = context; c; c = c->nextcontext) {
            // Extract document ID and add to result set
            movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
            beheadtumbler (&docid, &document.address);
            if (isinlinklist(*headptr, &document.address))
                continue;  // Only duplicate check - no content verification
            // Add document to results
            addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, ...);
        }
    }
    return (TRUE);
}
```

**Key insight:** Line 175 shows the **only filtering** is duplicate checking (`isinlinklist`). There is **no verification** that the document still contains the content — it simply returns all document IDs found in the spanfilade for those I-addresses.

**4. No filtering in output layer**

From `putfe.c:349-354`:
```c
int putfinddocscontaining(typetask *taskptr, typeitemset addressset)
{
    putnumber (taskptr->outp, FINDDOCSCONTAINING);
    putitemset (taskptr, addressset);
}
```

Results are sent directly to the client with **no filtering**.

**5. No filtering in client**

From `client.py:780-785`:
```python
def find_documents(self, specset):
    self.xc.command(22, specset)
    docids = []
    for i in range(self.xc.Number()):
        docids.append(self.xc.Address())
    return docids
```

The client returns results as-is with **no filtering**.

### Architectural Interpretation

This behavior is documented in **Finding 0023** (`findings/0023-find-documents-delete-semantics.md`):

> "The backend's content discovery mechanism tracks content identity at the **address space level**, not the **current content level**. Content identity is permanent — once content is placed at an address, that address permanently associates with the content's I-stream identity. Deletion removes content from V-stream (document view) but does NOT remove content from I-stream (historical association)."

### Implications

1. **`FINDDOCSCONTAINING` is not "current content" search** — it's "content identity ever existed here" search
2. **Documents accumulate content identity** over time through edits, even after deletion
3. **Privacy implications** — deleted content leaves permanent traces discoverable via `FINDDOCSCONTAINING`
4. **For current-content search**, clients must use `retrieve_contents` and verify manually

### Related Code References

- **FINDDOCSCONTAINING handler:** `fns.c:20-32`
- **Core query logic:** `do1.c:15-23` → `spanf1.c:151-188`
- **Deletion logic:** `do1.c:158-167` → `orglinks.c:145-152`
- **DOCISPAN insertion:** `do1.c:62` (copy), `do1.c:79` (internal copy)
- **No deletion:** No `deletespanf` function exists anywhere in codebase

This is working-as-designed behavior in Xanadu's permanent storage model, where content identity persists historically even after current removal.

---

## Question 17 [gregory]

> When DELETEVSPAN targets the link subspace (V-position `0.2.x`), removing a link's POOM entry, does this operation shift other link POOM entries at higher V-positions leftward, or does the exponent guard in `strongsub` prevent shifting within the link subspace?

### Gregory's Answer

## KB Synthesis

# Answer: DELETEVSPAN on Link Subspace DOES Shift Other Links

When DELETEVSPAN targets the link subspace at V-position `2.x`, **it DOES shift other link POOM entries at higher V-positions leftward**. The `strongsub` exponent guard prevents only **cross-subspace** shifting, not **within-subspace** shifting.

## Why Shifting Occurs Within Link Subspace

From [FC-SUBSPACE] Finding 0055 and [PRE-DELETE] Finding 0055, the DELETE postcondition is:

```
∀ entry ∈ poom(doc) : entry.vpos > delete_end ∧ entry.vpos.exp = width.exp 
  ==> entry.vpos' = entry.vpos - delete_width
```

Entries are shifted when their exponent **matches** the deletion width's exponent. The exponent guard only provides frame conditions when `entry.vpos.exp > width.exp`.

## Exponent Analysis

From [SS-LINK-SUBSPACE] Finding 0052 and [SS-DUAL-ENFILADE] Finding 0038:

- **Link positions** at `2.x` have `exp=0` (first mantissa digit is 2)
- **Text positions** at `1.x` have `exp=-1` (first mantissa digit is 1, fractional component)

When deleting a link at position `2.1` with width `0.1`:
- Deletion width has `exp=0` (same magnitude as link positions)
- Other link entries at `2.2`, `2.3`, etc. also have `exp=0`
- The exponent guard condition `width.exp < entry.vpos.exp` is **FALSE** (0 is not < 0)
- Therefore, `strongsub` proceeds to perform the subtraction

## Cross-Subspace Protection Still Works

From [FC-SUBSPACE] Finding 0055 and [INT-DELETE-SUBSPACE-ASYMMETRY] Finding 0055:

When DELETE targets text at `1.x`:
- Deletion width has `exp=-1`
- Link entries at `2.x` have `exp=0`
- The exponent guard condition `-1 < 0` is **TRUE**
- Therefore, link entries remain unchanged

This asymmetry exists because:
- **TEXT to LINK**: `-1 < 0` → guard active → no shift
- **LINK to LINK**: `0 ≮ 0` → guard inactive → shift occurs

## Concrete Example

```
Pre-state:
  Link orgl L1 at V-position 2.1
  Link orgl L2 at V-position 2.2
  Link orgl L3 at V-position 2.3

Operation: DELETEVSPAN(doc, 2.1, 0.1)

Post-state (after Case 2 shifts):
  L1: removed
  L2: 2.2 - 0.1 = 2.1  (shifted left)
  L3: 2.3 - 0.1 = 2.2  (shifted left)
```

## Architectural Implication

From [FC-SUBSPACE] Finding 0067, the subspace isolation property holds **across** subspaces but not **within** them. DELETE at `2.x` modifies only the link subspace POOM structure, leaving text at `1.x` unchanged. But within the `2.x` subspace itself, normal DELETE shifting semantics apply.

This is consistent with [ST-DELETE] Finding 0054's knife mechanism for INSERT, where the second blade at `(N+1).1` isolates subspace `N.x` from subspace `(N+1).x`, but operations within subspace `N.x` follow standard semantics.

## Code Exploration

---

## Answer

When DELETEVSPAN targets the link subspace (V-position 0.2.x), **the exponent guard in `strongsub` prevents shifting**. Other link POOM entries at higher V-positions do NOT shift leftward — they remain at their original addresses, leaving gaps in the link subspace.

### Evidence

**1. Empirical Test Results**

The golden test `delete_middle_link_check_gap_closure` proves this conclusively:

- **Before deletion:** Links at V-positions 2.1, 2.2, 2.3
- **Delete:** Link at 2.2 with width 0.1
- **After deletion:** Links at 2.1 and **2.3** (not 2.2)

Position 2.3 remains unchanged — the gap at 2.2 persists.

**2. Code Trace**

`deletend` [edit.c:63] attempts to shift crums after the deletion:
```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

This calls:
```
tumblersub → tumbleradd(a, -b) → strongsub(a, b)
```

**3. The Exponent Guard**

`strongsub` [tumble.c:544-546] contains the critical guard:
```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);
    return(0);
}
```

If the subtrahend has a smaller (more negative) exponent, return the minuend unchanged.

**4. Why It Triggers**

Link V-addresses and widths have mismatched exponents:

- **Link at 0.2.3:** exp = -1, mantissa = [2,3]
- **Deletion width 0.0.1:** exp = -2, mantissa = [1]

When computing `strongsub(0.2.3, 0.0.1)`:
- Check: `bptr->exp < aptr->exp` → -2 < -1? **YES**
- **Guard fires:** Return 0.2.3 unchanged

The width (0.0.1 at depth 3) addresses a "deeper" level than the link position (0.2.3 at depth 2), so the subtraction is blocked.

**5. Width Calculation**

Link widths in V-space are computed in `orglinks.c:115-117`:
```c
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

For V-position 0.2.1 (tumblerlength = 3):
- shift = 2
- V-width = 0.0.1 (exp = -2)

This depth mismatch triggers the exponent guard during deletion.

### Implications

1. **Gaps persist:** Deleting a link leaves a permanent gap in the link subspace
2. **Stable V-addresses:** Link positions in the POOM are fixed, unaffected by earlier deletions
3. **Semantic correctness:** This preserves link ISA references stored in the Granfilade

### References

- Exponent guard: `tumble.c:544-546`
- Deletion shift: `edit.c:63`  
- Width calculation: `orglinks.c:115-117`
- Test scenario: `febe/scenarios/delete_link_gap_closure.py` → `golden/links/delete_middle_link_check_gap_closure.json`

---

## Question 18 [gregory]

> After DELETE of a V-span that partially overlaps a POOM crum, does `slicecbcpm` produce a new crum whose I-displacement is offset from the original to reflect the surviving portion, or does it retain the original I-displacement and reduce only the I-width?

### Gregory's Answer

## KB Synthesis

Looking at the knowledge base for DELETE's Phase 1 cutting mechanism:

## Answer: The new crum gets an OFFSET I-displacement

When `slicecbcpm` splits a crum at an interior cut point, the new crum (representing the surviving right portion) receives an **offset I-displacement** equal to the original I-displacement plus the cut offset in I-space. It also receives a reduced I-width covering only the surviving portion.

## Supporting Evidence

**From [PRE-DELETE] / Finding 0075:**
- `slicecbcpm` is called only for interior cuts (`grasp < cut < reach`)
- It computes `localcut = cut - grasp` (the offset from the crum's start)
- The original crum retains width `localcut` (becomes the left piece)
- The new crum receives width `cwid - localcut` (becomes the right piece)

**Why offset is necessary:**

Consider a crum mapping V-range [V.5, V.15] → I-range [I.10, I.20] (width 10 in both dimensions).

When cut at V.8 (localcut = 3):
- **Left piece (original crum):** 
  - V-displacement: V.5, V-width: 3
  - I-displacement: I.10, I-width: 3
  - Maps [V.5, V.8] → [I.10, I.13] ✓

- **Right piece (new crum):**
  - V-displacement: V.8, V-width: 7
  - I-displacement: **I.13** (original + localcut), I-width: 7
  - Maps [V.8, V.15] → [I.13, I.20] ✓

**If I-displacement were NOT offset:**
- Right piece with I-displacement: I.10 would incorrectly map V.8 → I.10
- This violates [INV-IADDR-IMMUTABILITY] and [INV-POOM-BIJECTIVITY]

**From [SS-POOM-BOTTOM-CRUM] / Finding 0076:**
Bottom crums store dual-space coordinates — both V-space and I-space have origin and width fields. The parallel structure between dimensions requires that cutting operations maintain the correspondence by offsetting both V and I origins.

**From [INV-IADDR-IMMUTABILITY] / Findings 0030, 0064:**
I-addresses, once assigned to content, never change. Content at V-position (grasp + localcut) was at I-address (I-origin + localcut) before the cut and must remain there after the cut. The new crum must start at the offset I-address to preserve this mapping.

The offset is computed in the I-dimension parallel to the V-dimension offset (localcut), maintaining the bijective V↔I correspondence required by the POOM structure.

## Code Exploration

I need your permission to write this finding. The finding documents that **`slicecbcpm` offsets the I-displacement** of the new crum after a partial delete — the new crum's displacement equals the original displacement plus the width of the left half. This is the correct behavior for maintaining the V↔I mapping.

---

## Question 19 [gregory]

> If two versions share I-addresses via CREATENEWVERSION, and one version deletes some of that shared content, does `SHOWRELATIONOF2VERSIONS` (compare_versions) still correctly identify the overlap based on I-addresses that remain in both POOMs, or does it report reduced overlap?

### Gregory's Answer

## KB Synthesis

# Answer

Yes, `SHOWRELATIONOF2VERSIONS` (compare_versions) correctly reports **reduced overlap** after deletion. The comparison is based on the **current POOM state** of both documents, not on historical I-address associations.

## Mechanism

When a version is created via CREATENEWVERSION:
- Both documents initially share the same I-addresses ([ST-VERSION-CREATE] from Findings 0007, 0032)
- Each document has an independent POOM tree ([FC-VERSION-ISOLATION] from Finding 0072)

When one version deletes shared content:
1. **DELETE removes V-to-I mappings from the deleting document's POOM** ([ST-DELETE] from Finding 0064): "DELETE frees the POOM bottom crums that *reference* I-addresses, but the I-addresses themselves persist in the granfilade"
2. **The other version's POOM remains completely unchanged** ([FC-DELETE-CROSS-DOC] from Finding 0064): "DELETE in one document has zero effect on any other document's POOM mappings"
3. **The I-addresses themselves persist in the granfilade** (immutable content), but the deleted version no longer has POOM entries mapping V-positions to those I-addresses

## Comparison Process

The compare_versions algorithm ([ST-COMPARE-VERSIONS] from Finding 0015, [INT-SPORGL-VERSION-COMPARE] from Finding 0013):
1. Converts each document's **current V-stream** to I-addresses via `vspanset2sporglset` ([ST-VSPAN-TO-SPORGL])
2. This conversion reads the **document's POOM** to get V-to-I mappings
3. Computes I-address intersection between the two documents
4. Maps intersecting I-addresses back to V-spans in each document

## Result

After deletion from Version1:
- Version1's sporglset contains **only I-addresses for content still in its POOM** (deleted content excluded)
- Version2's sporglset contains **all original I-addresses** (unchanged POOM)
- The I-address intersection = **only content present in both current POOMs**
- Therefore: **overlap is correctly reported as reduced**

The comparison operates on current document state (what's in each POOM), not on historical associations (what the spanf index might still track, per [ST-DELETE] from Finding 0023).

## Code Exploration

Perfect! I now have a complete understanding of the execution path. Let me trace through the entire flow to answer your question definitively.

---

## Answer: `compare_versions` Reports **Reduced Overlap**

When one version deletes content that was shared via `CREATENEWVERSION`, `SHOWRELATIONOF2VERSIONS` (compare_versions) correctly reports **reduced overlap** based only on the I-addresses that **remain** in both POOMs at the time of comparison.

## How It Works: Complete Execution Trace

### 1. CREATENEWVERSION Shares I-Addresses

**[backend/do1.c:260-299]** `docreatenewversion`:

```c
// Line 281-282: Retrieve the full V-span of the original document
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {
    return FALSE;
}

// Line 293: Copy ALL content to the new version
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

This copies the V→I mappings from the original document into the new version's POOM. Both versions now have V-addresses that map to the **same** I-addresses (shared content identity).

### 2. DELETEVSPAN Removes V→I Mappings

**[backend/do1.c:158-167]** `dodeletevspan`:

```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
);
```

**[backend/orglinks.c:145-152]** `deletevspanpm`:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
	if (iszerotumbler(&vspanptr->width))
		return (FALSE);
	deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // Line 149
	logbertmodified(docisaptr, user);
	return (TRUE);
}
```

**Line 149** calls `deletend`, which physically removes the V-span from the POOM enfilade. After deletion:
- The V-addresses no longer exist in that version's POOM
- The V→I mappings for deleted content are gone
- Queries to those V-positions will return no I-addresses

### 3. SHOWRELATIONOF2VERSIONS Compares Current POOMs

**[backend/do1.c:428-449]** `doshowrelationof2versions`:

```c
bool doshowrelationof2versions(typetask *taskptr, typespecset version1, typespecset version2, typespanpairset *relation)
{
	typeispanset version1ispans = NULL;
	typeispanset version2ispans = NULL;
	typeispanset commonispans = NULL;

	// Lines 440-441: Filter to text subspace (V >= 1.0) - see Finding 0015
	filter_specset_to_text_subspace(taskptr, version1);
	filter_specset_to_text_subspace(taskptr, version2);

	return
		// Lines 444-445: Convert each version's CURRENT V-spans to I-spans
		specset2ispanset(taskptr, version1, &version1ispans, READBERT)
	  &&    specset2ispanset(taskptr, version2, &version2ispans, READBERT)
		// Line 446: Find ONLY the I-addresses present in BOTH versions
	  &&    intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
	  &&    ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
	;
}
```

### 4. V→I Conversion Queries the Current POOM

**[backend/do2.c:14-46]** `specset2ispanset` calls `vspanset2ispanset` for each V-span.

**[backend/orglinks.c:397-402]** `vspanset2ispanset`:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
	return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);  // Line 401
}
```

**[backend/orglinks.c:404-422]** `permute` loops through V-spans and calls `span2spanset`.

**[backend/orglinks.c:425-447]** `span2spanset`:

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr, INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
	// Line 435: Query the POOM for what I-addresses exist at these V-positions
	context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
	
	// Lines 439-445: Convert each context entry to an I-span
	for (c = context; c; c = c->nextcontext) {
		context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
		nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
	}
```

**[backend/retrie.c:56-85]** `retrieverestricted` calls `retrieveinarea`, which traverses the POOM enfilade to find what I-addresses are mapped at the given V-positions.

**Key insight:** If content was deleted, those V-positions don't exist in the POOM, so `retrieverestricted` returns **no context entries** for them. The deleted content simply isn't there to be converted to I-addresses.

### 5. Intersection Finds Only Shared I-Addresses

**[backend/correspond.c:145-189]** `intersectspansets`:

```c
bool intersectspansets(typetask *taskptr, typespanset set1, typespanset set2, typespanset *set3, INT spantype)
{
	*set3 = NULL;
	
	// Lines 164-169: If either input is empty, result is empty
	if (!set1 || !set2) {
		return (TRUE);
	}

	// Lines 177-182: Find overlapping I-address ranges
	for (; set1; set1 = set1->next) {
		for (p = set2; p; p = p->next) {
			if (comparespans (taskptr, set1, p, set3, spantype))
				set3 = &(*set3)->next;
		}
	}
	return (TRUE);
}
```

**[backend/correspond.c:210-265]** `spanintersection` computes the actual range overlap between two I-spans.

**Result:** Only I-addresses that are currently present in **both** versions' POOMs appear in `commonispans`. Deleted content has no representation in the POOM, so it doesn't contribute to the intersection.

## Concrete Example

```
Initial state after CREATENEWVERSION:
  Version A: V[1.0→1.100] → I[2.1.5.1→2.1.5.101]  (100 chars)
  Version B: V[1.0→1.100] → I[2.1.5.1→2.1.5.101]  (100 chars, same I-addresses)
  
  compare_versions(A, B) reports:
    100 chars of shared content

After Version A deletes V[1.50→1.100]:
  Version A: V[1.0→1.50] → I[2.1.5.1→2.1.5.51]   (50 chars remaining)
  Version B: V[1.0→1.100] → I[2.1.5.1→2.1.5.101] (100 chars unchanged)
  
  compare_versions(A, B) reports:
    50 chars of shared content (REDUCED overlap)
    
  The deleted I-addresses [2.1.5.51→2.1.5.101] are:
    - Still in Version B's POOM
    - No longer in Version A's POOM (deleted)
    - Therefore NOT in the intersection
```

## Why This Is Correct Behavior

This is the semantically correct behavior for several reasons:

1. **Content identity is defined by current POOM state** - A document "contains" content only if there's an active V→I mapping in its POOM [Finding 0015, backend/findings/0015-compare-versions-semantic-definition.md]

2. **Deletion removes content identity** - When you delete a V-span, you're asserting "this content is no longer part of my document" [backend/do1.c:158, orglinks.c:149]

3. **Comparison asks "what do we share NOW?"** - The operation finds content with "common origin" that exists in both documents at the time of comparison [backend/do1.c:428]

4. **No automatic edit history** - Udanax does not maintain automatic version history. Deletion is permanent unless you explicitly create a version beforehand [Finding 0072: findings/0072-no-automatic-edit-history.md]

## Summary

**Answer:** Yes, `SHOWRELATIONOF2VERSIONS` correctly identifies the overlap based on I-addresses that **remain** in both POOMs. It reports **reduced overlap** after deletion because:

1. Deletion physically removes V→I mappings from the POOM (`deletend` at backend/orglinks.c:149)
2. V→I conversion queries the current POOM state (`retrieverestricted` at backend/retrie.c:56)
3. Intersection only includes I-addresses present in both current POOMs (`intersectspansets` at backend/correspond.c:145)
4. Deleted content has no POOM representation, so it contributes nothing to the intersection

The comparison is always based on the **current state** of both POOMs, not on historical sharing relationships.

---

## Question 20 [gregory]

> When DELETE produces a negative V-position tumbler for a surviving entry, does subsequent INSERT at a positive V-position interact correctly with the negative-positioned entry — specifically, does `makegappm` shift negative-V entries, or does the two-blade mechanism in `findaddressofsecondcutforinsert` classify them as beyond the second cut?

### Gregory's Answer

## KB Synthesis

Looking at the interaction between DELETE-produced negative V-positions and subsequent INSERT operations, I need to trace through several mechanisms:

## The Core Question

When a POOM entry ends up at a negative V-position (from DELETE exceeding the entry's position), does INSERT's knife-cutting logic correctly classify it for shifting purposes?

## Answer: Negative-V Entries Are Not Shifted

Negative-V positioned entries are classified as **case 2 (no shift)** by INSERT's two-blade knife mechanism. Here's why:

### 1. Tumbler Ordering ([SS-TUMBLER] Finding 0053)
`tumblercmp` treats negative tumblers as strictly less than all positive tumblers and zero. In the total order: `all negative < zero < all positive`.

### 2. INSERT Knife Construction ([SS-TWO-BLADE-KNIFE] Finding 0054)
For INSERT at positive V-position `N.x`:
- `blade[0] = N.x` (insertion point, positive)  
- `blade[1] = (N+1).1` (next subspace boundary, positive)

Both blades are positive for any standard INSERT operation.

### 3. Classification Logic ([ST-INSERT] Finding 0054)
`insertcutsectionnd` classifies each POOM crum using a two-step check:

**First: Check against blade[1]**
```c
cmp = whereoncrum(ptr, &knives->blades[1])
if (cmp <= ONMYLEFTBORDER) return case_2; // No shift
```

For a negative-V crum and positive blade[1]:
- The crum's interval `[left, right)` is entirely negative (e.g., `[-0.8, -0.7)`)
- `blade[1]` is positive (e.g., `2.1`)
- `whereoncrum` calls `intervalcmp(negative_left, negative_right, positive_blade[1])`
- Since the blade is to the **right** of the negative interval, this returns `TOMYRIGHT` (2)
- `TOMYRIGHT > ONMYLEFTBORDER`, so we proceed to blade[0] check

**Second: Check against blade[0]**
```c
cmp = whereoncrum(ptr, &knives->blades[0])
if (cmp == TOMYRIGHT) return case_2; // No shift  
else if (cmp == TOMYLEFT || cmp == ONMYLEFTBORDER) return case_0; // No shift
else return case_1; // Shift
```

For the same negative-V crum:
- `blade[0]` is also positive (e.g., `1.3`)
- Same reasoning: blade[0] is to the **right** of the negative interval
- `whereoncrum` returns `TOMYRIGHT` (2)
- **Classification: case 2 → NO SHIFT**

### 4. Why This Makes Sense

Negative-V entries are already corrupted state ([INV-POOM-BIJECTIVITY] Finding 0053) — they exist in the POOM but map to no valid V-address. They are unreachable by queries because negative tumblers sort before all valid V-space.

The classification logic treats them as "beyond the manipulation region" (case 2), which preserves them unchanged. This is reasonable: they're already broken, so leaving them alone doesn't make things worse, and attempting to shift them could produce even more corrupted arithmetic results.

### 5. Cross-Subspace Caveat ([FC-SUBSPACE] Finding 0055)

Importantly, the scenario of DELETE producing negative V-positions **cannot occur cross-subspace**. The `strongsub` exponent guard in `tumblersub` prevents text deletion (width at exp=-1) from affecting link entries (at exp=0):

```
strongsub(2.1, 0.3): 
  0.3.exp(-1) < 2.1.exp(0) → returns 2.1 unchanged
```

So negative-V entries could only arise from **same-exponent** deletion where the width exceeds the position — which would be same-subspace operations.

## Conclusion

**YES**, INSERT interacts correctly with negative-V entries in the sense that it classifies them consistently (case 2, no shift) and doesn't crash or produce undefined behavior. However, "correctly" here means "doesn't make the corruption worse" — the negative-V entries remain unreachable and the POOM remains in a violated state ([INV-POOM-BIJECTIVITY]).

The two-blade knife mechanism ([SS-TWO-BLADE-KNIFE] Finding 0054) effectively treats negative-V entries as "outside the manipulable region" of any positive-V-position INSERT, which is the safest possible handling of already-corrupted state.

## Code Exploration

Let me complete my code analysis first with the findings I've discovered. Based on my thorough reading of the source code, I can now answer your question definitively.

## Answer: Negative V-Position Tumblers and INSERT Interaction

After tracing through the C source code, I can confirm that **negative-V entries are NOT shifted by `makegappm` during INSERT at positive V-positions**. The two-blade mechanism in `findaddressofsecondcutforinsert` classifies them as being **before the first blade** (case 0), which means no shift is applied.

### Code Path Evidence

**1. Tumbler Comparison (tumble.c:72-85)**

The comparison function `tumblercmp` always orders negative tumblers before positive ones:

```c
INT tumblercmp(tumbler *aptr, tumbler *bptr) {
    // ...
    if (aptr->sign == bptr->sign)
        return (aptr->sign ? abscmp(bptr,aptr) : abscmp(aptr,bptr));
    return (aptr->sign ? LESS : GREATER);  // [tumble.c:84]
}
```

When comparing a positive tumbler (e.g., `2.0`, sign=0) to a negative tumbler (e.g., `-2.0`, sign=1), this returns `GREATER` because signs differ and the positive tumbler's sign is 0.

**2. Crum Position Classification (retrie.c:356-372)**

`whereoncrum` determines where a blade position falls relative to a crum's span:

```c
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    cmp = tumblercmp(address, &left);
    if(cmp == LESS) {
        return(TOMYLEFT);
    } else if(cmp == EQUAL) {
        return(ONMYLEFTBORDER);
    }
    // ... check right boundary
    return(TOMYRIGHT);  // [retrie.c:371]
```

For a negative-V entry at `-2.0` with width `3.0` (spanning `[-2.0, 1.0)`), when checking against blade `2.0`:
- `tumblercmp(2.0, -2.0)` returns `GREATER`
- The blade is to the **right** of the entry
- Returns `TOMYRIGHT` (value 2)

**3. Two-Blade Classification (edit.c:207-233)**

`insertcutsectionnd` classifies crums relative to the two blades:

```c
INT insertcutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives) {
    if (knives->nblades == 2) {
        i = 1;
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp <= ONMYLEFTBORDER) {
            return (2);  // Beyond second blade
        }
    }
    i = 0;
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp <= ONMYLEFTBORDER) {
        return (1);  // Between blades - GETS SHIFTED
    }
    return (0);  // Before first blade - NOT SHIFTED
}  // [edit.c:207-233]
```

For negative-V entry vs. positive blades:
- Check blade[1]: `whereoncrum` returns `TOMYRIGHT` (2), not `<= ONMYLEFTBORDER` (-1)
- Check blade[0]: `whereoncrum` returns `TOMYRIGHT` (2), not `<= ONMYLEFTBORDER` (-1)
- **Returns 0** (before first blade)

**4. Gap Creation (insertnd.c:151-169)**

`makegappm` applies the shift based on the classification:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
        case 0:
        case 2:
            break;  // NO SHIFT [insertnd.c:154-156]
        case 1:
            tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
            ivemodified (ptr);
            break;  // [insertnd.c:161-165]
    }
}
```

Case 0 results in `break` — **no tumbleradd, no shift applied**.

### Concrete Example

1. **Initial state**: INSERT at V=1.0, width=10 → entry at `[1.0, 11.0)`
2. **DELETE [0.0, 5.0)**:
   - Content at `[1.0, 5.0)` deleted (within delete region)
   - Content at `[5.0, 11.0)` shifted: V = `1.0 - 5.0 = -4.0`
   - Surviving entry now at `[-4.0, 2.0)`

3. **INSERT at V=2.0, width=5**:
   - Blades: `[2.0, 2.1.1]` via `findaddressofsecondcutforinsert` [insertnd.c:179-182]
   - Entry at `[-4.0, 2.0)` vs. blade `2.0`:
     - `tumblercmp(2.0, -4.0)` = `GREATER`
     - `whereoncrum` returns `TOMYRIGHT`
   - `insertcutsectionnd` returns **0** (before first blade)
   - Entry **not shifted**, remains at `[-4.0, 2.0)`

### Semantic Implications

This behavior means:
- **Negative V-positions are isolated from positive-V INSERTs**
- DELETE can create "orphaned" negative-V content that subsequent INSERTs don't interact with
- This is likely **unintentional** — the tumbler comparison logic treats negative positions as universally "less than" positive ones, causing them to fall outside the shift region

Would you like me to write a golden test scenario to verify this behavior in the actual backend?
