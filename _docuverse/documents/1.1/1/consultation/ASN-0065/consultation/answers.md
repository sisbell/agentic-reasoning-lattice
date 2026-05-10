# Consultation Answers — REARRANGE Operation

**Inquiry:** What is the precise effect of reordering segments of Vstream content by cut points? What is preserved about content identity, what changes about position, and what invariants must the completed operation maintain?
**Date:** 2026-03-21 18:53
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When segments of a document's content stream are rearranged by cut points, does every byte of content retain its original identity, or does the act of repositioning create new content?

### Nelson's Answer

## Every byte retains its original identity. Rearrangement is purely a Vstream operation.

This is one of the clearest consequences of the Istream/Vstream separation. When you rearrange content, you change the **arrangement** (Vstream mapping), not the **content** (Istream addresses). The bytes themselves are untouched.

### The architectural basis

Content lives permanently in Istream. A document's Vstream is a mapping — an ordered sequence of references to Istream addresses. Rearranging cut-point regions changes which Istream addresses appear at which Vstream positions, but the Istream content is immutable:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The REARRANGE operation transposes regions of the virtual byte stream:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

This is a pure remapping. The V-addresses shift; the I-addresses do not.

### Why this must be so

Three guarantees depend on content identity surviving rearrangement:

1. **Link survivability.** Links attach to bytes via I-addresses. If rearrangement created new content, links would break on every edit. Instead:

   > "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

2. **Correspondence across versions.** Version comparison works because shared I-addresses identify "the same content." If rearrangement generated new I-addresses, two versions differing only in paragraph order would appear to share nothing — defeating the entire intercomparison facility:

   > "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

3. **Transclusion integrity.** If document B transcludes a span from document A, and document A rearranges that span's position, the transclusion must still resolve. It does, because B's reference is to the I-address, which is unaffected by A's Vstream changes:

   > "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

### The analogy

Think of a library and a reading list. Rearranging the reading list changes the order you encounter the books — it does not create new books. The library stacks (Istream) never change. The reading lists (Vstream) can be reordered freely.

### Summary

Repositioning content is an operation on the **view**, not on the **content**. The Istream is append-only — bytes are added, never overwritten, never regenerated. Every editorial operation (insert, delete, rearrange, copy) changes the Vstream mapping while leaving the permanent Istream identity of every byte intact. This is not a design choice that could have gone either way; it is the foundation on which permanence, link survivability, correspondence, and transclusion all rest.

---

## Question 2 [nelson]

> If a link addresses a span of content that is split by a cut point during rearrangement, must the link continue to address exactly the same content bytes, even though they now occupy non-contiguous positions?

### Nelson's Answer

## Yes — absolutely and by design.

This is one of the most important architectural consequences of Xanadu's Istream/Vstream separation. A link addresses **bytes by their permanent I-addresses**, not by their current positions in the document's Vstream. When REARRANGE splits the span, the link continues to address exactly the same bytes. The endset simply becomes discontiguous in Vstream terms.

### Three interlocking guarantees make this work:

**1. Links attach to bytes, not positions.**

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap" metaphor is precise: the strap is tied to the bytes themselves. Move the bytes around and the strap follows.

**2. Rearrangement changes Vstream, not Istream.**

REARRANGE is a pure Vstream operation — it changes the *arrangement* of content in the document's virtual byte stream, but the underlying I-addresses of every byte remain permanent and unchanged. Since links point to I-addresses, the link is unaffected by the rearrangement.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

**3. Discontiguous endsets are explicitly supported.**

Nelson anticipated exactly this scenario. The result of a rearrangement splitting a linked span is that the endset becomes a discontiguous set of bytes — and this is a first-class concept:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

### The survivability guarantee is explicit:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Note that **rearrangements** are named specifically alongside deletions and insertions. And since rearrangement preserves all bytes (it moves them, doesn't remove them), "anything is left at each end" is trivially satisfied — the link survives with its full original byte set intact.

### What the user sees

After rearrangement, a front end resolving the link's endset would find the same bytes now occupying two non-adjacent regions of the Vstream. The front end could:

- Highlight both regions as the link's extent
- Present them as a single logical selection spanning a gap
- Allow navigation to "the next piece" of the linked content

The system doesn't need to "fix" or "update" the link after rearrangement. The link was always pointing to I-addresses, which never changed. Only the V-to-I mapping changed — and that's the document's concern, not the link's.

---

## Question 3 [nelson]

> After rearrangement, does the document's content stream contain exactly the same set of content as before — no additions, no losses — or may rearrangement discard or duplicate material?

### Nelson's Answer

## REARRANGE Is Content-Preserving

After rearrangement, the document's content stream contains **exactly the same set of content** — no additions, no losses, no duplications. Nelson's specification is unambiguous on this point.

### The Specification

From LM 4/67 (page 234):

> "Rearrange **transposes** two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3. With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4."

The word **transposes** is precise. A transposition swaps two things — it is a permutation, not a transformation that can add, remove, or duplicate content. The two identified regions exchange positions; everything else stays where it is.

### Three-Cut vs Four-Cut

- **Three cuts** (A, B, C): Swaps the adjacent regions [A..B] and [B..C]
- **Four cuts** (A, B, C, D): Swaps the non-adjacent regions [A..B] and [C..D]

In both cases the operation is a swap. The document afterward contains the same bytes in a different Vstream order.

### Architectural Confirmation

REARRANGE is a **pure Vstream operation**. It changes the arrangement of content in the virtual byte stream without touching Istream (permanent storage). Nelson's FEBE command set separates concerns cleanly:

| Operation | Effect on content |
|-----------|-------------------|
| INSERT | Adds new bytes (extends Istream) |
| DELETE | Removes from Vstream (Istream unchanged) |
| COPY | Maps existing Istream content into Vstream (transclusion) |
| APPEND | Adds new bytes at end |
| **REARRANGE** | **Reorders Vstream — no Istream change** |

From LM 4/30 (page 197), confirming the Vstream-only nature:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."

Links survive rearrangement precisely *because* the bytes themselves are unchanged — only their Vstream positions shift.

### Summary

REARRANGE is a content-preserving transposition. The Vstream before and after contains the identical multiset of I-address references. No bytes are created, destroyed, or duplicated. This follows necessarily from the Istream/Vstream separation: REARRANGE modifies the mapping (which Istream content appears at which Vstream position), not the content itself.

---

## Question 4 [nelson]

> Must the system preserve a record of the original ordering so that the prior arrangement can be recovered, or is rearrangement a one-way transformation of document structure?

### Nelson's Answer

The system **must preserve the original ordering**. Rearrangement is not a one-way transformation. This follows from multiple converging guarantees in Literary Machines.

## The Storage Model Requires It

Nelson's storage architecture is explicitly append-only. Changes accumulate; nothing is overwritten:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

The phrase "any previous instant" is key. Not "any previous version" — any previous *instant*. This means every edit, including REARRANGE, produces a recoverable state.

## The I/V Separation Makes It Structural

REARRANGE is a pure Vstream operation. It changes which Istream addresses appear at which Vstream positions. The content bytes are untouched:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The prior arrangement is simply a prior V→I mapping. Since Istream content is immutable and the storage system records all changes chronologically, the old mapping is recoverable by reconstructing the state before the REARRANGE was applied.

## Historical Backtrack Is a Design Requirement

Nelson treats recoverability not as a feature but as the fundamental purpose of the storage system:

> "Under many circumstances the writer, or 'text user', needs to reach back to a former condition. This is in the nature of creative work." [LM 2/14]

> "Being able to go back through changes, and perhaps restore an earlier state, is called the problem of historical backtrack." [LM 3/13]

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

The "historical trace enfilade" was specifically designed for this purpose:

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

## The Ongoing Braid Metaphor

Nelson's central metaphor makes one-way transformation architecturally incoherent:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

A braid accumulates strands. It does not cut them away. REARRANGE adds a new twist to the braid; the prior twist remains in the structure.

## One Nuance: Version Boundaries vs. Continuous History

The FEBE protocol separates *editing within a version* (INSERT, DELETE, REARRANGE) from *creating a new version* (CREATENEWVERSION). The curated sources establish that the storage system records all changes at all times, not merely at version boundaries — Nelson says "successive instants of time," not "successive versions." But the exact granularity of recovery (every keystroke? every command? every save?) is not specified at the FEBE level.

What IS specified is the principle: the system keeps all former changes, and any previous instant can be reconstructed. REARRANGE is a change. Therefore the prior arrangement is kept and recoverable.

NEED_RAW: [4/67] — The REARRANGE command specification may contain additional detail about whether it implicitly creates a recoverable checkpoint. The curated source only gives the mechanical description ("transposes two regions of text").

---

## Question 5 [nelson]

> When a segment is moved to a new position in the content stream, do the positions of all other segments shift to accommodate it, and must the system guarantee that no two segments occupy the same position?

### Nelson's Answer

## Yes — on Both Counts

The answer requires distinguishing Xanadu's two address spaces, because they behave very differently.

### Vstream: Positions Always Shift

The Vstream (virtual byte stream) is the document's current arrangement. It is always **dense and contiguous** — positions run from 1 to N with no gaps. Every editing operation preserves this property:

**INSERT** explicitly shifts all subsequent positions:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

**DELETE** closes the gap:

> "This removes the given span from the given document." [LM 4/66]

**REARRANGE** transposes two regions, which necessarily reassigns V-addresses for everything between and including the transposed regions:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

Nelson confirms that V-addresses are ephemeral by design:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

And:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

So yes: when a segment moves, **all other V-positions shift** to maintain the contiguous sequence. And yes: **no two segments can occupy the same V-position** — the virtual byte stream is a linear sequence where each position maps to exactly one byte.

### Istream: Nothing Ever Moves

The Istream is permanent, append-only storage. Content at an I-address **never changes and never moves**:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

I-addresses are unique by construction — each new byte gets the next sequential address in the document's content space. There is no mechanism to reassign or overlap I-addresses.

### The Architecture That Makes This Work

The document IS the mapping from V-addresses to I-addresses. The POOM enfilade maintains this mapping efficiently:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The "canonical order" mandate is exactly the guarantee you're asking about — after every operation, the mapping is in a valid, consistent state with no overlaps or gaps in Vstream.

### Summary

| Property | Vstream | Istream |
|----------|---------|---------|
| Positions shift on edit? | **Yes** — always dense, always contiguous | **No** — permanent, append-only |
| Unique positions guaranteed? | **Yes** — each V-position maps to exactly one byte | **Yes** — each I-address holds exactly one byte |
| Content "moves"? | Yes — content is rearranged in the virtual view | Never — content stays at its creation address forever |

The system separates **arrangement** (Vstream, mutable) from **identity** (Istream, permanent). Rearranging content changes the arrangement; the identity remains fixed. Links point to I-addresses and thus survive all rearrangements.

---

## Question 6 [nelson]

> If a document transcludes content from another document and that transcluded region is split by a cut point during rearrangement, does the transclusion relationship survive intact for each resulting piece?

### Nelson's Answer

## Yes — the transclusion survives intact for each piece

The answer follows directly from the Istream/Vstream architecture. Let me trace through the mechanics.

### What transclusion actually is

A transclusion is not a pointer or a reference object — it is a **Vstream-to-Istream mapping**. When document B transcludes bytes from document A, B's Vstream contains entries that map to A's Istream addresses. Those bytes are "non-native" to B:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The transclusion relationship IS the I-address identity. There is no separate "transclusion record" that could be broken — the relationship is encoded in the addresses themselves.

### What REARRANGE does

REARRANGE is a **pure Vstream operation**. It transposes regions of the virtual byte stream:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3..." [LM 4/67]

V-addresses shift. I-addresses do not. Nelson is explicit about this separation:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

### The split scenario

Suppose document B transcludes a 100-byte region from document A (I-addresses A.1 through A.100), appearing at V-positions 50–149 in B. A REARRANGE with a cut point at V-position 80 splits this into two Vstream regions:

- **Piece 1**: still maps to I-addresses A.1–A.30
- **Piece 2**: still maps to I-addresses A.31–A.100

Each piece retains its I-address mapping to A's content. The bytes are still "native elsewhere" — still fetched from their home locations in A. The system still knows their origin because:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

FINDDOCSCONTAINING would still return document A for both pieces, because:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

### Why this must be so

The entire architecture is designed to make Vstream operations non-destructive to content identity:

- **Istream is permanent**: content at an I-address never changes
- **Vstream is ephemeral**: V-addresses shift freely during editing
- **Identity is structural**: the I-address encodes the home document in its tumbler fields (Node.0.User.0.Document.0.Element)

DELETE confirms the same principle from the other direction:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If deletion doesn't sever transclusion for *other* documents, rearrangement certainly doesn't sever it within the *same* document. Both are Vstream operations that leave I-address identity untouched.

### Summary

The transclusion relationship survives because it is not a fragile pointer that a cut can sever — it is the **identity of the bytes themselves**. Each byte's I-address permanently encodes its origin. REARRANGE changes where bytes appear in the Vstream; it cannot change what they are or where they came from. After the split, you have two Vstream regions, each still composed of bytes whose home is the source document, each still fetchable from that source, each still attributable and royalty-generating.

---

## Question 7 [nelson]

> Does rearrangement change what content the document contains, or only the order in which that content appears — and is this distinction a fundamental design guarantee?

### Nelson's Answer

## Rearrangement Changes Order, Not Content — and This Is Architectural

**Yes**, rearrangement changes only the order in which content appears, never what content the document contains. **Yes**, this distinction is a fundamental design guarantee — it falls directly from the Istream/Vstream separation, which is the deepest architectural invariant in Xanadu.

### What REARRANGE Does

The REARRANGE operation transposes regions of text within a document:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

Transposition is pure reordering. Region A moves to where Region B was, and vice versa. No bytes are created, destroyed, or modified. The same Istream content is present in the document before and after — only the Vstream positions change.

### Why This Is Architecturally Guaranteed

The Istream/Vstream separation makes this inevitable, not merely conventional:

- **Istream** is where content permanently lives. Addresses are absolute and immutable. Content at an Istream address never changes.
- **Vstream** is the document's current arrangement — a mapping from visual positions to permanent Istream addresses.

A document IS this mapping. Nelson says:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

REARRANGE modifies the V→I mapping (which Istream bytes appear at which Vstream positions) but cannot touch Istream itself. The bytes are the same bytes, at the same permanent addresses, with the same identity. They just appear in a different sequence.

### REARRANGE Is More Conservative Than DELETE

This is worth noting. DELETE removes content from the Vstream — the bytes vanish from the current view (though they survive in Istream and remain accessible via historical backtrack). REARRANGE doesn't even do that. It keeps every byte visible in the current version; it only permutes their positions. Of all editing operations, rearrangement is the most purely structural.

### Link Survivability Confirms the Guarantee

The fact that links survive rearrangement is not a happy accident — it's a direct consequence of content-addressed linking:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

Links attach to Istream addresses (content identity), not Vstream positions (current arrangement). Rearrangement changes positions, not identity. Therefore links are completely unaffected.

