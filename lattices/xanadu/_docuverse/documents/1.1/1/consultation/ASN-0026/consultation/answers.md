# Consultation Answers — I-Space and V-Space

**Inquiry:** What is the relationship between permanent content storage (I-space) and mutable document arrangement (V-space)? What invariants connect them?
**Date:** 2026-03-07 21:55
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> Once content is permanently stored, can any document operation — rearrangement, deletion from a document, or versioning — ever alter or destroy that stored content?

### Nelson's Answer

# No. Stored content is inviolable.

This is not a side-effect of the design — it is the central architectural principle. Every document operation works exclusively in V-space (the document's current arrangement). I-space (where content permanently lives) is append-only and immutable.

## The foundational separation

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

I-space is where content **permanently lives**. V-space is a **view** — a mapping that references I-space content and can be rearranged across versions. The document IS the mapping, not the content itself.

## What each operation actually does

**DELETE** removes content from V-space only:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Deletion makes bytes "not currently addressable" in that document's view. The I-space content is untouched.

**REARRANGE** is a pure V-space operation. It transposes regions of the virtual byte stream. The underlying I-space addresses don't change:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

**INSERT** adds new content to I-space (append-only) and updates the V-space arrangement:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The new bytes get fresh I-space addresses. No existing I-space content is touched.

**CREATENEWVERSION** creates a new V-space arrangement over the same I-space content:

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

**COPY** (transclusion) creates a V-space mapping to existing I-space — no duplication, no modification:

> "The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>." [LM 4/67]

## The storage model forbids it by design

Nelson explicitly rejects destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

And the non-destruction guarantee is stated directly:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

## Why this matters

The immutability of I-space is what makes every other guarantee possible:

- **Permanent addresses work** because the content at an I-address never changes
- **Links survive editing** because they point to I-space, not V-space positions
- **Historical backtrack works** because no previous state has been destroyed
- **Attribution is structural** because I-addresses encode the home document permanently
- **Transclusion works** because the referenced content cannot be altered out from under the reference

As I put it: "A document is really an evolving ONGOING BRAID" [LM 2/14]. The braid grows — strands are added, the arrangement shifts — but no strand is ever cut from the fabric of I-space.

---

## Question 2 [nelson]

> When a document arranges content in a particular order, does the document hold its own copy of that content, or does it refer to the single permanent instance?

### Nelson's Answer

## The Document Refers — It Does Not Copy

A document's arrangement is a **mapping** that refers to content stored permanently in I-space. The document does not hold its own copy. This is the central architectural distinction of Xanadu.

### The Two Spaces

Every document has a **V-space** (virtual space) arrangement that points to **I-space** (invariant space) content. The V-space is the order the reader sees; I-space is where the bytes permanently live. Nelson:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

The phrase "regardless of their native origin" is key. The document's arrangement treats all content identically — whether the bytes were originally created in this document or in some other document across the docuverse. The V-space is a sequence of references, not a container of duplicated bytes.

### Native vs. Non-Native — Both in I-Space

There are two kinds of content in a document's byte stream:

1. **Native bytes** — created originally in this document, stored "under its control"
2. **Non-native bytes** — included from other documents by reference

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Even native bytes live in I-space — in the permanent, append-only store. The document doesn't "contain" content in the way a file contains data. It arranges references to content that lives in I-space.

### The COPY Operation Creates References, Not Duplicates

When content moves between documents via the COPY command, no bytes are duplicated:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This "copy" is transclusion — a new V-space mapping to the same I-space bytes. Nelson makes the absence of duplication explicit:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

### Editing Changes the Map, Not the Territory

When you edit a document, you change its V-space arrangement. The I-space content is untouched:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address (position in the current arrangement) shifts with every insert and delete. But the I-address (permanent identity) never changes. Nelson on the conventional alternative he rejects:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Xanadu replaces this with append-only storage:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### Why This Matters

The reference-not-copy model enables every fundamental guarantee:

- **Links survive editing** — links point to I-space addresses, which don't change when V-space is rearranged
- **Attribution is structural** — every byte's I-address encodes its home document, so origin is always traceable
- **Versions are cheap** — a new version is a new V-space mapping over the same I-space content, not a full copy
- **Correspondence is computable** — two versions that share I-space content can be compared automatically
- **Transclusion preserves connection** — the included content IS the original, not a severed copy

Nelson's analogy captures it precisely:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

The glass pane (V-space) arranges what you see. The content visible through windows (I-space references) lives elsewhere permanently. The document is the arrangement, not the content.

---

## Question 3 [nelson]

> If two documents include the same passage, must the system guarantee that both arrangements point to identical underlying content, making the shared origin visible?

### Nelson's Answer

## Yes — but only when inclusion uses transclusion (the COPY operation)

The answer depends on *how* the two documents came to contain the same passage. Xanadu draws a sharp distinction.

### Transclusion: shared I-space origin is guaranteed

When document B includes a passage from document A via the COPY operation, both documents' V-space arrangements point to the **same I-space addresses**. The bytes are not duplicated — they exist once in I-space, and both V-streams reference them.

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

The COPY operation is explicitly described as transclusion — it "shares I-addresses with the source" [LM 4/67]. Both arrangements point to identical underlying content by construction.

### Shared origin is structurally visible and discoverable

The system provides FINDDOCSCONTAINING specifically for this:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

And origin traceability is a fundamental guarantee:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address itself encodes the originating document — `Node.0.User.0.Document.0.Element` — so shared origin is not metadata that can be stripped. It is structural.

### Independent creation: NO shared origin, even for identical text

This is the critical distinction. Content identity is based on **creation**, not **value**. If two users independently type the identical passage, each gets different I-space addresses. The system does not recognize them as sharing origin because they don't — they were created independently.

Only transclusion (COPY) produces shared I-space addresses. Only shared I-space addresses make the relationship visible to FINDDOCSCONTAINING and to the correspondence mechanism.

This is by design. Shared origin means "derived from the same act of creation," not "happens to contain the same bytes." The system preserves provenance, not textual coincidence.

### Summary

| Scenario | Same I-addresses? | Origin visible? | Discoverable via FINDDOCSCONTAINING? |
|----------|-------------------|-----------------|--------------------------------------|
| B transcludes from A (COPY) | Yes | Yes — structural | Yes |
| B independently types same text | No | No — different origins | No |
| B creates version of A (CREATENEWVERSION) | Yes | Yes — structural | Yes |

The guarantee is: **when two documents share content through the system's inclusion mechanism, they necessarily point to the same underlying I-space content, and that shared origin is always visible and discoverable.** The system does not merely *permit* this — it *cannot work any other way*, because transclusion is reference, not duplication.

---

## Question 4 [nelson]

> When a user rearranges content within a document, what must remain invariant about the content's permanent identity — its bytes, its origin, its order of arrival?

### Nelson's Answer

## What Remains Invariant Under Rearrangement

Rearrangement is a **pure V-space operation**. It changes the document's current arrangement (the virtual byte stream) but leaves three things absolutely untouched:

### 1. The Bytes Themselves (I-Space Content)

Content at an I-space address is immutable. Rearrangement changes *where* bytes appear in the document's virtual stream, not *what* those bytes are or *where they permanently live*.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

The I-space is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Nothing in I-space is overwritten, moved, or modified by a rearrangement.

### 2. The Origin (Encoded in the I-Address)

Every byte's permanent I-address has the form `Node.0.User.0.Document.0.Element` [LM 4/26]. This encodes *which server*, *which account*, *which document*, and *which element position* the byte was born into. Rearrangement cannot alter this.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Attribution is structural — it is the address itself, not metadata attached to the address. No V-space operation can sever it.

### 3. The Order of Arrival in I-Space

Bytes are appended to I-space in the order they were created. Their I-addresses reflect this chronological sequence permanently. V-space rearrangement changes the *presentation order* but never the *creation order*.

Nelson makes this explicit for links, which have an even stricter constraint:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

For bytes, the I-space position is similarly fixed at creation time. The V-space is the only thing that moves:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The "constantly changing" address here is the V-address (position in current arrangement). The I-address — the byte's permanent identity — never changes.

---

## What DOES Change

Only V-space is affected:

- **V-addresses shift.** After rearrangement, the same byte may have a different position in the virtual byte stream.
- **The V→I mapping changes.** The document's arrangement — which I-space bytes appear at which V-space positions — is rewritten.

The REARRANGE operation transposes two regions:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

This is purely a remapping of V-space over the same I-space content.

---

## Why This Matters: Link Survivability

The separation is not academic — it is what makes links survive editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Links point to I-space (bytes), not V-space (positions). Rearrangement moves bytes around in V-space but cannot disturb the I-space addresses that links reference. Therefore rearrangement cannot break any link.

---

## Summary

| Property | Invariant under rearrangement? |
|----------|-------------------------------|
| I-space bytes (content) | **Yes** — immutable, append-only |
| I-space address (identity) | **Yes** — permanent, encodes origin |
| Order of arrival in I-space | **Yes** — chronological, never reordered |
| V-space position | **No** — this is what rearrangement changes |
| V→I mapping | **No** — the document's arrangement is rewritten |
| Links to the content | **Survive** — they point to I-space, not V-space |

---

## Question 5 [nelson]

> Can a document's arrangement ever reference content that does not exist in permanent storage, or must every position in a document correspond to something already stored?

### Nelson's Answer

## Every V-Space Position Must Correspond to Stored I-Space Content

A document's V-stream (its current arrangement) is strictly a mapping to content that exists in I-space. Every position in the virtual byte stream resolves to actual stored bytes. There is no mechanism for a V-space position to reference "nothing."

### The Evidence

Nelson defines the V-stream as composed of two kinds of bytes, both of which must exist in storage:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [4/11]

Every byte is either natively stored or fetched from its home. There is no third category of "not yet existing." Non-native bytes participate fully:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [4/11]

The operations confirm this. INSERT creates new I-space content and places it in V-space simultaneously. COPY creates a V-space reference to *existing* I-space content from another document. APPEND adds new stored content. None of these operations allow referencing unstored content.

### The Ghost Element Distinction

Ghost elements might seem like a counterexample, but they operate at a different level entirely. Ghost elements are structural positions in the address hierarchy—servers, accounts, documents—not content bytes:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [4/23]

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [4/23]

Ghost elements are containers with no stored representative object. They are *not* content that a document's V-stream can include. You can link *to* a ghost element (a link's endset can point to an empty address), but you cannot include a ghost element in a document's byte stream.

### Link Endsets vs. Document Content

Link endsets and spans *can* reference addresses where nothing is stored:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [4/45]

> "A span that contains nothing today may at a later time contain a million documents." [4/25]

But these are references in the link/span addressing layer, not positions in a document's V-stream. A link's type endset can point to an empty address by design (type matching is by address, not content). A span can designate an empty range. Neither of these constitutes a document "containing" unstored content.

### Summary

The architecture has two layers with different rules:

| Layer | Can reference empty addresses? |
|-------|-------------------------------|
| **V-stream** (document content) | **No** — every position maps to stored I-space bytes |
| **Link endsets** (connections) | **Yes** — can point to ghost elements, empty ranges |
| **Spans** (address ranges) | **Yes** — can designate ranges with no current content |

A document's arrangement is always a concrete view over real, stored content. The addressing and linking layers are more permissive, allowing forward references and structural pointers into empty space. This separation is consistent with Nelson's design: content is permanent and real; connections and addressing are abstract and anticipatory.

---

## Question 6 [nelson]

> If content is added to permanent storage but no document currently arranges it, does that content still exist and remain retrievable?

### Nelson's Answer

## Yes — Content in I-Space Always Exists, But Addressability Is Through V-Space

The content **exists permanently**. I-space is append-only; nothing is ever removed from it. But "retrievable" requires some nuance about *how* you reach it.

### The Existence Guarantee

I-space is the permanent home of all content:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." — 2/14

Every byte created gets a permanent I-address that will always return that exact content. This is unconditional. No operation in the system removes content from I-space.

### The Addressability Question

The FEBE protocol provides exactly **one** content retrieval command: `RETRIEVEV`, which works through V-space addresses. There is no `RETRIEVEI`. Nelson is explicit that I-space addresses are internal:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." — 4/11

Users work in V-space. I-space is the back end's domain.

### The "Deleted Bytes" State

Nelson directly addresses content that exists in I-space but has been removed from a document's current V-space arrangement. The diagram on page 4/9 labels this state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" — 4/9

Three key phrases here:

1. **"not currently addressable"** — No current V-space arrangement maps to this content, so `RETRIEVEV` through the current document won't find it.

2. **"awaiting historical backtrack functions"** — Previous versions of the document still arrange this content in their V-space. You can always reconstruct those arrangements: "when you ask for a given part of a given version at a given time, it comes to your screen" (2/15).

3. **"may remain included in other versions"** — If other documents transclude this content, their V-space arrangements still reference it, and it remains fully addressable through those documents.

### The Practical Paths to Retrieval

Content that no *current* document arranges is still reachable through:

| Path | Mechanism |
|------|-----------|
| **Historical backtrack** | Request a previous version that included the content — its V-space arrangement is reconstructed on demand |
| **Transclusion in other documents** | Other documents that window this content still reference its I-address |
| **Links** | Links point to I-space; a link to this content still resolves even after V-space deletion |
| **FINDDOCSCONTAINING** | Can discover which documents (including historical versions) contain the material |

Additionally, Nelson confirms that deletion from one document does not affect others:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." — 4/11

### The Theoretical Edge Case

Could content exist in I-space with *no* V-space arrangement ever having referenced it? In practice, no. Every content-creation operation (`INSERT`, `APPEND`) simultaneously creates I-space content *and* a V-space mapping. There is no FEBE command to write directly to I-space without placing content in a document. So "orphaned" I-space content only arises through deletion — and deletion preserves historical versions.

### Summary

The content **exists** unconditionally and permanently. It is **retrievable** through historical backtrack, through other documents that transclude it, and through links that reference its I-address. What it is *not* is "currently addressable" through the document that deleted it from its present arrangement — but that is a narrow constraint on one access path, not on existence or retrievability in general.

Nelson designed the system so that the question "does it still exist?" always has the answer yes. The only question is which V-space arrangement you use to reach it.

---

## Question 7 [nelson]

> When a new version of a document rearranges its content differently, must the system preserve the previous arrangement as well, or only the underlying content?

### Nelson's Answer

## Both Are Preserved

The system must preserve **both** the previous arrangement and the underlying content. This is fundamental to Xanadu's architecture.

### The Arrangement IS the Version

A version in Xanadu is not a snapshot of content — it *is* a particular V-space arrangement over permanent I-space content. Each version has its own V-stream mapping. When you create a new version with a different arrangement, the old version's arrangement remains as a distinct, accessible V-space mapping.

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

### The Two-Layer Guarantee

**I-space (content):** Always preserved. Append-only, never overwritten.

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**V-space (arrangement):** Each version's arrangement is independently preserved and reconstructable.

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

### Why Arrangement Preservation Is Required

Three capabilities depend on it:

1. **Historical backtrack** — Users must be able to reconstruct any previous state, which means reconstructing the previous *arrangement*, not just knowing the content existed.

2. **Intercomparison** — Comparing versions requires both arrangements to exist simultaneously:

   > "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

3. **Correspondence** — The system must show which parts of one arrangement correspond to which parts of another. This is only meaningful if both arrangements are preserved:

   > "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

### The Braid Metaphor

Nelson's metaphor makes this explicit — editing is *re-twisting* the braid, not replacing it:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

The braid accumulates strands. Each twist (rearrangement) adds to the history; it does not erase what came before. Users can "scroll through an individual document, at successive instants of time" [LM 2/15] — which requires each arrangement to persist.

### Summary

Preserving only the content without the arrangement would violate historical backtrack, intercomparison, and correspondence — three of Xanadu's core capabilities. The V-space mapping of every version is as permanent as the I-space content it references.

---

## Question 8 [nelson]

> Must the mapping from a document's arrangement back to the permanent content be exact — byte-for-byte correspondence — or can a document transform or excerpt content in ways that break that correspondence?

### Nelson's Answer

## The mapping must be exact — byte-for-byte, no transformation

The V→I mapping in Xanadu is a strict, exact correspondence: each position in V-space maps to precisely one byte in I-space, with no transformation, summarization, or modification permitted at the mapping level.

### The evidence is structural

**I-space content is immutable.** Content at an I-space address never changes after creation. The entire I-space is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**V-space is a view, not a transform.** The document IS the mapping from V-addresses to I-addresses. Non-native bytes appear "just as if they were native":

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The word "just as if" is critical — the bytes appear identically, not in altered form.

### No transformation operation exists

The FEBE protocol defines exactly five editing operations. None performs transformation:

| Operation | What it does to I-space | What it does to V-space |
|-----------|------------------------|------------------------|
| **INSERT** | Creates new bytes (new I-addresses) | Adds positions, shifts subsequent |
| **APPEND** | Creates new bytes at end | Extends V-stream |
| **COPY** | Nothing — shares existing I-addresses | Adds positions referencing existing I-content |
| **DELETEVSPAN** | Nothing — bytes remain | Removes positions from view |
| **REARRANGE** | Nothing | Transposes regions |

COPY is the transclusion operation, and it explicitly shares I-addresses with the source:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This is reference, not duplication. The copied bytes retain their original I-addresses. There is no operation that says "take these I-space bytes, apply function F, and show the result."

### Excerpting is supported — but it's still exact

You can include a subset of another document's bytes (a span from position 47 to 92, say). This is excerpting. But the bytes you include are the exact original bytes — you select which ones, but you don't alter them. Nelson's Shakespeare example illustrates this:

> "Very well, if Hamlet is already on the system, then E.G. Jewett could publish his own Hamlet very easily: a quote-link to the first part of the original, just up to 'in the soliloquy'; then the word 'luge'; then a quote-link to the rest of the play."

Jewett's document has three V-space regions: a span of Shakespeare's I-bytes, a new I-byte ("luge"), and another span of Shakespeare's I-bytes. Each region maps exactly to its I-space source.

### Correspondence depends on exactness

The entire correspondence mechanism relies on this exactness:

> "Correspondence is a RELATION — the relationship between V-space positions that share the same I-space origin. If two V-positions in different documents (or different versions of the same document) map to the same I-address, those positions CORRESPOND."

If transformation were possible, shared I-addresses would no longer prove correspondence — the same I-bytes could appear differently in different V-space contexts. The version comparison operation SHOWRELATIONOF2VERSIONS returns "ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70], which only works if shared I-address means identical content.

### Attribution depends on exactness

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This guarantee — that you can trace any character to its origin — requires that the character at a V-position IS the character at the corresponding I-position. If transformation were allowed, you'd trace back to different content than what you're seeing.

### Content identity is creation-based, not value-based

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."

This means I-addresses are identity tokens, not content hashes. The system doesn't ask "do these bytes have the same value?" — it asks "are these the same bytes?" Transformation would sever identity while preserving some relationship to the original, but Xanadu has no mechanism for that intermediate state.

### Front-end rendering is separate

The front end may render the same bytes differently — display them in a different font, zoom into a bitmap, play audio at a different speed. But this is display-level interpretation, not a change to the V→I mapping. The bytes flowing from back end to front end are exact.

### Summary

The V→I mapping is a strict bijection at the byte level. Each V-position maps to exactly one I-byte, and that I-byte is delivered unchanged. The architecture provides three things you can do with content: **create** it (INSERT/APPEND → new I-addresses), **reference** it (COPY → shared I-addresses), or **hide** it (DELETE → V-space removal, I-space unchanged). There is no fourth option of "transform it." This exactness is not incidental — it is the foundation on which correspondence, attribution, link survivability, and royalty tracking all depend.

---

## Question 9 [nelson]

> If a user inserts new content into a document, must that content first be committed to permanent storage before the document can arrange it, or can the two happen simultaneously?

### Nelson's Answer

## Content Must Exist in I-Space Before V-Space Can Reference It

Nelson's architecture logically requires that content be committed to permanent storage (I-space) before or simultaneously with its arrangement in V-space — but the user never sees this as a two-step process. The FEBE protocol presents it as a single atomic command.

### The Logical Dependency

V-space is a **mapping** from virtual positions to I-space addresses. You cannot create a mapping to something that doesn't exist:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

V-space entries point TO I-space addresses. The I-space address is the identity. Without it, there is nothing for V-space to reference.

### The Protocol Hides This

INSERT is defined as a single FEBE command:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The user provides text and a V-space position. The system handles I-space commitment internally. Nelson explicitly says users don't see I-space:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

### The Enfilade Manages Both Together

The data structure handles storage and arrangement as a unified concern:

> "a data structure that manages huge agglomerates of text and their arrangement in and out of core." [LM 1/33]

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The "canonical order" mandate means that after any operation, the system is in a fully valid state — I-space and V-space are consistent. This implies atomicity: the two happen together, not as separable steps.

### COPY Confirms the Dependency

The COPY (transclusion) operation is revealing by contrast. It creates a V-space mapping to **already-existing** I-space content:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

COPY needs no new I-space storage because the content already has permanent addresses. INSERT must create those addresses. The append-only model describes how:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### Summary

**Logically**, I-space commitment must precede or be simultaneous with V-space arrangement — V-space is a mapping layer that references I-space, so the referent must exist. **Operationally**, Nelson treats this as a single atomic step. The FEBE protocol exposes one command (INSERT), the enfilade manages both concerns in one data structure, and the user never sees I-space directly. The ordering is an implementation detail that Nelson deliberately hides behind the protocol abstraction.

---

## Question 10 [nelson]

> When content is permanently stored, does it receive a fixed identity at that moment, and must every document arrangement that uses that content refer to it by that same identity forever?

### Nelson's Answer

# Yes, on Both Counts

## Content Receives Fixed Identity at Storage Time

When you create content — when bytes are first stored — they receive a permanent I-space address. That address encodes their origin: which server, which account, which document, which element position. This address is **immutable**. The content at that address **never changes**.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The storage model is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Nothing is overwritten. Nothing is reassigned. The I-address a byte receives at creation is the I-address it keeps forever.

## Every Arrangement Must Reference That Same Identity

A document's V-space (its current arrangement, the virtual byte stream the user sees) is a **mapping to I-space**. The document IS that mapping. When you "include" content from another document, you do not copy it — you create a V-space entry that points to the same I-space address where the content permanently lives.

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The V-address — where the content appears in the document right now — may change constantly through editing. But the I-address it refers to does not:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

That quote describes V-space addresses (positions in the arrangement) being ephemeral. The I-space addresses they point to are permanent.

## Why This Matters

This separation is the architectural foundation for everything else in Xanadu:

**Link survivability.** Links point to I-space addresses. Editing changes V-space arrangements. Therefore links survive editing:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

**Correspondence across versions.** When two versions share I-space content, the system knows which parts correspond — because they reference the same I-addresses. This is structural, not metadata:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

**Transclusion.** When you quote someone, your document's V-space points to their I-space. The content is fetched from its home. Attribution cannot be severed because the reference mechanism requires the I-address:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

**Non-destruction.** "Deleting" content removes it from V-space (the current arrangement) but not from I-space (permanent storage). Previous versions still contain it. Links to it still resolve.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## The Analogy

Think of I-space as library stacks where books have permanent shelf locations. V-space is a reading list that references those shelf locations. You can reorder the reading list, add entries, remove entries — but the books on the shelves never move. Two different reading lists that reference the same shelf location are referencing the same book. That identity — the shelf location — is fixed at the moment the book is shelved and never changes.

```
I-Space (permanent)              V-Space (arrangement)
┌─────────────────────┐          ┌─────────────────────┐
│ I-addr A: "hello"   │          │ Doc v1: [A, B]      │ → "hello world"
│ I-addr B: " world"  │     ──►  │ Doc v2: [A, C]      │ → "hello!"
│ I-addr C: "!"       │          │ Other doc: [A, B, C] │ → "hello world!"
│                     │          │                     │
│ (never changes)     │          │ (freely rearranged)  │
└─────────────────────┘          └─────────────────────┘
```

Every V-space arrangement, in every document, in every version, refers to content by its fixed I-space identity. That is not a convention — it is the architecture.

---

## Question 11 [gregory]

> When a POOM entry is split by INSERT (e.g., inserting into the middle of "ABCDE"), does the split produce two new bottom crums whose I-displacements and I-widths exactly partition the original I-span with no gaps or overlaps?

### Gregory's Answer

## KB Synthesis

## POOM Crum Splitting: V and I Dimensions

The KB directly addresses this, though from multiple angles that need combining.

### What the KB Confirms

**The V-dimension split is exact by construction.**

[INV-NO-ZERO-WIDTH-CRUM] (Finding 0075) describes `slicecbcpm` directly: when a cut falls strictly interior to a crum (`THRUME`), it computes:
- `localcut = tumblersub(cut, &grasp)` — the cut offset from the grasp
- Original crum retains width `localcut` (strictly positive)
- New crum receives `cwid - localcut` via `locksubtract` (also strictly positive)

These two widths sum to exactly `cwid` — no gap, no overlap in V-space.

**The I-width encodes the same count as the V-width.**

[INV-WIDTH-VALUE-EQUIVALENCE] (Finding 0076) states: `value(crum.width.dsas[V]) == value(crum.width.dsas[I])` for every POOM bottom crum. The V and I widths are different tumbler representations of the same integer count.

**A crum is a contiguous bijective mapping.**

[INV-POOM-BIJECTIVITY] establishes the POOM is designed as a bijection from V-addresses to I-addresses. Within a single crum, [SS-POOM-BOTTOM-CRUM] (Finding 0076) shows each crum holds `origin` and `width` in both V and I dimensions, covering a single contiguous block in each. [INV-WIDTH-VALUE-EQUIVALENCE] confirms the two dimensions span the same count.

### The Inference

Given these three facts together: if V and I widths are always numerically equal within a crum, and the V-split produces `(localcut, cwid - localcut)`, then the I-split must produce `(localcut, cwid - localcut)` in the same numeric values — otherwise the crum's V-width and I-width would diverge, violating [INV-WIDTH-VALUE-EQUIVALENCE] on the resulting crums.

