# Consultation Answers — Operational Fragmentation Bounds

**Inquiry:** What must the system guarantee about the growth of internal mapping entries as sequences of INSERT, DELETE, and COPY operations are applied? What bounds must hold on state representation size relative to content size?
**Date:** 2026-02-26 12:03
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When a document undergoes a long sequence of insertions and deletions, must the system's record of that document's structure remain bounded relative to the amount of content it currently contains?

### Nelson's Answer

# No — The System's Record Grows Without Bound By Design

Nelson's architecture explicitly rejects bounded storage relative to current content. The system is designed so that a document's total footprint grows monotonically with every operation ever performed on it, regardless of how much content the document currently displays.

## The Append-Only Principle

The storage model is fundamentally append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every insertion adds bytes to I-space permanently. Every deletion removes content only from V-space (the current arrangement), not from I-space (permanent storage):

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

A document that has undergone a thousand insertions followed by a thousand deletions retains all thousand insertions' worth of I-space content. The current V-space mapping may point to only a handful of bytes, but the historical I-space footprint is the sum of all content ever created.

## Historical Backtrack Requires Unbounded State

The guarantee of historical backtrack makes bounded state impossible in principle:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

To reconstruct any previous version on demand, the system must retain:
- All I-space content ever created (the raw bytes)
- All V-space arrangements ever constructed (the version mappings)
- Sufficient structural information to reconstruct any historical state

Nelson designed a specific data structure for this purpose — the **historical trace enfilade**:

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

## What IS Bounded vs. What Is Not

There are two distinct aspects of a document's structural record:

| Aspect | Bounded by current content? |
|--------|---------------------------|
| Current V→I mapping (one version's arrangement) | Yes — proportional to current byte count |
| Total I-space content (all bytes ever created) | **No** — grows monotonically with every insertion |
| Version history (all past arrangements) | **No** — grows with every edit operation |
| Link history (all links ever created) | **No** — deleted links await "historical backtrack functions" |

The current V-space mapping for a single version is naturally bounded by that version's content size. But the total system record for a document — which Nelson treats as "an evolving ONGOING BRAID" [LM 2/14] — accumulates without limit.

## Performance Despite Unbounded Growth

Nelson addresses the performance concern not by bounding state, but by requiring that operations remain efficient as state grows. The enfilade structures are designed so that:

> "By various enfilade structures we were able to come up with a design that could conceivably scale up infinitely" [LM 1/36]

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The "soft corridor" requirement [LM 4/2] demands that the system slow down only logarithmically as the docuverse grows — not that it discard history to stay small.

## The Economic Counterbalance

The only constraint on this unbounded growth is economic, not structural. Nelson's funding model requires ongoing storage rental paid by the document owner:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

If a document's accumulated history becomes expensive to store, the owner bears that cost. But the system never compacts, garbage-collects, or discards historical state. That would violate the permanence guarantee:

> "Any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

## Summary

The answer is unambiguously **no**. The system's record of a document's structure is not required to remain bounded relative to current content. It grows with every operation ever performed. This is not an oversight but a deliberate design choice flowing from three foundational commitments: append-only storage, historical backtrack, and permanent addressing. The engineering challenge — keeping operations fast despite unbounded growth — is solved by the enfilade data structures, not by discarding history.

---

## Question 2 [nelson]

> Must a single deletion operation — removing one character or one span — add at most a fixed, small number of new entries to the system's internal account of document structure?

### Nelson's Answer

## Answer: Nelson Does Not Explicitly State This Bound

Literary Machines does not contain an explicit guarantee that a single deletion adds at most a fixed, small number of new entries to the document's internal structural representation. Nelson describes the *effects* of deletion and the *efficiency* of the enfilade data structures, but not the specific structural overhead per operation.

### What Nelson Does Say

On the DELETE operation itself, the specification is terse:

> "This removes the given span from the given document." — 4/66

On enfilade efficiency, Nelson describes the properties qualitatively:

> "the system we now call the first enfilade — the Model T: a data structure that manages huge agglomerates of text and their arrangement in and out of core. With its attendant routines, the Model T enfilade handles the revision of serial data very quickly and very cleanly." — 1/33

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." — 1/34

On deletion semantics, he specifies that deletion is a V-space operation — content leaves the current arrangement but remains in I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" — 4/9

### What the Model Implies (But Nelson Doesn't State)

The bound *does* follow as a mathematical consequence of the span-based V-space model Nelson describes.

A document's V-stream is an ordered sequence of span entries, where each entry maps a contiguous V-range to a contiguous I-range. When a contiguous V-span is deleted:

- The span containing the **start** of the deletion may be split (if the deletion begins mid-span): +1 new entry
- The span containing the **end** of the deletion may be split (if the deletion ends mid-span): +1 new entry
- All spans fully covered by the deletion are removed: −N entries

So the worst case is **+2 new span entries** (from two boundary splits), which is indeed a fixed, small constant. This is inherent in how contiguous ranges work — cutting into a contiguous range at one point produces at most two pieces.

Nelson's own description of spans confirms the contiguous-range model:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse, (or merely to a series of elements of the same type, which is a degenerate case of a subtree)." — 4/24

And the V-stream is explicitly described as a sequence of such spans:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." — 4/11

### The Distinction

There are two levels where "new entries" could be counted:

1. **Span entries in the V→I mapping** — bounded by +2 per deletion, as argued above. This is the document's *logical* structure.

2. **Enfilade tree nodes** — the internal tree structure may require rebalancing after operations, potentially involving O(log n) node adjustments. Nelson does not specify this level of detail; the enfilade internals are described only as maintaining "canonical order" efficiently.

Nelson's claim that the system "could conceivably scale up infinitely" (1/36) and operates within a "soft corridor" of logarithmic slowdown (4/2) is consistent with bounded structural overhead, but these are performance claims, not structural-entry-count guarantees.

### Verdict

**No**, Nelson does not explicitly guarantee this bound. He provides a model (span-based V-space over permanent I-space) from which a constant bound on new span entries per deletion follows as a mathematical consequence, and he describes the enfilades as efficient and clean. But the specific invariant — that a single deletion adds at most a fixed, small number of new structural entries — is an *implication* of the design, not a *stated* requirement.

NEED_RAW: 1/33-1/38, 4/9, 4/66 — to verify whether Nelson says anything more specific about structural overhead in the original pages than what the curated sources capture.

---

## Question 3 [nelson]

> If a document is built entirely by copying spans from other documents, must the structural description of that document grow only with the number of distinct copy operations, not with the total volume of content referenced?

### Nelson's Answer

## Yes — and this follows necessarily from the span-based architecture.

A document built entirely from COPY operations has a structural description (its V→I mapping) that grows with the number of copy operations, not with the total bytes referenced. This is not an optimization — it is inherent in how Xanadu represents documents.

### The span is the fundamental unit of reference

A span is a pair of tumblers that designates a contiguous region of any size:

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." [LM 4/24]

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

A span that brackets ten bytes is the same size as a span that brackets ten billion bytes — it is always just two tumblers. The cost of *describing* a region is independent of the region's *volume*.

### COPY creates span mappings, not byte duplicates

The COPY operation works on span-sets:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This is transclusion — the copy shares I-addresses with the source. No new I-space content is created. What is created is a V-space mapping: "V-positions X through Y now refer to I-positions A through B." Each such mapping entry is a span pair — constant size regardless of how many bytes the span covers.

### The document IS its V→I mapping

A document's virtual byte stream is defined by its arrangement of I-space references:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The term **"non-native byte-spans"** is revealing. Each inclusion is represented as a span — a contiguous range reference — not as individual byte pointers. A document assembled from *k* COPY operations produces *k* span entries in the V→I mapping (assuming each copy is a contiguous source region). Whether those *k* spans collectively reference a thousand bytes or a trillion, the structural description has *k* entries.

### Enfilades maintain this efficiency internally

The POOM enfilade — which maps V-space to I-space — is specifically designed for this:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order." [LM 1/34]

> "By various enfilade structures we were able to come up with a design that could conceivably scale up infinitely." [LM 1/36]

The "soft corridor" performance requirement confirms that operations scale logarithmically with the structure's size, not with the volume of content:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. (It can't be linear. The system cannot slow down by half as its size doubles.)" [LM 4/2]

### The compound document confirms this

Nelson's description of compound documents makes the proportion explicit — a compound document is structurally defined by its references, not by the content those references resolve to:

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

The document's structure *is* the list of quote-links (span references). Its size is determined by how many references you make, not by how much content lies behind each reference.

### Summary

The answer is yes, and it is a **structural guarantee**, not an implementation choice. Because:

1. **Spans are constant-size** regardless of the region they cover
2. **COPY operates on span-sets**, creating one mapping entry per contiguous source region
3. **The V→I mapping IS the document** — its size equals the number of mapping entries
4. **Enfilades maintain logarithmic access** over this mapping

A document composed of 5 COPY operations referencing 5 terabytes of content has the same structural complexity as one composed of 5 COPY operations referencing 5 bytes. The structural description scales with *k* (the number of distinct operations), not with *n* (the total volume referenced).

---

## Question 4 [nelson]

> Must the system guarantee that an insertion into the middle of a document adds no more than a constant amount of bookkeeping beyond storing the new content itself?

### Nelson's Answer

# No. Nelson does not guarantee constant bookkeeping for mid-document insertion.

## What Nelson actually specifies

Nelson addresses insertion performance at three levels, none of which promise O(1) bookkeeping:

### 1. The INSERT operation (semantic level)

The FEBE specification describes what INSERT *does*, not what it *costs*:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

This describes the logical effect — all subsequent V-addresses shift — but says nothing about how much work that shift requires internally.

### 2. The enfilade structures (implementation level)

Nelson characterizes the enfilades qualitatively, not with complexity bounds:

> "the system we now call the first enfilade — the Model T: a data structure that manages huge agglomerates of text and their arrangement in and out of core. With its attendant routines, the Model T enfilade handles the revision of serial data **very quickly and very cleanly**." [LM 1/33]

On Barus's linking enfilade (the POOM, which maps V-space to I-space):

> "His new method would allow linkages to keep up with all changes. It was **instantaneous and permanent** and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

"Very quickly," "instantaneous," and "could grow indefinitely" are qualitative claims about the enfilade's behavior. "Instantaneous" in context means the result is immediately available and the structure remains valid — not that the operation completes in constant time. Tree-based structures (which enfilades are) achieve O(log n) per operation, not O(1).

### 3. The soft corridor (system-wide scaling)

The only quantitative performance bound Nelson specifies is system-wide, not per-operation:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. (It can't be linear. The system cannot slow down by half as its size doubles.)" [LM 4/2]

The soft corridor requires that response time degrades **logarithmically** as the docuverse grows — not that individual operations take constant time. This is a bound on how the *system* scales, not on how a single insertion behaves relative to document size.

## What the architecture implies

An insertion into the middle of a document involves two distinct costs:

1. **I-space append** — New bytes are appended to the permascroll. This is indeed O(1) in the content size: "User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

2. **V-space remapping** — The POOM enfilade must be updated to reflect the new insertion point. This is the "bookkeeping" the question asks about. Since the POOM is a tree structure that maps V-addresses to I-addresses, updating it after a mid-document insertion is O(log n) where n is the document size. Nelson never claims or requires this to be O(1).

## The answer

Nelson guarantees that insertion is *fast* and that the system *scales well*. He does not guarantee that insertion bookkeeping is bounded by a constant. The enfilade architecture he describes is tree-based, and the only quantitative bound he specifies (the soft corridor) is logarithmic, not constant. A system that requires O(log n) bookkeeping per mid-document insertion is fully consistent with everything Nelson wrote.

---

## Question 5 [nelson]

> When content is shared across many documents through transclusion, must the system's total state grow only with the number of sharing relationships, not with the size of the shared content multiplied by the number of uses?

### Nelson's Answer

## Yes — This Is Architectural, Not an Optimization

The answer is emphatically yes. This property is not merely desirable; it is a structural consequence of the I-space/V-space separation that defines how Xanadu stores everything.

### Content Is Stored Once

Content lives permanently in I-space. A document's arrangement lives in V-space as a mapping *over* that content. Multiple documents referencing the same content share the same I-space bytes:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The word "virtual" is doing real work here. An inclusion doesn't create new bytes — it creates a reference to existing bytes. The included bytes occupy V-space positions in the including document but occupy no additional I-space.

### COPY Is Reference, Not Duplication

The COPY operation — which is how transclusion happens at the protocol level — explicitly shares I-addresses:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This operation creates a V-space mapping from positions in the target document to I-space addresses that already exist in the source. The I-space content is not duplicated. Each transclusion adds only a mapping entry (a span in V-space pointing to a span in I-space), not a content copy.

### No Copying Between Documents

Nelson states this explicitly as a design achievement:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

This is stronger than merely saying "we avoid copying for efficiency." Nelson says copying is *not required* — the architecture makes it unnecessary. The system solves distributed update precisely because there is only one copy of the content.

### What Each Sharing Relationship Costs

When a document transcludes content, the cost is:

- **One V→I mapping entry** in the POOM enfilade (the positional mapping structure)
- **Zero additional I-space content** in the GRAN enfilade (the content store)

The enfilade structures are designed specifically for this:

> "the system we now call the first enfilade — the Model T: a data structure that manages huge agglomerates of text and their arrangement in and out of core." [LM 1/33]

The POOM enfilade maps V-addresses to I-addresses. The GRAN enfilade stores actual bytes. When 1,000 documents transclude the same paragraph, GRAN holds one copy of the paragraph; POOM holds 1,000 mapping entries (one per document). The growth is proportional to the number of sharing relationships, not to content size × number of uses.

### Versions Demonstrate This at Scale

The version mechanism is the most dramatic example. CREATENEWVERSION creates "a new document with the contents of document \<doc id\>" [LM 4/66], but the new document shares all I-space content with the original. Only subsequent edits add new I-space bytes.

Nelson describes this as "prismatic" storage:

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another." [LM 2/19]

A document with 100 versions doesn't store 100 copies. It stores the union of all unique content ever created, plus 100 V-space arrangements referencing that content. The "refractions" are views, not copies.

### The Discovery Operation Proves It

The existence of FINDDOCSCONTAINING confirms this architecture:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This operation is possible precisely *because* transclusion shares I-addresses. If content were copied, there would be no structural way to find all documents containing a given passage — you'd need full-text search. Because transclusion preserves I-address identity, the system can find all sharing relationships by tracing I-space references.

### The Principle

The deeper point: content identity in Xanadu is based on *creation*, not on *value*. As the sporgl-provenance concept notes: "Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address." Sharing is a structural relationship tracked by address identity, and the cost of each sharing relationship is one mapping entry — independent of the size of the shared content.

This is not a storage optimization. It is the foundation on which attribution, royalties, version comparison, and the entire interconnected docuverse rest.

---

## Question 6 [nelson]

> As a document accumulates a history of edits across many versions, must the system's representation of any single version remain proportional to that version's content size rather than to the total number of edits ever performed?

### Nelson's Answer

## Yes — But Nelson States It Architecturally, Not as a Formal Bound

Nelson never writes an explicit complexity guarantee like "retrieving version K must be O(|version K|) not O(|total edits|)." But his architecture *inherently achieves this property*, and his performance requirements *demand* it.

### The Architecture Makes It So

The V-space/I-space separation is the key. A version IS a V-space arrangement — a mapping from virtual positions to permanent I-space addresses. The size of this mapping is determined by how much content the version contains, not by how many edits preceded it.

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

Each version defines its own V→I mapping. A 1,000-byte version has a mapping over ~1,000 bytes of I-space content whether the document has been through 5 edits or 5,000 edits. The I-space content those spans point to is permanent and shared — it doesn't grow per-version.

Edits only change the V-space arrangement:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

INSERT shifts V-addresses; DELETE removes V-addresses; neither grows the I-space content that other versions reference. Previous versions' V→I mappings are untouched.

### Nelson's Performance Requirements Demand It

Nelson makes an explicit "virtually instantaneous" retrieval claim for any version:

> "We believe our Prismatic storage can support virtually instantaneous retrieval of any portion of any version (historical or alternative)." [LM 2/19]

If version retrieval degraded linearly with edit count, a heavily-edited document would eventually violate this guarantee. Nelson's phrasing — "any portion of any version" — implies uniform retrieval performance regardless of how deep in the history you reach.

The "part-pounce" mechanism confirms on-demand reconstruction from stored fragments:

> "When you 'go to' a certain part of a document, the whole document is not ready to show; yet the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." [LM 2/16]

The fragments are I-space content. The V→I mapping tells the system which fragments to assemble. The cost of assembly depends on how many fragments the *requested version* contains, not on how many edits have accumulated since.

### The Soft Corridor Principle

Nelson's "soft corridor" requirement applies to system-wide growth, but the principle is the same:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. (It can't be linear. The system cannot slow down by half as its size doubles.)" [LM 4/2]

A document's edit history is a form of growth. If retrieving version 1 of a document slowed linearly as versions 2 through 10,000 accumulated, that document would fall outside the soft corridor. The logarithmic-at-worst requirement applies at every level of the system's operation.

### Enfilades as the Mechanism

The enfilade data structures are explicitly designed to maintain efficient access as content grows:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

> "By various enfilade structures we were able to come up with a design that could conceivably scale up infinitely." [LM 1/36]

Nelson mentions three enfilade types: the GRAN (content storage), the POOM (V→I mapping — the "eye in the pyramid"), and the "historical trace enfilade" for version history [LM 1/36]. The separation of the historical trace from the positional mapping is architecturally significant — history tracking is a *separate* structure from version retrieval, preventing edit accumulation from degrading version access.

### Summary

Nelson guarantees this property through three reinforcing mechanisms:

| Mechanism | How it ensures proportionality |
|-----------|-------------------------------|
| **V-space/I-space separation** | A version's representation IS its V→I mapping, sized by content |
| **"Virtually instantaneous" retrieval** | Any version, any portion — implies edit-count independence |
| **Enfilade design** | Separate structures for positional mapping vs. historical trace |