### The Braid Metaphor

Nelson's metaphor captures this precisely:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." [LM 2/15]

The strands of the braid (Istream content) are permanent. Rearrangement re-twists the weaving (Vstream arrangement) — the same strands, a different pattern. The braid changes shape; its fibers do not.

### Summary

| Property | Changed by REARRANGE? |
|----------|----------------------|
| Istream content (what bytes exist) | No — immutable |
| Istream addresses (where bytes live permanently) | No — permanent |
| Vstream arrangement (what order bytes appear) | **Yes** — this is all it does |
| Links to content | No — they attach to I-addresses |
| Version history | No — previous arrangement preserved |
| Document identity | No — same content, different view |

The distinction between content and arrangement is not a policy choice or implementation detail. It is the foundational invariant of Xanadu's architecture — the separation of identity (Istream) from view (Vstream). Rearrangement, by definition, operates entirely within Vstream. It cannot touch Istream because nothing can.

---

## Question 8 [nelson]

> When two previously non-adjacent segments become adjacent through rearrangement, does the system treat the boundary between them differently from content that was originally contiguous?

### Nelson's Answer

## Boundary Treatment After Rearrangement

**Short answer:** The system structurally distinguishes the boundary at the Istream level, but the user sees no difference at the Vstream level. This is not a special case — it's how *every* edit works.

### The Architecture Makes This Clear

Xanadu's two-address-space design means every document is a sequence of **spans** — contiguous runs of V-addresses that map to contiguous I-addresses. Whenever consecutive V-positions map to non-contiguous I-positions, there is a span boundary in the internal mapping (the POOM enfilade).

After REARRANGE transposes two regions, the V-addresses are re-densified — no gaps, contiguous from 1 to N. But the V→I mapping now has additional discontinuities at the new adjacency points. Where segments A and B have been placed next to each other, the last I-address of A and the first I-address of B are not consecutive.

### What the User Sees: No Difference

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, **regardless of their native origin.**" [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream **just as if they were native** to the document." [LM 4/11]

The V-stream presents a seamless view. The user navigates across these boundaries without any indication that the content was rearranged. V-address 50 follows V-address 49 whether or not they share I-stream origin.

### What the System Knows: Structural Distinction

At the I-level, the boundary is real and detectable:

1. **Correspondence and version comparison.** SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. It can identify exactly where the rearrangement occurred by comparing the V→I mappings of the two versions. The span that was contiguous in version 1 is now split across two positions in version 2.

2. **Origin traceability.** Bytes on either side of the boundary still carry their original I-addresses, which encode their home document. The rearrangement doesn't change any I-address — it only changes the V→I mapping.

3. **Link behavior.** Links attach to I-addresses, not V-positions. A link spanning the pre-rearrangement boundary continues to reference the same bytes. A link that pointed to content on one side of the new boundary still works because:

   > "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

### This Is the Normal Case, Not a Special Case

Every editing operation creates or modifies span boundaries:

- **INSERT** adds new I-content at a point, creating two new span boundaries (before and after the insertion)
- **DELETE** may merge two formerly separated spans if content between them is removed
- **COPY** (transclusion) creates spans pointing to another document's I-space
- **REARRANGE** reorders existing spans

The POOM enfilade was specifically designed to handle this efficiently:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order." [LM 1/34]

### The Analogy

Think of the reading-list analogy from the Istream/Vstream model. Rearranging a reading list (moving chapter references around) changes what you see in what order, but doesn't alter the library shelves. The "boundary" between two books placed adjacent on your reading list is invisible to you as a reader — you just read one after the other — but the librarian knows they live on different shelves.

### Summary

| Level | Boundary visible? | Why |
|-------|-------------------|-----|
| **Vstream (user)** | No | V-addresses are dense and contiguous; content appears seamless |
| **POOM (mapping)** | Yes | Span boundary where V→I mapping is discontinuous |
| **Istream (storage)** | Yes | I-addresses remain at their original, non-adjacent positions |
| **Correspondence** | Yes | Version comparison reveals the rearrangement through span pairs |
| **Links** | No | Links follow I-addresses, unaffected by V rearrangement |

Nelson does not discuss this boundary explicitly — because in his architecture, there is nothing special about it. It is the *default* condition. A document that has undergone any editing at all is a patchwork of spans with boundaries between them. The entire design exists to make these boundaries invisible to users while preserving them for the system's structural guarantees.

NEED_RAW: [4/67, 4/30-4/31] — The REARRANGE operation description and the version/element addressing detail may contain additional specifics about how rearranged spans are represented internally. The curated sources cover the architectural answer well, but those pages might add implementation-level nuance.

---

## Question 9 [nelson]

> Must a rearrangement operation be expressible purely in terms of the document's own content stream, or can it reference content positions as they exist in other documents that share the same material?

### Nelson's Answer

## REARRANGE Operates Purely on the Document's Own Vstream

A rearrangement must be expressed entirely in terms of the document's own virtual byte stream. It cannot reference positions in other documents, even when those documents share the same Istream content.

### The Evidence

**REARRANGE is document-scoped.** The operation takes cuts that are positions within a single document:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

**All editing operations target a specific document.** INSERT takes `<doc id>` and `<doc vsa>` (a document virtual stream address). DELETEVSPAN removes "the given span from the given document." REARRANGE follows the same pattern — the cuts are V-addresses within the target document.

**REARRANGE is a pure Vstream operation.** It changes the arrangement of content without touching Istream. The concept mapping in [LM 4/11] lists REARRANGE alongside other editing operations that modify Vstream only.

### Why Other Documents Are Irrelevant

The V-address space treats all content uniformly, regardless of origin:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, **regardless of their native origin.**" [LM 4/11]

A document's Vstream already includes transcluded content from other documents. When you rearrange, you operate on V-addresses — and those V-addresses cover both native and non-native bytes indistinguishably. There is no need (and no mechanism) to reach into another document's address space.

### The Key Distinction

- **REARRANGE** = reorder content within your document's Vstream arrangement. All cuts are V-addresses in your document.
- **COPY** = bring content from another document into yours. This is the only editing operation that crosses document boundaries: "The material determined by `<spec set>` is copied to the document determined by `<doc id>` at the address determined by `<doc vsa>`." [LM 4/67]

COPY is how foreign content enters your Vstream. Once it's there, REARRANGE (and DELETE, INSERT) work on V-addresses without knowing or caring where the bytes originated. The I-address encodes origin permanently, but the V-address — which is what editing operations use — is purely local.

### Principle

This follows from the Istream/Vstream separation. Istream is identity (permanent, global, shared across documents). Vstream is arrangement (ephemeral, local, per-document). Editing operations — including REARRANGE — work on arrangement, not identity. They are scoped to a single document's Vstream by design.

---

## Question 10 [nelson]

> After rearrangement, if a reader follows a link into the rearranged document, must they arrive at the same content they would have reached before the rearrangement, regardless of its new position within the document?

### Nelson's Answer

## Yes — the reader arrives at the same content, regardless of its new position.

This is one of Xanadu's most fundamental architectural guarantees, and it follows directly from the two-address-space design.

### Why rearrangement cannot affect link targets

Links attach to **Istream addresses** (permanent content identity), not to **Vstream addresses** (current positions). REARRANGE is a pure Vstream operation — it changes where bytes appear in the document's current arrangement, but the bytes themselves remain at their permanent Istream addresses. Since links point to Istream, they are completely unaffected.

Nelson states this explicitly:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

And more broadly:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

### The mechanism

The Vstream position of a byte — its location in the document as currently arranged — is explicitly described as irrelevant to the link system:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

So when a reader follows a link into a rearranged document:

1. The link resolves to the same Istream bytes it always pointed to
2. The system locates those bytes in the document's current Vstream arrangement
3. The reader sees the same content, now at its new position

The reader arrives at the **same words**, even though those words may now be on a different "page" of the document. The link followed the content, not the position.

### The strap metaphor

Nelson's visualization captures this perfectly: a link is a "strap between bytes." If you rearrange the bytes (move paragraphs around), the strap stays attached to the same bytes and stretches to wherever they now sit. The strap doesn't care about position — it cares about identity.

---

## Question 11 [gregory]

> In `rearrangend`, how does `rearrangecutsectionnd` classify each POOM bottom crum relative to the 3 or 4 cut points — what are the distinct region categories, and which offset is applied to entries in each region?

### Gregory's Answer

## KB Synthesis

## `rearrangecutsectionnd` — Region Classification and Offset Application

The KB has detailed coverage of this in [ST-REARRANGE] (Finding 0056).

### Classification Scheme

`rearrangend` first calls `sortknives()` to order cut points ascending, then `makeoffsetsfor3or4cuts()` to compute displacement vectors. `rearrangecutsectionnd` then classifies each POOM bottom crum by its V-position relative to the sorted cuts, assigning it to a numbered section:

**Pivot (3 cuts: `cut0 < cut1 < cut2`)**

| Section | Region | Offset Applied |
|---------|--------|---------------|
| 0 | `v < cut0` (before first cut) | 0 — unchanged |
| 1 | `cut0 ≤ v < cut1` (first region) | `diff[1] = cut2 - cut1` (moves forward by size of region 2) |
| 2 | `cut1 ≤ v < cut2` (second region) | `diff[2] = -(cut1 - cut0)` (moves backward by size of region 1) |
| 3 | `v ≥ cut2` (after last cut) | 0 — unchanged |

**Swap (4 cuts: `cut0 < cut1 < cut2 < cut3`)**

| Section | Region | Offset Applied |
|---------|--------|---------------|
| 0 | `v < cut0` | 0 — unchanged |
| 1 | `cut0 ≤ v < cut1` (first swap region) | `diff[1] = cut2 - cut0` (moves to where region 3 was) |
| 2 | `cut1 ≤ v < cut2` (middle) | `diff[2] = (cut3 - cut2) - (cut1 - cut0)` (shifts by size difference of swapped regions) |
| 3 | `cut2 ≤ v < cut3` (second swap region) | `diff[3] = -(cut2 - cut0)` (moves to where region 1 was) |
| 4 | `v ≥ cut3` | 0 — unchanged |

### Offset Application

The offset is applied unconditionally via `tumbleradd` on the V-dimension displacement only:

```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])
```

Only `cdsp.dsas[V]` is modified — I-addresses are never touched [INV-REARRANGE-IDENTITY].

### Key Properties

- **No subspace guard**: `rearrangecutsectionnd` has no check that the resulting V-position stays within the same subspace digit. Cross-subspace cuts (e.g., spanning `1.x` into `2.x`) produce valid arithmetic but semantically invalid states [PRE-REARRANGE] (Finding 0051), [EC-REARRANGE-CROSS-SUBSPACE].

- **Cut points are in pre-move space**: All classification and offset computation references only the original (pre-operation) V-positions. There is no iterative re-classification [ST-REARRANGE] (Finding 0056).

- **Exterior regions are frame conditions**: Sections 0 and (3 or 4) — the content before `cut0` and after the final cut — satisfy the frame condition [FC-REARRANGE-EXTERIOR]: their V-positions and I-addresses are unchanged.

- **Empty regions are no-ops**: If `cutN == cutN+1`, no crums fall in that section, so no offsets are applied for it. The offset arithmetic is still computed but has no targets [EC-REARRANGE-EMPTY-REGION].

- **I-addresses preserved throughout**: Because only `cdsp.dsas[V]` is modified, the multiset of I-addresses in the document is identical before and after — the pure V-permutation property [INV-REARRANGE-IDENTITY] (Finding 0056).

---

## Code Exploration

I now have all the data I need. Here is the complete analysis.

---

## How `rearrangecutsectionnd` Classifies POOM Bottom Crums

### 1. Prerequisites: Constants and `whereoncrum`

**`common.h:86-90`** defines the five positional constants:

```
TOMYLEFT        = -2   address strictly left of crum
ONMYLEFTBORDER  = -1   address exactly at crum's left edge
THRUME          =  0   address strictly inside crum
ONMYRIGHTBORDER =  1   address exactly at crum's right edge
TOMYRIGHT       =  2   address strictly right of crum
```

**`retrie.c:345-398`** — `whereoncrum` for POOM/SPAN computes the crum's absolute interval in dimension `index` as:

```c
left  = offset->dsas[index] + ptr->cdsp.dsas[index]
right = left + ptr->cwid.dsas[index]
```

