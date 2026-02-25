# Consultation Answers — Rearrange Operation

**Inquiry:** What must REARRANGE (reordering content within a document without insertion or deletion) preserve and establish? How does moving content differ from delete-then-insert, and what address, link, and provenance guarantees must hold across rearrangement?
**Date:** 2026-02-24 21:38
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When content is rearranged within a document, must the identity of each content span remain the same as before the operation, or may the system assign new identities to the moved material?

### Nelson's Answer

## Identity Must Be Preserved During Rearrangement

**The identity of each content span MUST remain the same.** Rearrangement is purely a V-space operation. It changes which V-addresses map to which I-addresses, but the I-addresses themselves — the identity of the content — are permanent and immutable. The system may not assign new identities to moved material.

This follows directly from the I-space/V-space separation, which is the architectural core of Xanadu.

### The Argument from Architecture

I-space addresses are permanent. Content at an I-space address never changes. V-space is merely an arrangement — a mapping from "position in the document as the user sees it" to "permanent content identity."

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Nelson is explicit: editorial operations (including rearrangement) alter the *order* — the V-space mapping — but the bytes themselves retain their identity. Links attach to bytes, not positions, and survive because the bytes' identity is unchanged.

### The Argument from REARRANGE Semantics

The REARRANGE operation transposes regions of text:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

This is described in terms of *cuts* on the V-stream — positions in the current arrangement. The operation swaps which V-positions map to which I-content. The I-content itself is not touched.

### The Argument from Link Survivability

Nelson explicitly lists rearrangement among the operations links survive:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

This guarantee is only possible if rearrangement preserves content identity. If the system assigned new I-addresses to moved material, links to the old I-addresses would break — violating the survivability invariant.

### The Argument from Correspondence

Version comparison depends on shared I-space origin:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

The SHOWRELATIONOF2VERSIONS operation returns "a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. This works because both versions reference the same I-space content. If rearrangement created new identities, the system could not detect that rearranged content in version N+1 is "the same" as content in version N.

### The Argument from Append-Only Storage

The underlying storage model is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

In an append-only system, existing content is never modified or re-addressed. New content is appended; existing content retains its position. Rearrangement adds no new content to I-space — it only changes the V→I mapping.

### The Argument from Transclusion

If document A transcludes content from document B, and document B rearranges that content, the I-addresses must remain stable — otherwise document A's transclusion would silently break or point to different content:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Transclusions reference I-space addresses at "home locations." Those addresses must be stable across all editorial operations, including rearrangement.

### Summary

Rearrangement is a pure V-space operation. It is analogous to reordering a reading list without moving the books on the shelves. The books (I-space content) stay exactly where they are, with exactly the same shelf locations (I-addresses). Only the list (V-space arrangement) changes. The system **must not** assign new identities to moved material — doing so would violate permanence, break links, destroy correspondence, invalidate transclusions, and undermine the fundamental I-space/V-space contract.

---

## Question 2 [nelson]

> Must links that point to rearranged content continue to resolve to the same content after the move, regardless of where that content now sits within the document?

### Nelson's Answer

## Yes. This is an explicit, named guarantee.

Nelson specifically lists rearrangement alongside deletion and insertion as editing operations that links survive. This is not incidental—it is a stated design property of the link mechanism.

### The Direct Statement

The clearest statement comes from page 4/43, in a visual annotation Nelson labels "SURVIVABILITY":

> "Links between bytes can survive deletions, insertions and **rearrangements**, if anything is left at each end." [LM 4/43]

And from page 4/42:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

### Why This Works Architecturally

The guarantee follows from the I-space/V-space separation. REARRANGE is a **pure V-space operation**—it changes where content appears in the document's virtual byte stream, but does not touch the content's permanent I-space addresses.

Links point to I-space (content identity), not V-space (current position). Nelson states this explicitly on page 4/30:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

And on page 4/11:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address changes; the I-address does not. Links follow the I-address.

### The Strap Metaphor

Nelson's "strap between bytes" image on page 4/42 makes this vivid. Imagine a rubber strap connecting two groups of bytes. You can rearrange the bytes within the document—move paragraphs around, swap sections—and the strap stays attached to the same bytes. It doesn't care where those bytes sit in the document's current arrangement. It cares only that the bytes still exist.

### What REARRANGE Actually Does

From the FEBE specification:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

This operation swaps regions in V-space. The I-space content is completely unchanged. Since link endsets reference I-space spans, REARRANGE has **zero effect** on any link's resolution.

### Summary

The answer is unambiguous: links **must** continue to resolve to the same content after rearrangement. This is:

1. **Explicitly stated** as a survivability guarantee [LM 4/43]
2. **Architecturally guaranteed** by the I-space/V-space separation [LM 4/11, 4/30]
3. **Semantically necessary** because links attach to bytes (content identity), not positions (current arrangement) [LM 4/42]

A system that broke links on rearrangement would violate one of Xanadu's core design properties.

---

## Question 3 [nelson]

> How must rearrangement differ from a delete-then-insert sequence in terms of content continuity — must the system treat moved content as having never left the document?

### Nelson's Answer

# REARRANGE vs. DELETE+INSERT: Content Identity Must Be Preserved

## The Short Answer

Yes — REARRANGE **must** treat moved content as having never left the document. It is a **pure V-space operation** that changes only the arrangement of content, leaving I-space addresses untouched. A DELETE+INSERT sequence would destroy content identity by creating new I-space addresses for what merely looks like the same text.

## The Architectural Distinction

The I-space/V-space separation makes this unambiguous. From the concept-operation map in the curated sources:

| Operation | Effect |
|-----------|--------|
| **REARRANGE** | Pure V-space operation |
| **DELETE** | Removes from V-space only; I-space unchanged |
| **INSERT** | Adds to I-space; updates V-space arrangement |

REARRANGE changes the V→I mapping — which bytes appear at which virtual positions. The I-space addresses of those bytes remain exactly the same.

INSERT, by contrast, creates **new** bytes in I-space with **new** permanent addresses:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

A DELETE+INSERT sequence would therefore:
1. **DELETE**: Remove the V-space mapping (content exits the current view but remains in I-space at its original address)
2. **INSERT**: Create **new** bytes in I-space with **new** addresses, then map them into V-space

The result: text that *looks* identical but has a completely different identity. The original I-space content is orphaned; the new content is a stranger that happens to spell the same way.

## Why This Matters: Five Guarantees at Stake

### 1. Link Survivability

Links attach to I-space bytes, not V-space positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

REARRANGE preserves I-addresses → links follow the content to its new position. DELETE+INSERT creates new I-addresses → links still point to the original (now "deleted") bytes, and the newly inserted bytes have no links at all.

### 2. Origin Traceability

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Every byte's I-address encodes its origin document. REARRANGE preserves this encoding. DELETE+INSERT would make the content appear to originate from the *current* document at the *current* moment — severing provenance from whatever the content's actual history was.

### 3. Transclusion Integrity

If the rearranged content was transcluded from another document:

> "Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

REARRANGE preserves the transclusion — non-native bytes remain non-native, still pointing to their home document. DELETE+INSERT would replace transclusions with new native bytes, severing the connection to the original author and breaking the royalty chain:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

### 4. Version Correspondence

Correspondence between versions depends on shared I-space origin:

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

REARRANGE preserves shared I-addresses between the pre-rearrangement and post-rearrangement versions, so SHOWRELATIONOF2VERSIONS can identify that the content is the same, just repositioned. DELETE+INSERT would make the content appear entirely new, destroying correspondence.

### 5. Historical Backtrack

The append-only storage model means I-space content is never destroyed:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

REARRANGE adds only a mapping change to the history. DELETE+INSERT adds both a mapping removal *and* redundant new bytes to I-space — the same text stored twice under different addresses. This is wasteful and semantically wrong: it tells the system "old content was removed and different content was added" when what actually happened was "the same content moved."

## The Enfilade Perspective

The implementation architecture confirms this. The POOM (Positional) enfilade maps V→I addresses; the GRAN (Granfilade) stores actual I-space content:

- **REARRANGE** modifies only the POOM — the V→I mapping changes, but the GRAN is untouched
- **DELETE** modifies the POOM (removes a mapping) but not the GRAN
- **INSERT** modifies **both** — adds to the GRAN (new bytes) and updates the POOM (new mapping)

REARRANGE is structurally incapable of creating new content. It can only reorder existing mappings. This is the correct behavior.

## Nelson's REARRANGE Specification

The operation itself is defined as a transposition:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

"Transposes" — swaps positions. Not "removes and re-creates." The specification describes a movement of existing content, not a destruction-and-reconstruction sequence.

## Summary

REARRANGE **must** be a pure V-space operation that preserves content identity. The content must be treated as having never left the document — because at the I-space level, it literally hasn't. Only its position in the virtual byte stream has changed. A DELETE+INSERT sequence would violate permanence, attribution, link survivability, correspondence, and the append-only storage model simultaneously. Any implementation that reduces REARRANGE to DELETE+INSERT has misunderstood the I-space/V-space separation that is the foundation of Xanadu's architecture.

---

## Question 4 [nelson]

> After rearrangement, must the provenance record show that the content originated at its original moment of creation, or may it reflect the moment of the move?

### Nelson's Answer

# Rearrangement and Provenance: The Answer Is Unambiguous

**The provenance record MUST reflect the original moment of creation. Rearrangement cannot alter it.**

This isn't a design choice — it's a structural consequence of the I-space/V-space separation that is foundational to Xanadu.

## The Architecture Dictates the Answer

Rearrangement is a **pure V-space operation**. It changes which V-addresses map to which I-addresses, but it does not — and cannot — alter the I-addresses themselves.

From the REARRANGE specification:

> "Rearrange transposes two regions of text." [LM 4/67]

What this means concretely:

| Aspect | Before REARRANGE | After REARRANGE |
|--------|------------------|-----------------|
| V-addresses | Bytes at positions 1-100 | Bytes at new positions (reordered) |
| I-addresses | Unchanged | **Unchanged** |
| Provenance | Each byte traces to its creation document | **Identical** |

Nelson is explicit that V-space changes do not affect I-space identity:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

And:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address is what "may be constantly changing." The I-address — the provenance record — is invariant.

## Why the I-Address Cannot Reflect the Move

The I-address encodes the byte's **creation context**:

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

Every field in this address was determined at creation time: which server, which user, which document, which element position. Rearrangement changes none of these. The byte was born where it was born.

Furthermore, the storage model is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Rearrangement creates no new content in the append-only store. It only modifies the V-space mapping — the virtual byte stream that determines how existing I-space content is arranged for the reader. No new I-space entries means no new provenance records.

## What About Time?

Nelson explicitly separates time from addressing:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Time is metadata, tracked alongside the address system but not encoded within it. The I-address tells you **where** content was created (which document, which user, which server). Time tells you **when**. Neither changes during rearrangement because rearrangement creates nothing new — it rearranges what already exists.

## The Deeper Principle

This follows from Nelson's core architectural insight: **separation of content from arrangement**.

> I-Space guarantee: "Content you create gets a permanent I-space address. That address will always return that exact content. Content is immutable — it never changes after creation."
>
> V-Space guarantee: "Your document's arrangement (V-stream) can evolve."

If rearrangement could alter provenance, it would violate the invariance of I-space — the single property upon which permanent citation, link survivability, transclusion, version comparison, and royalty tracking all depend.

Consider the consequences if provenance *could* reflect the moment of the move:
- **Link survivability breaks** — links point to I-addresses; if those change on rearrangement, links break
- **Correspondence breaks** — version comparison depends on shared I-addresses across versions
- **Attribution breaks** — "you can at once ascertain the home document of any specific word or character" [LM 2/40] requires stable I-addresses
- **Royalty tracking breaks** — the system must know which document owns which bytes

## Summary

REARRANGE transposes regions in V-space. I-space is untouched. Provenance is I-space. Therefore provenance is untouched. The content originated at its original moment of creation, and no operation in the system — not rearrangement, not deletion, not versioning — can alter that fact. That is not a policy; it is the architecture.

---

## Question 5 [nelson]

> If rearranged content is shared by transclusion into other documents, must those other documents remain completely unaffected by the reordering in the source document?

### Nelson's Answer

## Yes — Completely Unaffected

The I-Space/V-Space separation guarantees this. REARRANGE is a **pure V-Space operation** — it changes only the source document's arrangement of content, never the content itself. Transcluding documents have their own independent V-Space arrangements pointing to the same I-Space addresses, so they are architecturally insulated from reordering in the source.

### The Mechanism

When document B transcludes content from document A via COPY, what happens is:

1. B's V-Space acquires mappings to the **I-Space addresses** of A's content
2. B has its own independent V-Space arrangement
3. The I-Space content is immutable — it never changes

When A then performs REARRANGE, only A's V-Space mapping changes. The I-Space addresses remain exactly where they were. B's V-Space still points to those same I-Space addresses in whatever order B established.

```
Before REARRANGE in A:

I-Space:     [X: "hello"]  [Y: " world"]  [Z: "!"]
A's V-Space: X → Y → Z     ("hello world!")
B's V-Space: X → Y          ("hello world")

After REARRANGE in A (swap first two):

I-Space:     [X: "hello"]  [Y: " world"]  [Z: "!"]   ← UNCHANGED
A's V-Space: Y → X → Z     (" worldhello!")           ← CHANGED
B's V-Space: X → Y          ("hello world")            ← UNCHANGED
```

### Nelson's Direct Statements

Nelson explicitly confirms that V-Space operations on one document do not affect other documents' transclusions. While he addresses DELETE rather than REARRANGE specifically, the principle is stronger for REARRANGE since it doesn't even remove content from V-Space:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If DELETE — which actually removes content from V-Space — leaves other documents' transclusions intact, then REARRANGE — which merely reorders content within V-Space — certainly does as well.

The concept-operation map in the I-Space/V-Space source explicitly classifies:

> **REARRANGE** | Pure V-space operation

And on the fundamental separation:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-Space addresses are ephemeral and document-local. I-Space addresses are permanent and universal. Transclusion works through I-Space, so V-Space operations in the source document are invisible to transcluding documents.

### The Deeper Principle

This follows from Nelson's core architectural decision: **separation of content from arrangement**.

> "Content is permanent (I-space) → enables permanent citations, links. Arrangement is flexible (V-space) → enables editing, versions."

Each document owns its own arrangement. The COPY operation gives the target document its own V-Space references to shared I-Space content. From that point forward, the two documents' arrangements are independent. The source document's author can rearrange freely; the transcluding document's author can rearrange freely; neither affects the other.

This is also consistent with Nelson's vision of non-destructive modification:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

If modifications to derivative documents cannot damage originals, the converse holds equally: modifications to originals (including rearrangement) cannot damage derivatives. Each document's V-Space is sovereign.

### What About "Floating" Windows?

Nelson describes two transclusion modes — location-fixed ("floating in time," where updates propagate) and time-fixed (frozen reference) [LM 2/37]. One might wonder whether a location-fixed window would track the source's rearrangement.

Even here, the answer is no. A location-fixed window tracks **content identity** (I-Space), not **positional arrangement** (V-Space). What propagates through a floating window is content changes (insertions, deletions in the source) — not reorderings. The "location" being tracked is the I-Space identity of the transcluded bytes, which is unaffected by rearrangement.

### Summary

REARRANGE in document A changes only A's V-Space. Document B's transclusions reference I-Space addresses, which are immutable. B is completely unaffected. This is not a special guarantee about REARRANGE — it falls directly out of the I-Space/V-Space architecture that is foundational to all of Xanadu.

---

## Question 6 [nelson]

> Must the document's version history record a rearrangement as a single atomic operation, distinct from any combination of deletions and insertions?

### Nelson's Answer

# Must REARRANGE Be Recorded as a Distinct Atomic Operation?

**Yes — functionally, it must be distinguishable from any combination of DELETE and INSERT.** The reason is not that Nelson mandates a specific history recording format, but that the I-space consequences of REARRANGE differ fundamentally from DELETE+INSERT, and the correspondence guarantee depends on this distinction.

## The Core Argument: I-Space Identity

REARRANGE is a **pure V-space operation**. It changes where content appears in the document's virtual byte stream without touching I-space at all. The content retains its permanent I-space addresses.

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4."
> — [LM 4/67]

INSERT, by contrast, **creates new I-space content**:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text."
> — [LM 4/66]

DELETE removes content from V-space but leaves I-space untouched:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"
> — [LM 4/9]

So consider what happens if you try to represent a rearrangement as DELETE + INSERT:

| Step | V-Space Effect | I-Space Effect |
|------|---------------|----------------|
| DELETE span at positions 50-100 | Span removed from V-stream | None (bytes remain in I-space) |
| INSERT same text at position 200 | New text appears at position 200 | **New bytes created with new I-addresses** |

The inserted text, even if byte-for-byte identical, has **different I-space addresses** than the original. Content identity in Xanadu is based on creation, not value:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."
> — (from the sporgl-provenance design intent, summarizing [LM 4/10-4/11])

## Why This Matters: Correspondence Breaks

The correspondence guarantee depends entirely on shared I-space origin:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same."
> — [LM 2/20]

SHOWRELATIONOF2VERSIONS computes correspondence by finding shared I-space addresses:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond."
> — [LM 4/70]

If the history decomposed REARRANGE into DELETE + INSERT:
- The pre-rearrangement version would contain I-addresses {A, B, C, D, E}
- The post-rearrangement version would contain I-addresses {A, B, **F, G**, E} (where F, G are new I-space for the "inserted" content that replaced the deleted C, D)
- SHOWRELATIONOF2VERSIONS would report that spans C-D in the old version have **no corresponding content** in the new version
- The rearranged content would appear as simultaneously deleted AND newly created — a false history

With REARRANGE recorded faithfully:
- The pre-rearrangement version contains I-addresses {A, B, C, D, E}
- The post-rearrangement version contains I-addresses {A, B, C, D, E} — same content, different V-space ordering
- SHOWRELATIONOF2VERSIONS correctly identifies that all content corresponds

## Could DELETE + COPY Work Instead?

COPY (transclusion) preserves I-space identity:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>."
> — [LM 4/67]

Since COPY creates a V-space reference to existing I-space content, a DELETE followed by COPY of the same I-space content would preserve I-addresses and thus preserve correspondence. However, this decomposition is awkward: after DELETE removes the content from V-space, you'd need to reference the I-space addresses of the "deleted" content to COPY them back in. Nelson doesn't describe this workflow. REARRANGE exists precisely to handle this case cleanly as a single V-space transformation.

## Nelson's Conceptual Model Treats Rearrangement as Primitive

Nelson lists rearrangement alongside addition and subtraction as a fundamental editorial operation — not derived from them:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are **rearranged, added or subtracted**... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex."
> — [LM 2/15]

REARRANGE appears as one of the 17 FEBE commands — a first-class protocol operation, not a convenience wrapper:

> "FEBE includes instructions for insertion in a document, deletion from a document, and rearrangements of unlimited size. These are conceptually simple."
> — [LM 4/61]

And in the concept-operation mapping, REARRANGE is classified as a **pure V-space operation** — the only editing command with this property. INSERT and APPEND modify both V-space and I-space. DELETE modifies V-space only. But REARRANGE is unique in being the operation that changes the arrangement without any I-space effect whatsoever.

