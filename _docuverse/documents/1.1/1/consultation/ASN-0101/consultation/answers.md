# Consultation Answers — DELETE Operation

**Inquiry:** What is the precise effect of removing content from a position in the Vstream? What is preserved, what shifts, and what invariants must the completed operation maintain?
**Date:** 2026-03-21 09:38
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When content is removed from a position in a document, does the content itself continue to exist in the system's permanent storage, or can deletion ever destroy content?

### Nelson's Answer

# Deletion Never Destroys Content

The answer is absolute: **deletion in Xanadu removes content from a document's current arrangement but never destroys the content itself.** This is not a policy choice — it is architectural. The system is built so that destruction of content is impossible by design.

## The Two Address Spaces

The key is the separation between Istream (permanent storage) and Vstream (current arrangement). When you "delete," you are modifying the Vstream — removing a mapping — while the Istream content remains untouched.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The Istream is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

## Nelson's Explicit Diagram

The diagram on page 4/9 shows "DELETED BYTES" as a named system state with this annotation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" — not gone. "Awaiting historical backtrack" — recoverable. "May remain included in other versions" — still visible elsewhere.

## What Deletion Affects and Does Not Affect

The owner's delete operation changes the Vstream mapping only:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This means:

| Aspect | Affected by DELETE? |
|--------|---------------------|
| Vstream arrangement (current view) | **Yes** — content removed |
| Istream content (permanent storage) | **No** — bytes remain forever |
| Previous versions | **No** — still contain the content |
| Transclusions in other documents | **No** — still show it |
| Links pointing to the content | **No** — still resolve to Istream |

## Why This Must Be So

This is not cautious engineering. It flows from the fundamental rejection of destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

The storage system preserves every state so that any previous arrangement can be reconstructed:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

And modifications to content — including deletion — must never damage what others depend on:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

## The Deeper Point

Deletion that destroys content would violate nearly every guarantee the system makes: permanence of addresses, historical backtrack, link survivability, transclusion integrity, and the rights of others who have linked to or transcluded that content. If I delete a paragraph from my essay, and you had transcluded that paragraph into your commentary, your document must not break. The paragraph still exists at its Istream address; my document simply no longer includes it in its current arrangement.

This is what I meant by calling the storage system a **hyperfile** [LM 2/22] — a structure where safety and backtrack are not separate problems bolted on after the fact, but emerge naturally from the architecture itself.

---

## Question 2 [nelson]

> After content is removed, do the positions of all content following the removal point shift to close the gap, or does the document retain a placeholder at the vacated positions?

### Nelson's Answer

## Positions Shift to Close the Gap

The Vstream always forms a **dense, contiguous sequence**. When content is removed, all subsequent positions shift down to maintain this invariant. There are no placeholders or holes.

### Direct Evidence

Nelson states explicitly for INSERT:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

DELETE is the symmetric operation. The Vstream is defined as a dense virtual byte stream:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

If you have 100 bytes and delete bytes 20–30, you now have 89 bytes addressed 1 through 89. The former byte 31 is now at V-address 20. The Vstream has no concept of "empty positions."

### Why This Works

The key is the two-address-space separation:

- **Vstream** (arrangement): positions shift freely during editing. "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing." [LM 4/11]

- **Istream** (identity): content remains forever at its permanent address. "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The deleted bytes are described as: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" means they have no V-address in the current version — not that they occupy a placeholder V-address. They still exist in Istream and in previous versions.

### The Braid Metaphor

Nelson's "ongoing braid" metaphor captures this perfectly:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." [LM 2/15]

When you subtract strands, the braid closes around the gap. It doesn't leave empty space where strands used to be.

### Summary

| Space | Effect of DELETE |
|-------|-----------------|
| **Vstream** | Gap closes; subsequent positions shift down; sequence remains dense 1..N |
| **Istream** | Nothing changes; bytes remain at permanent addresses forever |
| **Other versions** | Unaffected; each version has its own V-arrangement |
| **Links** | Survive, because they point to I-addresses, not V-positions |

NEED_RAW: [4/66] — to confirm whether Nelson's DELETEVSPAN description explicitly mentions position shifting, or whether the gap-closing property is only implicit from the dense-sequence invariant and the INSERT symmetry.

---

## Question 3 [nelson]

> If the same content appears in multiple documents through sharing, does removing it from one document affect its presence or position in any other document?

### Nelson's Answer

# No. Removing content from one document has absolutely no effect on any other document.

This is one of the most fundamental guarantees of the architecture, and it follows directly from the separation of Istream and Vstream.

## The Mechanism

When content appears in multiple documents through transclusion, each document has its own **Vstream** (arrangement) that maps to shared **Istream** (permanent storage). "Deleting" content from a document removes only that document's Vstream mapping. The Istream content is untouched.

Nelson states this explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Each document's Vstream is independent. Editing one document's arrangement — inserting, deleting, rearranging — changes only that document's V-to-I mapping. No other document's mapping is affected.

## Why This Works

The key is that transclusion is **reference to Istream**, not reference to another document's Vstream. When Document B transcludes content from Document A, Document B's Vstream points to the same Istream addresses as Document A — but it does not point *through* Document A. The relationship is:

```
Document A's Vstream ──→ Istream address X
Document B's Vstream ──→ Istream address X  (same content, independent mapping)
```

If Document A deletes that content from its arrangement, Document A's Vstream no longer references address X. But Document B's Vstream still does. The Istream content at address X is permanent and unchanged.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The bytes remain at their home location regardless of what any document does with its own arrangement.

## The Broader Principle

This is a direct consequence of Nelson's rejection of destructive replacement:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And the append-only storage model:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content in Istream is never removed. DELETE is a Vstream-only operation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## What About Position?

Positions in other documents are also unaffected. Each document's Vstream addresses are dense and independent — V-address 1 is always the first byte of *that* document's current arrangement. Editing Document A changes Document A's V-addresses but has no effect on Document B's V-addresses, even if they share Istream content.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

## Summary

The Istream/Vstream separation guarantees complete isolation between documents. Each document is an independent view over permanent content. No operation on one document can affect any other document's content, arrangement, or addresses.

---

## Question 4 [nelson]

> After removal, can a reader still discover that specific content once occupied that position in that document, or does the document appear as though the content was never there?

### Nelson's Answer

## The Current Version Shows No Trace; History Reveals Everything

The document appears as though the content was never there — **in the current version**. But the system provides full means to discover what was removed.

### The Vstream Closes the Gap

After DELETE, the Vstream re-densifies. V-addresses are always contiguous:

> "V-address 1 is always the first byte of the document right now. There are no gaps — if you have 100 bytes, you have addresses 1 through 100. DELETE removes addresses (closing the gap)."

If you delete bytes at V-positions 50–60, what was at 61 becomes 50. The current reader sees seamless text with no scar, no placeholder, no marker of absence.

### But Deleted Bytes Are Not Destroyed

The diagram on page 4/9 explicitly names "DELETED BYTES" as a system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" is the key phrase. The bytes exist in Istream — permanently, immutably — but the current Vstream arrangement no longer references them. The content has been removed from the *view*, not from *existence*.

### Three Paths to Discovery

A reader can discover the removal through:

**1. Historical backtrack.** Every previous version persists. A reader can request the document at any prior state:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

**2. Version comparison (SHOWRELATIONOF2VERSIONS).** This operation returns "a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. By comparing the pre-deletion version with the post-deletion version, the system reveals exactly which spans are present in the old version but absent in the new — exposing the deletion precisely.

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

**3. Transclusion survival.** If any other document transcludes the deleted content, that content remains visible there. Furthermore, FINDDOCSCONTAINING can locate all documents that include the same Istream bytes, even after those bytes are removed from the original document's current arrangement:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### The Design Intent

This is deliberate. Nelson wanted the current view to be clean — a seamless document, not one littered with deletion markers. But he equally wanted nothing to be truly lost:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Xanadu rejects destructive replacement. DELETE modifies the arrangement (Vstream), never the content (Istream). The current version is authoritative for "what the document says now." The full history is authoritative for "what the document has ever said."

### Summary

| What the reader sees | Deletion visible? |
|---|---|
| Current version (RETRIEVEV) | **No** — seamless, gap closed |
| Previous version (historical backtrack) | **Yes** — content still present |
| Version comparison (SHOWRELATIONOF2VERSIONS) | **Yes** — missing spans identified |
| Other documents transcluding same bytes | **Yes** — content still appears |
| Istream (permanent storage) | **Yes** — bytes exist forever |

The document appears as though the content was never there — but only to a reader who looks at nothing but the present.

---

## Question 5 [nelson]

> Does the original creator's attribution to the removed content persist after removal, and can the creator still be identified as its source?

### Nelson's Answer

# Yes — Attribution Survives Removal Absolutely

In Xanadu, "deletion" never touches the layer where attribution lives. The creator can always be identified. Here's why:

## DELETE Only Affects Vstream

DELETE removes content from the document's **current arrangement** (Vstream) but does not touch **permanent storage** (Istream):

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The content itself — and its permanent address — remain intact.

## Attribution Is Structural, Not Metadata

Every byte in Xanadu has a permanent Istream address with the form:

```
Node.0.User.0.Document.0.Element
```

The **User** field and **Document** field directly encode who created the content and in which document. This is not a tag that can be stripped — it is the address itself. To fetch the content, the system must reference this address:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

## The Chain After Deletion

After content is "deleted" from a document:

| What happens | Attribution affected? |
|---|---|
| Content removed from Vstream (current view) | No — I-address unchanged |
| Content remains in Istream permanently | No — still at original address |
| Previous versions still contain the content | No — same I-addresses |
| Other documents that transclude it still show it | No — they reference the same I-address |
| Links to the content's I-address still resolve | No — Istream is append-only |

## The Append-Only Foundation

The entire storage model prevents attribution loss:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is never overwritten, never truly removed. The permascroll (Nelson's "hyperfile") grows monotonically. Since the I-address encodes provenance and the content at that address is permanent, **there is no operation in Xanadu that can sever attribution**.

## Summary

The original creator's attribution persists after removal because:

1. **Deletion is a Vstream operation** — it changes the view, not the content
2. **I-addresses are permanent** — they encode the creator structurally
3. **Storage is append-only** — nothing is ever destroyed
4. **Attribution is the address** — it cannot be stripped without destroying the addressing system itself

This is by design. Nelson built Xanadu so that the connection between content and creator is inherent in the architecture, not dependent on any metadata that could be lost through editing operations.

---

## Question 6 [nelson]

> Must the system preserve the exact boundaries of what was removed — that is, must it remember precisely which content occupied which positions before the removal?

### Nelson's Answer

## Yes — the system must preserve exact deletion boundaries

This follows from three interlocking requirements Nelson specifies.

### 1. Historical backtrack demands full reconstruction

Nelson's storage model is append-only. Changes are recorded, not applied destructively:

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

The guarantee is that "when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15]. To reconstruct the pre-deletion state, the system must know exactly which Istream content occupied which Vstream positions before the removal.

### 2. Deleted bytes are explicitly tracked, not forgotten

The diagram on 4/9 shows "DELETED BYTES" as a distinct system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Awaiting historical backtrack functions" means these bytes and their former positions are known to the system — they are pending reconstruction, not discarded. The system retains the V→I mapping from the version before deletion.

### 3. Version comparison requires positional correspondence

SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. For this to work between pre-deletion and post-deletion versions, the system must know the exact Vstream mapping of both. Without the deletion boundaries, it cannot compute which spans in the old version correspond to which spans in the new one.

Nelson motivates this:

> "a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

### The mechanism

The DELETEVSPAN operation takes a span as input: "This removes the given span from the given document" [LM 4/66]. The span itself defines exact boundaries (a Vstream start and width). The operation modifies the Vstream mapping — removing those positions — but the previous mapping persists as a prior version. Since each version is a complete V→I mapping, the exact boundaries of what was removed are preserved structurally in the version that preceded the deletion.

The Istream content, of course, is untouched:

> "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Summary

The system must preserve exact deletion boundaries because:
- **Each version is a complete V→I mapping**, and the pre-deletion version persists
- **Historical backtrack** requires reconstructing any prior state, which requires knowing what was where
- **Version comparison** requires computing positional correspondence, which requires both mappings
- **Deleted bytes** are explicitly in a known state "awaiting historical backtrack functions," not forgotten

The boundaries are not stored as separate "deletion records" — they are implicit in the difference between the pre-deletion and post-deletion Vstream mappings, both of which the system retains.

---

## Question 7 [nelson]

> Does the document retain the same identity after a removal, or does removing content produce a distinct document with its own identity?

### Nelson's Answer

## The document retains its identity after removal.

DELETE is an in-place modification of the document's Vstream arrangement, not a creation of a new entity. The document's tumbler address, ownership, and history persist through the operation.

### Evidence from the FEBE operations

DELETEVSPAN operates *on* a document — it does not produce a new one:

> "This removes the given span from the given document." (4/66)

Contrast this with CREATENEWVERSION, which explicitly creates a *new* document with a *new* identity:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

DELETE has no "returns the id of the new document" — it modifies the existing one.

### The "ongoing braid" model

Nelson's document model is fundamentally one of identity-preserving evolution:

> "A document is really an evolving ONGOING BRAID." (2/14)

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." (2/15)

Editing — including removal — is re-twisting the braid, not cutting it and starting a new one. The document accumulates history; each state is recoverable:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)

### What DELETE actually affects

From the system state diagram on 4/9:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

And explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

DELETE removes bytes from the **Vstream** (current arrangement) but leaves **Istream** (permanent storage) untouched. The document's identity is rooted in its tumbler address, which is permanent. The Vstream is merely the document's current face — one cross-section of the evolving braid.

### Vstream changes don't alter document identity

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

Editorial operations — INSERT, DELETE, REARRANGE — alter V-addresses freely. The document absorbs these changes as part of its ongoing evolution. Links survive because they point to I-addresses, not V-addresses. The document's identity is the container for this evolution, not any particular arrangement within it.

### Summary