He does not state a formal O(n) bound, but the architecture makes version representations structurally proportional to content size, and the performance requirements prohibit edit-count-dependent degradation.

NEED_RAW: [pages 059-064 (LM 1/33-1/38)] — The enfilade section may contain more specific performance claims about the POOM and historical trace enfilades that would strengthen or qualify this answer.

---

## Question 7 [nelson]

> Must the system guarantee that no editing operation — insert, delete, or copy — can cause the structural description of an unrelated document to grow?

### Nelson's Answer

# Does Nelson Guarantee Editing Cannot Grow an Unrelated Document's Structure?

**Short answer:** Nelson's specification *implies* this property strongly through operation semantics, ownership principles, and the I-space/V-space architecture — but he never states it as an explicit guarantee. The property falls into a gap between his semantic-level specification and implementation-level concerns.

## What the Operation Specifications Say

Every FEBE editing operation targets a specific document by its `<doc id>`:

- **INSERT**: "This inserts `<text set>` in document `<doc id>` at `<doc vsa>`. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

- **DELETEVSPAN**: "This removes the given span from the given document." [LM 4/66]

- **COPY**: "The material determined by `<spec set>` is copied to the document determined by `<doc id>` at the address determined by `<doc vsa>`." [LM 4/67]

- **REARRANGE**: "Rearrange transposes two regions of text." [LM 4/67]

None of these operations describe any side effect on documents other than `<doc id>`. The specification is silent about structural effects on unrelated documents — not because it permits them, but because it never contemplates them. Each operation reads as a closed mutation of a single document's V-stream.

## What the Architecture Implies

The I-space/V-space separation provides the strongest structural argument:

1. **V-space changes are per-document.** Each document has its own V-stream — its arrangement of content. Editing document A changes A's V-to-I mapping. Document B's V-to-I mapping is a separate structure entirely.

2. **I-space is append-only.** New content enters I-space; nothing already there changes. INSERT adds new bytes to I-space under the edited document's address. No existing I-space content (including content owned by other documents) is modified.

   > "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

3. **DELETE is V-space only.** Deletion removes content from a document's current V-space arrangement but does not touch I-space:

   > "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

   Other documents' V-streams are explicitly unaffected.

4. **COPY creates a mapping in the target, not the source.** When you copy from A to B, you create a new V-space entry in B pointing to I-space content that happens to live under A's address. A is not consulted or modified:

   > "Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

   The inclusion lives in B's V-space. A's structure is untouched.

## What the Ownership Principle Requires

Nelson's ownership model would be violated if editing one document could grow another's structure:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

If inserting text into document A (owned by Alice) caused structural growth in document B (owned by Bob), then Alice's action would be modifying Bob's property without his consent. This contradicts the absolute ownership guarantee.

The storage funding model reinforces this:

> "ALL SERVICES MUST BE SELF-SUPPORTING." [LM 4/5]

If Alice's edits caused Bob's storage to grow, Bob would be paying for Alice's actions. The economic model assumes owners pay for their own content.

## Where the Guarantee Becomes Uncertain

The complication arises with **system-level indexes** that Nelson specifies operationally but not structurally:

- **FINDDOCSCONTAINING**: "This returns a list of all documents containing any portion of the material included by `<vspec set>`." [LM 4/70]

  For this to work after COPY from A to B, *some* index must record that B now contains A's content. Where does this index live? Nelson doesn't say. If it's a system-wide structure (maintained by the back end), it's not part of any document's description. If it's somehow attached to document A, then COPY *would* grow A's structural description.

- **FINDLINKSFROMTOTHREE**: "This returns a list of all links which are (1) in `<home set>`, (2) from all or any part of `<from set>`, and (3) to all or any part of `<to set>` and `<three set>`." [LM 4/69]

  To find links *pointing to* a document efficiently, some reverse index must exist. Again, Nelson specifies the operation but not the index's structural location.

Nelson explicitly separates these concerns:

> "None of these commands are to be seen by the user. The user's concerns are to be seen on the screen; the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." [LM 4/61]

The internal representation — including whether indexes are per-document or system-global — is deliberately left as an implementation matter.

## What Nelson *Does* Guarantee About Scaling

The closest Nelson comes to a structural growth guarantee is the "soft corridor" performance requirement:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. (It can't be linear. The system cannot slow down by half as its size doubles.)" [LM 4/2]

And about the enfilades:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

These speak to *system-wide* scaling behavior, not to per-document structural isolation. The guarantee is about performance degradation curves, not about whether document A's representation is affected by operations on document B.

## Conclusion

Nelson's specification is **consistent with and strongly implies** the property that editing operations cannot grow an unrelated document's structural description, through three independent arguments:

1. **Operation semantics**: Every editing command targets a single `<doc id>` with no described side effects
2. **Ownership**: Modifying another owner's property would violate the absolute ownership guarantee
3. **Economic model**: Growing another's storage would violate the self-supporting funding requirement

However, Nelson **does not explicitly state this as a guarantee**. His specification operates at the semantic level (what operations mean to users), not at the structural level (how the back end represents documents internally). The system-level indexes required for FINDDOCSCONTAINING and link search are specified by their behavior, not by their structural residence.

An implementation that satisfies all of Nelson's explicit guarantees *could* maintain per-document reverse indexes that grow when other documents transclude or link — this would not violate any stated guarantee, though it would violate the spirit of ownership isolation. The more natural reading of the architecture is that such indexes are system infrastructure, not part of any individual document's description.

---

## Question 8 [nelson]

> If a user performs a deletion that splits a contiguous span into two parts, must the cost in structural bookkeeping be bounded independently of the size of the spans on either side of the split?

### Nelson's Answer

## On Split Cost and Structural Bookkeeping

The short answer: yes, that is the design intent. But Literary Machines addresses this at the level of performance requirements and enfilade properties, not as an explicit formal bound on individual operations.

### The Soft Corridor Requirement

The governing constraint is what I called the "soft corridor" [LM 4/2]:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. (It can't be linear. The system cannot slow down by half as its size doubles.)"

This is a global constraint: operations on the docuverse must degrade logarithmically with total size, not linearly. A split whose cost grew with the size of the spans on either side would violate this requirement for large documents — a deletion in a million-byte span would cost proportionally to a million, which is linear degradation.

### What the Enfilade Design Provides

The enfilades were designed precisely to make structural operations fast regardless of data size. The Model T enfilade:

> "handles the revision of serial data very quickly and very cleanly." [LM 1/33]

And Barus's contribution — the "eye in the pyramid" — ensured that:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The critical phrase is **canonical order** — after any operation (including a split), the structure remains in its canonical form without requiring a traversal proportional to the data. The enfilade is a tree; operations on trees cost proportional to depth, not to the size of subtrees on either side of the modification point.

The system was designed so that:

> "By various enfilade structures we were able to come up with a design that could conceivably scale up infinitely." [LM 1/36]

"Scale up infinitely" is incompatible with split costs that grow with span size.

### The Specific Operation

When a user deletes from the middle of a contiguous V-space span, the POOM enfilade (which maps V-space to I-space) must split one mapping entry into two. In tree-structure terms, this is a local operation affecting nodes along a single root-to-leaf path. The spans on either side — whether they contain ten bytes or ten billion — are represented by subtrees that are not traversed during the split. The cost is bounded by the tree depth, which grows logarithmically with the total number of entries.

### What Literary Machines Does Not Say

Nelson discusses enfilades at the level of design intent and capability, not at the level of formal complexity proofs. Literary Machines does not contain a statement like "split cost is O(log n) independent of span size." The enfilade theory itself — which I credit to the work of Roger Gregory, Mark Miller, and Stuart Greene — would contain the formal guarantees.

NEED_RAW: 1/33-1/38 (enfilade discussion), 4/1-4/5 (performance requirements) — these pages may contain more specific statements about operation complexity that the curated summaries condensed away.

### Summary

The soft corridor requirement [LM 4/2] mandates sub-linear scaling. The enfilade tree structure achieves this by ensuring that modifications (including splits) affect only a root-to-leaf path, whose length is logarithmic. The size of the spans on either side of the split is irrelevant — they sit in subtrees that are not traversed. This is not stated as a formal theorem in Literary Machines, but it is the direct consequence of the performance architecture that the enfilades were specifically built to provide.

---

## Question 9 [nelson]

> Must the system ensure that the total representation size across all documents grows at most linearly with the combined number of editing operations applied to those documents?

### Nelson's Answer

## Answer: No Explicit Linear Space Growth Bound

Nelson does not specify that total representation size must grow at most linearly with the number of editing operations. His performance guarantees address **time complexity**, not **space complexity**, and his architectural choices constrain space growth implicitly rather than by stated bound.

---

### What Nelson DOES Specify About Growth

**Time performance bound (the "soft corridor"):**

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. (It can't be linear. The system cannot slow down by half as its size doubles.)" [LM 4/2]

This is explicitly about **response time vs. system size**, not representation size vs. editing operations. The soft corridor diagram (page 4/2) plots slowdowns against SIZE (servers, links, etc.), requiring at most logarithmic degradation.

**Enfilade performance:**

> "the Model T enfilade handles the revision of serial data very quickly and very cleanly." [LM 1/33]

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order." [LM 1/34]

> "By various enfilade structures we were able to come up with a design that could conceivably scale up infinitely" [LM 1/36]

Again: speed of operations, canonical ordering, and unbounded scalability — not space bounds.

---

### Architectural Properties That Constrain Space

Nelson's design has structural properties that bear on space growth, but he frames them as architectural principles, not as complexity guarantees:

**1. Append-only I-space:** New content is added; nothing is overwritten or removed.

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

I-space grows by exactly the volume of new content inserted. DELETE and REARRANGE add zero bytes to I-space. This is *consistent with* linear growth but is stated as a storage paradigm, not a bound.

**2. Transclusion avoids duplication:** COPY shares I-addresses rather than duplicating bytes.

> "The material determined by \<spec set\> is copied to the document... at the address determined by \<doc vsa\>." [LM 4/67]

> "Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

COPY operations add V-space mapping entries (references) but no I-space content. This means transclusion-heavy workloads grow sub-linearly in I-space relative to operations. But Nelson states this as a design principle ("reference, not copy"), not as a complexity claim.

**3. V-space is a mapping, not a copy:**

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

Each version is a V→I mapping. The size of this mapping depends on the data structure (enfilades), but Nelson never states how mapping size relates to edit count.

---

### What Is Left Unspecified

Nelson does not address:

- The space cost per editing operation in the V-space mapping structures
- Whether enfilade tree nodes grow linearly, logarithmically, or otherwise with edits
- Whether the "general theory of enfilades" [LM 1/36] includes space complexity bounds
- Total representation overhead from version history accumulation

The "general theory of enfilades" is mentioned but not elaborated in Literary Machines:

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

Any space complexity properties of enfilades would be implementation-level results, not design-level guarantees from Nelson.

---

### Summary

| Aspect | Specified? | What Nelson says |
|--------|-----------|-----------------|
| Time vs. system size | **Yes** — logarithmic slowdown | Soft corridor [LM 4/2] |
| I-space growth model | **Yes** — append-only | "filed chronologically" [LM 2/14] |
| Duplication avoidance | **Yes** — transclusion shares I-addresses | "virtual copies" [LM 4/11] |
| Space vs. edit count | **No** | Not addressed |
| V-space mapping overhead | **No** | Left to enfilade implementation |

Nelson's design is *architecturally compatible* with linear space growth — append-only I-space grows by inserted content, transclusion avoids duplication, V-space mappings are lightweight references. But he never states this as a requirement or guarantee. His explicit performance concern is time, not space.

---

## Question 10 [nelson]

> When content is permanently stored and later referenced by address in a new document, must the new document's structural description record only the reference boundaries, not duplicate any representation of the content's internal structure?

### Nelson's Answer

## Yes — and this follows from the architecture itself, not from an explicit prohibition.

### The V→I mapping records only boundaries

A document's structure is its V-space arrangement: a mapping from virtual positions to I-space addresses. When content from another document is included, that mapping records **which I-space span** appears at **which V-space position** — nothing more.

Nelson defines the structural unit of reference as the **span**, which is exactly two tumblers (boundary addresses):

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. **There is no choice as to what lies between; this is implicit in the choice of first and last point.**" [LM 4/25]

The content between the boundaries is implicit in the addresses themselves. The referencing document stores the boundary pair. It does not — and structurally cannot — represent what lies within.

### Non-native content is fetched, not stored

The including document contains no representation of the included content at all:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; **all other bytes are obtained by front-end or back-end requests to their home locations.**" [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called **inclusions** or **virtual copies**." [LM 4/11]

The word "virtual" is precise here. The including document's V-stream contains positions that map to I-addresses in another document. The bytes at those addresses are retrieved on demand. The including document stores only the mapping — the span boundaries that say "V-positions 47 through 312 correspond to I-addresses in document X."

### No copying means no duplication of any kind

Nelson is explicit that the system eliminates copying:

> "**No copying operations are required** among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

If no copying occurs, then no representation of the referenced content — not its bytes, not its structure, not its internal arrangement — is duplicated in the referencing document.

### The enfilade architecture enforces this

The implementation architecture makes the boundary-only principle concrete through two enfilade types:

- **GRAN** (Granfilade): stores actual content in I-space
- **POOM** (Positional): maps V-space positions to I-space addresses

The POOM enfilade for a document records span correspondences: "V-position range A–B maps to I-address range X–Y." This is a mapping of boundaries to boundaries. The POOM does not and cannot contain any representation of the content's internal structure — that information lives exclusively in the GRAN at the content's home location.

### The span itself is structurally opaque

Nelson emphasizes that a span is not even a count:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. **It does not designate a number of anything.**" [LM 4/24]

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

A span is a boundary pair over an abstract tree. It says nothing about the internal structure, quantity, or arrangement of what falls between its endpoints. The referencing document records this boundary pair and delegates everything else to the home location.

### Summary

The answer is **yes**, and it follows from three independent architectural principles:

1. **Spans are boundary pairs only** — "there is no choice as to what lies between" [LM 4/25]
2. **Non-native content is fetched, not stored** — "obtained by front-end or back-end requests to their home locations" [LM 4/11]
3. **No copying occurs** — the system eliminates duplication by design [LM 2/36]

A new document's structural description records where referenced content begins and ends in I-space. The content's internal structure is the exclusive concern of its home location.

---

## Question 11 [gregory]

> When INSERT splits an existing POOM bottom crum at an interior point via `slicecbcpm`, does the operation always produce exactly two crums from one, or can a single INSERT produce three or more bottom crums in the POOM?

### Gregory's Answer

## KB Synthesis

## INSERT crum production: exactly +2 from one existing crum in normal operation

A single INSERT produces at most **3 bottom crums from 1 existing crum** — never more in normal operation. The mechanism has two distinct sub-operations, each contributing crums.

### Sub-operation 1: `slicecbcpm` (the split)

`slicecbcpm` is guarded by `whereoncrum() == THRUME` [PRE-DELETE, Finding 0075]. When blade[0] (the insertion point) falls strictly interior to an existing crum, one `slicecbcpm` call splits it into **two halves** — a left piece and a right piece that later gets shifted. This is exactly one split producing two crums from one.

The knife has exactly 2 blades (`knives.nblades = 2`) [SS-TWO-BLADE-KNIFE]. Could blade[1] also trigger a second `slicecbcpm` call?

blade[1] is computed by `findaddressofsecondcutforinsert()` as `(N+1).1` — the first address of the next subspace [SS-TWO-BLADE-KNIFE, Finding 0054]. In a well-formed document (subspace convention maintained [INV-SUBSPACE-CONVENTION]):
- Text crums occupy 1.x and do not extend into 2.x
- blade[1] = 2.1 therefore falls at a crum boundary (ONMYLEFTBORDER of the nearest link crum, or TOMYRIGHT of all text crums)
- Since `slicecbcpm` requires THRUME, blade[1] does **not** trigger a second cut

Therefore, `slicecbcpm` is called **exactly once** per interior INSERT in normal operation.

### Sub-operation 2: new content crum

After the split, one new bottom crum is created for the inserted content at [v, v+width) [ST-INSERT, Finding 0062].

### Net result

| Before | After | Net |
|--------|-------|-----|
| 1 crum spanning the insertion point | Left half + new content + right half = 3 crums | +2 |

This is precisely what [ST-CRUM-BOUND] (Finding 0062) documents as the "split cost":

> "First insert at v: splits existing crum into [left, v) and [v+1, ...); creates new crum [v, v+1). Cost: +2 crums (split creates two halves, minus the one destroyed, plus one new = net +2)."

### Boundary and coalescing cases produce fewer crums

When the insertion point equals an existing crum's reach (ONMYRIGHTBORDER), `makegappm` returns early without calling `slicecbcpm` [PRE-INSERT, Finding 0062, SS-WHEREONCRUM]. Instead, `isanextensionnd()` extends the existing crum in place — **+0 crums**. This is the coalescing behavior for sequential interior typing.

### Theoretical maximum with subspace violation

If the subspace convention is violated (e.g., a single crum spans both 1.x and 2.x due to prior REARRANGE across subspace [EC-REARRANGE-CROSS-SUBSPACE]), then blade[1] could fall THRUME within that crum, causing a second `slicecbcpm` call: 1 crum → 2 (first cut) → 3 (second cut) + 1 new content crum = **4 from 1**. But this is an anomalous state arising from subspace invariant violations, not documented as observed normal behavior.

### Summary

In normal operation: a single INSERT calls `slicecbcpm` **at most once**, producing **exactly 3 bottom crums from 1** (net +2). The 2-blade knife structure permits at most 2 cuts, but the second blade (subspace boundary) is structurally guaranteed to fall at crum boundaries, not interiors, when the subspace convention holds.

---

## Code Exploration

I now have everything needed. Here is the full answer.

---

## Answer: `slicecbcpm` and the POOM Bottom-Crum Count After INSERT

### Short answer

A single INSERT **can produce exactly three bottom crums from one** when both of the two knife blades fall strictly interior to the original crum's V-space range. It cannot produce four or more, because the INSERT path hard-codes `nblades = 2`.

---

### Detailed trace

#### 1. `slicecbcpm` itself always produces exactly 2 crums from 1

`slicecbcpm` [`ndcuts.c:373`] takes a single bottom crum `ptr` and a pre-allocated empty crum `new`. It:

1. Verifies the cut (`cut`) falls strictly inside `ptr` (THRUME check, `ndcuts.c:383`).
2. Computes `localcut = cut - grasp` (the cut position relative to ptr's start, `ndcuts.c:396`).
3. Constructs `newwid` — the left portion's width — by setting `newwid.mantissa[0] = localcut.mantissa[0]` (`ndcuts.c:440`).
4. Sets `ptr->cwid = newwid` (ptr is now the left piece) and `new->cwid = ptr->cwid - newwid` (new gets the right piece, via `locksubtract`, `ndcuts.c:444-445`).
5. Sets `new->cdsp = ptr->cdsp + ptr->cwid` (new starts where ptr now ends, `ndcuts.c:446`).
6. Inserts `new` as `ptr`'s immediate right sibling: `adopt(new, RIGHTBRO, ptr)` [`ndcuts.c:448`].

**Every call to `slicecbcpm` converts exactly one crum into exactly two.**

---

#### 2. INSERT creates 2 blades, both of which may fall in the same crum

In `makegappm` [`insertnd.c:124`]:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);       // insertnd.c:144
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);  // insertnd.c:145
knives.nblades = /*1*/2;                                  // insertnd.c:146
```

Blade[0] is the insertion point P1. Blade[1] (P2) is computed by `findaddressofsecondcutforinsert` [`insertnd.c:174`] to lie just above P1 in tumbler space, establishing the "gap" between the pre-existing content and the new content. By construction P2 > P1.

---

#### 3. The blade loop in `makecutsbackuptohere` only slices `ptr` once per call

At the height-0 (bottom-crum) branch in `makecutsbackuptohere` [`ndcuts.c:77-91`]:

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {               // loops i=0 then i=1
        if (whereoncrum(..., &knives->blades[i], ...) == THRUME) {
            new = createcrum(...);
            slicecbcpm(ptr, offset, new, &knives->blades[i], ...); // ndcuts.c:84
            ivemodified(ptr);
            ivemodified(new);
            setwisp(ptr);
        }
    }
    return(0);
}
```

`whereoncrum` [`retrie.c:345`] for POOM:

```c
left  = offset + ptr->cdsp          // retrie.c:356
right = left   + ptr->cwid          // retrie.c:364
THRUME  iff  left < address < right  (strictly interior)  // retrie.c:366-367
```

**After `slicecbcpm` fires for blade[0]=P1:**
- `ptr` is truncated to [A, P1) — its `cwid` has been reduced.
- `new_0` = [P1, B) is inserted as ptr's right sibling.

**When the loop then checks blade[1]=P2 against `ptr`=[A,P1):**
- `left = A`, `right = P1`; P2 > P1 → `whereoncrum` returns `TOMYRIGHT`, **not THRUME**.
- `slicecbcpm` is **not** called for blade[1] on `ptr`.

So within one `makecutsbackuptohere` call, `ptr` is sliced at most once.

---

#### 4. The outer loop in `makecutsnd` runs a second pass for the remaining cut

Back in `makecutsnd` [`ndcuts.c:15`]:

```c
makecutsdownnd(fullcrumptr, &offset, knives);       // first pass
for (...; sonsarecut(fullcrumptr, &offset, knives); ...) {  // ndcuts.c:24
    makecutsdownnd(fullcrumptr, &offset, knives);   // second pass if any son is still cut
}
```

`sonsarecut` [`ndcuts.c:359`] checks whether any son of `fullcrumptr` is still THRUME by any blade. After the first pass:
- `new_0` = [P1, B) is THRUME for blade[1]=P2 (since P1 < P2 < B) → returns `TRUE`.

**Second pass: `makecutsbackuptohere` is called on `new_0`=[P1,B):**
- Blade[0]=P1: `whereoncrum([P1,B), P1)` → P1 equals `left` → `ONMYLEFTBORDER`, not THRUME. No slice.
- Blade[1]=P2: P1 < P2 < B → THRUME. `slicecbcpm` fires.
  - `new_0` becomes [P1, P2).
  - `new_1` = [P2, B) inserted as new_0's right sibling.

**After the second pass:** three crums in the tree: `[A,P1)`, `[P1,P2)`, `[P2,B)`.

**Third `sonsarecut` check:**  
- [A,P1): blade[0]=P1 → `ONMYLEFTBORDER`; blade[1]=P2 → `TOMYRIGHT`. Not THRUME.
- [P1,P2): blade[0]=P1 → `ONMYLEFTBORDER`; blade[1]=P2 → `ONMYRIGHTBORDER`. Not THRUME.
- [P2,B): blade[0]=P1 → `TOMYLEFT`; blade[1]=P2 → `ONMYLEFTBORDER`. Not THRUME.

→ `sonsarecut` returns `FALSE`. Outer loop exits. **Three crums, done.**

---

#### 5. The maximum is exactly three — not four or more

`MAXCUTS = 4` [`common.h:108`] defines the maximum blade-array size, but the INSERT path never approaches that ceiling. The knife structure is populated in only one place for INSERT — in `makegappm` — and it always sets:

```c
knives.nblades = /*1*/2;   // insertnd.c:146
```

The commented-out `/*1*/` shows a prior version used only one blade (which would always produce exactly two crums). The current code uses two blades, allowing up to two cuts and thus **at most three crums**.

Paths that use 3 or 4 blades live only in `rearrangend` (`edit.c:103`, which reads `nblades` from a cutseq), which is the delete-span / copy path, not the insert path.

---

### Summary

| Condition on original crum [A,B) | Crums produced | Mechanism |
|---|---|---|
| Only P1 strictly interior (P2 ≥ B) | **2** | One `slicecbcpm` call via blade[0]; blade[1] misses |
| Both P1 and P2 strictly interior (A < P1 < P2 < B) | **3** | blade[0] slices in pass 1; blade[1] slices `new_0` in pass 2 |

Three is the maximum a single INSERT can produce from one original bottom crum, because `makegappm` unconditionally sets `knives.nblades = 2` [`insertnd.c:146`], and two blades can create at most two cuts. `slicecbcpm` itself is always a strict one-into-two operation [`ndcuts.c:438-448`]; the three-way outcome arises from two sequential calls to `slicecbcpm` across two passes of the `makecutsnd` outer loop [`ndcuts.c:24-27`].

---

## Question 12 [gregory]

> Does DELETE ever increase the number of POOM bottom crums — specifically, when `deletend` slices boundary crums via the THRUME case, does the surviving fragment always replace the original crum in-place, or can it create additional entries?

### Gregory's Answer

## KB Synthesis

## DELETE and POOM Bottom Crum Count

**Yes, DELETE can increase bottom crum count by at most +1.**

The mechanism is two-phase and requires synthesizing [PRE-DELETE] (Finding 0075), [INV-NO-ZERO-WIDTH-CRUM] (Finding 0075), and [ST-DELETE] (Finding 0075).

---

### Phase 1: Cutting

`slicecbcpm` is called only when a deletion boundary falls strictly interior to a crum — `whereoncrum() == THRUME`, meaning `grasp < boundary < reach`. Each THRUME boundary **splits one crum into two** non-zero-width pieces:

- Original crum retains the left portion (width = `localcut`)  
- A new crum is created for the right portion (width = `cwid - localcut`)

From [INV-NO-ZERO-WIDTH-CRUM]: both resulting widths are guaranteed strictly positive. So Phase 1 can add up to +2 crums (one per deletion boundary), never in-place.

---

### Phase 2: Classification and Removal

After cutting, crums are classified:
- **Case 0** (before range): untouched
- **Case 1** (fully within range): `disown` + `subtreefree` — removed
- **Case 2** (after range): shifted

---

### The +1 Case

When both deletion boundaries are THRUME within the same single crum `[1.1, 1.9)` and the deletion is `[1.3, 1.6)`:

| Step | Action | Crum count |
|------|--------|-----------|
| Start | One crum `[1.1, 1.9)` | 1 |
| Phase 1, left cut | Split at 1.3 → `[1.1, 1.3)` + `[1.3, 1.9)` | 2 |
| Phase 1, right cut | Split at 1.6 → `[1.1, 1.3)` + `[1.3, 1.6)` + `[1.6, 1.9)` | 3 |
| Phase 2 | Remove interior fragment `[1.3, 1.6)` (Case 1) | **2** |

Net result: **1 → 2 crums. Count increased by +1.**

The surviving fragments (`[1.1, 1.3)` and `[1.6, 1.9)`) are not simple in-place replacements — the new right-side crum was freshly allocated by `slicecbcpm` during Phase 1.

---

### Other Cases Are Non-Increasing

- **Zero THRUME boundaries** (deletion is exactly crum-aligned): Phase 2 removes whole crums, no splits. Count decreases.
- **One THRUME boundary** (deletion starts interior, ends at crum boundary, or vice versa): +1 from split, -1 from removing the interior fragment. Net: 0.
- **THRUME boundaries in different crums spanning interior crums**: Phase 1 adds +2, Phase 2 removes the interior crums plus the two interior fragments. If there are ≥1 complete crums in the interior, net is non-positive.

---

### Maximum Increase

The maximum increase is **+1**, occurring precisely when both deletion boundaries fall strictly interior to the same single crum [PRE-DELETE, Finding 0075]. This is analogous to how INSERT at an interior position produces +2 crums [ST-INSERT, Finding 0062] — but DELETE recovers one of the new fragments by removing it in Phase 2.

From [ST-INSERT] Finding 0062 for contrast: consecutive interior typing after an initial interior insert costs +0 crums per character due to `isanextensionnd` coalescing. No equivalent coalescing exists for DELETE — every interior-to-interior deletion nets +1.

---

## Code Exploration

Now I have all the information needed. Let me compile the complete answer.

---

## Answer

### Short answer

Yes — DELETE can increase the number of POOM bottom crums, and it always does so when a cut boundary falls inside an existing bottom crum. The surviving left fragment replaces the original crum in-place; the right fragment is always a **newly created, separately inserted node** (not an in-place replacement). This is not a degenerate edge case — it is the designed and necessary mechanism.

---

### The two-phase structure of `deletend`

`deletend` [edit.c:31–76] has two sequential phases:

**Phase 1 — Pre-cutting via `makecutsnd`:**

```c
makecutsnd (fullcrumptr, &knives);
```

This must run first to guarantee that no bottom crum straddles any cut boundary. Without it, the classification step (phase 2) would encounter crums that cannot be cleanly categorized.

**Phase 2 — Classification and action:**

```c
newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case -1: gerror("deletend can't classify crum\n"); /* falls through */
      case 0:  break;                                    /* no action */
      case 1:  disown(ptr); subtreefree(ptr); break;    /* delete */
      case 2:  tumblersub(...); break;                  /* shift displacement */
    }
}
```

Note: `newfindintersectionnd` [ndinters.c:38–42] is now a stub — it sets `*ptrptr = fullcrumptr` and offset=0. The loop therefore iterates over **all** direct children of the full POOM crum, not a narrowed subtree.

---

### Where THRUME drives crum creation

The THRUME constant is defined as `0` [common.h:88]:

```c
#define TOMYLEFT      -2
#define ONMYLEFTBORDER -1
#define THRUME         0    /* cut falls inside the crum */
#define ONMYRIGHTBORDER 1
#define TOMYRIGHT      2
```

`whereoncrum` [retrie.c:345–373] returns THRUME for POOM when:

```
left = offset + cdsp
right = left + cwid
left < address < right
```

i.e., the cut address falls **strictly inside** the crum's virtual span.

---

### `makecutsbackuptohere` — where additional crums are born

When `makecutsbackuptohere` [ndcuts.c:69–140] reaches a height-0 (bottom) crum, it iterates over all knife blades:

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
            new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);  // line 80
            ...
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);  // line 84
            ivemodified((typecorecrum*)ptr);
            ivemodified((typecorecrum*)new);
            setwisp((typecorecrum*)ptr);
        }
    }
    return(0);
}
```

`slicecbcpm` [ndcuts.c:373–450] then does the actual split:

```c
// Left fragment: ptr keeps the portion [left, cut)
locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, ...);
movewisp(&newwid, &ptr->cwid);                    // ptr = left fragment, width shrunk