## Conclusion

Nelson does not explicitly say "the version history must record REARRANGE as atomic." What he specifies is:

1. REARRANGE is a distinct FEBE operation that transposes V-space regions
2. The system must reconstruct any previous version on demand
3. SHOWRELATIONOF2VERSIONS must correctly identify corresponding content via shared I-space

These three requirements together **imply** that REARRANGE cannot be decomposed into DELETE + INSERT in the version history, because doing so would create spurious I-space addresses that break correspondence. The version history must preserve the fact that content was moved, not destroyed and recreated.

NEED_RAW: [4/67] — I've relied on the curated extraction of the REARRANGE specification. The raw page may contain additional detail about how the operation interacts with history or I-space that the extraction condensed.

---

## Question 7 [nelson]

> Must the addresses of content that was NOT moved remain stable after a rearrangement operation changes the ordering around them?

### Nelson's Answer

# V-Space Address Stability After REARRANGE

## Short Answer

**No.** V-space addresses of unmoved content are not guaranteed to remain stable after a REARRANGE. But this is by design — V-space is inherently mutable, and the stability guarantee lives in I-space.

## The Evidence

### V-Space Is Designed to Be Ephemeral

Nelson explicitly states that V-space ordering changes during editing:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

V-space addresses are dense sequential positions — always 1 through N with no gaps. The v-space-addresses design intent confirms:

- "INSERT shifts addresses after the insertion point"
- "DELETE removes addresses (closing the gap)"
- "The same content gets different V-addresses after edits"

The INSERT operation makes this explicit:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

So even for INSERT — a simpler operation than REARRANGE — content that was NOT inserted still gets new V-addresses if it follows the insertion point. The precedent is clear: editing operations shift V-addresses of untouched content.

### REARRANGE Mechanics

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

Consider the **4-cut case** with non-adjacent regions of different sizes:

```
Before:  [prefix][AAAA][middle][BB][suffix]
              cut1  cut2   cut3 cut4

After:   [prefix][BB][middle][AAAA][suffix]
```

Here `middle` was not moved, yet its V-address shifted by `len(BB) - len(AAAA)`. The `suffix` also shifted. Only `prefix` (before both regions) retained its original V-addresses.

The **3-cut case** (adjacent regions) is more forgiving — content outside the swapped zone retains its V-addresses because the total size of the zone doesn't change:

```
Before:  [prefix][AAAA][BBB][suffix]
              cut1  cut2  cut3

After:   [prefix][BBB][AAAA][suffix]
```

`prefix` and `suffix` keep their V-addresses. But the bytes within AAAA and BBB all get new V-addresses even though only their relative ordering changed.

### The Stability Guarantee Lives in I-Space

This is the architectural point. Nelson designed two address spaces precisely so that one could be mutable while the other is permanent:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

I-space addresses — the permanent identity of content — never change for any reason. Links survive REARRANGE (and all editing) because they point to I-space:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

The link-survivability design intent makes the mechanism explicit: "Rearrangements (order changes don't affect content identity)." The content's *identity* (I-address) is stable. Its *position* (V-address) is not.

## Summary

| Address Space | Stable after REARRANGE? | By Design? |
|---|---|---|
| **I-space** (permanent identity) | Always — for ALL content | Yes — I-addresses never change |
| **V-space** (current position) | Only for content outside the affected zone, and only in the 3-cut case | Yes — V-space is mutable by definition |

Nelson's architecture treats V-address instability not as a bug but as the entire point of separating I-space from V-space. You edit in V-space; you cite in I-space. The rearrangement changes the view, not the content.

---

## Question 8 [nelson]

> When content is rearranged, must the system preserve the original author attribution of each moved span, even if a different user performs the rearrangement?

### Nelson's Answer

# Yes — Attribution Survives Rearrangement by Structural Necessity

The answer is unequivocally yes, and it's not merely a policy requirement — it's an architectural consequence of how Xanadu stores content. Attribution cannot be lost through rearrangement because it is encoded in the address itself.

## The Architectural Argument

Rearrangement is a **pure V-space operation**. It changes the order in which content appears in a document's virtual byte stream, but it does not — and cannot — alter the permanent I-space addresses of the bytes being moved.

Every byte's I-address has the form `Node.0.User.0.Document.0.Element`, which permanently encodes which server, which user account, and which document originally created that byte. Rearranging bytes in V-space is like reordering entries on a reading list — the books on the library shelves (I-space) don't move.

Nelson confirms this separation explicitly:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The V-address changes; the I-address — and therefore the attribution — does not.

## The User-Facing Guarantee

Nelson states the guarantee directly:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This holds regardless of who performed the rearrangement. Whether the original author reorders their own paragraphs, or a different user creates a compound document that rearranges transcluded material, the I-addresses trace back to the original creator.

## The REARRANGE Operation

The FEBE protocol defines rearrangement as transposing regions of text within a document:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

This operation modifies only the V-space mapping. The bytes at their I-space addresses are untouched.

## The Cross-Author Case

When a different user rearranges content that includes material from other authors, the compound document model applies:

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

> "Each compound document is like the other documents: it has an owner and receives royalties." [LM 2/33]

The compound document has its own owner (the person who assembled it), but each constituent span retains its I-space origin. The system can distinguish "who wrote what" automatically:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

This automatic splitting is possible precisely because attribution is structural — the I-addresses tell the system which bytes belong to which author, regardless of how they've been rearranged in V-space.

## Why Attribution Cannot Be Severed

The design intent document on origin traceability makes this explicit:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

To display transcluded content, the system must fetch it from its home location. The fetching mechanism itself requires knowing the origin. Attribution isn't a label attached to content — it's the address used to retrieve it.

## Summary

| Operation | V-Space Effect | I-Space Effect | Attribution Effect |
|-----------|---------------|----------------|-------------------|
| REARRANGE | Positions change | None | None — preserved |
| DELETE | Removed from view | None — bytes persist | None — preserved |
| COPY (transclusion) | New V-mapping created | None — shared I-addresses | None — preserved |
| INSERT (new content) | New positions created | New I-addresses created | New author recorded |

Rearrangement cannot affect attribution because attribution is not metadata — it is the address. The system doesn't need a rule saying "preserve attribution on rearrange." It is structurally impossible to lose it.

---

## Question 9 [nelson]

> Must a comparison between the version before rearrangement and the version after reveal exactly which spans changed position, rather than showing apparent deletions and insertions?

### Nelson's Answer

## Yes — and this is a structural guarantee, not a design choice

The architecture makes rearrangement distinguishable from deletion+insertion by construction. But Nelson does not state this explicitly for the REARRANGE case. It follows from three premises he does state.

### Premise 1: REARRANGE is a pure V-space operation

REARRANGE "transposes two regions of text" [LM 4/67]. It changes where bytes appear in the document's virtual byte stream. It does not create new bytes and does not remove bytes from I-space.

The concept mapping confirms this directly:

> REARRANGE — Pure V-space operation
> — [i-space-v-space concept, FEBE Operations table]

### Premise 2: Correspondence is computed from shared I-space origin

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. Correspondence is defined as shared I-space origin:

> Correspondence is a RELATION — the relationship between V-space positions that share the same I-space origin.
> — [correspondence design intent]

The system does not run a textual diff. It traces I-addresses.

### Premise 3: REARRANGE leaves I-space unchanged

Since REARRANGE only modifies V-space, every I-address that existed before the operation still exists after it. No bytes are created. No bytes are removed from I-space. The mapping from V-positions to I-addresses is rewritten; the I-addresses themselves are untouched.

### The conclusion

When you compare the version before rearrangement with the version after, SHOWRELATIONOF2VERSIONS computes correspondence via shared I-space origin. Because the I-space is identical in both versions, the operation returns a complete set of ordered pairs — every span in the old version has a corresponding span in the new version, and vice versa. Nothing is unmatched.

A naive positional diff would see "paragraph 3 disappeared from position 3 and new text appeared at position 1." But Xanadu's correspondence mechanism sees "the bytes at V-position 3 in version 1 share I-addresses with the bytes at V-position 1 in version 2 — they correspond."

The result: **rearrangement produces 100% correspondence with changed V-positions**. A deletion+reinsertion of identical text would produce **zero correspondence at the re-inserted location**, because the re-inserted bytes would have new I-addresses (fresh bytes appended to I-space), while the deleted bytes would have no counterpart in the new V-stream.

This distinction is unambiguous and automatic. The system cannot confuse the two cases.

### What Nelson says directly

Nelson does not explicitly discuss the rearrange-then-compare scenario. But he states the properties that make the answer deterministic:

> "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." [LM 3/13]

And on the structural basis:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The same principle that makes links survive rearrangement makes correspondence survive rearrangement: both track I-space identity, not V-space position.

### Summary

| Scenario | I-space change | Correspondence result |
|----------|---------------|----------------------|
| REARRANGE | None — same bytes, new arrangement | Complete correspondence; all spans match |
| DELETE + INSERT same text | Old bytes orphaned; new bytes created | Zero correspondence at affected positions |
| DELETE + COPY (transclusion) | Old bytes orphaned from V-space; COPY references existing I-bytes | Correspondence at copied spans (shared I-origin) |

The answer to your question is **yes**: the architecture guarantees that version comparison after REARRANGE reveals exactly which spans changed position, because correspondence is an I-space relation and REARRANGE is a pure V-space operation. Showing apparent deletions and insertions would require a system that ignores I-space identity — which is precisely what Xanadu was designed to avoid.

---

## Question 10 [nelson]

> If two spans of content within a document swap positions, must the system guarantee that no moment exists in which either span is absent from the document?

### Nelson's Answer

# Atomicity of REARRANGE: Must Spans Always Be Present?

## Short Answer

Nelson's design strongly implies **yes** — REARRANGE is a single atomic operation at the protocol level, and the enfilade system mandates that every change leaves the structure in canonical order. But Nelson does not explicitly state an atomicity guarantee in the way a database specification would. The question falls into a gap between his protocol-level design (where it's one command) and his implementation-level principles (which mandate structural integrity after every change).

## Evidence From Nelson's Design

### 1. REARRANGE Is a Single Protocol Command

REARRANGE is one of the 17 FEBE commands — it is not decomposed into DELETE followed by INSERT:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

The operation is defined by **cut points** that delineate the two regions, and the system transposes them. There is no intermediate step where one region has been removed but the other has not yet moved. The semantics are "swap these two regions," not "remove region A, then insert region A at B's position, then remove region B, then insert region B at A's position."

If REARRANGE could be reduced to a sequence of DELETEs and INSERTs, there would be no reason for it to exist as a separate command. Its existence as a primitive implies that it does something those operations cannot — namely, transpose content without passing through any state where content is absent.

### 2. The Canonical Order Mandate

The enfilade system — the data structure that implements Xanadu's storage — has an explicit mandate regarding structural integrity after changes:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. **All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system.**" [LM 1/34]

"Canonical order" after every change means the data structure is always in a well-formed state. There is no moment where the structure is inconsistent — which would include a moment where content present before the operation is absent during it.

### 3. REARRANGE Is a Pure V-Space Operation