and returns where `address` (a blade tumbler) falls relative to `[left, right)`. The critical threshold in the classifier is `cmp <= ONMYLEFTBORDER`, which fires when `address ≤ left` (blade is at or before the crum's start).

---

### 2. The Classifier: `rearrangecutsectionnd`

**`edit.c:191-204`**:

```c
INT rearrangecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
  INT i, cmp;

    for (i = knives->nblades -1; i >= 0 ; --i) {
        cmp = whereoncrum (ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME) {
            return (-1);
        } else if (cmp <= ONMYLEFTBORDER) {
            return (i+1);
        }
    }
    return (0);
}
```

**Algorithm:** Scan blades right-to-left (highest index first). For each blade `i`:

- `THRUME` → blade falls **strictly inside** the crum → return `-1` (error; impossible after `makecutsnd` has split the tree at all blades)
- `cmp <= ONMYLEFTBORDER` → blade `i` is **at or to the left** of the crum's start → return `i+1`
- Otherwise (`ONMYRIGHTBORDER` or `TOMYRIGHT`) → blade is to the crum's right; keep scanning leftward

If no blade satisfies the condition, return `0`.

The blades are sorted ascending before this call (`sortknives`, **`edit.c:250-263`**), so scanning from the highest index finds the **rightmost blade that is ≤ the crum's left edge**. The region number is that blade's index plus one.

---

### 3. The Five Regions

With `N` blades sorted `B[0] ≤ B[1] ≤ … ≤ B[N-1]`, `rearrangecutsectionnd` partitions every bottom crum into regions 0 through N:

| Return | Name | Condition on crum's left edge `L` | Position |
|--------|------|------------------------------------|----------|
| `0`   | Before all blades | `L < B[0]` | Crum entirely left of first cut |
| `1`   | Region 1 | `B[0] ≤ L < B[1]` | Crum starts at or after B[0] but before B[1] |
| `2`   | Region 2 | `B[1] ≤ L < B[2]` | Crum starts at or after B[1] but before B[2] |
| `3`   | Region 3 | `B[2] ≤ L < B[3]` (4-cut only) | Crum starts at or after B[2] but before B[3] |
| `4`   | After all blades | `B[3] ≤ L` (4-cut only) | Crum entirely right of last cut |

The boundary rule: a crum whose left edge **coincides with** blade `i` (i.e., `ONMYLEFTBORDER`) is classified into region `i+1` — it belongs to the region **to the right** of that blade.

For 3-cut calls, the maximum region is 3. For 4-cut calls, the maximum is 4.

---

### 4. Dispatch and Offset Application in `rearrangend`

**`edit.c:113-136`** applies the classification:

```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = ...) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case -1:
          gerror ("rearrangend can't classify crum\n");
      case 0:  case 4: /* these never move */
          break;
      case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
          tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
          ivemodified((typecorecrum*)ptr);
          break;
    }
}
```

- Regions `0` and `4` → **stationary**: no offset applied, crum stays put
- Regions `1`, `2`, `3` → **displaced**: `diff[region]` is added to `ptr->cdsp.dsas[index]`

The comment "3 only moves in 4 cuts" is technically accurate because `diff[3] = 0` in the 3-cut case (see below), making the add a no-op.

---

### 5. The Offset Values: `makeoffsetsfor3or4cuts`

**`edit.c:164-184`** — `diff[0]` is unused (no region 0 displacement). `diff[1..3]` vary by arity:

#### 3-cut case (`edit.c:177-181`)

```c
tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);  // diff[1] = B[2] - B[1]
tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]);  // diff[2] = B[1] - B[0]
diff[2].sign = !diff[2].sign;                                    // diff[2] = -(B[1]-B[0]) = B[0]-B[1]
tumblerclear (&(diff[3]));                                       // diff[3] = 0
```

(`tumblersub(a, b, c)` computes `c = a − b`, confirmed at **`tumble.c:406-429`** where the general path negates `b` and calls `tumbleradd`.)

| Region | Offset | Meaning |
|--------|--------|---------|
| 0 | — | Stationary |
| 1 | `B[2] - B[1]` | Forward shift: source content jumps to destination |
| 2 | `B[0] - B[1]` (negative) | Backward shift: the gap between source-end and destination closes |
| 3 | `0` | No-op (region 3 = after destination, nothing moves) |

This implements a **copy/move**: [B[0], B[1]) is the source span, B[2] is the insertion point. The source content (region 1) slides forward to the destination; material between source and destination (region 2) slides backward by the source width to close the hole.

#### 4-cut case (`edit.c:169-176`)

```c
tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));  // diff[1] = B[2] - B[0]
tumblersub (&knives->blades[1], &knives->blades[0], &a);           // a = B[1] - B[0]
tumblersub (&knives->blades[3], &knives->blades[2], &b);           // b = B[3] - B[2]
tumblersub (&b, &a, &(diff[2]));                                   // diff[2] = (B[3]-B[2]) - (B[1]-B[0])
movetumbler (&diff[1], &diff[3]);                                  // diff[3] = B[2] - B[0]
diff[3].sign = !diff[1].sign;                                      // diff[3] = -(B[2]-B[0]) = B[0]-B[2]
```

| Region | Offset | Meaning |
|--------|--------|---------|
| 0 | — | Stationary |
| 1 | `B[2] - B[0]` (positive) | First span slides right to where second span was |
| 2 | `(B[3]-B[2]) - (B[1]-B[0])` | Gap between spans adjusts for size difference |
| 3 | `B[0] - B[2]` (negative) | Second span slides left to where first span was |
| 4 | — | Stationary |

This implements a **transposition**: [B[0],B[1]) and [B[2],B[3]) are two non-overlapping spans; region 1 and region 3 swap positions, and the intervening gap (region 2) adjusts by the difference in their widths.

---

### 6. Entry Point Context

`rearrangend` is the POOM-level worker called from `rearrangepm` (**`orglinks.c:137-142`**), which is invoked by `dorearrange` (**`do1.c:34-43`**). The `cutseqptr` argument carries the 3 or 4 blade tumblers describing the rearrangement; `index = V` (the V dimension of the POOM). The call to `makecutsnd` (**`edit.c:110`**) splits the enfilade at each blade before classification, guaranteeing that no blade ever lands `THRUME` inside a leaf crum during the sweep — any `-1` return is a fatal error.

---

## Question 12 [gregory]

> When a cut point falls in the interior of an existing POOM bottom crum (not on a boundary), does `rearrangend` split the crum into two pieces before applying offsets, or does it treat the entire crum as belonging to one region?

### Gregory's Answer

## KB Synthesis

The KB does not describe a crum-splitting phase for `rearrangend`, and the evidence strongly indicates there is none.

**REARRANGE does not split crums at cut points.** It classifies each existing crum as a whole and displaces it as a unit.

The key evidence:

**Finding 0056** (`ST-REARRANGE`) explicitly states: *"No new I-addresses are allocated, no content is duplicated in the permascroll, and the same enfilade nodes (crums) are retained."* The operation calls `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], ...)` — updating each crum's V-displacement by the offset for whatever section the crum falls into. The crum structure is not restructured.

**Contrast with DELETE.** `PRE-DELETE` (Finding 0075) documents that DELETE *does* have a Phase 1 cutting step: `makecutsbackuptohere()` calls `slicecbcpm` whenever `whereoncrum() == THRUME` (strictly interior). This splits boundary-straddling crums before classifying them. REARRANGE has no equivalent Phase 1 — `rearrangecutsectionnd()` classifies crums directly and `tumbleradd` displaces them, with the code references limited to `edit.c:78-184` and no mention of `slicecbcpm`.

**Practical consequence.** If a cut point falls in the interior of a crum, the entire crum is classified into one section (based on where its grasp falls relative to the cuts) and displaced by that section's offset. Content at the other end of the crum — which logically belongs to a different region — moves with it. This is consistent with `EC-PIVOT-LINK-FRAGMENTATION` (Finding 0019), which documents unexpected endset fragmentation and duplication after pivot, suggesting the rearrangement produces internally fragmented state when crum boundaries don't align with cut points.

The KB does not specify the exact criterion `rearrangecutsectionnd()` uses to classify a straddling crum (e.g., whether it uses the crum's grasp or reach), but since crums are never split, any straddling crum is assigned wholesale to one of the regions.

---

## Code Exploration

Now I have everything I need. Let me trace the full execution path carefully.

---

## Answer

**`rearrangend` splits the crum first, then applies offsets. A cut through a crum's interior is never ignored — it is a hard precondition that must be resolved before any offset arithmetic begins.**

Here is the complete call sequence with line citations.

---

### Step 1: `rearrangend` calls `makecutsnd` before touching any offsets

`edit.c:110`:
```c
makecutsnd (fullcrumptr, &knives);
```

This is the very first substantive operation in `rearrangend`, called *before* the loop that applies offsets at `edit.c:113–136`. The offset application loop only runs after `makecutsnd` returns.

---

### Step 2: `makecutsnd` recursively ensures no crum straddles any knife

`ndcuts.c:15–31`:
```c
int makecutsnd(typecuc *fullcrumptr, typeknives *knives) {
    makecutsdownnd(fullcrumptr, &offset, knives);
    for (...; sonsarecut(fullcrumptr, &offset, knives); ...) {
        makecutsdownnd(fullcrumptr, &offset, knives);
    }
}
```

`sonsarecut` (`ndcuts.c:359–371`) tests every son with `whereoncrum == THRUME`. The outer loop keeps calling `makecutsdownnd` until no son is cut through. The function terminates only when the tree is clean.

---

### Step 3: At the bottom crum, `makecutsbackuptohere` detects THRUME and physically splits

`ndcuts.c:77–91`:
```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset,
                        &knives->blades[i], knives->dimension) == THRUME) {
            new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
            ...
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new,
                       &knives->blades[i], knives->dimension);
            ivemodified((typecorecrum*)ptr);
            ivemodified((typecorecrum*)new);
        }
    }
    return(0);
}
```

`THRUME` is defined in `common.h:88` as `0` — the return value of `whereoncrum` when the address lies **strictly inside** the crum (left boundary < address < right boundary). When that condition fires for a bottom crum (height == 0), the crum is not skipped or approximated — a new sibling is allocated and `slicecbcpm` is called immediately.

---

### Step 4: `slicecbcpm` performs the physical split

`ndcuts.c:373–450`:
```c
int slicecbcpm(typecorecrum *ptr, typewid *offset, typecorecrum *new,
               tumbler *cut, INT index)
{
    prologuend(ptr, offset, &grasp, NULL);
    // guard: must be THRUME
    if (whereoncrum(ptr, offset, cut, index) != THRUME)
        gerror("Why are you trying to slice me?\n");
    // guard: must be single-story width
    if (!lockis1story(ptr->cwid.dsas, widsize(enftype)))
        gerror("Not one story in POOM wid\n");

    tumblersub(cut, &grasp.dsas[index], &localcut);  // cut point relative to crum start

    movewisp(&ptr->cwid, &newwid);
    for (i = 0; i < widsize(enftype); i++) {
        newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
        tumblerjustify(&newwid.dsas[i]);
    }
    locksubtract(&ptr->cwid, &newwid, &new->cwid, widsize(enftype));  // right half width
    movewisp(&newwid, &ptr->cwid);                                     // left half stays in ptr
    dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);              // right half starts at cut
    move2dinfo(&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);
    adopt(new, RIGHTBRO, ptr);  // insert new as right sibling
}
```

The arithmetic is precise:
- `localcut = cut − grasp.dsas[index]` — the cut position relative to the crum's own left edge
- The original crum `ptr` is truncated to width `localcut` (left piece)
- `new` gets width `original_width − localcut` (right piece)
- `new->cdsp` is set so it starts exactly at the cut point

After `slicecbcpm`, the one crum that spanned the cut has become two adjacent crums, with the boundary between them sitting exactly on the knife.

---

### Step 5: After `makecutsnd`, the tree is guaranteed clean — THRUME is a fatal error

Back in `rearrangend`, the classification loop calls `rearrangecutsectionnd` on every child:

`edit.c:113–136`:
```c
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = rearrangecutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case -1:
        gerror ("rearrangend can't classify crum\n");  // edit.c:118
      case 0:  case 4:
        break;
      case 1:  case 2:  case 3:
        tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
        ivemodified(ptr);
        break;
    }
}
```

`rearrangecutsectionnd` at `edit.c:191–204`:
```c
INT rearrangecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives) {
    for (i = knives->nblades - 1; i >= 0; --i) {
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME)
            return (-1);          // → gerror in caller
        else if (cmp <= ONMYLEFTBORDER)
            return (i+1);
    }
    return (0);
}
```

If any crum still returns `THRUME` here, the code aborts with `gerror`. The `-1` / `gerror` path is not a fallback — it is a correctness assertion. The design contract is: *`makecutsnd` must eliminate all THRUME bottom crums before the offset loop runs.*

---

### Step 6: Tree-structure cleanup follows offset application

`edit.c:141`:
```c
(void)splitcrumupwards(fullcrumptr);
```

`split.c:16–44` handles the case where the slicing added children and a parent now has too many sons. This is structural balancing, not further splitting of crums at the cut boundary.

---

## Conclusion

When a cut point falls in the interior of a POOM bottom crum, `rearrangend` **physically splits that crum into two pieces** before applying any offsets. The split is performed by `slicecbcpm` (`ndcuts.c:373`), called from `makecutsbackuptohere` (`ndcuts.c:84`), called from `makecutsnd` (`ndcuts.c:15`) — which `rearrangend` invokes at `edit.c:110` as its very first action. After `makecutsnd` completes, every bottom crum lies entirely within one inter-knife region. The offset-application loop (`edit.c:113–136`) then assigns each such crum to a region (0–4) and adjusts its displacement accordingly. A crum that straddles a knife at offset-application time is a fatal invariant violation, caught by the `gerror` at `edit.c:118`.

---

## Question 13 [gregory]

> In `makeoffsetsfor3or4cuts`, how are the tumbler offsets for each region derived from the cut positions — is it pure arithmetic on the cut-point differences, and does the computation use `tumblersub`/`tumbleradd` or a different mechanism?

### Gregory's Answer

## KB Synthesis

Yes, the computation is pure arithmetic on cut-point differences, and it uses `tumblersub`/`tumbleradd` throughout. The full picture from the KB:

## Offset derivation: `makeoffsetsfor3or4cuts`

The function takes only `knives->blades[]` as input — no content, no enfilade state. It computes a displacement tumbler `diff[i]` for each region purely from cut-position arithmetic [ST-REARRANGE, Finding 0056].

**Pivot (3 cuts), `cut0 < cut1 < cut2`:**
- `diff[1] = cut2 - cut1` (region 1 shifts forward by the size of region 2)
- `diff[2] = -(cut1 - cut0)` (region 2 shifts backward by the size of region 1)

**Swap (4 cuts), `cut0 < cut1 < cut2 < cut3`:**
- `diff[1] = cut2 - cut0`
- `diff[2] = (cut3 - cut2) - (cut1 - cut0)` (middle shifts by the size difference)
- `diff[3] = -(cut2 - cut0)`

The subtracted quantities (`cut2 - cut1`, etc.) are computed via `tumblersub`. Negative offsets like `-(cut1 - cut0)` are produced using the sign-magnitude mechanism: `tumblersub(a, b)` where `b > a` sets `sign=1` on the result, yielding a valid negative tumbler rather than underflow [SS-TUMBLER, Finding 0053].

The offsets are then applied by `rearrangend` via `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], &ptr->cdsp.dsas[V])` — the V-address component of each matching POOM crum is updated in place, I-addresses untouched [ST-REARRANGE, Finding 0056, code ref `edit.c:125`].

**One pre-processing step:** `sortknives()` normalizes the cuts to ascending order before `makeoffsetsfor3or4cuts` runs, so misordered input is silently accepted [PRE-REARRANGE, Finding 0056]. All cut-point references are in the pre-move address space; there is no reference to post-move state anywhere in the computation.

---

## Code Exploration

Now I have everything needed. Here is the full analysis.

---

## `makeoffsetsfor3or4cuts`: Complete Analysis

### Function Location

`backend/edit.c:164–184`

```c
/* Prepares offsets for both 3 and 4 cut rearranges */

int makeoffsetsfor3or4cuts(typeknives *knives, tumbler diff[])
{
  tumbler a, b;

	/* diff[0] is simply ignored */
	if (knives->nblades == 4) {
		tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));
		tumblersub (&knives->blades[1], &knives->blades[0], &a);
		tumblersub (&knives->blades[3], &knives->blades[2], &b);
		tumblersub (&b, &a, &(diff[2]));
/*		tumblersub (&knives->blades[0], &knives->blades[2], &(diff[3]));*//* should be <0 */
		movetumbler (&diff[1], &diff[3]);
		diff[3].sign = !diff[1].sign;
	} else if (knives->nblades == 3) {
		tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);
		tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]); /* should be negative */
		diff[2].sign = !diff[2].sign;
		tumblerclear (&(diff[3]));
	} else
		gerror ("Wrong number of cuts.");
}
```

### Context: What `diff[]` Is For

The caller is `rearrangend` [`edit.c:78`]. After computing the cuts and classifying each crum into a numbered section (0–4), it applies the offset:

```c
// edit.c:125
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

So `diff[i]` is the signed displacement to add to every crum's stored address offset (`dsas`) in region `i`. Region 0 and (in 4-cut) region 4 never move — they are short-circuited before this line. `diff[0]` is explicitly ignored [`edit.c:168`].

The blades array is sorted ascending by `sortknives` before `makeoffsetsfor3or4cuts` is called [`edit.c:107`]. Denote the sorted cuts as **C0 < C1 < C2 < C3**.

---

### 4-Cut Case (`nblades == 4`)

```c
tumblersub(&blades[2], &blades[0], &diff[1]);   // diff[1] = C2 - C0
tumblersub(&blades[1], &blades[0], &a);          // a      = C1 - C0  (width of region 1)
tumblersub(&blades[3], &blades[2], &b);          // b      = C3 - C2  (width of region 3)
tumblersub(&b, &a, &diff[2]);                    // diff[2] = b - a = (C3-C2) - (C1-C0)
movetumbler(&diff[1], &diff[3]);                 // diff[3] = copy of diff[1]
diff[3].sign = !diff[1].sign;                    // diff[3] = -(C2 - C0)
```

| Region | Shift applied | Expression |
|--------|--------------|------------|
| 1 (`[C0,C1)`) | `+diff[1]` | `+(C2 − C0)` |
| 2 (`[C1,C2)`) | `+diff[2]` | `+(C3−C2) − (C1−C0)` = width(region 3) − width(region 1) |
| 3 (`[C2,C3)`) | `+diff[3]` | `−(C2 − C0)` |

**Semantic result:** Region 1 jumps forward by `C2−C0` (the combined span of itself and region 2), landing at position `C2`. Region 3 jumps backward by the same `C2−C0`, landing at `C0`. Region 2 shifts by the width difference between the two swapped outer regions. This is a transposition: regions 1 and 3 swap positions in address space, with region 2 adjusting to remain between them.

**Note on the commented-out line** [`edit.c:174`]:
```c
/*  tumblersub (&knives->blades[0], &knives->blades[2], &(diff[3])); */ /* should be <0 */
```
The original approach computed `diff[3] = C0 − C2` (which is naturally negative). The current code replaces this with a copy-and-sign-flip: `movetumbler(&diff[1], &diff[3]); diff[3].sign = !diff[1].sign;`. Both produce `-(C2−C0)`, but the current version avoids a redundant subtraction.

---

### 3-Cut Case (`nblades == 3`)

```c
tumblersub(&blades[2], &blades[1], &diff[1]);    // diff[1] = C2 - C1  (width of region 2)
tumblersub(&blades[1], &blades[0], &diff[2]);    // diff[2] = C1 - C0  (width of region 1)
diff[2].sign = !diff[2].sign;                    // diff[2] = -(C1 - C0)  [comment: "should be negative"]
tumblerclear(&diff[3]);                          // diff[3] = 0 (unused)
```

| Region | Shift applied | Expression |
|--------|--------------|------------|
| 1 (`[C0,C1)`) | `+diff[1]` | `+(C2 − C1)` = width of region 2 |
| 2 (`[C1,C2)`) | `+diff[2]` | `−(C1 − C0)` = −width of region 1 |
| 3 (unused)    | `+0`       | no movement |

**Semantic result:** Region 1 steps forward by the width of region 2; region 2 steps backward by the width of region 1. Their positions swap. This is a two-block cut-and-paste.

---

### How `tumblersub` Works

`tumblersub(a, b, c)` at `backend/tumble.c:406` computes `c = a − b`:

```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    if (iszerotumbler(bptr))
        movetumbler(aptr, cptr);
    else if (tumblereq(aptr, bptr))
        tumblerclear(cptr);
    else if (iszerotumbler(aptr)) {
        movetumbler(bptr, cptr);
        cptr->sign = !cptr->sign;
    } else {
        movetumbler(bptr, &temp);
        temp.sign = !temp.sign;   // negate b
        tumbleradd(aptr, &temp, cptr);  // then add
    }
    tumblerjustify(cptr);
}
```

It implements subtraction by **negating `b` (flipping its `.sign` flag) and calling `tumbleradd`**. `tumbleradd` (`tumble.c:365`) then dispatches to `absadd`, `strongsub`, or `weaksub` depending on whether the signs match.

So the chain is: `tumblersub` → negate sign → `tumbleradd` → (`absadd` | `strongsub` | `weaksub`). The subtraction in `makeoffsetsfor3or4cuts` always resolves to differences of sorted cut positions, so inputs to `tumblersub` are always non-negative tumblers with the larger value first — meaning `tumbleradd` always routes through `absadd` or `strongsub`, never `weaksub`.

---

### The Direct Sign Flip (Not `tumblersub`)

For `diff[3]` in the 4-cut branch and `diff[2]` in the 3-cut branch, negation is accomplished by **directly flipping `.sign`**, not by calling `tumblersub`:

```c
// 4-cut:
diff[3].sign = !diff[1].sign;    // edit.c:176

// 3-cut:
diff[2].sign = !diff[2].sign;    // edit.c:180
```

This is cheaper than a subtraction call. It relies on the fact that the magnitude is already correct and only the direction needs flipping. `tumblerclear` is never called to zero a diff before use in the signed arithmetic — the sign bit is simply toggled in-place on an already-computed result.

---

### Summary

Yes, the computation is **pure arithmetic on cut-point differences**, exclusively using `tumblersub` (which internally delegates to `tumbleradd`). `tumbleradd` does not appear directly in `makeoffsetsfor3or4cuts` — all arithmetic enters through `tumblersub`. Negation of already-computed results is done by **direct `.sign` bit toggling** (`!diff[i].sign`), not by calling `tumblersub` again. The offsets are derived from three geometric quantities: the span between the outer cut pair (`C2−C0`), and the individual widths of the two outer regions (`C1−C0`, `C3−C2`), combined to produce signed displacements that swap the outer regions while adjusting the middle.

---

## Question 14 [gregory]

> Does REARRANGE create, modify, or remove any spanfilade entries, or does it exclusively mutate the document's POOM while leaving the spanfilade and granfilade completely untouched?

### Gregory's Answer

## KB Synthesis

REARRANGE exclusively mutates the document's POOM and leaves both the spanfilade and the granfilade's content layer completely untouched.

**What REARRANGE actually does**

REARRANGE operates on the POOM by computing displacement offsets from the cut positions and applying them via `tumbleradd` to the V-address component (`cdsp.dsas[V]`) of affected orgl entries [ST-REARRANGE]. The I-address component (`cdsp.dsas[I]`) is never modified. No new I-addresses are allocated, no permascroll entries are created, and no enfilade nodes are freed or replaced — only V-position values shift [INV-REARRANGE-IDENTITY].

**Spanfilade: completely untouched**

The spanfilade contains two structures: the link endpoint index (I-address → link ISA) and the DOCISPAN index (I-address → document ISA). REARRANGE calls neither `insertspanf` nor any removal function from the spanf codebase. This matches the general pattern established for all non-insert operations: `rearrangend` (like `deletend`) operates exclusively on the document's orgl enfilade (POOM layer) with no calls to spanf functions [INV-SPANF-WRITE-ONLY, FC-CONTENT-SPANF-ISOLATION].

Because I-addresses are unchanged, the DOCISPAN entries correctly continue to assert that the document contains those I-addresses — no entries become stale, and no new entries are needed. Link endpoint entries likewise remain valid since the links reference I-addresses, not V-positions [INV-REARRANGE-LINK-SURVIVAL].

**Granfilade content: completely untouched**

The granfilade's content layer (permascroll text atoms, link orgls) is frame-preserved by REARRANGE. The explicit frame condition is: `∀ op ∈ {DELETE, REARRANGE} : granf_content_after(op) = granf_content_before(op)` [FC-GRANF-ON-DELETE]. REARRANGE is grouped with DELETE in this invariant — neither creates new I-addresses, neither frees permascroll content. This is observable: `compare_versions` before and after a rearrange reports all content as shared (same I-addresses), confirming zero granfilade change [INV-REARRANGE-IDENTITY, Finding 0018].

**Implication for link discovery**

Since the spanfilade is unmodified, `find_links` results are invariant under REARRANGE. Links bound to rearranged content remain discoverable because they are indexed by I-address, which REARRANGE never changes [INV-REARRANGE-LINK-SURVIVAL]. The V-position rendering of link endpoints will shift (resolved through the updated POOM), but the underlying link objects and their I-address-based discoverability are unaffected.

**Summary**

| Layer | Effect of REARRANGE |
|-------|-------------------|
| POOM (V→I mappings) | Modified — V-displacements shifted |
| Granfilade content (permascroll/orgls) | Unchanged — no allocation or deletion |
| Spanfilade link index | Unchanged — no insertspanf calls |
| Spanfilade DOCISPAN index | Unchanged — no insertspanf calls |

---

## Code Exploration

I now have all the evidence needed. Here is the complete analysis.

---

## Answer: REARRANGE Exclusively Mutates the POOM

REARRANGE does **not** create, modify, or remove any spanfilade or granfilade entries. It is a pure POOM mutation. Here is the proof by complete call-chain tracing.

---

### 1. The Entry Point: `dorearrange` — No Spanfilade Touch

`do1.c:34-43`:
```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
  typeorgl docorgl;
  bool findorgl(), rearrangepm();;

    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    /*&& TRUE*/ /* ht stuff */  );
}
```

Compare this to `docopy` at `do1.c:53-65`, which explicitly calls **both** `insertpm` (POOM) and `insertspanf` (spanfilade), or `docreatelink` at `do1.c:219` which calls `insertendsetsinspanf`. `dorearrange` calls neither. There is no reference to `spanf` at this level.

---

### 2. `rearrangepm` — Calls Only `rearrangend` on the POOM

`orglinks.c:137-142`:
```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`docorgl` is the **POOM enfilade root** returned from `findorgl(taskptr, granf, ...)`. It is passed directly to `rearrangend`. There is no `spanf` reference anywhere in this function.