The resulting partition is:
- **Left crum**: I-origin = original I-origin, I-width = `localcut`
- **Right crum**: I-origin = original I-origin + `localcut`, I-width = `cwid - localcut`

Together they span `[I_origin, I_origin + cwid)` with no gaps or overlaps — exactly partitioning the original I-span.

### Caveat

The KB does not contain a finding that directly inspects `slicecbcpm`'s I-dimension handling (the code at `ndcuts.c:396-444`). The conclusion is a necessary consequence of [INV-WIDTH-VALUE-EQUIVALENCE] holding on both result crums, not a direct code observation. If `slicecbcpm` somehow applied different arithmetic to the I-origin of the new crum, that invariant would be violated.

**Short answer**: Yes — the I-span is exactly partitioned with no gaps or overlaps. The split must be `(localcut, cwid - localcut)` in both dimensions to preserve [INV-WIDTH-VALUE-EQUIVALENCE] on the resulting crums, and [INV-NO-ZERO-WIDTH-CRUM] guarantees both parts are positive.

---

## Code Exploration

I now have everything needed. Here is my full answer.

---

## Does INSERT Splitting Exactly Partition the Original I-Span?

**Short answer: Yes, exactly — no gaps, no overlaps.** The guarantee is structural and provable directly from `slicecbcpm` in `backend/ndcuts.c`.

---

## Call Path from INSERT to Slice

**`doinsert`** (`do1.c:87`) calls `inserttextingranf` to allocate fresh I-space for the new content, then calls `docopy` → `insertpm`. For the POOM, the relevant path is:

**`insertnd`** (`insertnd.c:15`) — POOM case at line 53–61:
```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);   // [insertnd.c:54]
    setwispupwards(fullcrumptr,0);
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
```

**`makegappm`** (`insertnd.c:124`) sets up two knife positions:
```c
movetumbler (&origin->dsas[V], &knives.blades[0]);                          // [insertnd.c:144]
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);         // [insertnd.c:145]
knives.nblades = 2;
knives.dimension = V;
makecutsnd (fullcrumptr, &knives);                                           // [insertnd.c:148]
```

Knife[0] is the insertion V-address. Knife[1] is "just after" it — computed so the insertion point is isolated as a degenerate slice. `makecutsnd` descends and calls **`slicecbcpm`** on any bottom crum that straddles knife[0].

---

## `slicecbcpm`: The Actual Split (`ndcuts.c:373–450`)

This is the function that does the work. I trace each step for "ABCDE" (original crum: V-span `[1, 6)`, I-span `[I₀, I₀+5)`, width W=5) being cut at V=3 (localcut = 2):

### Step 1 — Assert 1-story invariant (`ndcuts.c:389–394`)
```c
if (!lockis1story (ptr->cwid.dsas, (unsigned)widsize(enftype)))
    gerror ("Not one story in POOM wid\n");
```
`lockis1story` (`wisp.c:298–304`) requires that every tumbler in the wid array has no second mantissa digit (`mantissa[1..] == 0`). For POOM, `widsize` = 2 (both V and I). This asserts `V_width == I_width` as a precondition. **Fatal error if violated.** For our example, both are W=5. ✓

### Step 2 — Compute the V-offset of the cut within this crum (`ndcuts.c:396`)
```c
tumblersub (cut, &grasp.dsas[index], &localcut);
```
`localcut = V_cut - V_crum_start` = 3 − 1 = **2**.

`is1story(&localcut)` is also checked (`ndcuts.c:410`); for integer offsets it must hold.

### Step 3 — Set both dimensions' widths of the left piece (`ndcuts.c:438–445`)
```c
movewisp (&ptr->cwid, &newwid);          // newwid = {V:5, I:5}  (original)
for (i = 0; i < widsize(enftype); i++) { // i = 0 (V), i = 1 (I)
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];   // both set to 2
    tumblerjustify (&newwid.dsas[i]);
}
// After loop: newwid = {V:2, I:2}
```
`tumblerjustify` (`tumble.c:289`) normalizes the mantissa (shifts leading zeros, adjusts exp). For our integer 2, this is a no-op. The loop uniformly assigns `localcut.mantissa[0]` to **every** dimension — both V and I get the same value.

### Step 4 — Right-piece width = original − left (`ndcuts.c:444`)
```c
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, widsize);
// = {V:5, I:5} − {V:2, I:2} = {V:3, I:3}
```
`locksubtract` (`wisp.c:275–279`) iterates `loxize` times (= `widsize` = 2), calling `tumblersub(lock1++, lock2++, lock3++)` — once for V, once for I. `tumblersub` (`tumble.c:406`) is exact subtraction, no rounding. Result: `new->cwid = {V:3, I:3}`.

### Step 5 — Left piece takes its new width (`ndcuts.c:445`)
```c
movewisp (&newwid, &ptr->cwid);          // ptr->cwid = {V:2, I:2}
```

### Step 6 — Right piece displacement = left start + left width (`ndcuts.c:446`)
```c
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
// new->cdsp = {V:1, I:I₀} + {V:2, I:2} = {V:3, I:I₀+2}
```
`dspadd` (`wisp.c:15–18`) calls `lockadd` which calls `tumbleradd` for each of `dspsize(POOM)` = 2 dimensions. Applied uniformly to V and I simultaneously.

---

## Mathematical Proof of Exact Partition

After the slice, the two bottom crums are:

| | V-start | V-width | I-start | I-width |
|---|---|---|---|---|
| **Left** (ptr) | V₀ = 1 | 2 | I₀ | 2 |
| **Right** (new) | 3 | 3 | I₀ + 2 | 3 |

**No gap**: `right.I_start = left.I_start + left.I_width = I₀ + 2`. Follows directly from `dspadd` at `ndcuts.c:446`, applied to I-dimension.

**No overlap**: left covers `[I₀, I₀+2)`, right covers `[I₀+2, I₀+5)`. They share only the boundary point.

**Complete coverage**: `left.I_width + right.I_width = 2 + 3 = 5 = W_original`. Follows from `locksubtract` at `ndcuts.c:444`: `new_width = original_width − left_width`, so `left + new = original` by construction.

The same arithmetic applies in all dimensions simultaneously because `locksubtract` and `lockadd` both iterate over all `widsize` (= 2 for POOM) dimensions.

---

## What Happens to I-Displacements After the Gap-Make

Back in `makegappm` (`insertnd.c:151–168`), after `makecutsnd`, each son is classified by `insertcutsectionnd`:

- **Case 0** (to the left of the insertion point): no change.
- **Case 1** (the right half of the split, between knife[0] and knife[1]): only **V-displacement** is shifted:
  ```c
  case 1:
      tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);  // [insertnd.c:162]
  ```
  The **I-displacement is not touched**. "CDE" stays at `I₀+2` forever; only its V-address shifts to make room for the new text.

- **Case 2** (already past the cut): no change.

The I-addresses of the two halves are immutable after the split. The newly inserted text gets a separately allocated I-span from `inserttextingranf` (`do1.c:118`) — it does not fill any gap between the halves because there is no gap.

---

## Summary

Yes — **the split is an exact partition of the original I-span, with no gaps or overlaps**, guaranteed by the mechanics of `slicecbcpm`:

1. **Precondition** (`ndcuts.c:389`): The 1-story invariant asserts `V_width == I_width`, so a V-offset uniquely determines an I-offset of equal magnitude. Fatal error if violated.
2. **Left-piece widths** (`ndcuts.c:439–441`): The loop over `widsize` sets `mantissa[0]` to `localcut.mantissa[0]` in **every dimension** — V and I receive the identical value.
3. **Right-piece widths** (`ndcuts.c:444`): `locksubtract` subtracts element-wise across all dimensions: `right_width[i] = original_width[i] − localcut` for each i.
4. **Right-piece position** (`ndcuts.c:446`): `dspadd` adds element-wise across all dimensions: `right_start[i] = left_start[i] + left_width[i]` for each i.

The result is algebraically exact: `left.I_width + right.I_width = W`, and `right.I_start = left.I_start + left.I_width`, proven by the subtraction law (`locksubtract`) and the addition law (`dspadd`) that define the construction.

---

## Question 12 [gregory]

> After DELETE removes a V-span that covers only part of a POOM bottom crum, does `slicecbcpm` preserve the exact I-displacement of the surviving portion, or does it recompute it from the V-side cut point?

### Gregory's Answer

## KB Synthesis

The KB does not contain the complete `slicecbcpm` source code, but the answer can be derived from what it does document.

## The I-displacement is recomputed from the V-side cut point

**The mechanics, from the KB:**

[PRE-DELETE / Finding 0075] establishes that `slicecbcpm` is only invoked when the cut falls strictly interior to a bottom crum (`whereoncrum() == THRUME`). The key computation is:

```
localcut = tumblersub(cut, &grasp)   // ndcuts.c:396 — V-side offset from crum grasp to cut
```

This `localcut` is a **V-space** quantity — the number of bytes from the crum's left edge to the cut point.

[INV-NO-ZERO-WIDTH-CRUM] confirms the split produces:
- Left crum: retains width `localcut` (the portion before the cut)
- Right crum: receives width `cwid - localcut` via `locksubtract` (the surviving portion)

**Why the I-displacement follows from V:**

[SS-POOM-BOTTOM-CRUM] establishes that each POOM bottom crum carries `origin.dsas[V]`, `width.dsas[V]`, `origin.dsas[I]`, and `width.dsas[I]` as separate fields. The V-width and I-width encode the same integer value at different tumbler precisions [INV-WIDTH-VALUE-EQUIVALENCE].

Because POOM crums maintain a 1:1 V-to-I correspondence (one I-address per byte of content), the right (surviving) crum's I-origin must be:

```
new_I_origin = old_I_origin + localcut
```

where `localcut` carries the same integer byte count derived from the V-side cut arithmetic. The right crum's I-displacement is not preserved from the original — it is advanced by `localcut` from the original I-origin. There is no separate I-space cut computation; the V-side offset drives both.

**Supporting structure:**

[ST-INSERT / Finding 0031] confirms that I-addresses and V-addresses advance in lockstep for text content — `tumblerincrement(&lsa, 0, textset->length, &lsa)` uses `rightshift=0`, advancing I-addresses by the same integer count as byte length. `slicecbcpm` uses the same integer quantity (`localcut`) to advance the I-origin of the right fragment.

**Summary:** `slicecbcpm` recomputes the I-displacement of the surviving right portion by adding `localcut` (the V-side integer offset) to the original crum's I-origin. The original I-displacement of the right fragment is not directly preserved — it is derived from the V-side cut point, consistent with the 1:1 V↔I byte correspondence that POOM crums maintain.

---

## Code Exploration

Now I have everything needed. Here is the full answer.

---

## Answer: `slicecbcpm` and I-Displacement After Partial POOM Crum Delete

### Execution path: DELETE → `slicecbcpm`

**`dodeletevspan`** [do1.c:158–166] calls `deletevspanpm`, which calls `deletend` [orglinks.c:145–151]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    ...
}
```

**`deletend`** [edit.c:31–76] sets two knife blades — `knives.blades[0] = origin`, `knives.blades[1] = origin + width` — then calls `makecutsnd`. When either blade falls `THRUME` (through the middle of) a height-0 POOM crum, `makecutsbackuptohere` [ndcuts.c:77–91] fires:

```c
if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
    new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
    ...
    slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
    ...
}
```
[ndcuts.c:79–84]

---

### Inside `slicecbcpm` [ndcuts.c:373–450]

The function splits crum `ptr` into a left part (kept in `ptr`) and a new right part (`new`).

**Step 1 — compute absolute grasp (I-start of this crum):**
```c
prologuend(ptr, offset, &grasp, NULL);   // line 382
```
`prologuend` [retrie.c:334–339] does:
```c
dspadd(offset, &ptr->cdsp, grasp, enftype);   // grasp = offset + ptr->cdsp
```
So `grasp.dsas[index]` is the absolute V-address of the crum's left edge.

**Step 2 — compute `localcut` (the V-cut offset within the crum):**
```c
tumblersub(cut, &grasp.dsas[index], &localcut);   // line 396
```
`localcut` = (absolute V-cut address) − (absolute V-start of crum) = V-distance from the crum's left edge to the cut.

**Step 3 — guard: the crum must be "1 story":**
```c
if (!lockis1story(ptr->cwid.dsas, widsize(enftype))) gerror(...)  // line 389–393
```
`is1story` [tumble.c:237–247] returns true only if `mantissa[i] == 0` for all `i >= 1` — meaning all dimensions have a single-digit width. This enforces that V-width == I-width numerically for this bottom POOM crum.

**Step 4 — split the width, then derive the right crum's I-displacement:**
```c
movewisp(&ptr->cwid, &newwid);                                        // line 438: copy original width

for (i = 0; i < widsize(enftype); i++) {                             // line 439
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];               // line 440
    tumblerjustify(&newwid.dsas[i]);                                  // line 441
}
// newwid now holds the left-portion width in ALL dimensions = V-cut offset

locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid,
             (tumbler*)&new->cwid, widsize(enftype));                 // line 444
// new->cwid = original_width − newwid (the right portion's width)