REARRANGE only changes the **V-space mapping** (the document's current arrangement), not the **I-space content** (permanent storage):

| Operation | How I-space/V-space applies |
|-----------|----------------------------|
| **REARRANGE** | Pure V-space operation |

The I-space content — the actual bytes — is never touched. Only the mapping from V-addresses to I-addresses changes. This means the operation is structurally simpler than it might appear: it is updating a mapping table, not moving data. The bytes exist permanently in I-space regardless of what V-space does.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

### 4. Non-Destruction as a System Principle

Nelson's non-destruction guarantee operates at every level:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Xanadu explicitly rejects this. Content is never destroyed by editing operations. DELETE itself only removes content from V-space; the I-space content remains. REARRANGE, being a pure V-space operation, has even less reason to create a state where content is absent — it is not removing anything, even from V-space. It is reordering.

## What Nelson Does NOT Say

Nelson does not explicitly address:

- **Observable intermediate states during a single operation.** He does not discuss what happens if another user reads the document while REARRANGE is executing.
- **Concurrency guarantees.** The FEBE protocol is presented as a sequential command interface. Nelson mentions future plans for concurrent users but does not specify a concurrency model:

  > "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." [LM 4/59]

- **Transaction semantics.** There is no COMMIT/ROLLBACK model. Each command is implicitly atomic.

NEED_RAW: 4/67 — The REARRANGE command description may have additional detail about error handling or partial-completion semantics not captured in OCR extraction.

## My Assessment as Nelson

The question reveals a concern rooted in implementation thinking — "what if the swap is half-done?" This concern arises from systems that decompose operations into sequences of smaller steps. Xanadu does not work this way.

REARRANGE is a **semantic primitive**. It means "these two regions trade places." The system computes the new V-space arrangement and presents it. There is no meaningful intermediate state because the operation is defined as a single transformation of the mapping.

Consider the analogy: when you rearrange chapters in a book by changing the table of contents, the chapters themselves (I-space) don't move. You rewrite the table of contents (V-space) to list them in a new order. At no point during the rewriting is a chapter "absent from the book" — the chapters are still on their shelves. You're just changing which order you read them in.

The canonical order mandate [LM 1/34] seals this: the system is **always** in a valid state. Not "eventually consistent," not "consistent after a commit" — always. This is an internal mandate, not a best-effort goal.

So yes: a conforming implementation must ensure that REARRANGE produces a new arrangement atomically, with no observable intermediate state where either span is absent from the document's V-stream.

---

## Question 11 [gregory]

> When `rearrangend` applies tumbler offsets to V-addresses in the POOM, does it modify bottom crum displacements in-place, or does it disown and recreate entries — and does this distinction affect whether `isanextensionnd` can later coalesce adjacent entries that were split by the rearrange?

### Gregory's Answer

## KB Synthesis

## REARRANGE: In-Place Modification and isanextensionnd Coalescing

### How rearrangend applies offsets

`rearrangend` modifies bottom crum V-displacements **in-place**. [ST-REARRANGE] (Finding 0056) is explicit:

> The operation modifies V-addresses exclusively — it calls `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])` which updates the displacement's V-address component. No I-addresses are touched, no content is copied, no new permascroll entries are created.

No crums are disowned, freed, or recreated. The POOM tree structure is unchanged; only the V-dimension displacement field of each affected crum is mutated.

### What the in-place modification preserves

After rearrange, each crum retains:

- Its `homedoc` field — unchanged
- Its I-dimension origin and width (`cdsp.dsas[I]`, `cwid.dsas[I]`) — unchanged
- Its place in the POOM tree structure — unchanged

Only `cdsp.dsas[V]` changes. This is confirmed by [FC-GRANF-ON-DELETE] (Finding 0061): REARRANGE does not touch the granfilade at all, so I-address allocation state is completely undisturbed.

### How this affects isanextensionnd

`isanextensionnd` checks two conditions [ST-INSERT], Finding 0062:

1. New content has the same `homedoc` as the existing crum
2. New content's I-origin equals the existing crum's I-reach (rightward only)

Because rearrange preserves all I-dimension values and `homedoc` fields, it **cannot break or create I-space contiguity** between crums. If crumA had I-reach at address I.7 before rearrange, it still has I-reach at I.7 after.

However, rearrange *can* change **which crum** a subsequent INSERT finds at a given V-position. Since `findsontoinsertundernd` locates crums by V-address, rearranging crums to new V-positions means a post-rearrange INSERT at V-position P will now encounter whichever crum was moved *to* P — potentially a different crum than was there before.

### The coalescing consequence

This creates a subtle interaction:

**Scenario A — coalescing opportunity preserved:** If crumA (originally at V:1.1–1.4, I-range 5.1–5.4) is moved by rearrange to V:2.1–2.4, and a subsequent INSERT at V:2.4 allocates I-address 5.5 (contiguous with crumA's I-reach and same homedoc), `isanextensionnd` succeeds and extends crumA in place. The rearrange did not disrupt this.

**Scenario B — coalescing opportunity created across formerly-disjoint regions:** Rearrange can bring two crums that were formerly V-adjacent but I-space non-contiguous into positions where a new INSERT between them gets fresh I-addresses — which will be contiguous with neither (since I-address allocation picks up from `max_iaddr(granf) + 1`, irrespective of V-position). No coalescing occurs in this case, but for the same reason it wouldn't have occurred before the rearrange.

**The key contrast with CREATELINK:** [ST-CRUM-BOUND] (Finding 0063) shows that CREATELINK breaks I-address contiguity by consuming I-address space between text insertions. REARRANGE does *not* consume I-address space (no granfilade writes per [FC-GRANF-ON-DELETE]), so it never disrupts the contiguous allocation sequence. A REARRANGE between two text INSERTs leaves the second INSERT able to coalesce with the first, unlike CREATELINK.

### Summary

| Property | After REARRANGE |
|----------|-----------------|
| Crum disowned/recreated | No — in-place `tumbleradd` on `cdsp.dsas[V]` |
| I-space contiguity between crums | Unchanged |
| `homedoc` fields | Unchanged |
| I-reach of any crum | Unchanged |
| Which crum appears at a given V-position | Changed |
| Post-rearrange INSERT coalescing possible | Yes, if I-space contiguity and homedoc conditions hold at the new V-position |
| I-address allocation disrupted | No (unlike CREATELINK) |

The in-place vs. disown distinction matters because disowning would remove crums from the tree entirely, potentially destroying I-space adjacency relationships and `homedoc` associations that `isanextensionnd` depends on. Since rearrange modifies in-place, all such relationships survive intact — the only change visible to `isanextensionnd` is that V-position lookups now route to different crums.

## Code Exploration

Now I have everything I need. Here is the full answer, with all code citations.

---

## `rearrangend`: In-Place Mutation, Not Disown/Recreate

### 1. What `rearrangend` actually does to displacements

`edit.c:78-160` contains the full implementation. After slicing the enfilade at cut points (`makecutsnd`, line 110) and finding the intersection father (`newfindintersectionnd`, line 111), it iterates over all children and applies tumbler offsets:

```c
/* edit.c:124-127 */
case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```

The displacement field `ptr->cdsp.dsas[index]` is modified **in-place** by adding the precomputed offset `diff[i]` and writing the result back into the same field. There is no `disown`, no `createcrum`, no `adopt`. The only structural change is the field value itself; the crum's identity, tree position, and all metadata remain unchanged.

Compare `deletend` (same file, line 59-60), which for crums that fall entirely inside the deleted span **does** call:
```c
disown ((typecorecrum*)ptr);
subtreefree ((typecorecrum*)ptr);
```
`rearrangend` never does this. The contrast is deliberate — deletion removes crums; rearrange slides them.

### 2. The offsets computed by `makeoffsetsfor3or4cuts`

`edit.c:164-184` computes the per-region offsets. For a 3-cut rearrange (the transpose case):

```c
/* edit.c:177-181 */
tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]); // region 1 moves right by len(region 2)
tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]); // diff[2] = blades[1]-blades[0]
diff[2].sign = !diff[2].sign;                                  // region 2 moves LEFT by len(region 1)
tumblerclear (&(diff[3]));                                     // region 3 does not move
```

Region 0 (`case 0`, line 122) and region 3 after blades[2] (`case 4`, same line) do not move. Regions 1, 2, 3 (`case 1, 2, 3`) are shifted. This is a classical segment-transpose: after the rearrange, the former region 2 occupies [blades[0], blades[0]+len(reg2)) and former region 1 occupies immediately after — they are address-adjacent.

### 3. How `prologuend` computes `reach` and what `isanextensionnd` checks

`retrie.c:334-339`:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```
`grasp = offset + cdsp`; `reach = grasp + cwid`. For POOM crums, `cdsp.dsas[V]` is the V-displacement relative to the parent's grasp.

`insertnd.c:301-309`:
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

Two guards before coalescence is allowed:
1. **`homedoc` must match** (`insertnd.c:305`): the new insertion must originate from the same home document as the existing crum.
2. **`reach == origin`** (`insertnd.c:308`): the crum's absolute right endpoint must exactly equal the origin of the new insertion.

When `isanextensionnd` returns TRUE, `insertcbcnd` extends the crum in-place (`insertnd.c:251`):
```c
dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
ivemodified (ptr);
```
No new crum is created; the existing crum simply grows.

### 4. Why the in-place distinction directly affects `isanextensionnd` correctness

The in-place approach in `rearrangend` preserves the entire crum struct except for `cdsp.dsas[index]`. In particular, `((type2dcbc *)ptr)->c2dinfo.homedoc` — the field checked at `insertnd.c:305` — is untouched. After a rearrange, when a subsequent insertion arrives at a post-rearrange crum's `reach`, the `homedoc` check passes correctly and `isanextensionnd` can return TRUE.

Had `rearrangend` used a `disown`/`createcrum`/`adopt` pattern instead:
- The new crum's `c2dinfo` would be zero-initialized (see `createcrum` pattern in `insertcbcnd` at `insertnd.c:260-268`, where `move2dinfo` must be called explicitly to populate it)
- `c2dinfo.homedoc` would be zero unless explicitly copied
- `isanextensionnd` would return FALSE on the `homedoc` guard even when the position arithmetic would otherwise permit extension

The in-place mutation is what guarantees `c2dinfo` fidelity across the rearrange.

### 5. Does `recombine` merge the cut-created adjacent fragments?

After `rearrangend` completes:
```c
/* edit.c:137-141 */
setwispupwards (father,1);
recombine (fullcrumptr);
(void)splitcrumupwards(fullcrumptr);
```

`recombine` dispatches to `recombinend` for POOM (`recombine.c:31-33`). `recombinend` (`recombine.c:104-131`) rebalances the enfilade tree by having underpopulated internal nodes absorb children from siblings via `takeovernephewsnd` and `eatbrossubtreend`. These operations adjust child displacements (via `dspadd`/`dspsub` in `fixdspsofbroschildren`, `recombine.c:259-267`) when changing a child's parent, but they operate on the **tree structure** level, not on the content-address adjacency of bottom crums.

`recombinend` does not scan for pairs of bottom crums whose `reach`/`origin` boundaries coincide and fuse them. There is no such fusion anywhere in the codebase. The fragments produced by `makecutsnd` at cut boundaries remain as separate crums after `recombine`.

`splitcrumupwards` (line 141, `split.c:16-44`) handles only the opposite case — overfull nodes — by calling `splitcrum` → `splitcrumpm` → `peelcrumoffnd` (`split.c:130`). This peels one child off into a new sibling node; again, it operates on tree structure, not on address-space adjacency of bottom crums.

### 6. What this means for `isanextensionnd` coalescence after rearrange

The post-rearrange state is:
- Former region 2 crums have been moved left, ending exactly at the point where former region 1 crums now begin
- These fragments remain **structurally separate** in the enfilade; no post-rearrange step merges them
- Their `cdsp` values are correct (updated in-place), so `prologuend` yields correct `reach` values
- Their `c2dinfo.homedoc` fields are intact (not disturbed by in-place displacement update)

On a **subsequent insertion**:
- If the insertion's `origin` exactly equals the `reach` of a post-rearrange fragment, `isanextensionnd` returns TRUE and the fragment is extended in-place — the extension optimization fires correctly
- But `isanextensionnd` does not merge two *existing* adjacent crums; it only prevents a third crum from being created when a new insertion is contiguous with an existing one
- The cut-created fragments from the rearrange persist as separate crums indefinitely, unless a future insertion happens to land at the precise join point (triggering extension of one, but leaving the other untouched)

### Summary

| Question | Answer | Cite |
|---|---|---|
| Does `rearrangend` modify displacements in-place? | **Yes.** `tumbleradd` writes to `ptr->cdsp.dsas[index]` directly, then `ivemodified` marks it dirty | `edit.c:125-127` |
| Does it disown/recreate? | **No.** No `disown`, `subtreefree`, or `createcrum` calls appear in the rearrange path | `edit.c:113-136` |
| Does `recombine` fuse address-adjacent bottom crums? | **No.** `recombinend` merges underpopulated internal nodes, not address-adjacent leaf crums | `recombine.c:104-131` |
| Does in-place mutation matter for `isanextensionnd`? | **Yes, critically.** In-place preserves `c2dinfo.homedoc`, which is the first guard in `isanextensionnd`; disown/recreate would zero it, silently breaking the extension check | `insertnd.c:305` |
| Can `isanextensionnd` coalesce rearrange-split fragments? | **No** — it can only extend an existing crum when a *new* insertion is contiguous; it has no mechanism to merge two already-existing crums | `insertnd.c:249-258` |

The practical consequence: `makecutsnd` leaves cut-boundary fragments scattered through the enfilade after every rearrange, and they accumulate. The in-place displacement update ensures their addresses are correct and their metadata valid, so future insertions at those boundaries will correctly use the extension path rather than creating yet another fragment — but the accumulated fragments from the rearrange itself are never retroactively fused.

---

## Question 12 [gregory]

> After a PIVOT(a, b, c), do the I-addresses in the swapped regions remain in exactly the same POOM bottom crums (just with modified V-displacements), or can the operation split a single bottom crum into multiple crums if a cut point falls in the interior of an existing span?

### Gregory's Answer

## KB Synthesis

## Pivot and POOM Crum Splitting

The answer is: **a cut point falling in the interior of an existing bottom crum does cause that crum to be split.** The I-addresses remain the same (content identity is fully preserved), but the POOM structural decomposition changes.

### Evidence for Splitting

**[EC-PIVOT-LINK-FRAGMENTATION]** (Finding 0019) is the most direct evidence. A 2-character link ("CD" at V 1.3, width 0.2) subjected to a pivot becomes *four* endset spans:

```
Before: "ABCDEFGH" — link on "CD" at V 1.3 width 0.2
Pivot:  swap BC and DE
After:  "ADEBCFGH" — endsets report FOUR spans:
        - 1.2 width 0.1 (twice)
        - 1.5 width 0.1 (twice)
```

A single 2-char span cannot become four separate spans unless the underlying POOM bottom crum representing "CD" was split during the operation. The two cut points (at positions straddling "CD") fell inside the existing crum, forcing it apart.

**Logical necessity**: REARRANGE classifies each POOM entry into a section via `rearrangecutsectionnd()` [ST-REARRANGE, Finding 0056], then applies a distinct `diff` offset per section via `tumbleradd()`. If a single bottom crum spans a cut boundary, the two halves must receive *different* offsets — which requires splitting the crum first. Without a cutting phase, it would be impossible to apply section-specific displacements to content that straddles a cut point.

**DELETE's analogous mechanism**: [PRE-DELETE] (Finding 0075) documents that `slicecbcpm` is invoked precisely when a knife falls `THRUME` — strictly interior to a crum — splitting it at the cut position. The ndcuts infrastructure (`makecutsbackuptohere`) is shared. REARRANGE uses the same code path (`rearrangend()` is in `edit.c:78-184`, adjacent to `deletend()`), which includes this cutting machinery.

### What Is and Is Not Preserved

**What changes:** The POOM bottom crum structure. A crum covering [1.3, 1.5) may become two crums at new V-positions after the pivot. The count of crums in the POOM can increase.

**What does not change:** The I-addresses. Per [INV-REARRANGE-IDENTITY] (Finding 0056):

> "The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched. No I-addresses are allocated, no content is duplicated in the permascroll, and **the same enfilade nodes (crums) are retained**."

The phrase "same enfilade nodes are retained" refers to the *granfilade content atoms* (no new text is written to the permascroll). It does not mean the POOM node topology is frozen — it means the identity mapping survives. Crum splitting in the POOM rearranges *how* I-addresses are indexed, without changing *which* I-addresses are present or their content.

### Summary

| Property | After PIVOT cut falls inside a crum |
|----------|-------------------------------------|
| I-addresses | **Unchanged** (INV-REARRANGE-IDENTITY) |
| Permascroll content | **Unchanged** (no new allocations) |
| POOM bottom crum count | **Can increase** (crum split at cut boundary) |
| V-displacement per section | **Different** offsets applied per section |
| Granfilade content atoms | **Unchanged** |

The fragmentation observed in [EC-PIVOT-LINK-FRAGMENTATION] is a direct consequence of this splitting: what was one crum covering "CD" becomes two (or more) crums at different V-positions after the pivot applies different displacements to each half.

## Code Exploration

Now I have everything. Let me synthesize the full answer.

---

## Answer: Does PIVOT Split Bottom Crums?

**Yes — unambiguously. When a PIVOT cut point falls strictly inside an existing POOM bottom crum's V-span, `makecutsnd` calls `slicecbcpm` to split that crum into two.** The I-addresses are preserved in both halves via `move2dinfo`.

---

### 1. The Call Chain

PIVOT is the REARRANGE operation. The dispatch is:

```
rearrange()           [fns.c:159]
  → dorearrange()     [do1.c:34-43]
    → rearrangepm()   [orglinks.c:137-142]
      → rearrangend() [edit.c:78]   (index = V)
```

`rearrangepm` [orglinks.c:137-142] is a one-liner wrapper:
```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

---

### 2. `rearrangend` — Two Distinct Phases

In `edit.c:78-160`, the function has two phases:

**Phase 1 (line 110): Cut the enfilade**
```c
makecutsnd (fullcrumptr, &knives);          // edit.c:110
```

**Phase 2 (lines 113-136): Classify and shift sons**
```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = ...) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case 0: case 4:            break;   // never moves
      case 1: case 2: case 3:             // moves
        tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
        ivemodified((typecorecrum*)ptr);
        break;
    }
}
```

The shift in Phase 2 **only modifies `ptr->cdsp.dsas[V]`** — the V-displacement. The I-dimension (`cdsp.dsas[I]`) and all content pointers are untouched.

---

### 3. Phase 1: `makecutsnd` Splits Bottom Crums

`makecutsnd` in `ndcuts.c:15-31` calls `makecutsdownnd` which calls `makecutsbackuptohere`. The critical bottom-crum branch is at `ndcuts.c:77-91`:

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset,
                        &knives->blades[i], knives->dimension) == THRUME) {
            new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new,
                       &knives->blades[i], knives->dimension);
            ivemodified((typecorecrum*)ptr);
            ivemodified((typecorecrum*)new);
        }
    }
    return(0);
}
```

The condition is `whereoncrum() == THRUME`. `THRUME` is defined as `0` in `common.h:88`, part of the ordered set:

```c
#define TOMYLEFT       -2   // cut strictly left of crum
#define ONMYLEFTBORDER -1   // cut on left edge of crum
#define THRUME          0   // cut strictly INSIDE crum
#define ONMYRIGHTBORDER 1   // cut on right edge
#define TOMYRIGHT       2   // cut strictly right of crum
```

`whereoncrum` [retrie.c:345-398] for a POOM crum computes:
- `left = offset.dsas[V] + ptr->cdsp.dsas[V]`
- `right = left + ptr->cwid.dsas[V]`

and returns `THRUME` when `left < cut_point < right` — strictly interior.

**If the cut falls on either border, no split occurs.** Split only fires for strictly interior cuts.

---

### 4. `slicecbcpm` — The Actual Split Mechanism

In `ndcuts.c:373-450`:

```c
int slicecbcpm(typecorecrum *ptr, typewid *offset, typecorecrum *new,
               tumbler *cut, INT index)
{
    prologuend (ptr, offset, &grasp, NULL);
    // assert: whereoncrum(ptr, offset, cut, index) == THRUME

    tumblersub (cut, &grasp.dsas[index], &localcut);  // localcut = cut - ptr_left

    // Build newwid = the width for the left piece [ptr_start, cut)
    movewisp (&ptr->cwid, &newwid);
    for (i = 0; i < widsize(enftype); i++) {
        newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
        tumblerjustify (&newwid.dsas[i]);
    }
    // new->cwid = original_wid - newwid   (right piece: [cut, ptr_end))
    locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid,
                  (tumbler*)&new->cwid, (unsigned)widsize(enftype));
    // ptr keeps the left piece
    movewisp (&newwid, &ptr->cwid);
    // new->cdsp = ptr_origin + ptr_new_width = cut
    dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);

    // *** Copy I-address info to the new crum ***
    move2dinfo (&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);

    // Insert new as right sibling of ptr
    adopt(new, RIGHTBRO, ptr);
}
```

`move2dinfo` is defined in `wisp.h:110`:
```c
#define move2dinfo(A,B) movmem((A),(B),sizeof(type2dbottomcruminfo))
```

This does a full memory-copy of the `type2dbottomcruminfo` struct (containing `homedoc` and related I-coordinate data [enf.h:108-131]) from `ptr` to `new`. Both resulting crums point to **the same underlying I-space content**.

After the split:
- `ptr` covers V-span `[cut_point_left, cut_point)` with the original I-address
- `new` covers V-span `[cut_point, original_right)` with the same I-address (copied)

---

### 5. After Cutting: Only V-Displacements Move

Back in `rearrangend` Phase 2, `rearrangecutsectionnd` [edit.c:191-204] classifies each son (which may now be a fragment of a formerly-larger bottom crum) into its between-knife region:

```c
INT rearrangecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    for (i = knives->nblades - 1; i >= 0; --i) {
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME)           return (-1);   // error: should never happen now
        else if (cmp <= ONMYLEFTBORDER) return (i+1);
    }
    return (0);
}
```

Since Phase 1 already ensured no bottom crum straddles any knife, `THRUME` here is an error path. Each crum is placed cleanly in one region (0 through N), and the corresponding V-displacement from `diff[]` is added:

```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);  // edit.c:125
```

Only `cdsp.dsas[V]` changes. The I-dimension (`cdsp.dsas[I]`), the crum's `cwid.dsas[I]`, and the `c2dinfo` (`homedoc`) are all untouched.

---

### Summary

| Condition | What happens |
|-----------|-------------|
| Cut point falls strictly inside a bottom crum's V-span (`THRUME`) | `slicecbcpm` splits the crum into two adjacent bottom crums, each covering half the original V-range; both carry copies of the original I-address (`c2dinfo`) |
| Cut point falls exactly on a crum's V-boundary (`ONMYLEFTBORDER` / `ONMYRIGHTBORDER`) | No split; the existing crum boundary already aligns with the cut |
| After all cuts | Each resulting crum (split or not) gets its V-displacement adjusted by `tumbleradd`; I-addresses are not touched |

**The I-addresses do not "remain in exactly the same POOM bottom crums."** A cut interior to a span creates a new bottom crum by splitting the old one. Both pieces retain the same I-address information (same `homedoc`), but they are now two distinct tree nodes covering adjacent V-intervals. The only thing that differs between the two halves is the V-span they represent — the I-content reference is identical in both.

---

## Question 13 [gregory]

> Does REARRANGE create any spanfilade entries (DOCISPAN or otherwise), or is it purely a POOM-local mutation — meaning `spanf' = spanf` is a strict frame condition?

### Gregory's Answer

## KB Synthesis

**REARRANGE is purely a POOM-local mutation. `spanf' = spanf` is a strict frame condition.**

## Evidence

**Mechanism confirms no spanfilade writes.** [ST-REARRANGE] (Finding 0056) is definitive: `rearrangend()` operates exclusively by calling `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])` on POOM entries. The finding states explicitly: "No I-addresses are touched, no content is copied, no new permascroll entries are created." There are no calls to `insertspanf`, `docopy`, or `inserttextingranf` anywhere in the REARRANGE code path (`edit.c:78-184`).

**The operation classification in [FC-GRANF-ON-DELETE] (Finding 0061)** groups DELETE and REARRANGE together as granf-preserving: "`∀ op ∈ {DELETE, REARRANGE} : granf_after(op) = granf_before(op)`." Since DOCISPAN entries are written by `insertspanf(..., DOCISPAN)`, which is only triggered from `docopy()` when content is placed into a document, and REARRANGE calls neither, no DOCISPAN entries are created or modified.

**[INV-REARRANGE-IDENTITY]** (Findings 0016, 0018, 0056) states the I-address multiset is invariant: `i_addresses(doc_after) = i_addresses(doc_before)`. DOCISPAN entries record which documents contain which I-addresses. Since the I-address associations are unchanged and no new I-address placements occur, there is nothing to index.

**Link discoverability is preserved without spanfilade changes.** [INV-REARRANGE-LINK-SURVIVAL] (Finding 0016) confirms links remain discoverable after pivot/swap — not because the spanfilade is updated, but because the spanfilade is *unchanged* and I-addresses are already indexed. This would be impossible if REARRANGE needed to write new spanfilade entries.

## Contrast with Operations That Do Touch spanf

| Operation | spanf change | Mechanism |
|-----------|-------------|-----------|
| INSERT | DOCISPAN written | `doinsert` → `docopy` → `insertspanf(..., DOCISPAN)` |
| COPY/VCOPY | DOCISPAN written | `docopy` → `insertspanf(..., DOCISPAN)` |
| CREATELINK | Link endsets indexed | `docreatelink` → `insertendsetsinspanf` |
| APPEND | None | `insertspanf` call commented out [EC-APPEND-NO-DOCISPAN] |
| DELETE | None | `deletevspanpm` → `deletend` only; no spanf call [ST-DELETE, Finding 0057] |
| **REARRANGE** | **None** | `rearrangend` → `tumbleradd` only; no spanf call |

## Formal Statement

`spanf' = spanf` holds unconditionally for REARRANGE. This follows from:
1. No `insertspanf` calls in the REARRANGE code path
2. No new I-address placements (pure V-address permutation per [INV-REARRANGE-IDENTITY])
3. No removal of I-address placements (V-space only mutation, unlike DELETE which also leaves spanf unchanged per [INV-SPANF-WRITE-ONLY])

The combined postcondition is: REARRANGE modifies only `poom(doc)` — the V-address component of displacement tumblers — leaving both `granf` (content bytes, permascroll, I-address allocations) and `spanf` (DOCISPAN index, link endset index) strictly unchanged.

## Code Exploration

I have everything needed for a complete, citation-backed answer.

---

## REARRANGE is Purely POOM-Local: `spanf' = spanf` is a Strict Frame Condition

### The Full Call Chain

**`fns.c:159-173` — top-level FEBE handler:**
```c
void rearrange(typetask *taskptr) {
    getrearrange(taskptr, &docisa, &cutseq);
    putrearrange(taskptr);
    if (!dorearrange(taskptr, &docisa, &cutseq))  // ← the whole work
        ...
}
```

