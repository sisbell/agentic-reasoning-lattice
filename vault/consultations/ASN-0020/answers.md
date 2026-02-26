# Consultation Answers — Allocation Order Invariants

**Inquiry:** What must the system guarantee about the relationship between the temporal order in which content is allocated and its spatial position in V-space? Must allocation order correspond to document order?
**Date:** 2026-02-25 17:42
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> Must the position assigned to content within a document reflect the chronological order in which that content was created by its author?

### Nelson's Answer

# No. V-Space Position Is Independent of Creation Order.

The answer is unambiguously **no**. This independence is, in fact, one of the central architectural achievements of the I-space/V-space separation.

## The Two Address Spaces

Xanadu maintains two distinct address spaces, and they have different relationships to chronology:

**I-Space (permanent storage)** is append-only and therefore inherently chronological:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**V-Space (document arrangement)** is freely reorderable:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The position a user sees — the V-space position — bears no necessary relationship to when the content was created. Nelson makes this explicit:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

## Operations That Prove Independence

The FEBE protocol provides three operations that directly decouple V-space ordering from creation order:

1. **INSERT** — places new content at any arbitrary V-space position, not just at the end: "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

2. **REARRANGE** — transposes regions of existing content: "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3." [LM 4/67]

3. **COPY** (transclusion) — places content from *any other document* at any position in the current document: "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

If position had to reflect creation order, INSERT-at-position and REARRANGE would be incoherent operations.

## The Design Principle

Nelson is explicit that the addressing system imposes no structure on content arrangement:

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]

> "The Xanadu document may have any structure (sequential or not) and may hold any type of information." [LM 4/6]

And the version model reinforces that arrangement is arbitrary — no ordering is privileged:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

## One Exception: Links

There is one notable asymmetry. Unlike byte content, **links do maintain their creation-order addresses permanently**:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

So link `2.1` is always the first link created in that document, and link `2.755` is always the 755th. This ordering is fixed and reflects chronology. But this applies to links within their own subspace — it does not constrain the arrangement of byte content in V-space.

## Summary

| Aspect | Reflects creation order? |
|--------|--------------------------|
| I-space addresses | Yes — append-only, chronological |
| V-space positions (bytes) | **No** — freely reorderable via INSERT, REARRANGE |
| Link instance addresses | Yes — permanent order of arrival |

The document's V-space arrangement — the position content occupies as the user sees it — is entirely at the author's discretion. The whole point of separating I-space from V-space is to let content have a permanent, chronological identity (I-space) while being freely arrangeable into any order the author desires (V-space).

---

## Question 2 [nelson]

> When a user inserts new content between two existing passages, must the new content receive a position that falls between the positions of those passages, or may it receive a position that reflects only when it was added?

### Nelson's Answer

## Answer: Both, in Different Address Spaces

This question cuts to the heart of the I-space/V-space separation, which is the central architectural insight of Xanadu. The answer is that **both happen simultaneously**, in different address spaces that serve different purposes.

### In V-Space: Position Falls Between

When you INSERT content between two existing passages, the new content **does** receive a V-space position between them. Nelson specifies the INSERT operation explicitly:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

V-space addresses are dense and contiguous — there are no gaps. After insertion, the system renumbers everything after the insertion point. If passages A and B were at V-positions 1–50 and 51–100, and you insert 10 bytes between them, then A stays at 1–50, the new content occupies 51–60, and B shifts to 61–110.

Nelson confirms this ephemeral, mutable nature:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

### In I-Space: Position Reflects Only When Added

The new content's **permanent I-space address** reflects only when it was added — it is appended to the document's I-stream, chronologically, after all previously created content:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

I-space is the permanent home of content. An I-address never changes once assigned. Content created later always gets a later I-address, regardless of where it appears in the document's current arrangement. The I-address encodes origin (which server, which user, which document), not position in any arrangement.

### The Mapping Is the Document

The document itself **is** the mapping from V-space positions to I-space addresses. Each version defines a different mapping. Editing changes the mapping, not the underlying I-space content:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The POOM enfilade (Nelson's "eye in the pyramid" from Barus) maintains this V→I mapping efficiently, so that after an INSERT:

- V-space sees content in the new logical order (new content between old passages)
- I-space sees content in creation order (new content after all older content)
- Links point to I-space addresses and are therefore unaffected by the V-space renumbering

### Why This Matters

This separation is what makes the system's guarantees possible simultaneously:

| Guarantee | Enabled by |
|-----------|-----------|
| Links survive editing | Links point to I-space (stable), not V-space (shifting) |
| Historical backtrack | I-space preserves all content in creation order |
| Version comparison | Shared I-space origin reveals correspondence |
| Intuitive editing | V-space presents content in logical arrangement |

Nelson captures the user experience succinctly:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

The braid metaphor is apt. Each editorial change re-twists the V-space arrangement while the strands (I-space content) remain individually intact and permanently addressable.

### Summary

**V-space position**: Falls between the existing passages. V-addresses are renumbered to maintain a contiguous sequence.

**I-space address**: Reflects only when the content was added. Append-only, chronological, permanent.

The INSERT operation specifies a V-space target (`<doc vsa>`) for where the content should appear in the document's arrangement, but the content's permanent identity address in I-space is determined solely by when it was created.

---

## Question 3 [nelson]

> Does the system guarantee that content added later in time always appears after content added earlier, or can a user place new content at any position within a document regardless of when it was composed?

### Nelson's Answer

# New Content Can Be Placed at Any Position

The answer is unambiguous: **a user can place new content at any position within a document regardless of when it was composed.** This is not a side effect — it is the entire point of the I-Space/V-Space separation.

## Two Spaces, Two Orderings

Xanadu maintains two distinct address spaces with different ordering guarantees:

**I-Space (storage) is chronological and append-only:**

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content added later in time *does* receive a later I-Space address. This ordering is permanent and immutable. But users never see I-Space directly.

**V-Space (the document) is freely arrangeable:**

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The document *as the user sees it* is a V-Space arrangement — a mapping from sequential positions to I-Space content. This mapping can be changed at will.

## The Operations Prove It

The FEBE protocol provides explicit operations for arbitrary placement:

**INSERT** takes a position parameter:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The `<doc vsa>` (V-stream address) is the user's chosen insertion point — not determined by time of creation.

**REARRANGE** transposes content regions:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3." [LM 4/67]

This explicitly reorders existing content, breaking any temporal sequence.

**APPEND** is the *only* operation that adds to the end:

> "This appends \<text set\> onto the end of the text space of the document \<doc id\>." [LM 4/67]

The existence of APPEND as a separate operation from INSERT confirms that adding-at-end is a *special case*, not the default.

## The Architectural Intent

Nelson frames this separation as fundamental:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

The "braid" metaphor captures exactly this: strands are added chronologically to I-Space, but the braid itself (V-Space) can be twisted into any arrangement. The document's structure is editorial, not temporal.

The V-Space design intent states it plainly:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

Users work entirely in V-Space, where position is determined by editorial choice, not creation time.

## Summary

| Space | Ordering | User-Visible? | Editable? |
|-------|----------|---------------|-----------|
| **I-Space** | Chronological (append-only) | No | No — permanent |
| **V-Space** | Editorial (user-arranged) | Yes | Yes — INSERT, REARRANGE, DELETE |

Content added at 3pm can appear before content added at 9am. The I-Space preserves the fact that the 9am content was created first (enabling historical backtrack), but the V-Space — what the user actually reads — reflects the author's chosen arrangement, not the clock.

---

## Question 4 [nelson]

> Must the system's permanent identity for a piece of content encode any information about when that content was allocated relative to other content?

### Nelson's Answer

## No. Time Is Explicitly Excluded from the Address.

Nelson states this directly:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

The tumbler — Xanadu's permanent identity — encodes **structural position in the ownership tree**, not temporal position. Its four fields are Server, User, Document, and Element. None of these encode when content was created.

---

## What the Address DOES Encode

The I-space address tells you **where content belongs**, not **when it appeared**:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]

The address encodes **provenance** (which server, which account, which document) and **identity** (which element). That is all.

---

## The Subtle Point: Sequential Numbering Within a Document

Within a single document's element space, content IS numbered sequentially by creation. For links, Nelson is explicit:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

And the permascroll is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

So within a document, element 5 was allocated after element 4. This creates an implicit **relative ordering** that correlates with creation sequence. But this is a consequence of sequential allocation, not a temporal encoding. Nelson treats this as structural ordering, not time — which is why he says time is "kept track of separately."

---

## Cross-Document: No Temporal Ordering At All

Across documents, accounts, or servers, addresses encode **no** temporal relationship. Document 1.3.27 on server 1 has no temporal relationship to document 2.7.4 on server 2. Even within a single account, document numbers reflect allocation order under that account — but forking can create sub-addresses at any time:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." [LM 4/20]

Item 2.4 might be created long after item 2.5 if forking creates sub-digits under 2.4 later. The tree structure means numbering reflects **ownership delegation**, not chronology.

---

## Summary

| Scope | Does the address encode relative allocation time? |
|-------|---------------------------------------------------|
| Within a document's elements | Implicitly, through sequential numbering — but Nelson calls this ordering, not time |
| Across documents in one account | Allocation order only; forking breaks strict temporal sequence |
| Across accounts or servers | No temporal information whatsoever |

The answer to the question is **no** — the permanent identity is not required to encode temporal information. Nelson explicitly designed it this way. Time is metadata tracked alongside the address, not embedded within it.

---

## Question 5 [nelson]

> If two authors create content simultaneously in separate documents, must the system impose a global ordering on their content, or may their positions be entirely independent?

### Nelson's Answer

# Simultaneous Content Creation: Independent Positions

**Their positions are entirely independent.** The system requires no global ordering on content created by different authors in separate documents. This falls directly out of the tumbler addressing design.

## Why No Coordination Is Needed

The tumbler system is built on **owned numbers** with local allocation:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

Alice allocates I-space addresses under her subtree (`1.0.1.0.D.0.E`). Bob allocates under his (`1.0.2.0.D.0.E`). Neither needs to know the other exists. Each "baptizes" new positions autonomously.

## Time Is Explicitly Excluded from Addresses

Nelson is direct about this:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

If Alice and Bob create content at the same instant, their addresses are determined by their position in the ownership tree, not by when they wrote. There is no timestamp race, no global sequence number, no coordination.

## The Tumbler Line Is Notational, Not Causal

All tumblers do form a single sortable sequence — the "tumbler line." But this ordering is a mathematical consequence of the tree structure, not something that must be enforced:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." [LM 4/22]

Alice's account 1 comes "before" Bob's account 2 on the tumbler line purely because 1 < 2 in the tree — not because Alice created content first. The ordering is **structural**, determined at account creation time, not at content creation time.

## Distributed Servers Reinforce Independence

The BEBE protocol is designed for servers that operate semi-independently:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." [LM 4/72]

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

Each server maintains a locally valid model. Content created on different servers need not be synchronized in real-time. The system assumes "computer networks are always broken" [LM 4/75] and routes around disconnection — it clearly does not depend on global ordering of concurrent writes.

## Within a Single Document: Arrival Order Matters

The one place where ordering IS tracked is **links within a single document**:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

But this is local to a document under one owner's control — not a global ordering across independent authors.

## Summary

| Scope | Ordering | Source |
|-------|----------|--------|
| Across authors/documents | **Independent** — each owner allocates locally | Forking mechanism [4/17-4/20] |
| Across servers | **Independent** — each server valid in isolation | BEBE protocol [4/72] |
| Time vs. address | **Decoupled** — time tracked separately | Explicit statement [4/18] |
| Within one document's links | **Ordered** — permanent order of arrival | Link addressing [4/31] |

The docuverse is "all really one big forking document" [LM 4/18] — but the forking mechanism means each branch grows independently. No global clock, no global lock, no global ordering constraint across independent authors.

---

## Question 6 [nelson]

> When content is rearranged within a document through editing, must the original allocation order remain recoverable as a distinct property from the current document order?

### Nelson's Answer

# Yes — Original Allocation Order Is a Permanent, Distinct Property

The original allocation order (I-space) and the current document order (V-space) are **architecturally separate address spaces** in Xanadu. This separation is not incidental — it is the foundational design decision from which most of Xanadu's guarantees flow.

## The Two Orders

**I-Space (Invariant Space)** records the permanent creation order. Content is "filed, as it were, chronologically" [LM 2/14] into an append-only store. Every byte gets a permanent I-address encoding its origin (server, account, document, element position). This address **never changes**:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." — 4/11

**V-Space (Virtual Space)** records the current arrangement. V-addresses are dense, contiguous, and ephemeral:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." — 4/30

When REARRANGE transposes two regions of text [LM 4/67], it changes V-space — the mapping from "position in the document" to "which I-space content appears here." The I-space content itself is untouched. The original allocation order remains exactly as it was.

## Why Recoverability Is Required

The original allocation order must remain recoverable because multiple core guarantees depend on it:

### 1. Historical Backtrack

Any previous V-space arrangement can be reconstructed from the I-space content plus the version history:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." — 2/15

If I-space allocation order were lost, previous arrangements could not be reconstructed.

### 2. Link Survivability

Links point to I-space addresses, not V-space positions. This is explicitly why they survive editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." — 4/42

If the original allocation order were merged with or overwritten by the current arrangement, links would break on every rearrangement.

### 3. Correspondence (Version Comparison)

The SHOWRELATIONOF2VERSIONS operation identifies which parts of two versions correspond by finding shared I-space origins:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." — 4/70

Without preserving original allocation order as a distinct queryable property, the system could not compute which parts of two different arrangements are "the same content."

### 4. Origin Traceability

Every byte's I-address encodes its home document permanently:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." — 2/40

Rearranging content in V-space does not affect this. The I-address — which encodes the allocation order — remains the permanent proof of origin.

### 5. Delete Semantics

When content is removed from V-space, it persists in I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" — 4/9

The allocation order is what makes "deleted" bytes recoverable. They still exist at their original I-addresses even after V-space no longer references them.

## The Mapping Is the Document

Nelson's architecture treats the document as the **mapping** from V-space to I-space, not as the content itself:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." — 4/11

The front end works with V-addresses (intuitive positions). The back end maintains I-addresses (permanent identity). The enfilade structures implement this: the GRAN enfilade stores I-space content; the POOM enfilade maps V-space positions to I-space addresses [LM 1/33-1/36]. Each version is a different POOM mapping over the same GRAN content.

## Summary

The original allocation order is not merely "recoverable" — it is the **primary reality** of the system. V-space is the ephemeral view that changes with every edit. I-space is the permanent truth that never changes. The two are architecturally distinct, maintained by separate data structures (GRAN vs POOM), addressed by separate numbering, and serve different purposes. Rearranging content changes V-space while leaving I-space — and its allocation order — completely intact.

---

## Question 7 [nelson]

> Must the system distinguish between the order in which content was brought into existence and the order in which a reader encounters it within a finished document?

### Nelson's Answer

# Yes — This Distinction Is the Architectural Foundation

The separation between creation order and presentation order is not merely acknowledged in Xanadu's design; it is the central structural decision from which most other guarantees flow. Nelson gives these two orderings their own address spaces, their own data structures, and their own semantics.

## The Two Spaces

**I-Space** records the order in which content was brought into existence. It is append-only and chronological:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte receives a permanent I-space address at the moment of creation. That address never changes and that content never moves.

**V-Space** records the order in which a reader encounters content in the finished document. It is the "virtual byte stream" — the logical sequence as the user sees it now:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

The V-space arrangement is explicitly mutable:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

## The Document IS the Mapping

A document is not a container of bytes. It is the mapping from V-addresses to I-addresses — the function that says "position 1 in the reader's view corresponds to this permanently-stored byte, position 2 to that one, and so on."

Each version defines a different mapping. Editing changes the mapping, not the stored content:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

Nelson's analogy captures this precisely:

```
I-Space (Library)              V-Space (Reading Lists)
┌─────────────────────┐        ┌─────────────────────┐
│ Shelf A: "hello"    │        │ My Essay v1:        │
│ Shelf B: " world"   │   ──►  │   [ref A, ref B]    │
│ Shelf C: "!"        │        │                     │
│                     │        │ My Essay v2:        │
│ (never changes)     │   ──►  │   [ref A, ref C]    │
└─────────────────────┘        └─────────────────────┘
```

The library stacks (creation order) never change. Reading lists (presentation order) can be rearranged freely.

## Operations Prove the Distinction

The FEBE operations make the separation concrete:

- **INSERT** affects both: new bytes enter I-space (creation), and V-space positions shift to accommodate them. "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

- **REARRANGE** affects V-space only: "Rearrange transposes two regions of text." [LM 4/67] The bytes don't move in I-space; only the presentation order changes.

- **DELETE** affects V-space only: content is removed from the current view but "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9] The I-space content — in its original creation order — remains forever.

- **COPY** (transclusion) creates a new V-space mapping to existing I-space content. The presentation order of the new document is independent of when the content was originally created. "The material determined by \<spec set\> is copied to the document \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

## Why the Distinction Must Exist

Five guarantees depend on it:

**1. Link survivability.** Links point to I-space (creation identity), not V-space (current position). When a document is edited, V-addresses shift but I-addresses do not. "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/42-4/43]