movewisp(&newwid, &ptr->cwid);                                        // line 445
// ptr->cwid ← newwid (left portion's new, truncated width)

dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);                 // line 446
// new->cdsp = ptr->cdsp + ptr->cwid_new
```

`dspadd` [wisp.c:15–18] does element-wise `lockadd` across all DSP slots:
```c
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype) {
    lockadd(a->dsas, b->dsas, c->dsas, dspsize(enftype));
}
```

---

### The Answer

**`slicecbcpm` does NOT preserve the right crum's I-displacement from any stored field. It recomputes it from the V-side cut point.** Specifically:

| Crum | `cdsp` (I-displacement) | `cwid` (width) |
|------|------------------------|----------------|
| **Left (`ptr`)** | **Preserved verbatim** — `ptr->cdsp` is never written | Set to `localcut.mantissa[0]`, derived from V-cut |
| **Right (`new`)** | **Recomputed**: `ptr->cdsp + ptr->cwid_new` [line 446] | `original_width − newwid`, residual after left split |

The right crum's I-displacement is assembled from two sources, both V-derived: `ptr->cdsp` (unchanged original left-edge I-displacement, which was itself originally set when the crum was inserted) plus `ptr->cwid_new` (the left portion's new width, which equals `localcut.mantissa[0]`, the V-distance from the crum's left edge to the cut).

**Why this is correct, not lossy**: The loop at lines 439–442 sets all dimensions of `newwid` (including the I-dimension) to `localcut.mantissa[0]`. This works because the guard at line 389 (`lockis1story`) enforces that all dimensions of the POOM bottom crum have the same single-digit width — V-span and I-span are the same number at the same tumbler level. Under that invariant, `localcut` (a V-offset) is numerically identical to the I-offset at the same point; there is no separate I-coordinate to consult or preserve.

The original author's comment at line 439 — `/* I really don't understand this loop */` — suggests even he found this multi-dimension overwrite surprising, but it is the mechanism that propagates the 1-story invariant into the split crums.

---

### After the cut: surviving portions in DELETE

After `makecutsnd` cuts both boundaries of the deleted span, `deletend` [edit.c:47–73] classifies each child:

- **Section 1** (entirely inside the deleted span): `disown` + `subtreefree` — **gone**
- **Section 2** (entirely to the right of the deleted span): `tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index])` — its V-displacement is decremented by the deleted width. Its **I-displacement is untouched** here. The I-displacement it carries is the one set (or recomputed) by `slicecbcpm` at the right boundary cut.

So the surviving left crum has its I-displacement exactly as it was before the cut — `slicecbcpm` left `ptr->cdsp` alone. The surviving right crum has an I-displacement that was recomputed by `dspadd` at line 446, derived from the V-cut point via `localcut`, not read from any independently stored I-address.

---

## Question 13 [gregory]

> When `vspanset2sporglset` walks the POOM to convert a V-span to I-spans, and the V-span crosses a boundary between two POOM entries with non-contiguous I-addresses, does it always produce exactly one sporgl per contiguous I-run — never merging across I-gaps or splitting within a contiguous I-run?

### Gregory's Answer

## KB Synthesis

## `vspanset2sporglset`: One Sporgl Per Contiguous I-Run

### The confirmed behavior

Yes — `vspanset2sporglset` produces exactly one sporgl per contiguous I-address run, neither merging across gaps nor splitting within a run. Here is what the KB supports for each half of that claim.

---

### Never merges across I-gaps

[ST-LINK-CREATE] (Finding 0037) provides the definitive confirmation via a concrete example:

> Document C contains "AABB" where "AA" came from document A and "BB" from document B — non-contiguous I-address regions.
>
> `create_link(source = V-span 1.1 width 0.4 in doc C)`
>
> Input: 1 V-span covering all of "AABB"  
> Output: **2 sporgls** — one for "AA"'s I-range, one for "BB"'s I-range

The conversion chain is:

```
V-span → vspanset2ispanset → permute → span2spanset
       → retrieverestricted → separate I-span per contiguous I-region
       → separate sporgl per I-span
```

The inner loop at `sporgl.c:49-58` creates one sporgl per I-span returned by `vspanset2ispanset` — it has no merging logic. Two non-contiguous I-regions in the POOM produce two I-spans, which produce two sporgls. The I-gap between "AA"'s permascroll addresses and "BB"'s permascroll addresses is preserved.

---

### Never splits within a contiguous I-run

This half is not explicitly confirmed in the KB but is well-supported by structural evidence:

1. **[INV-VSPAN-CONSOLIDATION]** (Finding 0028): "The enfilade consolidates logically contiguous V-space regions into a single span regardless of insertion history." Sequential inserts that receive contiguous I-addresses are stored compactly in the POOM — the enfilade is designed to avoid fragmentation.

2. **[SS-POOM-MULTIMAP]** (Finding 0039): The accumulation function `incontextlistnd()` collects POOM contexts sorted by V-address. For a query by V-span (V→I direction, via `permute`), each POOM crum that overlaps the V-span contributes one I-span. If two adjacent crums cover contiguous I-addresses, the resulting I-spans are contiguous — the KB identifies no merging step, but the phrase from [ST-LINK-CREATE] "separate I-span per **contiguous** I-address region" treats a contiguous region as a unit.

3. **[SS-VSPAN-TO-SPORGL]** (Finding 0013): "converts V-addresses to I-addresses via the document's enfilade (`vspanset2ispanset`)" — there is no documented consolidation step after the conversion, which means the POOM structure itself determines the I-span boundaries. Since [INV-VSPAN-CONSOLIDATION] confirms the POOM stores contiguous content compactly, a contiguous I-run maps to a compact POOM representation, producing a single I-span in output.

**Caveat**: The KB does not explicitly describe what happens when tree rebalancing or splitting (documented in [SS-ENFILADE-TREE] / Findings 0058, 0060) places adjacent POOM crums with contiguous I-addresses. Whether those produce one merged I-span or two adjacent I-spans from the `retrieverestricted` call chain is not confirmed. The KB cannot definitively rule out this edge case.

---

### Summary

| Case | KB support |
|------|-----------|
| Non-contiguous I-regions → separate sporgls | **Directly confirmed** by [ST-LINK-CREATE] (Finding 0037) |
| Contiguous I-region → single sporgl | **Inferred** from [INV-VSPAN-CONSOLIDATION] + [SS-VSPAN-TO-SPORGL]; not explicitly confirmed for tree-split crums |
| Merging across I-gaps | **Never** — no merging logic documented; inner loop is one-sporgl-per-I-span |

The KB is answerable on the non-contiguous case and directionally supported on the contiguous case, but the splitting-within-a-contiguous-run question for tree-internal crum boundaries is not explicitly addressed.

---

## Code Exploration

I now have everything needed for a complete answer. Here it is.

---

## Answer

**Yes — with a precise qualification.** `vspanset2sporglset` always produces exactly one sporgl per POOM leaf-crum contribution. It never merges across I-gaps, and it never splits within a single crum's contiguous I-range. However, it also never merges *across* adjacent crums that happen to be I-contiguous — so the guarantee is per-crum, not per maximal-contiguous-I-run across crum boundaries.

Here is the complete call chain traced from source.

---

### 1. The outer loop: one sporgl per I-span

`vspanset2sporglset` [sporgl.c:35–65]:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
        sporglset->itemid = SPORGLID;
        sporglset->next = NULL;
        movetumbler (docisa, &sporglset->sporgladdress);
        movetumbler(&ispanset->stream,&sporglset->sporglorigin);
        movetumbler (&ispanset->width, &sporglset->sporglwidth);
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

[sporgl.c:47–58]. The inner loop is a direct 1:1 traversal of `ispanset`: **one `typesporgl` allocated and filled per `ispanset` node, no merging, no skipping.** The question therefore reduces entirely to what `vspanset2ispanset` deposits into `ispanset`.

---

### 2. `vspanset2ispanset` → `permute` → `span2spanset`

[orglinks.c:397–402]:
```c
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` [orglinks.c:404–422] iterates over each V-span in the restriction set and calls `span2spanset` once per span, threading the tail pointer through so all results accumulate in one list.

`span2spanset` [orglinks.c:425–454]:
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

**One context → one I-span via `context2span` → appended via `onitemlist`.**

---

### 3. Context collection: `retrieveinarea` → `findcbcinarea2d`

`retrieverestricted` [retrie.c:56–85] delegates to `retrieveinarea` [retrie.c:87–110], which for POOM calls `findcbcinarea2d` [retrie.c:229–268]:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, infoptr))
        continue;
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

[retrie.c:252–264]. This is a recursive descent that visits every POOM leaf crum (`height == 0`) whose V-range overlaps the restriction span. **Each qualifying leaf crum produces exactly one context**, inserted into a sorted list by `incontextlistnd`.

`incontextlistnd` [context.c:75–111] sorts contexts in `index1` (V) order — it does not deduplicate or merge. Each context records the crum's `totaloffset` and `contextwid` in both V and I dimensions, copied verbatim from `makecontextfromcbc` [context.c:151–174]:

```c
context = createcontext(crumptr->cenftype);
movewisp(offsetptr, &context->totaloffset);
movewisp(&crumptr->cwid, &context->contextwid);
...
dspadd(&context->totaloffset, &crumptr->cdsp, &context->totaloffset, (INT)crumptr->cenftype);
```

[context.c:159–167]. The context's I-range is `[totaloffset.dsas[I], totaloffset.dsas[I] + contextwid.dsas[I])` — exactly the leaf crum's I-range.

---

### 4. Clipping within a crum: `context2span`

[context.c:176–212]:
```c
movetumbler (&restrictionspanptr->stream, &lowerbound);
tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
prologuecontextnd (context, &grasp, &reach);

if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement (&grasp.dsas[idx2], 0,
        (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement (&reach.dsas[idx2], 0,
        - tumblerintdiff (&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);
}
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);
```

[context.c:186–207]. This clips the crum's I-range (`idx2`) proportionally to the portion of the V-span (`idx1`) restriction that overlaps the crum. If the crum's left V-edge extends left of the V-span start, the I-origin is shifted right by the same integer amount. If the crum's right V-edge extends past the V-span end, the I-reach is shifted left. **Both adjustments are integer differences applied isometrically** (via `tumblerintdiff` which returns a scalar delta). The result is one contiguous I-span — a prefix/suffix/interior clip of the crum's I-range. No splitting.

---

### 5. Appending without merging: `onitemlist`

[orglinks.c:464–537]:
```c
((typeitemheader *)newitem)->next = NULL;
if (*itemsetptr == NULL) {
    *itemsetptr = newitem;
} else {
    for (temp = *itemsetptr; temp && ((typeitemheader *)temp)->next;
         temp = (typeitem *)((typeitemheader *)temp)->next) ;
    ((typeitemheader *)temp)->next = (typeitemheader *)newitem;
}
return (newitem);
```

[context.c:517–534]. This walks to the end of the existing list and appends. **There is no contiguity check, no tumbler comparison between the new span and the last span in the list, and no merging.** Two I-spans that happen to be adjacent in I-space produce two separate list nodes.

*(Note: `putvspaninlist` in orglinks.c:329–387 does have merge/sort logic, but that function is used for V-span lists in `walkorglonvpm`, not in this pipeline. `onitemlist` is what `span2spanset` calls.)*

---

### 6. What the scenario produces

When a V-span crosses the boundary between two POOM leaf crums A and B with non-contiguous I-addresses:

| Step | What happens |
|------|-------------|
| `findcbcinarea2d` | Finds both crums A and B (both qualify); creates two contexts, sorted by V via `incontextlistnd` |
| `context2span` (A) | Clips A's I-range to the portion of the V-span overlapping A → one contiguous I-span |
| `onitemlist` (A) | Appends that I-span to `ispanset` |
| `context2span` (B) | Clips B's I-range to the portion of the V-span overlapping B → one contiguous I-span |
| `onitemlist` (B) | Appends that I-span; **no check against A's I-span endpoint** |
| `vspanset2sporglset` | Iterates `ispanset`: allocates sporgl for A's I-span, then sporgl for B's I-span |

**Result: two sporgls, one per POOM crum, one per I-run.** Since the I-addresses are non-contiguous by premise, these are genuinely separate I-runs, and each gets exactly one sporgl. The I-gap between them is neither bridged nor collapsed.

---

### 7. The critical caveat

The guarantee holds exactly at **POOM leaf-crum granularity**:

- **One crum → one sporgl**, always. `context2span` clips proportionally without splitting [context.c:191–207].
- **No merging across crums**, ever. `onitemlist` has no merge logic [orglinks.c:517–534].

This means: if two adjacent POOM crums happen to have *contiguous* I-addresses (their I-ranges abut), the pipeline still produces **two separate sporgls** — a spurious split at the crum boundary in I-space. The function does not detect or collapse adjacent I-spans from different crums.

In the specific scenario the question asks about (two POOM entries with **non-contiguous** I-addresses), this caveat is irrelevant: both sporgls represent genuinely disjoint I-runs, so "one sporgl per contiguous I-run" holds exactly. The code never merges across I-gaps (no such logic exists) and never splits within a single crum's I-contribution (clipping is proportional and linear).

---

## Question 14 [gregory]

> Is there any operation that can change which I-address a given V-position maps to WITHOUT removing and re-inserting the POOM entry — for instance, does REARRANGE modify I-displacements in-place, or does it only adjust V-displacements while leaving I-fields untouched?

### Gregory's Answer

## KB Synthesis

**No operation modifies I-address fields in-place. REARRANGE modifies only V-displacements, leaving I-fields untouched.**

The key evidence is in [ST-REARRANGE] (Finding 0056):

> "The operation modifies V-addresses exclusively — it calls `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])` which updates the displacement's V-address component. No I-addresses are touched, no content is copied, no new permascroll entries are created."

The POOM bottom crum stores V and I coordinates separately [SS-POOM-BOTTOM-CRUM]:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler,  dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler,  dsas[V]: Tumbler }
}
```