**`do1.c:34-43` — `dorearrange`:**
```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr) {
    return (
        findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
     && rearrangepm(taskptr, docisaptr, docorgl, cutseqptr)
        /*&& TRUE*/ /* ht stuff */   ← commented out, never executes
    );
}
```

**`orglinks.c:137-142` — `rearrangepm`:**
```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr) {
    rearrangend((typecuc*)docorgl, cutseqptr, V);   // ← POOM tree edit
    logbertmodified(docisaptr, user);                // ← mark bert dirty
    return (TRUE);
}
```

**`edit.c:78-160` — `rearrangend`:** (the actual engine)
```c
int rearrangend(typecuc *fullcrumptr, typecutseq *cutseqptr, INT index) {
    // 1. Build knife array from cutseq
    // 2. makeoffsetsfor3or4cuts() — pure arithmetic [edit.c:108]
    makecutsnd(fullcrumptr, &knives);               // [edit.c:110] split leaf crums
    newfindintersectionnd(fullcrumptr, &knives,      // [edit.c:111] find intersection node
                          &father, &foffset);
    prologuend((typecorecrum*)father, ...);          // [edit.c:112] compute fgrasp
    for (ptr = findleftson(father); ptr; ...) {
        i = rearrangecutsectionnd(ptr, &fgrasp, &knives);  // [edit.c:114] classify
        switch (i) {
          case 1: case 2: case 3:
            tumbleradd(&ptr->cdsp.dsas[index],       // [edit.c:125] shift V-displacement
                       &diff[i], &ptr->cdsp.dsas[index]);
            ivemodified((typecorecrum*)ptr);          // [edit.c:127] mark crum dirty
        }
    }
    setwispupwards(father, 1);   // [edit.c:137]
    recombine(fullcrumptr);      // [edit.c:139]
    splitcrumupwards(fullcrumptr); // [edit.c:141]
}
```

### Exhaustive Spanfilade Search

A grep for `insertspanf` and `SPANRANGE` across the entire REARRANGE call graph (`edit.c`, `ndcuts.c`, `genf.c`) returns **no matches**. The spanfilade is not touched at any layer:

| File | `insertspanf` | `SPANRANGE` |
|------|--------------|-------------|
| `edit.c` | ✗ | ✗ |
| `ndcuts.c` | ✗ | ✗ |
| `genf.c` | ✗ | ✗ |

### The Decisive Contrast: `docopy` vs `dorearrange`

`docopy` [`do1.c:53-65`] explicitly calls **both** a POOM write and a spanfilade write:

```c
return (
   specset2ispanset(...)
&& findorgl(...)
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)   // POOM write
&&  insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // spanfilade write ← KEY
);
```

`dorearrange` [`do1.c:34-43`] has **no `insertspanf` call**. The `/* ht stuff */` comment at `do1.c:42` is a disabled stub that was present in `docopy` and `dodeletevspan` alike — it was never filled in for REARRANGE.

### Why This Is Correct by Design

The spanfilade records `(docISA, V-position) → I-span` mappings. These are used to resolve transclusion: given a V-address in a document, find the permascroll bytes.

REARRANGE changes V-positions of existing crums but **allocates no new permascroll content** — no new I-space addresses are created. The existing `(I-span, V-span)` pairs recorded in the spanfilade remain valid because the underlying permascroll identities are unchanged. Only the POOM's internal V-displacement fields (`ptr->cdsp.dsas[V]`) are updated.

An `insertspanf` call would be incorrect here: it would duplicate existing DOCISPAN entries with new V-positions, corrupting the mapping.

### Conclusion

**`spanf' = spanf` is a strict frame condition for REARRANGE.** The operation is purely POOM-local:

1. `makecutsnd` [`ndcuts.c:15`] — splits POOM leaf crums at cut boundaries
2. `rearrangecutsectionnd` + `tumbleradd` on `cdsp.dsas[V]` [`edit.c:114-127`] — shifts V-displacements of the affected crums
3. `recombine` + `splitcrumupwards` [`edit.c:139-141`] — rebalances the POOM enfilade

No spanfilade function is invoked anywhere in the call tree.

---

## Question 14 [gregory]

> In `makeoffsetsfor3or4cuts`, what happens when a cut point falls exactly on an existing crum boundary versus in the interior of a crum — does `rearrangecutsectionnd` use the same `whereoncrum` / `slicecbcpm` machinery as DELETE, or a different slicing path?

### Gregory's Answer

## KB Synthesis

## What the KB Tells Us

### DELETE's cutting machinery

[PRE-DELETE / Finding 0075] documents DELETE's two-phase approach explicitly. Phase 1 uses `makecutsbackuptohere()` (`ndcuts.c:77-90`), which calls `whereoncrum()` and only invokes `slicecbcpm` when the result is `THRUME` — meaning the cut falls **strictly interior** (`grasp < cut < reach`). Boundary-aligned cuts (`ONMYLEFTBORDER`, `ONMYRIGHTBORDER`) skip `slicecbcpm` entirely; the crum is handled whole in Phase 2. This five-way spatial classification (`whereoncrum`) is the gating mechanism for crum splitting.

### REARRANGE's different path

[ST-REARRANGE / Finding 0056] describes `rearrangend()` in four steps:

1. Sort cuts — `sortknives()`
2. Compute offsets — `makeoffsetsfor3or4cuts()` derives tumbler displacements from cut positions alone
3. Classify spans — `rearrangecutsectionnd()` assigns each orgl to a region (0–4)
4. Apply offsets — `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], ...)` shifts V-position in place

**No Phase 1 cutting is documented for REARRANGE.** The findings consistently describe the operation as modifying only the V-address displacement of existing orgls — "no content is copied, no new permascroll entries are created" [ST-REARRANGE / Finding 0056]. The code reference is `edit.c:78-184`, which contains no calls to `slicecbcpm` or `makecutsbackuptohere` per the findings.

[ST-REARRANGE / Finding 0051] confirms this directly: "`rearrangend()` calls `makeoffsetsfor3or4cuts()` to compute displacement vectors from the cut points, then applies `tumbleradd` to shift each orgl's V-position by the computed offset."

### The boundary question

The KB does not specify what `rearrangecutsectionnd` does when a cut point falls exactly on a crum boundary — this is a gap in the documented findings. However, several structural facts constrain the answer:

- Since there is no documented slicing phase in REARRANGE, crums are classified and displaced **whole**, not split
- `rearrangecutsectionnd` classifies each orgl into a numbered region based on where its V-position falls relative to the sorted cut points; the five-way `whereoncrum` result may inform this classification, but its role is **region assignment**, not crum splitting
- [EC-REARRANGE-EMPTY-REGION] notes that regions with no content are silently skipped — consistent with whole-orgl classification rather than sub-crum precision

### Summary

REARRANGE uses a **different path** from DELETE. DELETE needs `whereoncrum`/`slicecbcpm` because it must precisely excise a range — any crum straddling a deletion boundary must be split to avoid partial deletion. REARRANGE only needs to know **which displacement to apply** to each orgl; whole-orgl assignment suffices because each orgl is moved as a unit. A boundary-aligned cut in REARRANGE is handled by `rearrangecutsectionnd` assigning the orgl to one region or the other, with no crum splitting. The KB does not document which region a boundary-straddling crum gets assigned to, so that specific behavior is not answerable from the KB.

## Code Exploration

---

## `makeoffsetsfor3or4cuts` and the Rearrange Slicing Path

### The `whereoncrum` return-value landscape

`common.h:86-90` defines five ordered positions a knife can occupy relative to a crum:

```
TOMYLEFT (-2)  ONMYLEFTBORDER (-1)  THRUME (0)  ONMYRIGHTBORDER (1)  TOMYRIGHT (2)
```

`retrie.c:345-398` implements `whereoncrum` for SPAN/POOM. It computes:
- `left  = offset.dsas[index] + ptr->cdsp.dsas[index]`
- `right = left + ptr->cwid.dsas[index]`

Then returns `ONMYLEFTBORDER` if `address == left`, `THRUME` if `left < address < right`, `ONMYRIGHTBORDER` if `address == right`, etc.

---

### Phase 1 — Pre-slicing with `makecutsnd` / `slicecbcpm`

Before `rearrangecutsectionnd` is ever called, `rearrangend` first calls `makecutsnd` at `edit.c:110`:

```c
makecutsnd (fullcrumptr, &knives);   // edit.c:110
```

Inside `makecutsnd` → `makecutsdownnd` → `makecutsbackuptohere`, every **leaf crum** (height == 0) is examined against every knife (`ndcuts.c:78-90`):

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
            new = createcrum(...);
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
            ...
        }
    }
```

`slicecbcpm` is triggered **only when `whereoncrum == THRUME`** — i.e., only when the knife falls **strictly inside** the crum. `ndcuts.c:373-450` confirms this: `slicecbcpm` itself asserts at entry that `whereoncrum(...) == THRUME`, and crashes otherwise (`ndcuts.c:383-388`).

**When the cut point falls exactly on an existing crum boundary:**
- Left boundary: `whereoncrum` returns `ONMYLEFTBORDER` = -1. **`slicecbcpm` is not called.** The crum is already cleanly split there.
- Right boundary: `whereoncrum` returns `ONMYRIGHTBORDER` = 1. Same — no split needed.

So `slicecbcpm` machinery is **strictly for interior splits**. Boundary-aligned knives pass through the pre-slicing phase without touching any crum's width.

---

### `makeoffsetsfor3or4cuts` — what the offsets mean

`edit.c:164-184`:

```c
int makeoffsetsfor3or4cuts(typeknives *knives, tumbler diff[])
{
    /* diff[0] is simply ignored */
    if (knives->nblades == 4) {
        tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));         // diff[1] = blade[2]-blade[0]
        tumblersub (&knives->blades[1], &knives->blades[0], &a);                 // a = blade[1]-blade[0]
        tumblersub (&knives->blades[3], &knives->blades[2], &b);                 // b = blade[3]-blade[2]
        tumblersub (&b, &a, &(diff[2]));                                         // diff[2] = b-a
        movetumbler (&diff[1], &diff[3]);
        diff[3].sign = !diff[1].sign;                                            // diff[3] = -diff[1]
    } else if (knives->nblades == 3) {
        tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);           // diff[1] = blade[2]-blade[1]
        tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]);           // diff[2] = blade[1]-blade[0] ...
        diff[2].sign = !diff[2].sign;                                            // ...then negated
        tumblerclear (&(diff[3]));                                               // diff[3] = 0
    } else
        gerror ("Wrong number of cuts.");
}
```

The `diff[]` array encodes **how far each between-knife section must shift**. Sections are numbered by which knife they sit just to the right of:

| Section | Position | 4-cut shift | 3-cut shift |
|---------|----------|-------------|-------------|
| 0 | left of all knives | not moved | not moved |
| 1 | between blade[0] and blade[1] | `diff[1]` = blade[2]−blade[0] | `diff[1]` = blade[2]−blade[1] |
| 2 | between blade[1] and blade[2] | `diff[2]` = (blade[3]−blade[2]) − (blade[1]−blade[0]) | `diff[2]` = −(blade[1]−blade[0]) |
| 3 | between blade[2] and blade[3] (4-cut only) | `diff[3]` = −diff[1] | `diff[3]` = 0 (no-op) |
| 4 | right of all knives (4-cut only) | not moved | — |

Note the commented-out formula for 4-cut `diff[3]` at `edit.c:174`:
```c
/*  tumblersub (&knives->blades[0], &knives->blades[2], &(diff[3]));*//* should be <0 */
```
This was replaced by the sign-flip trick (`diff[3] = -diff[1]`), which gives the same result since `blade[0]−blade[2] = −(blade[2]−blade[0]) = −diff[1]`.

---

### Phase 2 — Classification with `rearrangecutsectionnd`

`edit.c:191-204`:

```c
INT rearrangecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    INT i, cmp;
    for (i = knives->nblades -1; i >= 0 ; --i) {
        cmp = whereoncrum (ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME) {
            return (-1);                   // error: crum was not pre-split
        } else if (cmp <= ONMYLEFTBORDER) {
            return (i+1);                  // blade[i] is at-or-left of crum's start
        }
    }
    return (0);
}
```

The loop walks knives **right-to-left**. For each knife, it asks: is this knife at or to the left of this crum's left boundary? The first (rightmost) knife that satisfies `cmp <= ONMYLEFTBORDER` establishes which section the crum is in: `i+1`.

**The critical boundary case:** `cmp <= ONMYLEFTBORDER` catches both `TOMYLEFT` (−2) and `ONMYLEFTBORDER` (−1). When a knife lands **exactly on a crum's left border**, the crum is classified exactly the same as if the knife were strictly to its left. The crum belongs to section `i+1` — the section whose left edge is that knife. There is no ambiguity and no special-case branching. A crum whose left border coincides with a knife is placed into the section **starting** at that knife.

The `THRUME` (= 0) guard acts as a post-condition assertion: after `makecutsnd` has done its work, no crum should be cut through by any knife. If one is, `rearrangecutsectionnd` returns −1, which causes `rearrangend` to call `gerror("rearrangend can't classify crum")` (`edit.c:118`).

---

### Comparison with DELETE

`deletecutsectionnd` (`edit.c:235-248`) is **structurally identical** to `rearrangecutsectionnd`:

```c
INT deletecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    INT i, cmp;
    for (i = knives->nblades-1; i >= 0; --i) {
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME) {
            return (-1);
        } else if (cmp <= ONMYLEFTBORDER) {
            return (i+1);
        }
    }
    return (0);
}
```

Same loop structure, same `whereoncrum` call, same `<= ONMYLEFTBORDER` test, same `THRUME` → −1 error path. The comment in `insertcutsectionnd` (`edit.c:209`) even acknowledges the heritage explicitly: `/*hacked from delete*/`.

**Both DELETE and REARRANGE use the exact same `whereoncrum`/`slicecbcpm` machinery.** The difference is only in what the caller does with the returned section number:

- `deletend` (`edit.c:49`): switch on return value → **disown+free** (section = 1) or **subtract width** (section = 2)
- `rearrangend` (`edit.c:114`): switch on return value → **add `diff[i]` displacement** (sections 1–3), leave section 0 and 4 unmoved

There is no separate "rearrange-specific" slicing path. The pre-split phase (`makecutsnd`→`slicecbcpm`) and the classification phase (`whereoncrum` with `<= ONMYLEFTBORDER`) are completely shared between delete and rearrange.

---

### Summary

1. **Interior cut** (`whereoncrum == THRUME`): `slicecbcpm` is called in the pre-split phase to physically split the leaf crum into two siblings. This happens identically for both DELETE and REARRANGE, before either `deletecutsectionnd` or `rearrangecutsectionnd` is invoked.

2. **Boundary-aligned cut** (`whereoncrum == ONMYLEFTBORDER` or `ONMYRIGHTBORDER`): no split occurs. The crum boundary already coincides with the knife. During classification, `ONMYLEFTBORDER` satisfies `cmp <= ONMYLEFTBORDER` and the crum is placed into section `i+1` — the section that begins at that knife.

3. `rearrangecutsectionnd` and `deletecutsectionnd` are the same function with the same `whereoncrum` logic. `makeoffsetsfor3or4cuts` precomputes per-section displacement vectors (`diff[1..3]`) that are then applied by the caller after classification — this is the only thing unique to rearrange.

---

## Question 15 [gregory]

> For a 4-cut SWAP(a, b, c, d), how are the three offsets computed for the three regions `[a,b)`, `[b,c)`, and `[c,d)` — specifically, does the middle region `[b,c)` get a net-zero offset when the swapped regions have equal width, and what happens to V-addresses when they have unequal width?

### Gregory's Answer

## KB Synthesis

## 4-Cut SWAP Offset Computation

The authoritative source is [ST-REARRANGE] (Finding 0056), which gives the concrete formulas extracted from `backend/edit.c:164-184` (`makeoffsetsfor3or4cuts`).

### The Three Offsets

For SWAP with cuts `a < b < c < d` (regions `[a,b)`, `[b,c)`, `[c,d)`):

| Region | Offset | Formula |
|--------|--------|---------|
| Region1 `[a,b)` | diff[1] | `+(c − a)` |
| Region2 `[b,c)` | diff[2] | `(d−c) − (b−a)` = `|R3| − |R1|` |
| Region3 `[c,d)` | diff[3] | `−(c − a)` |

These are applied by `tumbleradd` in-place to each POOM crum's V-dimension displacement. No I-addresses are touched ([INV-REARRANGE-IDENTITY], [ST-REARRANGE] Finding 0056).

---

### Equal-Width Case: Clean Swap

When `|R1| = b−a = d−c = |R3|`:

- **diff[2] = 0** — middle region `[b,c)` does not move
- Region1 lands exactly at `[c, c+|R1|)` — where Region3 started
- Region3 lands exactly at `[a, a+|R3|)` — where Region1 started
- All three regions partition the same total extent without gaps or overlaps

This is the KB's concrete example ([ST-REARRANGE] Finding 0056):

```
"ABCDEFGH", cuts at 1.2, 1.4, 1.6, 1.8:
  BC [1.2,1.4): +0.4 → [1.6,1.8)
  DE [1.4,1.6):  0   → [1.4,1.6)   (net zero, stays)
  FG [1.6,1.8): −0.4 → [1.2,1.4)
  Result: "AFGDEBCH" ✓
```

---

### Unequal-Width Case: Middle Shifts, V-Addresses Collide

When `|R1| ≠ |R3|`, diff[2] is non-zero. Tracing the post-swap positions:

- Region3 → `[a, a+|R3|)` (starts where R1 started)
- Region2 → `[a+|R3|, a+|R3|+|R2|)` (abutts Region3)
- Region1 → `[c, c+|R1|)` (starts at `c = a+|R1|+|R2|`)

For Region2 end = Region1 start, we need:

```
a + |R3| + |R2|  =  a + |R1| + |R2|
         |R3|    =  |R1|
```

This is only satisfied for equal widths. When widths differ:

- `|R3| > |R1|`: Region2 extends **past** Region1's start → V-address **overlap** in the POOM
- `|R3| < |R1|`: Region2 ends **before** Region1's start → V-address **gap**

[ST-REARRANGE] (Finding 0016) acknowledges this: *"the spec must distinguish between content preservation (the characters/identities are the same) and address preservation (V-addresses may shift for the middle segment if regions differ in size)."* However, the KB does not describe what happens to the POOM tree when the resulting V-positions overlap — this is a gap in KB coverage.

---

### Implementation Notes

- Cut points are sorted ascending before offset computation via `sortknives()`, so input order is irrelevant ([PRE-REARRANGE] Finding 0056)
- Operations are in pre-move address space: offsets are computed from `knives->blades[]` alone, with no reference to post-move state
- No subspace boundary check is performed — SWAP with cuts spanning the text/link boundary will displace content across subspaces ([EC-REARRANGE-CROSS-SUBSPACE], [PRE-REARRANGE] Finding 0051)
- An empty region (e.g., `a = b`) contributes zero to offset arithmetic and produces no POOM changes for that section ([EC-REARRANGE-EMPTY-REGION])
- I-addresses are never modified; the operation is a pure V-address permutation ([INV-REARRANGE-IDENTITY])

---

### Summary

The middle region `[b,c)` gets **net-zero offset if and only if the two swapped regions have equal width**. For unequal widths, it shifts by `|R3| − |R1|`. Based on the formulas in [ST-REARRANGE] (Finding 0056), this produces V-address collisions between the shifted middle and Region1 — a structural consequence the KB does not explicitly resolve for the unequal case.

## Code Exploration

Now I have everything I need. Here is the complete answer with full code citations.

---

## 4-Cut SWAP Offset Computation in udanax-green

### The Core Function: `makeoffsetsfor3or4cuts` — `edit.c:164–184`

```c
int makeoffsetsfor3or4cuts(typeknives *knives, tumbler diff[])
{
  tumbler a, b;

    /* diff[0] is simply ignored */
    if (knives->nblades == 4) {
        tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));
        tumblersub (&knives->blades[1], &knives->blades[0], &a);
        tumblersub (&knives->blades[3], &knives->blades[2], &b);
        tumblersub (&b, &a, &(diff[2]));