**2. Version correspondence.** The system identifies matching parts across versions by shared I-space origin. Two V-space positions correspond if they map to the same I-address. "A facility that holds multiple versions is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

**3. Origin traceability.** Every byte's I-address encodes which document created it. "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40] This works precisely because I-addresses are permanent and independent of presentation order.

**4. Historical backtrack.** You can reconstruct any previous presentation order because the creation-order record is immutable. "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

**5. Non-destructive editing.** "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14] Xanadu abolishes this by keeping creation order sacred while letting presentation order evolve freely. "A document is really an evolving ONGOING BRAID." [LM 2/14]

## The Implementation

The enfilade data structures implement this separation directly:

- The **GRAN** (granfilade) stores actual content in I-space — the creation-order record
- The **POOM** (positional enfilade) maintains the V→I mapping — translation from presentation order to creation order

The "eye in the pyramid" insight (Bill Barus's contribution) was specifically about making this mapping efficiently updatable: "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order." [LM 1/34]

## Summary

The system does not merely distinguish between creation order and presentation order — it is *architecturally organized around* this distinction. I-space is creation order made permanent. V-space is presentation order made flexible. The document is the mapping between them. Every core guarantee — permanence, survivability, correspondence, traceability, non-destruction — depends on keeping these two orderings separate and never confusing one for the other.

---

## Question 8 [nelson]

> If a document is constructed by assembling previously existing content into a new arrangement, must the document order bear any relationship to the creation dates of those pieces?

### Nelson's Answer

# No. Document Order Is Independent of Creation Date.

This is one of the most fundamental architectural commitments in Xanadu: the separation of **content identity** (I-space) from **content arrangement** (V-space). The entire point of this separation is that arrangement is arbitrary with respect to storage order.

## The Core Separation

I-space stores content permanently in chronological order of creation:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

V-space is the document's arrangement — a view over that content:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

The phrase "regardless of their native origin" is decisive. A byte's position in V-space has nothing to do with when or where it was created in I-space.

## Arrangement Is Unconstrained

Nelson makes this explicit at the tumbler level:

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]

And at the version level:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

If no arrangement is a priori better than any other, then chronological order has no privileged status.

## The Operations Confirm This

The COPY operation (transclusion) places content at an arbitrary V-space position:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The user specifies `<doc vsa>` — the V-space address where the content goes. There is no constraint that this position must reflect when the source content was created.

The REARRANGE operation exists precisely to reorder content:

> "Rearrange transposes two regions of text." [LM 4/67]

If arrangement had to follow creation order, REARRANGE would be incoherent.

## Time Is Explicitly Not Part of Addressing

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Time is metadata, not structure. It can be queried ("What links came in from last week?") but it does not constrain how content is arranged within a document.

## The Compound Document Model

Nelson's vision of compound documents makes this independence vivid:

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

The Shakespeare example illustrates: E.G. Jewett's modified Hamlet is a quote-link to the first part of the original, then the word "luge," then a quote-link to the rest. The arrangement follows *literary intent*, not the creation dates of Shakespeare's text versus Jewett's insertion.

The glass pane metaphor reinforces this:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

The author paints and windows wherever they choose. The order of layers reflects composition decisions, not temporal sequence of the referenced content.

## Summary

The document's V-space order reflects the author's intended arrangement. The content's I-space addresses reflect chronological creation order. These two orderings are deliberately, structurally independent. A document assembled from pieces created in 1985, 2003, and 1971 can present them in any order — 2003 first, then 1971, then 1985 — without violating any constraint in the system. That is the entire point of separating I-space from V-space.

---

## Question 9 [nelson]

> Does the system guarantee that the permanent address space grows monotonically with time, such that later allocations always occupy higher positions than earlier ones?

### Nelson's Answer

## No — Tumbler Addresses Do Not Grow Monotonically With Time

The permanent address space does **not** guarantee that later allocations always occupy higher positions on the tumbler line. Nelson explicitly decouples time from addressing:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

### Why Monotonicity Fails Across Branches

The forking mechanism is designed specifically to allow insertion *between* existing addresses:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

The word "inserted" is key. Consider this scenario:

1. **T1:** Account `1.1` is created
2. **T2:** Account `1.2` is created (higher on the tumbler line)
3. **T3:** Account `1.1` creates document `1.1.1` (sits *between* `1.1` and `1.2` on the line)

At T3, a new allocation occupies a *lower* position than the allocation made at T2. This is the fundamental nature of tree-to-line flattening via depth-first ordering — children always sit between their parent and the next sibling of their parent.

Nelson's own description of the tumbler line confirms this is structural, not accidental:

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

And spans can be retroactively populated:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

### Where Monotonicity *Does* Hold

At a **single level of forking** — successive siblings under the same parent — allocation is monotonic by construction:

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

So within account `1.2`, documents `1.2.1`, `1.2.2`, `1.2.3` are created in that order and occupy successively higher positions. Sibling numbering is monotonic.

Similarly, within a single document's I-space, bytes are appended chronologically — the element field grows monotonically as content is added. This follows from the append-only storage model:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### Summary

| Scope | Monotonic with time? |
|-------|---------------------|
| Siblings under same parent | **Yes** — 2.1, 2.2, 2.3 allocated in order |
| Bytes within a single document | **Yes** — append-only, chronological |
| Across different branches of the tree | **No** — children appear between parent and parent's next sibling |
| Across different accounts or servers | **No** — forking inserts addresses between existing ones |
| Docuverse-wide | **No** — time is explicitly decoupled from address |

The design intent is **permanent addressability and unlimited insertion**, not temporal ordering. Time is metadata tracked separately; the tumbler encodes *provenance and ownership* (which server, which account, which document), not *when*.

---

## Question 10 [nelson]

> Must the system preserve the ability to reconstruct the exact temporal sequence of allocations, even when the resulting document presents content in a completely different reading order?

### Nelson's Answer

# Yes — Temporal Allocation Sequence Must Be Preserved

The system must preserve the ability to reconstruct the exact temporal sequence of allocations. This is not an optional feature or an edge case — it is structurally inherent in the I-space model and required by the historical backtrack guarantee.

## The Two-Space Architecture Requires It

The entire I-space/V-space separation exists precisely to decouple *creation order* from *reading order*. I-space is the permanent, append-only store where content lives in allocation order. V-space is the ephemeral arrangement that presents content in whatever reading order the user desires.

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The word "chronologically" is critical. I-space is ordered by time of creation. Bytes allocated first get lower I-addresses than bytes allocated later. This ordering is permanent — it is the I-space itself.

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

The "braid" metaphor describes strands accumulated over time. Each new allocation adds a strand. The braid can be viewed at any temporal cross-section (a version), but the strands themselves are ordered by when they were woven in.

## Historical Backtrack Depends On It

The guarantee that users can reconstruct any previous version requires knowing *what existed at any prior moment*:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "Being able to go back through changes, and perhaps restore an earlier state, is called the problem of historical backtrack." [LM 3/13]

To reconstruct "a given part of a given version at a given time," the system must know which allocations existed at that time. If temporal sequence were lost, you could not distinguish between "the document before paragraph 3 was added" and "the document after paragraph 3 was added." The V-space arrangement alone is insufficient — you need to know the I-space allocation timeline.

## The Address Structure Encodes It

I-space addresses inherently encode allocation order within a document. Links make this explicit:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Links are addressed sequentially by creation order (`2.1`, `2.2`, `2.755`), and this order is permanent — it cannot be rearranged. Content bytes follow the same principle: they are appended to I-space in allocation order, and that ordering is preserved in their addresses.

Meanwhile, V-space is explicitly the *mutable* layer:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

V-space order changes freely. I-space order is invariant.

## Canonical Order Is an Internal Mandate

The enfilade structure enforces this at the implementation level:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

"Internal mandate" — not a preference, not an optimization, but a requirement. The system must remain in canonical order after every change. This canonical order is the I-space allocation sequence.

## Time vs. Tumblers

Nelson distinguishes absolute timestamps from structural ordering:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Wall-clock time is metadata stored alongside the structure. But *relative temporal sequence* — what was allocated before what — is encoded in the I-space address ordering itself. The append-only model guarantees this: if byte A has a lower I-address than byte B in the same document, A was allocated first. This is not metadata; it is structural.

## The Direct Answer

The V-space/I-space separation is designed so that:

- **V-space** presents content in any reading order the user desires
- **I-space** preserves the exact allocation sequence permanently

These are not in tension. They are the *same design*. The ability to reconstruct temporal allocation sequence while presenting content in arbitrary reading order is the fundamental achievement of the two-space architecture. Losing the temporal sequence would destroy historical backtrack, break version reconstruction, and collapse the distinction that makes the whole system work.

To put it in Nelson's own terms: the I-space is the library stacks where books have permanent shelf locations. The V-space is the reading list that can be reordered at will. You can rearrange the reading list without moving books on the shelves — but the shelves must remain as they are.

---

## Question 11 [gregory]

> After INSERT "A" at V:1.1 then INSERT "B" at V:1.1 (same position, LIFO), the later-allocated "B" (higher I-address) appears before the earlier-allocated "A" in V-space — is this inversion of allocation-order vs. document-order the only mechanism that produces such inversions, or can REARRANGE and COPY also create them?

### Gregory's Answer

## KB Synthesis

## Inversion of Allocation Order vs. Document Order

The LIFO insertion phenomenon is one of at least three distinct mechanisms that can produce higher-I-address content appearing at lower V-addresses. REARRANGE and COPY both create such inversions, through different paths.

---

### The LIFO Insertion Baseline

From [ST-INSERT] (Finding 0027): INSERT at position P prepends to whatever exists at P. INSERT "A" at V:1.1 allocates I.1; INSERT "B" at V:1.1 allocates I.2 and shifts "A" to V:1.2. Result: I.2 at V:1.1, I.1 at V:1.2 — higher allocation order before lower. From [INV-MONOTONIC] (Finding 0033), I-address allocation is strictly chronological, so "higher I-address" is equivalent to "allocated later."

---

### REARRANGE Creates Inversions (By Design)

From [INV-REARRANGE-IDENTITY] (Findings 0016, 0056): REARRANGE is explicitly defined as a pure V-address permutation — it modifies only `ptr->cdsp.dsas[index]` (the V-dimension displacement) and never touches I-addresses. The multiset of I-addresses is invariant.

Concrete example:
- "AB" with I.1 at V:1.1, I.2 at V:1.2 (natural order)
- `pivot([1.1, 1.2, 1.3])` → "BA" with I.2 at V:1.1, I.1 at V:1.2
- Higher I-address (later-allocated "B") now precedes lower I-address (earlier-allocated "A") in V-space

REARRANGE is the most general inversion mechanism: it can produce **any** permutation of I-addresses in V-space, including the reversal case, arbitrary interleaving, or restoration of natural order. From [ST-REARRANGE] (Finding 0056), the offset arithmetic operates purely on tumbler values with no I-address awareness, so there is no constraint preventing cross-allocation-order placement.

---

### COPY Creates Inversions (Through Cross-Context Placement)

From [ST-VCOPY] (Finding 0018): VCOPY preserves I-addresses from the source — copied content carries the same I-addresses into the target document's V-stream.

From [PRE-COPY] (Finding 0046): COPY performs no duplicate checking and accepts the caller-specified V-position unconditionally.

This creates inversions when content with higher I-addresses (allocated more recently) is copied to a V-position before content with lower I-addresses (allocated earlier):

- Document A: INSERT "Old" → I.1–I.3 at V:1.1–1.3
- Document B: INSERT "New" → I.4–I.6 at V:1.1–1.3 (later allocation)
- VCOPY "New" from B, inserting at V:1.1 of A:
  - "New" occupies V:1.1–1.3 → I.4–I.6 (higher I-addresses, allocated later)
  - "Old" shifts to V:1.4–1.6 → I.1–I.3 (lower I-addresses, allocated earlier)
  - Inversion: later-allocated content precedes earlier-allocated content in V-space

The same mechanism applies to **internal transclusion** ([EC-SELF-TRANSCLUSION], [SS-POOM-MULTIMAP]): VCOPY from a document to itself places existing I-addresses at new V-positions. If the newly placed content (at its new V-position) comes before existing content with lower I-addresses, an inversion results. Since the POOM is a multimap ([SS-POOM-MULTIMAP], Finding 0039), the same I-address can exist at multiple V-positions simultaneously.

---

### Summary

| Mechanism | How Inversion Arises | Generality |
|-----------|---------------------|------------|
| INSERT (LIFO) | Prepend-at-position shifts earlier content to higher V-addresses | Creates inversions only at the insertion point |
| REARRANGE | Pure V-permutation leaves I-addresses fixed; any V-permutation is achievable | Most general: can produce any I-address ordering in V-space |
| COPY/VCOPY | Existing I-addresses placed at caller-specified V-positions regardless of relative allocation order | Creates inversions whenever source I-addresses are higher than target context I-addresses |

From [FC-INSERT-IADDR] (Finding 0030): INSERT never modifies the I-address of any pre-existing content; it only allocates fresh I-addresses for new content. REARRANGE and COPY operate on existing I-addresses. The common thread is that the V→I mapping in the POOM is a multimap with no ordering constraint between V-address order and I-address magnitude — nothing in the storage layer enforces correspondence between allocation chronology and document reading order.

## Code Exploration

Now I have enough source coverage to give a complete, fully-cited answer. Here it is:

---

## Answer: Three Distinct Mechanisms Produce I/V Inversions

The LIFO INSERT inversion is **not** the only mechanism. REARRANGE and COPY can both produce inversions of allocation-order vs. document-order, but each does so through a structurally distinct code path.

---

### 1. LIFO INSERT — the known case

**Code path:** `do1.c:doinsert` (line 87) → `do1.c:docopy` (line 119) → `orglinks.c:insertpm` (line 130) → `insertnd.c:insertnd` (line 51–58) → `insertnd.c:makegappm` (line 124).

In `insertnd.c:makegappm` (lines 144–168):

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
```

Two blades bracket the insert position. `edit.c:insertcutsectionnd` (lines 207–233) classifies every existing crum: those **at or after** `origin` (case 1) get their V-offset advanced:

```c
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified(ptr);
    break;