REARRANGE writes to `cdsp.dsas[V]` only. The `dsas[I]` field is never modified by any displacement operation. This is reinforced by [INV-REARRANGE-IDENTITY] (Finding 0056):

> "The I-address, stored separately, is never touched."

The functional effect of changing which I-address a given V-position maps to is achieved entirely through V-field modification: after a pivot, the crum that formerly covered V[1.3, 1.4) now covers V[1.6, 1.7), so querying V=1.3 hits a different crum with a different I-origin. The observable mapping changes, but through V-shifting, not I-mutation.

To enumerate all four operation classes:

| Operation | POOM I-field | POOM V-field | Entry lifecycle |
|-----------|-------------|-------------|----------------|
| INSERT | Write-once (new entry) | Write-once (new entry) | Created |
| COPY/VCOPY | Write-once (new entry) | Write-once (new entry) | Created |
| DELETE | — | — | Removed via `disown`+`subtreefree` [ST-DELETE] |
| REARRANGE | **Untouched** | Modified in-place | Retained |

The I-address field of any POOM crum is write-once at creation time and never subsequently modified. REARRANGE is the only operation that mutates an existing entry's fields, and it restricts those mutations to the V-dimension exclusively [FC-POOM-MUTABILITY].

---

## Code Exploration

Now I have a complete picture. Let me compile the definitive answer.

---

## Answer

**REARRANGE modifies only V-displacements. I-fields are left completely untouched. No operation in the codebase can change the V→I mapping of an existing POOM entry without removing and re-inserting it.**

Here is the full evidence trail.

---

### 1. The POOM crum structure

Every crum (`typecorecrumhedr`, `typecuc`, `type2dcbc`) carries two fields:

```c
typewid cwid;   // width in each dimension
typedsp cdsp;   // displacement from parent in each dimension
```

Both are `typewid`, defined in `wisp.h:50-54` as:

```c
struct structwid {
    tumbler dsas[MAXLOXIZE];   // MAXLOXIZE = 2
};
```

The two slots are indexed by symbolic constants defined in `wisp.h:19-20`:

```c
#define I  0     // I-space (permascroll address dimension)
#define V  1     // V-space (virtual document position dimension)
```

So `cdsp.dsas[I]` is the I-displacement and `cdsp.dsas[V]` is the V-displacement, both stored per-crum, relative to the parent node's absolute position.

---

### 2. The rearrange call chain

The document-level rearrange entry point is `dorearrange` in `do1.c:34`:

```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    );
}
```

`rearrangepm` is in `orglinks.c:137-142`:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);   // [orglinks.c:139]
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

**`rearrangend` is always called with `index = V`.** This is not incidental; `ndenf.h:15` makes it a structural invariant:

```c
typedef struct structknives {
    INT nblades;
    tumbler blades[MAXCUTS];
    INT dimension;  /* always V, assigned by rearrange2d */   // [ndenf.h:15]
} typeknives;
```

---

### 3. What `rearrangend` actually modifies

`rearrangend` in `edit.c:78-160` does three things:

1. Cuts the enfilade at the given V-positions (`makecutsnd`).
2. Classifies each crum into a section (before cut 0, between cuts, after last cut) via `rearrangecutsectionnd`.
3. For crums that need to move, applies the displacement delta **only to `cdsp.dsas[index]`**:

```c
// edit.c:125
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
ivemodified((typecorecrum*)ptr);
```

With `index = V`, this line expands to:

```
ptr->cdsp.dsas[V] += diff[i]
```

`ptr->cdsp.dsas[I]` is **never referenced** anywhere in `rearrangend` or `rearrangecutsectionnd` [`edit.c:191-204`].

---

### 4. Are there any other paths that alter I-displacements in-place?

The complete list of code that writes to `cdsp.dsas[I]` or the entire `cdsp` structure:

| Site | What it does | Does it change V→I mapping? |
|------|-------------|----------------------------|
| `insertnd.c:212` `movewisp(origin, &ptr->cdsp)` | First insertion into empty enfilade — sets both I and V | No; first insert creates the mapping |
| `insertnd.c:263` `dspsub(origin, grasp, &new->cdsp, ...)` | Creates a brand-new crum (not modifying existing) | No; establishes new mapping for new crum |
| `makeroom.c:58` `movetumbler(newdsp, &crumptr->cdsp.dsas[index])` | `expandcrumleftward`: adjusts parent dsp when insertion extends to the left | No — compensated by line 65 which shifts all children by the same `base`, preserving absolute positions |
| `makeroom.c:65` `tumbleradd(base, &ptr->cdsp.dsas[index], ...)` | Children shifted to compensate for parent shift above | No — pure relative-encoding adjustment |
| `wisp.c:211` `dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, ...)` | `setwispnd`: normalizes relative displacements after restructuring | No — subtracts `mindsp` from every child and adds it to the parent (`wisp.c:200`), so absolute addresses are preserved |
| `wisp.c:224` `movewisp(&newdsp, &father->cdsp)` | Writes the recomputed dsp back to the parent in `setwispnd` | No — same normalization invariant |
| `recombine.c:248`, `recombine.c:265` `dspsub(...)` / `dspadd(...)` on `nephew->cdsp` | Node adoption during recombine/split | No — purely restructures the tree topology; absolute addresses unchanged |

The key insight for `setwispnd` (tree normalization, `wisp.c:171`): the routine subtracts `mindsp` from every child and adds `mindsp` to the father's absolute displacement (line 200: `dspadd(&father->cdsp, &mindsp, &newdsp, ...)`). This is a rigid body translation of the representation: **every existing crum's absolute position = sum of ancestor displacements is preserved in both I and V dimensions simultaneously.**

---

### 5. Definitive conclusion

> **REARRANGE modifies only V-displacements (by design and by code), leaving I-fields (`cdsp.dsas[I]`) completely untouched in all crums it touches.**

There is no operation in the codebase — not rearrange, not setwispnd, not recombine, not expandcrumleftward — that changes the absolute V→I mapping of an existing POOM entry without a destroy-and-recreate cycle. The I-address a given V-position maps to can only change by:

1. **Delete** (`deletend`/`deletevspanpm`): removes the crum entirely.
2. **Insert** (`insertnd`/`insertcbcnd`): creates a new crum with both `cdsp.dsas[I]` and `cdsp.dsas[V]` set from scratch (via `dspsub` at `insertnd.c:263` or `movewisp` at `insertnd.c:212`).

The asymmetry is architectural: V-space is the "editable" dimension (content can be moved around in document space), while I-space represents the permanent provenance record (permascroll addresses are immutable once assigned). REARRANGE is implemented to honor exactly this distinction.

---

## Question 15 [gregory]

> When `isanextensionnd` coalesces a new insertion into an existing POOM bottom crum (the ONMYRIGHTBORDER case), does it verify that the new I-address is exactly `existing_I_end + 1`, or could it coalesce I-addresses that are close but not strictly adjacent?

### Gregory's Answer

## KB Synthesis

The KB is explicit: `isanextensionnd` requires **exact** adjacency, not approximate closeness. It is a strict equality check in both dimensions.

From [ST-INSERT] (Finding 0062):

> `isanextensionnd()` checks two conditions: (1) the new content has the same `homedoc` as the existing crum, and (2) the new content's origin **equals** the existing crum's reach.

The condition is `reach == origin` — equality, not proximity. The crum's reach is `grasp + width` (its exclusive upper bound in both V and I space). The new insertion's origin must be that exact value. If the new I-address is `existing_I_end + 2` (a gap) or `existing_I_end - 1` (an overlap), `isanextensionnd` returns FALSE and a new crum is allocated instead.

[ST-VCOPY] (Finding 0046) confirms the same condition applies to COPY:

> `isanextensionnd()` at `insertnd.c:293-301` checks ... the new mapping starts **exactly** where the existing crum ends (contiguous in both V and I dimensions).