// Right fragment: new = portion [cut, right)
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);  // new starts where left ends

adopt(new, RIGHTBRO, ptr);   // line 448 — insert new as a RIGHT SIBLING
```

**`ptr` is mutated in-place** — its width is truncated to `[left, cut)`. **`new` is a freshly allocated crum** inserted as a new sibling node to the right of `ptr`. The tree gains one node per sliced bottom crum.

---

### Can one bottom crum be sliced by both knives?

Yes — if a single bottom crum spans the entire deletion range (from before `origin` to past `origin+width`), the loop in `makecutsbackuptohere` slices `ptr` at `blades[0]` (origin) on iteration `i=0`. After that slice, `ptr` covers only the left portion. When `i=1` runs, `whereoncrum(ptr, blades[1])` is no longer THRUME on the truncated `ptr`.

But the newly-created `new` (covering `[origin, original_end)`) now straddles `origin+width`. The outer retry loop in `makecutsnd` [ndcuts.c:24–27] handles this:

```c
for (fullcrumptr = findfullcrum((typecorecrum*)fullcrumptr);
     sonsarecut(fullcrumptr, &offset, knives);   // checks if any son still has THRUME
     fullcrumptr = findfullcrum((typecorecrum*)fullcrumptr)) {
    clear(&offset, sizeof(offset));
    makecutsdownnd(fullcrumptr, &offset, knives);
}
```

`sonsarecut` [ndcuts.c:359–371] returns TRUE if any son still has THRUME for any knife, causing a second pass. This second pass slices `new` at `origin+width`, yielding yet another new crum. **One crum that spans both boundaries becomes three crums** — left fragment, middle (to be deleted), right fragment.

---

### THRUME in `deletecutsectionnd` is a fatal error path

After `makecutsnd` completes, the code assumes all THRUME cases have been eliminated. If `deletecutsectionnd` returns -1 (THRUME), the switch statement in `deletend` hits:

```c
case -1:
    gerror ("deletend can't classify crum\n");
case 0:
    break;
```

There is **no `break` after case -1**. However, `gerror` is defined as `qerror` [common.h:119], which calls `abort()` [genf.c:546–551]:

```c
INT qerror(char *message) {
    fprintf (stderr, "Error: %s\n", message);
    abort();       // terminates process — never falls through to case 0
    return(1);
}
```

The fall-through to `case 0` is therefore dead code. THRUME in phase 2 is a hard invariant violation — it aborts the backend, not a silent no-op.

---

### Summary

| What happens | Effect on bottom crum count |
|---|---|
| `origin` cuts through a bottom crum | +1 (right fragment created via `adopt(new, RIGHTBRO, ptr)`) |
| `origin+width` cuts through a (different) bottom crum | +1 |
| One bottom crum spans both `origin` and `origin+width` | +2 (three crums from one) |
| Fully-enclosed crums in the deletion range | −N (disowned and freed) |
| Crums entirely outside the range | 0 |

The surviving left fragment of each sliced crum **always replaces the original in-place** (its `cwid` is shrunk, position unchanged). The right fragment **always creates a new additional node**, inserted as RIGHTBRO via `adopt(new, RIGHTBRO, ptr)` [ndcuts.c:448]. There is no mechanism by which a slice produces only an in-place replacement without also creating a new sibling — that is architecturally impossible given `slicecbcpm`'s design.

---

## Question 13 [gregory]

> Under what exact conditions does `isanextensionnd` coalesce a new POOM entry into an adjacent existing one during COPY — does it require strict I-address contiguity (reach == origin), and does it ever fire for COPY operations or only for sequential character-by-character INSERT?

### Gregory's Answer

## KB Synthesis

## `isanextensionnd` Coalescing: Exact Conditions and COPY Applicability

### The Three Conditions

`isanextensionnd` coalesces a new POOM entry into an existing crum when all three of the following hold simultaneously [ST-INSERT, Finding 0062; PRE-COPY, Finding 0046]:

**1. V-space boundary alignment (pre-filter, from `whereoncrum`)**
The insertion point must equal the existing crum's V-reach: `whereoncrum(crum, origin) == ONMYRIGHTBORDER`. This is checked upstream in `makegappm` — if the condition doesn't hold, `makegappm` returns 0 before `isanextensionnd` is ever called. The extension is strictly rightward; there is no left-extension check. [SS-WHEREONCRUM, Finding 0062]

**2. Strict I-address contiguity**
`new_content.I_origin == existing_crum.I_reach` — the new content's I-address origin must equal exactly the existing crum's I-address reach. This is the condition described at `insertnd.c:293-301`: "reach == origin" in I-space. Any gap in I-address space — even a single address — causes this check to fail. [ST-INSERT, Finding 0062]

**3. Matching `homedoc`**
The new content's native document (the document where those I-addresses were originally allocated) must match the existing crum's `homedoc`. This is the first condition `isanextensionnd` checks. [PRE-COPY, Finding 0046; ST-INSERT, Finding 0062]

### Does It Fire for COPY?

**Yes, explicitly.** COPY and INSERT share the identical call path: `docopy` → `insertpm` → `insertnd` → (optionally) `isanextensionnd`. Finding 0046 in [ST-VCOPY] directly addresses this:

> "When COPY inserts V→I mappings into a POOM, the insertion follows an extension-or-create rule. The function `isanextensionnd()` at `insertnd.c:293-301` checks two conditions..."

The practical behavior differs between INSERT and COPY due to the `homedoc` condition:

| Operation | `homedoc` of new content | When coalescing fires |
|-----------|--------------------------|----------------------|
| INSERT into doc T | T (fresh allocation native to T) | Sequential INSERT into T at contiguous V/I positions, absent any intervening CREATELINK |
| COPY from source S into T | S (I-addresses native to S) | COPY from same source S into T, where T already has a crum with `homedoc=S` whose I-reach equals the new copy's I-origin |

**Key consequence of the `homedoc` condition for COPY:** Two COPY operations from *different* source documents never coalesce with each other, even if V-positions are contiguous. "Crums from different source documents are never merged." [PRE-COPY, Finding 0046]

### What Breaks Coalescing

**CREATELINK** breaks coalescing for subsequent INSERT operations [ST-CRUM-BOUND, Finding 0063]. CREATELINK allocates a link orgl I-address in the granfilade via `createorglingranf`, advancing the granfilade's I-address maximum. The next INSERT's fresh I-addresses start above the link orgl's I-address, creating a gap — so `new.I_origin ≠ existing.I_reach`, and `isanextensionnd` fails. This is observable: INSERT "ABC" → CREATELINK → INSERT "DEF" yields 2 shared span pairs from `compare_versions`, while INSERT "ABC" → INSERT "DEF" yields 1. [INV-MONOTONIC, Finding 0063]

**Non-contiguous source content** in COPY: if the source V-span maps to multiple disjoint I-spans (e.g., content transcluded from multiple documents), the I-spans are non-contiguous, and each becomes a separate crum. [ST-VCOPY, Finding 0037]

**Cross-source COPY:** As noted, COPY from source A followed by COPY from source B cannot coalesce because their `homedoc` fields differ. [PRE-COPY, Finding 0046]

### Summary

`isanextensionnd` fires — for both INSERT and COPY — when:
```
whereoncrum(crum, v_origin) == ONMYRIGHTBORDER   // V-space: at right boundary
∧  new.I_origin == crum.I_reach                   // I-space: strictly contiguous, rightward
∧  new.homedoc  == crum.homedoc                   // Provenance: same native document
```

The check is identical in both cases. The practical difference is that INSERT coalesces with prior *same-document* allocations (broken only by CREATELINK or cursor repositioning), while COPY coalesces only with prior COPY from the *same source document* producing contiguous I-addresses at the same target V-position.

---

## Code Exploration

I have traced every relevant call path. Here is the complete answer.

---

## `isanextensionnd` — Complete Behavioral Analysis

### The function itself

```c
// insertnd.c:301-309
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions, both required:

**Condition 1 — `homedoc` equality** [`insertnd.c:305-306`]: The incoming insertion's `homedoc` must equal the existing bottom crum's stored `c2dinfo.homedoc`, tested with `tumblereq` (an exact tumbler match).

**Condition 2 — strict `dsp` contiguity** [`insertnd.c:307-308`]: `lockeq(reach.dsas, originptr->dsas, dspsize(enftype))` must return TRUE.

`lockeq` [`wisp.c:261-267`] iterates `dspsize(enftype)` tumbler slots and requires exact equality in every slot:
```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize) {
    while (loxize--)
        if (!tumblereq (lock1++, lock2++))
            return(FALSE);
    return(TRUE);
}
```

For a POOM node, `dspsize` covers **both** the V and I dimensions. `reach` is computed by `prologuend` [`retrie.c:334-339`]:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach) {
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

So `reach = offset + ptr->cdsp + ptr->cwid`. The contiguity test is:
> **`reach.dsas[V] == origin.dsas[V]` AND `reach.dsas[I] == origin.dsas[I]`** — simultaneously exact in both dimensions.

This is strict `reach == origin` with no tolerance. `reach < origin` (a gap) fails; `reach > origin` (an overlap) fails.

---

### Call stack — sole call site

`isanextensionnd` is called from exactly one place: `insertcbcnd` [`insertnd.c:242-275`]:

```c
INT insertcbcnd(typecuc *father, typedsp *grasp, typewid *origin, typewid *width,
                type2dbottomcruminfo *infoptr)
{
    for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
        if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {  // line 250
            dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // extend width in-place
            ivemodified (ptr);
            setwispupwards (father,1);
            if(!isfullcrum((typecorecrum*)father)){
                return(setwispupwards(findfather((typecorecrum*)father),1));
            }
            return(FALSE);
        }
    }
    // no match: create new bottom crum
    new = createcrum (0, (INT)father->cenftype);
    ...
}
```

`insertcbcnd` is reached only when `father->height == 1` in `insertmorend` [`insertnd.c:230-231`], which in turn is called from `doinsertnd` [`insertnd.c:195-196`] only when the enfilade is non-empty. When the enfilade is empty, `firstinsertionnd` is called directly and `isanextensionnd` is **never consulted** [`insertnd.c:191-194`].

`insertnd` has exactly two call sites:
- `orglinks.c:130` — `insertpm`
- `spanf1.c:51` — `insertspanf`

---

### Call chains: INSERT and COPY converge at `insertpm`

```
doinsert (do1.c:87)
  → inserttextingranf → inserttextgr     (allocates I-addresses, returns ISPANID ispanset)
  → docopy (do1.c:119)
       → insertpm (do1.c:60)
            → unpacksporgl
            → insertnd → doinsertnd → insertmorend → insertcbcnd → isanextensionnd

docopy (do1.c:45)
  → specset2ispanset (converts VSPECID→ISPANID via vspanset2ispanset)
  → insertpm (do1.c:60)
       → unpacksporgl
       → insertnd → doinsertnd → insertmorend → insertcbcnd → isanextensionnd
```

**`doinsert` calls `docopy` directly** [`do1.c:118-121`]. Both INSERT and COPY reach `isanextensionnd` through the identical code path. There is no branch or flag that distinguishes them at the `insertcbcnd` level.

---

### The `homedoc` value for INSERT vs. COPY

The key difference between the two cases lies in what `homedoc` is set to before reaching `isanextensionnd`. `homedoc` is populated in `unpacksporgl` [`sporgl.c:178-203`] for the `insertpm` path:

```c
int unpacksporgl(...) {
    if (itemid == ISPANID) {
        movetumbler (...stream..., streamptr);
        movetumbler (...width..., widthptr);
        tumblerclear (&infoptr->homedoc);            // homedoc = 0 (zero tumbler)
    } else if (itemid == SPORGLID) {
        movetumbler (...sporglorigin..., streamptr);
        movetumbler (...sporglwidth..., widthptr);
        movetumbler (...sporgladdress..., &infoptr->homedoc);  // homedoc = source doc ISA
    }
}
```

`docopy` produces its `ispanset` via `specset2ispanset` [`do2.c:14-46`], which always outputs **ISPANID** items (it converts VSPECID items to ISPANID via `vspanset2ispanset → permute → span2spanset`). Likewise, `inserttextingranf → inserttextgr` returns an ISPANID ispan.

Therefore, **in every call from `docopy` or `doinsert`**, `unpacksporgl` sees ISPANID and sets `homedoc = 0`. Condition 1 of `isanextensionnd` is satisfied whenever the existing POOM bottom crum also has `c2dinfo.homedoc = 0` — which is always the case for content that was itself inserted via ISPANID items.

For `insertspanf` [`spanf1.c:29-43`], ISPANID items set `homedoc = isaptr` (the destination document's ISA). So the spanfilade coalescing check is symmetric: new and existing crums match if they share the same destination document.

---

### Does `isanextensionnd` fire for COPY?

**Yes — it can fire.** There is nothing in `insertcbcnd` or `isanextensionnd` that gates on whether the caller is INSERT or COPY. The function tests two purely structural conditions: `homedoc` equality and `reach == origin`.

However, the two operations differ in how easily those conditions are satisfied:

**Sequential character-by-character INSERT**: Each appended character arrives with:
- V-address = previous V-reach (contiguous by construction, since the caller advances `vsaptr` by width after each insert)
- I-address = next permascroll slot (contiguous by construction, since `inserttextgr` allocates sequentially [`granf2.c:99-100`])
- `homedoc = 0` in both new insertion and existing crum

All three match naturally. Coalescing fires on every character after the first.

**COPY of a block**: The V-address of the destination is caller-controlled and can be made to equal the V-reach of an existing crum. But the I-addresses come from the source document's permascroll (translated by `vspanset2ispanset`). For Condition 2 to hold, the source I-address must equal the I-reach of the existing POOM crum. This is structurally unusual: it would require that the content being copied happened to have been allocated in I-space immediately after the content already in the destination's POOM — a specific coincidence of I-space layout, not an automatic structural property.

---

### The `makegappm` early-return corroborates this

`makegappm` [`insertnd.c:140-143`] contains a revealing guard:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

"Extensions to bc" = "extensions to the bottom crum." When `origin >= reach` at the V dimension (appending at or past the POOM's right V-edge), `makegappm` skips all cutting and returns immediately. This is the no-cut append path that falls straight through to `doinsertnd → insertmorend → insertcbcnd → isanextensionnd`. The comment explicitly designates this as the "extension" case and it applies to INSERT and COPY identically.

---

### Summary

| Property | Value |
|----------|-------|
| Where called | Only `insertcbcnd` [`insertnd.c:250`] |
| Condition 1 | Exact tumbler equality of `homedoc` in both new insertion and existing crum |
| Condition 2 | `reach == origin` exactly, across **all dsp dimensions** (for POOM: both V and I) |
| Strict contiguity? | **Yes** — `reach == origin`, not `reach <= origin` |
| Fires for INSERT? | **Yes** — naturally, on every appended character |
| Fires for COPY? | **Yes** — but only if the copy destination V-address equals the V-reach of an existing crum **and** the source I-address equals the I-reach of that same crum; this is not structurally guaranteed for typical COPY operations |
| `homedoc` for INSERT | 0 (cleared, from ISPANID via `unpacksporgl`) |
| `homedoc` for COPY (via `docopy → insertpm`) | 0 (cleared, from ISPANID via `specset2ispanset + unpacksporgl`) |
| Distinguishes INSERT from COPY? | **No** — identical code path; the structural coincidence of I-address contiguity is what differs in practice |

---

## Question 14 [gregory]

> When COPY of a source V-span that maps to N non-contiguous I-address ranges in the source POOM is inserted into the target, does the target POOM receive exactly N new bottom crums, or can `vspanset2sporglset` splitting produce more than N entries?

### Gregory's Answer

## KB Synthesis

## Answer: Exactly N sporgls, at most N new crums

**`vspanset2sporglset` produces exactly N sporgls — not more.**

### The conversion path

From [SS-VSPAN-TO-SPORGL] and [ST-LINK-CREATE] (Finding 0037), the chain is:

```
source V-span
  → vspanset2ispanset → permute → span2spanset → retrieverestricted
  → one I-span per contiguous I-region in source POOM
  → inner loop: one sporgl per I-span
```

Each POOM crum maps a contiguous V-range to a contiguous I-range. If the source V-span overlaps N non-contiguous I-address regions, `retrieverestricted` returns exactly N contexts — one per covering crum. The `vspanset2sporglset` inner loop at `sporgl.c:49-58` creates one sporgl per returned I-span. Result: exactly N sporgls.

There is no path by which the sporgl count can exceed the source POOM crum count.

### What the target POOM receives

Each sporgl drives one `insertpm` call, which either:

1. **Extends an existing crum** if `isanextensionnd` succeeds — requires same `homedoc`, and exact V+I contiguity with an existing crum [ST-VCOPY, Finding 0046].
2. **Creates a new crum** otherwise.

The N sporgls **cannot coalesce with each other**: they carry non-contiguous I-addresses, so the I-contiguity condition in `isanextensionnd` fails between any pair of them. Coalescing can only happen between a sporgl and a **pre-existing** crum in the target.

Therefore:
- **Upper bound:** N new crums (general case, no pre-existing adjacent content)
- **Lower bound:** fewer than N, if some sporgls happen to abut pre-existing target content in both V and I dimensions simultaneously

This is confirmed by [ST-COPY] / [SS-DOCISPAN] Finding 0047, which establishes the same proportionality for DOCISPAN entries: `|new_DOCISPAN_entries| = |ispanset(source_content)|` — fragmentation of source I-space determines the count, not byte volume.

### Summary

| Layer | Count |
|---|---|
| Sporgls from `vspanset2sporglset` | Exactly N |
| New DOCISPAN entries in spanf | Exactly N |
| New POOM bottom crums in target | At most N (exactly N absent pre-existing adjacency) |

`vspanset2sporglset` cannot produce more than N entries. The constraint is strict equality at the sporgl stage; the only compression happens later, at `insertpm`'s coalescing check.

---

## Code Exploration

I now have everything needed to trace the complete call chain. Here is the full analysis.

---

## Answer

### The COPY path does not call `vspanset2sporglset`

`docopy` (do1.c:45-65) uses a different V→I conversion function: `specset2ispanset`. The two paths are:

| Operation | V→I function | Then calls |
|---|---|---|
| `docopy` | `specset2ispanset` (do2.c:14) | `insertpm` |
| `docreatelink`/`domakelink` | `specset2sporglset` → `vspanset2sporglset` (sporgl.c:14, 35) | `insertendsetsinorgl` |

---

### Call chain for COPY

**do1.c:53–62** — `docopy` calls:
```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
```

**do2.c:14–46** — `specset2ispanset` iterates over the specset. For each V-spec:
```c
ispansetptr = vspanset2ispanset (taskptr, docorgl,
                ((typevspec *)specset)->vspanset, ispansetptr)
```
The full vspanset for that v-spec is passed in one call.

**orglinks.c:397–401** — `vspanset2ispanset` delegates to `permute`:
```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

**orglinks.c:404–422** — `permute` iterates over every vspan in the restriction set, calling `span2spanset` for each:
```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex, targspansetptr, targindex);
}
return (save);   // pointer to head of ispanset
```

**orglinks.c:425–454** — `span2spanset` calls `retrieverestricted` to find all bottom crums in the source POOM that overlap the given V-span, then for each found context:
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                              restrictionindex, (typespan*)NULL, targindex, NULL);
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                      (typeitemset*)targspansetptr);
}
```

**retrie.c:87–110 / 229–268** — `retrieveinarea` → `findcbcinarea2d` recursively walks the enfilade tree and appends one context per leaf crum that qualifies (`crumqualifies2d`). No context is merged or split here.

**context.c:75–111** — `incontextlistnd` performs a sorted insertion only; it does not merge or split contexts.

**context.c:176–212** — `context2span` converts one context into one span, clipping the I-range to the portion corresponding to the V-query:
```c
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```
One context → one `foundspan`. No splitting.

**orglinks.c:464–537** — `onitemlist` allocates a copy of `foundspan` and appends it to the list. One call → one new list entry.

#### Result of V→I translation

For a single V-span that intersects exactly N bottom crums in the source POOM, the pipeline is:

```
N bottom crums
  → N contexts (findcbcinarea2d, retrie.c:262-264)
  → N context2span calls (orglinks.c:443-444)
  → N onitemlist calls (orglinks.c:444)
  = exactly N I-spans in ispanset
```

There is no path that multiplies or splits this count. Each bottom crum contributes exactly one I-span.

---

### What `insertpm` does with the N I-spans

**orglinks.c:75–134** — `insertpm` loops once per sporgl/I-span item:
```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    // ... set crumorigin, crumwidth ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
}
```

Each of the N iterations calls `insertnd` exactly once. Inside `insertnd` → `insertcbcnd` (insertnd.c:242–275), there are two outcomes:

1. **Extension** — if `isanextensionnd` returns true (`lockeq(reach, origin)` AND `homedoc` matches, insertnd.c:301–309): the existing bottom crum is widened. **Zero new bottom crums.**

2. **New crum** — otherwise: `new = createcrum(0, ...)` creates exactly **one** new bottom crum (insertnd.c:260). `splitcrumupwards` (split.c:16–44) may then split **internal** tree nodes for rebalancing, but those are not bottom crums (`height == 0`); `splitcrumpm`/`splitcrumsp` (split.c:117–128, 95–106) both call `peelcrumoffnd` which creates a new intermediate node and moves existing sons — still no new bottom crums.

---

### What `vspanset2sporglset` does (for the link-creation path)

**sporgl.c:35–65** — the outer loop advances one V-span at a time, calling `vspanset2ispanset` with only the current element:
```c
ispanset = NULL;
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
        // ... fill in sporgladdress, sporglorigin, sporglwidth ...
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

**Important detail:** `vspanset` at each outer-loop iteration is the current node in the linked list, so its `->next` still points forward. That means `permute` (called inside `vspanset2ispanset`) will follow `->next` and process **all remaining vspans in the list**, not just the current one. For a **single** V-span, however, `->next` is NULL, so `permute` processes exactly one span and the double-counting does not apply.

For a single V-span with N non-contiguous I-address ranges:
- `vspanset2ispanset` → `permute` → `span2spanset`: N iterations of the context loop → N I-spans
- Inner `for (; ispanset; ...)` loop: N iterations → N sporgls

---

### Conclusion

**The target POOM receives at most N new bottom crums, and `vspanset2sporglset` produces exactly N entries — not more.**

The counting chain is strict 1-to-1 at every step:

| Step | Function | 1-to-1 mapping |
|---|---|---|
| Source POOM traversal | `findcbcinarea2d` (retrie.c:229) | 1 bottom crum → 1 context |
| Context insertion | `incontextlistnd` (context.c:75) | sorted insert, no merge/split |
| Span extraction | `context2span` (context.c:176) | 1 context → 1 I-span |
| List append | `onitemlist` (orglinks.c:464) | 1 call → 1 list item |
| Sporgl creation | `vspanset2sporglset` inner loop (sporgl.c:49-58) | 1 I-span → 1 sporgl |
| Crum insertion | `insertcbcnd` (insertnd.c:242) | 1 call → 0 or 1 new bottom crum |

The count can only decrease (via the extension path in `isanextensionnd`, insertnd.c:301), never increase. `splitcrumupwards` (split.c:16) affects only internal tree nodes for B-tree rebalancing — it does not create bottom crums.

---

## Question 15 [gregory]

> Since `levelpull` is disabled and trees only grow in height, what is the maximum POOM tree height reachable after a sequence of N INSERT operations given `MAXUCINLOAF=6` — is height bounded by `ceil(log_6(N))`, or can pathological split sequences produce taller trees?

### Gregory's Answer

## KB Synthesis

## POOM Height Bound Analysis

The answer is: height is **O(log(N))** but **not exactly `ceil(log_6(N))`**. Two structural facts from the KB produce a tighter and more nuanced bound, and one introduces a potential for modest additional growth.

---

### Fact 1: Mixed Branching Factors

[SS-ENFILADE-BRANCHING] / [SS-ENFILADE-TREE] (Finding 0060) establish that POOM uses two different limits:

| Level | Limit | Constant |
|-------|-------|----------|
| Height-1 (bottom) | `MAX2DBCINLOAF` | 4 |
| Height > 1 (upper) | `MAXUCINLOAF` | 6 |

The maximum capacity of a height-h POOM tree is therefore `4 × 6^(h-1)`, not `6^h`. The height needed for N bottom crums is:

```
h ≥ ceil(log_6(N/4)) + 1
```

For small N this exceeds `ceil(log_6(N))`. The pure `ceil(log_6(N))` formula only applies if the bottom level also used max=6, which it does not. Contrast with [SS-GRAN-MB-ONE] / [SS-GRAN-BOTTOM-SINGLETON] (Finding 0060), where `MAXBCINLOAF=1` forces `ceil(log_6(N)) + 1`; POOM avoids that degenerate +1 penalty but still cannot reach exactly `ceil(log_6(N))`.

---

### Fact 2: Peel-Off-1 POOM Split

[ST-SPLIT-2D] (Finding 0071) distinguishes the two 2D enfilades:

- **SPAN** — peels the child with the **largest diagonal** (L1-norm): a half-and-half style split
- **POOM** — `splitcrumpm` peels the child with the **largest SPANRANGE displacement only**, yielding a 1-from-N split

When a height-1 POOM node overflows at 5 children, `splitcrumpm` creates:
- Original: 4 children (at max)
- New sibling: **1 child** (far below the `toofewsons` threshold of `< B−1 = 3`)

This is structurally different from a standard B-tree half-split (which would give 2+3 or 3+2).

---

### Fact 3: Rebalancing Postcondition — Weaker Than Strict Minimum

[ST-REBALANCE-2D] / [INV-ENFILADE-OCCUPANCY] (Findings 0071, 0073) give `recombinend`'s postcondition as:

> No pair of children can be merged without exceeding `max_children`

For the (4, 1) pair after a peel-off split: combined = 5 > 4 = `MAX2DBCINLOAF`, so `ishouldbother` returns FALSE — **no full merge occurs**. Nephew-stealing (`takenephewnd`) redistributes until one or both nodes is no longer underfull, but if the only donor is the node at capacity (4 children), stealing 2 leaves the donor at 2 < 3 = `min`. [INV-ENFILADE-OCCUPANCY] lists height-1 POOM nodes as underfull at 1..`B−2` = 1..2, so minimum enforced is 3 — but two siblings of 4+1 cannot both satisfy that minimum simultaneously (4+1=5, max is 4).

The result: the `recombinend` postcondition ("no feasible pairwise merge") **does not guarantee all nodes meet minimum occupancy**. Some height-1 POOM nodes may legitimately hold fewer than 3 bottom crums after rebalancing.

---

### Implication for Height

Height increases only when the fullcrum overflows (> 6 children for height ≥ 2), triggering `levelpush` [SS-ENFILADE-TREE] (Finding 0058). Each non-root split adds 1 child to the parent. The fullcrum needs 7 children before `levelpush` fires; this requires at least 7 independent splits cascading up from lower levels.

Because `splitcrumpm` creates 1-child siblings that may not be fully rebalanced, the minimum number of bottom crums that must exist before the fullcrum overflows can be lower than in a balanced B-tree. If height-1 nodes can stably hold as few as 1 bottom crum (permitted by the rebalancing postcondition), the minimum capacity of a height-h tree degrades toward:

```
min_cap(h) ≈ 1 × 6^(h−2)   (if pairs are (4,1) at every level)
```

rather than the standard `(B_min/2)^h` guarantee. Solving `6^(h-2) ≥ N` gives `h ≤ log_6(N) + 2`, so height remains **O(log_6(N))** — the asymptotic class does not change.

---

### Summary

| Question | Answer |
|----------|--------|
| Is height bounded by `ceil(log_6(N))`? | **No** — exact formula is `≈ ceil(log_6(N/4)) + 1` due to mixed branching |
| Can pathological splits produce taller trees? | **Yes, by a constant** — peel-off-1 split + weaker rebalancing guarantee can leave underfull nodes, slightly raising height above the mixed-factor bound |
| Is height super-logarithmic? | **No** — height remains O(log_6(N)) because `levelpush` still requires the root to reach 7+ children, providing a 6× capacity multiplier per level |

The disabled `levelpull` [INV-ENFILADE-MINIMALITY] (Finding 0058) does not affect INSERT-only sequences, since height never spontaneously decreases. The relevant sources are [SS-ENFILADE-BRANCHING], [SS-ENFILADE-TREE], [ST-SPLIT-2D], [ST-REBALANCE-2D], [INV-ENFILADE-OCCUPANCY], [SS-GRAN-BOTTOM-SINGLETON], and [ST-INSERT] (Finding 0060).

---

## Code Exploration

I have all the source evidence needed. Here is the complete analysis.

---

## POOM Tree Height Bound After N INSERT Operations

**Short answer: Height is bounded by Θ(log₆(N)). The peel-one split does not produce pathologically taller trees than ⌈log₆(N)⌉ — it stays within a small additive constant of that value.**

---

### 1. The Constants

**`enf.h:26-28`:**
```c
#define MAXUCINLOAF     6     /* max children for height > 1 nodes */
#define MAX2DBCINLOAF   4     /* max bottom crums for height-1 nodes (2D, i.e. POOM/SPAN) */
#define MAXBCINLOAF     1     /* max bottom crums for height-1 nodes (GRAN only) */
```

The overflow predicates (`genf.c:244`):
```c
return (ptr->numberofsons > (ptr->height > 1 ? MAXUCINLOAF
                                              : (is2dcrum(ptr) ? MAX2DBCINLOAF : MAXBCINLOAF)));
```

So for the POOM enfilade:
- **height-1 nodes** (direct parents of bottom crums): overflow at `numberofsons > 4`
- **height ≥ 2 nodes** (including root): overflow at `numberofsons > 6`

---

### 2. `levelpull` Is Completely Disabled

**`genf.c:318-342`:**
```c
int levelpull(typecuc *fullcrumptr)
{
    return(0);   /* ← returns immediately; body is 100% commented-out */
/*
    if (!isfullcrum (fullcrumptr))  ...
    if (fullcrumptr->numberofsons > 1)   return;
    fullcrumptr->height--;
    ...
*/
}
```

`levelpull` is called in two places — `recombineseq` (`recombine.c:67`) and `recombinend` (`recombine.c:130`) — but both calls silently become no-ops. **Trees only ever grow in height.** This is the foundational premise of the question.

---

### 3. The Split Strategy: Peel One Child Off

When a POOM node overflows, the cascade in `splitcrumupwards` (`split.c:16-44`) fires:

```c
for (; toomanysons(father); father = (typecuc *)findfather((typecorecrum*)father)) {
    if (isfullcrum((typecorecrum*)father)) {
        levelpush(father);                          // root: height++
        splitcrum((typecuc*)findleftson(father));   // then split new child
        return(TRUE);
    }
    splitcrum(father);    // non-root: just split
    splitsomething = TRUE;
}
```

For a non-fullcrum POOM node, `splitcrum` → `splitcrumpm` (`split.c:117-128`):

```c
int splitcrumpm(typecuc *father)
{
    for(correctone=ptr=findleftson(father); ptr; ptr = findrightbro(ptr)) {
        if (tumblercmp(&ptr->cdsp.dsas[SPANRANGE],
                       &correctone->cdsp.dsas[SPANRANGE]) == GREATER)
            correctone = ptr;
    }
    peelcrumoffnd(correctone);   /* ← peel ONE child off, not half */
}
```

`peelcrumoffnd` (`split.c:130-169`) does:
1. `disown(ptr)` — remove ptr from its current parent (which had n+1 children)
2. `new = createcrum(father->height, ...)` — new sibling at the same level
3. `adopt(new, RIGHTBRO, father)` — new node is right sibling of original parent
4. `adopt(ptr, LEFTMOSTSON, new)` — new node has exactly 1 child (ptr)

**Result**: original node: n children → n−1 children; new sibling: 1 child.

This is **not** a balanced split. A standard B-tree splits evenly (≈k/2 each side); the POOM split leaves the overflowing node with `MAXUCINLOAF = 6` children and gives the new sibling just **1**. Minimum occupancy of any non-root node = 1.

---

### 4. `levelpush`: The Only Height Increment

**`genf.c:263-294`:**
```c
int levelpush(typecuc *fullcrumptr)
{
    new = createcrum((INT)fullcrumptr->height, (INT)fullcrumptr->cenftype);
    new->isleftmost = TRUE;
    transferloaf(fullcrumptr, new);          // move all children to new
    fullcrumptr->height++;                   // root grows one taller
    adopt((typecorecrum*)new, SON, (typecorecrum*)fullcrumptr);
    ...
}
```

After `levelpush`, root has height h+1 and exactly 1 child (the old-root contents). Then `splitcrumupwards` immediately calls `splitcrum` on that child, which peels one grandchild off into a new sibling. After the dust settles, root has **exactly 2 children** every time height increases.

---

### 5. Exact Height Bound: Derivation

**Define:** `f_h` = minimum bc insertions required to cause one split of an h-level node, starting from its seed state (1 child, 1 bc).

**At h = 1** (height-1 node, direct parent of bottom crums):
- Seed state: 1 bc
- Overflow fires at > 4 bc → need 4 more bc
- **`f_1 = 4`**

**At h ≥ 2** (internal node):
- Seed state: 1 child (1 bc)
- Overflow fires at > 6 children → need 6 more split events at level h−1
- Each sub-split requires `f_{h-1}` inserts (starting from the freshly-peeled 1-child seed)
- **`f_h = 6 × f_{h-1} = 4 × 6^{h-1}`**

**Define:** `T_h` = minimum total bc insertions to trigger the h-th `levelpush` (tree grows from height h to h+1).

After the (h−1)-th levelpush: root has 2 children of height h−1. Root overflows when it reaches 7 children → needs 5 more h−1-level splits, each requiring `f_{h-1}` inserts:

```
T_1 = 5        (height-1 root overflows at 5 bc, i.e. > MAX2DBCINLOAF=4)
T_h = T_{h-1} + 5 × f_{h-1}   for h ≥ 2
    = T_{h-1} + 5 × 4 × 6^{h-2}
    = T_{h-1} + 20 × 6^{h-2}
```

Solving the recurrence:

```
T_h = 1 + 4 × 6^{h-1}
```

**Verification:**

| h | T_h formula     | Value |
|---|-----------------|-------|
| 1 | 1 + 4×6⁰ = 1+4  | 5     |
| 2 | 1 + 4×6¹ = 1+24 | 25    |
| 3 | 1 + 4×6² = 1+144| 145   |
| 4 | 1 + 4×6³ = 1+864| 865   |
| 5 | 1 + 4×6⁴        | 5185  |

**Height after N inserts:**

Tree height is H where H−1 is the largest integer such that `T_{H-1} ≤ N`:

```
T_{H-1} = 1 + 4 × 6^{H-2} ≤ N
4 × 6^{H-2} ≤ N − 1
H ≤ 2 + floor(log₆((N−1)/4))
```

For large N this is approximately:
```
H ≤ log₆(N) + 2 − log₆(4) ≈ log₆(N) + 1.23
```

That is, **height ≤ ⌈log₆(N)⌉ + 1** in practice.

---

### 6. Does the Peel Strategy Create Pathological Heights?

No. Here is why intuitively: even though the peel split leaves a minimum occupancy of 1 (not 3, as in a standard B-tree), the **overflow threshold** that governs when `levelpush` fires is still `> MAXUCINLOAF = 6`. The rate of height growth is entirely determined by how many inserts are needed to overflow the root 7 times — and that is dictated by the overflow threshold, not the minimum fill.

Comparison:

| Strategy | Min fill | Overflow threshold | Height bound |
|----------|----------|--------------------|--------------|
| Standard B-tree (max k=6) | k/2 = 3 | > 6 | log₃(N) + O(1) ≈ 2·log₆(N) |
| POOM peel (max k=6)       | 1        | > 6 | log₆(N) + O(1) |

Counterintuitively, the peel strategy gives a **better** (lower) height bound than a standard B-tree with the same max fanout, because all splits above leaf level always produce trees that eventually fill to 6 children before overflowing — the minimum fill of 1 means nodes hold *less* than a balanced tree (more space wasted), but the root still needs 7 children before height grows.

A "pathological split sequence" — one that always inserts into the freshly-peeled 1-bc seed node — achieves **exactly** the `T_h = 1 + 4×6^{h-1}` lower bound, which is already logarithmic. There is no adversarial insert sequence that breaks the `O(log₆(N))` bound, because `levelpush` requires root overflow regardless of the subtree shape.

---

### 7. `recombine` Cannot Decrease Height

`recombinend` (`recombine.c:104-131`) steals children from sibling subtrees (via `takeovernephewsnd`/`eatbrossubtreend`) and, at the root, calls `levelpull`:

```c
if (father->isapex)
    levelpull(father);   /* genf.c:318: return(0); — no-op */
```

Recombination can compact fragmented subtrees and *slow* height growth (by preventing future overflows), but it can never decrease height. Once height reaches H, it stays at H or grows further.

---

### Final Answer

**The maximum POOM tree height after N INSERT operations is bounded by `⌈log₆(N)⌉ + O(1)`.** Specifically:

```
H(N) ≤ 2 + floor(log₆((N−1)/4))   ≈   log₆(N) + 1.23
```

The closed-form minimum for the h-th `levelpush` is `T_h = 1 + 4×6^{h-1}` (derived from `MAXUCINLOAF=6`, `MAX2DBCINLOAF=4`, and the peel-one split semantics of `splitcrumpm`/`peelcrumoffnd`).

**Pathological split sequences cannot produce taller trees.** The asymmetric "peel one" split (`split.c:127`, `split.c:130-169`) creates lopsided trees (minimum fill = 1), but since `levelpush` fires only when the root itself exceeds `MAXUCINLOAF=6` children (`genf.c:244`), the height is inescapably bounded by `log₆` of the bottom-crum count. The naive bound `⌈log₆(N)⌉` is essentially correct; the actual bound is that value plus at most 1–2.

---

## Question 16 [gregory]

> After a cycle of INSERT followed by DELETE of the same span repeated K times at the same V-position, how many POOM bottom crums remain compared to the initial state — does each cycle leave residual tree structure or fragment existing entries?

### Gregory's Answer

## KB Synthesis

## POOM Bottom Crum Count After K INSERT/DELETE Cycles

**Short answer:**

| K | Bottom crums | Net delta from K=0 |
|---|-------------|-------------------|
| 0 | 1 | — |
| 1 | 2 | +1 (permanent) |
| ≥2 | 2 | 0 (stable) |

The first cycle leaves a permanent residual split. All subsequent cycles are neutral. The tree does not accumulate structure beyond the first cycle.

---

### Cycle 1: INSERT at interior position P

Assume the document starts with one bottom crum covering the full V-span, say `[1.1, 1.n)`. Inserting at position P where `1.1 < P < 1.n` places P strictly inside that crum — `whereoncrum()` returns **THRUME** `[SS-WHEREONCRUM]`.

`makegappm` constructs a two-blade knife `[blade[0], blade[1])` where `blade[1] = (N+1).1` (the next subspace boundary). `slicecbcpm` is invoked because the cut point is THRUME — it splits the original crum into:

- Left fragment: `[1.1, P)` (original content, unshifted)
- Right fragment: `[P+W, 1.n+W)` (original content, shifted up by W)

A new bottom crum `[P, P+W)` is created for the inserted content, assigned fresh I-addresses from the current allocation ceiling `[INV-MONOTONIC]`.

**After Cycle 1 INSERT: 3 bottom crums (+2 from initial)** `[ST-INSERT Finding 0062]`.

### Cycle 1: DELETE of span `[P, P+W)`

The deletion range is `[P, P+W)` — exactly the inserted crum. Check the boundaries:

- Left boundary P falls on the **left edge** of the inserted crum → ONMYLEFTBORDER, not THRUME
- Right boundary P+W falls on the **right edge** of the inserted crum → ONMYRIGHTBORDER, not THRUME

Because neither boundary is THRUME, `slicecbcpm` is **not** invoked in Phase 1 `[PRE-DELETE Finding 0075]`. The inserted crum lies entirely within `[P, P+W)` → Case 1 in `deletend`: it is disowned and freed via `subtreefree`.

The right fragment `[P+W, 1.n+W)` shifts left by W, becoming `[P, 1.n)`.

**After Cycle 1 DELETE: 2 bottom crums (+1 net from initial)**.

The permanent residual: the original single crum was split into two fragments — `[1.1, P)` and `[P, 1.n)` — and those two fragments are never reunited. `isanextensionnd` cannot coalesce them because their I-addresses are non-contiguous: the left fragment covers `[i₁, i_P)` and the right covers `[i_{P+W}, i_n+W)`, with a gap of size W in the I-space `[INV-NO-IADDR-REUSE]`.

### Cycles 2+: INSERT at P

Now P sits at the boundary between crum₁ `[1.1, P)` and crum₂ `[P, 1.n)`. `whereoncrum()` for crum₁ returns **ONMYRIGHTBORDER** (P equals crum₁'s reach) `[SS-WHEREONCRUM]`.

`makegappm` hits the early-exit path: when the insertion point ≥ the reach of the current crum, no knife is constructed and `slicecbcpm` is **not** called `[ST-INSERT Finding 0062]`. No split occurs.

`isanextensionnd` is tested: could the new content extend crum₁ in-place? No — the new I-addresses are allocated above all prior allocations `[INV-MONOTONIC]` and are therefore not contiguous with crum₁'s I-range. A new bottom crum is created for the inserted content.

Crum₂ shifts right by W.

**After Cycle K≥2 INSERT: 3 bottom crums (+1 from the stable 2-crum state)**.

### Cycles 2+: DELETE of `[P, P+W)`

Identical boundary-aligned Case 1 removal as Cycle 1. New crum freed, crum₂ shifts back.

**After Cycle K≥2 DELETE: 2 bottom crums (stable)**.

### Why the two fragments never merge

The rebalancer (`toofewsons` + `levelpull`) could in principle reduce crum count, but:

1. **levelpull is disabled** — tree height never decreases `[INV-ENFILADE-MINIMALITY Finding 0058]` `[ST-DELETE Finding 0058]`.
2. **Rebalancing acts on internal nodes**, not bottom crums directly. Merging bottom crums would require stealing nephews from a sibling parent — which requires a sibling with excess children (sons ≥ B = `MAX2DBCINLOAF` = 4). A minimal two-crum POOM has no such siblings `[INV-ENFILADE-OCCUPANCY Finding 0070]` `[ST-REBALANCE-2D Finding 0071, 0073]`.
3. **I-addresses are not reused** — even if the tree structure could be merged, the I-gap `[i_P, i_{P+W})` between the two fragments means they cannot be represented as a single contiguous crum `[INV-NO-IADDR-REUSE]`.

This is a direct expression of `[INV-DELETE-NOT-INVERSE]`: DELETE+INSERT does not restore the original state. The I-addresses consumed by the first INSERT are permanently consumed; all subsequent INSERT calls draw from above the allocation ceiling.

### Summary

- **Each cycle does not accumulate residual structure** beyond K=1.
- **The first cycle is the only structurally destructive one**: it splits the original crum irreversibly.
- **Cycles 2 through K are perfectly symmetric**: +1 on INSERT (no split, just append), −1 on DELETE (boundary-aligned Case 1 removal), net 0.
- The POOM reaches a **fixed point of 2 bottom crums** after the first complete cycle and remains there for all K≥1.

---

## Code Exploration

I now have all the information I need from the code. Let me compile the complete analysis.

---

## Answer: POOM Bottom Crum Accumulation After K INSERT+DELETE Cycles

### The Code Path

**INSERT** (`doinsert` [do1.c:87]):
```
doinsert → docopy [do1.c:119] → insertpm [orglinks.c:75]
         → insertnd [insertnd.c:15] → makegappm [insertnd.c:54]
                                    → doinsertnd [insertnd.c:185]
         → recombine [insertnd.c:76]
```

**DELETE** (`dodeletevspan` [do1.c:158]):
```
dodeletevspan → deletevspanpm [orglinks.c:145]
             → deletend [edit.c:31] → makecutsnd + deletecutsectionnd
             → setwispupwards + recombine [edit.c:74-75]
```

---

### Mechanism 1: `makegappm` Splits Existing Crums (INSERT)

`makegappm` [insertnd.c:124] is called before each insert. It runs `makecutsnd` [ndcuts.c:15] with two knife-blades at the insert V-position:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
makecutsnd (fullcrumptr, &knives);   // [insertnd.c:148]
```

Inside `makecutsnd` → `makecutsbackuptohere` [ndcuts.c:69], when a bottom crum spans the cut point (returns `THRUME`):

```c
if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
    new = (typecuc *)createcrum((INT)ptr->height,(INT)ptr->cenftype);  // new crum!
    slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
    // [ndcuts.c:80-85]
```

`slicecbcpm` [ndcuts.c:373] **physically splits one bottom crum into two** — left half and right half at the cut point — setting their widths and dsps correctly, then calling `adopt(new, RIGHTBRO, ptr)` [ndcuts.c:448]. This adds one new POOM bottom crum.

**Guard clause** [insertnd.c:140–143]: `makegappm` returns early without cutting if the document is empty (`iszerotumbler(&fullcrumptr->cwid.dsas[V])`). This means the first insert into a virgin document skips all this.

### Mechanism 2: DELETE Permanently Frees Crums

`deletend` [edit.c:47–72] loops over children and frees those inside the delete range:

```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);   // [edit.c:59-61]
    break;
```

`subtreefree` [credel.c:413] calls `freecrum` → `efree` — the memory is returned to the allocator. The crum is gone.

### Mechanism 3: `recombine` and `levelpull` Are Both No-Ops Here

This is the critical finding. After DELETE, `recombine(father)` is called:

```c
int recombinend(typecuc *father)
{
    if (father->height < 2  || !father->modified)
        return(0);   // [recombine.c:112] — exits immediately for height-1 POOM
```

For any POOM with fewer than `MAX2DBCINLOAF` bottom crums, height stays at 1. `recombinend` **does nothing**.

And `levelpull` [genf.c:318–342] is **permanently disabled** — the entire function body is commented out:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (!isfullcrum (fullcrumptr))  ...
    if (fullcrumptr->numberofsons > 1) return;
    ...
    freecrum (ptr);
*/
}
```

Even if `recombinend` ran and found one surviving node, `levelpull` would not collapse the tree height. The tree **can only grow**, never shrink.

---

### Tracing K Cycles at the Same Interior Position P

**Initial state**: 1 bottom crum covering V=[`vsa`, `vsa+W`).

**Cycle 1 — INSERT at V=P (where `vsa` < P < `vsa+W`):**

1. `makegappm` calls `makecutsnd` with blade[0]=P, blade[1]=P' (`findaddressofsecondcutforinsert(P)`)
2. The existing crum spans P → `THRUME` → `slicecbcpm` fires → original 1 crum **split into 2**: left=[`vsa`, P), right=[P, `vsa+W`)
3. `insertcbcnd` [insertnd.c:242] creates a **3rd bottom crum** for the new content at V=[P, P+w)
4. After INSERT: **3 bottom crums** total.

**Cycle 1 — DELETE of [P, P+w):**

1. `deletend` → `deletecutsectionnd` classifies the new-content crum (entirely inside delete span → case 1) → `disown + subtreefree` → **new crum freed**
2. The right half's DSP is adjusted (case 2: subtract width): right half slides back to [P, `vsa+W`)
3. `recombine(father)` → `recombinend`: height = 1 < 2 → **immediate return, no merge**
4. After DELETE: **2 bottom crums** remain: [`vsa`, P) and [P, `vsa+W`)

**This 2-crum split is permanent.** The original 1 crum is now permanently 2 crums.

**Cycles 2, 3, … K — INSERT at V=P again:**

The crum boundaries are now aligned at P. Whether blade[1] (`findaddressofsecondcutforinsert(P)`) falls inside the right crum (which now starts exactly at P) depends on tumbler arithmetic. Since `findaddressofsecondcutforinsert` computes a sub-level address ("P at a finer precision"), it may be strictly greater than P and thus fall inside the right crum → another `slicecbcpm` on each cycle.

Regardless, after each DELETE `recombinend` remains a no-op for height < 2, so every split from every cycle is permanent.

**Special case — Empty document (V-width = 0):**

`makegappm` guard [insertnd.c:140–143]:
```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this is for extensions to bc without calling cut */
```

Width is zero → guard fires → `makegappm` returns immediately. Then `doinsertnd` detects `isemptyenfilade` [genf.c:97–116] → `firstinsertionnd` [insertnd.c:199] creates/reuses the single bottom crum. After DELETE the crum is freed. **No accumulation** for empty-document cycles.

---

### Quantitative Answer

| Scenario | After K Cycles | Bottom Crum Count |
|---|---|---|
| Empty document (insert-delete at 1.1) | any K | 0 (clean, no accumulation) |
| Non-empty doc, interior position P, K=0 | — | N (initial) |
| Non-empty doc, interior position P, K=1 | after delete | **N+1** (permanent split at P) |
| Non-empty doc, interior position P, K≥2 | after each delete | **≥ N+1** (possibly N+K if blade[1] re-slices) |

**The definitive answer**: Each INSERT+DELETE cycle at an interior position leaves **at least one additional residual POOM bottom crum** compared to the initial state, created by `slicecbcpm` during `makegappm`'s `makecutsnd` call. This split is **never reversed** because:

1. `recombinend` [recombine.c:112] exits immediately for `height < 2` — the normal case for small documents
2. `levelpull` [genf.c:318] is a permanent stub — `return(0)` — the tree height never decreases

Each cycle produces at minimum one `slicecbcpm` call if the existing crum still spans the cut point. After cycle 1 splits the original crum, subsequent cycles depend on whether `findaddressofsecondcutforinsert`'s blade[1] falls inside the new right half. If it does (likely, since it computes a sub-level address strictly greater than P), each cycle adds yet another micro-split. If blade[1] consistently lands on the right crum's boundary, the structure stabilizes at 2 crums after cycle 1.

**The structural invariant is monotonic**: POOM crum count can only grow or stay the same across INSERT+DELETE cycles at the same interior position. Recombine never fires at the relevant tree height, and levelpull is disabled entirely.

---

## Question 17 [gregory]

> Is there any mechanism in udanax-green — explicit or implicit — that compacts or defragments a POOM, merging adjacent bottom crums that happen to have contiguous I-addresses back into a single entry?

### Gregory's Answer

## KB Synthesis

## No Defragmentation Mechanism Exists

The KB documents no mechanism — explicit or implicit — that retroactively merges adjacent bottom crums with contiguous I-addresses back into a single entry.

### What Does Exist: Proactive Coalescing at Insertion Time

The closest mechanism is `isanextensionnd` [ST-INSERT, ST-CRUM-BOUND], invoked during every `insertnd` call. It checks two conditions:

1. The new content's `homedoc` matches the existing crum's homedoc
2. The new content's I-origin equals the existing crum's I-reach (contiguous at the boundary)

When both hold, the existing crum's width is extended in place rather than creating a new crum. This is why 100 sequential single-character inserts produce a single contiguous span [INV-VSPAN-CONSOLIDATION] — the fragmentation is prevented at insertion time, not compacted afterward.

**This is a forward-only, at-insertion-time check, not a compaction pass.** It asks "should I merge this *new* content with an existing crum?" not "should I merge two *existing* adjacent crums?"

### What the Rebalancing Machinery Does Not Do

The `recombinend` function [ST-REBALANCE-2D] merges B-tree *nodes* (internal tree structure) when their combined occupancy fits within the branching limit. It operates by examining `numberofsons` counts and uses `shellsort` diagonal ordering — it never inspects whether two bottom crums have contiguous I-addresses. It moves whole subtrees between parent nodes; the bottom crums inside those subtrees remain structurally unchanged as separate entries.

### The Fragmentation Case

When INSERT cuts a crum with a knife at an interior V-position [SS-TWO-BLADE-KNIFE, PRE-DELETE Finding 0075], `slicecbcpm` produces two crums whose I-ranges abut at the cut point. After the insertion places content between them:

```
Left crum:    V [v1, cut),        I [i1, i_mid)
New content:  V [cut, cut+width), I [i_new...] — fresh I-addresses
Right crum:   V [cut+width, v2),  I [i_mid, i2)
```

The left and right crums retain contiguous I-addresses. If the inserted content is later deleted, those two crums are still separate bottom crums with contiguous I-ranges — and nothing merges them.

### Why No Compaction Exists

This is consistent with the general pattern of irreversible growth in the codebase:

- `levelpull` (which would reduce tree height after underoccupancy) is **disabled** [INV-ENFILADE-MINIMALITY, SS-ENFILADE-TREE Finding 0058] — the tree never shrinks in height
- The granfilade is append-only [FC-GRANF-ON-DELETE]; DELETE frees POOM nodes but doesn't compact I-space
- [EC-EMPTY-DOC] Finding 0058 shows that after delete-everything, the tree retains its prior height with empty intermediate nodes — structural cleanup is incomplete even at the B-tree level, let alone at the bottom-crum content level

The INV-VSPAN-CONSOLIDATION invariant observed in golden tests is achieved entirely through `isanextensionnd`'s prevention of fragmentation during sequential typing — not through any post-hoc merging. A document that has been fragmented by interior edits and then had the interior content deleted will retain the fragmented crum structure permanently.

---

## Code Exploration

I now have enough information to give a complete, sourced answer.

---

## Is there a POOM compaction/defragmentation mechanism in udanax-green?

**Short answer: No.** There is no mechanism — explicit or implicit — that scans existing POOM bottom crums for I-address contiguity and merges them. The only bottom-crum merging that occurs is an opportunistic extension check at insertion time, and it is far narrower than "I-adjacent."

---

### 1. What a POOM bottom crum encodes

A POOM bottom crum (`type2dcbc`, defined in `backend/enf.h:109-131`) is a **rectangle in 2D (I, V) space**. Its fields are:

- `cdsp.dsas[I]` — displacement in I-address (permascroll) space [`wisp.h:19`]
- `cdsp.dsas[V]` — displacement in V-address (virtual/version) space [`wisp.h:20`]
- `cwid.dsas[I]` — width in I-space
- `cwid.dsas[V]` — width in V-space
- `c2dinfo.homedoc` — the source document ISA [`wisp.h:107-109`]:
  ```c
  typedef struct struct2dbottomcruminfo {
      tumbler homedoc;
  } type2dbottomcruminfo;
  ```

The crum says: "at V-positions [grasp.V, grasp.V + wid.V), the content originates from I-positions [grasp.I, grasp.I + wid.I) in document `homedoc`."

---

### 2. The only bottom-crum merging: `isanextensionnd()` — insertion time only

In `backend/insertnd.c:249-258`, during fresh insertion, `insertcbcnd()` checks whether the new content is a direct extension of an existing bottom crum:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified (ptr);
        ...
        return(FALSE);
    }
}
```