```

The newly-allocated I-address (always higher than any prior allocation) is then planted at `vsaptr` via `orglinks.c:insertpm` (line 113):

```c
movetumbler(vsaptr, &crumorigin.dsas[V]);
```

**Inversion mechanism:** Stack push. New (higher-I) content occupies `vsaptr`; old (lower-I) content is pushed right. Implicit and automatic — arises every time two INSERTs share the same V-address.

---

### 2. REARRANGE — explicit V-offset surgery

**Code path:** `orglinks.c:rearrangepm` (line 138) → `edit.c:rearrangend` (line 78).

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl,
                 typecutseq *cutseqptr) {
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

In `edit.c:rearrangend` the key step is at line 125:

```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
ivemodified((typecorecrum*)ptr);
```

**Only `cdsp.dsas[V]` is touched**. `cdsp.dsas[I]` is never modified. The `diff[]` offsets come purely from cut arithmetic (`edit.c:makeoffsetsfor3or4cuts`, lines 162–184):

For 3 cuts at [V_A, V_B, V_C]:
```c
diff[1] = V_C - V_B;   // region 1 jumps forward by size of region 2
diff[2] = -(V_B - V_A); // region 2 jumps backward by size of region 1
```

Regions 1 and 2 **swap** in V-space. Neither their I-addresses nor the permascroll content changes — only V-positions.

**Inversion mechanism:** Explicit block swap. If region 1 contains crums with lower I-addresses and region 2 contains crums with higher I-addresses, after REARRANGE the higher-I content precedes the lower-I content in V-space. No new I-addresses are allocated (as confirmed by Finding 0056). This is the deliberate purpose of REARRANGE — reorder V-space while preserving content identity.

**Example:** `"ABCDE"` with content allocated in order A→B→C→D→E (ascending I). After REARRANGE pivot at [V:1.2, V:1.4, V:1.6], the result is `"ADEBC"` (Finding 0056). `D` and `E` (higher I, allocated later) now precede `B` and `C` (lower I) in V-space.

---

### 3. COPY — arbitrary I↔V pairing

**Code path:** `do1.c:docopy` (line 45) → `orglinks.c:insertpm` (line 75).

In `do1.c:docopy` (lines 53–64):
```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)  // V-specs → source I-spans
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)      // plant at destination V
```

In `orglinks.c:insertpm` (lines 100–132), for each source I-span:
```c
unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
movetumbler(&lstream, &crumorigin.dsas[I]);   // source I-address
movetumbler(vsaptr, &crumorigin.dsas[V]);      // caller-specified dest V-address
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr); // advance vsaptr
```

**`lstream` (I-address) and `vsaptr` (V-address) are independently specified**. No constraint forces them to be monotonically aligned.

**Inversion mechanism:** Arbitrary I↔V pairing. Two ways this creates inversions:

**A — Cross-I-space transclusion to an earlier V-position:** If you COPY content from a later-allocated part of the permascroll (higher I-addresses) to a V-position earlier than existing content with lower I-addresses, the destination POOM will have higher-I crums preceding lower-I crums. `doinsert` itself is implemented this way (`do1.c:doinsert` line 118–119):
```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy(taskptr, docisaptr, vsaptr, ispanset)
```
INSERT is literally "allocate new I-address → COPY it to target V". The LIFO inversion is a special case of the general COPY mechanism where the freshly-allocated (highest) I-address lands at whatever V-position the caller specified.

**B — Propagation of existing inversions:** `specset2ispanset` traverses source content in source-V-space order. If the source already has inversions (from prior LIFO INSERT or REARRANGE), the retrieved I-spans will be in the inverted order, and COPY deposits them in that same order at the destination. Inversions are transitive through COPY.

Unlike INSERT, COPY reuses existing I-addresses (no new allocation). Unlike REARRANGE, COPY creates new POOM crums — the same I-address can appear at multiple V-positions simultaneously (Finding 0039 validates this; Finding 0046 documents the extension-vs-new-crum mechanics).

---

### Summary Table

| Property | LIFO INSERT | REARRANGE | COPY |
|---|---|---|---|
| New I-address allocated? | YES | NO | NO |
| I-axis changed by operation? | Via fresh alloc | Never touched | Uses existing I-addrs |
| V-address specified by? | Caller | Cut arithmetic | Caller |
| Creates POOM duplicates (same I, multiple V)? | No | No | Yes |
| Inversion mechanism | Stack push at V via `makegappm` | V-offset arithmetic on existing crums (`cdsp.dsas[V] += diff[i]`) | Arbitrary pairing: source I-spans deposited at caller-chosen V |
| Relevant code | `insertnd.c:makegappm:161–164` | `edit.c:rearrangend:125` | `orglinks.c:insertpm:105–131` |

**The LIFO INSERT inversion is not unique.** REARRANGE produces it deliberately (it is REARRANGE's purpose); COPY produces it structurally whenever a higher-I source region is transcluded to a lower-V destination. The three mechanisms share the same observable consequence — a POOM where `cdsp.dsas[V]` order does not monotonically match `cdsp.dsas[I]` order — but arrive there via entirely different code paths: stack push, cut-arithmetic offset addition, and unconstrained I/V pairing respectively.

---

## Question 12 [gregory]

> When COPY transcludes content from doc1 to doc2, the target POOM maps new V-positions to old I-addresses — does the POOM's `incontextlistnd` insertion-sort handle the case where transcluded I-addresses are interleaved with locally-allocated I-addresses that have higher values but earlier V-positions?

### Gregory's Answer

## KB Synthesis

## Short answer: yes — `incontextlistnd` sorts by V-address unconditionally, independent of I-address order.

Here is the full chain of reasoning.

---

### The scenario

After COPY, doc2's POOM can hold a configuration like this:

| V-position | I-address | Origin |
|---|---|---|
| 1.1 | I.1 | transcluded from doc1 (low I) |
| 1.2 | I.2 | transcluded from doc1 (low I) |
| 1.4 | I.100 | locally inserted in doc2 (high I) |
| 1.5 | I.101 | locally inserted in doc2 (high I) |

The I-address order and V-position order are misaligned: the transcluded content has numerically lower I-addresses but occupies earlier V-positions than locally-allocated content with high I-addresses.

---

### Why this situation arises

COPY does not allocate new I-addresses; it reuses the source document's existing ones [ST-COPY, INV-IADDR-PROVENANCE]. The I-address monotonic sequence in doc2 reflects doc2's own insertion history, so content COPYed in from doc1 carries low I-addresses regardless of when the COPY occurred [INV-MONOTONIC].

Because `isanextensionnd` requires both the same `homedoc` and contiguous I-addresses [ST-VCOPY, Finding 0046], transcluded content from doc1 will always create separate crums from locally-allocated content in doc2. The POOM therefore physically stores interleaved crums from different provenance sources.

---

### How the POOM tree organises these crums

The POOM is a 2D enfilade that orders its internal tree nodes by the **diagonal** (L1 norm) of the two displacement coordinates: `cdsp.dsas[ORGLRANGE] + cdsp.dsas[SPANRANGE]`, i.e. I-address + V-address [SS-ENFILADE-TREE, Finding 0071]. This ordering is used for rebalancing (`recombinend`/`shellsort`), and sibling order in the tree reflects it.

In the example above:
- Transcluded crums: diagonal ≈ I.1 + 1.1 → small
- Local crums: diagonal ≈ I.100 + 1.4 → large

The tree naturally places transcluded crums earlier in sibling order here. But consider the reverse: locally-inserted content at V 1.1 (low V, high I) and transcluded content at V 1.4 (high V, low I). Their diagonals might be comparable or even reversed, meaning tree traversal order and V-position order would diverge.

---

### Why retrieval is still correct

`findcbcinarea2d` traverses **all siblings at each level** and recurses into all qualifying subtrees, accumulating every matching leaf node [SS-DUAL-ENFILADE, Finding 0041]. It makes no assumption about the order in which contexts are discovered.

As each context is accumulated, `incontextlistnd` inserts it into a linked list sorted by `totaloffset.dsas[index]` — the left boundary in the queried dimension [SS-CONTEXT-LIST, Finding 0078]. For a V-range query (V→I direction), the sort key is V-address. The function performs explicit insertion-sort regardless of the discovery order from the tree traversal.

The KB states this invariant directly [INV-RETRIEVAL-V-SORTED]:

> `incontextlistnd()` performs explicit insertion-sort by V-address as contexts are discovered during B-tree traversal. Each leaf node found by `findcbcinarea2d()` is inserted into a linked list at the position that maintains ascending order.

And [INV-RETRIEVAL-TREE-INDEPENDENCE] confirms:

> The V-ordering of retrieval results is independent of the internal B-tree structure. Even if split/rebalance operations or out-of-order insertions produce a tree where sibling order does not match V-address order, the `incontextlistnd` insertion-sort re-establishes V-ordering during retrieval. Tree structure affects storage and traversal efficiency, but not the ordering of results.

The KB explicitly notes that this is *why* the N-dimensional enfilade uses `incontextlistnd` (insertion-sort) rather than `oncontextlistseq` (sequential append): the 2D diagonal tree structure does not guarantee V-order, so results must be re-sorted at collection time [SS-CONTEXT-LIST].

---

### What the sort key is for each retrieval direction

The `index` parameter to `incontextlistnd` selects which dimension to sort on:

- **V→I** (e.g., `vspanset2ispanset` converting a content region to I-addresses): sort key is V-address → results are V-sorted
- **I→V** (e.g., `ispan2vspanset` looking up which V-positions hold a given I-address, as in `find_links`): the same mechanism applies; results are sorted by whatever dimension is being queried

In neither direction does the I-address value of a crum determine its position in the output list. The I-address is the *restriction criterion* (which crums qualify), not the sort key.

---

### The `isanextensionnd` coalescing constraint

One subtle interaction: `isanextensionnd` only extends an existing crum when the new content is contiguous in **both** V and I dimensions and shares the same `homedoc` [ST-VCOPY, Finding 0046]. Transcluded content from doc1 will never coalesce with locally-inserted content from doc2 because the homedoc differs. This means:

- Two separate crums always exist for the two provenance classes
- The crums are stored independently in the POOM tree
- Retrieval correctly returns both, V-sorted by `incontextlistnd`

There is no code path that would merge or confuse crums from different home documents, so the interleaving poses no structural hazard.

---

### Summary

The scenario is correctly handled. The POOM's `incontextlistnd` insertion-sort is the deliberate mechanism for decoupling retrieval result order from tree-internal organisation [SS-CONTEXT-LIST, INV-RETRIEVAL-V-SORTED, INV-RETRIEVAL-TREE-INDEPENDENCE]. It sorts by V-address, making the output independent of I-address values, tree sibling order, or the diagonal-based rebalancing structure [SS-ENFILADE-TREE]. Transcluded I-addresses with low values at early V-positions and locally-allocated I-addresses with high values at later V-positions produce a correctly V-sorted retrieval result regardless of the order in which `findcbcinarea2d` discovers the crums.

## Code Exploration

Now I have everything I need for a complete, cited answer.

---

## Answer

### Architecture: `incontextlistnd` is a Retrieval Function, Not an Insertion Function

The first thing to establish is that **`incontextlistnd` is never called during COPY**. The call chain for `docopy` is:

```
docopy [do1.c:45]
  → insertpm [orglinks.c:75]      ← builds POOM crums
    → insertnd [insertnd.c:15]    ← inserts into enfilade tree
      → makegappm [insertnd.c:124]
      → doinsertnd [insertnd.c:185]
        → insertmorend [insertnd.c:219]
          → insertcbcnd [insertnd.c:242]
```

`incontextlistnd` has exactly one call site in the entire codebase, in the **retrieval** path:

```c
// retrie.c:263
incontextlistnd (headptr, context, index1);
```

inside `findcbcinarea2d` [retrie.c:229], which is called during V→I or I→V permutation queries. This is critical: the question's premise — that `incontextlistnd` is doing insertion-sort "when COPY transcludes content" — is inverted. The sort happens during read-out, not write-in.

---

### How COPY Writes Into the POOM

`insertpm` [orglinks.c:75-134] loops over the source I-spans (`sporglset`) and for each one builds a 2D crum:

```c
// orglinks.c:105-113
movetumbler (&lstream, &crumorigin.dsas[I]);   // I-address from source
movetumbler (vsaptr,   &crumorigin.dsas[V]);   // V-position in target doc
// ... compute V-width proportional to I-width ...
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // advance V insertion point
```

The last argument `V` [orglinks.c:130] tells `insertnd` the organizing dimension. The POOM enfilade tree is built and searched in V-order. I-addresses are **payload** stored in the crum's `cdsp.dsas[I]` / `cwid.dsas[I]` fields; they play no structural role in the tree. Mixed-provenance I-addresses (from doc1 vs. doc2) coexist without conflict because the tree only cares about V-positions.

Adjacent same-source crums are merged by `isanextensionnd` [insertnd.c:301-309], which checks both that `homedoc` fields match and that the existing crum's V/I reach exactly touches the new origin. Cross-source crums (different `homedoc`) are never merged, so transcluded doc1 ranges and locally-allocated doc2 ranges are stored as distinct crums in the POOM tree.

---

### How `incontextlistnd` Works During Retrieval

When a V→I or I→V permutation query runs (`permute` [orglinks.c:404] → `span2spanset` [orglinks.c:425] → `retrieverestricted` [retrie.c:56] → `retrieveinarea` [retrie.c:87] → `findcbcinarea2d` [retrie.c:229]), the 2D area walker visits every qualifying bottom crum:

```c
// retrie.c:252-264
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        // recurse into children
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);  // ← sort into result list
    }
}
```

`makecontextfromcbc` [context.c:151] copies the crum's absolute offset into `context->totaloffset` and its width into `context->contextwid`. Both V and I components are stored.

`incontextlistnd` [context.c:75-111] is a linked-list insertion sort. It calls `prologuecontextnd` [context.c:216] on the new context to get `grasp.dsas[index]` — the **start position in the `index` dimension** — then compares that against existing contexts using `whereoncontext` [context.c:124]:

```c
// context.c:80-110
prologuecontextnd (c, &grasp, (typedsp*)NULL);     // grasp.dsas[index] = start
...
if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
    // new start is TOMYLEFT(-2) or ONMYLEFTBORDER(-1) of head → prepend
} else {
    for (; nextc = clist->nextcontext; clist = nextc) {
        if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)   // ≥ THRUME
         && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER))  // = TOMYLEFT
            // insert between clist and nextc
    }
    // append at end
}
```

Using the constants from `common.h:86-90`:

```
TOMYLEFT=-2  ONMYLEFTBORDER=-1  THRUME=0  ONMYRIGHTBORDER=1  TOMYRIGHT=2
```

The sort key is **solely `grasp.dsas[index]`**. For a V-indexed sort (`index=V`), the I-addresses of the contexts are ignored. For an I-indexed sort (`index=I`), the V-positions are ignored. The two dimensions are completely independent.

---

### Does It Handle Interleaved Provenance?

**For V-sorted retrieval (`index1=V`, i.e. V→I lookup):**
The POOM tree was built in V-order. `findcbcinarea2d` traverses left-to-right through the enfilade, visiting crums in increasing V-start order. Each new context passed to `incontextlistnd` has a V-start strictly greater than or equal to all previous, so insertions always fall at the end of the list. I-addresses — whether from doc1's permascroll or doc2's — never participate in the comparison. There is no issue.

**For I-sorted retrieval (`index1=I`, i.e. I→V lookup):**
Contexts arrive in V-order (tree traversal) but must be placed into an I-ordered list. `incontextlistnd` is a correct insertion sort: each arriving context, regardless of its V-position, is inserted at the right I-address position. The scenario of "transcluded I-addresses interleaved with locally-allocated I-addresses" is precisely what this sort handles — the I-address of each context is compared against the existing list contents, and the context is spliced in wherever `grasp.dsas[I]` belongs.

---

### The One Genuine Boundary Defect — And Why It Doesn't Apply Here

There is a latent bug in the middle-insertion guard:

```c
// context.c:98-99
if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)   // > -1
 && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER))  // < -1
```

The second condition requires strictly `< -1`, i.e. only `TOMYLEFT(-2)`. If the new context's start falls exactly at `nextc`'s left border — returning `ONMYLEFTBORDER(-1)` — the condition fails. The loop advances past `nextc`, and the context is appended at the end instead of inserted before `nextc`. This places it out of order.

For this to occur at the I-dimension, two crums would need I-spans that are exactly adjacent in tumbler space: crum A ending at address X, and crum B starting at address X, while a third crum C arrives with I-start also equal to X.

This cannot arise from transcluded-vs-local content interleaving because:

1. **Different permascroll namespaces.** Doc1's permascroll addresses and doc2's addresses carry different account-level tumbler prefixes. They are in entirely separate regions of tumbler space. No doc1 I-boundary can coincide with any doc2 I-boundary.

2. **`isanextensionnd` merges within-source adjacencies.** Two crums from the same source document that are I-adjacent in the POOM are merged at insertion time [insertnd.c:250-258], so the pattern [A.I-end == B.I-start] with the same homedoc never persists as separate crums.

The defect is real but the only triggers are same-source crums with coincident I-boundaries — which are pre-emptively merged — or cross-account boundaries that coincide in tumbler arithmetic, which is structurally impossible.

---

### Summary

| Path | Where `incontextlistnd` lives | Sort key | I-address provenance effect |
|------|-------------------------------|----------|-----------------------------|
| COPY writes to POOM | `insertpm` → `insertnd`, index=V | — | I-addresses are payload, irrelevant to tree structure |
| V→I retrieval | `findcbcinarea2d` → `incontextlistnd`, index1=V | V-start only | No effect — I ignored |
| I→V retrieval | `findcbcinarea2d` → `incontextlistnd`, index1=I | I-start only | Handles interleaving correctly via insertion sort |

**`incontextlistnd` correctly handles the mixed-provenance interleaving scenario because the sort is one-dimensional: it compares only in the `index` dimension and ignores the other.** The arrangement of I-addresses within V-space (or V-positions within I-space) is irrelevant to the sort. The only structural concern — a boundary condition at `ONMYLEFTBORDER` in the middle-insertion guard — cannot be triggered by mixed transcluded/local content because cross-document I-addresses live in non-overlapping tumbler account spaces, and same-document adjacent I-spans are merged before they reach retrieval.

---

## Question 13 [gregory]

> Does REARRANGE (pivot or swap) ever update or recompute I-address-to-V-address mappings in the POOM's second dimension, or does it only modify V-displacements while leaving I-displacements untouched — meaning the 2D enfilade's I-dimension permanently reflects allocation order regardless of current V-order?

### Gregory's Answer

## KB Synthesis

Yes — REARRANGE modifies **only** the V-dimension displacement of POOM crums. The I-dimension is permanently frozen at allocation order and is never touched by rearrangement.

## Mechanism

The rearrange implementation in `edit.c:125` applies computed offsets via:

```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])
```

The `index` variable selects the V-dimension (SPANRANGE) only. [ST-REARRANGE], Finding 0056 is explicit: *"The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched. No new I-addresses are allocated, no content is duplicated in the permascroll, and the same enfilade nodes (crums) are retained."*

## POOM Crum Structure

Each POOM bottom crum holds dual-space coordinates [SS-POOM-BOTTOM-CRUM]:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler,  dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler,  dsas[V]: Tumbler }
}
```

After rearrangement, `dsas[V]` reflects the new virtual position; `dsas[I]` remains exactly where it was at allocation time.

## Consequence: Permanent I-Order Reflects Allocation Chronology

The I-dimension encodes insertion history, not current document structure. After a pivot of "BC" and "DE" in "ABCDE":

| Content | V-pos before | V-pos after | I-pos (always) |
|---------|-------------|------------|----------------|
| A | 1.1 | 1.1 | I.1 |
| B | 1.2 | 1.4 | I.2 |
| C | 1.3 | 1.5 | I.3 |
| D | 1.4 | 1.2 | I.4 |
| E | 1.5 | 1.3 | I.5 |

The V-dimension has been permuted; the I-dimension still reads I.1, I.2, I.3, I.4, I.5 in allocation order.

This is precisely what [INV-REARRANGE-IDENTITY] asserts: `i_addresses(doc_before_rearrange) = i_addresses(doc_after_rearrange)` as a multiset equality, and what [ST-REARRANGE] (Finding 0018) confirms empirically — `compare_versions` between pre- and post-rearrange states reports all content as shared because the I-addresses are identical.

