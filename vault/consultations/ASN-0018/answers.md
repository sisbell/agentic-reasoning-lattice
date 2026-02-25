# Consultation Answers — Concurrent Operation Ordering

**Inquiry:** What must the system guarantee about the result when multiple operations modify the same or overlapping content simultaneously? What determines the final state and what invariants must the resolution satisfy?
**Date:** 2026-02-25 13:30
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When two users simultaneously insert content at the same position within a shared document, must the system guarantee a single deterministic ordering of those insertions visible to all readers?

### Nelson's Answer

# Concurrent Insertion Ordering: Nelson's Answer Is Architectural, Not Algorithmic

## The Short Answer

No. Nelson does not specify a deterministic ordering guarantee for simultaneous insertions by multiple users into the same document — because **his architecture prevents the scenario from arising**. In Xanadu, documents have a single owner, and only the owner may modify a document. The question presupposes shared mutable state that Nelson's design deliberately excludes.

## The Ownership Invariant

Nelson is unambiguous:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." [LM 2/29]

This is not an access control policy layered on top of the system — it is the fundamental ownership model. INSERT, DELETE, REARRANGE, APPEND, and COPY-into all require ownership of the target document. There is no mechanism for granting write access to non-owners.

## What Happens When Two People Want to Edit the Same Content

Nelson's answer is **forking, not merging**:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

The session-model design intent captures this precisely:

**Writing always succeeds.** If you cannot modify the original, you create a version. In conventional systems, access denial is an error. In Xanadu, denial is a fork. The user gets a version.

The CREATENEWVERSION operation makes this concrete:

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

So if Alice owns document D, and both Bob and Carol want to modify D:

1. Bob creates version D-bob (CREATENEWVERSION of D), then modifies his copy
2. Carol creates version D-carol (CREATENEWVERSION of D), then modifies her copy
3. D remains untouched — Alice's original is preserved
4. D-bob and D-carol are independent documents with independent owners
5. No conflict arises because no mutable state is shared

## No Concurrency Specification

Nelson explicitly leaves concurrency mechanics unspecified. The session-model analysis identifies five gaps:

- **No OPEN/CLOSE operations** — Nelson's 17 commands establish no session state on a document
- **No read vs. write modes** — you own it (modify freely) or you do not (create a version)
- **No locking protocol** — no mention of concurrent editing of the same document
- **No session lifecycle** — no connect/authenticate/disconnect sequence
- **No access control lists** — only owner/designees/everyone; no per-user grants

The single reference to concurrent users is about *search*, not editing:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." [LM 4/59]

## Why the Architecture Makes This Unnecessary

Nelson's design has three properties that eliminate the concurrent-insertion problem:

**1. Single writer per document.** Only the owner modifies. No two users ever write to the same V-space.

**2. I-space is append-only.** Content creation adds to I-space; it never modifies existing I-space addresses. Two users creating content simultaneously produce bytes at different I-addresses (under their respective accounts). There is no collision.

**3. Versioning replaces merging.** Nelson explicitly rejects the notion of a privileged "main" version:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

Without a canonical "main" version that multiple writers converge on, there is nothing to order deterministically.

## The V-Space Insert Operation

For completeness, here is what Nelson specifies about INSERT:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

This is a sequential description of a single operation on a single document by its owner. Nelson specifies no atomicity guarantees, no ordering constraints relative to other operations, and no conflict resolution — because in his model, only one person can issue this command against any given document.

## What Nelson DOES Guarantee About Multi-User Scenarios

The guarantees that matter across users are about **reading and linking**, not concurrent writing:

- **Anyone can read** any published document [LM 2/42]
- **Anyone can link to** any published document [LM 2/43]
- **Links survive editing** — because they attach to I-space bytes, not V-space positions [LM 4/42]
- **Correspondence is computable** across versions via shared I-space origin [LM 2/20]

These guarantees work precisely because each document has a single owner-writer. The web of connections between documents (links, transclusions, versions) is what creates the collaborative fabric — not shared editing of a single document.

## Summary

| Question | Nelson's Position |
|----------|-------------------|
| Can two users write to the same document? | No — single owner only |
| What if a non-owner wants to modify? | They create a version (fork) |
| Is there a merge/conflict resolution model? | No — versions coexist independently |
| Is there a locking protocol? | Not specified |
| Is there a deterministic insertion ordering? | Not needed — no concurrent writes to same document |
| How do multiple viewpoints coexist? | Through versions, transclusions, and links |

The architectural answer to "must the system guarantee a single deterministic ordering?" is that Nelson designed the system so the question never arises. Collaboration in Xanadu happens through **linking and versioning across independently owned documents**, not through concurrent modification of shared mutable state.

NEED_RAW: 4/59, 4/65-4/67 — to verify there is no concurrent-access language in the FEBE command specifications beyond what the curated sources capture.

---

## Question 2 [nelson]

> If one operation deletes a span of content while another operation concurrently creates a link to that same span, must the link survive and continue to reference the original content?

### Nelson's Answer

# Yes — The Link Must Survive

The answer follows directly from three architectural principles that Nelson specifies explicitly. No special concurrency handling is needed because the operations cannot conflict at the level that matters.

## 1. DELETE Does Not Destroy Content