In Nelson's model, a document is not a snapshot but a *trajectory*. Removal changes the trajectory's current state without altering which trajectory it is. To get a distinct identity, you must explicitly invoke CREATENEWVERSION. All other editing operations — including DELETE — evolve the document in place.

---

## Question 8 [nelson]

> If permissions were granted on a region of a document that overlaps with the removed content, what must happen to those permissions after the removal?

### Nelson's Answer

## Nelson Does Not Specify Per-Region Permissions

This question presupposes a mechanism that does not exist in Literary Machines. My access model operates at the **document level**, not the region level:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

There are no permissions granted on regions of documents. A document is either private (owner and designees) or published (everyone). That is the entire access model.

## What DOES Happen to Structures on Removed Content

DELETE removes content from the **Vstream** (current arrangement) but not from **Istream** (permanent storage):

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So after deletion:

- **Links** to the removed region **survive** — they point to Istream addresses, not Vstream positions: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]
- **Transclusions** in other documents are **unaffected** — they reference Istream content directly
- **Previous versions** still contain the content
- The content's **permanent I-address** and origin traceability are unchanged

The document-level access status (private or published) does not change because of a Vstream deletion. A published document remains published. Content removed from the current view remains accessible through historical backtrack and through any other documents that transclude it.

If your question arises from an implementation that introduces sub-document permissions (which would go beyond what I specified), that is an implementation design decision, not something Literary Machines addresses. NEED_RAW: [4/9, 2/42-2/43] if you want to verify against the original pages.

---

## Question 9 [nelson]

> Can a removal be partial — removing content from the middle of a single stored unit — or must removal always operate on whole units as they were originally contributed?

### Nelson's Answer

## Removal Is Partial — Down to the Individual Byte

Removal operates on **arbitrary V-spans**, not on "units as originally contributed." There is no concept of a "stored unit" that must be removed whole. The granularity is the individual byte.

### The Operation

DELETEVSPAN takes a span argument — any contiguous range of positions in the document's virtual byte stream:

> "This removes the given span from the given document." [LM 4/66]

The span can be as small as one byte or as large as the entire document. It bears no relation to how the content was originally inserted.

### Why This Works

The Istream/Vstream separation makes this clean. Content lives permanently at I-addresses; the document's arrangement is a V-to-I mapping. DELETE modifies the mapping, not the content:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

"Regardless of their native origin" is the key phrase. A V-span can cross boundaries between different insertions, between native and transcluded content, between content from different sources. The Vstream doesn't know or care about contribution boundaries.

### What Happens to the Removed Bytes

They remain in Istream. The diagram on 4/9 shows:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Concrete Example

If you INSERT "Hello World" (11 bytes), those 11 bytes get 11 I-addresses and 11 V-addresses (say, positions 1–11). You can then DELETEVSPAN on positions 6–6 (just the space), or 6–10 ("World"), or 4–8 ("lo Wo") — any contiguous range. The deleted bytes vanish from the current arrangement but remain permanently in Istream, recoverable through historical backtrack or still visible in other versions and transclusions.

Similarly, REARRANGE operates on arbitrary regions defined by cut points, not by original contribution boundaries:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3." [LM 4/67]

### Summary

All editing operations — INSERT, DELETEVSPAN, REARRANGE, COPY — work at **byte-level granularity** on the **Vstream**. There is no notion of an indivisible "contribution unit." The system treats the document as a stream of individually addressable bytes that can be sliced at any point.

---

## Question 10 [nelson]

> After removal, must the system guarantee that any prior state of the document — including the removed content in its original position — remains recoverable and citable?

### Nelson's Answer

## Yes — both recovery and citability are guaranteed

Nelson's design answers this unambiguously across three reinforcing layers: Istream permanence, historical backtrack, and link survivability.

### 1. Removed content remains in permanent storage

DELETE is a Vstream operation only. It removes content from the document's current arrangement but leaves the Istream untouched.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The phrase "not currently addressable" is precise — the bytes are not addressable *in this version's Vstream*, but they remain at their permanent I-address forever. The append-only storage model makes this structural:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### 2. Prior states — including position — are recoverable

Historical backtrack explicitly reconstructs the full arrangement, not just the raw bytes:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

This means the *position* of removed content within the prior version's Vstream is recoverable — you get back the arrangement as it was, not just a bag of bytes. Nelson calls this "pounce":

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

And there is no privileged "current" version:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

### 3. Removed content remains citable

Citability follows from the permanence of I-addresses. Every byte has a permanent tumbler address that never changes:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Links to deleted content survive because they attach to I-addresses (bytes), not V-addresses (positions):

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Since DELETE never touches Istream, the bytes to which links are "strapped" remain. The links continue to resolve.

Furthermore, version-spanning links mean a citation to the pre-deletion version reaches through to corresponding content:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

### 4. The principle behind the guarantee

Nelson frames this as the core design commitment:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

Xanadu exists precisely to abolish destructive editing. The guarantee is not a feature bolted onto the system — it is the reason the system has two address spaces (Istream and Vstream) in the first place. Separation of permanent content from ephemeral arrangement is the architectural decision that makes recovery and citability automatic rather than optional.

### Summary

| Question | Answer | Mechanism |
|----------|--------|-----------|
| Must removed content be recoverable? | Yes | Istream is append-only; bytes never leave |
| Must prior arrangement be recoverable? | Yes | Historical backtrack reconstructs any version |
| Must removed content remain citable? | Yes | I-addresses are permanent; links survive |
| Is this a guarantee or a feature? | Guarantee | It is the architectural reason for I/V separation |

---

## Question 11 [gregory]

> When `deletend` constructs knives from the two cut points of a V-span, does it always produce exactly two knives, and what happens when a cut point falls exactly on an existing POOM crum boundary versus interior to a crum (`whereoncrum == THRUME`)?

### Gregory's Answer

## KB Synthesis

## DELETE Knife Construction

### Two knives, always

DELETE always constructs exactly two knife blades: `blade[0] = origin` (start of deletion) and `blade[1] = origin + width` (end of deletion). Unlike INSERT, which uses `findaddressofsecondcutforinsert()` to place the second blade at the next subspace boundary, DELETE's knife blades are simply the two endpoints of the deletion span — no subspace boundary computation occurs. [FC-SUBSPACE], [INT-DELETE-SUBSPACE-ASYMMETRY]

### Phase 1: cutting at each blade

For each of the two blade positions, `makecutsbackuptohere()` (`ndcuts.c:77-90`) consults `whereoncrum()` to classify the blade's position relative to each bottom crum:

**When the blade falls in the interior (THRUME):** `grasp < blade < reach`. `slicecbcpm` is called. This splits the crum at the local offset `blade - grasp`, producing two fragments with widths `blade - grasp` and `reach - blade` respectively. Both are strictly positive (the THRUME precondition guarantees it), so no zero-width crums are created. [PRE-DELETE], [INV-NO-ZERO-WIDTH-CRUM]

**When the blade aligns exactly with a crum boundary (ONMYLEFTBORDER or ONMYRIGHTBORDER):** `slicecbcpm` is NOT called. The crum is left structurally intact and passed to Phase 2 for whole-crum classification. This is a structural optimization: boundary alignment means no split is geometrically necessary. [PRE-DELETE], [INV-NO-ZERO-WIDTH-CRUM]

**When the blade falls outside the crum (TOMYLEFT or TOMYRIGHT):** no cutting, the crum is simply classified in Phase 2.

### Phase 2: classify and act

After Phase 1 cutting, each bottom crum is classified:
- **Before the deletion range (TOMYLEFT of `blade[0]`):** untouched — no displacement, no removal
- **Fully within `[blade[0], blade[1])`:** Case 1 — `disown` + `subtreefree` (crum freed from tree)
- **After `blade[1]` (Case 2):** V-displacement shifted by subtracting the deletion width via `tumblersub`

The shift in Case 2 uses `strongsub` under the hood, which has an exponent guard: if the deletion width's exponent is smaller than the crum's displacement exponent, the subtraction is a no-op. This is the mechanism by which DELETE in the text subspace (`1.x`) incidentally leaves link crums at `2.x` unshifted — not by deliberate design but by arithmetic. [FC-SUBSPACE], [ST-DELETE], [INT-DELETE-SUBSPACE-ASYMMETRY]

### Concrete example

```
Crum A: [1.1, 1.4)   Crum B: [1.4, 1.7)   Crum C: [1.7, 1.10)

DELETE [1.1, 1.7):  blade[0]=1.1, blade[1]=1.7

Phase 1, blade[0]=1.1:
  Crum A: whereoncrum(1.1, A) → ONMYLEFTBORDER  → no slicecbcpm
Phase 1, blade[1]=1.7:
  Crum C: whereoncrum(1.7, C) → ONMYLEFTBORDER  → no slicecbcpm

Phase 2:
  Crum A: fully within [1.1, 1.7) → disown + subtreefree
  Crum B: fully within [1.1, 1.7) → disown + subtreefree
  Crum C: after 1.7 → shift backward by 0.6

DELETE [1.2, 1.5):  blade[0]=1.2, blade[1]=1.5

Phase 1, blade[0]=1.2:
  Crum A [1.1,1.4): whereoncrum(1.2, A) → THRUME → slicecbcpm
  Splits A into [1.1,1.2) and [1.2,1.4)
Phase 1, blade[1]=1.5:
  Crum B [1.4,1.7): whereoncrum(1.5, B) → THRUME → slicecbcpm
  Splits B into [1.4,1.5) and [1.5,1.7)

Phase 2:
  [1.1,1.2): before blade[0] → unchanged
  [1.2,1.4): within [1.2,1.5) → remove
  [1.4,1.5): within [1.2,1.5) → remove
  [1.5,1.7): after blade[1]  → shift backward by 0.3
  Crum C [1.7,1.10): after blade[1] → shift backward by 0.3
```

---

## Code Exploration

I now have everything. Here is the full answer.

---

## `deletend`: Knife Count and Cut-Point Boundary Semantics

### 1. Does `deletend` always produce exactly two knives?

**Yes. Unconditionally.**

`edit.c:40–43`:
```c
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
knives.nblades = 2;
knives.dimension = index;
```

`blades[0]` is set to `origin` (the left cut: start of the V-span to delete). `blades[1]` is set to `origin + width` (the right cut: end of the span). `nblades = 2` is hardcoded. There is no conditional path that produces 1 knife, 3 knives, or 4 knives from `deletend`. (Contrast with `rearrangend` at `edit.c:78`, which uses a `cutseq` of variable length and can fill up to `MAXCUTS = 4` knives [`common.h:108`].)

`newfindintersectionnd` at `ndinters.c:38–42` is a stub that simply sets `*ptrptr = fullcrumptr` and zeroes the offset — it does not descend to find a common ancestor. So `deletend` iterates over the direct children of the full root.

---

### 2. The two phases where `whereoncrum` matters

The cut points are used in two distinct phases: **cut-making** (`makecutsnd`) and **section classification** (`deletecutsectionnd`). THRUME means strictly different things in each.

#### Constants (`common.h:86–90`):
```c
#define TOMYLEFT       -2    // address < crum.left
#define ONMYLEFTBORDER -1    // address == crum.left
#define THRUME          0    // crum.left < address < crum.right (strictly interior)
#define ONMYRIGHTBORDER 1    // address == crum.right
#define TOMYRIGHT       2    // address > crum.right
```

`whereoncrum` for POOM/SPAN (`retrie.c:356–373`):
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);  // left = abs. crum start
cmp = tumblercmp(address, &left);
if (cmp == LESS)  return(TOMYLEFT);
if (cmp == EQUAL) return(ONMYLEFTBORDER);
tumbleradd(&left, &ptr->cwid.dsas[index], &right);                // right = left + crum width
cmp = tumblercmp(address, &right);
if (cmp == LESS)  return(THRUME);
if (cmp == EQUAL) return(ONMYRIGHTBORDER);
else              return(TOMYRIGHT);
```

---

### Phase 1: `makecutsnd` — Splitting crums at cut points

`makecutsnd` calls `makecutsdownnd` → `makecutsbackuptohere`. At leaf crums (`height == 0`), `ndcuts.c:77–91`:

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum(..., &knives->blades[i], ...) == THRUME) {
            new = createcrum(...);
            slicecbcpm(ptr, offset, new, &knives->blades[i], ...);
            ivemodified(ptr); ivemodified(new);
            setwisp(ptr);
        }
    }
    return(0);
}
```