This is why [ST-INSERT] (Finding 0063) documents the CREATELINK-breaks-coalescing effect: after CREATELINK allocates a link orgl in I-space, the next text INSERT's I-address origin is no longer equal to the previous text crum's I-address reach — there is a gap (the link orgl's allocation). `isanextensionnd` returns FALSE, a new crum is created, and `compare_versions` shows two disjoint I-span pairs instead of one.

The concrete example from [ST-INSERT] (Finding 0062) makes the exact-equality semantics clear:

```
Crum covers [1.3, 1.4) in V; corresponding I-addresses have reach I_r

INSERT "Y" at v+1, new I-address = I_r exactly → isanextensionnd TRUE → coalesce
INSERT "Y" at v+1, new I-address = I_r + 1     → isanextensionnd FALSE → new crum
```

No tolerance for "close but not adjacent" exists in the implementation.

---

## Code Exploration

I now have all the necessary pieces. Let me compile the full answer.

---

## Answer

`isanextensionnd` requires **exact equality** — the new I-address must be precisely `existing_I_start + existing_I_width` (i.e., `existing_I_end + 1`). There is no tolerance for "close but not strictly adjacent."

---

### Full trace

#### 1. `isanextensionnd` — `insertnd.c:301`

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

Three things happen:

1. **Homedoc guard** [`insertnd.c:305`]: the home document of the new insertion must match the existing crum's home document — or coalescing is refused unconditionally.

2. **`prologuend`** [`retrie.c:334–339`] computes `grasp` and `reach`:

   ```c
   int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
   {
       dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
       if (reach)
           dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
   }
   ```

   - `grasp = offset + ptr->cdsp` — absolute start address of the crum in all dimensions
   - `reach = grasp + ptr->cwid` — absolute end address (exclusive endpoint) in all dimensions

   For POOM, this operates on **both** the V-dimension and I-dimension simultaneously via `dspadd`, which calls `lockadd` over `dspsize(POOM) = 2` tumblers [`wisp.h:26`, `wisp.c:17`].

3. **`lockeq`** [`insertnd.c:308`] checks strict equality:

   ```c
   bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize)
   {
       while (loxize--)
           if (!tumblereq (lock1++, lock2++))
               return(FALSE);
       return(TRUE);
   }
   ```
   [`wisp.c:261–267`]

   For POOM: `loxize = dspsize(POOM) = 2` [`wisp.h:26`, `wisp.h:61`], so it calls `tumblereq` on **both** `reach.dsas[V]` and `reach.dsas[I]`.

#### 2. `tumblereq` — `tumble.c:24–36`

```c
bool tumblereq(tumbler *a, tumbler *b)
{
  register INT i;
    if (a->xvartumbler != b->xvartumbler) return FALSE;
    if (a->varandnotfixed != b->varandnotfixed) return FALSE;
    if (a->sign != b->sign) return FALSE;
    if (a->exp != b->exp) return FALSE;
    for (i = 0; i < NPLACES; i++) {
        if (a->mantissa[i] != b->mantissa[i]) return FALSE;
    }
    return TRUE;
}
```

This is a **field-by-field bitwise equality** check — every bit of every field of the tumbler must match. There is no rounding, no delta tolerance, no approximation.

#### 3. What `reach.dsas[I]` actually is

For a POOM bottom crum with:
- I-start = `ptr->cdsp.dsas[I]` (stored in the crum's DSP)
- I-width = `ptr->cwid.dsas[I]` (stored in the crum's width)

After `prologuend`:
```
reach.dsas[I] = (offset.dsas[I] + ptr->cdsp.dsas[I]) + ptr->cwid.dsas[I]
              = absolute_I_start + I_width
              = existing_I_end + 1
```

`isanextensionnd` then returns `TRUE` only if `origin.dsas[I]` equals `reach.dsas[I]` exactly — i.e., if the new insertion starts at exactly `existing_I_end + 1`.

An I-address that is "close but not strictly adjacent" (e.g., `existing_I_end + 2`) would make `tumblereq` return `FALSE`, `lockeq` return `FALSE`, and `isanextensionnd` return `FALSE`, so no coalescing occurs and a new bottom crum is created instead [`insertnd.c:260–274`].

#### 4. The ONMYRIGHTBORDER question

The term "ONMYRIGHTBORDER" appears in `whereoncrum` [`retrie.c:367–371`] and `findsontoinsertundernd` [`insertnd.c:293–296`] — that is, in the logic that selects *which* crum to insert into at internal node height. Once the tree traversal reaches the bottom layer (`father->height == 1`), control passes to `insertcbcnd` [`insertnd.c:242–275`], which iterates over bottom crums and calls `isanextensionnd` on each one [`insertnd.c:250`]. The ONMYRIGHTBORDER classification in the upper layers only controls tree traversal; the actual coalescing decision is entirely inside `isanextensionnd`, which uses strict `lockeq` equality — not ONMYRIGHTBORDER — as its acceptance criterion.

---

### Summary

`isanextensionnd` performs **strict exact-adjacency verification**. It computes `reach = existing_start + existing_width` across all POOM dimensions (both V and I), then uses `lockeq` → `tumblereq` for field-by-field bit equality. The new I-address must be exactly `existing_I_start + existing_I_width` — which is precisely `existing_I_end + 1`. I-addresses that are close but not strictly adjacent cannot coalesce.

---

## Question 16 [gregory]

> In the POOM's 2D enfilade, the I-dimension index enables reverse lookup (given an I-address, find V-positions). When multiple V-positions map to the same I-address (self-transclusion), does `incontextlistnd` return ALL matching V-positions in a single traversal, or does it require multiple queries?

### Gregory's Answer

## KB Synthesis

**A single traversal returns all matching V-positions.**

The definitive evidence is in [SS-POOM-MULTIMAP] (Finding 0039):

> The search algorithm `findcbcinarea2d()` traverses all siblings at each B-tree level and recursively descends into **all qualifying subtrees**, accumulating every matching leaf node. The accumulation function `incontextlistnd()` inserts each found context into a sorted linked list, **never replacing existing entries**.

The concrete example from that entry confirms this:

```
Document has "B" at V-positions 1.2, 1.4, and 1.5, all referencing I-address i_B.

ispan2vspanset(poom, i_B) = {
  VSpan(1.2, width=0.1),
  VSpan(1.4, width=0.1),
  VSpan(1.5, width=0.1)
}
Result set cardinality = 3 (one per V-position referencing i_B)
```

The mechanism works because `findcbcinarea2d()` does not stop at the first match — it continues traversing all siblings via `getrightbro` and all qualified subtrees, invoking `incontextlistnd()` per leaf. `incontextlistnd()` performs insertion-sort into the accumulated list rather than replacement, so each V-position referencing the queried I-address gets a distinct context entry.

The ordering guarantee from [SS-CONTEXT-LIST] (Finding 0078) applies: the returned list is sorted by V-address regardless of tree structure or insertion order, as a property of the insertion-sort in `incontextlistnd()`.

This single-traversal, all-results behavior is also confirmed by [INV-RETRIEVAL-TREE-INDEPENDENCE] — the result set is independent of how the POOM tree is structured internally, meaning the completeness property holds for any tree shape, not just pathological or simple cases.

**Summary:** One call to `ispan2vspanset` (via `findcbcinarea2d` + `incontextlistnd`) returns all V-positions mapping to a given I-address, sorted by V-address, in a single traversal.

---

## Code Exploration

I have all the code I need. Here is the complete answer.

---

## Answer: `incontextlistnd` is a single-insertion function; all V-positions are collected in one traversal pass

### The POOM's 2D structure

Each POOM bottom crum (`type2dcbc`) holds a 2D displacement/width pair indexed by `I=0` and `V=1` [`wisp.h:19-20`]:

```
/* wid and dsp indexes for pm */
#define I  0
#define V  1
```

Every bottom crum occupies a rectangle in the I×V space. Self-transclusion means multiple such crums share the same I-extent but differ in their V-coordinate — the same I-content appears at more than one V-position.

---

### The reverse-lookup call chain (I → V)

`ispan2vspanset` [orglinks.c:389-393] is the public entry point:

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute` [orglinks.c:404-422] iterates over every span in the restriction set and calls `span2spanset` for each:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
}
```

`span2spanset` [orglinks.c:425-454] drives the actual tree traversal and then iterates the resulting context list:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);  // [orglinks.c:435]

for (c = context; c; c = c->nextcontext) {                                 // [orglinks.c:439]
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`retrieverestricted` [retrie.c:56-85] → `retrieveinarea` [retrie.c:87-110] → `findcbcinarea2d` [retrie.c:229].

---

### `findcbcinarea2d`: the full-tree traversal that collects all matches

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {          // [retrie.c:252]
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset,
                         span1start, span1end, index1,
                         span2start, span2end, index2, headptr, infoptr); // [retrie.c:259]
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr); // [retrie.c:262]
        incontextlistnd (headptr, context, index1);                            // [retrie.c:263]
    }
}
```

Three things to note:

1. **The outer `for` loop iterates all right-siblings at each level** — it does not stop at the first match.
2. **`findcbcinarea2d` recurses into every qualifying upper crum** — depth-first, touching every qualifying subtree.
3. **`incontextlistnd` is called once per qualifying bottom crum** — it is a list-*insertion* function, not a query function.

`crumqualifies2d` [retrie.c:270-305] checks whether a crum's I-extent overlaps the query I-span. When `span2` is null (no V restriction — the case for a pure I→V lookup), `iszerotumbler(span2end)` returns `TOMYRIGHT` [retrie.c:292], meaning every crum qualifies on the V axis. All bottom crums whose I-extent overlaps the query are found, regardless of their V-position.

---

### `incontextlistnd`: sorted list insertion, not a query

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)   // [context.c:75]
{
    prologuecontextnd (c, &grasp, (typedsp*)NULL);
    c->nextcontext = NULL;
    clist = *clistptr;
    if (!clist) {                                          /* 1st insertion */
        *clistptr = c;
        return(0);
    }
    if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist;                            /* on beginning */
        *clistptr = c;
        return(0);
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            if ((whereoncontext (clist, ...) > ONMYLEFTBORDER)
             && (whereoncontext (nextc, ...) < ONMYLEFTBORDER)) {
                c->nextcontext = nextc;                    /* in middle */
                clist->nextcontext = c;
                return(0);
            }
        }
    }
    clist->nextcontext = c;                                /* on end */
}
```

`whereoncontext` for `POOM` type [context.c:137-139]:

```c
case POOM:
    movetumbler (&ptr->totaloffset.dsas[index], &left);
    tumbleradd (&left, &ptr->contextwid.dsas[index], &right);
```

The position comparison constants [common.h:86-90]:

```
TOMYLEFT=-2, ONMYLEFTBORDER=-1, THRUME=0, ONMYRIGHTBORDER=1, TOMYRIGHT=2
```

`incontextlistnd` inserts `c` into the linked list sorted by I-position. It makes no attempt to deduplicate, merge, or suppress entries with the same I-address. Every qualifying crum that `findcbcinarea2d` discovers is inserted unconditionally.

---

### Self-transclusion: what happens

For self-transclusion — say two bottom crums `A` and `B` both covering I-span `[5, 10)` but at V-positions `3` and `7` respectively — `findcbcinarea2d` will:

1. Visit crum `A` (qualifies on I), call `incontextlistnd` → list is `[A]`
2. Continue the sibling loop, visit crum `B` (also qualifies on I), call `incontextlistnd` → list is `[A, B]` (or `[B, A]` depending on I-sort order, which is the same here)

After the traversal, `span2spanset` loops over `[A, B]` [orglinks.c:439] and converts each to a V-span via `context2span`, appending both to the result span-set. Both V-positions — 3 and 7 — appear in the output.

---

### Conclusion

**`incontextlistnd` returns nothing — it inserts one context per call.** The function that does the actual "finding" is `findcbcinarea2d`, which performs a complete recursive walk over the POOM tree in a single traversal, calling `incontextlistnd` once for every qualifying bottom crum it encounters. All crums whose I-extent overlaps the query I-address are collected into the sorted context list before the traversal returns. The caller (`span2spanset`) then iterates the complete list and emits a V-span for each entry.

**Self-transclusion requires no additional queries.** All V-positions that map to the same I-address are found and returned in the single call to `retrieverestricted` / `findcbcinarea2d`. The context list handed back to `span2spanset` already contains all of them, sorted by I-position.

---

## Question 17 [gregory]

> After COPY creates shared I-address references between two documents, if the source document DELETEs that content, do the target document's POOM entries still resolve correctly through the granfilade — i.e., is there any reference-counting or liveness check that could invalidate the target's I→content mapping?

### Gregory's Answer

## KB Synthesis

Yes, the target document's POOM entries resolve correctly. No, there is no reference-counting or liveness check of any kind.

## What DELETE Actually Does

[FC-DELETE-CROSS-DOC] states this explicitly: DELETE operates on a single document's POOM tree only — `deletend` frees bottom crums from that document's orgl, and other documents' trees are completely separate data structures, untouched. The concrete consequence:

```
D has "ABCD", T transcluded "BC" (sharing I(5.2), I(5.3))

After DELETE "BC" from D:
  POOM(D): V(1.1)→I(5.1)  V(1.2)→I(5.4)    — BC mapping gone from D
  POOM(T): V(2.1)→I(5.2)  V(2.2)→I(5.3)    — UNCHANGED
  Granfilade: I(5.2)="B"  I(5.3)="C"        — content bytes persist
```

## Why the Granfilade Doesn't Care

[FC-GRANF-ON-DELETE] establishes that DELETE is a pure V-space operation — it never calls any granfilade modification function. `dodeletevspan` → `deletevspanpm` → `deletend` all operate exclusively on the POOM (document orgl enfilade). The granfilade is append-only; [INV-NO-IADDR-REUSE] confirms that deleted I-addresses remain allocated in the granfilade tree permanently and continue to influence future allocation (via `findpreviousisagr`).

[INV-IADDR-IMMUTABILITY] makes this a system-wide guarantee: "DELETE frees the POOM bottom crums that *reference* I-addresses, but the I-addresses themselves persist in the granfilade unconditionally."

## No Reference Counting

There is no reference counting, garbage collection, or liveness predicate anywhere. [SS-POOM-MUTABILITY] establishes the architecture: the granfilade is the immutable I-address store, the POOM is the per-document mutable V→I mapping, and these layers are independent. When T's POOM entry at V(2.1) is resolved, it looks up I(5.2) in the granfilade tree — a lookup that succeeds regardless of whether D still references I(5.2).

The only way T's I-address mappings could become unresolvable is if T itself DELETEs them, or if the content were never in the granfilade to begin with. The source document's lifecycle is irrelevant to T's retrieval path.

---

## Code Exploration

Now I have a complete picture. Let me compile the full answer.

---

## Full Analysis: COPY, DELETE, and I→Content Liveness in udanax-green

### The Short Answer

There is **no reference counting and no liveness check** that could invalidate a target document's I→content mapping after a source document deletes content. The target's POOM entries resolve correctly through the granfilade after the source deletes — because DELETE only removes V→I mappings from the *source's* own POOM. It never touches the granfilade, and it never touches any other document's POOM.

---

### Step 1: How COPY Creates Shared I-Addresses

`docopy()` [do1.c:45-65]:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset) {
    return (
       specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa(vsaptr, docorgl)
    && insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)
    && insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    );
}
```

The key step is `insertpm()` [orglinks.c:75-134]:

```c
for (; sporglset; sporglset = (typesporglset)sporglset->xxxxsporgl.next) {
    unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
    movetumbler(&lstream, &crumorigin.dsas[I]);  // ← raw I-address copied in
    movetumbler(vsaptr,   &crumorigin.dsas[V]);  // ← new V-address in target
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
}
```

This inserts a new **2D bottom crum** into TARGET's POOM. The crum's structure is `type2dcbc` [enf.h:108-131]:

```c
struct struct2dcbc {
    /* ... corum header fields ... */
    typewid cwid;               // cwid.dsas[I] = I-width, cwid.dsas[V] = V-width
    typedsp cdsp;               // cdsp.dsas[I] = I-offset, cdsp.dsas[V] = V-offset
    type2dbottomcruminfo c2dinfo;  // just: tumbler homedoc
};
```

And `type2dbottomcruminfo` [wisp.h:107-109]:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

**The POOM bottom crum stores a raw I-address (a tumbler), nothing more.** There is no pointer into the granfilade, no reference count, no epoch number, no validity bit.

The I-address placed into TARGET's crum is the same I-address that SOURCE's POOM references. They share the same I-address by value — two independent POOM trees, each containing a crum that encodes the same I-tumbler range.

---

### Step 2: How DELETE Operates — and What It Doesn't Touch

`dodeletevspan()` [do1.c:158-167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr) {
    return (
       findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`deletevspanpm()` [orglinks.c:145-152]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr) {
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`docorgl` is SOURCE's own POOM, obtained from `findorgl(... docisaptr ...)`. DELETE operates exclusively on **SOURCE's POOM** in the V-dimension.

`deletend()` [edit.c:31-76] places two knife cuts at the V-span boundaries, then for each child crum in the deletion zone:

```c
case 1:  // crum fully inside deletion zone
    disown((typecorecrum*)ptr);
    subtreefree((typecorecrum*)ptr);  // ← frees the POOM tree node
    break;
case 2:  // crum is to the right; shift it left
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

**`subtreefree()` frees the POOM crum node in memory. It does not touch the granfilade.** The granfilade entry at the I-address stored in the freed crum continues to exist unchanged.

