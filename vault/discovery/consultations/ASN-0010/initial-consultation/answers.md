# Consultation Answers — Content Retrieval

**Inquiry:** What must RETRIEVE guarantee about returned content? How does retrieval interact with transclusion, versioning, and the two address spaces?
**Date:** 2026-02-24 01:20
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When a user retrieves a span of a document, must the returned content be identical byte-for-byte to what was originally stored, regardless of how many documents transclude that same content?

### Nelson's Answer

## Yes — by design intent. Content at an I-address is immutable and singular.

The answer follows from three interlocking properties of Nelson's architecture:

### 1. I-Space Immutability

Content stored at an I-space address never changes. This is foundational to the entire system.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The curated I-space concept file states the guarantee plainly: "Content at an I-space address never changes" and "Content is immutable — it never changes after creation."

Nelson's storage model is explicitly append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Bytes are added, never overwritten. Retrieval of any I-address must return the same bytes that were originally stored there.

### 2. Transclusion Makes the "Regardless of How Many" Clause Moot

The number of documents transcluding content is irrelevant because transclusion is **reference, not copy**. There is only ever one physical instance of the content — at its home location in I-space. Every transclusion resolves back to that single source.

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The term "virtual copies" is precise — they are virtual, not physical. Whether one document or a million documents transclude the same span, they all fetch from the same I-space location. The content is not duplicated, so there is no divergence problem. The bytes returned are the bytes at the home location, period.

### 3. The Caveat: No Cryptographic Guarantee

Nelson's design **intends** byte-for-byte fidelity but provides **no technical verification mechanism** to prove it. The guarantee is contractual, not cryptographic.

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

> "Storage Vendor makes no guarantee as to the correctness or authenticity of any material received from other Users." [LM 5/18]

> "User acknowledges that due to possible unreliability of the software, unreliability and vulnerability of transmission systems, and myriad possibilities for intrusion and malicious mischief by unseen parties throughout the universe, all storage, and transmission of contents and links, and attempts to deliver such material, are at User's risk." [LM 5/18]

The system relies on the Storage Vendor franchise — contractual trust, not bit-level verification. If the vendor is honest and the software correct, retrieval returns identical bytes. But Nelson explicitly disclaims any technical proof of this.

### Summary

| Property | Status |
|----------|--------|
| Design intent: byte-for-byte fidelity | **Yes** — I-space is immutable by definition |
| Architectural mechanism | **Singular storage** — transclusion references one copy, not many |
| Effect of transclusion count | **None** — all transclusions resolve to same I-address |
| Technical verification | **Not provided** — trust is contractual, not cryptographic |

The system is designed so that retrieval always returns the original bytes. The number of transclusions cannot affect this because there is only one physical copy to return. But Nelson acknowledges that the guarantee rests on trusting the infrastructure, not on mathematical proof of integrity.

---

## Question 2 [nelson]

> If a document includes content by transclusion from another document, must retrieval return the content as though it were native to the requesting document, or must the system reveal its origin?

### Nelson's Answer

## Both: Content Returns Seamlessly, but Origin Is Always Discoverable

Nelson's answer is unambiguous on both halves of this question, and the two halves are not in tension — they operate at different layers.

### The Back End Returns Content as Though Native

The V-stream makes no distinction between native and transcluded bytes at the retrieval level:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

The RETRIEVEV command returns "the material (text and links) determined by \<spec set\>" [LM 4/67] — it does not annotate which bytes are native and which are transcluded. The front end receives a unified byte stream.

Furthermore, Nelson explicitly shields the front end from I-space internals:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

### The System Always Makes Origin Discoverable

At the same time, origin is structurally encoded and always queryable:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The operation FINDDOCSCONTAINING exists precisely for this: "This returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70]. Origin is computable from I-addresses, not from metadata that could be stripped.

### The Front End Decides Presentation — and Nelson Gives Guidance

This is where Nelson's design becomes most interesting. He distinguishes between two presentation modes for transcluded content, and assigns them to different link types:

**Inclusions are NOT ordinarily indicated to the reader:**

> "Note that a quote-link is not the same as an inclusion, which is not ordinarily indicated" [LM 4/53]

**Quote-windows ARE indicated — the reader sees a boundary:**

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

> "Only when you step through the window — turning one glass page and going on in the next — do you reach the original that you wanted. But stepping through the window means you are now in another work." [LM 2/34]

So the front end has two choices depending on the document's structure:

| Type | Visible to reader? | Origin discoverable? |
|------|-------------------|---------------------|
| **Inclusion** (plain transclusion) | Not ordinarily indicated | Yes, always queryable |
| **Quote-window** (quote-link) | Yes — shown as a window boundary | Yes, and navigable ("step through") |

In both cases, two-way reading is available:

> "It is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37]

### Summary

The **back end** returns transcluded content indistinguishably from native content in the V-stream. The **system** always preserves origin structurally in I-addresses. The **front end** decides whether to reveal boundaries, with Nelson specifying that plain inclusions are invisible by default while quote-windows are visible. But in all cases, origin is one query away — it is structural, not metadata, and cannot be severed.

The design principle: **seamless by default, transparent on demand**.

---

## Question 3 [nelson]

> When retrieving from a specific version of a document, must the system guarantee that the returned content reflects exactly the state at version-creation time, even if later versions exist?

### Nelson's Answer

# Yes — Version Retrieval Is Exact

The system must guarantee that retrieving from a specific version returns exactly the state at version-creation time. This follows from three converging aspects of Nelson's design.

## The Explicit Promise

Nelson states the guarantee directly:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "We believe our Prismatic storage can support virtually instantaneous retrieval of any portion of any version (historical or alternative)." [LM 2/19]

The phrase "a given part of a given version at a given time" is precise: you specify which version, and you get that version's content — not the latest version, not a "best effort" reconstruction.

## Why the Architecture Makes It Inevitable

Each version is a distinct V-space arrangement (a mapping from V-positions to I-addresses). Two properties make version retrieval exact:

1. **I-space immutability.** Content at an I-address never changes. "Native bytes of a document are those actually stored under its control and found directly in storage under its control" [LM 4/11]. Once bytes are written, they are permanent.

2. **Per-version V-space.** Each version has its own V→I mapping. Editing creates a new version with a new mapping; it does not modify the old version's mapping. CREATENEWVERSION "creates a new document with the contents of document \<doc id\>" [LM 4/66] — the old document is untouched.

Since the V→I mapping for a version is fixed at creation time, and the I-space content those addresses point to is immutable, the version's content is frozen the moment it is created. Later versions cannot retroactively change what an earlier version contains.

## No "Basic" Version — All Are Equal

Nelson is explicit that later versions have no special authority over earlier ones:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

Supersession links can *inform* a reader that a newer version exists, but the older version remains fully retrievable at its original content:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version." [LM 4/52]

The supersession link is advisory. It does not alter what the old version returns.

## The Transclusion Subtlety

One nuance arises with transcluded content. If version V1 of document X transcludes content from document Y, and Y is later edited, what does V1 show?

The answer: V1 shows exactly what it showed at creation. The transclusion is stored as a reference to specific I-addresses, and I-addresses are immutable. "Editing" document Y means creating a new V-space arrangement for Y — the I-space bytes that V1 references remain unchanged.

Nelson does describe a front-end choice between "time-fixed" and "location-fixed" windows:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

But this is a **front-end presentation choice**, not a back-end storage property. The back-end stores the I-address reference. A "location-fixed" window is the front-end choosing to resolve correspondence and show the current version's equivalent content — the underlying version's stored state is unaffected.

## The Conservation Law

This guarantee is not an incidental feature. It is entailed by the deepest principle of the system — append-only storage with no destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

If the storage system is append-only, and versions are V-space arrangements over immutable I-space content, then version retrieval is exact by construction. There is nothing in the system that *could* alter what a version returns, even if some component wanted to.

## Summary

**Yes.** Retrieving from a specific version must return exactly the state at version-creation time. This is guaranteed by I-space immutability, per-version V-space mappings, the append-only storage model, and Nelson's explicit promise that you get "a given part of a given version" on demand. The existence of later versions, supersession links, or edits to transcluded documents' arrangements does not and cannot affect what an earlier version returns.

---

## Question 4 [nelson]

> Must retrieval of a document region that spans both original and transcluded material return a seamless, contiguous result, or may the system return fragments with gaps?

### Nelson's Answer

## Retrieval Must Be Seamless

The system must return a seamless, contiguous result. Nelson's design is unambiguous on this point, and the guarantee follows from multiple reinforcing commitments.

### The V-Space Guarantee

The virtual byte stream makes no distinction between native and transcluded bytes. Nelson states this explicitly:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Non-native bytes are as much a logical part of a document as native bytes." [LM 4/11]

The V-space is dense and contiguous by definition. Every byte — whether originally written in this document or transcluded from another — occupies a sequential position in the byte stream. There are no gaps. A retrieval request specifies V-space spans, and the system returns the material at those positions regardless of where the underlying I-space content physically resides.

### The Part-Pounce Contract

Nelson describes retrieval as on-demand construction from fragments — but the fragmentation is an implementation detail invisible to the user:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

> "This system is built around the assumption that you are reading from a screen, not from paper. When you 'go to' a certain part of a document, the whole document is not ready to show; yet the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." [LM 2/16]

> "We call this pounce. You pounce like a cat on a given thing, and it seems to be there, having been constructed while you wait, as it were, in midair." [LM 2/16]

The word "materializing" is precise: the system assembles a coherent result from distributed fragments, but what the user receives is the materialized whole, not the fragments.

### RETRIEVEV Returns "The Material"

The FEBE protocol reinforces seamlessness:

> "This returns the material (text and links) determined by \<spec set\>." [LM 4/67]

Not "fragments of the material," not "available portions" — *the material*. The spec-set identifies V-space spans; the back end resolves them to I-space content (which may be scattered across documents and servers) and returns the result as a unified response.

### The Glass Pane Metaphor

Nelson's metaphor for compound documents makes the seamlessness visual:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

The reader sees through the windows. The layering is structural, not visible as seams or breaks. And:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

You can *ascertain* origin (structural traceability is preserved), but the experience is of one coherent document.

### The Network Makes Distribution Invisible

When transcluded content lives on a remote server, the BEBE protocol handles this transparently:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." [LM 4/70]

The user's local server fetches remote content and integrates it before delivery. The distributed nature of storage is an infrastructure concern, not a user-facing one.

### Summary

The answer is definitive: **retrieval must return a seamless, contiguous result.** This follows from:

1. **V-space density** — non-native bytes occupy ordinal positions "just as if" they were native [4/11]
2. **Part-pounce** — the system materializes coherent results from fragments [2/16]
3. **RETRIEVEV semantics** — returns "the material," not partial results [4/67]
4. **BEBE integration** — distributed storage is melded into a single unified space [4/70]

The front end may then expose provenance (which bytes are native, which are transcluded) as a separate layer of information — Nelson explicitly supports this with the "home document" traceability guarantee. But the byte stream itself has no gaps, no seams, and no fragmentation visible to the retrieval operation.

---

## Question 5 [nelson]

> If the same content appears at two different positions within a document through transclusion, must retrieval at each position return identical results?

### Nelson's Answer

## Yes — identical results are guaranteed, by structure

If the same content appears at two V-space positions within a document through transclusion, retrieval at each position **must** return identical bytes. This is not a special rule requiring enforcement; it falls out directly from the architecture.

### Why it must be so

The document's V-stream is a mapping from V-positions to I-addresses. When content is transcluded (via COPY) to two positions, both V-positions map to the **same I-addresses**. Retrieval at any V-position works by:

1. Resolving the V-address to its I-address through the POOM mapping
2. Fetching the bytes at that I-address
3. Returning them

Since both positions resolve to the same I-address, and I-space content is immutable, the returned bytes are necessarily identical. There is no mechanism by which the same I-address could yield different content.

### Nelson's architecture makes this unavoidable

The I-space guarantee is absolute:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Non-native bytes (transclusions) are fetched from their **home location** — the permanent I-address. Two transclusions of the same content go to the same home:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The word "virtual" is key — these are not copies in the conventional sense. No duplication occurs:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

### The content exists once; the references are two

The two V-positions are two views into the same I-space content. Nelson's glass-pane metaphor applies even within a single document:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else." [LM 2/34]

Two windows in the same sheet of glass looking at the same underlying content necessarily show the same thing.

### What about RETRIEVEV?

The retrieval operation works on V-space positions:

> "This returns the material (text and links) determined by \<spec set\>." [LM 4/67]

A spec-set specifying V-position 10 and a spec-set specifying V-position 50 will return identical bytes if both map to the same I-address range. The operation is deterministic — it resolves V→I, then fetches from I-space.

### One qualification: front-end presentation may differ

The **bytes returned** are identical. But the front-end might present them differently based on context — surrounding formatting, link overlays, or annotation layers. Nelson is clear that front-end presentation is separate from back-end content:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The back end delivers the same bytes. What the front end does with them is its business.

### Summary

The identity is **structural, not enforced**. Two V-positions mapping to the same I-address return the same bytes because there is only one copy of the content, and both references point to it. This is the entire point of transclusion over copying — the content exists once, and all references to it are references to that single truth.

---

## Question 6 [nelson]

> Does retrieval carry any obligation to report where the returned content originally came from, or is provenance information separate from the content guarantee?

### Nelson's Answer

## Provenance and Retrieval: Separate Guarantees

Nelson guarantees that provenance is always **determinable** but does not bundle it with content delivery. These are distinct system capabilities.

### The Structural Guarantee

Every byte has a permanent I-address encoding its origin:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is structural — the I-address format `Node.0.User.0.Document.0.Element` embeds the originating document. The system cannot deliver content without knowing where it lives. But *knowing* provenance internally and *reporting* it to the user are separate matters.

### Retrieval Returns Content, Not Provenance

The sole content-delivery command is terse in specification:

> "RETRIEVEV: This returns the material (text and links) determined by \<spec set\>." [LM 4/67]

Nelson says "material" — bytes and links. He does not say "material with origin annotations." More pointedly, he explicitly states:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The front end is **unaware** of I-addresses. It works in V-space. When it requests V-positions 1 through 100, it gets bytes — not a map of which bytes came from which home documents.

### Provenance Is Discoverable Through Separate Operations

The system provides explicit provenance-discovery operations, separate from retrieval:

**FINDDOCSCONTAINING**: "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This is the operation that answers "where did this content originate?" It searches by I-space origin, returning all documents that share the same underlying bytes. It is a query you *choose* to make, not information that accompanies every delivery.

**SHOWRELATIONOF2VERSIONS**: "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

This computes correspondence — shared I-space origin between versions. Again, a separate query.

### Reconciling "At Once" with "Unaware"

The apparent tension between "at once ascertain the home document" [2/40] and "front-end application is unaware" [4/11] resolves when you see that Nelson is describing two different things:

- The **front end** does not track I-addresses during normal operation (rendering, editing)
- The **user** can always query the system to discover provenance ("at once" meaning the capability is always available, not that it arrives unbidden)

The front end is the user's tool. When the user wants provenance, the front end issues the appropriate query (FINDDOCSCONTAINING or equivalent). The information is always available in the back end — it merely requires asking.

### The Transclusion Context

This separation makes particular sense for compound documents. Nelson describes how windowed content appears seamlessly:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The user experience is coherent: transcluded content appears as part of your document. But you can always "step through the window" to the original:

> "Only when you step through the window—turning one glass page and going on in the next—do you reach the original that you wanted. But stepping through the window means you are now in another work." [LM 2/34]

"Stepping through" is a user action — a deliberate navigation from the compound view to the source. It is not automatic annotation of every delivered byte.