## Why This Works in a 2D Enfilade

The POOM is a 2D B-tree with SPANRANGE (V) and ORGLRANGE (I) dimensions [SS-ENFILADE-TREE], [Finding 0066]. The relative-addressing invariant [INV-ENFILADE-RELATIVE-ADDRESSING] means `absolute_grasp(node) = sum_of_ancestor_displacements + node.cdsp` holds for both dimensions independently. Rearrangement adjusts ancestors' V-dimension `cdsp` values via `setwispupwards` after the displacement add, but the I-dimension subtree structure and displacements are untouched — the I-dimension wispography is read-only with respect to rearrange.

## Implication

The POOM after an arbitrary sequence of rearrangements is a non-identity permutation matrix: V-order may be any permutation of I-order. `compare_versions` works by ignoring V-addresses entirely and intersecting on I-addresses [INT-SPORGL-VERSION-COMPARE], which is exactly why it correctly detects shared content even after rearrangement. The I-dimension is the stable reference frame; the V-dimension is the mutable view.

## Code Exploration

I now have everything I need. Here is the full answer.

---

## Answer: REARRANGE, the I-Dimension, and the Permanence of Allocation Order

**Short answer: REARRANGE only ever modifies V-displacements. The I-dimension is never updated or recomputed by REARRANGE. The I-dimension permanently reflects permascroll allocation order regardless of current V-order.**

---

### The Call Chain

`dorearrange` [`do1.c:34`] → `rearrangepm` [`orglinks.c:137`] → `rearrangend` [`edit.c:78`]

```c
// orglinks.c:137-142
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);   // ← V is hardcoded
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`rearrangepm` passes `V` (= 1) as the `index` argument. This is the only call site. There is no call that passes `I`.

The `typeknives` struct in `ndenf.h:15-16` documents this as a structural constraint, not merely a runtime choice:

```c
typedef struct structknives {
    INT nblades;
    tumbler blades[MAXCUTS];
    INT dimension;  /* always V, assigned by rearrange2d */
} typeknives;
```

---

### What `rearrangend` Actually Does to Displacements

The displacement-modifying loop in `rearrangend` [`edit.c:113-135`]:

```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = (typecuc *)findrightbro((typecorecrum*)ptr)) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case 0:  case 4: /* these never move */
        break;
      case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
        tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
        //                       ^^^^^^^^^^                    ^^^^^^^^^^
        //                       index = V = 1                index = V = 1
        ivemodified((typecorecrum*)ptr);
        break;
    }
}
```

The only write is `ptr->cdsp.dsas[index]` where `index = V = 1`. The field `ptr->cdsp.dsas[I]` (index 0) is read for nothing and written for nothing. It is untouched.

Compare to `deletend` [`edit.c:63`] which follows the same pattern:

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

Both editing operations are axis-specific: they operate on the `index` dimension only, and `index` is always `V` for POOM operations.

---

### The POOM Coordinate System (from `wisp.h`)

```c
// wisp.h:19-20
#define I  0
#define V  1
```

Each POOM bottom crum (`type2dcbc`) carries a `typedsp cdsp` and `typewid cwid`, each an array of two tumblers:

```
cdsp.dsas[I]  →  permascroll origin of this run
cdsp.dsas[V]  →  document (virtual) origin of this run
cwid.dsas[I]  →  permascroll width of this run
cwid.dsas[V]  →  document (virtual) width of this run
```

These are set once at insertion time by `insertpm` [`orglinks.c:100-131`]:

```c
movetumbler (&lstream, &crumorigin.dsas[I]);   // from permascroll sporgl
movetumbler (vsaptr, &crumorigin.dsas[V]);     // from document VSA
// ...
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

The I-origin is the permascroll address (`lstream`) allocated when text was stored in the granfilade. The V-origin is the document address (`vsaptr`) chosen at copy time. After `insertnd` completes, neither is ever touched by REARRANGE.

---

### The One Subtlety: `slicecbcpm` During Cut Preparation

`rearrangend` calls `makecutsnd` first to prepare the tree. When a V-cut boundary falls inside an existing bottom crum, `makecutsnd` calls `slicecbcpm` [`ndcuts.c:373`] to split it. This function **does** modify I-values — but only to structurally subdivide an existing run, not to remap I-positions to new V-positions:

```c
// ndcuts.c:438-446
movewisp (&ptr->cwid, &newwid);
for (i = 0; i < widsize(enftype); i++) { /* I really don't understand this loop */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];   // same first digit for I AND V
    tumblerjustify (&newwid.dsas[i]);
}
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, (unsigned)widsize(enftype));
movewisp (&newwid, &ptr->cwid);
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);   // new->cdsp = old_dsp + new_wid (both I and V)
```

What this does: the V-cut position's leading digit (`localcut.mantissa[0]`) is applied proportionally to **all** dimensions. If the V-cut falls 40% through the crum's V-extent, the I-extent is also split 40%/60%. The second fragment's I-displacement is set to `first_I_displacement + first_I_width`.

This maintains the POOM's invariant: **within a single bottom crum, I-order equals V-order** (they represent a contiguous physical run). The split correctly subdivides the run into two contiguous sub-runs, each still mapping a contiguous I-range to a contiguous V-range. This is a structural consistency operation — the permascroll addresses of the bytes do not move, they are simply correctly partitioned between the two resulting crum records.

After `makecutsnd` returns, the V-cut displacement adjustments in `rearrangend` touch only `cdsp.dsas[V]`.

---

### How V↔I Lookup Works Post-Rearrangement

`ispan2vspanset` and `vspanset2ispanset` [`orglinks.c:389-402`] both call `permute`, which calls `span2spanset` → `retrieverestricted` → `findcbcinarea2d` [`retrie.c:229`].

`findcbcinarea2d` walks the POOM tree checking both dimensions simultaneously via `crumqualifies2d` [`retrie.c:270`]:

```c
// retrie.c:282-301
endcmp = whereoncrum (crumptr, offset, span1end, index1);     // check restriction dim
...
startcmp = whereoncrum (crumptr, offset, span1start, index1);
...
endcmp = whereoncrum (crumptr, offset, span2end, index2);     // check target dim
...
startcmp = whereoncrum (crumptr, offset, span2start, index2);
```

For `ispan2vspanset`, `index1=I, index2=V`. This works correctly after REARRANGE because:
- The I-values are stable (never changed by REARRANGE)
- The V-values of each crum have been updated to the new document positions
- The 2D tree walk finds all crums whose I-range overlaps the query, and for each qualifying crum, reads its V-position

---

### Summary

| Operation | Touches `cdsp.dsas[I]`? | Touches `cdsp.dsas[V]`? |
|---|---|---|
| `insertpm` / `insertnd` | Yes — set once from permascroll stream | Yes — set from document VSA |
| `rearrangend` (displacement update) | **No** | **Yes** — shifted by `diff[i]` |
| `makecutsnd` → `slicecbcpm` (cut prep) | Yes — proportionally subdivided | Yes — proportionally subdivided |
| `deletend` | **No** | **Yes** — subtracted by deleted width |

**The I-dimension is permanently set at allocation time and is never recomputed in response to V-order changes.** REARRANGE exclusively adjusts V-displacements. The POOM's 2D structure encodes the permutation implicitly: any given set of crums in V-order can differ from that same set of crums in I-order. The retrieval functions (`permute`/`findcbcinarea2d`) exploit this 2D layout to cross-convert between V-spans and I-spans, but no bookkeeping structure is maintained for this mapping — the POOM crums *are* the mapping.

The answer to the question is unambiguous: **REARRANGE modifies only V-displacements. The I-dimension permanently reflects permascroll allocation order.** After any number of rearrangements, the I-addresses of all crums are exactly as they were when their content was first written to the permascroll.

---

## Question 14 [gregory]

> When `retrievevspansetpm` walks the POOM to return document content, does it enumerate entries in V-address order or in I-address order, and what guarantees that the returned spans reflect current document order rather than allocation order?

### Gregory's Answer

## KB Synthesis

## Retrieval Order in `retrievevspansetpm`

The answer requires synthesizing the traversal mechanism, the accumulation strategy, and the independence of those from POOM tree topology.

### Traversal Dimension: V-Address, Not I-Address

`retrievevspansetpm` queries the POOM in the V-dimension — it constructs separate link and text spans by reading V-displacement/width metadata from the POOM tree, using `is1story()` to detect subspace boundaries and `maxtextwid()` for recursive V-extent traversal [SS-DUAL-ENFILADE, SS-VSPAN-VS-VSPANSET]. The POOM stores `(V-position, I-address)` mappings; retrieval that produces V-spans necessarily walks in V-space.

### The Sorting Guarantee

When the POOM B-tree is traversed by `findcbcinarea2d`, siblings are walked left-to-right in tree order — but tree sibling order does not necessarily match V-address order. The 2D rebalancing algorithm uses a diagonal sort (`shellsort` by L1-norm of both address dimensions) during rebalancing, which can produce trees where sibling order is unrelated to V-address sequence [SS-ENFILADE-TREE, ST-REBALANCE-2D].

The V-ordering guarantee is supplied by `incontextlistnd()`, which performs **explicit insertion-sort by V-address left boundary** as each context is discovered during traversal [SS-CONTEXT-LIST]. Each discovered leaf node is inserted at the position maintaining ascending order of `totaloffset.dsas[V]`. This is the mechanism for N-dimensional (POOM) enfilades; 1D (GRAN) enfilades use `oncontextlistseq()` which merely appends in tree order.

The invariant is stated formally in [INV-RETRIEVAL-V-SORTED]:

```
∀ j, k :: 0 ≤ j < k < |contexts| ⟹
  contexts[j].totaloffset.dsas[V] ≤ contexts[k].totaloffset.dsas[V]
```

This holds regardless of which order the B-tree delivers contexts.

### Why V-Order = Current Document Order, Not Allocation Order

I-addresses encode *when* content was allocated (monotonically increasing by insertion time) [INV-MONOTONIC, SS-ADDRESS-SPACE]. V-addresses encode *where* content currently sits in the document. These diverge whenever:

- **INSERT** shifts all entries after the insertion point in V-space, leaving their I-addresses unchanged [ST-INSERT, FC-INSERT-IADDR]
- **REARRANGE** changes V-addresses by adding computed displacements to `cdsp.dsas[V]` without touching I-addresses at all [ST-REARRANGE, INV-REARRANGE-IDENTITY]

Because `incontextlistnd()` sorts by the V-dimension, rearranged content appears at its post-rearrangement V-position in results — not at its original I-address-derived allocation order. A pivot that moves "XYZ" from V:1.1–1.3 to V:1.7–1.9 will return "XYZ" as the last span in retrieval, even though its I-addresses were allocated first.

### Independence From Tree Shape

The sort is performed during retrieval, so tree-internal reorganization (splits, rebalances per [ST-SPLIT-2D, ST-REBALANCE-2D]) does not affect result ordering. Two trees containing identical `(V, I)` entries in different structural arrangements produce identical retrieval sequences [INV-RETRIEVAL-TREE-INDEPENDENCE, FC-ENFILADE-QUERY-INDEPENDENCE].

### Summary

`retrievevspansetpm` enumerates in **V-address order**. The guarantee comes entirely from `incontextlistnd()`'s insertion-sort during B-tree traversal — not from any tree-level structural invariant. Because V-addresses reflect the current state of all INSERT and REARRANGE operations (which modify V-positions while leaving I-addresses intact), V-order equals current document order by definition, irrespective of allocation chronology.

## Code Exploration

I now have everything needed to answer comprehensively. Here is the full analysis.

---

## How `retrievevspansetpm` Enumerates Spans and What Guarantees Document Order

### The Live Implementation (orglinks.c:173–221)

`retrievevspansetpm` in its current form **does not walk the POOM tree by enumeration at all**. It reads aggregate information directly from the root crum (the `orgl` cast to `typecorecrum *`).

```c
/* orglinks.c:181 */
ccptr = (typecorecrum *) orgl;
```

It then branches on `is1story` [tumble.c:237–247], which tests whether `cwid.dsas[V].mantissa[1..NPLACES-1]` are all zero — i.e., whether the V-width is a single-story tumbler (no link space, pure text document):

---

#### Case 1: Single-story V-width (text-only document) — orglinks.c:184–190

```c
if (is1story (&ccptr->cwid.dsas[V])) {
    vspan.itemid = VSPANID;
    movetumbler (&ccptr->cdsp.dsas[V], &vspan.stream);
    movetumbler (&ccptr->cwid.dsas[V], &vspan.width);
    vspan.next = NULL;
    putvspaninlist (taskptr, &vspan, vspansetptr);
    return TRUE;
}
```

No traversal at all. The root crum's `cdsp.dsas[V]` (V-displacement) and `cwid.dsas[V]` (V-width) are read directly, and a **single aggregate vspan** covering the entire document is returned. This is the common case for plain documents.

---

#### Case 2: Multi-story V-width (document with both text and link space) — orglinks.c:192–220

```c
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.stream);
linkvspan.stream.mantissa[1] = 0;    // zero out story-1 component
tumblerjustify(&linkvspan.stream);   // left-justify the mantissa
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.width);
linkvspan.width.mantissa[1] = 0;
tumblerjustify(&linkvspan.width);
// ...
maxtextwid(taskptr, ccptr, &voffset, &maxwid);
vspan.itemid = VSPANID;
tumblerclear (&vspan.stream);
movetumbler (&maxwid, &vspan.width);
vspan.width.mantissa[0] = 0;         // zero out story-0 component
```

Two vspans are built: one for the text portion (story 0) and one for the link portion (story 1). The text span is found by calling `maxtextwid`.

**`maxtextwid` (orglinks.c:224–245)** walks the tree via `findleftson`/`findrightbro` to find the maximum V-reach of text crums:

```c
if (istextcrum (crumptr)) {
    tumbleradd (voffset, &crumptr->cdsp.dsas[V], &tmpwid);
    tumblermax(&tmpwid, maxwidptr, maxwidptr);
} else {
    tumbleradd (voffset, &crumptr->cdsp.dsas[V], &localvoffset);
    for(ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro (ptr)){
        if(ptr && !islinkcrum(ptr)){
            maxtextwid(taskptr, ptr, &localvoffset, maxwidptr);
        }
    }
}
```

`istextcrum` (orglinks.c:246–253) identifies leaves with `cdsp.dsas[V].mantissa[1] == 0` and a single-story width. `islinkcrum` (orglinks.c:255–260) identifies crums entirely in link space (`cdsp.dsas[V].mantissa[0] == 1 && mantissa[1] != 0`).

This traversal follows **sibling-chain order** (leftmost to rightmost child per node, depth-first), which is the internal tree order — not intrinsically V-sorted. But the goal is only to find a maximum, not to emit ordered spans.

---

### The Abandoned Implementation (`#ifdef UnDEFined`, orglinks.c:263–313)

The original design used `walkorglonvpm`:

```c
bool retrievevspansetpm(...) {     // orglinks.c:266
    tumblerclear (&voffset);
    *vspansetptr = NULL;
    walkorglonvpm (taskptr, (typecorecrum*)orgl, &voffset, vspansetptr);
    cleanupvspanlist (taskptr, vspansetptr);
    return (TRUE);
}

int walkorglonvpm(...) {           // orglinks.c:277
    if (is1story (&crumptr->cwid.dsas[V])) {
        vspan.itemid = VSPANID;
        tumbleradd (voffset, &crumptr->cdsp.dsas[V], &vspan.stream);
        movetumbler (&crumptr->cwid.dsas[V], &vspan.width);
        putvspaninlist (taskptr, &vspan, vspansetptr);
    } else {
        tumbleradd (voffset, &crumptr->cdsp.dsas[V], &localvoffset);
        for(ptr = findleftson(...); ptr; ptr = findrightbro (ptr)){
            walkorglonvpm(taskptr, ptr, &localvoffset, vspansetptr);
        }
    }
}
```

This **did** enumerate bottom crums, also in sibling-chain tree order. It accumulated V-displacements top-down, computed each leaf's absolute V-address as `voffset + cdsp.dsas[V]`, and submitted each leaf's vspan to `putvspaninlist`. Then `cleanupvspanlist` merged adjacent spans.

---

### What Guarantees Returned Spans Reflect Current Document Order (V-order)

Three independent mechanisms work together:

#### 1. V-displacement maintenance by `makegappm` on insertion

When `insertpm` [orglinks.c:100] calls `insertnd` [insertnd.c:15] with `index=V`, the POOM path invokes `makegappm` [insertnd.c:54]. This function classifies each sibling via `insertcutsectionnd` [edit.c:207–233]. A return value of `1` means the crum's span lies entirely to the right of the insertion cut, triggering an explicit V-displacement increment:

```c
/* insertnd.c:162 */
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified (ptr);
    break;
```

Every crum displaced rightward in document order gets its `cdsp.dsas[V]` increased by the inserted width. This is the primary mechanism that keeps V-displacements current.

#### 2. V-displacement maintenance by `deletend` on deletion

In `deletend` [edit.c:31], `deletecutsectionnd` [edit.c:235] returns `2` for crums to the right of the deleted range, causing:

```c
/* edit.c:63 */
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

Rightward crums have their V-displacement reduced by the deleted width, keeping them V-correct.

#### 3. `putvspaninlist` enforces V-sorted insertion into the output list

Even if the tree were walked in arbitrary order, `putvspaninlist` [orglinks.c:329–387] performs a **sorted insert by V-address**, comparing `spanptr->stream` against existing spans' streams and reaches, and merges contiguous/overlapping spans. Regardless of what order crums are visited during `walkorglonvpm`, the final vspan list is sorted by V-address and has redundant ranges coalesced.

```c
/* orglinks.c:345 */
spancmp = tumblercmp (&spanptr->stream, &oldspanend);
if (!spancmp) {
    tumbleradd (&ptr->width, &spanptr->width, &ptr->width);  // extend
    return(0);
} else if (spancmp == GREATER)
    continue;
// ...else insert before ptr
```

Similarly, `incontextlistnd` [context.c:75–111], the sorted-insert function used for context lists in the `permute`/`vspanset2ispanset` path, explicitly labels itself **"put c on clist in index order"** and inserts by comparing the supplied `index` dimension — V or I depending on the call.

---

### Summary

| Question | Answer |
|---|---|
| Does `retrievevspansetpm` walk the POOM? | **No** (live code). The simple case reads the root aggregate directly; the multi-story case uses `maxtextwid` to find maximum text reach, walking in sibling-chain tree order, not V-order. |
| What order does the abandoned `walkorglonvpm` walk in? | Sibling-chain order (leftmost to rightmost per node, depth-first), which is internal tree order — neither strictly V nor I. |
| What guarantees the result reflects current document order? | (1) `makegappm` [insertnd.c:162] shifts `cdsp.dsas[V]` of rightward crums on every insert; (2) `deletend` [edit.c:63] shifts `cdsp.dsas[V]` of rightward crums on every delete; (3) `putvspaninlist` [orglinks.c:329] re-sorts and merges spans by V-address as they are added to the result list, regardless of traversal order. |
| Where is I-address order used? | I-addresses are permanent allocation-order coordinates (`cdsp.dsas[I]`). The `vspanset2ispanset`/`permute` path [orglinks.c:397–422] uses `retrieverestricted` with `index=V` and `targindex=I` to cross-reference V-spans to their I-spans; `incontextlistnd` [context.c:75] then inserts those into a list sorted by the queried index. |

The absolute V-address of any bottom crum at retrieval time is the sum of all its ancestors' `cdsp.dsas[V]` values accumulated root-to-leaf. Because `makegappm` and `deletend` update these displacements on every mutation, and because `putvspaninlist` sorts the output by V-address regardless, the returned spans always reflect the document's current virtual order rather than allocation order.

---

## Question 15 [gregory]

> In `findcbcinarea2d`, when the 2D tree traversal encounters POOM entries where V-order and I-order diverge (e.g., after a REARRANGE), does the diagonal-sum ordering used in `recombinend` for rebalancing risk placing entries in a physical tree order that conflicts with the V-address insertion-sort in `incontextlistnd`?

### Gregory's Answer

## KB Synthesis

## Answer: No Conflict on Correctness; Performance Interaction Exists

The diagonal-sum ordering in `recombinend` and the V-address insertion-sort in `incontextlistnd` operate at different levels of abstraction and do not conflict. The insertion-sort is the invariant-holder; the tree organization is merely an efficiency concern.

### Why There Is No Correctness Conflict

`incontextlistnd` performs an **explicit, unconditional insertion-sort** by V-address on every context it receives, regardless of the order in which `findcbcinarea2d` discovers them [SS-CONTEXT-LIST]. Each arriving leaf is individually placed into the correct position in the result list via `whereoncontext()` + `intervalcmp()`. The sort does not assume or exploit any ordering property of the tree traversal.

This is stated directly as an invariant:

> [INV-RETRIEVAL-TREE-INDEPENDENCE]: "Even if split/rebalance operations (Finding 0071) or out-of-order insertions (Finding 0041) produce a tree where sibling order does not match V-address order, the `incontextlistnd` insertion-sort re-establishes V-ordering during retrieval. Tree structure affects storage and traversal efficiency, but not the ordering of results."

And as a postcondition:

> [INV-RETRIEVAL-V-SORTED]: The result list is sorted by left boundary in the queried dimension, **independent of tree structure** — it holds regardless of insertion order, split/rebalance operations, or diagonal ordering in 2D enfilades.

The `findcbcinarea2d` traversal walks siblings left-to-right via sibling links [SS-ENFILADE-TREE], so after diagonal-sort rebalancing the traversal order follows diagonal-key order — but `incontextlistnd` treats this as an arbitrary permutation of correct values and re-sorts. No matter what order contexts arrive, the postcondition holds.

### The Performance Interaction After REARRANGE

After REARRANGE displaces V-positions while leaving I-positions fixed [ST-REARRANGE], V-order and I-order in the POOM diverge. Subsequent rebalancing in `recombinend` uses diagonal keys `cdsp.dsas[0] + cdsp.dsas[1]` (I-sum + V-sum) [SS-ENFILADE-TREE] to order siblings for merge consideration, and `splitcrumpm` uses SPANRANGE (V-space) only for splits [ST-SPLIT-2D]. Neither of these organizing principles is V-address order after a cross-region rearrangement.

The effect: `findcbcinarea2d` delivers contexts to `incontextlistnd` in an order that may be poorly correlated with V-address order. Insertion-sort is O(n) when input arrives sorted, O(n²) worst-case when it arrives reversed. After significant REARRANGE operations, traversal order correlates poorly with V-order, so `incontextlistnd` may operate near its worst-case quadratic bound.

This is a **performance degradation, not a correctness failure**.

### The POOM Split/Merge Asymmetry

There is an additional asymmetry specific to the POOM worth noting [ST-SPLIT-2D]:

| Operation | POOM uses | SPAN uses |
|-----------|-----------|-----------|
| `recombinend` (merge) | diagonal L1 key (V+I) | diagonal L1 key (V+I) |
| `splitcrumpm` / `splitcrumsp` (split) | SPANRANGE only (V) | diagonal L1 key (V+I) |

So for POOM, split and rebalance use *different* dimensional orderings. After REARRANGE fragments V/I correlation, this asymmetry means split may produce a tree shape that `recombinend` then reorganizes using a different criterion. The result is a tree whose physical organization reflects neither pure V-order nor pure I-order — but since `incontextlistnd` sorts by V regardless, the retrieval invariant is unaffected.

### Conclusion

The diagonal-sum ordering in `recombinend` cannot conflict with `incontextlistnd`'s correctness because [INV-RETRIEVAL-V-SORTED] is achieved by an explicit per-result sort that is independent of tree structure [INV-RETRIEVAL-TREE-INDEPENDENCE]. REARRANGE-induced V/I divergence makes the traversal order more random relative to V-order, degrading insertion-sort performance from O(n) toward O(n²), but the final sorted output is always correct.

## Code Exploration

I now have all the code I need. Let me write the complete analysis.

---

## Full Analysis: `findcbcinarea2d`, diagonal-sum rebalancing, and `incontextlistnd` ordering

### 1. The coordinate model

From `wisp.h:19-20`:
```c
#define I  0
#define V  1
```

A POOM crum has a 2D displacement: `cdsp.dsas[0]` is the I-displacement and `cdsp.dsas[1]` is the V-displacement. Both are stored per-crum as `typedsp` (a `typewid` of `tumbler dsas[MAXLOXIZE]`, `MAXLOXIZE=2`).

---

### 2. How REARRANGE creates V/I divergence

`rearrangend` in `edit.c:78-160` operates on a single dimension. From `ndenf.h:15`:
```c
INT dimension;  /* always V, assigned by rearrange2d */
```

The core of `rearrangend` shifts V-positions of crums falling in each cut-section, updating only `cdsp.dsas[index]` (V):

```c
// edit.c:125
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

I-positions (`cdsp.dsas[I]`) are never touched. After a REARRANGE, a crum that was at V=10, I=2 might now be at V=3, I=2. Siblings' V-order can be completely inverted relative to their I-order. The tree structure does not require any ordering of siblings in a 2D enfilade, so no tree invariant is violated.

---

### 3. The diagonal-sum sort in `recombinend`

`recombine.c:118` calls `getorderedsons` before pairing:

```c
// recombine.c:270-280
int getorderedsons(typecuc *father, typecorecrum *sons[])
{
  ...
  for (ptr = getleftson (father), i = 0; ptr; ptr =(typecorecrum *)getrightbro (ptr))
      sons[i++] = ptr;
  sons[i] = NULL;
  shellsort (sons, i);
}
```

`shellsort` (`recombine.c:282-311`) builds its sort keys as:
```c
// recombine.c:296-300
for(i=0;i<n;i++){/* build up a list of sumps of disp[0] and dsp[1]*/
                 /* for compare crums diagonally hack */
    tumbleradd(&v[i]->cdsp.dsas[0],&v[i]->cdsp.dsas[1],&tarray[i]);
    tarrayp[i] = &tarray[i];
}
```

This is `cdsp[I] + cdsp[V]` per sibling. The comment explicitly calls it a "hack." The standalone `comparecrumsdiagonally` function (`recombine.c:313-320`) confirms the intent:
```c
tumbleradd (&a->cdsp.dsas[0], &a->cdsp.dsas[1], &amagnitude);
tumbleradd (&b->cdsp.dsas[0], &b->cdsp.dsas[1], &bmagnitude);
return (tumblercmp (&amagnitude, &bmagnitude));
```

After a REARRANGE, the V-components have been reshuffled while I-components were left untouched. The diagonal sum `I+V` no longer corresponds to either axis's ordering. The sorted `sons[]` array is therefore a semantically arbitrary sequence — it is neither V-ordered nor I-ordered in any predictable way.

The sort determines which sibling *pairs* `(sons[i], sons[j])` are candidates for merging via `takeovernephewsnd`. It does **not** physically reorder the sibling chain in the tree — `takeovernephewsnd` either removes `bro` entirely (`eatbrossubtreend`) or migrates children from `bro` to `me`, appending them with `RIGHTMOSTSON`.

---

### 4. `findcbcinarea2d` makes no assumption about sibling order