There is no call to any granfilade deletion function. Searching the entire source tree confirms there is no `deletegr` or equivalent. The granfilade is purely append-only by design.

---

### Step 3: How the Target Resolves I→Content After the Delete

When TARGET's content is retrieved, the path is:

`doretrievev()` [do1.c:338-346] → `specset2ispanset()` + `ispanset2vstuffset()` [granf1.c:57-74] → `ispan2vstuffset()` [granf2.c:286-318]:

```c
typevstuffset *ispan2vstuffset(typetask *taskptr, typegranf fullcrumptr, typeispan *ispanptr, ...) {
    movetumbler(&ispanptr->stream, &lowerbound);
    tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
    context = retrieveinspan((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
    for (temp = context; temp; temp = temp->nextcontext) {
        if (context2vstuff(taskptr, temp, ispanptr, &vstuffset)) {
            *vstuffsetptr = vstuffset;
            ...
        }
    }
}
```

`retrieveinspan()` [retrie.c:112-136] walks the **granfilade** — the global, append-only store — looking for `GRANTEXT` crums whose `WIDTH` range intersects the requested I-span. Since granfilade crums are **never deleted**, and the I-address placed into TARGET's POOM by COPY points to granfilade entries that persist forever, TARGET's retrieval succeeds identically before and after SOURCE's delete.

---

### Step 4: The `homedoc` Field — Is It a Liveness Check?

The only document-identity field in a POOM crum is `c2dinfo.homedoc`. It's checked in `crumqualifies2d()` [retrie.c:270-279]:

```c
if ((crumptr->height == 0) && infoptr && !tumblereq(&infoptr->homedoc, &(((type2dcbc*)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

This check triggers only when `infoptr != NULL`. The caller `retrieverestricted()` [retrie.c:77-84] passes `infoptr = NULL` unless `docisaptr` is non-null. And the call site `span2spanset()` [orglinks.c:435] passes `(typeisa*)NULL` for `docisaptr`:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
```

Furthermore, `findcbcinarea2d()` [retrie.c:244-251] has a DISTRIBUTION guard that calls `gerror()` if `infoptr` is ever non-null:

```c
if (infoptr)
    gerror("!NULL");
```

**The `homedoc` filter is dead code in all normal retrieval paths.** It was apparently intended for a future home-document restriction feature that was never activated.

---

### Conclusion

| Property | Finding | Evidence |
|----------|---------|----------|
| Reference counting | **None** | No refcount field in `type2dbottomcruminfo` [wisp.h:107] or `typegranbottomcruminfo` [wisp.h:100] |
| Granfilade deletion | **Never happens** | `deletend()` [edit.c:31] only modifies the POOM tree; no granfilade delete function exists |
| Cross-document POOM invalidation | **None** | `dodeletevspan()` [do1.c:158] fetches *source's* `docorgl` only; TARGET's POOM is not accessed |
| Liveness bit or epoch | **None** | `type2dcbc.c2dinfo` contains only `homedoc` [wisp.h:107] |
| `homedoc` as liveness check | **Inert** | Passed as NULL in all retrieval call sites [orglinks.c:435]; `gerror()` fired if non-null [retrie.c:249] |
| I-address persistence | **Permanent** | Granfilade is append-only; I-addresses are eternal permascroll positions |

After SOURCE deletes its content:
- SOURCE's POOM loses the V→I crum nodes for those V-addresses [`deletend()`, edit.c:59]
- TARGET's POOM retains its own crum nodes with the same I-addresses — untouched
- The granfilade entries at those I-addresses remain valid and retrievable
- TARGET's RETRIEVE resolves I→content identically, before and after the delete

This is the Xanadu permascroll invariant expressed in code: **content insertion is permanent; document deletion removes only the document's view of that content.** The design has no mechanism to violate it, because there is no mechanism connecting the two documents' POOM trees after the copy completes.

---

## Question 18 [gregory]

> When CREATENEWVERSION copies the text subspace POOM, does it create new bottom crums with identical I-displacement and I-width values (byte-for-byte copies), or does it go through `insertpm` which might split or coalesce entries differently?

### Gregory's Answer

## KB Synthesis

## Answer

CREATENEWVERSION goes through `insertpm` — it does **not** create byte-for-byte crum copies.

### The Call Chain

From [ST-VERSION] Finding 0077, the full path is:

```
docreatenewversion
  → createorglingranf          (allocates new doc address; creates empty POOM)
  → doretrievedocvspanfoo      (gets source's text V-span)
  → docopyinternal
      → specset2ispanset       (converts V-spans to I-spans via source's POOM)
      → insertpm               (inserts I-spans into version's fresh POOM)
      → insertspanf            (records DOCISPAN entries)
```

### What insertpm Does

From [ST-VCOPY] Finding 0046, `insertpm` → `insertnd` applies the extension-or-create rule:

- If the new I-span is **contiguous** with the last crum AND shares the same `homedoc` → `isanextensionnd` merges them (extends existing crum width in place)
- Otherwise → new crum created

So the version's POOM structure is determined by the I-space fragmentation of the source's content, not a structural copy of the source's tree.

### Structural Consequences

**Simple source (only text inserts):** The source has one contiguous I-span. This gets inserted via `firstinsertionnd` as one bottom crum in the version's fresh height-1 tree.

**Fragmented source (inserts interrupted by link creation):** From [ST-CRUM-BOUND] Finding 0063, CREATELINK advances the I-address allocator, breaking text contiguity. The source's content spans multiple non-contiguous I-address ranges. These become multiple crums in the version, since `isanextensionnd` fails for non-contiguous I-addresses.

**Crucially**, from [INV-MONOTONIC] Finding 0077: CREATENEWVERSION does **not** advance the content I-address allocator at all (no call to `findisatoinsertgr`). The version's POOM is populated by re-inserting the source's existing I-addresses through the standard copy path — so a subsequent INSERT into the original allocates contiguous I-addresses after the existing content, and `compare_versions` shows a single shared span pair.

### Summary

| Property | Answer |
|----------|--------|
| Path through `insertpm`? | Yes |
| Byte-for-byte crum copy? | No |
| Tree height of new version | Starts at 1, grows with `splitcrumupwards` as I-spans are inserted |
| Crum count | Determined by I-span fragmentation of source; contiguous same-homedoc spans coalesce |
| I-address allocator affected? | No (Finding 0077) |

The version's POOM is semantically equivalent to the source's (same V→I mapping) but may differ structurally — particularly in tree height and crum count — since it's built fresh via the standard insertion path rather than cloned.

---

## Code Exploration

Now I have a complete picture. Let me compile the full answer.

---

## Answer

`CREATENEWVERSION` **does go through `insertpm`**, and the I-displacement/I-width values are **passed directly from the source POOM's bottom crums** — but `insertpm` recomputes the V-widths and `insertcbcnd` may coalesce adjacent crums. Here is the full trace with citations.

---

### Step 1 — `docreatenewversion` obtains a single V-span for the source doc

`docreatenewversion` [do1.c:260–299] calls:

```c
doretrievedocvspanfoo(taskptr, isaptr, &vspan)   // do1.c:281
```