### Summary

| Aspect | Guarantee |
|--------|-----------|
| **Provenance exists** | Always — I-address encodes origin permanently |
| **Provenance accompanies retrieval** | No — RETRIEVEV returns bytes, not origin metadata |
| **Provenance is discoverable** | Always — via FINDDOCSCONTAINING and related operations |
| **Front end tracks I-addresses** | No — explicitly "unaware" of them |
| **User can determine origin** | Yes — "at once ascertain the home document" |

Provenance is a **capability** of the system, not a **component** of content delivery. The content guarantee (you get the bytes) and the provenance guarantee (you can find their origin) are architecturally independent, served by different operations, and invoked at the user's discretion.

---

## Question 7 [nelson]

> When content is retrieved by its permanent identity rather than by its position in a document, must the system return exactly the same bytes as retrieval by document position would?

### Nelson's Answer

## Yes — by architectural definition, not by special rule.

The answer follows from how Nelson designed the two address spaces. V-space is not a separate store; it is a *mapping* to I-space. Retrieving content by V-address means looking up the corresponding I-address and fetching the bytes from there. There is no other source of bytes.

### The Architecture Makes This Tautological

Nelson defines the relationship explicitly:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Content lives in I-space. V-space arranges references to that content. When you retrieve through V-space, the system resolves the V→I mapping and returns the I-space bytes. When you retrieve by I-address, you go to the same bytes directly. There is no intermediate representation where they could diverge.

### The FEBE Protocol Exposes Only V-Space

Notably, Nelson's protocol does not offer direct I-space retrieval to users:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The sole content retrieval command is RETRIEVEV, which works with V-space spec-sets: "This returns the material (text and links) determined by \<spec set\>." [LM 4/67]

I-space retrieval happens *internally* — when the back end fetches non-native bytes from their home locations to fulfill a V-space request. The user never specifies an I-address.

### Why This Matters: Transclusion Depends On It

The identity guarantee is what makes transclusion meaningful. When document A transcludes content from document B, both documents' V-streams map to the *same* I-addresses. The bytes a reader sees through A's V-space are the bytes at B's I-space home. Nelson's glass-pane metaphor captures this:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else." [LM 2/34]

The "window" doesn't create a copy — it shows the original. Both paths (through A's V-space, or through B's V-space, or hypothetically through the I-address directly) reach the same bytes because they *are* the same bytes.

### Immutability Seals It

I-space content never changes after creation. This is not merely a convention but a structural property:

> "Content at an I-space address never changes." (from the I-space/V-space concept definition, consistent with Nelson's permanence guarantee)

> "Any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Since I-space content is immutable and V-space is a mapping to I-space, the bytes returned are always the same regardless of which path you take to reach them.

### Summary

The question posits a distinction that Nelson's architecture collapses by design. There is no separate "I-space retrieval" versus "V-space retrieval" — there is only I-space content, accessed either directly (back-end internal) or indirectly (through V-space mapping). The bytes must be identical because they are literally the same bytes at the same permanent address. Nelson achieves this not through a correctness check but through the architectural decision that V-space contains no content — only references to I-space where all content lives.

---

## Question 8 [nelson]

> Must the system guarantee that content retrievable today remains retrievable tomorrow — does permanence of storage imply permanence of access?

### Nelson's Answer

# Permanence of Storage vs. Permanence of Access

Nelson treats these as related but distinct concepts, and the curated sources reveal a genuine tension in his design.

## Three Levels of Permanence

### 1. Permanence of Address — Unconditionally Guaranteed

Tumbler addresses, once assigned, are never reused or invalidated:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This is structural, not policy. The addressing scheme makes reuse impossible — forking only creates new sub-addresses; it never reclaims old ones.

### 2. Permanence of Content (I-Space) — Strongly Guaranteed

I-space is append-only. Content is never overwritten or destroyed:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

DELETE removes content from V-space (the current view) but not from I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The content survives in I-space. Nothing in the specification provides a mechanism for removing bytes from I-space.

### 3. Permanence of Access — Intended but Economically Conditioned

This is where the tension lies. Nelson makes strong statements in both directions.

**The promise of permanent access:**

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "This attrition of the heritage can in principle be stopped." [LM 3/25]

> "Only digital archives give us long-term hope for preserving our heritage—not just writings, but text, paintings (stored as detailed photographs), sculpture, architecture, whatever." [LM 3/25]

**The economic constraint on that promise:**

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Storage requires ongoing rental paid by the content owner. Nelson specifies concrete costs: "$20/meg" one-time, "$1/meg" annual maintenance per server [LM 5/11]. This is not a one-time act; it is a continuing obligation.

## The Unresolved Question

If a publisher dies, goes bankrupt, or simply stops paying storage rental — what happens to the content?

Nelson does not answer this directly. The curated sources identify several pieces of the puzzle but no complete resolution:

**Vendor failure is addressed.** The Storage Vendor Contract requires: "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16]. Content migrates when a vendor shuts down.

**Publisher failure is not addressed.** No mechanism is specified for what happens when the *publisher* (not the vendor) stops paying. The content exists in I-space. The address is valid. But who funds the ongoing storage?

**The Author's Fund is a partial answer.** "When bytes are taken from an unpublished document (one in the public domain), this surcharge is added to the Author's Fund, an escrow account whose purpose is the charitable funding of worthy causes within the network" [LM 5/12]. But this fund is explicitly for public domain content, not for abandoned published content.

**Royalty revenue is another partial answer.** Popular content generates per-byte royalties when accessed: "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned" [LM 2/43]. For widely-read content, delivery charges could offset storage costs. But rarely-read content would not generate enough revenue.

## The Link Argument for Permanent Access

Nelson's strongest argument for permanent access is not economic but structural — it comes from link ownership:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work." [LM 2/43]

If Alice publishes document D and Bob creates links to it, those links are *Bob's property* at *Bob's address*. Withdrawing D doesn't just affect Alice's content — it destroys the referential integrity of Bob's links. This is why Nelson insists on the "lengthy due process" requirement for withdrawal.

The contrast with "privashing" makes this explicit. Privashing means universal access but the right to withdraw:

> "An author who wishes to render his or her work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution." [LM 2/59-2/60]

The key distinction: privashed content earns no royalty. Publication earns royalty but sacrifices the right to withdraw. This implies that **publication is a permanent commitment to access** — that is the bargain.

## The Honest Answer

Nelson intends permanence of access as a consequence of publication. The act of publishing is a "solemn event" that creates a permanent obligation. Content in I-space never disappears. Addresses never break. Published documents stay published.

But the economic mechanism for funding permanent access to abandoned or rarely-read published content is not specified. The specification has:

- A permanence **principle** (content must remain accessible)
- A permanence **structure** (I-space is append-only, addresses are eternal)
- A permanence **obligation** (publication is irrevocable)
- But no permanence **funding model** for the case where the publisher is gone and readers are few

This is a gap. Nelson identifies the aspiration — "deep rock and deep space" [LM 3/25], archives surviving wars and governments — but the self-sustaining economics he insists on [LM 4/5] do not fully close the loop for the long tail of rarely-accessed content whose owners have disappeared.

The system guarantees that content *exists* (I-space permanence) and that its address *works* (tumbler permanence). Whether that content remains *deliverable* depends on someone continuing to pay for the storage infrastructure — and Nelson leaves that someone unidentified for the edge case where the original publisher is no longer present.

---

## Question 9 [nelson]

> If a link points to a region of a document and that region contains transcluded content, must retrieval through the link return the content as the document presents it, not as the source document organizes it?

### Nelson's Answer

## Yes — retrieval through a link returns the document's presentation, including transcluded content

This follows directly from three interlocking elements of Nelson's design.

### 1. The V-stream is uniform

Transcluded bytes occupy positions in the virtual byte stream indistinguishably from native bytes:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

The V-stream makes no architectural distinction between native and transcluded content. Both are addressed the same way:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, **regardless of their native origin**." [LM 4/11]

### 2. Links connect spans in this uniform stream

Link endsets are span-sets — regions of the V-stream:

> "A Xanadu link is not between points, but between spans of data." [LM 4/42]

When MAKELINK creates a link, its from-set and to-set specify spans in the document's virtual byte stream. Those spans may cross boundaries between native and transcluded content without any special handling — because the V-stream doesn't expose those boundaries at the addressing level.

### 3. Retrieval operates on the V-stream

RETRIEVEV returns material determined by a spec-set, which is a set of vspans. Following a link to a region of document D means retrieving that region of D's V-stream. The result includes whatever bytes occupy those V-positions — native or transcluded.

### The glass pane model confirms this

Nelson's metaphor makes the point visually:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

When you look at a region of the glass, you see whatever is there — painted content and content visible through windows, composited into one view. A link that points to a region of that glass gives you that composite view.

### But origin remains discoverable

The document presents transcluded content as its own, but the user can always pierce this:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

And the user can explicitly "step through" to the source:

> "Only when you step through the window — turning one glass page and going on in the next — do you reach the original that you wanted. But stepping through the window means you are now in another work." [LM 2/34]

FINDDOCSCONTAINING can also reveal provenance: it "returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70], working from I-space identity rather than V-space arrangement.

### Summary

The document's V-stream is the authoritative presentation. Links address it. Retrieval returns it. Transcluded content appears in place, as the document's author arranged it. Origin is always discoverable but is not the default view — the default is the document as composed.

---

## Question 10 [nelson]

> When a document has multiple versions, must retrieval of shared content across those versions return identical results, confirming that versioning does not alter the underlying content?

### Nelson's Answer

# Yes — Shared Content Across Versions Must Return Identical Results

This is not merely a desirable property but a direct consequence of Xanadu's most fundamental architectural decision: the separation of I-space from V-space.

## The Architectural Guarantee

Versions are different V-space arrangements over **the same** I-space content. A version is not a copy — it is a mapping. When two versions share content, they both reference the same I-space addresses, and I-space content is immutable:

> "Content at an I-space address never changes after creation."

The library analogy from Nelson's design makes this concrete:

```
I-Space (Library)              V-Space (Reading Lists)
┌─────────────────────┐        ┌─────────────────────┐
│ Shelf A: "hello"    │        │ My Essay v1:        │
│ Shelf B: " world"   │   ──►  │   [ref A, ref B]    │  → "hello world"
│ Shelf C: "!"        │        │                     │
│                     │        │ My Essay v2:        │
│ (never changes)     │   ──►  │   [ref A, ref C]    │  → "hello!"
└─────────────────────┘        └─────────────────────┘
```

Both versions retrieve "hello" from the same Shelf A. The result is identical not by coincidence but because it **is the same bytes at the same address**.

## Nelson's Words

On I-space permanence:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

On version creation:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

CREATENEWVERSION does not copy bytes. It creates a new V-space arrangement that references the existing I-space content. The new version's V-stream points to the same I-addresses as the original.

On the nature of versions:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

The phrase "the same materials" is key — all versions share the same underlying materials. They differ only in arrangement.

## Correspondence Proves It

The SHOWRELATIONOF2VERSIONS operation exploits this property directly:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

Correspondence is defined by shared I-space origin. Two V-positions in different versions correspond **if and only if** they map to the same I-address. If retrieval could return different results for the same I-address, correspondence would be meaningless — you could not "show you, word for word, what parts of two versions are the same" [LM 2/20].

## The Non-Destruction Guarantee

Nelson states this as a fundamental principle:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

"Without damaging the originals" means the shared content is identical before and after versioning. If creating a version could alter shared content, the originals would be damaged — violating this guarantee.

## The Storage Model Enforces It

Nelson's append-only storage model makes alteration structurally impossible:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is appended, never overwritten. There is no mechanism by which versioning could alter existing I-space content, because I-space only grows — it never mutates.

## Summary

Retrieval of shared content across versions **must** return identical results. This follows from three converging properties:

1. **I-space immutability** — bytes at an I-address never change
2. **Versions share I-addresses** — CREATENEWVERSION maps to existing content, not copies
3. **Append-only storage** — no mechanism exists to alter stored content

The entire correspondence system, the royalty model (paying the original author for shared bytes), and the intercomparison facility all depend on this guarantee holding absolutely. It is not a feature of versioning — it is the reason versioning works at all.

---

## Question 11 [gregory]

> When RETRIEVEDOCVSPAN is called on a document containing both text and links, does it return a single bounding span covering both subspaces, and if so, does the returned content include raw link orgl bytes interleaved with text?

### Gregory's Answer

## KB Synthesis

**Yes to the first part; No (with qualification) to the second.**

## RETRIEVEDOCVSPAN returns a bounding span across both subspaces

[SS-VSPAN-VS-VSPANSET] (Findings 0017, 0035) establishes this directly. RETRIEVEDOCVSPAN (opcode 14) calls `retrievevspanpm()`, which reads the root node's raw V-dimension displacement and width without any subspace awareness. For a document with text at 1.x and one link (internally at 2.x), it returns something like `1.1 for 1.2` — a bounding box that bridges both subspaces. This is documented as Bug 0011. By contrast, RETRIEVEDOCVSPANSET uses `retrievevspansetpm()` which detects the subspace partition and returns separate spans per occupied region.

## The content retrieval does NOT include link orgl bytes

If a caller uses the bounding span to retrieve content via `doretrievev`, the link-subspace V-positions (0.x / 2.x) are converted to I-addresses via `specset2ispanset`. Those I-addresses are **link orgl ISAs** — tumbler addresses like `1.1.0.1.0.1.0.2.1` in document address space, not permascroll addresses.

`ispanset2vstuffset` then attempts to look up these ISAs in the permascroll (which stores raw text bytes at `2.x.0.y.0.z` addresses). Since the link orgl ISAs are in a completely different tumbler range from permascroll content, the lookup produces NULL or garbage bytes — not the actual link orgl structure. [SS-DUAL-ENFILADE] Finding 0011 states this explicitly: "Dereferencing a link ISA as content produces garbage, but no error is raised."

The link orgl structure (containing endpoint sporgls, type reference, etc.) lives in the granfilade as a structured tree node — it is not stored as raw bytes in the permascroll and therefore cannot be retrieved via the text content path.

## Summary

| V-positions in bounding span | I-address type | `ispanset2vstuffset` result |
|------------------------------|----------------|-----------------------------|
| 1.x (text) | Permascroll addresses | Correct text bytes |
| 0.x / 2.x (links) | Link orgl ISAs | NULL / garbage (silent failure) |

[EC-RETRIEVE-VSPANSET-BOTH-SUBSPACES] and [PRE-RETRIEVE-CONTENTS] both document this as a known failure mode: using the bounding span from RETRIEVEDOCVSPAN as input to content retrieval produces corrupt mixed output without raising an error. This is why [PRE-COMPARE-VERSIONS] requires filtering to text subspace before operation, and why [PRE-VCOPY] requires matching I-address types to destination subspace.

## Code Exploration

Now I have everything needed. Let me synthesize the complete answer from the source code trace.

---

## RETRIEVEDOCVSPAN with Text + Links: Full Analysis

### Call Chain

**`RETRIEVEDOCVSPAN`** [fns.c:303-315]:
```c
bool getretrievedocvspan(), doretrievedocvspan();
if (
   getretrievedocvspan(taskptr, &docisa)
&& doretrievedocvspan(taskptr, &docisa, &vspan))
    putretrievedocvspan(taskptr, &vspan);
```

**`doretrievedocvspan`** [do1.c:312-320]:
```c
bool doretrievedocvspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return
        findorgl(taskptr, granf, docisaptr, &docorgl, READBERT)
     && retrievevspanpm(taskptr, docorgl, vspanptr);
}
```

**`retrievevspanpm`** [orglinks.c:165-172] — the actual implementation:
```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler(&((typecuc *)orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler(&((typecuc *)orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This reads exactly two values from the POOM root node and returns them as a single `typevspan` with `next = NULL`. **One span only, always.**

---

### Question 1: Single Bounding Span Covering Both Subspaces?

**Yes.** The `cdsp.dsas[V]` and `cwid.dsas[V]` fields of the POOM root are the bounding box across all V-space content, maintained by `setwispnd()` [wisp.c:171-228]:

```c
/* find new upper-left corner (minimum across all children) */
movewisp(&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ...) {
    lockmin((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, ...);
}

/* find new lower-right corner (maximum reach across all children) */
clear(&newwid, sizeof(newwid));
for (ptr = findleftson(father); ptr; ptr = getrightbro(ptr)) {
    lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid, &tempwid, ...);
    lockmax((tumbler*)&newwid, (tumbler*)&tempwid, ...);
}
movewisp(&newwid, &father->cwid);
```

`lockmax` over all children's `(cdsp + cwid)` — this covers both subspaces.

#### How Text and Links Occupy Different V-Regions

**Text** is inserted starting at V = `1.1` [orglinks.c:42-43 `findvsatoappend`]:
```c
tumblerincrement(vsaptr, 0, 1, vsaptr);  // → "1"
tumblerincrement(vsaptr, 1, 1, vsaptr);  // → "1.1"
```

**Links** are positioned by `findnextlinkvsa()` [do2.c:151-166]:
```c
tumblerclear(&firstlink);
tumblerincrement(&firstlink, 0, 2, &firstlink);  // → "2"
tumblerincrement(&firstlink, 1, 1, &firstlink);  // → "2.1"

(void) doretrievedocvspan(taskptr, docisaptr, &vspan);
tumbleradd(&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp(&vspanreach, &firstlink) == LESS)
    movetumbler(&firstlink, vsaptr);   // link VSA = "2.1" if doc is small
else
    movetumbler(&vspanreach, vsaptr);
```

The minimum first-link position is `"2.1"`. After inserting 10-character text "Click here" at V = `"1.1"`, the text reach is `"1.11"` (< `"2.1"`), so the link goes to V = `"2.1"`.

#### Bounding Box Computation

After inserting text at V = `"1.1"` width `"0.10"` and a link at V = `"2.1"` width `"0.1"`:

- POOM root `cdsp.dsas[V]` = `"1.1"` (minimum V-displacement)
- POOM root `cwid.dsas[V]` = `"1.2"` (max reach = `"2.1" + "0.1" = "2.11"` → `"1.2"` relative to root start)

`retrievevspanpm` returns:
- `stream = "1.1"`, `width = "1.2"`

**The golden test `retrieve_vspan_with_links.json` confirms this exactly:**

```json
{
  "op": "retrieve_vspan",
  "result": "<VSpan in 1.1.0.1.0.1 at 1.1 for 1.2>",
  "comment": "Overall extent (may cover both subspaces)"
}
```

The returned span `"1.1 for 1.2"` covers V = `"1.1"` through `"2.3"` in tumbler arithmetic, spanning across both the text range (`"1.1"` to `"1.11"`) and the link range (`"2.1"` to `"2.11"`), with a gap between them.

Compare to `RETRIEVEDOCVSPANSET` [orglinks.c:173-221], which returns **two separate spans** for the same document:
```json
{ "spans": [
    { "start": "0", "width": "0.1" },
    { "start": "1", "width": "1"   }
]}
```
`retrievevspansetpm` uses `is1story()` [tumble.c:237-247] to detect the multi-subspace case and decomposes them via `maxtextwid()` [orglinks.c:224-245]. `RETRIEVEDOCVSPAN` makes no such decomposition.

Also note: `retrievedocumentpartofvspanpm` [orglinks.c:155-162] — called internally by `docreatenewversion` via `doretrievedocvspanfoo` — has **identical body** to `retrievevspanpm`. Both read the same root POOM fields.

---

### Question 2: Does the Returned Content Include Raw Link Orgl Bytes Interleaved with Text?

**`RETRIEVEDOCVSPAN` returns zero bytes of content.** The response is only the coordinate pair `(stream, width)`, encoded via `putretrievedocvspan` [putfe.c:327-331]:

```c
int putretrievedocvspan(typetask *taskptr, typespan *vspanptr)
{
    putnumber(taskptr->outp, RETRIEVEDOCVSPAN);
    putspan(taskptr, vspanptr);   // just two tumblers
}
```

#### What Happens If You Retrieve Using the Bounding Span

If the caller subsequently uses the bounding V-span as a V-spec for `RETRIEVE` (`doretrievev`), the critical function is `context2vstuff` [context.c:240-275]:

```c
bool context2vstuff(typetask *taskptr, typecontext *context,
                    typeispan *ispanptr, typevstuffset *vstuffsetptr)
{
    contextinfotype = context->contextinfo.granbottomcruminfo.infotype;
    switch (contextinfotype) {
      case GRANTEXT:
        // Returns TEXTID item — actual character bytes from permascroll
        vstuffset = taskalloc(sizeof(typetext));
        ((typeitemheader *)vstuffset)->itemid = TEXTID;
        context2vtext(context, ispanptr, vstuffset);
        break;
      case GRANORGL:
        // Returns ADDRESSID item — ONLY the ISA tumbler, NOT the orgl's bytes
        vstuffset = taskalloc(sizeof(typeaddress));
        ((typeitemheader *)vstuffset)->itemid = ADDRESSID;
        movetumbler(&context->totaloffset.dsas[WIDTH],
                    &((typelink *)vstuffset)->address);
    }
}
```

Key observations:

1. **Not interleaved**: Text occupies V = `"1.1"` to `"1.11"`, link occupies V = `"2.1"` to `"2.11"`. There is a large V-space gap between `"1.11"` and `"2.1"` containing no content crums. Retrieval finds each in its own region.

2. **Not raw orgl bytes**: The `GRANORGL` case returns an `ADDRESSID` item containing only `context->totaloffset.dsas[WIDTH]` — the I-space ISA tumbler (the link's identity number like `"1.1.0.1.0.1.0.2.1"`). The actual link orgl structure (its from/to endpoint data stored in the link's own POOM) is **never touched**. To read link internals you'd call `FOLLOWLINK`.

3. **Different item types in sequence**: If you retrieved using the bounding span, the `vstuffset` list would contain `TEXTID` items followed (non-adjacently in V-space) by `ADDRESSID` items — not byte-level interleaving but type-level mixing. The client's `Content_read()` handles both (`"t"` prefix for text, digit-start for address).

4. **The gap is silent**: The V-space between `"1.11"` and `"2.1"` has no POOM crums, so `retrieverestricted()` [retrie.c:87-110] simply finds nothing there. No filler bytes, no padding.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Single bounding span? | **Yes** — `retrievevspanpm` reads `cdsp.dsas[V]` + `cwid.dsas[V]` directly, always returning one span with `next=NULL` | `orglinks.c:165-172` |
| Span covers both subspaces? | **Yes** — `setwispnd` computes bounding box across text (V≈1.1) and link (V≈2.1) content | `wisp.c:207-214`; confirmed `retrieve_vspan_with_links.json`: `"at 1.1 for 1.2"` |
| Content returned by RETRIEVEDOCVSPAN? | **None** — only two tumblers (start, width) | `putfe.c:327-331` |
| Link orgl bytes in retrieval? | **No** — link granf crums yield only an `ADDRESSID` (ISA tumbler); raw orgl bytes are never emitted by `context2vstuff` | `context.c:264-271` |
| Interleaved with text? | **No** — text and link content are in non-overlapping, non-adjacent V-regions with a gap between them | `findnextlinkvsa`: link at V≥"2.1", text at V="1.1" |

The architectural reason is explained by `istextcrum`/`islinkcrum` [orglinks.c:246-261]: the POOM uses V-address structure (mantissa[0]=1, mantissa[1]≠0 means link crum) to segregate the two content types. `retrievevspanpm` ignores this structure entirely and returns the union bounding box; the finer decomposition requires `retrievevspansetpm` or post-retrieval filtering.

---

## Question 12 [gregory]

> Does RETRIEVEDOCVSPANSET always return exactly two VSpecs (one for text subspace 1.x, one for link subspace 0.2.x), or can it return more than two if there are gaps within a single subspace?

### Gregory's Answer

## KB Synthesis

RETRIEVEDOCVSPANSET returns **at most two VSpecs** — one per occupied subspace — not one per contiguous run within a subspace. Internal gaps within the text subspace do not cause additional VSpecs.

## Mechanism

`retrievevspansetpm()` at `orglinks.c:173-221` constructs spans using two distinct approaches per subspace [SS-VSPAN-VS-VSPANSET, Finding 0035]:

- **Text subspace (1.x):** Uses `maxtextwid()` (`orglinks.c:224-245`), described as a "recursive text-extent traversal." This produces a single width value representing the full extent of the text region — a bounding span, not an enumeration of contiguous runs.
- **Link subspace (2.x internally):** Constructed as a single span from the link displacement.

The `is1story()` check determines whether the POOM root's content occupies one or multiple subspaces, but the result is always at most one span per subspace.

## Observable return counts

| Document content | RETRIEVEDOCVSPANSET result |
|-----------------|---------------------------|
| Empty | NULL (0 spans) |
| Text only | 1 span: `{start: "1.1", width: "0.N"}` |
| Links only | 1 span: `{start: "2.1", width: "0.N"}` |
| Text + links | 2 spans: `[{start: "0", width: "0.1"}, {start: "1", width: "1"}]` |

[SS-DUAL-ENFILADE, Finding 0038] confirms the two-span maximum with concrete examples. Note also the normalization: when text coexists with links, the link subspace is reported with start `"0"` (normalized from the internal `2.x`); when links exist without text, the actual `2.x` position is reported.

## Consequence for intra-subspace gaps

Because `maxtextwid()` computes the full text extent recursively as a single value, content at `V:1.1` and `V:1.50` (with nothing between them) would be reported as a single text span from `1.1` to `1.50+N`, not two separate spans. The returned span is a **bounding box**, not a coverage map. This is the same lossy property identified for RETRIEVEDOCVSPAN ([SS-VSPAN-VS-VSPANSET], [EC-VSPAN-MISLEADING-SIZE]) — the single-subspace case of that lossiness applies here too.

The KB contains no evidence of RETRIEVEDOCVSPANSET returning more than two VSpecs under any normal operation sequence.

## Code Exploration

Now I have a complete, code-verified picture. Here is the full answer.

---

## Answer: RETRIEVEDOCVSPANSET Return Count

**Short answer:** The active code hard-caps the return at 2 VSpans. Gaps within a subspace do not produce additional VSpans. The general N-span tree-walk algorithm exists in the codebase but is compiled out with `#ifdef UnDEFined`.

---

### Terminology correction

The question says "VSpecs" but RETRIEVEDOCVSPANSET returns **VSpans** (`VSPANID = 2`), not VSpecs (`VSPECID = 3`). `xanadu.h:28-29` defines both, and `xanadu.h:73`:

```c
typedef typespan typevspan;
typedef typevspan * typevspanset;
```

A VSpec (`typevspec`) contains a document ISA plus a nested vspanset and is a different type. `putfe.c:154-155` confirms: when serializing items with `VSPANID`, it calls `putspan` (just stream + width), not `putitem` with `VSPECFLAG`.

---

### Call chain: fns.c → do1.c → orglinks.c

**`fns.c:129-141`** — top-level dispatcher:
```c
void retrievedocvspanset(typetask *taskptr)
{
  typeisa docisa;
  typevspanset vspanset;
  ...
  if (getretrievedocvspanset(taskptr, &docisa)
   && doretrievedocvspanset(taskptr, &docisa, &vspanset))
      putretrievedocvspanset(taskptr, &vspanset);
```

**`do1.c:322-336`** — `doretrievedocvspanset`:
```c
bool doretrievedocvspanset(typetask *taskptr, typeisa *docisaptr, typevspanset *vspansetptr)
{
  typeorgl docorgl;
  ...
  if (!findorgl(taskptr, granf, docisaptr, &docorgl, READBERT))
      return FALSE;

  if (isemptyorgl(docorgl)) {
      *vspansetptr = NULL;  /* Empty document returns empty vspanset */
      return TRUE;
  }

  return retrievevspansetpm(taskptr, docorgl, vspansetptr);
}
```

So the possible exit paths from this function are already:
- **0 spans**: empty document (`isemptyorgl` true) → returns `NULL`
- **1 or 2 spans**: non-empty document → delegated to `retrievevspansetpm`

---

### The active `retrievevspansetpm` (orglinks.c:173-221)

There are **two definitions** of `retrievevspansetpm` in the file. The second (line 266) is inside `#ifdef UnDEFined` — dead code. The first (line 173) is live.

```c
bool retrievevspansetpm(typetask *taskptr, typeorgl orgl, typevspanset *vspansetptr)
{
  tumbler voffset, maxwid;
  typevspan vspan, linkvspan;
  bool is1story();
  typecorecrum *ccptr;

  ccptr = (typecorecrum *) orgl;
  tumblerclear(&voffset);
  *vspansetptr = NULL;

  if (is1story(&ccptr->cwid.dsas[V])) {           /* [orglinks.c:184] */
      /* Case 1: text-only. Return ONE span. */
      vspan.itemid = VSPANID;
      movetumbler(&ccptr->cdsp.dsas[V], &vspan.stream);
      movetumbler(&ccptr->cwid.dsas[V], &vspan.width);
      vspan.next = NULL;
      putvspaninlist(taskptr, &vspan, vspansetptr);
      return TRUE;

  } else {                                          /* [orglinks.c:191] */
      /* Case 2: text + links. Return EXACTLY TWO spans. */
      linkvspan.itemid = VSPANID;
      movetumbler(&ccptr->cwid.dsas[V], &linkvspan.stream);
      linkvspan.stream.mantissa[1] = 0;             /* strip sub-digit */
      tumblerjustify(&linkvspan.stream);
      movetumbler(&ccptr->cwid.dsas[V], &linkvspan.width);
      linkvspan.width.mantissa[1] = 0;
      tumblerjustify(&linkvspan.width);
      linkvspan.next = NULL;

      maxtextwid(taskptr, ccptr, &voffset, &maxwid);
      vspan.itemid = VSPANID;
      tumblerclear(&vspan.stream);                  /* stream = 0 */
      movetumbler(&maxwid, &vspan.width);
      vspan.width.mantissa[0] = 0;                 /* strip 1st-story digit */
      vspan.next = NULL;

      putvspaninlist(taskptr, &vspan, vspansetptr);     /* text span */
      putvspaninlist(taskptr, &linkvspan, vspansetptr); /* link span */
      return TRUE;
  }
}
```

**`is1story` (`tumble.c:237-247`)** returns TRUE if the tumbler has only one non-zero mantissa digit:
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

When the root crum's V-width `cwid.dsas[V]` is a 1-story tumbler (only `mantissa[0]` is non-zero), the document contains only text content. When the V-width is multi-story (has sub-digits), it contains link references too.

**The critical structural fact**: `putvspaninlist` is called **at most twice** in the active code path. No loop, no recursion through the enfilade tree. The two spans are constructed from top-level root crum metadata (`ccptr->cwid`, `maxtextwid`) — not from tree traversal.

---

### The dead N-span code (`orglinks.c:266-313`)

```c
#ifdef UnDEFined

bool retrievevspansetpm(typetask *taskptr, typeorgl orgl, typevspanset *vspansetptr)
{
  tumbler voffset;
  tumblerclear(&voffset);
  *vspansetptr = NULL;
  walkorglonvpm(taskptr, (typecorecrum*)orgl, &voffset, vspansetptr);
  cleanupvspanlist(taskptr, vspansetptr);
  return (TRUE);
}

int walkorglonvpm(typetask *taskptr, typecorecrum *crumptr, tumbler *voffset, typevspanset *vspansetptr)
{
  if (is1story(&crumptr->cwid.dsas[V])) {
      /* emit one VSpan for this contiguous region */
      vspan.stream = voffset + crumptr->cdsp.dsas[V];
      vspan.width = crumptr->cwid.dsas[V];
      putvspaninlist(taskptr, &vspan, vspansetptr);
  } else {
      /* recurse into children */
      for (ptr = findleftson(...); ptr; ptr = findrightbro(ptr))
          walkorglonvpm(taskptr, ptr, &localvoffset, vspansetptr);
  }
}

int cleanupvspanlist(...) { /* merge adjacent spans */ }
```

`#endif` at `orglinks.c:313`.

This disabled version **would** return N spans reflecting actual gaps: it walks the enfilade recursively, emits one span per contiguous leaf region, then merges adjacent ones. Multiple disjoint regions — whether text gaps or multiple link entries — would each produce a span. This code is the semantically "correct" implementation; the active code is an approximation built from root-crum shortcuts.

---

### What the golden tests confirm

**Text-only document** — `three_links_vspan_growth.json`, label `"initial"`:
```
"spans": ["1.1-0.24"]
```
One span: `stream=1.1, width=0.24` — 24 chars of text.

**After 1st link**:
```
"spans": ["0-0.1", "1-1"]
```
Two spans: `stream=0, width=0.1` (text summary) and `stream=1, width=1` (link summary).

**After 2nd link**, **After 3rd link** — same result:
```
"spans": ["0-0.1", "1-1"]
```
Three links produce the same two spans as one link. The algorithm does **not** enumerate link entries individually.

---

### Subspace address correction

The question describes the link subspace as "0.2.x". That is not what the document POOM uses.

**`findnextlinkvsa` (`do2.c:151-167`)** computes the V-address for the first link reference in a document:
```c
tumblerclear(&firstlink);
tumblerincrement(&firstlink, 0, 2, &firstlink);  /* firstlink = 2 */
tumblerincrement(&firstlink, 1, 1, &firstlink);  /* firstlink = 2.1 */
```
`tumblerincrement(src, rightshift, amount, dst)` adds `amount` at position `lastNonzeroIdx + rightshift`. For a zero tumbler, it writes to `mantissa[0]`. So:
- After first call: `mantissa[0] = 2` → tumbler `2`
- After second call: idx of last nonzero in `2` = 0; `0 + 1 = 1`; `mantissa[1] += 1` → tumbler `2.1`

So the **link reference subspace starts at V = 2.1**, not 0.2.x. The `"0.2.x"` numbers you see in the output (`1.1.0.1.0.1.0.2.1`) are the **link ISA** (its address in the granfilade object space), not its virtual space position in the document's POOM.

The `setlinkvsas` in `do2.c:169-183` sets from/to VSAs for the **link object's own POOM** (1.1 and 2.1 within the link), separate from the document's POOM.

---

### Summary

| Condition | VSpans returned |
|---|---|
| Empty document (`isemptyorgl`) | 0 |
| Non-empty, text only (`is1story` of cwid) | 1 |
| Non-empty, text + ≥1 link reference | 2 (always, regardless of gap count) |
| Gaps within a subspace | No effect — algorithm does not see them |

**RETRIEVEDOCVSPANSET cannot return more than 2 VSpans** under any circumstances with the active code. The 2-span maximum is a structural consequence of the active `retrievevspansetpm` calling `putvspaninlist` at most twice, computing two summary spans from root-crum metadata rather than walking the enfilade tree.

Gaps within the text or link subspace are invisible to this operation because the algorithm approximates the occupied range from the root crum's `cdsp`/`cwid` fields and the `maxtextwid` scan — it does not enumerate contiguous regions. The disabled `walkorglonvpm` code would return N spans per distinct contiguous region, but that code is dead.

---

## Question 13 [gregory]

> When retrieving a V-span that crosses a POOM entry boundary (where two non-contiguous I-address ranges are mapped to adjacent V-positions), does the retrieval silently concatenate the content from both I-ranges into a single byte sequence?

### Gregory's Answer

## KB Synthesis

Yes, retrieval silently concatenates content from all I-address ranges that cover the queried V-span, assembled in V-position order.

## The Retrieval Path

The call chain for `retrieve_contents` is [PRE-RETRIEVE-CONTENTS]:

```
specset → specset2ispanset → ispanset2vstuffset → byte content
```

`specset2ispanset` converts V-specs to I-spans by walking the POOM. For a V-span that crosses multiple crum boundaries, this produces **one I-span per POOM crum** in the range. When those crums map to non-contiguous I-address ranges (e.g., because a `CREATELINK` ran between two `INSERT` operations), `specset2ispanset` returns a multi-element ispanset with disjoint I-address ranges.

`ispanset2vstuffset` then dereferences each I-span from the granfilade via raw byte copy (`movmem`) [SS-CONTENT-IDENTITY Finding 0034]. The multiple I-spans are processed in the order they appear in the ispanset.

## Why the Order Is V-Sorted

[INV-RETRIEVAL-V-SORTED] establishes that contexts accumulated during POOM B-tree traversal are maintained in ascending V-position order by `incontextlistnd()`. The ispanset fed into `ispanset2vstuffset` therefore reflects V-order, not I-address order. So when two non-contiguous I-ranges map to adjacent V-positions, their bytes are retrieved and assembled in V-order — silently concatenated.

## The Non-Contiguity Case Concretely

[INT-LINK-INSERT Finding 0063] documents the most common source of non-contiguous I-addresses at adjacent V-positions: `INSERT "ABC"` followed by `CREATELINK` followed by `INSERT "DEF"`. The text "ABC" occupies I.1–I.3 and "DEF" occupies I.2.1+ (a gap in the text I-address sequence because the link orgl consumed intermediate addresses). A `retrieve_contents` over the V-span covering both "ABC" and "DEF" walks two separate POOM crums with non-contiguous I-ranges, but the caller receives `"ABCDEF"` — the concatenation is fully transparent.

The evidence from [SS-COMPARE-VERSIONS]: when this same document is compared against a version created before the link, `compare_versions` reports **two** shared span pairs (not one), because the I-address gap is visible at the identity level. But `retrieve_contents` over the same V-span returns the bytes concatenated in V-order regardless.

## The Sporgl Evidence

[ST-LINK-CREATE Finding 0037] provides corroborating evidence from the link creation path. When `vspanset2sporglset` converts a V-span that maps to multiple non-contiguous I-regions (e.g., transcluded content from two sources), it produces one sporgl per I-region — the split is preserved for identity-tracking purposes. But for `retrieve_contents`, the downstream `ispanset2vstuffset` reassembles from those separate I-spans in V-order, producing a single concatenated byte sequence.

## Summary

The POOM lookup transparently handles I-address discontinuities: the retrieval produces one I-span per POOM crum within the queried V-range, resolves each to bytes via the granfilade, and assembles them in V-sorted order. From the caller's perspective, `retrieve_contents` over any V-span returns a single concatenated byte sequence — the I-address non-contiguity is invisible at the retrieval level, though it remains visible to identity-aware operations like `compare_versions`.

## Code Exploration

I now have a complete trace of the entire retrieval pipeline. Here is my answer.

---

## Retrieval Across POOM Entry Boundaries: Silent Concatenation

**Short answer: Yes.** When a V-span crosses a POOM entry boundary — where two non-contiguous I-address ranges map to adjacent V-positions — udanax-green silently concatenates the content from both I-ranges into a single byte sequence. The client receives one TEXT item with no indication of the I-space discontinuity.

---

### The Full Call Chain

**Step 1: `retrievev` dispatches to the domain logic**

`fns.c:175–187`:
```c
void retrievev(typetask *taskptr)
{
    if (getretrievev(taskptr, &specset)
     && doretrievev(taskptr, specset, &vstuffset))
        putretrievev(taskptr, &vstuffset);
```

**Step 2: `doretrievev` converts V→I then I→bytes** (`do1.c:338–346`)

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
    return specset2ispanset(taskptr, specset, &ispanset, READBERT)
        && ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr);
}
```

**Step 3: V→I conversion via the POOM** (`do2.c:34–36`, `orglinks.c:397–422`)

`specset2ispanset` calls `vspanset2ispanset` which calls `permute(orgl, vspanset, V, *, I)`. For each V-span in the input, `permute` calls `span2spanset`:

```c
// orglinks.c:425–454
typespanset *span2spanset(...) {
    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, V, NULL, I, NULL);
    for (c = context; c; c = c->nextcontext) {
        context2span(c, restrictionspanptr, V, &foundspan, I);
        nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
    }
}
```

**Step 4: All qualifying POOM crums are collected** (`retrie.c:87–110`)

`retrieverestricted` → `retrieveinarea` → `findcbcinarea2d`:

```c
// retrie.c:252–265
for (; crumptr; crumptr = getrightbro(crumptr)) {
    if (!crumqualifies2d(crumptr, offsetptr, span1start, span1end, index1, ...))
        continue;
    if (crumptr->height != 0) {
        findcbcinarea2d(findleftson(...), &localoffset, ...);
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd(headptr, context, index1);  // sorted by V-position
    }
}
```

When the requested V-span crosses two POOM leaf crums, **both are collected into the context list**, sorted by their V-coordinate (`incontextlistnd`, `context.c:75–111`).

**Step 5: Each POOM crum yields one I-span** (`context.c:176–212`)

`context2span` clips the requested V-span to the crum's V-range, then maps proportionally into I-space:

```c
// context.c:191–207
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
    // V-start of crum precedes restriction: shift I-start proportionally
    tumblerincrement(&grasp.dsas[idx2], 0,
        (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
    // V-end of crum exceeds restriction: trim I-end proportionally
    tumblerincrement(&reach.dsas[idx2], 0,
        -tumblerintdiff(&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);
}
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

Two POOM crums → two I-spans, each pointing into a different (non-contiguous) I-address range.

**Step 6: Each I-span is fetched from the granfilade** (`granf1.c:57–74`, `granf2.c:286–318`)

`ispanset2vstuffset` iterates the I-span list; for each I-span, `ispan2vstuffset` calls `retrieveinspan` to find the granfilade leaf crums, then `context2vstuff` → `context2vtext` to copy the raw bytes into a `typetext` item. Two I-spans → two `typetext` items in a linked list.

**Step 7: `puttextset` concatenates all consecutive TEXT items** (`putfe.c:189–206`)

This is the decisive operation:

```c
// putfe.c:189–206
int puttextset(typetask *taskptr, typetext **textptrptr)
{
    // Pass 1: sum the total byte count across all consecutive TEXTID items
    for (i = 0, textptr = *textptrptr; textptr && textptr->itemid == TEXTID; textptr = textptr->next)
        i += textptr->length;

    // Emit ONE TEXTFLAG header with the combined length
    xuputc(TEXTFLAG, taskptr->outp);
    putnumber(taskptr->outp, i);

    // Pass 2: emit all bytes from all consecutive TEXTID items in order
    for (textptr = *textptrptr; textptr && textptr->itemid == TEXTID; textptr = textptr->next)
        for (i = 0; i < textptr->length; ++i)
            xuputc(textptr->string[i], taskptr->outp);

    *textptrptr = last;  // advance past all consumed items
}
```

The outer `putitemset` (`putfe.c:130–131`) also collapses consecutive TEXTID items in the item count:

```c
while (((typeitemheader *)temp)->itemid == TEXTID
    && ((typeitemheader *)temp)->next
    && ((typeitemheader *)temp)->next->itemid == TEXTID)
    temp = (typeitemset)((typeitemheader *)temp)->next; /* count lots of textitems as one item */
```

---

### Conclusion

The concatenation is **intentional and explicit**. The POOM is a permutation matrix that virtualizes I-space into V-space; from the V-space perspective the content is logically contiguous. The retrieval pipeline respects this abstraction:

1. `findcbcinarea2d` collects all POOM crums that intersect the requested V-span — regardless of how many there are or how non-contiguous their I-ranges are.
2. `context2span` maps each crum's overlapping V-region to its corresponding I-region, yielding one I-span per crum.
3. `ispan2vstuffset` fetches the actual bytes for each I-span separately from the granfilade, producing one `typetext` item per I-span.
4. `puttextset` (`putfe.c:189–206`) unconditionally concatenates all consecutive TEXTID items into a **single TEXTFLAG wire packet** — one length field, one byte stream.

The client receives a single text payload covering the full requested V-span. There is no boundary marker, no gap indicator, and no mechanism to distinguish which bytes came from which I-address range. The I-space discontinuity is entirely hidden at the FEBE protocol level.

---

## Question 14 [gregory]

> After COPY transcludes content from doc1 into doc2, does retrieving the same V-span from both documents return byte-identical content, and is the retrieval path identical (same granfilade leaf nodes accessed)?

### Gregory's Answer

## KB Synthesis

## COPY Transclusion: Retrieval Equivalence

**Byte-identical content: Yes, unconditionally.**

COPY does not duplicate bytes in the granfilade. It calls `docopy` with an existing `ispanset` (already-allocated I-addresses from the source) and writes new V→I mappings into the target document's POOM via `insertpm` [ST-VCOPY, Finding 0046]. No call to `inserttextingranf` occurs — no new I-addresses are allocated, no new granfilade leaf nodes are written.

Since both doc1 and doc2 map their respective V-spans to the same I-addresses, and [INV-IADDR-IMMUTABILITY] guarantees content at an I-address never changes, retrieval from either document must return byte-identical results. [ST-VCOPY, Finding 0018] states this explicitly: `I-addresses(target[v_target..len]) = I-addresses(source[v_source..len])`.

**Same retrieval path: Split answer — POOM differs, granfilade is identical.**

The retrieval pipeline is: V-span → POOM traversal → I-address → granfilade traversal → bytes.

*POOM layer (differs):* Each document has its own POOM enfilade — separate B-tree structures, separate crums, separate disk blocks [SS-POOM-MUTABILITY, Finding 0072]. The path through doc1's POOM tree to find the I-address is physically distinct from the path through doc2's POOM tree.

*Granfilade layer (identical):* The granfilade is a single shared global structure [SS-UNIFIED-STORAGE, Finding 0059; SS-DUAL-ENFILADE, Finding 0012]. Once both POOMs resolve to the same I-addresses, `ispanset2vstuffset` traverses the same granfilade tree nodes to locate the bytes. Same I-address → same B-tree traversal path → same leaf nodes (`typecorecrum` instances) → same bytes.

The shared cache reinforces this: [SS-CACHE-MECHANISM] shows all crums from all enfilades share a single grim-reaper list. A granfilade leaf loaded by doc1's retrieval sits in the same cache for doc2's retrieval. There is no per-document granfilade copy.

**Summary:**

| Layer | doc1 vs doc2 path |
|-------|-------------------|
| POOM B-tree traversal | Different (separate trees) |
| I-addresses resolved | Identical (shared by transclusion) |
| Granfilade B-tree traversal | Identical (same I-address → same tree path) |
| Granfilade leaf nodes accessed | Identical (physically the same crums) |
| Bytes returned | Identical (immutable content at same I-addresses) |

This is the core mechanism by which Xanadu achieves its "bytes never die, addresses never change" property [INV-IADDR-IMMUTABILITY, FC-GRANF-ON-DELETE]: transclusion creates reference sharing at the POOM level without any duplication at the storage level.

## Code Exploration

Here is the full answer, with every claim grounded in specific source lines.

---

## Answer: COPY Transclusion — Byte Identity and Granfilade Path Identity

**Short answer:** YES on both counts. After `COPY`, retrieving the transcluded content from doc2 is byte-identical to doc1, and the granfilade leaf nodes accessed are the same. What differs is only the per-document POOM traversal path, which converges on the same I-addresses before entering the shared granfilade.

---

## Full Trace

### 1. `docopy` entry point [`do1.c:45–65`]

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    typeispanset ispanset;
    typeorgl docorgl;
    ...
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)   /* always TRUE [do2.c:110-113] */
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    ...
    );
}
```

Two operations carry the semantic weight:
- `specset2ispanset` — translates doc1's V-spans into I-spans via doc1's POOM
- `insertpm` — writes those I-spans into doc2's POOM at the new V-position `vsaptr`

`acceptablevsa` is a stub that always returns `TRUE` [`do2.c:110-113`].

---

### 2. V→I translation via doc1's POOM [`do2.c:14–46`]

```c
for (; specset; specset = ...) {
    if (specset->itemid == VSPECID) {
        findorgl(taskptr, granf, &specset->docisa, &docorgl, type);  /* doc1's POOM */
        ispansetptr = vspanset2ispanset(taskptr, docorgl,
                                        specset->vspanset, ispansetptr);
    }
}
```

`vspanset2ispanset` [`orglinks.c:397-402`] calls `permute` → `span2spanset` → `retrieverestricted` [`retrie.c:56-85`] → `findcbcinarea2d` [`retrie.c:229-268`].

This walks doc1's POOM tree. Each leaf crum (a 2D bottom crum) contains a 2D bounding box in (I, V) space. `context2span` [`context.c:176-212`] clips the crum's I-extent to the requested V-restriction and returns an `ISPANID` span.

**Result:** `ispanset` holds the raw permascroll I-addresses for the content in doc1.

---

### 3. I-spans stored verbatim into doc2's POOM [`orglinks.c:75-134`]

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
    for (; sporglset; sporglset = ...) {
        unpacksporgl(sporglset, &lstream, &lwidth, &linfo);

        movetumbler(&lstream, &crumorigin.dsas[I]);   /* I-coord = source I-address */
        movetumbler(&lwidth,  &crumwidth.dsas[I]);    /* I-width = source I-width   */
        movetumbler(vsaptr,   &crumorigin.dsas[V]);   /* V-coord = new position in doc2 */
        /* ... compute V-width ... */

        insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
        tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);
    }
}
```