Compare to `deletevspanpm` immediately below at `orglinks.c:145-152`, which calls `deletend((typecuc*)docorgl, ...)` on the same POOM root. Neither delete nor rearrange touches the spanfilade; only insert/copy operations do.

---

### 3. `rearrangend` — Operates Entirely Within the Passed POOM Tree

`edit.c:78-160`. The function signature:
```c
int rearrangend(typecuc *fullcrumptr, typecutseq *cutseqptr, INT index)
```

`fullcrumptr` is `docorgl` — the POOM root. Every operation inside touches only this tree:

| Operation | Where | What it touches |
|---|---|---|
| `makecutsnd(fullcrumptr, &knives)` | `ndcuts.c:15` | Splits POOM crums at cut boundaries |
| `newfindintersectionnd(fullcrumptr, ...)` | `ndinters.c:38-42` | Returns `fullcrumptr` itself (trivially) |
| `rearrangecutsectionnd(ptr, ...)` | `edit.c:191` | Classifies POOM child nodes |
| `tumbleradd(&ptr->cdsp.dsas[index], ...)` | `edit.c:125` | Adjusts V-axis offsets in POOM nodes |
| `ivemodified((typecorecrum*)ptr)` | `edit.c:127` | Marks POOM nodes dirty |
| `setwispupwards(father, 1)` | `edit.c:137` | Propagates POOM wid sums upward |
| `recombine(fullcrumptr)` | `edit.c:139` | Merges POOM nodes |
| `splitcrumupwards(fullcrumptr)` | `edit.c:141` | Splits over-full POOM nodes |

There is no reference to `spanf`, `granf`, or any other global enfilade pointer within `rearrangend`.

---

### 4. `findfullcrum` Cannot Escape the POOM Apex

`makecutsnd` at `ndcuts.c:24` loops using `findfullcrum`:
```c
for (fullcrumptr = findfullcrum((typecorecrum*)fullcrumptr); sonsarecut(...); ...)
```

`findfullcrum` is defined at `genf.c:89-95`:
```c
typecuc *findfullcrum(typecorecrum *descendant)
{
    for (ptr = (typecuc*)descendant; !isfullcrum((typecorecrum*)ptr); ptr = findfather((typecorecrum*)ptr));
    return (ptr);
}
```

And `isfullcrum` is defined at `enf.h:176`:
```c
#define isfullcrum(x) ((bool)((typecorecrum *)(x))->isapex)
```

`docorgl` is the POOM apex (`isapex == TRUE`). `findfullcrum` called on it returns immediately — the loop never walks upward into a parent structure. All `makecutsnd` iterations stay within the POOM tree rooted at `docorgl`.

---

### 5. `splitcrum` and `recombine` Dispatch on `cenftype` — Stay POOM

`recombine` at `recombine.c:22-34` dispatches:
```c
case POOM:
    recombinend (father);
```

`splitcrum` at `split.c:49-66` dispatches:
```c
case POOM:
    splitcrumpm(father);
```

`splitcrumpm` at `split.c:117-128` calls `peelcrumoffnd`, which creates new crums via `createcrum((INT)father->height, (INT)father->cenftype)` — the `cenftype` is `POOM`, so all newly created crums are POOM crums, adopted into the POOM tree.

Similarly `makecutsbackuptohere` at `ndcuts.c:80` creates new crums with `createcrum((INT)ptr->height, (INT)ptr->cenftype)` — same `cenftype` inheritance, all POOM.

---

### Conclusion

REARRANGE is a **pure POOM mutation**. It repositions sections of content within the document's V-space by:
1. Slicing the POOM at the specified cut positions (`makecutsnd`)
2. Adjusting the V-axis displacement (`cdsp.dsas[V]`) of the nodes that fall in each cut section (`tumbleradd`)
3. Rebalancing the POOM tree (`recombine`, `splitcrumupwards`)