```c
// retrie.c:252-265
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, (type2dbottomcruminfo*)infoptr)){
        continue;
    }
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

This is a **complete linear scan** of all siblings. Every sibling is tested against `crumqualifies2d` (`retrie.c:270-305`), which is a pure 2D area intersection test on both dimensions independently. There is no early stopping, no binary search. The traversal order through siblings is `getrightbro` in physical tree order, but all siblings are visited. This is the correct implementation for a 2D enfilade, where no single ordering of siblings is structurally guaranteed.

---

### 5. `incontextlistnd` is an insertion sort — order-independent

```c
// context.c:74-111
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
  typecontext *clist, *nextc;
  typedsp grasp;

    prologuecontextnd (c, &grasp, (typedsp*)NULL);
    c->nextcontext = NULL;
    clist = *clistptr;
    /* 1st insertion */
    if (!clist) { *clistptr = c; return(0); }
    /* on beginning */
    if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist;
        *clistptr = c;
        return(0);
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            /* in middle */
            if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
                && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
                c->nextcontext = nextc;
                clist->nextcontext = c;
                return(0);
            }
        }
    }
    /* on end */
    c->nextcontext = NULL;
    clist->nextcontext = c;
}
```

The sort key is `grasp.dsas[index]` (absolute address on dimension `index`, typically V=1). `prologuecontextnd` (`context.c:216-221`) computes this as `totaloffset` from the context:

```c
int prologuecontextnd(typecontext *ptr, typedsp *grasp, typedsp *reach)
{
    movewisp (&ptr->totaloffset, grasp);
    if (reach)
        dspadd (grasp, &ptr->contextwid, reach, ptr->contexttype);
}
```

The `totaloffset` is the accumulated sum of `cdsp` values along the root-to-leaf path, set at context creation time by `makecontextfromcbc` (`context.c:151-174`). This absolute address is independent of where the crum sits in sibling order.

The insertion sort at `context.c:90-106` finds the right position by walking the already-sorted linked list and comparing absolute addresses. **No assumption about input order is made.** Contexts arriving in reverse-V order, scrambled order, or V-order are all handled identically and correctly.

---

### Direct answer to the question

**There is no conflict between the diagonal-sum ordering in `recombinend` and the V-address sort in `incontextlistnd`.**

The insertion sort in `incontextlistnd` is correct regardless of traversal order. `findcbcinarea2d` scans all siblings unconditionally, so physical sibling order is irrelevant to completeness. The resulting context list is correctly V-ordered (or I-ordered when `index1=I`) regardless of what `recombinend` did to the physical tree layout.

---

### The actual subtle risk

There is a real risk, but it is downstream of the merging arithmetic, not of the ordering conflict.

After REARRANGE, siblings have I-positions and V-positions that are no longer correlated. The diagonal-sum sort will pair siblings that may be *non-adjacent* in both V and I. `takeovernephewsnd` calls `eatbrossubtreend` for small merges, which calls:

```c
// recombine.c:213-215
makeroomonleftnd (me, &offset, &bro->cdsp, &grasp);
fixdspsofbroschildren (me, bro);
```

`makeroomonleftnd` (`makeroom.c:13-49`) iterates over **both** dimensions and calls `expandcrumleftward` per dimension whenever the incoming origin is to the left of the current grasp:

```c
// makeroom.c:25-43
for (i = 0; i < widsize(father->cenftype); ++i) {
    if (tumblercmp (&origin->dsas[i], &grasp->dsas[i]) == LESS) {
        tumblersub (&grasp->dsas[i], &origin->dsas[i], &base);
        tumblersub (&origin->dsas[i], &offset->dsas[i], &newdsp.dsas[i]);
        expandcrumleftward ((typecorecrum*)father, &newdsp.dsas[i], &base, i);
        prologuend ((typecorecrum*)father, offset, grasp, (typedsp*)NULL);
    }
}
```

`expandcrumleftward` (`makeroom.c:52-74`) shifts `me`'s `cdsp` and `cwid`, and then bumps ALL of `me`'s existing children's `cdsp.dsas[index]` by `base`:

```c
movetumbler (newdsp, &crumptr->cdsp.dsas[index]);
tumbleradd(base, &crumptr->cwid.dsas[index], &crumptr->cwid.dsas[index]);
for (; ptr; ptr = findrightbro(ptr)) {
    tumbleradd(base, &ptr->cdsp.dsas[index], &ptr->cdsp.dsas[index]);
```

After REARRANGE, two siblings chosen by the diagonal-sum heuristic may be V-adjacent but not I-adjacent, or I-adjacent but not V-adjacent, or non-adjacent in both. If they are V-adjacent but not I-adjacent, `expandcrumleftward` correctly leaves the I-dimension alone (the `if (tumblercmp... LESS)` check for dimension I would not fire if `me` already covers `bro` in I). But if REARRANGE has produced a state where `bro`'s I-displacement lands outside `me`'s I-coverage, `expandcrumleftward` will fire for dimension I, shifting all of `me`'s existing children's I-positions by `base` — even though those children's V-positions already place them in known, correct I-positions from the original insertion.

This would silently corrupt I-displacements without affecting V-displacements. The immediate effect on `incontextlistnd` (called with `index1=V`) would be **none** — the V-addresses remain correct and the sort works. But the corruption would surface on the next I-address query (e.g., a follow-link or V-to-I mapping via `orglinks.c`).

---

### Summary

| Concern | Verdict | Evidence |
|---|---|---|
| Does diagonal-sum pairing reorder siblings physically? | No | It selects pairs; merges remove or subsume one sibling, leaving others in original physical positions | `recombine.c:120-131` |
| Does `findcbcinarea2d` rely on V-ordered siblings? | No | Full linear scan, no early stop | `retrie.c:252-265` |
| Does `incontextlistnd` require V-ordered input? | No | Self-contained insertion sort on absolute `totaloffset` | `context.c:75-111` |
| Is there a real risk? | Yes — I-displacement corruption | `expandcrumleftward` bumps all children's `cdsp[I]` when merging non-I-adjacent siblings selected by the post-REARRANGE diagonal-sum heuristic | `makeroom.c:52-74`, `recombine.c:296-300` |

The ordering conflict as literally stated does not exist: `incontextlistnd` is an insertion sort and needs no ordered input. The real vulnerability is in the displacement arithmetic when `recombinend`'s meaningless-after-REARRANGE diagonal-sum selects non-adjacent sibling pairs — a mistake in geometry, not in sort direction.

---

## Question 16 [gregory]

> After a sequence INSERT "ABC" then DELETE "B" then INSERT "XY" at the gap, the new "XY" has higher I-addresses than "C" but sits between "A" and "C" in V-space — does `compare_versions` (SHOWRELATIONOF2VERSIONS) correctly identify the shared "A" and "C" spans despite the I-address gap created by the interleaved allocation?

### Gregory's Answer

## KB Synthesis

## Answer

Yes, `compare_versions` correctly identifies the shared "A" and "C" spans. The I-address gap caused by the interleaved allocation is irrelevant to the comparison mechanism, which operates on I-address identity, not I-address ordering.

---

### Step 1: I-Address Allocation Trace

| Operation | Content | I-addresses | POOM V-mapping |
|-----------|---------|-------------|-----------------|
| INSERT "ABC" | A, B, C | I.1, I.2, I.3 | V.1.1→I.1, V.1.2→I.2, V.1.3→I.3 |
| DELETE "B" at V.1.2 | — | (I.2 remains in granfilade, V-mapping freed) | V.1.1→I.1, V.1.2→I.3 (C shifted) |
| INSERT "XY" at V.1.2 | X, Y | I.4, I.5 | V.1.1→I.1, V.1.2→I.4, V.1.3→I.5, V.1.4→I.3 |

**Why I.4, I.5 — not I.2?** DELETE is a POOM-only operation; the granfilade retains I.1, I.2, and I.3 [FC-GRANF-ON-DELETE], [ST-DELETE (Finding 0064)]. The next INSERT calls `findpreviousisagr`, which finds I.3 as the highest granfilade entry, then increments to I.4 [INV-NO-IADDR-REUSE], [INV-MONOTONIC]. Deleted I-addresses are never reused regardless of V-space gaps.

**Why three separate POOM crums (not merged)?** The `isanextensionnd` check requires both V-space contiguity (`new.origin == existing.reach` in V-space) and I-address contiguity (`new.I-origin == existing.I-reach`). When XY (I.4..I.5) is inserted at V.1.2:
- Against A's crum: A's I-reach = I.2, XY's I-origin = I.4 → **not** an extension [ST-INSERT (Finding 0062)]
- Against C's crum: C is now at V.1.4, not V-adjacent to the insertion point V.1.2 → **not** an extension

Result: three crums in POOM, each an independent V→I mapping.

---

### Step 2: What `vspanset2ispanset` Returns

The POOM retrieval via `incontextlistnd` sorts contexts by V-address [INV-RETRIEVAL-V-SORTED], yielding three I-spans in V-order:

| V-address (sorted) | I-span returned |
|--------------------|----------------|
| V.1.1 (A) | `{I.1, width=0.1}` |
| V.1.2–1.3 (XY) | `{I.4, width=0.2}` |
| V.1.4 (C) | `{I.3, width=0.1}` |

Note the I-spans are **non-monotonic in I-space** (I.1, then I.4..I.5, then I.3), but that is immaterial to the comparison.

---

### Step 3: compare_versions I-Span Intersection

`compare_versions` (SHOWRELATIONOF2VERSIONS) converts both documents' V-spans to I-spans, then intersects them pairwise. It is purely I-address identity comparison — V-address proximity and I-address ordering play no role [SS-COMPARE-VERSIONS].

Comparing the edited document against the original "ABC" document (whose I-span is the contiguous `{I.1, width=0.3}` covering A, B, C):

| Edited I-span | Original I-span | Intersection | Interpretation |
|--------------|----------------|--------------|---------------|
| `{I.1, 0.1}` | `{I.1, 0.3}` | `{I.1, 0.1}` ✓ | **A shared** |
| `{I.4, 0.2}` | `{I.1, 0.3}` | `∅` | XY not shared (fresh addresses) |
| `{I.3, 0.1}` | `{I.1, 0.3}` | `{I.3, 0.1}` ✓ | **C shared** |

The output is two correspondence pairs — identical to what Finding 0007 describes as "split-identity" behavior [ST-INSERT (Finding 0007)]:

```
[{edited: V.1.1 for 0.1, original: V.1.1 for 0.1},   // "A"
 {edited: V.1.4 for 0.1, original: V.1.3 for 0.1}]   // "C" (V-shifted in edited)
```

---

### Why the "Gap" Doesn't Matter

Three invariants combine to guarantee correctness:

1. **I-address immutability** [INV-IADDR-IMMUTABILITY]: A retains I.1 and C retains I.3 regardless of what DELETE and subsequent INSERT do. No operation reassigns these addresses.

2. **No I-address reuse** [INV-NO-IADDR-REUSE]: I.2 (deleted B) is never recycled. XY receives I.4..I.5 above the previous maximum, so there is no collision or ambiguity.

3. **compare_versions is I-address intersection** [SS-COMPARE-VERSIONS]: The nested loop in `correspond.c` intersects I-span ranges. The range `[I.1, I.1+0.1]` intersects `[I.1, I.1+0.3]` regardless of whether I.2 is occupied in V-space. The range `[I.3, I.3+0.1]` intersects `[I.1, I.1+0.3]` regardless of I.4 and I.5 sitting numerically between them.

The scenario is structurally identical to the mid-span insert case documented in [ST-INSERT (Finding 0030)]: the V-to-I mapping for A and C is "the same as before" — only their V-addresses differ — and `compare_versions` reports them correctly. The interleaved DELETE and INSERT merely produce a more fragmented I-span set from the edited document's POOM, which the intersection loop handles without special-casing.

## Code Exploration

I now have a complete trace of the full execution path. Here is the full analysis:

---

## Does `compare_versions` Correctly Identify Shared "A" and "C" Despite the I-Address Gap?

**Yes.** The algorithm correctly identifies both shared spans. Here is the precise trace through the source code.

---

### Setup: What the Allocation Sequence Produces

After INSERT "ABC" → DELETE "B" → INSERT "XY" at the gap, assign concrete permascroll addresses:

- INSERT "ABC": one contiguous permascroll block. A = perm₁+0, B = perm₁+1, C = perm₁+2 (width=1 each).
- DELETE "B": `deletend` (edit.c:31) is called on the POOM.
- INSERT "XY": a fresh permascroll block. X = perm₂+0, Y = perm₂+1, where perm₂ > perm₁+2 (confirming the premise: XY has higher I-addresses than C).

**After all operations**, V2's POOM has three separate leaf crums:

| Char | V-address | I-address |
|------|-----------|-----------|
| A    | V=1.1     | perm₁+0   |
| X    | V=1.2     | perm₂+0   |
| Y    | V=1.3     | perm₂+1   |
| C    | V=1.4     | perm₁+2   |

V1's POOM (the "ABC" version) still holds A, B, C as a single crum: V=[1.1, w=3], I=[perm₁, w=3].

---

### Step 1: V→I Conversion via `specset2ispanset`

`doshowrelationof2versions` [do1.c:443-448]:
```c
specset2ispanset(taskptr, version1, &version1ispans, READBERT)
specset2ispanset(taskptr, version2, &version2ispans, READBERT)
intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
```

`specset2ispanset` [do2.c:14] calls `vspanset2ispanset` → `permute` [orglinks.c:404] → `span2spanset` [orglinks.c:425] → `retrieverestricted` [retrie.c:56] → `findcbcinarea2d` [retrie.c:229].

`findcbcinarea2d` recursively descends the enfilade tree [retrie.c:252–265]:
```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, ...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson ((typecuc*)crumptr), ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);  // sorted by V-order
    }
}
```

Each leaf crum produces **one context**, which `span2spanset` then converts to one I-span via `context2span` [context.c:176]. Because the three leaf crums (A, XY, C) are distinct, the output is **three separate I-spans**:

- **V1 I-spans**: `[perm₁, w=3]` (A+B+C as one original crum)
- **V2 I-spans**: `[perm₁+0, w=1]` (A) · `[perm₂, w=2]` (XY) · `[perm₁+2, w=1]` (C)

The crums are inserted in V-order via `incontextlistnd` [context.c:75], so C's I-span `[perm₁+2, w=1]` appears third in the list even though its I-address (`perm₁+2`) is lower than XY's (`perm₂`). This ordering mismatch is irrelevant to correctness because `intersectspansets` is order-independent.

---

### Step 2: I-Span Intersection via `intersectspansets`

`intersectspansets` [correspond.c:145] does an **O(n×m) pairwise loop**, calling `comparespans` → `spanintersection` [correspond.c:210] for every pair:

```c
for (; set1; set1 = set1->next)
    for (p = set2; p; p = p->next)
        if (comparespans (taskptr, set1, p, set3, spantype))
            set3 = &(*set3)->next;