DELETE removes content from V-space (the document's current arrangement) but leaves I-space (permanent storage) untouched.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes still exist. They are merely no longer part of the current view.

## 2. Links Attach to I-Space Content, Not V-Space Positions

Links reference the permanent identity of bytes, not their ephemeral position in any document's current arrangement.

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

The survivability diagram on 4/43 states:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

## 3. I-Space Content Is Permanent — The Condition Is Always Satisfied

The "if anything is left at each end" condition is always met because I-space content never disappears:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

From the storage model:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

I-space is append-only. Bytes are never removed. The I-space address of deleted content remains valid and resolvable forever.

## Putting It Together

The two operations work in different spaces that do not interfere:

| Operation | What It Affects | What It Does NOT Affect |
|-----------|----------------|------------------------|
| **DELETE** | V-space arrangement | I-space content |
| **MAKELINK** | Creates link pointing to I-space addresses | Does not depend on V-space arrangement |

The link's endsets point to I-space byte addresses. The DELETE operation touches only V-space. These are orthogonal — the link's targets are unaffected by the deletion regardless of timing or ordering.

## The Deeper Point

Nelson designed this to be the case. The entire I-space/V-space separation exists precisely so that connections survive editing:

> "Links point to I-space → survive editing. Edits change V-space → don't destroy content." (from the i-space-v-space concept)

The scenario you describe — concurrent deletion and link creation — is not a special case requiring special handling. It is the **normal case** that the architecture was built to handle. Every edit is a V-space operation. Every link is an I-space reference. They operate in different planes.

## What Nelson Does Not Specify

Nelson does not address concurrency mechanics directly. There is no locking protocol, no session model, and no discussion of simultaneous operations on the same content. But the question resolves without needing any concurrency specification, because the two operations cannot conflict architecturally. The link references bytes that DELETE cannot reach.

---

## Question 3 [nelson]

> Must every modification to a document produce a distinct, permanently retrievable version, even when multiple modifications arrive simultaneously?

### Nelson's Answer

# Does Every Modification Produce a Distinct Version?

**No.** Nelson draws a clear distinction between two different concepts that are often conflated: **named versions** (deliberate forks with their own tumbler addresses) and **historical states** (any past arrangement, reconstructable on demand from the chronological change log). Not every modification creates a new named version. But every modification is captured permanently, and any prior state can be retrieved.

## The Two Axes: Version and Time

The evidence for this distinction is structural. Nelson separates version identity from temporal tracking:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately."
> — [LM 4/18]

Versions have tumbler addresses. Time does not. This means temporal states and named versions are different coordinates. You navigate them independently:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version **at a given time**, it comes to your screen."
> — [LM 2/15]

Note the phrasing: "a given version **at a given time**." You specify both. A version is a named entity; a time selects a historical state within that version's evolution. If every modification automatically produced a new named version, there would be no need to specify time separately from version.

## Named Versions Are Deliberate Acts

The FEBE protocol treats version creation as an explicit, separate operation:

> **CREATENEWVERSION**: "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry."
> — [LM 4/66]

This is a deliberate fork — it creates a **new document** whose tumbler address encodes its lineage. It is not triggered automatically by INSERT, DELETE, or REARRANGE. Those editing operations modify the current document's V-space arrangement without spawning new version identities.

The editing operations are listed separately and described without any mention of automatic versioning:

> "FEBE includes instructions for insertion in a document, deletion from a document, and rearrangements of unlimited size. These are conceptually simple."
> — [LM 4/61]

INSERT shifts V-stream addresses. DELETE removes spans from V-space (while I-space content persists). REARRANGE transposes regions. None of these descriptions mention creating new versions as a side effect.

## What Happens Instead: Append-Only Accumulation

Modifications don't create versions — they **accumulate** in the append-only store:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically."
> — [LM 2/14]

Every change adds to I-space; nothing is overwritten. The system tracks the sequence of changes, enabling reconstruction of any past arrangement on demand. This is the "part-pounce" mechanism:

> "We call this pounce. You pounce like a cat on a given thing, and it seems to be there, having been constructed while you wait, as it were, in midair."
> — [LM 2/16]

Content at any historical moment is **reconstructed from fragments**, not retrieved from a pre-stored snapshot. The system doesn't need to create a discrete version for every edit because it can reconstruct any state from the chronological record.

## The Ongoing Braid Metaphor

Nelson's metaphor reinforces continuous evolution, not discrete snapshots:

> "A document is really an evolving ONGOING BRAID."
> — [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex."
> — [LM 2/15]

The braid is continuous. You can examine it at any point along its length (time), but the named strands (versions) are the deliberate forks, not the individual twists.

## Simultaneous Modifications

Nelson does not address this scenario directly, and it is largely moot in his architecture for two reasons:

**First, single ownership constrains concurrent editing.** Only the document owner can modify it:

> "Only the owner has a right to withdraw a document or change it."
> — [LM 2/29]

Multiple users cannot simultaneously edit the same document. If someone else wants to modify your work, they create their own version — a separate document at their own address.

**Second, the append-only model serializes naturally.** Changes "flow into the storage system, filed, as it were, chronologically." Even rapid successive modifications by the same owner are serialized by the append mechanism. Each change lands in I-space in sequence. No special versioning ceremony is needed because the chronological record itself is the history.

Nelson explicitly left concurrency mechanisms unspecified. The session model design intent notes that there is no locking protocol and no mention of concurrent editing of the same document in Literary Machines. The FEBE protocol is stateless at the command level — commands name documents by tumbler address and execute.

## Summary

| Concept | What It Is | How Created |
|---------|-----------|-------------|
| **Named version** | A new document with its own tumbler address, encoding ancestry | Deliberately, via CREATENEWVERSION |
| **Historical state** | Any past arrangement of a document, reconstructable on demand | Automatically, via append-only accumulation |
| **Edit operation** | A modification to the current V-space arrangement | INSERT, DELETE, REARRANGE, APPEND |

The guarantee is not "every modification produces a version" but rather **"every modification is captured, and any prior state can be reconstructed."** Named versions are deliberate landmarks in the document's continuous evolution; the append-only store preserves the full history between them.

---

## Question 4 [nelson]

> When overlapping edits target the same content within a document, must the system preserve every user's contributed content without silent loss, or may one edit supersede another?

### Nelson's Answer

# Overlapping Edits: Nelson's Architecture Sidesteps the Problem

The question presupposes a scenario that Xanadu's architecture is designed to make impossible. Nelson's answer is unambiguous: **no content is ever silently lost**, but this is achieved not through conflict resolution but through structural prevention of conflicts in the first place.

## Single-Owner Documents Prevent Edit Conflicts

Only the document owner may modify a document. This is a hard guarantee, not a policy:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." [LM 2/29]

There is no mechanism in FEBE for two users to issue competing edits against the same document. The 17 commands Nelson specifies establish no session state, no locking protocol, and no concurrent editing model. As the session-model analysis notes: "Nelson's model is: you own it (modify freely) or you do not (create a version)."

## Non-Owners Fork, They Don't Collide

When someone other than the owner wants to modify content, they create their own version — a separate document that transcludes the shared material:

> "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion." [LM 2/37, from windowing concept]

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

The result: Alice's document and Bob's version are **independent documents** sharing I-space content. Their edits cannot overlap because they are editing different V-space arrangements.

## Even the Owner Cannot Silently Lose Content

When the owner edits, the I-space/V-space separation guarantees nothing is destroyed:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

DELETE is a V-space operation only. The permanent I-space content is untouched:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every previous arrangement remains recoverable:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

## The Deeper Principle: Writing Always Succeeds

The fundamental design principle is that denial of modification is never a dead end — it is a fork:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

If you cannot modify the original, you create a version. Your version is a first-class document with its own address, its own owner, and its own V-space arrangement over shared I-space content. Nothing is lost; it simply exists in a different place.

## Summary

| Scenario | What Happens |
|----------|-------------|
| Two users edit same document | **Cannot occur.** Only owner can modify. Non-owner creates a version. |
| Owner's edit removes content | **V-space only.** I-space content permanent. Previous versions recoverable. |
| Two versions diverge from same source | **Independent documents.** No conflict — different V-space, shared I-space. |
| Links to edited content | **Survive.** Links point to I-space, which is immutable. |

Nelson's system does not need conflict resolution because it prevents conflicts structurally. One edit cannot supersede another because edits by different users always target different documents. And within a single owner's editing, the append-only I-space and version history guarantee that **every byte ever contributed is permanently preserved**, even if a particular V-space arrangement no longer includes it.

---

## Question 5 [nelson]

> Does the system guarantee that the identity of any content byte remains stable regardless of how many concurrent operations attempt to rearrange or copy the surrounding material?

### Nelson's Answer

# Yes — By Architectural Design, Not Concurrency Protocol

The system guarantees byte identity stability through the immutability of I-space itself, which renders the concurrency question moot at the identity level.

## The Core Guarantee

Every content byte receives a permanent I-space address at creation. That address never changes, and the content at that address never changes. This is not a policy — it is the architecture:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The storage model is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

## Why Concurrent Operations Cannot Affect Identity

All editing operations — INSERT, DELETE, REARRANGE, COPY — operate on **V-space** (the document's current arrangement), never on **I-space** (where bytes permanently live):

| Operation | V-space effect | I-space effect |
|-----------|---------------|----------------|
| INSERT | Adds mapping; shifts V-addresses after insertion point | New bytes appended (never overwrites) |
| DELETE | Removes mapping from current view | **None** — bytes remain forever |
| REARRANGE | Reorders V→I mappings | **None** |
| COPY | Creates new V-space mapping to **existing** I-addresses | **None** — shares identity with source |

Nelson is explicit that V-space positions shift freely while I-space identity holds:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

And:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

That quote refers to V-addresses — the position in the current arrangement — which may indeed change constantly. But the I-address (permanent identity) is immutable.

## COPY Specifically Preserves Identity

The COPY operation is transclusion, not duplication. It creates a V-space reference to existing I-space content:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The copy **shares I-addresses with the source**. No new I-space content is created. Ten thousand concurrent COPYs of the same paragraph all point to the same permanent bytes.

## The Enfilade Guarantee

The data structures themselves were designed to maintain canonical order through arbitrary changes:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

## What Nelson Does NOT Address

Nelson does not specify concurrency control for **V-space operations**. If two users simultaneously INSERT at the same V-space position in the same document, the system must resolve the ordering — but this is a V-space consistency question, not an identity question. The curated session-model source confirms:

> Nelson does not specify a session model. [...] No locking protocol — no mention of concurrent editing of the same document.

Nelson acknowledges future concurrent use:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." [LM 4/59]

But he leaves the mechanics of concurrent write resolution unspecified.

## Summary

**The identity of any content byte is guaranteed stable** — not through a concurrency protocol, but through the more fundamental guarantee that I-space is append-only and immutable. No operation in the system can alter or reassign an I-space address. The question "what happens with concurrent operations?" reduces to: many operations may simultaneously change V-space arrangements, but since none of them can touch I-space, byte identity is invariant by construction.

The principle is architectural, stated plainly on [LM 2/14]: content is filed chronologically into append-only storage. Once a byte exists at an I-address, it exists there permanently, regardless of what any number of concurrent operations do to the V-space arrangements that reference it.

---

## Question 6 [nelson]

> If two users simultaneously transclude the same passage into different documents, must both transclusions independently reflect any concurrent edits to the original passage?

### Nelson's Answer

# Transclusion, Editing, and the Two Window Modes

The short answer is: **it depends on the window mode chosen**, and the two transclusions are completely independent of each other. But the deeper answer reveals something important about how Xanadu handles this.

## I-Space Is Immutable

The foundation here is that I-space content never changes:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When Carol "edits" her document, she is not changing I-space bytes. She is changing her document's **V-space arrangement** — the mapping from display positions to permanent I-space addresses. New bytes she types get new I-space addresses. Bytes she "deletes" are removed from V-space but remain permanently in I-space.

So "edits to the original passage" really means: Carol's V-space arrangement has changed. The I-space bytes that Alice and Bob transcluded still exist, unchanged, at their permanent addresses.

## The Two Window Modes

Nelson explicitly provides two modes for transclusion, and this is where the answer hinges:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

**Location-fixed (floating in time):** Both Alice's and Bob's transclusions would independently resolve against Carol's *current* V-space arrangement. If Carol edits, both see the update. Nelson says this solves the distributed update problem:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

**Time-fixed:** Both transclusions would continue showing the passage as it existed when the window was created. Neither reflects Carol's edits until the user explicitly asks.

## Independence of the Two Transclusions

The two transclusions are completely independent. Alice's window into Carol's document and Bob's window into Carol's document have no knowledge of or dependency on each other. Each is a separate V-space mapping in a separate document, independently resolving against Carol's content.

There is no coupling mechanism between them. They don't need to "agree" or synchronize. Each independently follows the same rules:

- If location-fixed: each independently resolves to Carol's current arrangement
- If time-fixed: each independently shows the state at its own creation time

Alice could even use a location-fixed window while Bob uses a time-fixed window. They would then see different things — Alice sees Carol's latest version, Bob sees the version at the time he created his transclusion.

## Ownership Constrains "Concurrent Edits"

One important clarification: only Carol can edit Carol's document.

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

So "concurrent edits to the original passage" really means Carol's own sequential edits. If Alice or Bob want to make changes, they create their own versions:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

## Summary

| Scenario | Alice sees edit? | Bob sees edit? | Independent? |
|----------|-----------------|----------------|--------------|
| Both location-fixed | Yes, automatically | Yes, automatically | Yes — each resolves independently |
| Both time-fixed | No, until she asks | No, until he asks | Yes — each has its own freeze point |
| Alice location-fixed, Bob time-fixed | Yes | No | Yes — different modes, different behavior |

The design guarantees that transclusion is always reference, never copy. Both transclusions point through to the same underlying content. Whether they "reflect edits" is a function of the window mode, not of any interaction between the two transclusions themselves. The system provides the choice; the users decide.

---

## Question 7 [nelson]

> Must the system assign unambiguous authorship and ownership to each fragment of content that results from resolving simultaneous modifications by different users?

### Nelson's Answer

## Answer: Simultaneous Modification and Unambiguous Ownership

The question presupposes a scenario — simultaneous modification by different users producing merged fragments — that Nelson's architecture prevents by design. The system never produces ambiguously-owned content because it never allows the conditions that would create it.

### Single-Owner Modification Is an Architectural Invariant

Nelson's ownership model is absolute and non-negotiable:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Only the owner may INSERT, DELETE, REARRANGE, or COPY-INTO a document. There is no concept of shared write access to the same document. Two users cannot simultaneously modify the same document because only one person owns it.

### I-Space Makes Authorship Structurally Unambiguous

Every byte created in Xanadu receives a permanent I-space address encoding its origin:

```
Node.0.User.0.Document.0.Element
```

The User and Document fields identify who created the bytes and in which document. This is not metadata that could become ambiguous during a merge — it is the address itself. As the origin-traceability design intent notes: "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses."

There is no mechanism in Nelson's specification for bytes that lack a single, unambiguous home document.

### Nelson Does Not Address Concurrent Editing

The session-model design intent file is explicit: Nelson specifies **no locking protocol** and makes **no mention of concurrent editing of the same document**. His 17 FEBE commands establish no session state. The question of "what happens when two users edit simultaneously" simply does not arise in the architecture as specified.

The closest Nelson comes to acknowledging multiple simultaneous users is about search optimization, not editing:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." [LM 4/59]

### The Architectural Answer to Collaboration Is Versioning, Not Merging

When someone other than the owner wants to modify content, Nelson's answer is not shared editing but **versioning by inclusion**:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

Each user creates their own document. Each document has a single owner. Each byte created belongs unambiguously to its home document. There is no merge step and therefore no merge-produced fragments requiring ownership assignment.

Nelson makes this architectural choice explicit:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

Alternative versions coexist as parallel documents, each owned by their respective creators. Correspondence between versions is tracked through shared I-space origins, but each version's *new* content belongs unambiguously to its creator.

### Summary

The system does not need to assign authorship to merge-resolution fragments because:

1. **Only the owner modifies a document** — simultaneous modification cannot occur
2. **Every byte gets a permanent I-address encoding its creator** — authorship is structural, not assignable
3. **Collaboration produces parallel versions, not merged documents** — each version has one owner
4. **Nelson specifies no concurrency protocol** — the scenario is outside the design space

The answer to the question as posed is: the scenario does not arise. But the deeper architectural commitment is clear — **yes, every fragment of content must have unambiguous ownership**, and the system guarantees this by making ownership an inherent property of the I-space address, not a label that could become ambiguous through operational conflict.

---

## Question 8 [nelson]

> When concurrent operations produce a conflict over document structure, must the resolution satisfy the invariant that no content ever added to the system becomes unreachable or unaddressable?

### Nelson's Answer

# Concurrent Conflicts and the Unreachability Invariant

## Short Answer

Yes. The invariant that no content ever added becomes unreachable or unaddressable is an absolute architectural requirement. It follows necessarily from multiple independently stated principles. However, Nelson does not directly address concurrent conflict resolution because the architecture is designed to make destructive conflicts structurally impossible.

## The Invariant Is Explicit

Nelson states the permanence guarantee directly:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This is not qualified by "unless there's a conflict" or "under normal conditions." It is stated as an absolute property of the addressing system.

The append-only storage model reinforces this:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

In an append-only system, there is no operation that removes content from I-space. Conflicts over V-space arrangement cannot affect I-space permanence because the two spaces are architecturally independent.

## Why Concurrency Cannot Violate the Invariant

The I-space/V-space separation is the key. Concurrent operations affect **V-space arrangements** (which document shows what content in what order), but I-space content is immutable once written:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Even DELETE — the most destructive-seeming operation — only affects V-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" means not in the current V-stream — but still present in I-space, still recoverable through historical backtrack, still reachable by their permanent I-address.

## Nelson's Model: Conflict Produces Forks, Not Errors

Nelson does not specify a concurrency protocol — no locking, no session lifecycle, no OPEN/CLOSE operations. But the architectural response to conflicts is clear from the ownership and versioning model:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

When two parties want to modify the same document structure, the resolution is **forking**: each party gets their own version. The session model document synthesizes this principle:

> "Writing always succeeds. In conventional systems, access denial is an error. In Xanadu, denial is a fork. The user gets a version."

This is supported by ownership semantics:

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

If you are the owner, you modify your document. If you are not, you create a version. There is no scenario where two parties have simultaneous write authority to the same V-space arrangement, because ownership is singular and structural (encoded in the tumbler address).

## The Enfilade Guarantee

At the data structure level, the enfilade system maintains canonical order through all operations:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

"Canonical order" after every operation is an internal mandate — meaning the data structure is always in a valid state. There is no intermediate state where content becomes unreachable due to a partially applied operation.

## The Network Consistency Model

For distributed operations across servers, Nelson describes an incremental assimilation model:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

Each server is "at all times unified and operational" — meaning every incremental update leaves the server in a valid state. Content migration between servers is additive (improving the map), not destructive.

## What Nelson Does Not Address

Nelson does not specify:

- A locking protocol for concurrent access to the same document
- What happens if two operations arrive simultaneously at the back end
- How the enfilade handles concurrent modifications at the data structure level
- Whether operations are serialized or can execute in parallel

NEED_RAW: [4/59, 4/75-4/79] — Nelson mentions a "barrel-roll shared search model" for concurrent users (4/59) and unimplemented features (4/79) that may contain relevant constraints.

## Conclusion

The invariant holds absolutely. It is not a design choice that competes with other goals — it is a structural consequence of the architecture:

1. **I-space is append-only** — no operation removes content
2. **Addresses are permanent** — no operation invalidates an address
3. **V-space edits don't affect I-space** — arrangement changes cannot make content unreachable
4. **Conflicts produce forks, not errors** — competing modifications create versions, not corrupted states
5. **Enfilades maintain canonical order** — every operation leaves the system in a valid state
6. **Servers are always operational** — distributed updates are incremental and non-destructive

Any conflict resolution mechanism an implementation introduces must satisfy these constraints. A resolution that made content unreachable would violate the permanent address guarantee [LM 4/19], the append-only storage model [LM 2/14], and the non-destruction principle [LM 2/45] simultaneously.

---

## Question 9 [nelson]

> Must the system guarantee that the sequence of versions for a document forms a single linear history, or may concurrent modifications produce branching version histories that later require explicit merging?

### Nelson's Answer

# Branching Version Histories in Xanadu

Nelson's design **explicitly permits and encourages branching version histories**. A single linear history is not required. However, **merging is not specified** — the model is diverge-and-compare, not diverge-merge-converge.

## Branching Is a First-Class Feature

Nelson treats alternative versions as co-equal with historical versions. There is no privileged "main branch":

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

The system lists "alternative versions" alongside "historical backtrack" as distinct capabilities:

> "It is a system for the rapid delivery of linked documents (which may share material) and the assimilation and storage of changes. System facilities permit promiscuous linkage and windowing among all materials; with special features for alternative versions, historical backtrack and arbitrary collaging." [LM 3/4]

And the versioning problem itself is framed as managing concurrent alternatives:

> "We often have to keep similar files organized in several different ways: for instance, the same program set up for different computers. Or it is desirable to maintain several possible designs or plans at once. These are examples of the versioning problem." [LM 3/12]

## The Tumbler System Naturally Produces Trees

The forking mechanism that generates version addresses is inherently tree-structured. Document 1.2.3 can fork into versions 1.2.3.1, 1.2.3.2, 1.2.3.3, and each of those can fork further:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." [LM 4/20]

CREATENEWVERSION reflects this tree structure:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The word "ancestry" (not "predecessor") implies a tree.

## Version Numbers Don't Even Enforce Derivation

Nelson makes a striking statement that the version numbering is even looser than a strict tree:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

This means document 1.2.3.1 does not *necessarily* derive from 1.2.3 in any strict genealogical sense — the tumbler hierarchy is organizational, not genealogical. The system is more flexible than even a tree would imply.

## Multiple Users Naturally Produce Branches

Nelson explicitly supports "versioning by inclusion" — anyone can create their own version of someone else's document:

> "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion."

Since only the owner can modify a document [LM 2/29], but anyone can create a version [LM 2/45], concurrent independent versions are the natural and expected outcome.

The session model design intent in the curated sources reinforces this: "In conventional systems, access denial is an error. In Xanadu, denial is a fork. The user gets a version." Concurrent modification doesn't produce conflicts — it produces branches.

## Comparison Without Merging

Nelson provides powerful tools for **comparing** branches but specifies no mechanism for **merging** them:

**Comparison tools:**
- SHOWRELATIONOF2VERSIONS — "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]
- Correspondence tracking — "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]
- Highlighting differences — "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." [LM 3/13]

**No merge mechanism:**
- No MERGE operation in the 17 FEBE commands
- No discussion of conflict resolution
- No concept of combining divergent V-space arrangements

If you want to combine two versions, the Xanadu way is to create a *new* version that transcludes from both:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

## The Prismatic Metaphor

Nelson's chosen metaphor for the version system is a prism — light refracting into multiple beams:

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another." [LM 2/19]

A prism produces divergence, not convergence. Content refracts into multiple simultaneous arrangements. This is the intended mental model.

## Summary

| Question | Answer |
|----------|--------|
| Must versions form a linear history? | **No.** Alternative versions are explicitly co-equal. |
| Can concurrent modifications branch? | **Yes.** Forking is the fundamental mechanism; denial-as-branching is the design intent. |
| Is merging specified? | **No.** The model provides comparison (SHOWRELATIONOF2VERSIONS, correspondence) but no merge operation. |
| How do you combine branches? | Create a new version that transcludes from both, using inclusion links. |
| Is there a "main" branch? | **No.** "There is no 'basic' version." |

The Xanadu version model is: **diverge freely, compare precisely, combine by transclusion — never merge destructively.**

---

## Question 10 [nelson]

> If simultaneous operations each modify content that is shared across multiple documents through transclusion, must every document referencing that content converge to a consistent view of the resolved state?

### Nelson's Answer

# The Question Dissolves Under Xanadu's Architecture

The short answer: **the scenario as described cannot arise.** Xanadu's I-space/V-space separation makes "modifying shared content" a category error. What is shared (I-space) is immutable; what is mutable (V-space) is never shared. Consistency is guaranteed structurally, not through convergence.

## Why the Premise Doesn't Hold

Transclusion in Xanadu means that multiple documents' V-spaces reference the **same I-space addresses**. But I-space is append-only and immutable:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every editing operation in FEBE either **adds new bytes to I-space** (INSERT, APPEND) or **modifies a single document's V-space arrangement** (DELETE, REARRANGE, COPY). None of them alter existing I-space content:

- **INSERT** — creates new I-space bytes, updates the inserting document's V-space
- **DELETE** — removes from V-space only; "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)" [LM 4/9]
- **REARRANGE** — pure V-space operation
- **COPY** — creates a V-space mapping to existing I-space content (this IS transclusion)

As Nelson states:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

## The Two Things That Could Be "Shared"

### 1. I-Space Content (Truly Shared, But Immutable)

When Document B transcludes content from Document A, both documents' V-spaces map to the same I-space addresses. Those addresses are permanent:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Since I-space content never changes, all documents referencing those addresses will always retrieve the same bytes. There is nothing to converge because there is nothing to diverge.

### 2. V-Space Arrangement (Mutable, But Never Shared)

Each document has its own V-space arrangement. Editing Document A changes only Document A's V-stream. Document B's V-space is completely independent — it is owned by B's owner, and only B's owner can modify it [LM 2/29].

> "Every document has an owner... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Even two users editing the **same** document simultaneously would not produce a convergence problem. Nelson's architecture handles this through forking:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals." [LM 2/45]

The session model design intent confirms: "Writing always succeeds. If you cannot modify the original, you create a version." Nelson specifies no locking protocol and no concurrent-edit merging — denial produces a branch, not a conflict.

## What About Location-Fixed Windows?

Nelson describes two windowing modes:

> "A quotation—an inclusion window—may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

A location-fixed window tracks the source document's V-space arrangement. If Document A rearranges or deletes content, Document B's location-fixed window reflects the change. But this is a **front-end display concern**, not a storage-level consistency problem. The underlying I-space content hasn't changed — Document A has simply changed which I-space bytes its V-space maps to. Document B's window follows A's arrangement, and A's arrangement is controlled solely by A's owner.

Time-fixed windows are completely unaffected by any subsequent editing of the source.

## The Architectural Guarantee

The consistency guarantee is absolute and structural:

| Layer | Shared? | Mutable? | Consistency |
|-------|---------|----------|-------------|
| I-space (content) | Yes (via transclusion) | No (append-only) | Trivially consistent — immutable |
| V-space (arrangement) | No (per-document) | Yes (by owner) | No sharing → no conflict |

Every document that transcludes the same content will **always** see identical bytes at those I-space addresses, because those bytes can never be modified, only appended to. And every document's arrangement of those bytes is private to that document's owner.

Nelson's inter-server protocol reinforces this:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere." [LM 4/72]

Servers don't need to resolve conflicting states because I-space content is immutable across the entire docuverse. What moves between servers is content that was already permanent when created.

## Summary

Xanadu does not need a convergence protocol for shared content because it was designed so that convergence is never required. The I-space/V-space separation is not merely an implementation convenience — it is the architectural decision that makes this entire class of problems disappear. Content is permanent; arrangement is private. There is nothing shared and mutable, so there is nothing to converge.

---

## Question 11 [gregory]

> When two FEBE sessions issue INSERT at the same V-position in the same document, does the run-to-completion scheduling in `bed.c`'s `select()` loop guarantee a deterministic winner, and does the second INSERT see the shifted V-addresses produced by the first?

### Gregory's Answer

## KB Synthesis

## Concurrent INSERT at the Same V-Position

### 1. Does run-to-completion scheduling guarantee a deterministic winner?

Yes, with a precise qualification about what "deterministic" means.

[INV-ATOMICITY] (Finding 0042) establishes that `bed.c`'s event loop calls `xanadu(&task)` to completion for each request before returning to `select()`. There are no threads, no signal handlers that mutate state, and no preemption.

[INV-SEQUENTIAL-DISPATCH] (Finding 0042) adds the key detail: when `select()` returns with multiple FDs ready simultaneously, the loop iterates over them in FD order, calling `xanadu()` for each in turn. Session A's INSERT runs to total completion before Session B's INSERT begins.

The "winner" — whichever session runs first — is determined by FD iteration order, which is fixed for a given `select()` result. This is deterministic in the sense that the same FD ordering always produces the same execution sequence. It is not deterministic in the sense of being predictable from application logic, since OS `select()` readiness can vary.

### 2. Does the second INSERT see the shifted V-addresses produced by the first?

Yes, unconditionally. Because run-to-completion scheduling means Session B's INSERT executes only after Session A's INSERT has fully modified the POOM, B operates on the post-A state.

**What A's INSERT does to the POOM:**

[ST-INSERT] (Finding 0054) describes the two-blade knife: INSERT at V-position P constructs blades `[P, (N+1).1]` where N is the subspace digit. All POOM entries in `[P, (N+1).1)` are shifted right by A's insertion width W. Entries at or beyond the subspace boundary are unaffected [FC-SUBSPACE].

[ST-INSERT] (Finding 0030) states the full postcondition:
```
D'(v) = D(v)           if v < P
D'(v) = fresh(v)       if P ≤ v < P + W   (A's new content)
D'(v) = D(v - W)       if v ≥ P + W
```

**What B sees when it inserts at the same V-position P:**

When B executes its INSERT at V-position P, it reads the post-A POOM. V-position P in the post-A POOM is the gap before A's newly inserted content (since A's content was placed at P and the prior occupants were shifted to P+W).

This produces the LIFO behavior documented in [ST-INSERT] (Finding 0027):

```
After A inserts "First" at P:    document = "First[...original at P shifted...]"
After B inserts "Second" at P:   document = "SecondFirst[...original shifted further...]"
```

B's content prepends to A's content at position P. The second session does not "miss" A's insert — it inserts into the already-shifted state. V-position P in B's request refers to the current gap at P in the post-A POOM, not to any pre-A position.

### Formal Summary

| Property | Guarantee | Mechanism |
|---|---|---|
| Execution order | Deterministic by FD iteration | [INV-SEQUENTIAL-DISPATCH] |
| Atomicity of each INSERT | Complete before next begins | [INV-ATOMICITY] |
| Second INSERT sees first's shifts | Yes, operates on post-A POOM | [ST-INSERT] (Finding 0030, 0054) |
| Ordering of two same-position inserts | LIFO — later insert prepends | [ST-INSERT] (Finding 0027) |
| Cross-subspace isolation preserved | Yes, for both INSERTs | [FC-SUBSPACE] |

One subtle point: I-address allocation is also sequential. [SS-ADDRESS-SPACE] (Finding 0061) establishes that each INSERT queries `findpreviousisagr` for the current granfilade maximum and increments. B's INSERT queries after A's allocation has been committed, so B receives I-addresses strictly greater than A's — no collision is possible regardless of V-position overlap.

## Code Exploration

Now I have everything I need. Let me write the full answer.

---

## Concurrent INSERT at the Same V-Position in udanax-green

### 1. The Scheduling Model in `bed.c`

The backend is a **single-threaded event loop** with no preemption. The main loop in `bed.c:103–149`:

```c
for (;;) {
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {        // bed.c:118
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                ...
                xanadu(&task);               // bed.c:128
                ...
            }
        }
    }
}
```

`select()` returns a bitmask of all file descriptors with pending data [bed.c:111]. The inner `for` loop walks from `i=0` to `i=nfds` in strictly ascending integer order [bed.c:118]. Each call to `xanadu()` at [bed.c:128] runs to full completion before the next fd is checked. There is no preemption, no yielding, and no interleaving.

`xanadu()` itself [bed.c:153–172] processes exactly one complete request per call:

```c
int xanadu(typetask *taskptr) {
    ...
    if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);   // dispatch + execute handler
        sendresultoutput(taskptr);          // flush response
        ...
    }
    tfree(taskptr);
    ...
}
```

**Conclusion on scheduling**: Run-to-completion is guaranteed. One request is fully executed and its response flushed before the next fd is serviced. If sessions A and B both have pending INSERT messages when `select()` returns, the backend will process them sequentially, not concurrently.

---

### 2. Which Session "Wins"

The winner is **deterministic but structurally predetermined**: whichever session has the **lower file descriptor number** is processed first [bed.c:118–128]. File descriptors are allocated by the OS in ascending order as sessions connect via `accept()`. The first session to connect gets the lower fd and is always scheduled first when both have pending input in the same `select()` wakeup.

This is not a race in the typical sense — there is no nondeterminism between two simultaneous requests. The outcome is fixed by fd assignment at connection time.

---

### 3. The INSERT Handler: ACK Sent Before Execution

The `insert()` handler in `fns.c:84–98` has a notable ordering:

```c
void insert(typetask *taskptr) {
    typeisa docisa, vsa;
    typetextset textset;

    (void) getinsert(taskptr, &docisa, &vsa, &textset);  // fns.c:90 — read from pipe
    putinsert(taskptr);                                    // fns.c:91 — ACK sent FIRST
    if (!doinsert(taskptr, &docisa, &vsa, textset))       // fns.c:92 — then execute
        ...
}
```

The response (`putinsert`) is sent to the frontend **before** `doinsert()` modifies the data structures. The commented-out version above it [fns.c:69–82] used the safer `get → do → put` ordering. The live code inverts this to `get → put → do`.

---

### 4. The V-Address: Read from Wire, Never Translated

`getinsert()` in `get1.c:32–43` reads the V-address directly from the frontend's buffered byte stream:

```c
bool getinsert(typetask *taskptr, tumbler *docisaptr, tumbler *vsaptr, typetextset *textsetptr)
{
    ...
    if (!getvsa(taskptr, vsaptr))     // get1.c:41 — raw tumbler from protocol stream
        return(FALSE);
    return(TRUE);
}
```

The `vsaptr` contains whatever tumbler the frontend encoded in its FEBE message. This value was computed by the frontend at the time it composed the request, without knowledge of what other sessions might be doing.

---

### 5. `acceptablevsa` Is a Stub That Always Returns TRUE

Before the insertion is performed, `docopy()` in `do1.c:53–64` calls `acceptablevsa()`:

```c
return (
   specset2ispanset(...)
&& findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa(vsaptr, docorgl)          // do1.c:57
&& asserttreeisok(docorgl)
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)
...
```

`acceptablevsa()` in `do2.c:110–113`:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);      // do2.c:112 — unconditional stub
}
```

**It is a complete stub.** No bounds check, no validity test, no detection of V-address conflicts.

---

### 6. `insertpm` Uses the Raw V-Address Directly

`insertpm()` in `orglinks.c:75–134` takes the `vsaptr` and passes it into `insertnd()` as the V-dimension coordinate for the new POOM crum:

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
    ...
    for (; sporglset; ...) {
        ...
        movetumbler(vsaptr, &crumorigin.dsas[V]);   // orglinks.c:113
        ...
        insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V); // orglinks.c:130
        tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr); // orglinks.c:131
    }
    return(TRUE);
}
```