**The I-coordinates are moved with `movetumbler` — a direct copy, no arithmetic, no transformation.** No new content is written to the granfilade. A new 2D POOM crum is added to doc2's enfilade mapping its new V-position to the exact same I-address that doc1's POOM crum held.

---

### 4. Retrieval from doc2 [`do1.c:338-346`]

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
    return
       specset2ispanset(taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr);
}
```

- `specset2ispanset` now walks **doc2's** POOM. It finds the crum that `insertpm` placed there, clips it, and returns its I-extent. This is the **same I-span** as in doc1.
- `ispanset2vstuffset` [`granf1.c:58-74`] calls `ispan2vstuffset` [`granf2.c:286-318`].

---

### 5. Granfilade lookup by I-address — the shared path [`granf2.c:286-318`, `retrie.c:112-136`]

```c
typevstuffset *ispan2vstuffset(..., typeispan *ispanptr, ...)
{
    movetumbler(&ispanptr->stream, &lowerbound);
    tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
    context = retrieveinspan((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
    for (temp = context; temp; temp = temp->nextcontext)
        context2vstuff(taskptr, temp, ispanptr, &vstuffset);
}
```

`retrieveinspan` [`retrie.c:112-136`] dispatches to `findcbcinspanseq` [`retrie.c:307-329`], which walks the single global `granf` tree, calling `crumintersectsspanseq` at each node to find leaf crums covering the I-address range.

**There is one granfilade.** It is not per-document. The `fullcrumptr` passed in is the global `granf`. When the I-span is identical, `findcbcinspanseq` follows the identical branching sequence — every `getrightbro`/`findleftson` call, every `dspadd` offset accumulation — to arrive at the **same leaf crums** in both retrievals.

---

### 6. Byte extraction [`context.c:277-309`]

```c
int context2vtext(typecontext *context, typeispan *ispanptr, typevstuffset vstuffset)
{
    movetumbler(&context->totaloffset.dsas[WIDTH], &crumistart);
    /* ... clip to ispanptr->stream / width ... */
    movmem(&context->contextinfo...textstring[i], vstuffset->string, vtlength);
}
```

Bytes come from `textstring` embedded directly in the granfilade leaf crum. Same I-address → same leaf crum → same `textstring` array → byte-identical output.

---

## Summary Table

| Question | Answer | Why |
|---|---|---|
| Byte-identical content from doc1 and doc2? | **YES** | `insertpm` copies I-addresses verbatim [`orglinks.c:105-113`]. Same I-address → same granfilade crum → same `textstring`. |
| Same granfilade leaf nodes accessed? | **YES** | `ispan2vstuffset` → `retrieveinspan` → `findcbcinspanseq` walks the single global `granf` by I-address. Same I-span → identical tree path → identical leaf set. |
| Same POOM traversal path? | **NO** | doc1 and doc2 each have their own POOM enfilade (fetched via `findorgl` [`granf1.c:17-41`] → `fetchorglgr` [`granf2.c:22-81`]). They are independent trees. Their V-addresses differ. |

**COPY is true transclusion**: the permascroll content is referenced, never copied. The granfilade is append-only and immutable at existing addresses. `insertpm` adds a single 2D POOM crum to doc2 pointing at the same I-address — there is no `inserttextingranf` call inside `docopy`, only inside `doinsert`. The shared I-address is the implementation of content identity.

---

## Question 15 [gregory]

> After CREATENEWVERSION, does retrieving the full text span from the version return byte-identical content to retrieving the same span from the original, even if the original has been subsequently edited?

### Gregory's Answer

## KB Synthesis

**Short answer: Yes for the version (stable snapshot), No for equality with the edited original.**

## At creation time

Immediately after `CREATENEWVERSION(original)`, the version's POOM maps the same V-positions to the same I-addresses as the original's POOM [ST-VERSION-CREATE, Finding 0043/0046]. Both retrieve byte-identical content, because they draw from the same I-addresses in the granfilade, which contains the actual bytes [INV-IADDR-IMMUTABILITY].

## After editing the original

**The version's content is stable.** Version and original have independent POOM trees from the moment of creation [FC-VERSION-ISOLATION, Finding 0072]:

> Edits to the original document modify only the original's POOM. Edits to the version modify only the version's POOM. Neither affects the other.

When the original is subsequently edited:
- **INSERT** adds new V→I mappings to the original's POOM and shifts existing V-positions, but does not touch the version's POOM [FC-VERSION-ISOLATION, ST-INSERT]
- **DELETE** removes V→I mappings from the original's POOM, but the version's POOM retains those mappings [ST-DELETE, FC-VERSION-ISOLATION]
- **REARRANGE** permutes V-positions in the original's POOM, leaving the version's POOM unchanged [ST-REARRANGE]

The granfilade (content bytes) is append-only and immutable [SS-POOM-MUTABILITY]:

> The granfilade is immutable, append-only. The POOM is the sole locus of destructive mutation.

So the bytes the version's POOM points to are never modified — only the mapping in the original's POOM changes.

## Result

| Retrieval | Content returned |
|-----------|-----------------|
| Version (any time after creation) | Creation-time snapshot — unchanged |
| Original before editing | Byte-identical to version |
| Original after editing | Post-edit content — diverges from version |

Retrieving the full text span from the version always returns the creation-time bytes. After the original is edited, the version and original no longer return byte-identical content. The version is a permanent snapshot of the original's text subspace at creation time [ST-VERSION-CREATE, FC-VERSION-ISOLATION, INV-IADDR-IMMUTABILITY].

One caveat: CREATENEWVERSION copies only the **text** subspace (1.x), not the link subspace (2.x) [ST-VERSION-CREATE, Finding 0043]. If "full text span" is interpreted as the document's text vspan from `retrievedocumentpartofvspanpm`, this is exactly what was copied and will be stable. Link orgl entries at 2.x are not present in the version's POOM at all.

## Code Exploration

I now have everything needed for a complete answer. Here it is:

---

## Answer: Version Retrieval and Byte Identity After Original Edits

**Yes. Retrieving the full text span from a version returns byte-identical content to what was in the original at the time `CREATENEWVERSION` was called, even after the original has been subsequently edited.** This is not accidental — it is an architectural consequence of how the I-address layer and the POOM work.

---

### The Mechanism, Step by Step

#### Step 1: `docreatenewversion` captures a snapshot of I-addresses

`docreatenewversion` [do1.c:260–298] does the following:

```c
// do1.c:281-293
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) return FALSE;

vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);   // docisa = ORIGINAL document
vspec.vspanset = &vspan;              // V-span = original's V-extent