/*      tumblersub (&knives->blades[0], &knives->blades[2], &(diff[3]));*//* should be <0 */
        movetumbler (&diff[1], &diff[3]);
        diff[3].sign = !diff[1].sign;
    } ...
}
```

After `sortknives` (`edit.c:250`), the four cut positions are stored as:
- `blades[0]` = **a**
- `blades[1]` = **b**
- `blades[2]` = **c**
- `blades[3]` = **d**

with the invariant a < b < c < d. Naming `w₁ = b − a` (width of region 1) and `w₂ = d − c` (width of region 3):

---

### The Three Offsets — Exactly as Computed

| diff index | Region | Code | Value |
|---|---|---|---|
| `diff[1]` | [a, b) | `tumblersub(blades[2], blades[0], …)` | **c − a** |
| `diff[2]` | [b, c) middle | `b = d−c; a = b−a; diff[2] = b − a` | **w₂ − w₁** |
| `diff[3]` | [c, d) | `movetumbler(diff[1]); diff[3].sign = !diff[1].sign` | **−(c − a)** |

Note on naming: the local `a` and `b` tumblers in `makeoffsetsfor3or4cuts` shadow the conceptual positions — they hold widths, not positions. `a` = `blades[1] − blades[0]` = w₁, `b` = `blades[3] − blades[2]` = w₂. The commented-out line `/* should be <0 */` [`edit.c:174`] confirms the sign of diff[3].

---

### How Offsets Are Applied — `rearrangend`, `edit.c:113–136`

```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = ...) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case 0:  case 4: /* these never move */
          break;
      case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
          tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
          ...
    }
}
```

`rearrangecutsectionnd` (`edit.c:191`) returns which zone each crum is in: 1 = [a,b), 2 = [b,c), 3 = [c,d). The offset is then added **in-place** to the crum's V-axis displacement `cdsp.dsas[index]`. I-addresses are never touched.

---

### Equal-Width Case: Middle Gets Zero Offset

When **w₁ = w₂**:

```
diff[2] = w₂ − w₁ = 0
```

The middle region [b, c) receives a zero tumbler offset. Its V-positions are **unchanged**.

The complete resulting layout (adding offsets to absolute V-addresses):
- `[c, d)` content: `v + (a − c)` → maps to **[a, a+w₂)** = [a, b) exactly ✓
- `[b, c)` middle: `v + 0` → stays at **[b, c)** ✓
- `[a, b)` content: `v + (c − a)` → maps to **[c, c+w₁)** = [c, d) exactly ✓

Regions fit together perfectly, no gaps or overlaps. This is the only case all three existing swap golden tests exercise:
- `swap_non_adjacent`: "BC" (2) ↔ "FG" (2) → "AFGDEBCH" [`golden/rearrange/swap_non_adjacent.json`]
- `swap_first_and_last`: "H" (1) ↔ "O" (1) → "OELLH" [`golden/rearrange/swap_first_and_last.json`]
- `swap_words_in_sentence`: "quick" (5) ↔ "brown" (5) → "The brown quick fox" [`golden/rearrange/swap_words_in_sentence.json`]

---

### Unequal-Width Case: V-Address Collision in the Middle

When **w₁ ≠ w₂**, the three resulting ranges are:

| Origin | New range |
|---|---|
| `[c, d)` (w₂ wide) | `[a, a+w₂)` |
| `[b, c)` middle | `[b + (w₂−w₁), c + (w₂−w₁))` |
| `[a, b)` (w₁ wide) | `[c, c+w₁)` |

Check boundary 1 — `[c,d)` end vs middle start:
- End of `[c,d)` moved: `a + w₂`
- Start of middle moved: `b + w₂ − w₁ = (a + w₁) + w₂ − w₁ = a + w₂` ✓ **contiguous**

Check boundary 2 — middle end vs `[a,b)` start:
- End of middle moved: `c + (w₂ − w₁)`
- Start of `[a,b)` moved: `c` (always)
- **When w₂ > w₁**: end > start → **OVERLAP** — the shifted middle region extends into the same V-addresses as the repositioned [a,b) content
- **When w₂ < w₁**: end < start → **GAP** — a hole appears between the middle and the repositioned [a,b) content
- **When w₂ = w₁**: end = start = c → perfect ✓

This is a structural consequence of the offset formula. The code has no guard for unequal widths — it silently proceeds. The result is two crums claiming the same V-address range (overlap case), producing ambiguous or duplicate content on retrieval, or a V-address hole that can never be read.

There is no validation at the FEBE handler level either. `fns.c:159` shows `rearrange()` unconditionally calls `dorearrange()` after deserializing the cut sequence:

```c
void rearrange(typetask *taskptr) {
    (void) getrearrange (taskptr, &docisa, &cutseq);
    putrearrange (taskptr);
    if (!dorearrange (taskptr, &docisa, &cutseq))
        fprintf(stderr,"rearrange failed \n");
}
```

No width-equality check exists anywhere between `fns.c` and `makeoffsetsfor3or4cuts`. The invariant is caller-enforced only.

---

### Summary Table

| Condition | diff[1] | diff[2] | diff[3] | [b,c) result |
|---|---|---|---|---|
| Any | `c − a` | `w₂ − w₁` | `a − c` | shifts by `w₂ − w₁` |
| w₁ = w₂ | `c − a` | **0** | `a − c` | net-zero, stays at [b,c) |
| w₁ ≠ w₂ | `c − a` | **≠ 0** | `a − c` | V-collision with [a,b) content |

**Key code loci:**
- Offset formula: `edit.c:164–184` (`makeoffsetsfor3or4cuts`)
- Offset application: `edit.c:113–136` (`rearrangend`)
- Region classification: `edit.c:191–204` (`rearrangecutsectionnd`)
- No width validation: `fns.c:159–173` (`rearrange`)

---

## Question 16 [gregory]

> If a link's source endset spans content that REARRANGE splits across non-contiguous V-positions (e.g., a single-span endset `[1.1,1.5]` becomes `[1.1,1.2]` and `[1.4,1.5]` after a pivot), does `retrieveendsets` return one VSpec or two — and is the I-address span still reported as a single contiguous range?

### Gregory's Answer

## KB Synthesis

## Answer

This question spans the intersection of the rearrange operation, the three-layer link model, and the endset retrieval mechanism. The answer requires distinguishing what changes in storage from what changes in reported V-addresses.

---

### I-address span: still a single contiguous range

REARRANGE modifies only V-positions — it never touches I-addresses [INV-REARRANGE-IDENTITY]. The link orgl lives in I-space and is permanent [INV-LINK-PERMANENCE, SS-THREE-LAYER-MODEL]. Concretely:

- At link creation, the V-span `[1.1, 1.5]` was converted to I-spans via `vspanset2sporglset` and stored in the link orgl as one contiguous I-span (call it `[I.1, I.5]`), assuming the content at creation time was a single contiguous I-address run [SS-LINK-ENDPOINT, Finding 0037].
- After the pivot, the I-span `[I.1, I.5]` stored in the link orgl is **unchanged**. No operation removes or modifies link orgl entries [INV-LINK-PERMANENCE].

So yes, the I-address span remains a single contiguous range in the link's permanent storage.

---

### `retrieveendsets` return: two V-Specs (with a duplication artifact)

The retrieval path is what changes. FOLLOWLINK and RETRIEVEENDSETS both perform I-to-V conversion using the querying document's current POOM [SS-FOLLOWLINK, Finding 0048; SS-RETRIEVE-ENDSETS, Finding 0035].

After a pivot that splits `[1.1, 1.5]` into `[1.1, 1.2]` and `[1.4, 1.5]`, the POOM still contains all the original I-addresses but now maps them to two non-adjacent V-regions. When `linksporglset2specset()` calls `span2spanset()` → `retrieverestricted()` against the POOM, it discovers that the I-addresses from the stored sporgl map to two separate V-locations [SS-FOLLOWLINK]. The results are accumlated in sorted V-order via `incontextlistnd()` [SS-CONTEXT-LIST, INV-RETRIEVAL-V-SORTED].

This is directly confirmed by the documented edge case:

> **[EC-PIVOT-LINK-FRAGMENTATION]**: "When linked content is rearranged via pivot, the link's endsets become fragmented into multiple spans." The concrete example: after pivoting to make "CD" non-contiguous, endsets report **four** spans (1.2 width 0.1 twice, 1.5 width 0.1 twice).

So `retrieveendsets` returns **two V-Specs** — one per contiguous V-region — along with a duplication artifact (each span appears twice) whose origin the KB describes as either a bug or an internal representation issue.

---

### Why the split happens at retrieval, not in storage

The architectural explanation is the three-layer model [SS-THREE-LAYER-MODEL]:

| Layer | State after pivot |
|---|---|
| I-space (link orgl) | Unchanged — single I-span `[I.1, I.5]` |
| Spanfilade (DOCISPAN) | Unchanged — append-only [INV-SPANF-WRITE-ONLY] |
| POOM (document V-stream) | Modified — I-addresses now map to non-adjacent V-positions |

REARRANGE operates exclusively on the POOM [SS-POOM-MUTABILITY]. The I-to-V translation at retrieval time reads the current POOM state, which now maps the link's I-address range to two disjoint V-regions. The POOM is a multimap [SS-POOM-MULTIMAP], so one I-span can legitimately produce multiple V-spans.

---

### Summary

- The **stored I-address span** in the link orgl is still a single contiguous range — REARRANGE never touches I-space.
- **`retrieveendsets` returns two V-Specs** (plus a duplication artifact yielding four in practice), because the I-to-V conversion reads the post-pivot POOM, which maps the link's I-addresses to two non-adjacent V-regions.
- This is classified as [EC-PIVOT-LINK-FRAGMENTATION] and is a direct consequence of the architecture: link endpoints are anchored to I-addresses [INV-REARRANGE-IDENTITY], while V-position reports are computed dynamically from the mutable POOM [SS-POOM-MUTABILITY].

## Code Exploration

Now I have all the information needed. Let me trace the complete answer with precision.

---

## Answer: What `retrieveendsets` Returns After a Pivot

### 1. How Link Endsets Are Stored (the starting state)

When a link is created, `docreatelink` in `do1.c` calls `insertendsetsinspanf` [do2.c:116-128]:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
&& insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
```

Inside `insertspanf` [spanf1.c:15-54], each sporgl is inserted into the 2D spanfilade with:
- **ORGLRANGE dimension** (`crumorigin.dsas[ORGLRANGE]`): the link's ISA prefixed with span-type constant (`LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`) [spanf1.c:22]
- **SPANRANGE dimension** (`crumorigin.dsas[SPANRANGE]`): the **I-address** (permascroll address) of the linked content [spanf1.c:49]

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // [spanf1.c:22]
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);             // [spanf1.c:49]
movetumbler(&lwidth, &crumwidth.dsas[SPANRANGE]);               // [spanf1.c:50]
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE); // [spanf1.c:51]
```

The `lstream`/`lwidth` values are the I-addresses, obtained by `vspanset2sporglset` → `vspanset2ispanset` [sporgl.c:35-58] at creation time. **The spanfilade records the I-addresses (permascroll coordinates), not V-addresses.**

For the single V-span `[1.1, 1.5]` at link-creation time, if the content was originally inserted as one block, `vspanset2ispanset` produces **one I-span** — say `[perm_addr, width]` — and the spanfilade gets **one crum entry** for the FROM endset.

---

### 2. What REARRANGE Modifies

`dorearrange` [do1.c:34-43] calls `rearrangepm` [orglinks.c:137-142]:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);   // [orglinks.c:139]
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`rearrangend` [edit.c:78-160] operates **exclusively on `docorgl`** — the POOM (permutation matrix enfilade). It adjusts the V-dimension displacement (`ptr->cdsp.dsas[index]`) of POOM nodes [edit.c:125]:

```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

**The spanfilade is never touched.** The link's entry in `spanf` — the I-address crum at `SPANRANGE = [perm_addr, width]` — is identical before and after any REARRANGE. This is architectural: REARRANGE is a POOM-only operation.

---

### 3. The `retrieveendsets` Call Chain

`retrieveendsets` [fns.c:350-362] → `doretrieveendsets` [do1.c:369-374] → `retrieveendsetsfromspanf` [spanf1.c:190-234].

**Step A — Identify the link in the spanfilade:**

```c
specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)  // [spanf1.c:222]
```

This converts the input (the link's ISA) to sporgl entries locating it in `spanf`.

**Step B — Retrieve the FROM endset from the spanfilade:**

```c
retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)  // [spanf1.c:223]
```

`fromspace` has `stream.mantissa[0] = LINKFROMSPAN = 1` and `width.mantissa[0] = 1` [spanf1.c:210-211] — it restricts the ORGLRANGE dimension to the FROM endset slot.

`retrievesporglsetinrange` [spanf1.c:237-267] calls `retrieverestricted` on the spanfilade, then calls `contextintosporgl` for each matching context [spanf1.c:250]:

```c
contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglset, SPANRANGE);
```

Which captures [sporgl.c:205-219]:
```c
movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);  // doc ISA (non-zero)
movetumbler(&context->totaloffset.dsas[SPANRANGE], &sporglptr->sporglorigin);  // I-address start
movetumbler(&context->contextwid.dsas[SPANRANGE], &sporglptr->sporglwidth);    // I-address width
```

Because the spanfilade has **one crum** for the FROM endset (the original single I-span), `fromsporglset` contains **one sporgl**: `{sporgladdress=docisa, sporglorigin=perm_addr, sporglwidth=original_width}`.

The **I-address span is still a single contiguous range** — `sporglorigin=perm_addr, sporglwidth=original_width` — exactly what was stored at link-creation time, unmodified by REARRANGE.

**Step C — Convert I-address sporgl back to a specset:**

```c
linksporglset2specset(taskptr, &docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)  // [spanf1.c:224]
```

`linksporglset2specset` [sporgl.c:97-123] iterates over the sporgl list. For each sporgl:
- If `sporgladdress == 0`: emit an ISPAN directly
- If `sporgladdress != 0` (our case — it's the docisa): call `linksporglset2vspec` [sporgl.c:116]

Since our sporgl's `sporgladdress` = docisa (non-zero), it calls `linksporglset2vspec` [sporgl.c:127-137], which calls `sporglset2vspanset` [sporgl.c:141-175], which calls `ispan2vspanset` [orglinks.c:389-393]:

```c
return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
```

**Step D — The pivot-sensitive I→V conversion:**

`permute` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-454]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, I,
                              (typespan*)NULL, V, (typeisa*)NULL);  // [orglinks.c:435]
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, I, &foundspan, V);         // [orglinks.c:443]
    nextptr = (typeitem *)onitemlist(taskptr, (typeitem*)&foundspan,
                                    (typeitemset*)targspansetptr); // [orglinks.c:444]
}
```

Here `orgl` is the POOM for the document. `retrieverestricted` queries the POOM restricted to `[perm_addr, perm_addr+width]` in the I-dimension and collects **all POOM leaf nodes** whose I-range intersects it.

**After the pivot,** the POOM has been split (by `makecutsnd` and V-displacement adjustments in `rearrangend` [edit.c:110-139]). A single contiguous I-range `[perm_addr, perm_addr+width]` now maps to **multiple POOM leaf nodes** at non-contiguous V-positions — for example `[1.1, 1.2]` and `[1.4, 1.5]`.

`retrieverestricted` returns **two context entries** (one per POOM leaf). `context2span` [context.c:176-212] converts each context to a V-span by taking the intersection of the context's V-range with the I-restriction and projecting onto the V-dimension [context.c:206-207]:

```c
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

`onitemlist` [orglinks.c:464-537] appends each `foundspan` to the list **without merging** (unlike `putvspaninlist`, which merges adjacents — but `span2spanset` uses `onitemlist`). So `specptr->vspanset` ends up as a linked list with **two separate V-spans**: `[1.1, 1.2]` and `[1.4, 1.5]`.

Back in `linksporglset2specset` [sporgl.c:103-121], **one `typevspec` item** is allocated and linked into `*specsetptr`:

```c
specset = (typespecset)taskalloc(taskptr, sizeof(typevspec));
// ...
linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);  // [sporgl.c:116]
// ...
*specsetptr = specset;
specsetptr = (typespecset *)&((typeitemheader *)specset)->next;
```

The loop runs **once** (one sporgl in `fromsporglset`), producing **one `VSPECID` item**.

---

### Answers

**Q: Does `retrieveendsets` return one VSpec or two?**

**One VSpec** (`VSPECID` item) is returned in the `fromset`. Because:
1. The link's FROM endset was stored as a single I-span in the spanfilade (one sporgl crum)
2. REARRANGE does not modify the spanfilade → `retrievesporglsetinrange` returns one sporgl
3. `linksporglset2specset` allocates one `typevspec` per sporgl → one VSpec

However, that VSpec's `vspanset` field is a linked list of **two V-spans** — `[1.1, 1.2]` and `[1.4, 1.5]` — because `ispan2vspanset` queries the now-pivoted POOM and finds two separate leaves covering the original I-range.

**Q: Is the I-address span still reported as a single contiguous range?**

**Yes, the I-address is still a single contiguous range in the spanfilade.** The spanfilade crum for the FROM endset retains `SPANRANGE = [perm_addr, original_width]` exactly as stored at link-creation time. REARRANGE (`rearrangend`) modifies only `docorgl` (the POOM) via `rearrangepm` [orglinks.c:137-142] — never `spanf`.

The returned **specset to the client is a VSpec** (not an ISPAN), because `sporgladdress = docisa ≠ 0`, so `linksporglset2specset` always calls `linksporglset2vspec`. The client never directly receives the I-address; it receives V-spans derived from the current POOM state.

---

### Empirical Caveat (Finding 0019)

The empirical golden test `endsets_after_pivot` [Finding 0019, §3] observed **four spans** returned (and the same link returned twice by `find_links`). This suggests that in practice the pivot's `recombine` step [edit.c:139] may fail to consolidate some POOM crums, producing additional fragmentation beyond what the 2-leaf model predicts. The code path analysis establishes the canonical behavior; the duplication effect is a known artifact documented in Finding 0019.

---

### Key Code References