No lookup, no adjustment, no translation. The tumbler from the protocol message becomes the V-dimension origin in the POOM enfilade directly.

---

### 7. What Actually Happens at the POOM Level

`makegappm()` in `insertnd.c:124–172` is called for POOM enfilades (document address space). It cuts the POOM at the requested V-position and shifts crums to the right:

```c
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
        case 1:   /* insertnd.c:161 — crum is to the right of cut */
            tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]); // insertnd.c:162
            ivemodified(ptr);
            break;
    }
}
```

After session A inserts N characters at V-position P, every crum with V ≥ P has its displacement increased by N [insertnd.c:162]. The POOM now reflects that original content starting at P has moved to P+N.

When session B's INSERT is then processed with the **same original V-address P** (the value it sent in its message, computed before A executed):

- `makegappm()` cuts the POOM again at V-position P
- At this point, A's newly inserted content occupies P..P+N-1; original content is at P+N onward
- B's content is inserted at V-position P, pushing A's content upward

**Session B does NOT see the shifted V-addresses produced by session A.** It uses the V-address from its original message. The backend applies no operational transformation, no last-write-wins rewrite, no conflict detection. The two inserts compose in fd-order, and the second session's content lands at the original V-address regardless of the first session's shift.

---

### Summary

| Question | Answer | Citation |
|---|---|---|
| Is scheduling run-to-completion? | Yes — one `xanadu()` call completes fully before the next fd is touched | `bed.c:118–141` |
| Is the winner deterministic? | Yes — lowest fd number is processed first | `bed.c:118` |
| Is V-address validated against current doc state? | No — `acceptablevsa()` is an unconditional stub | `do2.c:110–113` |
| Is B's V-address translated to account for A's shift? | No — the raw tumbler from the protocol message is used | `get1.c:41`, `orglinks.c:113`, `insertnd.c:162` |
| Is there an ACK-before-execute quirk? | Yes — `putinsert()` fires before `doinsert()` | `fns.c:91–92` |

The net behavioral consequence: two sessions issuing INSERT at the same V-position P in the same document will have their content composed sequentially in fd order at that same V-address. The second session's content lands at P in the state left by the first session's insert — it is not "aware" of the shift, and the backend does not correct for it. There is no operational transformation and no error. The document becomes a superposition of both inserts at the same original position, with the second insert's content placed at (or interleaved with) the position that the first insert's content had just occupied.

---

## Question 12 [gregory]

> If session A issues DELETE on V-span [1.3,1.5] and session B issues INSERT at V:1.4 in the same document, does the final POOM state depend entirely on which operation the event loop processes first, with no merging or conflict detection?

### Gregory's Answer

## KB Synthesis

Yes. The final POOM state depends entirely on which operation the event loop processes first. There is no merging, conflict detection, or operational transformation of any kind.

## Serialization Mechanism

The backend uses a single-threaded event loop that processes operations via run-to-completion scheduling [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH]. When `select()` returns with both sessions' FDs ready, the loop iterates over file descriptors in order: session A's operation executes entirely before session B's (or vice versa), with no interleaving [INV-SEQUENTIAL-DISPATCH].

Each operation — including the multi-step DELETE (cut crums, shift POOM entries, rebalance) and INSERT (allocate I-addresses, update POOM, create DOCISPAN) — is fully atomic with respect to all other operations [INV-ATOMICITY].

## The Two Possible Outcomes Are Structurally Different

**DELETE [1.3,1.5] first, then INSERT at V:1.4:**

DELETE removes the content at V-positions [1.3,1.5) from the POOM and shifts all entries at V ≥ 1.5 left by the deletion width [ST-DELETE]. Session B's INSERT at V:1.4 then operates on the post-deletion document — V:1.4 now refers to what was originally at approximately V:1.5+. The new content is inserted between the shifted survivors, and the originally deleted bytes are permanently gone [INV-DELETE-NOT-INVERSE].

**INSERT at V:1.4 first, then DELETE [1.3,1.5]:**

INSERT places new content at V:1.4, shifting all entries at V ≥ 1.4 right by the insertion width [ST-INSERT]. The two-blade knife restricts the shift to within the text subspace [FC-SUBSPACE]. Session A's DELETE [1.3,1.5] then operates on this modified document — the range [1.3,1.5] now spans some of the pre-existing content and potentially some of the newly inserted content, depending on the inserted width. The DELETE removes whatever POOM crums fall within [1.3,1.5] in the current (post-insert) coordinates [ST-DELETE].

## No Merging or Conflict Detection

The system provides no mechanism for:

- **Operational transformation** — the backend has no knowledge that both sessions targeted the overlapping range.
- **Conflict detection** — no version vectors, timestamps, or sequence numbers are compared.
- **Merge resolution** — even CONFLICT_COPY, the closest analog, explicitly does not merge changes [EC-CONFLICT-COPY-NO-MERGE].

The BERT write-exclusivity protocol [INV-WRITE-EXCLUSIVITY] is intended to prevent this situation — at most one session should hold WRITEBERT for a document, blocking the other from writing. However, BERT enforcement is advisory rather than enforced at the mutation gate [INT-BERT-FEBE, EC-RESPONSE-BEFORE-CHECK]: the backend sends a success response before executing the `doXXX` operation, so even a session without WRITEBERT can submit a write that silently fails — or, if the BERT check is bypassed entirely, executes without restriction.

Assuming both sessions do hold write access (or bypass BERT), the FD iteration order within the `select()` loop is the sole determinant of the outcome [INV-SEQUENTIAL-DISPATCH]. The system is confluent only in the sense that the enfilade produces consistent results for a given serialization order [INV-ENFILADE-CONFLUENCE]; it provides no guarantee that the serialization order reflects any intended semantic combination of the two concurrent edits.

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## Does the final POOM state depend entirely on processing order, with no merging or conflict detection?

**Yes — with one structural safeguard that changes the scenario's preconditions.**

### 1. The event loop is strictly single-threaded. Operations are serialized by fd ordering, not by semantics.

`bed.c:103-149` implements the entire multi-user dispatch:

```c
for (;;) {
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {
        ...
    } else {
        for (i = 0; i <= nfds; i++) {           /* bed.c:118 */
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                ...
                xanadu(&task);                   /* bed.c:128 */
                ...
            }
        }
    }
}
```

`xanadu()` (`bed.c:153-172`) dispatches exactly one request to completion before returning:

```c
} else if (getrequest(taskptr, &request)) {
    (*requestfns[request])(taskptr);             /* bed.c:162 */
    sendresultoutput(taskptr);
```

There are no threads, no coroutines, no async operations. When `select()` returns multiple ready fds in a single pass, the inner `for` loop processes them one at a time in ascending fd order (`bed.c:118`). This is the only scheduling policy. **The state of the POOM after two operations is entirely determined by which fd was numerically lower at the moment `select()` returned.**

---

### 2. BERT (document open table) prevents two sessions from holding WRITEBERT on the same document version simultaneously — but does not resolve conflicts, it prevents them by forking versions.

Both `dodeletevspan` and `doinsert` require WRITEBERT access. Tracing the call chain:

- `dodeletevspan` [`do1.c:158-167`]:
  ```c
  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
  ```

- `doinsert` [`do1.c:87-123`] calls `docopy`, which calls `findorgl(..., WRITEBERT)` [`do1.c:60`].

`findorgl` [`granf1.c:17-41`] calls `checkforopen(isaptr, type, user)` and returns `FALSE` if the result is `<= 0`:

```c
if ((temp = checkforopen(isaptr, type, user)) <= 0) {
    if (!isxumain) {
        return FALSE;
    }
}
```

`checkforopen` [`bert.c:52-87`] scans the `berttable` hash for open entries on that document. The access matrix at `bert.c:45-51` shows:

```
type     Not Open  # Open READ   # Open WRITE
         !owned|owned  # conn==|conn!= # conn==|conn!=
WRITE      -1  |  0   #   -1  |   -1  # WRITE |  -1
```

If session B holds WRITEBERT on document D, and session A calls `checkforopen(D, WRITEBERT, connectionA)`: the loop finds a non-READBERT entry for a different connection (`bert->type != READBERT` → `foundnonread = TRUE`), and since `foundnonread` is true, returns `-1`. `findorgl` returns FALSE. The operation silently fails.

This means **the normal case blocks the scenario entirely**: only one session can hold WRITEBERT on a given document version. The second session's write calls fail at `findorgl`.

---

### 3. The OPEN protocol with BERTMODECOPYIF creates diverging versions — and those versions never merge.

`doopen` [`bert.c:264-322`] handles the case where a document is already held for WRITE by another session via `BERTMODECOPYIF`:

```c
case BERTMODECOPYIF:
    if (openState == -1) {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);
        addtoopen(newtp, connection, TRUE, type);
    } else if (type != WRITEBERT && openState != WRITEBERT) {
        incrementopen(tp, connection);
    } else {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);
        addtoopen(newtp, connection, TRUE, type);
    }
```

When session B tries to open a document already held WRITE by session A, `BERTMODECOPYIF` causes `docreatenewversion` to fork a new version for session B. From this point, sessions A and B work on **separate POOM trees**. Their operations never interact, and no conflict detection or merging occurs. The two versions simply diverge.

There is no code anywhere in the backend that:
- Transforms one session's operations relative to another's (no OT)
- Computes a merge of diverging POOM states
- Records vector clocks or timestamps per operation
- Compares pending operations from different sessions before execution