which calls `retrievedocumentpartofvspanpm` [orglinks.c:155–162]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->itemid = VSPANID;
    movetumbler(&((typecuc *)orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler(&((typecuc *)orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This reads the **root crum's** `cdsp.dsas[V]` and `cwid.dsas[V]` directly — a single V-span covering the whole document with no traversal of the bottom crums.

Then [do1.c:285–293]:

```c
vspec.docisa = *isaptr;         // source document ISA
vspec.vspanset = &vspan;        // single V-span (whole doc)
...
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

---

### Step 2 — `docopyinternal` calls `insertpm`

`docopyinternal` [do1.c:66–82]:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)  // line 74
...
insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)        // line 78
```

**Yes, it goes through `insertpm`.**

---

### Step 3 — `specset2ispanset` walks the source POOM crum by crum

`specset2ispanset` [do2.c:14–46] finds the source document's POOM and calls `vspanset2ispanset` [orglinks.c:397]:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

`permute` → `span2spanset` [orglinks.c:425] calls `retrieverestricted` to walk the source POOM, producing one context per bottom crum. Each context becomes an **ISPANID** span via `context2span` → `onitemlist`, with:
- `stream` = absolute I-address of that bottom crum
- `width` = I-width of that bottom crum

So **the ispanset has one entry per source bottom crum**, and each entry's I-displacement and I-width come directly from the source crum.

---

### Step 4 — `insertpm` processes each I-span into the new POOM

`insertpm` [orglinks.c:75–134], for each entry in the sporglset:

```c
unpacksporgl(sporglset, &lstream, &lwidth, &linfo);     // line 101

movetumbler(&lstream, &crumorigin.dsas[I]);              // I-displacement preserved as-is
movetumbler(&lwidth, &crumwidth.dsas[I]);                // I-width preserved as-is
movetumbler(vsaptr, &crumorigin.dsas[V]);                // V-address is freshly assigned

shift = tumblerlength(vsaptr) - 1;                      // lines 115–117
inc = tumblerintdiff(&lwidth, &zero);
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]); // V-width RECOMPUTED

insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // line 130

tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);          // advance V-address
```

Key observations:

1. **I-displacement** (`crumorigin.dsas[I]`) = `lstream` from `unpacksporgl` — the source crum's absolute I-address, passed through without modification.
2. **I-width** (`crumwidth.dsas[I]`) = `lwidth` from `unpacksporgl` — the source crum's I-width, passed through without modification.
3. **V-width is NOT copied** — it is recomputed from `tumblerlength(vsaptr)` (depth of the new V-address) and `tumblerintdiff(&lwidth, &zero)` (integer size of the I-width). This may produce a different tumbler shape than the source even if the integer values match.

For ISPANID items (the type produced by `specset2ispanset`), `unpacksporgl` [sporgl.c:180–184] sets `homedoc = 0`:

```c
if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
    movetumbler(&((typeispan *)sporglptr)->stream, streamptr);
    movetumbler(&((typeispan *)sporglptr)->width, widthptr);
    tumblerclear(&infoptr->homedoc);   // homedoc zeroed
}
```

---

### Step 5 — Potential coalescing in `insertcbcnd`

`insertnd` → `insertmorend` → `insertcbcnd` [insertnd.c:242] checks `isanextensionnd` [insertnd.c:301–308] before creating each new bottom crum:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

This coalesces a new insertion into an existing crum if both:
- `homedoc` values match (both zero for ISPANID — this condition is always satisfied between any two source-derived crums)
- The existing crum's reach equals the new insertion's origin in **both V and I dimensions**

Since `vsaptr` advances by exactly `crumwidth.dsas[V]` after each insertion [orglinks.c:131], consecutive crums are always V-adjacent. So **coalescing occurs whenever consecutive source crums are also I-adjacent** (pointing to consecutive permascroll locations). A document whose content was inserted in a single operation will produce a single bottom crum in the new version, not multiple crums.

---

### Summary

| Property | Behavior |
|---|---|
| Goes through `insertpm`? | **Yes** [do1.c:78, orglinks.c:75] |
| I-displacement (`cdsp.dsas[I]`) | **Preserved byte-for-byte** from source crum [orglinks.c:105] |
| I-width (`cwid.dsas[I]`) | **Preserved byte-for-byte** from source crum [orglinks.c:109] |
| V-width (`cwid.dsas[V]`) | **Recomputed** from V-address depth and I-width integer value [orglinks.c:115–117] |
| Coalescing possible? | **Yes** — I-adjacent source crums with shared homedoc (=0) are merged by `isanextensionnd` [insertnd.c:301–308] |

The new version's POOM bottom crums have identical I-displacement and I-width values to the source, but the V-widths are freshly computed, and I-adjacent source crums may be merged into single crums in the copy.

---

## Question 19 [gregory]

> The spanfilade indexes I-spans per document via DOCISPAN entries. When a single POOM entry (one contiguous I-span) is split by INSERT into two entries, does the original DOCISPAN entry remain valid for link discovery, or must new DOCISPAN entries be created for the two halves?

### Gregory's Answer

## KB Synthesis

The original DOCISPAN entry remains valid. No new entries are needed for the split halves.

**Why:**

INSERT's knife-cut mechanism splits POOM crums in **V-space only**. When a crum covering `[V_a, V_b) → [I_a, I_b)` is cut at position `V_p`, the result is two crums: `[V_a, V_p) → [I_a, I_p)` and `[V_p + width, V_b + width) → [I_p, I_b)`. The I-address range `[I_a, I_b)` is not split — it is merely accessed via two POOM crums instead of one. The underlying permascroll content is unchanged.

DOCISPAN entries index **I-address ranges → documents** [SS-DOCISPAN]. The original DOCISPAN entry, created when the content was first placed via INSERT or COPY, covered `[I_a, I_b)`. After the POOM split, that I-range still exists contiguously and still belongs to the same document. The DOCISPAN entry remains an accurate index: this document contains I-addresses `[I_a, I_b)`.

INSERT adds to the spanfilade only for **newly allocated I-addresses** — the fresh I-addresses for the inserted text get their own new DOCISPAN entry [ST-INSERT, Finding 0036]. The call chain `doinsert → inserttextingranf → docopy → insertspanf(..., DOCISPAN)` creates entries only for the newly inserted ispanset, never touching existing entries.

This is structurally guaranteed by three interlocking properties:

1. **Granfilade immutability** [INV-IADDR-IMMUTABILITY]: Existing I-addresses are never moved, renumbered, or split. The I-span the original DOCISPAN covers remains byte-for-byte identical.

2. **Spanfilade write-only** [INV-SPANF-WRITE-ONLY]: There is no `deletespanf` or `modifyspanf`. INSERT can only add entries, never modify or remove the original.

3. **Content-spanf isolation** [FC-CONTENT-SPANF-ISOLATION]: INSERT's only spanfilade effect is writing new DOCISPAN entries for newly allocated I-spans. POOM restructuring (the knife-cut, shifting, crum creation) occurs entirely in the granfilade and has no spanfilade code path.

The consequence for link discovery: `FINDDOCSCONTAINING` queries against the original I-range will still return this document correctly, even when the content has been fragmented across N POOM crums by subsequent inserts. DOCISPAN coverage is cumulative and I-space-based — it does not require POOM contiguity.

---

## Code Exploration

Now I have all the code I need to trace the full path. Let me give the definitive answer.

---

## Answer: DOCISPAN Entries After a POOM Split

**The original DOCISPAN entry remains valid. No new DOCISPAN entries are created for the split halves.** Here is the full trace.

---

### The INSERT Execution Path

`doinsert` [do1.c:87-123] runs two sequential operations:

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset));
```

`inserttextingranf` allocates new permascroll space and returns a **single ispan** covering the entire new text [granf2.c:102-107]:

```c
ispanptr->itemid = ISPANID;
movetumbler (&spanorigin, &ispanptr->stream);
tumblersub (&lsa, &spanorigin, &ispanptr->width);
*ispansetptr = ispanptr;
```

`docopy` [do1.c:45-65] then calls **both** the POOM update and the spanfilade update, passing only this new ispanset:

```c
insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // do1.c:60
&& insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // do1.c:62
```

---

### Where the POOM Gets Split

`insertpm` [orglinks.c:75-134] calls:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```
[orglinks.c:130]

`insertnd` [insertnd.c:51-61], for POOM type, calls `makegappm` **before** `doinsertnd`:

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);
    ...
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
```

`makegappm` [insertnd.c:124-172] makes two cuts at the insertion V-address:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
knives.dimension = V;
makecutsnd (fullcrumptr, &knives);
```

`makecutsnd` → `makecutsbackuptohere` → `slicecbcpm` [ndcuts.c:373-450] is invoked when a POOM leaf is `THRUME` (straddles the knife). It **physically splits** the leaf:

```c
// [ndcuts.c:438-447]
movewisp (&ptr->cwid, &newwid);
for (i = 0; i < widsize(enftype); i++) {/* I really don't understand this loop */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
    tumblerjustify (&newwid.dsas[i]);
}
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, (unsigned)widsize(enftype));
movewisp (&newwid, &ptr->cwid);
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
move2dinfo (&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);
adopt(new,RIGHTBRO,ptr);
```

The loop applies the V-cut position proportionally to **both V and I dimensions** (POOM has `widsize = 2`). The right half's displacement is set to `ptr->cdsp + ptr->cwid`, giving it the correct I-origin. Both halves get the same `homedoc` via `move2dinfo`. The original leaf is physically split into two POOM leaves, each covering half the old I-span and half the old V-span.

Then `makegappm` shifts V-offsets of all crums to the right of the cut [insertnd.c:161-164]:

```c
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified (ptr);
```

This is a pure V-space adjustment. **The I-dimension offsets (`dsas[I]`) of existing crums are not touched.**

---

### No Spanfilade Update for Existing Crums

`makegappm` contains zero calls to `insertspanf` or any spanfilade update. The only DOCISPAN writes are in `docopy` → `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` [do1.c:62], which carries only the **new** ispanset returned by `inserttextingranf`. 

`insertspanf` [spanf1.c:15-54] inserts one spanfilade entry per ispan in that new set:

```c
for (; sporglset; sporglset = ...) {
    ...
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

Existing DOCISPAN entries — covering the I-spans of content that was already in the document — receive **no write**.

---

### Why Existing DOCISPAN Entries Remain Valid

The invariant that protects DOCISPAN validity is the **immutability of permascroll I-spans**.

`finddocscontainingsp` [spanf1.c:151-188] queries the spanfilade indexed by I-span in SPANRANGE:

```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
```

When the original text [I=A, width=W] was inserted, `insertspanf` wrote one DOCISPAN entry: I-span [A, A+W) → document D. When a subsequent INSERT splits the POOM leaf that covers [A, A+W) into two halves — say covering [A, A+W₁) and [A+W₁, A+W) — this restructuring lives entirely inside the POOM. The spanfilade entry for [A, A+W) → D is untouched.

Link discovery queries the spanfilade with an I-span, finds the covering DOCISPAN entry, and returns the document address. The POOM split does not narrow or invalidate that I-span range in the spanfilade. The query still succeeds.

---

### Summary

| Event | POOM | Spanfilade (DOCISPAN) |
|---|---|---|
| Text inserted at V=X | New leaf: [V=X, I=newtext] | New entry: [I=newtext] → doc |
| Later INSERT at V=Y (within existing content) | `makegappm` splits existing leaf at V=Y; shifts right-half V-offsets | **No change** |
| Link discovery via `finddocscontainingsp` | Not consulted | Finds original DOCISPAN entry; still valid |

The original DOCISPAN entry remains valid for link discovery. The POOM split is structurally invisible to the spanfilade because: (1) DOCISPAN entries are keyed by I-span, not V-span; (2) I-spans are immutable permascroll addresses; (3) `makegappm` only adjusts V-offsets and creates no spanfilade side effects. No new DOCISPAN entries are written for the two POOM halves.

---

## Question 20 [gregory]

> Is there a mechanism that detects or prevents a POOM from containing two entries whose I-address ranges overlap — for example, if COPY transcludes content that partially overlaps with content already present in the target document at different V-positions?

### Gregory's Answer

## KB Synthesis

There is no mechanism — neither detection nor prevention — for overlapping I-address ranges in the POOM. The KB is explicit on all relevant points.

## The POOM is designed to hold overlapping I-ranges

[SS-POOM-MULTIMAP] establishes that the POOM is explicitly a **multimap**: "a single I-address can map to multiple V-positions within the same document." The search algorithm `findcbcinarea2d()` accumulates *all* matching contexts via `incontextlistnd()`, never replacing existing entries. This is the fundamental mechanism for transclusion.

[EC-SELF-TRANSCLUSION] confirms vcopy within the same document creates exactly this state — the same I-addresses at multiple V-positions — and treats it as correct behavior. [ST-VCOPY] (Finding 0039) verifies pairwise comparisons among three positions sharing one I-address all report shared content. There is no cardinality constraint on how many V-positions can reference the same I-address.

## COPY performs no overlap checking

[PRE-COPY] is explicit:

> The COPY operation performs NO duplicate checking before inserting V→I mappings into the target document's POOM. `isanextensionnd()` checks only whether the new content is contiguous with an existing crum — never whether the I-address already exists in the target. A COPY of I-addresses that already exist at some V-position in the target document is unconditionally accepted.

The only check `isanextensionnd()` performs is for *contiguity* (enabling crum extension rather than creation of a new crum). Overlap is not checked and not rejected.

## The "bijection" invariant does not guard against this

[INV-POOM-BIJECTIVITY] describes I₁ as a bijection between V-addresses and I-addresses, but the violation it documents is DELETE producing *negative V-positions* — not overlapping I-ranges. The multimap structure from [SS-POOM-MULTIMAP] makes clear that the I→V direction is deliberately not injective; the functional constraint (each V-position maps to exactly one I-address) runs V→I only.

## Summary

The scenario in the question — COPY of content that partially overlaps existing content at different V-positions — is precisely what transclusion does, and the POOM is structurally designed to accommodate it. No assertion, validation, or structural constraint exists to detect or reject it. The closest observable effect is that `ispan2vspanset` returns a set of multiple V-spans for the overlapping I-range [SS-POOM-MULTIMAP], but this is the correct query result, not an error signal.

---

## Code Exploration

All citations confirmed. Here is the full technical answer.

---

## POOM I-Address Overlap Detection in udanax-green

**Short answer: There is no such mechanism. The backend trusts callers to never produce overlapping I-spans. Overlapping inserts would silently create a corrupted POOM.**

---

### The Validation Hook That Does Nothing

`acceptablevsa()` is the designated gate in `docopy`:

```c
// do2.c:110-113
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

It is the only place in the COPY call chain where such a check could plausibly occur. It is completely vacuous — no examination of the existing POOM contents, no comparison against any span.

It is called at `do1.c:56`, between resolving the target POOM (`findorgl`) and performing the actual insertion (`insertpm`). The slot exists; the body is empty.

---

### The COPY Call Chain

`docopy` [do1.c:45-65]:

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // convert spec→I-spans
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)        // locate target POOM
&& acceptablevsa (vsaptr, docorgl)                                  // ← always TRUE
&& asserttreeisok(docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)         // insert into POOM
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // insert into spanfilade
&& asserttreeisok(docorgl)
);
```

`asserttreeisok` checks structural tree integrity (node heights, sibling pointers) — not semantic invariants about I-span ranges.

---

### `insertpm` — No I-Span Comparison

`insertpm` [orglinks.c:75-134] iterates over the incoming sporglset, builds `crumorigin`/`crumwidth` with the I-stream address on the I-axis and the V-address on the V-axis, then calls `insertnd` [orglinks.c:130]:

```c
// orglinks.c:100-131
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);     // I-axis origin
    movetumbler (&lwidth,  &crumwidth.dsas[I]);      // I-axis width
    movetumbler (vsaptr,   &crumorigin.dsas[V]);     // V-axis origin
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
}
```

There is no query of existing crums' I-axis ranges at any point here.

---

### `insertnd` → `makegappm` — V-Axis Gap Only

`makegappm` [insertnd.c:124-172] is the function that shifts existing content to make room for an insertion. The guard at lines 140–143:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

This only checks the **V-axis** — whether the V-insertion point falls inside the existing tree's V-range. It adjusts V-displacements of existing crums [lines 161-164] so that they slide right to accommodate the new entry. It does not look at the I-axis at all, because V-axis gap-making and I-axis content identity are independent concerns.

---

### `insertcbcnd` — Adjacency Check, Not Overlap Check

At the bottom level [insertnd.c:242-309], `insertcbcnd` iterates existing crums and calls `isanextensionnd`:

```c
// insertnd.c:249-258
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // widen crum
        ...
        return(...);
    }
}
// else: fall through and create a new crum
```

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

`isanextensionnd` checks: does the incoming span's **origin exactly equal** the existing crum's right boundary (`reach`)? If yes, widen that crum. If no, fall through and create a new crum.

This is a **coalescence optimization**, not an overlap check. If the incoming I-span's origin falls *within* an existing crum's I-range rather than at its right edge, `isanextensionnd` returns FALSE, a new crum is created without complaint, and the POOM now contains two crums with overlapping I-addresses.

---

### THRUME — Not an Overlap Guard

`makegappm` treats a `THRUME` return from `insertcutsectionnd` as a fatal error [insertnd.c:157-159]:

```c
case -1:      /* THRUME*/
    dump(ptr);
    gerror ("makegappm can't classify crum\n");
```

`insertcutsectionnd` returns -1 when a V-axis cut lands exactly on a crum boundary [edit.c:~221-224]. This is a V-axis structural anomaly during gap-making — not an I-axis overlap detection.

---

### Summary

| Function | File | I-overlap check? | What it actually validates |
|---|---|---|---|
| `acceptablevsa()` | do2.c:110 | **None** — always `TRUE` | Nothing |
| `insertpm()` | orglinks.c:75 | **None** | VSA not zero/negative |
| `makegappm()` | insertnd.c:124 | **None** | V-axis insertion point in range |
| `isanextensionnd()` | insertnd.c:301 | **None** | Exact adjacency at right boundary |
| `insertcbcnd()` | insertnd.c:242 | **None** | Crum not zero-width |
| `insertspanf()` | spanf1.c:15 | **None** | None |
| `asserttreeisok()` | (debug) | **None** | Tree height/structure consistency |

**No function in the COPY path reads existing I-span ranges from the POOM and compares them against the incoming I-span.**

---

### Architectural Implication

The POOM is a 2D enfilade. `insertpm` inserts crums keyed by `(V-address, I-address)` pairs. The V-axis is managed carefully — `makegappm` shifts existing crums to keep V-addresses consistent after each insert. The I-axis is treated as **read-only metadata** attached to each crum: the backend records *which* I-content lives *where* in V-space, but it never cross-checks the I-addresses of distinct crums against each other.

The invariant "no two POOM entries share any I-address" is therefore a **pre-condition that callers must enforce**, not a post-condition the backend verifies. If a COPY operation transcludes an I-span that partially overlaps content already present in the POOM at different V-positions, the backend will silently insert a new crum with that overlapping I-span. The structural tree operations will succeed; the semantic corruption will be undetected.