**`whereoncrum == THRUME` (cut falls strictly inside the crum):**
`slicecbcpm` is invoked (`ndcuts.c:373–450`). It:
1. Guards that the cut is truly THRUME: `ndcuts.c:383–388` — `gerror` if not.
2. Computes `localcut = cut - grasp` (cut's position relative to crum start): `ndcuts.c:396`.
3. Validates `localcut.exp == ptr->cwid.dsas[index].exp` (same tumbler level) and `is1story(&localcut)`.
4. Derives `newwid` = the left-piece width by copying the crum's wid and setting the mantissa to `localcut.mantissa[0]`: `ndcuts.c:438–442`.
5. Computes right-piece width: `new->cwid = ptr->cwid - newwid` via `locksubtract`: `ndcuts.c:444`.
6. Shrinks original crum: `ptr->cwid = newwid`: `ndcuts.c:445`.
7. Sets right-piece start: `new->cdsp = ptr->cdsp + ptr->cwid` (after the shrink): `ndcuts.c:446`.
8. Copies 2D info (home document) to the new crum: `ndcuts.c:447`.
9. Inserts `new` as `RIGHTBRO` of `ptr`: `ndcuts.c:448`.

After `slicecbcpm`, the cut position is exactly `ONMYRIGHTBORDER` of the left piece and `ONMYLEFTBORDER` of the right piece. The crum interior has been subdivided at the cut.

**`whereoncrum != THRUME` (cut on or outside the crum boundary):**
The `if` at `ndcuts.c:79` is not entered. Nothing is done for that knife on that crum. The cut already aligns with an existing boundary (or is completely outside the crum's span), so no split is needed or warranted.

**The post-condition of `makecutsnd`:**
After all knife positions have been processed, every knife sits exactly at a crum boundary. No crum straddles any knife. This is the invariant required by the deletion phase.

---

### Phase 2: `deletecutsectionnd` — Classifying each crum for deletion

`edit.c:235–248`:
```c
INT deletecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
  INT i, cmp;
    for (i = knives->nblades-1; i >= 0; --i) {
           cmp = whereoncrum(ptr, offset, &knives->blades[i], ...);
           if (cmp == THRUME)             return (-1);
           else if (cmp <= ONMYLEFTBORDER) return (i+1);
    }
    return (0);
}
```

With `nblades = 2` and `blades[0] = origin < blades[1] = origin+width`, the loop scans right-to-left:

**i = 1 (right knife, `origin+width`):**

| `whereoncrum` result | Meaning | Action |
|---|---|---|
| `THRUME` | knife is strictly inside crum | return -1 — fatal: `makecutsnd` missed a cut |
| `TOMYLEFT` or `ONMYLEFTBORDER` | crum starts at or after `origin+width` | return 2 — crum is entirely RIGHT of deleted region |
| `ONMYRIGHTBORDER` or `TOMYRIGHT` | crum ends at or before `origin+width` | continue to i=0 |

**i = 0 (left knife, `origin`):**
Only reached when knife[1] is `ONMYRIGHTBORDER` or `TOMYRIGHT` (crum ends at or before the right cut).

| `whereoncrum` result | Meaning | Action |
|---|---|---|
| `THRUME` | knife is strictly inside crum | return -1 — fatal |
| `TOMYLEFT` or `ONMYLEFTBORDER` | crum starts at or after `origin` | return 1 — crum is entirely WITHIN deleted region |
| `ONMYRIGHTBORDER` or `TOMYRIGHT` | crum ends at or before `origin` | continue; fall through to return 0 |

**return 0:** Crum is entirely LEFT of the deleted region (both knives are at or past its right border).

Back in `deletend` (`edit.c:49–73`), these return values map to:

| Return | Case | Action |
|---|---|---|
| -1 | THRUME: unexpected cut interior | `gerror("deletend can't classify crum\n")` — program halt |
| 0 | Crum fully left of deleted span | `break` — untouched |
| 1 | Crum fully within deleted span | `disown(ptr); subtreefree(ptr)` — crum removed from tree |
| 2 | Crum fully right of deleted span | `tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index])` — displacement shifted left by `width` |

---

### Summary

`deletend` always produces **exactly two knives**, hardcoded at `edit.c:42`. The design is a two-phase protocol:

1. **`makecutsnd` guarantees no crum straddles a knife.** For any knife that falls THRUME (strictly interior to a leaf crum), `slicecbcpm` physically splits that crum into two at the cut point, consuming THRUME and creating two boundary-aligned pieces. For knives that already fall on a crum boundary (`ONMYLEFTBORDER` or `ONMYRIGHTBORDER`), nothing is done — the alignment is already correct.

2. **`deletecutsectionnd` then classifies crums assuming the THRUME invariant holds.** If THRUME appears here, it is a bug — `makecutsnd` failed to split something it should have — and the code calls `gerror` to halt. Under normal operation, THRUME never occurs in this phase: every crum either sits left-of, within, or right-of the two-knife window, and receives the corresponding treatment (untouched, deleted, or displaced).

---

## Question 12 [gregory]

> After DELETE shifts surviving POOM entries left via `tumblersub`, is there any reconciliation pass that detects when two formerly non-adjacent crums become I-address-contiguous and merges them, or do they remain as separate POOM entries permanently?

### Gregory's Answer

## KB Synthesis

No reconciliation pass exists. After DELETE shifts surviving POOM entries left, they remain as permanently separate crums.

Here is what the KB tells us about each stage of DELETE's aftermath:

**Phase 1 & 2 (cutting and classification)** [PRE-DELETE, ST-DELETE]: `deletend()` slices crums that straddle the deletion boundary, removes crums entirely within the deleted range, and shifts crums after the deletion via `tumblersub`. At no point does this pass check I-address relationships between survivor crums.

**Post-deletion rebalancing** [ST-REBALANCE-2D, INV-ENFILADE-OCCUPANCY]: After `setwispupwards` recalculates widths, `recombinend` rebalances the tree. Its merge criterion in `ishouldbother` is purely occupancy-based: `dest->numberofsons + src->numberofsons <= max_children`. It reorganizes which parent nodes group which content crums — it never examines or exploits I-address contiguity between leaf-level mappings.

**Why contiguity can't emerge anyway**: Even if two crums become V-adjacent after deletion (crum A's reach == crum B's grasp), they are I-address non-adjacent. The deleted content occupied I-addresses between them, and those I-addresses remain allocated in the append-only granfilade [FC-GRANF-ON-DELETE, INV-NO-IADDR-REUSE]. The gap in I-address space persists. So `isanextensionnd()`'s criterion — same `homedoc` AND reach equals origin in I-space [ST-INSERT, Finding 0062] — would fail even if it were invoked.

**The extension check is INSERT-only**: `isanextensionnd()` is called only from `insertnd()` during content insertion [ST-INSERT]. DELETE does not invoke this path. There is no equivalent "merge if now contiguous" scan in the DELETE or rebalancing code paths.

**Structural consequence**: This is consistent with [INV-VSPAN-CONSOLIDATION] — the single-span consolidation guarantee holds because `isanextensionnd()` catches contiguity at insertion time. DELETE can fragment what was once contiguous, and that fragmentation is permanent. The crum count after a sequence of insertions and deletions follows the bound `c ≤ 1 + 2C + ...` from [ST-CRUM-BOUND, Finding 0062], where each interior insertion costs +2 crums that deletion never reclaims through merging.

**Bottom line**: Formerly non-adjacent crums that become V-adjacent after DELETE shifting remain as separate POOM entries permanently. The rebalancing that does occur operates on tree occupancy (B-tree node consolidation [ST-REBALANCE-2D]), not on content-level crum consolidation.

---

## Code Exploration

Now I have the complete picture. Here is the full answer.

---

## Answer: No Reconciliation Pass Exists After DELETE

### The Complete Delete Execution Path

**Entry point** — `dodeletevspan` [do1.c:158–167]:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

**`deletevspanpm`** [orglinks.c:145–152] — a thin wrapper with no post-processing:
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
No merge opportunity here. Just `deletend` + a bert log entry.

**`deletend`** [edit.c:31–76] — where the actual work happens:

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    makecutsnd (fullcrumptr, &knives);                    // [edit.c:44] cut at origin and origin+width
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);  // [edit.c:45]
    ...
    for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {  // [edit.c:47]
        switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 1:
            disown ((typecorecrum*)ptr);       // [edit.c:59] fully deleted crum: remove
            subtreefree ((typecorecrum*)ptr);  // [edit.c:60]
            break;
          case 2:
            tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
            // [edit.c:63] surviving crum after the hole: shift I-address left
            break;
        }
    }
    setwispupwards (father,1);  // [edit.c:74] update wid counts upward
    recombine (father);          // [edit.c:75] ← the only post-delete pass
}
```

Case 2 is the `tumblersub` shift. After it, `recombine(father)` is called. This is the **sole post-delete operation**.

---

### What `recombine` Actually Does

**`recombine`** [recombine.c:22–34] dispatches to `recombinend` for POOM:
```c
int recombine(typecuc *father)
{
    switch (father->cenftype) {
      case POOM:
        recombinend (father);   // [recombine.c:32]
    }
}
```

**`recombinend`** [recombine.c:104–131]:
```c
int recombinend(typecuc *father)
{
    if (father->height < 2  || !father->modified)
        return(0);           // [recombine.c:112] guard: interior nodes only, height ≥ 2

    for (ptr = getleftson (father); ptr; ptr=(typecorecrum *)getrightbro (ptr)){
        recombinend (ptr);   // [recombine.c:114–116] recurse into children
    }

    getorderedsons (father, sons);   // [recombine.c:118] sort siblings by diagonal magnitude
    n = father->numberofsons;
    for (i = 0; i < n-1; i++) {
        for (j = i+1; sons[i] && j < n; j++) {
            if(i != j && sons[j] && ishouldbother(sons[i],sons[j])){
                takeovernephewsnd (&sons[i], &sons[j]);  // [recombine.c:123] balance siblings
            }
        }
    }
    if (father->isapex)
        levelpull (father);   // [recombine.c:130]
}
```

The decision criterion is `ishouldbother` [recombine.c:150–163]:
```c
bool ishouldbother(typecuc *dest, typecuc *src)
{
    ...
    return (dest->numberofsons + src->numberofsons
            <= (dest->height>1 ? MAXUCINLOAF : MAX2DBCINLOAF)
            && randomness(.3));   // [recombine.c:162]
}
```

**This is a pure tree-balance criterion**: "will the combined child count fit in one loaf node?" There is no check for I-address adjacency between the bottom crums those interior nodes contain.

`eatbrossubtreend` [recombine.c:205–233] and `takenephewnd` [recombine.c:235–257] merge or relocate children of sibling interior nodes (moving height-1 subtrees around), adjusting DSPs accordingly via `makeroomonleftnd` and `dspadd`/`dspsub`. Neither inspects whether the **bottom crums** (height-0 leaves) in those subtrees happen to be I-address-adjacent.

`comparecrumsdiagonally` [recombine.c:313–320] — used by `getorderedsons` for sort order — is also not an adjacency test:
```c
INT comparecrumsdiagonally(typecorecrum *a, typecorecrum *b)
{
    tumbleradd (&a->cdsp.dsas[0], &a->cdsp.dsas[1], &amagnitude);  // sum of I+V
    tumbleradd (&b->cdsp.dsas[0], &b->cdsp.dsas[1], &bmagnitude);
    return (tumblercmp (&amagnitude, &bmagnitude));
}
```

It sorts by `I+V` magnitude, not I-address end-meets-start.

---

### Where I-Address Contiguity IS Checked (Only on Insert)

The only place that checks whether two POOM crums are I-address-adjacent is `isanextensionnd` [insertnd.c:301–309], called exclusively inside `insertcbcnd` [insertnd.c:242–275]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);                            // [insertnd.c:305] same home doc?
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
    // [insertnd.c:308] does this crum's right edge equal the new insertion's origin?
}
```

If it returns `TRUE`, `insertcbcnd` simply widens the existing crum's width instead of allocating a new one [insertnd.c:251]:
```c
if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
    dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // [insertnd.c:251]
    ...
    return(FALSE);
}
```

This path is only reachable via `insertnd` → `insertmorend` → `insertcbcnd`. There is no equivalent call chain triggered by `deletend`.

---

### Conclusion

**Yes, two formerly non-adjacent POOM crums that become I-address-contiguous after DELETE remain as separate entries permanently** (unless a subsequent INSERT happens to land exactly at the boundary, in which case `isanextensionnd` would merge the new insertion with one of them — but that would not merge the two survivors with each other).

The call `recombine(father)` at [edit.c:75] is a **B-tree balance pass**, not a semantic merge. It operates at interior-node level (height ≥ 2 guard at [recombine.c:112]), relocates subtrees to balance loaf occupancy, and has no awareness of I-address adjacency between bottom crums. The only I-address contiguity check in the entire codebase — `isanextensionnd` at [insertnd.c:301–309] — is insert-path-only and never fires during or after delete.

---

## Question 13 [gregory]

> When a deletion span partially overlaps a POOM crum (e.g., deleting the last 3 bytes of a 5-byte crum), does `slicecbcpm` produce a single shortened crum with adjusted V-width and I-width, or does it disown the original and create a fresh crum for the surviving portion?

### Gregory's Answer

## KB Synthesis

## Mechanics of `slicecbcpm` on Partial Overlap

`slicecbcpm` **modifies the original crum in-place and creates a new sibling** — it does not disown the original.

### Phase 1: The Cut

When a deletion boundary falls strictly interior to a crum (i.e., `whereoncrum() == THRUME`), `makecutsbackuptohere()` calls `slicecbcpm` [PRE-DELETE, Finding 0075]. The split works as follows (`ndcuts.c:396-444`):

1. Compute the local offset: `localcut = cut - grasp` (the surviving prefix width, guaranteed positive)
2. **Original crum**: width shrunk in-place to `localcut` — this is the portion *before* the cut point
3. **New sibling crum**: created with width `cwid - localcut` (via `locksubtract` at `ndcuts.c:444`) — this is the portion *after* the cut point

For your example — deleting the last 3 bytes of a 5-byte crum `[1.1, 1.6)` with cut at `1.3`:
- `localcut = 1.3 - 1.1 = 0.2`
- Original crum: modified in-place to `[1.1, 1.3)`, width `0.2` ← **survives**
- New crum: `[1.3, 1.6)`, width `0.3` ← created, then eliminated in Phase 2

Both resulting widths are strictly positive — `slicecbcpm` cannot produce zero-width crums because the `THRUME` guard enforces strict interiority [INV-NO-ZERO-WIDTH-CRUM].

### Phase 2: Removal

The newly created sibling covers the deletion range entirely (Case 1 in `deletend`): `disown` + `subtreefree` removes it. The original crum, now covering only the surviving prefix, is classified as Case 0 (outside the deletion range) and left intact [ST-DELETE, Finding 0075].

### Contrast: Boundary-Aligned Deletion

If the deletion boundary aligns exactly with the crum's grasp or reach (`ONMYLEFTBORDER` or `ONMYRIGHTBORDER`), `slicecbcpm` is never called — `makecutsbackuptohere()` guards on `THRUME` only. The crum is then handled whole in Phase 2 as either Case 0 (skip) or Case 1 (disown + free), without any splitting [PRE-DELETE, Finding 0075].

### Summary

| Scenario | `slicecbcpm` called? | Original crum | New crum |
|----------|---------------------|---------------|----------|
| Cut strictly interior (THRUME) | Yes | Modified in-place (shortened) | Created, then Phase 2 deletes it |
| Cut at boundary (ONMYLEFT/ONMYRIGHT) | No | Handled whole in Phase 2 | None created |