---

### 4. If the BERT check is bypassed or a document is accessed without a proper OPEN, order is the sole arbiter — and the second operation uses stale V-positions.

Here is a critical structural observation from `fns.c`. Both `insert` and `deletevspan` send success to the client **before** performing the mutation:

`deletevspan` [`fns.c:333-347`]:
```c
(void) getdeletevspan (taskptr, &docisa, &vspan);
putdeletevspan (taskptr);                          /* SUCCESS SENT FIRST */
if (!dodeletevspan (taskptr, &docisa, &vspan))
    fprintf(stderr,"deletevspan failed \n");
```

`insert` [`fns.c:84-98`]:
```c
(void) getinsert (taskptr, &docisa, &vsa, &textset);
putinsert (taskptr);                               /* SUCCESS SENT FIRST */
if (!doinsert (taskptr, &docisa, &vsa, textset))
    fprintf(stderr,"requestfailed in insert\n");
```

If `dodeletevspan` or `doinsert` fails internally (e.g., BERT check returns FALSE), the backend logs to `stderr` in debug builds and does nothing in distribution builds — but the client has already been told it succeeded. There is no error propagation back to the client for these operations.

If both operations somehow execute against the same live POOM tree (e.g., if a single session issues both, or if BERT is bypassed):

- The first operation (`dodeletevspan` or `doinsert`) executes against the POOM tree as it exists at the time of processing.
- `makegappm` [`insertnd.c:124-172`] shifts existing crum V-positions to open a gap. `deletend` [`edit.c:31-76`] cuts crums using the knife positions specified by the delete span, subtracting width from surviving crums at `edit.c:63`.
- The second operation uses V-positions that were valid when the client constructed the request, but that are now stale. After DELETE of [1.3, 1.5], the INSERT at V:1.4 would operate on a V-space where that position no longer exists or has shifted. There is no adjustment.

The outcome depends entirely on which fd had the lower index when `select()` returned at `bed.c:118`.

---

### Summary

| Property | udanax-green behavior |
|----------|----------------------|
| Concurrency model | Single-threaded `select()` event loop; one operation at a time [`bed.c:118-128`] |
| Scheduling policy | Ascending fd index order, no semantic priority [`bed.c:118`] |
| Cross-session write conflict | Blocked at OPEN: second writer gets a new version via `BERTMODECOPYIF` [`bert.c:264`] |
| Conflict detection at write time | None — `findorgl` returns FALSE, not a conflict notification [`granf1.c:22-38`] |
| Operational transformation | Not implemented anywhere |
| Post-fork merging | Not implemented anywhere |
| Client error on silent failure | None — `putX` before `doX` in `fns.c` means client gets success regardless [`fns.c:91`, `fns.c:340`] |

**The final POOM state depends entirely on which operation the event loop processes first.** BERT prevents the question from arising for the same document version (by forking instead of conflicting), but across versions or when BERT is bypassed, pure serial order determines outcome, with no merging and no conflict awareness at any layer.

---

## Question 13 [gregory]

> When two sessions each COPY overlapping I-address ranges into the same target document at the same V-position, does `isanextensionnd` coalesce the second copy's POOM entries with the first's if their I-addresses happen to be contiguous?

### Gregory's Answer

## KB Synthesis

## Short Answer

No, `isanextensionnd` will not coalesce the two copies when both target the same V-position — even if the I-addresses are numerically contiguous and come from the same source document.

---

## Mechanics

**`isanextensionnd` requires two simultaneous conditions** [ST-INSERT / Finding 0062, ST-VCOPY / Finding 0046]:

1. The incoming content's `homedoc` matches the existing crum's `homedoc` (I-address origin document)
2. The incoming content starts exactly where the existing crum ends — in **both** V-space and I-space simultaneously (`new.V_origin == crum.V_reach` AND `new.I_origin == crum.I_reach`)

---

## Why Same-V-Position Breaks Condition 2

**Operations are strictly sequential** [INV-SEQUENTIAL-DISPATCH / Finding 0042]. "Two sessions" means two COPYs running one after the other.

Trace with I-contiguous ranges from the same source doc (α₁..α₅ then α₆..α₁₀), both targeting V=P:

**After Session 1's COPY** — target POOM has:
```
[V=P, V=P+5) → [α₁..α₅]   homedoc = doc_A
```

**Session 2 COPYs α₆..α₁₀ to V=P:**

`insertcutsectionnd` classifies the existing crum [P, P+5) relative to blade[0]=P. Since the crum's grasp equals the insertion point, it falls in the shift region (case 1). After `makegappm` shifts it right by width 5:

```
[V=P+5, V=P+10) → [α₁..α₅]   (shifted)
```

Now `isanextensionnd` checks whether the new content (V=P, I=α₆) extends any existing crum:
- The only adjacent crum is [P+5, P+10)→α₁..α₅ with `V_reach = P+10` and `I_reach = α₆`
- Condition 2 requires `new.V_origin == crum.V_reach`, i.e., `P == P+10` — **FALSE**

A new, separate crum is created. Final POOM:

```
[V=P,   V=P+5)  → [α₆..α₁₀]  (Session 2, at lower V)
[V=P+5, V=P+10) → [α₁..α₅]   (Session 1, shifted right)
```

The **LIFO insertion semantics** [ST-INSERT / Finding 0027] invert the V-I relationship: Session 2's higher I-addresses (α₆..α₁₀) occupy lower V-positions than Session 1's lower I-addresses (α₁..α₅). `isanextensionnd` demands forward co-directionality in both dimensions — this cannot be satisfied when V-order and I-order are reversed.

---

## Condition 1: The `homedoc` Obstacle for Different Source Documents

If the two sessions copy from **different** source documents, condition 1 fails unconditionally [INV-IADDR-PROVENANCE / Finding 0046]: each I-address has exactly one native document, and COPY does not change that provenance. Numerical I-address contiguity across different source documents does not satisfy the `homedoc` match requirement.

---

## When Coalescing Does Occur