`isanextensionnd()` [`insertnd.c:301-309`] fires only when **all three** conditions hold simultaneously:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

1. `homedoc` matches (same source document)
2. The existing crum's **reach** (absolute end in both dimensions) equals the new insertion's **origin** — checked via `lockeq(reach.dsas, originptr->dsas, dspsize(POOM))`, which compares **both** I and V tumblers simultaneously [`wisp.h:60-61`]

If all three hold, the existing crum's `cwid` is widened rather than creating a new crum. This is purely an opportunistic optimization at the moment of insertion — **not a retrospective compaction pass**.

---

### 3. `recombinend()` — merges internal nodes only, never bottom crums

`backend/recombine.c:22-34` dispatches POOM recombination to `recombinend()`:

```c
int recombine(typecuc *father)
{
    switch (father->cenftype) {
        ...
        case POOM:
            recombinend (father);
    }
}
```

But `recombinend()` [`recombine.c:104-131`] immediately bails for anything near the leaves:

```c
int recombinend(typecuc *father)
{
    if (father->height < 2 || !father->modified)
        return(0);
    ...
    takeovernephewsnd (&sons[i], &sons[j]);
```

The `height < 2` guard ensures it only operates on nodes **two or more levels above bottom crums**. It merges height-2+ **internal nodes** by redistributing their children between siblings — the bottom crums themselves are moved as atomic units and are never inspected for I-address adjacency or merged with each other.