The original crum is never disowned by `slicecbcpm` — only shrunk. Disowning is a Phase 2 operation and applies to the *new* crum (or to fully-interior crums), not to the crum whose boundary was cut.

---

## Code Exploration

I have the full picture. Here is the complete answer.

---

## How `slicecbcpm` handles partial POOM crum overlap

**Short answer:** The original crum `ptr` *is* the surviving portion — its width is reduced in-place. A fresh crum is created for the *other* (to-be-deleted) portion. The original is never disowned during slicing.

---

### Step 0 — Caller pre-allocates a fresh crum

Before `slicecbcpm` is called, `makecutsbackuptohere` at `ndcuts.c:80` does:

```c
new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
```

`createcrum` → `createcruminternal` (`credel.c:541`) allocates `sizeof(type2dcbc)` for a POOM leaf crum and **zero-initializes both `cdsp` and `cwid`** (`credel.c:580–581`):

```c
clear(&ptr->cdsp, sizeof(ptr->cdsp));
clear(&ptr->cwid, sizeof(ptr->cwid));
```

For a GRAN crum, `ndcuts.c:82` copies the `infotype` from `ptr` into `new` before the call.

---

### Step 1 — Entry guards

```c
// ndcuts.c:382
prologuend(ptr, offset, &grasp, (typedsp*)NULL);
```
Computes `grasp`: the absolute V/I address where `ptr` starts in the enfilade.

```c
// ndcuts.c:383
if (whereoncrum(ptr, offset, cut, index) != THRUME)
    gerror("Why are you trying to slice me?\n");
```
The cut must fall *through* this crum (not before it or after it). If not, it's a hard abort.

```c
// ndcuts.c:389
if (!lockis1story(ptr->cwid.dsas, (unsigned)widsize(enftype)))
    gerror("Not one story in POOM wid\n");
```
The crum's width must be a contiguous single-story span — i.e., it maps a contiguous V-range to a contiguous I-range.

---

### Step 2 — Compute local cut offset

```c
// ndcuts.c:396
tumblersub(cut, &grasp.dsas[index], &localcut);
```

`localcut = cut − grasp_start` — the offset of the cut *within* this specific crum. For the example of cutting after byte 2 of a 5-byte crum, `localcut` = 2.

Two more assertions check that the exponents match (`ndcuts.c:398`) and that `localcut` is itself 1-story (`ndcuts.c:410`).

---

### Step 3 — Partition the width

```c
// ndcuts.c:438
movewisp(&ptr->cwid, &newwid);          // newwid = ptr->cwid  (= 5)
```

`movewisp` is a macro (`wisp.h:58`): `#define movewisp(A,B) movmem((A),(B),sizeof(typewisp))` — a plain struct copy.

```c
// ndcuts.c:439–442
for (i = 0; i < widsize(enftype); i++) { /* I really don't understand this loop */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
    tumblerjustify(&newwid.dsas[i]);
}
```

`newwid` is now set to `localcut` (= 2), preserving the exponent from `ptr->cwid`. The in-source comment "I really don't understand this loop" is verbatim in the original code at `ndcuts.c:439`.

```c
// ndcuts.c:444
locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, (unsigned)widsize(enftype));
```

`locksubtract` (`wisp.c:275`) calls `tumblersub` across each dimension:
`new->cwid = ptr->cwid − newwid = 5 − 2 = 3`
The **right (to-be-deleted) portion** gets width 3.

```c
// ndcuts.c:445
movewisp(&newwid, &ptr->cwid);          // ptr->cwid = 2
```

The **original crum `ptr` is shortened in-place**: its width drops from 5 to 2. `ptr` is not disowned. No new allocation is made for the surviving portion.

---

### Step 4 — Set displacement and 2D info for the new crum

```c
// ndcuts.c:446
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
```

`dspadd` (`wisp.c:15`) = `lockadd` across DSP dimensions:
`new->cdsp = ptr->cdsp + 2` — the new crum's displacement begins immediately after the surviving portion.

```c
// ndcuts.c:447
move2dinfo(&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);
```

Copies the 2D span info (the I-space layout) from `ptr` into `new`.

---

### Step 5 — Insert new crum as right sibling

```c
// ndcuts.c:448
adopt(new, RIGHTBRO, ptr);
```

`adopt` (`genf.c:419`) splices `new` into the enfilade as `ptr`'s right sibling (`genf.c:460–462`):
```c
left = old;               // ptr stays in place
father = findfather(left);
right = findrightbro(left);
```

The original `ptr` remains in its position in the tree. `new` is inserted to its right.

---

### Step 6 — Back in the caller

```c
// ndcuts.c:85–86
ivemodified((typecorecrum*)ptr);
ivemodified((typecorecrum*)new);
```

Both crums are marked dirty. The deletion machinery (`deletecutsectionnd` via `edit.c`) subsequently walks the tree and `disown`s the crums that fall inside the deletion interval — that is `new`, the 3-byte right portion — not `ptr`.

---

### Summary

| | `ptr` (original) | `new` (fresh allocation) |
|---|---|---|
| Width after slice | 2 (shortened in-place) | 3 (the to-be-deleted portion) |
| Displacement | unchanged | `ptr->cdsp + 2` |
| Tree position | original position | inserted as `ptr`'s right sibling via `adopt` |
| Fate | **survives** — the shortened crum | **deleted** by subsequent deletion pass |

`slicecbcpm` does **not** disown the original crum and does **not** create a fresh crum for the surviving portion. It mutates `ptr->cwid` in-place to represent the surviving fragment, and the freshly `createcrum`'d `new` receives the complement width and is the one that gets removed. The surviving portion is, at all times, the identity-continuous original crum node with an adjusted width field.

---

## Question 14 [gregory]

> Under what specific conditions does `tumblersub` during DELETE shifting produce a negative V-position tumbler — is it only when the deletion width's mantissa exceeds the surviving entry's V-displacement mantissa at the same exponent, and does the system continue to function correctly with negative V-positions in the POOM?

### Gregory's Answer

## KB Synthesis

## Conditions for Negative V-Position Tumblers from DELETE

Two conditions must both hold simultaneously for `tumblersub` to produce a negative V-position during DELETE's Case 2 shifting:

**Condition 1 — Exponent match.** The deletion width's exponent must equal the surviving entry's V-displacement exponent. `deletend` calls `tumblersub` which delegates to `strongsub`. The `strongsub` exponent guard at `tumble.c:534-547` returns the minuend unchanged when `width.exp < entry.vpos.exp` — no subtraction occurs. This is why cross-subspace deletions cannot produce negative link-subspace entries: text deletion widths have exponent -1, while link crums at `2.x` have exponent 0. `strongsub(2.1, 0.3)` simply returns `2.1` [ST-DELETE, FC-SUBSPACE, INT-DELETE-SUBSPACE-ASYMMETRY].

**Condition 2 — Width exceeds displacement.** At the same exponent, the deletion width's mantissa must exceed the surviving entry's V-displacement mantissa. When both operands share the same exponent and `b > a` in absolute value, `tumblersub` produces `sign=1` (negative) with the magnitude of `b - a`. Since `tumblercmp` treats negative tumblers as strictly less than all positive tumblers and zero, the resulting entry sorts before all valid V-addresses [SS-TUMBLER Finding 0053].

Concretely: a text crum at V-displacement `0.4` (exp=-1) struck by a deletion of width `0.6` (exp=-1) would yield `sign=1, magnitude=0.2` — a negative tumbler stored back into `cdsp.dsas[V]` at `edit.c:63`.

### Scope Narrowed by Finding 0055

Finding 0055 corrects Finding 0053's broader claim. The negative V-position hazard applies only to **same-subspace, same-exponent** entries where the deletion width exceeds the entry's displacement. The often-observed empty endsets after deletion are more commonly caused by a different mechanism: I-address mappings being removed from the POOM via `disown` + `subtreefree` (Case 1 in `deletend`, for entries whose grasp falls within the deletion range) rather than their V-position going negative [EC-DEEPLY-ORPHANED-LINK].

### Behavior with Negative V-Positions in the POOM

The system does not detect, reject, or clean up negative V-position entries:

- **No integrity check.** `deletevspanpm` only verifies non-zero width before calling `deletend`. No guard exists on the resulting post-shift position [PRE-DELETE].
- **Entry persists as dead state.** The POOM tree retains the entry at its negative displacement. `tumblercmp` places it before all positive V-addresses, so it is unreachable by any V-space query that uses positive start positions [INV-POOM-BIJECTIVITY].
- **FOLLOWLINK returns empty.** The I-to-V conversion path at `orglinks.c:446-448` calls `retrieverestricted` against the document's POOM. A negative V-position has no match for positive-address queries, so the address is silently dropped — FOLLOWLINK succeeds but returns empty endsets [EC-DEEPLY-ORPHANED-LINK, INV-ITOV-FILTERING].
- **FINDLINKS cannot locate the link.** Since the entry's V-position is negative and V-space queries operate over non-negative addresses, the link cannot be rediscovered through content-identity search either [EC-DEEPLY-ORPHANED-LINK].
- **Cannot be deleted.** A subsequent DELETEVSPAN targeting the link's original position (e.g., `2.1`) will not reach the entry, because the entry now resides at a negative V-position. The leaked entry is irrecoverable through normal operations.
- **INV-POOM-BIJECTIVITY is violated.** The POOM's intended bijection from V-addresses to I-addresses holds only for non-negative V-addresses. The spec must weaken the bijectivity invariant to: `poom_d restricted to non-negative V-addresses is a bijection` [INV-POOM-BIJECTIVITY].

The system continues to function — it does not crash — but the affected link enters a permanently unreachable state distinct from both normal orphaning (content deleted, POOM entry cleanly removed or at valid position) and reverse orphaning (POOM entry cleanly removed via DELETEVSPAN) [EC-REVERSE-ORPHAN].

---

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## `tumblersub` During DELETE: Negative V-Position Conditions and Structural Safety

### The Exact Site

The `tumblersub` call in question is at `edit.c:63`, inside `deletend` (`edit.c:31`):

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```

This is reached for every crum classified "case 2" by `deletecutsectionnd` — crums that survive the deletion and must shift leftward.

---

### How Delete Gets Here

Call chain: `dodeletevspan` (`do1.c:158`) → `deletevspanpm` (`orglinks.c:145`) → `deletend` (`edit.c:31`).

`deletevspanpm` (`orglinks.c:149`) calls:
```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

Inside `deletend`, two knife positions are set (`edit.c:40-41`):
```c
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
```

After `makecutsnd` splits the tree at both knife positions, `newfindintersectionnd` finds the deepest common-ancestor node (`father`) and its accumulated absolute V-offset (`foffset`). Then (`edit.c:46`):
```c
prologuend ((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
```
which computes `fgrasp.dsas[V] = foffset.dsas[V] + father->cdsp.dsas[V]` — the absolute V-start of the father's subtree.

---

### What `deletecutsectionnd` "case 2" Means