Coalescing would succeed if Session 2 instead targeted `V = P+5` (the end of Session 1's content):

- `whereoncrum([P, P+5), P+5)` → `ONMYRIGHTBORDER` → `makegappm` early-exit, no shift [PRE-INSERT / Finding 0062]
- `isanextensionnd`: `crum.V_reach = P+5 = new.V_origin` ✓ AND `crum.I_reach = α₆ = new.I_origin` ✓ AND same homedoc ✓
- Crum extends to [P, P+10) → [α₁..α₁₀] — single coalesced crum

---

## Summary

| Condition | Same V-position (both at P) | Sequential V-position (P then P+5) |
|-----------|----------------------------|-------------------------------------|
| Same homedoc | Possible | Possible |
| I-contiguous | Given by assumption | Given by assumption |
| V-contiguity for extension | **Fails** (LIFO reversal) | Satisfied |
| Coalesces? | **No** | Yes |

The obstacle is structural, not a question of homedoc or I-address contiguity: same-position COPY via LIFO semantics unavoidably inverts the V-I ordering, and `isanextensionnd` cannot bridge that inversion.

## Code Exploration

I now have all the information needed to give a complete, cited answer.

---

## Answer: Does `isanextensionnd` coalesce cross-session COPY entries at the same V-position?

**Short answer: No.** When two sessions COPY to the same V-position, `isanextensionnd` will not coalesce the second copy's POOM entries with the first's — even when the I-addresses are contiguous. Below is the complete trace proving why.

---

### The Call Chain from COPY to `isanextensionnd`

1. `fns.c:35` `copy()` → calls `docopy()`
2. `do1.c:53–65` `docopy()` calls `specset2ispanset()` then `insertpm()`:
   ```c
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
   && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
   ```
3. `do2.c:14` `specset2ispanset()` — converts VSPEC items to **ISPANID** items. The source-doc ISA is consumed during V→I translation via `vspanset2ispanset`, but the resulting items carry `itemid = ISPANID` and contain no docisa.
4. `orglinks.c:100–131` `insertpm()` loops over each ispanset item, calling `unpacksporgl()`:
   ```c
   unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
   ...
   insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
   ```
5. `sporgl.c:178–203` `unpacksporgl()` — two branches:
   - `ISPANID` path (always taken for COPY-from-VSPEC): **`tumblerclear(&infoptr->homedoc)`** [sporgl.c:183] → **homedoc = 0**
   - `SPORGLID` path: `movetumbler(&sporgladdress, &infoptr->homedoc)` [sporgl.c:187]
6. `insertnd.c:15` `insertnd()` → for POOM calls `makegappm()` [line 54] **before** `doinsertnd()` [line 57]
7. `doinsertnd()` → `insertmorend()` → `insertcbcnd()`
8. `insertnd.c:249–258` `insertcbcnd()` loops over existing bottom crums calling `isanextensionnd()`:
   ```c
   for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
       if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
           dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
           ...
       }
   }
   ```

---

### `isanextensionnd` — Two Guards, Both Must Pass

```c
// insertnd.c:301-309
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

**Guard 1 — homedoc match** [insertnd.c:305]: `infoptr->homedoc` must equal the existing crum's `c2dinfo.homedoc`.

Since both sessions go through `specset2ispanset` → `unpacksporgl` ISPANID path, both get `homedoc = 0`. Every POOM crum created this way also stores `homedoc = 0`. So **Guard 1 always passes** for any two COPY-from-VSPEC operations.

**Guard 2 — 2D reach == origin** [insertnd.c:308]: `lockeq(reach.dsas, originptr->dsas, dspsize(POOM))`.

`dspsize(POOM)` is defined as `DSPSIZEPM = 2` [wisp.h:26]:
```c
#define DSPSIZEPM 2
```

`lockeq` iterates over 2 tumblers [wisp.c:261–267]:
```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize)
{
    while (loxize--)
        if (!tumblereq (lock1++, lock2++))
            return(FALSE);
    return(TRUE);
}
```

`prologuend` computes `reach = offset+cdsp + cwid` in **both V and I** [retrie.c:334–339]:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

So `lockeq` requires `reach.dsas[V] == origin.dsas[V]` **and** `reach.dsas[I] == origin.dsas[I]`.

---

### Why Same-V-Position Inserts Cannot Coalesce

**The critical obstacle: `makegappm`.**

`makegappm` [insertnd.c:124–172] is called before `doinsertnd` for every POOM insert. It:
1. Cuts the enfilade at the insertion V-address
2. Calls `insertcutsectionnd` on each child crum
3. For crums whose V-address falls after the cut point (case 1), it adds the new V-width to their displacement [insertnd.c:162–164]:
   ```c
   case 1:
       tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
   ```

**Concrete scenario:**

- **Session 1** copies I-range `[iA, iA+w1]` to V-position `V0`. Creates crum₁:
  - `cdsp = (V0, iA)`, `cwid = (v₁, w1)`  where `v₁` = the computed V-width
  - absolute reach = `(V0+v₁, iA+w1)`

- **Session 2** then copies I-range `[iA+w1, iA+w1+w2]` — I-addresses are contiguous — also to V-position `V0`.
  1. `makegappm` fires for session 2's insert at V0. Crum₁ has V-address `V0 ≥ V0`, so its displacement is shifted: `crum₁.cdsp.dsas[V] += v₂` [insertnd.c:162]. Now crum₁ sits at `(V0+v₂, iA)` with reach `(V0+v₂+v₁, iA+w1)`.
  2. Session 2's insert origin = `(V0, iA+w1)`.
  3. `insertcbcnd` calls `isanextensionnd(crum₁, offset, origin=(V0, iA+w1), linfo)`:
     - Guard 1: `0 == 0` → passes ✓
     - Guard 2: `lockeq(reach=(V0+v₂+v₁, iA+w1), origin=(V0, iA+w1), 2)`:
       - V: `V0+v₂+v₁ ≠ V0` → **FAILS** ✗
  4. **No coalescing. A new crum₂ is created at `(V0, iA+w1)`.**

The V-dimension mismatch is structural: `makegappm` pushes all prior same-position content rightward before the new insert even arrives at `insertcbcnd`. The two crums end up adjacent in V-space (`V0` → `V0+v₂`), but the extension check requires `reach.V == origin.V`, not adjacency.

---

### When Cross-Session Coalescing *Can* Occur

Coalescing between two separate COPY invocations is only possible when the **second** session's V-origin happens to equal the **V-reach** of the first session's last crum — i.e., session 2 explicitly targets `V = V0 + v₁` — AND the I-addresses are simultaneously contiguous:

- Crum₁ reach: `(V0+v₁, iA+w1)` 
- Session 2 origin: `(V0+v₁, iA+w1)` ← must choose this V-address deliberately
- `lockeq`: both dimensions match → coalesces

In practice this happens naturally **within a single `insertpm` call** when the specset contains multiple contiguous ISPANID spans: after inserting the first span, `vsaptr` is advanced by `v₁` [orglinks.c:131]:
```c
tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
```
The second span's origin is then exactly at the first span's reach — coalescing fires.

But across independent COPY calls at the same V-position, `makegappm` always breaks the V-contiguity needed by `isanextensionnd`.

---

### Summary

| Condition | Result |
|-----------|--------|
| Guard 1 (`homedoc`): both sessions COPY-from-VSPEC | Always passes: `homedoc = 0` both sides [sporgl.c:183] |
| Guard 2 V-dimension: after `makegappm` shifts crum₁ | **Fails**: `reach.V = V0+v₂+v₁ ≠ V0 = origin.V` [insertnd.c:162, 308] |
| Guard 2 I-dimension: I-addresses are contiguous | Would pass if V-dimension also passed [insertnd.c:308] |
| **Overall coalescing** | **No** |

`isanextensionnd` does **not** coalesce the second copy's POOM entries with the first's when both insert at the same V-position. The `lockeq` call [insertnd.c:308] tests V and I reach together (`dspsize(POOM) = 2`, wisp.h:26), and `makegappm` [insertnd.c:54] guarantees the first crum's V-reach is displaced beyond the second insert's V-origin before the extension check ever runs.

---

## Question 14 [gregory]

> Does `makegappm` in `insertnd.c` shift ALL entries at or beyond the insertion point in a single tree walk, or could a concurrent cache eviction via `grimlyreap` leave the POOM in a partially-shifted state mid-operation?

### Gregory's Answer

## KB Synthesis

## `makegappm` Atomicity and Cache Eviction

The answer has two distinct parts: **in-memory operational correctness** and **crash-durability behavior**. They have different answers.

---

### In-Memory: Full Shift Completes Atomically

`makegappm` operates within the single-threaded run-to-completion event loop. From [INV-ATOMICITY] (Finding 0042):

> The `xanadu(&task)` call executes the entire operation — request parsing, state mutation, response sending, and memory cleanup — before returning to `select()`. There are no threads, no state-modifying signal handlers, and no preemption.

And from [INV-SEQUENTIAL-DISPATCH] (Finding 0042):

> Even when multiple frontends have requests ready simultaneously, the event loop processes them strictly sequentially.

`grimlyreap` is triggered by `ealloc` on allocation failure, which runs **synchronously within the operation's call stack**. It is not concurrent — it is a nested call occurring within the same sequential dispatch. No other FEBE operation can observe the POOM between the first and last shift applied by `makegappm`.

The shift itself is bounded by the two-blade knife [SS-TWO-BLADE-KNIFE] (Finding 0054): only POOM entries in `[blade[0], blade[1])` are shifted. The postcondition is:

```
∀ entry ∈ poom(doc) : blade[0] ≤ entry.vpos < blade[1] ⟹ entry.vpos' = entry.vpos + insert_width
```

This full postcondition is achieved before `xanadu()` returns.

---

### Crash-Durability: Partially-Shifted State IS Possible on Disk

Here the picture is different. `grimlyreap` writes modified crums to disk and frees them from the cache during `ealloc`. If, during `makegappm`'s tree walk:

1. Some crums have already been shifted and marked `modified = TRUE`
2. A subsequent allocation triggers `grimlyreap`
3. `grimlyreap` evicts **unvisited crums** (age ≥ OLD) and writes them to disk **before** `makegappm` has shifted them
4. The system then crashes

The on-disk state will contain a mix: some crums shifted, others not. This is explicitly documented in [EC-CRASH-MID-WRITE] (Finding 0059):

> If a crash occurs mid-write (e.g., after writing leaf and middle nodes but before updating the root), the on-disk enfilade enters an inconsistent state.

And [SS-DURABILITY-BOUNDARY] (Finding 0059):

> On crash/kill: only crums previously evicted by the grim reaper survive. Recent INSERTs still in cache are lost. ... No transaction log.

The system provides session-level durability (`writeenfilades()` at clean exit), not operation-level durability.

---

### RESERVED Crums: A Partial Mitigation

[FC-RESERVED-CRUM] (Finding 0071) documents that `grimlyreap` skips crums with `age == RESERVED`. The rebalancing machinery uses RESERVED to protect in-progress crums. However, the KB does not document whether `makegappm` specifically marks crums it is actively visiting as RESERVED during the shift walk. If it does not, `grimlyreap` could evict crums that are in the shift range but not yet reached.

---

### Summary

| Concern | Answer |
|---------|--------|
| Can another session observe a partially-shifted POOM? | **No** — single-threaded run-to-completion ([INV-ATOMICITY], [INV-SEQUENTIAL-DISPATCH]) |
| Does `grimlyreap` interrupt the logical walk? | **No** — it is synchronous within the same call stack |
| Can a crash leave partially-shifted state on disk? | **Yes** — `grimlyreap` can write unshifted crums to disk before `makegappm` reaches them ([EC-CRASH-MID-WRITE], [SS-DURABILITY-BOUNDARY]) |
| Is there a transaction mechanism preventing this? | **No** — no transaction log, no fsync, no atomic commit ([SS-DURABILITY-BOUNDARY]) |

The spec should model INSERT as presenting an atomic postcondition to other operations [INV-ATOMICITY], while separately noting that the durability guarantee is session-level only [SS-DURABILITY-BOUNDARY] — a crash mid-INSERT can leave disk state with a partially-applied shift, which is unrecoverable without a prior clean session exit.

## Code Exploration

---

## Answer: `makegappm` and `grimlyreap` — Atomicity and Partial-Shift Risk

### The Short Answer

**A concurrent `grimlyreap` causing a partially-shifted POOM is structurally impossible.** The displacement loop in `makegappm` allocates no memory — making it impossible for `grimlyreap` to fire during the shift phase — and the system is single-threaded with no preemptive concurrency anyway.

---

### 1. What `makegappm` actually does

`makegappm` [insertnd.c:124–172] operates in three sequential phases:

**Phase 1 — Cut** [insertnd.c:144–148]:
```c
movetumbler(&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
knives.dimension = V;
makecutsnd(fullcrumptr, &knives);
```
`makecutsnd` splits bottom crums that straddle the insertion point. It calls `createcrum` internally (via `slicecbcpm` → `createcrum` in ndcuts.c:80, and via `peelsoncorrectly` → `createcrum` in ndcuts.c:226). **This is the only part of `makegappm` that can trigger `grimlyreap`.**

**Phase 2 — Find intersection** [insertnd.c:149]:
```c
newfindintersectionnd(fullcrumptr, &knives, &father, &foffset);
```
`newfindintersectionnd` [ndinters.c:38–42] is a **stub**:
```c
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives, typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;
    clear(offset, sizeof(*offset));
}
```
It sets `father = fullcrumptr` (the root apex) and returns immediately. The old descending-traversal algorithm was commented out. No allocation, no `grimlyreap` exposure.

**Phase 3 — Displacement loop** [insertnd.c:151–168]:
```c
prologuend((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case 1:  /* beyond insertion point — shift */
        tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
        ivemodified(ptr);
        break;
      ...
    }
}
```

---

### 2. The displacement loop is allocation-free

Every function called inside the loop body:

| Call | Allocates? | Can trigger `grimlyreap`? |
|------|-----------|--------------------------|
| `findrightbro(ptr)` [genf.c:177–186] | No — pointer follow + `rejuvinateifnotRESERVED` (macro, sets age=NEW) | No |
| `insertcutsectionnd` [edit.c:207–233] | No — pure `whereoncrum` arithmetic | No |
| `tumbleradd` | No — in-place arithmetic | No |
| `ivemodified` [genf.c:522–544] | No — sets `modified=TRUE`, calls `rejuvinateifnotRESERVED` (a macro) | No |

`rejuvinateifnotRESERVED` [common.h:126]:
```c
#define rejuvinateifnotRESERVED(x) (((x)->age==RESERVED)?(int)(x):((x)->age = NEW))
```
A pure macro — no function call, no allocation.

`grimlyreap` [credel.c:106] is only reachable from `ealloc` [credel.c:75]:
```c
// credel.c:70-76 (inside ealloc's retry loop)
if (grimreaper == NULL){
    xgrabmorecore();
    continue;
}
grimlyreap();
```
Since the loop body never calls `ealloc` (directly or transitively), **`grimlyreap` is unreachable during the shift phase**.

---

### 3. The pre-loop `findleftson` is protected

The loop initializer `findleftson(father)` [genf.c:206–232] CAN trigger a disk read if children are not in memory:

```c
if (ptr->leftson == NULL) {
    if (ptr->sonorigin.diskblocknumber == DISKPTRNULL) {
        return(NULL);
    }
    reserve((typecorecrum*)ptr);   // <-- age = RESERVED
    inloaf(ptr);                   // disk read → varunpackloaf → createcrum → ealloc → grimlyreap possible
    if (oldage != RESERVED)
        rejuvinate((typecorecrum*)ptr);
}
```

`varunpackloaf` [corediskin.c:116–117] calls `createcrum` for each son read from disk:
```c
while (numberofsonstoread--) {
    ptr = (typecuc *)createcrum(height, enftype);
```

If `ealloc` fails during this, `grimlyreap` fires. But two protections hold:

1. **`father` is `reserve()`d** [genf.c:216] before `inloaf`. `isreapable` [credel.c:144] skips any `age == RESERVED` crum. The father cannot be reaped.
2. **Newly allocated sons have `age = NEW`** [credel.c:577: `ptr->age = NEW`]. `isreapable` [credel.c:176–179] returns FALSE when `age < OLD`. No freshly loaded child can be reaped before the loop even begins.

---

### 4. No concurrency exists

`grimlyreap` is **synchronous** and **cooperative** — not a concurrent background thread or async callback. The event loop [bed.c:103–148] is single-process, single-threaded, `select()`-multiplexed:

```c
// bed.c:103-148
for (;;) {
    select(...);
    for (i = 0; i <= nfds; i++) {
        if ((1<<i) & inputfds2) {
            xanadu(&task);  // one request at a time
        }
    }
}
```

The installed signal handlers [bed.c:70–73] (`SIGPIPE → crash`, `SIGHUP → crash`, `SIGXCPU → SIG_IGN`, `SIGINT → flagquitting`) do not invoke `grimlyreap` or touch the POOM. `flagquitting` only sets `quitafteruser = TRUE` or exits cleanly.

There is no mechanism — no thread, no signal, no timer — by which `grimlyreap` could preempt `makegappm`'s loop.

---

### 5. The `isreapable` cross-sibling guard (belt-and-suspenders)

Even in a hypothetical scenario where allocation somehow occurred mid-loop, `isreapable` [credel.c:250–258] checks **all siblings** before reaping any one of them:

For height-0 crums:
```c
for (p = weakfindleftmostbro(localreaper); p; p = p->rightbro) {
    if(p->age < OLD || p->age == RESERVED){
        return(FALSE);
    }
    ...
}
return(TRUE);
```

After the first case-1 shift, `ivemodified` calls `rejuvinateifnotRESERVED` on that sibling, setting its `age = NEW`. Since `NEW < OLD`, **any shifted sibling's NEW age would prevent `isreapable` from reaping any of its not-yet-shifted siblings** — a second barrier even if the first were somehow breached.

---

### Summary

`makegappm` shifts entries at or beyond the insertion point in what is effectively an **atomic single-pass loop**. The loop [insertnd.c:151–168] contains zero memory allocations. `grimlyreap` is a synchronous, cooperative reclaimer invocable only from `ealloc`, which is only reachable from `createcrum`. The loop never calls `createcrum`. The backend is single-threaded. There are no concurrent or async reapers. A partially-shifted POOM from a `grimlyreap` interruption is not possible.

---

## Question 15 [gregory]

> If session A performs REARRANGE (pivot) on V:[1.1,1.3,1.5] while session B simultaneously issues DELETE on V:[1.2,1.4], does the event loop's atomic processing of each operation guarantee that the second operation sees a fully consistent POOM from the first, with no interleaved crum modifications?

### Gregory's Answer

## KB Synthesis

Yes. The event loop guarantees this absolutely, with no caveats about crum modifications. Here is why:

## The Guarantee: Total Serialization

**[INV-ATOMICITY]** and **[INV-SEQUENTIAL-DISPATCH]** (both from Finding 0042) jointly establish the mechanism. The `bed.c` event loop uses `select()` to detect ready file descriptors and then calls `xanadu(&task)` for each ready FD **sequentially and to completion**:

```
select() → FD_A and FD_B both ready
→ Process A's REARRANGE: getrequest → rearrangend (all crum modifications) → sendresult → tfree
→ THEN process B's DELETE: getrequest → deletend → sendresult → tfree
```

There are no threads, no preemption, and no state-modifying signal handlers. This produces **total global serialization** — stronger than per-document locking. Session B's DELETE does not begin executing until session A's REARRANGE has returned from `xanadu()`.

## What This Means for the Specific Operations

**REARRANGE** (via `rearrangend` in `edit.c:78-160`) applies `tumbleradd` to each affected POOM crum's V-displacement, then calls `setwispupwards` and `recombine`. All of this — every displacement modification, every widdative summary update, every tree rebalancing step — completes before the event loop iterates to the next FD.

**[SS-POOM-MUTABILITY]** confirms the POOM is part of shared global state (not per-session), so session B's DELETE operates on the same POOM structure. But because of sequential dispatch, by the time `deletend` runs for session B, `rearrangend` has left the POOM in a fully settled state: V-positions have been arithmetically adjusted **[ST-REARRANGE]**, `setwispnd` has recalculated all relative displacements **[SS-ENFILADE-TREE]**, and `recombine` has completed any structural consolidation **[ST-REBALANCE-2D]**.

## Why PRE-CONCURRENT-INSERT Concerns Don't Apply Here

**[PRE-CONCURRENT-INSERT]** (Finding 0041) warns that concurrent unsynchronized insertion is unsafe because `adopt(new, RIGHTBRO, ptr)` modifies shared pointers and `father->numberofsons` can suffer lost updates. This concern is **rendered moot** by the sequential dispatch invariant — there is no actual concurrent execution. Finding 0041 states a structural risk that would exist if concurrency were permitted; **[INV-SEQUENTIAL-DISPATCH]** explains why it never is.

## Summary

Session B's DELETE sees a POOM that is fully consistent with the result of session A's REARRANGE, with no partial or interleaved state. The guarantee is unconditional: the event loop is single-threaded and processes operations one at a time to completion. This is a stronger guarantee than most concurrent systems provide — it is total global linearizability at the operation granularity, not merely per-document isolation.

## Code Exploration

---

## Answer: REARRANGE Atomicity — Event Loop Serialization Analysis

### Question Restated

If session A performs REARRANGE (pivot) on V:[1.1,1.3,1.5] and session B simultaneously issues DELETE on V:[1.2,1.4], does the event loop guarantee B sees a fully consistent post-rearrange POOM with no interleaved crum modifications?

**Yes — unconditionally, by structural design.** Here is the full chain of evidence.

---

### 1. The Process Is Single-Threaded: No Parallelism Exists

A search for `pthread`, `mutex`, `semaphore`, `atomic`, and `thread` across all C source files returns **zero threading primitives**. The grep across 52 source files finds only incidental matches (`clock`, `mightbeblocked`, comments). There is no `pthread_create`, no `pthread_mutex_t`, no `sem_t`, no `fork` per connection.

The backend is a single OS process. "Simultaneous" requests from two sessions are simultaneous only at the network level — they queue in the kernel socket buffers. The backend processes them one at a time.

---

### 2. The Event Loop: One Request at a Time to Completion

`bed.c:103-149` is the main loop:

```c
for (;;) {
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {           /* [bed.c:118] */
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];            /* [bed.c:120] */
                task.inp = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;
                ...
                xanadu(&task);                   /* [bed.c:128] */
                ...
            }
        }
    }
    leave(player, &n_players);                   /* [bed.c:145] */
    new_players(player, &n_players, FALSE, &task);
}
```

When `select()` returns, **all ready file descriptors are already captured in `inputfds2`** (a snapshot). The inner `for` loop then walks them in ascending fd order. For each ready fd, it calls `xanadu(&task)` **synchronously and to completion** before incrementing `i` to the next fd.

There is no `continue`, no early exit, no yield, no `poll()` re-entry within the inner loop. If session A has fd 3 and session B has fd 5 and both are ready in the same `select()` round, A's full request executes before B's fd is even examined.

---

### 3. `xanadu()` Is a Complete, Non-Yielding Dispatch

`bed.c:153-172`:

```c
int xanadu(typetask *taskptr)
{
    logstuff = FALSE;
    if (setjmp(frontendeof)) {
        dobertexit(user);
        player[user].wantsout = TRUE;
    } else if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);    /* [bed.c:162] — full dispatch */
        sendresultoutput(taskptr);
        if (request == QUIT) {
            player[user].wantsout = TRUE;
        }
    }
    tfree(taskptr);
    ...
}
```

The dispatch `(*requestfns[request])(taskptr)` at `bed.c:162` runs the entire request handler — get parameters, mutate data structures, send response — all in a single synchronous call stack. `xanadu()` does not return until the handler completes.

`setjmp(frontendeof)` at `bed.c:158` is the only non-linear path: it fires via `longjmp` in `frontenddied()` if the frontend disconnects mid-read. That path calls `dobertexit()` and marks `wantsout`, but it only triggers during `getrequest()` (reading the wire), not during POOM mutation.

---

### 4. The `rearrange` Handler Runs Atomically

From `fns.c:159-173` (the active implementation — the original check-then-respond version is commented out):

```c
void rearrange(typetask *taskptr)
{
    (void) getrearrange (taskptr, &docisa, &cutseq);
    putrearrange (taskptr);                          /* [fns.c:166] — response BEFORE mutation */
    if (!dorearrange (taskptr, &docisa, &cutseq))    /* [fns.c:167] */
        fprintf(stderr,"rearrange failed \n");
}
```

Note the ordering: the response is sent (`putrearrange`) **before** the POOM is actually mutated (`dorearrange`). But this doesn't break atomicity — `dorearrange` still runs synchronously to completion within `xanadu()`. No other session can observe the POOM mid-mutation.

`dorearrange` (`do1.c:34-43`) calls `rearrangepm`, which calls `rearrangend` (`edit.c:78-160`):

```c
int rearrangend(typecuc *fullcrumptr, typecutseq *cutseqptr, INT index)
{
    /* build knives from cutseq */
    sortknives (&knives);                            /* [edit.c:107] */
    makeoffsetsfor3or4cuts (&knives, diff);          /* [edit.c:108] */
    makecutsnd (fullcrumptr, &knives);               /* [edit.c:110] — split crums at cut points */
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
    prologuend ((typecorecrum*)father, &foffset, &fgrasp, NULL);
    for (ptr = (typecuc*)findleftson(father); ptr; ptr = ...) {
        i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
        switch (i) {
          case 1: case 2: case 3:
            tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]); /* [edit.c:125] */
            ivemodified((typecorecrum*)ptr);         /* [edit.c:127] */
            break;
        }
    }
    setwispupwards (father, 1);                      /* [edit.c:137] */
    recombine (fullcrumptr);                         /* [edit.c:139] */
    (void)splitcrumupwards(fullcrumptr);             /* [edit.c:141] */
}
```

Every step — cut positioning, crum offset adjustment, wisp recalculation, tree recombination, and final split — happens without returning to the event loop. All crum `.cdsp.dsas[index]` fields are updated before `rearrangend` returns.

---

### 5. `deletevspan` Then Sees a Fully Consistent POOM

After `xanadu()` returns for session A, the inner `for` loop reaches session B's fd. `deletevspan` dispatches to `dodeletevspan` (`do1.c:158-167`) → `deletevspanpm` → `deletend` (`edit.c:31-76`):

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    makecutsnd (fullcrumptr, &knives);               /* [edit.c:44] */
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
    ...
    for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
        switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 1:
            disown ((typecorecrum*)ptr);             /* [edit.c:59] — remove crum */
            subtreefree ((typecorecrum*)ptr);
            break;
          case 2:
            tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]); /* [edit.c:63] */
            break;
        }
    }
    setwispupwards (father, 1);                      /* [edit.c:74] */
    recombine (father);                              /* [edit.c:75] */
}
```

`deletend` calls `makecutsnd` and `newfindintersectionnd` on whatever POOM state currently exists in memory. Since `rearrangend` has fully completed — including `recombine(fullcrumptr)` at `edit.c:139` and `splitcrumupwards(fullcrumptr)` at `edit.c:141` — the POOM is in a consistent state when B's delete begins.