The `ishouldbother()` predicate [`recombine.c:150-163`] that gates whether to merge two nodes also makes no reference to I-address content:

```c
bool ishouldbother(typecuc *dest, typecuc *src)
{
    ...
    return (dest->numberofsons + src->numberofsons <= (dest->height>1 ? MAXUCINLOAF : MAX2DBCINLOAF)
            && randomness(.3));
}
```

It only checks son-count capacity, not address contiguity.

---

### 4. `levelpull()` — dead code

`backend/genf.c:318-342` is the one function that might have reduced tree height when the apex had a single child:

```c
int levelpull(typecuc *fullcrumptr)
{
    return(0);            /* line 321 — returns immediately */
    /*
     ... commented-out code for height reduction ...
    */
}
```

It is called in `recombinend()` and `recombineseq()` but does nothing. Even if active, it would only collapse a single-child apex downward — it would not merge bottom crums.

---

### 5. The grep confirms: no compaction language exists

A search for `contiguous`, `adjacent`, `merge`, `compact`, `defrag`, `coalesce` across all `backend/*.c` files returns **no matches**. The concept does not appear in the codebase.

---

### 6. Why merging would generally be impossible anyway

Even if such logic existed, merging two POOM bottom crums requires them to be adjacent in **both** I and V simultaneously, with the same `homedoc`. After typical operations:

- **Delete** (`edit.c:31-76`, `deletend()`): adjusts V-displacements of crums to the right of the deleted span. Two crums that were separated by deleted content become V-adjacent in the POOM, but nothing checks them for I-adjacency afterward.

- **Copy/transclusion** (`do1.c:45-65`, `docopy()`): inserts content at a chosen V-address with its I-span from the source. This produces a new crum whose V-position is determined by the caller, deliberately independent of any existing I-adjacent crum.

- **Rearrange** (`edit.c:78-160`, `rearrangend()`): shifts V-displacements of cut sections to implement move. The POOM ends up with crums whose V-order no longer matches I-order; I-adjacent crums may end up at arbitrary V-positions.

In all cases, the residual crums may share I-address contiguity with neighbors, but the code never looks for this.

---

### Conclusion

udanax-green contains **no compaction or defragmentation mechanism** for POOM bottom crums. The bottom-crum count grows monotonically with operations and is never retrospectively reduced by merging I-adjacent entries. The sole merging optimization — `isanextensionnd()` in `insertnd.c:301` — applies only at the moment of a fresh insertion, and only when the new content is contiguous with an existing crum in **both** I and V space simultaneously. Existing fragmented crums accumulate indefinitely.

---

## Question 18 [gregory]