`deletecutsectionnd` (`edit.c:235`) iterates knives from i=1 (deletion end) down to i=0 (deletion start). For POOM/SPAN nodes, `whereoncrum` (`retrie.c:355-372`) computes:
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);   // absolute start
tumbleradd(&left, &ptr->cwid.dsas[index], &right);                 // absolute end
```
and returns TOMYLEFT / ONMYLEFTBORDER / THRUME / ONMYRIGHTBORDER / TOMYRIGHT.

Case 2 means: checking knife 1 (deletion end = `origin + width`) returns ≤ ONMYLEFTBORDER, i.e., the crum's absolute left border is at or before the deletion end address. Combined with not matching case 1, this means **the crum lies entirely to the right of or at the deletion end** — it survives and must be shifted left by `width`.

---

### The Precise Negative-V Condition

The shift is:
```c
tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])   // edit.c:63
```

`tumblersub` (`tumble.c:406`):
```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr) {
    ...
    movetumbler (bptr, &temp);
    temp.sign = !temp.sign;
    tumbleradd (aptr, &temp, cptr);
    tumblerjustify (cptr);
}
```

In `functiontumbleradd` (`tumble.c:365`), when `|a| < |b|`:
```c
} else {
    weaksub (bptr, aptr, cptr);
    cptr->sign = bptr->sign;  // bptr = temp (sign=1), so cptr->sign = 1
```

**The result is negative (sign=1) if and only if `|ptr->cdsp.dsas[V]| < |width|`.**

To be precise about the mantissa comparison: `abscmp` (`tumble.c:87`) first compares exponents; if equal, it compares mantissa arrays element-by-element. So the question is mantissa-centric **when the exponents are equal**: `ptr->cdsp.dsas[V].mantissa[0] < width.mantissa[0]`. When exponents differ, the lower exponent is automatically smaller in `abscmp`.

**This situation arises structurally** when the `father` node found by `newfindintersectionnd` has already accumulated an absolute V-offset (`fgrasp.dsas[V]`) strictly greater than the deletion start `origin`. In that case:
- A crum `ptr` can have a small relative displacement `ptr->cdsp.dsas[V]` — small relative to `father` — while still having an absolute position `fgrasp.dsas[V] + ptr->cdsp.dsas[V]` that lies beyond the deletion end.
- The shift subtracts the full `width` from the small relative displacement, producing a negative result.

Concretely: if `fgrasp.dsas[V] = 5`, `ptr->cdsp.dsas[V] = 2`, `origin = 1`, `width = 4` (deletion end = 5), then absolute position = 7 ≥ 5 (case 2 fires), but `new_cdsp = 2 − 4 = −2`.

The commented-out debug code at `tumble.c:407-416` confirms this was observed and accepted:
```c
/*
    if(aptr->sign || bptr->sign) {
        fprintf(stderr,"TUMBLERSUB NEG IN \n");
        ...
    }
*/
```
And at `tumble.c:432-438`:
```c
/*
    if (cptr->sign) {
        fprintf(stderr,"TUMBLERSUB NEGATIVE OUTPUT\n");
        ...
    }
*/
```
These were removed as debug noise, not as error handlers — the negative output was deliberate.

---

### Does `tumblercheck` Catch Negative Displacements?

No. `tumblercheckptr` (`tumble.c:169`) checks for:
- `exp > 0` → error
- `sign=1 && mantissa[0]==0` → "negative zero" error
- Negative mantissa **digit** values (each `mantissa[i] < 0`) → error

It does **not** check for `sign == 1` with a nonzero mantissa. A proper negative tumbler (sign=1, mantissa=[2,0,...]) is **not flagged as invalid**. Similarly, `assertwidsarepositive` (`test.c:336`) calls `tumblercheckptr` on displacements but would not catch negative-signed tumblers. The name "assertwidsarepositive" is aspirational rather than enforced.

---

### Does the System Function Correctly? Yes — via `setwispnd` Normalization

Immediately after the shift loop in `deletend` (`edit.c:74-75`):
```c
setwispupwards (father, 1);
recombine (father);
```

`setwispupwards` calls `setwispnd` (`wisp.c:171`) for `father`, which is precisely the node whose children may now have negative displacements.

`setwispnd` computes the **element-wise minimum displacement** across all sons (`wisp.c:193-196`):
```c
movewisp (&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro(ptr))
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp, dspsize(...));
```

`lockmin` uses `macrotumblermin` (`common.h:144`):
```c
#define macrotumblermin(a,b,c) ((*(tumbler*)(c)) = (tumblercmp((a),(b)) == LESS) ? ... : ...)
```
which uses `tumblercmp` (`tumble.c:72`) — correctly ordering negative tumblers by sign first, then absolute magnitude.

Then (`wisp.c:197-211`):
```c
lockiszerop = iszerolock((tumbler*)&mindsp, dspsize(father->cenftype));
if (!lockiszerop) {
    dspadd (&father->cdsp, &mindsp, &newdsp, ...);  // father shifts backward by |mindsp|
    ...
    for (ptr = findleftson(father); ...) {
        dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, ...); // each child: cdsp -= mindsp
```

`iszerolock` (`wisp.c:253`) returns FALSE for any negative tumbler because `iszerotumbler` checks `mantissa[0] == 0`, and a negative tumbler has nonzero mantissa. So the normalization branch always fires when any child has a negative displacement.

`dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp)` = `ptr->cdsp − mindsp`. When `mindsp` is negative (say −2): `ptr->cdsp − (−2) = ptr->cdsp + 2`. The originally-negative child gets `−2 + 2 = 0`. Other children get shifted up by the same amount. `father->cdsp` gets `+mindsp = +(−2)`, i.e., decremented, preserving all absolute positions.

The normalization is conservative on sign but not on absolute displacements: it guarantees all children end with non-negative displacements, and the father absorbs the shift. Absolute V-positions are preserved throughout because `tumbleradd` operates correctly on signed tumblers.

---

### Summary

**Condition for negative V-position:** `tumblersub` at `edit.c:63` produces a negative `ptr->cdsp.dsas[V]` when the deletion width `width` exceeds the surviving crum's relative V-displacement `ptr->cdsp.dsas[V]` in absolute magnitude — i.e., `|ptr->cdsp.dsas[V]| < |width|`. At equal exponent, this reduces to the mantissa comparison the question poses: `width.mantissa[0] > ptr->cdsp.dsas[V].mantissa[0]` after exponent alignment in `abscmp`. At different exponents, the lower-exponent operand is automatically smaller. The structural precondition is that `father` (the intersection node) already has an accumulated absolute V-offset exceeding the deletion start, leaving children with small relative displacements that underflow when the full width is subtracted.

**Does the system continue to function?** Yes, completely. The negative displacement is transient by design. `setwispnd` (`wisp.c:171`), invoked immediately via `setwispupwards(father, 1)` at `edit.c:74`, detects the minimum (negative) child displacement via `lockmin`/`tumblercmp`, then normalizes the subtree in-place: each child's displacement is increased by `|mindsp|` and the father's displacement is correspondingly decreased. This preserves all absolute V-positions while eliminating all negative relative displacements before any retrieval or comparison operation sees the POOM state.

---

## Question 15 [gregory]

> When `deletend` calls `subtreefree` on fully-contained crums, does it free only the POOM tree nodes (upper crums and bottom crums), or does it also touch the granfilade leaf nodes those bottom crums pointed to — and is there any reference-counting mechanism that tracks how many POOMs reference a given I-address range?

### Gregory's Answer

## KB Synthesis

`subtreefree` frees only the POOM tree nodes — the in-memory crum structures themselves — and does not touch the granfilade.

## What `subtreefree` frees

When `deletend` classifies a bottom crum as fully within the deletion range (Case 1), it calls `disown` to remove the crum from its parent/sibling pointers, then `subtreefree` to recursively free memory (`credel.c:413-436`). These are POOM crums: upper crums and bottom crums that store the V→I displacement/width mappings. Freeing them removes the document's V-address-to-I-address mappings. [ST-DELETE, Finding 0064]

The granfilade leaf nodes the bottom crums point to are untouched. The granfilade is strictly append-only — no deletion function exists anywhere in the granf codebase. DELETE modifies only the spanfilade's POOM layer; `dodeletevspan` makes no call to any granf removal function. [FC-GRANF-ON-DELETE, INV-IADDR-IMMUTABILITY]

The canonical statement from the KB: "DELETE frees the POOM bottom crums that *reference* I-addresses, but the I-addresses themselves persist in the granfilade unconditionally." [INV-IADDR-IMMUTABILITY, Finding 0064]

## Reference counting

The disk loaf header structure does include a `refcount` field, described in the source as "For subtree sharing / GC":

```c
typedef struct structdiskloafhedr {
    ...
    SINT refcount;  // For subtree sharing / GC
    ...
} typediskloafhedr;
```
[SS-UNIFIED-STORAGE, Finding 0059]

However, the KB contains no finding documenting this field being used to track how many POOMs reference a given I-address range. The behavioral evidence points the other way: multiple documents can reference the same I-addresses via transclusion with no documented coordination between their POOMs [FC-DELETE-CROSS-DOC], and there is no garbage collection of I-addresses — the monotonic allocation invariant means every allocated I-address persists forever regardless of how many (or zero) POOMs currently reference it [INV-NO-IADDR-REUSE, INV-MONOTONIC].

The `refcount` field appears to have been intended infrastructure for subtree sharing or GC that was never implemented in a way that affects I-address lifetime. This is consistent with the broader pattern in the codebase of intended-but-unimplemented enforcement (e.g., `acceptablevsa` always returning TRUE [SS-SUBSPACE-CONVENTION], `levelpull` being disabled [SS-ENFILADE-TREE]).

## Summary

- `subtreefree` frees POOM crum nodes only (in-memory tree structures storing V→I mappings)
- Granfilade leaf nodes are not touched — they are permanent by design
- No active reference-counting mechanism tracks how many POOMs reference a given I-address range; the `refcount` field exists structurally but has no documented behavioral role in managing I-address reachability

---

## Code Exploration

I now have all the information I need. Let me compile the complete answer from the source code evidence.

---

## Answer: `subtreefree` scope and reference counting in POOM deletion

### 1. What `subtreefree` actually frees

`deletend` calls `subtreefree` for case 1 — crums fully inside the knife cuts — at `edit.c:59-61`:

```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);
    break;
