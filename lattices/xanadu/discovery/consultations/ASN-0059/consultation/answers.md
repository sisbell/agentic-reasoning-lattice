# Consultation Answers — INSERT Operation

**Inquiry:** What is the precise effect of inserting new content at a position in the Vstream? What is allocated, what shifts, and what invariants must the completed operation preserve?
**Date:** 2026-03-20 20:53
**Questions:** 18 (8 nelson, 10 gregory)

---

## Question 1 [nelson]

> When new content is inserted at a position in a document's stream, does every byte of the existing content retain its original permanent identity, or does shifting content to make room assign new identities?

### Nelson's Answer

## Every byte retains its permanent identity. Insertion never reassigns existing identities.

This is the entire point of the Istream/Vstream separation. The two address spaces serve different purposes:

- **Istream** — where content **permanently lives**. Addresses are absolute and immutable. Content at an Istream address never changes. [LM 4/10-4/11]
- **Vstream** — the document's **current arrangement**. A view that references Istream content. Can be rearranged across versions. [LM 4/10-4/11]

### What INSERT actually does

Nelson's specification of INSERT is explicit:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Three things happen:

1. **New content gets fresh I-addresses.** The inserted bytes are appended to Istream — the append-only store where content permanently resides. Nelson: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

2. **Vstream addresses shift.** Following characters get higher V-addresses. This is purely a change to the document's arrangement — which positions in the virtual byte stream map to which permanent content.

3. **Istream addresses of existing bytes are untouched.** The bytes that were already in the document retain their permanent identities exactly as before.

### Nelson says this explicitly

On V-addresses changing while identity is preserved:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

On V-addresses being ephemeral:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