addtoopen(newisaptr, user, TRUE, WRITEBERT);
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

The `vspec` is built with `docisa` pointing to the **original** and `vspanset` containing the original's current V-span. This is the only input to `docopyinternal`.

#### Step 2: `doretrievedocvspanfoo` reads the original's V-extent from the POOM root

`doretrievedocvspanfoo` [do1.c:301–309] calls `retrievedocumentpartofvspanpm` [orglinks.c:155–162]:

```c
// orglinks.c:155-162
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge */
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This reads the root crum's V-dimension displacement (`cdsp.dsas[V]`) and width (`cwid.dsas[V]`) — the bounding box of the entire document tree in V-space. This covers the **text subspace** (V ≥ 1.x), not the link subspace (V = 0.x). Finding 0043 confirms only text content is copied.

#### Step 3: `docopyinternal` → `specset2ispanset` converts V→I at versioning time

`docopyinternal` [do1.c:66–82]:

```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED);
```

`specset2ispanset` [do2.c:14–46] sees a `VSPECID` item, fetches the **original document's POOM** via `findorgl`, then calls `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` [orglinks.c:397–453]. This **walks the original document's POOM tree at the moment of the call**, extracting the I-spans (granfilade addresses) corresponding to all its V-addresses:

```c
// do2.c:34-37
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl,
    ((typevspec *)specset)->vspanset, ispansetptr))
```

These I-addresses are **permanent** — they are the addresses in the granfilade where the actual bytes live.

#### Step 4: `insertpm` stores those I-addresses in the new version's own POOM

`insertpm` [orglinks.c:75–134] creates bottom crums in the **new version's POOM** (not the original's), mapping:
- `crumorigin.dsas[I]` = the captured I-address (granfilade position of content)
- `crumwidth.dsas[I]` = the captured I-width
- `crumorigin.dsas[V]` = V-address in the new version's V-space
- `crumwidth.dsas[V]` = V-width in the new version's V-space

```c
// orglinks.c:105-130
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);   // I-address of content
    movetumbler (&lwidth, &crumwidth.dsas[I]);
    movetumbler (vsaptr, &crumorigin.dsas[V]);     // V-address in new doc
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
}
```

The version's POOM is **a completely separate enfilade tree** stored as its own orgl in the granfilade. It has no shared structure with the original's POOM.

#### Step 5: The granfilade is append-only for content

Content is written by `inserttextgr` [granf2.c:83–109] via `insertseq`:

```c
// granf2.c:95-101
for (; textset; textset = textset->next) {
    locinfo.granstuff.textstuff.textlength = textset->length;
    movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);
}
```

There is **no `deletetextgr`**, **no `overwritetextgr`**, and no other function that modifies bytes stored at a granfilade I-address. The granfilade is append-only for content: once bytes are written at an I-address, they are never moved, overwritten, or deleted.

#### Step 6: Subsequent edits to the original only touch the original's POOM

When the original document is edited after versioning:
- `doinsert` → `insertnd` on the original's POOM [do1.c:117–123, insertnd.c:15–111]
- `dodeletevspan` → `deletend` on the original's POOM [do1.c:162–167, orglinks.c:144–151]
- `dorearrange` → `rearrangend` on the original's POOM [do1.c:34–43]

All of these operate **exclusively on the original document's orgl tree**. Finding 0067 (Frame Axiom F0) confirms this by both code inspection and empirical testing: operations on one document's POOM never touch another document's POOM.

#### Step 7: Retrieval from the version uses the version's own POOM

`RETRIEVE` on the version calls `doretrievev` → `specset2ispanset` + `ispanset2vstuffset`. `specset2ispanset` now walks the **version's own POOM** to get I-addresses, then `ispanset2vstuffset` → `ispan2vstuffset` [granf1.c:57–74, granf2.c:286–318] reads the bytes from the granfilade at those I-addresses. Those bytes are the same bytes that were written there when the original was first created — completely unaffected by any subsequent edits to the original's POOM.

---

### Golden Test Confirmation

Two golden tests directly verify this:

**`golden/versions/modify_original_after_version.json`** — insert " modified" into original after versioning:
```json
{"op": "retrieve_contents", "doc": "original", "result": ["Original text modified"]}
{"op": "retrieve_contents", "doc": "version",  "result": ["Original text"]}
```

**`golden/versions/delete_from_original_check_version.json`** — delete first 5 chars from original after versioning:
```json
{"op": "retrieve_contents", "doc": "original", "result": ["to delete"]}
{"op": "retrieve_contents", "doc": "version",  "result": ["Text to delete"]}
```

Both confirm byte-identical preservation of the versioned content.

---

### Summary

| Property | Evidence | Citation |
|---|---|---|
| Version captures I-addresses from original at versioning time | `specset2ispanset` walks original's POOM | do2.c:34–37 |
| I-addresses stored in version's own separate POOM | `insertpm` writes to new orgl | orglinks.c:99–133 |
| Granfilade content at I-addresses never changes | No `deletetextgr`; `insertseq` is append-only | granf2.c:95–101 |
| Editing original only modifies original's POOM | `insertnd`/`deletend` are tree-local | insertnd.c:15–111, edit.c:30–75 |
| Retrieval from version reads version's own POOM | `specset2ispanset` on version's POOM | do2.c:14–46 |
| Empirically confirmed | Two golden tests | golden/versions/*.json |

**The architecture guarantees byte identity.** The I-address layer (granfilade content) is permanent and immutable once written. `CREATENEWVERSION` takes a snapshot of I-address mappings at call time. The two POOMs (original and version) diverge from that point onward, each independently mapping V→I in their own trees. Subsequent edits to the original update only the original's V→I mapping — they cannot reach back and alter the version's POOM or the bytes in the granfilade at the I-addresses the version references.

---

## Question 16 [gregory]

> When a V-span request partially overlaps a POOM entry (e.g., requesting V:[1.3,1.5] when a single entry covers V:[1.1,1.7]), does the retrieval slice the I-address range correspondingly, or does it return the full entry's content?

### Gregory's Answer

## KB Synthesis

## Retrieval Slices the I-Address Range Correspondingly

The POOM's linear mapping within each crum means a partial-overlap query returns only the I-addresses corresponding to the requested V sub-range — not the full crum's content.

### The Mechanism

Each POOM bottom crum stores a dual-space coordinate pair: `(V_origin, I_origin, width)`, where both V and I dimensions share the same numeric width value [SS-POOM-BOTTOM-CRUM, INV-WIDTH-VALUE-EQUIVALENCE]. The mapping within a crum is a pure linear displacement:

```
I_address = I_origin + (V_address - V_origin)
```

When `findcbcinarea2d()` traverses the POOM tree searching for the query range V:[1.3,1.5], it classifies each crum via `whereoncrum()` [SS-WHEREONCRUM]. For the crum covering V:[1.1,1.7]:

- The query's left boundary (1.3) falls THRUME (strictly interior)
- The query's right boundary (1.5) falls THRUME (strictly interior)

The context accumulated by `incontextlistnd()` [SS-CONTEXT-LIST] captures the **intersection** of the query interval with the crum's interval. The `totaloffset.dsas[V]` in the accumulated context reflects the query start (1.3), and the width is clipped to the query extent (0.2).

Applying the linear mapping: `I_start = I_origin + (1.3 - 1.1) = I_origin + 0.2`. The returned I-span covers [I_origin+0.2, I_origin+0.4] — exactly the I-addresses corresponding to V:[1.3,1.5].

### Supporting Evidence

This behavior is confirmed by several KB entries:

- **INV-SINGLE-CHAR-GRANULARITY**: every byte position has exactly one I-address; the one-to-one linear mapping within a crum enables precise sub-range slicing.
- **ST-INSERT (Finding 0030)**: the postcondition shows `D(v-n)` for shifted content — V-to-I mapping is a displacement function, not a lookup table. Sub-ranges of any V-span map to sub-ranges of the corresponding I-span.
- **SS-SPORGL (Finding 0013)**: `vspanset2sporglset` converts each vspan to I-addresses via the document's enfilade. It produces one sporgl per contiguous I-region corresponding to the requested V-span — not one sporgl per touched crum at full crum width.
- **PRE-DELETE (Finding 0075)**: the `slicecbcpm` cutting mechanism physically splits a crum at an interior boundary when needed for DELETE. This confirms the system can identify and operate on partial crum extents. For reads, the same boundary arithmetic applies without needing to physically split.
- **SS-FIND-LINKS (Finding 0028)**: partial transclusion (e.g., copying "link" from "hyperlink text") returns I-addresses for only the copied portion — exactly the I-sub-range corresponding to the transcluded V-span.

### Summary

For a query V:[1.3,1.5] against a crum V:[1.1,1.7]→I:[I_origin,I_origin+0.6]:

| Query boundary | `whereoncrum` result | Action |
|---|---|---|
| 1.3 (left) | THRUME | clip crum's left extent to 1.3 |
| 1.5 (right) | THRUME | clip crum's right extent to 1.5 |

**Returned**: I_span = [I_origin+0.2, I_origin+0.4], width 0.2.

The full crum content (width 0.6) is never returned for a narrower query.

## Code Exploration

---

## Answer: Partial V-span Overlap — The Retrieval **Slices** the I-range Proportionally

The code **does not return the full entry's content**. It clips the I-address range proportionally to match the V-span restriction. Here is the full traced execution path.

---

### Call Stack: `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → `context2span`