| File | Line | Role |
|------|------|------|
| `fns.c` | 350-362 | `retrieveendsets` — FEBE handler |
| `do1.c` | 369-374 | `doretrieveendsets` — thin wrapper |
| `spanf1.c` | 190-234 | `retrieveendsetsfromspanf` — core logic |
| `spanf1.c` | 15-54 | `insertspanf` — stores I-addr in SPANRANGE at link creation |
| `spanf1.c` | 237-267 | `retrievesporglsetinrange` — queries spanfilade, returns I-addr sporgls |
| `sporgl.c` | 97-123 | `linksporglset2specset` — **one VSpec per sporgl** |
| `sporgl.c` | 141-175 | `sporglset2vspanset` — calls ispan2vspanset per sporgl |
| `orglinks.c` | 389-393 | `ispan2vspanset` — delegates to permute(I→V) |
| `orglinks.c` | 425-454 | `span2spanset` — queries POOM, **one V-span per POOM leaf** |
| `orglinks.c` | 137-142 | `rearrangepm` — POOM-only; **spanfilade untouched** |
| `edit.c` | 78-160 | `rearrangend` — adjusts `cdsp.dsas[V]`, never touches SPANRANGE |

---

## Question 17 [gregory]

> Since REARRANGE has no subspace boundary guard (`makeoffsetsfor3or4cuts` uses pure tumbler arithmetic), what actually happens at the POOM level if cuts straddle the `1.x`/`0.2.x` boundary — do text crums get relocated into the link subspace address range, and if so, are they retrievable via `retrievevspansetpm` for the link subspace?

### Gregory's Answer

## KB Synthesis

## What Happens at the POOM Level When REARRANGE Crosses the Subspace Boundary

The short answer: yes on both counts. Text crums ARE relocated into the 2.x V-address range, and they ARE retrievable there — but through the link-subspace reporting path of `retrievevspansetpm`, not the text-subspace path. Here is the full picture.

---

### 1. The Relocation Mechanism

REARRANGE applies pure tumbler arithmetic to POOM crum displacements with no subspace guard [PRE-REARRANGE / Finding 0051]. The relevant line is:

```c
tumbleradd(&ptr->cdsp.dsas[V], &diff[i], &ptr->cdsp.dsas[V])
```

For a pivot with cuts `[1.1, 1.4, 2.5]`:
- `diff[1] = 2.5 - 1.4 = 1.1`
- Every crum classified as section 1 (content between `1.1` and `1.4`) has its V-displacement incremented by `1.1`
- A crum originally at `1.1–1.3` ends up at `2.2–2.4` [ST-REARRANGE / Finding 0056]

This is arithmetically unconditional. REARRANGE has **no** equivalent of INSERT's two-blade knife (which limits shifting to the current subspace via `findaddressofsecondcutforinsert` [SS-TWO-BLADE-KNIFE / Finding 0054]) and **no** equivalent of DELETE's accidental `strongsub` exponent guard [INT-DELETE-SUBSPACE-ASYMMETRY / Finding 0055]. It is the only operation with zero protection — deliberate or incidental — against cross-subspace displacement [FC-SUBSPACE / Finding 0067].

After `rearrangend` completes, `setwispupwards` recalculates the POOM tree's relative displacements bottom-up [SS-ENFILADE-TREE / Finding 0066]. The root's `cdsp.dsas[V]` (minimum V-address across all crums) and `cwid.dsas[V]` (total extent) are updated to reflect the new layout. The displaced text crums are now legitimate entries in the POOM at 2.x V-addresses; the I-addresses they carry are unchanged — still permascroll addresses, not link orgl ISAs [INV-REARRANGE-IDENTITY / Finding 0056].

---

### 2. What `retrievevspansetpm` Reports

`retrievevspansetpm` (called by `RETRIEVEDOCVSPANSET`) uses `is1story()` to detect whether content spans a single subspace. After cross-subspace rearrangement the answer is no — the POOM contains crums at both `1.x` and `2.x` — so the function enters its multi-subspace decomposition path [SS-VSPAN-VS-VSPANSET / Findings 0035, 0038].

The decomposition logic keys on the leading mantissa digit of V-addresses:
- Content at `1.x` → text subspace span (uses `maxtextwid()`)
- Content at `2.x` → link subspace span (zeroes mantissa[1], normalizes to `"0"` in output when text also exists)

**The relocated text crums at `2.x` are reported in the link-subspace portion of the vspanset.** Finding 0051's concrete experiment confirms this: after the cross-subspace pivot, `vspanset` returns `{at 0 for 0.2, at 1 for 1}` — the `"at 0 for 0.2"` span represents the displaced text, normalized from `2.x` to `"0"` [EC-VSPAN-NORMALIZATION / Finding 0038]. `retrievevspansetpm` cannot distinguish permascroll I-addresses from link orgl ISAs because the POOM is untyped [SS-SUBSPACE-CONVENTION / Finding 0011].

---

### 3. Content Retrieval via `retrieve_contents`

`retrieve_contents` (`doretrievev`) is agnostic to V-address subspace semantics. It converts the caller-specified V-span to I-addresses via the POOM, then dereferences those I-addresses in the granfilade [PRE-RETRIEVE-CONTENTS / Finding 0010].

Since the displaced text crums carry permascroll I-addresses (text bytes), querying `retrieve_contents` at the 2.x V-addresses returns the actual text bytes normally. Finding 0051 records this explicitly: `retrieve_contents` at `2.x` returns `"ABC"` — the text that was moved there by the pivot. The granfilade has no concept of which V-subspace its content was "supposed" to live in [SS-CONTENT-IDENTITY / Finding 0002].

---

### 4. The Violation Is Silent and Persistent

[INV-SUBSPACE-CONVENTION] / Finding 0009 states the subspace convention — permascroll I-addresses belong in `1.x`, link orgl ISAs belong in `2.x` — is a caller-enforced protocol with no runtime check. REARRANGE violates it without error, and the violation persists:

- `retrieve_contents` at `2.x` returns text bytes (should only find link structure) [EC-REARRANGE-CROSS-SUBSPACE / Finding 0056]
- `retrievevspansetpm` reports text crums as link-subspace spans
- `compare_versions` using the returned vspanset could crash if it receives the malformed link-subspace span and tries to interpret permascroll I-addresses as link ISAs [EC-COMPARE-VERSIONS-LINK-CRASH / Finding 0009]
- Any code path that calls `find_links` on the `2.x` content expecting link orgls would find nothing meaningful

There is no cleanup or correction mechanism. Unlike INSERT (which has `acceptablevsa` as a designated enforcement point, however unimplemented) [PRE-ENF0-PLACEMENT-GAP / Finding 0049], REARRANGE has no comparable hook — its V-position modification path (`tumbleradd` in `edit.c:125`) runs unconditionally on every affected crum [PRE-REARRANGE / Finding 0051].

---

### Summary

| Aspect | Answer |
|--------|--------|
| Text crums relocated into `2.x`? | **Yes** — `tumbleradd` shifts V-displacement unconditionally |
| Detectable by POOM? | **No** — POOM is untyped, stores all as `(V, I)` pairs |
| Visible in `retrievevspansetpm`? | **Yes** — reported in link-subspace portion, normalized to `"0"` |
| Retrievable via `retrieve_contents`? | **Yes** — permascroll I-addresses work regardless of V-subspace |
| Subspace invariant preserved? | **No** — INV-SUBSPACE-CONVENTION violated silently |
| Protection mechanism? | **None** — REARRANGE has neither INSERT's deliberate knife nor DELETE's accidental `strongsub` guard |

## Code Exploration

Now I have all the code I need. Let me compile the complete analysis.

---

## Analysis: REARRANGE Cross-Subspace Contamination in the POOM

### 1. The POOM V-Space Address Layout

Before tracing what breaks, the actual subspace structure must be established from first principles.

**Text content** is inserted via `appendpm` → `findvsatoappend` → `insertpm`. `findvsatoappend` [`orglinks.c:36-43`] sets:
```c
tumblerclear(&linkspacevstart);
tumblerincrement(&linkspacevstart, 0, 2, &linkspacevstart);  // = 2
// ...
tumblerincrement(vsaptr, 0, 1, vsaptr);  /* no text in doc */
tumblerincrement(vsaptr, 1, 1, vsaptr);  // vsaptr = 1.1
```

`tumblerincrement` with `rightshift=1` writes into `mantissa[idx+1]`, so the sequence `(0,1)` then `(1,1)` from zero produces tumbler `{exp=0, mantissa[0]=1, mantissa[1]=1}` — the printed form `1.1`. Text content begins here. In `insertpm` [`orglinks.c:114-131`]:
```c
shift = tumblerlength(vsaptr) - 1;   // = 2 - 1 = 1 for vsaptr = 1.1
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);  // width = 0.inc
```
Crumwidth is thus a sub-integer tumbler (e.g., `0.5` for five characters). Text crums span `[1.1, 1.6)`, `[1.6, 1.16)` etc. — all within the `1.x` range.

**Link references** (link-ISA spans copied into the document's POOM) start at `firstlink = 2.1`, per `findnextlinkvsa` [`do2.c:156-158`]:
```c
tumblerincrement(&firstlink, 0, 2, &firstlink);  // = 2
tumblerincrement(&firstlink, 1, 1, &firstlink);  // = 2.1
```

**Link-object endpoints** within a link's own POOM, from `setlinkvsas` [`do2.c:171-176`]:
```c
fromvsa = 1.1   (tumblerincrement x2: 0→1→1.1)
tovsa   = 2.1   (tumblerincrement x2: 0→2→2.1)
threevsa = 3.1
```

**The hard boundary** is `linkspacevstart = 2` [`orglinks.c:36-37`]: below `2` is text zone (`1.x`), at or above `2` is link reference zone. A secondary view from `filter_vspanset_to_text_subspace` [`do1.c:393-408`] treats `V < 1.0` as "link subspace" (sub-integer addresses), but these don't arise in normal operation.

After `setwispnd` [`wisp.c:171-228`] normalizes the tree, the root absorbs the minimum son displacement into its own `cdsp.dsas[V]`, and all sons' displacements become relative. For a document with text at absolute `[1.1, 1.6)` and a link at `[2.1, 2.2)`:
- Root: `cdsp.dsas[V] = 1.1`, `cwid.dsas[V] = 1.1` (total extent `1.1` wide)
- Text son (relative): `cdsp.dsas[V] = 0`, `cwid.dsas[V] = 0.5`
- Link son (relative): `cdsp.dsas[V] = 1.0` → simplifies to `1` (mantissa[0]=1, mantissa[1]=0)

---

### 2. `makeoffsetsfor3or4cuts` Has No Boundary Guard

The full body of `makeoffsetsfor3or4cuts` [`edit.c:164-184`]:

```c
int makeoffsetsfor3or4cuts(typeknives *knives, tumbler diff[])
{
  tumbler a, b;
    /* diff[0] is simply ignored */
    if (knives->nblades == 4) {
        tumblersub(&knives->blades[2], &knives->blades[0], &(diff[1]));
        tumblersub(&knives->blades[1], &knives->blades[0], &a);
        tumblersub(&knives->blades[3], &knives->blades[2], &b);
        tumblersub(&b, &a, &(diff[2]));
        movetumbler(&diff[1], &diff[3]);
        diff[3].sign = !diff[1].sign;
    } else if (knives->nblades == 3) {
        tumblersub(&knives->blades[2], &knives->blades[1], &diff[1]);
        tumblersub(&knives->blades[1], &knives->blades[0], &diff[2]);
        diff[2].sign = !diff[2].sign;
        tumblerclear(&(diff[3]));
    } else
        gerror("Wrong number of cuts.");
}
```

Every operation is a `tumblersub` — pure arithmetic difference between blade addresses. There is no test against `linkspacevstart` (`= 2`), no check against the `1.x`/`2.x` transition, no `tumblerincrement` boundary, no predicate testing subspace membership. The function cannot know or care whether blades straddle a semantic zone boundary.

`tumblersub` itself [`tumble.c:406-440`] is correspondingly pure:
```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    if (iszerotumbler(bptr)) movetumbler(aptr, cptr);
    else if (tumblereq(aptr, bptr)) tumblerclear(cptr);
    else if (iszerotumbler(aptr)) { movetumbler(bptr, cptr); cptr->sign = !cptr->sign; }
    else { movetumbler(bptr, &temp); temp.sign = !temp.sign; tumbleradd(aptr, &temp, cptr); }
    tumblerjustify(cptr);
}
```

No domain awareness. The resulting `diff[]` values are arithmetic displacements that will be applied wholesale to every crum in each zone.

`rearrangend` applies them at [`edit.c:125`]:
```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

This unconditional `tumbleradd` shifts a crum's absolute V displacement by `diff[i]`. A text crum that was at `1.4` and receives `diff[1] = +0.7` lands at `2.1`. A link crum at `2.1` receiving `diff[2] = -0.4` lands at `1.7`. There is no guard.

---

### 3. What Actually Happens to Crum Positions

**Concrete cross-boundary scenario** — 3-cut rearrange with blades straddling the text/link boundary at V = `2.0`:

```
blade[0] = 1.3   (text zone)
blade[1] = 1.7   (text zone)
blade[2] = 2.1   (link zone)
```

`makeoffsetsfor3or4cuts` computes:
```
diff[1] = blade[2] - blade[1] = 2.1 - 1.7 = 0.4   (zone 1 moves forward)
diff[2] = -(blade[1] - blade[0]) = -(0.4) = -0.4   (zone 2 moves backward)
diff[3] = 0
```

Applied by `rearrangend` [`edit.c:113-136`] to crums in each zone:

| Zone | Range | Crums | diff | Effect |
|------|-------|-------|------|--------|
| 1 | `[blade[0], blade[1])` | Text crums at `1.4`, `1.5` | +0.4 | `1.4→1.8`, `1.5→1.9` — still text zone |
| 2 | `[blade[1], blade[2])` | Text crum at `1.8`; link crum at `2.1` | -0.4 | `1.8→1.4` (text); `2.1→1.7` (**link moved into text zone**) |

If the zone boundary had been:
```
blade[0] = 1.3, blade[1] = 1.6, blade[2] = 2.3
diff[1] = 2.3 - 1.6 = 0.7  (large forward push)
```
Then text crums in zone 1 at `1.5` → `2.2` (into link zone), and link crums in zone 2 at `2.1` → `2.1 - 0.7 = 1.4` (into text zone).

The **4-cut** case (swap) is symmetrical — `diff[3] = -diff[1]`, so the displaced items swap zones in both directions simultaneously.

After `rearrangend` completes, `setwispupwards(father, 1)` and `recombine(fullcrumptr)` run [`edit.c:137-141`]. `setwispnd` [`wisp.c:171-228`] renormalizes: the root absorbs the new minimum displacement, and all sons' relative displacements are updated via `dspsub`. The logical V ordering is preserved, but addresses that crossed zone boundaries retain their new (incorrect) subspace membership.

Note: `slicecbcpm` in `ndcuts.c:389-436` does enforce `lockis1story` on POOM crum widths and checks `tumblerlength(cut) == tumblerlength(cwid)` before cutting — so the cutting phase only handles correctly-formed crums. But this guard is a structural precondition, not a subspace guard. After the cuts are made, the differential offsets in `rearrangend` are applied with no such protection.

---

### 4. Classification Predicates Break After Relocation

`istextcrum` [`orglinks.c:246-252`] and `islinkcrum` [`orglinks.c:255-261`]:

```c
bool istextcrum(typecorecrum *crumptr) {
    if (crumptr->cdsp.dsas[V].mantissa[1] == 0
        && is1story(&crumptr->cwid.dsas[V])) return TRUE;
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr) {
    if (crumptr->cdsp.dsas[V].mantissa[0] == 1
        && crumptr->cdsp.dsas[V].mantissa[1] != 0)
    /* "if the whole crum is displaced into link space it is a link crum
       this is true if the tumbler is a 1.n tumbler where n != 0" */
        return TRUE;
    return FALSE;
}
```

These predicates test the *relative* displacement `cdsp.dsas[V]` stored in the crum. After setwispnd normalizes, the relative displacements change. Consider the outcomes for each cross-boundary case:

**Case A: Link crum moved from absolute `2.1` to `1.7`:**
After setwispnd, if root cdsp remains at `1.1`, relative displacement = `1.7 - 1.1 = 0.6`:
- `mantissa[0] = 6, mantissa[1] = 0`
- `islinkcrum`: `mantissa[0] == 1`? → NO (it's 6). **Misclassified: NOT a link crum.**
- `istextcrum`: `mantissa[1] == 0`? YES; `is1story(cwid)` for a link crum with `cwid = 0.1`? YES. → **Misclassified as TEXT crum.**

**Case B: Text crum moved from absolute `1.5` to `2.2`:**
Relative displacement = `2.2 - 1.1 = 1.1`:
- `mantissa[0] = 1, mantissa[1] = 1`
- `islinkcrum`: `mantissa[0] == 1 && mantissa[1] != 0`? → YES. **Misclassified as LINK crum.** (Per the comment: "a 1.n tumbler where n != 0")
- `istextcrum`: `mantissa[1] == 0`? → NO. Correctly rejected.

**Case C: Text crum moved to absolute `2.01`** (3-story tumbler, e.g. in a large document):
Relative `= 2.01 - 1.1 = 0.91`:
- `mantissa[0] = 9, mantissa[1] = 1`
- `islinkcrum`: `mantissa[0] == 1`? → NO.
- `istextcrum`: `mantissa[1] == 0`? → NO.
- **INVISIBLE to both predicates.**

---

### 5. Retrievability via `retrievevspansetpm`

`retrievevspansetpm` [`orglinks.c:173-221`]:

```c
bool retrievevspansetpm(typetask *taskptr, typeorgl orgl, typevspanset *vspansetptr)
{
    ccptr = (typecorecrum *) orgl;
    if (is1story(&ccptr->cwid.dsas[V])) {
        // Simple: return one span from root cdsp/cwid
        vspan.stream = ccptr->cdsp.dsas[V];
        vspan.width  = ccptr->cwid.dsas[V];
        putvspaninlist(taskptr, &vspan, vspansetptr);
        return TRUE;
    } else {
        // Complex: split into "link part" and "text part"
        linkvspan.stream = ccptr->cwid.dsas[V];
        linkvspan.stream.mantissa[1] = 0;       // zero second digit
        tumblerjustify(&linkvspan.stream);
        linkvspan.width  = ccptr->cwid.dsas[V];
        linkvspan.width.mantissa[1] = 0;
        tumblerjustify(&linkvspan.width);

        maxtextwid(taskptr, ccptr, &voffset, &maxwid);
        vspan.stream = 0;
        vspan.width  = maxwid;
        vspan.width.mantissa[0] = 0;           // zero first digit of maxwid
        putvspaninlist(taskptr, &vspan, vspansetptr);
        putvspaninlist(taskptr, &linkvspan, vspansetptr);
        return TRUE;
    }
}
```

**The link span is not enumerated from crums.** It is extracted heuristically from the root's `cwid.dsas[V]` by zeroing `mantissa[1]`. After cross-boundary REARRANGE, the root's cwid incorporates the new (corrupted) extents, so this heuristic produces a wrong link span regardless.

**`maxtextwid` [`orglinks.c:224-244`]** is what actually walks crums:

```c
int maxtextwid(typetask *taskptr, typecorecrum *crumptr, tumbler *voffset, typevspanset *maxwidptr)
{
    if (istextcrum(crumptr)) {
        tumbleradd(voffset, &crumptr->cdsp.dsas[V], &tmpwid);
        tumblermax(&tmpwid, maxwidptr, maxwidptr);
    } else {
        tumbleradd(voffset, &crumptr->cdsp.dsas[V], &localvoffset);
        for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
            if (ptr && !islinkcrum(ptr)) {   // skip link crums
                maxtextwid(taskptr, ptr, &localvoffset, maxwidptr);
            }
        }
    }
}
```

The `!islinkcrum(ptr)` guard at [`orglinks.c:240`] skips crums where `islinkcrum` returns true. Combined with the misclassification from §4:

| Relocated crum | After relocation | `islinkcrum` | `istextcrum` | `maxtextwid` fate |
|---|---|---|---|---|
| Link crum → text zone (`0.6` relative) | `maxtextwid` descends into it → `istextcrum` = TRUE | FALSE | TRUE | **Included in text span (wrong)** |
| Text crum → link zone (`1.1` relative, i.e. `1.x` position) | Classified as link crum | TRUE | FALSE | **Skipped by `!islinkcrum`** |
| Text crum → deep link zone (`0.91` relative, 2-digit offset) | Invisible | FALSE | FALSE | **Skipped by both branches (height=0, no sons)** |

**Summary of `retrievevspansetpm` behavior after cross-boundary REARRANGE:**

1. **Text crums moved to `1.x`-relative addresses** (matching `islinkcrum`'s `mantissa[0]==1 && mantissa[1]!=0` pattern): skipped by `maxtextwid`, so dropped from the declared text span. They do NOT appear in the link span either — the link span is a heuristic from root cwid, not an enumeration.

2. **Text crums moved to addresses with `mantissa[0] ≠ 1`** (invisible to both predicates): completely invisible to `maxtextwid`; dropped from the text span silently.

3. **Link crums moved to integer-offset addresses**: misclassified as text crums; incorrectly appear in the text span returned by `retrievevspansetpm`.

**The short answer**: relocated text crums are NOT retrievable via `retrievevspansetpm`'s declared link-subspace span. The heuristic span computation doesn't enumerate individual crums. The predicates don't hold up after cross-subspace displacement. A crum that lands in the link address range is either invisible to `maxtextwid` or misclassified — either way, `retrievevspansetpm` does not surface it correctly.

---

### 6. Low-Level Retrieval Still Works

`findcbcnd` [`retrie.c:208-227`] and `findcbcinarea2d` [`retrie.c:229-268`] use only `whereoncrum` — pure tumbler interval arithmetic — to locate crums. They have no predicate based on `islinkcrum` or `istextcrum`. A text crum relocated to absolute V address `2.1` WILL be found by:

```c
// retrie.c:208-215
typecontext *findcbcnd(typecorecrum *father, typewid *offsetptr, tumbler *address, INT index) {
    if ((cmp = whereoncrum(father, offsetptr, address, index)) < ONMYLEFTBORDER
        || cmp > THRUME) return NULL;
    ...
}
```

This is the path taken by `permute` → `span2spanset` → `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d`. If you construct a V query span that covers `2.1`, the relocated text crum's content will be returned with its correct I-space mapping. So V→I permutation (`vspanset2ispanset`) works at the arithmetic level.

The failure is specifically in `retrievevspansetpm`'s span abstraction layer: the declared vspansets it returns are corrupted by the cross-contamination, so they don't correctly point the caller to the relocated crum's address. The crum exists and is arithmetic-queryable, but the span declarations cannot be trusted to lead there.

---

### Summary

| Claim | Evidence |
|---|---|
| `makeoffsetsfor3or4cuts` is pure arithmetic with no boundary guard | `edit.c:164-184`: only `tumblersub` calls; no comparison to `linkspacevstart` or any subspace predicate |
| Text crums CAN be relocated into link V-address range | `rearrangend` at `edit.c:125`: unchecked `tumbleradd` to `cdsp.dsas[V]`; `tumblersub`/`tumbleradd` are purely numeric (`tumble.c:365-440`) |
| After relocation, `islinkcrum` / `istextcrum` misfire | `orglinks.c:246-261`: both predicates test `cdsp.mantissa[]` values that change after relocation + `setwispnd` normalization (`wisp.c:171-228`) |
| `maxtextwid` drops or misroutes relocated crums | `orglinks.c:239-240`: `!islinkcrum(ptr)` guard silently drops misclassified text crums; invisible crums (neither predicate matches) fall through |
| `retrievevspansetpm` link span is heuristic, not enumerated | `orglinks.c:196-203`: link span computed by zeroing `mantissa[1]` of root cwid — no crum walk |
| Direct address lookup via `findcbcnd`/`findcbcinarea2d` still finds relocated crums | `retrie.c:208-268`: uses only `whereoncrum` (tumbler interval arithmetic) with no subspace predicates |

The root cause: the enfilade's address-agnostic arithmetic design treats the POOM V axis as a uniform number line. The subspace semantics (`1.x` = text, `2.x+` = link references) exist only in the allocation policy (`findvsatoappend`, `findnextlinkvsa`, `setlinkvsas`) and in the retrieval heuristics (`istextcrum`, `islinkcrum`, `retrievevspansetpm`). REARRANGE — which runs on the raw enfilade — is unaware of and does not preserve those conventions. There is no enforcement mechanism at the POOM tree level.

---

## Question 18 [gregory]

> If you REARRANGE content in a document that has been transcluded into another document, the source document's POOM changes but the target document's POOM is unchanged per FC-DOC-ISOLATION — does this mean `compare_versions` between the rearranged document and its pre-rearrange version shows zero shared content (since V-positions differ) or full shared content (since I-addresses match)?

### Gregory's Answer

## KB Synthesis

## REARRANGE + compare_versions: Full Shared Content, Shifted Pairs

The answer is **full shared content** — `compare_versions` between a rearranged document and its pre-rearrange version returns all content as shared. The V-position pairs in the result will differ, but no content is lost from the intersection.

---

### Why: compare_versions operates in I-space

`compare_versions` (SHOWRELATIONOF2VERSIONS) works by converting V-spans to I-spans, intersecting I-spans across documents, then mapping back to V-positions [SS-COMPARE-VERSIONS]. Each result pair `(span_a, span_b)` satisfies:

```
VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)
```

The comparison is entirely identity-based, not position-based.

---

### REARRANGE leaves I-addresses unchanged

[INV-REARRANGE-IDENTITY] is unambiguous across three findings:

- **Finding 0056**: "The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched."
- **Finding 0018**: "compare_versions between pre- and post-rearrange states returns all content as shared."
- **Finding 0016**: "Content `'BC'` at V-address 1.2 has I-address `I_bc`. After `pivot(doc, 1.2, 1.4, 1.6)`, `'BC'` is at a new V-address but still has I-address `I_bc`."

The multiset of I-addresses in the document is identical before and after rearrangement. So the I-span intersection in `compare_versions` is complete — every I-address from the pre-rearrange version is still present in the rearranged document.

---

### What the result looks like

Suppose D originally has "First Second" and is pivoted to "SecondFirst ":

```
Pre-rearrange version V:
  "First"  at V 1.1, I-addresses α₁..α₅
  "Second" at V 1.7, I-addresses α₆..α₁₂