This quote is about V-addresses (the "address of a byte in its native document" refers to the byte's position in the current arrangement). The I-address — where the byte permanently lives — never changes.

### Why this matters: link survivability

The guarantee that existing bytes retain their identities is what makes link survivability possible:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

If insertion reassigned I-addresses to existing bytes, links would break on every edit. The entire link survivability guarantee depends on content identity being invariant under editing operations.

### The library analogy

Think of it as Nelson's library stacks versus reading lists:

- **Istream (library stacks):** Each book has a permanent shelf location. Adding a new book means placing it on a **new** shelf. You never move existing books.
- **Vstream (reading list):** Your reading list references shelf locations. Inserting a new reference at position 3 shifts items 3, 4, 5... to positions 4, 5, 6... But the books on the shelves haven't moved.

### Summary

| What changes on INSERT | What does NOT change |
|---|---|
| V-addresses of following bytes (shift up) | I-addresses of any existing bytes |
| The V→I mapping (new entries added) | Content stored at existing I-addresses |
| The document's current arrangement | Links attached to existing bytes |

The document IS the mapping from V-addresses to I-addresses [LM 4/10-4/11]. INSERT modifies that mapping by adding new entries and shifting existing V-positions. It never touches the Istream content or its addresses.

---

## Question 2 [nelson]

> After insertion, if a reader retrieves the document, must the new content appear at exactly the specified position with all prior content in its original relative order on either side?

### Nelson's Answer

## Yes — Nelson specifies this explicitly.

The INSERT command definition at [LM 4/66] states:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text."

This gives three guarantees:

1. **New content appears at the specified V-address.** The `<doc vsa>` parameter is the exact Vstream position where the inserted text will begin.

2. **Content before the insertion point is undisturbed.** V-addresses 1 through P-1 remain unchanged — Nelson says only "following characters" are affected.

3. **Content after the insertion point preserves its relative order**, shifted uniformly by the insertion length. "Increased by the length of the inserted text" means every post-insertion byte shifts by the same amount, preserving their relative ordering exactly.

### Why this follows from the Vstream model

The Vstream is always a dense, contiguous sequence. Nelson at [LM 4/30]:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address."

There are no gaps in V-addresses. If you have N bytes, you have positions 1 through N. After inserting `len` bytes at position P, the result is positions 1 through N+len, with the new content occupying P through P+len-1 and the formerly-at-P-and-after content occupying P+len through N+len.

### Istream is unaffected

At [LM 4/11]:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control."

INSERT adds new bytes to Istream (append-only storage) and updates the Vstream mapping to splice them in. No prior Istream content is moved or altered. The shift is purely a Vstream phenomenon — the mapping from virtual positions to permanent content addresses is updated.

This is further confirmed by the link survivability guarantee at [LM 4/30]:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."

Links survive insertion precisely because they point to Istream addresses (permanent), not Vstream positions (which shift). The prior content's identity is unchanged; only its virtual position moves.

### Summary

After INSERT at position P with content of length L:
- V-positions 1..P-1: unchanged (same content, same addresses)
- V-positions P..P+L-1: the new content
- V-positions P+L..N+L: the prior content that was at P..N, in original relative order

This is not inferred — it is the direct, specified semantics of INSERT at [LM 4/66].

---

## Question 3 [nelson]

> If the same content appears in multiple documents through sharing, does inserting into one document's stream affect the position or appearance of that shared content in any other document?

### Nelson's Answer

## No. Insertion into one document's stream does not affect shared content in any other document.

This is a direct consequence of the Istream/Vstream separation.

### Each document has its own independent Vstream

When content is shared between documents (via COPY/transclusion), both documents' Vstreams contain mappings that point to the same Istream bytes. But the Vstreams themselves are completely independent structures.

INSERT is explicitly scoped to a single document:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters **in the document** are increased by the length of the inserted text." [LM 4/66]

The phrase "in the document" is the key constraint. Only the target document's V-addresses shift. Every other document's Vstream is untouched.

### Istream content is immutable

INSERT creates **new** Istream bytes and weaves them into the target document's Vstream. It does not modify existing Istream content. The shared bytes remain at their permanent I-addresses, unchanged:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address of shared content never changes. No operation on any document can alter what lives at an I-address.

### Nelson confirms this explicitly for DELETE (the parallel case)

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If DELETE from one document doesn't affect other documents containing the same content, INSERT certainly doesn't either. Both are Vstream operations scoped to a single document.

### The analogy

Using Nelson's library analogy: Istream is the library stacks (permanent shelf locations), Vstream is a reading list (references that can be reordered). If two professors have reading lists that both reference the same book on shelf A, one professor inserting a new book into her reading list does not change the other professor's reading list, nor does it move the book on the shelf.

### The windowing nuance

There is one case where changes to Document A can be *visible through* Document B: when Document B has a **location-fixed window** into Document A (floating in time). In that mode:

> "at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

But this is not shared content being affected — it is Document B's window *designed to follow* Document A's current Vstream arrangement. The mechanism is fundamentally different from content sharing via COPY. The window is tracking a live view of another document, not holding independent references to shared Istream bytes.

### Summary

| What happens | Effect on other documents |
|---|---|
| INSERT into Doc A's Vstream | None. Other documents' Vstreams unchanged. |
| New Istream bytes created | Other documents don't reference them. |
| Doc A's V-addresses shift | Other documents' V-addresses unaffected. |
| Shared Istream bytes | Remain at same I-addresses, immutable. |

The entire architecture is designed so that editing is a per-document Vstream operation with no side effects on other documents. This is what makes the system safe for concurrent use by independent authors building on shared content.

---

## Question 4 [nelson]

> Must the insertion operation be atomic — either fully completed with all guarantees preserved, or not performed at all — with no observable intermediate state?

### Nelson's Answer

# Must INSERT Be Atomic?

Nelson does not use the word "atomic" or discuss transaction semantics anywhere in Literary Machines. He does not explicitly address observable intermediate states, partial completion, or rollback for any FEBE operation, including INSERT.

However, his design principles strongly constrain the answer.

## The Canonical Order Mandate

The closest Nelson comes to addressing this is in his discussion of enfilades:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The phrase **"canonical order, which was an internal mandate"** is the key. This is not a suggestion — it is a design requirement. After any change, the system must be in canonical order. The phrase "once made" implies changes complete as units: you go from one canonical state to another.

## What INSERT Must Preserve

The INSERT operation is defined as:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

This single sentence specifies **two coupled effects**:
1. New content appears at the specified V-address
2. All following V-addresses shift by the insertion length

These are not independent operations. If a reader could observe the content inserted but the addresses not yet shifted, they would see corrupted V-stream addresses — two different bytes claiming the same position. This violates canonical order.

Additionally, link survivability requires consistency:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Links attach to I-addresses, which don't move during INSERT. But the V→I mapping must be updated consistently. If a front end retrieves content during a half-completed INSERT, it could receive a V-span that maps to the wrong I-addresses — the link would appear to point to different content than intended.

## The FEBE Command Model

Nelson describes FEBE as a command-response protocol:

> "FEBE commands are presently in verbose ASCII." [LM 4/61]

Each of the 17 operations takes parameters and returns results. INSERT returns nothing explicit (it modifies state), but the protocol structure implies: you issue a command, the back end processes it, the state changes. There is no provision for "INSERT succeeded partially" or "INSERT is in progress."

## What Nelson Does NOT Say

Nelson does not address:
- What happens if INSERT fails midway (hardware failure, storage exhaustion)
- Whether concurrent readers can see intermediate states
- Whether the system should roll back on failure
- Any formal transaction semantics

He also does not address concurrent modification. The session model discussion notes that Nelson specifies no locking protocol, no OPEN/CLOSE lifecycle, and no concurrent editing mechanism.

## My Answer

The question frames atomicity as a formal requirement with specific computer science meaning: "either fully completed or not performed at all, with no observable intermediate state."

Nelson does not frame his requirements in those terms. What he requires is something subtler but equally demanding: **the system must always be in canonical order**. Every change, "once made," leaves the system valid. This is not a transactional guarantee — it is a structural invariant.

The practical consequence is the same: an INSERT that leaves the system in a non-canonical state (content present but V-addresses not shifted, or V-addresses shifted but content not present) violates the internal mandate. The system must move from one canonical state to another with no intermediate state visible to any observer.

Whether you call this "atomicity" is a matter of vocabulary. Nelson would call it maintaining canonical order. The effect is identical: INSERT either completes fully or does not appear to have happened.

The deeper principle is that Xanadu's guarantees — permanence, link survivability, origin traceability — are **invariants**, not eventual properties. They hold at every observable moment, not merely "after the system settles." A system where INSERT could be observed mid-flight, with links temporarily pointing to wrong content or V-addresses temporarily inconsistent, would violate the guarantees Nelson considers fundamental.

So: yes, INSERT must be atomic in effect, though Nelson's language for this requirement is "canonical order" rather than "atomicity." The mandate is from [LM 1/34], and it applies to all editing operations, not just INSERT.

NEED_RAW: 4/65-4/67 (full context around INSERT and neighboring operations for any error handling discussion), 1/33-1/38 (full enfilade discussion for additional canonical order context)

---

## Question 5 [nelson]

> After insertion shifts existing content to later positions in the document stream, must every prior reference to that existing content — by its permanent identity, not by document position — still resolve to exactly the same bytes?

### Nelson's Answer

**Yes. Absolutely and unconditionally.**

This is the central architectural invariant of Xanadu. The entire Istream/Vstream separation exists to guarantee exactly this property.

## What INSERT affects

INSERT operates on **Vstream** — the document's current arrangement:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

V-addresses shift. That is their nature — they are ephemeral positions in the current view.

## What INSERT does not affect

INSERT does not touch **Istream** — the permanent identity space where content lives:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

Nelson is explicit: V-addresses "may be constantly changing" through editorial operations, but the permanent identity of the bytes — their I-addresses — is unaffected. The front end doesn't even see the I-addresses changing, because they don't.

## The design principle

The Istream is **append-only**:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content at an I-address never changes. New content gets new I-addresses. INSERT adds new bytes to Istream (the inserted text) and updates the Vstream mapping (shifting positions) — but every prior I-address resolves to exactly the same bytes it always did.

## Why this matters

This invariant is what makes link survivability possible:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Links reference I-addresses. INSERT shifts V-addresses. Therefore links are completely unaffected by insertion. The "strap between bytes" stays attached to the same bytes because those bytes' permanent identities have not changed — only their positions in the current document arrangement have shifted.

## Summary

The permanent identity of content (Istream address) is invariant under all editing operations — INSERT, DELETE, REARRANGE, COPY. This is not a feature bolted onto the system; it is the foundational architectural decision. Vstream is the view that changes; Istream is the identity that does not. Any reference by permanent identity resolves to the same bytes before and after insertion, unconditionally.

---

## Question 6 [nelson]

> Is there a design constraint on where insertion may occur — must it be permitted at any position within the stream, including the very beginning and the very end?

### Nelson's Answer

## INSERT Position Constraints

Nelson's description of INSERT is position-based and unrestricted:

> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The phrasing "any following characters" accommodates all positions naturally:

- **At the beginning** (position 1): all existing characters are "following" — all shift forward
- **In the middle** (position k): characters from k onward shift
- **At the end**: no following characters — the statement is vacuously satisfied

The V-stream is a dense, contiguous address space starting at 1. There is no structural reason to exclude any position within the range [1, N+1] for a document of length N.

### APPEND as Convenience, Not Constraint

APPEND exists as a separate operation:

> "This appends <text set> onto the end of the text space of the document <doc id>." [LM 4/67]

APPEND relieves the caller from needing to know the document's current length. It does not imply that INSERT cannot reach the end — it's a convenience for a common case, not a restriction on INSERT's domain. For an empty document (created by CREATENEWDOCUMENT, which "creates an empty document" [LM 4/65]), INSERT at position 1 and APPEND produce identical results.

### Design Philosophy Supports Unrestricted Position

Nelson describes these operations as "conceptually simple" [LM 4/61]. Arbitrary positional restrictions would contradict that simplicity. The deeper principle from storage design reinforces this:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." [LM 2/15]

Content can be "added" anywhere the braid admits — which is anywhere.

### The Istream Perspective

INSERT always appends to the Istream (new bytes get fresh, permanent I-addresses). The positional question is purely about the Vstream mapping. Since the V→I mapping is the document's structure and is freely rearrangeable, there is no Istream-side reason to restrict insertion position either.

### Summary

**Yes — INSERT must be permitted at any position, including the very beginning and the very end.** The operation is defined by a V-stream address parameter with no stated restriction on its range. The dense, gap-free nature of V-addresses, the existence of APPEND as convenience rather than necessity, and Nelson's emphasis on conceptual simplicity all point to unrestricted positional insertion.

NEED_RAW: [4/66 (raw page 233)] — The curated sources give the one-line specification of INSERT. The raw page may contain additional parameter constraints, edge-case notes, or diagrams that further clarify the valid range of `<doc vsa>`.

---

## Question 7 [nelson]

> When content is inserted, does the system guarantee that the new content is immediately and permanently retrievable by its assigned identity from that point forward, with no possibility of loss?

### Nelson's Answer

# Permanence of Inserted Content

## The Design Intent: Yes, Permanent from Creation

Nelson's architecture is built around the principle that content, once created, exists permanently. The Istream is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Once bytes are appended to the Istream, they receive a permanent I-address — a tumbler encoding their server, account, document, and element position. That address is guaranteed stable:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

And content at an I-address never changes. Even "deletion" only removes content from the Vstream (current arrangement) — the Istream bytes persist:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The retrieval model assumes immediate availability — Nelson's "pounce" concept:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

## Three Caveats Nelson Himself Acknowledges

### 1. No Technical Guarantee Against Loss

Nelson explicitly disclaims reliability at the infrastructure level:

> "User acknowledges that due to possible unreliability of the software, unreliability and vulnerability of transmission systems, and myriad possibilities for intrusion and malicious mischief by unseen parties throughout the universe, all storage, and transmission of contents and links, and attempts to deliver such material, are at User's risk." [LM 5/18]

The system provides no cryptographic verification of integrity:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

Trust rests on the Storage Vendor franchise — contractual, not mathematical.

### 2. Economic Conditionality

Permanence requires ongoing payment:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Nelson does not specify what happens if storage rental lapses. The I-address remains permanently *assigned* (no reuse), but *accessibility* depends on someone continuing to pay.

### 3. Network Propagation

Nelson acknowledges that the distributed network is inherently imperfect:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

Content is immediately available at the local server after insertion. But network-wide availability depends on the BEBE protocol's forwarding and subrepresentation mechanisms, which propagate incrementally:

> "Whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

## Summary

| Aspect | Guaranteed? |
|--------|-------------|
| I-address permanently assigned at insertion | **Yes** — by architecture |
| Content never overwritten in Istream | **Yes** — by append-only design |
| Immediately retrievable on local server | **Yes** — by "pounce" model |
| Immediately retrievable network-wide | **No** — propagation delay |
| No possibility of loss (bit-level) | **No** — explicitly disclaimed [LM 5/18] |
| Accessible indefinitely | **Conditional** — requires ongoing storage payment |

Nelson's design *intends* that insertion is a permanent, irrevocable act — the architectural equivalent of writing in ink. But he is honest that the infrastructure beneath this intent is fallible. The permanence guarantee is a **design invariant** (the system is built to preserve it), not a **physical impossibility of loss** (which Nelson acknowledges no system can provide).

The INSERT operation itself [LM 4/66] specifies no atomicity, durability, or acknowledgment semantics. It says what the operation *does* (adds content, shifts V-addresses) but not what happens if the operation is interrupted mid-execution or the server fails before propagation.

NEED_RAW: [4/65-4/67] — The INSERT operation definition on these pages may contain additional detail about operation completion semantics not captured in the curated extracts.

---

## Question 8 [nelson]

> Does the design distinguish between inserting content that is entirely new to the system versus inserting content that already exists elsewhere — and if so, must the operation produce different guarantees for each case?

### Nelson's Answer

## Yes — the distinction is fundamental, and the operations are explicitly separate

Xanadu's design draws a sharp line between inserting new content and incorporating existing content. These are **different FEBE operations** with **different Istream consequences** and **different guarantees**.

### The Two Operations

**INSERT** (and APPEND) — for content new to the system:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

**COPY** — for content that already exists elsewhere:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

Note the parameter difference: INSERT takes a `<text set>` (raw content). COPY takes a `<spec set>` (addresses of existing content).

### Different Istream Guarantees

The consequences for Istream are opposite:

| Guarantee | INSERT | COPY |
|-----------|--------|------|
| **New I-addresses created?** | Yes — fresh, unique | No — references existing ones |
| **Home document** | The inserting document | The *original* document |
| **Native bytes?** | Yes — "native bytes of a document are those actually stored under its control" [LM 4/11] | No — "Non-native byte-spans are called inclusions or virtual copies" [LM 4/11] |
| **Attribution** | You are the originator | Original author retains attribution |
| **Royalties** | Accrue to you | Accrue to original owner |

Nelson is explicit about the native/non-native distinction:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

### Identity Is Based on Creation, Not Value

This is the deepest consequence. Two INSERTs of identical text produce **different I-addresses**. A COPY of existing text produces a reference to the **same I-addresses**. The system distinguishes "wrote the same words independently" from "quoted from the original."

This matters for:

- **FINDDOCSCONTAINING** — finds all documents containing content from the same Istream origin. Independent INSERTs of identical text are invisible to each other. COPYs (transclusions) are all discoverable.

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

- **Correspondence** — shared Istream origin is the structural basis for version comparison. COPY preserves correspondence; INSERT creates content with no correspondence to anything.

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

- **Origin traceability** — I-addresses encode the home document. INSERT makes you the home. COPY preserves the original home.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

### The Vstream Is Identical

From the user's perspective, both operations produce the same Vstream effect: content appears at the specified position. The document reads the same either way. But the *structural* properties — attribution, royalties, discoverability, correspondence — differ completely based on which operation was used.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The front end doesn't need to care about the distinction at display time. But the back end must maintain it permanently.

### CREATENEWVERSION as the Extreme Case

The version operation is essentially a whole-document COPY:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The new version shares all I-addresses with the source. No new Istream content is created. This is what enables version comparison — the shared I-addresses ARE the correspondence.

### The Compound Document Model

Nelson's compound document model depends entirely on this distinction:

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

A compound document is a mix of INSERTed content (the author's new words) and COPYed content (transclusions from other documents). The system must distinguish these permanently because:

1. The original owners get royalties for their COPYed portions
2. The compound document owner gets royalties for INSERTed portions
3. Attribution for each byte traces to its actual originator

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

### Summary

The design does not merely distinguish these cases — the distinction is **architecturally load-bearing**. INSERT creates new Istream content with the inserting document as home. COPY creates Vstream mappings to existing Istream content with the original document remaining as home. Every downstream guarantee — attribution, royalties, discoverability, correspondence, version comparison — depends on which operation was used. The Vstream presentation is identical; the Istream identity is fundamentally different.

---

## Question 9 [gregory]

> When INSERT splits an existing POOM bottom crum at the insertion point, does `insertnd` produce exactly two child crums from the original (one for content before, one for content after), or can the split cascade into more fragments?

### Gregory's Answer

## KB Synthesis

The split produces exactly **two** fragments from the original bottom crum, with no further fragmentation of that crum.

## Mechanism

When INSERT at position `v` encounters a bottom crum whose range `[grasp, reach)` straddles the insertion point (`whereoncrum` returns `THRUME`), `makegappm` constructs a **two-blade knife** [SS-TWO-BLADE-KNIFE]:

- `blade[0]` = insertion V-position `v`
- `blade[1]` = next subspace boundary `(N+1).1`

`slicecbcpm` is invoked for `blade[0]` only when `grasp < v < reach` (strictly interior). It cuts the crum into **exactly two pieces**: `[grasp, v)` and `[v, reach)`. A third, separate crum is then allocated for the inserted content `[v, v+width)`. [ST-INSERT / Finding 0062]

The concrete example from the KB confirms this count:

```
INSERT "X" at 1.3 into crum₁ [1.1, 1.6):
  crum₁ → [crum₂: 1.1..1.3, crum₃: 1.4..1.6]   (two fragments)
  new crum₄: [1.3..1.4) for "X"                  (the insert content)
  crums = 3  (Δ = +2)
```

## Why Only Two Fragments

`blade[1]` is placed at the **next subspace boundary**, not within the current crum. Since a well-formed bottom crum cannot span across subspace boundaries (that would violate [INV-SUBSPACE-CONVENTION]), `blade[1]` never falls interior to the same crum that `blade[0]` is cutting. Each blade independently calls `slicecbcpm` only when `THRUME` — and a single crum can satisfy `THRUME` for at most one blade. [SS-TWO-BLADE-KNIFE / Finding 0054, PRE-DELETE / Finding 0075]

## B-tree Structural Splits Are Separate

Parent-level B-tree splits (`splitcrumupwards`) **can** cascade upward through internal nodes when a parent accumulates too many children after receiving the two new bottom crums. [SS-ENFILADE-TREE / Finding 0060] But this reorganizes internal (upper) nodes — it does not re-fragment the bottom crums. The bottom level always ends with exactly the two pieces from the original plus the new insert crum.

## The Coalescing Exception

If the insertion point equals an existing crum's **reach** (`ONMYRIGHTBORDER`), `makegappm` early-exits without cutting at all. [SS-WHEREONCRUM / Finding 0062] `isanextensionnd` then extends the existing crum in place, producing **zero** new crums (Δ = 0). This is the coalescing path for sequential interior typing. [ST-INSERT / Finding 0062]

---

## Code Exploration

Now I have all the information needed to give a complete, cited answer. Let me synthesize the full execution path.

---

## Answer: Two-Fragment or Three-Fragment Split — Both Are Possible, With the Second a True Cascade

### The Execution Path

For a POOM enfilade, `insertnd` [insertnd.c:51–61] does two distinct phases:

1. **`makegappm`** — cuts existing crums to open a gap in V-space
2. **`doinsertnd`** — inserts the new mapping entry into the gap

The question concerns phase 1 only.

---

### Phase 1: `makegappm` Places Two Knives

```c
/* insertnd.c:144-148 */
movetumbler(&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
knives.dimension = V;
makecutsnd(fullcrumptr, &knives);
```

`makegappm` always creates **two** knife blades — not one:

- **`blades[0]`** = the insertion point in V-space
- **`blades[1]`** = a derived second address, computed by `findaddressofsecondcutforinsert` [insertnd.c:174–183]:

```c
/* insertnd.c:174-183 */
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut) {
    tumbler zero, intpart;
    tumblerclear(&zero);
    tumblerincrement(position, -1, 1, secondcut);
    beheadtumbler(position, &intpart);
    tumblerincrement(secondcut, 0, -tumblerintdiff(&intpart, &zero), secondcut);
    tumblerincrement(secondcut, 1, 1, secondcut);
}
```

This produces `blades[1]` as a tumbler address just offset from `blades[0]` — a neighboring fractional address. The function comment says "needs this to give it a place to find intersection of for text is 2.1", implying the second cut is at a sub-integer tumbler address adjacent to the first.

---

### The Cutting Mechanism: `slicecbcpm`

`makecutsnd` → `makecutsdownnd` → `makecutsbackuptohere` reaches the bottom crums. At height 0 [ndcuts.c:77–91]:

```c
/* ndcuts.c:77-91 */
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
            new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
            ...
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
            ivemodified((typecorecrum*)ptr);
            ivemodified((typecorecrum*)new);
            setwisp((typecorecrum*)ptr);
        }
    }
    return(0);
}
```

`slicecbcpm` [ndcuts.c:373–450] always and only produces **exactly two pieces** from one:

```c
/* ndcuts.c:444-448 */
locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, (unsigned)widsize(enftype));
movewisp(&newwid, &ptr->cwid);                    /* ptr = left portion */
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype); /* new starts where ptr ends */
move2dinfo(&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);
adopt(new, RIGHTBRO, ptr);                        /* new is inserted as right sibling */
```

`ptr` becomes the left fragment `[A, blade[i])`, `new` becomes the right fragment `[blade[i], B)`, adopted as `ptr`'s right sibling.

---

### The First Cut Alone Gives Two Fragments — But One More Pass Follows

In the bottom-crum loop, for i=0: if `blades[0]` falls THRUME the original crum, `slicecbcpm` runs, splitting it into:
- `ptr` = `[A, blades[0])` (left fragment)
- `new` = `[blades[0], B)` (right sibling)

Then for i=1: the loop checks `ptr` again against `blades[1]`. Since `ptr` now ends at `blades[0]` and `blades[1] > blades[0]`, `whereoncrum(ptr, ..., blades[1], ...)` returns `TOMYRIGHT` — **not** `THRUME`. The second knife does nothing to `ptr`.

`new` (the right fragment `[blades[0], B)`) is NOT revisited in this inner loop — it was just created and adopted, but the `for (i ...)` loop only operates on the fixed `ptr`.

---

### The Cascade: `makecutsnd`'s Outer Loop Applies the Second Knife to `new`

This is the crucial mechanism. Back in `makecutsnd` [ndcuts.c:15–31]:

```c
/* ndcuts.c:22-27 */
makecutsdownnd(fullcrumptr, &offset, knives);
clear(&offset, sizeof(offset));
for (fullcrumptr = findfullcrum((typecorecrum*)fullcrumptr);
     sonsarecut(fullcrumptr, &offset, knives);
     fullcrumptr = findfullcrum((typecorecrum*)fullcrumptr)) {
    clear(&offset, sizeof(offset));
    makecutsdownnd(fullcrumptr, &offset, knives);
}
```

`sonsarecut` [ndcuts.c:359–371] scans all siblings under the intersection node:

```c
/* ndcuts.c:359-371 */
bool sonsarecut(typecuc *ptr, typewid *offset, typeknives *knives) {
    prologuend((typecorecrum*)ptr, offset, &grasp, (typedsp*)NULL);
    for (son = ...; son; son = ...) {
        if (crumiscut(son, &grasp, knives))
            return(TRUE);
    }
    return(FALSE);
}
```

After the first pass, `new` = `[blades[0], B)` is now a son. If `blades[1]` falls strictly inside `[blades[0], B)` — meaning `blades[0] < blades[1] < B` — then `crumiscut` returns TRUE for `new`, and `sonsarecut` returns TRUE.

A **second pass** of `makecutsdownnd` then finds `new` and calls `makecutsbackuptohere(new, ...)`. This time, for i=1, `blades[1]` IS `THRUME` through `new`, and `slicecbcpm` runs again:

- `new` → `[blades[0], blades[1])` (middle fragment)
- `new2` → `[blades[1], B)` (right fragment)

---

### Result: Three Fragments from One Original

When the insertion point falls strictly inside an existing POOM bottom crum and both knives intersect it (i.e., `blades[0]` and `blades[1]` both lie within `[A, B)`):

| Fragment | V-range | Source |
|---|---|---|
| Left piece | `[A, blades[0])` | first `slicecbcpm` pass on original |
| Middle piece | `[blades[0], blades[1])` | second `slicecbcpm` pass on right fragment |
| Right piece | `[blades[1], B)` | right sibling created in second pass |

**The original crum is replaced by three crums, not two.** The cascade is real — it is driven by the outer `sonsarecut` loop in `makecutsnd` re-running `makecutsdownnd` until no sons remain THRUME by any knife.

---

### When Only Two Fragments Result

If `blades[0]` falls THRUME an existing crum but `blades[1]` does **not** (e.g., `blades[1] >= B`), then only the first knife cuts, and exactly two fragments result. This occurs when the original crum's V-range is narrow — wide enough to include the insertion point but not the second cut address.

Similarly, if the insertion is at the exact **left boundary** of a crum (`whereoncrum` returns `ONMYLEFTBORDER`, not `THRUME`), no slicing occurs at all — the crum is simply a candidate for displacement adjustment in `makegappm`'s post-cut shift loop.

---

### The Maximum Fragment Count Per Original Crum

With exactly `nblades = 2` [insertnd.c:146], at most **two** cuts can apply to any single crum, yielding at most **three** fragments. The split does **not** cascade further because:

1. `slicecbcpm` always produces exactly two pieces per call — it is not self-recursive.
2. `makegappm` fixes `knives.nblades = 2` unconditionally — no additional knives are added mid-operation.
3. After three fragments exist (`[A, b0)`, `[b0, b1)`, `[b1, B)`), none of them is THRUME by either knife, so `sonsarecut` returns FALSE and the loop terminates.

The structural tree-rebalancing (`splitcrumupwards` [split.c:16], `levelpush` [genf.c:263]) that may follow is a b-tree overflow response — it reorganizes parent nodes but does NOT further fragment the content-carrying bottom crums.

---

### Summary

> **The split can cascade to produce exactly three fragments from one original crum** when both knife blades (`blades[0]` at the insertion point and `blades[1]` from `findaddressofsecondcutforinsert`) fall inside the original crum's V-range. Each individual `slicecbcpm` call strictly produces two pieces; the cascade comes from the outer `sonsarecut` loop in `makecutsnd` driving a second pass. The maximum is three fragments — the architecture is bounded by `knives.nblades = 2`.

---

## Question 10 [gregory]

> How does `findaddressofsecondcutforinsert` compute the second blade tumbler from the insertion V-address — does it increment the first mantissa digit (e.g., V:1.3 → blade at 2.0), or does it use a different rule when the insertion is deeper in the tumbler hierarchy (e.g., V:1.1.0.2.0.5)?

### Gregory's Answer

## KB Synthesis

## How `findaddressofsecondcutforinsert` Computes the Second Blade

The algorithm always produces `(N+1).1` where `N` is the **first mantissa digit** (the subspace digit) of the insertion address — regardless of how deep the tumbler is. [SS-TWO-BLADE-KNIFE]

### The Four-Step Algorithm

For an insertion at V-address `N.x` (where `.x` may be arbitrarily long, e.g., `1.1.0.2.0.5`):

1. **Increment first digit**: `N.x → (N+1).x`  
2. **Behead** (strip first digit to get fractional tail): `N.x → 0.x`  
3. **Subtract fractional part**: `(N+1).x − 0.x = (N+1).0`  
4. **Add 1 at second digit**: `(N+1).0 → (N+1).1`

Steps 2–3 strip the entire fractional tail regardless of its length. Only the first digit survives.

### Concrete Examples

| Insertion address | N | Second blade |
|---|---|---|
| `1.3` | 1 | `2.1` |
| `1.1.0.2.0.5` | 1 | `2.1` |
| `2.5` | 2 | `3.1` |
| `3.7` | 3 | `4.1` |

The source comment confirms the design intent: *"needs this to give it a place to find intersectionof for text is 2.1"* — for all text-subspace insertions (first digit = 1), the blade is always `2.1`, regardless of fractional depth. [SS-TWO-BLADE-KNIFE]

### Significance

This means the shift region `[blade[0], blade[1])` is always bounded to the current subspace. An insertion at `1.1.0.2.0.5` shifts only entries in `[1.1.0.2.0.5, 2.1)` — entirely within the text subspace — and never touches link entries at `2.x`. This is the structural mechanism behind [FC-SUBSPACE]'s subspace isolation guarantee for INSERT.

---

## Code Exploration

I have everything needed. Here is the complete answer.

---

## How `findaddressofsecondcutforinsert` computes the second blade

### The function (insertnd.c:174–183)

```c
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut)
{    /*needs this to give it a place to find intersectionof for text is 2.1*/
  tumbler zero, intpart;

       tumblerclear (&zero);
       tumblerincrement (position, -1, 1, secondcut);   // line 179
       beheadtumbler (position, &intpart);              // line 180
       tumblerincrement(secondcut,0,-tumblerintdiff(&intpart,&zero),secondcut); // line 181
       tumblerincrement (secondcut, 1, 1, secondcut);   // line 182
}
```

Called from `makegappm` [insertnd.c:145] which places the first blade at the raw insertion V-address and asks this function to compute the second. The caller:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);
```

---

### Tumbler representation

`mantissa[0]` is the most-significant digit (highest level), `mantissa[1]` the next, etc. `exp = 0` for normal addresses. `nstories` = index of last non-zero digit + 1. So V:1.3 → `mantissa=[1,3,0,…]`, V:1.1.0.2.0.5 → `mantissa=[1,1,0,2,0,5,0,…]`.

`tumblerincrement(aptr, rightshift, bint, cptr)` [tumble.c:599–622]:
- Finds `idx` = index of the last non-zero mantissa digit [tumble.c:611]
- Adds `bint` to `mantissa[idx + rightshift]` [tumble.c:621]
- `rightshift = -1` → modifies the digit **one slot left** of the last digit (the parent level)
- `rightshift = 0` → modifies the last digit itself
- `rightshift = +1` → writes a **new sub-digit** one slot right of the last digit

`beheadtumbler(aptr, bptr)` [tumble.c:673–683]: strips the first digit, returning the remainder. For V:1.3 → returns 3. For V:1.1.0.2.0.5 → returns 1.0.2.0.5.

`tumblerintdiff(aptr, bptr)` [tumble.c:591–597]: returns `(a−b).mantissa[0]`, i.e. the first digit of the difference. Used here with `bptr = zero`, so it just returns `intpart.mantissa[0]` = the second digit of `position`.

---

### Step-by-step trace for V:1.3

`position = [1, 3, 0, …]`, `idx` of last non-zero = 1.

**Line 179** — `tumblerincrement(position, −1, 1, secondcut)`:
- `idx = 1`, add 1 to `mantissa[1−1] = mantissa[0]`
- `secondcut = [2, 3, 0, …]` = V:2.3

**Line 180** — `beheadtumbler(position, &intpart)`:
- Zeros `mantissa[0]` of position, justifies → `intpart = [3, 0, …]` = 3
- `tumblerintdiff(intpart, zero)` = 3

**Line 181** — `tumblerincrement(secondcut, 0, −3, secondcut)`:
- `secondcut = [2, 3, 0, …]`, `idx = 1`
- Add −3 to `mantissa[1]`: 3 − 3 = 0
- `secondcut = [2, 0, …]` = 2

**Line 182** — `tumblerincrement(secondcut, +1, 1, secondcut)`:
- `secondcut = [2, 0, …]`, `idx = 0`
- Add 1 to `mantissa[1]`
- `secondcut = [2, 1, 0, …]` = V:2.1

**Result: V:1.3 → second blade at V:2.1**, matching the embedded comment.

For any two-level address V:M.N (any N): line 179 increments `mantissa[0]` to M+1 (because rightshift=-1 on idx=1 hits index 0); line 181 then subtracts exactly N from the last digit, zeroing it; line 182 appends .1. **The final digit N is always cancelled out.** The result is V:(M+1).1 regardless of N.

---

### Step-by-step trace for V:1.1.0.2.0.5

`position = [1, 1, 0, 2, 0, 5, 0, …]`, last non-zero at `idx = 5`.

**Line 179** — `tumblerincrement(position, −1, 1, secondcut)`:
- `idx = 5`, add 1 to `mantissa[5−1] = mantissa[4]`
- `mantissa[4]` was 0, becomes 1
- `secondcut = [1, 1, 0, 2, 1, 5, 0, …]`

**Line 180** — `beheadtumbler([1,1,0,2,0,5,…], &intpart)`:
- Zeros `mantissa[0]`, justifies: `intpart = [1, 0, 2, 0, 5, …]` = 1.0.2.0.5
- `tumblerintdiff(intpart, zero)` = **1** (= `position`'s second digit, `d₂`)

**Line 181** — `tumblerincrement(secondcut, 0, −1, secondcut)`:
- `secondcut = [1, 1, 0, 2, 1, 5, …]`, `idx = 5`
- Add −1 to `mantissa[5]`: 5 − 1 = 4
- `secondcut = [1, 1, 0, 2, 1, 4, 0, …]`

**Line 182** — `tumblerincrement(secondcut, +1, 1, secondcut)`:
- `idx = 5`, add 1 to `mantissa[6]`
- `secondcut = [1, 1, 0, 2, 1, 4, 1, 0, …]`

**Result: V:1.1.0.2.0.5 → second blade at V:1.1.0.2.1.4.1**

This is a 7-level tumbler. The algorithm does **not** touch the first digit at all for deep tumblers.

---

### General rule for a k-level tumbler V:d₁.d₂.d₃…dₖ

Let `idx = k−1` (zero-based index of last non-zero digit).

| Step | Operation | Net effect on mantissa |
|---|---|---|
| Line 179 | `rightshift=−1` on idx | `mantissa[k−2] += 1` (penultimate digit++) |
| Line 180 | behead position | `intpart.mantissa[0] = d₂` |
| Line 181 | `rightshift=0`, add `−d₂` | `mantissa[k−1] −= d₂` (last digit adjusted) |
| Line 182 | `rightshift=+1`, add 1 | new `mantissa[k] = 1` (new sub-digit appended) |

The second blade is:

```
V: d₁ . d₂ . … . d_{k-2} . (d_{k-1}+1) . (d_k − d₂) . 1
```

(with a special case when `d_k − d₂ = 0`: the zero digit collapses and the .1 lands one level higher.)

For **two-level** V:M.N: `d₁=M`, `d₂=N`, `k=2`, `d_{k−1}=d₁=M`, `d_k=d₂=N`:
- Penultimate = `mantissa[0]` → M+1
- Last digit: N − N = 0 (collapses)
- Appended .1 lands at index 1
- **Result: V:(M+1).1** — the last digit is always erased, first digit incremented

For **deep** V:1.1.0.2.0.5: `d₂=1`, penultimate `d₅=0→1`, last `d₆=5→4`, appended .1:
- **Result: V:1.1.0.2.1.4.1** — the first digit is untouched; the second-to-last digit is bumped, the last digit shrinks by `d₂`, then `.1` is appended

### Summary

The function does **not** simply increment the first mantissa digit. The "increment first digit, reset to .1" shorthand is only accurate for two-level (one-dot) tumblers. For deeper tumblers the rule is: **increment the penultimate digit, subtract the second digit from the last digit, append .1**. The amount subtracted at line 181 is always `d₂` — the digit immediately after the top-level digit of the original insertion address. For deep tumblers where `d₂ < d_k`, this creates a compound sub-address at the end rather than collapsing it cleanly to .1.

---

## Question 11 [gregory]

> When `isanextensionnd` detects the ONMYRIGHTBORDER case and coalesces a new insert into an existing crum, does it modify the existing crum's V-width and I-width in place, or does it replace the crum with a new one carrying the extended range?

### Gregory's Answer

## KB Synthesis

The KB is explicit on this: `isanextensionnd` triggers **in-place modification** of the existing crum — no replacement occurs.

From [ST-INSERT] (Finding 0062):

> When `isanextensionnd()` returns TRUE (same `homedoc`, `reach == origin`), **the existing crum's width is extended in place** at `insertnd.c:243`. No new crum is allocated.

The postcondition stated there is:

> `crum.width' = crum.width + content.width ∧ crum.grasp' = crum.grasp ∧ num_crums' = num_crums`

So the grasp (left boundary) is unchanged, the width grows rightward, and the total crum count is unaffected (`Δ = 0`). A new crum is only created at `insertnd.c:252-260` when `isanextensionnd` returns FALSE.

Since POOM bottom crums carry dual-space coordinates ([SS-POOM-BOTTOM-CRUM]), both the V-width and I-width fields of the existing crum must be updated to reflect the larger range, consistent with [INV-WIDTH-VALUE-EQUIVALENCE] (both encode the same integer value at different tumbler precisions). The [SS-INSERT-VWIDTH-ENCODING] entry describes how the V-width is re-encoded from the I-width's integer value, so the in-place update applies the same encoding logic used at original crum creation.

---

## Code Exploration

I now have a complete picture of the execution path. Here is the full answer.

---

## Answer: `isanextensionnd` and the ONMYRIGHTBORDER Coalescing Case

The existing crum is **modified in place**. No new crum is allocated. No replacement occurs.

---

### 1. What `isanextensionnd` actually tests

**`insertnd.c:301-309`**:
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

`prologuend` (`retrie.c:334-339`) computes:
- `grasp = offset + ptr->cdsp` — absolute start of the crum
- `reach = grasp + ptr->cwid` — absolute end of the crum (its right border)

Then `lockeq(reach.dsas, originptr->dsas, dspsize(enftype))` (`wisp.c:261-267`) performs element-wise tumbler equality across all dimensions. For SPAN and POOM, `dspsize = 2` (`wisp.h:24-27`), so both the I and V tumbler components must match.

The function returns TRUE only when the new insertion's origin equals the crum's right border — i.e., the new content begins exactly where the existing crum ends. This is the ONMYRIGHTBORDER condition.

---

### 2. What happens when it returns TRUE

The caller is `insertcbcnd` (`insertnd.c:249-258`):

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // line 251
        ivemodified (ptr);                                               // line 252
        setwispupwards (father,1);                                       // line 253
        if(!isfullcrum((typecorecrum*)father)){
            return(setwispupwards(findfather((typecorecrum*)father),1));
        }
        return(FALSE);
    }
}
```

**Line 251** — `dspadd`:

```c
// wisp.c:15-18
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype)
{
    lockadd (a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

Called as `dspadd(&ptr->cwid, width, &ptr->cwid, ...)`. This is `c = a + b` with `c == a` — the destination is the same as the first operand. `lockadd` iterates across `dspsize` tumblers, adding each component of `width` to the corresponding component of `ptr->cwid` and writing the result back into `ptr->cwid`. For SPAN/POOM (`dspsize = 2`, `wisp.h:24-27`), both the I-width (`dsas[0]`) and V-width (`dsas[1]`) are extended simultaneously by the incoming width's respective components.

**Line 252** — `ivemodified(ptr)` marks the existing crum as dirty so it gets flushed to disk.

**No new crum is created.** `createcrum` at `insertnd.c:260` is only reached when the `for` loop exhausts all siblings without finding an extension match:

```c
new = createcrum (0, (INT)father->cenftype);   // line 260 — NOT reached on extension
reserve (new);
adopt (new, SON, (typecorecrum*)father);
...
```

---

### 3. What is and is not changed on the existing crum

| Field | Changed? |
|-------|----------|
| `ptr->cwid` (V-width and I-width) | **Yes** — extended by `dspadd` |
| `ptr->cdsp` (displacement / start position) | **No** — not touched |
| `ptr->c2dinfo.homedoc` (home document) | **No** — equality was the gate |
| Crum identity / tree position | **No** — same node, same siblings |

The crum's right edge moves outward (its width grows); its left edge (encoded in `cdsp`, relative to parent grasp) stays fixed. The crum is neither replaced nor moved in the sibling chain.

---

### Summary

`isanextensionnd` detects the ONMYRIGHTBORDER case by checking `lockeq(reach, origin)` — that the new insertion begins exactly at the existing crum's right edge. When it matches, `insertcbcnd` performs a **direct in-place field update**: `dspadd(&ptr->cwid, width, &ptr->cwid, ...)` widens both I and V components of the existing crum's width in a single operation, marks it modified, and returns without allocating any new crum. The crum is extended, not replaced.

---

## Question 12 [gregory]

> If you insert at a V-position beyond the current document extent (e.g., document spans V:[1.1,1.5] and you insert at V:1.100), does `makegappm` still execute a shift pass over all POOM entries, or does it detect the absence of entries at or beyond the target and skip shifting?

### Gregory's Answer

## KB Synthesis

## Behavior: Insert Beyond Document Extent

The POOM traversal still executes, but **shifting is completely bypassed** — not because a detection optimization exists, but because two independent guards both fire.

### Guard 1: `makegappm` early exit

From **[SS-WHEREONCRUM]** / **[PRE-INSERT]** Finding 0062, `makegappm` has a compound early-exit at its top:

```c
if (iszerotumbler(&fullcrumptr->cwid.dsas[V])
    || tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS
    || tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);
```

The third clause fires when `origin >= reach`. For any existing crum covering `[1.1, 1.5)` with reach `= 1.5`, inserting at `1.100` satisfies `1.100 > 1.5`, so `tumblercmp(1.100, 1.5) != LESS` is TRUE. `makegappm` returns 0 immediately — **no knife is constructed, no cuts are scheduled**.

### Guard 2: `insertcutsectionnd` case classification

Even if the knife were constructed, from **[ST-INSERT]** / **[FC-SUBSPACE]** Finding 0054, the two-blade knife would have:
- `blade[0]` = 1.100 (insertion point)
- `blade[1]` = 2.1 (next subspace boundary)

`insertcutsectionnd` classifies all existing crums (which sit at positions `< 1.100`) as **case 0** (before `blade[0]`). Case 0 means: no shift. The shift formula `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])` is never called.

### What does happen

The B-tree traversal proceeds normally to find the insertion position. `isanextensionnd()` **[ST-INSERT]** Finding 0062 checks whether `new_origin == existing_crum.reach`. Since `1.100 ≠ 1.5`, no coalescing occurs. A **new bottom crum** is allocated at `[1.100, 1.100 + insert_width)`, becoming a new sibling of the existing crums.

From **[SS-ENFILADE-TREE]** Finding 0058, this may trigger `splitcrumupwards` if the parent exceeds its branching limit, but that is purely structural — no content shifting.

### Net result

Inserting beyond the current document extent:
1. Creates a gap in V-space (positions 1.5 through 1.100 are unoccupied)
2. Performs **zero shift operations** on existing crums
3. Allocates a new crum at the target position

The document's vspanset will subsequently report two separate spans: the original `[1.1, 1.5)` and the new `[1.100, ...]`, not a single consolidated span — because **[INV-VSPAN-CONSOLIDATION]** only consolidates spans that are actually contiguous in both V-space and I-space.

---

## Code Exploration

I have everything needed to answer definitively. Here is the full analysis.

---

## Answer: `makegappm` Detects Out-of-Range Origin and Returns Early — No Shift Pass Executes

### The Guard Clause

`makegappm` [`insertnd.c:124`] opens with a three-part early-return condition evaluated **before** it does any work:

```c
/* insertnd.c:138-143 */
clear (&offset, sizeof(offset)); /* fullcrum always has zero offset */
prologuend ((typecorecrum*)fullcrumptr, &offset, &grasp, &reach);
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

### What `prologuend` Computes

`prologuend` [`makeroom.c:334-339`] is:

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

Called with `offset = 0`:
- `grasp = 0 + fullcrumptr->cdsp` → the **V-start** of the document (e.g., V:1.1)
- `reach = grasp + fullcrumptr->cwid` → the **V-end** of the document (e.g., V:1.5, exclusive upper bound)

### Applying the Guard to Your Scenario

Document spans V:[1.1, 1.5]; insert origin = V:1.100 (second tumbler digit 100 >> 5).

| Sub-condition | Evaluation | Why |
|---|---|---|
| `iszerotumbler(&fullcrumptr->cwid.dsas[V])` | FALSE | Document has non-zero width |
| `tumblercmp(&origin[V], &grasp[V]) == LESS` | FALSE | V:1.100 > V:1.1 (100 > 1 in 2nd digit) |
| `tumblercmp(&origin[V], &reach[V]) != LESS` | **TRUE** | V:1.100 > V:1.5 (100 > 5 in 2nd digit), so result is `GREATER`, and `GREATER != LESS` |

The third sub-condition fires. The `if` is true. `makegappm` executes `return(0)` at line 143.

### What Is Skipped

Everything after line 143 does not execute:

- `makecutsnd` [`insertnd.c:148`] — no cuts are made at the insertion point
- `newfindintersectionnd` [`insertnd.c:149`] — no father node is found
- The sibling loop [`insertnd.c:151-169`] — **no shift pass runs**
- `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], ...)` [`insertnd.c:162`] — no displacement adjustments are applied

### Why This Is Correct

The comment names it precisely: _"this if for extensions to bc without calling cut"_. An insertion **beyond** the current document's reach is a pure extension — no existing POOM entry sits at or to the right of V:1.100, so there is nothing to shift rightward. Shifting is only needed when inserting **within** `[grasp, reach)`. The guard encodes exactly that interval check: the shift pass is gated by `origin ∈ [grasp, reach)`. Origin at or past `reach` → unconditional early return.

### Summary

**Yes — `makegappm` detects the absence.** It does so via an explicit range check at [`insertnd.c:140-143`]: if `origin ≥ reach` (i.e., beyond the current document's V-extent), it returns 0 immediately. The entire shift pass — cuts, intersection finding, and sibling displacement — is skipped. No POOM entries are touched.

---

## Question 13 [gregory]

> When multiple characters are inserted one at a time at successive V-positions (interior typing: first at V:1.3, then V:1.4, then V:1.5), the KB says the first costs +2 crums and subsequent ones cost +0 — does the coalescing depend on the new I-address being exactly `previous_I-address + 1`, and would a CREATELINK between single-character inserts break the coalescing chain?

### Gregory's Answer

## KB Synthesis

Yes to both.

## Coalescing requires exact I-address contiguity

The `isanextensionnd()` check has two conditions [ST-INSERT, Finding 0062]:
1. `new_content.homedoc == crum.homedoc`
2. `new_content.origin == crum.reach` — the new I-address must equal exactly the existing crum's right endpoint

Since I-address allocation is `findpreviousisagr → tumblerincrement(max, 0, 1)` [SS-ADDRESS-SPACE, Finding 0033], sequential text inserts get I.n, I.n+1, I.n+2, etc. Each insert's `origin` equals the previous crum's `reach`, so coalescing fires. But this is a strict equality test — any gap breaks it.

## CREATELINK breaks the chain

[INT-LINK-INSERT, Finding 0063] documents this directly: `createorglingranf()` (called by CREATELINK) allocates a link orgl I-address via the same `findisatoinsertgr` mechanism, consuming space in the shared monotonic sequence. After:

```
INSERT "A"    → I.1 allocated, crum covers [I.1, I.2)
CREATELINK    → link orgl allocated at I.2 (or nearby higher range)
INSERT "B"    → findpreviousisagr returns the link orgl's address as max
               → "B" gets I.3 (or higher), NOT I.2