> The spanfilade receives one DOCISPAN entry per contiguous I-span per INSERT and per COPY — after N operations each producing M I-spans, is the spanfilade entry count exactly the cumulative sum of spans across all operations, with no deduplication or merging of overlapping entries?

### Gregory's Answer

## KB Synthesis

## Spanfilade DOCISPAN Entry Count: Cumulative Sum With No Cross-Operation Deduplication

The short answer is **yes for the cumulative sum, yes for no deduplication** — with one important precision about what "per operation" means.

---

### Within a Single Operation: One Entry Per Contiguous I-Span

[SS-DOCISPAN] Finding 0047 establishes the within-operation granularity precisely: `insertspanf` iterates the `ispanset` linked list and makes **one `insertnd` call per `typeispan` struct**. A `typeispan` represents a contiguous I-address range (start + width). Therefore:

- INSERT of k contiguous bytes → 1 I-span → **1 DOCISPAN entry**
- COPY of fragmented source (3 non-contiguous I-span regions) → **3 DOCISPAN entries**

The consolidation happens upstream, in `vspanset2ispanset` / `specset2ispanset`, which packages the entire content placement into the fewest possible contiguous I-spans before they reach `insertspanf`. The spanfilade itself sees only the consolidated spans.

---

### Across Operations: Cumulative Sum, No Deduplication or Merging

[INV-SPANF-WRITE-ONLY] (Findings 0057, 0067) establishes that the spanfilade is **strictly append-only**. Inspection of `spanf1.c` and `spanf2.c` reveals no `deletespanf`, `removespanf`, or any removal mechanism. The set of entries is monotonically non-decreasing:

> `∀ t₁ < t₂ : spanf_entries(t₁) ⊆ spanf_entries(t₂)`

[INV-SPANF-GROWTH] states the growth model directly as an equality:

> `S(t) = Σ |ispanset placed into doc d|` across all INSERT and COPY operations up to time t

This `=` (not `≤`) reflects the absence of cross-operation merging. Each operation's I-spans are appended independently.

There is no deduplication for overlapping I-address ranges. [PRE-COPY] confirms: "The COPY operation performs NO duplicate checking before inserting V→I mappings." The same absence of duplicate-checking extends to `insertspanf` — COPY of the same I-addresses multiple times creates multiple DOCISPAN entries pointing the same document to the same I-addresses. [EC-STALE-SPANF-REFERENCE] is a direct consequence of this: after DELETE removes a POOM mapping, the corresponding DOCISPAN entry remains, making `FIND_DOCUMENTS` return a superset of documents actually containing the content.

---

### The `isanextensionnd` Question

One might ask whether the `isanextensionnd` mechanism (documented in [ST-VCOPY] Finding 0046 for POOM insertions) could merge DOCISPAN entries across consecutive operations. That function checks: same `homedoc` AND `crum.reach == new_origin` (contiguous I-addresses). Since consecutive INSERTs into the same document produce contiguous I-addresses ([INV-MONOTONIC]), the extension condition would be satisfied.

However:

1. The KB documents `isanextensionnd` exclusively in the POOM context. The SPAN (spanfilade) is a 2D enfilade with two independent dimensions (ORGLRANGE = document ISA, SPANRANGE = I-address), and extension in 2D requires simultaneously satisfying both — a stricter condition.
2. [INV-SPANF-GROWTH] uses the equality formula `S(t) = Σ |ispanset(op)|`, which would fail if cross-operation merging were occurring.
3. The characterization as "proportional to the number of distinct content placements" further implies per-operation accounting.

The KB treats cross-operation merging as not occurring in the spanfilade.

---

### Summary

| Property | Behavior |
|----------|----------|
| Granularity per operation | One entry per contiguous I-span in the operation's `ispanset` |
| Across operations | Pure cumulative sum — `|DOCISPAN_total| = Σ_ops |ispanset(op)|` |
| Deduplication of re-inserted I-addresses | None — same I-address range can appear in multiple entries |
| Removal of stale entries after DELETE | Never — entries persist permanently (see [EC-STALE-SPANF-REFERENCE]) |
| Effect on `FIND_DOCUMENTS` | Returns superset: `actual_docs(i) ⊆ find_documents(i)` |

The entry count is exactly the cumulative sum. There is no deduplication, no merging across operations, and no cleanup. This is not an oversight — it is a structural consequence of the append-only spanfilade design and the permanent-identity model ([INV-IADDRESS-PERMANENT], [INV-SPANF-WRITE-ONLY]).

---

## Code Exploration

Now I have all the pieces I need to give a definitive answer. Let me compile the complete analysis.

---

## Answer

The spanfilade entry count is **not always the cumulative sum** of spans across operations. The `isanextensionnd` mechanism in `insertcbcnd` merges adjacent I-spans from the same document into a single existing crum, producing **fewer entries** than a naïve sum would predict. Here is the full derivation.

---

### 1. Entry path: one `insertnd` call per ispan per operation

Both INSERT and COPY converge on `insertspanf` [`spanf1.c:15`]:

**INSERT** path (`fns.c:84` → `do1.c:87`):
```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)   /* do1.c:119 */
    );
```

**COPY** path (`fns.c:35` → `do1.c:45`):
```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  /* do1.c:54 */
    && findorgl (...)
    && insertpm (...)
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)     /* do1.c:62 */
```

`insertspanf` iterates over every element of `ispanset` and calls `insertnd` once per element [`spanf1.c:25–52`]:
```c
for (; sporglset; sporglset = ...) {
    /* extract lstream and lwidth from each ispan */
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

So **one `insertnd` call per I-span per operation** is confirmed — the question's premise is correct this far.

---

### 2. What `inserttextgr` produces for INSERT

In `granf2.c:83`, `inserttextgr` (called by `inserttextingranf`) always returns **exactly one** `ispanptr` regardless of the number of text chunks:

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typetextset textset, typeispanset *ispansetptr)
{
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))   /* granf2.c:92 */
        return (FALSE);
    movetumbler (&lsa, &spanorigin);                                   /* granf2.c:94 */
    for (; textset; textset = textset->next) {                         /* granf2.c:95 */
        insertseq (...);
        tumblerincrement (&lsa, 0, textset->length, &lsa);
    }
    ispanptr->itemid = ISPANID;
    ispanptr->next   = NULL;
    movetumbler (&spanorigin,           &ispanptr->stream);           /* granf2.c:105 */
    tumblersub  (&lsa, &spanorigin,     &ispanptr->width);            /* granf2.c:106 */
    *ispansetptr = ispanptr;                                           /* granf2.c:107 */
```

The entire text is allocated contiguously from `spanorigin` to `lsa`, yielding a **single I-span covering all inserted text**. This I-span starts at whatever address `findisatoinsertmolecule` returns.

Crucially, for sequential text inserts to the same document, `findisatoinsertmolecule` [`granf2.c:158`] finds the previous highest text ISA in the document and increments it by 1:

```c
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
    tumblerincrement (isaptr, 1, 1, isaptr);                          /* granf2.c:167 */
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);                     /* granf2.c:169 */
}
```

So I-span N+1 starts exactly where I-span N ended: **consecutive inserts produce SPANRANGE-adjacent I-spans**.

---

### 3. What `specset2ispanset` produces for COPY

`specset2ispanset` in `do2.c:14` calls `vspanset2ispanset` → `permute` → `span2spanset` (once per V-span) → `retrieverestricted` → one context entry per contiguous POOM crum. Each context becomes one I-span:

```c
/* orglinks.c:414 */
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, ...);
}
```

Note the commented-out pre-consolidation at `orglinks.c:412`:
```c
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset); */
```

This was explicitly removed. The ispanset is built without pre-merging.

---

### 4. The merging condition in `insertcbcnd`

This is the critical code path. `insertnd` → `doinsertnd` → (when enfilade is non-empty) → `insertmorend` → `insertcbcnd` [`insertnd.c:242`]:

```c
INT insertcbcnd(typecuc *father, typedsp *grasp, typewid *origin, typewid *width, type2dbottomcruminfo *infoptr)
{
    typecorecrum *ptr, *new;
    bool isanextensionnd(), iszerolock();

    for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
        if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {   /* insertnd.c:250 */
            dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype); /* MERGE: widen existing crum */
            ivemodified (ptr);
            setwispupwards (father,1);
            ...
            return(FALSE);   /* NO new crum created */
        }
    }
    new = createcrum (0, (INT)father->cenftype);   /* only here is a new crum created */
    ...
```

`isanextensionnd` [`insertnd.c:301`]:
```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;

    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);                          /* condition 1: same homedoc */
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
    /* condition 2: reach of existing crum == origin of new entry (both dimensions) */
}
```

**Two conditions must both hold for merging:**

**Condition 1** — same `homedoc`: In `insertspanf`, `linfo.homedoc` is set to `docisaptr` (the destination document) for every ispan in the same call [`spanf1.c:29`]:
```c
movetumbler (isaptr, &linfo.homedoc);
```
For entries from the same `insertspanf` call, homedoc is identical. For entries from different calls to the same document, homedoc is also identical. **This condition is always true for entries associated with the same document.**

**Condition 2** — reach equals origin in BOTH dimensions: The ORGLRANGE width is **cleared to zero** before the loop and never updated [`spanf1.c:23`]:
```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
tumblerclear (&crumwidth.dsas[ORGLRANGE]);          /* width in ORGLRANGE = 0 always */
```

For any DOCISPAN crum: ORGLRANGE-reach = ORGLRANGE-origin + 0 = ORGLRANGE-origin. Since `prefixtumbler(isaptr, DOCISPAN, ...)` [`tumble.c:641`] is deterministic for the same `isaptr` and `spantype`, all entries for the same document share identical ORGLRANGE origin and zero ORGLRANGE width. **The ORGLRANGE component of the reach-equals-origin check is always satisfied for entries from the same document.**

Therefore, **the entire merging decision reduces to a single check on the SPANRANGE dimension**: is the new I-span's `stream` address equal to the existing crum's SPANRANGE reach (i.e., `existing.stream + existing.width`)?

---

### 5. When merging actually fires

For sequential text INSERTs into the same document:
- INSERT 1 allocates I-span [A, N] in the granfilade and inserts it into the spanfilade → new crum created.
- INSERT 2 allocates I-span [A+N, M] (next sequential granfilade address) → `isanextensionnd` fires: `homedoc` matches, ORGLRANGE trivially matches, SPANRANGE reach of crum 1 = A+N = SPANRANGE origin of new entry. Result: `dspadd` widens the existing crum from width N to N+M. **No new crum is created.**

This is not a hypothetical: it is the normal behavior for any sequence of text inserts into the same document, since text allocation in the granfilade is sequential.

---

### 6. Summary

| Claim | Verdict |
|---|---|
| One `insertnd` call per contiguous I-span per INSERT/COPY | **True** — confirmed in `insertspanf` [`spanf1.c:51`] |
| One I-span per INSERT | **True** — `inserttextgr` always yields one ispan [`granf2.c:102–107`] |
| One I-span per contiguous permascroll segment per COPY | **True** — `span2spanset` yields one ispan per POOM context [`orglinks.c:439–444`] |
| Spanfilade entry count = cumulative sum of spans | **False** — `insertcbcnd` merges via `isanextensionnd` [`insertnd.c:250`] |
| No merging of adjacent entries | **False** — `isanextensionnd` explicitly widens existing crums when same-document + SPANRANGE-adjacent |
| No deduplication of overlapping entries | **True** — no code deduplicates truly overlapping (non-adjacent) entries |

**The definitive answer:** The spanfilade does NOT accumulate one entry per span per operation. The `isanextensionnd` mechanism in `insertcbcnd` [`insertnd.c:249–258`] merges a new insertion into an existing crum whenever (a) both belong to the same document and (b) the new I-span is SPANRANGE-contiguous with the existing crum's reach. Because the ORGLRANGE width is always zero for DOCISPAN entries, condition (a) trivially reduces to same document, and merging fires whenever permascroll addresses are adjacent. For sequential text inserts into the same document — the normal usage pattern — all inserts coalesce into a single growing spanfilade crum. The cumulative-sum formula overcounts; the actual count depends on how many SPANRANGE gaps exist between insertions.

---

## Question 19 [gregory]

> For the granfilade with `MAXBCINLOAF=1`, each inserted byte occupies exactly one leaf position — does this mean granfilade tree node count grows as O(B) for B total bytes ever inserted, or do the upper crum layers add significant overhead beyond O(B/6^h) per level?

### Gregory's Answer

## KB Synthesis

## Granfilade Node Count: O(B) with Constant ~2.2

Yes, the total node count is O(B) for B bytes inserted via single-byte operations, but the constant factor is **~2.2**, dominated by the doubled bottom two levels. Here's the breakdown.

### Structure created per inserted byte (single-byte inserts)

[SS-GRAN-BOTTOM-SINGLETON] and [SS-GRAN-MB-ONE] establish that `MAXBCINLOAF=1` forces a strict 1:1 mapping: every height-0 bottom crum is wrapped in its own height-1 node. From [SS-ENFILADE-TREE] / Finding 0060:

```
For B single-byte inserts:

Height-0 (bottom crums):  B nodes   — one per text atom
Height-1 (wrappers):      B nodes   — one per bottom crum (1:1 due to MAXBCINLOAF=1)
Height-2:                 B/6       — MAXUCINLOAF=6 upper crums
Height-3:                 B/36
Height h (h≥2):           B/6^(h-1)
```

### Total node count

The geometric series for height ≥ 2 converges:

```
Total = 2B + B·∑(1/6^k, k=1..∞)
      = 2B + B · (1/6)/(1 - 1/6)
      = 2B + B/5
      ≈ 2.2B
```

So **upper crum layers add only ~0.2B overhead** — a 1/5 factor — beyond the dominant 2B from the doubled height-0/height-1 levels. Upper levels are negligible by comparison.

### The "extra +1 height" consequence

[SS-GRAN-MB-ONE] notes the tree height is `⌈log_6(B)⌉ + 1` — one level taller than a uniform M=6 tree would need. For B inserts, this extra height-1 pass-through layer is precisely what creates the second O(B) term. A hypothetical granfilade with `MAXBCINLOAF=4` (like the POOM) would instead have total nodes ≈ 1.33B.

### Caveat: the unit is INSERT operations, not bytes directly

[SS-GRAN-BOTTOM-SINGLETON] and Finding 0034 ([SS-CONTENT-IDENTITY]) confirm that one INSERT of k bytes creates **one** bottom crum (one `GRANTEXT` atom, up to 950 bytes). So:

- Single-byte inserts: B bottom crums, ~2.2B total nodes → **O(B)**
- Full-atom inserts (950 bytes): B/950 bottom crums, ~2.2B/950 nodes → **O(B/950)**

The O(B) bound holds in the worst case of single-byte insertions. For bulk insertions, the constant shrinks proportionally to atom fill.

### Summary

| Level | Count | Contribution |
|-------|-------|-------------|
| Height-0 | B | 1.0 · B |
| Height-1 | B | 1.0 · B (MAXBCINLOAF=1 overhead) |
| Height ≥ 2 | ~B/5 | 0.2 · B (geometric series) |
| **Total** | **~2.2B** | **O(B)** |

The upper crum layers (height ≥ 2) add significant **height** — `log_6(B)` levels — but negligible **node count** (~1/5 of the bottom-level overhead). The design cost of `MAXBCINLOAF=1` is almost entirely in doubling the node count, not in expanding the upper levels.

---

## Code Exploration

I now have a complete picture from reading all relevant source. Here is my full answer.

---

## Granfilade Node Count with `MAXBCINLOAF=1`

### The key constants

From `enf.h:26-28`:
```c
#define MAXUCINLOAF 6
#define MAXBCINLOAF    1        /* so text will fit *//* as you wish */
#define MAX2DBCINLOAF   4       /* for a start */
```

These govern `toomanysons` in `genf.c:239-245`:
```c
bool toomanysons(typecuc *ptr)
{
    if (ptr->height) { findleftson(ptr); }
    return (ptr->numberofsons > (ptr->height > 1
        ? MAXUCINLOAF
        : (is2dcrum((typecorecrum*)ptr) ? MAX2DBCINLOAF : MAXBCINLOAF)));
}
```

**Critical branch:** `is2dcrum` is `cenftype != GRAN` (`genf.c:21`). So for a GRAN granfilade:
- **height > 1 nodes:** `toomanysons` triggers at `numberofsons > 6`
- **height = 1 nodes:** `toomanysons` triggers at `numberofsons > 1` (MAXBCINLOAF)

And identically for `roomformoresons` (`genf.c:255-261`) — a height=1 GRAN node reports room only when `numberofsons < 1`, which is never true in practice once the node has a leaf.

---

### Two distinct tier regimes

**Tier 1 — height=1 nodes (direct leaf parents):** capacity = `MAXBCINLOAF = 1`.  
Each height=1 node can hold exactly **one** leaf before `toomanysons` fires.

**Tier 2 — height≥2 nodes:** capacity = `MAXUCINLOAF = 6`.  
These can hold up to 6 children before splitting.

---

### How splits propagate (`split.c:16-43`)

`splitcrumupwards` walks upward splitting any overfull node:
```c
for (; toomanysons(father); father = findfather(father)) {
    if (isfullcrum(father)) {
        levelpush(father);          // grow tree height
        splitcrum(findleftson(father));
        return(TRUE);
    }
    splitcrum(father);
    splitsomething = TRUE;
}
```

`splitcrumseq` (the GRAN splitter, `split.c:70-93`) moves `numberofsons/2` rightmost sons to a newly created sibling. For a height=1 node with 2 sons: `halfsons = 2/2 = 1`. One leaf moves to the sibling; both height=1 nodes end up with exactly 1 leaf each.

The net effect of every leaf insertion: **one new height=0 leaf + one new height=1 node**, since the height=1 parent always overflows immediately and splits 1-to-1.

---

### Does recombine reverse this? (`recombine.c:38-68`)