The spanfilade records which I-spans (permascroll addresses) are endpoints of which links in which documents. REARRANGE changes where content sits in V-space but does **not** change the underlying permascroll addresses — the I-spans are stable. Therefore it is both mechanically correct (no `spanf` pointer is ever referenced) and semantically correct (the spanfilade's invariants are not disturbed) that the spanfilade and granfilade are completely untouched.

---

## Question 15 [gregory]

> If a 3-cut pivot is issued where cut `a` is in text subspace `1.x` and cut `c` crosses into link subspace `2.x`, does `rearrangend` proceed and relocate link POOM entries into text V-positions (or vice versa), or does some other guard prevent this?

### Gregory's Answer

## KB Synthesis

Yes — `rearrangend` proceeds unconditionally and will relocate POOM entries across subspace boundaries. No guard prevents this.

## What happens

`rearrangend` in `edit.c:78-160` executes the same pipeline regardless of cut geometry [ST-REARRANGE/Finding 0056]:

1. **Sort cuts** — `sortknives()` normalizes to ascending order
2. **Compute offsets** — `makeoffsetsfor3or4cuts()` derives tumbler displacements purely arithmetically from cut positions:
   - `diff[1] = c - b` (region between cuts a and b moves forward)
   - `diff[2] = -(b - a)` (region between cuts b and c moves backward)
3. **Classify spans** — `rearrangecutsectionnd()` assigns each POOM entry to a section
4. **Apply offsets** — `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], ...)` — no subspace check anywhere

## Concrete consequence

With cuts at `[1.1, 1.4, 2.5]` [PRE-REARRANGE/Finding 0051]:

```
diff[1] = 2.5 - 1.4 = 1.1   → text "ABC" at V:1.1–1.3 displaced to V:2.2–2.4
diff[2] = -(1.4 - 1.1) = -0.3 → link orgl at V:2.1 displaced down into 1.x range
```

Text bytes end up in the link subspace; link orgl references end up in the text subspace. `retrieve_contents` at `2.x` returns text bytes [EC-REARRANGE-CROSS-SUBSPACE].

## Why no guard stops this

The two mechanisms that protect INSERT and DELETE do not apply here:

- **INSERT** uses a deliberate two-blade knife with `blade[1]` at `(N+1).1`, structurally confining shifts to one subspace [FC-SUBSPACE/Finding 0054, SS-TWO-BLADE-KNIFE]
- **DELETE** accidentally benefits from `strongsub`'s exponent guard, which returns the minuend unchanged when `width.exp < entry.vpos.exp` [FC-SUBSPACE/Finding 0055, INT-DELETE-SUBSPACE-ASYMMETRY]

REARRANGE uses `tumbleradd`, which has no equivalent cross-exponent guard. The offset arithmetic crosses subspace digit-0 boundaries without restriction [ST-REARRANGE/Finding 0056].

## Missing precondition

The spec requires a precondition not implemented in the code [PRE-REARRANGE/Finding 0051]:

```
requires ∀ orgl ∈ affected(cuts):
  subspace(vpos(orgl) + diff[section(orgl)]) == subspace(vpos(orgl))
```

Without it, a pivot spanning `1.x` and `2.x` produces a well-formed (no crash) but semantically invalid document state, violating `INV-SUBSPACE-CONVENTION` [INV-SUBSPACE-CONVENTION/Finding 0051].

---

## Code Exploration

Here is the complete answer.

---

## Cross-Subspace Pivot in `rearrangend`: Full Analysis

### Short Answer

`rearrangend` has **no guard whatsoever** against cross-subspace pivots. When cut `a` is in text subspace `1.x` and cut `c` is in `2.x`, the operation proceeds normally, relocates POOM entries by pure tumbler arithmetic, and leaves content stranded in the wrong subspace. This is confirmed by a golden test.

---

### Call Chain

The FEBE `REARRANGE` command arrives at:

**`do1.c:34-43`** — `dorearrange` passes directly to `rearrangepm` with no pre-flight checks:
```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    );
}
```

**`orglinks.c:137-142`** — `rearrangepm` is a one-liner that passes the cut sequence straight to `rearrangend`:
```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

No validation at either layer.

---

### Inside `rearrangend` [`edit.c:78-160`]

The function takes the cuts and dimension index:

```c
// edit.c:102-107 — copy cuts into knives array; no subspace check
knives.dimension = index;
knives.nblades = cutseqptr->numberofcuts;
for (i = 0; i < knives.nblades; i++) {
    movetumbler (&cutseqptr->cutsarray[i], &knives.blades[i]);
}
sortknives (&knives);                          // line 107 — pure numeric sort
makeoffsetsfor3or4cuts (&knives, diff);        // line 108 — pure arithmetic
makecutsnd (fullcrumptr, &knives);             // line 110 — makes the cuts
```

Then for every crum under the pivot root:

```c
// edit.c:113-135
for (ptr = (typecuc*)findleftson(father); ptr; ...) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case 1:  case 2:  case 3:
        tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]); // line 125
        ivemodified((typecorecrum*)ptr);
        break;
    }
}
```

Line 125 blindly adds the computed offset to every crum in the affected regions — text POOM, link POOM, SPAN, all treated identically.

---

### Offset Arithmetic [`edit.c:164-184`]

For a 3-cut pivot with cuts `a`, `b`, `c`:

```c
// edit.c:177-181
tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);   // diff[1] = c - b
tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]);   // diff[2] = b - a
diff[2].sign = !diff[2].sign;                                     // diff[2] = -(b - a)
```

With your specific case — `a = 1.1`, `b = 1.4`, `c = 2.5`:
- `diff[1] = 2.5 − 1.4 = 1.1` — region 1 (between `a` and `b`) moves forward by 1.1
- `diff[2] = −(1.4 − 1.1) = −0.3` — region 2 (between `b` and `c`) moves backward by 0.3

A crum at V-position `1.2` (in region 1) would be relocated to `1.2 + 1.1 = 2.3`. It is now in the `2.x` subspace. `tumbleradd` [tumble.c:365-404] is purely positional addition with no awareness that `1.x` and `2.x` are semantically distinct subspaces.

---

### Why `whereoncrum` Cannot Save It

`rearrangecutsectionnd` uses `whereoncrum` [retrie.c:345-398] to classify each crum:

```c
// retrie.c:354-372 — SPAN and POOM case
case SPAN:
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    cmp = tumblercmp(address, &left);
    if (cmp == LESS)   return(TOMYLEFT);
    if (cmp == EQUAL)  return(ONMYLEFTBORDER);
    tumbleradd (&left, &ptr->cwid.dsas[index], &right);
    cmp = tumblercmp(address, &right);
    // ...
```

`tumblercmp` [tumble.c:72-85] compares `exp` then `mantissa[i]` lexicographically — it treats the entire V-space as a single ordered line. Comparing `1.2` vs `2.5` works numerically; there is no concept of a subspace boundary encoded in that comparison. The crum will be classified as `TOMYLEFT` of cut `c` and thereby assigned to region 1, and its V-position will be offset.

---

### What Happens to Link POOM Entries

Links are stored with V-positions in `0.x` (confirmed by `do1.c:377-411`, the `filter_vspanset_to_text_subspace` fix, which identifies link positions as those with stream `< 1.0`). In the scenario described:

- Cut `a = 1.1` is above `0.x`, so link POOM crums at `0.x` are entirely **to the left of all cuts** — they fall into region 0 (`case 0` at `edit.c:122`), which is the "these never move" branch.
- Text POOM crums between `1.1` and `1.4` fall into region 1 and are relocated into `2.x`.

So the specific cross-contamination is: **text content moves into link subspace `2.x`**, not the reverse. Link entries at `0.x` are unaffected because they lie outside the cut window entirely.

---

### Confirmed by Golden Test

Finding `0051-rearrange-crosses-subspace-boundaries.md` (status: **Validated**) documents exactly this:

> Pivot with cuts at 1.1, 1.4, 2.5  
> Content "ABC" is retrievable from 2.x subspace: `retrieve_after_2x: ['ABC']`  
> vspanset after shows: `at 0 for 0.2, at 1 for 1`

The golden test file is `golden/rearrange/pivot_cross_subspace_boundary.json`.

---

### The Contrast: Where Subspace *Is* Filtered

The only subspace guard in the codebase is in `do1.c:377-426` (`filter_vspanset_to_text_subspace`, `filter_specset_to_text_subspace`), applied only in `doshowrelationof2versions` [do1.c:428]. That fix was added reactively (Bug 009) for the compare-versions query path. It was **not** applied to `rearrangend`, and there is no analogous check anywhere in the rearrange path.

---

### Summary

| Question | Answer |
|---|---|
| Does `rearrangend` guard against cross-subspace pivots? | No. Zero validation at any level. |
| Where would a guard need to go? | Before `edit.c:125`, or in `makeoffsetsfor3or4cuts`, checking that `diff[i]` applied to crums in that region stays within the same top-level digit of V-space. |
| Does the operation corrupt POOM? | Yes — text POOM entries in the `1.x` region between cuts `a` and `b` are relocated into `2.x` by pure `tumbleradd` arithmetic. |
| Do link POOM entries (`0.x`) get relocated into text V-positions? | Not by this specific pivot (cuts `1.x`→`2.x`), because `0.x` falls outside all cut windows. But a pivot whose `a` cut is placed at `0.x` would drag link POOM entries into text space. |
| Is this an implementation bug or intended behavior? | Finding 0051 leaves it open. The spec question is whether REARRANGE is supposed to respect CD0 or operate purely spatially. The code is purely spatial. |

---

## Question 16 [gregory]

> What happens in `rearrangend` when the supplied cut points are outside the document's current V-span — does the function detect this and abort, silently produce a no-op, or apply offsets to whatever entries happen to be in range?

### Gregory's Answer

## KB Synthesis

The KB doesn't have a finding that directly probes this specific scenario, but the behavior is fully derivable from what's documented.

## No detection or abort — silent no-op for out-of-range cuts

**Step 1: No bounds validation exists.** [PRE-REARRANGE] (Finding 0056) documents only two precondition checks: `|cuts| ∈ {3,4}` (enforced with abort) and `sortknives()` which silently reorders misordered cuts. There is no check that cut points fall within the document's V-span. [ST-REARRANGE] (Finding 0056) confirms the algorithm is pure offset arithmetic — `rearrangend()` calls `makeoffsetsfor3or4cuts()` then classifies each orgl via `rearrangecutsectionnd()` and applies `tumbleradd()`. No bounds comparison occurs before this loop.

**Step 2: Classification handles out-of-range content correctly.** `rearrangecutsectionnd()` assigns each POOM orgl a section number based on its V-position relative to the sorted cuts. For a pivot `[c0, c1, c2]`:

- Orgls with `vpos < c0` → section 0, diff = 0 (no movement)
- Orgls with `c0 ≤ vpos < c1` → section 1, diff = `c2 - c1`
- Orgls with `c1 ≤ vpos < c2` → section 2, diff = `-(c1 - c0)`
- Orgls with `vpos ≥ c2` → exterior, diff = 0 (no movement)

If cuts are entirely beyond the document's V-span, every orgl falls in section 0 (diff = 0). If cuts are entirely before the document's V-span, every orgl falls in the exterior (diff = 0). In both cases: no orgl is modified.

**Step 3: Empty regions are explicitly handled.** [EC-REARRANGE-EMPTY-REGION] states: "If a region `[cutN, cutN+1)` contains no content, it contributes to offset computation but doesn't move anything. The algorithm operates per-span, and empty regions simply have no spans to process." When cuts are entirely outside the document, every region between the cuts is also empty — the offsets are computed (diff[1], diff[2] get nonzero values) but there are no orgls classified into those sections to receive them.

**Step 4: No cross-section contamination.** The two-blade knife used by INSERT would normally guard subspace boundaries, but rearrange uses a different mechanism (`rearrangecutsectionnd`). As documented in [ST-REARRANGE] (Finding 0056), the exterior of the cut range always receives diff = 0 regardless of arithmetic — the offset table only contains nonzero entries for the interior sections.

## Summary

`rearrangend` produces a silent no-op when all cut points fall outside the document's V-span. The function computes offsets, iterates all orgls, classifies each as exterior (section 0 or terminal), applies diff = 0, and exits with the POOM unmodified. No error is returned, no backend abort occurs, and the front end receives a success response (per the response-before-check pattern documented in [EC-RESPONSE-BEFORE-CHECK]).

---

## Code Exploration

Now I have everything I need. Here is the complete analysis.

---

## What `rearrangend` does when cut points are outside the document's V-span

### Call chain (no bounds checking anywhere)

```
fns.c:159    rearrange()
do1.c:39     → dorearrange() → rearrangepm()
orglinks.c:137-142  → rearrangepm() calls rearrangend((typecuc*)docorgl, cutseqptr, V) then returns TRUE
edit.c:78    → rearrangend()
```

`rearrangepm` [orglinks.c:137-142] is a literal one-liner that passes the cut sequence straight through:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

There is **no validation of cut positions against the document's V-span at any level**: not in `fns.c`, not in `do1.c`, not in `rearrangepm`, and not in `rearrangend` itself.

---

### Step 1: `makecutsnd` — splitting crums at the cut positions

`rearrangend` [edit.c:110] calls `makecutsnd(fullcrumptr, &knives)`, which calls `makecutsdownnd` [ndcuts.c:33], which calls `makecutsbackuptohere` [ndcuts.c:69].

The critical inner test is in `makecutsbackuptohere` [ndcuts.c:77-91]:

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
            // only splits when THRUME
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], ...);
```

`whereoncrum` [retrie.c:355-373] for POOM/SPAN computes:

```
left  = offset.dsas[index] + ptr->cdsp.dsas[index]
right = left + ptr->cwid.dsas[index]
```

and returns one of `{TOMYLEFT, ONMYLEFTBORDER, THRUME, ONMYRIGHTBORDER, TOMYRIGHT}`. A split (call to `slicecbcpm`) **only happens when the return is `THRUME`**, i.e., when the cut address strictly falls inside a crum's extent.

**If a cut point is outside the document's V-span, it will be either `TOMYRIGHT` (past the right end) or `TOMYLEFT` (before the left start) for every crum. `slicecbcpm` is never called for that cut. No crum is split at that position.** Out-of-span cuts produce no structural changes to the enfilade in phase 1.

---

### Step 2: `newfindintersectionnd` — the stub that changed everything

`rearrangend` [edit.c:111] calls `newfindintersectionnd`. The old traversal-based `findintersectionnd` that descended to the common-ancestor crum is entirely commented out [ndinters.c:18-37]. The current implementation [ndinters.c:38-42] is a stub:

```c
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives, typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;
    clear(offset, sizeof(*offset));
}
```

`father` is always set to `fullcrumptr` (the document root) and `foffset` is always zero. `prologuend(father, &foffset, &fgrasp, NULL)` [retrie.c:334-339] then computes `fgrasp = foffset + father->cdsp = fullcrumptr->cdsp` — the root's own displacement (zero for a well-formed full crum).

**Consequence:** The loop at [edit.c:113] always iterates over the direct children of the document root, not over a narrowed subtree.

---

### Step 3: `rearrangecutsectionnd` — classifying each crum

For each child `ptr`, `rearrangecutsectionnd` [edit.c:191-204] is called:

```c
for (i = knives->nblades -1; i >= 0; --i) {
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME)      return (-1);           // error — cut passes through, should have been split
    else if (cmp <= ONMYLEFTBORDER) return (i+1);  // knife is left of or at crum's left border
}
return (0);   // all knives are to the right of this crum
```

The logic is: iterate knives from highest to lowest. Return the index of the rightmost knife that is **at or to the left of** the crum's start. Return 0 if no knife qualifies (all knives are `TOMYRIGHT`).

---

### Step 4: `makeoffsetsfor3or4cuts` — the displacement table

The precomputed displacement table [edit.c:164-184] for sorted blades b0 < b1 < b2 (3-cut case):

```c
diff[1] = b2 - b1      // moves section 1 forward to the destination
diff[2] = -(b1 - b0)   // moves section 2 back by selection length (negated)
diff[3] = 0            // explicit tumblerclear
```

For 4-cut:
```c
diff[1] = b2 - b0
diff[2] = (b3 - b2) - (b1 - b0)
diff[3] = -(b2 - b0)   // negated diff[1]
case 4 → explicitly "never moves"
```

---

### Behavior for the three out-of-bounds cases

#### Case A: All cuts are **beyond the document's right end** (all blades `> right_end`)

For any crum `ptr`:
- `whereoncrum(ptr, offset, blade[i], V)` returns `TOMYRIGHT` for all `i` — the blade is to the right of the crum
- In `rearrangecutsectionnd`: all iterations return `TOMYRIGHT` (not `<= ONMYLEFTBORDER`), loop falls through → **returns 0**
- In `rearrangend` [edit.c:122-123]: `case 0` → **no displacement applied**
- `makecutsnd` made no splits
- **Result: complete silent no-op.** The enfilade is structurally unchanged. `setwispupwards` and `recombine` run but find nothing to do.