```

Now `new_content.origin = I.3` but `crum.reach = I.2`. The equality fails, `isanextensionnd()` returns FALSE, a new crum is created. This costs the full +2 (split + new crum).

The refined crum bound from [ST-CRUM-BOUND, Finding 0063] captures this:

```
c ≤ 1 + 2C + 2L + 3R + 3P
```

where L counts interleaved CREATELINK operations — each is an "invisible cursor repositioning" from the I-address allocator's perspective.

[INV-MONOTONIC, Finding 0063] confirms the mechanism: CREATELINK is not in the granfilade-preserving set `{DELETE, REARRANGE}`. It modifies the granfilade by adding an orgl entry, permanently advancing the maximum I-address. Subsequent text inserts start a fresh, non-contiguous I-address run.

---

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## Does Coalescing Require Exact I-Address Adjacency, and Does CREATELINK Break It?

### 1. The Extension Check Is 2D — Both V and I Must Be Adjacent

The coalescing decision lives in `isanextensionnd` (`insertnd.c:301-309`):

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

`prologuend` computes `reach = grasp + width` for both dimensions (`retrie.c:334-338`). `lockeq` (`wisp.c:261-267`) iterates through `loxize` tumblers and returns TRUE only if **every one** matches:

```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize) {
    while (loxize--)
        if (!tumblereq (lock1++, lock2++))
            return(FALSE);
    return(TRUE);
}
```

For a POOM crum, `dspsize(POOM) = DSPSIZEPM = 2` (`wisp.h:26`). The DSP has two slots: `dsas[V]` and `dsas[I]`. So `lockeq` checks **both** V and I simultaneously:

- `reach.dsas[V] == origin.dsas[V]` — new V-position must be exactly one past the previous crum's V-end
- `reach.dsas[I] == origin.dsas[I]` — new I-address must be exactly one past the previous crum's I-end

**Yes — coalescing is strictly conditional on `new_I == previous_I + previous_W_I`, which for single-character inserts means `new_I == previous_I + 1` exactly.**

### 2. Consecutive Text Inserts Produce Consecutive I-Addresses

`doinsert` (`do1.c:87-123`) calls `inserttextingranf` → `inserttextgr` → `findisatoinsertgr` → `findisatoinsertmolecule` (`granf2.c:158-181`) to allocate the I-address:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);                        // first text ever
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);               // subsequent text
    } ...
```