```c
int recombineseq(typecuc *father)
{
    if (father->height < 3 || !father->modified) { return(0); }   // <-- guard
    ...
    if (ptr->leftson && roomformoresons(ptr)) { ... }
```

Two blockers prevent merging at the height=1 tier:

1. **Height guard:** `recombineseq` is a no-op for any node with `height < 3`. It never runs on height=1 or height=2 nodes directly.

2. **`roomformoresons` on height=1:** Even when a height=3 node recurses into its height=2 children, the inner loop checks `roomformoresons(ptr)` where `ptr` is height=1. That returns `numberofsons < MAXBCINLOAF = 1`, which is always false. So height=1 nodes never absorb nephews.

**Conclusion:** height=1 nodes remain permanently 1-to-1 with leaves and are never collapsed.

---

### `levelpull` is a no-op (`genf.c:318-342`)

```c
int levelpull(typecuc *fullcrumptr)
{
    return(0);
    /* entire body commented out */
```

Tree height never decreases. No vertical compression happens.

---

### `GRANTEXTLENGTH` packing — important nuance

From `common.h:115`:
```c
#define GRANTEXTLENGTH  950
```

The `fillupcbcseq` path in `insertseq` (`insert.c:34-42`) packs text into an existing leaf crum if it still has room (up to 950 bytes). So in a purely sequential workload, new height-0 crums are **not** created for every byte — up to 950 bytes share one leaf.

`MAXBCINLOAF=1` means each leaf crum occupies its **own loaf** (disk block), not that each byte gets a leaf. The tree's node count per leaf slot is what the question is really asking.

If B = total bytes and inserts are sequential, the leaf count is roughly B/950. If B counts distinct `insertseq` calls (arbitrary-sized text chunks), each call may or may not create a new leaf.

The question premises each byte as one leaf position — that's the `MAXBCINLOAF=1` regime with single-byte inserts, or equivalently just tracking node count as a function of leaf count L.

---

### Node count per level (as a function of L leaves)

| Height | Capacity bound | Node count |
|--------|---------------|------------|
| 0 (leaves) | — | L |
| 1 | MAXBCINLOAF = 1 | **L** (one-to-one) |
| 2 | MAXUCINLOAF = 6 | ≈ L/3 to L/4 (split halves at 7, steady state ~3-4 sons) |
| 3 | 6 | ≈ L/18 to L/24 |
| h ≥ 2 | 6 | ≈ L / 6^(h-1) |

The upper levels form a geometric series:
```
Sum(h≥2) L/6^(h-1) = L/6 * 1/(1 - 1/6) = L/5
```

**Total node count:**
```
N = L (leaves) + L (height-1) + L/5 (height≥2 converging series)
  ≈ 2.2 × L
  = O(L) = O(B) for single-byte inserts
```

---

### Direct answer to the question

**Yes, total granfilade node count is O(B)**, not super-linear. But the constant factor is larger than one might naively expect from the B-tree analogy, because `MAXBCINLOAF=1` governs **two** levels simultaneously:

- Every leaf gets its own height=0 crum: **+L nodes**
- Every height=1 node (the loaf parent of a leaf) also holds exactly 1 child due to the same `MAXBCINLOAF` constant: **+L more nodes**

The upper tiers from height=2 upward add only ~L/5 total nodes — a convergent geometric series at base 6 (`MAXUCINLOAF`). These contribute O(B/6^(h-2)) per level h≥2, and the series is well within the O(B) envelope.

The answer to whether "O(B/6^h) per level" formula holds: **it holds starting from height=2, not height=1**. The height=1 tier breaks the pattern — it contributes O(B) rather than O(B/6^0) = O(B) from the B-tree formula perspective, but that O(B) is the same order as the leaves. What it breaks is the fan-out: you lose the factor-of-6 compression for one whole level, doubling the leaf-tier node cost.

Formally:
- **Leaves + height-1 together:** 2B nodes = O(B)
- **Height ≥ 2:** ~B/5 additional nodes = O(B)
- **Total:** ~2.2B = **O(B)**, with the constant driven by the MAXBCINLOAF=1 choice forcing a 1:1 leaf-parent ratio at height=1.

---

## Question 20 [gregory]

> In the `recombinend` 2D rebalancing algorithm for POOMs, the commented-out `break` statements allow a single receiver to absorb multiple donors — does this merging reduce the total number of upper crums below what strict pairwise rebalancing would produce, and can it ever reduce bottom crum count?

### Gregory's Answer

## KB Synthesis

## Multi-Donor Absorption in `recombinend`: Upper Crums vs. Bottom Crums

### Upper Crum Reduction: Yes, Below Strict Pairwise

Multi-donor absorption does reduce upper crum count below what strict pairwise rebalancing achieves, and can do so in a single pass.

The mechanism is established in [ST-REBALANCE-2D] (Finding 0073): the inner `j` loop does not break after a successful merge (break statements commented out, dated "6/16/84"). This means a single receiver at position `i` can absorb multiple donors `j=i+1, j=i+2, ...` in sequence. Compare the two strategies for 5 height-1 nodes each containing 1 bottom crum (branching limit `MAX2DBCINLOAF = 4`):

**Multi-donor (`recombinend`)** — single pass:
```
sons = [c0, c1, c2, c3, c4]
i=0: c0 absorbs c1 (combined=2), steals from c2 (combined=3),
     depletes c3 (combined=4, receiver saturated — roomformoresons=FALSE)
     c1 → NULL, c3 → NULL
i=2: c2' absorbs c4
Result: 2 upper nodes (c0, c2')
```

**Strict pairwise (`recombineseq`, 1D variant)** — adjacent pairs, one merge per invocation:
```
Pass 1: merge (c0,c1), merge (c2,c3) → 3 nodes remain (c01, c23, c4)
Pass 2: merge (c01,c23) → 2 nodes remain (c0123, c4)
Pass 3: ishouldbother(c0123, c4)? 4+1=5 > 4 → FALSE, done
Result: 2 upper nodes — but required 3 passes vs. 1
```

In this case the final count is the same, but consider when the initial distribution is less symmetric. With 4 nodes each containing 1 child, multi-donor gives 1 node (one receiver absorbs 3 donors: 1+1+1+1 = 4 ≤ 4). Strict pairwise gives 2 nodes (two pairs merge: (c0,c1) and (c2,c3)).

The postcondition property from [ST-REBALANCE-2D] (Finding 0071) captures this: after `recombinend`, the result is **saturated** — `∀ i,j ∈ children: ¬ishouldbother(i,j)`. This saturation is achieved in one pass. `recombineseq` only guarantees incremental progress, requiring repeated invocations to reach the same fixed point. Therefore multi-donor absorption reaches a lower or equal upper-crum count compared to any single invocation of strict pairwise, and typically achieves saturation that strict pairwise would reach only after multiple calls.

There is a complication: `levelpull` would reduce tree height when the root ends up with a single child after saturation. But [SS-ENFILADE-TREE] (Finding 0058) confirms `levelpull` is disabled (immediately returns 0), so height reductions that would follow aggressive merging never occur. The saturation is local to the node being rebalanced, not propagated upward.

### Bottom Crum Count: No

`recombinend` cannot reduce bottom crum count. The operations it performs — `eatbrossubtreend` (full subtree merge) and `takeovernephewsnd` (nephew stealing, from [ST-REBALANCE-2D] Finding 0071) — move bottom crums between height-1 containers but never create or destroy them.

When `eatbrossubtreend` processes two height-1 nodes, it:
1. Transfers all bottom crum pointers (`sons[]`) from the donor to the receiver
2. Calls `disown` + frees the donor height-1 node
3. Bottom crum count: unchanged — the same bottom crums now sit under one height-1 node instead of two

When `takeovernephewsnd` steals nephews at height-1, it moves individual bottom crums one by one. When the donor is depleted, it is freed, but the bottom crums it held are now in the receiver. Again: count unchanged.

Bottom crum lifecycle is controlled exclusively by:
- **INSERT** via `insertseq` — allocates new bottom crums via `adopt(new, RIGHTBRO, ptr)` [ST-INSERT]
- **DELETE** via `deletend` Case 1 — frees bottom crums via `disown + subtreefree` [ST-DELETE]

Rebalancing operates on the containment hierarchy above the bottom layer. This is also consistent with [SS-GRAN-BOTTOM-SINGLETON] for GRAN enfilades, where each height-1 node holds exactly 1 bottom crum — merging two height-1 GRAN nodes would violate the `MAXBCINLOAF = 1` constraint and would be blocked by `ishouldbother`.

### Summary

| Effect | Multi-donor vs. strict pairwise |
|--------|--------------------------------|
| Upper crum count | Can be lower (saturation in one pass) |
| Bottom crum count | Identical (rebalancing only moves, never destroys) |
| Tree height | Identical (`levelpull` disabled, no level collapse) |

---

## Code Exploration

Now I have everything I need. Let me write the complete analysis.

---

## `recombinend` 2D Rebalancing: The Commented-Out `break` and Crum Count Effects

### The Code Under Analysis

The two commented-out `break` statements are at `recombine.c:124-125`:

```c
for (i = 0; i < n-1; i++) {
    for (j = i+1; sons[i] && j < n; j++) {
        if(i != j && sons[j] && ishouldbother(sons[i],sons[j])){
            takeovernephewsnd (&sons[i], &sons[j]);
            /*break;*/
            /*break;//zzz6/16/84 reg//*/
        }
    }
}
```

The second carry a date annotation `zzz6/16/84 reg` — Roger Gregory commented these out in June 1984. Without a `break`, after `sons[i]` successfully absorbs a donor `sons[j]`, the inner loop continues at `j+1`, looking for additional donors for the same receiver `i`.

---

### Structural Context

**`recombinend` only runs on upper crums.** The guard at `recombine.c:112`:

```c
if (father->height < 2  || !father->modified)
    return(0);
```

...means the function only performs merge work when `father->height >= 2`. Its `sons[]` array therefore contains nodes at height `father->height - 1 >= 1` — upper crums, never bottom crums (height 0).

**Capacity limits** from `enf.h:26-28`:

```c
#define MAXUCINLOAF 6       /* max sons for upper crums (height >= 2 nodes) */
#define MAX2DBCINLOAF 4     /* max sons for height-1 nodes in POOM/SPAN */
#define MAXBCINLOAF 1       /* max sons in GRAN bottom crums (not relevant here) */
```

**`ishouldbother`** selects the applicable limit based on `dest->height` (`recombine.c:162`):

```c
return (dest->numberofsons + src->numberofsons <=
        (dest->height>1 ? MAXUCINLOAF : MAX2DBCINLOAF) && randomness(.3));
```

Note: `randomness(.3)` always returns `TRUE` — its probabilistic body is fully commented out at `recombine.c:135-146`.

---

### The Diagonal Sort

`getorderedsons` (`recombine.c:270-280`) invokes `shellsort`, which sorts sons by the **sum of both dimension displacements** (`cdsp.dsas[0] + cdsp.dsas[1]`). This "diagonal" ordering ensures siblings in 2D space are visited in a globally consistent sequence — from bottom-left to top-right — independent of which V or I dimension coordinate is dominant. The merge sweep therefore operates on geographically adjacent siblings first.

---

### Question 1: Does Multi-Donor Absorption Reduce Upper Crum Count Below Strict Pairwise?

**Yes, definitively.**

#### Mechanism

`takeovernephewsnd` has two paths (`recombine.c:179-201`):

1. **Complete absorption** — if `me->numberofsons + bro->numberofsons <= MAXUCINLOAF`, calls `eatbrossubtreend(me, bro)`, which splices `bro`'s child list into `me`'s, then `disown(bro); freecrum(bro)` (`recombine.c:227-228`). Sets `*broptr = NULL`.

2. **Partial absorption** — loops `takenephewnd` one child at a time while `roomformoresons(me)` is true (`recombine.c:187-192`). If bro is drained to zero children, it is also freed (`recombine.c:197-199`).

When `*broptr = NULL` after complete absorption, the outer loop's check `sons[j] &&` catches the nulled slot. The **inner loop continues with `j+1`**, testing the next donor against the same receiver `sons[i]` — whose `numberofsons` has now grown.

#### Concrete example

`father` at height=2, four sons at height=1, each with 1 bottom crum child. Capacity: MAX2DBCINLOAF = 4.

**Without `break` (actual behavior):**

| Step | i | j | sons[i].n | sons[j].n | Total | ≤ 4? | Action |
|------|---|---|-----------|-----------|-------|------|--------|
| 1 | 0 | 1 | 1 | 1 | 2 | YES | eatbrossubtreend → sons[0].n=2, sons[1]=NULL |
| 2 | 0 | 2 | 2 | 1 | 3 | YES | eatbrossubtreend → sons[0].n=3, sons[2]=NULL |
| 3 | 0 | 3 | 3 | 1 | 4 | YES | eatbrossubtreend → sons[0].n=4, sons[3]=NULL |
| 4 | 1 | — | NULL | — | — | — | inner skips, `sons[i]` is NULL |
| 5 | 2 | — | NULL | — | — | — | same |

Result: **1 remaining upper crum** with 4 bottom crums. **3 upper crums eliminated.**

**With `break` (strict pairwise, hypothetical):**

| Step | i | j | sons[i].n | sons[j].n | Action |
|------|---|---|-----------|-----------|--------|
| 1 | 0 | 1 | 1 | 1 | eatbrossubtreend → sons[0].n=2, sons[1]=NULL. BREAK. |
| 2 | 1 | — | NULL | — | sons[i]=NULL, inner loop falls through |
| 3 | 2 | 3 | 1 | 1 | eatbrossubtreend → sons[2].n=2, sons[3]=NULL. BREAK. |

Result: **2 remaining upper crums** (sons[0] with 2, sons[2] with 2). **2 upper crums eliminated.**

The no-break version eliminates **one additional upper crum** in this case. With a larger fan-out (e.g., a father with n=6 sons each at 1/6 of the capacity limit), the multi-donor version can reduce the upper crum count to 1 while strict pairwise would converge to n/2.

#### Why `roomformoresons` keeps this safe

Even in the partial-absorption path, `takeovernephewsnd`'s inner loop (`recombine.c:187`) checks `roomformoresons(me)` before each child move. `roomformoresons` (`genf.c:255-261`):

```c
bool roomformoresons(typecuc *ptr)
{
    if(ptr->height && !ptr->leftson) findleftson(ptr);
    return (ptr->numberofsons < (ptr->height > 1 ? MAXUCINLOAF : MAX2DBCINLOAF));
}
```

stops the loop when the receiver is full. And `ishouldbother` pre-checks total capacity before any absorption attempt. So the no-break continuation can only proceed when there is genuine room — no upper crum ever overflows its capacity limit, and no subsequent `splitcrumupwards` is triggered by the merging itself.

---

### Question 2: Can the Merging Ever Reduce Bottom Crum Count?

**No. Never.**

The merging operations exclusively move bottom crums between upper crum containers. No path in `recombinend` or its callees creates or destroys a bottom crum.

#### `eatbrossubtreend` (`recombine.c:205-233`)

This is called when a donor is completely absorbed. The critical lines (`recombine.c:217-219`) splice `bro`'s child linked-list onto the right end of `me`'s child list:

```c
getleftson (bro)->leftbroorfather = getrightmostbro (getleftson (me));
getrightmostbro (getleftson (me))->rightbro = getleftson (bro);
bro->leftson->isleftmost = FALSE;
```

Then `bro` itself (an upper crum) is freed (`recombine.c:227-228`):

```c
disown (bro);
freecrum (bro);
```

`bro`'s children — bottom crums if `father->height == 2` — are linked into `me`'s child list. They are not freed. `me->numberofsons` is incremented by `bro->numberofsons` (`recombine.c:221`).

#### `takenephewnd` (`recombine.c:235-257`)

Moves a single child from its current parent to the receiver:

```c
disown (nephew);         // removes from bro's child list, no free
adopt (nephew, RIGHTMOSTSON, me);  // re-parents to me
```

If `bro->numberofsons` reaches 0 after losing all its children:

```c
disown (bro);
freecrum (bro);          // only the empty upper crum is freed
```

Again: the child (bottom crum) is moved, not freed.

#### Invariant

The bottom crum set is **structurally invariant** under `recombinend`. Before and after any invocation, the total count and contents of bottom crums within `father`'s subtree are identical. Only the mapping of bottom crums to their immediate upper crum parents changes.

Bottom crum count changes only via:
- **Insertion** — `insertcbcnd` (`insertnd.c:260`) allocates a new bottom crum with `createcrum(0, enftype)`
- **Extension optimization** — `isanextensionnd` (`insertnd.c:250`) widens an existing adjacent bottom crum instead of creating one, suppressing a net +1
- **Deletion** — frees bottom crums

None of these occur inside `recombinend`. The `break`-less behavior affects only the number of upper crum intermediate nodes — which is exactly the variable the algorithm is designed to minimize.

---

### Summary

| Effect | With `break` (pairwise) | Without `break` (actual) |
|--------|------------------------|--------------------------|
| Upper crums after merge | n/2 (at best) | Can reach 1 if all fit | 
| Bottom crums after merge | Unchanged | Unchanged |
| Overflow risk | None | None (`ishouldbother` guards) |

**Q1 answer:** Yes — a single receiver can absorb multiple donors, eliminating more upper crum intermediate nodes than strict pairwise rebalancing in one pass. The gain is bounded by how many siblings can collectively fit within the receiver's capacity (MAXUCINLOAF=6 at height≥2, MAX2DBCINLOAF=4 at height=1). In the limit with maximally sparse children, the multi-donor approach reduces a fully populated loaf to a single survivor rather than n/2 survivors.

**Q2 answer:** No — `recombinend` never reduces the bottom crum count. `eatbrossubtreend` (`recombine.c:217-219`) and `takenephewnd` (`recombine.c:242-244`) are pure pointer-relinking operations on the upper crum tree. Bottom crums are moved between containers but never freed by these routines, regardless of whether `break` is active or suppressed.