---

### Step 1 — Entry point: `vspanset2ispanset` [`orglinks.c:397–402`]

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
    typespanset *permute();
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`V=1` is the **restriction** index (we're filtering by V-address), `I=0` is the **target** index (we want to produce I-spans).

---

### Step 2 — `permute` iterates over V-spans [`orglinks.c:404–422`]

```c
typespanset *permute(typetask *taskptr, typeorgl orgl, typespanset restrictionspanset,
                     INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                      restrictionindex, targspansetptr, targindex);
    }
    return (save);
}
```

Each span in the requested V-span set is handled separately by `span2spanset`.

---

### Step 3 — `span2spanset` retrieves matching crums and clips them [`orglinks.c:425–454`]

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl,
                          typespanset restrictionspanptr, INT restrictionindex,
                          typespanset *targspansetptr, INT targindex)
{
    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                                  (typespan*)NULL, targindex, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
        nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, ...);
    }
    ...
}
```

`retrieverestricted` finds all POOM bottom-crums whose **V coordinate overlaps** the requested V-span. For each such crum, `context2span` is called to produce the output I-span.

---

### Step 4 — `retrieverestricted` / `findcbcinarea2d` qualifies crums [`retrie.c:56–110`, `retrie.c:229–305`]

`retrieverestricted` [`retrie.c:56`] calls `retrieveinarea` which calls `findcbcinarea2d`. The key filter is `crumqualifies2d` [`retrie.c:270–305`]:

```c
bool crumqualifies2d(typecorecrum *crumptr, typedsp *offset,
                     tumbler *span1start, tumbler *span1end, INT index1, ...)
{
    endcmp = whereoncrum(crumptr, offset, span1end, index1);
    if (endcmp <= ONMYLEFTBORDER) return (FALSE);  // crum is entirely right of our span end

    startcmp = whereoncrum(crumptr, offset, span1start, index1);
    if (startcmp > THRUME) return (FALSE);          // crum is entirely left of our span start

    ...
    return (TRUE);
}
```

A crum qualifies if it **partially or fully overlaps** the requested V-span — including the single-entry case V:[1.1,1.7] when requesting V:[1.3,1.5].

---

### Step 5 — The critical function: `context2span` clips the I-range [`context.c:176–212`]

This is where the slicing happens:

```c
int context2span(typecontext *context, typespan *restrictionspanptr,
                 INT idx1, typespan *foundspanptr, INT idx2)
{
    movetumbler(&restrictionspanptr->stream, &lowerbound);
    tumbleradd(&lowerbound, &restrictionspanptr->width, &upperbound);
    prologuecontextnd(context, &grasp, &reach);
    //   grasp.dsas[V] = crum's V-start (e.g. 1.1)
    //   grasp.dsas[I] = crum's I-start
    //   reach.dsas[V] = crum's V-end   (e.g. 1.7)
    //   reach.dsas[I] = crum's I-end

    if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
        // Crum starts before requested V-start → advance I-start by the V-gap
        tumblerincrement(&grasp.dsas[idx2], 0,
            (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
            &grasp.dsas[idx2]);
    }
    if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
        // Crum ends after requested V-end → retract I-end by the V-overshoot
        tumblerincrement(&reach.dsas[idx2], 0,
            -tumblerintdiff(&reach.dsas[idx1], &upperbound),
            &reach.dsas[idx2]);
    }

    movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);  // I-start (clipped)
    tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);  // I-length (clipped)
    ...
}
```

**Low-end clip** [`context.c:191–196`]: If the crum's V-start (1.1) is less than the requested V-start (1.3), the I-start is advanced by `tumblerintdiff(1.3, 1.1) = 2` positions.

**High-end clip** [`context.c:197–203`]: If the crum's V-end (1.7) exceeds the requested V-end (1.5), the I-end is retracted by `tumblerintdiff(1.7, 1.5) = 2` positions.

`tumblerintdiff` [`tumble.c:591–596`] computes the integer difference (`a - b`, returning `mantissa[0]`), so this arithmetic is exact integer arithmetic on tumbler positions.

---

### Step 6 — Why V and I advance at the same integer rate in a single POOM entry

From `wisp.h:19–20`, the POOM crum uses two parallel tumbler dimensions:

```c
#define I  0
#define V  1
```

Each POOM bottom-crum's `cwid` stores both `dsas[I]` (I-width) and `dsas[V]` (V-width), and they are equal for a contiguous text mapping — this is the defining property of a permutation matrix: every character of text occupies exactly one I-address and maps to exactly one V-address. `insertpm` [`orglinks.c:75–134`] sets both widths identically:

```c
movetumbler(&lwidth, &crumwidth.dsas[I]);
...
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);  // inc = tumblerintdiff(&lwidth, &zero)
```

So `crumwidth.dsas[I] == crumwidth.dsas[V]` for a plain text insertion.

---

### Conclusion

For a request of V:[1.3,1.5] against a single POOM entry covering V:[1.1,1.7]:

1. `crumqualifies2d` accepts the crum because V:[1.1,1.7] overlaps V:[1.3,1.5]. [`retrie.c:270–305`]
2. `context2span` clips the I-range at both ends by the V-overlap gaps:
   - I-start is advanced by 2 (the distance from V:1.1 to V:1.3). [`context.c:191–196`]
   - I-end is retracted by 2 (the distance from V:1.5 to V:1.7). [`context.c:197–203`]
3. Only the **proportional sub-range of I-addresses** is returned — not the full entry.

The retrieval **slices the I-address range proportionally**. This is not a coincidence; it is a fundamental invariant of the POOM (Permutation Of Original Media): V and I coordinates advance in lockstep (1:1), so any V-subrange maps precisely to the corresponding I-subrange. The clipping arithmetic in `context2span` enforces this invariant for partial overlaps.

---

## Question 17 [gregory]

> Does retrieval of link subspace content (V-addresses in 0.2.x) return the raw link orgl structure as bytes, and if so, what is the byte layout — are the three endsets stored as serialized tumbler sequences?

### Gregory's Answer

## KB Synthesis

## Retrieving Link Subspace Content

The KB gives partial answers here, and I'll be explicit about where it runs out.

### What the retrieval path does

`retrieve_contents` calls `doretrievev` → `specset2ispanset` → `ispanset2vstuffset(granf, ispanset)`. The last call looks up content bytes in the granfilade at the specified I-addresses. [PRE-RETRIEVE-CONTENTS/Finding 0010]

When the specset covers V-positions in the link subspace (0.x / internally 2.x), the I-addresses extracted are link orgl ISAs — addresses like `1.1.0.1.0.1.0.2.1`. These are **document-address-space tumblers**, not permascroll addresses. `ispanset2vstuffset` is type-agnostic [SS-DUAL-ENFILADE/Finding 0011], so it attempts the lookup anyway. The KB says this "produces NULL or garbage bytes — a silent failure." [PRE-RETRIEVE-CONTENTS/Finding 0010]

### The contradictory observation

Finding 0024 [SS-ADDRESS-SPACE] shows the Python febe client returning `{"link_id": "1.1.0.1.0.1.0.2.1"}` from `retrieve_contents` on the link subspace. This looks like client-side interpretation, not raw bytes from the granfilade. The KB doesn't resolve how the client produces this representation — it could be detecting the link subspace and calling a different code path, or the client is parsing whatever bytes come back and recognizing the tumbler pattern.

### What the link orgl actually contains

FOLLOWLINK reads endsets at sub-addresses **0.1**, **0.2**, and **0.3** relative to the link's ISA via `retrieverestricted()` [SS-FOLLOWLINK/Finding 0048]. This tells us the link orgl stores its FROM/TO/THREE endsets at these sub-I-addresses, each containing a sporgl (I-address + width + source-doc ISA) [SS-SPORGL/Finding 0013]. The link ISA structure allocates at `docISA.0.2.N` (element field 2) [SS-ADDRESS-SPACE/Finding 0065].

### What the KB does not answer

The **raw serialized byte layout** of a link orgl crum in the granfilade is not documented in any finding. The KB documents the logical structure (sporgls at 0.1/0.2/0.3 sub-addresses, accessed via `retrieverestricted`) but not the on-disk or in-memory byte encoding of those sporgls. Whether `ispanset2vstuffset` applied to a link ISA hits the link orgl's crum data and returns its bytes verbatim, or misses entirely and returns zeros, is not answerable from the KB.

The short answer: the KB confirms you don't get a meaningful text-like byte stream. You get either nothing or whatever the granfilade crum containing the link orgl serializes to — and the byte format of that serialization is below the abstraction level the findings cover.

## Code Exploration

I now have all the source evidence needed. Let me write the complete answer.

---

## Retrieval of Link Subspace Content in udanax-green

### Short Answer

No. Retrieving V-addresses in the link subspace (V ≥ `0.2~`) does **not** return the raw link orgl structure as bytes. It returns the link's **ISA tumbler** (granfilade identity address) as an `ADDRESSID` item on the FEBE wire. The three endsets are stored as 2D POOM crums inside the link's private orgl — they are inaccessible via `retrievev` and require `followlink` or `retrieveendsets` to read.

---

### 1. Where is the link subspace?

`orglinks.c:37` (`findvsatoappend`):
```c
tumblerclear (&linkspacevstart);
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);
```

This sets `linkspacevstart` = `{exp=0, mantissa=[2,0,...]}` = FEBE wire form `0.2~`. The link subspace starts at V = `0.2~`. Actual link placements begin at `0.2.1~` per `findnextlinkvsa` (`do2.c:157-158`):

```c
tumblerincrement (&firstlink, 0, 2, &firstlink);   // → mantissa=[2,0,...]
tumblerincrement (&firstlink, 1, 1, &firstlink);   // → mantissa=[2,1,0,...] = "0.2.1~"
```

So the first link in a document lives at V = `0.2.1~`, the second at `0.2.2~`, etc.

---

### 2. What does `retrievev` do with a V-address in the link subspace?

The call path from the FEBE request:

**`fns.c:175-187`** → `retrievev()` → `doretrievev()`  
**`do1.c:338-346`** → `doretrievev`:
```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
  typeispanset ispanset;
    return
       specset2ispanset (taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```

**Step 1: V-span → I-span** via the document's POOM  
`do2.c:14-46` → `specset2ispanset` → `vspanset2ispanset` → `permute` → `retrieverestricted` on the document orgl.

The document orgl (a POOM = permutation matrix enfilade) maps V-coordinates to I-coordinates. The V-span `[0.2.1~, 0.2.1~ + width]` maps to an I-span covering the granfilade positions where the link's record lives. This mapping is performed by `orglinks.c:397-422` (`vspanset2ispanset` / `permute` / `span2spanset`).

**Step 2: I-span → content** from the granfilade  
**`granf1.c:58-74`** → `ispanset2vstuffset` → `ispan2vstuffset` (`granf2.c:286-318`) → `retrieveinspan` → `findcbcinspanseq`.

The granfilade (gran enfilade) is keyed on granf-sequential (WIDTH) addresses. At the I-address corresponding to the link, the bottom crum is a **`GRANORGL`** type, not `GRANTEXT`. The `context2vstuff` function handles this at `context.c:240-275`:

```c
bool context2vstuff(typetask *taskptr, typecontext *context, typeispan *ispanptr, typevstuffset *vstuffsetptr)
{
  INT contextinfotype = context->contextinfo.granbottomcruminfo.infotype;
  if (contextinfotype != GRANTEXT && contextinfotype != GRANORGL)
      return (FALSE);
  switch (contextinfotype) {
    case GRANTEXT:
      /* ... fills in typetext ... */
    case GRANORGL:
      vstuffset = (typevstuffset) taskalloc (taskptr, sizeof (typeaddress));
      ((typeitemheader *)vstuffset)->next = NULL;
      ((typeitemheader *)vstuffset)->itemid = ADDRESSID;
      movetumbler (&context->totaloffset.dsas[WIDTH], &((typelink *)vstuffset)->address);
  }
```

**`context->totaloffset.dsas[WIDTH]`** is the granfilade sequential (I) address of the link's entry — which is identical to the link's ISA (the link's identity address in the granfilade hierarchy).

The returned item is a `typeaddress` / `typelink`:
```c
// xanadu.h:98-107
typedef struct structtypeaddress{
    struct structtypeaddress *next;
    typeitemid      itemid;   // = ADDRESSID
    typeisa address;           // the link's ISA tumbler
} typeaddress;
typedef typeaddress typelink;
```

---

### 3. What arrives on the wire?

**`putfe.c:270-275`** (`putretrievev`) → `putitemset` → `putitem`:

```c
// putfe.c:168-174
case ADDRESSID:
    puttumbler (outfile, &((typeaddress *)itemptr)->address);
    break;
```

And `puttumbler` (`putfe.c:104-117`) serializes a tumbler as:
```
-exp . mantissa[0] . mantissa[1] ... ~
```

So for a link with ISA = `1.1.0.2.0.1` the wire response to `retrievev` is:
```
<RETRIEVEV>~ 1~ 0.1.1.0.2.0.1~
```

That is: request code, count = 1 item, then the link ISA tumbler. **Nothing about endsets, nothing about the orgl internals.**

---

### 4. Are the three endsets stored as serialized tumbler sequences?

No. They are stored as **2D POOM crums** inside the link's private orgl (a separate POOM enfilade, not the document's).

When a link is created (`do1.c:195-221`, `docreatelink`):

```c
// do1.c:217-219
setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`setlinkvsas` (`do2.c:169-183`) assigns V-positions **within the link's own POOM**:

| Endset | V-position in link orgl | mantissa |
|--------|------------------------|---------|
| From   | `0.1.1~`               | [1,1,0,...] |
| To     | `0.2.1~`               | [2,1,0,...] |
| Three  | `0.3.1~`               | [3,1,0,...] |

`insertendsetsinorgl` (`do2.c:130-148`) calls `insertpm` for each endset (`orglinks.c:75-134`), which inserts a 2D POOM crum with:
- **I-coordinate**: the sporgl origin/width (I-span in the source doc's granfilade)
- **V-coordinate**: the V-position above (1.1, 2.1, or 3.1)
- **Crum info**: `type2dbottomcruminfo` containing `homedoc` = source document ISA

```c
// orglinks.c:101-130 (insertpm)
unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
movetumbler (&lstream, &crumorigin.dsas[I]);
movetumbler (&lwidth, &crumwidth.dsas[I]);
movetumbler (vsaptr, &crumorigin.dsas[V]);
...
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

The endsets are also registered in the global spanfilade (`insertendsetsinspanf` → `insertspanf` in `spanf1.c`) for link-following queries.

None of this is byte-serialized as tumbler sequences. It is live enfilade tree structure, loaded or paged from disk as needed.

---

### 5. How to access the endsets

To read what is at V=`0.1.1~` through `0.3.1~` **inside a link's orgl**, you use:

- **`followlink`** (`fns.c:114-127`) → `dofollowlink` (`do1.c:223-232`) → `link2sporglset` (`sporgl.c:67-95`) which calls `retrieverestricted` on the link's own orgl, restricted to the `whichend` V-position.

- **`retrieveendsets`** (`fns.c:350-362`) → `doretrieveendsets` → `retrieveendsetsfromspanf`, which queries the spanfilade.

Both paths consult the link's POOM and return reconstituted V-specs (document ISA + V-span set), never raw bytes.

---

### Summary

| What you do | What you get |
|-------------|-------------|
| `retrievev` with V in `[0.2.1~, 0.2.x~]` | `ADDRESSID` item = link ISA tumbler |
| `followlink(linkISA, whichend)` | V-spec: source doc ISA + V-span of the endset |
| `retrieveendsets(vspec)` | Three V-specs (from, to, three) via spanfilade |

The link orgl is a POOM enfilade in memory/disk. Its three endsets live at V-positions `0.1.1~`, `0.2.1~`, `0.3.1~` within it. They are stored as 2D crums (`type2dbottomcruminfo` with `homedoc`). They are not raw bytes, and they are not serialized tumbler sequences — they are a structured tree traversed by the enfilade retrieval engine.

---

## Question 18 [gregory]

> After INSERT shifts existing content to higher V-positions, does retrieving by the OLD V-addresses return the newly inserted content, or does it return empty/error for addresses that no longer map to the original content?

### Gregory's Answer

## KB Synthesis

After INSERT, retrieving by the **old V-addresses returns the newly inserted content** — not an error, and not the original content.

## Why

The INSERT postcondition [ST-INSERT] (Finding 0030) defines the V-to-I mapping after inserting length-n content at position p:

```
D'(v) =
  D(v)            if v < p          (before insertion point: unchanged)
  fresh_iaddr(v)  if p ≤ v < p+n   (the new content)
  D(v - n)        if v ≥ p+n        (old content shifted forward)
```

So position p **after** the insert maps to the newly inserted content. The content that previously occupied position p has been pushed to position p+n. There is no "invalid" or "stale" state — V-addresses always point to whatever currently occupies that position.

This is confirmed by the LIFO semantics [ST-INSERT] (Finding 0027): inserting "Second" at position 1.1 into a document containing "First" produces "SecondFirst". Retrieving at 1.1 now returns "S" (first byte of "Second"), not "F" (first byte of "First").

## The Key Asymmetry

V-addresses and I-addresses behave oppositely under INSERT:

| Layer | After INSERT at p |
|-------|------------------|
| **V-address** (position) | Mutable — position p now holds new content; old content shifted to p+n |
| **I-address** (identity) | Immutable — existing I-addresses are unchanged [INV-IADDR-IMMUTABILITY] |

[FC-INSERT-IADDR] (Finding 0030) makes this explicit: "INSERT does not modify the I-address of any pre-existing content... Within the target document, existing I-addresses are preserved — only V-addresses change."

## Consequence

If you want to retrieve the **original content** after an INSERT, you must use its new (shifted) V-address (p+n), not the old address (p). The old address reliably returns the inserted content. No error is produced in either case — V-addresses have no concept of "previously valid but now stale."

## Code Exploration

I now have everything I need: source code traces through the full call stack, the golden test, and multiple cross-referenced findings. Here is the complete answer.

---

## Answer: Old V-addresses return the newly inserted content — not empty, not error

After INSERT, retrieving by the old V-addresses returns the **newly inserted content** (for addresses inside the insertion range) or the **original content at its new, shifted V-position** (for addresses past the insertion). The original content that was at those old V-addresses is no longer there — it has been pushed forward.

---

## The Mechanism, Step by Step

### 1. `doinsert` → `docopy` → `insertpm` → `insertnd`

`doinsert` [`do1.c:117-122`]:
```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
);
```

`docopy` calls `insertpm` [`do1.c:60`]:
```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
```

`insertpm` calls `insertnd` with the POOM enfilade, which dispatches to the POOM branch [`insertnd.c:53-60`]:
```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);
    ...
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);
    ...
    break;