For TEXTATOM (`xanadu.h:145: #define TEXTATOM 1`):
- `upperbound = docisa.0.(TEXTATOM+1) = docisa.0.2`
- `findpreviousisagr` returns the **last ISA below `docisa.0.2`** — i.e., the address of the last character written
- `findlastisaincbcgr` (`granf2.c:280-284`) adjusts for multi-char GRANTEXT crums: `tumblerincrement(offset, 0, textlength - 1, offset)` — so the returned `lowerbound` is the address of the last individual character
- Then: `isaptr = lowerbound + 1` (`granf2.c:169`)

The new I-address is always exactly `previous_last_char + 1`. This is the chain that makes coalescing work.

### 3. CREATELINK Allocates I-Addresses in a Separate Zone

`docreatelink` (`do1.c:195-220`) calls:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)   // allocates link ISA
     ...
     && docopy (taskptr, docisaptr, &linkvsa, ispanset)       // places link ref in POOM
     ...
);
```

For LINKATOM (`xanadu.h:146: #define LINKATOM 2`), `findisatoinsertmolecule` uses:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// upperbound = docisa.0.(LINKATOM+1) = docisa.0.3
```

And the LINKATOM branch allocates at `docisa.0.2.*`.

**Critical isolation**: when the text allocator runs its `findpreviousisagr` with `upperbound = docisa.0.2`, it searches for the greatest ISA strictly less than `docisa.0.2`. Link ISAs live at `docisa.0.2.*` — which are all **greater** than `docisa.0.2` — so they are completely excluded from the text search. Link allocation and text allocation are in disjoint tumbler zones and never interfere.

### 4. CREATELINK's POOM Crum Is Moved Before Extension Checking

`findnextlinkvsa` (`do2.c:151-167`) places the link's document reference at the current document V-reach:

```c
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);
else
    movetumbler (&vspanreach, vsaptr);   // link goes at end of document