Rearranged document D:
  "Second" at V 1.1, I-addresses α₆..α₁₂
  "First"  at V 1.8, I-addresses α₁..α₅

compare_versions(V, D):
  I-address intersection: {α₁..α₁₂}  — complete, nothing missing
  Result pairs:
    (V: 1.1 for 0.5, D: 1.8 for 0.5)   // "First"
    (V: 1.7 for 0.6, D: 1.1 for 0.6)   // "Second"
```

The result is **two pairs, covering all content**, with crossed V-position mappings reflecting the pivot.

---

### The transclusion angle

If the content was also transcluded into document T:

- T's POOM is unchanged by D's rearrangement [FC-DOC-ISOLATION, Finding 0064]
- T still maps to the same I-addresses α₁..α₁₂

`compare_versions(T, D_after)` still returns full shared content. But now the V-position pairs reflect:
- T's original V-positions (unchanged)
- D's new, rearranged V-positions

This is correct behavior — the comparison truthfully reports which content is shared and *where it currently sits* in each document. The rearrangement in D is faithfully represented as a cross in the position pairs.

---

### The PRE-COMPARE-VERSIONS caveat

One constraint applies regardless of rearrangement: [PRE-COMPARE-VERSIONS] requires input V-spans to be restricted to the text subspace (1.x). If D contains links in the 2.x subspace, including those spans would trigger Bug 0009 (crash) [EC-COMPARE-VERSIONS-LINK-CRASH]. REARRANGE does not create new exposure here — the precondition applies whether or not rearrangement has occurred. But note that REARRANGE with cross-subspace cuts ([EC-REARRANGE-CROSS-SUBSPACE], Finding 0051) can move text content into the 2.x subspace, which would then become dangerous input to `compare_versions`.

---

### Summary

| What changes after REARRANGE | What stays the same |
|------------------------------|---------------------|
| V-positions of all affected content | I-addresses of all content |
| V-position pairs in `compare_versions` output | Set of shared I-addresses (complete) |
| Appearance of content in V-stream | Content identity, link discoverability, transclusion |

`compare_versions` shows **zero** new loss of shared content from rearrangement alone. The operation is transparent to identity comparison. [INV-REARRANGE-IDENTITY], [SS-COMPARE-VERSIONS]

## Code Exploration

Now I have everything needed to answer this definitively. Let me trace the complete execution path.

---

## Answer

**`compare_versions` shows full shared content (I-addresses match), not zero.** The comparison is conducted entirely in I-space, and rearrange only modifies V-space. Here is the proof, line by line.

---

### 1. What `rearrange` actually changes

`dorearrange` [do1.c:34-43] → `rearrangepm` [orglinks.c:137-142] → `rearrangend(docorgl, cutseqptr, V)` [edit.c:78-160].

The sole mutation of crum data occurs at:

```c
// edit.c:125
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

`index` is `V` — passed at [orglinks.c:139]:

```c
// orglinks.c:139
rearrangend((typecuc*)docorgl, cutseqptr, V);
```

This means only `cdsp.dsas[V]` (the V-dimension displacement) is modified. `cdsp.dsas[I]` — the I-address (permascroll address) of every crum — is **never touched**. The I-addresses of all content are invariant across a rearrange.

---

### 2. How `compare_versions` operates

`doshowrelationof2versions` [do1.c:428-449]:

```c
// do1.c:443-448
return
    specset2ispanset(taskptr, version1, &version1ispans, READBERT)
  &&    specset2ispanset(taskptr, version2, &version2ispans, READBERT)
  &&    intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
  &&    ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
;
```

The pipeline is:

**Step 1 — V → I conversion.** `specset2ispanset` [do2.c:14-46] calls `vspanset2ispanset` [orglinks.c:397-401]:

```c
// orglinks.c:397-401
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute(V, I)` [orglinks.c:404-422] walks each V-span against the document's POOM tree via `retrieverestricted`, collecting all I-spans that those V-spans cover. For a full-document comparison, this yields the complete set of I-addresses present in each version.

**Step 2 — I-space intersection.** `intersectspansets` [correspond.c:145-189] is called with `ISPANID` as span type:

```c
// do1.c:446
intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
```

This calls `spanintersection` [correspond.c:210-265] on each pair of I-spans, computing overlap purely in permascroll address arithmetic. V-positions are not consulted here.

**Step 3 — Map back to V-spans.** `ispansetandspecsets2spanpairset` [do2.c:185-207] calls `restrictvspecsetovercommonispans` [correspond.c:52-90], which uses `ispan2vspanset` → `permute(I, V)` [orglinks.c:389-393] to find where each common I-address appears in each document's V-space.

---

### 3. The result for a rearranged document

Given:
- **Pre-rearrange version** (D₀): content with I-addresses {I₁, I₂, I₃} at V-positions {V₁, V₂, V₃} in that order.
- **Rearranged version** (D₁): same I-addresses {I₁, I₂, I₃} but at different V-positions — say {V₂, V₁, V₃} — because `rearrangend` added offsets to `dsas[V]` without touching `dsas[I]`.

Pipeline trace:
1. `specset2ispanset(D₀, full_vspan)` → permute V→I → yields I-span set `{I₁, I₂, I₃}`
2. `specset2ispanset(D₁, full_vspan)` → permute V→I → also yields `{I₁, I₂, I₃}` (same I-addresses, despite shuffled V-positions)
3. `intersectspansets({I₁,I₂,I₃}, {I₁,I₂,I₃})` → **full intersection** = `{I₁, I₂, I₃}`
4. `ispansetandspecsets2spanpairset` maps each common I-span back to V-positions in each document → produces span pairs like:
   - `(D₀:V₁, D₁:V₂, width_of_I₁)` — I₁ is at V₁ in old, V₂ in rearranged
   - `(D₀:V₂, D₁:V₁, width_of_I₂)` — I₂ is at V₂ in old, V₁ in rearranged
   - etc.

**The returned span pair set records full shared content, but with differing V-positions in each version.**

---

### 4. Architectural intent confirmed by the comment

The purpose of `doshowrelationof2versions` is stated explicitly in `do1.c:378-384`:

```c
// do1.c:378-384
/* Bug 009 SEMANTIC FIX: Filter vspanset to text subspace only (V >= 1.0).
 *
 * compare_versions finds content with "common origin" - shared permascroll
 * identity. Link references at V-position 0.x are document metadata, not
 * transcludable content.
 */
```

"Common origin" = shared permascroll I-address. This is explicitly and intentionally I-space identity, not V-space position. A rearrange changes V-positions but not I-addresses, so it cannot reduce the common-origin count.

---

### Conclusion

`compare_versions` between a rearranged document and its pre-rearrange version reports **100% shared content**, because:

1. `rearrangend` [edit.c:125] modifies only `cdsp.dsas[V]` — never `cdsp.dsas[I]`
2. `doshowrelationof2versions` [do1.c:443-448] intersects **I-span sets**, not V-span sets
3. `vspanset2ispanset` [orglinks.c:397] and `ispan2vspanset` [orglinks.c:389] handle V↔I translation per-document, so each document's rearranged V-layout is correctly decoded to its unchanged I-addresses
4. The returned span pairs will show the **differing V-positions** in each version — that is the point — but the count of shared content equals the full document size

The V-positions differ (the span pairs capture this), but this is the *output* of the comparison, not a reason for zero. FC-DOC-ISOLATION ensures the *other* document's POOM is untouched, but this is irrelevant to the comparison: `doshowrelationof2versions` queries each document's POOM independently to convert V→I, then intersects in I-space.

---

## Question 19 [gregory]

> How does REARRANGE interact with the POOM's 2D enfilade indexing — when V-displacements change but I-displacements stay the same, does `setwispnd` need to recompute the root displacement, and can this trigger `recombinend` rebalancing along the diagonal sort order?

### Gregory's Answer

## KB Synthesis

## REARRANGE, `setwispnd`, and the 2D POOM

### What REARRANGE does to V-displacements

REARRANGE operates by directly applying `tumbleradd` to `ptr->cdsp.dsas[index]` — the V-dimension displacement of each affected POOM crum — while leaving `cdsp.dsas[I]` (the I-dimension displacement) completely untouched [ST-REARRANGE, Finding 0056]. This is how it achieves INV-REARRANGE-IDENTITY: the I-address layer is unchanged, only the V→position mapping shifts.

The classification via `rearrangecutsectionnd` groups crums into regions (0 through 3 for pivot, 0 through 4 for swap), and different regions receive different signed offsets. Crums in region 0 (exterior to all cuts) receive no displacement change at all.

### Does `setwispnd` need to recompute?

Yes, in principle, but the KB has a gap here.

The 2D POOM uses relative displacement encoding: each node's `cdsp.dsas[V]` is stored relative to its parent, and the parent's `cdsp.dsas[V]` tracks the minimum V-displacement across descendants [INV-ENFILADE-RELATIVE-ADDRESSING, Finding 0066]. `setwispnd` maintains this by:
1. Finding `mindsp` = minimum across all children
2. Adding `mindsp` to the parent's `cdsp`
3. Subtracting `mindsp` from every child's `cdsp`

After REARRANGE applies different offsets to crums in different sections, the parent's cached minimum becomes stale — some crums have shifted, others haven't. The parent `cdsp.dsas[V]` no longer equals the minimum child displacement, breaking the invariant that `absolute_grasp(node) = Σ ancestor_cdsp + node.cdsp`.

The KB explicitly confirms that `setwispupwards` is called after DELETE to restore this invariant [ST-DELETE, Finding 0058]: *"After pruning, `setwispupwards` recalculates widths up the tree and `recombine` rebalances."* The analogous need exists for REARRANGE, but the KB does not explicitly state whether `rearrangend` (at `edit.c:78-184`) makes a corresponding `setwispnd` or `setwispupwards` call. This is a genuine gap in the KB's coverage of REARRANGE's post-operation tree maintenance.

That said, REARRANGE is observable to produce correct results (INV-REARRANGE-IDENTITY holds; `compare_versions` confirms content identity is preserved), which implies the tree must reach a consistent state. One resolution is that the traversal through `rearrangend` itself maintains local consistency as it walks — but the KB doesn't confirm this.

### Can this trigger `recombinend` rebalancing?

**No, REARRANGE cannot trigger `recombinend`.**

The critical point: `recombinend` is triggered by node underfullness — when `toofewsons(node)` returns TRUE, meaning a node's `numberofsons` falls below `M_b - 1` or `M_u - 1` [ST-REBALANCE-2D, INV-ENFILADE-OCCUPANCY, Finding 0071]. REARRANGE never removes crums from the tree; it only modifies their `cdsp.dsas[V]` values in place. Therefore `numberofsons` is unchanged at every node, `toofewsons` is not triggered, and `recombinend` has no reason to fire.

Compare with DELETE, which calls `disown` + `subtreefree` to remove bottom crums [ST-DELETE, Finding 0072], reducing `numberofsons` and triggering the rebalance path through `recombinend`. REARRANGE has no equivalent removal step.

### Hypothetical: if `recombinend` ran after REARRANGE

If rebalancing *were* triggered for some other reason after a REARRANGE (e.g., a concurrent operation), the diagonal sort would use the new V-displacements. The `getorderedsons` function in `recombinend` orders children by `cdsp.dsas[0] + cdsp.dsas[1]` — the L1-norm diagonal across both dimensions [ST-REBALANCE-2D, Finding 0071].

After REARRANGE has changed `cdsp.dsas[V]` for some crums (and `setwispnd` has recalculated relative values), these diagonal sort keys would reflect the post-rearrangement V-positions. The diagonal sweep for merge candidate selection would then operate on the rearranged order, potentially merging different pairs than would have been merged before the rearrangement. However, since REARRANGE is content-volume-preserving (INV-REARRANGE-IDENTITY), the overall span coverage at each level is the same — only the distribution may differ.

### Summary