```

### 2. `makegappm` physically shifts existing V-positions rightward

This is the key function. It cuts the POOM at the insertion point and then walks all children, classifying each crum by `insertcutsectionnd` [`edit.c:207-233`]:

- **Case 0**: crum is entirely LEFT of insertion point → no change
- **Case 2**: crum straddles the cut boundary → no displacement change  
- **Case 1**: crum is entirely RIGHT of insertion point → **shift its V-displacement**

The shift [`insertnd.c:161-164`]:
```c
case 1:/*9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified (ptr);
    break;
```

Every POOM crum after the insertion point has `width` added to its V-dimension displacement (`cdsp.dsas[V]`). This is a direct in-tree mutation of V-addresses. The gap is now open.

### 3. `doinsertnd` inserts the new crum at the old V-position

After `makegappm` has cleared the space, `doinsertnd` → `insertmorend` → `insertcbcnd` places a new bottom crum at `origin` (the insertion V-address). This crum maps to the new content's I-addresses — freshly allocated from the granfilade.

### 4. RETRIEVE looks up the CURRENT, MUTATED POOM

`doretrievev` [`do2.c:338-346`]:
```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
    return
       specset2ispanset (taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```

`specset2ispanset` [`do2.c:34-38`] calls `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted`, all walking the POOM as it now exists. There is no version snapshotting — every retrieve consults the live tree. The POOM lookup returns whatever I-addresses are mapped at those V-coordinates today.

---

## The Resulting State After INSERT

For INSERT "XY" at V-address 1.3 into a document containing "ABCDE" at V=1.1..1.5:

| V-address | Before INSERT | After INSERT |
|-----------|--------------|-------------|
| 1.1       | A (I.1)      | A (I.1) — unchanged |
| 1.2       | B (I.2)      | B (I.2) — unchanged |
| 1.3       | C (I.3)      | **X (I.6) — newly inserted** |
| 1.4       | D (I.4)      | **Y (I.7) — newly inserted** |
| 1.5       | E (I.5)      | C (I.3) — original "C" shifted +2 |
| 1.6       | (empty)      | D (I.4) — original "D" shifted +2 |
| 1.7       | (empty)      | E (I.5) — original "E" shifted +2 |

Retrieving old V-address 1.3 now returns **"X"** — the newly inserted content. The original "C" has moved to 1.5.

---

## Confirmed by Golden Test

The golden test for this exact scenario [`golden/content/insert_vspace_mapping.json:74-83`]:

```json
{
  "op": "content_at_positions",
  "label": "after_middle_insert",
  "positions": {
    "1.1": "A",
    "1.2": "B",
    "1.3": "X",
    "1.4": "Y",
    "1.5": "C",
    "1.6": "D",
    "1.7": "E"
  }
}
```

The backend itself returns `"1.3": "X"` — confirming that retrieving by old V-address 1.3 (where "C" used to live) returns the newly inserted "X".

The `compare_versions` output [`golden/content/insert_vspace_mapping.json:86-113`] further confirms the I-address picture:

```json
"shared_spans": [
  { "version_before": {"start":"1.1","width":"0.2"},
    "after_insert":   {"start":"1.1","width":"0.2"} },   // "AB" — same position
  { "version_before": {"start":"1.3","width":"0.3"},
    "after_insert":   {"start":"1.5","width":"0.3"} }    // "CDE" — shifted +2
]
```

"CDE" (which was at V=1.3..1.5 in the version snapshot) now lives at V=1.5..1.7 in the post-insert document. The span 1.3..1.5 in the current document is occupied by the new content "XY" + "C" (first char of original post-insert content).

---

## Why Not Empty or Error?

There is no check in the retrieval path for "did this V-address used to mean something different?" The POOM is simply a 2D enfilade mapping V-addresses to I-addresses at the moment of query. `acceptablevsa` [`do2.c:110-113`] always returns `TRUE`:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No validation, no version tracking, no "tombstone" at old positions. The addresses are addresses in a live, mutable coordinate system.

---

## Summary

**V-addresses in udanax-green are mutable document coordinates, not stable references.**

- INSERT at V-position P shifts all content at V ≥ P rightward by the insertion width.
- The new content occupies the addresses P through P+width, taking over those coordinates.
- Old V-addresses in that range now point to the new content — **not** empty, **not** error.
- The original content is still accessible, but at its new higher V-addresses.
- I-addresses (permascroll locations) are the stable, immutable layer. V-addresses are not.

---

## Question 19 [gregory]

> Does `incontextlistnd` affect retrieval ordering when a document contains self-transclusion (the same I-addresses at multiple V-positions), and if so, are results always returned in ascending V-address order regardless of POOM tree shape?

### Gregory's Answer

## KB Synthesis

Yes to both parts of the question.

## `incontextlistnd` Sorting of Self-Transclusion Results

**All V-positions are accumulated.** When `ispan2vspanset` queries a POOM containing self-transclusion — say, I-address `i_B` mapped to V-positions 1.2, 1.4, and 1.5 — `findcbcinarea2d()` traverses all siblings at each B-tree level and recursively descends into every qualifying subtree. For each leaf node found, it calls `incontextlistnd()`. Because the POOM is a multimap `[SS-POOM-MULTIMAP]`, all three matching crums are discovered and passed to `incontextlistnd` regardless of sibling ordering in the tree.

**`incontextlistnd` imposes ascending V-order.** The function performs insertion-sort: each newly discovered context is inserted at the position that maintains ascending order of `totaloffset.dsas[V]` (the left V-boundary). It has four cases — prepend if new context precedes head, insert between two adjacent contexts, append to end, or first insertion — and uses `intervalcmp()` for comparison `[INV-RETRIEVAL-V-SORTED]`. The result is that `ispan2vspanset(poom, i_B)` returns:

```
Context(V=1.2) → Context(V=1.4) → Context(V=1.5)
```

regardless of the order in which the B-tree traversal discovered them.

**Tree shape is irrelevant.** Splits, rebalances, and the diagonal-sort merge ordering (Finding 0071) can produce tree structures where sibling order does not match V-address order. This does not affect retrieval output because `incontextlistnd` re-establishes V-ordering during accumulation `[INV-RETRIEVAL-TREE-INDEPENDENCE]`. The sorted-result postcondition holds for any valid tree storing the same `(V-position, I-address)` entries.

**Contrast with GRAN.** For 1D GRAN enfilades, `oncontextlistseq()` is used instead — it appends in tree traversal order. This is safe because GRAN tree structure preserves sequential order by design. POOM trees make no such guarantee (due to 2D diagonal rebalancing), which is precisely why `incontextlistnd` with its explicit insertion-sort is required `[SS-CONTEXT-LIST]`.

**Self-transclusion confirmed working.** `[EC-SELF-TRANSCLUSION]` documents N-ary self-transclusion (tested up to 3 copies) where all pairwise `compare_versions` calls correctly report shared content — which depends on all V-positions being returned and correctly sorted by the retrieval path.

**Summary:** `incontextlistnd` is the mechanism that makes self-transclusion retrieval correct. It ensures that a POOM query by I-address always yields its complete set of matching V-positions in ascending V-address order, independent of how splits, rebalances, or insertion order shaped the B-tree.

## Code Exploration

I now have all the source I need. Let me compile a thorough traced answer.

---

## Answer: `incontextlistnd`, Self-Transclusion, and V-Address Ordering

### 1. Where `incontextlistnd` Is Called

The only call site that matters for retrieval is in `findcbcinarea2d` [retrie.c:263]:

```c
} else {
    context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
    incontextlistnd (headptr, context, index1);   // retrie.c:263
}
```

This is the 2-D POOM enfilade traversal used by `retrieveinarea` [retrie.c:97], which is called from `retrieverestricted` [retrie.c:83], which is called from `span2spanset` [orglinks.c:435], which is called from `permute` [orglinks.c:415], the core of both `vspanset2ispanset` and `ispan2vspanset` [orglinks.c:393–402].

The full call chain for a standard document retrieve is:

```
doretrievev [do1.c:338]
  → specset2ispanset [do2.c:14]
    → vspanset2ispanset [orglinks.c:389]
      → permute(taskptr, orgl, vspanset, V, ispansetptr, I) [orglinks.c:404]
        → span2spanset(..., restrictionindex=V, targindex=I) [orglinks.c:425]
          → retrieverestricted(orgl, restrictionspan, V, NULL, I, NULL) [orglinks.c:435]
            → retrieveinarea(..., index1=V, index2=I) [retrie.c:87]
              → findcbcinarea2d(..., index1=V, index2=I) [retrie.c:97]
                → incontextlistnd(headptr, context, index1=V)  [retrie.c:263]
```

The third argument, `index1`, is the **restriction dimension** — V when converting V→I (and I when going I→V). This is the dimension that `incontextlistnd` sorts on.

---

### 2. What `incontextlistnd` Does

```c
// context.c:75–111
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
  typecontext *clist, *nextc;
  typedsp grasp;

  prologuecontextnd (c, &grasp, (typedsp*)NULL);  // grasp = c->totaloffset
  c->nextcontext = NULL;
  clist = *clistptr;

  if (!clist) { *clistptr = c; return(0); }         // first insertion

  if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
    c->nextcontext = clist; *clistptr = c; return(0);  // before head
  } else {
    for (; nextc = clist->nextcontext; clist = nextc) {
      if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
       && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
        c->nextcontext = nextc; clist->nextcontext = c; return(0);  // in middle
      }
    }
  }
  c->nextcontext = NULL; clist->nextcontext = c;  // append at end
}
```

This is a **linked-list insertion sort**. Every time a qualifying leaf node is found during the POOM tree walk, its context is inserted into the sorted list at the correct position in the `index` dimension (V, during V→I retrieval).

The comparison function is `whereoncontext` [context.c:124–149], which for a POOM context uses:

```c
case POOM:
    movetumbler (&ptr->totaloffset.dsas[index], &left);   // context's start address
    tumbleradd (&left, &ptr->contextwid.dsas[index], &right);
    break;
return (intervalcmp (&left, &right, address));
```

and `intervalcmp` returns one of the five positional constants [common.h:86–90]:

```c
#define TOMYLEFT        -2
#define ONMYLEFTBORDER  -1
#define THRUME           0
#define ONMYRIGHTBORDER  1
#define TOMYRIGHT        2
```

The probe address is `grasp.dsas[index]` — the **start (left border)** of the new context in the sort dimension. Conditions:

| Condition | Meaning | Action |
|-----------|---------|--------|
| `< THRUME` at head | new_start ≤ head.left | insert before head |
| `> ONMYLEFTBORDER` at clist AND `< ONMYLEFTBORDER` at nextc | clist.left ≤ new_start AND new_start < nextc.left (strict) | insert between |
| neither matched | new_start ≥ tail.right | append at tail |

The sort is ascending by the left boundary of each context in the `index` dimension.

---

### 3. Self-Transclusion: What It Looks Like in the POOM

Self-transclusion in udanax-green means the same I-address range appears at multiple V-positions. In the POOM (Permutation Matrix) enfilade, each bottom crum (`type2dcbc`) has:
- `cdsp.dsas[I]` — I-space start
- `cdsp.dsas[V]` — V-space start  
- `cwid.dsas[I]` — width in I-space
- `cwid.dsas[V]` — width in V-space

A self-transclusion document might have:
- Crum A: V=[1,5), I=[100,104)  — original insertion
- Crum B: V=[10,14), I=[100,104) — copy via `docopy`/`insertpm`

(Both crums point at the same permascroll I-addresses.)

`docopy` [do1.c:45–65] is the operation that creates this structure: it calls `insertpm` [orglinks.c:75–134] which inserts a new POOM bottom crum with the caller's target V-address (`vsaptr`) paired to the source's I-addresses. After the copy, two distinct POOM crums cover the same I-range at different V-positions.

---

### 4. Retrieval Ordering with Self-Transclusion

When we retrieve by V-span (e.g., V=[1,5)):

`findcbcinarea2d` [retrie.c:229–268] walks the POOM tree depth-first, left-to-right at each sibling level, using `crumqualifies2d` [retrie.c:270–305] to prune nodes. Each qualifying leaf becomes a context and is passed to `incontextlistnd`.

**Tree-shape independence:** The POOM tree's internal structure reflects the history of `insertnd`/`adopt`/`disown` operations [genf.c]. Insertions, deletions, level pushes, and rebalancing via `recombine` can leave the POOM tree in shapes that don't correspond to simple V-sorted sibling order. Despite this, `incontextlistnd` performs insertion sort on each discovered context. Regardless of the order in which the tree walk encounters crums, the output list is always sorted by V-start.

**Self-transclusion case:** If V=[1,15) is queried (covering both Crum A at V=[1,5) and Crum B at V=[10,14)):
- `crumqualifies2d` passes both crums (both overlap [1,15) on V; span2 is zero so no I restriction [retrie.c:292–300])
- Crum A yields context_A with `totaloffset.dsas[V] = 1`
- Crum B yields context_B with `totaloffset.dsas[V] = 10`
- `incontextlistnd(..., V)` inserts them: context_A first, context_B second (ascending V-start)

This result list is then consumed by `span2spanset` [orglinks.c:439–445]:

```c
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`context2span` [context.c:176–212] projects each POOM context down to its I-coordinate, producing an I-span. Since the iteration is over the V-sorted list, the I-spans are yielded in **ascending V-address order of their source V-positions** — i.e., I-span for V=1 before I-span for V=10. Because both contexts have the same I-start (self-transclusion), the resulting I-spans are identical, but they are appended in sequence through `onitemlist` [orglinks.c:464–537], which simply appends to the tail of the target list. This means the output ispanset contains duplicate I-spans in V-ascending order.

---

### 5. One Caveat: Equal-V-Start Tie-Breaking

The "in middle" condition uses `< ONMYLEFTBORDER` (strictly less than −1, i.e., only `TOMYLEFT = −2`) for the nextc test. This means: if new_start **equals** nextc's left border (result is `ONMYLEFTBORDER = −1`), the middle insertion doesn't fire, and the loop continues. If no later slot is found, the new context appends to the end. So for two crums with the identical V-start (possible in degenerate or corrupt trees, but not in a normal self-transclusion where copy and original have different V-addresses), the tie is broken by **tree walk order** (whatever `getrightbro` returns first), not by any deterministic secondary key. This is the one case where tree shape affects result order.

For standard self-transclusion (distinct V-positions per I-address), this tie case does not arise.

---

### 6. Contrast with `oncontextlistseq`

For comparison: `findcbcinspanseq` [retrie.c:307–329], used for granfilade (1D, content) retrieval, calls `oncontextlistseq` [context.c:113–123] instead:

```c
int oncontextlistseq(typecontext **clistptr, typecontext *c)
{
  c->nextcontext = NULL;
  if (!*clistptr) {
    *clistptr = c; c->lastcontext = c;
  } else {
    (*clistptr)->lastcontext->nextcontext = c;
    (*clistptr)->lastcontext = c;
  }
}
```

This is a **tail-append only** — no sorting. The ordering for granfilade retrieval is whatever order the tree walk visits bottom crums (which, for a sequential granfilade, is left-to-right = width-ascending, so the result is naturally in order). `incontextlistnd` exists specifically for the 2D POOM case, where tree walk order is not guaranteed to match the desired output dimension order.

---

### Summary

**Yes, `incontextlistnd` directly determines retrieval output ordering for POOM-based retrievals.** Specifically:

1. It is called at [retrie.c:263] inside `findcbcinarea2d`, for every qualifying POOM leaf node found during the tree walk.
2. It performs an insertion sort keyed on the **restriction dimension's start address** (`index1`), which is V for V→I retrieval [context.c:90, 98–99].
3. The sort is **tree-shape-independent**: no matter what order the POOM tree walk visits leaf crums (which depends on insertion history, rebalancing, and disk layout), the output context list is always in ascending V-address order.
4. For self-transclusion specifically — same I-addresses at multiple V-positions — each V-copy produces its own context, and these are sorted by V-start. The downstream `span2spanset` loop consumes them in that V-ascending order, producing I-spans in the order their V-copies appear in the document.
5. The only exception: crums with identical V-starts are not deterministically ordered relative to each other (a subtle asymmetry in the "< ONMYLEFTBORDER" test in the middle-insertion clause [context.c:99]). For ordinary self-transclusion with distinct V-positions, this does not apply.

---

## Question 20 [gregory]

> When retrieving from a document where DELETE has produced negative V-position tumblers, does the retrieval function accept a negative V-address as a query parameter and return the displaced content, or are negative V-positions unreachable through the normal retrieval interface?

### Gregory's Answer

## KB Synthesis

## Negative V-Positions: Unreachable Through Normal Retrieval

Negative V-position entries created by DELETE are unreachable through the normal retrieval interface. The unreachability is a structural consequence of the tumbler total order and B-tree traversal, not an explicit bounds check.

**Why the traversal cannot reach them**

The retrieval path navigates the enfilade using `whereoncrum` [SS-WHEREONCRUM], which classifies a query address relative to each crum's interval `[grasp, reach)` with five outcomes: `TOMYLEFT`, `ONMYLEFTBORDER`, `THRUME`, `ONMYRIGHTBORDER`, `TOMYRIGHT`. The tumbler total order places all negative tumblers strictly less than zero and all positive values [SS-TUMBLER, Finding 0053]:

```
tumblercmp(-0.8, 0.0)  → LESS
tumblercmp(-0.8, 1.1)  → LESS
```

Any retrieval query using a non-negative V-address (the only addresses in valid V-space) will classify a crum whose grasp is negative as `TOMYLEFT`. The B-tree traversal never descends into a subtree that lies entirely to the left of the query address. Since negative-V crums occupy positions before all valid V-addresses, tree traversal from any well-formed specset simply passes them by.

**The FOLLOWLINK evidence**

[ST-DELETE, Finding 0053] documents this directly: after DELETE shifts a link endset's V-position to a negative value, `FOLLOWLINK` returns **empty endsets**. The link POOM entry still physically exists in the tree, but the I-to-V conversion path (`linksporglset2specset` → `span2spanset` → `retrieverestricted`) finds no matching crum for the positive-valued I-address lookup and silently drops it [INV-ITOV-FILTERING]. The result is empty, not an error.

**The KB's stated conclusion**

[INV-POOM-BIJECTIVITY] characterizes these entries explicitly:

> "A negative V-position is in the domain of the stored POOM map but does not correspond to any valid V-address in the document's V-stream (which is defined over non-negative tumblers only). The entry occupies tree space and has a valid I-address target, but its V-address key is outside the legal V-space... the entries are simply unreachable by any V-space query."

**Could a client deliberately query with a negative V-address?**

The KB does not document this path. Negative tumblers are syntactically valid (sign=1, positive magnitude) [SS-TUMBLER, Finding 0031], so the machinery would not crash on receipt. If a client constructed and sent a negative V-address, the `whereoncrum` total-order comparison would handle it correctly — the traversal would need to descend left rather than right. Whether the enfilade tree structure would successfully route to such an entry depends on how the tree is balanced, and this scenario is not addressed in the KB.

**Practical consequence**

From the spec's perspective, these entries constitute leaked dead state [EC-DEEPLY-ORPHANED-LINK]: they cannot be reclaimed by `DELETEVSPAN` (which requires a non-negative V-span argument), they do not appear in `retrieve_contents` results, and links whose POOM entries have drifted negative behave identically to orphaned links whose endpoint content has been deleted. The precondition in [INV-POOM-BIJECTIVITY] should therefore be weakened from "bijection over all V-addresses" to "bijection restricted to non-negative V-addresses."

## Code Exploration

I now have everything I need to answer the question thoroughly. Let me synthesize the code evidence.

---

## Answer: Negative V-Positions After DELETE — What the Code Actually Does

### 1. The Tumbler Data Type Has a Sign Bit

From `backend/common.h:59-65`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;  /* 1 if negative, otherwise 0 */
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