```

After INSERT at V:1.3 (width 1), the document reach is V:1.4. So the link reference lands at **V:1.4** in the POOM (I = link_ISA in `docisa.0.2.*`).

When the next INSERT at V:1.4 executes, `insertnd` for POOM runs in this order (`insertnd.c:53-61`):

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);   // 1st: shifts link crum V:1.4 → V:1.5
    ...
    bothertorecombine=doinsertnd(...);                 // 2nd: then checks extension
```

`makegappm` adjusts the `cdsp.dsas[V]` of any crum straddling the insertion point (`insertnd.c:162-164`):

```c
case 1:
    tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
```

Only the V dimension is shifted. The link crum moves from V:1.4 to V:1.5. Its I-address (`docisa.0.2.*`) is untouched.

Then `insertcbcnd` → `isanextensionnd` checks each crum. For the previous text "a" crum:
- `reach.dsas[V]` = 1.3 + 1 = **1.4** ✓ (matches new V-origin 1.4)
- `reach.dsas[I]` = I₀ + 1 = **I₁** ✓ (matches new I-address I₁ = I₀+1)

The `isanextensionnd` check for the link crum would fail: its `reach.I = docisa.0.2.*` ≠ I₁ = `docisa.0.1.*+1`, so it is never mistaken for a text extension.

**Result: coalescing succeeds. The second text insert costs +0 crums.**

### Summary

| Condition | Result |
|-----------|--------|
| Coalescing test | Both V AND I must be exactly adjacent (`isanextensionnd` via `lockeq` with `DSPSIZEPM=2`, `insertnd.c:308`) |
| New I-address | Always `previous_last_char + 1` (`granf2.c:169`) for consecutive text inserts to same document |
| LINKATOM zone | `docisa.0.2.*` — separated from TEXTATOM zone `docisa.0.1.*` by the `upperbound = docisa.0.2` search boundary (`granf2.c:162`) |
| CREATELINK V-crum interference | Resolved by `makegappm` running before `doinsertnd` (`insertnd.c:54, 57`); link crum is shifted out of V:1.4 before the extension check runs |
| CREATELINK effect on I-address sequence | **None** — link ISAs are in a disjoint tumbler zone, invisible to text ISA allocation |

**CREATELINK between single-character inserts does NOT break the coalescing chain.** The text I-address sequence (`docisa.0.1.*`) is monotonically allocated regardless of intervening link operations, and `makegappm` evacuates the link's V-crum before extension checking. The coalescing holds as long as the client presents consecutive V-positions — the interleaved CREATELINK is irrelevant to that test.

---

## Question 14 [gregory]

> Does `makegappm` shift POOM entries by adding the insertion width to their V-displacement using `tumbleradd`, and if so, does it operate on the relative displacement stored in each crum or on the absolute V-address computed during traversal?

### Gregory's Answer

## KB Synthesis

Yes on both counts, and the answer is **relative displacement**.

## `makegappm` shifts relative `cdsp` directly

From [SS-TWO-BLADE-KNIFE] and [ST-INSERT] (Finding 0054), `makegappm` uses a two-blade knife to classify POOM crums into three cases via `insertcutsectionnd`:

- Case 0: crum is before `blade[0]` — no shift
- Case 1: crum is between `blade[0]` and `blade[1]` — **shifted**
- Case 2: crum is at or beyond `blade[1]` — no shift

The shift is applied at [ST-INSERT] (Finding 0054), citing `insertnd.c:162`:

```c
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])
```

This operates directly on `ptr->cdsp.dsas[V]` — the **relative displacement** stored in each crum, not the absolute V-address.

## Why relative, not absolute

From [SS-ENFILADE-TREE] (Finding 0066), 2D enfilades (POOM and SPAN) use coordinate-transform-based displacement. Each crum's `cdsp` is stored **relative to its parent's grasp**, not as an absolute V-address. The root's `cdsp` holds the minimum address across all content; children store offsets relative to that. During retrieval, `prologuend` computes `grasp = offset + ptr->cdsp` by accumulating ancestor displacements ([SS-ENFILADE-TREE] Finding 0066, `retrie.c:334-339`).

Since `cdsp` is relative, adding `width` to `cdsp` correctly shifts the crum's absolute position without needing to know the full ancestor chain. After modification, `setwispupwards` recalculates the root's displacement from the new minimum across all children, adjusting relative displacements accordingly ([ST-INSERT] Finding 0066).

## The second blade enforces subspace isolation

From [SS-TWO-BLADE-KNIFE] (Finding 0054), `blade[1]` is always `(N+1).1` for an insertion at `N.x`. This means:

- INSERT at `1.x` → `blade[1] = 2.1` → only crums with `cdsp` in `[1.x, 2.1)` are shifted
- Crums at `2.x` (link subspace) have absolute positions ≥ `2.1`, so `whereoncrum` returns `ONMYLEFTBORDER` or `TOMYRIGHT` relative to `blade[1]`, classifying them as case 2 — **no shift**

This is the structural mechanism behind [FC-SUBSPACE]: INSERT at `1.x` cannot shift link crums at `2.x`. [FC-SUBSPACE] (Finding 0055) notes that DELETE achieves the same isolation incidentally through `strongsub`'s exponent guard, but INSERT's isolation is deliberate by design.

## Summary

`makegappm` adds `width->dsas[V]` to `ptr->cdsp.dsas[V]` (the stored **relative** displacement) for every crum classified as case 1 (between the two blades). Crums outside the blade range — including all crums in other subspaces — are untouched. After all shifts, `setwispupwards` re-anchors the tree by recalculating the root displacement from the new minimum.

---

## Code Exploration

I now have all the data needed. Here is the full answer.

---

## Does `makegappm` shift POOM entries with `tumbleradd`, and on what does it operate?

### Short answers

1. **Yes**, `makegappm` uses `tumbleradd` to shift POOM entries — but only a narrow subset of them (case-1 crums, defined precisely below).
2. It operates on the **relative displacement** stored in each crum (`ptr->cdsp.dsas[V]`), not on the absolute V-address. The absolute position (`fgrasp`) is computed and used only for **classification**, not for the arithmetic of the shift.

---

### Walking the code

#### 1. `prologuend` computes absolute positions from relative displacements