```

The implementation is at `credel.c:413-432`:

```c
/* assumes crum is disowned */
void subtreefree(typecorecrum *ptr)
{
  typecorecrum *p, *right;

    if (!ptr)
        gerror ("boom in subtreefree called with ptr == NULL");
    if (ptr->height > 0) {
        for (p = ((typecuc *)ptr)->leftson; p; p = right) {
            right = p->rightbro;
            disown (p);
            subtreefree (p);
        }
    } else if (ptr->cenftype == GRAN && ((typecbc *)ptr)->cinfo.infotype == GRANORGL && ((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglincore)
        orglfree (((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglptr);
    freecrum (ptr);
}
```

The logic branches on `height`:

- **Height > 0 (upper crums)**: Recursively `disown` + `subtreefree` every child, then `freecrum(ptr)`.
- **Height == 0 (bottom crums)**: Enters the `else if` only when **all three** conditions hold: `cenftype == GRAN`, `infotype == GRANORGL`, and `orglincore == TRUE`. Otherwise calls only `freecrum(ptr)`.

**POOM bottom crums always miss this branch.** A POOM bottom crum is `type2dcbc` with `cenftype == POOM` (`enf.h:113`). The condition `ptr->cenftype == GRAN` is false, so execution goes directly to `freecrum(ptr)`.

### 2. What POOM bottom crums actually contain

`type2dcbc` is defined at `enf.h:109-131`. Its payload field is:

```c
type2dbottomcruminfo c2dinfo;
```

And `type2dbottomcruminfo` is defined at `wisp.h:107-109`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

That's it — a single `tumbler` value stored **by value** inside the struct. There is no pointer to any granfilade node. The `homedoc` tumbler records the I-address of the home document (the document this V→I mapping belongs to), but it is a coordinate by value, not a heap pointer. `freecrum` releases only the crum struct itself.

This is confirmed by the extension check in `insertnd.c:305`:

```c
if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
    return (FALSE);
```

Both sides are tumblers compared by value — no pointer dereferencing into the granfilade.

### 3. When would `subtreefree` reach the granfilade?

Only when freeing a **GRAN** bottom crum with `infotype == GRANORGL` and `orglincore == TRUE`. In that case, `orglfree` (`credel.c:470-490`) is called:

```c
void orglfree(typecuc *ptr)
{
    ...
    ((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglincore = FALSE;
    ((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglptr = NULL;
    subtreefree ((typecorecrum*)ptr);
}
```

This clears the `orglincore`/`orglptr` fields on the back-pointer (the granfilade bottom crum), then recursively calls `subtreefree` on the POOM enfilade that was stored inside the GRAN orgl crum. **This POOM enfilade is the per-document orgl.** But this path is entered from the GRAN side, not from a POOM deletion. When `deletend` operates on a POOM (version enfilade), none of the POOM crums it frees have `cenftype == GRAN`, so `orglfree` is never called and the granfilade is never touched.

**The call chain that would touch the granfilade is**:  
`deleteseq` (edit.c:16) → `freecrum(granfilade bottom crum)` — or — any path that reaches `subtreefree` on a GRAN bottom crum directly.

### 4. Reference counting for I-address ranges

**In-core: None exists.**

The `typecorecrum` / `typecuc` / `typecbc` structs (all defined in `enf.h:31-131`) have no `refcount` or `usecount` field. The closest thing is a deliberate TODO comment in `freecrum` at `credel.c:450`:

```c
/*zzz should it decrement usecount here sometimes?*/
```

This comment sits between the grimreaper circular-list unlinking and the `efree()` call. It is a dead stub — the field was never added and the decrement was never implemented.

**On-disk: A reference count exists, but for loaf sharing, not I-address tracking.**

`typediskloafhedr` in `coredisk.h:18` has:

```c
SINT refcount;      /* for subtree sharing, */
                    /* disk garbage collecting */
```

The functions `changerefcount` and `changeunterrefcount` in `disk.c:60-154` increment or decrement this when disk loafs are shared during write-out (`corediskout.c:336`, `corediskout.c:397`, `corediskout.c:485`). This tracks shared disk blocks so the disk garbage collector can free them only when the last referent is gone.

This on-disk ref count is at the **loaf level** (groups of crums packed together on disk), not at the I-address level. It answers "how many on-disk subtrees share this serialized loaf block", not "how many POOMs reference a given I-address range."

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Does `subtreefree` touch granfilade nodes when freeing POOM crums? | **No.** POOM bottom crums (`cenftype == POOM`) skip the `else if ... GRAN` branch entirely. | `credel.c:423-431` |
| What do POOM bottom crums contain that `subtreefree` must clean up? | Only a `tumbler homedoc` stored by value. No heap pointer. `freecrum()` suffices. | `wisp.h:107-109`, `enf.h:109-131` |
| Is there in-core reference counting for I-address ranges? | **No.** The `/*zzz should it decrement usecount here sometimes?*/` comment in `freecrum` marks an unimplemented idea. No `refcount` field exists in any crum struct. | `credel.c:450`, `enf.h:31-131` |
| Is there any reference counting at all? | On-disk only: `typediskloafhedr.refcount` tracks shared serialized loaf blocks for disk GC. Managed by `changerefcount`/`changeunterrefcount` in `disk.c`. | `coredisk.h:18`, `disk.c:60-154` |

The net consequence: when `deletend` calls `subtreefree` on fully-contained POOM nodes, it performs a pure in-memory free of those POOM tree nodes (upper and bottom). The granfilade is left entirely undisturbed. Nothing tracks how many POOMs reference a given I-address range, because POOM bottom crums carry that information as a plain tumbler value — a coordinate, not a counted pointer.

---

## Question 16 [gregory]

> Does DELETE on a span that covers the entire document content (full-width delete) leave the POOM in a state where subsequent retrieval returns an empty specset, and does the tree height remain at whatever level it grew to during prior insertions since `levelpull` is disabled?

### Gregory's Answer

## KB Synthesis

Yes to both.

**Full-width delete → empty retrieval**

When DELETE covers the entire document, `deletend` Case 1 (`disown` + `subtreefree`) removes all height-0 bottom crums. After the operation, the POOM tree has no bottom nodes and maps no V-addresses to I-addresses. `retrieve_vspanset` returns zero-width content — functionally empty. [ST-DELETE, Finding 0058]

**Tree height persists**

`recombinend` is called during rebalancing and invokes `levelpull` on the apex, but `levelpull` is disabled — it immediately returns 0 without executing the collapse logic. Height increases via `levelpush` are permanent; they are never reversed. [INV-ENFILADE-MINIMALITY, SS-ENFILADE-TREE, Finding 0058]

Concrete outcome: a document grown to height 3 that has all content deleted ends up with:
```
Fullcrum (height=3, numberofsons=2)    ← height unchanged
  ├─ Height-2 node (numberofsons=0)    ← empty, not freed
  └─ Height-2 node (numberofsons=0)    ← empty, not freed
```

**Additional consequence**

This post-delete empty state is structurally distinct from the never-filled state produced by `createenf` (height=1, one zero-width bottom crum). The never-filled state satisfies the implicit precondition `has_bottom_node(enf(doc))` required by `firstinsertionnd`. The delete-everything state does not — it has empty intermediate nodes but no bottom crums. Attempting INSERT or VCOPY into a delete-everything document crashes with a null pointer dereference (Bug 0019). [EC-EMPTY-DOC, Finding 0058, Finding 0064]

---

## Code Exploration

I now have the full picture from the source. Here is the complete answer:

---

## Full-Width Delete: POOM State and Tree Height After `deletend`

### 1. Does the POOM become logically empty after a full-width delete, causing subsequent retrieval to return an empty specset?

**Yes — and the specific mechanism that enforces it is an explicit NULL-children guard in `setwispnd`.**

#### Call chain

```
dodeletevspan          [do1.c:158–167]
  → deletevspanpm      [orglinks.c:145–152]
    → deletend         [edit.c:31–76]
      → setwispupwards [wisp.c:83–111]
        → setwispnd    [wisp.c:171–228]
```

**`dodeletevspan`** [`do1.c:158–167`] simply acquires the document's POOM orgl and delegates:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

**`deletevspanpm`** [`orglinks.c:145–152`] forwards directly to `deletend` on the POOM, using the V-dimension index:

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

**`deletend`** [`edit.c:31–76`] sets up two knife cuts (`origin` and `origin+width`), finds the covering node via `newfindintersectionnd`, then walks its children and classifies each:

```c
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    next = (typecuc *) findrightbro((typecorecrum*)ptr);
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 1:
        disown ((typecorecrum*)ptr);      // edit.c:59
        subtreefree ((typecorecrum*)ptr); // edit.c:60
        break;
      case 2:
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]); // edit.c:63
        break;
    }
}
setwispupwards (father,1); // edit.c:74
recombine (father);        // edit.c:75
```

For a **full-width delete** (the span covers the entire V-extent of the document), every crum bottom-node is classified `case 1` — completely inside the deletion interval — so every crum is `disown`ed and recursively freed via `subtreefree`. The covering `father` node is left with **no children** (`leftson == NULL`).

#### The zero-propagation guarantee

`setwispupwards` walks upward calling `setwisp` → `setwispnd` on each ancestor. **`setwispnd`** [`wisp.c:171–228`] has an explicit early branch for the no-children case:

```c
if ((ptr = findleftson (father)) == NULL) {
    /* All children deleted - clear width and mark modified */
    clear (&father->cdsp, sizeof(father->cdsp)); // wisp.c:187
    clear (&father->cwid, sizeof(father->cwid)); // wisp.c:188
    ivemodified((typecorecrum*)father);           // wisp.c:189
    return (TRUE);
}
```

This clears **both** `cdsp` (displacement) and `cwid` (width) on the node, marks it modified, and returns `TRUE` to continue propagating upward. For a full-width delete, this eventually reaches the POOM apex (fullcrum), whose `cwid` and `cdsp` are both zeroed.

#### Retrieval sees empty

`isemptyorgl` [`orglinks.c:539–544`] tests exactly those two fields on the apex:

```c
bool isemptyorgl(typeorgl fullcrumptr)
{
    return (
       iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cwid, widsize(POOM))
    && iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cdsp, dspsize(POOM)));
}
```

After the full-width delete, both are zero → `isemptyorgl` returns `TRUE`.

`doretrievedocvspanset` [`do1.c:322–336`] uses this directly:

```c
if (isemptyorgl (docorgl)) {
    *vspansetptr = NULL;  /* Empty document returns empty vspanset */
    return TRUE;
}
```

For the content-retrieval path (`doretrievev` → `specset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d`), the empty POOM means `findcbcinarea2d` [`retrie.c:229–268`] finds no qualifying crums, the context list remains NULL, no ispanset entries are produced, and `ispanset2vstuffset` returns an empty vstuffset.

**Conclusion:** A full-width delete leaves the POOM apex with `cwid = 0` and `cdsp = 0`. Both retrieval paths (`doretrievedocvspanset` and `doretrievev`) return empty results.

---

### 2. Does the tree height remain at whatever level it grew to during prior insertions, since `levelpull` is disabled?

**Yes — `levelpull` is unconditionally disabled; the height field can only ever grow.**

#### `levelpull` is a stub

`genf.c:318–342`:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (!isfullcrum (fullcrumptr))
        ...
    if (fullcrumptr->numberofsons > 1)
        return;
    if (fullcrumptr->height <= 1)
        return;
    ptr = (typecuc *) findleftson (fullcrumptr);
    dspadd (&fullcrumptr->cdsp, &ptr->cdsp, &fullcrumptr->cdsp, ...);
    disown (ptr);
    fullcrumptr->height--;
    transferloaf (ptr, fullcrumptr);
    setwispupwards (fullcrumptr,1);
    freecrum (ptr);
*/
}
```

The entire body — including `fullcrumptr->height--` — is commented out. The function returns `0` immediately.

#### `levelpull` is called from both recombine paths

`recombineseq` (for GRANfilades) [`recombine.c:66–68`]:

```c
if (father->isapex)
    levelpull (father);   // no-op
```

`recombinend` (for POOM and SPAN) [`recombine.c:129–131`]:

```c
if (father->isapex)
    levelpull (father);   // no-op
```

Both `recombine` callsites in `deletend` [`edit.c:75`] and `insertnd` [`insertnd.c:76`] dispatch to `recombinend` for POOM enfilades [`recombine.c:31–33`]. Neither path can ever reduce the height.

#### `levelpush` is fully active and increases height

`genf.c:263–294` (abbreviated):

```c
int levelpush(typecuc *fullcrumptr)
{
    new = (typecuc *)createcrum ((INT)fullcrumptr->height, ...);
    new->isleftmost = TRUE;
    transferloaf (fullcrumptr, new);
    fullcrumptr->height++;           // genf.c:285 — increments height
    adopt ((typecorecrum*)new, SON, (typecorecrum*)fullcrumptr);
    ...
}
```

`levelpush` is called from `splitcrumupwards` (invoked from `insertcbcnd` [`insertnd.c:272`] and `rearrangend` [`edit.c:141`]) whenever too many sons accumulate at a level. Each push bumps `height` by 1. There is no corresponding decrement anywhere in live code.

#### Post-delete state of the height field

After a full-width delete:

1. `deletend` removes all crums → `setwispnd` zeros `cwid`/`cdsp` on the apex
2. `recombine(father)` → `recombinend(father)` [`recombine.c:112–113`]:
   ```c
   if (father->height < 2  || !father->modified)
       return(0);
   ```
   If the apex height is 1, early return — nothing changes. If height ≥ 2, the take-nephew loop runs over an empty sons array (n=0), does nothing, then calls `levelpull(father)` — which is a no-op.
3. **The `height` field on the apex is not touched.** It retains whatever value was accumulated during prior insertions.

**Conclusion:** The tree height is permanently frozen at its high-water mark. A document that received N insertions forcing K `levelpush` calls will have `height == K` on the POOM apex forever. Subsequent full-width deletes leave the tree structurally hollow — zero width, no bottom crums — but at its original height. Re-insertion into this "empty tall tree" will follow the `isemptyenfilade` branch in `doinsertnd` [`insertnd.c:191–194`]:

```c
if (isemptyenfilade (father)) {
    firstinsertionnd (father, origin, width, infoptr);
    return(FALSE);
}
```

`firstinsertionnd` [`insertnd.c:199–218`] handles the case where `findleftson(father) == NULL` (the original bottom crum was freed by `subtreefree`) by creating a fresh bottom crum and adopting it under the apex — so re-insertion works correctly despite the orphaned height.

---

## Question 17 [gregory]

> When DELETE removes a V-span that was previously the target of a transclusion (shared I-addresses with another document), do the now-orphaned DOCISPAN entries in the spanfilade cause `find_documents_containing` to falsely report that the deleted-from document still contains that content?

### Gregory's Answer

## KB Synthesis

Yes — this is a confirmed, permanent behavior. The relevant KB entries converge on a clear picture.

## What Happens

**DELETE does not touch the spanfilade.** `dodeletevspan` → `deletevspanpm` → `deletend` modifies only the document's POOM (the V-to-I mapping). There is no call to any spanf removal function — none exists [ST-DELETE, Finding 0057].

**The spanfilade is write-only.** Inspection of `spanf1.c` and `spanf2.c` reveals only insertion and query functions. No `deletespanf` exists anywhere in the codebase [INV-SPANF-WRITE-ONLY].

**Consequence:** After DELETE removes a V-span from document D, the DOCISPAN entries that were created when that content was originally placed (via INSERT or COPY) persist indefinitely in the spanfilade, asserting that D contains those I-addresses. `FINDDOCSCONTAINING` queries the spanfilade directly and returns D in its results — even though D's POOM no longer maps those I-addresses to any V-position [EC-STALE-SPANF-REFERENCE, INV-IADDRESS-PERMANENT].

This applies equally whether the content was transcluded (shared I-addresses with another document) or not — the DOCISPAN entry records `D` as a containing document regardless of where the I-addresses originated.

## The Formal Characterization

The invariant is asymmetric [INT-DELETE-SPANF-DIVERGENCE]:

```
∀ D, i: (∃ v : poom.D(v) = i) ⟹ i ∈ spanf_index(D)
```

But the converse **does not hold** after DELETE:

```
i ∈ spanf_index(D) ⇏ ∃ v : poom.D(v) = i
```

So `find_documents(i)` returns a **superset** of actual containing documents:

```
actual_docs(i) ⊆ find_documents(i)
```

## The "Correction" Mechanism

The I-to-V conversion layer [INV-ITOV-FILTERING] silently drops unreferenced I-addresses when converting results back to V-addresses — `span2spanset` returns NULL for I-addresses with no POOM mapping, which are silently excluded. But this filtering only applies when a caller subsequently tries to resolve V-positions from the result. The `find_documents_containing` result itself is unfiltered.

## One Nuance: Transclusion Context

For the specific transclusion scenario you describe: if D transcluded content from source S (sharing I-addresses), and D then deletes that content, the DOCISPAN entry for D persists. Searching those I-addresses returns both S (which still has them in its POOM) and D (stale). Finding 0018 [FC-CONTENT-SPANF-ISOLATION] confirms this: "The spanf index retains the I-address mapping even after deletion from a document's V-stream" — even for the deleted-from document itself.

There is no reference counting, no cleanup mechanism, and no tombstone. The stale entry is permanent [INV-SPANF-WRITE-ONLY].

---

## Code Exploration

This has been thoroughly documented already. Here is the complete answer:

---

## Answer

**Yes, stale DOCISPAN entries in the spanfilade cause `find_documents_containing` to falsely report deleted-from documents.** This is a confirmed architectural property, documented in Findings 0057 and 0023.

---

### The Write Path (COPY → INSERT)

`docopy` in `do1.c:45-65` writes to **two** independent structures:

```c
// do1.c:60-62
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

1. **`insertpm`** — writes the V→I mapping into the document's POOM (in `granf`)
2. **`insertspanf`** — writes a DOCISPAN record into the global `spanf`, indexing the document as containing those I-addresses

`insertspanf` in `spanf1.c:15-54` encodes the ORGLRANGE key as `prefix(docisa, DOCISPAN)` and the SPANRANGE key as the I-address. This is an independent, global index entry.

---

### The Delete Path (DELETE)

`dodeletevspan` in `do1.c:158-167`:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
  /*&& TRUE*/ /* ht stuff */ );
}
```

`deletevspanpm` in `orglinks.c:145-152`:

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

`deletend` operates only on `docorgl` — the document's POOM node in `granf`. The global `spanf` is never touched. **There is no call to remove the DOCISPAN entry.**

---

### No Delete Function Exists for Spanf

A search across all `backend/*.c` confirms: there is no `deletespanf`, no `removespanf`, and no call to `deletend` on `spanf` anywhere in the codebase. The spanfilade is **write-only** — `spanf1.c` and `spanf2.c` implement only insertion and querying:

- `insertspanf` — ✅ exists
- `finddocscontainingsp` — ✅ exists
- `deletespanf` — ❌ does not exist

---

### How `find_documents_containing` Queries

`finddocscontainingsp` in `spanf1.c:151-188`:

```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                  ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        // ... return docid
    }
}
```

It queries `spanf` using the DOCISPAN subspace as the ORGLRANGE filter and the query I-span as the SPANRANGE restriction. It returns every document ISA found in matching spanfilade crums. Since those crums are never removed, the deleted-from document returns every time.

---

### The Asymmetry, Summarized

| Operation | Granf (POOM) | Spanf (DOCISPAN) |
|-----------|-------------|-------------------|
| **COPY** (transclusion) | `insertpm` adds V→I | `insertspanf` adds I→docISA |
| **DELETE** | `deletend` removes V→I | ❌ Nothing |

---

### Observable Behavior

After `DELETE`:

1. The POOM for the deleted-from document has no V-address mapping to the transcluded I-addresses. `retrieve_contents` returns nothing for those addresses.
2. The spanfilade still has the DOCISPAN entry: `(docISA at DOCISPAN offset) → I-addresses`.
3. `find_documents_containing` returns the deleted-from document. The result is a **false positive** — the document is reported as containing content whose V→I mapping no longer exists.
4. Filtering is only possible post-hoc by attempting V-conversion (Finding 0048): a caller who tries to resolve the returned docISA's V-addresses will get empty results.

---

### Architectural Interpretation

This is consistent across all spanfilade indexing: link deletion also leaves stale entries (Finding 0024). The spanfilade acts as a **historical journal** — it records "this document has ever contained this I-address" — not a **current index**. Whether this is intentional (permanent-record philosophy aligned with the permascroll) or a missing feature (no `deletend`-for-SPAN implementation was ever written) cannot be determined from the code alone. The code comment `/* ht stuff */` at `do1.c:166` suggests delete was also meant to have additional work that was never completed.

---

## Question 18 [gregory]

> If a document has two non-contiguous POOM crums mapping to I-addresses `[.0.1.1, .0.1.3]` and `[.0.1.7, .0.1.9]`, and a DELETE removes the first crum entirely, does the second crum shift left by exactly the V-width of the first crum, and is the resulting V-position computed by `tumblersub(original_vpos, deleted_width)` or by some other mechanism?

### Gregory's Answer

## KB Synthesis

## Delete Mechanics for Two Non-Contiguous Crums

Synthesizing from the KB:

### Phase 1 — Cutting

[PRE-DELETE] Finding 0075 and [SS-WHEREONCRUM]: `makecutsbackuptohere` only calls `slicecbcpm` when `whereoncrum() == THRUME` (strictly interior). If the deletion boundaries align exactly with Crum A's grasp and reach, both return `ONMYLEFTBORDER` and `ONMYRIGHTBORDER` respectively — no cutting occurs. Crum A is handled whole in Phase 2.

### Phase 2 — Classification and Action

[ST-DELETE] Finding 0075 and edit.c:31-76: `deletend` applies a two-case classification to each crum:

- **Crum A** (entirely within deletion range): **Case 1** → `disown` + `subtreefree`. The crum and its children are physically removed from the tree and freed.
- **Crum B** (entirely after the deletion range): **Case 2** → the shift is applied:
  ```c
  tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])
  ```
  where `width` is the deletion's V-span width.

### The Exponent Guard — Critical Caveat

[ST-DELETE] Finding 0055 corrects Finding 0053: `tumblersub` delegates to `strongsub`, which has an exponent guard:

> `if (bptr->exp < aptr->exp) { movetumbler(aptr, cptr); return(0); }`

So the shift **only occurs when** `width.exp >= crum_B.vpos.exp`.

- **Same exponent (typical text crums):** `deleted_width.exp = crum_B.vpos.exp = -1` → condition false → subtraction proceeds → result = `original_vpos - deleted_width` (exact shift by Crum A's V-width)
- **Cross-exponent (e.g., link crum at exp=0 vs text deletion at exp=-1):** condition true → `strongsub` returns Crum B's position unchanged — no shift. This is the mechanism behind [FC-SUBSPACE] subspace isolation for DELETE.

### Relative Addressing

[INV-ENFILADE-RELATIVE-ADDRESSING] Finding 0066: The `tumblersub` operates on `ptr->cdsp.dsas[V]` — the **relative** displacement stored in the crum node, not an absolute V-position. After all crums are processed, `setwispupwards` recalculates the root's minimum displacement across all remaining children, adjusting the absolute interpretation accordingly.

### Summary

For two same-exponent text crums where the first is removed entirely:

1. Crum A → Case 1 → physically freed from tree
2. Crum B → Case 2 → `tumblersub(original_cdsp, deleted_width)` shifts it left by exactly Crum A's V-width
3. The mechanism is `tumblersub` (via `strongsub`) on the relative `cdsp.dsas[V]` field
4. `setwispupwards` + `recombine` finalize tree structure

The `original_vpos - deleted_width` result holds precisely when both operands share the same exponent. Cross-exponent cases produce a no-op shift — not a different computation, but `strongsub` short-circuiting to return the original value unchanged [SS-TUMBLER] Finding 0055.

---

## Code Exploration

Now I have everything I need. The code is fully traced. Here is the complete answer.

---

## How V-Positions Shift After Deletion in the POOM Enfilade

### The Short Answer

Yes. The second crum shifts left by **exactly** the V-width of the deleted region. The mechanism is:

```c
tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```
— `edit.c:63`

This is a direct application of `tumblersub`, not a relative mechanism.

---

### Step-by-Step Trace

#### 1. Entry: `deletend` — `edit.c:31-76`

`dodeletevspan` calls into `deletend(fullcrumptr, origin, width, index)` where `index` is the V dimension.

```c
movetumbler(origin, &knives.blades[0]);           // knife[0] = start of delete
tumbleradd(origin, width, &knives.blades[1]);     // knife[1] = start + width
knives.nblades = 2;
makecutsnd(fullcrumptr, &knives);                  // split crums at both boundaries
newfindintersectionnd(fullcrumptr, &knives, &father, &foffset); // find common parent
```
— `edit.c:40-45`

`makecutsnd` ensures no crum straddles either knife. After this call, every node in the tree lies **entirely within one inter-knife interval**: before `origin`, between `origin` and `origin+width`, or after `origin+width`.

#### 2. Classification: `deletecutsectionnd` — `edit.c:235-248`

The loop then iterates direct children of `father` and classifies each:

```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = next) {
    switch (deletecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 0: break;                                    // before delete range — unchanged
      case 1: disown(ptr); subtreefree(ptr); break;    // inside delete range — freed
      case 2:
        tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
        break;                                          // after delete range — shifted
    }
}
```
— `edit.c:47-72`

`deletecutsectionnd` works by iterating knives from last to first and calling `whereoncrum`:

```c
for (i = knives->nblades-1; i >= 0; --i) {
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME) return (-1);
    else if (cmp <= ONMYLEFTBORDER) return (i+1);
}
return (0);
```
— `edit.c:239-247`

#### 3. `whereoncrum` — `retrie.c:345-398`

For POOM nodes (and SPAN), this computes:

```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);  // absolute V-start
tumbleradd(&left, &ptr->cwid.dsas[index], &right);                 // absolute V-end
```
— `retrie.c:356, 364`

The return codes are defined in `common.h:87-89`:

```c
#define ONMYLEFTBORDER  -1    // knife == crum's left edge
#define THRUME           0    // knife is inside crum
#define ONMYRIGHTBORDER  1    // knife == crum's right edge
// TOMYLEFT = <-1 (knife is left of crum)
// TOMYRIGHT = >1 (knife is right of crum)
```

So `cmp <= ONMYLEFTBORDER` means the knife is **at or left of** the crum's left edge — i.e., the crum starts **at or after** this knife.

With two knives (`blades[0]` = `origin`, `blades[1]` = `origin + width`):

| i | Knife | `cmp <= ONMYLEFTBORDER` means | Returns |
|---|-------|-------------------------------|---------|
| 1 | `origin+width` | crum starts at or after end of delete | 2 — **after delete range** |
| 0 | `origin` | crum starts at or after start but before end | 1 — **inside delete range** |
| — | (neither) | crum is before `origin` | 0 — **before delete range** |

#### 4. The Position Update — `edit.c:63`

For **case 2** (crum is after the deleted region):

```c
tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

`ptr->cdsp.dsas[index]` is the crum's **V-displacement relative to its parent**. Subtracting `width` from it reduces the crum's contribution to the accumulated absolute V-address by exactly `width`. When the tree is subsequently traversed to compute an absolute address via `prologuend`:

```c
dspadd(offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);   // grasp = offset + cdsp
```
— `retrie.c:336`

the accumulated result is now `width` smaller — exactly as if the crum shifted left by the deleted V-width.

#### 5. `tumblersub` — `tumble.c:406-440`

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
        temp.sign = !temp.sign;
        tumbleradd(aptr, &temp, cptr);     // c = a + (-b)
    }
    tumblerjustify(cptr);
}
```
— `tumble.c:406-440`

This is full arbitrary-precision tumbler subtraction implemented as negated addition. No special-casing for the enfilade structure — it is purely arithmetic on the tumbler representation.

#### 6. Post-deletion cleanup — `edit.c:74-75`

```c
setwispupwards(father, 1);
recombine(father);
```

These revalidate the tree's **width** (`cwid`) fields bottom-up and may merge underfull nodes. They do **not** re-adjust V-positions — that already happened at `edit.c:63`.

---

### Applied to Your Scenario

Given:
- Crum A: I-addresses `[.0.1.1, .0.1.3]`, V-displacement `V_A` (relative to parent), V-width `W_A`
- Crum B: I-addresses `[.0.1.7, .0.1.9]`, V-displacement `V_B` (relative to parent)
- DELETE removes crum A entirely (origin = absolute V-start of A, width = `W_A`)

After `makecutsnd`, the tree has clean split points. In `deletend`'s loop:
- Crum A → `case 1` → `disown` + `subtreefree` (deleted) — `edit.c:59-60`
- Crum B → `case 2` → `tumblersub(&B->cdsp.dsas[V], W_A, &B->cdsp.dsas[V])` — `edit.c:63`

Crum B's stored displacement becomes `V_B − W_A`. Its observable absolute V-address decreases by exactly `W_A`. The shift is **computed by `tumblersub`** applied to `cdsp.dsas[V]` directly, not by any relative-offset cascade or parent node adjustment.

If Crum B is not a direct child of `father` but is a descendant of one, the same `tumblersub` is applied to its **ancestor** that is a direct child of `father`, which shifts the entire subtree — and Crum B's position within that subtree is unchanged, but its absolute V-address shifts by exactly `W_A` regardless.

---

### Summary Table

| Claim | Source |
|-------|--------|
| Delete range set up as 2-knife cut | `edit.c:40-44` |
| Crums split at knife boundaries before iteration | `edit.c:44` (`makecutsnd`) |
| Parent node of affected region located | `edit.c:45` (`newfindintersectionnd`) |
| Case 2 = crum is after the delete range | `edit.c:243-244`, `retrie.c:356-372` |
| V-position adjusted by `tumblersub` on `cdsp.dsas[V]` | `edit.c:63` |
| `width` argument is the exact V-width of the deleted region | `edit.c:31` (parameter), `edit.c:41` |
| `tumblersub(a, b, c)` computes `c = a − b` via negated `tumbleradd` | `tumble.c:426-428` |
| `cdsp.dsas[V]` is V-displacement relative to parent | `retrie.c:336` (`prologuend`: `grasp = offset + cdsp`) |
| No further adjustment during `setwispupwards`/`recombine` | `edit.c:74-75` (these fix widths, not positions) |

---

## Question 19 [gregory]

> Does the `strongsub` exponent guard that provides subspace isolation during DELETE operate symmetrically — that is, does a delete in the link subspace (V-position `2.x`) also leave text subspace entries (`1.x`) unchanged, or does the guard only protect higher-exponent entries from lower-exponent widths?

### Gregory's Answer

## KB Synthesis

The guard operates symmetrically in **effect** — a delete in the link subspace (2.x) leaves text entries (1.x) unchanged — but through a **different mechanism** than the reverse direction. The two directions are protected by entirely different parts of the code.

---

## Direction 1: DELETE in text subspace (1.x) → link entries (2.x) unchanged

This is the case documented in [FC-SUBSPACE] / Finding 0055. Link crums sit at V-displacement exp=0 (e.g., `2.1`). The text deletion width (e.g., `0.3`) has exp=−1. `deletecutsectionnd` classifies link crums as Case 2 (after the deletion range), so `tumblersub(2.1, 0.3)` is called — but `strongsub` fires its exponent guard:

```
b.exp (−1) < a.exp (0)  →  TRUE  →  returns 2.1 unchanged
```

Protection is **arithmetically accidental**: the exponent mismatch prevents subtraction. There is no design comment indicating awareness of this as a subspace guard.

---

## Direction 2: DELETE in link subspace (2.x) → text entries (1.x) unchanged

Text crums sit at V-positions like `1.5` (exp=−1), which are numerically less than any 2.x address. The DELETE knife blades for a link-subspace operation are `[2.1, 2.2]`. `deletecutsectionnd` classifies text crums as **Case 0** (TOMYLEFT of blade[0]):

```
text_vpos (1.5) < blade[0] (2.1)  →  Case 0  →  no shift, no subtraction
```

`strongsub` is **never called** on text entries at all. Protection is **positional**: text lives below the deletion range. The exponent guard plays no role.

---

## Verification: Finding 0040 directly confirms the symmetric result

[SS-THREE-LAYER-MODEL] / Finding 0040 provides empirical confirmation: after `DELETEVSPAN(2.1)`, the resulting vspanset shows `{"start": "1.1", "width": "0.11"}` — the text subspace is completely unchanged.

---

## Summary

| Delete direction | Other subspace protected? | Mechanism |
|---|---|---|
| Text (1.x) delete | Link (2.x) entries safe | `strongsub` exponent guard: b.exp(−1) < a.exp(0) |
| Link (2.x) delete | Text (1.x) entries safe | Positional classification: text < blade[0], Case 0 |

The guard is **not symmetric in mechanism**. INSERT achieves symmetry through a deliberate structural guard (two-blade knife with subspace boundary at `(N+1).1`). DELETE achieves it through two independent and unrelated properties — an arithmetic accident for one direction, and ordinary positional ordering for the other. As [INT-DELETE-SUBSPACE-ASYMMETRY] notes, the arithmetic protection is fragile: if `strongsub` were ever modified to handle cross-exponent subtraction, text-subspace deletes would break link subspace isolation, while the positional protection for the reverse direction would remain intact.

---

## Code Exploration

I now have all the evidence needed. Here is the complete analysis.

---

## Does the `strongsub` exponent guard operate symmetrically in DELETE?

**Short answer: No. The two directions of subspace isolation use entirely different mechanisms.** The guard protects link-subspace crums from text-subspace deletions. Text-subspace crums are protected from link-subspace deletions by spatial ordering alone — the guard never fires in that direction because `tumblersub` is never called on them.

---

### The delete path

`dodeletevspan` [do1.c:158-167] → `deletevspanpm` [orglinks.c:145-152] → `deletend` [edit.c:31-76].

`deletend` plants two knife blades:

```c
// edit.c:40-43
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
```

Then iterates over children of the spanning father node and classifies each crum via `deletecutsectionnd` [edit.c:235-248]:

- **Case 0**: crum is entirely to the LEFT of blade[0] — before the deletion. No action.
- **Case 1**: crum's left edge falls between blade[0] and blade[1] — within the deletion. `disown` + `subtreefree`.
- **Case 2**: crum's left edge is at or after blade[1] — entirely to the right of the deletion. `tumblersub` is called:

```c
// edit.c:63
tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

`tumblersub` [tumble.c:406-439] negates `width.sign` and calls `tumbleradd`, which dispatches to **`strongsub`** [tumble.c:534-565] when `abscmp(crum_disp, width) == GREATER`.

---

### The exponent guard in `strongsub`

```c
// tumble.c:544-546
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);
    return(0);
}
```

`aptr` = the crum's V-displacement, `bptr` = the deletion width (as a magnitude). When `bptr->exp` is more negative (finer-grained) than `aptr->exp`, the guard fires and returns `aptr` unchanged.

---

### V-space layout: what exponents look like

**Text subspace** crums are inserted at V-positions 1.1, 1.2, … via `findvsatoappend` [orglinks.c:42-43]:

```c
tumblerincrement (vsaptr, 0, 1, vsaptr);   // → 1
tumblerincrement (vsaptr, 1, 1, vsaptr);   // → 1.1
```

These tumblers have `exp=0`, `mantissa=[1,1,0,…]`.

**Link subspace** crums are inserted starting at 2.1 via `findnextlinkvsa` [do2.c:157-158]:

```c
tumblerincrement (&firstlink, 0, 2, &firstlink);  // → 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // → 2.1
```

Tumblers with `exp=0`, `mantissa=[2,1,0,…]`.

**Deletion widths** for a typical intra-subspace cut are computed via `strongsub`. Deleting [1.x, 1.y) or [2.x, 2.y):

`strongsub([1,y,…], [1,x,…])` [tumble.c:534-565]:

- `exp` starts at 0; mantissa[0] matches (both 1), so `--answer.exp` makes it **-1**
- `answer.mantissa[0] = y - x`
- Result: **`exp = -1`, `mantissa = [y-x, 0, …]`**

All intra-subspace deletion widths have `exp = -1`.

---

### Direction 1: Delete in text subspace → effect on link crums

Delete at `[1.1, 1.4)`. Blade[0] = `[1,1,…] exp=0`, blade[1] = `[1,4,…] exp=0`, width = `[3,0,…] exp=-1`.

A link crum at absolute V-position `2.1` has V-displacement (relative to root at 0): `[2,1,…] exp=0`.

- `whereoncrum(link_crum, offset, blade[1]=[1,4,…])`: link left edge `2.1 > 1.4` → blade is **TOMYLEFT** of the link crum → `cmp <= ONMYLEFTBORDER` → **case 2**.
- `tumblersub([2,1,… exp=0], [3,… exp=-1])` is called.
- → `tumbleradd([2,1,…], -[3,… exp=-1])` → `abscmp`: `aptr.exp=0 > bptr.exp=-1` → GREATER → `strongsub`:

```c
// tumble.c:544-546
if (bptr->exp(-1) < aptr->exp(0))   // TRUE
    movetumbler(aptr, cptr);         // link displacement returned unchanged
    return(0);
```

**Link crum displacement is unchanged. The guard fires.** ✓

---

### Direction 2: Delete in link subspace → effect on text crums

Delete at `[2.1, 2.4)`. Blade[0] = `[2,1,…] exp=0`, blade[1] = `[2,4,…] exp=0`.

A text crum at V-position `1.1`, right edge `1.2`.

`deletecutsectionnd` [edit.c:235-248]:

- i=1, `whereoncrum(text_crum, offset, blade[1]=[2,4,…])`:
  - left = `1.1 < 2.4`, right = `1.2 < 2.4` → blade is TOMYRIGHT of crum (address > right edge) → returns **TOMYRIGHT**
  - Not THRUME, not `<= ONMYLEFTBORDER` → continue.
- i=0, `whereoncrum(text_crum, offset, blade[0]=[2.1])`:
  - Same: right edge `1.2 < 2.1` → **TOMYRIGHT** → continue.
- Loop ends. Return **0**.

**Case 0: `tumblersub` is never called on the text crum.** The guard is never reached. Text crums at `1.x` are always to the LEFT of any `2.x` knife boundary — `whereoncrum` returns TOMYRIGHT for both blades, landing in case 0 every time.

---

### The asymmetry, precisely stated

| Scenario | Mechanism | Guard fires? |
|---|---|---|
| Delete `[1.x, 1.y)` → link crum at `2.z` | `strongsub` exponent guard: `bptr.exp=-1 < aptr.exp=0` → crum unchanged | **Yes** |
| Delete `[2.x, 2.y)` → text crum at `1.z` | `deletecutsectionnd` case 0 → `tumblersub` never called | **Never reached** |

The guard is **not symmetric**. It operates in only one direction — protecting integer-exponent (`exp=0`) V-displacements from sub-integer (`exp=-1`) deletion widths. The other direction of isolation is provided entirely by the spatial ordering of V-space: since all text positions (`1.x`) are numerically less than all link positions (`2.x`), text crums always fall to the LEFT of any link-subspace cut (`deletecutsectionnd` case 0), and the `tumblersub`/`strongsub` call chain is never entered for them.

The guard can be said to protect "higher-exponent entries from lower-exponent widths" (your framing is correct for the direction it covers). It does not need to protect in the reverse direction — and structurally cannot, since text crums are never candidates for case 2 shifting during link-space deletions.

---

## Question 20 [gregory]

> After DELETE creates unreachable I-addresses (content present in granfilade but referenced by no POOM), is there any operation or query path in the backend that can enumerate these orphaned I-address ranges, or are they permanently invisible unless their addresses are already known from a prior retrieval?

### Gregory's Answer

## KB Synthesis

Orphaned I-address ranges are permanently invisible through any described public operation unless their addresses are already known from a prior retrieval.

**Why there is no enumeration path:**

The granfilade is append-only and contains all I-addresses ever allocated [INV-MONOTONIC, FC-GRANF-ON-DELETE]. But there is no described FEBE operation that traverses or enumerates granfilade content by I-address. All retrieval paths require either a starting V-address (which orphaned content lacks) or an I-address you already possess.

The three public query mechanisms all fail to surface orphaned I-addresses:

1. **V-space queries** (`RETRIEVEDOCVSPAN`, `RETRIEVEDOCVSPANSET`, `RETRIEVE_CONTENTS`): These operate through the POOM — they return only content with current V→I mappings. DELETE removes those mappings, so orphaned I-addresses have no V-position and are structurally invisible [ST-DELETE, Finding 0064].

2. **`FINDDOCSCONTAINING`**: Requires a known I-address as input. It searches the spanfilade, which remains stale after DELETE [INV-SPANF-WRITE-ONLY, EC-STALE-SPANF-REFERENCE] — it can confirm that a *known* I-address was once in a document, but provides no mechanism to discover *which* I-addresses are now orphaned.

3. **Link operations** (`FOLLOWLINK`, `RETRIEVEENDSETS`): These perform I→V conversion, which silently drops unreferenced I-addresses without error [INV-ITOV-FILTERING]. Empty endsets signal orphaning but only for I-addresses already known via the link's endset structure [EC-GHOST-LINK].

**The one detection path — not enumeration:**

If you hold a link whose endpoint I-addresses were deleted, `FOLLOWLINK` returning `[]` with `works: true` tells you those specific I-addresses are now orphaned [EC-GHOST-LINK, EC-ORPHANED-LINK]. But this detects orphaning of *known* I-addresses; it does not enumerate unknown ones.

**Why the stale spanfilade doesn't help:**

The post-DELETE spanfilade state satisfies `actual_docs(i) ⊆ find_documents(i)`, not equality [EC-STALE-SPANF-REFERENCE]. Even if you probed `FINDDOCSCONTAINING` for a range, you'd get a superset of current references — and you'd still need to already know which I-address to probe.

**Bottom line:** The architecture has no "scan orphaned I-addresses" operation. The internal `findpreviousisagr` function used by the allocator traverses the granfilade tree to find the maximum I-address, but it is not exposed as a FEBE operation and operates within a bounded document address range, not across all orphaned content. Any orphaned I-address range is recoverable only if its address was captured before deletion — for example, stored in a link endset, recorded by the client, or derivable from the monotonic allocation sequence of a known document.

---

## Code Exploration

Now I have a complete picture. Here is the full analysis:

---

## Answer: Orphaned I-Addresses After DELETE Are Permanently Invisible

### 1. What DELETE Actually Does

The delete path is:

`deletevspan` (`fns.c:333-347`) → `dodeletevspan` (`do1.c:158-167`) → `deletevspanpm` (`orglinks.c:145-152`) → `deletend` (`edit.c:31-76`)

`dodeletevspan` [do1.c:163-166]:
```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
);
```

`deletevspanpm` [orglinks.c:145-152]:
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

`deletend` [edit.c:31-76] removes POOM crums in the deleted V-range:
- `case 1:` → `disown` + `subtreefree` — POOM crum is freed
- `case 2:` → `tumblersub` on `cdsp.dsas[index]` — POOM crum is displaced

**Three crucial omissions:**
1. The granfilade (`granf`) is never touched. Content at those I-addresses stays in place.
2. The spanfilade (`spanf`) is never touched. The I→document entries inserted by the original `insertspanf` call remain.
3. `deleteversion` [bert.c:348-353] is a **stub** — the function body contains only a debug `fprintf` and no logic whatsoever.

---

### 2. What the Granfilade Holds

When content is inserted via `doinsert` [do1.c:87-123]:
```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
);
```

`inserttextgr` [granf2.c:83-109] allocates a new I-address (`findisatoinsertgr`), writes bytes via `insertseq`, and returns the resulting ispan. This content is written once and never removed by any operation in the codebase.

`docopy` [do1.c:45-65] then calls both:
```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)    /* POOM */
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) /* SPANFILADE */
```

After DELETE only modifies the POOM, the granfilade byte content and the spanfilade I→doc association both survive.

---

### 3. The Complete FEBE Query Surface

Every exposed operation in `fns.c` falls into one of two categories:

**V-address-in, content-out** (blocked by missing POOM entry):

| Operation | Path | Blocked? |
|-----------|------|---------|
| `retrievev` | V-specset → `specset2ispanset` → POOM → I-spans → granfilade | **Yes** — POOM entry removed |
| `retrievedocvspan` / `retrievedocvspanset` | Returns POOM root crum `cdsp.dsas[V]` / `cwid.dsas[V]` | Shows only what POOM still holds |
| `copy` | V-specset → I-spans → new POOM entry | **Yes** — can't copy what you can't address |
| `rearrange` | V-address cuts → POOM rearrangement | Operates only on POOM |

**I-address-in or link-in** (not enumeration):

| Operation | Path | Can it find orphans? |
|-----------|------|---------------------|
| `finddocscontaining` [do1.c:15-23] | I-spans (provided by caller) → SPANFILADE → doc ISAs | **No** — caller must already know the I-spans |
| `findlinksfromtothree` [do1.c:348-353] | V-specset → I-spans → SPANFILADE → link ISAs | **No** — still requires V-addresses |
| `followlink` [do1.c:223-232] | Link ISA → link endpoint specsets | **No** — requires knowing the link |
| `retrieveendsets` | Link specset → SPANFILADE endpoint sets | **No** — requires knowing the link |
| `showrelationof2versions` | V-specsets → I-span intersection | **No** — still V-in |

There is no FEBE operation that takes an I-span range as *primary* input for open-ended enumeration, nor any operation that traverses the granfilade or spanfilade from their roots to enumerate all stored ranges.

---

### 4. Internal Functions That Could Enumerate — But Are Not Exposed

The granfilade traversal machinery exists internally:

- `retrieveinspan` [retrie.c:112-136]: scans all leaf crums in a given I-span range via `findcbcinspanseq`. Could, in principle, enumerate all content in the granfilade given `spanstart=0` and `spanend=∞`. **Not exposed via any `do*` function or FEBE handler.**

- `findlastcbcseq` [retrie.c:138-158]: walks the rightmost chain to find the maximum I-address. **Not exposed.**

- `ispan2vstuffset` [granf2.c:286-318]: retrieves content for a specific I-span by calling `retrieveinspan`. Only called from `ispanset2vstuffset` [granf1.c:58-74], which is only called from `doretrievev`, which gets its I-spans from the POOM. The chain is V→POOM→I→granfilade with no external I-span entry point.

- `isaexistsgr` [granf2.c:244-253]: can verify whether a *specific* I-address exists in the granfilade. Only called by `findisatoinsertgr` during new-address allocation. Not called from any query path.

---

### 5. The Spanfilade Is Also a Dead End

Even though `dodeletevspan` does not clean up the spanfilade, the spanfilade provides no enumeration escape hatch:

`finddocscontaining` [spanf1.c:151-188] issues a `retrieverestricted` call against the spanfilade:
```c
context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                               ispanset, SPANRANGE, (typeisa*)NULL);
```
The `ispanset` (SPANRANGE restriction) must be supplied by the caller. It cannot be null — passing `NULL` for `span1ptr` in `retrieverestricted` [retrie.c:56-85] replaces it with a zero-tumbler pair `{0,0}`, which matches nothing.

There is no "scan all SPANRANGE entries" operation exposed to the FEBE client.

---

### 6. Conclusion

After `dodeletevspan` removes the V→I mapping from the POOM:

- The granfilade retains the byte content at those I-addresses permanently. Nothing removes granfilade entries. `deleteversion` [bert.c:348-353] is an empty stub.
- The spanfilade retains the I→document associations from the original `insertspanf` call, but this information is also unreachable — there is no way to enumerate which I-spans are recorded without already knowing the I-spans.
- **Every read path is top-down from V-addresses through the POOM.** The POOM is the only directory of what content is addressable. Once a POOM crum is removed by `deletend`, the I-addresses it mapped become invisible.
- **No FEBE operation enumerates I-addresses bottom-up from the granfilade or spanfilade.**

The orphaned I-address ranges are **permanently invisible unless already known from a prior retrieval**. The content occupies granfilade space indefinitely with no garbage collection path and no client-accessible enumeration mechanism.