---

### 6. Signals Do Not Interrupt POOM Mutation

`bed.c:70-73` installs four signal handlers:

| Signal | Handler | POOM impact |
|--------|---------|-------------|
| `SIGPIPE` | `crash()` | Calls `exit(9)` — kills the process entirely |
| `SIGHUP` | `crash()` | Same |
| `SIGXCPU` | `SIG_IGN` | Ignored |
| `SIGINT` | `flagquitting()` | Sets `quitafteruser = TRUE` — checked only at `bed.c:129`, **after** `xanadu()` returns |

`flagquitting()` (`bed.c:175-188`) only touches the quit flag. It never accesses the POOM. If `SIGINT` fires during `rearrangend`, the mutation continues to completion, and `quitafteruser` is only checked after `xanadu()` returns. The POOM is not left in a torn state by any signal.

---

### Conclusion

The event loop in `bed.c` provides **total serialization** through a combination of:

1. **Single-threaded process** — no concurrent execution possible at any point
2. **`select()` + sequential `for` loop** (`bed.c:118-142`) — ready fds processed one at a time, in ascending fd order
3. **Non-yielding `xanadu()` dispatch** (`bed.c:162`) — each request runs from parse to completion before the next fd is examined
4. **`rearrangend` internal sequencing** (`edit.c:107-141`) — all crum modifications, tree rebalancing, and splits complete before returning
5. **Signal handlers that don't touch POOM** — `flagquitting` only sets a quit flag, checked post-`xanadu()`

Session B's DELETE on V:[1.2,1.4] **always** executes against the fully post-rearranged POOM. The word "simultaneously" describes what the two clients *experience* (their TCP connections deliver data around the same time), but the backend sees only a deterministic queue serialized by the `select()` loop. There is no race condition, no torn write, no partial crum state visible to the second operation.

---

## Question 16 [gregory]

> When two CREATELINK operations from different sessions target the same document, does `findnextlinkvsa` always return distinct link V-addresses because the second call sees the first link's POOM entry, or is there a race in the query-and-increment allocation?

### Gregory's Answer

## KB Synthesis

## Link V-Address Allocation Under Concurrent CREATELINK

**Short answer:** Yes, the two operations always receive distinct link V-addresses. There is no race, because the backend is fundamentally single-threaded.

---

### The Dispatch Architecture Eliminates the Race

[INV-ATOMICITY] establishes that the `bed.c` event loop dispatches each FEBE operation as a run-to-completion unit. The call `xanadu(&task)` parses the request, executes all internal steps (granf creation, `findnextlinkvsa`, `insertpm`, `insertendsetsinspanf`), sends the response, and frees working memory — all before returning to `select()`.

[INV-SEQUENTIAL-DISPATCH] reinforces this: even when multiple frontend file descriptors are simultaneously ready in `select()`'s result set, the loop iterates over them sequentially. Session A's CREATELINK runs to completion; only then does Session B's CREATELINK begin.

This means the window in which a race could occur — after Session A calls `findnextlinkvsa` but before it commits the new link to the POOM — simply cannot exist in this architecture.

---

### How `findnextlinkvsa` Allocates Correctly

[SS-LINK-SUBSPACE] (Finding 0052) specifies that `findnextlinkvsa` computes the insertion point as `vspanreach` — the current end of the document's V-extent — or `2.1` if no links exist yet. This value is read from the live POOM state at the moment of the call.

Because Session A's CREATELINK completes entirely (including the `insertpm` that writes the link at position P₁), Session B's subsequent `findnextlinkvsa` call reads a POOM that already contains the entry at P₁. It therefore computes `vspanreach` as some P₂ > P₁ and allocates there. The two allocations are necessarily distinct.

---

### The Theoretical Race That Cannot Occur

[EC-CONCURRENT-LINK-CREATION] (Finding 0052) explicitly identifies the race that *would* matter in a multi-threaded system:

> If operation A calls `findnextlinkvsa` to get position P, then operation B inserts a link before P, then A inserts at P — B's link would be shifted by A's insertion.

This is the correct concern for a concurrent system. However, the same finding immediately constrains it:

> The V-positions of link orgls are NOT stable under concurrent modification, **even though they are stable under sequential modification**.

The emphasis on "sequential" points directly to [INV-SEQUENTIAL-DISPATCH] as the resolution. The race is real in the abstract, but the single-threaded event loop makes it unreachable in this implementation.

---

### Cross-Check: The Analogous Document Allocation Case

[INV-GLOBAL-ADDRESS-UNIQUENESS] (Finding 0022) confirms the same pattern holds for document address allocation: two sessions creating documents under the same account get distinct addresses because the backend maintains a shared, sequentially-accessed counter. The mechanism is identical — sequential dispatch ensures each allocation sees the committed result of all prior allocations.

---

### Summary

| Property | Citation | Effect |
|---|---|---|
| Run-to-completion dispatch | [INV-ATOMICITY] | No interleaving possible within one operation |
| Sequential FD processing | [INV-SEQUENTIAL-DISPATCH] | Session B waits until Session A finishes |
| `vspanreach`-based placement | [SS-LINK-SUBSPACE] | Second call reads first call's committed state |
| Theoretical race identified | [EC-CONCURRENT-LINK-CREATION] | Confirms what would fail without sequential dispatch |

The allocation is safe not because `findnextlinkvsa` implements a compare-and-swap or holds a lock, but because the entire architecture serializes all operations through a single event loop. The query-and-increment pattern in `findnextlinkvsa` is inherently safe in this context — the "increment" (POOM insertion) is always visible to the next "query" because no interleaving exists.

## Code Exploration

I now have everything I need. Here is the full answer.

---

## `findnextlinkvsa`: Single-Threaded Safety, Not Atomic Allocation

### The Implementation

`findnextlinkvsa` is defined at `backend/do2.c:151–167`:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);  /* firstlink = 0.2.… */
    tumblerincrement (&firstlink, 1, 1, &firstlink);  /* firstlink = 0.2.1 */

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);
    else
        movetumbler (&vspanreach, vsaptr);
    return (TRUE);
}
```

The function:
1. Constructs a hardcoded floor `firstlink = 0.2.1`.
2. Calls `doretrievedocvspan` to read the document's current V-span from the in-memory granfilade. Note the `(void)` cast — the return value is discarded intentionally.
3. Computes `vspanreach = vspan.stream + vspan.width` (the end of the current POOM extent).
4. Returns `max(0.2.1, vspanreach)`.

There is **no increment, no counter, no compare-and-swap**. It is a pure read of current POOM state.

---

### How It Is Called in `docreatelink`

In `backend/do1.c:207–221`:

```c
bool docreatelink(...)
{
    makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
    return (
         createorglingranf (taskptr, granf, &hint, linkisaptr)   /* alloc link ISA  */
      && tumbler2spanset (taskptr, linkisaptr, &ispanset)         /* ISA → ispan     */
      && findnextlinkvsa (taskptr, docisaptr, &linkvsa)           /* read POOM end   */
      && docopy (taskptr, docisaptr, &linkvsa, ispanset)          /* WRITE to POOM   */
      && ...
    );
}
```

`findnextlinkvsa` reads the POOM end (step 3), then `docopy` immediately extends the POOM to that point (step 4). This is a classic read-then-write pattern. Its safety depends entirely on the concurrency model.

---

### The Concurrency Model: Single-Threaded Event Loop

The backend is a **single-threaded, non-preemptive, select-based event loop** (`backend/bed.c:103–149`):

```c
for (;;) {
    ...
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];          /* pick a session  */
                task.inp = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;
                xanadu(&task);                 /* process ONE full request */
                ...
            }
        }
    }
    ...
}
```

`xanadu()` at `bed.c:153–172` reads the request, dispatches to the handler (e.g., `createlink` → `docreatelink`), sends the response, and frees task memory — **all before returning**. The next iteration of the `for(i)` loop then picks the next ready FD.

There are no threads. There is no preemption between any two lines of `docreatelink`. The entire chain `findnextlinkvsa → docopy` runs atomically from the perspective of all other sessions.

---

### What Actually Happens With Two Sessions

Suppose session A and session B both have CREATELINK requests pending on the same document, and `select()` reports both FDs ready at the same instant.

The `for(i)` loop will process them in FD-index order:

1. **Session A processes fully**: `findnextlinkvsa` reads POOM end (e.g., returns V-address `X`), then `docopy` inserts link A's ISA at position `X`, extending the in-memory POOM to `X + width(A)`. `xanadu()` returns.

2. **Session B processes fully**: `findnextlinkvsa` calls `doretrievedocvspan`, which reads the **already-updated** in-memory granfilade (via `findorgl` → `fetchorglgr` at `granf1.c:39`). `vspanreach` is now `X + width(A)`, strictly greater than `X`. B gets a different V-address. `docopy` extends the POOM further. `xanadu()` returns.

The second call **does** see the first link's POOM entry, not because of any atomic counter, but because the single-threaded event loop ensures the first request's `docopy` has already committed to the in-memory enfilade before the second request's `findnextlinkvsa` runs.

---

### The `(void)` Cast Edge Case

The return value of `doretrievedocvspan` is silently discarded at `do2.c:160`:

```c
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
```

If the document has no content yet (empty POOM), `doretrievedocvspan` → `retrievevspanpm` may fail, leaving `vspan` zeroed. Then `vspanreach = 0`, which is `< firstlink = 0.2.1`, so the floor value `0.2.1` is used. This is the correct behavior for the **first ever link** on a document: it lands at V-address `0.2.1`.

---

### Is There a Race? No — With a Caveat

**There is no race condition** in the current architecture because the server is single-threaded. The query-and-write pattern in `findnextlinkvsa` + `docopy` is only safe *because* of this property.

If the server were ever made multi-threaded or asynchronous without adding a lock around `findnextlinkvsa → docopy`, there would be a classic TOCTOU race: two sessions could call `findnextlinkvsa` before either calls `docopy`, both see the same `vspanreach`, and both attempt to insert a link at the same V-address — a collision in the document's POOM.

The current code has **no such lock**. Its correctness is an implicit architectural invariant of the single-threaded event loop in `bed.c`, not an explicit atomic allocation mechanism.

---

## Question 17 [gregory]

> If session A deletes content at I-address range [.0.1.3,.0.1.5] from doc1 while session B simultaneously copies that same I-address range from doc1 into doc2, does `vspanset2sporglset` in session B's COPY read doc1's pre-delete or post-delete POOM depending solely on event loop ordering?

### Gregory's Answer

## KB Synthesis

Yes, solely by event loop ordering — and the reason is architectural.

## The Single-Threaded Event Loop

The backend daemon multiplexes all frontend connections via `select()`, but processes each request to completion before accepting the next. From **INV-ATOMICITY** [Finding 0042]:

> The `xanadu(&task)` call executes the entire operation — request parsing, state mutation, response sending, and memory cleanup — before returning to `select()`. There are no threads, no state-modifying signal handlers, and no preemption.

**INV-SEQUENTIAL-DISPATCH** [Finding 0042] sharpens this: even when multiple FDs are ready simultaneously after `select()`, the loop iterates over them sequentially. Frontend *i*'s request completes entirely before frontend *i+1* begins.

There is no true simultaneity. The word "simultaneously" in the question means only "both requests are pending when `select()` returns."

## What `vspanset2sporglset` Reads

From **SS-VSPAN-TO-SPORGL** [Finding 0013], the COPY path runs:

```
vspanset2sporglset(doc1, vspan)
  → vspanset2ispanset(doc1, vspan)   # reads doc1's POOM
  → attach doc1 ISA → sporgls