`retrie.c:334-338`:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd(offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd(grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```
`grasp = offset + ptr->cdsp`. The parent's absolute position (`offset`) plus the crum's stored relative displacement (`ptr->cdsp`) gives the crum's absolute grasp. This confirms that `ptr->cdsp.dsas[V]` is always a **relative** offset from the parent.

#### 2. `whereoncrum` uses the relative displacement to compute the absolute left boundary

`retrie.c:355-362` (SPAN/POOM branch):
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
cmp = tumblercmp(address, &left);
if (cmp == LESS)       return(TOMYLEFT);
else if (cmp == EQUAL) return(ONMYLEFTBORDER);
```
`left = offset + ptr->cdsp.dsas[V]` — the absolute left boundary. This is purely for locating the crum; it does not modify `ptr->cdsp`.

`common.h:86-90` defines the return values:
```c
#define TOMYLEFT        -2
#define ONMYLEFTBORDER  -1
#define THRUME           0
#define ONMYRIGHTBORDER  1
#define TOMYRIGHT        2
```

#### 3. `insertcutsectionnd` classifies each child of `father`

`edit.c:207-233`, with `knives->nblades == 2`, `blade[0] = origin`, `blade[1] = origin+ε`:

```c
// Check blade[1] = origin+ε first
i = 1;
cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
if (cmp == THRUME)           return(-1);   // spans blade[1] — should be impossible after cuts
else if (cmp <= ONMYLEFTBORDER) return(2); // crum's left boundary >= origin+ε → RIGHTWARD

// Then check blade[0] = origin
i = 0;
cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
if (cmp == THRUME)           return(-1);   // spans blade[0] — impossible after cuts
else if (cmp <= ONMYLEFTBORDER) return(1); // crum's left boundary ∈ [origin, origin+ε) → AT the slot

return(0);  // crum's right boundary <= origin → LEFTWARD
```

Meaning:
| Return | Condition on crum's absolute left | Semantic |
|--------|-----------------------------------|---------|
| 0 | `left < origin` | entirely to the left of the insertion point |
| 1 | `origin ≤ left < origin+ε` | sitting in the slot carved by the two cuts |
| 2 | `left ≥ origin+ε` | entirely to the right of both cuts |
| −1 | spans a cut | impossible after `makecutsnd`, causes `gerror` |

#### 4. `makegappm`: the shift is on the stored relative displacement

`insertnd.c:124-172`. The relevant logic after `makecutsnd` and `newfindintersectionnd`:

```c
prologuend((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);  // line 150
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);                      // line 152
    switch (i) {
      case 0:
      case 2:
        break;   // no shift
      case -1:
        gerror("makegappm can't classify crum\n");
      case 1:   /* 9-17-87 fix */
        tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // line 162
        ivemodified(ptr);
        break;
    }
}
```

Line 162 in full:
```c
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
```

The three operands are:
- `ptr->cdsp.dsas[V]` — the **relative** V-displacement stored in the crum (input and output)
- `width->dsas[V]` — the insertion width in V-space

`fgrasp` does not appear in this expression. The absolute position is computed at line 150 and passed to `insertcutsectionnd` at line 152 only for the purpose of classifying whether the child falls in case 0, 1, or 2. Once classification is done, `fgrasp` plays no further role: the shift is computed and stored entirely in the crum's own `cdsp` field.

#### 5. Why only case 1, not case 2?

The two cuts at `origin` and `origin+ε` are designed so that case-1 crums are exactly those with their absolute left boundary AT the insertion slot — content that, before the cut, began at `origin`. These are the crums that were split off from whatever spanned `origin`, and they must move rightward to open space for the new content. Case-2 crums (already starting at `origin+ε` or beyond) lie outside the insertion range because, in the POOM's V-space model, `origin+ε` is already guaranteed to be past the new content's V-extent. The second cut position computed by `findaddressofsecondcutforinsert` (`insertnd.c:145`, `insertnd.c:174-183`) is specifically chosen to create this boundary.

---

### Definitive answers

**Q1: Does `makegappm` shift POOM entries using `tumbleradd`?**

Yes — at `insertnd.c:162` — but only for case-1 crums: those whose absolute left boundary (`fgrasp + ptr->cdsp.dsas[V]`) falls in the half-open interval `[origin, origin+ε)`. Case-0 (left of origin) and case-2 (right of `origin+ε`) crums are untouched.

**Q2: Does it operate on the stored relative displacement or the computed absolute address?**

It operates on the **relative displacement** `ptr->cdsp.dsas[V]` stored directly in the crum. The `tumbleradd` at line 162 has the form:

```
new_cdsp_V = old_cdsp_V + width_V
```

`fgrasp` (the absolute V-position of the father node) is computed at line 150 and used at line 152 solely to let `insertcutsectionnd → whereoncrum` compute each child's absolute left boundary for classification. It is never added to or subtracted from during the shift arithmetic. The stored relative displacement is what gets modified, in place.

---

## Question 15 [gregory]

> After INSERT creates a new POOM entry and shifts existing entries, does `insertnd` trigger `recombinend` (2D rebalancing) or `splitcrumupwards` on the POOM, and what determines which rebalancing path is taken?

### Gregory's Answer

## KB Synthesis

After INSERT, the POOM follows the **split path** (`splitcrumupwards`), not the rebalance path (`recombinend`). Here's the full mechanism:

## INSERT's POOM Update Path

**Step 1 — Gap creation and crum placement**

`insertnd` calls `makegappm` to shift existing POOM entries (only those in `[blade[0], blade[1])`, i.e., within the insertion subspace) [SS-TWO-BLADE-KNIFE, FC-SUBSPACE]. Then it either:
- **Extends** an existing crum if `isanextensionnd` succeeds (same `homedoc`, contiguous I-address at crum's reach → zero new crums) [ST-INSERT Finding 0062], or
- **Creates** a new bottom crum and inserts it into the appropriate height-1 parent via `insertcbcnd` [INV-ENFILADE-OCCUPANCY Finding 0070].

**Step 2 — Overflow check → `splitcrumupwards`**

After adding a child, `insertcbcnd` triggers `splitcrumupwards(parent)`, which loops while `toomanysons(ptr)` is TRUE. For the POOM, the threshold is `MAX2DBCINLOAF = 4` at height-1 and `MAXUCINLOAF = 6` at height > 1 [SS-ENFILADE-BRANCHING].

The split path branches on `isfullcrum(ptr)`:
- **Root overflow**: `levelpush` increments tree height, then `splitcrum` divides the demoted root's children between two new siblings [SS-ENFILADE-TREE Finding 0058].
- **Internal node overflow**: `splitcrum` → for POOM specifically, `splitcrumpm` peels off the child with the **largest SPANRANGE displacement** (`cdsp.dsas[SPANRANGE]`), not the diagonal key [ST-SPLIT-2D Finding 0071].

After insertion, `setwispupwards` recalculates the 2D displacement (root `cdsp` = minimum address across children) to maintain the relative-addressing invariant [INV-ENFILADE-RELATIVE-ADDRESSING].

## Why `recombinend` Is Not Triggered by INSERT

`recombinend` is the **underflow** response. It is called when `toofewsons(ptr)` is TRUE (`sons < B-1`), which can only happen after **DELETE** removes children from a node [ST-DELETE Finding 0058, ST-REBALANCE-2D Finding 0071]. INSERT only adds children — it can cause overflow (→ split) but never underflow (→ merge/steal).

## Determining Factor

The branching factor constants and `whereoncrum`/`isanextensionnd` together determine which path INSERT takes:

| Condition | Path | Δ crums |
|-----------|------|---------|
| `origin == crum.reach` AND same `homedoc` | Extension (no split) | 0 |
| `origin < crum.reach` (THRUME) | Knife cut → new crum | +2 (split original, add new) |
| Parent overflow after new crum | `splitcrumupwards` → `splitcrumpm` | net +1 node at parent level |
| Parent at capacity but not overflow | Absorbed into existing node, no split | 0 at parent level |

The coalescing behavior means **continuous interior typing costs +2 crums once** (for the first character at a new position), then +0 per subsequent character at the same position [ST-CRUM-BOUND Finding 0062]. CREATELINK breaks this coalescing by advancing the I-address allocation pointer, causing the next INSERT to fail `isanextensionnd` [ST-CRUM-BOUND Finding 0063, INT-LINK-INSERT].

---

## Code Exploration

---

## Answer: POOM Rebalancing After INSERT — `splitcrumupwards` vs. `recombinend`

The two operations are **not alternative paths** — they are **sequential**, and `recombinend` only fires as a consequence of whether `splitcrumupwards` did work. Here is the complete trace.

---

### 1. Entry point: `insertnd` (`insertnd.c:15`)

```c
int insertnd(typetask *taskptr, typecuc *fullcrumptr, typewid *origin,
             typewid *width, type2dbottomcruminfo *infoptr, INT index)
```

For a POOM insert, the function body at `insertnd.c:46-77` does the following in order:

1. **Record current state**: `oldheight = fullcrumptr->height` [line 47]
2. **Create gap**: `makegappm(...)` [line 54] — shifts existing POOM entries to make room (POOM-only step, not done for SPAN)
3. **Insert**: `bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index)` [line 57]
4. **Conditionally recombine** [lines 70–77]:

```c
if(/*TRUE||*/bothertorecombine||(fullcrumptr->height != oldheight)){
    recombine (fullcrumptr);
}
```

---

### 2. The descent: `doinsertnd` → `insertmorend` → `insertcbcnd`

`doinsertnd` (`insertnd.c:185`) handles two cases:
- **Empty enfilade**: calls `firstinsertionnd` [line 192], returns `FALSE` — no split, no recombine
- **Non-empty**: calls `insertmorend` [line 196]

`insertmorend` (`insertnd.c:219`) recurses to the leaf level. At `height == 1` it calls `insertcbcnd` [line 231]; the return value (`splitsomething`) bubbles all the way back to `bothertorecombine` in `insertnd`.

---

### 3. The fork point: `insertcbcnd` (`insertnd.c:242`)

This function contains the critical branch:

**Path A — Extension (adjacent insert):**
```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified (ptr);
        setwispupwards (father,1);
        if(!isfullcrum((typecorecrum*)father)){
            return(setwispupwards(findfather((typecorecrum*)father),1));
        }
        return(FALSE);   // ← bothertorecombine = FALSE
    }
}
```
[`insertnd.c:250–258`]

`isanextensionnd` (`insertnd.c:301`) checks whether the new content is contiguous with an existing crum (same homedoc, and `reach == origin`). If so, it widens the existing crum in-place. **`splitcrumupwards` is never called. `recombine` will not be triggered.**

**Path B — New crum created:**
```c
new = createcrum (0, (INT)father->cenftype);   // insertnd.c:260
reserve (new);
adopt (new, SON, (typecorecrum*)father);        // insertnd.c:262
...
splitsomething = splitcrumupwards (father);    // insertnd.c:272
rejuvinate (new);
return(splitsomething);                        // ← becomes bothertorecombine
```
[`insertnd.c:260–274`]

When the insert is not adjacent to any existing crum, a new bottom crum is created. `splitcrumupwards` is **always** called here.

---

### 4. `splitcrumupwards` (`split.c:16`)

```c
bool splitcrumupwards(typecuc *father)
{
    splitsomething = FALSE;
    for (; toomanysons(father); father = (typecuc *)findfather((typecorecrum*)father)) {
        if (isfullcrum((typecorecrum*)father)) {
            levelpush(father);                           // grow tree height
            splitcrum((typecuc*)findleftson(father));
            return(TRUE);
        }
        splitcrum (father);
        splitsomething = TRUE;
    }
    return(splitsomething);
}
```
[`split.c:17–44`]

`toomanysons` (`genf.c:239`) checks:
```c
ptr->numberofsons > (ptr->height > 1 ? MAXUCINLOAF : (is2dcrum(ptr) ? MAX2DBCINLOAF : MAXBCINLOAF))
```
- Interior nodes (height > 1): capacity = **6** (`MAXUCINLOAF`, `enf.h:26`)
- 2D bottom nodes (POOM/SPAN, height == 1): capacity = **4** (`MAX2DBCINLOAF`, `enf.h:28`)

The loop walks upward. At each overfull node:
- **If it's the fullcrum (apex)** [`split.c:28`]: calls `levelpush(father)` — inserts a new intermediate node between the apex and its current children, incrementing `fullcrumptr->height` — then calls `splitcrum` on the new intermediate node. Returns `TRUE` immediately.
- **Otherwise** [`split.c:37`]: calls `splitcrum(father)`.

For POOM, `splitcrum` dispatches to `splitcrumpm` (`split.c:53–55`), which calls `peelcrumoffnd` on the son with the largest `cdsp.dsas[SPANRANGE]` (most diagonally displaced). `peelcrumoffnd` disowns that son and rehomes it under a newly created sibling of `father` (`split.c:130–168`).

---

### 5. `recombine` → `recombinend` (`recombine.c:22`, `recombine.c:104`)

Back in `insertnd`:
```c
if(bothertorecombine || (fullcrumptr->height != oldheight)) {
    recombine(fullcrumptr);
}
```
[`insertnd.c:70–77`]

`recombine` dispatches to `recombinend` for both POOM and SPAN [`recombine.c:29–32`].

`recombinend` is a **2D consolidation pass**:
```c
int recombinend(typecuc *father)
{
    if (father->height < 2  || !father->modified)
        return(0);
    for (ptr = getleftson(father); ptr; ptr = getrightbro(ptr))
        recombinend(ptr);                        // recurse first
    getorderedsons(father, sons);                // sort by diagonal position
    n = father->numberofsons;
    for (i = 0; i < n-1; i++) {
        for (j = i+1; sons[i] && j < n; j++) {
            if (sons[j] && ishouldbother(sons[i],sons[j]))
                takeovernephewsnd(&sons[i], &sons[j]);
        }
    }
    if (father->isapex)
        levelpull(father);                       // stubbed out — returns 0
}
```
[`recombine.c:104–131`]

`ishouldbother` merges two sibling subtrees if their combined child count fits within capacity (`MAXUCINLOAF` or `MAX2DBCINLOAF`). Sons are sorted diagonally (by `cdsp[0] + cdsp[1]`) before pairwise comparison, which groups spatially nearby nodes for consolidation.

Note: `levelpull` is a stub at `genf.c:318–342` (`return(0)` immediately) — tree height never shrinks after a `recombine`.

---

### Summary

| Condition | `splitcrumupwards` triggered? | `recombine` triggered? |
|---|---|---|
| Insert extends existing crum | **No** | **No** |
| Insert creates new crum, no overflow | **Yes** (called, returns FALSE) | **No** |
| Insert creates new crum, interior overflow | **Yes**, returns TRUE | **Yes** |
| Insert creates new crum, apex overflow (`levelpush`) | **Yes**, returns TRUE + height increases | **Yes** (both conditions fire) |

**What determines which rebalancing path is taken:**

1. **`splitcrumupwards` fires** iff `isanextensionnd` returns FALSE for every existing sibling in `insertcbcnd` — i.e., the new content is not contiguous with any existing crum. It is the **1D overflow handler**: splits loaves with too many sons by peeling the most-displaced child off into a new sibling, walking upward until no loaf is overfull. If the root itself overflows, `levelpush` grows the tree by one level.

2. **`recombine` fires** iff `splitcrumupwards` returned TRUE **or** the fullcrum's height changed. It is the **2D consolidation pass**: merges underloaded siblings to reduce fragmentation. The guard `father->height < 2 || !father->modified` at `recombine.c:112` means it only processes modified non-leaf nodes, so it does not run on trees that were untouched.

---

## Question 16 [gregory]

> The spanfilade DOCISPAN entry created by INSERT — does `insertspanf` record the document's I-address as the full `docISA` tumbler or just the document-level prefix, and does a single bulk INSERT of N bytes produce exactly one DOCISPAN entry covering the contiguous I-span?

### Gregory's Answer

## KB Synthesis

Both parts are directly answered by the KB.

**1. What `insertspanf` records for the document key**

The call is `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` [SS-DOCISPAN, Finding 0036]. The third argument is `docisaptr` — the full document ISA tumbler (e.g., `1.1.0.1.0.1`), not a truncated prefix. The DOCISPAN entry maps `(I-span) → docISA`, where docISA is the complete document address as used throughout the granfilade address space [SS-ADDRESS-SPACE, SS-LINK-HOME-DOCUMENT].

**2. How many DOCISPAN entries a single bulk INSERT produces**

Exactly one [SS-DOCISPAN, Finding 0047].

The call chain is: `doinsert` → `inserttextingranf` → `docopy` → `insertspanf(..., DOCISPAN)` [ST-INSERT, Finding 0036]. `inserttextingranf` allocates the N bytes as a single contiguous I-span (monotonic increment, `tumblerincrement(&lsa, 0, N, &lsa)` [ST-INSERT, Finding 0031]). `docopy` calls `specset2ispanset`, which returns 1 `typeispan` struct covering that contiguous range. `insertspanf` loops over the `ispanset` linked list making one `insertnd` call per `typeispan` [SS-DOCISPAN, Finding 0047]. Since there is one `typeispan`, there is one `insertnd` call and one DOCISPAN entry: `(α₁, width N) → docISA`.

The concrete example from Finding 0047 confirms:
```
INSERT "ABCDEFGHIJ" (10 bytes):
  inserttextingranf → 1 contiguous I-span {α₁, width 10}
  insertspanf → 1 insertnd call → 1 DOCISPAN entry
```

The number of DOCISPAN entries is O(number of operations), not O(bytes) [INV-SPANF-GROWTH]. For sequential single-character inserts, each insert individually produces 1 DOCISPAN entry, but the I-spans are contiguous in I-space (monotonic allocation [INV-MONOTONIC]), so they represent the same logical content range spread across N operations rather than 1 — still 1 entry per INSERT call, N entries total for N single-character inserts.

---

## Code Exploration

I now have everything needed to answer both questions definitively. Here is the full analysis:

---

## DOCISPAN Entry Structure in `insertspanf`

### Call Chain

```
fns.c:insert → do1.c:doinsert → do1.c:docopy → spanf1.c:insertspanf
```

`doinsert` [do1.c:117-122]:
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
    ...
```

`inserttextingranf` is a one-line wrapper [granf1.c:44-47]:
```c
bool inserttextingranf(typetask *taskptr, typegranf granfptr, typehint *hintptr, typetextset textset, typeispanset *ispansetptr)
{  bool inserttextgr();
   return (inserttextgr (taskptr, granfptr, hintptr, textset, ispansetptr));
}
```

`docopy` [do1.c:53-63] calls:
```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
...
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

---

## Question 1: Full `docISA` or just document-level prefix?

`insertspanf` [spanf1.c:15-53] begins:

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr, typesporglset sporglset, INT spantype)
{
  typedsp crumorigin;
  ...
  prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

`prefixtumbler` [tumble.c:641-651]:
```c
int prefixtumbler(tumbler *aptr, INT bint, tumbler *cptr)
{
  tumbler temp1, temp2;
    tumblerclear (&temp1);
    temp1.mantissa[0] = bint;          // temp1 = DOCISPAN (4), single digit
    movetumbler (aptr, &temp2);        // temp2 = full docISA
    if (!iszerotumbler (&temp2))
        temp2.exp -= 1;                // shift docISA one digit position rightward
    tumbleradd (&temp1, &temp2, cptr); // result = DOCISPAN prepended to full docISA
}
```

**`DOCISPAN = 4`** [xanadu.h:39]. The result stored in `crumorigin.dsas[ORGLRANGE]` is `4.<fullDocISA>` — the full document ISA is retained as the suffix.

Then for ISPANID items (which is what `inserttextgr` produces), the bottom crum `homedoc` field is set [spanf1.c:29]:
```c
movetumbler (isaptr, &linfo.homedoc);
```
`type2dbottomcruminfo` [wisp.h:107-109] has exactly one field:
```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

**Answer to Q1:** `insertspanf` records the **full `docISA` tumbler** — not a truncated prefix. The ORGLRANGE key is `prefixtumbler(docISA, DOCISPAN)` = `4.<fullDocISA>`, and `linfo.homedoc` separately stores the raw full `docISA`. The `DOCISPAN` (4) value is a category prefix, not a replacement for the document address.

---

## Question 2: Single bulk INSERT of N bytes → exactly one DOCISPAN entry?

**Step 1: `inserttextgr` collapses all text into one ispan.**

`inserttextgr` [granf2.c:83-109]:
```c
movetumbler (&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    ...
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);
}
ispanptr = (typeispan *) taskalloc (taskptr, sizeof(typeispan));
ispanptr->itemid = ISPANID;
ispanptr->next = NULL;
movetumbler (&spanorigin, &ispanptr->stream);
tumblersub (&lsa, &spanorigin, &ispanptr->width);
*ispansetptr = ispanptr;
```

Regardless of how many `textset` chunks are passed, this always produces **exactly one `typeispan`** node: stream = start address, width = total accumulated length. The list has `next = NULL`.

**Step 2: `specset2ispanset` passes ISPANID items through unchanged.**

[do2.c:24-26]:
```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;
    ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
```

ISPANID items are chained directly into the output, no transformation.

**Step 3: `insertspanf` iterates the ispanset and calls `insertnd` once per item.**

[spanf1.c:25-51]:
```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    if (((typeitemheader *)sporglset)->itemid == ISPANID) {
        movetumbler (&((typeispan *)sporglset)->stream, &lstream);
        movetumbler (&((typeispan *)sporglset)->width, &lwidth);
        movetumbler (isaptr, &linfo.homedoc);
    } ...
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
}
```

Since the ispanset has exactly one item, the loop runs once, and `insertnd` is called once.

**Answer to Q2:** Yes — a single bulk INSERT of N bytes produces **exactly one DOCISPAN crum** in the spanfilade. The one crum's SPANRANGE key covers the entire contiguous I-span `[stream, stream+N)`, its ORGLRANGE key is `4.<fullDocISA>`, and its `homedoc` bottom-crum field holds the full docISA. This holds even when the client sends multiple `textset` chunks: `inserttextgr` folds them all into one ispan before `insertspanf` is ever called.

---

## Question 17 [gregory]

> When inserting into a document that has entries in both text subspace (1.x) and link subspace (2.x internally), does `insertnd` traverse the entire POOM tree including link-subspace crums during the shift pass, classifying each as case 0/1/2, or does the two-blade mechanism prune the traversal so link-subspace nodes are never visited?

### Gregory's Answer

## KB Synthesis

## Traversal Depth vs. Classification

The KB directly addresses this, though it distinguishes two separate levels.

### What the KB does confirm: classification, not pruning

**[FC-SUBSPACE]** (Finding 0054) is the most precise source. For INSERT at `1.x` with blades `[1.x, 2.1)`:

> "For a link crum at `2.1` with `blade[1] = 2.1`, `whereoncrum` returns `ONMYLEFTBORDER` (-1). Since `cmp <= ONMYLEFTBORDER`, the crum is classified as **case 2** (no shift) and the `blade[0]` check is never reached."

The phrasing — that `whereoncrum` is called on the link crum and produces a specific classification — indicates the link-subspace crum **is visited** during `insertcutsectionnd`, not pruned before reaching it. The subspace isolation guarantee comes from the classification result, not from a pre-traversal skip.

**[SS-TWO-BLADE-KNIFE]** (Finding 0054) confirms that `insertcutsectionnd` has a three-case structure driven by the two blades, with case 2 (`>= blade[1]`) being the "no shift" path. The structural guarantee is: link crums encounter case 2 and are left untouched.

### What the KB does not confirm: B-tree subtree pruning

**[INV-ENFILADE-RELATIVE-ADDRESSING]** (Finding 0066) establishes that each POOM internal node carries a bounding box (`cdsp` = minimum V-address, `cwid` = extent). This structure *could* support pruning entire subtrees whose bounding box lies entirely at `>= blade[1]` — the internal node's displacement would indicate all children are in the link subspace. However, the KB does not document `makegappm`/`insertcutsectionnd` using this optimization. The retrieval path (`findcbcinarea2d` from **[SS-CONTEXT-LIST]**, Finding 0078) explicitly uses bounding boxes to prune descent, but the gap-making path is a different code path with different semantics.

### Summary

The KB supports this conclusion: **link-subspace crums are visited and classified as case 2 (no shift)** via the `whereoncrum` check against `blade[1]`. The subspace isolation invariant in **[FC-SUBSPACE]** is guaranteed by the knife classification mechanism, not by traversal pruning. Whether the 2D bounding boxes allow entire link-subtrees to be skipped before reaching individual leaf crums is not documented in the KB — you would need to read `insertcutsectionnd`/`makegappm` directly to confirm whether that optimization is present.

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## Answer: The shift pass visits link-subspace nodes but classifies them as case 2 (no-op). The two-blade mechanism does not prune them.

### Execution path

**Entry: `insertnd` [insertnd.c:51-61]**

For a POOM enfilade, `insertnd` dispatches to `makegappm` before calling `doinsertnd`:

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);  // insertnd.c:54
    ...
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
```

---

**`makegappm` [insertnd.c:124-172] — the shift pass**

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);         // insertnd.c:144
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);  // insertnd.c:145
knives.nblades = 2;
knives.dimension = V;                                       // insertnd.c:147
```

Both blades are in the **V dimension**, and both are computed from `origin->dsas[V]` — a position in the text subspace (1.x range). `findaddressofsecondcutforinsert` [insertnd.c:174-183] computes a ghost cut nearby within the same 1.x subspace. Neither blade ever touches the link subspace (2.x range).

After slicing the tree with `makecutsnd`, the intersection node is found:

```c
newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);  // insertnd.c:149
```

**`newfindintersectionnd` [ndinters.c:38-42] is a stub:**

```c
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives,
                          typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;          // always returns the fullcrum
    clear (offset,sizeof(*offset)); // zero offset
}
```

The old descent-based `findintersectionnd` (which would have walked down the tree to find a minimal containing node) is entirely commented out [ndinters.c:18-37]. The new version unconditionally sets `father = fullcrumptr` with zero offset. **There is no subspace-aware pruning here.**

---

**The shift-pass loop [insertnd.c:151-169]**

With `father = fullcrumptr` and `foffset = 0`, `fgrasp = {0,0}` (the fullcrum always has zero displacement). The loop iterates over **every direct child** of the fullcrum:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    i=insertcutsectionnd(ptr,&fgrasp,&knives);
    switch (i) {
      case 0:
      case 2:
            break;
      case -1:      /* THRUME*/
            gerror ("makegappm can't classify crum\n");
      case 1:
            tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
            ivemodified (ptr);
            break;
    }
}
```