```

`spanintersection` [correspond.c:210] uses two early-exit guards [lines 217–221]:
```c
tumbleradd (&bptr->stream, &bptr->width, &bend);
if (tumblercmp (&aptr->stream, &bend) >= EQUAL)  return (FALSE);
tumbleradd (&aptr->stream, &aptr->width, &aend);
if (tumblercmp (&bptr->stream, &aend) >= EQUAL)  return (FALSE);
```

Now trace the three pairings with `a = [perm₁, w=3]` (V1):

**Pairing 1**: `[perm₁, w=3]` ∩ `[perm₁+0, w=1]` — finding A
- aend = perm₁+3, bend = perm₁+1
- `perm₁ < perm₁+1` → first guard passes
- `perm₁+0 < perm₁+3` → second guard passes
- `tumblercmp(perm₁, perm₁+0) == EQUAL` → case EQUAL; `tumblercmp(aend=perm₁+3, bend=perm₁+1) == GREATER` → `cptr->width = bptr->width = 1`
- **Result: `[perm₁+0, w=1]` ✓ (A identified)**

**Pairing 2**: `[perm₁, w=3]` ∩ `[perm₂, w=2]` — testing XY
- aend = perm₁+3, bend = perm₂+2
- `perm₁ < perm₂+2` → first guard passes
- `perm₂ >= perm₁+3 = aend` because perm₂ > perm₁+2 (given by the premise: XY allocated after C)
- Second guard: `tumblercmp(bptr->stream=perm₂, aend=perm₁+3) >= EQUAL` → **`return FALSE`** ✓
- **Result: empty (XY correctly excluded)**

**Pairing 3**: `[perm₁, w=3]` ∩ `[perm₁+2, w=1]` — finding C
- aend = perm₁+3, bend = perm₁+3
- `perm₁ < perm₁+3` → first guard passes
- `perm₁+2 < perm₁+3` → second guard passes
- `tumblercmp(perm₁, perm₁+2) == LESS` → case LESS; `tumblercmp(aend=perm₁+3, bend=perm₁+3) == EQUAL` → `cptr->width = bptr->width = 1`
- **Result: `[perm₁+2, w=1]` ✓ (C identified despite the gap at perm₁+1)**

The I-address "gap" at perm₁+1 (B's former address) is irrelevant because `spanintersection` asks only whether the ranges **overlap**, not whether they are contiguous. C's address perm₁+2 is within V1's range `[perm₁, perm₁+3)`.

---

### Step 3: I→V Back-Mapping via `ispansetandspecsets2spanpairset`

`ispansetandspecsets2spanpairset` [do2.c:185] calls `restrictspecsetsaccordingtoispans` [correspond.c:18] → `restrictvspecsetovercommonispans` [correspond.c:52] → `ispan2vspanset` → `permute` [orglinks.c:389] with I as the restriction axis and V as the target.

For the common I-span `[perm₁+2, w=1]` (C), `context2span` [context.c:176] handles the partial-overlap case. V1's POOM has a single crum `[V=1.1, w=3, I=perm₁, w=3]`. The restriction span is `I=[perm₁+2, w=1]`:

```c
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement (&grasp.dsas[idx2], 0,
        (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
```

`tumblerintdiff` [tumble.c:591] returns `c.mantissa[0]` — the integer delta at the highest significant position, valid for within-block same-level tumblers. With idx1=I, idx2=V:
- `grasp.dsas[I] = perm₁`, `lowerbound = perm₁+2`, diff = 2
- `grasp.dsas[V] = 1.1 + 2 = 1.3`
- `reach.dsas[I] = perm₁+3 = upperbound` → no adjustment; `reach.dsas[V] = 1.4`
- **Returns V=[1.3, w=1] for C in V1** ✓

For V2's POOM (C is a separate crum: `[V=1.4, w=1, I=perm₁+2, w=1]`):
- `crumqualifies2d` finds the crum (I=perm₁+2 within restriction)
- No partial clipping needed; returns **V=[1.4, w=1] for C in V2** ✓

---

### Final Span Pairs Produced

| Content | V-span in V1   | V-span in V2   | I-address    |
|---------|----------------|----------------|--------------|
| A       | [1.1, w=1]     | [1.1, w=1]     | perm₁+0      |
| C       | [1.3, w=1]     | [1.4, w=1]     | perm₁+2      |

"C" is correctly reported at V=1.3 in V1 and V=1.4 in V2 — reflecting the fact that the XY insertion shifted C rightward by two positions in V2.

---

### Why the Algorithm Is Correct

The I-address gap does **not** confuse the algorithm for three independent structural reasons:

1. **POOM crums are independent** [edit.c:58–63]: `deletend` splits the ABC crum before removing B. After the split, C holds its original I-address (perm₁+2) in a separate crum — there is no "collapsed" or merged representation that would hide the gap.

2. **`intersectspansets` uses range overlap, not contiguity** [correspond.c:177–182]: The O(n×m) pairwise loop with `spanintersection` asks whether two arbitrary tumbler ranges overlap. C's range `[perm₁+2, perm₁+3)` overlaps with V1's range `[perm₁, perm₁+3)` regardless of what is at perm₁+1.

3. **`context2span` correctly computes partial-crum V-offsets** [context.c:191–203]: When a common I-span corresponds to only part of a crum, `context2span` uses `tumblerintdiff` to compute the proportional V-offset. This correctly maps perm₁+2 → V=1.3 within V1's ABC crum.

The one unstated assumption the algorithm makes — that the 1:1 ratio between V-offsets and I-offsets within a single crum holds — is satisfied by the POOM invariant: a crum always maps a V-span of width *w* to an I-span of the same width *w*.

---

## Question 17 [gregory]

> When `vspanset2sporglset` converts a contiguous V-span to sporgls, and the V-span covers content from multiple temporal insertions (so I-addresses are non-contiguous), does it split at every I-address discontinuity, and is the resulting sporgl set ordered by V-position or by I-address?

### Gregory's Answer

## KB Synthesis

## Splitting Behavior

Yes, `vspanset2sporglset` splits at every I-address discontinuity. The mechanism is explicit in [ST-LINK-CREATE] / Finding 0037:

> The critical mechanism is the inner loop in `vspanset2sporglset` (sporgl.c:49-58), which iterates over every I-span returned by `vspanset2ispanset` and creates a separate sporgl for each.

The conversion chain is:

```
V-span → vspanset2ispanset → permute → span2spanset → retrieverestricted
       → one I-span per contiguous I-address region
       → one sporgl per I-span
```

`permute` walks the POOM, collecting each bottom crum that falls within the query V-range. Each crum covers a contiguous V-to-I mapping; gaps between crums (from different insertions, different source documents, or interleaved allocations) produce separate I-spans and thus separate sporgls. There is no consolidation step.

If a single V-span covers content from N distinct temporal insertions producing N non-contiguous I-address regions, the result is N sporgls. [SS-SPORGL] / Finding 0013 confirms this: "produces the multi-sporgl endset."

## Ordering: V-position, Not I-address

The resulting sporgl set is ordered by **V-position**. This follows from [INV-RETRIEVAL-V-SORTED] / Finding 0078:

> `incontextlistnd()` performs explicit insertion-sort by V-address as contexts are discovered during B-tree traversal... the result list is sorted by left boundary in the queried dimension.

For a V→I query (which is what `vspanset2ispanset` performs via `permute`), the queried dimension is V. `findcbcinarea2d` traverses the POOM B-tree and accumulates contexts via `incontextlistnd`, which maintains ascending V-position order regardless of tree structure or discovery sequence.

Consequently, sporgls appear in V-stream sequential order. The I-addresses of successive sporgls may be entirely unordered—they reflect insertion chronology, not document position.

## Practical Implication

For a document where:
- Content "ABCD" was inserted first (I-addresses I.1–I.4)
- A link was created (consuming I-address space)
- Content "EFGH" was appended (I-addresses I.2.1–I.2.4, per [INT-LINK-INSERT] / Finding 0063)

A V-span covering all eight characters produces two sporgls ordered by V-position:
- Sporgl 1: origin=I.1, width=4 (for "ABCD" at lower V-addresses)
- Sporgl 2: origin=I.2.1, width=4 (for "EFGH" at higher V-addresses)

The I-address ordering happens to match V-position here, but after a rearrange or pivot the sporgls would still be V-sorted while I-addresses could appear in reverse or interleaved order. [INV-RETRIEVAL-TREE-INDEPENDENCE] / Finding 0078 confirms this V-sort holds regardless of tree internal structure.

## Code Exploration

Now I have everything I need. Here is the full analysis.

---

## `vspanset2sporglset`: Splitting and Ordering

### Call Chain

```
vspanset2sporglset          sporgl.c:35
  └─ vspanset2ispanset       orglinks.c:397
       └─ permute            orglinks.c:404  (restrictionindex=V, targindex=I)
            └─ span2spanset  orglinks.c:425
                 └─ retrieverestricted  retrie.c:56
                      └─ retrieveinarea retrie.c:87
                           └─ findcbcinarea2d  retrie.c:229
                                └─ incontextlistnd  context.c:75  ← ordering here
```

---

### 1. Does it split at every I-address discontinuity?

**Yes, unconditionally.** Here is how:

Each call to `doinsert` flows through `insertpm` [`orglinks.c:75`], which calls `insertnd` for each sporgl, creating a fresh POOM leaf crum per temporal insertion. Two insertions at non-contiguous I-addresses are always stored as distinct crums in the POOM tree.

`findcbcinarea2d` [`retrie.c:229`] walks sibling crums and at each qualifying leaf (height == 0) creates a separate context object:

```c
// retrie.c:261-264
} else {
    context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
    incontextlistnd (headptr, context, index1);
}
```

There is no merging step here—each leaf crum yields exactly one context, regardless of whether its I-range is adjacent to the previous one.

Back in `span2spanset` [`orglinks.c:439`], each context is converted to an ispan via `context2span` and appended to the ispanset via `onitemlist`:

```c
// orglinks.c:439-444
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`onitemlist` [`orglinks.c:518`] is a pure append-to-tail with **no adjacent-span merging**:

```c
// orglinks.c:521-534
} else {
    for (temp = *itemsetptr;
         temp && ((typeitemheader *)temp)->next;
         temp = (typeitem *)((typeitemheader *)temp)->next)
        ;
    ((typeitemheader *)temp)->next = (typeitemheader *)newitem;
}
```

Compare this with `putvspaninlist` [`orglinks.c:329`], which *does* merge adjacent/overlapping V-spans. `onitemlist` has no equivalent logic—it just threads items onto the end of the list.

Therefore: a V-span touching N distinct temporal insertions produces exactly **N ispans** and exactly **N sporgls**. Every I-address discontinuity is a split point.

---

### 2. Is the resulting sporgl set ordered by V-position or by I-address?

**Ordered by V-position.**

The ordering is imposed at `retrie.c:263` — `findcbcinarea2d` calls `incontextlistnd(headptr, context, index1)`, where `index1` is the restriction dimension passed in from `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d`. In this call chain, `index1 = V` [`wisp.h:21`: `#define V 1`].

`incontextlistnd` [`context.c:75`] is explicitly documented as an insertion sort on `index`:

```c
// context.c:74-75
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
```

The sort key is `grasp.dsas[index]` = `c->totaloffset.dsas[V]` — the absolute V-start address of the leaf crum. The three insertion-point cases (beginning, middle, end) all use `whereoncontext(..., &grasp.dsas[index], index)` to find the correct ascending position:

```c
// context.c:89-103
if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
    // grasp < clist.start → insert at beginning
    c->nextcontext = clist;
    *clistptr = c;
    return(0);
} else {
    for (; nextc = clist->nextcontext; clist = nextc) {
        if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
            && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
            // clist.start ≤ grasp < nextc.start → insert between
            c->nextcontext = nextc;
            clist->nextcontext = c;
```

(Constants from `common.h:86-89`: `TOMYLEFT=-2`, `ONMYLEFTBORDER=-1`, `THRUME=0`, `ONMYRIGHTBORDER=1`, `TOMYRIGHT=2`.)

Since `onitemlist` appends in list-traversal order, the ispanset is assembled in the same V-ascending order as the sorted context list. Finally, `vspanset2sporglset` [`sporgl.c:49`] links sporgls as it iterates the ispanset:

```c
// sporgl.c:49-58
for (; ispanset; ispanset = ispanset->next) {
    sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
    ...
    movetumbler(&ispanset->stream, &sporglset->sporglorigin);
    movetumbler(&ispanset->width,  &sporglset->sporglwidth);
    *sporglsetptr = (typesporglset)sporglset;
    sporglsetptr = (typesporglset *)&sporglset->next;
}
```

The sporgls are linked in ispanset order = context-list order = **ascending V-position order**.

The I-addresses of the sporgls are therefore **not sorted**. They reflect whatever non-contiguous I-addresses the underlying temporal insertions used, in the order those insertions appear in V-space.

---

### Summary

| Question | Answer | Key citation |
|---|---|---|
| Does it split at every I-address discontinuity? | Yes — one sporgl per POOM leaf crum, no ispan merging | `onitemlist` append-only: `orglinks.c:518`; `findcbcinarea2d` per-leaf dispatch: `retrie.c:261` |
| Sporgl set ordered by V or I? | By **V-position** (ascending) | `incontextlistnd(..., index1)` where `index1=V`: `retrie.c:263`, `context.c:74` |

---

## Question 18 [gregory]

> For the spanfilade's DOCISPAN entries, each INSERT creates one entry per contiguous I-span — when a document's V-order completely disagrees with I-order (after many rearrangements), does `findlinksfromtothreesp` still correctly discover links by searching the I-dimension, independent of the document's current V-ordering?

### Gregory's Answer

## KB Synthesis

Yes — `findlinksfromtothreesp` discovers links correctly regardless of how far a document's V-order has drifted from I-order. The independence holds structurally, not by coincidence.

## Why V/I Disagreement Doesn't Matter

**The search operates in I-space throughout.** The call chain is:

1. Query V-spec → converted to I-spans via the document's current POOM
2. I-spans searched in the spanfilade for matching link endsets
3. Matching links returned

Steps 2 and 3 are purely I-dimension operations. The spanfilade is indexed by I-address — period. V-ordering is irrelevant to what the spanfilade contains or how it is queried. [SS-SPANF-OPERATIONS, SS-FIND-LINKS]

## REARRANGE Leaves the Spanfilade Untouched

REARRANGE (`rearrangend()`) applies `tumbleradd` only to `ptr->cdsp.dsas[V]` — the V-dimension displacement component. I-addresses stored in POOM crums are never touched. [ST-REARRANGE, Finding 0056]

Because REARRANGE modifies only the granf (POOM layer) and the spanfilade is write-only with no delete operation, the frame condition holds absolutely: `∀ op ∈ {REARRANGE} : spanf_after(op) = spanf_before(op)`. [INV-SPANF-WRITE-ONLY, FC-CONTENT-SPANF-ISOLATION, Finding 0061]

This means DOCISPAN entries and link endset entries created at INSERT/CREATELINK time remain exactly as recorded, regardless of any subsequent rearrangements.

## INV-REARRANGE-IDENTITY Closes the Loop

The invariant `I-addresses(doc_after_rearrange) = I-addresses(doc_before_rearrange)` as a multiset confirms the same I-addresses exist in the document — just mapped to different V-positions. [INV-REARRANGE-IDENTITY]

So when step 1 converts V-positions to I-spans via the current (post-rearrangement) POOM, it produces the same I-addresses that were indexed in the spanfilade at creation time. The match succeeds.

## DOCISPAN Granularity Is an Orthogonal Concern

DOCISPAN entries are created at per-I-span granularity: one `insertnd` call per contiguous I-address range, not per byte. [SS-DOCISPAN, Finding 0047] Rearrangement can make a contiguous I-range appear non-contiguous in V-space — but this affects only the *V-space presentation*, not the spanfilade entry. The DOCISPAN still records the contiguous I-span, and searching by those I-addresses still works.

## The Orgl-Filter Caveat (Orthogonal)

There is a separate known bug: the orgl-range parameter to `findlinksfromtothreesp` is effectively ignored via a `TRUE||` guard in `sporglset2linkset`, making all searches global in the orgl dimension. [EC-FIND-LINKS-GLOBAL, Finding 0069] This is orthogonal to the V/I ordering question — it affects *which documents* are searched, not whether the I-dimension search itself is correct.

## Summary

The design is sound for this scenario because the two concerns are architecturally separated:

| Layer | Mutable by REARRANGE? | Role in link search |
|-------|----------------------|---------------------|
| POOM (granf) | Yes — V-positions shift | V→I address translation at query time |
| Spanfilade | No — write-only | I-address → link lookup |
| I-addresses themselves | Never | Stable keys throughout |

A V-order that completely disagrees with I-order simply means the POOM maps V-positions to I-addresses in a non-monotone way — the link search converts through that mapping correctly, then searches the spanfilade using the resulting I-addresses, which remain exactly what was indexed. [SS-DUAL-ENFILADE, INV-REARRANGE-IDENTITY, INV-SPANF-WRITE-ONLY]

## Code Exploration

I now have the complete picture. Here is the full analysis.

---

## Answer

**Yes — `findlinksfromtothreesp` correctly discovers links by searching the I-dimension, independent of any V-ordering.** The spanfilade has no V-dimension at all. The design achieves this through three structural properties: (1) the spanfilade is keyed purely by I-coordinates, (2) V→I translation via the orgl is V-order-agnostic, and (3) the struct memory layouts are deliberately aliased so I-coordinates are passed through the type system cleanly. What follows is the full code trace.

---

### 1. How the Spanfilade Is Written: I-Coordinates Only

When a link is created, `docreatelink` [do1.c:195-221] calls:

```c
insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`insertendsetsinspanf` [do2.c:116-128] fans this out to three calls:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // 1
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)     // 2
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN) // 3
```

Inside `insertspanf` [spanf1.c:15-54], for each sporgl in the set:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // [spanf1.c:22]
// ...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);             // [spanf1.c:49]
movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);              // [spanf1.c:50]
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE); // [spanf1.c:51]
```

- **SPANRANGE** ← I-coordinates (`lstream`, `lwidth`) of the endpoint content.
- **ORGLRANGE** ← `linkisaptr` prefixed with the endpoint type (`LINKFROMSPAN`=1, `LINKTOSPAN`=2, `LINKTHREESPAN`=3).

The `lstream`/`lwidth` values come from `sporglorigin`/`sporglwidth` fields of the sporgl items [spanf1.c:27-28, 31-32], which are themselves I-coordinates. **No V-dimension is ever stored in the spanfilade.**

---

### 2. How `findlinksfromtothreesp` Reads: V→I Then I-Search

`findlinksfromtothreesp` [spanf1.c:56-103] receives v-specsets and converts them to I-span sporglsets:

```c
specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED)   // [spanf1.c:71]
specset2sporglset(taskptr, tovspecset,   &tosporglset,   NOBERTREQUIRED)   // [spanf1.c:73]
specset2sporglset(taskptr, threevspecset,&threesporglset,NOBERTREQUIRED)   // [spanf1.c:75]
```

Then for each endpoint set it calls:

```c
sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN) // [spanf1.c:77]
```

#### 2a. V→I Translation via the Orgl

`specset2sporglset` [sporgl.c:14-33] handles two cases:

- **ISPANID** items: passed through as-is (already I-coordinates) [sporgl.c:20-22]
- **VSPECID** items: calls `vspanset2sporglset(taskptr, &docisa, vspanset, ...)` [sporgl.c:25]

`vspanset2sporglset` [sporgl.c:35-65] does:

```c
findorgl(taskptr, granf, docisa, &orgl, type)          // [sporgl.c:44] — get permutation matrix
vspanset2ispanset(taskptr, orgl, vspanset, &ispanset)  // [sporgl.c:48] — V→I via orgl
```

`vspanset2ispanset` [orglinks.c:397] calls:

```c
permute(taskptr, orgl, vspanptr, V, ispansetptr, I)    // [orglinks.c:401]
```

`permute` [orglinks.c:404-422] calls `span2spanset` for each input span, which calls:

```c
retrieverestricted((typecuc*)orgl, restrictionspanset, V, (typespan*)NULL, I, (typeisa*)NULL)  // [orglinks.c:435]
```

This queries the **orgl** (the permutation matrix enfilade for this document), restricted to a V-span, and returns the matching I-extents. This is exactly the V→I mapping. Crucially, the orgl is a 2D enfilade of (V, I) pairs — it faithfully records the current permutation after every `dorearrange` call [do1.c:34-43, orglinks.c:137-142]. No matter how scrambled V-order is relative to I-order, the orgl's tree structure encodes the current bijection correctly, and this retrieval extracts it.

The resulting `ispanset` items are then packed into sporgl structs [sporgl.c:50-57]:

```c
movetumbler(&ispanset->stream, &sporglset->sporglorigin)  // I-start
movetumbler(&ispanset->width,  &sporglset->sporglwidth)   // I-width
movetumbler(docisa,            &sporglset->sporgladdress)
```

#### 2b. Spanfilade Search in I-Space

`sporglset2linkset` [sporgl.c:222-237] has a hardcoded override:

```c
if (TRUE||!homeset) {       // [sporgl.c:227] — always true, orglrange param ignored
    nullhomeset.width.mantissa[0] = 100;
    homeset = &nullhomeset;
}
sporglset2linksetinrange(taskptr, spanfptr, sporglset, linksetptr, homeset, spantype)
```

The `TRUE||!homeset` condition unconditionally overrides whatever `orglrange` was passed from `findlinksfromtothreesp`. The nullhomeset has stream=0, width=100 — a wide ORGLRANGE filter that spans all valid link addresses.

`sporglset2linksetinrange` [sporgl.c:239-269]:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);  // [sporgl.c:257] — e.g. 1.0 for LINKFROMSPAN
prefixtumbler(&orglrange->width,  0,        &range.width);   // [sporgl.c:258] — 0.100
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, NULL); // [sporgl.c:259]
```

The ORGLRANGE restriction filters by spantype prefix — so only FROM/TO/THREE entries of the correct kind are returned — but with a wide enough range to cover all document addresses.

#### 2c. The Struct Aliasing Is Intentional

`retrieverestricted` [retrie.c:56-85] accesses its `span1ptr` argument as:

```c
movetumbler(&span1ptr->stream, &span1start);               // [retrie.c:64]
tumbleradd(&span1start, &span1ptr->width, &span1end);      // [retrie.c:65]
```

The argument is `(typespan*)sporglset`. The struct layouts in `xanadu.h` are:

```c
// typespan [xanadu.h:65-70]:
struct { struct *next; typeitemid itemid; tumbler stream; tumbler width; }

// typesporgl [xanadu.h:115-121]:
struct { struct *next; typeitemid itemid; tumbler sporglorigin; tumbler sporglwidth; typeisa sporgladdress; }
```

`stream` and `sporglorigin` sit at the same byte offset. `width` and `sporglwidth` sit at the same byte offset. The type-cast `(typespan*)sporglset` is therefore not a random punning — it is the intended mechanism by which `sporglorigin`/`sporglwidth` (I-coordinates) are presented to `retrieverestricted` as `stream`/`width`.

`retrieveinarea` → `findcbcinarea2d` [retrie.c:229-268] then walks the spanfilade tree, calling `crumqualifies2d` [retrie.c:270-305] to test each node against:
- `(span1start, span1end)` in `SPANRANGE` — the I-coordinate query
- `(span2start, span2end)` in `ORGLRANGE` — the spantype+docaddr range

When a bottom crum qualifies, its ORGLRANGE value (which holds `linkisaptr` prefixed with spantype, as stored during `insertspanf`) is extracted via `beheadtumbler` [sporgl.c:264] to strip the spantype prefix, yielding the raw link ISA. This ISA is added to the result linkset.

---

### 3. The Final Intersection

Back in `findlinksfromtothreesp` [spanf1.c:100]:

```c
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr)
```

`intersectlinksets` [spanf2.c:46-120] returns link ISAs that appear in all non-null sets. The intersection is done in tumbler-address space with no reference to V-ordering.

---

### Summary

| Path | Where V→I Happens | Where I Is Used |
|------|-------------------|-----------------|
| Link creation | `specset2sporglset` converts V-specs to I-sporgls | `insertspanf` stores I in SPANRANGE |
| Link discovery | `specset2sporglset` → `vspanset2ispanset` → `permute` via orgl | `sporglset2linksetinrange` queries SPANRANGE |

The spanfilade contains no V-coordinates whatsoever. After any number of `dorearrange` calls — even maximal reversal — the orgl permutation matrix correctly maps the current V-locations back to their stable I-addresses. The link lookup then operates entirely in I-space, which never changes for a given piece of content. `findlinksfromtothreesp` is therefore provably correct regardless of V-order.

One note: the `TRUE||!homeset` guard at [sporgl.c:227] silently drops the `orglrange` parameter. This is likely a known simplification ("trying to kluge" per the comment context at [sporgl.c:251]) — link lookup works but cannot be restricted to a particular document's address range. All link addresses globally matching the I-span and spantype are returned.

---

## Question 19 [gregory]

> Does the `isanextensionnd` coalescing optimization in `insertpm` check I-address contiguity only, or does it also verify that the new entry's V-position is adjacent to the existing entry's V-span — and if a COPY places I-address-contiguous content at a non-adjacent V-position, does it incorrectly coalesce?

### Gregory's Answer

## KB Synthesis

## `isanextensionnd`: Both Dimensions Required

`isanextensionnd` enforces contiguity in **both V-space and I-space simultaneously**, plus `homedoc` identity. Placing I-address-contiguous content at a non-adjacent V-position does **not** trigger incorrect coalescing — the V-adjacency check fails independently and a new crum is created.

---

### What `isanextensionnd` Actually Checks

[ST-INSERT] (Finding 0046) states explicitly:

> `isanextensionnd()` at `insertnd.c:293-301` checks two conditions: (1) the new mapping has the same `homedoc` (I-address origin document) as an existing crum, and (2) the new mapping starts exactly where the existing crum ends (**contiguous in both V and I dimensions**).

For a POOM bottom crum — which stores dual-space coordinates [SS-POOM-BOTTOM-CRUM] — extension requires:

```
new_content.V-origin == existing_crum.V-reach     (V-adjacency)
new_content.I-origin == existing_crum.I-reach     (I-adjacency)
new_content.homedoc  == existing_crum.homedoc     (provenance match)
```

All three conditions must hold. Failure of any one → `FALSE` → new crum created.

---

### The COPY-at-Non-Adjacent-V Case: No Incorrect Coalescing

Finding 0046 provides the exact scenario you describe as a concrete example:

```
Before: target POOM has crum [V 1.1..1.5 → i₁..i₅]

COPY same source at V=1.6 (contiguous in both dimensions):
  isanextensionnd() → TRUE
  Result: crum extended to [V 1.1..1.10 → i₁..i₁₀]

COPY same source at V=1.20 (V-position non-adjacent; I-addresses same i₁..i₅):
  isanextensionnd() → FALSE
  Result: new crum created [V 1.20..1.24 → i₁..i₅]
```

The second COPY has I-address content (`i₁..i₅`) that is identical to (and thus "contiguous with") the existing crum's I-span — but because `V-origin(1.20) ≠ V-reach(1.6)`, the V-adjacency check fails. A new, separate crum is created at V 1.20.

---

### Corroborating Evidence: I-adjacency Fails Independently Too

[ST-CRUM-BOUND] (Finding 0063) shows the symmetric case — V-adjacent but I-non-adjacent — also fails:

> CREATELINK breaks `isanextensionnd` coalescing for subsequent text INSERTs. After CREATELINK consumes I-address space, the next INSERT's text I-addresses are non-contiguous with the previous INSERT's text I-addresses. When `isanextensionnd` checks whether the new content's origin equals the existing crum's reach, the check fails.

Even if the INSERT targets the immediately next V-position, the I-address gap from the link orgl allocation means `I-origin ≠ I-reach` → new crum created (+2 cost instead of +0).

---

### Why Both Dimensions Are Required by Design

A POOM bottom crum is a 2D structure representing a **bijection between a V-span and an I-span** [SS-POOM-BOTTOM-CRUM]. Extension means appending to this bijection: the new content must be adjacent in V-space (so the V-span grows contiguously) AND adjacent in I-space (so the I-span grows contiguously). If either fails, the new content represents a **different** (V→I) relationship and cannot be merged into the existing crum without creating a false mapping.

Coalescing at only one dimension would corrupt the POOM's fundamental invariant [INV-POOM-BIJECTIVITY] — a single crum would then claim to map a contiguous V-span to a contiguous I-span when in reality the I-addresses (or V-positions) have a gap in the middle.

---

### Summary

| Scenario | V-adjacent | I-adjacent | homedoc match | `isanextensionnd` | Result |
|----------|-----------|-----------|---------------|-------------------|--------|
| Sequential typing | ✓ | ✓ | ✓ | TRUE | Extend crum (+0) |
| COPY at V=1.6 (contiguous) | ✓ | ✓ | ✓ | TRUE | Extend crum (+0) |
| COPY at V=1.20 (I-same, V-gap) | ✗ | ✓ | ✓ | **FALSE** | New crum created |
| INSERT after CREATELINK | ✓ | ✗ | ✓ | **FALSE** | New crum created |
| COPY different homedoc | ✓ | ✓ | ✗ | **FALSE** | New crum created |

No incorrect coalescing is possible — the check is a conjunction, and the V-dimension component fully prevents the spurious merge described in your question.

## Code Exploration

I now have all the evidence needed to give a definitive answer. Let me trace through the complete picture:

---

## Answer

### The Short Answer

`isanextensionnd` checks **both** I-address contiguity **and** V-position adjacency simultaneously, using a single 2D comparison. A COPY that places I-address-contiguous content at a non-adjacent V-position does **not** incorrectly coalesce.

---

### Full Trace

#### `isanextensionnd` — the coalescing gate

`backend/insertnd.c:301-309`:
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

Two guards:
1. **`homedoc` equality** [`insertnd.c:305`]: the source document of the new entry must match the source document of the existing crum. For a COPY, this is the source document's ISA tumbler, set by `unpacksporgl` [`sporgl.c:187`]: `movetumbler(&sporglptr->sporgladdress, &infoptr->homedoc)`.
2. **`lockeq` on `reach` vs. `origin`** [`insertnd.c:308`]: the ABSOLUTE END of the existing crum must equal the ABSOLUTE START of the new entry — in ALL dimensions.

#### `prologuend` computes both ends in both dimensions

`backend/retrie.c:334-339`:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

`reach.dsas[I]` = absolute I-end; `reach.dsas[V]` = absolute V-end.

#### `dspsize(POOM) = 2` — the critical constant

`backend/wisp.h:26,61`:
```c
#define DSPSIZEPM 2
#define dspsize(A) ((A)==GRAN?DSPSIZEGR:((A)==SPAN?DSPSIZESP:DSPSIZEPM))
```

For a POOM crum, `dspsize` returns **2** — meaning two tumblers, one for each dimension.

The dimension layout is also from `wisp.h:19-20`:
```c
#define I  0
#define V  1
```

So `dsas[0]` is I, `dsas[1]` is V.

#### `lockeq` iterates over ALL dimensions

`backend/wisp.c:261-267`:
```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize)
{
    while (loxize--)
           if (!tumblereq (lock1++, lock2++))
                    return(FALSE);
    return(TRUE);
}
```

With `loxize=2`, it compares:
- `reach.dsas[0]` (I-end of existing) vs. `originptr->dsas[0]` (I-start of new)
- `reach.dsas[1]` (V-end of existing) vs. `originptr->dsas[1]` (V-start of new)

Both must be **`tumblereq`** — equal — or it returns FALSE.

#### Call path for a COPY

`docopy` (`do1.c:45`) → `insertpm` (`orglinks.c:60`) → per sporgl, `insertnd(taskptr, orgl, &crumorigin, &crumwidth, &linfo, V)` (`orglinks.c:130`) → `doinsertnd` (`insertnd.c:196`) → `insertmorend` → `insertcbcnd` (`insertnd.c:231`) → `isanextensionnd` (`insertnd.c:250`).

Inside `insertpm` (`orglinks.c:105-117`), for each sporgl the origin is assembled:
```c
movetumbler (&lstream, &crumorigin.dsas[I]);   // I-start from source span
movetumbler (vsaptr,   &crumorigin.dsas[V]);   // V-position from caller
```

For a COPY, `vsaptr` is the **destination** V-address, which may be anywhere — including non-adjacent to any existing crum's V-end.

#### The COPY + non-adjacent V-position scenario

Suppose an existing POOM crum has:
- `reach.dsas[I]` = `X` (contiguous with what we're about to insert)
- `reach.dsas[V]` = `Y` (some V-end)

The incoming COPY has:
- `originptr->dsas[I]` = `X` (I-addresses ARE contiguous) ✓
- `originptr->dsas[V]` = `Z ≠ Y` (V-position is NOT adjacent) ✗

`lockeq(reach.dsas, originptr->dsas, 2)` on the second iteration (`dsas[V]`) calls `tumblereq(Y, Z)` → FALSE. `lockeq` returns FALSE immediately. `isanextensionnd` returns FALSE. No coalescing.

---

### Conclusion

The `isanextensionnd` coalescing optimization **checks both dimensions jointly** via `lockeq(..., dspsize(POOM)=2)` [`insertnd.c:308`]. It is not an I-only check. The V-adjacency requirement is implicit in the `loxize` parameter: since POOM has `DSPSIZEPM=2` [`wisp.h:26`], both `dsas[I]` and `dsas[V]` must match.

A COPY that places I-address-contiguous content at a non-adjacent V-position passes the first dimension check but fails the second, causing `lockeq` to return FALSE and preventing any coalescing. **There is no bug here** — the guard is correctly two-dimensional.

---

## Question 20 [gregory]

> When two documents share I-addresses via COPY but have different V-orderings of that content (e.g., doc1 has "AB" at V:1.1 and doc2 has the same content reversed via REARRANGE), does `find_links` with a V-span covering only "A" in doc2 correctly resolve to the same I-address as "A" in doc1, even though "A" occupies different V-positions in each document?

### Gregory's Answer

## KB Synthesis

Yes. `find_links` with a V-span covering "A" in the rearranged doc2 resolves to exactly the same I-address as "A" in doc1. Here is the chain of reasoning:

---

**Step 1: VCOPY gives doc2 the same I-addresses as doc1**

After `VCOPY(doc1 → doc2)`, both documents share permascroll I-addresses. If "A" is i_A and "B" is i_B in doc1, then doc2's POOM maps the same i_A and i_B to the corresponding V-positions at creation time [ST-VCOPY, INV-TRANSITIVE-IDENTITY].

---

**Step 2: REARRANGE changes V-positions but never touches I-addresses**

From [INV-REARRANGE-IDENTITY] (Findings 0016, 0056):

> The code modifies only `ptr->cdsp.dsas[index]` (the V-address displacement). The I-address, stored separately, is never touched.

After reversing "AB" to "BA" in doc2 via REARRANGE:
- V:1.1 → i_B ("B" now here)
- V:1.2 → i_A ("A" now here)

The POOM crums have their V-displacements updated; their I-address entries are unchanged. [ST-REARRANGE] confirms this: `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])` — only the V-dimension displacement changes.

---

**Step 3: find_links converts V-span to I-address via the POOM, then searches the spanf**

From [SS-FIND-LINKS] (Finding 0028):

> `find_links(search_specset)` discovers links by I-address intersection. The search specset is converted to I-addresses, and links are returned if any I-address overlaps with link endpoint I-addresses.

When you query `find_links` with a V-span covering "A" in doc2 (say V:1.2, width 0.1):

1. The call chain converts this V-span to I-addresses by traversing doc2's POOM.
2. Doc2's POOM correctly maps V:1.2 → i_A (because REARRANGE only changed V-displacements, not the I-address stored in the crum).
3. The spanf index is searched for i_A.
4. Any link whose endset contains i_A is returned — the same links discoverable from doc1's "A".

The V-to-I conversion is what makes this work: `specset2ispanset` → `permute` → `retrieverestricted` traverses the POOM tree mechanically, yielding whatever I-address is stored at the crum corresponding to V:1.2. Since REARRANGE only moved the V-displacement pointer, the I-address stored in that crum is still i_A.

---

**Step 4: The spanf index is V-order–agnostic**

From [SS-LINK-SPACE] (Finding 0028b):

> Links are stored in a separate address space (the spanf enfilade) indexed by I-address for efficient discovery. Document identity plays no role — a document that was not involved in link creation can discover the link if it shares content identity via I-address overlap.

The spanf stores the mapping `{i_A → link_id}`. It neither knows nor cares what V-position i_A occupies in any document. Once the V-to-I conversion yields i_A, the spanf search succeeds identically regardless of whether "A" was at V:1.1 (doc1) or V:1.2 (doc2 after rearrange).

---

**Why this must hold: the content identity model is position-independent**

From [INV-LINK-IDENTITY-DISCOVERY] (Finding 0039):

> `forall v1 v2 : VPos, doc : Doc :: iaddrs(doc, v1) = iaddrs(doc, v2) ==> findlinks(doc, v1) = findlinks(doc, v2)`

The converse also follows: if two V-positions in *different* documents both map to i_A, `find_links` on either yields the same links. V-ordering is irrelevant; only content identity matters.

[INV-REARRANGE-IDENTITY] provides the guarantee that doc2's POOM preserves i_A at the new V-position of "A" after rearrange. [SS-FIND-LINKS] provides the guarantee that find_links operates entirely in I-space after the initial V-to-I conversion.

---

**Summary**

The answer is **yes**, and it follows directly from three converging properties:
1. VCOPY creates I-address identity between doc1 and doc2 [ST-VCOPY]
2. REARRANGE preserves I-addresses, only updating V-displacements [INV-REARRANGE-IDENTITY]
3. `find_links` resolves V-spans to I-addresses via the POOM before searching the spanf — so the new V-position of "A" in doc2 yields the same i_A, the same spanf hit, and the same links [SS-FIND-LINKS, SS-LINK-SPACE]

## Code Exploration

Now I have everything I need. Let me trace the complete call chain with precise citations.

---

## Answer: V→I Resolution Across COPY + REARRANGE in `find_links`

**Short answer: Yes, `find_links` with a V-span for "A" in doc2 correctly resolves to the same I-address as "A" in doc1.** The design is intentional and mechanically guaranteed by two orthogonal invariants. Here is the full proof from the code.

---

### 1. What COPY records in the POOM

`docopy` [do1.c:45–65]:
```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)    // V→I for source
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)       // install in target POOM
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)    // register in spanfilade
```

Step 1 (`specset2ispanset` [do2.c:14–46]) walks the source specset. For each `VSPECID` it calls `findorgl` to get the source doc's POOM, then calls `vspanset2ispanset` [orglinks.c:397–402]:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

`permute` → `span2spanset` → `retrieverestricted` [retrie.c:56–85] searches the source POOM with the given V-span, and `context2span` [context.c:176–212] extracts the corresponding I-coordinates. This is the actual permascroll address of "A" (and "B").

Step 2 (`insertpm` [orglinks.c:75–134]) inserts 2D crums into doc2's POOM. For each I-span it allocates:

```c
movetumbler(&lstream, &crumorigin.dsas[I]);   // I-axis: permascroll address
movetumbler(&lwidth,  &crumwidth.dsas[I]);
movetumbler(vsaptr,   &crumorigin.dsas[V]);   // V-axis: position in doc2
// crumwidth.dsas[V] computed proportionally
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```
[orglinks.c:105–130]

Each crum in doc2's POOM is a 2D object: one axis is V-position in doc2, the other is the immutable permascroll I-address shared with doc1.

---

### 2. What REARRANGE does — and doesn't do — to those crums

`dorearrange` [do1.c:34–43] → `rearrangepm` [orglinks.c:137–142] → `rearrangend(docorgl, cutseqptr, V)` [edit.c:78–160].

Inside `rearrangend`, for each crum in the intersection zone:

```c
case 1:  case 2:  case 3:
    tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```
[edit.c:124–127]

`index` = V throughout (passed in as the 3rd argument [orglinks.c:139]). So `rearrangend` **only ever modifies `ptr->cdsp.dsas[V]`** — the V-axis displacement of each crum.

`ptr->cdsp.dsas[I]` is never touched by any code path in `rearrangend`, `rearrangecutsectionnd` [edit.c:191–204], or `makeoffsetsfor3or4cuts` [edit.c:164–184]. The I-coordinates set by COPY are structurally immutable to REARRANGE.

After REARRANGE on doc2:
- "A" crum: V-displacement updated to reflect its new position in doc2's V-ordering
- "A" crum: I-displacement is **identical** to the permascroll address COPY recorded

---

### 3. How `find_links` resolves the V-span

**Entry point** [fns.c:189–202] → `dofindlinksfromtothree` [do1.c:348–353] → `findlinksfromtothreesp` [spanf1.c:56–103].

**Step 1:** Convert V-spec → sporglset (I-spans) [spanf1.c:70–71]:

```c
specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
```

`specset2sporglset` [sporgl.c:14–33] → `vspanset2sporglset` [sporgl.c:35–65]:

```c
if (!findorgl(taskptr, granf, docisa, &orgl, type)) return(NULL);
for (; vspanset; vspanset = vspanset->next) {
    vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    // ... pack I-spans into sporglset
}
```

`vspanset2ispanset` [orglinks.c:397–402] runs `permute(taskptr, orgl, V→I)` on **doc2's POOM** with the given V-span. After REARRANGE, doc2's POOM has "A" at its new V-position. `retrieverestricted` [retrie.c:56–85] finds the crum whose updated V-displacement covers this new position:

```c
context = retrieveinarea(fullcrumptr, &span1start, &span1end, index1, ...);
```
[retrie.c:83]

`context2span` [context.c:176–212] then extracts the I-coordinates from that crum:

```c
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);  // idx2 = I
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```
[context.c:206–207]

These are the I-coordinates that COPY wrote and REARRANGE left untouched — exactly "A"'s permascroll address.

**Step 2:** Search spanfilade by I-span [spanf1.c:77]:

```c
sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

→ `sporglset2linksetinrange` [sporgl.c:239–269]:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, infoptr);
```
[sporgl.c:259]

The spanfilade is global (not per-document). Any link whose endpoint was registered against "A"'s I-span — whether attached through doc1 or any other document — appears here. Crucially, note that the `homedoc` filter is **explicitly disabled**:

```c
if (FALSE/*trying to kluge links followable thru versions */&&...SPORGLID...) {
    movetumbler(&sporglset->sporgladdress, &linfo.homedoc);
} else
    infoptr = NULL;
```
[sporgl.c:251–255]

`infoptr = NULL` means `retrieverestricted` does not filter by document identity. The lookup is purely I-span-based.

---

### 4. Summary: The Invariant Chain

| Step | What happens | I-address of "A" |
|------|-------------|-----------------|
| `insert` in doc1 | I-address assigned from permascroll | established |
| `copy` to doc2 | `insertpm` records `dsas[I]` = same permascroll address | preserved |
| `rearrange` on doc2 | `rearrangend` only modifies `dsas[V]` [edit.c:125] | **unchanged** |
| `find_links` V-spec on doc2 | `permute` searches doc2 POOM by new V-position → same crum → same `dsas[I]` | resolved correctly |
| spanfilade lookup | `retrieverestricted` on global spanfilade by I-span | finds all links |

**"A" in doc1 and "A" in doc2 share the same permascroll I-address because COPY encoded it into the POOM's I-axis, and REARRANGE operates exclusively on the V-axis.** `find_links` running `permute` on doc2's post-rearrangement POOM recovers that I-address correctly regardless of where "A" sits in V-space in doc2. The link resolution is therefore identical, by structural construction.