```

Step 1 consults doc1's POOM — the mutable V→I mapping. From **SS-POOM-MUTABILITY** [Finding 0072]:

> The POOM maps V-addresses to I-addresses and is modified in-place by INSERT, DELETE, and REARRANGE. There are no copy-on-write semantics, no shadow copies, and no journaling at the POOM level.

## The Two Outcomes

**If DELETE processes first:**
Session A's `deletend` removes the V→I mappings for the affected range from doc1's POOM [**ST-DELETE**, Finding 0064]. When session B's COPY subsequently calls `vspanset2ispanset`, the POOM has no entries covering that V-range. The result is an empty or partial sporgl set — COPY produces nothing or partial content in doc2.

Note: the I-addresses themselves still exist in the granfilade [**INV-IADDR-IMMUTABILITY**, Finding 0064] — DELETE never touches the granfilade. But `vspanset2sporglset` routes through the POOM, not directly through I-space.

**If COPY processes first:**
Session B reads the intact POOM, converts V-addresses to I-addresses correctly, and produces a complete sporgl set. doc2 receives the full content with shared identity. Session A's subsequent DELETE removes the mappings from doc1's POOM only [**FC-DELETE-CROSS-DOC**, Finding 0064] — doc2's newly-written POOM is unaffected.

## Summary

The outcome is determined by which request `select()` picked first in its iteration over ready file descriptors. There is no race condition in the concurrent-programming sense; there is only serialization order. Both operations execute atomically with respect to each other, and the POOM — as the sole mutable layer — reflects exactly one of these states when the second operation begins.

## Code Exploration

Now I have everything I need. Let me compile the complete answer.

---

## Answer

**Yes, which POOM state `vspanset2sporglset` observes depends solely on event loop ordering.** Here is the full trace.

---

### 1. The Event Loop is Fully Serial — No Interleaving

`bed.c` runs a single-process, single-thread `select()` event loop:

```c
// bed.c:110-141
inputfds2 = inputfds;
if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {
    ...
} else {
    for (i = 0; i <= nfds; i++) {
        if ((1<<i) & inputfds2) {
            user = fdtoplayer[i];
            task.inp = player[user].inp;
            task.outp = player[user].outp;
            task.account = player[user].account;
            ...
            xanadu(&task);      // ← processes ONE request to completion
```

`xanadu()` at `bed.c:153` dispatches the request and runs it to completion before returning to the loop:

```c
// bed.c:161-163
} else if (getrequest(taskptr, &request)) {
    (*requestfns[request])(taskptr);   // ← entire operation happens here
    sendresultoutput(taskptr);
```

**There is no interleaving.** Once session A's fd wins a turn, A's request runs entirely before B's fd is serviced, and vice versa.

**Ordering tie-break:** When both sessions have sent a request before the same `select()` returns, both fds are set in `inputfds2`. The `for (i = 0; i <= nfds; i++)` loop at `bed.c:118` processes them in **ascending fd-index order**. The session with the lower fd number goes first.

---

### 2. Session A's DELETE Mutates the POOM In-Place

The DELETE handler in `fns.c:333` calls `dodeletevspan` (do1.c:158):

```c
// do1.c:158-167
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`deletevspanpm` at `orglinks.c:145` calls `deletend` directly on the live POOM tree:

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

`deletend` is a destructive, in-place mutation of the enfilade tree. **There is no copy-on-write, no snapshotting, no versioning.** After `dodeletevspan` completes, the V-addresses covering the deleted range are gone from doc1's POOM immediately.

---

### 3. Correction: `vspanset2sporglset` Is NOT on the COPY Path

The COPY handler (`fns.c:35`) calls `docopy` (`do1.c:45`):

```c
// do1.c:53-65
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
...
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
...
```

`docopy` calls `specset2ispanset` (`do2.c:14`), which reads doc1's POOM to convert V-spans → I-spans:

```c
// do2.c:34-38
if (!(
   findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)))){
       return (FALSE);
}
```

`vspanset2sporglset` is a distinct function in `sporgl.c:35` called from `specset2sporglset` (`sporgl.c:14`), which is used by **link creation** (`do1.c:187, 214-216`) and link retrieval (`spanf1.c:71-75, 222`), not by plain COPY.

---

### 4. Both Paths Read the Same Live POOM — No Snapshot

Whether the path is `specset2ispanset` → `vspanset2ispanset` (COPY) or `specset2sporglset` → `vspanset2sporglset` (link creation), both do the same thing: they call `findorgl` to retrieve the **current live state** of doc1's POOM (`orgl`) and then call `vspanset2ispanset` on it:

```c
// sporgl.c:43-48
ispanset = NULL;
if (!findorgl (taskptr, granf, docisa, &orgl, type)){
    return (NULL);
}
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
```

`findorgl` at `granf1.c:17` is simply a fetch of the current in-memory granfilade node:

```c
// granf1.c:39
*orglptr = fetchorglgr(taskptr, granfptr, isaptr);
return (*orglptr ? TRUE : FALSE);
```

There is no snapshot. The `orgl` returned is the live, mutable POOM node.

---

### 5. Conclusion: It Depends Solely on fd-Index Order

**Case A — session A's fd index < session B's fd index (or A's request arrived first):**
Session A's DELETE runs first. `deletend` removes the V-address nodes covering the deleted range from doc1's POOM. When session B's COPY (or link creation) subsequently calls `findorgl` and `vspanset2ispanset`, the V→I mapping for that range returns empty or null. The COPY either fails (`specset2ispanset` returns FALSE) or silently copies nothing.

**Case B — session B's fd index < session A's fd index (or B's request arrived first):**
Session B's operation runs first. `vspanset2sporglset` (or `vspanset2ispanset`) calls `findorgl`, sees the **pre-delete POOM**, finds the V→I mapping intact, and the operation succeeds against the complete document. Session A's DELETE runs afterward.

There is no mutex, no lock, no transaction isolation, and no journal. The only concurrency primitive is the serialized `select()` loop and fd iteration order at `bed.c:111-141`. Whichever fd appears lower in the `for` loop determines which session sees which state.

---

## Question 18 [gregory]

> After two overlapping DELETE operations on the same document — first deleting V:[1.2,1.4] then V:[1.1,1.3] — can `tumblersub` shifting from the second DELETE produce negative V-position tumblers for entries that were already shifted left by the first DELETE?

### Gregory's Answer

## KB Synthesis

## Two Overlapping Deletes: Can `tumblersub` Produce Negative V-Positions?

The short answer is **no, not for this specific geometry** — but the mechanism deserves careful tracing, because the general risk is real and documented.

---

### The Relevant Mechanisms

**`strongsub` and the exponent guard** [SS-TUMBLER Finding 0055]

`tumblersub` delegates to `strongsub`, which has one guard: if `b.exp < a.exp`, it returns `a` unchanged without subtracting. When both operands share the same exponent (as same-subspace entries and their deletion widths do), subtraction proceeds unconditionally — and can produce a negative tumbler if `b > a` in absolute value.

**DELETE's Case 2 shifting** [ST-DELETE Finding 0053]

`deletend()` classifies POOM entries into three cases: entries before the deletion (no change), entries inside it (removed via `disown`+`subtreefree`), and entries after it (Case 2: shifted left by `tumblersub(entry.vpos, width)`). Negative V-positions arise precisely when Case 2 applies and `width > entry.vpos`. The implementation has no guard against this — `deletevspanpm()` checks only for zero width [PRE-DELETE Finding 0040, 0053].

**Finding 0055's refinement** [ST-DELETE Finding 0055]

Finding 0053's concern about cross-subspace corruption was partially retracted: the exponent mismatch between text deletion widths (exp=-1) and link crums (exp=0) causes `strongsub` to no-op on link entries. But for **same-exponent** text entries, the subtraction fully proceeds with no protection.

---

### Tracing the Specific Geometry: DELETE [1.2, 1.4] Then DELETE [1.1, 1.3]

Both deletions have width 0.2 in the 1.x text subspace. Call the initial state "all text entries at their original V-positions."

**After first DELETE [1.2, 1.4]:**

The cut boundaries are checked via `whereoncrum` [SS-WHEREONCRUM]; `slicecbcpm` fires only on THRUME (strictly interior) cuts [PRE-DELETE Finding 0075]. The classification:

| Original V-position | Case | Result |
|---|---|---|
| < 1.2 | Case 0 | Unchanged |
| ∈ [1.2, 1.4) | Case 1 | Removed |
| ≥ 1.4 | Case 2 | Shifted by −0.2 |

So an entry at 1.5 moves to 1.3; one at 1.41 moves to 1.21; one at 1.9 moves to 1.7.

**After second DELETE [1.1, 1.3] (operating on post-first-delete V-space):**

| Post-first-delete V-position | Case | Result |
|---|---|---|
| < 1.1 | Case 0 | Unchanged |
| ∈ [1.1, 1.3) | Case 1 | Removed |
| = 1.3 (ONMYRIGHTBORDER) | Case 2 | Shifted by −0.2 → 1.1 |
| > 1.3 | Case 2 | Shifted by −0.2 |

Now trace back to original positions:

- Originally at 1.41–1.49 → shifted to 1.21–1.29 → falls inside [1.1, 1.3) → **removed** by second delete (not shifted twice)
- Originally at 1.5 → shifted to 1.3 → ONMYRIGHTBORDER → shifted to **1.1** (positive)
- Originally at 1.5+ε → shifted to 1.3+ε → Case 2 → shifted to **1.1+ε** (positive)

**For an entry to receive two Case-2 shifts**, it must be:
- After 1.4 (to survive the first delete as Case 2), AND
- After 1.3 in the post-first-delete space (to survive the second delete as Case 2), meaning: `original - 0.2 ≥ 1.3`, so `original ≥ 1.5`

The minimum original position that takes two shifts is 1.5. Its final position is 1.5 − 0.2 − 0.2 = **1.1**, which is positive. Any larger original position yields a larger final position.

**Conclusion for this geometry:** No negative V-position tumblers are produced. The cumulative shift (0.4) is always less than the minimum surviving entry's position (≥ 1.1).

---

### When Two Deletes *Do* Produce Negative V-Positions

The KB explicitly documents this in [ST-DELETE Finding 0053]:

> After shifting 1.5 → 1.2 (first delete of 3 bytes), a second delete of 10 bytes shifts: `1.2 − 0.10 = −0.8` (negative).

The condition is: **the total cumulative shift must exceed the entry's current V-position at the time of the second delete.** Formally [ST-DELETE Finding 0055]:

```
∀ entry : entry.vpos > delete_end ∧ entry.vpos.exp = width.exp
  ⟹ entry.vpos' = entry.vpos - delete_width
```

If `entry.vpos - delete_width < 0`, the result is a valid negative tumbler (sign=1, positive magnitude) that is stored without error. Such an entry becomes permanently invisible: negative tumblers sort before all valid V-addresses [SS-TUMBLER Finding 0053], and no V-space query ever reaches them. Critically, `DELETEVSPAN` cannot target them because it requires a positive-valued V-span argument. This constitutes leaked state — the POOM retains a ghost entry that cannot be reclaimed [EC-DEEPLY-ORPHANED-LINK Finding 0053].

For the specific scenario asked about, this threshold is never crossed because both deletion widths are small (0.2) and the surviving entries start at V ≥ 1.5, giving a floor of 1.1 after both shifts.

---

### Summary

| Property | Finding |
|---|---|
| `strongsub` produces negatives when `width > entry.vpos` and exponents match | [SS-TUMBLER Finding 0053, 0055] |
| Case 2 shifting applies without any positivity guard | [ST-DELETE Finding 0053] |
| Cross-subspace entries are immune (exponent mismatch) | [ST-DELETE Finding 0055], [FC-SUBSPACE Finding 0055] |
| Same-subspace double-shifting CAN go negative (large enough widths) | [ST-DELETE Finding 0053] |
| For DELETE [1.2,1.4] then [1.1,1.3] specifically: minimum surviving position is 1.1 | Derived above |
| Negative V-position entries are leaked, invisible, irrecoverable | [INV-POOM-BIJECTIVITY Finding 0053], [EC-DEEPLY-ORPHANED-LINK] |

For the specific overlapping deletes asked about, no negative V-position tumblers result. But the risk is real and geometry-dependent: a second delete with a width large enough to exceed the (already-shifted) entry's V-position will silently produce negative tumblers, violating the bijectivity invariant [INV-POOM-BIJECTIVITY] with no error and no recovery path.

## Code Exploration

I now have all the code I need. Here is the complete answer.

---

## Answer: Can `tumblersub` in the second DELETE produce negative V-position tumblers?

**No. The enfilade structure's mathematical invariant prevents this.** Here is the full chain of evidence.

---

### 1. The call chain

`dodeletevspan` [do1.c:158-167] → `deletevspanpm` [orglinks.c:145-150] → `deletend` [edit.c:31-76]:

```c
// orglinks.c:149
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

The POOM root (`docorgl`) is passed directly as `fullcrumptr`.

---

### 2. The critical stub: `newfindintersectionnd` always returns the root

```c
// ndinters.c:38-42
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives,
                          typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;
    clear(offset, sizeof(*offset));
}
```

The original descent logic (`findintersectionnd`) is commented out above this. The stub **always sets `father = fullcrumptr` (the POOM root) and `foffset = zero`**. This means `deletend` invariably iterates over only the **root's direct children**.

Additionally, `makecutsdownnd`'s descent loop is also dead code [ndcuts.c:40]:

```c
for (;(knives->nblades > 1) && FALSE && ptr->height;) {
```

The `FALSE` disables it. All cuts happen at the root level.

---

### 3. `prologuend` computes the accumulated offset

```c
// retrie.c:334-338
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd(offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd(grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

In `deletend`, `foffset = zero` → `fgrasp.dsas[V] = zero + root->cdsp.dsas[V]`. Call this `F`.

---

### 4. `whereoncrum` classification [retrie.c:354-372]

For POOM/SPAN nodes, `whereoncrum(child, &fgrasp, blade, V)` computes:

```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
// left = fgrasp.dsas[V] + child->cdsp.dsas[V]  ← child's absolute V-position
```

`left` is the child's **absolute V-position**. The function then compares `blade` against `[left, left+child->cwid]`.

**Case 2** is returned when `blade ≤ left` (blade ≤ ONMYLEFTBORDER in terms of the child):

- i=1 (blade[1] = origin + width): `blade[1] ≤ child.absolute` → child is entirely to the **right** of the delete zone → return 2 (shift left)

---

### 5. The subtraction in `deletend` [edit.c:63]

```c
case 2:
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

This computes: `child->cdsp.dsas[V] -= width`.

**The invariant proof:**

| Step | Expression | Value |
|------|-----------|-------|
| Case 2 trigger condition | `blade[1] ≤ child.absolute` | `origin + width ≤ F + child->cdsp` |
| Rearranging | `child->cdsp ≥ (origin + width) − F` | `= origin − F + width` |
| After subtraction | `child->cdsp − width ≥ origin − F` | |
| Valid V-addresses require | `origin ≥ F` (delete origin ≥ document V-start) | `→ result ≥ 0` |

The result is **never negative** for any validly-addressed delete.

---

### 6. Tracing the specific overlapping scenario

Assume `F = 0` (POOM root `cdsp.dsas[V] = 0`).

**DELETE 1: origin=1.2, width=0.2, blade[1]=1.4**

Before DELETE 1, consider a node at `cdsp = 1.5` (absolute V=1.5):
- Case 2 (1.5 ≥ 1.4) → `1.5 − 0.2 = 1.3` ✓

**DELETE 2: origin=1.1, width=0.2, blade[1]=1.3**

The previously-shifted node is now at `cdsp = 1.3`.

Before the classification loop, `makecutsnd` [ndcuts.c:15-31] ensures nodes are split at both blades (1.1 and 1.3). The node at 1.3 starts exactly at blade[1].

In `deletecutsectionnd` for this node:
- i=1: `whereoncrum(node, fgrasp=0, blade[1]=1.3, V)`: `left = 1.3`, `cmp = tumblercmp(1.3, 1.3) = EQUAL` → ONMYLEFTBORDER ≤ ONMYLEFTBORDER → **return 2**
- `tumblersub(1.3, 0.2, &cdsp)` → `cdsp = 1.1 > 0` ✓

For any node at `cdsp ≥ 1.3` (case 2 for DELETE 2): `new_cdsp = cdsp − 0.2 ≥ 1.1 > 0`.

---

### 7. Checking cascaded shifts (node shifted by BOTH deletes)

A node originally at `cdsp = C` shifts under DELETE 1 (case 2 requires `C ≥ 1.4`):
- After DELETE 1: `cdsp = C − 0.2 ≥ 1.2`

For DELETE 2 case 2, that shifted node must satisfy `C − 0.2 ≥ 1.3`, so `C ≥ 1.5`:
- After DELETE 2: `cdsp = C − 0.4 ≥ 1.1 > 0` ✓

No matter how many overlapping deletions cascade, the minimum value after each case-2 subtraction is `origin − F`, which is bounded below by 0 for valid V-addresses.

---

### 8. The only path to a negative tumbler

`tumblersub` [tumble.c:406-440] **can** produce a negative result — it uses a sign bit internally (`cptr->sign = 1`). But this would require `origin < F` (the delete starts before the document's V-space), which violates the precondition that the delete V-span lies within the document. There is no guard against this in `deletend` itself, but valid FEBE protocol usage prevents it.

---

### Summary

**`tumblersub` at `edit.c:63` cannot produce a negative V-position tumbler** for the scenario described. The classification logic in `deletecutsectionnd` guarantees that any case-2 node satisfies `child->cdsp ≥ origin + width − F`, and subtracting `width` leaves `child->cdsp − width ≥ origin − F ≥ 0`. This is a structural consequence of three design properties working together:

1. **`newfindintersectionnd` always returns root with zero offset** [ndinters.c:38-42] — making `fgrasp` the document's absolute V-start.
2. **`whereoncrum`'s case-2 classification** [retrie.c:356-362] — requires the child's absolute position ≥ blade_right.
3. **`blade_right = origin + width ≥ F`** for any in-document delete origin.

---

## Question 19 [gregory]

> When session A performs INSERT at V:1.3 and session B performs CREATENEWVERSION on the same document, does the version capture the pre-insert or post-insert text depending entirely on event loop order, and does `docopyinternal` take a consistent snapshot of the text subspace POOM?

### Gregory's Answer

## KB Synthesis

## Version Captures Whichever Snapshot the Event Loop Delivers

The answer has three parts: serialization, snapshot mechanism, and what "consistent" means in this context.

---

### 1. Ordering is determined entirely by the event loop — no interleaving is possible

[INV-ATOMICITY] and [INV-SEQUENTIAL-DISPATCH] (both Finding 0042) are definitive here. The `bed.c` event loop processes each FEBE operation via run-to-completion scheduling: `xanadu(&task)` executes the entire operation — request parsing, all state mutations, response sending, memory cleanup — before returning to `select()`. Even when both sessions have requests ready simultaneously on their file descriptors, the loop iterates over ready FDs sequentially and blocks on each `xanadu()` call before advancing to the next FD.

Consequence: INSERT and CREATENEWVERSION cannot interleave at all. One executes to full completion before the other begins. Which goes first is determined by which FD appears earlier in the `select()` result iteration for that particular scheduling tick.

---

### 2. `docopyinternal` reads live POOM state — there is no snapshot mechanism

[SS-POOM-MUTABILITY] (Finding 0072) states explicitly: "There are no copy-on-write semantics, no shadow copies, and no journaling at the POOM level." The POOM is a mutable in-place tree structure.

[ST-VERSION-CREATE] (Findings 0032, 0043, 0046) details what CREATENEWVERSION does:

1. `createorglingranf` — allocates a new document address
2. `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm` — reads the source document's V-dimension displacement and width from the root crum (text subspace only, at V-position 1.x)
3. `docopyinternal` — walks that vspan, converting V-positions to I-addresses via the live POOM, and inserts corresponding entries into the new version's POOM

All three steps happen atomically within a single `xanadu()` call. There is no point at which another session could modify the source document's POOM between steps 2 and 3 — the event loop prevents it.

---

### 3. The version captures exactly the state at the moment it runs — no more, no less

Because of sequential dispatch:

- **If CREATENEWVERSION runs before INSERT**: `doretrievedocvspanfoo` reads the pre-insert root crum. The version POOM captures V→I mappings for the unmodified text. After CREATENEWVERSION completes, INSERT runs and modifies the original document's POOM in-place; [FC-VERSION-ISOLATION] (Finding 0072) confirms that subsequent mutations to the original's POOM leave the version's POOM untouched.

- **If INSERT runs before CREATENEWVERSION**: `doretrievedocvspanfoo` reads the post-insert root crum. The version POOM captures V→I mappings including the newly inserted content at V:1.3 and the shifted content after it.

In neither case is there a partial or inconsistent snapshot. The POOM read by `docopyinternal` is always a stable, complete state because no other operation can touch it during execution.

---

### What "consistent snapshot" means here

`docopyinternal` does not implement a traditional snapshot (no MVCC, no log-structured copy). What provides consistency is the event loop's mutual exclusion: the source document's POOM is quiescent for the entire duration of CREATENEWVERSION's execution. The result is equivalent to a consistent snapshot by scheduling guarantee rather than by data-structure mechanism.

[INV-SEQUENTIAL-DISPATCH] is the load-bearing invariant. Without it (e.g., if the system were multi-threaded without locks, as [PRE-CONCURRENT-INSERT] warns), `docopyinternal` could read a partially-applied INSERT and produce a semantically incoherent version. But the single-threaded event loop prevents exactly this.

---

**In short**: the version captures pre-insert or post-insert state based purely on `select()` ordering; `docopyinternal` takes no explicit snapshot but reads a consistent live POOM because the event loop serializes all access; once the version is created, [FC-VERSION-ISOLATION] guarantees it is immune to subsequent mutations of the original.

## Code Exploration

I now have everything needed for a complete, cited answer.

---

## Answer: INSERT vs. CREATENEWVERSION — Event Loop Order and POOM Snapshot Semantics

### 1. The Backend Is Single-Threaded and Non-Preemptive

The event loop in `bed.c` uses UNIX `select()` to multiplex between frontends, but processes exactly one request at a time:

```c
// bed.c:110-141
inputfds2 = inputfds;
if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
else {
    for (i = 0; i <= nfds; i++) {
        if ((1<<i) & inputfds2) {
            user = fdtoplayer[i];
            ...
            xanadu(&task);   // bed.c:128 — runs to complete completion
        }
    }
}
```

`xanadu()` itself [bed.c:153-172] calls the request handler (`(*requestfns[request])(taskptr)`) and only then calls `sendresultoutput(taskptr)`. The inner loop does not re-enter `select()` until `xanadu()` has returned. There is no threading, no preemption, and no interleaving of operations from different sessions within a single request.

**Consequence:** INSERT from session A and CREATENEWVERSION from session B are strictly serialized. One finishes completely before the other begins. Which runs first is determined by which fd `select()` marks ready when the kernel returns — that is, OS socket scheduling.

---

### 2. The `insert()` Handler Uses an Optimistic Response Pattern

`fns.c:insert()` [fns.c:84-98] is unusual:

```c
void insert(typetask *taskptr) {
    (void) getinsert(taskptr, &docisa, &vsa, &textset);  // parse request
    putinsert(taskptr);                                   // fns.c:91 — SEND RESPONSE FIRST
    if (!doinsert(taskptr, &docisa, &vsa, textset))       // fns.c:92 — MUTATE POOM AFTER
        fprintf(stderr, "requestfailed in insert\n");     // fns.c:94
}
```

The success acknowledgment is buffered to the client **before** `doinsert()` modifies the POOM. However, since the event loop is single-threaded, session B cannot execute between these two lines. From session B's perspective, the POOM is either fully pre-insert or fully post-insert — never mid-mutation. The practical implication is only that if `doinsert()` fails, session A has already been told it succeeded, with no way to retract that.

---

### 3. `docreatenewversion` Reads Live POOM State — No Snapshot

`do1.c:docreatenewversion()` [do1.c:260-299]:

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr) {
    ...
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) return FALSE;  // do1.c:277

    if (!doretrievedocvspanfoo(taskptr, isaptr, &vspan)) return FALSE;       // do1.c:281
    //   ^^^^^ reads current POOM state RIGHT NOW

    vspec.next = NULL;
    vspec.itemid = VSPECID;
    movetumbler(isaptr, &vspec.docisa);   // do1.c:287 — original doc's ISA
    vspec.vspanset = &vspan;              // do1.c:289 — the vspan just read

    addtoopen(newisaptr, user, TRUE, WRITEBERT);           // do1.c:292
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // do1.c:293
    logbertmodified(newisaptr, user);
    doclose(taskptr, newisaptr, user);
    return TRUE;
}
```

`doretrievedocvspanfoo()` [do1.c:301-309] calls `findorgl()` (gets the document's POOM root), then calls `retrievedocumentpartofvspanpm()` [orglinks.c:155-162]:

```c
bool retrievedocumentpartofvspanpm(...) { /* this is a kluge */
    vspanptr->stream = ((typecuc*)orgl)->cdsp.dsas[V];   // orglinks.c:159 — live V-origin
    vspanptr->width  = ((typecuc*)orgl)->cwid.dsas[V];   // orglinks.c:160 — live V-width
    return TRUE;
}
```

This reads `cdsp.dsas[V]` (the virtual stream origin) and `cwid.dsas[V]` (the virtual width) **directly from the in-memory POOM node's cached summary fields**. It does not walk the tree; it reads the root node's aggregate width that `setwispupwards()` maintains. If INSERT has already run and updated these fields, the vspan reflects the inserted content. If INSERT has not yet run, it reflects the pre-insert state.

---

### 4. `docopyinternal` Does Not Snapshot — It Copies Live State In-Place

`do1.c:docopyinternal()` [do1.c:66-82]:

```c
bool docopyinternal(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset) {
    if (!specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE;  // do1.c:74
    if (!findorgl(taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)) return FALSE;  // do1.c:75
    if (!acceptablevsa(vsaptr, docorgl)) return FALSE;                                 // do1.c:76
    if (!asserttreeisok(docorgl)) return FALSE;                                        // do1.c:77
    if (!insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;        // do1.c:78
    if (!insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;     // do1.c:79
    if (!asserttreeisok(docorgl)) return FALSE;                                        // do1.c:80
    return TRUE;
}
```

There is **no snapshot, no copy-on-write, and no transaction isolation**. `specset2ispanset()` converts the `vspec` (built from the live vspan read at `do1.c:281`) into intrinsic spans by walking the current state of the spanfilade. `insertpm()` then inserts those intrinsic spans into the new document's POOM.

The consistency guarantee comes entirely from the single-threaded event loop: because `docreatenewversion()` runs atomically with respect to other sessions (no session can interleave), the state read by `doretrievedocvspanfoo()` at `do1.c:281` is consistent with the state consumed by `insertspanf()` at `do1.c:79`. The POOM cannot change between those lines. But this is scheduler-level consistency, not transactional snapshot isolation.

---

### 5. Decisive Determination of Pre- or Post-Insert Content

The `vspec` passed into `docopyinternal` describes: "all V-spans of document `isaptr`, from stream `vspan.stream` with width `vspan.width`." This `vspan` was captured at `do1.c:281` from the live POOM fields.

`doinsert()` ultimately calls `inserttextingranf()` [granf2.c:83-109] which allocates text in the granfilade, then `docopy()` which calls `insertpm()` and `insertspanf()` — updating both the document POOM's `cwid.dsas[V]` (via `setwispupwards` [insertnd.c:56,64]) and the spanfilade.

So the timeline is unambiguous:

| Event Loop Order | What CREATENEWVERSION Captures |
|---|---|
| INSERT (A) → CREATENEWVERSION (B) | `doretrievedocvspanfoo` sees the post-insert `cwid.dsas[V]`; copies include inserted content |
| CREATENEWVERSION (B) → INSERT (A) | `doretrievedocvspanfoo` sees the pre-insert `cwid.dsas[V]`; new version has no knowledge of A's text |

---

### Summary

1. **Ordering is entirely determined by `select()` socket readiness** [bed.c:111]. The first fd marked ready processes its full request before the second can begin [bed.c:128]. There is no lock, no transaction, and no coordination between sessions.

2. **`docreatenewversion` captures whatever the POOM contains at the moment it runs.** `doretrievedocvspanfoo` reads `cwid.dsas[V]` and `cdsp.dsas[V]` directly from the live POOM root's cached summary [orglinks.c:159-160]. This is labeled "a kluge" in the source.

3. **`docopyinternal` takes no independent snapshot.** It operates directly on the live granf and spanf. It is consistent within itself only because the single-threaded event loop prevents any other mutation while it runs.

4. **The `insert()` optimistic response** [fns.c:91-92] means session A gets a success acknowledgment before `doinsert()` has touched the POOM, but this has no observable consequence for session B since there is no interleaving.

---

## Question 20 [gregory]

> If two sessions issue APPEND and INSERT to the same document in rapid succession, does the I-address allocation via `findisatoinsertmolecule` guarantee non-overlapping I-addresses because the second operation's `findpreviousisagr` query sees the first operation's granfilade entry?

### Gregory's Answer

## KB Synthesis

## I-Address Allocation Across APPEND + INSERT

Yes, non-overlapping I-addresses are guaranteed — but the mechanism is not concurrent visibility. The correct explanation is simpler and stronger: **the two operations cannot actually execute concurrently**.

### The Guarantee Comes From Sequential Dispatch

[INV-ATOMICITY] (Finding 0042) and [INV-SEQUENTIAL-DISPATCH] (Finding 0042) are the relevant entries. The `bed.c` event loop processes each FEBE operation via run-to-completion scheduling:

> "The `xanadu(&task)` call executes the entire operation — request parsing, state mutation, response sending, and memory cleanup — before returning to `select()`."
> "Even when multiple frontends have requests ready simultaneously, the event loop processes them strictly sequentially."

So "rapid succession" from the client's perspective means the backend has already *finished* the first operation before beginning the second. There is no race.

### What `findpreviousisagr` Actually Sees

[SS-ADDRESS-ALLOC] (Finding 0061) confirms allocation is stateless — no cached counter, purely query-and-increment on the in-memory granfilade tree:

> "Each INSERT queries the granfilade tree via `findpreviousisagr` to find the highest existing I-address below an upper bound, then increments by 1."

By the time APPEND's follow-on INSERT runs, APPEND has completed. Its I-address allocations are already in the in-memory granfilade tree (the tree IS the cache, per [SS-CACHE-MECHANISM]). INSERT's `findpreviousisagr` traverses that same tree and finds APPEND's allocations as the new maximum. The result is strict monotonic growth — [INV-MONOTONIC] (Findings 0033, 0061):

> "I-address allocation is strictly monotonically increasing... Any session querying the same granfilade tree will allocate identically."

### One Subtlety: APPEND and DOCISPAN

APPEND does NOT create DOCISPAN entries [EC-APPEND-NO-DOCISPAN] (Finding 0036) — `insertspanf(..., DOCISPAN)` is explicitly commented out. But this is orthogonal to I-address allocation. APPEND still allocates I-addresses in the granfilade (it must store text content somewhere); it just doesn't index those addresses in the spanfilade. So `findpreviousisagr` in a subsequent INSERT sees APPEND's I-addresses and will allocate above them regardless.

### The Grim Reaper Caveat

A theoretical concern: if APPEND's granfilade crums are evicted between the two operations by [SS-CACHE-MECHANISM]'s grim reaper, could `findpreviousisagr` miss them? No — eviction writes to disk, and the tree traversal would load disk-based crums as needed. The tree traversal is not cache-only. This is a robustness property of the allocation mechanism, separate from the sequential dispatch guarantee.

### Summary

The guarantee holds, but the framing in your question slightly overstates the mechanism. It's not that `findpreviousisagr` "sees" the first entry through some concurrent visibility guarantee. Rather, by [INV-SEQUENTIAL-DISPATCH], the first operation has fully completed before the second starts — so there is no concurrent state to reason about. I-address non-overlap is a trivial consequence of single-threaded run-to-completion semantics combined with append-only granfilade allocation.

## Code Exploration

Now I have everything I need. Let me write the complete answer.

---

## Analysis: I-Address Non-Overlap Across Sessions

### Short Answer

**Yes — non-overlapping I-addresses are guaranteed, but not because of any explicit locking or transaction mechanism.** The guarantee falls out of the backend's single-threaded, run-to-completion event loop. Session B's `findpreviousisagr` *always* sees session A's committed granfilade entry, because session A's `xanadu()` call finishes completely — including all `insertseq()` mutations to the in-memory crum tree — before the event loop can dispatch any request from session B.

---

### 1. The Event Loop Is Single-Threaded

`bed.c:103–149` is the entire concurrency model:

```c
// bed.c:110-141
for (;;) {
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp  = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;
                xanadu(&task);              // ← runs to completion
            }
        }
    }
}
```

`xanadu()` at `bed.c:153–172`:

```c
int xanadu(typetask *taskptr)
{
    ...
    if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);    // full dispatch
        sendresultoutput(taskptr);
    }
    tfree(taskptr);
    ...
}
```

There are no threads, no signals that touch data structures, no coroutines, no I/O interleaving inside a request. `select()` is called only after every pending-ready fd has been drained by sequential `xanadu()` calls. Even if both session A and session B have data ready in the same `select()` result, the inner `for` loop processes them **one at a time**: A completes, *then* B starts.

---

### 2. The I-Address Allocation Path (INSERT)

For an INSERT:

**`fns.c:84–98`** → **`do1.c:87–123`** (`doinsert`):

```c
// do1.c:117-122
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy(taskptr, docisaptr, vsaptr, ispanset));
return(ret);
```

**`granf1.c:44–47`** → **`granf2.c:83–109`** (`inserttextgr`):

```c
// granf2.c:92-101
if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, &lsa))
    return (FALSE);
movetumbler(&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    locinfo.infotype = GRANTEXT;
    locinfo.granstuff.textstuff.textlength = textset->length;
    movmem(textset->string, locinfo.granstuff.textstuff.textstring,
           locinfo.granstuff.textstuff.textlength);
    insertseq((typecuc*)fullcrumptr, &lsa, &locinfo);   // ← commits to tree
    tumblerincrement(&lsa, 0, textset->length, &lsa);
}
```

**`granf2.c:130–156`** (`findisatoinsertgr`): for `ATOM` subtype, calls `findisatoinsertmolecule`.

**`granf2.c:158–181`** (`findisatoinsertmolecule`):

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;
    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); // ← reads tree
    if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {
        tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement(isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement(&lowerbound, 0, 1, isaptr);    // ← new ISA = lowerbound + 1
    }
    ...
}
```

**`granf2.c:255–278`** (`findpreviousisagr`): recursively walks the in-memory granfilade crum tree to find the highest ISA strictly below `upperbound`.

---

### 3. Why the Second Session Sees the First's Entry

The granfilade tree is a pure in-memory structure of linked `typecorecrum` / `typecbc` nodes. `insertseq()` at `insert.c:17–70` modifies this tree **immediately and synchronously**:

```c
// insert.c:43-69
reserve((typecorecrum*)ptr);
new = createcrum(0, (INT)ptr->cenftype);
reserve(new);
adopt(new, RIGHTBRO, (typecorecrum*)ptr);
ivemodified(new);
splitsomething = splitcrumupwards(findfather(new));
moveinfo(info, &((typecbc*)new)->cinfo);
// ... cwid adjustments, setwispupwards calls ...
if (splitsomething) {
    recombine(fullcrumptr);
}
```

After `insertseq()` returns, the crum tree permanently reflects the new ISA. There is no write-buffer, no deferred commit. When session A's `xanadu()` returns from this call chain, the granfilade is updated.

Because the event loop enforces that **session B's `xanadu()` cannot start until session A's has returned**, `findpreviousisagr` in session B necessarily walks a tree that already contains session A's crum. It will return session A's ISA as the lowerbound, and session B's computed address will be strictly greater.

---

### 4. No Hazard — Even in the "Same select() Batch" Case

The most plausible near-collision scenario is both sessions having requests buffered simultaneously, so `select()` marks both fds ready in one call (`bed.c:111`). Even then, the inner `for` loop at `bed.c:118`:

```c
for (i = 0; i <= nfds; i++) {
    if ((1<<i) & inputfds2) {
        ...
        xanadu(&task);   // session A completes entirely here
        ...
    }
    // then i++ and the loop processes session B
}
```

Session A at fd `i` finishes completely. When the loop reaches session B at fd `j > i`, the tree already has A's entry.

---

### 5. The One Real Subtlety: APPEND vs INSERT

The question mentions APPEND. `doappend()` at `do1.c:25–32` calls `appendpm()` (not shown in this file — it lives in the POOM layer), which calls `inserttextingranf` via a different path. But it still ultimately calls `findisatoinsertgr` → `findisatoinsertmolecule` → `findpreviousisagr` → `insertseq`. The serialization guarantee holds identically. The APPEND/INSERT distinction affects which virtual address (VSA) is used for the POOM insertion, not the granfilade ISA allocation.

---

### Summary Table

| Concern | Verdict | Evidence |
|---|---|---|
| Are multiple sessions truly concurrent? | No | `bed.c:103–149` — single-threaded `select()` loop |
| Is `xanadu()` preemptible mid-request? | No | `bed.c:153–172` — run to completion, no yield points |
| Does `insertseq()` modify the tree immediately? | Yes | `insert.c:43–69` — direct pointer manipulation |
| Does `findpreviousisagr` read live tree state? | Yes | `granf2.c:255–278` — walks in-memory crum pointers |
| **Can two sessions get the same ISA?** | **No** | The second session's `findpreviousisagr` walks an already-mutated tree |

The I-address non-overlap guarantee is **structurally absolute** given the single-process backend. It requires no explicit atomics or locking because the concurrency model admits no interleaving.