This visits all top-level children — including any link-subspace UCCs.

---

**`insertcutsectionnd` [edit.c:207-233] — classification**

```c
INT insertcutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    if (knives->nblades == 2) {
        i = 1;
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME)          return (-1);
        else if (cmp <= ONMYLEFTBORDER)  return (2);
    }
    i = 0;
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME)              return (-1);
    else if (cmp <= ONMYLEFTBORDER) return (1);
    return (0);
}
```

**`whereoncrum` [retrie.c:345-398]** for POOM uses `index == V`:

```c
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    cmp = tumblercmp(address, &left);
    if (cmp == LESS)  return (TOMYLEFT);
    ...
```

---

**Constants [common.h:86-90]:**

```c
#define TOMYLEFT       -2
#define ONMYLEFTBORDER -1
#define THRUME          0
#define ONMYRIGHTBORDER  1
#define TOMYRIGHT        2
```

---

### What happens for a link-subspace node

A link-subspace upper crum has `ptr->cdsp.dsas[V]` in the 2.x range. Both knives are in 1.x.

Inside `whereoncrum`, with `offset = {0,0}` (fgrasp is zero):

```
left = 0 + ptr->cdsp.dsas[V] = 2.x
address = blades[1]           = 1.x
tumblercmp(1.x, 2.x) → LESS      [tumble.c:87-111, abscmp: mantissa[0] 1 < 2]
→ returns TOMYLEFT (-2)
```