Negative tumblers are representable in memory. `tumblercmp` at `backend/tumble.c:72-85` handles them correctly: a negative tumbler is always `LESS` than zero, and two negative tumblers compare by reverse absolute magnitude.

---

### 2. What DELETE Actually Does to V-Positions

`dodeletevspan` at `backend/do1.c:158-167` delegates to `deletevspanpm` at `backend/orglinks.c:145-152`, which calls `deletend` at `backend/edit.c:31-76`.

The core of `deletend` is:

```c
// edit.c:56-65
case 1:
    disown((typecuc*)ptr);
    subtreefree((typecuc*)ptr);
    break;
case 2:
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

- **Case 1**: Crums entirely *inside* the deleted span are removed.
- **Case 2**: Crums entirely *after* the deleted span have their relative displacement (`cdsp.dsas[V]`) decremented by `width`.

**Can the relative displacement go negative?** Yes. For a child crum of `father`:
- Case 2 requires its **absolute** V-position `≥ origin + width`
- Absolute V = `fgrasp.dsas[V] + child.cdsp.dsas[V]`
- After adjustment: `child.cdsp.dsas[V] -= width`
- The new value is: `child.cdsp - width ≥ (origin + width - fgrasp) - width = origin - fgrasp`

If `fgrasp > origin`, then `origin - fgrasp < 0`, so **`cdsp` can become negative**.

Concrete example: delete V=[5, 8] (origin=5, width=3), father's grasp is at V=7, child's cdsp=1 (absolute V=8 = edge of deletion, case 2). After: `cdsp = 1 - 3 = -2`. New absolute V = `7 + (-2) = 5`. The internal relative displacement goes negative; the absolute V-position does not.

---

### 3. Absolute V-Positions Remain Non-Negative After Delete

For any case-2 crum, the **absolute** V-position after deletion is:

```
new_absolute = fgrasp + (old_cdsp - width) = old_absolute - width
```

Since case-2 requires `old_absolute ≥ origin + width`, we get:

```
new_absolute ≥ origin + width - width = origin ≥ 0
```

So **absolute V-positions (as seen externally) always remain ≥ 0**. The negative values produced by `tumblersub` at `edit.c:63` are *internal relative displacements inside the tree*, not observable V-addresses.

---

### 4. The Serialization Layer Blocks Negative Tumblers

`backend/tumbleari.c:77-78`:
```c
INT tumblerfixedtoptr(tumbler *ptr, humber p)
{
    if(ptr->sign)
        gerror("negative tumbler in tumblerfixedtoptr\n");
```

This is the function that encodes a tumbler for the wire protocol. It calls `gerror` (which aborts) if the tumbler's sign bit is set. The backend **cannot send a negative tumbler to the client** under any circumstances.

---

### 5. The Retrieval Interface Has No Guard Against Negative V-Addresses

`acceptablevsa` at `backend/do2.c:110-113`:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

Unconditionally returns TRUE. No sign check.

The retrieval path — `fns.c:175` `retrievev()` → `do1.c:338` `doretrievev()` → `specset2ispanset()` → `vspanset2ispanset()` → `permute()` → `span2spanset()` → `retrieverestricted()` → `retrieveinarea()` → `findcbcinarea2d()` → `crumqualifies2d()` — never checks whether the query V-span start is negative.

In `crumqualifies2d` at `backend/retrie.c:286-290`:
```c
startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return (FALSE);
```

`THRUME = 0`. If `span1start` is negative, `whereoncrum` returns `TOMYLEFT = -2` for all crums (negative address is left of any positive content). The condition `-2 > 0` is false, so this check **always passes** for a negative query start. A negative V-address in the query start is effectively treated as "before all content," and the span end determines what is found.

The only guard in the retrieval path against malformed queries is at `backend/do2.c:28-33`, which checks that the **document ISA** is not zero — not the V-span value.

---

### 6. Insertion Is Guarded Against Negative V-Addresses

By contrast, `insertpm` at `backend/orglinks.c:93-98` does check:
```c
if (tumblercmp(vsaptr, &zero) == LESS)
#ifndef DISTRIBUTION
    gerror("insertpm called with negative vsa.\n");
```

This ensures content is never placed at a negative V-address to begin with. Combined with the serialization guard in `tumblerfixedtoptr`, the client can never learn of a negative V-address through normal API use.

---

### Conclusion

**The premise of the question does not hold for external V-positions.**

DELETE does not produce negative V-position tumblers in any externally observable sense:

1. **Internal tree state** (`cdsp.dsas[V]` at `edit.c:63`): These relative displacements *can* go negative after `tumblersub`, but they are implementation internals — the cumulative sum walking root-to-leaf always yields a non-negative absolute position.

2. **External V-addresses**: All surviving content after DELETE remains at positive (non-negative) V-addresses. Displaced content is at `original_position - width`, which is `≥ origin ≥ 0`.

3. **Retrieval of displaced content**: No negative V-address is needed. Displaced content has simply moved to a *lower* positive address and is reachable by querying that lower address normally.

4. **If a negative V-address were submitted as a query start**: The retrieval engine at `retrie.c:270-305` would process it correctly (since `tumblercmp` handles sign), treating it as "before all content." Content within the positive part of the query span would still be returned. But this scenario cannot arise through normal client usage because:
   - The backend never sends negative V-addresses to the client [`tumbleari.c:77-78`]
   - `insertpm` never places content at negative V-addresses [`orglinks.c:93-98`]

Negative V-positions are unreachable through the normal retrieval interface for the simple reason that they don't exist at the external level — not because the retrieval engine would reject them.