#### Case B: All cuts are **before the document's left start** (all blades `< left_start`)

For any crum `ptr`:
- `whereoncrum(ptr, offset, blade[i], V)` returns `TOMYLEFT` for all `i`
- In `rearrangecutsectionnd`: i starts at `nblades-1`; first knife is `TOMYLEFT` → `<= ONMYLEFTBORDER` → returns `nblades`
  - **3-blade cut**: returns 3 → `diff[3] = 0` (explicitly cleared by `tumblerclear`) → displacement added is zero → **no-op**
  - **4-blade cut**: returns 4 → `case 4` is grouped with `case 0` as "these never move" [edit.c:122-123] → **no-op**
- **Result: complete silent no-op.**

#### Case C: **Partial overlap** — some cuts in-span, some outside

This is the dangerous case.

`makecutsnd` will split crums at the in-span cut positions but produce **no splits** at the out-of-span positions. The enfilade is thus partially restructured: cut boundaries exist at some of the blade positions but not all.

`makeoffsetsfor3or4cuts` performs **pure tumbler arithmetic** on all the blade values with no awareness of document bounds [edit.c:164-184]. For example, in a 3-cut rearrangement where blade[2] (the destination) is outside the document's right end:

```
diff[1] = blade[2] - blade[1]
```

This is computed as a large positive tumbler value. In the classification loop, crums classified as section 1 (between blade[0] and blade[1], i.e., the selected region) receive:

```c
tumbleradd(&ptr->cdsp.dsas[V], &diff[1], &ptr->cdsp.dsas[V]);  // edit.c:125
ivemodified((typecorecrum*)ptr);                                  // edit.c:127
```

The displacement is applied unconditionally. The crums are moved to a V-address that is outside the document's current span — or into negative/undefined tumbler space if the blade was before the left start.

**There is no check, no abort, no rollback.** The `ivemodified` call marks each such crum as dirty, causing them to be written back to disk in the corrupted state.

---

### Summary

| Situation | `makecutsnd` | `rearrangecutsectionnd` result | Effect |
|---|---|---|---|
| All cuts past right end | No splits | 0 for all crums | Silent no-op |
| All cuts before left start | No splits | `nblades` for all crums → `diff[nblades] = 0` (3-cut) or case 4 (4-cut) | Silent no-op |
| Partial overlap (some in, some out) | Splits only at in-span cuts | In-span section crums classified normally; get `diff[i]` applied using out-of-span blade arithmetic | **Blindly applies offset; corrupts crum displacements; no error** |

`rearrangend` contains **no bounds detection of any kind**. The function trusts entirely that the caller has validated cut points against the document's V-span. When that assumption is violated:

- **Pure out-of-bounds inputs** happen to produce a no-op, not through any defensive logic, but as an accidental consequence of `whereoncrum` returning `TOMYRIGHT`/`TOMYLEFT` on every crum, which maps to case 0 or cases that apply a zero displacement.
- **Mixed in/out-of-bounds inputs** bypass the accidental safety entirely — the in-span portion of the operation proceeds while the out-of-span blade values are fed raw into tumbler arithmetic, producing structurally invalid crum displacements without any indication of failure.

---

## Question 17 [gregory]

> After a 3-cut pivot fragments a previously contiguous I-span across two non-adjacent V-regions, does `incontextlistnd` correctly return both V-positions when resolving that I-span back to V-space for link endset retrieval?

### Gregory's Answer

## KB Synthesis

## Short answer: Yes for V-position retrieval, but with duplication artifacts in link endsets.

---

### 1. POOM multimap accumulation is correct

After a 3-cut pivot, the POOM is a multimap in which the queried I-span maps to two non-adjacent V-regions. The traversal mechanism is designed for exactly this case.

From [SS-POOM-MULTIMAP] (Finding 0039), `ispan2vspanset` calls `permute()` → `findcbcinarea2d()`, which "traverses all siblings at each B-tree level and recursively descends into all qualifying subtrees, accumulating every matching leaf node." `incontextlistnd()` "inserts each found context into a sorted linked list, never replacing existing entries."

From [INV-RETRIEVAL-V-SORTED] (Finding 0078), `incontextlistnd()` performs explicit insertion-sort by V-address as contexts are discovered. The postcondition is:

```
∀ j < k : result[j].totaloffset.dsas[V] ≤ result[k].totaloffset.dsas[V]
```

This holds regardless of tree structure — [INV-RETRIEVAL-TREE-INDEPENDENCE] confirms the sorted-result postcondition is independent of B-tree sibling ordering, split history, or insertion order.

So both V-positions are returned, correctly sorted.

---

### 2. But the link endset layer has duplication artifacts

The duplication arises one level up, in how the endset itself was encoded at link-creation time.

From [SS-LINK-ENDPOINT] (Finding 0037), `vspanset2sporglset()` decomposes each V-span into one sporgl per **contiguous I-address region**. If the V-span covers content transcluded from two sources, it produces two sporgls. These two sporgls are independently indexed in the spanfilade — two separate `insertnd` calls via `insertendsetsinspanf` [ST-CREATE-LINK].

After a pivot rearranges content so that a previously contiguous I-span is split across two non-adjacent V-regions, the same fragmentation logic applies in reverse: `ispan2vspanset` returns two V-regions, yielding two sporgls, and the link is found twice in the spanfilade search — once per sporgl match.

[EC-PIVOT-LINK-FRAGMENTATION] (Finding 0019) documents this directly: after a pivot rearranges linked content, `retrieve_endsets` reports **four spans** for a link originally created on two characters ("CD"), and `find_links` returns the link **twice**. The note is: "This suggests that rearrangement can cause internal fragmentation in the enfilade structure that is visible through the endset API. The duplication may be a bug or may reflect the internal representation of fragmented spans."

---

### 3. Mechanism summary

| Layer | Behavior |
|-------|----------|
| POOM traversal (`findcbcinarea2d`) | Finds all matching crums across both V-regions — correct |
| `incontextlistnd` accumulation | Inserts both into a sorted list — correct |
| I-to-V conversion (`span2spanset`) | Returns both V-spans — correct |
| Spanfilade lookup | Independently matches both sporgls — produces duplication |
| `find_links` result | Link returned twice — artifact |

The retrieval machinery in [SS-CONTEXT-LIST] / [INV-RETRIEVAL-V-SORTED] works correctly. The duplication is not a failure of `incontextlistnd` but a consequence of the spanfilade indexing each sporgl independently: after pivot, the single link's endset is represented as two independent I-span records in the spanfilade, and each matches the query separately.

---

## Code Exploration

I now have everything needed to answer this definitively. Here is the full analysis, with every claim tied to source.

---

## Full Answer

### The 3-Cut Pivot and What It Does to the POOM

`rearrangend` in `edit.c:78` performs the pivot on the document's POOM (permutation matrix enfilade) in V-space. For 3 blades `[c0, c1, c2]`, `makeoffsetsfor3or4cuts` at `edit.c:177-183` computes:

```c
diff[1] = c2 - c1   // section 1 (between c0 and c1) shifts right
diff[2] = -(c1 - c0) // section 2 (between c1 and c2) shifts left
diff[3] = 0          // section 3 (after c2) doesn't move
```

After `makecutsnd` splits crums at V-positions c0, c1, c2, then `rearrangend:125` adds each `diff[i]` to `ptr->cdsp.dsas[V]` for each section:

```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);  // edit.c:125
ivemodified((typecorecrum*)ptr);
```

The I-coordinates (`dsas[I]`) are never touched. This is the critical point: **a 3-cut pivot changes V-displacement while preserving I-addresses**. A contiguous I-span [i_start, i_end) that occupied a contiguous V-range [v_start, v_end) before the pivot now appears in the POOM as two or more leaf crums with the same I-addresses but with V-displacements shuffled into non-adjacent positions.

---

### Resolving an I-Span to V-Space: The Call Chain

When link endset retrieval must resolve a stored I-span back to V-positions, the chain is:

```
dofollowlink [do1.c:223]
  → link2sporglset [sporgl.c:67]
      → retrieverestricted on the link POOM [retrie.c:56]
  → linksporglset2specset [sporgl.c:97]
      → sporglset2vspanset [sporgl.c:141]
          → ispan2vspanset [orglinks.c:389]
              → permute(..., I, ..., V) [orglinks.c:404]
                  → span2spanset [orglinks.c:425]
                      → retrieverestricted [retrie.c:56]
                          → retrieveinarea [retrie.c:87]
                              → findcbcinarea2d [retrie.c:229]
                                  → incontextlistnd [context.c:75]
                      → context2span (for each context) [context.c:176]
```

---

### What `findcbcinarea2d` Sees After the Pivot

`retrieverestricted` at `retrie.c:56` is called from `span2spanset` as:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
// restrictionindex = I,  targindex = V
```

This calls `retrieveinarea` → `findcbcinarea2d` [retrie.c:229]. The function walks all right-siblings in the POOM recursively, calling `crumqualifies2d` [retrie.c:270] to filter. `crumqualifies2d` checks:

```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT :
         whereoncrum(crumptr, offset, span1end, index1);   // I-end check
if (endcmp <= ONMYLEFTBORDER) return FALSE;                // retrie.c:283

startcmp = whereoncrum(crumptr, offset, span1start, index1); // I-start check
if (startcmp > THRUME) return FALSE;                          // retrie.c:287

// V range: span2start = span2end = 0 (NULL restriction)
endcmp = iszerotumbler(span2end) ? TOMYRIGHT : ...;           // retrie.c:292
// always TOMYRIGHT since span2ptr was NULL → always passes
startcmp = whereoncrum(crumptr, offset, span2start, index2); // retrie.c:297
// span2start=0, so any crum with V >= 0 qualifies
```

**After the 3-cut pivot**, a previously-contiguous I-span [i_start, i_end) that was split by the cuts at [c0, c1, c2] now exists as at least two separate POOM leaf crums — e.g.:

- Leaf crum A: I=[i_start, i_mid), V=[v2, v2+k)   ← section 2 after pivot
- Leaf crum B: I=[i_mid, i_end), V=[v1, v1+m)     ← section 1 after pivot

Both satisfy the I-span restriction since both have I-extents overlapping [i_start, i_end). Both pass `crumqualifies2d` with no V restriction. `findcbcinarea2d` calls `incontextlistnd` for each:

```c
context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr); // retrie.c:262
incontextlistnd(headptr, context, index1);                            // retrie.c:263
```

---

### Inside `incontextlistnd` [context.c:75]

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
  prologuecontextnd(c, &grasp, (typedsp*)NULL);  // sets grasp = c's totaloffset
  // grasp.dsas[index] = c's I-start (since index = I)

  if (!clist) { *clistptr = c; return(0); }      // first insertion

  if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) {
    c->nextcontext = clist; *clistptr = c; return(0); // insert at beginning
  } else {
    for (; nextc = clist->nextcontext; clist = nextc) {
      if ((whereoncontext(clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
       && (whereoncontext(nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
        c->nextcontext = nextc; clist->nextcontext = c; return(0); // middle
      }
    }
  }
  clist->nextcontext = c; // append at end
}
```

`prologuecontextnd` [context.c:216] extracts `grasp.dsas[I]` = the I-start of the new context. The list is **sorted by I-position**.

For Crum A (I-start = i_start) inserted first into an empty list: trivially inserted.

For Crum B (I-start = i_mid > i_start) inserted second:
- `whereoncontext(A, i_mid, I)`: A covers [i_start, i_mid). `intervalcmp(i_start, i_mid, i_mid)` → address equals right → `ONMYRIGHTBORDER`.
- `ONMYRIGHTBORDER < THRUME`? The return values in order are: TOMYLEFT < ONMYLEFTBORDER < THRUME < ONMYRIGHTBORDER < TOMYRIGHT. So **NO** — the "beginning" condition fails.
- The `for` loop has no iterations (A has no nextcontext).
- Crum B is appended at end.

**Result: the context list correctly contains both [A, B] in I-order.**

---

### `context2span` Maps Each Fragment to Its V-Position [context.c:176]

For each context in the list, `span2spanset` [orglinks.c:439] calls:

```c
context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
// idx1 = I,  idx2 = V
```

`context2span` [context.c:191-211] does:

```c
prologuecontextnd(context, &grasp, &reach);
// grasp.dsas[I] = crum's I-start,  grasp.dsas[V] = crum's V-start
// reach.dsas[I] = crum's I-end,    reach.dsas[V] = crum's V-end

if (tumblercmp(&grasp.dsas[I], &lowerbound) == LESS)
    // trim V-start if I-start is before restriction's I-start
    tumblerincrement(&grasp.dsas[V], 0,
        (INT)tumblerintdiff(&lowerbound, &grasp.dsas[I]), &grasp.dsas[V]);

if (tumblercmp(&reach.dsas[I], &upperbound) == GREATER)
    // trim V-end if I-end is past restriction's I-end
    tumblerincrement(&reach.dsas[V], 0,
        -tumblerintdiff(&reach.dsas[I], &upperbound), &reach.dsas[V]);

movetumbler(&grasp.dsas[V], &foundspanptr->stream);
tumblersub(&reach.dsas[V], &grasp.dsas[V], &foundspanptr->width);
```

For Crum A (I=[i_start, i_mid), V=[v2, v2+k)), restriction [i_start, i_end):
- I-start == lowerbound → first `if` skips → V-start stays at v2
- I-end < upperbound → second `if` skips → V-end stays at v2+k
- **foundspan = V=[v2, v2+k)**

For Crum B (I=[i_mid, i_end), V=[v1, v1+m)), restriction [i_start, i_end):
- I-start > lowerbound → first `if` skips → V-start stays at v1
- I-end == upperbound → second `if` skips → V-end stays at v1+m
- **foundspan = V=[v1, v1+m)**

Both are added to `targspansetptr` via `onitemlist` [orglinks.c:464], which appends them in order.

---

### Answer to the Question

**Yes — `incontextlistnd` correctly identifies and returns both V-positions.** Here is why:

1. **The POOM after a 3-cut pivot contains distinct leaf crums** for each fragment. The fragments have non-overlapping I-extents (split at cut-points) and non-adjacent V-displacements. Nothing in `rearrangend` [edit.c:78] merges crums that were separated by cuts — `recombine` [edit.c:139] and `splitcrumupwards` [edit.c:141] operate on structural housekeeping, not on re-fusing semantically distinct spans.

2. **`findcbcinarea2d` [retrie.c:229] finds all qualifying leaf crums** regardless of their V-positions, because `crumqualifies2d` [retrie.c:270] uses `iszerotumbler(span2end) ? TOMYRIGHT` when there is no V restriction — passing `TOMYRIGHT` to the `endcmp <= ONMYLEFTBORDER` guard, which always lets through.