| Aspect | Answer |
|--------|--------|
| V-displacements changed? | Yes — `tumbleradd` on `cdsp.dsas[V]` for each classified crum |
| I-displacements changed? | No — `cdsp.dsas[I]` untouched |
| `setwispnd` needed? | Yes by [INV-ENFILADE-RELATIVE-ADDRESSING]; whether `rearrangend` calls it is a KB gap |
| `recombinend` triggered? | No — no occupancy change, `toofewsons` not satisfied |
| Diagonal sort affected? | Only if `recombinend` runs for other reasons; diagonal keys shift with V-displacements |

## Code Exploration

Now I have everything I need for a complete, code-cited answer. Here it is.

---

## How REARRANGE Interacts with POOM 2D Enfilade Indexing

### 1. What `rearrangend` actually touches

`rearrangend` [edit.c:78] receives an `index` parameter from its caller. Per the `typeknives` comment in `ndenf.h:15`:

```c
INT dimension;  /* always V, assigned by rearrange2d */
```

The knives dimension is set to V at entry [edit.c:102]: `knives.dimension = index`. The loop over sons [edit.c:113–136] only modifies the **V-component** of each son's displacement:

```c
// edit.c:125
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
ivemodified((typecorecrum*)ptr);  // edit.c:127
```

`index` is V (`1` per `wisp.h:21`). The I-component (`cdsp.dsas[I]`, index `0`) is **not touched**.

---

### 2. What `setwispnd` does when V-displacements change

After the rearrange loop, `rearrangend` calls:

```c
setwispupwards (father,1); /* should do nothing, */
		/* but, just on general principles.. */
// edit.c:137
```

The comment is wrong in the general case. `setwispupwards` [wisp.c:83] walks upward calling `setwisp` → `setwispnd` (for POOM, dispatched at `wisp.c:131`).

`setwispnd` [wisp.c:171] recomputes the father's `cdsp` and `cwid` by inspecting all sons. The critical section:

```c
// wisp.c:193–202
movewisp (&ptr->cdsp, &mindsp);                              // seed with first son
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro(ptr)) {
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp,
             (tumbler*)&mindsp, (unsigned)dspsize(ptr->cenftype));
}
lockiszerop = iszerolock((tumbler*)&mindsp, (unsigned)dspsize(father->cenftype));
if (!lockiszerop) {
    somethingchangedp = TRUE;
    dspadd (&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype);
} else {
    movewisp(&father->cdsp, &newdsp);
}
```

`lockmin` at `wisp.c:281` is **component-wise minimum** over the full `dsp` lock array (size 2 for POOM: `[I, V]`). So `mindsp` gets the minimum I and minimum V independently across all sons.

**When only V-displacements change**: I-components of sons are untouched, so `mindsp.dsas[I]` stays 0 (assuming the invariant was maintained). But `mindsp.dsas[V]` is the new minimum V-displacement across all sons, which may be non-zero if the rearrange moved all sons to higher V values.

If `mindsp.dsas[V] != 0`, then `lockiszerop = FALSE` and normalization fires:

```c
dspadd (&father->cdsp, &mindsp, &newdsp, father->cenftype);   // wisp.c:200
// then for each son:
dspsub (&ptr->cdsp, &mindsp, &ptr->cdsp, ptr->cenftype);       // wisp.c:211
```

- **Father's `cdsp.dsas[V]`** is incremented by `mindsp.dsas[V]`
- **Every son's `cdsp.dsas[V]`** is decremented by `mindsp.dsas[V]`
- **No I-component changes** because `mindsp.dsas[I] = 0`

This is the root displacement recomputation the question asks about: **yes, it happens whenever the minimum V across sons shifts away from 0**.

The outer loop in `setwispupwards` [wisp.c:95–101] continues upward as long as `setwisp` returns TRUE. The normalization is strictly local at each level — it adds `mindsp` to the father and subtracts from sons, preserving relative separations.

After normalization:

```c
// wisp.c:208–215
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
    lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid,
            (tumbler*)&tempwid, (unsigned)widsize(ptr->cenftype));
    lockmax((tumbler*)&newwid, (tumbler*)&tempwid,
            (tumbler*)&newwid, (unsigned)widsize(ptr->cenftype));
}
```

The new `cwid` (father's bounding box) is the component-wise max of `(cdsp + cwid)` across all sons — both I and V are recomputed together.

---

### 3. Does `setwispupwards` "should do nothing"?

The comment at `edit.c:137` expects the wisp to be unchanged. This holds only if:
1. The minimum V-displacement across sons doesn't change (some son was already at V=0 before, and that son is not moved), AND
2. The maximum (cdsp + cwid) doesn't change (the bounding box is unaffected)

In a typical 3-cut rearrange (A B C → A C B), section A stays in place, which keeps a son at the minimum V. The comment is valid for that common case. But for a 3-cut rearrange that moves all sections rightward (e.g., a prepend gap), `mindsp.dsas[V]` will be non-zero and normalization fires. The `#ifdef UNdeFined` blocks at `edit.c:86–100` and `edit.c:142–157` — with calls to `fixincoresubtreewids` and `dumppoomwisps` — indicate the author was uncertain whether wisps were always correct at this point.

---

### 4. `recombinend` and the diagonal sort order

After `setwispupwards`, `rearrangend` calls:

```c
recombine (fullcrumptr);  // edit.c:139
```

`recombine` dispatches to `recombinend` for POOM [recombine.c:31].

`recombinend` [recombine.c:104]:

```c
if (father->height < 2  || !father->modified)
    return(0);  // recombine.c:112
for (ptr = getleftson(father); ptr; ptr = getrightbro(ptr))
    recombinend(ptr);  // recombine.c:114-116

getorderedsons (father, sons);  // recombine.c:118
n = father->numberofsons;
for (i = 0; i < n-1; i++) {
    for (j = i+1; sons[i] && j < n; j++) {
        if (i != j && sons[j] && ishouldbother(sons[i], sons[j]))
            takeovernephewsnd (&sons[i], &sons[j]);
    }
}
```

**The diagonal sort**: `getorderedsons` [recombine.c:270] calls `shellsort` [recombine.c:282], which builds sort keys:

```c
// recombine.c:296-300
for (i = 0; i < n; i++) {
    tumbleradd(&v[i]->cdsp.dsas[0], &v[i]->cdsp.dsas[1], &tarray[i]);
    tarrayp[i] = &tarray[i];
}
```

`dsas[0]` is I, `dsas[1]` is V (per `wisp.h:19–20`). The sort key is `I + V` — the diagonal magnitude. Sons with smaller `I + V` appear first in the `sons[]` array.

**What changes after a rearrange**: When V-displacements change, `cdsp.dsas[V]` values change for some sons. This directly changes their `I + V` diagonal magnitude, potentially reordering the `sons[]` array. A son that previously appeared late (high diagonal) may now appear early (low diagonal) and vice versa.

After `setwispnd` normalization, the normalized dsps are what `recombinend` sees. Normalization subtracts the **same** `mindsp` from all sons, so the **relative diagonal differences** between sons are preserved: if A's diagonal was 5 more than B's pre-normalization, it's still 5 more post-normalization. The normalization does not change the diagonal sort order.

**The merge trigger**: `ishouldbother` [recombine.c:150]:

```c
return (dest->numberofsons + src->numberofsons <=
        (dest->height > 1 ? MAXUCINLOAF : MAX2DBCINLOAF)
    && randomness(.3));  // recombine.c:162
```

`randomness` always returns TRUE [recombine.c:133–136]. So the merge decision is purely capacity-based, not spatial. However, **which pairs are tested** changes when V-displacements change the diagonal ordering.

Concrete example: Suppose before rearrange, sons in diagonal order are `[A(I=0,V=1), B(I=1,V=3), C(I=2,V=0)]` with diagonals `[1, 4, 2]` → sorted order `[A, C, B]`. After rearrange moves B to V=0 and C to V=3, diagonals become `[1, 1, 5]` → sorted order `[A, B, C]`. The pair `(A, B)` is now tested; previously `(A, C)` was. If `A` and `B` have few combined sons, they will be merged — a merge that couldn't happen in the old diagonal ordering.

---

### 5. Summary

| Step | Code location | What happens |
|------|--------------|-------------|
| `rearrangend` modifies sons' `cdsp.dsas[V]` only | `edit.c:125` | I-components untouched |
| `setwispnd` computes `mindsp` via component-wise `lockmin` | `wisp.c:194–195` | Finds min I and V independently |
| If min V ≠ 0: father's `cdsp.dsas[V]` incremented, all sons' `cdsp.dsas[V]` decremented | `wisp.c:200, 211` | Re-normalization propagates upward |
| I-components unchanged because `mindsp.dsas[I] = 0` | — | I-invariant preserved |
| `setwispupwards` continues if `setwisp` returned TRUE | `wisp.c:95–101` | Change can propagate to root |
| `recombinend` sorts sons by `cdsp.dsas[I] + cdsp.dsas[V]` | `recombine.c:296–303` | Diagonal sort order reflects new V layout |
| Different adjacent pairs in diagonal order → different merge candidates | `recombine.c:120–128` | Previously non-adjacent pairs may now be merged |

**Direct answer**: Yes, `setwispnd` can recompute the father's root displacement when V-displacements shift the minimum V away from 0 — but it only adjusts `cdsp.dsas[V]` (the comment "should do nothing" is wrong for the general case). Yes, this feeds into `recombinend` rebalancing: the new diagonal sort order after the rearrange presents different adjacent pairs for the `ishouldbother` capacity check, and if formerly non-adjacent sons now sit next to each other along the diagonal and have room to merge, `takeovernephewsnd` will combine them.

---

## Question 20 [gregory]

> If you perform DELETE of region `[a,b)` followed by INSERT of the same bytes at position `c`, the content gets fresh I-addresses and all links to the original content are severed — can you confirm that REARRANGE moving `[a,b)` to position `c` preserves the original I-addresses completely, making it the only edit operation that relocates content without breaking link and transclusion relationships?

### Gregory's Answer

## KB Synthesis

Yes, confirmed. REARRANGE is the only primitive edit operation that physically relocates content while preserving I-addresses — and therefore the only one that leaves link endpoints, transclusion relationships, and version comparison intact.

## DELETE + INSERT: Identity-Severing Relocation

**DELETE** removes the V-to-I mapping from the document's POOM but leaves the granfilade (I-space) unchanged [ST-DELETE, FC-GRANF-ON-DELETE]. The content bytes persist at their original I-addresses; only the document's local reference is severed.

**INSERT** always allocates *fresh* I-addresses via `inserttextingranf` → `findisatoinsertmolecule`. The allocation is purely additive — `next_iaddr = max_iaddr(granf) + 1` — and will never reuse the addresses freed from POOM by the preceding DELETE [INV-NO-IADDR-REUSE, INV-MONOTONIC].

The KB states this explicitly [INV-DELETE-NOT-INVERSE, Finding 0064]:

> All relationships indexed by I-address are permanently severed: transclusions, link endpoints, version comparison results, and provenance chains. The document *looks* the same in V-space but is identity-disconnected in I-space.

Formally: `i' ∩ i = ∅` — the re-inserted bytes occupy a disjoint I-address range, so `compare_versions` reports no shared content and `find_links` cannot locate links whose endpoints indexed the original I-addresses.

## REARRANGE: Identity-Preserving Relocation

REARRANGE operates exclusively on the V-dimension displacement field of each POOM crum. From [ST-REARRANGE, Finding 0056]:

> The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched. No new I-addresses are allocated, no content is duplicated in the permascroll, and the same enfilade nodes (crums) are retained.

The offset arithmetic for a pivot at `[cut₀, cut₁, cut₂]` is pure tumbler addition/subtraction on V-coordinates:
- Region 1 gets `diff[1] = cut₂ - cut₁`
- Region 2 gets `diff[2] = -(cut₁ - cut₀)`

Neither the granfilade nor the spanfilade is touched [FC-CONTENT-SPANF-ISOLATION, FC-GRANF-ON-DELETE]. The invariant holds unconditionally [INV-REARRANGE-IDENTITY]:

> `∀ c ∈ content(doc): i_addr(c, doc_after) = i_addr(c, doc_before)`

This is what makes the consequences follow:

| Relationship | After DELETE+INSERT | After REARRANGE |
|---|---|---|
| Links on content | Severed (new I-addrs) | Intact [INV-REARRANGE-LINK-SURVIVAL] |
| Transclusion identity | Broken | Preserved [FC-INSERT-IADDR] |
| `compare_versions` | No shared content | All content shared [INV-REARRANGE-IDENTITY] |
| `find_links` | Returns nothing | Returns same links [INV-REARRANGE-LINK-SURVIVAL] |

## VCOPY Is Not Relocation

One might ask whether VCOPY also qualifies, since it shares I-addresses rather than creating new ones [ST-VCOPY]. But VCOPY *adds* a new reference to existing content — it does not remove the original. It creates an additional V→I mapping while leaving the source intact. Relocation implies the content moves; VCOPY duplicates the reference. VCOPY followed by DELETE of the source would still sever the original I-addresses from the source document, though the destination would retain them.

## Qualification: Subspace Boundary Risk

One caveat: REARRANGE has a missing precondition — it does not guard against cuts that span subspace boundaries [PRE-REARRANGE, EC-REARRANGE-CROSS-SUBSPACE, Finding 0051]. If cuts produce offsets that displace text content from the `1.x` subspace into the `2.x` (link) subspace, the I-addresses are preserved but the subspace invariant [INV-SUBSPACE-CONVENTION] is violated. The links and transclusions still track the I-addresses correctly, but the content becomes semantically misplaced. For REARRANGE to safely serve as the identity-preserving relocation primitive, all cut points must remain within the same V-subspace.

Within those bounds, the confirmation stands: REARRANGE is the one and only edit primitive in udanax-green that relocates content — changes which V-addresses map to which I-addresses — without creating or destroying any I-address mappings, making it the exclusive mechanism for moving content while preserving the full web of links, transclusions, and version relationships anchored to it.

## Code Exploration

I now have everything I need. Let me compile the full analysis.

---

## Confirmed: REARRANGE Is the Only Edit That Preserves I-Addresses

The answer is **yes, fully confirmed** by source code tracing. Here is the complete proof, tracing every operation through to the data structures they touch.

---

### The Three Data Structures

Before tracing code paths, understand what lives where:

| Structure | What it is | Keyed by |
|-----------|------------|----------|
| `granf` | Granfilade — stores actual text content | I-address (permascroll address) |
| `docorgl` (POOM) | Permutation Object Organized Matrix — the mapping between document positions and content | V↔I |
| `spanf` | Spanfilade — stores link endpoints | (orgl-prefix, I-address) |

Links survive or die depending on whether their I-address keys in `spanf` remain reachable through the POOM after an edit.

---

### DELETE path

`fns.c:333` → `dodeletevspan` [do1.c:158-167] → `deletevspanpm` [orglinks.c:145-152]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` [edit.c:31-76] operates **only on `docorgl` (the POOM)**. For nodes entirely inside the deleted range, case 1:

```c
case 1:
    disown ((typecorecrum*)ptr);      // edit.c:59
    subtreefree ((typecorecrum*)ptr); // edit.c:60
    break;
```

These POOM nodes are **destroyed**. The I-addresses they pointed to are still in `granf` and still registered in `spanf`, but there is no longer any POOM path from V-space to reach them in this document. `granf` is never touched. `spanf` is never touched.

---

### INSERT path

`fns.c:84` → `doinsert` [do1.c:87-123]:

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset));
    return(ret);
}
```

Step 1 — `inserttextgr` [granf2.c:83-109] allocates **fresh I-addresses**:

```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))  // granf2.c:92
    return (FALSE);
movetumbler (&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    ...
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);  // granf2.c:99 — new granf entry
    tumblerincrement (&lsa, 0, textset->length, &lsa);  // granf2.c:100
}
ispanptr->stream = spanorigin;  // the freshly allocated I-address returned
```

`findisatoinsertgr` → `findisatoinsertmolecule` [granf2.c:158-181] finds the next available I-address by scanning `findpreviousisagr` and incrementing past it. These are **new** addresses, distinct from any deleted content.

Step 2 — `docopy` → `insertpm` [orglinks.c:75-134] creates **new POOM nodes** pointing to these new I-addresses:

```c
movetumbler (&lstream, &crumorigin.dsas[I]);   // orglinks.c:105
movetumbler (vsaptr, &crumorigin.dsas[V]);     // orglinks.c:113
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V); // orglinks.c:130
```

Result: The bytes are re-stored at completely new I-addresses. The old I-addresses (where links were registered in `spanf`) now point to content that still exists in `granf` but has no POOM mapping in this document. **Links are severed.**

---

### REARRANGE path

`fns.c:159` → `dorearrange` [do1.c:34-43] → `rearrangepm` [orglinks.c:137-142]:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);  // orglinks.c:139
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`rearrangend` [edit.c:78-160] — the decisive function. The only mutations to POOM nodes are at line 125:

```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
ivemodified((typecorecrum*)ptr);
```

where `index = V` (passed in from `rearrangepm`, `orglinks.c:139`).

This modifies **only `cdsp.dsas[V]`** — the V-dimension displacement (document position). The field `cdsp.dsas[I]` — the I-dimension displacement (permascroll coordinate) — is **never touched**. The `diff[]` offsets computed by `makeoffsetsfor3or4cuts` [edit.c:164-183] are pure arithmetic rearrangements of the cut positions, applied only in V-space.

Four things REARRANGE does NOT do:
1. It does not call `disown` or `subtreefree` — no POOM nodes are destroyed
2. It does not call `insertseq` or `inserttextgr` — no new granf entries are created
3. It does not allocate new I-addresses
4. It does not touch `spanf`

The same POOM nodes exist before and after REARRANGE. Their I-coordinates are bit-for-bit identical. They have merely shifted in V-space. The link infrastructure in `spanf` keys on I-addresses. Since those I-addresses are unchanged and still reachable through the (repositioned) POOM nodes, **all link and transclusion relationships survive intact**.

---

### Why Link Lookup Survives Rearrange But Not Delete+Insert

Link finding goes through `specset2sporglset` [referenced in spanf1.c:70-75], which converts a V-address specset into I-address sporglsets by looking up through the POOM. That intermediate result is then used to query `spanf` by I-address in `retrievesporglsetinrange` [spanf1.c:237-267].

After **REARRANGE**: The POOM still maps the *new* V-position `c` → the same I-addresses as the *old* V-position `a`. The spanf lookup by those I-addresses still finds the registered link endpoints. Links are discoverable.

After **DELETE + INSERT**: The POOM maps V-position `c` → *new* I-addresses. The spanf lookup by *new* I-addresses finds nothing (links were registered against the *old* I-addresses). Old I-addresses are orphaned from V-space. Links are lost.

---

### Summary

REARRANGE is structurally distinct from all other edit operations:

- **DELETE** destroys POOM nodes (`disown`/`subtreefree`, edit.c:59-60), orphaning I-addresses
- **INSERT** creates new granf entries at freshly allocated I-addresses (`inserttextgr`, granf2.c:92-109), never reusing old ones
- **COPY** does the same as INSERT for the POOM side
- **REARRANGE** shifts only `cdsp.dsas[V]` in existing POOM nodes (edit.c:125), leaving `cdsp.dsas[I]`, `granf`, and `spanf` entirely untouched

REARRANGE is therefore the **only** edit operation that relocates content in V-space without altering the I-addresses of the content. It is the only operation under which previously established link and transclusion relationships survive a positional move.