Back in `insertcutsectionnd`:

```
cmp = TOMYLEFT = -2
cmp == THRUME?            -2 == 0 → FALSE
cmp <= ONMYLEFTBORDER?    -2 <= -1 → TRUE  → return 2
```

**Every link-subspace child of the fullcrum returns case 2.** In the switch: `case 2: break` — no modification.

---

### Conclusion

The two-blade mechanism does **not** prune link-subspace nodes from the traversal. `newfindintersectionnd` [ndinters.c:38-42] is a no-op stub that always sets the intersection to the fullcrum; the old descent-based pruner is commented out. The shift loop [insertnd.c:151] therefore visits every direct child of the fullcrum, regardless of subspace.

For link-subspace children (V coords in 2.x): the insert-point blades (1.x) fall `TOMYLEFT` of those crums; `insertcutsectionnd` returns case 2, which is identical in effect to case 0 — the `switch` hits `break` with no V-displacement change.

The blades provide **classification correctness** — link crums correctly receive no shift — but they provide **no traversal pruning**. A document with many link-subspace entries at the top level of the POOM will still have all of them visited on every text insertion; each is merely classified as a no-op after evaluating `whereoncrum` once (checking blade[1] only, since that returns case 2 immediately without reaching the blade[0] check).

---

## Question 18 [gregory]

> For the granfilade write that stores the inserted text, does `doinsert` create a single leaf node containing all N bytes of the insertion, or does the `MAXBCINLOAF=1` constraint mean each byte gets its own bottom crum, with the tree growing by N leaves per INSERT?

### Gregory's Answer

## KB Synthesis

A single INSERT of N bytes (where N ≤ 950) creates **one leaf node** containing all N bytes. The `MAXBCINLOAF=1` constraint and the per-byte granularity of I-addresses are orthogonal concerns.

**What `MAXBCINLOAF=1` actually constrains:**

`MAXBCINLOAF=1` means each height-1 node in the granfilade holds exactly one bottom crum (height-0 node). The "one entry" is one *text atom* (`typegrantext`), not one byte. [SS-UNIFIED-STORAGE] is explicit: "Leaf nodes for text content (`GRANTEXT` type) hold up to 950 bytes (`GRANTEXTLENGTH`)." [SS-GRAN-MB-ONE] explains this creates a degenerate pass-through layer at height-1, not per-byte storage.

**What actually happens during INSERT:**

`doinsert` calls `inserttextingranf`, which allocates a fresh `typegrantext` atom containing all N bytes via a single `insertseq` call. [ST-INSERT / Finding 0031] confirms this: `tumblerincrement(&lsa, 0, textset->length, &lsa)` advances by the total length in one step, producing a single contiguous I-span. [SS-DOCISPAN / Finding 0047] independently confirms this: "inserting 10 contiguous bytes creates 1 DOCISPAN entry, not 10" — because `insertspanf` receives one `typeispan` struct covering the entire range.

**The resulting tree change:**

One INSERT → one new bottom crum (containing the atom with all N bytes) → adopted as right sibling under a height-1 node → `splitcrumupwards` checks if that height-1 node now has 2 children → since `MAXBCINLOAF=1`, it does trigger a split. So a single INSERT causes tree structural work (one split, possibly a `levelpush` at the fullcrum), but always yields exactly one new leaf, not N leaves.

**The per-byte granularity is I-address granularity, not storage granularity.** Each of the N bytes gets its own I-address [INV-SINGLE-CHAR-GRANULARITY], but they are all packed into one `typegrantext` atom in one bottom crum. The comment "so text will fit" in `enf.h` signals the intent: the atom is large enough that one atom per crum is workable storage.

---

## Code Exploration

---

## Answer: One Leaf Per INSERT, Not One Leaf Per Byte

`MAXBCINLOAF=1` is a **tree fan-out limit** at the bottom level, not a constraint on how many bytes each leaf holds. A single `doinsert` of N bytes creates **one new bottom crum** containing all N bytes. Here is the complete trace.

---

### Step 1 — `doinsert` calls `inserttextingranf`

`doinsert` [do1.c:118]:
```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
```

`inserttextingranf` [granf1.c:44-47] is a one-line wrapper:
```c
bool inserttextingranf(...) {
    bool inserttextgr();
    return (inserttextgr (taskptr, granfptr, hintptr, textset, ispansetptr));
}
```

---

### Step 2 — `inserttextgr` packs all bytes into one `locinfo` and calls `insertseq` once

`inserttextgr` [granf2.c:83-109]:
```c
for (; textset; textset = textset->next) {
    locinfo.infotype = GRANTEXT;
    locinfo.granstuff.textstuff.textlength = textset->length;
    movmem(textset->string, locinfo.granstuff.textstuff.textstring,
           locinfo.granstuff.textstuff.textlength);
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);         // [granf2.c:99]
    tumblerincrement (&lsa, 0, textset->length, &lsa);
}
```

The outer `for` loop iterates over linked `typetext` segments in `textset`. A single FEBE INSERT produces one segment. `insertseq` is called **once**, with all N bytes packed into the single `locinfo` struct. There is no per-byte loop.

---

### Step 3 — The leaf (`typecbc`) holds a `typegrantext` of up to 950 bytes

The bottom crum struct [enf.h:84-107]:
```c
struct structcbc {
    ...
    typegranbottomcruminfo  cinfo;    // ONE record, not an array
};
```

`typegranbottomcruminfo` [wisp.h:100-104]:
```c
typedef struct structgranbottomcruminfo {
    typegranstuff granstuff;   // union: typegrantext OR typegranorgl
    INT infotype;
} typegranbottomcruminfo;
```

`typegrantext` [wisp.h:74-78]:
```c
typedef struct structgrantext {
    char textstring[GRANTEXTLENGTH];   // 950 bytes
    unsigned textlength;
} typegrantext;
```

`GRANTEXTLENGTH = 950` [common.h:115]:
```c
#define GRANTEXTLENGTH  950
```

Each leaf node has **one** `cinfo` slot (a union, not an array), and that slot's text buffer holds up to **950 bytes**.

---

### Step 4 — `insertseq` creates one new leaf, not N leaves

`insertseq` [insert.c:17-70]:

**Path A — pack into existing leaf** (if adjacent leaf has room):
```c
if (info->infotype == GRANTEXT
 && ptr->cinfo.infotype == GRANTEXT
 && ptr->cinfo.granstuff.textstuff.textlength < GRANTEXTLENGTH) {
    if (!fillupcbcseq (ptr, &nextaddress, info)) {
        ivemodified ((typecorecrum*)ptr);
        return(0);                        // no new crum at all
    }
}
```

If all N bytes fit into the existing leaf, `fillupcbcseq` returns FALSE ("not overflowing"), `ivemodified` is called, and the function returns with **zero new crums created**.

**Path B — create one new leaf** (existing leaf is full or has different type):
```c
new = createcrum (0, (INT)ptr->cenftype);   // one new typecbc, height=0
adopt (new, RIGHTBRO, (typecorecrum*)ptr);
...
moveinfo (info, &((typecbc *)new)->cinfo);  // copy ALL N bytes in
```

`moveinfo` [wisp.h:117] is `movmem(A, B, sizeof(typebottomcruminfo))` — it copies the full `typegranbottomcruminfo` (with all N bytes in `textstring`) into the new leaf in a single shot. **One new leaf, holding all N bytes.**

---

### Step 5 — What does `MAXBCINLOAF=1` actually control?

`MAXBCINLOAF=1` [enf.h:27], comment: `/* so text will fit */`:
```c
#define MAXBCINLOAF    1        /* so text will fit *//* as you wish */
```

Used in `toomanysons` / `roomformoresons` [genf.c:244,260]:
```c
return (ptr->numberofsons > (ptr->height > 1
    ? MAXUCINLOAF
    : (is2dcrum(...) ? MAX2DBCINLOAF : MAXBCINLOAF)));
```

When `ptr->height == 1` (an interior node whose children are bottom crums), the max fan-out is `MAXBCINLOAF=1`. This means each height-1 internal node has at most **1 leaf child** — it is a structural tree balance parameter, not a byte-per-leaf constraint.

The comment "so text will fit" explains *why* 1 was chosen: a leaf node must hold the full `typegrantext[950]` in memory. If the fan-out were higher (e.g. 6 like `MAXUCINLOAF`), each "loaf" (disk block) would need to pack 6 such records, making disk blocks very large. Setting fan-out to 1 at the bottom means each leaf lives alone in its block and can use all available space for its 950-byte text buffer.

The consequence is that every INSERT of new text immediately triggers `splitcrumupwards` [insert.c:48] because the height-1 parent jumps from 1 to 2 sons (exceeding `MAXBCINLOAF=1`), propagating splits up the tree to maintain balance. But this is a structural bookkeeping effect, not a content effect.

---

### Summary

| Question | Answer |
|---|---|
| Does `doinsert` create 1 leaf for N bytes? | **Yes** — when the adjacent leaf is full or absent, `insertseq` creates exactly 1 `typecbc` and copies all N bytes in via `moveinfo` [insert.c:52] |
| Does `MAXBCINLOAF=1` mean each byte gets its own leaf? | **No** — it is the fan-out limit for height-1 internal nodes (max 1 leaf child per interior node), chosen so a single text record fits in one disk block |
| How much can one leaf hold? | Up to **950 bytes** (`GRANTEXTLENGTH` [common.h:115]) stored in `typegrantext.textstring` |
| Can INSERT produce zero new leaves? | **Yes** — if the adjacent leaf is a GRANTEXT crum with room, `fillupcbcseq` packs bytes in without allocating any new crum [insert.c:34-41] |

**The tree grows by at most 1 leaf per INSERT** (all N bytes in one `typecbc`), not by N leaves. `MAXBCINLOAF=1` forces every new leaf to be the sole child of a new height-1 parent, which triggers structural splits up the tree, but does not fragment the text content into per-byte leaves.