3. **`incontextlistnd` [context.c:75] correctly inserts both fragments** because they have different I-starts (split at the cut). The sorted insertion logic places Crum A (lower I-start) before Crum B (higher I-start), and the append-at-end fall-through at `context.c:109-110` correctly handles the adjacent-I-boundary case where `whereoncontext` returns `ONMYRIGHTBORDER` rather than the `< THRUME` threshold.

4. **`context2span` [context.c:176] correctly maps each fragment's I-range to its corresponding V-range** independently, clipping only to the restriction I-span, which doesn't affect either fragment in the common case where the restriction spans the full original I-range.

---

### One Real Defect in `incontextlistnd`

The "in middle" insertion condition at `context.c:99` requires:

```c
&& (whereoncontext(nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)
```

`< ONMYLEFTBORDER` means strictly `TOMYLEFT`. If two contexts have identical I-starts — which cannot happen from a 3-cut pivot (cuts produce distinct fragments), but could theoretically arise from independent insertions — this condition would fail to detect the correct insertion point, and the second context would be appended at the end rather than interleaved. **This bug does not affect the 3-cut pivot scenario** because the cut positions always produce fragments with strictly distinct I-starts.

---

### Conclusion

For the specific case described — a 3-cut pivot that fragments a contiguous I-span into two crums across non-adjacent V-regions — the system works correctly end-to-end. `findcbcinarea2d` discovers both crums, `incontextlistnd` inserts both into the context list in I-order (the sorting being harmless since `context2span` processes each independently), and `context2span` emits the correct non-adjacent V-spans. Both V-positions are returned.

---

## Question 18 [gregory]

> Can `makeoffsetsfor3or4cuts` produce a negative tumbler offset that, when added to a POOM entry's V-displacement, yields a negative V-position — analogous to the `tumblersub` issue in DELETE?

### Gregory's Answer

## KB Synthesis

No. `makeoffsetsfor3or4cuts` can produce negative tumbler offsets, but adding them to valid POOM V-displacements cannot yield a negative V-position — for structural reasons that differ from the DELETE case.

## Why offsets are negative

From [ST-REARRANGE] (Finding 0056), the backward-moving regions receive negative offsets:

- **Pivot**: region 2 (`[cut1, cut2)`) gets `diff[2] = -(cut1 - cut0)`
- **Swap**: region 3 (`[cut2, cut3)`) gets `diff[3] = -(cut2 - cut0)`, and region 2 gets `diff[2] = (cut3-cut2) - (cut1-cut0)` which is negative when the left region is larger

These are applied via `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], ...)`, which handles sign-magnitude arithmetic directly — no `strongsub` exponent guard is involved.

## Why negative V-positions cannot result

The key constraint: the displaced entry is always within its region, and the offset magnitude is bounded by the adjacent region's size.

For the pivot case, an entry at V-position `v` in region 2 satisfies `v >= cut1`. Its new position is:

```
v + diff[2] = v - (cut1 - cut0) >= cut1 - (cut1 - cut0) = cut0 > 0
```

For the swap's region 3, entries satisfy `v >= cut2`, and the offset is `-(cut2 - cut0)`:

```
v - (cut2 - cut0) >= cut2 - (cut2 - cut0) = cut0 > 0
```

For swap's region 2 with negative diff, entries satisfy `v >= cut1`, and the worst case is `v = cut1`:

```
cut1 + diff[2] = cut1 + (cut3-cut2) - (cut1-cut0) = cut0 + (cut3-cut2) > 0
```

In all cases, the minimum displaced position equals `cut0`, which is a valid positive V-address. Negative results require `cut0 < 0`, which cannot occur with valid docuverse addresses.

## Contrast with DELETE

DELETE uses `strongsub`, which has an exponent guard: when the deletion width's exponent is less than the entry's displacement exponent, `strongsub` returns the minuend unchanged [SS-TUMBLER] (Finding 0055). This guard protects cross-subspace entries by accident.

REARRANGE uses `tumbleradd` directly — no exponent guard. But rearrange doesn't need one for this purpose: the mathematical structure of the offsets (derived as *differences between cut positions*) ensures the result stays positive. DELETE's problem arose because a fixed-width deletion could underflow an arbitrarily small displacement; rearrange's displacements are always relative to adjacent cuts, so the math is self-bounding.

## Remaining concern: cross-subspace displacement

REARRANGE can still violate the subspace convention ([EC-REARRANGE-CROSS-SUBSPACE], [PRE-REARRANGE] Finding 0051) — moving text into 2.x or links into 1.x — but the displaced V-positions are positive throughout. The `tumbleradd` call in `edit.c:125` has no subspace guard and performs the arithmetic unconditionally, producing valid-but-semantically-wrong positive addresses.

---

## Code Exploration

I now have all the evidence needed. Let me synthesize the complete analysis.

---

## Analysis: Can `makeoffsetsfor3or4cuts` Produce Negative V-Positions?

### Short Answer

**`makeoffsetsfor3or4cuts` intentionally produces negative tumbler offsets, but the mathematical structure of the enfilade bounds prevent them from driving a POOM entry's V-displacement below zero — unlike the DELETE case (Finding 0053).** The structural guarantee holds for valid POOM state; it does not hold if the tree has already been contaminated by the DELETE bug.

---

### 1. What Offsets `makeoffsetsfor3or4cuts` Produces

Full function at `edit.c:164–184`:

```c
int makeoffsetsfor3or4cuts(typeknives *knives, tumbler diff[])
{
  tumbler a, b;
    /* diff[0] is simply ignored */
    if (knives->nblades == 4) {
        tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));       // diff[1] = b2-b0 (+)
        tumblersub (&knives->blades[1], &knives->blades[0], &a);               // a = b1-b0 (+)
        tumblersub (&knives->blades[3], &knives->blades[2], &b);               // b = b3-b2 (+)
        tumblersub (&b, &a, &(diff[2]));                                        // diff[2] = b-a = (b3-b2)-(b1-b0)
/*      tumblersub (&knives->blades[0], &knives->blades[2], &(diff[3]));*//* should be <0 */
        movetumbler (&diff[1], &diff[3]);
        diff[3].sign = !diff[1].sign;                                          // diff[3] = -(b2-b0)
    } else if (knives->nblades == 3) {
        tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);         // diff[1] = b2-b1 (+)
        tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]);         /* should be negative */
        diff[2].sign = !diff[2].sign;                                          // diff[2] = -(b1-b0)
        tumblerclear (&(diff[3]));                                             // diff[3] = 0
    } else
        gerror ("Wrong number of cuts.");
}
```

**Negative offsets produced:**

| Case | Offset | Sign | Condition |
|------|--------|------|-----------|
| 3-cut | `diff[2] = -(b1-b0)` | **always negative** | explicit sign flip at `edit.c:180` |
| 4-cut | `diff[3] = -(b2-b0)` | **always negative** | sign flip at `edit.c:176` |
| 4-cut | `diff[2] = (b3-b2)-(b1-b0)` | **negative when region 1 wider than region 3** | depends on cut spacing |

The commented-out line at `edit.c:174` — `/* should be <0 */` — is original author confirmation that signed arithmetic was deliberately used here.

---

### 2. How These Diffs Are Applied

In `rearrangend`, `edit.c:113–135`:

```c
for (ptr = (typecuc*)findleftson(father); ptr; ...) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case 0:  case 4: /* these never move */
          break;
      case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
          tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
          ivemodified((typecorecrum*)ptr);
          break;
    }
}
```

`index` = `V` (`wisp.h:21`) when called via `rearrangepm` at `orglinks.c:139`. The diff is added directly to `ptr->cdsp.dsas[V]` — the V-displacement of the POOM crum — with **no guard against a negative result**.

---

### 3. Section Classification Constrains the Result

`whereoncrum` for a POOM crum (`retrie.c:356`):

```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);  // left = offset.V + cdsp.V
```

So a crum's absolute V-start is `fgrasp.V + cdsp.V`.

`rearrangecutsectionnd` returns section `i+1` when `blade[i] <= fgrasp.V + cdsp.V` (`edit.c:196–203`). This means a node assigned to **section k** (k = 1, 2, or 3) satisfies:

```
cdsp.V >= b_{k-1} - fgrasp.V
```

Now compute the post-diff minimum:

**3-cut, section 2** (gets `diff[2] = -(b1-b0)`):
```
new_cdsp.V = cdsp.V + diff[2]
           >= (b1 - fgrasp.V) - (b1 - b0)
           = b0 - fgrasp.V
```

**4-cut, section 3** (gets `diff[3] = -(b2-b0)`):
```
new_cdsp.V >= (b2 - fgrasp.V) - (b2 - b0)
           = b0 - fgrasp.V
```

**4-cut, section 2** (gets `diff[2] = (b3-b2)-(b1-b0)`, possibly negative):
```
new_cdsp.V >= (b1 - fgrasp.V) + (b3-b2) - (b1-b0)
           = b3 - b2 + b0 - fgrasp.V
```

In all three cases, the minimum result is `>= b0 - fgrasp.V`.

**The bound holds if and only if `fgrasp.V <= b0`** — i.e., the father's absolute V-start is at or before the smallest cut. This is guaranteed by the enfilade invariant: the "father" returned by `newfindintersectionnd` at `edit.c:111` is the lowest common ancestor of all cut points. Its V-span must contain all blades, so `fgrasp.V <= b0 <= b1 <= b2 (< b3)`. Therefore `b0 - fgrasp.V >= 0`.

**Conclusion**: For a valid POOM, `makeoffsetsfor3or4cuts` cannot drive `cdsp.V` below zero.

---

### 4. The Critical Structural Difference from DELETE

In **DELETE** (`edit.c:63`):
```c
tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```
The `width` subtracted is the deletion span width — a value completely unconstrained relative to `cdsp.V`. A node far to the right of a large deletion will have its cdsp reduced by more than its current value, yielding a negative tumbler (Finding 0053).

In **REARRANGE** (`edit.c:125`):
```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```
The diff for section k is derived from the same cut positions that determine section assignment. The classification lower-bounds `cdsp.V` by exactly enough to absorb the maximum negative diff, leaving the result `>= b0 - fgrasp.V >= 0`.

This is a **self-compensating invariant**: the more negative the diff (wider region 1 compared to region 3), the larger `cdsp.V` must be for the node to be in that section.

---

### 5. Residual Risk: Pre-Contaminated State

The guarantee above depends on **valid POOM state**. If DELETE has already introduced negative V-positions (Finding 0053), those entries sit at `cdsp.V < 0`. Their absolute V-start `fgrasp.V + cdsp.V` is less than `fgrasp.V`, and since all cuts `b0, b1, ... >= fgrasp.V`, `whereoncrum(ptr, fgrasp, b0) == TOMYRIGHT` — the blade is to the right of the crum. The crum falls in **section 0** (never moves). So REARRANGE does **not further damage** already-negative entries, but it also does not repair them.

There is one other subtle risk: if `newfindintersectionnd` returns an incorrect `father` (one whose span doesn't contain all blades), the bound `fgrasp.V <= b0` can be violated. In that case, even REARRANGE could produce a negative displacement. But this would be a separate `ndcuts.c`/`ndinters.c` bug, not a property of `makeoffsetsfor3or4cuts` itself.

---

### Code Citations

| Claim | File:Line |
|-------|-----------|
| `diff[2]` sign-flip (3-cut) | `edit.c:180` |
| `diff[3]` sign-flip (4-cut) | `edit.c:176` |
| Commented `/* should be <0 */` | `edit.c:174` |
| diff applied to `cdsp.dsas[V]` via `tumbleradd` | `edit.c:125` |
| `whereoncrum` computes `left = offset.V + cdsp.V` | `retrie.c:356` |
| `V = 1` constant for POOM | `wisp.h:21` |
| `rearrangepm` calls `rearrangend(…, V)` | `orglinks.c:139` |
| DELETE uses unconstrained `tumblersub` | `edit.c:63` |
| `tumblersub` allows negative results | `tumble.c:424,427` |
| `diff[2] = -(b1-b0)` (3-cut comment "should be negative") | `edit.c:179` |

---

### Summary

Yes, `makeoffsetsfor3or4cuts` **does** produce negative tumbler offsets — this is explicit and intentional (`diff[2]` for 3-cut, `diff[3]` for 4-cut, and conditionally `diff[2]` for 4-cut). These are applied without any post-application guard to `cdsp.dsas[V]`.

However, the mechanism is **not analogous to the DELETE bug** in its outcome. In DELETE, the subtracted `width` is independent of `cdsp.V`, so underflow to negative is possible whenever the deletion span is larger than the node's displacement. In REARRANGE, the negative diff and the minimum `cdsp.V` for section membership are derived from the same cut positions: section assignment guarantees `cdsp.V >= b_{k-1} - fgrasp.V`, and the negative diff for that section is exactly `fgrasp.V - b_{k-1}` in the worst case, making the result `>= 0` whenever the enfilade is in valid state (`fgrasp.V <= b0`).

The only path to a negative V-position via REARRANGE is an already-corrupted POOM (from the DELETE bug) or a malformed `father` from `newfindintersectionnd` — not from `makeoffsetsfor3or4cuts` itself operating on valid state.

---

## Question 19 [gregory]

> In a 4-cut swap where the middle region `[b,c)` contains no POOM entries (a gap), does `rearrangend` still compute and apply offsets to the empty region, or does it skip the middle and only exchange the `[a,b)` and `[c,d)` regions?

### Gregory's Answer

## KB Synthesis

From [ST-REARRANGE] Finding 0056 and [EC-REARRANGE-EMPTY-REGION], the answer is clear:

**`rearrangend` always computes offsets for all regions from the cut geometry, but applies offsets only to the POOM entries that exist.**

The algorithm has two independent phases:

1. **Offset computation** (`makeoffsetsfor3or4cuts()`) — purely geometric, references only `knives->blades[]`. For a 4-cut swap at `cut0 < cut1 < cut2 < cut3`:
   - Region 1 `[cut0, cut1)`: `diff[1] = cut2 - cut0`
   - Region 2 `[cut1, cut2)`: `diff[2] = (cut3 - cut2) - (cut1 - cut0)`
   - Region 3 `[cut2, cut3)`: `diff[3] = -(cut2 - cut0)`

   This runs regardless of whether the middle is empty. The code at `edit.c:164-183` has no awareness of POOM state.

2. **Displacement application** — iterates over POOM entries, classifies each into a region via `rearrangecutsectionnd()`, then calls `tumbleradd` on the V-displacement. If no POOM entries fall in `[cut1, cut2)`, the middle offset is computed but never applied to anything.

[EC-REARRANGE-EMPTY-REGION] states this explicitly: "The algorithm operates per-span, and empty regions simply have no spans to process. This is correct behavior — the offset arithmetic is unaffected."

So for a swap where the middle is a gap: the two outer regions `[a,b)` and `[c,d)` are exchanged normally, and the empty middle contributes its size difference to the offset arithmetic but produces no displacement operations. The result is equivalent to a direct exchange of the two outer regions.

---

## Code Exploration

Now I have everything needed. Here is the complete analysis:

---

## Answer

### Short answer

`rearrangend` **always computes `diff[2]`** (the offset for the middle region), but **only applies it when nodes actually exist in `[b,c)`**. If the middle region is empty, `diff[2]` is silently a no-op. The `[a,b)` and `[c,d)` regions are swapped regardless.

---

### The computation: `makeoffsetsfor3or4cuts`

`rearrangend` calls `makeoffsetsfor3or4cuts` unconditionally before touching any nodes [`edit.c:108`]:

```c
makeoffsetsfor3or4cuts (&knives, diff);
```

For `nblades == 4` [`edit.c:169-176`]:

```c
tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));   // diff[1] = c - a
tumblersub (&knives->blades[1], &knives->blades[0], &a);            // a = b - a
tumblersub (&knives->blades[3], &knives->blades[2], &b);            // b = d - c
tumblersub (&b, &a, &(diff[2]));                                     // diff[2] = (d-c) - (b-a)
movetumbler (&diff[1], &diff[3]);
diff[3].sign = !diff[1].sign;                                        // diff[3] = -(c-a)
```

`diff[2]` is always computed. There is no guard checking whether any node occupies `[b,c)`.

---

### The classification: `rearrangecutsectionnd`

After cutting and finding the intersection father node, `rearrangend` iterates over all children and classifies each into a section number [`edit.c:113-114`]:

```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = (typecuc *)findrightbro((typecorecrum*)ptr)) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
```

`rearrangecutsectionnd` scans knives from highest to lowest and returns the first `i+1` where `knife[i] <= node.start` [`edit.c:195-203`]:

```c
for (i = knives->nblades -1; i >= 0 ; --i) {
    cmp = whereoncrum (ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME)       return (-1);
    else if (cmp <= ONMYLEFTBORDER) return (i+1);
}
return (0);
```

`whereoncrum` for a POOM node with DSP `d` and WID `w` [`retrie.c:356-372`]:
- Returns `ONMYLEFTBORDER` (-1) when `address == node.start`
- Returns `THRUME` (0) when `node.start < address < node.end`
- Returns `TOMYRIGHT` (> 1) when `address > node.end`

So `cmp <= ONMYLEFTBORDER` is true when `address <= node.start` — the knife is at or before the node's left border.

For 4 knives `a < b < c < d`, the section assignments are:

| Node range | Section returned |
|---|---|
| `(-∞, a)` | 0 — never moves |
| `[a, b)` | 1 — shifted by `diff[1]` = `c−a` (moves right) |
| `[b, c)` | 2 — shifted by `diff[2]` = `(d−c)−(b−a)` |
| `[c, d)` | 3 — shifted by `diff[3]` = `a−c` (moves left) |
| `[d, ∞)` | 4 — never moves |

---

### The application: the switch in `rearrangend`

```c
switch (i) {
  case 0:  case 4: /* these never move */
      break;
  case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
      tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
      ivemodified((typecorecrum*)ptr);
      break;
```
[`edit.c:122-128`]

**The loop iterates only over existing children.** If the middle region `[b,c)` is empty, no child node will ever be classified as section 2, and thus `diff[2]` is never passed to `tumbleradd`. There is no explicit skip — the emptiness is simply handled by the fact that the iteration produces no case-2 nodes.

---

### Conclusion

1. **`diff[2]` is always computed** by `makeoffsetsfor3or4cuts`, regardless of whether `[b,c)` is populated [`edit.c:108`, `edit.c:173`].

2. **`diff[2]` is never applied when `[b,c)` is empty.** The application loop is node-driven, not region-driven. Zero nodes in section 2 → zero applications of `diff[2]`.

3. **The swap still executes correctly.** Nodes in `[a,b)` receive `diff[1] = c−a` (shift right) and nodes in `[c,d)` receive `diff[3] = a−c` (shift left). An empty middle region is transparently a no-op; `rearrangend` does not need to special-case it.

---

## Question 20 [gregory]

> After REARRANGE moves entries within the POOM's 2D enfilade, does `recombinend` fire to rebalance the tree, and if so, does the diagonal-sum reordering ever change the logical V-address ordering of the result — or is confluence guaranteed regardless of post-rearrange tree shape?

### Gregory's Answer

## KB Synthesis

Two separate questions here — whether `recombinend` fires, and whether confluence is preserved. The KB answers them independently.

## Does `recombinend` fire after REARRANGE?

Almost certainly not. The rebalancing triggers are purely occupancy-based: `toomanysons` fires when a node exceeds its branching limit, `toofewsons` fires when a node falls below it [INV-ENFILADE-OCCUPANCY, SS-ENFILADE-TREE/Finding 0070]. REARRANGE adds no crums and removes no crums — it only mutates existing crums' `cdsp.dsas[V]` fields in-place via `tumbleradd` [ST-REARRANGE/Finding 0056]. Occupancy counts are unchanged, so neither split nor merge is triggered.

What does happen is `setwispupwards` after displacement mutations, which recalculates each ancestor node's `cdsp` (minimum displacement) and `cwid` (extent width) to reflect the new V-position distribution [INV-ENFILADE-RELATIVE-ADDRESSING/Finding 0066]. This is structural bookkeeping, not rebalancing. Compare with INSERT, which explicitly calls `splitcrumupwards` after adding a crum [ST-INSERT/Finding 0060], or DELETE, which explicitly calls `recombinend` after removing crums [ST-DELETE/Finding 0058]. The REARRANGE code path has neither.

## Does the diagonal-sum reordering ever change logical V-address ordering?

No. Confluence is guaranteed regardless of tree shape.

The diagonal sort in `recombinend` — ordering children by `cdsp.dsas[0] + cdsp.dsas[1]` (L1-norm) — determines which pairs of siblings are *considered* for merging, and determines the resulting tree shape after rebalancing [ST-REBALANCE-2D/Finding 0071]. Different insertion histories or rearrangement sequences can produce different tree shapes with different sibling orderings.

But retrieval is insulated from this at the collection layer. `incontextlistnd()` performs explicit insertion-sort by V-address on every context discovered during B-tree traversal [INV-RETRIEVAL-V-SORTED/Finding 0078]. The discovery order — which follows tree sibling structure, itself a product of diagonal ordering — is irrelevant to the final result:

> "The V-ordering of retrieval results is independent of the internal B-tree structure... even if split/rebalance operations or out-of-order insertions produce a tree where sibling order does not match V-address order, the `incontextlistnd` insertion-sort re-establishes V-ordering during retrieval." [INV-RETRIEVAL-TREE-INDEPENDENCE/Finding 0078]

This is consistent with [INV-ENFILADE-CONFLUENCE/Finding 0041]:

> "Confluence holds at the abstraction boundary (query results) but NOT at the physical level (tree shape, sibling ordering, split points differ based on insertion order)."

## Summary

`recombinend` does not fire after REARRANGE because occupancy is unchanged. Even in cases where rebalancing does fire (e.g., after DELETE), the diagonal reordering is a physical tree property, not an observable one — `incontextlistnd`'s insertion-sort guarantees V-address ordering in all retrieval results regardless of how the 2D enfilade is shaped internally.

---

## Code Exploration

I have all the code I need. Let me now compose the full answer.

---

## Answer: `recombinend` After REARRANGE — Confluence and Diagonal-Sum Ordering

### 1. Does `recombinend` fire?

**Yes, unconditionally for POOM.** The call chain is:

`rearrangend` [edit.c:139]:
```c
recombine (fullcrumptr);
```

`recombine` [recombine.c:22–34]:
```c
int recombine(typecuc *father)
{
    switch (father->cenftype) {
      case POOM:
            recombinend (father);
    }
}
```

Note that `rearrangend` passes `fullcrumptr` — the full-crum root — not just `father` (the intersection node found at line 111). So `recombinend` is called on the entire POOM tree, not only on the subtree that was mutated. This is a wider sweep than, for example, `deletend`, which only calls `recombine(father)` on the local intersection node [edit.c:75].

**The `modified` guard is also satisfied.** During the offset-adjustment loop [edit.c:125–127], every moved crum calls `ivemodified(ptr)`. `ivemodified` [genf.c:539] chains upward setting `modified = TRUE` on each leftmost-ancestor. The preceding `setwispupwards(father, 1)` call [edit.c:137] propagates wid sums. Thus by the time `recombine` fires, the `modified` flag is set through the path from moved crums up to the root, satisfying the guard in `recombinend` [recombine.c:112]:

```c
if (father->height < 2  || !father->modified)
    return(0);
```

---

### 2. What `recombinend` actually does

`recombinend` [recombine.c:104–131] is a post-order bottom-up tree rebalancing pass:

```c
int recombinend(typecuc *father)
{
    // depth-first: process children first
    for (ptr = getleftson(father); ptr; ptr=(typecorecrum *)getrightbro(ptr)){
        recombinend(ptr);
    }

    getorderedsons (father, sons);  // sort sons by diagonal sum
    n = father->numberofsons;
    for (i = 0; i < n-1; i++) {
        for (j = i+1; sons[i] && j < n; j++) {
            if(i != j && sons[j] && ishouldbother(sons[i],sons[j])){
                takeovernephewsnd (&sons[i], &sons[j]);
            }
        }
    }
    if (father->isapex)
        levelpull(father);
}
```

The goal is to **collapse under-full sibling upper-crums** (UCs) by moving grandchildren from one sibling into another. The pair selection is driven by `ishouldbother` [recombine.c:150–163], which checks that `dest->numberofsons + src->numberofsons <= MAX2DBCINLOAF` (or `MAXUCINLOAF` for height > 1).

---

### 3. The Diagonal-Sum Sort

`getorderedsons` [recombine.c:270–280] collects sons into an array and calls `shellsort`:

```c
int shellsort(typecorecrum *v[], INT n)
{
    for(i=0;i<n;i++){
        tumbleradd(&v[i]->cdsp.dsas[0],&v[i]->cdsp.dsas[1],&tarray[i]);
        tarrayp[i] = &tarray[i];
    }
    // shell-sort by tarray[i] ascending
}
```

The key [recombine.c:298]: `tarray[i] = cdsp.dsas[0] + cdsp.dsas[1]`. For POOM, `dsas[0]` = I-space displacement, `dsas[1]` = V-space displacement. The sort key is the tumbler sum of both dimensions — the "diagonal" in I×V space. Sons with smaller diagonal sums are listed first and become **merge destinations** (outer-`i` position), while sons with larger diagonal sums are **merge sources** (inner-`j` position).

This ordering is purely a **merge-priority heuristic**. It does not reorder the content in logical V-space, nor does it control which bottom crums end up in which UC — only in what sequence merges are attempted.

---

### 4. Does the diagonal-sum reordering change logical V-address ordering?

**No. Confluence is guaranteed.**

The logical V-address of any bottom crum is the sum of all `cdsp.dsas[V]` values along the path from root to that crum. Every merge operation (`eatbrossubtreend` and `takenephewnd`) performs an exact coordinate-frame transform that preserves this absolute address.

**`eatbrossubtreend`** [recombine.c:205–233]:
```c
makeroomonleftnd (me, &offset, &bro->cdsp, &grasp);
fixdspsofbroschildren (me, bro);
// splice bro's children onto the right end of me's child list
getleftson(bro)->leftbroorfather = getrightmostbro(getleftson(me));
getrightmostbro(getleftson(me))->rightbro = getleftson(bro);
```

`fixdspsofbroschildren` [recombine.c:259–268]:
```c
for (nephew = getleftson(bro); nephew; nephew = getrightbro(nephew)){
    dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, me->cenftype);
    dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);
    ivemodified(nephew);
}
```

This transforms each nephew's cdsp from bro-relative → absolute → me-relative. The absolute V-address is:

```
before: bro->cdsp[V] + nephew_old_cdsp[V]
after:  me->cdsp[V]  + nephew_new_cdsp[V]
      = me->cdsp[V]  + (bro->cdsp[V] + nephew_old_cdsp[V] - me->cdsp[V])
      = bro->cdsp[V] + nephew_old_cdsp[V]   ← identical
```

**`takenephewnd`** [recombine.c:235–257] performs the same transform for the partial-merge case:
```c
dspadd(&bro->cdsp, &nephew->cdsp, &nephew->cdsp, bro->cenftype);  // → absolute
// ... adopt nephew under me ...
dspsub(&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);    // → me-relative
```

Again, absolute address is invariant.

**Retrieval is address-based, not sibling-position-based.** `prologuend` [retrie.c:334–339] computes absolute addresses:
```c
dspadd(offset, &ptr->cdsp, grasp, ...);
dspadd(grasp, &ptr->cwid, reach, ...);
```

And `whereoncrum` [retrie.c:345–398] classifies a query address against `[grasp, grasp+cwid)`. No code in the retrieval path uses sibling position to determine whether a crum's content is relevant — only `cdsp` and `cwid` values matter. Similarly, `findsontoinsertundernd` [insertnd.c:277–298] iterates all siblings and selects by DSP comparison, not by position in the sibling list.

---

### 5. The POOM Split/Merge Metric Mismatch

One architectural oddity: `recombinend` uses **diagonal sum** (V+I) as its merge priority [recombine.c:298], but `splitcrumpm` [split.c:117–128] uses a **maximum SPANRANGE** criterion:

```c
int splitcrumpm(typecuc *father)
{
    for(correctone=ptr=findleftson(father);ptr;ptr=findrightbro(ptr)) {
        if (tumblercmp(&ptr->cdsp.dsas[SPANRANGE], &correctone->cdsp.dsas[SPANRANGE]) == GREATER)
            correctone = ptr;
    }
    peelcrumoffnd(correctone);
}
```

And notably [edit.c:141] after `recombine`, `rearrangend` also calls:
```c
(void)splitcrumupwards(fullcrumptr);/* can we move this before recombine ?*/
```

The comment "can we move this before recombine?" shows the authors were uncertain about the ordering. These two passes (merge by diagonal-sum priority, then split by max-SPANRANGE) are different heuristics operating on the same tree. Neither affects confluence — they affect tree balance and I/O performance, not logical content.

---

### Summary

| Question | Answer | Key evidence |
|---|---|---|
| Does `recombinend` fire after REARRANGE? | **Yes**, on the full-crum root | `edit.c:139`, `recombine.c:31` |
| Guard conditions satisfied? | Yes — `ivemodified` [edit.c:127] sets `modified=TRUE` up the ancestor chain | `genf.c:539`, `recombine.c:112` |
| What does diagonal-sum sort control? | **Merge priority** only — which sibling pairs are attempted first | `recombine.c:296-310` |
| Does it change logical V-address ordering? | **No** — each merge performs an exact coordinate transform preserving absolute addresses | `recombine.c:259-268`, `recombine.c:243` |
| Is confluence guaranteed? | **Yes** — retrieval uses `cdsp`/`cwid` arithmetic, not sibling position | `retrie.c:334-398` |
| Any caveats? | POOM split uses SPANRANGE-max metric, merge uses diagonal-sum; ordering of split-vs-recombine is unresolved in the code itself | `split.c:123`, `edit.c:141` comment |
